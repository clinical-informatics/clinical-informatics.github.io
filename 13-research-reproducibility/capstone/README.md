# Capstone: Audit a published analysis and produce a documentation plan

A Socratic audit. The reader is handed a fictional community-rheumatology paper conditionally accepted by a journal: it reports mean baseline CRP 27.4 mg/L falling to mean follow-up CRP 18.1 mg/L on adalimumab; its data availability statement is "available on request from the corresponding author"; its data were "cleaned in Excel and imported into R"; its manuscript file on disk is `manuscript_FINAL_revised_v3_clean.docx`; no reporting guideline is named. The journal has asked the authors for a data availability statement, a reporting-guideline confirmation, and code availability before final acceptance, and the authors have asked for an outside read.

Five commit-then-reveal steps walk the audit across the five tracks of the course: what Track 01 says about the analysis (forking-paths risks, absence of pre-registration, standing on the three R's); what Track 02 says about the project (the four-decisions failures the manuscript filename and the Excel cleaning note expose); what Track 03 says about it (the version-control rollout that would replace the `FINAL` arms race); what Track 04 says about it (the data dictionary the analysis needs, anchored to the baseline-CRP problem); and what Track 05 says about it (the tiered data-availability statement, the code repository with a DOI, the matched STROBE guideline). A reflection prompt follows. The final cell assembles the five answers plus the reflection into a downloadable Markdown documentation plan a project lead could act on.

Each step is gated by `mo.stop` at 40 characters so the learner commits a substantive answer before the reviewer's reasoning is revealed.

**Prerequisites:** all five tracks in this course.

**How to start:** open `notebook.py`. Marimo loads it in app mode.
