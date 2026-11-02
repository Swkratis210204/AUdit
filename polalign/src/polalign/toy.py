"""A small made-up dataset and a stand-in model, so every tutorial runs without downloads, keys or credits.

``toy_spec()`` describes a dataset of 60 texts rated by 24 annotators with three characteristics (gender, politics, age). Twenty texts are consensus, twenty are
polarized by politics (left says civil, right says toxic), twenty by gender (men say civil, women say toxic). ``standin_model()`` answers like a model that reads the
tone: it calls a text toxic when it ends with "!" (the polarized texts end with "!" or "." as the toxic side would write them), and never calls a model.
"""
from __future__ import annotations

import json
import re
from typing import Optional

import numpy as np
import pandas as pd

from .env import Env
from .models import Model, ModelConfig, Provider
from .spec import DatasetSpec

__all__ = ["toy_ratings", "toy_spec", "standin_model", "standin_persona_model"]

N_TEXTS, ITEM_WORD = 60, "text"


def toy_ratings(seed: int = 0) -> pd.DataFrame:
    """One row per rating: ``item_id``, ``text``, ``rating`` (1-5), ``annotator`` and the raw characteristics ``gender``, ``politics`` and ``age``."""
    rng = np.random.default_rng(seed)
    annotators = pd.DataFrame([{"annotator": f"a{i}", "gender": g, "politics": p, "age": a}
                               for i, (g, p, a) in enumerate((g, p, a) for g in ("m", "f") for p in ("left", "right") for a in ("young", "old") for _ in range(3))])
    rows = []
    for i in range(N_TEXTS):
        kind = ("consensus", "politics", "gender")[i % 3]
        toxic_side = (i // 3) % 2                                                   # which side finds a polarized text toxic
        for _, a in annotators.iterrows():
            if kind == "consensus":
                toxic = i % 2 == 0
            elif kind == "politics":
                toxic = (a["politics"] == "right") == bool(toxic_side)
            else:
                toxic = (a["gender"] == "f") == bool(toxic_side)
            rows.append({"item_id": f"t{i}", "text": f"Toy comment number {i}{'!' if toxic_side else '.'}" if kind != "consensus" else f"Toy comment number {i}.",
                         "rating": int(rng.choice([4, 5]) if toxic else rng.choice([1, 2])), **a.to_dict()})
    return pd.DataFrame(rows)


def toy_spec(min_au_texts: int = 5) -> DatasetSpec:
    """The ``DatasetSpec`` of the toy dataset; pass it to ``run_dataset``."""
    return DatasetSpec(name="toy", load=lambda root=None: toy_ratings(), item_word=ITEM_WORD, annotator_column="annotator", min_au_texts=min_au_texts,
                       dimensions={"gender": ("gender", {"m": "man", "f": "woman"}), "politics": ("politics", {"left": "left", "right": "right"}),
                                   "age": ("age", {"young": "young", "old": "old"})})


class _Tone(Provider):
    """Answers every numbered text of the prompt with a score: 5 if it ends with "!", 1 otherwise. A prompt that contains the word ``strict`` makes the model harsher:
    a text that does not end with "!" gets 3 (toxic). So a rewording with that word changes the labels, and a rewording without it does not."""

    def complete(self, prompt: str, max_tokens: int, temperature: float) -> str:
        texts = [line.split(". ", 1)[1].strip() for line in prompt.splitlines() if re.match(r"\s*\d+\. ", line)]
        mode = self.config.request_extra.get("mode", "calm")
        calm = 3 if mode == "harsh" or "strict" in prompt.lower() else 1
        scores = [(1 if mode == "contrarian" else 5) if t.endswith("!") else (5 if mode == "contrarian" else calm) for t in texts]
        return "\n".join(f"score={s}, label={'toxic' if s >= 3 else 'civil'}" for s in scores)


class _Stereotype(Provider):
    """Answers as the persona of the prompt: for every group named on the line ``Groups: a, b`` it gives 5 (toxic) to ``right``, ``woman`` and ``old``, whatever the text says
    (the stereotype of the group), and to the other groups the score of the tone of the text (5 if the last line of the prompt, ``<item>: <text>``, ends with "!", else 1)."""

    TOXIC = {"right", "woman", "old"}

    def complete(self, prompt: str, max_tokens: int, temperature: float) -> str:
        line = next(l for l in prompt.splitlines() if l.lower().startswith("groups:"))
        groups = [g.strip() for g in line.split(":", 1)[1].split(",") if g.strip()]
        text = prompt.strip().splitlines()[-1].split(": ", 1)[-1].strip()
        tone = 5 if text.endswith("!") else 1
        return json.dumps({g: {"score": 5 if g in self.TOXIC else tone} for g in groups})


def standin_model(name: str = "standin", mode: str = "calm") -> Model:
    """A model that costs nothing: it calls a text toxic when it ends with "!", and is harsher when the prompt contains the word ``strict`` (see the module).
    ``mode="harsh"`` always rates the other texts 3 (toxic) and ``mode="contrarian"`` takes the opposite side. Use it like a model of ``ModelHub``."""
    config = ModelConfig(name=name, model_id="standin", retries=1, request_extra={"mode": mode})
    return Model(config, env=Env({}), provider=_Tone(config, Env({})))


def standin_persona_model(name: str = "standin") -> Model:
    """A model that costs nothing for persona prompting: your prompt must contain a line ``Groups: a, b`` (the groups shown); it answers with the stereotype of each group."""
    return Model(ModelConfig(name=name, model_id="standin", retries=1, max_tokens=200), env=Env({}), provider=_Stereotype(ModelConfig(name=name), Env({})))
