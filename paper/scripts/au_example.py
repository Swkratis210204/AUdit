"""Figure au_example: AU on a synthetic text rated by eight annotators (all ratings, politics split, gender split).

Colour encodes the characteristic (not the rating): politics green, gender orange, all annotators gray.
The civil / toxic cut (ratings 1-2 | 3-5) is a dashed line between 2 and 3.
Writes new_results/au/au_example.pdf and the copy used by the paper, new_draft/ArrAposterioriLLM/images/au_example.pdf.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
OUT = [ROOT / "new_results" / "au" / "au_example.pdf", ROOT / "new_draft" / "ArrAposterioriLLM" / "images" / "au_example.pdf"]

W, H = 543.63, 350.24                         # figure size in points (as before)
POLITICS, GENDER, ALL = "#009E73", "#E69F00", "#4D4D4D"
POLITICS_TEXT, GENDER_TEXT = "#00694D", "#8A5700"     # darker shades of the same hues for the text (contrast >= 4.5 on white)

# (title, counts of ratings 1..5, nDFU, colour, box in points: x0, x1, y_top, y_bottom)
PANELS = [
    ("All annotators", [3, 1, 0, 2, 2], 0.67, ALL, (34.2, 170.0, 62.7, 295.5)),
    ("Politics: left", [3, 1, 0, 0, 0], 0.00, POLITICS, (217.5, 353.2, 62.7, 143.0)),
    ("Politics: right", [0, 0, 0, 2, 2], 0.00, POLITICS, (217.5, 353.2, 215.2, 295.5)),
    ("Gender: man", [1, 1, 0, 1, 1], 1.00, GENDER, (400.7, 536.4, 62.7, 143.0)),
    ("Gender: woman", [2, 0, 0, 1, 1], 0.50, GENDER, (400.7, 536.4, 215.2, 295.5)),
]


def make():
    fig = plt.figure(figsize=(W / 72, H / 72))
    for title, counts, ndfu, color, (x0, x1, top, bottom) in PANELS:
        ax = fig.add_axes([x0 / W, 1 - bottom / H, (x1 - x0) / W, (bottom - top) / H])
        ax.bar(range(1, 6), counts, color=color, edgecolor="black", linewidth=0.6)
        ax.axvline(2.5, color="black", linestyle="--", linewidth=0.8)
        ax.text(2.35, 3.55, "civil", ha="right", va="center", fontsize=10)
        ax.text(2.65, 3.55, "toxic", ha="left", va="center", fontsize=10)
        ax.set_ylim(0, 4)
        ax.set_xticks(range(1, 6))
        ax.set_yticks(range(5))
        ax.set_title(f"{title}\nDFU = {ndfu:.2f}", fontsize=10)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        if bottom > 290:
            ax.set_xlabel("rating", fontsize=10)
        if x0 < 100:
            ax.set_ylabel("annotators", fontsize=10)
    fig.text(196.5 / W, 1 - 337 / H, "\u2714 Split by politics: attributed", color=POLITICS_TEXT, fontsize=10, fontweight="bold", ha="center", va="center")
    fig.text(378 / W, 1 - 337 / H, "\u2718 Split by gender: not attributed", color=GENDER_TEXT, fontsize=10, fontweight="bold", ha="center", va="center")
    return fig


if __name__ == "__main__":
    fig = make()
    for path in OUT:
        fig.savefig(path)
        print(path)
