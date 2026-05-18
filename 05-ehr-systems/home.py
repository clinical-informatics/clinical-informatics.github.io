"""Course 05: EHR systems.

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
        # 05: EHR systems

        ## How the EHR actually stores and moves data, past the UI.

        This course is currently scaffolded. The track folders exist with short READMEs describing what each one will cover; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for progress.

        ### Tracks

        | # | Track | What it will cover |
        |---|---|---|
        | 01 | **How EHRs structure data internally** | What the database behind the interface looks like. Why clicking 'medications' pulls from three tables. |
        | 02 | **HL7 v2, CDA, and the mess we inherited** | The historical arc. Why each standard made sense and what it couldn't do. Forward reference to FHIR. |
        | 03 | **Clinical data warehouses** | What a CDW is, how it differs from the operational EHR, why research uses it. |
        | 04 | **Imaging informatics: PACS, DICOM, RIS, structured reporting** | The imaging subsystem. DICOM tags and study/series/instance hierarchy, PACS as storage and viewing, RIS for orders and reporting, structured reporting vs free-text PDF. Reyes's hand radiograph series. |
        | 05 | **Real-world data quality problems** | Duplicate patients, inconsistent coding, missing structured data, note-only findings, applied to Ms. Reyes. |

        ### Capstone

        **Audit a synthetic EHR extract for data quality issues with a structured checklist interface.**

        ---

        Each track folder has a `README.md` you can read now. The `notebook.py` files render a placeholder until the track is built.
        """
    )
    return


if __name__ == "__main__":
    app.run()
