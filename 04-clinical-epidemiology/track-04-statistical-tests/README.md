# Track 04: Basic statistical tests

"Which test do I run?" is the wrong starting question. The right starting question is "what do my variables look like?" Once you have the answer to that, the test you should run is a lookup, not a memorization problem.

This track teaches the variable-type-by-variable-type framework. Four answers get you to the right test: what is the exposure variable (categorical or continuous), what is the outcome variable (continuous, categorical, ordinal, time-to-event, or count), what is the group structure (one sample, two independent, two paired, three or more), and (when the outcome is continuous) is the distribution close enough to normal to trust a parametric test or not.

The first interactive is a live decision-tree that applies the four questions and returns the named test plus the reasoning. The second runs both a t-test and a Mann-Whitney on the same data, switchable between a clearly skewed dataset (where the two tests give noticeably different p-values) and an approximately normal dataset (where they agree). The third puts a sample-size slider against a fixed underlying effect and shows how the p-value shrinks while the confidence interval tightens around the truth, so the reader can see what extra information the CI carries that the p-value collapses.

**Prerequisite:** Tracks 01 and 02 of this course (the cohort vocabulary; the bias vocabulary). Track 03 is helpful but not required.


**How to start:** `marimo run track-04-statistical-tests/notebook.py`, or click the run button from the course home page.

## What you will leave with

- A reflex for picking a statistical test by reading the variable types first, not the textbook back-to-front.
- A working understanding of the parametric vs non-parametric trade-off, with a concrete demo of where the choice matters.
- A clear picture of why a confidence interval carries more information than a p-value, and what to look for when a paper reports only one.
- A reading habit: scan a paper's variable types before scanning its statistical methods.

## What's next

Track 05 is study designs: longitudinal designs, survival analysis intuition (Kaplan-Meier and the log-rank test), and a five-question design-picker (exposure, outcome, point of observation, what's measured, time component).
