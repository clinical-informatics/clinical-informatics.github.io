# Track 04: Data provenance and documentation

A published table reports that Ms. Reyes's RA cohort had a mean baseline CRP of 18 mg/L. Where did that number come from? Which CRP draw counted as baseline, the one nearest enrollment or the one nearest diagnosis? Were the high-sensitivity and standard CRP assays pooled? Were values below the assay's detection limit set to zero, to the limit, or dropped? Each of these is a defensible choice, and each produces a different 18. Provenance is the recorded answer to "how did this number get here," and without it the table cannot be defended when an editor or a regulator asks.

The track defines **provenance** (the recorded origin and processing history of a dataset) and **data lineage** (the step-by-step record of every transformation from raw source to analysis-ready table), and it shows how to document both in plain English: a transformation log, a data dictionary that defines every variable and its units and its missingness convention, and a record of who did what and when. The closing section is the cross-reference back to Course 07. The OMOP mapping reflection made the point that no standard is lossless: mapping Ms. Reyes's EHR to OMOP discarded or approximated real clinical detail. The reproducibility consequence is that the loss itself is part of the provenance, and documenting what a transformation discarded matters as much as documenting what it kept. The notebook walks a raw-to-final lineage for the CRP variable and shows how an undocumented choice becomes an unanswerable question downstream.

**Prerequisites:** Tracks 01 through 03 of this course. Course 07 Track 4 (OMOP) is the anchor for the closing cross-reference.

**How to start:** open `notebook.py`. Marimo loads it in app mode.

**Companion reading:** `go-deeper.md` in this folder.

**What's next:** Track 05 (sharing and publication).
