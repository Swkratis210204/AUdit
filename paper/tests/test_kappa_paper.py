"""The kappa tables and figures of the paper (LaTeX tables, two-panel figures), on the same toy data as the tests of ``compute_kappa``.
Tests of the kappa between the models and the groups (section 7.2), on a small made-up dataset where the answers are known."""
import json

import numpy as np
import pandas as pd
import pytest

from polalign import DatasetSpec, compute_kappa, run_dataset, save_kappa
from polalign.kappa_groups import _constant_summary, _kappa

N = 12                                    # texts t0..t5: men civil, women toxic; texts t6..t11: men toxic, women civil


def toy_result():
    rows = []
    for i in range(N):
        men, women = (1, 5) if i < 6 else (5, 1)
        rows += [{"item_id": f"t{i}", "text": f"text {i}", "rating": men, "sex": "m"} for _ in range(2)]
        rows += [{"item_id": f"t{i}", "text": f"text {i}", "rating": women, "sex": "f"} for _ in range(2)]
    raw = pd.DataFrame(rows)
    spec = DatasetSpec(name="attitudes", load=lambda root: raw, dimensions={"gender": ("sex", {"m": "man", "f": "woman"})}, min_au_texts=1)
    return run_dataset(spec, raw=raw)


def man_toxic(i):
    return i >= 6


def build(tmp_path, with_deepseek=True):
    """chatgpt: baseline always toxic (constant), scd always right. deepseek: baseline right for women (= toxic on t0-t5), scd wrong on 4 texts as a man."""
    folder = tmp_path / "attitudes"
    (folder / "baseline").mkdir(parents=True)
    (folder / "scd").mkdir(parents=True)
    ids = [f"t{i}" for i in range(N)]
    def persona(model, i, wrong_as_man):
        man = man_toxic(i) != (i in wrong_as_man)
        return json.dumps([{"as": "man", "score": 5 if man else 1, "label": "x"}, {"as": "woman", "score": 1 if man_toxic(i) else 5, "label": "x"}])
    for model, base, wrong in (("chatgpt", [5] * N, []), ("deepseek", [5 if i < 6 else 1 for i in range(N)], [0, 1, 6, 7])):
        if model == "deepseek" and not with_deepseek:
            continue
        pd.DataFrame({"dataset": "attitudes", "item_id": ids, "text": "x", "model": model, "run": "baseline", "score": base,
                      "label": ["toxic" if s >= 3 else "civil" for s in base]}).to_csv(folder / "baseline" / f"{model}.csv", index=False)
        pd.DataFrame({"dataset": "attitudes", "item_id": ids, "dimension": "gender", "text": "x", "model": model, "run": "scd",
                      "personas": [persona(model, i, wrong) for i in range(N)]}).to_csv(folder / "scd" / f"{model}.csv", index=False)
    given = pd.DataFrame({"dataset": "attitudes", "dimension": "gender", "item_id": ids})
    return tmp_path, given


def one_prompt(tmp_path, prompt, reps=2000, models=("chatgpt", "deepseek")):
    results_dir, given = build(tmp_path)
    return compute_kappa({"attitudes": toy_result()}, results_dir, given, reps=reps, seed=42, models=list(models), prompt=prompt)


def tables(tmp_path, reps=2000, models=("chatgpt", "deepseek")):
    """Both prompts together (the default tables and the SCD tables of 7.2 and 7.3 side by side), for the tests of the numbers."""
    results_dir, given = build(tmp_path)
    default, scd = (compute_kappa({"attitudes": toy_result()}, results_dir, given, reps=reps, seed=42, models=list(models), prompt=prompt) for prompt in ("baseline", "scd"))
    by_group, gaps = pd.concat([default["by_group"], scd["by_group"]], ignore_index=True), pd.concat([default["gaps"], scd["gaps"]], ignore_index=True)
    return {**default, "by_group": by_group, "gaps": gaps, "prompt_change": scd["prompt_change"], "constant": _constant_summary(by_group)}


def test_latex_tables_one_per_dataset(tmp_path):
    from paper.kappa_tables import save_kappa_tables
    t = tables(tmp_path / "runs", reps=200)
    assert "se" in t["by_group"].columns and (t["by_group"]["se"] >= 0).all()
    written = save_kappa_tables(t["by_group"], tmp_path / "tables")
    text = written["attitudes"].read_text(encoding="utf-8")
    assert set(written) == {"attitudes"} and r"\label{tab:kappa_attitudes}" in text and r"\toprule" in text and "Toxic labels" in text
    assert text.count("\makecell") == 8 and "$^\dagger$" in text and "{[}" in text and "(D)" in text


def test_kappa_figures_draw_what_the_csv_says(tmp_path):
    from paper.kappa_figures import save_kappa_figures
    t = tables(tmp_path / "runs", reps=300)
    info = save_kappa_figures(t["by_group"], t["gaps"], tmp_path / "images")
    row = info.iloc[0]
    assert (tmp_path / "images" / "kappa_attitudes.pdf").stat().st_size > 0 and (tmp_path / "images" / "kappa_attitudes.png").stat().st_size > 0
    assert row["colored_bars"] == row["colored_bars_in_csv"] == int(t["gaps"].query("prompt == 'baseline'")["interval_excludes_zero"].sum())
    base = t["by_group"].query("prompt == 'baseline'")
    assert row["outlined_cells"] == int(((base["ci_low"] > 0) | (base["ci_high"] < 0)).sum()) and row["height_inches"] <= 8


def test_default_and_scd_are_separate_sections(tmp_path):
    from paper.kappa_tables import save_kappa_tables
    default, scd = one_prompt(tmp_path / "d", "baseline", 300), one_prompt(tmp_path / "s", "scd", 300)
    assert set(default["by_group"]["prompt"]) == {"baseline"} and set(default["gaps"]["prompt"]) == {"baseline"} and "prompt_change" not in default
    assert set(scd["by_group"]["prompt"]) == {"scd"} and set(scd["gaps"]["prompt"]) == {"scd"} and len(scd["prompt_change"]) == 4       # the change belongs to 7.3
    both = tables(tmp_path / "both", 300)
    row = ["model", "group"]                                                                 # the same resamples: a prompt gives the same numbers alone or together
    assert default["by_group"].set_index(row)["kappa"].equals(both["by_group"].query("prompt == 'baseline'").set_index(row)["kappa"])
    assert default["by_group"].set_index(row)["ci_low"].equals(both["by_group"].query("prompt == 'baseline'").set_index(row)["ci_low"])
    save_kappa(default, tmp_path / "kappa" / "default"), save_kappa(scd, tmp_path / "kappa" / "scd")
    assert not (tmp_path / "kappa" / "default" / "kappa_prompt_change.csv").exists() and (tmp_path / "kappa" / "scd" / "kappa_prompt_change.csv").exists()
    assert "default prompt only" in (tmp_path / "kappa" / "default" / "README.md").read_text(encoding="utf-8")
    save_kappa_tables(default["by_group"], tmp_path / "kappa" / "default" / "tables"), save_kappa_tables(scd["by_group"], tmp_path / "kappa" / "scd" / "tables")
    text_default = (tmp_path / "kappa" / "default" / "tables" / "table_attitudes.tex").read_text(encoding="utf-8")
    text_scd = (tmp_path / "kappa" / "scd" / "tables" / "table_attitudes.tex").read_text(encoding="utf-8")
    assert "with the default prompt" in text_default and "Baseline" not in text_default and text_default.count(r"\makecell") == 4
    assert r"with the \ac{SCD} prompt" in text_scd and text_scd.count(r"\makecell") == 4
