# Track 03: Diagnostic test performance

A 52-year-old woman with three months of bilateral MCP and PIP swelling comes to your rheumatology clinic. You're about to order an anti-CCP. The number that comes back will land in one of two ways depending on a single fact about her: how likely you thought she had RA *before* you ordered it. This track is about why that's true.

The 2x2 table is the central object. Sensitivity, specificity, PPV, NPV, and likelihood ratios are five different views of the same four cells. The point of the track is to make the relationships between them visible: how the same test produces a confidently positive result in one clinic and a confidently negative one across town, and what changes is not the test but the prevalence the test is being applied to.

The track has two reactive pieces. The first puts sensitivity, specificity, and prevalence on sliders driving a live 2x2 table with PPV, NPV, and likelihood ratios computed in plain sight. The second is an ROC explorer: two synthetic anti-CCP distributions (RA patients vs joint-pain controls), a threshold slider, and side-by-side panels showing the distributions, the live 2x2, and the ROC curve with a dot at the current threshold. AUC is computed from the same synthetic data so the curve and the summary number match what the learner can see.

**Prerequisite:** Track 01 (the basic 2x2 vocabulary helps but is not required). Track 02 (bias) is helpful for thinking about what "ground truth" means in any test-evaluation study.


**How to start:** `marimo run track-03-diagnostic-test/notebook.py`, or click the run button from the course home page.

## What you will leave with

- A reflex for asking "what's the pre-test probability here?" before ordering a test.
- A working definition for sensitivity, specificity, PPV, NPV, LR+, and LR-, with the relationships between them.
- A concrete feel for why PPV collapses at low prevalence, even for a good test.
- A way to read an ROC curve and an AUC number without needing to redo the math.

## What's next

Track 04 is basic statistical tests: the variable-type-by-variable-type framework for picking the right test, the parametric vs non-parametric decision, and the CI-vs-p-value question reframed.