# Is attribution more than luck? The exact permutation null

Date: 2026-11-05

## Question
A characteristic with more groups has smaller groups on each text, and a small group passes the unimodality test more easily. So part of the AU
attribution rate of a characteristic, and part of the gap between non-demographic and demographic characteristics, may be luck. How much of each
remains once luck is removed?

## Design
Null hypothesis: the rating a rater gives does not depend on the rater's group.

For every characteristic and every testable text (a polarized text with at least 4 ratings, counting only the groups kept by the 10-text rule):

1. **Keep everything except the link between rating and group.** The text's ratings stay the same, and so does the size of every group on the text.
2. **Take every other possible assignment of the raters to the groups, once each.** The observed (starting) assignment is left out.
   Example: 2 men + 2 women (raters a, b, c, d). The "men" can be {a,b}, {a,c}, {a,d}, {b,c}, {b,d}, {c,d}: 6 assignments, so **5 besides the observed one**.
3. **Run the AU test on each assignment** with the same rules as the paper: a group needs at least 2 ratings, at least 2 such groups are needed, and
   every such group must be unimodal.
4. **Chance probability of the text** = the share of those assignments in which the text is attributed.
5. **Combine the texts:** compare the chance rate of each characteristic, and the gap computed from the chance rates, with what is observed.

The null is exact: no assignment is drawn twice, none is missed, and nothing is random apart from the bootstrap of the gap.

Each characteristic is tested separately, and the thin-group removal rule is not rerun. Because the group sizes are fixed, a text that is testable
stays testable in every assignment.

## Counting assignments by their histograms (weighting)
The test only sees each group's histogram, so many assignments give the same result. Each distinct split of the rating values among the groups is
tested once and counted as many times as there are rater assignments that produce it (its weight). This is identical to listing every assignment.

Example: ratings 1, 1, 5, 5 in two groups of 2 (6 assignments):

| group A | group B | assignments | attributed? |
|---|---|---|---|
| {1,1} | {5,5} | 1 | yes |
| {5,5} | {1,1} | 1 | yes |
| {1,5} | {1,5} | 4 | no ({1,5} is not unimodal) |

Weighted: 2/6 = 33%, which is correct. Counting each row once instead would give 2/3, which is wrong.

## Formulas
Notation: a text has N ratings, with histogram c = (c_1, ..., c_V) over the scale values 1..V, and G groups of sizes n_1, ..., n_G. A split gives group g
the histogram h_g, with sum_g h_g = c and sum_v h_gv = n_g.

**Number of assignments** of a text:

    T = N! / (n_1! n_2! ... n_G!)

**Weight of a split** (the raters with value v are dealt among the groups):

    w(h) = prod_v [ c_v! / (h_1v! h_2v! ... h_Gv!) ]          and  sum over all splits of w(h) = T

Equivalently, group by group, the share of the remaining assignments in which group g gets h_g (multivariate hypergeometric), where r = the ratings
still left:

    share(h_g | r) = prod_v C(r_v, h_gv) / C(sum_v r_v, n_g)          (C = binomial coefficient; the last group takes what is left)

**Unimodal** (DFU = 0) for a histogram h_1..h_V: let k be the first position of the maximum. Then there is no rise after k (h_{j+1} <= h_j for j >= k)
and no fall before k (h_{j+1} >= h_j for j < k). Equal neighbours are not a rise or a fall. On a 3-point scale, (a, b, c) fails only when b < min(a, c).

**Attributed** (for one assignment): the text is testable, meaning at least 2 groups have n_g >= 2, and every group with n_g >= 2 is unimodal. Groups with
1 rating are not tested, but they still receive a rating.

**Share of attributed assignments** (observed included):

    P = sum over splits of w(h) * 1[attributed(h)] / T

**Chance probability of text i**, with the observed assignment left out (o_i = 1 if the observed text is attributed, else 0):

    q_i = (P_i * T_i - o_i) / (T_i - 1)  =  P_i + (P_i - o_i) / (T_i - 1)

**Per characteristic** (n testable texts, k observed attributed texts):

    chance %   = 100 * sum_i q_i / n
    observed % = 100 * k / n
    excess     = observed % - chance %          (percentage points)
    ratio      = observed % / chance %

**Null distribution** of the number X of attributed texts (Poisson-binomial, the texts are independent). It starts with pmf_0 = [1] and adds one text at a time:

    pmf_i(x) = pmf_{i-1}(x) * (1 - q_i) + pmf_{i-1}(x - 1) * q_i

    p            = P(X >= k) = sum_{x >= k} pmf_n(x)
    chance range = [100 * x_2.5 / n, 100 * x_97.5 / n],   where x_a = the smallest x with P(X <= x) >= a / 100

**Gap** (D = demographic: gender, race, age; N = the rest). The sums run over the (text, characteristic) pairs of each type:

    observed rate_D = attributed_D / testable_D         chance rate_D = sum q (pairs of type D) / testable_D      (the same for N)
    observed gap    = observed rate_N - observed rate_D
    excess gap      = (observed rate_N - chance rate_N) - (observed rate_D - chance rate_D)

Bootstrap: 10,000 resamples of the polarized texts with replacement (seed 42, the same draws as Table 3). The rates are recomputed in each resample.
The range is the 2.5–97.5 percentiles, and "share <= 0" is the share of resamples with a gap <= 0. The q_i are exact, so they stay fixed in the bootstrap.

**Holm correction** (18 characteristics): sort the p-values p_(1) <= ... <= p_(m), with m = 18. Reject p_(j) while p_(j) <= 0.05 / (m - j + 1), and stop
at the first one that fails. For example, the 4th smallest p-value must be <= 0.05 / 15 = 0.0033.

**Spearman correlation**: the rank correlation of the number of groups with the observed % and with the chance %, over the 18 characteristics.

## Scale of the enumeration
- **Attitudes** and **Kumar** (at most 6 ratings per text): at most about 10 assignments per text, so 5 to 30 alternatives.
- **POPQUORN** (at most 10 ratings): up to about 10^5 assignments per text (occupation, 5 groups).
- **MHS**: up to 774 ratings per text, and up to about 10^327 assignments (ideology, 3 groups).

These are only feasible by counting histograms with weights. Splits with a share below 1e-30 are skipped; their total is far below the precision reported.

A text with few ratings has few alternatives (2 + 2 ratings: 5), so its chance probability takes few values. It is exact, not noisy.

The weighted counting was checked against a full listing of every assignment on 479 small real cases and 300 random cases. All gave identical results.

## Results

### Per characteristic

| dataset | characteristic | type | groups | testable | observed % | chance % | chance range | excess (pp) | ratio | p |
|---|---|---|---|---|---|---|---|---|---|---|
| Attitudes | gender | D | 2 | 164 | 6.1 | 3.9 | [1.2, 6.7] | +2.2 | 1.57 | 0.088 |
| Attitudes | race | D | 2 | 239 | 5.9 | 4.6 | [2.5, 7.1] | +1.2 | 1.26 | 0.201 |
| Attitudes | age | D | 3 | 97 | 6.2 | 4.2 | [1.0, 8.2] | +2.0 | 1.47 | 0.208 |
| Attitudes | politics | N | 2 | 144 | 8.3 | 6.6 | [3.5, 9.7] | +1.7 | 1.26 | 0.202 |
| Attitudes | traditionalism | N | 2 | 154 | 5.8 | 3.6 | [1.3, 6.5] | +2.2 | 1.61 | 0.094 |
| POPQUORN | gender | D | 2 | 615 | 2.3 | 2.6 | [1.5, 3.7] | -0.3 | 0.88 | 0.744 |
| POPQUORN | race | D | 2 | 204 | 6.4 | 4.3 | [2.0, 6.9] | +2.0 | 1.46 | 0.090 |
| POPQUORN | age | D | 2 | 583 | 9.4 | 8.5 | [7.0, 9.9] | +1.0 | 1.11 | 0.124 |
| POPQUORN | education | N | 3 | 591 | 8.0 | 6.2 | [4.4, 8.1] | +1.7 | 1.27 | 0.048 |
| POPQUORN | occupation | N | 5 | 418 | 12.9 | 12.6 | [9.8, 15.6] | +0.3 | 1.03 | 0.438 |
| MHS | gender | D | 2 | 529 | 8.1 | 8.4 | [6.4, 10.4] | -0.3 | 0.97 | 0.644 |
| MHS | age | D | 2 | 305 | 9.8 | 7.4 | [4.9, 9.8] | +2.4 | 1.33 | 0.040 |
| MHS | ideology | N | 3 | 336 | 9.5 | 8.8 | [6.2, 11.3] | +0.7 | 1.08 | 0.324 |
| Kumar | gender | D | 2 | 19436 | 6.3 | 5.6 | [5.3, 5.9] | +0.7 | 1.12 | <0.0001 |
| Kumar | race | D | 3 | 5727 | 11.7 | 7.5 | [6.9, 8.1] | +4.2 | 1.55 | <0.0001 |
| Kumar | age | D | 3 | 11400 | 9.1 | 8.7 | [8.2, 9.2] | +0.4 | 1.04 | 0.055 |
| Kumar | politics | N | 3 | 15584 | 12.3 | 11.7 | [11.2, 12.2] | +0.6 | 1.05 | 0.005 |
| Kumar | religion | N | 2 | 15940 | 7.8 | 5.5 | [5.2, 5.8] | +2.3 | 1.42 | <0.0001 |

### Luck or not
- **More than luck** (after the Holm correction): Kumar gender, race, religion. The effects are small: race +4.2 pp, religion +2.3 pp, gender +0.7 pp
  (gender is significant only because Kumar is large).
- **Borderline** (p < 0.05 alone, not after the correction): POPQUORN education, MHS age, Kumar politics.
- **Consistent with luck:** everything else. Attitudes shows about +2 pp over chance on most characteristics, but it has too few texts to tell that
  apart from chance. The right wording is "not distinguishable from chance", not "proven chance".

### The gap (non-demographic minus demographic, pp)

| dataset | observed D % | observed N % | observed gap [range] | chance D % | chance N % | excess gap [range] | share <= 0 |
|---|---|---|---|---|---|---|---|
| Attitudes | 6.0 | 7.0 | +1.1 [-2.4, +4.6] | 4.3 | 5.1 | +0.3 [-3.2, +3.9] | 44.5% |
| POPQUORN | 5.8 | 10.0 | +4.2 [+2.1, +6.3] | 5.3 | 8.9 | +0.6 [-1.4, +2.5] | 28.4% |
| MHS | 8.8 | 9.5 | +0.8 [-2.7, +4.3] | 8.1 | 8.8 | +0.0 [-3.5, +3.6] | 50.1% |
| Kumar | 8.0 | 10.0 | +2.0 [+1.6, +2.4] | 6.9 | 8.6 | +0.3 [-0.1, +0.8] | 6.7% |

The gap is luck in all four datasets. The raw gaps in POPQUORN (+4.2) and Kumar (+2.0) are significant, but almost all of each is reproduced by
chance. They come from the composition of the groups (more groups, so smaller groups, which pass the test more easily), not from real attribution.

The number of groups correlates equally with the observed rate and with the chance rate: Spearman +0.572 for both.

### Compared with the earlier version (1,000 random shuffles)
The conclusions are the same.
- Chance rates are 0–0.4 pp lower, because leaving out the observed assignment removes one attributed case from every attributed text.
- The p-values are slightly smaller. The old ones could not go below 1/1001.
- POPQUORN education (0.059 → 0.048) and MHS age (0.081 → 0.040) move just under 0.05, but neither survives the correction.
- Excess gaps: +0.2 / +0.5 / +0.0 / +0.3 before, +0.3 / +0.6 / +0.0 / +0.3 now.

## Limits
- Chance uses the groups retained by the 10-text removal rule; the rule is not rerun on the alternative assignments.
- The texts are treated as independent, so the null distribution of a characteristic is a Poisson-binomial.
- Leaving out the observed assignment matters most for small texts. With it included, the chance probabilities are slightly higher. That version
  was not run, but it should sit between the earlier shuffle results and these.
