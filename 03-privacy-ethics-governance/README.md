# 03: Privacy, ethics, and governance

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/03-privacy-ethics-governance?quickstart=1)

Privacy, ethics, and governance for clinical data: what HIPAA does and does not cover, when de-identification is sufficient, where the IRB fits, and how governance decisions get made in practice.

Each track in this course pairs a written introduction with an interactive Marimo notebook. The intro frames the question and the vocabulary; the notebook is where you build intuition through interactive work.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum. It is currently **scaffolded only**: the structure, file layout, and short per-track descriptions are in place; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for current progress.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | Why privacy matters in health data | Re-identification, documented re-identifications of "anonymized" data, the difference between de-identification and anonymization. |
| 02 | HIPAA and beyond | HIPAA as a floor, not a ceiling. Safe Harbor vs Expert Determination. Data use agreements and the IRB. |
| 03 | Secondary use of clinical data | Data collected for care, repurposed for research. The ethical, legal, and operational tensions. |
| 04 | Algorithmic fairness and equity | Where bias enters: training data, labels, features, deployment context. What to ask of any model. |
| 05 | Governance structures | Who decides what gets built and deployed. Data governance committees, vendor contracts, the clinician's role. |
| ... | **Capstone** | Privacy, governance, and equity analysis of a proposed research project using EHR data (Socratic). |

## What you'll find in this repo

```
03-privacy-ethics-governance/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── track-01-why-privacy/
├── track-02-hipaa/
├── track-03-secondary-use/
├── track-04-algorithmic-fairness/
├── track-05-governance/
└── capstone/
```

## How to start

Once the content is built: click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) will open in your browser. While the course is still scaffolded, the home.py renders a track list with descriptions so you can see what's coming.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
