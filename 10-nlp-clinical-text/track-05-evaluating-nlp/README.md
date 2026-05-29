# Track 05: Evaluating NLP tools

Any NLP tool is evaluated against a gold-standard annotation: a corpus that human annotators have marked up with the labels the tool is supposed to produce. The track defines precision (the fraction of tool predictions that match the gold) and recall (the fraction of gold annotations the tool found), makes the explicit mapping to PPV and sensitivity from Course 04, presents the F1 score as the standard harmonic-mean summary, distinguishes strict from lenient span matching, addresses inter-annotator agreement (the gold itself is not perfectly gold), and closes with the cost-asymmetry argument that clinical NLP usually prioritizes recall because missed entities tend to cost more than over-flagged entities. A reactive demo computes precision, recall, and F1 on a small annotated dataset and shows how each changes as the recall-vs-precision trade-off moves.

**Prerequisites:** Tracks 01 through 04 of this course; Course 04 Track 3 (sensitivity, specificity, PPV, NPV, the 2x2 table).

**How to start:** open `notebook.py`.

**Companion reading:** `go-deeper.md` in this folder.

**What's next:** the course capstone (build a structured representation of Ms. Reyes's record from her 8 notes).
