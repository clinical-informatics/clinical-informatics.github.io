# 09: AI in medicine

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/09-ai-in-medicine?quickstart=1)

**Machine learning for clinicians who evaluate, not build. Explicitly deepens Track 04 (epi).**

Each track in this course pairs a written introduction with an interactive Marimo notebook. The intro frames the question and the vocabulary; the notebook is where you build intuition through interactive work.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum. It is currently **scaffolded only**: the structure, file layout, and short per-track descriptions are in place; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for current progress.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | What a model actually does | Intuition before math. A model as a function. What training and prediction mean. |
| 02 | Training, validation, overfitting | Why you can't test on what you trained on. Overfitting shown visually. |
| 03 | Discrimination vs calibration | ROC, threshold slider, 2x2, and calibration plot side by side. Why a well-discriminating model can still be useless. |
| 04 | Reading an AI paper critically | What to look for: training population, outcome, validation approach, calibration, subgroup performance. |
| 05 | Bias, fairness, and clinical risk | Where bias enters. Disparate subgroup performance. What to ask a vendor. |
| 06 | LLMs in clinical workflows | What LLMs are without math. Where they help, where they're dangerous, hallucination explained clearly. |
| ... | **Capstone** | Critical appraisal of a published clinical AI model across each appraisal dimension (Socratic). |

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

Once the content is built: click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) will open in your browser. While the course is still scaffolded, the home.py renders a track list with descriptions so you can see what's coming.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
