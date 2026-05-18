# 18: Population health and public health informatics

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/18-population-public-health?quickstart=1)

**From individual patient care to population view. Reyes is one of 1,247 RA patients in her health system's registry. Risk stratification, value-based care, SDOH, public health surveillance (NEDSS, ESSENCE).**

Each track in this course pairs a written introduction with an interactive Marimo notebook. The intro frames the question and the vocabulary; the notebook is where you build intuition through interactive work.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum. It is currently **scaffolded only**: the structure, file layout, and short per-track descriptions are in place; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for current progress.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | From individual care to population view | Kindig and Stoddart 2003. Population vs public health. The denominator question. Reyes as one row vs Reyes in the registry. |
| 02 | Registries and the population data model | Disease registries, quality registries (NCDR, NSQIP). Registry-vs-EHR distinction. Reyes's RA registry membership. |
| 03 | Risk stratification | HCC, LACE, HOSPITAL. AI-based stratification. Interactive: comorbidity slider showing Reyes's score shift. |
| 04 | Value-based care and delivery models | ACOs (MSSP, REACH), PCMH, BPCI bundles, pay-for-performance. Reyes's ACO attribution. |
| 05 | Social determinants of health | Five-domain framework, PRAPARE, Gravity, SDOH-CC IG. The Reyes food-insecurity capture problem. |
| 06 | Public health informatics | Notifiable disease reporting (NEDSS), syndromic surveillance (ESSENCE), IIS, NHSN. Reyes's COVID and flu cases walked through. |
| ... | **Capstone** | Design a diabetes population health management program: cohort, risk stratification, VBC alignment, SDOH integration, public health reporting, equity (Socratic). |

## What you'll find in this repo

```
18-population-public-health/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── patients/                ← symlink to start-here/patients/
├── track-01-population-view/
├── track-02-registries/
├── track-03-risk-stratification/
├── track-04-value-based-care/
├── track-05-sdoh/
├── track-06-public-health-informatics/
└── capstone/
```

## How to start

Once the content is built: click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) will open in your browser. While the course is still scaffolded, the home.py renders a track list with descriptions so you can see what's coming.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
