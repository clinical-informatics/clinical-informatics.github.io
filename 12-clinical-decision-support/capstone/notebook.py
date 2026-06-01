"""Capstone for course 12: The curriculum's grand-finale CDS design exercise.

The reader produces a complete CDS-intervention design for a Reyes-style
RA flare alert across seven dimensions: the computational decomposition
of the rule (Course 01), the FHIR data the rule depends on (Course 06),
the CQL logic that implements the rule (Track 02), the CDS Hook that
delivers it (Track 03), the evaluation plan (Course 04), the DCA-based
threshold (Course 11), and the equity-monitoring plan (Course 03). The
output is an exportable Markdown brief a real implementation team
could act on.
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
        # Capstone: Design a complete CDS intervention for a Reyes-style RA flare alert

        ## The curriculum's grand finale

        Across the seven steps below, build a complete design brief for a CDS intervention that would notify Ms. Reyes's rheumatologist (or any rheumatologist caring for a similar patient) when the patient is at elevated risk of an RA flare. Each step asks for a written specification; the Markdown summary at the bottom assembles the seven specifications into a single document the reader can copy out of the notebook.

        The capstone integrates everything every prior course has covered. Each step is labelled with the Courses it draws on.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            ### The clinical scenario

            Ms. Elena Reyes is a 52-year-old woman with seropositive erosive rheumatoid arthritis. She is on methotrexate 25 mg subcutaneous weekly plus adalimumab 40 mg subcutaneous every 2 weeks. Her CRP has been monitored every 8 to 12 weeks across four years. Her rheumatologist would value an alert that surfaces, at chart open, when the patient's recent CRP trajectory and clinical context suggest an elevated probability of a flare in the next 90 days, so a treatment-escalation conversation can be scheduled rather than discovered at the next routine visit.

            Your task across the seven steps is to specify that intervention end to end.
            """
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Step 1: Computational decomposition of the rule (Course 01)

        Decompose the alert into its parts. The Course 01 framework names six parts of any clinical decision rule: cohort, signals, thresholds, time window, data source, trigger moment. For the RA-flare alert, write a sentence or two for each. The goal of the step is to make the rule's structure explicit before any code is written.
        """
    )
    return


@app.cell
def _(mo):
    step1_input = mo.ui.text_area(
        label="The six parts of the rule (cohort, signals, thresholds, time window, data source, trigger moment). One short sentence per part.",
        placeholder="Cohort: adult patients with active RA on the rheumatology panel. Signals: most recent CRP, CRP trajectory across last 3 visits, current biologic. Thresholds: ... Time window: ... Data source: ... Trigger moment: ...",
        rows=8,
        full_width=True,
    )
    step1_input
    return (step1_input,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Step 2: FHIR data the rule depends on (Course 06)

        Name the FHIR resources the CDS service needs in the request payload to evaluate the rule. For each resource, name the relevant fields. The goal is to know what the CDS Hooks service will tell the EHR to prefetch.
        """
    )
    return


@app.cell
def _(mo):
    step2_input = mo.ui.text_area(
        label="FHIR resources and the fields each contributes. One resource per line.",
        placeholder="Patient: gender, birthDate. Condition: code (filtered to RA value set), clinicalStatus. Observation: code (CRP LOINC), value, effective (last 3 values). MedicationStatement: medication (filtered to biologic value set), status, effectivePeriod. ...",
        rows=6,
        full_width=True,
    )
    step2_input
    return (step2_input,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Step 3: CQL logic (Track 02 of this course)

        Sketch the CQL logic that implements the rule. A pseudocode CQL fragment is acceptable; the goal is the logic, not perfect syntax. Reference value sets by name. The fragment should make the rule's behavior unambiguous to a CQL-fluent reader.
        """
    )
    return


@app.cell
def _(mo):
    step3_input = mo.ui.text_area(
        label="CQL or CQL-style pseudocode for the rule.",
        placeholder="""define "RA Flare Risk Elevated":
  exists ([Condition: "Rheumatoid Arthritis"]) C where C.clinicalStatus = 'active'
  and "Most Recent CRP" > 10 'mg/L'
  and "CRP Trend" = 'rising'
  and not exists ([MedicationStatement: "Biologic Initiated Last 30 days"])
""",
        rows=10,
        full_width=True,
    )
    step3_input
    return (step3_input,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Step 4: CDS Hook and card content (Track 03 of this course)

        Pick the hook (patient-view, order-select, order-sign) and design the card the CDS service returns when the rule fires. The goal is to commit to a workflow moment and to a specific card the clinician would actually act on.
        """
    )
    return


@app.cell
def _(mo):
    step4_hook = mo.ui.radio(options=["patient-view", "order-select", "order-sign"], label="Hook (when the alert fires)")
    step4_indicator = mo.ui.radio(options=["info", "warning", "critical"], label="Card indicator level")
    step4_summary = mo.ui.text(label="Card summary (one sentence)", placeholder="Elevated RA flare risk: consider scheduling early follow-up", full_width=True)
    step4_detail = mo.ui.text_area(
        label="Card detail (the clinical rationale the clinician will read)",
        placeholder="This patient's CRP has been rising across the last 3 visits and currently sits at 14.3 mg/L. The biologic regimen has been unchanged for 6+ months. Consider scheduling a treatment-escalation conversation rather than waiting for the routine visit in 8 weeks.",
        rows=4,
        full_width=True,
    )
    step4_action = mo.ui.text(label="Suggested action (the button text)", placeholder="Schedule rheumatology follow-up within 14 days", full_width=True)
    mo.vstack([step4_hook, step4_indicator, step4_summary, step4_detail, step4_action])
    return step4_action, step4_detail, step4_hook, step4_indicator, step4_summary


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Step 5: Evaluation plan (Course 04 + Track 04 of this course)

        Specify the evaluation design. Name the study design (interrupted time series, controlled before-after, stepped-wedge), the primary outcome the alert is meant to improve, the baseline measurement, and the time horizon. The goal is an evaluation plan a stats reviewer would accept.
        """
    )
    return


@app.cell
def _(mo):
    step5_design = mo.ui.radio(
        options=["Simple before-after", "Interrupted time series (ITS)", "Stepped-wedge / controlled before-after"],
        label="Study design",
        value="Interrupted time series (ITS)",
    )
    step5_outcome = mo.ui.text(label="Primary outcome (what the alert is meant to improve)", placeholder="Time from CRP rise detection to next rheumatology visit (days)", full_width=True)
    step5_baseline = mo.ui.text(label="Baseline period length", placeholder="12 months prior to go-live", full_width=True)
    step5_horizon = mo.ui.text(label="Post-go-live evaluation horizon", placeholder="12 months", full_width=True)
    mo.vstack([step5_design, step5_outcome, step5_baseline, step5_horizon])
    return step5_baseline, step5_design, step5_horizon, step5_outcome


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Step 6: DCA-based threshold (Course 11)

        Specify the firing threshold and the reasoning. The threshold is a probability cutoff above which the alert fires. State the threshold, the prevalence the alert operates against, and the expected PPV at that threshold. Reference the DCA logic from Course 11 Track 5 in the rationale.
        """
    )
    return


@app.cell
def _(mo):
    step6_threshold = mo.ui.slider(start=0.05, stop=0.80, step=0.01, value=0.30, label="Firing threshold probability", show_value=True)
    step6_prevalence = mo.ui.slider(start=0.01, stop=0.30, step=0.01, value=0.08, label="Expected prevalence of next-90-day flare in alert cohort", show_value=True)
    step6_rationale = mo.ui.text_area(
        label="Rationale for the threshold (cite DCA, expected PPV, alert volume considerations)",
        placeholder="At threshold 0.30, the expected PPV is approximately 30% / X% = ... The DCA chart from the pilot dataset showed net benefit positive across threshold range 0.20 to 0.50, with the operating-region centered on 0.30. Lower thresholds would produce more alerts but lower PPV; the chosen threshold balances detection against the alert-volume burden on the rheumatology clinicians.",
        rows=4,
        full_width=True,
    )
    mo.vstack([step6_threshold, step6_prevalence, step6_rationale])
    return step6_prevalence, step6_rationale, step6_threshold


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Step 7: Equity-monitoring plan (Course 03 + Track 05 of this course)

        Name two specific equity concerns about the alert and describe the monitoring approach for each. Subgroup categories to consider: race, sex, age band, primary language, insurance type, urban vs rural residence. The goal is a concrete monitoring plan, not an abstract acknowledgement.
        """
    )
    return


@app.cell
def _(mo):
    step7_concern_1 = mo.ui.text_area(
        label="Equity concern 1 and its monitoring approach",
        placeholder="Concern: the alert may have lower PPV in Spanish-speaking patients because the CRP-trend signal depends on consistent visit attendance, and Spanish-speaking patients in the panel attend fewer visits per year on average. Monitoring: subgroup-stratified PPV and alert-fire-rate reported quarterly to the CDS governance committee, with primary-language as the stratification variable.",
        rows=4,
        full_width=True,
    )
    step7_concern_2 = mo.ui.text_area(
        label="Equity concern 2 and its monitoring approach",
        placeholder="Concern: the alert may produce alert fatigue at higher rates for clinicians serving the urban-safety-net clinic that has a higher RA patient volume. Monitoring: per-clinic override rates reviewed monthly; thresholds may need clinic-specific tuning.",
        rows=4,
        full_width=True,
    )
    mo.vstack([step7_concern_1, step7_concern_2])
    return step7_concern_1, step7_concern_2


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The assembled CDS design brief

        The Markdown below assembles the seven specifications into a single design document. Copy it (right-click the rendered area, "View source") and paste into a real document or share with the CDS governance committee as the starting deliverable.
        """
    )
    return


@app.cell
def _(
    step1_input,
    step2_input,
    step3_input,
    step4_action,
    step4_detail,
    step4_hook,
    step4_indicator,
    step4_summary,
    step5_baseline,
    step5_design,
    step5_horizon,
    step5_outcome,
    step6_prevalence,
    step6_rationale,
    step6_threshold,
    step7_concern_1,
    step7_concern_2,
):
    brief = f"""# CDS Design Brief: RA Flare Risk Alert (Reyes-style cohort)

## Step 1: Computational decomposition of the rule

{step1_input.value or '_(not yet specified)_'}

## Step 2: FHIR data the rule depends on

{step2_input.value or '_(not yet specified)_'}

## Step 3: CQL logic

```cql
{step3_input.value or '_(not yet specified)_'}
```

## Step 4: CDS Hook and card content

- **Hook**: {step4_hook.value or '_(not yet specified)_'}
- **Indicator**: {step4_indicator.value or '_(not yet specified)_'}
- **Card summary**: {step4_summary.value or '_(not yet specified)_'}

**Card detail**

{step4_detail.value or '_(not yet specified)_'}

- **Suggested action**: {step4_action.value or '_(not yet specified)_'}

## Step 5: Evaluation plan

- **Study design**: {step5_design.value or '_(not yet specified)_'}
- **Primary outcome**: {step5_outcome.value or '_(not yet specified)_'}
- **Baseline period**: {step5_baseline.value or '_(not yet specified)_'}
- **Post-go-live evaluation horizon**: {step5_horizon.value or '_(not yet specified)_'}

## Step 6: DCA-based threshold

- **Firing threshold (probability)**: {step6_threshold.value:.2f}
- **Expected alert-cohort prevalence**: {step6_prevalence.value:.1%}
- **Threshold rationale**: {step6_rationale.value or '_(not yet specified)_'}

## Step 7: Equity-monitoring plan

**Concern 1**

{step7_concern_1.value or '_(not yet specified)_'}

**Concern 2**

{step7_concern_2.value or '_(not yet specified)_'}

---

_Generated from the Course 12 capstone notebook. This brief is the starting deliverable for a CDS governance committee. The committee, the clinical content owner, the implementation analyst, the evaluation lead, and the patient-safety oversight should each see and sign off on the brief before implementation begins._
"""
    return (brief,)


@app.cell
def _(brief, mo):
    mo.md(brief)
    return


@app.cell
def _(brief, mo):
    download = mo.download(
        data=brief.encode("utf-8"),
        filename="cds-design-brief-ra-flare-alert.md",
        label="Download the design brief as Markdown",
    )
    download
    return (download,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## How to take this further

        Three operational guidelines for the reader who would actually deploy this kind of intervention.

        First, the design brief is the start, not the end. The governance committee will ask hard questions about the threshold, the FHIR-data prefetch performance, the override-rate target, the equity-monitoring frequency, and the retirement criteria. Each answer is a conversation, not a single sentence.

        Second, the prototype CDS service is the next deliverable. The brief specifies the logic; building the CQL library, the CDS Hooks service, and the EHR registration of the service is the next phase of work. Open-source CQL engines (DBCG CQL Translator, Pathling, the Apelon engine) are appropriate starting points.

        Third, the evaluation pre-registration is the next research deliverable. A pre-registered ITS plan (the design, the outcome, the analysis approach, the success criteria) protects the institution and the analysis team from the temptation to redefine success after the fact when the early results are mixed.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The curriculum closes

        Course 12 is the curriculum's capstone course. The seven-step exercise above integrates everything every prior course has covered: the computational decomposition from Course 01, the data-literacy framing from Course 02, the privacy and governance framework from Course 03, the epidemiology of the 2x2 table from Course 04, the EHR-systems understanding from Course 05, the FHIR data model from Course 06, the data-wrangling and OMOP material from Course 07, the visualization principles that shape how the alert renders from Course 08, the model-evaluation discipline from Course 09, the NLP toolset from Course 10, and the health-economics decision and DCA framework from Course 11.

        A reader who has worked through all twelve courses can sit in a CDS governance committee meeting as a credible clinical informaticist. The seven-step brief is the artifact that says so.

        Welcome to the field.
        """
    )
    return


if __name__ == "__main__":
    app.run()
