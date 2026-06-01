"""Course 20: Bioinformatics for clinical informaticists.

Marimo course menu. Five tracks plus the precision-medicine-program Socratic
capstone that closes the curriculum.
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

        ## The final course in the curriculum. Concept level only.

        Five tracks plus the Socratic precision-medicine-program capstone. The course covers where genomic and molecular data live in clinical and research systems, how research bioinformatics infrastructure is organized, and how clinical genomics intersects with the EHR. Ms. Reyes's HLA-DRB1 shared-epitope test, her TPMT screening, and her 23andMe direct-to-consumer test carry the course end to end.

        ### Tracks

        | # | Track | What it covers |
        |---|---|---|
        | 01 | **What bioinformatics is** | The molecular-to-translational-to-clinical-genomics spectrum. Reyes's HLA-DRB1 test from buccal swab to chart line. |
        | 02 | **Genomic data structures and file types** | FASTQ, BAM, VCF, GFF / GTF, BED. What each contains and when. Interactive format identifier. |
        | 03 | **Clinical genomics in the EHR** | HL7 Genomics Reporting IG, ACMG 79-gene list, pharmacogenomics, the PDF-vs-structured-field gap. |
        | 04 | **Research bioinformatics infrastructure** | Cores, HPC, secure enclaves, dbGaP. NCBI databases (GenBank, dbSNP, ClinVar, OMIM). Public datasets. |
        | 05 | **Population genomics, equity, and the future** | All of Us, UK Biobank, MyCode, eMERGE. PRS. Ancestry vs race. DTC testing. |

        ### Capstone

        **Design a precision medicine program.** A pharmacogenomic-testing-at-the-point-of-prescribing program walked across six Socratic dimensions: infrastructure, standards, returns to patients, research/clinical coexistence, governance, equity. The capstone that closes the curriculum.

        ---

        Each track folder has a `README.md` and a `notebook.py`. Open the notebook in Marimo to interact with the material.
        """
    )
    return


if __name__ == "__main__":
    app.run()
