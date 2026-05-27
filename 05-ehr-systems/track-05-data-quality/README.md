# Track 05: Real-world data quality problems

You can know the schema, the messages, the warehouse, and the imaging subsystem inside out and still produce a cohort with a third of the patients duplicated and half the structured DAS28 values missing. The first four tracks of this course taught you the architecture. This track teaches you what the architecture produces when it meets a thirty-year hospital data history.

Five problem families show up everywhere:

1. **Duplicate patients** with overlapping but non-identical demographics.
2. **Inconsistent coding** for the same clinical concept across systems.
3. **Missing structured data** for concepts the chart appears to cover.
4. **Note-only findings** that never made it into the structured fields.
5. **Late-binding terminology drift** as local codes diverge from standard vocabularies over time.

Each of the five is illustrated on Ms. Reyes's records. We use a synthetic but realistic 15-row export that seeds the same problems a real EHR export would show.

**Estimated time:** 75 minutes.

**Prerequisites:** Tracks 01 through 04 of this course.

**How to start:** open `notebook.py` in Marimo. The notebook covers the five problem families on a synthetic export, classifies each against the Weiskopf and Weng (2013) data-quality dimensions, and arrives at the capstone, where you will run the audit yourself.

**Companion reading:** `05.1-data-quality.md` in this folder.

**What's next:** the course capstone, where you audit a synthetic EHR extract end to end.
