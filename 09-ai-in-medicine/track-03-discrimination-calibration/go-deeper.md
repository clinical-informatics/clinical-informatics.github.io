# Go deeper: Discrimination vs calibration

**If you want to understand the calibration concept better before moving on:**

- [Frank Harrell's Statistical Thinking blog](https://www.fharrell.com/post/) is the most-cited single source on calibration in the prediction-modeling community. The posts on calibration are short and surface the distinction the track makes (discrimination is necessary but not sufficient).
- The Wikipedia article on the [Brier score](https://en.wikipedia.org/wiki/Brier_score) is brief and accurate; it defines the score, decomposes it into calibration and refinement components, and links to the original Brier 1950 reference.

**If you want to see this applied clinically:**

- [Steyerberg's Clinical Prediction Models](https://www.clinicalpredictionmodels.org/) is the canonical reference text for clinical-prediction-model validation. The book's companion website hosts code and supplementary chapters; the chapter on calibration is the one that pinned the discrimination-vs-calibration distinction in the clinical literature.
- The published [TRIPOD-AI guideline](https://www.equator-network.org/reporting-guidelines/tripod-statement/) requires calibration reporting (calibration plot, Brier score, intercept and slope). The reporting-checklist section of the guideline is the operational version of the track's recommendation that calibration is the second of two model-quality questions.

**If you want to go significantly further:**

- [The Elements of Statistical Learning](https://hastie.su.domains/ElemStatLearn/), Section 9.1.2 and Chapter 8, presents the probability-calibration view at the level required to follow contemporary methods papers on isotonic regression and Platt scaling, the two standard post-hoc calibration corrections that vendors apply to neural-network outputs before deployment.
