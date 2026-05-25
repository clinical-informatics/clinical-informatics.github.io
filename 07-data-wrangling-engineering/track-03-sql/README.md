# Track 03: SQL, the extraction layer

SQL is the language used to extract cohorts and summaries from an OMOP warehouse. This track frames each query as a clinical question first, then constructs the SQL that returns the answer from an in-memory SQLite database holding Reyes plus a small synthetic RA cohort in OMOP shape. The query patterns demonstrated (cohort filter, GROUP BY aggregation, window functions, date arithmetic, the WITH / CTE structure) cover the majority of analytic SQL written against OMOP warehouses.

**Prerequisites:** Tracks 01 and 02 of this course. Course 02 Track 05 (databases) is helpful but not required.

**How to start:** open `notebook.py`. Marimo loads it in app mode.

**Companion reading:** `go-deeper.md` in this folder.

**What's next:** Track 04 (pandas, the post-extraction analytic layer).
