"""Track 04: Imaging informatics (PACS, DICOM, RIS, structured reporting).

The imaging subsystem inside the enterprise. DICOM tags and the
study/series/instance hierarchy, PACS as storage and viewing, RIS for
orders and reporting, DICOM Structured Reporting versus the PDF report
that most hospitals still ship. Carried by Ms. Reyes's bilateral hand
radiograph series.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import types

    import marimo as mo
    import pandas as pd

    # Cross-reference helpers inlined from shared/cross_reference.py so the
    # WASM export is self-contained. Exposed as the `xref` namespace so the
    # call sites read the same as before.
    _COURSE_TITLES = {
        "00": "Foundations of clinical informatics",
        "01": "Computational thinking",
        "02": "Data literacy",
        "03": "Privacy, ethics, and governance",
        "04": "Clinical epidemiology",
        "05": "EHR systems",
        "06": "Learn FHIR",
        "07": "Data wrangling and engineering",
        "08": "Clinical visualization",
        "09": "AI in medicine",
        "10": "NLP and clinical text",
        "11": "Health economics data",
        "12": "Clinical decision support",
        "13": "Research reproducibility",
        "14": "Interoperability policy",
        "15": "Data storytelling",
    }

    def _course_label(course_id):
        title = _COURSE_TITLES.get(course_id.split("-")[0])
        if title is None:
            return course_id
        return f"course {course_id.split('-')[0]}: {title}"

    def _xref_callback(from_course, to_course, topic, body):
        src = _course_label(to_course)
        return mo.callout(
            mo.vstack([mo.md(f"**Remember {topic} from {src}?**"), mo.md(body)]),
            kind="info",
        )

    def _xref_forward(from_course, to_course, topic, body):
        dst = _course_label(to_course)
        return mo.callout(
            mo.vstack([mo.md(f"**Forward to {dst}: {topic}**"), mo.md(body)]),
            kind="neutral",
        )

    xref = types.SimpleNamespace(callback=_xref_callback, forward=_xref_forward)

    return mo, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 04: Imaging informatics (PACS, DICOM, RIS, structured reporting)

        ## The four-system view

        Open Ms. Reyes's chart and click into her 2024-08-04 bilateral hand series. The chart shows three thumbnails (PA right, PA left, oblique both hands) and a one-paragraph radiology report. From the chart, it looks like a single integrated view.

        Behind that view are four distinct systems. They have been talking to each other for thirty years, and the conventions of that conversation determine almost everything about how clinical imaging actually moves through a hospital.

        ```
        +---------+   order   +-----+  worklist  +-----------+
        |   EHR   |---------->| RIS |----------->| Modality  |   (the x-ray machine itself)
        +---------+           +-----+            +-----------+
             ^                   ^                     |
             | report PDF        | dictation           | DICOM C-STORE
             |                   |                     v
             |              +---------+   image   +--------+
             +--------------|  RIS    |<----------|  PACS  |
                            |dictation|           +--------+
                            +---------+                 |
                                                        | viewer
                                                        v
                                                   +----------+
                                                   |Radiologist|
                                                   |  reading  |
                                                   |   room    |
                                                   +----------+
        ```

        - **EHR** writes an imaging order. The order carries the patient identifier, the study type, the indication.
        - **RIS** (Radiology Information System) takes the order, schedules it, sends a worklist entry to the modality, receives the dictation back, and forwards the final report PDF to the EHR.
        - **Modality** is the imaging device itself (the digital radiography unit, the CT, the MRI). It pulls a DICOM Modality Worklist when the patient arrives, performs the study, and sends DICOM image objects to the PACS.
        - **PACS** (Picture Archiving and Communication System) stores the DICOM images, serves them to viewers, and handles the storage tiering across hot, warm, and cold media.

        Four systems, three protocols (DICOM between the modality and the PACS, HL7 v2 between the EHR and the RIS, sometimes also between the RIS and the PACS, and increasingly DICOMweb on top of HTTPS). When you understand the four-system picture, every downstream choice about how imaging data flows starts to make sense.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## DICOM: the standard

        **DICOM** stands for Digital Imaging and Communications in Medicine. It is the standard the field has used for imaging data exchange since 1993 (DICOM 3.0). It has two parts: a *file format* (how a single image and its metadata are encoded into a `.dcm` file) and a *network protocol* (how DICOM files are exchanged between systems).

        Three structural facts about DICOM that shape how you reason about imaging informatics:

        1. **The hierarchy is Patient -> Study -> Series -> Instance.** A *patient* has one or more *studies*. A study (e.g. Ms. Reyes's 2024-08-04 hand series) contains one or more *series*. A series contains one or more *instances*. Each instance is one image (or one slice for cross-sectional modalities).
        2. **Each instance is identified by a globally unique UID.** DICOM UIDs are long strings like `1.2.840.113619.2.55.3.604688334.123.1722777612.345`. They are constructed so that no two instances anywhere in the world should collide.
        3. **Metadata travels with the pixels.** A DICOM file is the image pixels plus a header of *tags*. Each tag is a `(group, element)` pair like `(0010, 0010)` for Patient Name. Hundreds of tags are defined in the standard; vendors add private tags for vendor-specific information.

        Below is what the DICOM header for Ms. Reyes's 2024-08-04 right-hand PA radiograph looks like, with the most-relevant tags decoded.
        """
    )
    return


@app.cell
def _(mo, pd):
    dicom_tags = pd.DataFrame([
        {"tag": "(0008,0016)", "name": "SOP Class UID", "value": "1.2.840.10008.5.1.4.1.1.1.1 (Digital X-Ray Image Storage - For Presentation)"},
        {"tag": "(0008,0018)", "name": "SOP Instance UID", "value": "1.2.840.113619.2.55.3.604688334.123.1722777612.345"},
        {"tag": "(0008,0020)", "name": "Study Date", "value": "20240804"},
        {"tag": "(0008,0030)", "name": "Study Time", "value": "091523"},
        {"tag": "(0008,0050)", "name": "Accession Number", "value": "ACC-2024-080401"},
        {"tag": "(0008,0060)", "name": "Modality", "value": "DX (Digital Radiography)"},
        {"tag": "(0008,0070)", "name": "Manufacturer", "value": "Synthetic Imaging Corp"},
        {"tag": "(0008,0080)", "name": "Institution Name", "value": "Bay Rheumatology Clinic"},
        {"tag": "(0008,0090)", "name": "Referring Physician", "value": "Bennett^Maya^^^MD"},
        {"tag": "(0008,1030)", "name": "Study Description", "value": "Hands, bilateral, 3 views"},
        {"tag": "(0008,103E)", "name": "Series Description", "value": "PA right hand"},
        {"tag": "(0010,0010)", "name": "Patient Name", "value": "Reyes^Elena^Maria"},
        {"tag": "(0010,0020)", "name": "Patient ID", "value": "ER-001"},
        {"tag": "(0010,0030)", "name": "Patient Birth Date", "value": "19740209"},
        {"tag": "(0010,0040)", "name": "Patient Sex", "value": "F"},
        {"tag": "(0018,0015)", "name": "Body Part Examined", "value": "HAND"},
        {"tag": "(0018,1110)", "name": "Distance Source to Detector", "value": "1000 mm"},
        {"tag": "(0018,5101)", "name": "View Position", "value": "PA"},
        {"tag": "(0020,000D)", "name": "Study Instance UID", "value": "1.2.840.113619.2.55.3.604688334.123.1722777200.1"},
        {"tag": "(0020,000E)", "name": "Series Instance UID", "value": "1.2.840.113619.2.55.3.604688334.123.1722777612.1"},
        {"tag": "(0020,0011)", "name": "Series Number", "value": "1"},
        {"tag": "(0020,0013)", "name": "Instance Number", "value": "1"},
        {"tag": "(0020,0020)", "name": "Patient Orientation", "value": "A\\R"},
        {"tag": "(0028,0010)", "name": "Rows", "value": "2500"},
        {"tag": "(0028,0011)", "name": "Columns", "value": "2048"},
        {"tag": "(0028,0030)", "name": "Pixel Spacing", "value": "0.139\\0.139"},
        {"tag": "(0028,0100)", "name": "Bits Allocated", "value": "16"},
        {"tag": "(0028,1052)", "name": "Rescale Intercept", "value": "0"},
        {"tag": "(0028,1053)", "name": "Rescale Slope", "value": "1"},
        {"tag": "(7FE0,0010)", "name": "Pixel Data", "value": "[binary, 10,240,000 bytes]"},
    ])
    dicom_tags.index = range(1, len(dicom_tags) + 1)
    dicom_tags.index.name = "row"

    mo.vstack([
        mo.md("**DICOM header dump for Reyes's 2024-08-04 right-hand PA radiograph (selected tags):**"),
        mo.as_html(dicom_tags),
        mo.callout(
            mo.md(
                "Three things to read off this header. **First, the SOP Class UID** (top row) tells the receiver what kind of object this is. "
                "`1.2.840.10008.5.1.4.1.1.1.1` is the SOP Class for Digital X-Ray Image (for presentation). The receiver looks at that "
                "tag to decide how to handle the file. **Second, the patient-identity tags** `(0010,xxxx)` carry MRN, name, DOB, sex. "
                "Those identity tags travel embedded inside the DICOM header on every instance, which is the source of most DICOM PHI exposure when images get shared. "
                "**Third, the UIDs `(0020,000D)` and `(0020,000E)`** are the persistent identifiers that PACS-to-PACS exchange relies on. "
                "Other systems refer to this image by its Study Instance UID and Series Instance UID; both are stable forever."
            ),
            kind="info",
        ),
    ])
    return (dicom_tags,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The DICOM hierarchy on Ms. Reyes

        Three studies, totaling six instances:

        | Study UID (truncated) | Study Date | Description | Series | Instances |
        |---|---|---|---|---|
        | `...1717200.1` | 2022-02-14 | Hands, bilateral, 2 views | 2 | 2 (PA right, PA left) |
        | `...1720310.1` | 2022-08-18 | Hands, bilateral, 2 views | 2 | 2 (PA right, PA left) |
        | `...1722777200.1` | 2024-08-04 | Hands, bilateral, 3 views | 3 | 3 (PA right, PA left, oblique both) |

        The 2024 study has three series because oblique views were added that year for better visualization of MCP-joint erosion. The series are independent: a viewer can pull a single series, compare the same series across studies, or load everything.

        For Sharp/van der Heijde scoring of erosion and joint-space narrowing, the radiologist will load the PA views from all three studies side by side in the reading-room viewer. That comparison requires the PACS to pull from all three studies, possibly from different storage tiers (the 2022 study has been migrated to warm storage; the 2024 study is still on hot).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## PACS: storage and viewing

        A **PACS** is the imaging system's analog of the EHR database. It stores DICOM instances, indexes them by study/series/instance UIDs and by patient identifiers, and serves them to viewers. Production PACS implementations have three responsibilities:

        1. **Receive** new images from modalities. The modality sends each instance to the PACS using **DICOM C-STORE**, an operation in the legacy DICOM network protocol (also called DIMSE).
        2. **Store** images across tiers (Track 01). Recent studies live on flash. Studies older than two to five years migrate to warmer SSD or HDD tiers. Studies older than ten years often live on cold-archive object storage with a documented recall latency.
        3. **Serve** images to viewers. The reading-room workstation, the EHR-embedded viewer, the mobile radiologist app, and the AI inference pipeline all ask the PACS for images.

        ### How systems retrieve images from a PACS

        Two protocol families:

        - **Legacy DIMSE.** Verb-based queries (C-FIND to search, C-MOVE or C-GET to retrieve) over a custom TCP protocol. Built in the early 1990s. Still ubiquitous between modality and PACS. Painful for web applications because it predates HTTP.
        - **DICOMweb.** The modern alternative built on HTTPS. Three services:
            - **QIDO-RS** (Query based on ID for DICOM Objects, Restful Services). Search for studies by patient ID, accession number, study date.
            - **WADO-RS** (Web Access to DICOM Objects, Restful Services). Retrieve studies, series, or instances by URL.
            - **STOW-RS** (Store Over the Web, Restful Services). Submit new instances.

        DICOMweb is the imaging-equivalent of FHIR. The same architectural bet: HTTP, JSON for metadata responses, REST verbs. Vendors are still in the middle of adopting it. As of 2026, most new PACS support DICOMweb natively. Many legacy installations still expose only DIMSE.

        When a web-based viewer (an EHR-embedded viewer, a SMART-on-FHIR imaging app, an AI tool) asks the PACS for Ms. Reyes's 2024 hand series, the request URL looks like:

        ```
        GET /dicom-web/studies/1.2.840.113619.2.55.3.604688334.123.1722777200.1
            /series/1.2.840.113619.2.55.3.604688334.123.1722777612.1
            /instances
            /metadata
        ```

        And the PACS returns the DICOM metadata as JSON. That URL pattern is the imaging-side answer to the FHIR resource URL pattern from course 06.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## RIS: orders and reporting

        The **RIS** (Radiology Information System) is the workflow layer that sits between the EHR and the imaging hardware. Three responsibilities:

        1. **Order management.** Receive imaging orders from the EHR (typically as HL7 v2 ORM messages, increasingly as FHIR ServiceRequests). Schedule the study. Manage the worklist.
        2. **Modality Worklist.** Provide a DICOM Modality Worklist to each modality so that when a patient arrives, the radiographer can pick the right order without typing anything. The Modality Worklist is what populates the patient demographics on the DICOM header automatically: the worklist message includes the MRN, name, DOB, accession number, and procedure code, and the modality copies those values into the DICOM header of every instance it produces.
        3. **Reporting workflow.** Receive the radiologist's dictation, manage the structured report or free-text PDF, and send the final report back to the EHR as an HL7 v2 MDM message (or, increasingly, as a FHIR DiagnosticReport).

        The RIS is invisible to most clinicians, but it is where most imaging-workflow problems live. If Ms. Reyes shows up for her hand series and the modality cannot find her on the worklist, the RIS has failed. If the radiologist's dictation never makes it to the chart, the RIS has failed.

        ### Putting it together: Reyes's 2024-08-04 study

        | Step | System | Protocol | What happened |
        |---|---|---|---|
        | 1 | EHR | (chart) | Dr. Bennett orders bilateral hand radiographs from the rheum visit |
        | 2 | EHR -> RIS | HL7 v2 ORM | Order message with patient MRN, accession ACC-2024-080401, procedure code |
        | 3 | RIS | (internal) | Schedules Ms. Reyes for 2024-08-04 09:15 |
        | 4 | RIS -> modality | DICOM Modality Worklist | Worklist entry pushed to the digital radiography unit |
        | 5 | Modality | (study) | Three exposures acquired, three DICOM instances created |
        | 6 | Modality -> PACS | DICOM C-STORE | Three instances stored in PACS |
        | 7 | Radiologist -> PACS | DICOM viewer | Comparison reading with 2022 studies opened |
        | 8 | Radiologist -> RIS | dictation | Sharp/van der Heijde scored, report dictated |
        | 9 | RIS -> EHR | HL7 v2 MDM | Final report PDF and structured report attached to Ms. Reyes's chart |

        Three systems and three protocols collaborated to deliver one chart-side row. **When the row is missing** (the report never showed up, or the images do not load, or the patient is not on the worklist), the problem is somewhere in that chain, and being able to walk it backwards is most of the troubleshooting work.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Structured reporting (DICOM SR) versus the PDF reality

        Ms. Reyes's radiology report from 2024-08-04 contains, somewhere in the prose, a Sharp/van der Heijde modified total score of **18**, broken down as erosion 11 (of a possible 280) and joint-space narrowing 7 (of a possible 168). The actual report PDF that lands on the chart reads:

        > Bilateral hands and wrists, three views. Erosive changes are present at the right second and third MCP joints and the left third MCP joint, with new periarticular osteopenia at the bilateral wrists since the prior 2022-08-18 study. Joint-space narrowing is moderate at the right second MCP. The modified Sharp/van der Heijde score is 18 (erosion 11, JSN 7), compared with 12 (erosion 8, JSN 4) on the 2022-08-18 prior. Findings are consistent with progressive erosive rheumatoid arthritis.

        Beautiful prose. Completely unstructured. If you want to plot Ms. Reyes's Sharp/van der Heijde trajectory over five years, you have to parse the score out of the prose by hand or by NLP. The PDF carries the answer; it does not surface it.

        ### What DICOM SR offers

        **DICOM Structured Reporting (DICOM SR)** is a DICOM object type designed to carry the same information *as structured fields*. A Sharp/van der Heijde SR would look like a tree of templated nodes:

        ```
        Imaging Measurement Report
          Patient: Reyes, Elena (ER-001)
          Procedure: Hands bilateral, 3 views, 2024-08-04
          Findings:
            Sharp/van der Heijde modified total score: 18
              Erosion subscore: 11 / 280
              Joint-space narrowing subscore: 7 / 168
            Joint-specific findings:
              Right MCP 2: erosion present, score 3
              Right MCP 3: erosion present, score 2
              Left MCP 3: erosion present, score 2
              Right MCP 2: JSN moderate, score 2
              [...]
            Comparison: 2022-08-18 study, modified total 12, change +6
            Interpretation: Progressive erosive RA
        ```

        Each line is a coded entry tied to a SNOMED CT concept or a DICOM-defined code. A downstream analytical pipeline can pull the modified total score directly into a time series, with no NLP and no manual abstraction.

        ### Why most reports are still PDFs

        Three reasons:

        1. **Radiologist workflow.** Dictation-based reporting is faster for the radiologist than structured-form filling. The PDF is whatever the speech-to-text engine produces, lightly edited.
        2. **Template proliferation.** DICOM SR templates exist for many domains, but coverage is uneven. A radiologist who has to switch between five different structured templates per shift will hate it.
        3. **Receiver tolerance.** The EHR happily ingests a PDF and attaches it to the chart. There is no incentive on the EHR side to push for SR.

        The trend is slow but real. AI radiology tools (Course 09) increasingly produce DICOM SR outputs because they can. Some specialties (mammography with BI-RADS, lung-cancer screening with Lung-RADS, prostate MRI with PI-RADS) have moved meaningfully toward structured reporting because of the standardized templates the specialty itself adopted. The general radiology report is still mostly a PDF.

        We pick up this thread in Track 05 of this course (data quality) and in Course 10 (NLP and clinical text), since extracting structured data from radiology PDFs is one of the largest NLP use cases in clinical informatics.
        """
    )
    return


@app.cell
def _(mo):
    imaging_quiz = mo.ui.radio(
        options=[
            "DIMSE C-STORE",
            "HL7 v2 ORM",
            "HL7 v2 MDM",
            "DICOMweb QIDO-RS",
        ],
        label=(
            "**The 2024-08-04 hand series is acquired on the digital radiography unit. The unit sends the three "
            "DICOM instances to the PACS. Which protocol carries that hand-off?**"
        ),
    )
    imaging_quiz
    return (imaging_quiz,)


@app.cell
def _(imaging_quiz, mo):
    mo.stop(imaging_quiz.value is None, mo.md("_Choose an answer._"))
    imaging_correct = imaging_quiz.value == "DIMSE C-STORE"

    if imaging_correct:
        imaging_feedback = (
            "Right. The legacy DICOM network protocol (DIMSE) carries C-STORE between the modality and the PACS. "
            "Modalities have been speaking C-STORE for thirty years and most still do, even in hospitals that have "
            "added DICOMweb on the viewer side. HL7 v2 ORM is the order message between the EHR and the RIS; "
            "HL7 v2 MDM is the final report going back to the EHR. DICOMweb QIDO-RS is the modern web-based search "
            "verb, not a modality-to-PACS push. The chain in order is: EHR -> RIS (ORM) -> modality (Modality Worklist) "
            "-> PACS (DIMSE C-STORE) -> EHR (MDM report)."
        )
    elif imaging_quiz.value == "HL7 v2 ORM":
        imaging_feedback = (
            "Wrong direction. HL7 v2 ORM is the *order* message that goes from the EHR to the RIS at the start of the "
            "workflow. The modality-to-PACS hand-off, where the actual images move, is DICOM-side: DIMSE C-STORE."
        )
    elif imaging_quiz.value == "HL7 v2 MDM":
        imaging_feedback = (
            "MDM is the final-report message back to the EHR after dictation. It does not carry the image instances "
            "themselves. The image push from modality to PACS is DIMSE C-STORE."
        )
    else:
        imaging_feedback = (
            "QIDO-RS is the modern DICOMweb *search* verb (Query based on ID for DICOM Objects). It is used by viewers "
            "to find studies by ID, not by the modality to store new images. The modality-to-PACS push is DIMSE C-STORE."
        )
    mo.callout(mo.md(imaging_feedback), kind="success" if imaging_correct else "warn")
    return


@app.cell
def _(xref):
    xref.forward(
        from_course="05",
        to_course="09",
        topic="Radiology AI",
        body=(
            "This track set up the data flow. Course 09 (AI in medicine) is where you evaluate the AI models that read "
            "the same images Reyes's radiologist did. Two of the FDA-cleared radiology AI categories that matter for RA "
            "monitoring are bone-density estimation and joint-erosion detection. The course-09 critical-appraisal "
            "framework (training population, outcome definition, validation approach, calibration reporting, subgroup "
            "performance) applies directly to imaging AI. The trick for imaging specifically is that the training set "
            "is a set of DICOM studies, the outcome is a structured report or pixel-level annotation, and the deployment "
            "context is the reading-room workflow above."
        ),
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Where this leaves you

        Imaging is the part of the clinical data ecosystem that lives in parallel to the EHR rather than inside it. Four systems collaborate on every study (EHR, RIS, modality, PACS), DICOM is the lingua franca between them, and the radiologist's interpretation lands on the chart as a PDF even when the structured-reporting machinery exists to do better.

        Track 05 picks up the PDF-versus-structured-data tension as one instance of the broader real-world data-quality story. The capstone of this course is where the five tracks converge.
        """
    )
    return


if __name__ == "__main__":
    app.run()
