# Track 03: Discrimination vs calibration

A model has two quality questions, and they are independent. Discrimination asks whether the model ranks high-risk patients above low-risk patients; it is summarized by AUC and visualized by the ROC curve. Calibration asks whether the probabilities the model produces match the observed event rates at those probabilities; it is summarized by the Brier score and visualized by the calibration plot. The track presents the ROC explorer (threshold slider, 2x2 table, ROC curve with AUC) alongside the calibration plot, then shows two models with the same AUC but very different calibration so the distinction is impossible to miss. The clinical consequence: clinicians act on the probability number, not on the rank, and a poorly calibrated model misleads even when its AUC is excellent.

**Prerequisites:** Tracks 01 and 02 of this course; Course 04 Track 3 (sensitivity, specificity, PPV, NPV, the 2x2 table).

**How to start:** open `notebook.py`.

**Companion reading:** `go-deeper.md` in this folder.

**What's next:** Track 04 (Reading an AI paper critically).
