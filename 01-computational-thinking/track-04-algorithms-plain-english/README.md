# Track 04: Algorithms in plain English

An algorithm is a finite list of named operations on named inputs. Every clinical score (CHA₂DS₂-VASc, Wells, Centor, qSOFA, MELD, APGAR, Glasgow Coma Scale, DAS28) is one of these. They differ in which inputs they take and which operations they perform. They share the same skeleton: take a few inputs, transform each one in a defined way, weight the transformed values, sum them, and compare the sum against a clinical cutoff.

The worked example is DAS28, the rheumatology standard for rheumatoid arthritis disease activity. It takes four inputs (tender joint count out of 28, swollen joint count out of 28, an acute-phase reactant, and a patient global assessment) and produces a continuous score with conventional cutoffs for remission, low, moderate, and high disease activity. DAS28 is the running example for three reasons: the curriculum's running patient (Ms. Elena Reyes) has seropositive RA, the score is small enough to walk end to end in one notebook, and its weighted-and-transformed-sum skeleton is the same skeleton most other published clinical scores use. Read DAS28 once and the others read similarly.

You will move sliders for Ms. Reyes's TJC28, SJC28, CRP, and PGA, and watch each step's contribution to the score update live. After the notebook, you can read any published clinical score the same way: read the formula, ask what each transformation is doing, and ask why each weight is the size it is.


**Prerequisite:** Tracks 01 through 03. Track 04 reuses the same vocabulary (inputs, transformations, thresholds, cutoffs) without re-introducing it.

**How to start:** open `notebook.py` from the file tree on the left. Marimo loads it in app mode.

**Companion reading:** [`04.1-algorithms.md`](04.1-algorithms.md) is the reference essay. Read it first, after, or not at all.

**What's next:** Track 05 closes the course. With decomposition, edge-case generation, abstraction, and algorithmic reading in place, the final question is when to trust what the algorithm tells you. The track presents the four-question framework and applies it to a fictional hospital deterioration score.
