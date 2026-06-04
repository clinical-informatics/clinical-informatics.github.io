"""Course 21: pathology, ancillary systems, and medical device integration.

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
        # 21: Pathology, ancillary systems, and medical device integration

        ## The systems-side gap-fill: laboratory information systems, anatomic and clinical pathology workflows, digital pathology, pharmacy systems, medical device integration, and the rest of the ancillary-system ecosystem the EHR depends on.

        This course is currently scaffolded. The track folders exist with short READMEs describing what each one will cover; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for progress.

        ### Tracks

        | # | Track | What it will cover |
        |---|---|---|
        | 01 | **Pathology informatics and the LIS** | Anatomic vs clinical pathology. The LIS as a system: order entry, accessioning, instrument autoverification, result release. AP-CP integration. |
        | 02 | **Digital pathology and whole-slide imaging** | WSI formats (BigTIFF, DICOM WSI), viewer architecture, telepathology, FDA-cleared primary diagnosis. AI in pathology (cross-ref Course 09). |
        | 03 | **Pharmacy informatics and the closed-loop medication system** | CPOE, pharmacy verification, eMAR, BCMA, smart pumps. The five rights as system goal. Cross-ref Course 12. |
        | 04 | **Medical device integration (MDI)** | IEEE 11073, HL7 v2 device messaging, FHIR Device and DeviceMetric. Vital-signs monitors, ventilators, anesthesia. The mixed-vendor reality and device cybersecurity. |
        | 05 | **Other ancillary systems** | Scheduling and registration (ADT), dietary, materials management. Imaging (PACS/DICOM/RIS) callback to Course 05. The ancillary-to-clinical interface pattern. |
        | 06 | **Special and emerging data sources** | Patient-generated data, genomic data, SDOH, wearables. The "everything is FHIR now" pattern alongside format diversity in legacy ancillaries. |

        ### Capstone

        **Audit the LIS-and-pathology rollout at a synthetic 350-bed community hospital across instrument integration, autoverification, AP-CP integration, EHR result delivery, and pharmacy/device interfaces (Socratic).**

        ---

        Each track folder has a `README.md` you can read now. The `notebook.py` files render a placeholder until the track is built.
        """
    )
    return


if __name__ == "__main__":
    app.run()
