# 10: NLP and clinical text

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/10-nlp-clinical-text?quickstart=1)

**The data that lives in notes, not fields. Most clinically meaningful information lives here.**

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum. It is currently **scaffolded only**: the structure, file layout, and short per-track descriptions are in place; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for current progress.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | Structured vs unstructured data | What lives in notes that doesn't live in fields. Why that matters for research and CDS. |
| 02 | What NLP actually does | Tokenization, named entity recognition, relation extraction, each with one of Ms. Reyes's notes. |
| 03 | De-identification | Why it's hard. Common approaches. What residual risk looks like. |
| 04 | LLMs and clinical text | How LLMs relate to traditional NLP. Practical use cases and failure modes. |
| 05 | Evaluating NLP tools | Precision, recall, F1 in plain English. Same idea as sensitivity/specificity, different vocabulary. |
| ... | **Capstone** | Run a pre-built NLP pipeline on Ms. Reyes's notes; compare to structured EHR fields. |

## What you'll find in this repo

```
10-nlp-clinical-text/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── track-01-structured-unstructured/
├── track-02-what-nlp-does/
├── track-03-de-identification/
├── track-04-llms-text/
├── track-05-evaluating-nlp/
└── capstone/
```

## How to start

Once the content is built: click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) will open in your browser. While the course is still scaffolded, the home.py renders a track list with descriptions so you can see what's coming.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
