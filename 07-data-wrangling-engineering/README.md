# 07: Data wrangling and engineering

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/07-data-wrangling-engineering?quickstart=1)

**From the clinical data warehouse to a clinical answer.** Code standards, OMOP CDM, SQL extraction, pandas analysis, and graph databases at concept level.

Each track in this course pairs a written introduction with an interactive Marimo notebook. The intro frames the question and the vocabulary; the notebook is where you build intuition through interactive work.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | Standards in the EHR | LOINC, SNOMED CT, ICD-10-CM, CPT, RxNorm, NDC. Which standard names which slice of the record, where in the EHR each is stored, and the failure modes of queries that filter on the wrong vocabulary. |
| 02 | OMOP Common Data Model | The fixed schema layered on top of the code standards. Six core tables presented on Reyes's record. The vocabulary layer and the standard-concept-vs-source-concept distinction. |
| 03 | SQL, the extraction layer | Each clinical question stated first, then the SQL that answers it. Cohort filter, GROUP BY aggregation, window functions, date arithmetic, common table expressions. |
| 04 | pandas, the post-extraction analytic layer | Tidying, per-patient summaries, time-since-event computation, reactive filtering. Tool comparison with DuckDB, polars, and dplyr. |
| 05 | Graph databases, conceptual | When a problem is graph-shaped. Nodes, edges, properties, traversal. Cypher pseudocode on Reyes's medication graph and on SNOMED is-a hierarchy traversal. |
| ... | **Capstone** | From raw EHR files to a clinical answer. Three messy raw tables mapped to OMOP shape, then queried for three clinical questions, one per analytic layer. |

## What you'll find in this repo

```
07-data-wrangling-engineering/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── track-01-standards/
├── track-02-omop/
├── track-03-sql/
├── track-04-pandas/
├── track-05-graph-databases/
└── capstone/
```

## How to start

Click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) will open in your browser. From the menu, each track has its own folder with a `README.md` (intro and prerequisites), a `notebook.py` (the interactive notebook), and a `go-deeper.md` (a curated reading list for further study).

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
