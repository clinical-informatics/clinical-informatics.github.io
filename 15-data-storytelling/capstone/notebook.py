"""Capstone for course 15: Data storytelling.

Building capstone. The reader takes the CDS design brief from Course 12
(the Reyes-style RA-flare alert) and produces two communication
artifacts: a 2-minute verbal pitch for a CMO and a one-page visual
summary for clinical staff. Both are assembled from form fields and
exportable as Markdown.

WASM-safe: no shared imports, no data files, no relative paths.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import pandas as pd

    import marimo as mo

    REYES_CRP = pd.DataFrame(
        [
            {"date": "2022-02-14", "crp": 42.1},
            {"date": "2022-05-22", "crp": 28.4},
            {"date": "2022-08-18", "crp": 19.2},
            {"date": "2022-11-09", "crp": 16.8},
            {"date": "2023-02-15", "crp": 22.5},
            {"date": "2023-05-23", "crp": 31.6},
            {"date": "2023-08-21", "crp": 26.9},
            {"date": "2023-11-13", "crp": 33.4},
            {"date": "2024-01-08", "crp": 36.2},
            {"date": "2024-04-17", "crp": 18.7},
            {"date": "2024-07-22", "crp": 14.1},
            {"date": "2024-10-30", "crp": 11.4},
            {"date": "2025-02-04", "crp": 13.8},
            {"date": "2025-05-12", "crp": 16.5},
            {"date": "2025-08-19", "crp": 14.9},
            {"date": "2025-11-21", "crp": 18.2},
            {"date": "2026-02-10", "crp": 21.4},
            {"date": "2026-04-28", "crp": 19.8},
        ]
    )
    REYES_CRP["date"] = pd.to_datetime(REYES_CRP["date"])

    MEDICATIONS = pd.DataFrame(
        [
            {"date": "2022-03-15", "label": "MTX started"},
            {"date": "2024-02-10", "label": "Adalimumab added"},
        ]
    )
    MEDICATIONS["date"] = pd.to_datetime(MEDICATIONS["date"])

    return MEDICATIONS, REYES_CRP, alt, mo, pd


@app.cell
def _(mo):
    mo.md(
        r"""
        # Capstone: Produce two communication artifacts from the Course 12 CDS design brief

        The CDS design brief from Course 12 specified an RA-flare-monitoring CDS alert: a chart-open notification on the rheumatology service when a patient on biologic therapy has a dosing interval longer than scheduled, intended to surface the conversation about treatment adherence and flare risk. The brief is the design artifact; the design must now be communicated to the audiences who will approve, fund, deploy, and use it. This capstone produces those communication artifacts.

        Two artifacts are required.

        - **Part A.** A 2-minute verbal pitch for a CMO, in BLUF structure (ask, finding, implication, action, risk and mitigation).
        - **Part B.** A one-page visual summary for clinical staff, in a five-section structure (situation, population, threshold and override, success criterion, illustrative chart).

        Each part is assembled reactively below. Each part is exportable as Markdown for use in actual meetings.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            ### The CDS design brief (recap from Course 12)

            **Clinical problem.** Across the rheumatology service, the rate of moderate-to-severe RA flares has risen 60% in the past year, concentrated in patients with biologic dosing intervals longer than scheduled. Each flare adds approximately $4,800 in unbudgeted utilization plus the patient-experience and adverse-event burden.

            **Proposed intervention.** A CDS alert that flags patients on biologic therapy whose dosing interval has extended beyond the scheduled window. The alert appears at chart-open during the rheumatology visit; the response is a recommended adherence-and-flare-risk conversation.

            **Population and rule.** Adult RA patients on biologics (adalimumab, etanercept, infliximab, tocilizumab, others). Excludes patients in active hospice and patients on attending-ordered dose hold. Fires when the last biologic dose is more than 14 days beyond the scheduled interval.

            **Expected behavior.** Firing rate approximately 0.4 per clinic day per attending; override rate target at or below 60%.

            **Evaluation.** Stepped-wedge pilot in the rheumatology service for 6 months starting Q1 2026. Primary outcome: moderate-to-severe flare rate in the alert-exposed cohort. Success criterion: 30% reduction at the 6-month gate, with override rate at or below 60%.

            **Owner and accountability.** Rheumatology CDS working group, accountable to the CMIO.

            **Cost.** Capital $40K (build and integration); annual operating $12K (monitoring and quarterly review).
            """
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Part A: A 2-minute verbal pitch for a CMO

        BLUF structure. The pitch leads with the ask, then the finding that motivates the ask, then the implication that connects the finding to the CMO's domain, then the recommended action, then the risk and the mitigation. Five short sentences total; the CMO can stop after sentence 1 and still have the ask.

        Fill in each field below. The assembled pitch appears further down the notebook and is exportable as Markdown.
        """
    )
    return


@app.cell
def _(mo):
    cmo_ask = mo.ui.text_area(
        label="A.1 The ask (one sentence; lead with the verb)",
        placeholder=(
            "Approve a 6-month pilot of an RA-flare CDS alert in the "
            "rheumatology service, $40K capital, $12K annual operating."
        ),
        rows=2,
        full_width=True,
    )
    cmo_finding = mo.ui.text_area(
        label="A.2 The finding (one sentence; lead with the headline number)",
        placeholder=(
            "Moderate-to-severe RA flares rose 60% (12 to 19 per 100 "
            "patient-quarters) between 2024 Q2 and 2025 Q2, concentrated in "
            "patients with extended biologic dosing intervals."
        ),
        rows=2,
        full_width=True,
    )
    cmo_implication = mo.ui.text_area(
        label="A.3 The implication (one sentence; tie to the CMO's domain)",
        placeholder=(
            "Each flare adds about $4,800 in unbudgeted utilization (clinic "
            "visits, prednisone management); the cohort-level cost is "
            "approximately $480K annually, plus the patient-experience and "
            "adverse-event burden."
        ),
        rows=2,
        full_width=True,
    )
    cmo_action = mo.ui.text_area(
        label="A.4 The action (one sentence; specific, time-bound, owned)",
        placeholder=(
            "Build the alert specified in the attached design brief; pilot in "
            "the rheumatology service for 6 months starting Q1 2026; owner "
            "the rheumatology CDS working group accountable to the CMIO; "
            "success a 30% flare reduction at the 6-month gate with override "
            "rate at or below 60%."
        ),
        rows=2,
        full_width=True,
    )
    cmo_risk = mo.ui.text_area(
        label="A.5 The risk and mitigation (one sentence; specific on both sides)",
        placeholder=(
            "The observational baseline is open to confounding; the pilot's "
            "stepped-wedge design and the 6-month evaluation gate are the "
            "primary defenses, with quarterly equity-stratified reporting as "
            "the secondary defense."
        ),
        rows=2,
        full_width=True,
    )
    mo.vstack(
        [
            mo.md("### Part A: Form fields"),
            cmo_ask,
            cmo_finding,
            cmo_implication,
            cmo_action,
            cmo_risk,
        ]
    )
    return cmo_action, cmo_ask, cmo_finding, cmo_implication, cmo_risk


@app.cell
def _(cmo_action, cmo_ask, cmo_finding, cmo_implication, cmo_risk, mo):
    cmo_pitch = f"""# CMO pitch: RA-flare CDS pilot

_2-minute verbal pitch. BLUF-structured for executive review._

**The ask.** {cmo_ask.value or '_(not yet specified)_'}

**The finding.** {cmo_finding.value or '_(not yet specified)_'}

**The implication.** {cmo_implication.value or '_(not yet specified)_'}

**The action.** {cmo_action.value or '_(not yet specified)_'}

**The risk and mitigation.** {cmo_risk.value or '_(not yet specified)_'}

---

_Generated from the Course 15 capstone notebook. This pitch is the BLUF-structured talking points for a CMO conversation about pilot approval for the RA-flare CDS design specified in the Course 12 capstone brief._
"""
    mo.vstack(
        [
            mo.md("### Part A: Assembled pitch"),
            mo.md(cmo_pitch),
        ]
    )
    return (cmo_pitch,)


@app.cell
def _(cmo_pitch, mo):
    cmo_download = mo.download(
        data=cmo_pitch.encode("utf-8"),
        filename="ra-flare-cds-cmo-pitch.md",
        label="Download Part A (CMO pitch) as Markdown",
    )
    cmo_download
    return (cmo_download,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Part B: A one-page visual summary for clinical staff

        Five-section structure (situation, population, threshold and override, success criterion, illustrative chart). The clinical audience reads to learn what the alert will look like at the bedside and what the success criterion implies for their service. The illustrative chart is Ms. Reyes's CRP series with the medication-change annotations from Track 04; it makes the longitudinal-monitoring framing of the alert concrete.

        Fill in the form fields below. The assembled one-pager appears further down and is exportable as Markdown.
        """
    )
    return


@app.cell
def _(mo):
    cs_situation = mo.ui.text_area(
        label="B.1 The clinical situation (what fires, when, how it appears)",
        placeholder=(
            "When a rheumatology patient on biologic therapy presents for a "
            "routine visit, the EHR will flag the patient if their last "
            "biologic dose was more than 14 days beyond the scheduled "
            "interval. The alert appears at chart-open and offers a "
            "recommended adherence-and-flare-risk conversation."
        ),
        rows=3,
        full_width=True,
    )
    cs_population = mo.ui.text_area(
        label="B.2 The patient population (who is flagged, who is excluded)",
        placeholder=(
            "Adult RA patients on biologics (adalimumab, etanercept, "
            "infliximab, tocilizumab, others). Exclusions: patients in active "
            "hospice, patients on attending-ordered dose hold."
        ),
        rows=3,
        full_width=True,
    )
    cs_threshold = mo.ui.text_area(
        label="B.3 The threshold and override (firing rate, dismissal mechanism)",
        placeholder=(
            "Fires when the last biologic dose was more than 14 days beyond "
            "the scheduled interval. Expected firing rate approximately 0.4 "
            "per clinic day per attending. Dismiss as \"not applicable\" with "
            "one click; the dismissal is logged for the quarterly review."
        ),
        rows=3,
        full_width=True,
    )
    cs_success = mo.ui.text_area(
        label="B.4 The success criterion (what we will evaluate, when)",
        placeholder=(
            "Primary: 30% reduction in moderate-to-severe flares in the "
            "alert-exposed cohort at the 6-month gate. Secondary: override "
            "rate at or below 60%; documentation time under 90 seconds; no "
            "differential override rate across patient subgroups."
        ),
        rows=3,
        full_width=True,
    )
    cs_caption = mo.ui.text_area(
        label="B.5 The illustrative-chart caption (one sentence)",
        placeholder=(
            "Ms. Reyes's CRP trajectory, with the medication-change events "
            "marked: CRP fell from a peak of 36 mg/L pre-biologic to a nadir "
            "of 11 mg/L after adalimumab was added, illustrating the kind of "
            "response the alert is designed to support."
        ),
        rows=2,
        full_width=True,
    )
    mo.vstack(
        [
            mo.md("### Part B: Form fields"),
            cs_situation,
            cs_population,
            cs_threshold,
            cs_success,
            cs_caption,
        ]
    )
    return cs_caption, cs_population, cs_situation, cs_success, cs_threshold


@app.cell
def _(MEDICATIONS, REYES_CRP, alt, mo, pd):
    _base = (
        alt.Chart(REYES_CRP)
        .mark_line(color="steelblue", point=True)
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("crp:Q", title="CRP (mg/L)", scale=alt.Scale(domain=[0, 50])),
        )
    )
    _ref_band = (
        alt.Chart(pd.DataFrame({"low": [0], "high": [5]}))
        .mark_rect(opacity=0.18, color="seagreen")
        .encode(y="low:Q", y2="high:Q")
    )
    _med_rules = (
        alt.Chart(MEDICATIONS)
        .mark_rule(color="firebrick", strokeDash=[4, 4])
        .encode(x="date:T")
    )
    _med_text = (
        alt.Chart(MEDICATIONS)
        .mark_text(align="left", dx=5, dy=-180, color="firebrick", fontSize=11)
        .encode(x="date:T", text="label:N")
    )
    _chart = (_ref_band + _base + _med_rules + _med_text).properties(
        width=600,
        height=300,
        title="Illustrative trajectory: a patient on biologic therapy responding to treatment",
    )
    mo.vstack(
        [
            mo.md("### Part B: Illustrative chart preview"),
            mo.ui.altair_chart(_chart),
        ]
    )
    return


@app.cell
def _(cs_caption, cs_population, cs_situation, cs_success, cs_threshold, mo):
    clinical_summary = f"""# RA-flare CDS alert: one-page summary for clinical staff

_For the rheumatology service. 6-month pilot starting Q1 2026._

## The clinical situation

{cs_situation.value or '_(not yet specified)_'}

## The patient population

{cs_population.value or '_(not yet specified)_'}

## Threshold and override

{cs_threshold.value or '_(not yet specified)_'}

## Success criterion

{cs_success.value or '_(not yet specified)_'}

## Illustrative chart

_(Ms. Reyes's CRP trajectory, shown in the notebook above. Caption follows.)_

{cs_caption.value or '_(not yet specified)_'}

---

_Generated from the Course 15 capstone notebook. This one-pager is the rheumatology-facing communication artifact for the RA-flare CDS pilot specified in the Course 12 capstone brief._
"""
    mo.vstack(
        [
            mo.md("### Part B: Assembled one-page summary"),
            mo.md(clinical_summary),
        ]
    )
    return (clinical_summary,)


@app.cell
def _(clinical_summary, mo):
    clinical_download = mo.download(
        data=clinical_summary.encode("utf-8"),
        filename="ra-flare-cds-clinical-staff-summary.md",
        label="Download Part B (clinical-staff summary) as Markdown",
    )
    clinical_download
    return (clinical_download,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Closing

        The two artifacts produced above are the operational output of the five tracks of this course. Audience analysis (Track 01) is the reason the same CDS design brief produces two artifacts: the CMO and the clinical staff need differently-shaped versions of the same facts. Plain-English writing (Track 02) is the sentence-level craft of the pitch. Narrative structure (Track 03) determines the BLUF shape of the pitch and the situation-population-threshold-override-success shape of the clinical summary. Visual presentation (Track 04) determines the chart and its annotations. Vendor and AI-team communication (Track 05) is the operational backdrop that the design-brief work assumes.

        An informaticist who has produced these two artifacts has the communication-craft fluency to take an analysis or a CDS design from the working group through the approvals and into the rollout. That is the practice this course exists to teach.
        """
    )
    return


if __name__ == "__main__":
    app.run()
