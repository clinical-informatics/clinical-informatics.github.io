# 12: Clinical decision support

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/12-clinical-decision-support?quickstart=1)

**The curriculum's capstone course.**

Five tracks plus the curriculum's grand-finale capstone. The course covers what CDS actually is and why most of it fails, the standards-based logic layer (CQL), the standards-based delivery layer (CDS Hooks), evaluation methods that combine DCA from Course 11 with study designs from Course 04, and the governance and equity questions that determine whether a CDS deployment helps patients or harms them. The capstone is a seven-step design exercise that integrates Courses 01, 03, 04, 06, 09, 10, and 11 into a single CDS intervention design brief.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | What CDS actually is | The spectrum from passive alerts to autonomous actions, the five-rights framework, the alert-fatigue and 97%-override-rate problem, and the diagnostic-test framing of a CDS alert. |
| 02 | CQL: Clinical Quality Language | Why CQL exists (same motivation as FHIR and OMOP, applied to logic). Reading a published CQL fragment. Writing a small CQL rule. The role of VSAC value sets. |
| 03 | CDS Hooks | The hook-as-workflow-moment architecture, the patient-view / order-select / order-sign hooks, the JSON request and response payload, and a simulated end-to-end CDS Hooks call with a card-design exercise. |
| 04 | Evaluating CDS | DCA from Course 11 applied to a CDS alert threshold. Before-and-after study designs from Course 04. The unintended-consequences checklist (workflow disruption, equity, automation bias, alert-fatigue spillover). |
| 05 | Governance and the human side | Who decides what CDS gets built. Clinician input into CDS design. Equity in CDS. The CDS regulatory landscape (FDA SaMD, ONC certification). The vendor-evaluation checklist for a new CDS tool. |
| ... | **Capstone** | Design a complete CDS intervention for a Reyes-style RA flare alert across all seven steps (computational decomposition, FHIR data, CQL logic, CDS Hook design, evaluation plan, DCA threshold, equity monitoring). Output is a CDS design brief a real implementation team could act on. |

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

Click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) opens in a browser tab. Each track folder has a `README.md` that frames the topic and a `notebook.py` that contains the interactive material.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
