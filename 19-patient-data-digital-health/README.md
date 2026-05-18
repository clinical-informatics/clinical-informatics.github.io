# 19: Patient-generated data, telemedicine, and digital health

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/19-patient-data-digital-health?quickstart=1)

**The 2020s reality. Reyes uses MyChart, tracks symptoms in RheumaTrack, wears an Apple Watch monitoring HRV, had a cross-state telemedicine flare visit, fills out PROMIS-29 every 6 months. The gap between what she generates and what her rheumatologist sees is the worked example.**

Each track in this course pairs a written introduction with an interactive Marimo notebook. The intro frames the question and the vocabulary; the notebook is where you build intuition through interactive work.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum. It is currently **scaffolded only**: the structure, file layout, and short per-track descriptions are in place; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for current progress.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | Patient portals and patient-generated health data | MyChart, FollowMyHealth, Athena. HHS PGHD definition. Integration models (copy-forward, view-only, structured). |
| 02 | Wearables and remote patient monitoring | Apple HealthKit, CGMs, FDA-cleared RPM vs consumer. The data-volume problem. Reyes's HRV time-series. |
| 03 | Telemedicine workflows | Synchronous vs asynchronous, e-consult. Reyes's cross-state flare visit. Licensure, billing, documentation. PHE expansion and after. |
| 04 | Digital therapeutics and patient-facing apps | FDA-cleared SaMD. Pear, Akili, BlueStar. Prescription DTx. Reimbursement realities. |
| 05 | Patient-reported outcomes (PROMs/PROs) | PROMIS, NeuroQOL, EQ-5D. The Reyes PROMIS-29 example. The collect-often, surface-rarely problem. |
| ... | **Capstone** | Design a remote-monitoring program for newly-diagnosed RA patients on biologics: data capture, surfacing, telemedicine touchpoints, workflow mesh, governance, equity (Socratic). |

## What you'll find in this repo

```
19-patient-data-digital-health/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── patients/                ← symlink to start-here/patients/
├── track-01-portals-pghd/
├── track-02-wearables-rpm/
├── track-03-telemedicine/
├── track-04-digital-therapeutics/
├── track-05-proms/
└── capstone/
```

## How to start

Once the content is built: click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) will open in your browser. While the course is still scaffolded, the home.py renders a track list with descriptions so you can see what's coming.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
