# 13: Research reproducibility

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/13-research-reproducibility?quickstart=1)

**Unglamorous, and the thing most people wish someone had taught them early.**

Five tracks plus a Socratic capstone. The course covers why reproducibility is a clinical-research problem and not only a software problem, how to organize a data project so a stranger (or future you) can rerun it, what version control does without requiring the reader to write code, how to document where a dataset came from and what was done to it, and what the rules and reporting guidelines require when an analysis is shared or published. The capstone is a reproducibility audit: given a synthetic published analysis with poor reproducibility practices, identify what is missing and produce a documentation plan that would let an independent group rerun the work.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum. No coding experience is required; Track 03 explains version control in plain English without asking the reader to run a single command.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | Why reproducibility matters | The replication crisis in clinical research. The reproducible / replicable / robust distinction. Why an analysis can be wrong even when every number is correct. |
| 02 | Project organization | How to structure a data project so it can be rerun. File naming, folder structure, the raw-data-is-sacred rule, README-driven development. |
| 03 | Version control without coding | What Git does in plain English, and the one problem it solves. GitHub for non-developers; issues and pull requests as collaboration tools. |
| 04 | Data provenance and documentation | Where a dataset came from and what was done to it. Documenting transformations and the loss they introduce. Cross-reference to Course 07: no mapping is lossless. |
| 05 | Sharing and publication | What to share and what to withhold. Code sharing, preprints, persistent identifiers, and the EQUATOR reporting guidelines. Cross-reference to Course 03 on privacy. |
| ... | **Capstone** | Audit a synthetic published RA analysis for reproducibility gaps and produce a documentation plan that would make it reproducible (Socratic). |

## What you'll find in this repo

```
13-research-reproducibility/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── track-01-why-reproducibility/
├── track-02-project-org/
├── track-03-version-control/
├── track-04-provenance/
├── track-05-sharing/
└── capstone/
```

## How to start

Click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) opens in a browser tab. Each track folder has a `README.md` that frames the topic and a `notebook.py` that contains the interactive material.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
