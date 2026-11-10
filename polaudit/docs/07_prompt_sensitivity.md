# Prompt sensitivity

Does the model's answer depend on how you *word* the question? Run the same texts with two or more prompts that carry **the same information** (same scale, same rule, same
reply format) and compare the runs. If a rewording changes the labels, a result that you report belongs to the prompt and not only to the model.

```python
from polalign import annotate, compare_prompts, sample_inputs

sample = sample_inputs(inputs, 50, seed=42)          # the same random texts for every prompt and model
annotate(model, sample, "results", prompt=baseline_prompt, run="baseline")
annotate(model, sample, "results", prompt=reworded_prompt, run="reworded")

compare_prompts("results", datasets=["mydata"], runs=["baseline", "reworded"], models=["chatgpt"])
```

One row per dataset, model and pair of runs, on the texts rated in both:

| column | meaning |
|---|---|
| `label_agreement_pct` and `label_agreement_ci` | share of texts with the same label (score 3 or more is toxic), with a 95% bootstrap range |
| `kappa` | Cohen's kappa of the two sets of labels |
| `weighted_kappa` and `weighted_kappa_ci` | quadratic weighted kappa of the 1-5 scores, with a 95% bootstrap range |
| `spearman` | do the two prompts put the texts in the same order? |
| `mean_shift` | mean of (second score - first score): does the model become harsher or milder? |

**Design tips.** Change only the wording, keep every rule and the reply format. Use a new `run` name for every prompt. Keep the sample and the seed fixed. Compare the change due to wording with
the change due to using another model (`compare_models`, see [08](08_model_eda.md)) to see which matters more. The paper's own version of this check, with its figures, is `paper/ablation_prompt.py`.

**Notebook:** [07_prompt_sensitivity.ipynb](../notebooks/07_prompt_sensitivity.ipynb)
