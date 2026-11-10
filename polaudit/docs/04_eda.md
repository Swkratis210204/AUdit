# Describing a dataset (EDA)

`eda_tables(result)` and `save_eda(result, folder)` describe one dataset after the cleaning. Nothing here calls a model.

| table | what it shows |
|---|---|
| `preprocessing` | ratings and texts before and after each cleaning step |
| `overview` | ratings per text, DFU, polarized share |
| `rating_distribution` | the share of each rating |
| `funnel` | what happens to the texts of each characteristic: not polarized, too few groups, a group is not unimodal, AU |
| `groups` | ratings and toxic share of every group, among all texts and among the attributed ones |
| `au_labels` | the position (toxic / civil) of each group on the attributed texts |
| `text_length` | words per text |

```python
from polaudit import eda_tables, save_eda

tables = eda_tables(result)
save_eda(result, "eda_mydata")      # the tables as csv and the figures as png (needs matplotlib)
```

`dataset_tables(result)` adds a description of the dataset itself: who the annotators are and how raw values became groups.

**Notebook:** [04_eda.ipynb](../notebooks/04_eda.ipynb)
