# 00: Foundations of clinical informatics

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/00-foundations?quickstart=1)

**The orientation course. What clinical informatics is as a field, how clinical data flows through systems, and where the actors sit in US healthcare. The course every later course assumes.**

Each track in this course pairs a written introduction with an interactive Marimo notebook. The intro frames the question and the vocabulary; the notebook is where you build intuition through interactive work.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum. It is currently **scaffolded only**: the structure, file layout, and short per-track descriptions are in place; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for current progress.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | What clinical informatics is and how it got here | Definition, brief history (Weed's POMR, the NLM, HITECH 2009, FHIR, AI), and Ms. Reyes introduced as the running patient. |
| 02 | DIKW and the lifecycle of clinical data | Data, information, knowledge, wisdom with Reyes's CRP walked through each layer. The capture-store-use-share-retire lifecycle. |
| 03 | How computers represent and store data | Bits, data structures, file types (TXT/CSV/JSON/XML), what a database is, relational concept, OLTP vs OLAP, database languages. |
| 04 | How computers move data | Client-server, the hospital LAN/VPN/firewall, the internet, HTTP/REST/APIs at concept level, on-prem vs cloud, security boundaries. |
| 05 | The American health system and its parts | Providers, payers, EHR vendors, regulators, research infrastructure, public health, standards bodies. Where informatics lives within each. |
| 06 | Informatics field: roles, ethics, and where the literature lives | CMIO/CNIO/CRIO/analyst distinctions. The AMIA pathway. Where the field publishes. |
| ... | **Capstone** | A community hospital wants to share readmission predictions with its ACO. Walk the problem through DIKW, CS plumbing, network, stakeholders, and governance (Socratic). |

## What you'll find in this repo

```
00-foundations/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── patients/                ← symlink to start-here/patients/
├── track-01-what-is-informatics/
├── track-02-dikw-lifecycle/
├── track-03-data-at-rest/
├── track-04-data-in-motion/
├── track-05-health-system/
├── track-06-roles-ethics-literature/
└── capstone/
```

## How to start

Once the content is built: click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) will open in your browser. While the course is still scaffolded, the home.py renders a track list with descriptions so you can see what's coming.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
