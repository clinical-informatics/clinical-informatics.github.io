"""Course 05: EHR systems.

Marimo course menu. Shows the five tracks and the capstone, with
one-paragraph descriptions and direct-launch buttons.
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
        # 05: EHR systems

        ## How the EHR actually stores and moves data, past the UI.

        Five tracks plus a building capstone. Each track pairs a one-page intro with an interactive Marimo notebook. The intros frame the question and the vocabulary; the notebooks are where you build intuition through interactive work, all anchored on Ms. Elena Reyes.

        Written by **Mario David Felix, MD MHS**.

        ### Tracks

        | # | Track | What it covers |
        |---|---|---|
        | 01 | **How EHRs structure data internally** | The relational schema behind the chart, the flowsheet (EAV) pattern, indexes, and the physical storage layer (block vs object, SSD vs HDD, on-prem vs cloud, RPO and RTO). |
        | 02 | **HL7 v2, CDA, and what we inherited** | The historical arc. Real ADT and ORU messages, a CDA fragment, and what each format could and could not do. Forward reference to FHIR. |
        | 03 | **Clinical data warehouses** | OLTP versus OLAP, ETL and ELT, the warehouse / lake / lakehouse distinction, and the star schema walked on Ms. Reyes's CRP. |
        | 04 | **Imaging informatics: PACS, DICOM, RIS, structured reporting** | The four-system imaging architecture. DICOM tags and the study / series / instance hierarchy, DIMSE versus DICOMweb, structured reporting versus PDF. Reyes's hand-radiograph series. |
        | 05 | **Real-world data quality problems** | The five Weiskopf-Weng dimensions and the recurring problem families (duplicate patients, inconsistent coding, missing structured data, note-only findings, terminology drift, plausibility failures, MRN drift, phantom encounters). |

        ### Capstone

        **Audit a synthetic EHR extract for data quality issues**, propose remediation, and apply the cleanup decisions with `shared.cohort_builder` to watch attrition shape the final cohort. Building capstone; ends in a one-page hand-off memo.

        ---

        Each track folder has a `README.md` you can read on the side, a reference essay `XX.X-*.md`, the Marimo `notebook.py`, and a curated `go-deeper.md`. Open the notebooks in Marimo to do the work.
        """
    )
    return


if __name__ == "__main__":
    app.run()
