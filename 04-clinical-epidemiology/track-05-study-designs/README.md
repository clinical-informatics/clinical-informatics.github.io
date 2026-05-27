# Track 05: Study designs

Which study design could answer this question, and what would it cost you. The same answer is true for almost every clinical question: there is a design that can answer it cleanly (usually expensive and slow), and there are designs that can answer it approximately (usually cheap and fast). The thinking move is to know which is which, and to read a paper with the design's strengths and weaknesses already in your head.

This track centers on the five-question framework: name the exposure, name the outcome, locate the point of observation in time, name what is being measured, and identify the time component. Those five answers map to one of six designs: randomized controlled trial, prospective cohort, retrospective cohort, case-control, cross-sectional, or case series. The first interactive applies the five questions and returns the matching design with a one-paragraph reasoning.

Track 5 also covers the two ideas that make longitudinal designs land: person-time as the denominator that enables incidence rates and hazard ratios (cross-sectional designs cannot), and Kaplan-Meier curves with their three subtleties (censoring is not the same as no event; the log-rank test compares whole curves; the hazard ratio is only meaningful when the proportional-hazards assumption holds). The second interactive draws KM curves for two arms under either a clean proportional-hazards scenario or a curves-cross scenario, and shows what each gets right and what each gets wrong.

**Prerequisite:** Tracks 01 (the incidence rate and HR vocabulary) and 02 (bias / DAGs) of this course. Tracks 03 and 04 help but are not required.


**How to start:** `marimo run track-05-study-designs/notebook.py`, or click the run button from the course home page.

## What you will leave with

- A reflex for picking a study design by applying the five-question framework, not by trying to remember a textbook chart.
- A working definition for the six study designs, with what each one can and cannot tell you about causation.
- The longitudinal-design vocabulary: prospective vs retrospective cohorts, person-time, and what these enable that cross-sectional designs cannot.
- A reading habit for Kaplan-Meier curves: spot censoring tick marks; check whether the curves cross before you trust an HR; read the log-rank as a whole-curve test.

## What's next

The course capstone: a Socratic walk-through of a synthetic observational RA dataset, where you identify the three biggest threats to validity in a naive analysis and propose how you would address each one.
