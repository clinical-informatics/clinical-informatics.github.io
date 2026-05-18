# 04: Clinical epidemiology

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/04-clinical-epidemiology?quickstart=1)

Clinical epidemiology for clinicians: the measures, biases, designs, and tests that show up in every clinical paper and every AI model writeup, with intuition built before vocabulary.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum. It is currently **scaffolded only**: the structure, file layout, and short per-track descriptions are in place; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for current progress.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | Measures of frequency and association | Incidence, prevalence, RR, OR, HR, each with a clinical example from Ms. Reyes's cohort. |
| 02 | Bias | Selection, information, confounding, with real clinical examples and a confounder you can add to an analysis on a slider. |
| 03 | Diagnostic test performance | The 2x2 table as the core intuition exercise. Sliders for sensitivity, specificity, prevalence; watch PPV collapse. |
| 04 | Basic statistical tests | Match the test to the data type. P-values and CIs done right. Common misinterpretations. |
| 05 | Study designs | Which design could answer the question, at what cost. Causation vs association. |
| ... | **Capstone** | Identify the three biggest threats to validity in a naive analysis of a synthetic RA dataset (Socratic). |

## What you'll find in this repo

```
04-clinical-epidemiology/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── track-01-frequency-association/
├── track-02-bias/
├── track-03-diagnostic-test/
├── track-04-statistical-tests/
├── track-05-study-designs/
└── capstone/
```

## How to start

Once the content is built, click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) will open in your browser. While the course is still scaffolded, `home.py` renders a track list with descriptions so you can see what is coming.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
