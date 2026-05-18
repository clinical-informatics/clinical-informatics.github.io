# 20: Bioinformatics for clinical informaticists

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/20-bioinformatics?quickstart=1)

**The final course. Concept-level only. How bioinformatics relates to clinical informatics and the health system, plus the research infrastructure around it. Reyes hooks: her HLA-DRB1 shared-epitope test, TPMT screening, 23andMe DTC results.**

Each track in this course pairs a written introduction with an interactive Marimo notebook. The intro frames the question and the vocabulary; the notebook is where you build intuition through interactive work.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum. It is currently **scaffolded only**: the structure, file layout, and short per-track descriptions are in place; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for current progress.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | What bioinformatics is and how it relates to clinical informatics | Definition. Molecular to translational to clinical genomics. Brief history. Reyes's HLA-DRB1 test walked from buccal swab to chart line. |
| 02 | Genomic data structures and file types | Concept-level FASTQ, BAM, VCF, GFF/GTF, BED. What each contains, when each appears. Interactive: format identifier. |
| 03 | Clinical genomics in the EHR | HL7 Genomics Reporting IG, GA4GH variant representation, ACMG 79-gene list. Pharmacogenomics (TPMT, CYP2C19, HLA-B*5701). The PDF-vs-structured-field gap. |
| 04 | Research bioinformatics infrastructure | Cores, HPC clusters, secure enclaves, dbGaP. NHGRI and NCBI databases (GenBank, dbSNP, ClinVar, OMIM). CTSA. TCGA/GTEx/ENCODE/gnomAD. |
| 05 | Population genomics, equity, and the future | All of Us, UK Biobank, MyCode, eMERGE. PRS at concept level. Ancestry vs race in genomics. DTC testing. Reyes's 23andMe results. |
| ... | **Capstone** | Design a precision medicine program (pharmacogenomic testing at the point of high-risk prescribing): infrastructure, standards, returns to patients, research/clinical coexistence, governance, equity (Socratic). Closes the curriculum. |

## What you'll find in this repo

```
20-bioinformatics/
├── README.md
├── pyproject.toml
├── .devcontainer/devcontainer.json
├── home.py                  ← Marimo course menu (auto-launches in Codespaces)
├── GLOSSARY.md
├── shared/                  ← symlink to start-here/shared/
├── patients/                ← symlink to start-here/patients/
├── track-01-what-is-bioinformatics/
├── track-02-genomic-file-types/
├── track-03-clinical-genomics-ehr/
├── track-04-research-infrastructure/
├── track-05-population-genomics-equity/
└── capstone/
```

## How to start

Once the content is built: click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) will open in your browser. While the course is still scaffolded, the home.py renders a track list with descriptions so you can see what's coming.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
