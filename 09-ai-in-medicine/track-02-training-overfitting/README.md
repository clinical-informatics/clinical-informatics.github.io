# Track 02: Training, validation, and overfitting

A model that is evaluated on the same data it was trained on always looks excellent. The model has memorized the data; the evaluation is not a test of anything. This track defines the train / validation / test split, demonstrates overfitting by plotting training error and test error against model complexity (training error goes to zero, test error climbs), defines generalization as the goal that overfitting fails, and introduces k-fold cross-validation as the workaround when the dataset is too small to afford three separate splits.

**Prerequisites:** Track 01 of this course.

**How to start:** open `notebook.py`.

**Companion reading:** `go-deeper.md` in this folder.

**What's next:** Track 03 (Discrimination vs calibration).
