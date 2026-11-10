# Load and clean a dataset

A dataset is a long table with one row per rating: `item_id`, `text`, `rating` and one column per annotator characteristic. A `DatasetSpec` says where it comes from and how its raw values become groups.

## What `run_dataset` does

1. loads the table (`spec.load`) and applies the `prefilter` (for example "at least 4 ratings per text"),
2. drops the ratings whose characteristic value is not in the mapping (a value you do not list is removed),
3. runs the AU analysis of every characteristic (see [03_attribution](03_attribution.md)),
4. returns a `DatasetResult`.

```python
result = run_dataset(spec, raw=my_dataframe)
print(result.describe())     # ratings and texts before and after the cleaning
result.groups                # ratings per group after the cleaning
```

## Your own dataset

```python
from polaudit import DatasetSpec

spec = DatasetSpec(
    name="mydata",
    load=lambda root: my_dataframe,
    dimensions={"gender": ("gender", {"m": "man", "f": "woman"}),         # characteristic -> (column, raw value -> group)
                "politics": ("politics", {"l": "left", "r": "right"})},
    scale_max=5,                  # ratings run from 1 to scale_max
    toxic_threshold=3,            # a rating at or above this is toxic
    min_au_texts=10,              # the 10-text rule
)
```

A mapping can also be a function when the groups come from a number (an age, for example). The four datasets of the paper (POPQUORN, Attitudes, MHS, Kumar) are
in `polaudit.SPECS`; their raw files are not shipped, see [reference.md](reference.md#data).

**Notebook:** [01_data.ipynb](../notebooks/01_data.ipynb)
