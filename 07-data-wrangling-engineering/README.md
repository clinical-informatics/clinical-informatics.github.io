# 07: Data wrangling and engineering

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/07-data-wrangling-engineering?quickstart=1)

**SQL, pandas, OMOP, graph databases. The data engineering layer.**

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum. It is currently **scaffolded only**: the structure, file layout, and short per-track descriptions are in place; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for current progress.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | SQL from first principles | Clinical questions first, SQL second. Aggregations, grouping, and window functions via clinical use cases. |
| 02 | pandas for clinical data | DataFrames as clinical tables. Filtering, grouping, merging through clinical scenarios. Dates as a special focus. |
| 03 | Standards: why they exist | Portability vs interoperability defined and distinguished. The same fact stored six ways across six EHRs. |
| 04 | OMOP CDM | Why OMOP exists. Core tables, concept IDs, the vocabulary layer. Mapped from Ms. Reyes's EHR. |
| 05 | Graph databases | Conceptual fluency only. When a problem is graph-shaped. Ms. Reyes's medication history as a knowledge graph. |
| ... | **Capstone** | Build an OMOP-structured dataset for a synthetic RA cohort from messy source data; run three clinical queries. |

## What you'll find in this repo

```
07-data-wrangling-engineering/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── track-01-sql/
├── track-02-pandas/
├── track-03-standards/
├── track-04-omop/
├── track-05-graph-databases/
└── capstone/
```

## How to start

Once the content is built: click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) will open in your browser. While the course is still scaffolded, the home.py renders a track list with descriptions so you can see what's coming.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
