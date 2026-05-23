# Track 02: Bias

The number you see in a paper can be the wrong number. This track shows three ways that happens (selection, information, confounding) and gives you the visual grammar (DAGs) for spotting which one is in play before you read another result.

The track centers on a single clinical question: *does the TNFi cohort have more serious infections than the csDMARD cohort?* We carry forward the 2,000-patient cohort from Track 01, then add the variable that Track 01 quietly hid: prednisone co-use. Prednisone is a confounder of the TNFi-infection question, and the crude estimate you get without it is misleadingly large. You will see the crude number, you will adjust for prednisone, and you will watch the estimate move.

The same machinery (a small synthetic example, a DAG, a crude estimate, a conditioned estimate) is then turned three ways: a covariate as a confounder, as a mediator, and as a collider. Adjusting for a confounder fixes the bias. Adjusting for a mediator zeroes out the effect you wanted to measure. Adjusting for a collider induces bias where there was none. Same syntax, three different consequences, and the only thing that tells them apart is the DAG.

**Prerequisite:** Track 01 of this course. The cohort, the rates, and the HR computation from Track 01 are reused here.


**How to start:** `marimo run track-02-bias/notebook.py`, or click the run button from the course home page.

## What you will leave with

- A sentence for each of selection, information, and confounding that names a clinical example and the structural feature that defines it.
- A working DAG vocabulary: node, directed edge, path, backdoor path, and the three covariate roles (confounder, mediator, collider).
- A reflex for asking "which role does this covariate play?" before you decide whether to adjust for it.
- A concrete feel, from numbers and not from words, for what happens when you adjust for the wrong thing.

## What's next

Track 03 is diagnostic test performance: sensitivity, specificity, PPV, NPV, and the Bayesian intuition exercise where PPV collapses as prevalence drops. The 2x2 table reappears there as the central object.
