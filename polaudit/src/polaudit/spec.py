"""The description of one dataset: how to load it and how its annotator groups are defined."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple, Union

import pandas as pd

__all__ = ["DatasetSpec"]

# a dimension is defined by a column of the raw table and a mapping raw value -> group.
# The mapping is a dict (a value that is not listed is removed) or a function Series -> Series (missing = removed).
Mapping = Union[Dict, Callable[[pd.Series], pd.Series]]


@dataclass(frozen=True)
class DatasetSpec:
    name: str
    load: Callable[..., pd.DataFrame]               # load(root) -> long table with item_id, text, rating and the raw attribute columns
    dimensions: Dict[str, Tuple[str, Mapping]]      # dimension -> (raw column, mapping)
    scale_max: int = 5                              # ratings run from 1 to scale_max
    toxic_threshold: float = 3
    tolerance: float = 0.0
    min_au_texts: int = 10                          # a group in fewer AU texts than this is removed (the 10-text rule); 0 keeps every group, i.e. all AU texts
    min_ratings: int = 2                            # a group needs at least this many ratings on a text to be compared
    min_groups: int = 2                             # a text needs at least this many such groups to be tested
    label_rule: str = "majority_then_mean"          # how a group's position (toxic / civil) is decided: "majority_then_mean", "majority" or "mean"
    prefilter: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None     # applied to the raw table before the cleaning
    item_word: str = "tweet"                        # how a text is called in prompts ("tweet", "comment", ...)
    description: str = ""
    annotator_column: Optional[str] = None          # the column of the loaded table with the annotator id; None when the data has no annotator id
    rating_column: str = "rating"                   # the name of the rating in the original data (the loaded table calls it "rating")
