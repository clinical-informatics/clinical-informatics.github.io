# 06: Learn FHIR

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/06-learn-fhir?quickstart=1)

FHIR is the modern healthcare data-exchange standard. It uses the same architecture as the modern web (REST, JSON, HTTP). This course teaches it from zero, with no prior FHIR or web-API experience required.

Each track in this course pairs a written introduction with an interactive Marimo notebook. The intro frames the question and the vocabulary; the notebook is where you build intuition through interactive work.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum. All six tracks are fully built. The course-level capstone is scaffolded and will be filled in next. Check `tasks.md` in the curriculum root for current progress.

---

## Course map

| Track | Title | What it covers | Status |
|---|---|---|---|
| 0 | Before FHIR (no code) | Data vs structure, HTTP/REST/JSON via the restaurant analogy, health-data history. Closes by diagnosing four real interop differences between Ms. Reyes's Epic and Cerner exports. | Built |
| 1 | FHIR fundamentals | Resources, references, bundles, terminology (LOINC/SNOMED/RxNorm/UCUM/ICD-10/CVX), search parameters at a concept level. Capstone navigates Ms. Reyes's actual FHIR bundle. | Built |
| 2 | Working with FHIR servers | Real hapi.fhir.org calls with cached fallback, gentle Python intro, interactive search URL builder, pagination patterns. Capstone pulls CRP and ESR for a 5-patient synthetic RA cohort and renders a 4-year Altair trend chart. | Built |
| 3 | Clinical modeling | Authoring valid FHIR. Minimum required fields, profiles with US Core, must-support semantics, extensions, reading OperationOutcomes from `$validate`. Capstone authors Ms. Reyes's next follow-up visit and live-validates against hapi.fhir.org. | Built |
| 4 | Implementation guides | IG anatomy walked on real US Core and mCODE StructureDefinitions; the must-support footgun; portability vs interoperability. Capstone produces a one-page gap analysis of US Core for rheumatology. | Built |
| 5 | SMART on FHIR | Two launch flavors; six-step OAuth dance on a cached well-known/smart-configuration; scope vocabulary; CDS Hooks and Bulk Data at concept level. Capstone designs a SMART app for RA monitoring as a one-page brief. | Built |
| ... | **Capstone** | Author and validate a complete FHIR record for Ms. Reyes on hapi.fhir.org. | Scaffolded |

## What you'll find in this repo

```
06-learn-fhir/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── track-00-before-fhir/
├── track-01-fhir-fundamentals/
├── track-02-fhir-servers/
├── track-03-clinical-modeling/
├── track-04-implementation-guides/
├── track-05-smart-on-fhir/
└── capstone/
```

## How to start

Click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) opens in your browser. The home page renders a track list with descriptions and launch buttons.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
