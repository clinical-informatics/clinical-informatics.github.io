# 08: Clinical visualization

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/08-clinical-visualization?quickstart=1)

**Charts that communicate. Charts that mislead.**

Each track in this course pairs a written introduction with an interactive Marimo notebook. The intro frames the question and the vocabulary; the notebook is where the reader builds intuition through direct manipulation.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | Choosing the right chart type | Data type to chart type as a decision. Six clinical scenarios with the right chart for each, and three common mismatches that mislead. |
| 02 | Longitudinal and time-series data | Ms. Reyes's four-year CRP and ESR trajectory. Reference-range bands, medication-change annotations, smoothing decisions, and how each obscures or clarifies the underlying signal. |
| 03 | Visualizing uncertainty | Standard error, confidence interval, and prediction interval as three distinct claims about the same data. Confidence-level slider on Ms. Reyes's CRP rolling mean. |
| 04 | Common misleading patterns | Truncated axes, cherry-picked time windows, dual axes, time series as bar charts, monthly aggregation that hides intra-month spikes. Each shown as honest-vs-misleading pairs on Ms. Reyes's labs. |
| ... | **Capstone** | A disease-activity dashboard for an RA cohort centered on Ms. Reyes. Patient selector, date-range selector, lab multi-select, DAS28 toggle, medication-timeline toggle, chart-type selector per panel. The dashboard assembles reactively from the controls. |

## What you'll find in this repo

```
08-clinical-visualization/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── track-01-chart-types/
├── track-02-longitudinal/
├── track-03-uncertainty/
├── track-04-misleading-patterns/
└── capstone/
```

## How to start

Click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) opens in a browser tab. Each track folder has a `README.md` that frames the topic and a `notebook.py` that contains the interactive material.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
