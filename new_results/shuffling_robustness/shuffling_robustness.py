"""Exact permutation null for the attribution rates and the demographic / non-demographic gap (section 7.7). The logic is in ``polaudit/shuffling_robustness.py``.

Run from the repository root:  python new_results/shuffling_robustness/shuffling_robustness.py
Output (next to this script): attribution_null_per_characteristic.csv, attribution_null_gap.csv, per_pair_chance_probability.csv, summary.md
Every assignment of the raters of a text to its groups, once each, the observed assignment left out (no random draws).
"""
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / "polaudit" / "src"))     # works without installing the package

from polaudit import compute_null, load_results, save_null

if __name__ == "__main__":
    tables = compute_null(load_results(), reps=10_000, seed=42, exclude_observed=True)
    print(tables["checks"].to_string(index=False))
    print(save_null(tables, Path(__file__).resolve().parent, reps=10_000, seed=42))
