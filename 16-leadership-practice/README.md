# 16: Informatics leadership and professional practice

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/16-leadership-practice?quickstart=1)

**How to actually do the job. The CMIO just handed you the RA-CDS you designed in the Course 12 capstone. Eight tracks teach you the strategic-planning, project-management, change-management, KPI, financial, leadership-communication, and implementation-and-operations moves to deploy it.**

Each track in this course pairs a written introduction with an interactive Marimo notebook. The intro frames the question and the vocabulary; the notebook is where you build intuition through interactive work.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum. It is currently **scaffolded only**: the structure, file layout, and short per-track descriptions are in place; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for current progress.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | The working clinical informaticist: roles, scope, day-to-day | Roles, org-chart placement, reporting lines, committees, the 'who decides what' matrix for the RA-CDS deployment. |
| 02 | Project management for informatics | PMBOK, Waterfall/Agile/Scrum/Kanban, the five PMI process groups, RACI, Gantt, the SDLC. Build the RA-CDS plan. |
| 03 | Change management | Kotter, Lewin, ADKAR. Why technical-only deployments fail. The Sepsis Watch case. Change-readiness assessment for the RA-CDS. |
| 04 | Healthcare quality improvement and operations management | Model for Improvement and PDSA at depth. Lean (5S, value stream, gemba), Six Sigma DMAIC, run/control charts, IHI Triple/Quadruple Aim. KPIs informaticists own (HCAHPS, readmissions, override rates). Balanced scorecards. RA-CDS dashboard. |
| 05 | Financial management for informaticists | Capex vs opex, ROI, NPV, TCO, vendor economics. RA-CDS budget and 5-year ROI calculator. |
| 06 | Leadership and communication | Leadership styles, executive communication (BLUF), conflict resolution. RA-CDS 3-slide board pitch builder. Brief board-pathway career orientation. |
| 07 | Strategic planning and IT portfolio management | Mission/vision and SWOT for IT strategy. Multi-year roadmaps and capital planning. IT portfolio management as managed-investment view. Enterprise alignment. |
| 08 | Implementation and operations of CIS | The deploy-and-run lifecycle past go-live: command-center, change-control board, support tiers, downtime procedures, post-go-live optimization. Forward-ref Course 17 and Course 22. |
| ... | **Capstone** | Assemble the eight track artifacts plus a post-go-live operations plan and a risk register into the implementation plan for the RA-CDS the learner designed in Course 12. The 'now actually deploy it' capstone. |

## What you'll find in this repo

```
16-leadership-practice/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── patients/                ← symlink to start-here/patients/
├── track-01-working-informaticist/
├── track-02-project-management/
├── track-03-change-management/
├── track-04-quality-kpis/
├── track-05-financial-management/
├── track-06-leadership-communication/
├── track-07-strategic-planning/
├── track-08-implementation-operations/
└── capstone/
```

## How to start

Once the content is built: click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) will open in your browser. While the course is still scaffolded, the home.py renders a track list with descriptions so you can see what's coming.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
