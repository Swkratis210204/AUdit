# Annotating with LLMs

You bring the **prompt** and the **models**; the package batches the texts, calls the model, retries, parses and saves every answer so a run can be resumed.

```python
from perspective_audit import ModelHub, annotate, load_model_inputs

inputs = load_model_inputs("results/aposteriori_for_models.csv")     # the attributed texts, written by save_au_tables
hub = ModelHub.from_env()                                            # keys from your .env, see reference.md

def my_prompt(texts, item):                                          # texts: the batch, numbered "1. ...", item: "tweet", "comment", ...
    return f"Rate how toxic each {item} is from 1 to 5.\nFormat: score=<n>, label=<toxic/civil>\n\n{texts}"

annotate(hub["chatgpt"], inputs, "results", prompt=my_prompt, run="baseline")
```

- **Your prompt.** `prompt(texts, item) -> str`. The reply must have one line `score=<n>, label=<toxic/civil>` per text. Use a new `run` name for every prompt.
- **Your model.** `ModelHub` has ChatGPT, DeepSeek, Gemini and Mistral by default. A `ModelConfig` adds any OpenAI-compatible endpoint, Gemini, or your own `Provider`.
- **Safe to rerun.** Finished batches are kept; a batch whose reply has the wrong number of scores is asked again twice and then raises `AnnotationError`. No answer is guessed.
- **Persona prompting (SCD).** `annotate_personas` asks the model to answer as a member of each group of a characteristic, with your own `prompt(text, item, dimension, groups)`.
- **A free stand-in.** `perspective_audit.toy.standin_model()` answers without any API. The notebook uses it.

Everything is saved as `results/<dataset>/<run>/<model>.csv` and a raw copy of every reply in `raw/`, plus `run_log.csv`. The providers' answers do not carry a model version: write
the model id and the date down in your own notes.

**Notebook:** [05_llm_annotation.ipynb](../notebooks/05_llm_annotation.ipynb)
