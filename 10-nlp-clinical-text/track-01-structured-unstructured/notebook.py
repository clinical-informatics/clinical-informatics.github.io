"""Track 01: Structured vs unstructured data.

A clinical encounter produces both structured data (the coded fields in
the EHR) and unstructured data (the narrative note). The two are not
interchangeable. The track addresses the categorical distinction with
a worked side-by-side of one of Ms. Reyes's encounters and frames the
rest of the course as the toolset that bridges the two representations.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import types

    import marimo as mo
    import pandas as pd

    _COURSE_TITLES = {
        "02": "Data literacy",
        "05": "EHR systems",
        "07": "Data wrangling and engineering",
        "12": "Clinical decision support",
    }

    def _course_label(course_id):
        title = _COURSE_TITLES.get(course_id.split("-")[0])
        return f"Course {course_id}: {title}" if title else f"Course {course_id}"

    def _xref_callback(from_course, to_course, topic, body):
        return mo.callout(
            mo.md(f"**Callback to {_course_label(to_course)}.** {topic}\n\n{body}"),
            kind="neutral",
        )

    def _xref_forward(from_course, to_course, topic, body):
        return mo.callout(
            mo.md(f"**Forward to {_course_label(to_course)}.** {topic}\n\n{body}"),
            kind="neutral",
        )

    xref = types.SimpleNamespace(callback=_xref_callback, forward=_xref_forward)

    return mo, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 01: Structured vs unstructured data

        ## The premise: most of the clinical detail lives in the note

        A clinical encounter produces two parallel records. The structured record is the set of coded fields the clinician populated in the EHR: the diagnosis code, the medication order, the lab results, the problem list update, the vital signs. The unstructured record is the narrative note: the history of present illness, the assessment paragraph, the plan, and every other prose section of the chart.

        The two records are not interchangeable. Most clinical reasoning, most context, most uncertainty, and most of the texture that gives the chart its meaning lives in the narrative side, not the structured side. A query that touches only the structured fields will return a rough sketch of the encounter and miss the parts that are clinically load-bearing. The rest of the course is the toolset that bridges the two representations.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The two records, in one table
        """
    )
    return


@app.cell
def _(pd):
    distinction_table = pd.DataFrame(
        [
            {
                "Aspect": "Examples",
                "Structured": "ICD-10-CM diagnosis codes, CPT procedure codes, RxNorm medications, LOINC labs, problem list entries, vital signs.",
                "Unstructured": "History of present illness, review of systems, assessment paragraphs, plan narrative, free-text notes, discharge summaries, telephone-call documentation.",
            },
            {
                "Aspect": "Where it sits in the EHR",
                "Structured": "Named columns in the operational tables; codes drawn from controlled vocabularies.",
                "Unstructured": "TEXT or CLOB columns associated with each note; usually one row per note, often versioned through addenda.",
            },
            {
                "Aspect": "Volume relative to structured",
                "Structured": "A modest number of rows per encounter (tens, sometimes hundreds).",
                "Unstructured": "A few thousand to tens of thousands of characters per note; many notes per encounter; orders of magnitude more bytes than structured.",
            },
            {
                "Aspect": "Queryable directly",
                "Structured": "Yes. SQL on the structured tables returns the field values.",
                "Unstructured": "Only as text. Free-text search returns mentions; an NLP pipeline is required to turn mentions into structured outputs.",
            },
            {
                "Aspect": "Authoring effort",
                "Structured": "Often a single click in a problem-list picker or a code-search dialog.",
                "Unstructured": "The bulk of the documentation time. Most of what the clinician writes.",
            },
            {
                "Aspect": "Carries clinical reasoning",
                "Structured": "Rarely. The code asserts the fact, not why it was asserted.",
                "Unstructured": "Almost always. The assessment paragraph is where the reasoning is written down.",
            },
        ]
    )
    distinction_table.index = range(1, len(distinction_table) + 1)
    distinction_table.index.name = "row"
    distinction_table
    return (distinction_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three properties of the distinction are load-bearing.

        First, the structured record records the conclusion; the note records the path that produced it. A diagnosis code says "the patient has rheumatoid arthritis"; the note says which features the clinician considered, which alternatives were excluded, which labs are pending, and what level of confidence the assessment carries.

        Second, the structured record is a sample of the encounter, not a summary. Many true clinical facts are not codable in the working vocabulary, and many that are codable are not coded because the documentation workflow does not require it. A claim "the structured record represents the encounter" overstates what the record actually is.

        Third, the two records are written by the same clinician at the same moment but with different incentives. The structured fields are populated to satisfy billing, regulatory, and order-entry requirements. The note is populated to communicate with the next clinician who sees the patient. The incentive gap explains most of what is missing on the structured side.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A worked encounter: Reyes's diagnosis visit (2022-03-07)

        Ms. Reyes's second visit (2022-03-07) is the visit at which her rheumatologist formally diagnosed seropositive erosive rheumatoid arthritis and started methotrexate. The structured side of the encounter is shown below; the narrative side is the source note from `start-here/patients/elena-reyes/notes.txt`.
        """
    )
    return


@app.cell
def _(pd):
    structured_side = pd.DataFrame(
        [
            {"Table": "condition_occurrence", "Field": "condition_concept_id", "Value": "4035611 (Rheumatoid arthritis)"},
            {"Table": "condition_occurrence", "Field": "condition_source_value", "Value": "M05.79 (ICD-10-CM)"},
            {"Table": "drug_exposure", "Field": "drug_concept_id", "Value": "1503297 (methotrexate)"},
            {"Table": "drug_exposure", "Field": "drug_source_value", "Value": "methotrexate 10 mg PO weekly"},
            {"Table": "drug_exposure", "Field": "quantity", "Value": "4"},
            {"Table": "drug_exposure", "Field": "days_supply", "Value": "28"},
            {"Table": "drug_exposure", "Field": "refills", "Value": "11"},
            {"Table": "measurement", "Field": "CRP (LOINC 1988-5)", "Value": "42.1 mg/L (H)"},
            {"Table": "measurement", "Field": "ESR (LOINC 4537-7)", "Value": "58 mm/h (H)"},
            {"Table": "measurement", "Field": "anti-CCP (LOINC 32218-7)", "Value": "178 U/mL (H)"},
            {"Table": "measurement", "Field": "RF (LOINC 11572-5)", "Value": "84 IU/mL (H)"},
            {"Table": "visit_occurrence", "Field": "visit_concept_id", "Value": "9202 (Outpatient visit)"},
        ]
    )
    structured_side.index = range(1, len(structured_side) + 1)
    structured_side.index.name = "row"
    structured_side
    return (structured_side,)


@app.cell
def _(mo):
    mo.md(
        r"""
        The structured side records the diagnosis, the medication start, the abnormal lab values, and the visit type. A SQL query against the OMOP tables returns approximately the table above. The query result is a faithful skeleton of the encounter.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The narrative side of the same encounter

        > **INTERVAL HISTORY.** Returns to review labs. Joint pain persists, modest improvement on naproxen. Morning stiffness now approximately 60 to 75 minutes. Has continued working, though she finds the second half of the workday difficult.
        >
        > **LABS.** CRP 42.1 (H), ESR 58 (H), anti-CCP 178 (markedly elevated, H), RF 84 (H), ANA negative, Hep B and C negative, uric acid 4.2, TSH 2.1, Hgb 11.6 (L), WBC 8.1, plt 389, ALT 22, Cr 0.78. Hand films show periarticular osteopenia and very early erosive changes at MCP 2 and the right wrist.
        >
        > **ASSESSMENT.** Seropositive erosive rheumatoid arthritis. Anti-CCP markedly positive, RF positive, elevated acute phase reactants, x-ray evidence of erosive disease. Meets 2010 ACR/EULAR classification criteria.
        >
        > **PLAN.**
        >
        > - Initiate methotrexate 10 mg PO weekly, with folic acid 1 mg daily.
        > - Plan to escalate methotrexate over 4 to 6 weeks toward 20 to 25 mg weekly based on tolerance and response.
        > - Will recheck CBC and LFTs in 4 weeks, then monthly for 3 months.
        > - Discussed risk of hepatotoxicity, marrow suppression, teratogenicity (she reports completed childbearing). Advised to limit alcohol while on MTX.
        > - Continue naproxen as needed for breakthrough symptoms.
        > - Plan follow-up in 6 weeks. If inadequate response to MTX at 3 months, will consider adding a biologic DMARD.

        (Source: `start-here/patients/elena-reyes/notes.txt`, Note 2 of 8.)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What the structured record contains, and what the note contains

        Compare the two representations. The structured record contains the codes, the dose, the days-supply, and the abnormal lab flags. The note contains everything else: the patient's functional status (working but struggling), the duration of morning stiffness (a continuous-valued clinical observation rarely captured in structured fields), the radiograph reading (periarticular osteopenia and erosive changes at MCP 2 and the right wrist), the assessment reasoning (the 2010 ACR/EULAR classification criteria are met), the medication-titration plan (escalate to 20 to 25 mg over 4 to 6 weeks), the monitoring plan (CBC and LFTs at 4 weeks then monthly for 3 months), the risks discussed and the patient's reported response, and the contingency (consider a biologic if MTX is inadequate at 3 months).

        None of these items appears in the structured record. A researcher who queries the structured side will know that Ms. Reyes was diagnosed and started on MTX. The researcher will not know how aggressive the disease was, what the planned dose escalation looked like, what monitoring was committed to, or what the contingency plan was. A different clinician picking up the chart cold from the structured side alone would not know how to continue the plan.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Five categories of clinical fact that live primarily in notes

        Across an institution's full record, the categories of clinical fact that are systematically present in narrative notes and systematically absent from structured fields cluster into five groups.

        - **Functional status.** Can the patient climb stairs, type all day, lift a grocery bag, sleep through the night? Captured in HPI and ROS narrative; rare in any structured field outside specialty registries.
        - **Symptom severity, quality, and duration.** "Morning stiffness 60 to 75 minutes," "sharp pain radiating to the shoulder," "intermittent over 3 weeks." Free-text by convention; the structured side has the symptom name at best, never the quality and rarely the duration.
        - **Clinical reasoning and differential diagnosis.** "Suspect RA given symmetric small joint involvement, prolonged morning stiffness, and gradual onset." The clinician's reasoning lives in the assessment paragraph; the structured side has the conclusion but not the path.
        - **Plan and rationale.** "Escalate MTX over 4 to 6 weeks toward 20 to 25 mg weekly based on tolerance and response." The titration plan, the monitoring plan, the contingency plan: in the note. The structured medication-order row captures only the current dose.
        - **Risks discussed and patient response.** The teratogenicity discussion, the alcohol counseling, the patient's reported childbearing status. Documented in the note as part of the medical-decision-making narrative; the structured fields rarely have a place for them.

        Any clinical research question that depends on these five categories has to involve the narrative side, which means it has to involve NLP. The remainder of the course addresses the NLP toolset.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The information-loss problem

        A common pattern in clinical research and quality-improvement work: a researcher writes a SQL query against the structured tables, gets a count, and treats the count as if it represents the underlying clinical reality. The count is a count of patients for whom a particular structured field was populated, not a count of patients for whom the underlying clinical fact was true.

        A worked instance. A researcher counts patients in the EHR who "discussed teratogenicity with their rheumatologist before starting methotrexate" by querying for a particular smart-phrase or by counting a particular order. The query returns 142 patients. The true count is likely much higher; the teratogenicity discussion appeared in the note for most patients but the smart-phrase was inconsistently used. The researcher's denominator is a denominator of well-documented patients, not a denominator of patients who had the discussion.

        The information-loss problem applies to any query that depends on a structured proxy for a fact that primarily lives in notes. Three operational consequences follow.

        - **Cohort definitions** that depend on note-resident facts (functional status, severity, reasoning) need NLP to be reliably constructed.
        - **Quality measures** that depend on note-resident facts (counseling, shared decision-making, medication reconciliation reasoning) will systematically under-count unless an NLP layer is added to the measurement pipeline.
        - **CDS rules** that depend on note-resident facts cannot fire on the structured side alone; they need an NLP step in the firing logic or have to accept that they fire on a subset of the truly eligible patients.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "10",
        "02",
        "The data-types vocabulary from Course 02",
        "Course 02 Track 1 introduced the distinction between numeric, categorical, and text data types. The structured / unstructured distinction here is the same distinction operationalized at the EHR level: the structured side is numeric and categorical, the unstructured side is text. Course 02 also addressed why text values that should be numeric (CRP stored as a string, lab values with `<` and `>` operators) produce silent analytic failures; the same pattern applies to clinical note extraction.",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "10",
        "12",
        "CDS rules and the note-vs-field decision",
        "Course 12 takes up the construction of CDS rules. A rule that needs a note-resident fact (the patient declined a recommended screening, the patient is being palliated, the patient's functional status is poor) requires an NLP-layered alert. The Track 4 of this course (LLMs and clinical text) is the operational form that question has taken in 2025 to 2026.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        A clinical encounter produces two parallel records. The structured record captures the conclusion (the code, the order, the lab value) but rarely captures the reasoning, the context, or the texture. The narrative note captures most of the rest. Five categories of clinical fact (functional status, symptom severity, clinical reasoning, plan and rationale, risks-discussed) live primarily in the narrative side. A query that depends on these facts and only touches the structured side will systematically under-count.

        Track 02 takes up the NLP toolset that turns narrative text into the structured outputs the structured side does not have.
        """
    )
    return


if __name__ == "__main__":
    app.run()
