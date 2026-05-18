# 08: Clinical visualization

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/08-clinical-visualization?quickstart=1)

**Charts that communicate. Charts that mislead.**

Each track in this course pairs a written introduction with an interactive Marimo notebook. The intro frames the question and the vocabulary; the notebook is where you build intuition through interactive work.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum. It is currently **scaffolded only**: the structure, file layout, and short per-track descriptions are in place; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for current progress.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | Choosing the right chart type | Data type → chart type as a decision. Common mismatches and why they mislead. |
| 02 | Longitudinal and time-series data | Disease activity over time. How to show change, how to show uncertainty in a trend. |
| 03 | Visualizing uncertainty | Error bars, confidence intervals, prediction intervals. Same data, different uncertainty display, different impression. |
| 04 | Common misleading patterns | Truncated axes, cherry-picked windows, inappropriate chart types, dual axes, with real clinical examples. |
| ... | **Capstone** | Disease activity dashboard for Ms. Reyes's RA cohort: DAS28 over time, lab trends, medication history. |

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

Once the content is built: click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) will open in your browser. While the course is still scaffolded, the home.py renders a track list with descriptions so you can see what's coming.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
