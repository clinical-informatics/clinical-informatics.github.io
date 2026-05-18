# Track 03: Null values and missingness

A blank cell is not zero. A blank cell is not normal. A blank cell is a question, and the answer determines what every downstream analysis is allowed to assume.

This track works that question. Five pieces:

1. **What a null actually is.** Across the systems you touch (pandas, SQL, FHIR, the export your CDW gives you), null is not one thing. It is at least four things, and the differences matter.
2. **The four causes of missing data in clinical extracts.** Why the cell ended up empty. Telling them apart is the substrate for everything that follows.
3. **MCAR, MAR, MNAR.** The classic framework from Rubin's 1976 paper, in plain English. Each with a real clinical example. Each shown on a slider so the bias is visible.
4. **Imputation.** The menu of options: mean/median, LOCF, regression, multiple imputation (MICE), and the "don't impute, flag it" option. What each one assumes, when each works, and the bias each one creates when its assumption is wrong.
5. **Drop or keep?** When to drop a row (complete-case analysis), when to drop a column, when to keep a missing column as itself (missingness as a feature), and how to make the call defensibly.

The interactive piece is two parts:
- A slider and three missingness mechanisms, showing the bias each produces on a synthetic RA cohort with a known true mean.
- An imputation menu applied to the same biased data, showing which methods recover the truth and which do not.


**Prerequisites:** Tracks 01 and 02 of this course. The missingness framework assumes the columns are correctly typed (Track 01) and the table is tidy (Track 02). An "empty cell" in a wide-format repeating-groups column is a structural placeholder, not a missing value. That is a Track 02 problem.

**Companion reading:** `03.1-missingness.md` in this folder.

**What's next:** Track 04 on joins. Joins are where missingness multiplies: a left-joined table has missing rows on the right side, and figuring out whether those nulls are MCAR or MNAR is the same framework applied to a different shape of data.
