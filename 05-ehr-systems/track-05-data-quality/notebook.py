"""Track 05: Real-world data quality problems.

Five families of data-quality problem that show up in every clinical
data extract, illustrated on a synthetic but realistic export of
Ms. Reyes's records. Classified against the Weiskopf and Weng (2013)
data-quality framework. Sets up the course capstone.
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
        # Track 05: Real-world data quality problems

        ## What the architecture produces when it meets thirty years of clinical history

        Tracks 01 through 04 of this course taught you how the EHR is structured, how its messages move, how the warehouse sits next to it, and how imaging fits. All of that architecture is correct. None of it stops the export you actually receive from being a mess.

        A typical data request returns a CSV or a database extract. Some of the rows are right. Some are duplicated. Some have the diagnosis code spelled differently than every other row of the same patient. Some have an MRN that no longer matches the patient's current MRN (a merge happened). Some have a CRP value of "5,000" because somebody typed a comma where a decimal point should have gone. Some encounters show up that never happened, because a registration was started and abandoned.

        Cleaning this up is most of clinical data engineering. The reasons are structural (the architecture allows it, the EHR optimizes for charting and not for export), behavioral (clinicians enter data under time pressure), and historical (data quality conventions changed three times in the institution's history). This track is about the recurring shapes of the mess and the framework for classifying any new shape you find.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Weiskopf and Weng framework

        Nicole Weiskopf and Chunhua Weng's 2013 JAMIA paper *Methods and dimensions of electronic health record data quality assessment* is the standard reference. The paper reviews the published literature and lands on five dimensions that almost every assessment uses:

        | Dimension | Plain-English version | The question to ask |
        |---|---|---|
        | **Completeness** | Is the value present when it should be? | "Did we capture this fact at all?" |
        | **Correctness** | Does the recorded value match clinical reality? | "Is what we wrote down what actually happened?" |
        | **Concordance** | Do different parts of the record agree with each other? | "Does the problem list say RA but the diagnosis code say RA?" |
        | **Plausibility** | Is the value within clinically reasonable bounds? | "Is this CRP of 5000 mg/L plausible or a typo?" |
        | **Currency** | Is the value up to date for the question being asked? | "Is this active medication actually still being taken?" |

        Every concrete data-quality problem you find can be classified against one of these dimensions. Doing the classification is useful because the *fix* for each dimension is different. Completeness is fixed by upstream capture changes; correctness by validation rules; concordance by reconciliation routines; plausibility by range checks; currency by review cadence.

        The five problem families below each anchor on one or two of these dimensions. We walk them in order.
        """
    )
    return


@app.cell
def _(mo, pd):
    # Build the synthetic 15-row export with seeded data-quality problems.
    export = pd.DataFrame([
        # Reyes, three identifiers (duplicate patient)
        {"row_id": 1,  "mrn": "ER-001",   "name": "Reyes, Elena Maria", "dob": "1974-02-09",
         "service_date": "2022-02-14", "code_system": "ICD-10-CM", "code": "M79.7",   "display": "Polyarthralgia, unspecified",
         "value": None,    "unit": None,  "flag": None},
        {"row_id": 2,  "mrn": "ER-001",   "name": "Reyes, Elena",       "dob": "1974-02-09",
         "service_date": "2022-03-07", "code_system": "ICD-10-CM", "code": "M05.79",  "display": "Seropositive erosive rheumatoid arthritis",
         "value": None,    "unit": None,  "flag": None},
        {"row_id": 3,  "mrn": "ER-1001",  "name": "Reyes, E",            "dob": "1974-02-09",
         "service_date": "2023-08-04", "code_system": "ICD-10",    "code": "M05.79",  "display": "Rheumatoid arthritis",
         "value": None,    "unit": None,  "flag": None},
        # CRP, three rows with concordance and plausibility issues
        {"row_id": 4,  "mrn": "ER-001",   "name": "Reyes, Elena Maria", "dob": "1974-02-09",
         "service_date": "2024-01-08", "code_system": "LOINC",     "code": "1988-5",  "display": "C reactive protein",
         "value": "36.2",  "unit": "mg/L",  "flag": "H"},
        {"row_id": 5,  "mrn": "ER-001",   "name": "Reyes, Elena Maria", "dob": "1974-02-09",
         "service_date": "2024-01-08", "code_system": "LOINC",     "code": "1988-5",  "display": "C reactive protein",
         "value": "36.2",  "unit": "mg/L",  "flag": "H"},
        {"row_id": 6,  "mrn": "ER-001",   "name": "Reyes, Elena Maria", "dob": "1974-02-09",
         "service_date": "2024-04-17", "code_system": "LOCAL",     "code": "CRP-HOSP", "display": "CRP",
         "value": "5000",  "unit": "mg/L",  "flag": "H"},
        # Anti-CCP missing the structured row, only in notes
        {"row_id": 7,  "mrn": "ER-001",   "name": "Reyes, Elena Maria", "dob": "1974-02-09",
         "service_date": "2024-01-08", "code_system": "NOTE",      "code": None,      "display": "Note: anti-CCP markedly positive at 154 U/mL",
         "value": None,    "unit": None,  "flag": None},
        # DAS28 missing for 2022-2023, only computed in 2024+
        {"row_id": 8,  "mrn": "ER-001",   "name": "Reyes, Elena Maria", "dob": "1974-02-09",
         "service_date": "2026-02-10", "code_system": "LOINC",     "code": "76374-2", "display": "DAS28-CRP",
         "value": "2.8",   "unit": "score","flag": None},
        # Penicillin allergy stored three ways
        {"row_id": 9,  "mrn": "ER-001",   "name": "Reyes, Elena Maria", "dob": "1974-02-09",
         "service_date": "2003-06-12", "code_system": "ICD-10-CM", "code": "Z88.0",   "display": "Allergy status to penicillin",
         "value": None,    "unit": None,  "flag": None},
        {"row_id": 10, "mrn": "ER-001",   "name": "Reyes, Elena Maria", "dob": "1974-02-09",
         "service_date": "2003-06-12", "code_system": "RXNORM",    "code": "7980",    "display": "Penicillin G",
         "value": None,    "unit": None,  "flag": "ALLERGY"},
        {"row_id": 11, "mrn": "ER-001",   "name": "Reyes, Elena Maria", "dob": "1974-02-09",
         "service_date": "2024-01-08", "code_system": "NOTE",      "code": None,      "display": "Note: 'NKDA' documented at biologic-initiation visit",
         "value": None,    "unit": None,  "flag": None},
        # MRN drift after a merge
        {"row_id": 12, "mrn": "ER-X-99",  "name": "REYES ELENA",        "dob": "1974-02-09",
         "service_date": "2020-11-15", "code_system": "ICD-10-CM", "code": "Z00.00",  "display": "Routine general medical exam",
         "value": None,    "unit": None,  "flag": None},
        # Phantom encounter
        {"row_id": 13, "mrn": "ER-001",   "name": "Reyes, Elena Maria", "dob": "1974-02-09",
         "service_date": "2025-12-31", "code_system": "CPT",       "code": "99213",   "display": "Office visit, est patient, low complexity",
         "value": None,    "unit": None,  "flag": "CANCELED"},
        # Adalimumab, current med (correct)
        {"row_id": 14, "mrn": "ER-001",   "name": "Reyes, Elena Maria", "dob": "1974-02-09",
         "service_date": "2024-01-08", "code_system": "RXNORM",    "code": "327361",  "display": "Adalimumab 40 mg/0.8 mL Pen Inj",
         "value": "40",    "unit": "mg",  "flag": "ACTIVE"},
        # Old MTX dose row that was never closed (currency problem)
        {"row_id": 15, "mrn": "ER-001",   "name": "Reyes, Elena Maria", "dob": "1974-02-09",
         "service_date": "2022-04-04", "code_system": "RXNORM",    "code": "1156665", "display": "Methotrexate 10 mg/mL Inj Soln",
         "value": "10",    "unit": "mg",  "flag": "ACTIVE"},
    ])
    export.index = range(1, len(export) + 1)
    export.index.name = "row"

    export_view = mo.vstack([
        mo.md(
            "**Synthetic Reyes export, 15 rows.** Six categorical problems are seeded across these rows. "
            "Read it once for shape, then we walk each problem in turn."
        ),
        mo.as_html(export),
    ])
    export_view
    return (export,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Problem 1: Duplicate patients

        Look at rows 1, 2, and 3. Same DOB (1974-02-09). Three different MRNs (`ER-001`, `ER-001`, `ER-1001`). Three different name renderings (`Reyes, Elena Maria`, `Reyes, Elena`, `Reyes, E`). The three rows look as if they were three different patients because the *primary key* (MRN) is different across them.

        Whoever exported this data ran their query on MRN. Without a patient-matching pass that links `ER-1001` back to `ER-001`, an analytic question like *how many patients have had at least one M05.79 diagnosis* would count Ms. Reyes twice.

        Duplicate patients (also called *unmerged patients* or *MRN fragmentation*) come from three places:

        1. **Registration retypes.** A clerk registers the patient under a slightly different spelling or DOB and creates a second MRN. Hospitals catch most of these with patient-matching software (sometimes called Enterprise Master Patient Index, or EMPI), but never all of them.
        2. **Acquisitions.** When two hospitals merge, two patient populations merge. Some patients are in both populations under different MRNs. Reconciling them is multi-year work.
        3. **Sub-system MRNs.** Specialty systems (radiology, pathology, dental, behavioral health) sometimes mint their own identifiers that diverge from the EHR-wide MRN.

        **Dimension affected:** Concordance (different records of the same person disagree on identifiers).

        **Fix:** patient-matching pass at extract time, using DOB plus name plus address plus phone, often weighted by a probabilistic matcher (Fellegi-Sunter is the foundational algorithm). Vendor products do this; OHDSI's `usagi` and other open tools do simpler versions.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Problem 2: Inconsistent coding for the same concept

        Penicillin allergy in rows 9, 10, and 11. Row 9 codes it as ICD-10-CM `Z88.0` (allergy status to penicillin) on the problem list. Row 10 codes it as RxNorm `7980` (Penicillin G) with an `ALLERGY` flag. Row 11 is a note from her 2024 biologic-initiation visit that says "NKDA" (no known drug allergies) was documented.

        Three different representations of the same clinical fact, in three different systems, with one of them outright contradicting the other two. A naive query that filters for "current penicillin allergy" might:

        - Pick up row 9 only, miss row 10.
        - Pick up row 10 only, miss row 9.
        - Pick up both rows 9 and 10, and also pick up row 11's NKDA (and not know which one to trust).

        This is the most painful single class of data-quality problem because it conflates two issues: terminology drift (the *same* fact written with different code systems) and concordance failure (the *contradicting* fact written by mistake or in a different context).

        The Track 02 mapping-table problem comes back: every health system has internal mappings that translate local codes to standard ones. The Track 04 structured-vs-PDF problem comes back: row 11 is a note string, not a structured allergy entry, so it does not appear in the allergy module of the chart at all.

        **Dimensions affected:** Concordance and correctness, with terminology drift driving both.

        **Fix:** a value-set strategy. Define the *concept* (penicillin allergy) in terms of a value set that includes ICD-10 codes, RxNorm ingredient codes, SNOMED CT codes, and any local codes the institution uses. Query the concept against the value set, not against any single code.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Problem 3: Missing structured data (the DAS28 gap)

        Row 8 has Ms. Reyes's DAS28-CRP captured as a structured LOINC-coded value at her 2026-02-10 visit. There is no equivalent structured row for her 2022, 2023, or early 2024 visits. The notes (course 10's territory) show that DAS28 was computed at every visit; the rheumatologist wrote it in the assessment. The DAS28 value never made it into the flowsheet.

        This is the *missing structured data* problem: the fact existed, the clinician knew it, the chart has it in the note, but the structured field is empty. If you build a DAS28-trajectory analysis from the structured `LOINC 76374-2` rows only, you get the 2024-2026 portion and miss the 2022-2023 portion entirely.

        Same shape problem with row 7: anti-CCP at the 2024-01-08 visit shows up only as a free-text note that says "anti-CCP markedly positive at 154 U/mL." There is no structured `LOINC 32218-7` row in this extract for that result (compare to the Reyes Epic export from Track 01, which *does* have a structured anti-CCP row; this fictional export is from a different system that lost it in extract).

        Why this happens:

        1. **Flowsheets not built.** Some institutions never built a DAS28 flowsheet row, so the score lives in narrative.
        2. **Workflow friction.** Even when the flowsheet exists, entering it is one more click. Under time pressure, the clinician writes it in the assessment.
        3. **Extract gaps.** The data engineer pulled from a table that does not include free-text values, so anything that lived only in the note is invisible.

        **Dimension affected:** Completeness.

        **Fix:** structured-capture promotion (workflow changes to make structured entry frictionless), plus NLP on the notes when the captured share is below threshold. Course 10 covers the NLP side; this track flags the operational consequence.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Problem 4: Note-only findings (the Sharp/van der Heijde score)

        Track 04 set this up. Ms. Reyes's 2024-08-04 hand radiology report says the modified Sharp/van der Heijde score is 18 (erosion 11, JSN 7). The score lives in the PDF. Nowhere in the structured data is `Sharp_total = 18`.

        In the synthetic export above, this problem appears as the absence of any Sharp-related row at all. The score is real, the clinician wrote it, the radiologist computed it, the patient was scored. The export has no place to put it because the analytical schema has no structured field for Sharp/van der Heijde scores.

        Note-only findings are different from missing structured data in one important way: there is no structured *slot* to put the finding in, regardless of clinician motivation. Anti-CCP has a LOINC code and a flowsheet row; Sharp/van der Heijde modified total has neither in most US EHR deployments.

        **Dimensions affected:** Completeness and (subtly) concordance, since the report exists but disagrees with what the structured chart can show.

        **Fix:** specialty-specific structured templates (DICOM SR for imaging, structured flowsheets for clinic-side scoring) at the institutions that care enough to invest in them, plus NLP for the rest. RA-specific structured templates exist; very few US institutions have implemented them.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Problem 5: Late-binding terminology drift

        Row 6 has a CRP value coded with a *local* code system (`LOCAL` with code `CRP-HOSP`) instead of LOINC (`1988-5`). The display is `CRP`, the value is `5000 mg/L`, and the row is flagged High. Two problems here, layered:

        - The terminology drifted: the lab system at this site uses a local code for CRP rather than LOINC, and somewhere along the extraction path the LOINC was not joined in. A query filtering on `LOINC = 1988-5` would miss this row entirely.
        - The value is implausible: a CRP of 5000 mg/L is not biologically possible (the assay does not produce values that high). This is almost certainly a unit error or a typo; the value was probably 50.0 mg/L and somebody typed `5000` by accident. The plausibility check would flag it before the analytical layer ever sees it.

        Late-binding terminology is the slow version of the inconsistent-coding problem: code systems migrate over time, mappings drift, new local codes get introduced for new tests, retired codes hang around in old data. **It is the data-quality issue that grows on you over time** if you do not maintain the mapping aggressively.

        Plausibility failures sit next to terminology drift in this row because the two often go together: a malformed extract is more likely to also carry a malformed value, since whoever shipped one shipped the other.

        **Dimensions affected:** Conformance (terminology) and plausibility (value range).

        **Fix:** a vocabulary-management practice (someone owns the mapping tables, reviews them periodically) plus value-level range checks at the extract layer (LOINC-aware reference ranges that flag impossible values before the row is loaded).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Two more, briefly

        Two problems on the export that we have not walked yet:

        **Row 12: MRN drift after a merge.** Ms. Reyes was registered under `ER-X-99` at a 2020 primary-care visit, and during a 2022 merge her records were unified under `ER-001`. The 2020 row carries the old MRN. A query that pulls by `mrn = 'ER-001'` will miss that visit unless the merge-history table is in scope. **Dimension affected:** Currency of the identifier, concordance.

        **Row 13: Phantom encounter.** A 2025-12-31 office visit with `CANCELED` flag. The encounter row exists in the table, but the visit never happened. Patient was registered and then no-showed (or the appointment was canceled and the registration never withdrew). A naive *encounter count* query that does not filter on the `CANCELED` flag will overcount visits. **Dimension affected:** Correctness, completeness of cancellation propagation.

        And row 15 has a currency problem: Ms. Reyes started methotrexate at 10 mg in early 2022, was escalated to 25 mg over the following months, but the *original* 10 mg order in row 15 is still flagged `ACTIVE`. Nobody closed it when the dose was escalated. A query that pulls "all active MTX orders" would return both rows 15 and a 25 mg row (if 25 mg also exists), implying Ms. Reyes is on both. **Dimension affected:** Currency of the medication record.
        """
    )
    return


@app.cell
def _(mo):
    dq_quiz = mo.ui.radio(
        options=[
            "Completeness: the value was not captured at all.",
            "Concordance: two parts of the record disagree.",
            "Plausibility: the value is outside biologically reasonable bounds.",
            "Currency: the value was right once and is now out of date.",
            "Correctness: the value was wrong when entered.",
        ],
        label=(
            "**The synthetic export shows Ms. Reyes's anti-CCP from 2024-01-08 only as a free-text note (row 7), "
            "and there is no structured LOINC 32218-7 row for that date. Reading the Reyes notes file confirms the "
            "result was 154 U/mL and was acted on clinically. Which Weiskopf-Weng dimension does this fail on most directly?**"
        ),
    )
    dq_quiz
    return (dq_quiz,)


@app.cell
def _(dq_quiz, mo):
    mo.stop(dq_quiz.value is None, mo.md("_Choose an answer._"))
    dq_correct = dq_quiz.value.startswith("Completeness")

    if dq_correct:
        dq_feedback = (
            "Right. **Completeness** is the dimension. The structured slot for anti-CCP exists "
            "(LOINC 32218-7 with a flowsheet or lab-result row), the clinician knew the value, "
            "and the value should have been captured there. It was not. The note has it; the structured "
            "field does not. Completeness is the dimension that workflow changes and NLP-augmented extracts "
            "can address. Concordance does not fit because there are no two structured records to disagree; "
            "there is one note and a missing structured slot. Plausibility, currency, and correctness do "
            "not fit either, since the note itself is correct and timely."
        )
    elif dq_quiz.value.startswith("Concordance"):
        dq_feedback = (
            "Concordance describes the case where two parts of the record disagree (the problem list says X, "
            "the diagnosis code says Y). Here the issue is different: there is only one place the fact appears "
            "(the note), and the structured slot is empty. That is a completeness failure, not a concordance failure."
        )
    elif dq_quiz.value.startswith("Plausibility"):
        dq_feedback = (
            "Plausibility describes a value that is outside biologically reasonable bounds (CRP of 5000 mg/L, "
            "potassium of 12 mmol/L). The anti-CCP value of 154 U/mL is biologically plausible. The issue is that "
            "the value never made it into the structured field, which is a completeness problem."
        )
    elif dq_quiz.value.startswith("Currency"):
        dq_feedback = (
            "Currency describes a value that was right once and is no longer current (an active medication order "
            "that was never closed when the dose was escalated). The anti-CCP example is about capture, not currency: "
            "the value was correct and timely; the structured slot was never populated. That is "
            "completeness."
        )
    else:
        dq_feedback = (
            "Correctness describes a value that was wrong when entered (typo, unit confusion, dictation error). "
            "Here the note value is correct; the structured slot is empty. The failure is at the capture step, "
            "not the entry step. That puts it in completeness."
        )
    mo.callout(mo.md(dq_feedback), kind="success" if dq_correct else "warn")
    return


@app.cell
def _(xref):
    xref.forward(
        from_course="05",
        to_course="13",
        topic="Documenting what was done to the data",
        body=(
            "Every data-quality fix you apply is a *transformation* of the data, and the next analyst (or "
            "future you) needs to know what was done. Course 13 (Research reproducibility) Track 4 picks up "
            "this problem explicitly: data provenance is the practice of recording where the dataset came from "
            "and every change applied to it, in a form that someone else can reconstruct. The audit you do "
            "in the course capstone produces a finding list. The provenance documentation Course 13 teaches "
            "is what turns that finding list into a defensible analytic dataset."
        ),
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Where this leaves you

        The architecture of the first four tracks is correct. None of it stops the extract on your screen from carrying duplicate patients, inconsistent coding, missing structured data, note-only findings, terminology drift, and plausibility failures. Most of clinical data engineering is the work of cleaning the export against those failures. None of the fixes are free. Every correction loses some information, which is why Course 13 of this curriculum is about documenting the trade-offs so the analytical user can decide whether to trust the result.

        The course capstone is where you do this work on a larger synthetic extract from scratch.
        """
    )
    return


if __name__ == "__main__":
    app.run()
