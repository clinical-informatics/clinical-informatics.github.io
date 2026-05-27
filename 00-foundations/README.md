# 00: Foundations of clinical informatics

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/00-foundations?quickstart=1)

The orientation course. What clinical informatics is as a field, how clinical data flows through systems, and where the actors sit in U.S. healthcare. The course every later course assumes.

This is the first content course in the curriculum. There is no coding. Every interaction is a click-through, a radio button, or a short prompt. After the six tracks and the Socratic capstone, you will have a working mental model of the field, the vocabulary it uses, the lifecycle of clinical data, the network architecture clinical systems run on, the actors whose agreement everything depends on, and the publication venues where the field's work lives.

Each track in this course pairs a written introduction with an interactive Marimo notebook. The intro frames the question and the vocabulary; the notebook is where you build intuition through interactive work.

Written by **Mario David Felix, MD MHS**.

---

## Who this is for

- Clinicians who want a working mental model of the field before learning specific tools.
- Trainees evaluating whether clinical informatics is a direction they want to go.
- Researchers who need to navigate the clinical-data ecosystem without becoming engineers.
- Anyone curious about how the chart they open every morning came to look the way it does.

No coding is required for this course. Nothing to install. All interactions are radio buttons, multi-selects, or short reflections. Python and SQL appear in later courses, explained where they first come up.

## Prerequisites

None. This is the orientation course. Medical-school-level clinical literacy is assumed, but no informatics background is.

For an orientation to the wider curriculum (and Ms. Reyes, the patient who appears in every course), see the [start-here repo](https://github.com/clinical-informatics/start-here). You can also begin here directly.

---

## How to start

1. Click the Codespaces badge above. A development environment loads in your browser. Allow about ninety seconds.
2. The course menu (`home.py`) opens automatically.
3. Begin with **Track 01: What clinical informatics is and how it got here**. The tracks run in order.

---

## Course map

Six tracks plus a Socratic capstone. Each track is a short interactive notebook (20 to 30 minutes). The capstone is a short walkthrough of one scenario in which every track is in play.

| Track | Title | What it covers |
|---|---|---|
| 01 | What clinical informatics is and how it got here | Definition, brief history (Weed's POMR, the NLM, HITECH 2009, FHIR, AI), and Ms. Reyes introduced as the running patient. |
| 02 | DIKW and the lifecycle of clinical data | Data, information, knowledge, wisdom with Reyes's CRP at each layer. The capture-store-use-share-retire lifecycle. |
| 03 | How computers represent and store data | Bits, data structures, file types (TXT/CSV/JSON/XML), what a database is, relational concept, OLTP vs OLAP, database languages. |
| 04 | How computers move data | Client-server, the hospital LAN/VPN/firewall, the internet, HTTP/REST/APIs at concept level, on-prem vs cloud, security boundaries. |
| 05 | The American health system and its parts | Providers, payers, EHR vendors, regulators, research infrastructure, public health, standards bodies. Where informatics lives within each. |
| 06 | Informatics field: roles, ethics, and where the literature lives | CMIO/CNIO/CRIO/analyst distinctions. The AMIA pathway. Where the field publishes. |
| ... | **Capstone** | Walden Community Hospital wants to share its readmission predictions with its ACO. Walk the problem through DIKW, the plumbing, the stakeholders, and the governance. Socratic. |

## What you can do afterward

- Define clinical informatics in plain English and distinguish the field's work from the clinical work that uses what the field builds.
- Name the four DIKW layers, walk a clinical value through the five lifecycle stages, and locate common failure modes at specific intersections of stage and layer.
- Sketch what a clinical system looks like underneath (data structures, file types, OLTP vs OLAP) and what the network around it looks like (LAN, firewall, VPN, public internet, the boundaries data crosses).
- Name the seven actor groups in U.S. healthcare and identify whose agreement is load-bearing for any particular clinical informatics decision.
- Recognize the working titles in the field, the training pathways into it, and the publication venues where its literature lives.

## Where this goes next

The vocabulary built here is the substrate for the rest of the curriculum. The Ms. Reyes you meet in Track 01 returns in every course. The DIKW vocabulary returns in every conversation about predictions, alerts, and extracts. The lifecycle returns when FHIR resources, OMOP records, and claims travel through systems. The actor groups return whenever an integration is being scoped.

Most learning paths route from here directly into **`01-computational-thinking`**.

---

## Repo contents

```
00-foundations/
├── home.py                                     ← Marimo course menu (opens automatically)
├── GLOSSARY.md                                 ← Plain-English definitions of terms used here
├── track-01-what-is-informatics/               ← One track per folder
├── track-02-dikw-lifecycle/
├── track-03-data-at-rest/
├── track-04-data-in-motion/
├── track-05-health-system/
├── track-06-roles-ethics-literature/
├── capstone/                                   ← Socratic Walden ACO scenario
├── shared/                                     ← Symlink to ../start-here/shared/
└── patients/                                   ← Symlink to ../start-here/patients/
```

---

## License and use

- **Course content:** Creative Commons BY 4.0. Use it, remix it, teach with it. Please credit Mario David Felix, MD MHS.
- **Code:** MIT.

This is a single-author curriculum, not an open contribution project. Pull requests are not accepted. To report an error or suggest something, open an issue.
