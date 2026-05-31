# 11: Health economics data

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/11-health-economics-data?quickstart=1)

**Claims, costs, decisions, and value.**

Six tracks plus a building capstone. The course covers how claims data is structured (and where it differs from the clinical record), the cost and utilization vocabulary, decision analysis with reactive probability sliders, cost-effectiveness analysis (QALYs and ICERs), decision curve analysis as the unifying framework that closes the threshold question left open in Course 04, and how to read outcomes data critically.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | How claims data is structured | What a claim records, what it can and cannot tell you. The 7 claim rows for Ms. Reyes's 2024-01-08 visit, the institutional vs professional split, and the common claims-research mistakes. |
| 02 | Cost and utilization measures | The vocabulary: total cost of care, PMPM, utilization rate, allowed vs paid vs patient-responsibility. Ms. Reyes's 2024 utilization summarized by month and by claim category. |
| 03 | Decision analysis | A decision tree as a picture and as math. Reactive probability sliders on the biologic-vs-csDMARD choice for a patient like Ms. Reyes. One-way sensitivity analysis showing where the preferred strategy flips. |
| 04 | Cost-effectiveness | QALYs, ICERs, willingness-to-pay thresholds, the cost-effectiveness plane. A worked CE comparison of the biologic-add and csDMARD-monotherapy strategies. |
| 05 | Decision curve analysis | Net benefit defined in one paragraph. The three curves (treat all, treat none, use the model). A reactive DCA on a synthetic flare-prediction model. The threshold-question payoff that Course 04 Track 3 and Course 09 Track 3 set up. |
| 06 | Reading outcomes data critically | Value-based care vocabulary. Common confounders in health-economics research (treatment selection, immortal time, channeling). The CHEERS reporting checklist as the appraisal framework. |
| ... | **Capstone** | Build a decision tree for the RA treatment choice. Run a one-way sensitivity analysis. Interpret whether the preferred strategy is stable across plausible probability ranges. |

## What you'll find in this repo

```
11-health-economics-data/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── track-01-claims-data/
├── track-02-cost-utilization/
├── track-03-decision-analysis/
├── track-04-cost-effectiveness/
├── track-05-dca/
├── track-06-outcomes-data/
└── capstone/
```

## How to start

Click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) opens in a browser tab. Each track folder has a `README.md` that frames the topic and a `notebook.py` that contains the interactive material.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
