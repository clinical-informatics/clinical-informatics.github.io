# Track 4: Implementation guides

> Two vendors both claim to support US Core. One displays the lab `interpretation` flag prominently. The other stores it but never shows it. Both can defensibly claim conformance. What happened?

This track teaches you to read published implementation guides (IGs) with enough fluency to evaluate vendor claims, plan a real project, and write the gap analysis that says what your workflow needs that the IG does not cover. You walk two real IGs (US Core and mCODE) from their published StructureDefinitions, learn what differential / snapshot / must-support / constraints mean in practice, and learn the must-support footgun ("what does support actually mean?") that produces most claimed-conformance disputes. You also fix the distinction between **portability** (data exits your system intact) and **interoperability** (data works intact in the next system). That distinction is the difference between OMOP and FHIR in one sentence.

The capstone is a one-page gap analysis of US Core for rheumatology: a structured form where you rate US Core Observation Lab's coverage of RA monitoring needs row by row, name the RA-specific data US Core does not cover cleanly, and the notebook assembles the answers into a markdown report ready to copy out as your draft for a project kickoff.


**Prerequisites:** Tracks 0 through 3 of this course. Track 3's profile and must-support introduction is the load-bearing prerequisite; this track deepens it.

**How to start:** open `notebook.py` in this folder from the file tree on the left. Marimo loads it in app mode. The cached US Core Observation Lab and mCODE Primary Cancer Condition StructureDefinitions are in `cache/`; the notebook reads them directly so you can see real IG content rather than hand-waving.

**Companion reading:** [`04.1-implementation-guides.md`](04.1-implementation-guides.md) is a short reference essay on IG anatomy, profile inheritance, must-support footguns, and portability vs interoperability.

**What's next:** Track 5 introduces SMART on FHIR. SMART is itself an implementation guide layered on top of US Core, so this track's vocabulary lets the SMART spec feel ordinary instead of magical.
