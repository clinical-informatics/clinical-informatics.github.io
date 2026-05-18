# 12: Clinical decision support

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/12-clinical-decision-support?quickstart=1)

**The capstone course. Requires courses 06 and 09. All prior concepts revisited and connected.**

Each track in this course pairs a written introduction with an interactive Marimo notebook. The intro frames the question and the vocabulary; the notebook is where you build intuition through interactive work.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum. It is currently **scaffolded only**: the structure, file layout, and short per-track descriptions are in place; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for current progress.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | What CDS actually is | Passive alerts → active recommendations → autonomous actions. Why most CDS fails. The five rights. |
| 02 | CQL: Clinical Quality Language | Why CQL exists. Reading published CQL. Writing simple CQL. Value sets. |
| 03 | CDS Hooks | Architecture in plain English. patient-view, order-select, order-sign. A simulated CDS Hooks request. |
| 04 | Evaluating CDS | DCA from course 11. Before/after study design. Unintended consequences checklist. |
| 05 | Governance and the human side | Who decides what gets built. Equity in CDS. Regulatory landscape. |
| ... | **Capstone** | Design a complete CDS intervention for RA end to end, drawing on every prior course; export as PDF. |

## What you'll find in this repo

```
12-clinical-decision-support/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── track-01-what-cds-is/
├── track-02-cql/
├── track-03-cds-hooks/
├── track-04-evaluating-cds/
├── track-05-governance-human/
└── capstone/
```

## How to start

Once the content is built: click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) will open in your browser. While the course is still scaffolded, the home.py renders a track list with descriptions so you can see what's coming.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
