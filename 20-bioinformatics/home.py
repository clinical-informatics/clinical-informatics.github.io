"""Course 20: bioinformatics for clinical informaticists.

Marimo course menu. The course is currently scaffolded; track content will
be filled in as the curriculum builds out. The menu below lists the tracks
and a one-sentence description of what each one will cover.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # 20: Bioinformatics for clinical informaticists

        ## The final course. Concept-level only. How bioinformatics relates to clinical informatics and the health system, plus the research infrastructure around it. Reyes hooks: her HLA-DRB1 shared-epitope test, TPMT screening, 23andMe DTC results.

        This course is currently scaffolded. The track folders exist with short READMEs describing what each one will cover; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for progress.

        ### Tracks

        | # | Track | What it will cover |
        |---|---|---|
        | 01 | **What bioinformatics is and how it relates to clinical informatics** | Definition. Molecular to translational to clinical genomics. Brief history. Reyes's HLA-DRB1 test walked from buccal swab to chart line. |
        | 02 | **Genomic data structures and file types** | Concept-level FASTQ, BAM, VCF, GFF/GTF, BED. What each contains, when each appears. Interactive: format identifier. |
        | 03 | **Clinical genomics in the EHR** | HL7 Genomics Reporting IG, GA4GH variant representation, ACMG 79-gene list. Pharmacogenomics (TPMT, CYP2C19, HLA-B*5701). The PDF-vs-structured-field gap. |
        | 04 | **Research bioinformatics infrastructure** | Cores, HPC clusters, secure enclaves, dbGaP. NHGRI and NCBI databases (GenBank, dbSNP, ClinVar, OMIM). CTSA. TCGA/GTEx/ENCODE/gnomAD. |
        | 05 | **Population genomics, equity, and the future** | All of Us, UK Biobank, MyCode, eMERGE. PRS at concept level. Ancestry vs race in genomics. DTC testing. Reyes's 23andMe results. |

        ### Capstone

        **Design a precision medicine program (pharmacogenomic testing at the point of high-risk prescribing): infrastructure, standards, returns to patients, research/clinical coexistence, governance, equity (Socratic). Closes the curriculum.**

        ---

        Each track folder has a `README.md` you can read now. The `notebook.py` files render a placeholder until the track is built.
        """
    )
    return


if __name__ == "__main__":
    app.run()
