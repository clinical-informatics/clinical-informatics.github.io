# 14: Interoperability policy

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/14-interoperability-policy?quickstart=1)

**The policy context that makes the technical courses meaningful.**

Five tracks plus a Socratic policy-analysis capstone. The course covers why federal policy had to enter the picture at all (information blocking is the problem the rest of the field had been describing without naming), what the 21st Century Cures Act required and what its exceptions actually mean in practice, how the ONC and CMS rules turned the Cures Act into technical mandates that explain why FHIR adoption accelerated when it did, how the international policy landscape differs in foundational ways (GDPR, NHS Digital, the European Health Data Space), and where the gaps still are (patient matching, USCDI evolution, TEFCA roll-out, AI transparency under HTI-1). The capstone applies the framework to three real-shaped scenarios in which a patient, a researcher, and an outside vendor each run into the policy layer.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum. Course 06 (FHIR) and Course 07 (OMOP) are the natural prerequisites; the technical standards those courses cover are what the policies in this course mandate, restrict, or accelerate.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | Why policy exists | Information blocking as the structural problem. HITECH and Meaningful Use as the precondition. Who benefited from blocking and how. |
| 02 | 21st Century Cures Act | What the 2016 law required. The information-blocking exceptions (eight in the original Cures Final Rule, ten after HTI-1). What changed in practice, what did not. |
| 03 | ONC and CMS interoperability rules | The Cures Act Final Rule, HTI-1, HTI-2, CMS Patient Access and Payer-to-Payer. Cross-reference to Course 06: why FHIR adoption accelerated. |
| 04 | The international landscape | GDPR versus HIPAA. NHS Digital. The European Health Data Space. What other countries do differently and why. |
| 05 | Where the gaps still are | Patient matching without a national patient identifier. USCDI evolution. TEFCA and the QHIN network. AI transparency under HTI-1. |
| ... | **Capstone** | Apply the policy framework to three health-system scenarios (records access, dataset access, vendor restriction) and produce a written analysis (Socratic). |

## What you'll find in this repo

```
14-interoperability-policy/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── track-01-why-policy/
├── track-02-cures-act/
├── track-03-onc-cms-rules/
├── track-04-international/
├── track-05-gaps/
└── capstone/
```

## How to start

Click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) opens in a browser tab. Each track folder has a `README.md` that frames the topic and a `notebook.py` that contains the interactive material.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
