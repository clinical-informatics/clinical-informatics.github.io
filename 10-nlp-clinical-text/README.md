# 10: NLP and clinical text

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/10-nlp-clinical-text?quickstart=1)

**The data that lives in notes, not fields.**

Five tracks plus a building capstone. The course addresses why the majority of clinically meaningful information lives in narrative notes rather than structured fields, what natural language processing pipelines do to extract that information, how clinical notes are de-identified for research use, where large language models fit in the modern NLP landscape, and how to evaluate any NLP tool before adoption.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | Structured vs unstructured data | The categorical reality of clinical data: most of the clinically meaningful detail is in the notes, not the structured fields. A worked side-by-side of one of Ms. Reyes's encounters showing what the structured EHR record captures and what only the note captures. |
| 02 | What NLP actually does | The classical pipeline (tokenization, sentence segmentation, named entity recognition, relation extraction, negation and uncertainty), each illustrated on Ms. Reyes's notes. An inline regex + dictionary NER demo extracting medications, labs, and conditions. |
| 03 | De-identification | The HIPAA Safe Harbor 18 identifiers reviewed in operational form. Three approaches (rule-based, ML-based, hybrid). A before-and-after de-identification of a Reyes note. Residual-risk discussion: quasi-identifiers, k-anonymity, and why no method is lossless. |
| 04 | LLMs and clinical text | Two strands of clinical NLP today (classical pipelines plus LLMs). When to use which. Clinical-domain fine-tuning (BioBERT, ClinicalBERT). Prompted extraction with an explicit schema. The clinical-NLP benchmark landscape. |
| 05 | Evaluating NLP tools | Precision, recall, F1 in plain English; the explicit mapping to PPV and sensitivity from Course 04. Strict vs lenient span matching. Inter-annotator agreement. The cost-asymmetry argument for why clinical NLP usually prioritizes recall. Reactive demo of P/R/F1 on a small annotated set. |
| ... | **Capstone** | Build a structured representation of Ms. Reyes's record from her 8 clinical notes, contrast with the structured EHR fields, and quantify what was lost when only the structured fields were queried. |

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

Click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) opens in a browser tab. Each track folder has a `README.md` that frames the topic and a `notebook.py` that contains the interactive material.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
