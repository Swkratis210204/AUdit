# paper: reproducing the tables and figures of the paper

This folder is **not** part of the `perspective-audit` package. It holds the code that rebuilds the tables and figures of
*Polarization Auditing Framework for LLMs: a Toxicity Detection Study* (current version of the manuscript) from the results saved in `new_results/`.
It imports the package, so install that first (`pip install -e perspective_audit`).

| file | what it builds |
|---|---|
| `notebooks/Datasets.ipynb` | the whole pipeline of the paper, section by section: AU texts of the four datasets, annotating with the four models, and sections 7.1 to 7.7 |
| `notebooks/polarization_metrics.ipynb` | the comparison of polarization metrics on synthetic distributions (the choice of DFU, Appendix A) |
| `kappa_tables.py`, `kappa_figures.py` | the LaTeX kappa tables and the two-panel kappa figures (7.2, 7.3) |
| `model_comparison.py` | the heatmap of the agreement between the models (7.4); the numbers come from `perspective_audit.compare_models` |
| `ablation_prompt.py` | the prompt-wording ablation with its figures (6.2) |
| `eda_total.py`, `dfu_total.py`, `au_total.py` | the descriptions of all four datasets together (appendix figures and tables) |
| `expected.py` | the counts of the paper, passed to `compute_kappa` and `compute_poles` to check that the AU results are the ones the tables were made from |
| `scripts/` | `poles.py` and `pooled_vs_group.py`, the same analyses as stand-alone scripts |
| `tests/` | the tests of this code (`cd paper && pytest`) |

The raw datasets are not in the repository (see `perspective_audit/docs/reference.md`, section Data). **Careful:** the notebook has a switch `RUN_MODELS` (section 6) that is currently `True`, so running those cells calls the paid model APIs with your keys. Set it to `False` to only read the saved runs.
