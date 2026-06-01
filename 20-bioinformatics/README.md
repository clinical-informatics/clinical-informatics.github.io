# 20: Bioinformatics for clinical informaticists

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/clinical-informatics/20-bioinformatics?quickstart=1)

**The final course. Concept level only.**

Five tracks plus a Socratic precision-medicine-program capstone. The course is for clinical informaticists who do not do bench bioinformatics but need to understand where genomic and molecular data live in clinical and research systems, how research bioinformatics infrastructure is organized, and how clinical genomics intersects with the EHR. Ms. Reyes's HLA-DRB1 shared-epitope test, her TPMT screening, and her 23andMe direct-to-consumer test carry the course.

Written by **Mario David Felix, MD MHS**.

This course is part of the [clinical-informatics](https://github.com/clinical-informatics/start-here) curriculum.

---

## Course map

| Track | Title | What it covers |
|---|---|---|
| 01 | What bioinformatics is and how it relates to clinical informatics | The molecular-to-translational-to-clinical-genomics spectrum. The boundary between bioinformatics and clinical informatics. Brief field history. Ms. Reyes's HLA-DRB1 test walked from buccal swab to chart line. |
| 02 | Genomic data structures and file types | The sequencer-to-report pipeline. FASTQ (raw reads), BAM (aligned reads), VCF (variant calls), GFF/GTF (annotations), BED (regions). What each contains and when each appears. An interactive file-type identifier on real-format snippets. |
| 03 | Clinical genomics in the EHR | The order-result-display loop. HL7 Genomics Reporting IG and GA4GH variant representation. The ACMG 79-gene incidental findings list. Pharmacogenomics (TPMT, CYP2C19, HLA-B*5701). The PDF-vs-structured-field gap on Reyes's HLA-DRB1 result. |
| 04 | Research bioinformatics infrastructure | Institutional ecosystem (genomics cores, computational biology cores, biostatistics cores, HPC, secure enclaves). Federal infrastructure (NHGRI, NCBI databases, CTSA). Public datasets (TCGA, GTEx, ENCODE, gnomAD). Reyes's hypothetical RA-biobank enrollment walked through the infrastructure. |
| 05 | Population genomics, equity, and the future | All of Us, UK Biobank, MyCode, eMERGE network. Polygenic risk scores at concept level. Ancestry vs race in genomics. Direct-to-consumer testing and what it actually says. Reyes's 23andMe results. |
| ... | **Capstone** | Design a precision medicine program (pharmacogenomic testing at the point of high-risk prescribing) across infrastructure, standards, returns to patients, research/clinical coexistence, governance, and equity. The Socratic capstone that closes the curriculum. |

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

Click the Codespaces badge, wait about ninety seconds, and the course menu (`home.py`) opens in a browser tab. Each track folder has a `README.md` that frames the topic and a `notebook.py` that contains the interactive material.

## What this course is not

- Not a molecular bioinformatics course. No sequence-alignment algorithms beyond concept-level mention. No statistical genetics depth.
- Not a comprehensive clinical genomics course. Concept level only.
- Not a substitute for dedicated bioinformatics curricula (Coursera's Genomic Data Science, the EMBL-EBI training resources). Those are the right next steps for a reader who wants to go further.

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted.
