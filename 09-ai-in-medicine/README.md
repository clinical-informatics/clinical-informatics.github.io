# 09: AI in medicine

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/09-ai-in-medicine?quickstart=1)

**Machine learning for clinicians who evaluate, not build.**

Each track pairs a written introduction with an interactive Marimo notebook. The course deepens the discrimination and calibration vocabulary introduced in Course 04 Track 3, applies it to model evaluation, and ends with a critical-appraisal capstone.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | What a model actually does | A model as a function: inputs in, score out. What training and prediction mean without math. A worked readmission scoring example with reactive sliders. |
| 02 | Training, validation, and overfitting | The train / validation / test split. Why a model that memorizes its training set has zero training error and useless test performance. Cross-validation in plain English. |
| 03 | Discrimination vs calibration | The ROC explorer (threshold slider, 2x2 table, ROC curve, AUC) alongside the calibration plot (predicted vs observed probability, Brier score). Two models with the same AUC but very different calibration, side by side. |
| 04 | Reading an AI paper critically | A five-dimension appraisal framework (training population, outcome definition, validation approach, calibration reporting, subgroup performance) applied to a published clinical AI paper. |
| 05 | Bias, fairness, and clinical risk | Where bias enters (training data, labels, features, deployment context). Subgroup performance demonstrated on a synthetic model. The trade-offs between fairness metrics. What to ask a vendor. |
| 06 | LLMs in clinical workflows | Next-token prediction as the intuition. Hallucination, retrieval-augmented generation, and evaluation. Where LLMs help (summarization, drafting) and where they are dangerous (diagnosis, dosing, citation). |
| ... | **Capstone** | Critical appraisal of a vendor-pitched "RA flare predictor" against the Track 04 framework, in the Socratic commit-then-reveal pattern. |

## What you'll find in this repo

```
09-ai-in-medicine/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── track-01-what-a-model-does/
├── track-02-training-overfitting/
├── track-03-discrimination-calibration/
├── track-04-reading-papers/
├── track-05-bias-fairness/
├── track-06-llms/
└── capstone/
```

## How to start

Click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) opens in a browser tab. Each track folder has a `README.md` that frames the topic and a `notebook.py` that contains the interactive material.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
