# Go deeper: Training, validation, and overfitting

**If you want to understand the bias-variance picture better before moving on:**

- [StatQuest with Josh Starmer](https://statquest.org/) has a dedicated video series on the bias-variance trade-off, on cross-validation, and on regularization. The cross-validation video is the right starting point if k-fold is the first time the concept has come up.
- [An Introduction to Statistical Learning](https://www.statlearning.com/), Chapter 5 "Resampling Methods," is the standard accessible treatment of cross-validation and the bootstrap. The chapter starts with the practical motivation (the dataset is too small for a clean three-way split) and works through both methods with worked examples.

**If you want to see this applied clinically:**

- The [TRIPOD-AI guideline](https://www.equator-network.org/reporting-guidelines/tripod-statement/) (Collins et al. 2024) is the published consensus on what an AI prediction-model study should report. The validation-approach items (internal, temporal, geographic, external) operationalize the train / test framing of this track at the level a peer reviewer or clinical informaticist would use.

**If you want to go significantly further:**

- [The Elements of Statistical Learning](https://hastie.su.domains/ElemStatLearn/) by Hastie, Tibshirani, and Friedman is free online and is the graduate-level reference. Chapter 7 "Model Assessment and Selection" is the most thorough treatment of overfitting, regularization, and resampling-based model selection in any free text.
