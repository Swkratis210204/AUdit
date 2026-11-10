# Exact permutation null for the attribution rates

Chance = the AU test run on **every** assignment of a text's raters to the retained groups of the characteristic with the observed group sizes (N! / (n1! n2! ...) assignments, each once, the observed assignment left out), on every polarized text with at least four ratings; thin groups are not removed again and nothing is drawn at random. The chance probability of a text is the share of those assignments in which it is attributed. Under the null the number of attributed texts is a sum of independent yes / no results with these probabilities, computed exactly: chance % is its mean, the range its 2.5–97.5 percentiles, p = P(attributed >= observed). D = demographic (gender, race, age), N = non-demographic. The observed testable counts, attributed counts and rates, the pooled rates and the gap with its range reproduce Tables 2 and 3 (checked against `attribution_gap`).

## Attitudes

| characteristic | type | n groups | testable | observed attributed | observed % | chance % | chance range | excess (pp) | ratio | p |
|---|---|---|---|---|---|---|---|---|---|---|
| gender | D | 2 | 164 | 10 | 6.1 | 3.9 | [1.2, 6.7] | +2.2 | 1.57 | 0.0881 |
| race | D | 2 | 239 | 14 | 5.9 | 4.6 | [2.5, 7.1] | +1.2 | 1.26 | 0.2006 |
| age | D | 3 | 97 | 6 | 6.2 | 4.2 | [1.0, 8.2] | +2.0 | 1.47 | 0.2080 |
| politics | N | 2 | 144 | 12 | 8.3 | 6.6 | [3.5, 9.7] | +1.7 | 1.26 | 0.2017 |
| traditionalism | N | 2 | 154 | 9 | 5.8 | 3.6 | [1.3, 6.5] | +2.2 | 1.61 | 0.0938 |

## POPQUORN

| characteristic | type | n groups | testable | observed attributed | observed % | chance % | chance range | excess (pp) | ratio | p |
|---|---|---|---|---|---|---|---|---|---|---|
| gender | D | 2 | 615 | 14 | 2.3 | 2.6 | [1.5, 3.7] | -0.3 | 0.88 | 0.7435 |
| race | D | 2 | 204 | 13 | 6.4 | 4.3 | [2.0, 6.9] | +2.0 | 1.46 | 0.0895 |
| age | D | 2 | 583 | 55 | 9.4 | 8.5 | [7.0, 9.9] | +1.0 | 1.11 | 0.1243 |
| education | N | 3 | 591 | 47 | 8.0 | 6.2 | [4.4, 8.1] | +1.7 | 1.27 | 0.0482 |
| occupation | N | 5 | 418 | 54 | 12.9 | 12.6 | [9.8, 15.6] | +0.3 | 1.03 | 0.4384 |

## MHS

| characteristic | type | n groups | testable | observed attributed | observed % | chance % | chance range | excess (pp) | ratio | p |
|---|---|---|---|---|---|---|---|---|---|---|
| gender | D | 2 | 529 | 43 | 8.1 | 8.4 | [6.4, 10.4] | -0.3 | 0.97 | 0.6437 |
| age | D | 2 | 305 | 30 | 9.8 | 7.4 | [4.9, 9.8] | +2.4 | 1.33 | 0.0395 |
| ideology | N | 3 | 336 | 32 | 9.5 | 8.8 | [6.2, 11.3] | +0.7 | 1.08 | 0.3244 |

## Kumar

| characteristic | type | n groups | testable | observed attributed | observed % | chance % | chance range | excess (pp) | ratio | p |
|---|---|---|---|---|---|---|---|---|---|---|
| gender | D | 2 | 19436 | 1224 | 6.3 | 5.6 | [5.3, 5.9] | +0.7 | 1.12 | <0.0001 |
| race | D | 3 | 5727 | 667 | 11.7 | 7.5 | [6.9, 8.1] | +4.2 | 1.55 | <0.0001 |
| age | D | 3 | 11400 | 1038 | 9.1 | 8.7 | [8.2, 9.2] | +0.4 | 1.04 | 0.0548 |
| politics | N | 3 | 15584 | 1924 | 12.3 | 11.7 | [11.2, 12.2] | +0.6 | 1.05 | 0.0049 |
| religion | N | 2 | 15940 | 1237 | 7.8 | 5.5 | [5.2, 5.8] | +2.3 | 1.42 | <0.0001 |

## The gap (non-demographic minus demographic, percentage points)

Bootstrap: 10,000 resamples of the polarized texts (seed 42, as Table 3). In every resample the observed rates are recomputed and the chance rates are the mean of the exact chance probabilities of the resampled pairs.

| dataset | observed D % | observed N % | observed gap [range] | share <= 0 | chance D % | chance N % | excess gap [range] | share <= 0 |
|---|---|---|---|---|---|---|---|---|
| Attitudes | 6.0 | 7.0 | +1.1 [-2.4, +4.6] | 28.2% | 4.3 | 5.1 | +0.3 [-3.2, +3.9] | 44.5% |
| POPQUORN | 5.8 | 10.0 | +4.2 [+2.1, +6.3] | 0.0% | 5.3 | 8.9 | +0.6 [-1.4, +2.5] | 28.4% |
| MHS | 8.8 | 9.5 | +0.8 [-2.7, +4.3] | 34.1% | 8.1 | 8.8 | +0.0 [-3.5, +3.6] | 50.1% |
| Kumar | 8.0 | 10.0 | +2.0 [+1.6, +2.4] | 0.0% | 6.9 | 8.6 | +0.3 [-0.1, +0.8] | 6.7% |

## Spearman correlation over all characteristics and datasets

| measure | Spearman | characteristics |
|---|---|---|
| n_groups vs observed % | +0.572 | 18 |
| n_groups vs chance % | +0.572 | 18 |

## Checks

| dataset | polarized texts with >= 4 ratings | cases checked by brute force |
|---|---|---|
| Attitudes | 262 | 150 |
| POPQUORN | 684 | 150 |
| MHS | 1316 | 29 |
| Kumar | 38171 | 150 |

## Caveats

- Chance is computed with the groups retained by the paper's 10-text removal rule; the rule is not rerun on the assignments.
- An assignment keeps every group's size on every text, so a text with a group of one rating is never made testable or untestable; only which ratings fall in which group changes.
- A text with few ratings has few assignments (2 + 2 ratings: 5 besides the observed one), so its chance probability takes few values; it is exact, not noisy. Leaving the observed assignment out lowers the probability of an attributed text and raises that of a non-attributed one; the effect is largest for small texts (`chance_probability_with_observed` in the per-pair file has the value with it included).
- Splits of the ratings with a share below 1e-30 of the assignments are skipped (texts with hundreds of ratings only); their total is far below the precision shown.
- The bootstrap range of the excess gap treats the chance probabilities as fixed; they are exact, so there is no permutation noise to add.
- Characteristics with fewer than 15 testable texts (their chance range and p are coarse): none.
- The per-pair chance probabilities are in `per_pair_chance_probability.csv` (one row per testable text and characteristic, with the number of assignments as log10).
