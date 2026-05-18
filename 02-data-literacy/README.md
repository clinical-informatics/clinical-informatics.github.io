# 02: Data literacy

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/02-data-literacy?quickstart=1)

The mental model for working with clinical data: rows, columns, joins, and the ways data can go missing.

Each track in this course pairs a written introduction with an interactive Marimo notebook. The intro frames the question and the vocabulary; the notebook is where you build intuition through interactive work.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum. It is currently **scaffolded only**: the structure, file layout, and short per-track descriptions are in place; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for current progress.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | Data types and why they matter | Numbers vs text, dates (the special nightmare), categories and codes; CRP stored as text and the average that breaks. |
| 02 | Tidy data | One fact per cell. What untidy data looks like in clinical practice and what reshaping the medication table actually does. |
| 03 | Null values and missingness | MCAR, MAR, MNAR in plain English. What happens when you ignore each one, watched on a slider. |
| 04 | Joins: the central skill | Inner, left, right, anti-join, applied to two clinical tables. The 'silent patient loss' problem made visible. |
| 05 | What a database actually is | Why a database is not a spreadsheet. Schema, constraints, and the forward reference to FHIR and OMOP. |
| ... | **Capstone** | Clean, join, and summarize three messy synthetic clinical tables using the cohort builder. |

## What you'll find in this repo

```
02-data-literacy/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── track-01-data-types/
├── track-02-tidy-data/
├── track-03-missingness/
├── track-04-joins/
├── track-05-databases/
└── capstone/
```

## How to start

Once the content is built: click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) will open in your browser. While the course is still scaffolded, the home.py renders a track list with descriptions so you can see what's coming.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
