# How sure are the alignment numbers? Bootstrap resampling of the attributed texts

Date: 2026-11-05

## Question
On the attributed (AU) texts we measure how well each model agrees with each annotator group (Cohen's kappa), whether it agrees more with one group than
another (gap), whether the persona prompt (SCD) changes the agreement (prompt change), and which side the model takes when the groups split (poles).
These are computed on few texts: 6 to 55 per characteristic, and only 10 per group for Kumar. How much would each number move with a different set of
texts, and which differences are larger than that movement?

## Design
For every dataset and characteristic, the unit is the **attributed text** (one text x characteristic row). For Kumar it is the evaluated sample of 65
rows (13 groups x 10).

1. **Resample the texts with replacement.** Draw n texts from the n attributed texts of the characteristic, each with probability 1/n per draw. A text can
   appear 0, 1, 2, ... times.
2. **Recompute everything on the resample:** every group, model and prompt, and from these every gap and prompt change. All quantities of a characteristic
   use **the same resamples**. A gap between two groups is therefore paired: both kappas are computed on the same drawn texts.
3. **Repeat B times** with a fixed seed (42). B is 1,000 for the group kappas, gaps and prompt changes (7.2, 7.3), and 10,000 for the persona matrix and the
   poles (7.3, 7.6). The first 1,000 of the 10,000 resamples are exactly the 1,000 used in 7.2 and 7.3, so all sections share the same draws.
4. **Summarise** the B values of each quantity: the standard error (SD), the 95% percentile interval, and the share of resamples below, at and above 0.

The observed number (the "point estimate") is always computed on the original texts; the bootstrap only gives its uncertainty.

### Example
A characteristic with 4 attributed texts {t1, t2, t3, t4}. One resample might be {t1, t1, t3, t4}: t1 counts twice and t2 is missing. It is stored as draw
counts per text, c = (2, 0, 1, 1). Every kappa of that resample is computed with these counts as weights. A group that is compared on t2 only would have no
text in this resample, so its kappa has no value there.

### Why repeats are allowed here (unlike the permutation null)
In the permutation null each assignment is equally likely, so taking each one once is the exact null. In a bootstrap, the resamples are **not** equally
likely: {t1, t2, t3, t4} (each once) has probability 4!/4^4 = 9.4%, while {t1, t1, t1, t1} has 1/4^4 = 0.4%. Drawing at random with replacement gives each
resample its correct probability, and a resample that is drawn twice is simply a likely one. Repeats are part of the method, not an error.

For very small characteristics, the number of distinct resamples is small, so repeats are frequent (see Scale). There an **exact bootstrap** is
possible: list every distinct resample once and weight it by its probability (the same idea as the weighting in the permutation null). It has not been done.

## Formulas
Notation for one characteristic: n attributed texts i = 1..n. For group g, s_ig = 1 if the group is compared on text i (its "presence"), y_ig = 1 if the
group's position on text i is toxic, and x_i = 1 if the model's label is toxic. A rating of 3 or more is toxic, for humans and models; for MHS the humans'
scale is 1-3 and only 3 is toxic. The group's position is the majority of its binary labels, with a tie decided by the group's mean rating.
For the SCD prompt, x_ig is the model's label as a person of group g.

**One resample** (b = 1..B): the draw counts

    c_b = (c_b1, ..., c_bn) ~ Multinomial(n; 1/n, ..., 1/n),      sum_i c_bi = n

    P(a resample with counts c) = n! / (c_1! c_2! ... c_n!) * n^(-n)
    distinct resamples = C(2n - 1, n)

The original texts are the weights c = (1, ..., 1).

**Cohen's kappa with weights** w_i = c_i * s_ig (only the texts where the group is compared):

    TT = sum w_i y_i x_i        TC = sum w_i y_i (1 - x_i)        CT = sum w_i (1 - y_i) x_i        CC = sum w_i (1 - y_i)(1 - x_i)
    W  = TT + TC + CT + CC

    p_o = (TT + CC) / W                                      observed agreement
    m   = (TT + CT) / W        g = (TT + TC) / W             share toxic: model, group
    p_e = m g + (1 - m)(1 - g)                               agreement expected by chance
    kappa = (p_o - p_e) / (1 - p_e)

- If m = 0 or m = 1 (the model gives one label to every text), kappa = 0 (`constant_model`). This also applies inside a resample.
- If W = 0 (the group has no text in the resample), kappa has no value. That resample is counted in `resamples_without_value` and left out.

**Gap** between groups A and B, and **prompt change** for group g (each per resample b, and on the original texts):

    gap_b    = kappa_b(A) - kappa_b(B)
    change_b = kappa_b(SCD, g) - kappa_b(default, g)

**Persona matrix** (SCD): the kappa of persona P's labels against group G's positions, on the texts where both are compared (w_i = c_i s_iP s_iG). The
diagonal P = G is the SCD kappa of the group. **Persona pairs**: the kappa between the labels of personas A and B on the same texts.

**Poles** (7.6). A text is split when at least one group is toxic and at least one is civil (z_i = 1). The share of split texts the model labels toxic is

    share_b = sum_i c_bi z_i x_i / sum_i c_bi z_i

The same formula, with the group's position in place of x_i, gives how often a group is at the toxic pole.

**Summaries** over the valid resamples (v_1..v_B', the values that exist):

    SE (sd)       = standard deviation of v_b (ddof = 1)
    95% interval  = [2.5th percentile, 97.5th percentile] of v_b
    share_lt0 / share_eq0 / share_gt0 = % of v_b < 0 / = 0 / > 0,      share_le0 = share_lt0 + share_eq0
    interval_excludes_zero = (ci_low > 0) or (ci_high < 0)

A difference is called **clear** when its 95% interval excludes 0. This is roughly a two-sided test at 5%, and share_le0 (or share_gt0) is roughly a
one-sided p-value. There is no correction for the number of comparisons.

**Mirrored characteristic**: two groups that take opposite sides on every text (y_iA = 1 - y_iB). Then kappa(A) = -kappa(B), and the gap is twice a kappa.

## Scale

Attributed texts per characteristic (the most any group has):

| dataset | characteristics (n texts) |
|---|---|
| Attitudes | gender 10, race 14, age 6, politics 12, traditionalism 9 |
| POPQUORN | gender 14, race 13, age 55, education 44, occupation 52 |
| MHS | gender 43, age 30, ideology 29 |
| Kumar | 10 per group in every characteristic (the sample) |

Distinct possible resamples, and how many of the drawn resamples repeat an earlier one (seed 42):

| n texts | distinct possible | repeats in 1,000 draws | repeats in 10,000 draws |
|---|---|---|---|
| 6 | 462 | 666 | 9,550 |
| 9 | 24,310 | 54 | 3,519 |
| 10 | 92,378 | 17 | 1,454 |
| 14 | 20,058,300 | 0 | 13 |
| 30 | 5.9 x 10^16 | 0 | 0 |
| 55 | 4.9 x 10^31 | 0 | 0 |

Repeats are expected and correct (see above). They matter only for the smallest characteristics (Attitudes age, n = 6), where only 462 resamples
exist and the interval can take only a few values. There an exact bootstrap would remove the random part entirely.

## Results

### Kappa of each group (176 group x model rows per prompt)

| dataset | mean kappa (default) | intervals above 0 (default) | mean kappa (SCD) | intervals above 0 (SCD) | constant model label (default / SCD) |
|---|---|---|---|---|---|
| Attitudes | 0.05 | 0 / 40 | 0.08 | 1 / 40 | 4 / 10 |
| POPQUORN | 0.15 | 6 / 56 | 0.13 | 10 / 56 | 0 / 0 |
| MHS | 0.01 | 0 / 28 | 0.04 | 0 / 28 | 7 / 13 |
| Kumar | 0.12 | 5 / 52 | 0.12 | 2 / 52 | 1 / 1 |

Agreement with the groups is low everywhere, with mean kappa between 0.0 and 0.15. Few groups have an interval clearly above 0.
In MHS, no group's interval lies above 0, and the models often give one label to every text, which gives kappa 0.

### Gaps between groups (148 pairs per prompt)

| dataset | clear gaps (default) | clear gaps (SCD) |
|---|---|---|
| Attitudes | 0 / 20 | 2 / 20 (race: black vs white, ChatGPT and Gemini) |
| POPQUORN | 13 / 64 (mostly occupation, Student vs the rest) | 12 / 64 (mostly occupation) |
| MHS | 0 / 20 | 0 / 20 |
| Kumar | 13 / 44 (politics: liberal vs the rest; age; race) | 5 / 44 (politics, age) |
| **all** | **26 / 148** | **19 / 148** |

With 148 comparisons and no correction, about 7 clear gaps per prompt would appear by luck alone (5%). Both prompts are above that, so some gaps are real.
They concentrate in two places: POPQUORN occupation (the Student group, 11 texts) and Kumar politics (liberal). Each of these involves groups with
10–11 texts, so the intervals are wide (often about ±0.5 to ±0.7). Kumar gender with Gemini (gap 2.0) is a mirrored characteristic: the model agrees fully
with one group and so disagrees fully with the other.

### Prompt change, SCD minus default (176 rows)

| dataset | mean change | changes above 0 | clear changes |
|---|---|---|---|
| Attitudes | +0.02 | 19 / 40 | 0 |
| POPQUORN | -0.02 | 20 / 56 | 1 |
| MHS | +0.04 | 11 / 28 | 0 |
| Kumar | -0.00 | 20 / 52 | 2 (Gemini gender, Female and Male: mirrored) |
| **all** | | | **3 / 176** |

There are 3 clear changes out of 176, fewer than the about 9 expected by luck alone. **The persona prompt does not change the agreement with the groups.**

### Persona matrix (SCD)
Does the persona of group G agree with group G better than the other personas do? Pooled over all characteristics and models, the diagonal cell is higher than
an off-diagonal cell in 131 of 280 comparisons (47%), tied in 58 and lower in 91. That is no better than a coin flip. The personas also answer alike:
45 of 148 persona pairs have kappa > 0.8, and the median is 0.47.

### Poles (default prompt; each distinct text once)
Share of split texts the model labels toxic, with its 95% interval:

| dataset | split texts | ChatGPT | DeepSeek | Gemini | Mistral |
|---|---|---|---|---|---|
| Attitudes | 32 | 75% [60, 89] | 84% [71, 97] | 84% [71, 97] | 81% [68, 94] |
| POPQUORN | 76 | 59% [48, 70] | 49% [37, 60] | 55% [44, 67] | 75% [65, 84] |
| MHS | 94 | 94% [88, 98] | 98% [95, 100] | 98% [95, 100] | 97% [93, 100] |
| Kumar | 46 | 52% [38, 66] | 48% [34, 62] | 57% [42, 70] | 63% [49, 77] |

When the groups split, the models side with the toxic pole in Attitudes and MHS (the interval is above 50% for all models), and with Mistral in POPQUORN.
In Kumar, and with the other models in POPQUORN, the interval includes 50%, so there is no clear side.

## Limits
- **No correction for multiple comparisons.** Each interval is a 95% interval on its own; across 148 gaps or 176 changes, about 5% clear by luck is expected.
  Holm or false discovery rate control would leave fewer clear results.
- **Small groups.** Kumar has 10 texts per group and Attitudes 6–14 per characteristic. With so few texts a kappa can jump between -1 and 1, and the
  percentile interval is coarse and may be biased. For n = 6 only 462 resamples exist.
- **The texts are the only source of uncertainty.** The models' answers are taken as fixed. Re-asking a model could change its labels, and that is not in
  the intervals. The humans' group positions are also taken as fixed.
- **Kumar is a sample** of 65 of its attributed rows. The intervals describe those 65, not all of Kumar.
- **Constant labels give kappa 0** by rule, which can make a model that always says "toxic" look like chance. This happens often in MHS, and in
  Attitudes under SCD.
- **Percentile intervals** are the simplest bootstrap interval. BCa or an exact bootstrap for the smallest characteristics would be more accurate there.
