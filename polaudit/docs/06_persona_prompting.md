# Persona (sociodemographic) prompting

The default prompt asks "is this text toxic?". **Persona prompting (SCD)** asks the model to answer *as* a member of each group of a characteristic. It tells you how stable
a model's side is: if the labels follow the persona, the side can be moved. We use it as a diagnostic and not as a mitigation.

```python
from polalign import annotate_personas, load_persona_inputs

inputs = load_persona_inputs("results/aposteriori_for_models.csv")     # one row per (text, characteristic) with the groups of that characteristic

def persona_prompt(text, item, dimension, groups):                     # you write it
    return f"""Answer as an annotator of each group, rating how toxic the {item} is from 1 to 5.
Groups: {", ".join(groups)}
Reply with JSON, one key per group: {{"{groups[0]}": {{"score": 3}}, ...}}

{item}: {text}"""

annotate_personas(hub["chatgpt"], inputs, "results", prompt=persona_prompt, run="scd", seed=42)
```

- **One call per text and characteristic.** All groups of the characteristic are rated in the same call, in a **seeded random order** (`seed`), so the first group is not always the same.
- **Your prompt, a fixed reply.** The prompt is yours; the reply must be JSON with one key per group, written exactly as given, and a score 1-5 for each. The label follows from the score.
  A reply without a valid score for every group is asked again (with a larger token budget) and then raises `AnnotationError`.
- **Compare with the default.** With the default run already saved, `compute_kappa(..., prompt="scd")` gives the kappa of each group under the persona prompt and the **change** from the default prompt
  (`prompt_change`), with the same bootstrap resamples. `compute_persona_kappa` gives the full matrix persona by group.
- **Resumable and safe.** Like `annotate`: finished calls are kept, nothing is guessed, and a new prompt or seed needs a new `run` name.

**Notebook:** [06_persona_prompting.ipynb](../notebooks/06_persona_prompting.ipynb)
