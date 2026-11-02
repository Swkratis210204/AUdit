"""Names, order and colours shared by the analyses and the figures: how the datasets and the models are called and in which order they are shown."""
from __future__ import annotations

__all__ = ["DATASET_LABEL", "DATASET_ORDER", "DATASET_COLOR", "MODEL_NAME", "ordered_datasets"]

DATASET_LABEL = {"popquorn": "POPQUORN", "attitudes": "Attitudes", "mhs": "MHS", "kumar": "Kumar"}      # the names in the figures
DATASET_ORDER = ["attitudes", "popquorn", "mhs", "kumar"]                                               # the order of the panels and the legends
DATASET_COLOR = {"attitudes": "#4C72B0", "kumar": "#55A868", "mhs": "#C44E52", "popquorn": "#8172B3"}
MODEL_NAME = {"chatgpt": "ChatGPT", "deepseek": "DeepSeek", "gemini": "Gemini", "mistral": "Mistral"}


def ordered_datasets(names) -> list:
    """The dataset names in the order of the figures (a name that is not listed goes last, in the order it comes)."""
    names = list(dict.fromkeys(names))
    return sorted(names, key=lambda n: DATASET_ORDER.index(n) if n in DATASET_ORDER else len(DATASET_ORDER))
