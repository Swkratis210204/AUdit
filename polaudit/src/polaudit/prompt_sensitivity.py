"""Prompt sensitivity: does rewording the question change the ratings of a model?

Run the same texts with two or more prompts (one ``run`` name per prompt, see ``annotate``), then ``compare_prompts`` compares every pair of runs for every model.
Nothing here asks a model for anything: it reads ``<dataset>/<run>/<model>.csv``. For a fair comparison the prompts must carry the same information (the same scale, rule
and reply format) so that a difference can only come from the wording.
"""
from __future__ import annotations

from itertools import combinations
from pathlib import Path
from typing import Dict, Sequence

import numpy as np
import pandas as pd

from .agreement import cohen_kappa, spearman, weighted_kappa
from .kappa_groups import THRESHOLD, _r

__all__ = ["compare_prompts"]


def _scores(results_dir: Path, dataset: str, run: str, model: str) -> pd.Series:
    path = Path(results_dir) / dataset / run / f"{model}.csv"
    if not path.exists():
        raise FileNotFoundError(f"no ratings of {model} for {dataset} in run {run!r}: {path}")
    return pd.read_csv(path, dtype={"item_id": str}).drop_duplicates("item_id").set_index("item_id")["score"]


def _interval(values: np.ndarray) -> tuple:
    values = values[~np.isnan(values)]
    return (_r(np.percentile(values, 2.5)), _r(np.percentile(values, 97.5))) if len(values) else (np.nan, np.nan)


def compare_prompts(results_dir: Path, datasets: Sequence[str], runs: Sequence[str], models: Sequence[str], reps: int = 1_000, seed: int = 42,
                    threshold: int = THRESHOLD) -> pd.DataFrame:
    """One row per dataset, model and pair of runs, on the texts rated in both runs.

    ``label_agreement_pct`` is the share of texts with the same label (a score at or above ``threshold`` is toxic), ``kappa`` the Cohen's kappa of the labels,
    ``weighted_kappa`` the quadratic weighted kappa of the 1-5 scores, ``spearman`` their rank correlation and ``mean_shift`` the mean of (second - first) score.
    ``label_agreement_ci`` and ``weighted_kappa_ci`` are 95% bootstrap ranges (the texts are resampled ``reps`` times, with ``seed``)."""
    rows = []
    for dataset in datasets:
        for model in models:
            scores = {run: _scores(results_dir, dataset, run, model) for run in runs}
            for first, second in combinations(runs, 2):
                ids = scores[first].index.intersection(scores[second].index)
                a, b = scores[first].loc[ids].to_numpy(), scores[second].loc[ids].to_numpy()
                la, lb = a >= threshold, b >= threshold
                draws = np.random.default_rng(seed).integers(0, len(ids), size=(reps, len(ids))) if len(ids) else np.empty((0, 0), dtype=int)
                agree = np.array([np.mean(la[d] == lb[d]) * 100 for d in draws])
                wk = np.array([weighted_kappa(a[d], b[d]) for d in draws])
                rows.append({"dataset": dataset, "model": model, "first": first, "second": second, "n_texts": int(len(ids)),
                             "label_agreement_pct": round(100 * float(np.mean(la == lb)), 2) if len(ids) else np.nan, "label_agreement_ci": _interval(agree),
                             "kappa": _r(cohen_kappa(la, lb)), "weighted_kappa": _r(weighted_kappa(a, b)), "weighted_kappa_ci": _interval(wk),
                             "spearman": _r(spearman(a, b)), "mean_shift": round(float(np.mean(b - a)), 3) if len(ids) else np.nan})
    return pd.DataFrame(rows)
