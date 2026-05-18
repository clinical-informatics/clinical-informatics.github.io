# Track 01: Data types and why they matter

A column's data type determines what operations it supports. CRP stored as the number `42.1` is a measurement that averages to 22.4 mg/L across a cohort. CRP stored as the text `"42.1"` is a label that looks like a number and breaks the calculation. Both look identical in the spreadsheet view.

Type mismatches are a leading cause of quietly wrong clinical analyses. The code rarely throws an error. Means come out plausibly. Charts look fine. The clinical conclusion is slightly off, and the chain of evidence does not point at the type.

This track works the problem in four pieces:

1. **The four data types that matter in clinical work.** Numbers, text, dates, and categorical codes. What goes where, and what each one is for.
2. **Dates and their many formats.** Year-month-day, day-month-year, month/day/year, ISO 8601, free-text "last March," and an Excel timestamp that drifted by a day because two time zones disagreed. The most common date bug in clinical data, and the easiest one to miss.
3. **Categories and codes.** "Female," "F," and "2" can all encode the same fact. Coding systems exist so that "patient has rheumatoid arthritis" travels without ambiguity. When the encoding is broken, the analysis is broken in a way the cohort builder cannot see.
4. **Spotting type errors in real-looking data.** A short audit on a messy synthetic export. Every cell is plausible and roughly a third of them are wrong.


**Prerequisites:** None. Track 01 of `01-computational-thinking` (the six-part decomposition of a clinical rule) helps. The audit at the end of this track is the same decomposition move applied to a dataset rather than a rule.

**Companion reading:** `01.1-data-types.md` in this folder. Read it before, after, or skip it. The notebook is where the ideas land.

**What's next:** Track 02 on tidy data, which takes the typed columns you trust and asks the next question: is the table shaped like a table?