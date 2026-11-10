"""Alignment of the models with the toxic and the civil pole of polarized texts (section 7.6). The logic is in ``polaudit/poles.py``.

Run from the repository root:  python paper/scripts/poles.py
Output: new_results/poles/poles_alignment.csv, poles_groups.csv, poles_direction.csv, summary.md
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "polaudit" / "src"))     # works without installing the package

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from paper.expected import EXPECTED_ATTRIBUTIONS
from polaudit import compute_poles, find_root, load_results, save_poles

if __name__ == "__main__":
    root = find_root()
    given = pd.read_csv(root / "new_results" / "aposteriori_for_models.csv", dtype={"item_id": str})
    tables = compute_poles(load_results(), root / "new_results", given, reps=10_000, seed=42, expected_attributions=EXPECTED_ATTRIBUTIONS)
    print(tables["checks"].to_string(index=False))
    print(save_poles(tables, root / "new_results" / "poles"))
