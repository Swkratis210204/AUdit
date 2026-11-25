"""Steps 1-3 of the audit on DICES: preprocessing, polarization (DFU), a-posteriori unimodality (AU)."""
import sys
from pathlib import Path
import pandas as pd
from polaudit import run_dataset
from polaudit.spec import DatasetSpec

HERE = Path(__file__).parent
FILE = sys.argv[1] if len(sys.argv) > 1 else "dices_350.csv"
RATING = {"No": 1, "Unsure": 2, "Yes": 3}          # Q_overall: is the response unsafe? (3-point scale)


def load(root):
    raw = pd.read_csv(HERE / FILE)
    raw["text"] = raw["context"].astype(str) + "\n" + raw["response"].astype(str)
    raw["rating"] = raw["Q_overall"].map(RATING)
    return raw.dropna(subset=["rating"]).astype({"rating": int})


keep = lambda *v: {x: x for x in v}
SPEC = DatasetSpec(
    name="dices", load=load, scale_max=3, item_word="conversation", annotator_column="rater_id", rating_column="Q_overall",
    dimensions={
        "gender": ("rater_gender", keep("Man", "Woman")),
        "race": ("rater_race", keep("White", "Black/African American", "Asian/Asian subcontinent", "LatinX, Latino, Hispanic or Spanish Origin", "Multiracial")),
        "age": ("rater_age", keep("gen z", "millenial", "gen x+")),
        "education": ("rater_education", keep("College degree or higher", "High school or below")),
    },
)

res = run_dataset(SPEC, root=HERE)
print("=== 1. PREPROCESSING ===");  print(res.describe())
print("\nratings per group:\n", res.groups)

print("\n=== 2. POLARIZATION (DFU of all ratings of a text) ===")
for dim, pr in res.pruned.items():
    r = pr.result
    print(f"{dim:10s} texts {len(r)}  polarized (DFU>0) {int((r['dfu'] > 0).sum())}  mean DFU {r['dfu'].mean():.3f}")

print("\n=== 3. A-POSTERIORI UNIMODALITY (attribution) ===")
print(res.per_dimension)
for dim, pr in res.pruned.items():
    print(f"\n[{dim}] reasons:\n{res.tool.reason_counts(pr.result).to_string()}")
print("\nAU texts per group:\n", res.per_group)
print("\nstarting list (before/after removing thin groups):\n", res.starting_list)
res.au.to_csv(HERE / f"au_{Path(FILE).stem}.csv", index=False)
