"""How much the models agree with each other, as a diagnostic: Spearman correlation of their scores and Cohen's kappa of their labels.

It reads the ratings the models already gave with the default prompt (``<dataset>/baseline/<model>.csv``) and asks nothing of a model. For every dataset and every pair
of models the two sets of ratings of the texts that both rated are compared.
"""
from __future__ import annotations

from itertools import combinations
from pathlib import Path
from typing import Dict, Sequence

import numpy as np
import pandas as pd

from .agreement import cohen_kappa, spearman
from .kappa_groups import MODELS, THRESHOLD, _r
from .names import DATASET_ORDER

__all__ = ["compare_models", "MEASURES"]

MEASURES = {"spearman": "Spearman correlation", "kappa": "Cohen's kappa"}


def _scores(results_dir: Path, dataset: str, models: Sequence[str]) -> Dict[str, pd.Series]:
    out = {}
    for model in models:
        path = Path(results_dir) / dataset / "baseline" / f"{model}.csv"
        if not path.exists():
            raise FileNotFoundError(f"no default ratings of {model} for {dataset}: {path}")
        out[model] = pd.read_csv(path, dtype={"item_id": str}).drop_duplicates("item_id").set_index("item_id")["score"]
    return out


def compare_models(results_dir: Path, datasets: Sequence[str] = DATASET_ORDER, models: Sequence[str] = MODELS, threshold: int = THRESHOLD) -> Dict[str, pd.DataFrame]:
    """The tables: ``pairwise`` (one row per dataset and pair of models) and ``matrices`` (the same numbers as a matrix per dataset and measure, diagonal 1).
    ``results_dir`` holds ``<dataset>/baseline/<model>.csv``; a score at or above ``threshold`` is toxic."""
    pairs, matrices = [], []
    for dataset in datasets:
        scores = _scores(results_dir, dataset, models)
        values = {m: {measure: pd.Series(np.nan, index=models) for measure in MEASURES} for m in models}
        for m in models:
            for measure in MEASURES:
                values[m][measure][m] = 1.0
        for a, b in combinations(models, 2):
            both = scores[a].index.intersection(scores[b].index)
            x, y = scores[a].loc[both], scores[b].loc[both]
            label_x, label_y = (x >= threshold).to_numpy(), (y >= threshold).to_numpy()
            spear, kappa = spearman(x, y), cohen_kappa(label_x, label_y)
            pairs.append({"dataset": dataset, "model_a": a, "model_b": b, "n_texts": int(len(both)), "spearman": _r(spear), "kappa": _r(kappa),
                          "agreement_pct": round(100 * float(np.mean(label_x == label_y)), 2), "pct_toxic_a": round(100 * float(label_x.mean()), 2),
                          "pct_toxic_b": round(100 * float(label_y.mean()), 2), "constant_a": bool(len(set(label_x)) == 1), "constant_b": bool(len(set(label_y)) == 1)})
            for measure, value in (("spearman", spear), ("kappa", kappa)):
                values[a][measure][b] = values[b][measure][a] = _r(value)
        for measure in MEASURES:
            for m in models:
                matrices.append({"dataset": dataset, "measure": measure, "model": m, **values[m][measure].to_dict()})
    return {"pairwise": pd.DataFrame(pairs), "matrices": pd.DataFrame(matrices)}
