# 15: Data storytelling

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/15-data-storytelling?quickstart=1)

**The course that makes everything else useful beyond your own work.**

Five tracks plus a building capstone. The course covers how to make the work the rest of the curriculum produced (data analyses, evaluation reports, vendor assessments, CDS designs) usable to the audiences who have to act on it. Four audience types appear in any clinical informatics setting (technical, clinical, executive, patient); each needs a differently-shaped version of the same set of facts. The five tracks cover audience analysis, the craft of writing about data, the three-part narrative structure that turns a finding into a recommendation, the practice of presenting visuals to non-technical readers, and communicating with AI teams and vendors as a clinician in the room. The capstone takes the CDS design brief from Course 12 and produces two communication artifacts: a 2-minute verbal pitch for a CMO and a one-page visual summary for clinical staff.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum. The course assumes the analytic and clinical-informatics material from Courses 02 through 14; it teaches the communication craft that makes that material land outside the analyst's own workspace.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | Knowing your audience | Four audience types in clinical informatics (technical, clinical, executive, patient). What each needs and does not need. How to identify the audience before composing the message. |
| 02 | Writing about data clearly | Plain English for quantitative findings. Explaining uncertainty in language a reader can act on. Phrases that obscure rather than communicate. |
| 03 | Building a narrative | The three-part structure (finding, implication, recommendation) that turns data into a recommendation an audience can act on. The clinical story that gives data its meaning. |
| 04 | Presenting visuals to non-technical audiences | Cross-reference to Course 08. How to walk a non-technical audience through a chart. What to annotate. What to leave out. |
| 05 | Communicating with AI teams and vendors | The questions a clinician should ask in a vendor or AI-team meeting. The clinician as the domain expert in the room. |
| ... | **Capstone** | Take the CDS design brief from Course 12 and produce two artifacts: a 2-minute verbal pitch for a CMO and a one-page visual summary for clinical staff. |

## What you'll find in this repo

```
15-data-storytelling/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── track-01-audience/
├── track-02-writing/
├── track-03-narrative/
├── track-04-visuals-presenting/
├── track-05-ai-vendor-communication/
└── capstone/
```

## How to start

Click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) opens in a browser tab. Each track folder has a `README.md` that frames the topic and a `notebook.py` that contains the interactive material.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
