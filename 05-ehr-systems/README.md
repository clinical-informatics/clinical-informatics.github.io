# 05: EHR systems

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/05-ehr-systems?quickstart=1)

**How the EHR actually stores and moves data, past the UI.**

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum. It is currently **scaffolded only**: the structure, file layout, and short per-track descriptions are in place; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for current progress.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | How EHRs structure data internally | What the database behind the interface looks like. Why clicking 'medications' pulls from three tables. |
| 02 | HL7 v2, CDA, and the mess we inherited | The historical arc. Why each standard made sense and what it couldn't do. Forward reference to FHIR. |
| 03 | Clinical data warehouses | What a CDW is, how it differs from the operational EHR, why research uses it. |
| 04 | Imaging informatics: PACS, DICOM, RIS, structured reporting | The imaging subsystem. DICOM tags and study/series/instance hierarchy, PACS as storage and viewing, RIS for orders and reporting, structured reporting vs free-text PDF. Reyes's hand radiograph series. |
| 05 | Real-world data quality problems | Duplicate patients, inconsistent coding, missing structured data, note-only findings, applied to Ms. Reyes. |
| ... | **Capstone** | Audit a synthetic EHR extract for data quality issues with a structured checklist interface. |

## What you'll find in this repo

```
05-ehr-systems/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── track-01-internal-structure/
├── track-02-hl7-cda/
├── track-03-warehouses/
├── track-04-imaging-pacs-dicom/
├── track-05-data-quality/
└── capstone/
```

## How to start

Once the content is built: click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) will open in your browser. While the course is still scaffolded, the home.py renders a track list with descriptions so you can see what's coming.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
