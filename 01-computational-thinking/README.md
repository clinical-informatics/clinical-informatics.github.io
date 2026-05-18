# 01: Computational thinking

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/01-computational-thinking?quickstart=1)

Computational thinking is the discipline of restating a clinical problem in terms a computer can act on: cohorts, signals, thresholds, time windows, sources, triggers. This course teaches that discipline for clinicians, trainees, and clinical researchers.

This is the entry-point course for the `clinical-informatics` curriculum. There are no formulas and no visible code. Every interaction is a slider, a checkbox, or a short prompt. After the five tracks and capstone, you can look at any clinical rule, alert, or model and ask the four questions that decide whether to trust it.

Written by **Mario David Felix, MD MHS**.

---

## Who this is for

- Clinicians who want to know what is happening when an algorithm flags their patient.
- Trainees deciding between clinical and quantitative work.
- Researchers handed a model and asked to evaluate it.
- Anyone curious about how informatics reasons.

No coding is required for this course. Nothing to install. All interactions are sliders or short prompts. Python and SQL appear in later courses, explained where they first come up.

## Prerequisites

None. This is the first course in the curriculum.

For an orientation to the wider curriculum (and Ms. Reyes, the patient who appears in every course), see the [start-here repo](https://github.com/clinical-informatics/start-here). You can also begin here directly.

---

## How to start

1. Click the Codespaces badge above. A development environment loads in your browser. Allow about ninety seconds.
2. The course menu (`home.py`) opens automatically.
3. Begin with **Track 01: Decomposing a clinical problem**. The tracks run in order.

---

## Course map

Five tracks plus a capstone. Each track is a short interactive notebook (20 to 40 minutes). The capstone is a Socratic design exercise.

| Track | Title | The scenario |
|---|---|---|
| 01 | Decomposing a clinical problem | A sepsis alert fires 40 times a day. Clinicians ignore it. Why? You'll rebuild the rule yourself and see what went wrong. |
| 02 | Patterns, rules, and edge cases | Start with "flag HR>100 and temp>38.5." Add a condition. Watch every edge case appear. |
| 03 | Abstraction: what to ignore | Which features would you leave out of a readmission model, and why? Building the feature list is the assignment. |
| 04 | Algorithms in plain English | DAS28, step by step, with sliders for the joint counts and the labs. |
| 05 | When to trust a computer | Four questions to ask any algorithm. Applied to a fictional hospital deterioration score. |
| ... | **Capstone** | Design your own clinical decision rule. Socratic walkthrough. The output is a written design document. |

## What you can do afterward

- Break a clinical problem into its computational parts: inputs, outputs, rules, edge cases.
- Read a clinical decision rule and identify what it assumes, what it ignores, and who it might fail.
- Hold a credible conversation with a data scientist or vendor about what their algorithm does.

## Where this goes next

Concepts introduced here return in:

- **04: Clinical epidemiology**, at the 2x2 table and the question of which patients a test actually catches.
- **09: AI in medicine**, in the appraisal of a published clinical model.
- **12: Clinical decision support**, in the design of a real CDS rule.

Each later course flags when it picks up a thread from here.

---

## Repo contents

```
01-computational-thinking/
├── home.py                          ← Marimo course menu (opens automatically)
├── GLOSSARY.md                      ← Plain-English definitions of terms used here
├── track-01-decomposing/            ← One track per folder
├── track-02-patterns-rules/
├── track-03-abstraction/
├── track-04-algorithms-plain-english/
├── track-05-when-to-trust/
├── capstone/                        ← Socratic design exercise
└── shared/                          ← Symlink to ../start-here/shared/, the components every course imports
```

---

## License and use

- **Course content:** Creative Commons BY 4.0. Use it, remix it, teach with it. Please credit Mario David Felix, MD MHS.
- **Code:** MIT.

This is a single-author curriculum, not an open contribution project. Pull requests are not accepted. To report an error or suggest something, open an issue.
