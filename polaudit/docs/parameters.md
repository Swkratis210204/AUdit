# Parameters: what you can change

Every rule of the audit is an argument with the paper's value as default. Nothing is fixed in the code.

## The AU analysis (`DatasetSpec`, or a keyword of `run_dataset`)

```python
run_dataset(spec, raw=df)                          # the paper's rules
run_dataset(spec, raw=df, min_au_texts=5)          # groups need 5 attributed texts, not 10
run_dataset(spec, raw=df, min_au_texts=0)          # no 10-text rule: keep every group, all AU texts
run_dataset(spec, raw=df, min_ratings=3, min_groups=3)
run_dataset(spec, raw=df, tolerance=0.05, label_rule="mean")
```

| parameter | default | meaning |
|---|---|---|
| `min_au_texts` | 10 | a group in fewer attributed texts is removed (round by round). `0` keeps every group |
| `min_ratings` | 2 | ratings a group needs on a text to be compared |
| `min_groups` | 2 | groups a text needs (with `min_ratings`) to be tested at all |
| `tolerance` | 0 | a DFU up to this value counts as unimodal (a dip of noise in a large group) |
| `label_rule` | `"majority_then_mean"` | position of a group: majority of its binary ratings, an exact tie decided by the mean (`"majority"` or `"mean"` alone) |
| `scale_max` | 5 | ratings run from 1 to this |
| `toxic_threshold` | 3 | a rating at or above this is toxic |
| `prefilter` | none | a function applied to the raw table first (for example, at least 4 ratings per text) |
| `dimensions` | | which characteristics, which column, how raw values become groups |

`run_dataset(..., cache=path)` keeps a large result in a file; the file is only reused when the rules are the same.

## Attribution rate and the chance check

| function | parameters |
|---|---|
| `attribution_gap`, `compute_null` | `demographic=("gender", "race", "age")` (which characteristics are called demographic), `min_text_ratings` (default `min_ratings * min_groups`), `reps`, `seed` |
| `compute_null` | `exclude_observed=True` (leave the observed assignment out of the null); no permutations: every assignment is enumerated |

## Models and prompts

| function | parameters |
|---|---|
| `annotate` | `prompt` (yours), `run`, `batch_size=10`, `parse_retries=2`, `limit`, `scale_max`, `toxic_threshold`, `item_words` |
| `annotate_personas` | `prompt` (yours), `run`, `seed`, `max_attempts`, `first_max_tokens`, `scale_max`, `toxic_threshold` |
| `ModelConfig` | `model_id`, `temperature`, `max_tokens`, `retries`, `base_url`, `request_extra` |
| `sample_inputs` | `n`, `seed` |

## Alignment and the checks

| function | parameters |
|---|---|
| `compute_kappa` | `reps=1_000`, `seed`, `models`, `prompt` (`"baseline"` or `"scd"`), `threshold=3` (the rating from which a model's rating is toxic), `small_n=10` (flag a characteristic with fewer attributed texts), `demographic` |
| `compute_persona_kappa` | `reps`, `seed`, `models`, `threshold` |
| `compute_poles` | `reps`, `seed`, `models`, `threshold`, `small_n=5` |
| `compare_prompts` | `runs` (any number), `models`, `reps`, `seed`, `threshold` |
| `model_eda`, `compare_models` | `datasets`, `models`, `threshold`, and for `model_eda` the rating `scale` |

The 95% range of every interval is the 2.5th to 97.5th percentile of the bootstrap.

## Add your own

A model is a `ModelConfig` (any OpenAI-compatible endpoint, Gemini) or your own `Provider` with a `complete(prompt, max_tokens, temperature)` method. A prompt is a plain function.
A dataset is a `DatasetSpec` with your loader. Nothing else needs to change.
