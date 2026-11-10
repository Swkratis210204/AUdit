"""Exact permutation null for the attribution rates: how much of the AU attribution rate of a characteristic (Table 2) and of the gap between
non-demographic and demographic characteristics (Table 3) is chance?

A characteristic with more groups gives smaller groups per text, and a small group passes the unimodality test more easily. For every characteristic the null keeps
everything but the link between a rating and the group of its rater:

* the texts are the polarized texts with at least four ratings (``attribution_bootstrap.attribution_table``);
* for every such text **every** assignment of the text's raters to the **retained groups** of the characteristic (the groups left after the removal of thin groups,
  Appendix D.2) with the observed group sizes is considered, once each, and by default **the observed assignment is left out**. A text whose groups have sizes
  n1, n2, ... (N ratings in all) has N! / (n1! n2! ...) assignments: 2 + 2 ratings give 6, so 5 besides the observed one. Nothing is drawn at random;
* the AU test is run on every assignment with the rules of ``Unimodality.analyse_text`` (a group needs at least two ratings, at least two such groups, every such
  group has DFU = 0; the text is polarized overall by construction). The removal rule is not run again. The group sizes do not change, so every assignment of a
  testable text is testable;
* the chance probability of a (text, characteristic) pair is the share of those assignments in which the text is attributed. The assignments are not listed one by
  one: the test only sees the histogram of every group, so every distinct split of the rating values among the groups is tested once and counted as many times as
  there are assignments of raters that give it (a product of binomial coefficients). The result is the same as listing every assignment; splits whose share is
  below 1e-30 are skipped (only texts with hundreds of ratings have such splits; their total is far below the precision of the result);
* the texts are independent, so the number of attributed texts of a characteristic under the null is a sum of independent yes / no results with these
  probabilities (a Poisson-binomial distribution), computed exactly: the chance rate is its mean, the range its 2.5 and 97.5 percentiles, and p the probability of
  at least the observed number.

Checks (the run stops when one fails): the vectorised AU test on the observed assignment gives the AU texts of the results; for texts with at most 5,000
assignments the weighted enumeration equals a brute-force listing of every assignment (up to ``BRUTE_CHECKS`` distinct cases per characteristic); the number of
attributed assignments is a whole number, and at least one when the observed text is attributed; the observed rates and Table 3 are reproduced.

Nothing here asks a model for anything and nothing changes the AU results: it reads them.
"""
from __future__ import annotations

import itertools
import math
import time
import warnings
from functools import lru_cache
from pathlib import Path
from typing import Dict, Optional, Sequence

import numpy as np
import pandas as pd
from scipy.special import gammaln
from scipy.stats import ConstantInputWarning, spearmanr

from .attribution_bootstrap import COLUMNS, DEMOGRAPHIC, attribution_gap, attribution_table
from .names import DATASET_LABEL, ordered_datasets
from .pipeline import DatasetResult

__all__ = ["compute_null", "save_null"]

LOG_PRUNE = math.log(1e-30)          # a split of the ratings with a smaller share of the assignments is skipped
BRUTE_CHECKS = 30                    # distinct (group sizes, ratings) cases per characteristic checked against a brute-force listing
BRUTE_MAX = 5_000                    # ... when they have at most this many assignments


def _unimodal(counts: np.ndarray) -> np.ndarray:
    """DFU == 0 for histograms ``counts`` (..., V), as ``ndfu.dfu``: no rise after the first maximum and no fall before it (equal counts are not a rise or a fall)."""
    diff = np.diff(counts, axis=-1)
    peak = np.argmax(counts, axis=-1)[..., None]
    steps = np.arange(counts.shape[-1] - 1)
    rise_after = ((steps >= peak) & (diff > 0)).any(axis=-1)
    fall_before = ((steps < peak) & (diff < 0)).any(axis=-1)
    return ~(rise_after | fall_before)


def _hist(values: np.ndarray, group: np.ndarray, n_groups: int, scale: int) -> np.ndarray:
    """T x G x V: the histogram of every group of every text."""
    member = group[:, :, None] == np.arange(n_groups)[None, None, :]
    onehot = values[:, :, None] == np.arange(1, scale + 1)[None, None, :]
    return np.einsum("tmg,tmv->tgv", member.astype(np.float32), onehot.astype(np.float32)).round().astype(np.int64)


def _au(values: np.ndarray, group: np.ndarray, n_groups: int, scale: int, min_ratings: int, min_groups: int) -> tuple:
    """For every text: (testable, AU) of the assignment given by ``group`` (the local group index of every slot, -1 for padding)."""
    counts = _hist(values, group, n_groups, scale)
    eligible = counts.sum(axis=2) >= min_ratings
    testable = eligible.sum(axis=1) >= min_groups
    return testable, testable & (~eligible | _unimodal(counts)).all(axis=1)                        # the text is polarized overall by construction


def _arrays(result: DatasetResult, dimension: str, items: pd.Index) -> dict:
    """The ratings of the retained groups of ``dimension`` of the texts ``items``, one row per text: ratings, the local group index of every slot (sorted), padding."""
    pr = result.pruned[dimension]
    ratings = result.clean[["item_id", "rating", dimension]]
    ratings = ratings[ratings["item_id"].isin(items) & ~ratings[dimension].isin(pr.removed)].copy()
    codes = {g: i for i, g in enumerate(sorted(pr.counts, key=str))}
    ratings["group"] = ratings[dimension].map(codes)
    assert ratings["group"].notna().all(), f"{result.spec.name}/{dimension}: a rating of an unknown group"
    ratings = ratings.sort_values(["item_id", "group"], kind="stable")
    ratings["slot"] = ratings.groupby("item_id").cumcount()
    row = pd.Series(np.arange(len(items)), index=items)
    r, m = row.loc[ratings["item_id"]].to_numpy(), ratings["slot"].to_numpy()
    values = np.zeros((len(items), m.max() + 1), dtype=np.int16)
    group = np.full(values.shape, -1, dtype=np.int16)
    scores = ratings["rating"].to_numpy()
    assert np.array_equal(scores, scores.astype(int)), "the ratings are not whole numbers"
    values[r, m], group[r, m] = scores.astype(int), ratings["group"].to_numpy()
    return {"values": values, "group": group, "n_groups": len(codes)}


def _observed_check(result: DatasetResult, dimension: str, items: pd.Index, arrays: dict) -> np.ndarray:
    """The vectorised test on the observed assignment must give the AU texts of the results; returns the observed AU of every text."""
    testable, au = _au(arrays["values"], arrays["group"], arrays["n_groups"], result.spec.scale_max, result.tool.min_ratings, result.tool.min_groups)
    observed = result.pruned[dimension].result.set_index("item_id")["au"].reindex(items).to_numpy(dtype=bool)
    assert testable.all(), f"{result.spec.name}/{dimension}: a testable text is not testable in the arrays"
    assert np.array_equal(au, observed), f"{result.spec.name}/{dimension}: the vectorised AU test differs from the AU results"
    return observed


# --- the exact enumeration ---------------------------------------------------------------------------------------------------------------------
def _ok(h: np.ndarray, size: int, min_ratings: int) -> np.ndarray:
    """A group passes when it is too small to be tested or its histogram is unimodal."""
    return np.ones(len(h), dtype=bool) if size < min_ratings else _unimodal(h)


def _compositions(n: int, rem: np.ndarray) -> np.ndarray:
    """Every histogram h with sum n and 0 <= h <= rem (K x V)."""
    h = np.zeros((1, 0), dtype=np.int64)
    for v in range(len(rem) - 1):
        k = np.arange(rem[v] + 1)
        h = np.column_stack([np.repeat(h, len(k), axis=0), np.tile(k, len(h))])
        h = h[h.sum(axis=1) <= n]
    last = n - h.sum(axis=1)
    keep = last <= rem[-1]
    return np.column_stack([h[keep], last[keep]])


def _log_comb(a, b):
    return gammaln(np.asarray(a) + 1.0) - gammaln(np.asarray(b) + 1.0) - gammaln(np.asarray(a) - np.asarray(b) + 1.0)


@lru_cache(maxsize=None)
def _p_attributed(sizes: tuple, counts: tuple, min_ratings: int) -> float:
    """The share of the assignments of the ratings ``counts`` (a histogram) to groups of ``sizes`` (ascending) in which every group with at least
    ``min_ratings`` ratings is unimodal. The first group takes every possible split h of the ratings, with the share prod_v C(c_v, h_v) / C(N, n) of the
    assignments; the rest is the same question for the remaining ratings and groups (the last group takes what is left)."""
    rem = np.asarray(counts, dtype=np.int64)
    n, rest = sizes[0], sizes[1:]
    if not rest:
        return float(_ok(rem[None], n, min_ratings)[0])
    h = _compositions(n, rem)
    log_share = _log_comb(rem, h).sum(axis=1) - _log_comb(rem.sum(), n)
    keep = _ok(h, n, min_ratings) & (log_share > LOG_PRUNE)
    h, share = h[keep], np.exp(log_share[keep])
    if len(rest) == 1:
        return float(share[_ok(rem - h, rest[0], min_ratings)].sum())
    return float(sum(s * _p_attributed(rest, tuple(int(x) for x in rem - hh), min_ratings) for s, hh in zip(share, h)))


@lru_cache(maxsize=None)
def _assignments(sizes: tuple) -> int:
    """N! / (n1! n2! ...): the number of assignments of the raters to groups of these sizes."""
    total = math.factorial(sum(sizes))
    for n in sizes:
        total //= math.factorial(n)
    return total


def _brute(values: Sequence[int], sizes: tuple, min_ratings: int, scale: int) -> tuple:
    """(attributed, assignments) by listing every assignment of the raters (positions of ``values``) to groups of ``sizes``: only for small texts, as a check."""
    hit = total = 0

    def deal(left: tuple, g: int, groups: list):
        nonlocal hit, total
        if g == len(sizes) - 1:
            total += 1
            hit += all(len(members) < min_ratings or bool(_unimodal(np.bincount([values[i] for i in members], minlength=scale + 1)[1:][None])[0])
                       for members in groups + [left])
            return
        for chosen in itertools.combinations(left, sizes[g]):
            deal(tuple(i for i in left if i not in chosen), g + 1, groups + [chosen])

    deal(tuple(range(len(values))), 0, [])
    return hit, total


def _null_one(result: DatasetResult, dimension: str, items: pd.Index, exclude_observed: bool) -> dict:
    arrays = _arrays(result, dimension, items)
    observed = _observed_check(result, dimension, items, arrays)
    scale, min_ratings = result.spec.scale_max, result.tool.min_ratings
    counts = _hist(arrays["values"], arrays["group"], arrays["n_groups"], scale)
    sizes, ratings = counts.sum(axis=2), counts.sum(axis=1)
    p_all, chance, log_assign = np.empty(len(items)), np.empty(len(items)), np.empty(len(items))
    checked = {}
    for i in range(len(items)):
        sz = tuple(sorted(int(s) for s in sizes[i] if s > 0))
        cnt = tuple(int(c) for c in ratings[i])
        p = _p_attributed(sz, cnt, min_ratings)
        total = _assignments(sz)
        p_all[i], log_assign[i] = p, math.log10(total)
        if observed[i]:
            assert p > 0, f"{result.spec.name}/{dimension}/{items[i]}: the observed text is attributed but no assignment is"
        if total <= 10**9:                                          # whole numbers: the attributed assignments are counted exactly
            attributed = p * total
            assert abs(attributed - round(attributed)) < 1e-3, f"{result.spec.name}/{dimension}/{items[i]}: {attributed} attributed assignments is not a whole number"
            attributed = round(attributed)
            chance[i] = (attributed - observed[i]) / (total - 1) if exclude_observed else attributed / total
        else:                                                       # (p T - observed) / (T - 1), written so that T need not fit in a float
            chance[i] = p + (p - observed[i]) * math.exp(-math.log(total - 1)) if exclude_observed else p
        if total <= BRUTE_MAX and len(checked) < BRUTE_CHECKS and (sz, cnt) not in checked:
            row = arrays["group"][i] >= 0
            vals, grp = arrays["values"][i][row], arrays["group"][i][row]
            order = sorted(np.unique(grp), key=lambda g: (int((grp == g).sum()), int(g)))           # the groups in the order of ``sz``
            vals = [int(v) for g in order for v in vals[grp == g]]
            hit, n = _brute(vals, sz, min_ratings, scale)
            assert n == total and abs(hit / n - p) < 1e-9, f"{result.spec.name}/{dimension}/{items[i]}: enumeration {p} against brute force {hit}/{n}"
            checked[(sz, cnt)] = True
    return {"chance_probability": chance, "chance_probability_with_observed": p_all, "assignments_log10": log_assign, "observed": observed, "brute_checked": len(checked)}


def _poisson_binomial(q: np.ndarray) -> np.ndarray:
    """The distribution of the number of successes of independent yes / no results with probabilities ``q`` (index = number of successes)."""
    q = np.asarray(q, dtype=float)
    ones = int((q >= 1).sum())
    q = q[(q > 0) & (q < 1)]
    pmf = np.zeros(len(q) + 1)
    pmf[0] = 1.0
    for k, p in enumerate(q, start=1):
        pmf[1:k + 1] = pmf[1:k + 1] * (1 - p) + pmf[0:k] * p
        pmf[0] *= 1 - p
    return np.concatenate([np.zeros(ones), pmf])


# --- the tables --------------------------------------------------------------------------------------------------------------------------------
def compute_null(results: Dict[str, DatasetResult], reps: int = 10_000, seed: int = 42, log=print, demographic: Sequence[str] = DEMOGRAPHIC,
                 min_text_ratings: Optional[int] = None, exclude_observed: bool = True) -> Dict[str, pd.DataFrame]:
    """``per_characteristic``, ``gap``, ``per_pair``, ``correlation`` and ``checks``. Reproduces the observed rates and gap of ``attribution_gap`` first and stops when
    they differ. The null is exact (every assignment of the raters to the groups, once each); ``exclude_observed`` (default True) leaves the observed assignment
    out. ``reps`` and ``seed`` are those of the bootstrap of the gap (as Table 3); nothing else is random."""
    reference_gap = attribution_gap(results, reps=reps, seed=seed, demographic=demographic, min_text_ratings=min_text_ratings)
    label = "exact, observed excluded" if exclude_observed else "exact, observed included"
    per_char, pairs, gap_rows, checks = [], [], [], []
    for dataset in ordered_datasets(results):
        result = results[dataset]
        table = attribution_table(result, demographic, min_text_ratings)
        chance = {"D": np.zeros(len(table)), "N": np.zeros(len(table))}
        brute = 0
        for dimension in result.pruned:
            rows = result.pruned[dimension].result.set_index("item_id")
            testable = (rows["polarised"] & (rows["kept_groups"].map(len) >= result.tool.min_groups)).reindex(table.index, fill_value=False)
            items = table.index[testable.to_numpy()]
            kind = "D" if dimension in demographic else "N"
            started = time.perf_counter()
            null = _null_one(result, dimension, items, exclude_observed)
            brute += null["brute_checked"]
            chance[kind][table.index.get_indexer(items)] += null["chance_probability"]
            n, observed = len(items), int(null["observed"].sum())
            pmf = _poisson_binomial(null["chance_probability"])
            cdf = np.cumsum(pmf)
            mean = 100 * float(null["chance_probability"].sum()) / n
            low, high = (100 * int(np.searchsorted(cdf, x)) / n for x in (0.025, 0.975))
            p = float(min(1.0, pmf[observed:].sum()))
            log(f"{dataset}/{dimension}: {n} testable texts, up to 10^{null['assignments_log10'].max():.0f} assignments per text, {time.perf_counter() - started:.1f} s")
            per_char.append({"dataset": dataset, "characteristic": dimension, "type": kind, "n_groups": len(result.pruned[dimension].counts), "testable": n,
                             "observed_attributed": observed, "observed_pct": round(100 * observed / n, 2), "chance_mean_pct": round(mean, 2),
                             "chance_ci_low_pct": round(low, 2), "chance_ci_high_pct": round(high, 2), "excess_pct": round(100 * observed / n - mean, 2),
                             "ratio": round(100 * observed / n / mean, 3) if mean > 0 else np.nan, "p": p, "null": label})
            pairs.append(pd.DataFrame({"dataset": dataset, "characteristic": dimension, "item_id": items, "chance_probability": null["chance_probability"],
                                       "chance_probability_with_observed": null["chance_probability_with_observed"],
                                       "assignments_log10": null["assignments_log10"].round(3), "observed_attributed": null["observed"]}))
        mine = pd.DataFrame([r for r in per_char if r["dataset"] == dataset]).groupby("type")[["testable", "observed_attributed"]].sum()
        for kind in ("D", "N"):                                    # Table 2 per characteristic adds up to the per-text table behind Table 3
            assert int(mine.loc[kind, "testable"]) == int(table[f"testable {kind}"].sum()) and int(mine.loc[kind, "observed_attributed"]) == int(table[f"attributed {kind}"].sum()), \
                f"{dataset}: the testable or attributed counts of type {kind} differ from the table behind Table 3"
        gap_rows.append(_gap(dataset, table, chance, label, reps, seed, reference_gap.loc[dataset]))
        checks.append({"dataset": dataset, "polarized texts with >= 4 ratings": len(table), "null": label, "cases checked by brute force": brute})
    per_char = pd.DataFrame(per_char)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ConstantInputWarning)          # a constant column (every characteristic has 2 groups, for example) has no correlation: the value is NaN
        corr = pd.DataFrame([{"measure": f"n_groups vs {name}", "spearman": round(float(spearmanr(per_char["n_groups"], per_char[column]).statistic), 3), "characteristics": len(per_char)}
                             for name, column in (("observed %", "observed_pct"), ("chance %", "chance_mean_pct"))])
    return {"per_characteristic": per_char, "gap": pd.DataFrame(gap_rows), "per_pair": pd.concat(pairs, ignore_index=True), "correlation": corr, "checks": pd.DataFrame(checks)}


def _gap(dataset: str, table: pd.DataFrame, chance: dict, label: str, reps: int, seed: int, reference: pd.Series) -> dict:
    """The observed gap and the gap in excess of chance, with the bootstrap of the texts of Table 3 (``bootstrap_gap``: the same generator and draws)."""
    values = np.column_stack([table[COLUMNS].to_numpy(dtype=float), chance["D"], chance["N"]])        # testable D, attributed D, testable N, attributed N, chance D, chance N
    n = len(values)
    rng = np.random.default_rng(seed)
    gaps, excess = np.empty(reps), np.empty(reps)
    for b in range(reps):
        s = np.bincount(rng.integers(0, n, n), minlength=n) @ values
        with np.errstate(divide="ignore", invalid="ignore"):
            obs_d, obs_n, ch_d, ch_n = s[1] / s[0], s[3] / s[2], s[4] / s[0], s[5] / s[2]
        gaps[b], excess[b] = 100 * (obs_n - obs_d), 100 * ((obs_n - ch_n) - (obs_d - ch_d))
    total = values.sum(axis=0)
    obs_d, obs_n, ch_d, ch_n = total[1] / total[0], total[3] / total[2], total[4] / total[0], total[5] / total[2]
    finite, finite_excess = gaps[np.isfinite(gaps)], excess[np.isfinite(excess)]
    row = {"dataset": dataset, "texts": n, "testable_D": int(total[0]), "attributed_D": int(total[1]), "testable_N": int(total[2]), "attributed_N": int(total[3]),
           "observed_rate_D_pct": round(100 * obs_d, 2), "observed_rate_N_pct": round(100 * obs_n, 2), "chance_rate_D_pct": round(100 * ch_d, 2), "chance_rate_N_pct": round(100 * ch_n, 2),
           "observed_gap_pp": round(100 * (obs_n - obs_d), 2), "gap_ci_low": round(float(np.percentile(finite, 2.5)), 2), "gap_ci_high": round(float(np.percentile(finite, 97.5)), 2),
           "gap_share_le0_pct": round(100 * float(np.mean(finite <= 0)), 2),
           "excess_gap_pp": round(100 * ((obs_n - ch_n) - (obs_d - ch_d)), 2), "excess_ci_low": round(float(np.percentile(finite_excess, 2.5)), 2),
           "excess_ci_high": round(float(np.percentile(finite_excess, 97.5)), 2), "excess_share_le0_pct": round(100 * float(np.mean(finite_excess <= 0)), 2), "null": label}
    same = (row["observed_rate_D_pct"], row["observed_rate_N_pct"], row["observed_gap_pp"], row["gap_ci_low"], row["gap_ci_high"], round(row["gap_share_le0_pct"], 2))
    paper = (reference["rate D %"], reference["rate N %"], reference["N - D (pp)"], reference["95% interval low"], reference["95% interval high"],
             reference["share of resamples with N - D <= 0 (%)"])
    if not np.allclose(same, paper, atol=1e-9):
        raise ValueError(f"{dataset}: Table 3 is not reproduced: {same} against {tuple(paper)}")
    return row


# ---------------------------------------------------------------------------------------------------------------------------------------------
def _p(value: float) -> str:
    return f"{value:.4f}" if value >= 0.0001 else "<0.0001"


def summary_text(tables: Dict[str, pd.DataFrame], reps: int, seed: int) -> str:
    c, g = tables["per_characteristic"], tables["gap"]
    excluded = "excluded" in str(c["null"].iloc[0])
    L = ["# Exact permutation null for the attribution rates", "",
         "Chance = the AU test run on **every** assignment of a text's raters to the retained groups of the characteristic with the observed group sizes "
         f"(N! / (n1! n2! ...) assignments, each once{', the observed assignment left out' if excluded else ', the observed assignment included'}), on every polarized "
         "text with at least four ratings; thin groups are not removed again and nothing is drawn at random. The chance probability of a text is the share of those "
         "assignments in which it is attributed. Under the null the number of attributed texts is a sum of independent yes / no results with these probabilities, "
         "computed exactly: chance % is its mean, the range its 2.5–97.5 percentiles, p = P(attributed >= observed). D = demographic (gender, race, age), "
         "N = non-demographic. The observed testable counts, attributed counts and rates, the pooled rates and the gap with its range reproduce Tables 2 and 3 "
         "(checked against `attribution_gap`).", ""]
    for dataset in ordered_datasets(c["dataset"].unique()):
        part = c[c["dataset"] == dataset]
        L += [f"## {DATASET_LABEL.get(dataset, dataset)}", "",
              "| characteristic | type | n groups | testable | observed attributed | observed % | chance % | chance range | excess (pp) | ratio | p |", "|---|---|---|---|---|---|---|---|---|---|---|"]
        for _, r in part.iterrows():
            L.append(f"| {r['characteristic']} | {r['type']} | {r['n_groups']} | {r['testable']} | {r['observed_attributed']} | {r['observed_pct']:.1f} | {r['chance_mean_pct']:.1f} | "
                     f"[{r['chance_ci_low_pct']:.1f}, {r['chance_ci_high_pct']:.1f}] | {r['excess_pct']:+.1f} | {r['ratio']:.2f} | {_p(r['p'])} |")
        L.append("")
    L += ["## The gap (non-demographic minus demographic, percentage points)", "",
          f"Bootstrap: {reps:,} resamples of the polarized texts (seed {seed}, as Table 3). In every resample the observed rates are recomputed and the chance rates are the mean of the "
          "exact chance probabilities of the resampled pairs.", "",
          "| dataset | observed D % | observed N % | observed gap [range] | share <= 0 | chance D % | chance N % | excess gap [range] | share <= 0 |", "|---|---|---|---|---|---|---|---|---|"]
    for _, r in g.iterrows():
        L.append(f"| {DATASET_LABEL.get(r['dataset'], r['dataset'])} | {r['observed_rate_D_pct']:.1f} | {r['observed_rate_N_pct']:.1f} | {r['observed_gap_pp']:+.1f} "
                 f"[{r['gap_ci_low']:+.1f}, {r['gap_ci_high']:+.1f}] | {r['gap_share_le0_pct']:.1f}% | {r['chance_rate_D_pct']:.1f} | {r['chance_rate_N_pct']:.1f} | "
                 f"{r['excess_gap_pp']:+.1f} [{r['excess_ci_low']:+.1f}, {r['excess_ci_high']:+.1f}] | {r['excess_share_le0_pct']:.1f}% |")
    L += ["", "## Spearman correlation over all characteristics and datasets", "", "| measure | Spearman | characteristics |", "|---|---|---|"]
    L += [f"| {r['measure']} | {r['spearman']:+.3f} | {r['characteristics']} |" for _, r in tables["correlation"].iterrows()]
    L += ["", "## Checks", "", "| dataset | polarized texts with >= 4 ratings | cases checked by brute force |", "|---|---|---|"]
    L += [f"| {DATASET_LABEL.get(r['dataset'], r['dataset'])} | {r['polarized texts with >= 4 ratings']} | {r['cases checked by brute force']} |" for _, r in tables["checks"].iterrows()]
    low = c[c["testable"] < 15]
    L += ["", "## Caveats", "",
          "- Chance is computed with the groups retained by the paper's 10-text removal rule; the rule is not rerun on the assignments.",
          "- An assignment keeps every group's size on every text, so a text with a group of one rating is never made testable or untestable; only which ratings fall in which group changes.",
          "- A text with few ratings has few assignments (2 + 2 ratings: 5 besides the observed one), so its chance probability takes few values; it is exact, not noisy."
          + (" Leaving the observed assignment out lowers the probability of an attributed text and raises that of a non-attributed one; the effect is largest for small "
             "texts (`chance_probability_with_observed` in the per-pair file has the value with it included)." if excluded else ""),
          "- Splits of the ratings with a share below 1e-30 of the assignments are skipped (texts with hundreds of ratings only); their total is far below the precision shown.",
          "- The bootstrap range of the excess gap treats the chance probabilities as fixed; they are exact, so there is no permutation noise to add.",
          f"- Characteristics with fewer than 15 testable texts (their chance range and p are coarse): {', '.join(f'{r.dataset}/{r.characteristic} ({r.testable})' for r in low.itertuples()) or 'none'}.",
          "- The per-pair chance probabilities are in `per_pair_chance_probability.csv` (one row per testable text and characteristic, with the number of assignments as log10).", ""]
    return "\n".join(L)


def save_null(tables: Dict[str, pd.DataFrame], folder: Path, reps: int = 10_000, seed: int = 42) -> Dict[str, Path]:
    """Write the three csv files and ``summary.md`` into ``folder`` (created if needed)."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    written = {}
    for file, key in (("attribution_null_per_characteristic.csv", "per_characteristic"), ("attribution_null_gap.csv", "gap"), ("per_pair_chance_probability.csv", "per_pair")):
        tables[key].to_csv(folder / file, index=False, encoding="utf-8")
        written[file] = folder / file
    (folder / "summary.md").write_text(summary_text(tables, reps, seed), encoding="utf-8")
    written["summary.md"] = folder / "summary.md"
    return written
