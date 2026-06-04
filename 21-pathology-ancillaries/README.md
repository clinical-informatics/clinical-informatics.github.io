# 21: Pathology, ancillary systems, and medical device integration

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/21-pathology-ancillaries?quickstart=1)

**The systems-side gap-fill: laboratory information systems, anatomic and clinical pathology workflows, digital pathology, pharmacy systems, medical device integration, and the rest of the ancillary-system ecosystem the EHR depends on.**

Each track in this course pairs a written introduction with an interactive Marimo notebook. The intro frames the question and the vocabulary; the notebook is where you build intuition through interactive work.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum. It is currently **scaffolded only**: the structure, file layout, and short per-track descriptions are in place; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for current progress.

The course was added 2026-06-04 after a board-syllabus gap analysis identified pathology informatics, LIS, pharmacy systems, medical device integration, and other ancillary systems as substantive areas not previously covered. The course depends on the EHR-systems material from Course 05 and connects forward to Course 22 (security) for the cybersecurity dimension of medical devices and connected systems.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | Pathology informatics and the LIS | Anatomic vs clinical pathology. The LIS as a system: order entry, accessioning, instrument autoverification, result release. AP-CP integration. |
| 02 | Digital pathology and whole-slide imaging | WSI formats (BigTIFF, DICOM WSI), viewer architecture, telepathology, FDA-cleared primary diagnosis. AI in pathology (cross-ref Course 09). |
| 03 | Pharmacy informatics and the closed-loop medication system | CPOE, pharmacy verification, eMAR, BCMA, smart pumps. The five rights as system goal. Cross-ref Course 12. |
| 04 | Medical device integration (MDI) | IEEE 11073, HL7 v2 device messaging, FHIR Device and DeviceMetric. Vital-signs monitors, ventilators, anesthesia. The mixed-vendor reality and device cybersecurity. |
| 05 | Other ancillary systems | Scheduling and registration (ADT), dietary, materials management. Imaging (PACS/DICOM/RIS) callback to Course 05. The ancillary-to-clinical interface pattern. |
| 06 | Special and emerging data sources | Patient-generated data, genomic data, SDOH, wearables. The "everything is FHIR now" pattern alongside format diversity in legacy ancillaries. |
| ... | **Capstone** | Audit the LIS-and-pathology rollout at a synthetic 350-bed community hospital across instrument integration, autoverification, AP-CP integration, EHR result delivery, and pharmacy/device interfaces (Socratic). |

## What you'll find in this repo

```
21-pathology-ancillaries/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── patients/                ← symlink to start-here/patients/
├── track-01-lis-pathology/
├── track-02-digital-pathology/
├── track-03-pharmacy-systems/
├── track-04-medical-device-integration/
├── track-05-ancillary-systems/
├── track-06-emerging-data-sources/
└── capstone/
```

## How to start

Once the content is built: click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) will open in your browser. While the course is still scaffolded, the home.py renders a track list with descriptions so you can see what's coming.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
