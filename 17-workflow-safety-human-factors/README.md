# 17: Workflow, patient safety, and human factors

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/17-workflow-safety-human-factors?quickstart=1)

**Anchored to Ms. Reyes's rheumatology visit. The 7 places to enter joint counts, the 4 alerts dismissed on chart open, the methotrexate near-miss. Workflow mapping, human factors, alarm fatigue, safety frameworks, RCA, FMEA, sociotechnical theory.**

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum. It is currently **scaffolded only**: the structure, file layout, and short per-track descriptions are in place; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for current progress.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | Workflow mapping and process re-engineering | Swimlanes, BPMN, time-motion. Reyes's 20-min visit as the swimlane example. Interactive: drag-and-drop step reorder. |
| 02 | Human factors engineering for clinical systems | Nielsen's 10 heuristics, user-centered design, cognitive load. The 7-places-to-enter-joint-counts problem. |
| 03 | Alarm fatigue and alert override | 90%+ override rates in the literature. The 5 Rights of CDS. Interactive: alert-tuning slider for the 4 chart-open alerts. |
| 04 | Patient safety frameworks | SAFER Guides, Vincent, Reason's Swiss cheese, To Err Is Human, just culture. Reyes's MTX near-miss as the worked example. |
| 05 | Root cause analysis and FMEA | 5 Whys, fishbone, FMEA S/O/D/RPN scoring. Walk the near-miss through both. Interactive: FMEA worksheet with reactive RPN. |
| 06 | Sociotechnical systems theory | Why technical-only deployments fail. Sittig and Singh's 8-dimensional model. Cross-ref Course 16 Track 3 and Course 12. |
| ... | **Capstone** | Sign-off review on a sepsis CDS deployment: workflow, human factors, alert tuning, safety risk register, FMEA, sociotechnical readiness (Socratic). |

## What you'll find in this repo

```
17-workflow-safety-human-factors/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── patients/                ← symlink to start-here/patients/
├── track-01-workflow-mapping/
├── track-02-human-factors/
├── track-03-alarm-fatigue/
├── track-04-safety-frameworks/
├── track-05-rca-fmea/
├── track-06-sociotechnical/
└── capstone/
```

## How to start

Once the content is built: click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) will open in your browser. While the course is still scaffolded, the home.py renders a track list with descriptions so you can see what's coming.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
