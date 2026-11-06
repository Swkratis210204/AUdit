"""The counts of the paper, to check that the AU results of the four datasets are the ones the tables were made from. Pass them to
``compute_kappa(expected_distinct=..., expected_sample_rows=...)`` and ``compute_poles(expected_attributions=...)``."""

EXPECTED_DISTINCT = {"attitudes": 41, "popquorn": 154, "mhs": 95, "kumar": 5209}          # distinct attributed texts of the full AU results
EXPECTED_SAMPLE_ROWS = {"kumar": 342}                                                      # Kumar: only the sample of 342 attributions (every group >= 50 times) goes to the models
EXPECTED_ATTRIBUTIONS = {"attitudes": 51, "popquorn": 183, "mhs": 105, "kumar": 342}       # attributed rows (text x characteristic) used in the paper
