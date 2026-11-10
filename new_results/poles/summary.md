# Alignment with the toxic and the civil pole (default prompt)

Split text = an attributed text where at least one group is toxic and at least one is civil. Bootstrap: 10,000 resamples of the texts, seed 42. † = the model gave one label to every attributed text of the characteristic. \* = fewer than 5 texts. Kumar: the sample given to the models. The row `all (distinct texts)` counts each distinct text once, split if it is split under at least one characteristic.

## 1. Kumar

**Alignment with the poles (default prompt)**

| characteristic | model | n attributed | n split | n same | model toxic / civil on split | share toxic on split (SD) [2.5–97.5] | share toxic on same |
|---|---|---|---|---|---|---|---|
| gender | ChatGPT | 50 | 47 | 3 | 26 / 21 | 55% (7) [41%, 70%] | 100% |
| gender | DeepSeek | 50 | 47 | 3 | 24 / 23 | 51% (7) [37%, 65%] | 100% |
| gender | Gemini | 50 | 47 | 3 | 23 / 24 | 49% (7) [35%, 63%] | 100% |
| gender | Mistral | 50 | 47 | 3 | 33 / 14 | 70% (7) [57%, 83%] | 100% |
| race | ChatGPT | 92 | 67 | 25 | 33 / 34 | 49% (6) [37%, 61%] | 48% |
| race | DeepSeek | 92 | 67 | 25 | 23 / 44 | 34% (6) [23%, 46%] | 44% |
| race | Gemini | 92 | 67 | 25 | 31 / 36 | 46% (6) [34%, 58%] | 40% |
| race | Mistral | 92 | 67 | 25 | 44 / 23 | 66% (6) [54%, 77%] | 64% |
| age | ChatGPT | 75 | 43 | 32 | 23 / 20 | 53% (8) [38%, 68%] | 34% |
| age | DeepSeek | 75 | 43 | 32 | 18 / 25 | 42% (8) [27%, 57%] | 25% |
| age | Gemini | 75 | 43 | 32 | 26 / 17 | 60% (7) [46%, 75%] | 28% |
| age | Mistral | 75 | 43 | 32 | 29 / 14 | 67% (7) [53%, 81%] | 47% |
| politics | ChatGPT | 75 | 42 | 33 | 25 / 17 | 60% (8) [44%, 74%] | 39% |
| politics | DeepSeek | 75 | 42 | 33 | 22 / 20 | 52% (8) [37%, 67%] | 33% |
| politics | Gemini | 75 | 42 | 33 | 22 / 20 | 52% (8) [37%, 67%] | 33% |
| politics | Mistral | 75 | 42 | 33 | 31 / 11 | 74% (7) [60%, 86%] | 61% |
| religion | ChatGPT | 50 | 48 | 2 | 23 / 25 | 48% (7) [34%, 62%] | 100% |
| religion | DeepSeek | 50 | 48 | 2 | 15 / 33 | 31% (7) [18%, 45%] | 100% |
| religion | Gemini | 50 | 48 | 2 | 22 / 26 | 46% (7) [32%, 60%] | 100% |
| religion | Mistral | 50 | 48 | 2 | 35 / 13 | 73% (6) [60%, 85%] | 100% |
| all (distinct texts) | ChatGPT | 340 | 245 | 95 | 130 / 115 | 53% (3) [47%, 59%] | 43% |
| all (distinct texts) | DeepSeek | 340 | 245 | 95 | 102 / 143 | 42% (3) [36%, 48%] | 37% |
| all (distinct texts) | Gemini | 340 | 245 | 95 | 124 / 121 | 51% (3) [44%, 57%] | 37% |
| all (distinct texts) | Mistral | 340 | 245 | 95 | 170 / 75 | 69% (3) [64%, 75%] | 59% |

**Which group holds each pole** (split texts where the group has a position)

| characteristic | group | n split texts | at toxic pole | at civil pole | toxic-pole share SD | [2.5–97.5] |
|---|---|---|---|---|---|---|
| gender | Female | 47 | 32% | 68% | 7 | [19%, 46%] |
| gender | Male | 47 | 68% | 32% | 7 | [54%, 81%] |
| race | Asian | 29 | 59% | 41% | 9 | [40%, 77%] |
| race | Black | 40 | 98% | 2% | 2 | [92%, 100%] |
| race | White | 65 | 17% | 83% | 5 | [8%, 27%] |
| age | gen x+ | 30 | 57% | 43% | 9 | [39%, 74%] |
| age | gen z | 22 | 41% | 59% | 11 | [21%, 62%] |
| age | millenial | 34 | 50% | 50% | 9 | [33%, 67%] |
| politics | conservative | 33 | 79% | 21% | 7 | [64%, 92%] |
| politics | independent | 27 | 30% | 70% | 9 | [12%, 48%] |
| politics | liberal | 24 | 33% | 67% | 10 | [15%, 54%] |
| religion | high | 48 | 90% | 10% | 4 | [80%, 98%] |
| religion | not_high | 48 | 10% | 90% | 4 | [2%, 20%] |

**Direction by group** (politics)

| characteristic | group | model | model toxic when group at toxic pole (n) | model civil when group at civil pole (n) |
|---|---|---|---|---|
| politics | conservative | ChatGPT | 54% (26) | 43% (7) |
| politics | conservative | DeepSeek | 38% (26) | 29% (7) |
| politics | conservative | Gemini | 38% (26) | 29% (7) |
| politics | conservative | Mistral | 73% (26) | 29% (7) |
| politics | independent | ChatGPT | 75% (8) | 47% (19) |
| politics | independent | DeepSeek | 75% (8) | 53% (19) |
| politics | independent | Gemini | 75% (8) | 53% (19) |
| politics | independent | Mistral | 88% (8) | 21% (19) |
| politics | liberal | ChatGPT | 62% (8) | 31% (16) |
| politics | liberal | DeepSeek | 75% (8) | 50% (16) |
| politics | liberal | Gemini | 75% (8) | 50% (16) |
| politics | liberal | Mistral | 62% (8) | 31% (16) |

## 2. Other datasets

### attitudes

**Alignment with the poles (default prompt)**

| characteristic | model | n attributed | n split | n same | model toxic / civil on split | share toxic on split (SD) [2.5–97.5] | share toxic on same |
|---|---|---|---|---|---|---|---|
| gender | ChatGPT | 10 | 10 | 0 | 8 / 2 | 80% (13) [50%, 100%] | – |
| gender | DeepSeek | 10 | 10 | 0 | 10 / 0 | 100%† (0) [100%, 100%] | – |
| gender | Gemini | 10 | 10 | 0 | 10 / 0 | 100%† (0) [100%, 100%] | – |
| gender | Mistral | 10 | 10 | 0 | 9 / 1 | 90% (10) [70%, 100%] | – |
| race | ChatGPT | 14 | 11 | 3 | 7 / 4 | 64% (15) [33%, 91%] | 67% |
| race | DeepSeek | 14 | 11 | 3 | 8 / 3 | 73% (14) [44%, 100%] | 67% |
| race | Gemini | 14 | 11 | 3 | 8 / 3 | 73% (14) [44%, 100%] | 100% |
| race | Mistral | 14 | 11 | 3 | 9 / 2 | 82% (12) [56%, 100%] | 100% |
| age | ChatGPT | 6 | 4 | 2 | 3 / 1 | 75% (23) [25%, 100%] | 50% |
| age | DeepSeek | 6 | 4 | 2 | 4 / 0 | 100% (0) [100%, 100%] | 0% |
| age | Gemini | 6 | 4 | 2 | 3 / 1 | 75% (23) [25%, 100%] | 50% |
| age | Mistral | 6 | 4 | 2 | 3 / 1 | 75% (23) [25%, 100%] | 100% |
| politics | ChatGPT | 12 | 6 | 6 | 5 / 1 | 83% (16) [50%, 100%] | 67% |
| politics | DeepSeek | 12 | 6 | 6 | 5 / 1 | 83% (16) [50%, 100%] | 67% |
| politics | Gemini | 12 | 6 | 6 | 6 / 0 | 100% (0) [100%, 100%] | 83% |
| politics | Mistral | 12 | 6 | 6 | 4 / 2 | 67% (20) [25%, 100%] | 100% |
| traditionalism | ChatGPT | 9 | 7 | 2 | 6 / 1 | 86% (13) [57%, 100%] | 50% |
| traditionalism | DeepSeek | 9 | 7 | 2 | 6 / 1 | 86% (13) [57%, 100%] | 50% |
| traditionalism | Gemini | 9 | 7 | 2 | 6 / 1 | 86% (13) [57%, 100%] | 100% |
| traditionalism | Mistral | 9 | 7 | 2 | 6 / 1 | 86% (13) [57%, 100%] | 100% |
| all (distinct texts) | ChatGPT | 41 | 32 | 9 | 24 / 8 | 75% (8) [60%, 89%] | 78% |
| all (distinct texts) | DeepSeek | 41 | 32 | 9 | 27 / 5 | 84% (6) [71%, 97%] | 67% |
| all (distinct texts) | Gemini | 41 | 32 | 9 | 27 / 5 | 84% (6) [71%, 97%] | 78% |
| all (distinct texts) | Mistral | 41 | 32 | 9 | 26 / 6 | 81% (7) [68%, 94%] | 100% |

**Which group holds each pole** (split texts where the group has a position)

| characteristic | group | n split texts | at toxic pole | at civil pole | toxic-pole share SD | [2.5–97.5] |
|---|---|---|---|---|---|---|
| gender | man | 10 | 50% | 50% | 16 | [20%, 80%] |
| gender | woman | 10 | 50% | 50% | 16 | [20%, 80%] |
| race | black | 11 | 82% | 18% | 12 | [57%, 100%] |
| race | white | 11 | 18% | 82% | 12 | [0%, 43%] |
| age | gen x+ | 4 | 25% | 75% | 23 | [0%, 75%] |
| age | millenial | 4 | 75% | 25% | 23 | [25%, 100%] |
| politics | left | 6 | 50% | 50% | 22 | [0%, 100%] |
| politics | right | 6 | 50% | 50% | 22 | [0%, 100%] |
| traditionalism | high | 7 | 57% | 43% | 19 | [17%, 89%] |
| traditionalism | not_high | 7 | 43% | 57% | 19 | [11%, 83%] |

**Direction by group** (politics)

| characteristic | group | model | model toxic when group at toxic pole (n) | model civil when group at civil pole (n) |
|---|---|---|---|---|
| politics | left | ChatGPT | 100% (3)* | 33% (3)* |
| politics | left | DeepSeek | 100% (3)* | 33% (3)* |
| politics | left | Gemini | 100% (3)* | 0% (3)* |
| politics | left | Mistral | 100% (3)* | 67% (3)* |
| politics | right | ChatGPT | 67% (3)* | 0% (3)* |
| politics | right | DeepSeek | 67% (3)* | 0% (3)* |
| politics | right | Gemini | 100% (3)* | 0% (3)* |
| politics | right | Mistral | 33% (3)* | 0% (3)* |

### popquorn

**Alignment with the poles (default prompt)**

| characteristic | model | n attributed | n split | n same | model toxic / civil on split | share toxic on split (SD) [2.5–97.5] | share toxic on same |
|---|---|---|---|---|---|---|---|
| gender | ChatGPT | 14 | 11 | 3 | 7 / 4 | 64% (15) [33%, 91%] | 33% |
| gender | DeepSeek | 14 | 11 | 3 | 6 / 5 | 55% (15) [25%, 83%] | 33% |
| gender | Gemini | 14 | 11 | 3 | 6 / 5 | 55% (15) [25%, 83%] | 33% |
| gender | Mistral | 14 | 11 | 3 | 9 / 2 | 82% (12) [56%, 100%] | 67% |
| race | ChatGPT | 13 | 12 | 1 | 6 / 6 | 50% (14) [23%, 77%] | 0% |
| race | DeepSeek | 13 | 12 | 1 | 4 / 8 | 33% (14) [8%, 62%] | 0% |
| race | Gemini | 13 | 12 | 1 | 9 / 3 | 75% (12) [50%, 100%] | 0% |
| race | Mistral | 13 | 12 | 1 | 9 / 3 | 75% (12) [50%, 100%] | 0% |
| age | ChatGPT | 55 | 22 | 33 | 14 / 8 | 64% (10) [43%, 83%] | 39% |
| age | DeepSeek | 55 | 22 | 33 | 11 / 11 | 50% (11) [29%, 71%] | 21% |
| age | Gemini | 55 | 22 | 33 | 13 / 9 | 59% (11) [38%, 80%] | 21% |
| age | Mistral | 55 | 22 | 33 | 17 / 5 | 77% (9) [58%, 94%] | 52% |
| education | ChatGPT | 47 | 25 | 22 | 13 / 12 | 52% (10) [32%, 71%] | 18% |
| education | DeepSeek | 47 | 25 | 22 | 11 / 14 | 44% (10) [25%, 64%] | 18% |
| education | Gemini | 47 | 25 | 22 | 11 / 14 | 44% (10) [25%, 64%] | 23% |
| education | Mistral | 47 | 25 | 22 | 17 / 8 | 68% (9) [48%, 86%] | 41% |
| occupation | ChatGPT | 54 | 17 | 37 | 11 / 6 | 65% (12) [41%, 88%] | 38% |
| occupation | DeepSeek | 54 | 17 | 37 | 10 / 7 | 59% (12) [33%, 82%] | 30% |
| occupation | Gemini | 54 | 17 | 37 | 12 / 5 | 71% (11) [47%, 92%] | 32% |
| occupation | Mistral | 54 | 17 | 37 | 15 / 2 | 88% (8) [71%, 100%] | 54% |
| all (distinct texts) | ChatGPT | 154 | 76 | 78 | 45 / 31 | 59% (6) [48%, 70%] | 33% |
| all (distinct texts) | DeepSeek | 154 | 76 | 78 | 37 / 39 | 49% (6) [37%, 60%] | 23% |
| all (distinct texts) | Gemini | 154 | 76 | 78 | 42 / 34 | 55% (6) [44%, 67%] | 24% |
| all (distinct texts) | Mistral | 154 | 76 | 78 | 57 / 19 | 75% (5) [65%, 84%] | 49% |

**Which group holds each pole** (split texts where the group has a position)

| characteristic | group | n split texts | at toxic pole | at civil pole | toxic-pole share SD | [2.5–97.5] |
|---|---|---|---|---|---|---|
| gender | Man | 11 | 45% | 55% | 15 | [17%, 75%] |
| gender | Woman | 11 | 55% | 45% | 15 | [25%, 83%] |
| race | Black or African American | 12 | 92% | 8% | 8 | [73%, 100%] |
| race | White | 12 | 8% | 92% | 8 | [0%, 27%] |
| age | gen x+ | 22 | 73% | 27% | 10 | [53%, 90%] |
| age | millenial | 22 | 27% | 73% | 10 | [10%, 47%] |
| education | College degree | 23 | 39% | 61% | 10 | [19%, 60%] |
| education | Graduate degree | 14 | 71% | 29% | 12 | [45%, 93%] |
| education | High school diploma or equivalent | 18 | 39% | 61% | 12 | [17%, 62%] |
| occupation | Employed | 17 | 71% | 29% | 11 | [47%, 92%] |
| occupation | Retired | 3 | 67% | 33% | 31 | [0%, 100%] |
| occupation | Self-employed | 7 | 0% | 100% | 0 | [0%, 0%] |
| occupation | Student | 5 | 60% | 40% | 25 | [0%, 100%] |
| occupation | Unemployed | 4 | 25% | 75% | 24 | [0%, 100%] |

**Direction by group** (gender, race, age, education, occupation)

| characteristic | group | model | model toxic when group at toxic pole (n) | model civil when group at civil pole (n) |
|---|---|---|---|---|
| gender | Man | ChatGPT | 60% (5) | 33% (6) |
| gender | Man | DeepSeek | 40% (5) | 33% (6) |
| gender | Man | Gemini | 40% (5) | 33% (6) |
| gender | Man | Mistral | 60% (5) | 0% (6) |
| gender | Woman | ChatGPT | 67% (6) | 40% (5) |
| gender | Woman | DeepSeek | 67% (6) | 60% (5) |
| gender | Woman | Gemini | 67% (6) | 60% (5) |
| gender | Woman | Mistral | 100% (6) | 40% (5) |
| race | Black or African American | ChatGPT | 55% (11) | 100% (1)* |
| race | Black or African American | DeepSeek | 36% (11) | 100% (1)* |
| race | Black or African American | Gemini | 73% (11) | 0% (1)* |
| race | Black or African American | Mistral | 73% (11) | 0% (1)* |
| race | White | ChatGPT | 0% (1)* | 45% (11) |
| race | White | DeepSeek | 0% (1)* | 64% (11) |
| race | White | Gemini | 100% (1)* | 27% (11) |
| race | White | Mistral | 100% (1)* | 27% (11) |
| age | gen x+ | ChatGPT | 56% (16) | 17% (6) |
| age | gen x+ | DeepSeek | 50% (16) | 50% (6) |
| age | gen x+ | Gemini | 50% (16) | 17% (6) |
| age | gen x+ | Mistral | 81% (16) | 33% (6) |
| age | millenial | ChatGPT | 83% (6) | 44% (16) |
| age | millenial | DeepSeek | 50% (6) | 50% (16) |
| age | millenial | Gemini | 83% (6) | 50% (16) |
| age | millenial | Mistral | 67% (6) | 19% (16) |
| education | College degree | ChatGPT | 56% (9) | 43% (14) |
| education | College degree | DeepSeek | 44% (9) | 50% (14) |
| education | College degree | Gemini | 56% (9) | 64% (14) |
| education | College degree | Mistral | 89% (9) | 36% (14) |
| education | Graduate degree | ChatGPT | 50% (10) | 25% (4)* |
| education | Graduate degree | DeepSeek | 50% (10) | 75% (4)* |
| education | Graduate degree | Gemini | 20% (10) | 25% (4)* |
| education | Graduate degree | Mistral | 50% (10) | 25% (4)* |
| education | High school diploma or equivalent | ChatGPT | 43% (7) | 55% (11) |
| education | High school diploma or equivalent | DeepSeek | 29% (7) | 64% (11) |
| education | High school diploma or equivalent | Gemini | 57% (7) | 55% (11) |
| education | High school diploma or equivalent | Mistral | 71% (7) | 27% (11) |
| occupation | Employed | ChatGPT | 67% (12) | 40% (5) |
| occupation | Employed | DeepSeek | 67% (12) | 60% (5) |
| occupation | Employed | Gemini | 83% (12) | 60% (5) |
| occupation | Employed | Mistral | 92% (12) | 20% (5) |
| occupation | Retired | ChatGPT | 100% (2)* | 100% (1)* |
| occupation | Retired | DeepSeek | 100% (2)* | 0% (1)* |
| occupation | Retired | Gemini | 100% (2)* | 100% (1)* |
| occupation | Retired | Mistral | 100% (2)* | 0% (1)* |
| occupation | Self-employed | ChatGPT | – (0)* | 29% (7) |
| occupation | Self-employed | DeepSeek | – (0)* | 29% (7) |
| occupation | Self-employed | Gemini | – (0)* | 14% (7) |
| occupation | Self-employed | Mistral | – (0)* | 0% (7) |
| occupation | Student | ChatGPT | 33% (3)* | 0% (2)* |
| occupation | Student | DeepSeek | 0% (3)* | 0% (2)* |
| occupation | Student | Gemini | 0% (3)* | 0% (2)* |
| occupation | Student | Mistral | 67% (3)* | 0% (2)* |
| occupation | Unemployed | ChatGPT | 100% (1)* | 33% (3)* |
| occupation | Unemployed | DeepSeek | 100% (1)* | 67% (3)* |
| occupation | Unemployed | Gemini | 100% (1)* | 0% (3)* |
| occupation | Unemployed | Mistral | 100% (1)* | 33% (3)* |

### mhs

**Alignment with the poles (default prompt)**

| characteristic | model | n attributed | n split | n same | model toxic / civil on split | share toxic on split (SD) [2.5–97.5] | share toxic on same |
|---|---|---|---|---|---|---|---|
| gender | ChatGPT | 43 | 43 | 0 | 38 / 5 | 88% (5) [79%, 98%] | – |
| gender | DeepSeek | 43 | 43 | 0 | 41 / 2 | 95% (3) [88%, 100%] | – |
| gender | Gemini | 43 | 43 | 0 | 41 / 2 | 95% (3) [88%, 100%] | – |
| gender | Mistral | 43 | 43 | 0 | 41 / 2 | 95% (3) [88%, 100%] | – |
| age | ChatGPT | 30 | 30 | 0 | 28 / 2 | 93% (5) [83%, 100%] | – |
| age | DeepSeek | 30 | 30 | 0 | 29 / 1 | 97% (3) [90%, 100%] | – |
| age | Gemini | 30 | 30 | 0 | 30 / 0 | 100%† (0) [100%, 100%] | – |
| age | Mistral | 30 | 30 | 0 | 29 / 1 | 97% (3) [90%, 100%] | – |
| ideology | ChatGPT | 32 | 30 | 2 | 29 / 1 | 97% (3) [89%, 100%] | 50% |
| ideology | DeepSeek | 32 | 30 | 2 | 30 / 0 | 100%† (0) [100%, 100%] | 100% |
| ideology | Gemini | 32 | 30 | 2 | 30 / 0 | 100% (0) [100%, 100%] | 50% |
| ideology | Mistral | 32 | 30 | 2 | 29 / 1 | 97% (3) [89%, 100%] | 100% |
| all (distinct texts) | ChatGPT | 95 | 94 | 1 | 88 / 6 | 94% (3) [88%, 98%] | 0% |
| all (distinct texts) | DeepSeek | 95 | 94 | 1 | 92 / 2 | 98% (1) [95%, 100%] | 100% |
| all (distinct texts) | Gemini | 95 | 94 | 1 | 92 / 2 | 98% (1) [95%, 100%] | 0% |
| all (distinct texts) | Mistral | 95 | 94 | 1 | 91 / 3 | 97% (2) [93%, 100%] | 100% |

**Which group holds each pole** (split texts where the group has a position)

| characteristic | group | n split texts | at toxic pole | at civil pole | toxic-pole share SD | [2.5–97.5] |
|---|---|---|---|---|---|---|
| gender | female | 43 | 70% | 30% | 7 | [56%, 84%] |
| gender | male | 43 | 30% | 70% | 7 | [16%, 44%] |
| age | gen x+ | 30 | 73% | 27% | 8 | [57%, 87%] |
| age | millenial | 30 | 27% | 73% | 8 | [13%, 43%] |
| ideology | conservative | 21 | 71% | 29% | 10 | [50%, 90%] |
| ideology | liberal | 28 | 43% | 57% | 9 | [25%, 61%] |
| ideology | neutral | 11 | 27% | 73% | 14 | [0%, 56%] |

**Direction by group** (ideology)

| characteristic | group | model | model toxic when group at toxic pole (n) | model civil when group at civil pole (n) |
|---|---|---|---|---|
| ideology | conservative | ChatGPT | 93% (15) | 0% (6) |
| ideology | conservative | DeepSeek | 100% (15) | 0% (6) |
| ideology | conservative | Gemini | 100% (15) | 0% (6) |
| ideology | conservative | Mistral | 93% (15) | 0% (6) |
| ideology | liberal | ChatGPT | 100% (12) | 6% (16) |
| ideology | liberal | DeepSeek | 100% (12) | 0% (16) |
| ideology | liberal | Gemini | 100% (12) | 0% (16) |
| ideology | liberal | Mistral | 100% (12) | 6% (16) |
| ideology | neutral | ChatGPT | 100% (3)* | 0% (8) |
| ideology | neutral | DeepSeek | 100% (3)* | 0% (8) |
| ideology | neutral | Gemini | 100% (3)* | 0% (8) |
| ideology | neutral | Mistral | 100% (3)* | 0% (8) |

## 3. Caveats

n split per characteristic (attributed texts in brackets):

| dataset | characteristic | n split | n attributed |
|---|---|---|---|
| attitudes | gender | 10 | 10 |
| attitudes | race | 11 | 14 |
| attitudes | age | 4 | 6 |
| attitudes | politics | 6 | 12 |
| attitudes | traditionalism | 7 | 9 |
| attitudes | all (distinct texts) | 32 | 41 |
| popquorn | gender | 11 | 14 |
| popquorn | race | 12 | 13 |
| popquorn | age | 22 | 55 |
| popquorn | education | 25 | 47 |
| popquorn | occupation | 17 | 54 |
| popquorn | all (distinct texts) | 76 | 154 |
| mhs | gender | 43 | 43 |
| mhs | age | 30 | 30 |
| mhs | ideology | 30 | 32 |
| mhs | all (distinct texts) | 94 | 95 |
| kumar | gender | 47 | 50 |
| kumar | race | 67 | 92 |
| kumar | age | 43 | 75 |
| kumar | politics | 42 | 75 |
| kumar | religion | 48 | 50 |
| kumar | all (distinct texts) | 245 | 340 |

- Direction cells with fewer than 5 texts: 104 of 352 (4 with no text).
- Models that gave one label to every attributed text of a characteristic (share toxic on split is then 0% or 100%):
  - attitudes/gender: DeepSeek (toxic)
  - attitudes/gender: Gemini (toxic)
  - mhs/age: Gemini (toxic)
  - mhs/ideology: DeepSeek (toxic)
- Characteristics with no split text: none.
- Attributed rows per dataset: attitudes 51, popquorn 183, mhs 105, kumar 342; checked against the expected counts when the tables are computed.
