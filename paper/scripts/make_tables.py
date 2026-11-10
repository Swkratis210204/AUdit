"""Write the tabular bodies of the paper's kappa tables from new_results/kappa (no numbers typed by hand).

Run from anywhere:  python paper/scripts/make_tables.py [output folder]
Default output: new_draft/ArrAposterioriLLM/tables (kappa_default_<dataset>.tex, kappa_pit_<dataset>.tex, delta_kumar.tex).
Rerun it whenever new_results/kappa changes; the paper reads the files with \\input.
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]                     # the repository root
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "new_draft" / "ArrAposterioriLLM" / "tables"
MODELS = [("chatgpt", "GPT"), ("deepseek", "DS"), ("gemini", "Gem"), ("mistral", "Mis")]
LABEL = {"millenial": "Millennial", "gen x+": "Gen X+", "gen z": "Gen Z", "not_high": "Not high", "high": "High",
         "Black or African American": "Black", "College degree": "College", "Graduate degree": "Graduate",
         "High school diploma or equivalent": "High school"}
CHAR = {"ideology": "Politics"}
TYPE = {"demographic": "D", "non-demographic": "N"}
SPLIT = {"kumar": [["gender", "race", "age"], ["politics", "religion"]],
         "popquorn": [["gender", "race", "age"], ["education", "occupation"]],
         "attitudes": [["gender", "race", "age"], ["politics", "traditionalism"]],
         "mhs": [["gender", "age", "ideology"]]}
FEW = {("attitudes", "age"), ("attitudes", "traditionalism")}        # fewer than ten polarizers


def num(x):
    s = f"{x:.2f}"
    if s == "-0.00":
        s = "0.00"
    return "$-$" + s[1:] if s.startswith("-") else s


def cell(r):
    v = num(r.kappa)
    if (r.ci_low > 0) or (r.ci_high < 0):
        v = r"\textbf{" + v + "}"
    if r.constant_model:
        v += r"$^\dagger$"
    return f"{v} ({r.se:.2f})"


def label(g):
    return LABEL.get(g, g[:1].upper() + g[1:])


def tabular(d, dataset, chars, toxic=None):
    cols = []
    for ch in chars:
        part = d[(d.characteristic == ch)]
        groups = list(dict.fromkeys(part.group))
        cols.append((ch, groups))
    ncol = sum(len(g) for _, g in cols)
    extra = toxic is not None
    lines = [r"\begin{tabular}{@{}l*{%d}{c}%s@{}}" % (ncol, "r" if extra else ""), r"\toprule"]
    head, rules, start = ["Model"], [], 2
    top = [""]
    for ch, groups in cols:
        name = CHAR.get(ch, ch.capitalize())
        dag = r"$^\ddagger$" if (dataset, ch) in FEW else ""
        top.append(r"\multicolumn{%d}{c}{%s (%s)%s}" % (len(groups), name, TYPE[d[d.characteristic == ch].type.iloc[0]], dag))
        rules.append(r"\cmidrule(lr){%d-%d}" % (start, start + len(groups) - 1))
        start += len(groups)
        head += [label(g) for g in groups]
    if extra:
        top.append("")
        head.append(r"Toxic (\%)")
    lines.append(" & ".join(top) + r" \\")
    lines.append("".join(rules))
    lines.append(" & ".join(head) + r" \\")
    n = ["$n$"] + [str(int(d[(d.characteristic == ch) & (d.group == g)].n_texts.iloc[0])) for ch, groups in cols for g in groups]
    if extra:
        n.append("")
    lines.append(" & ".join(n) + r" \\")
    lines.append(r"\midrule")
    for m, short in MODELS:
        row = [short]
        for ch, groups in cols:
            for g in groups:
                r = d[(d.characteristic == ch) & (d.group == g) & (d.model == m)].iloc[0]
                row.append(cell(r))
        if extra:
            row.append(f"{toxic[m]:.0f}")
        lines.append(" & ".join(row) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines)


def kappa_tables(prompt):
    d = pd.read_csv(ROOT / "new_results" / "kappa" / prompt / "kappa_by_group.csv")
    out = {}
    for dataset, splits in SPLIT.items():
        part = d[d.dataset == dataset]
        toxic = part.groupby("model").pct_toxic_model.mean().to_dict()
        blocks = []
        for i, chars in enumerate(splits):
            blocks.append(tabular(part, dataset, chars, toxic if i == len(splits) - 1 else None))
        out[dataset] = "\n\n\\medskip\n\n".join(blocks)
    return out


def delta_kumar():
    c = pd.read_csv(ROOT / "new_results" / "kappa" / "scd" / "kappa_prompt_change.csv").query("dataset == 'kumar'")
    order = [("gender", "Gender (D)"), ("race", "Race (D)"), ("age", "Age (D)"), ("politics", "Politics (N)"), ("religion", "Religion (N)")]
    lines = [r"\begin{tabular}{@{}l*{4}{rrr}@{}}", r"\toprule",
             r"& \multicolumn{3}{c}{GPT} & \multicolumn{3}{c}{DS} & \multicolumn{3}{c}{Gem} & \multicolumn{3}{c}{Mis} \\",
             r"\cmidrule(lr){2-4}\cmidrule(lr){5-7}\cmidrule(lr){8-10}\cmidrule(lr){11-13}",
             r"Group & Def. & PIT & $\Delta$ & Def. & PIT & $\Delta$ & Def. & PIT & $\Delta$ & Def. & PIT & $\Delta$ \\", r"\midrule"]
    for ch, name in order:
        lines.append(r"\multicolumn{13}{@{}l}{\textit{%s}} \\" % name)
        part = c[c.characteristic == ch]
        for g in dict.fromkeys(part.group):
            row = [r"\quad " + label(g)]
            for m, _ in MODELS:
                r = part[(part.group == g) & (part.model == m)].iloc[0]
                delta = ("$+$" if r.change >= 0 else "$-$") + f"{abs(r.change):.2f}"
                if r.interval_excludes_zero:
                    delta = r"\cellcolor{gray!20}\textbf{" + delta + "}"
                row += [num(r.kappa_baseline), num(r.kappa_scd), delta]
            lines.append(" & ".join(row) + r" \\")
        lines.append(r"\addlinespace[3pt]")
    lines[-1] = r"\bottomrule"
    lines.append(r"\end{tabular}")
    return "\n".join(lines)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    NOTE = "% generated from new_results/kappa by paper/scripts/make_tables.py; do not edit by hand\n"
    for prompt, tag in (("default", "default"), ("scd", "pit")):
        t = kappa_tables(prompt)
        for dataset in SPLIT:
            (OUT / f"kappa_{tag}_{dataset}.tex").write_text(NOTE + t[dataset] + "\n", encoding="utf-8")
    (OUT / "delta_kumar.tex").write_text(NOTE + delta_kumar() + "\n", encoding="utf-8")
    print(sorted(p.name for p in OUT.iterdir()))
