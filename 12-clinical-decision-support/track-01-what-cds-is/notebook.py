"""Track 01: What CDS actually is.

Clinical decision support is a spectrum, not a single thing. The track
defines the spectrum, names the five-rights framework, addresses the
alert-fatigue / 97%-override-rate problem, and frames a CDS alert as a
diagnostic test the same low-prevalence-low-PPV math from Course 04
applies to.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import types

    import altair as alt
    import marimo as mo
    import pandas as pd

    _COURSE_TITLES = {
        "01": "Computational thinking",
        "04": "Clinical epidemiology",
        "09": "AI in medicine",
        "11": "Health economics data",
        "17": "Workflow, safety, human factors",
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

    return alt, mo, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 01: What CDS actually is

        ## The premise: CDS is a spectrum

        Clinical decision support is a spectrum of interventions, not a single thing. At the passive end, the EHR displays a flag or a banner the clinician reads or ignores. In the middle, the EHR returns an active recommendation with a suggested action the clinician can accept or reject inline. At the autonomous end, the EHR takes the action without clinician input (an order set fires automatically when a sepsis screen positive, an order is cancelled because of a drug-drug interaction). The same intervention sits at different points on the spectrum depending on the workflow placement and the institutional governance.

        The track defines the spectrum, names the five-rights framework that distinguishes a designed intervention from a noisy one, addresses the alert-fatigue and 97%-override-rate problem that is the default outcome of poorly designed CDS, and reframes the alert as a diagnostic test the same low-prevalence-low-PPV math from Course 04 governs.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The three-point CDS spectrum
        """
    )
    return


@app.cell
def _(pd):
    spectrum_table = pd.DataFrame(
        [
            {
                "Spectrum point": "Passive alert",
                "What it does": "Displays information; the clinician reads or ignores. No action is requested. No accept/reject control.",
                "Examples": "Best-practice advisory banner at chart open. Flagged lab value with a recommended-action note. Cohort-membership ribbon.",
                "When to use": "When the information should be visible but the clinician's clinical judgment determines whether and how to act.",
            },
            {
                "Spectrum point": "Active recommendation",
                "What it does": "Surfaces a specific suggested action the clinician can accept or reject. The accept control applies the change without forcing the clinician to navigate elsewhere.",
                "Examples": "Order-set suggestion at order entry. Dose-adjustment card at order-sign. Alternative-medication offer at order-select.",
                "When to use": "When the recommended action is specific, the evidence supports it, and the workflow moment is the right one for the clinician to decide.",
            },
            {
                "Spectrum point": "Autonomous action",
                "What it does": "Takes the clinical action without clinician decision in the moment. The clinician may be notified after the fact, may have to consciously opt out, or may not be involved at all.",
                "Examples": "Auto-cancellation of an order with a hard-stop drug-drug interaction. Automatic sepsis-bundle order set when a screening rule fires. Automatic chart-deficiency closure.",
                "When to use": "When the rule is high-specificity, the consequence of the action is reversible, and the governance is willing to take responsibility for the action.",
            },
        ]
    )
    spectrum_table.index = range(1, len(spectrum_table) + 1)
    spectrum_table.index.name = "row"
    spectrum_table
    return (spectrum_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Two properties of the spectrum are load-bearing for the rest of the course.

        First, the spectrum is not a maturity ladder. A well-designed passive alert can be more useful than a poorly-designed autonomous action; an autonomous action that takes the wrong action removes the clinician's ability to catch the error. The right point on the spectrum depends on the rule, the workflow, and the cost of being wrong, not on a generic preference for one end over the other.

        Second, most clinical CDS today is passive or active-recommendation. Autonomous actions are reserved for narrow categories where the rule is highly specific and the action is reversible. The published literature on CDS evaluation almost entirely concerns passive and active-recommendation interventions; the alert-fatigue evidence comes from those categories.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Why most CDS fails: alert fatigue and the 97% override

        The published override rates for inpatient drug-interaction alerts range from approximately 49% to 96% depending on the institution and the alert category. The pattern is well-documented across thirty years of CDS evaluation literature. A clinician seeing the same low-yield alert many times per day stops reading the alerts; once that pattern sets in, real signals are missed inside the noise. This is alert fatigue, and it is the default outcome of CDS that has not been carefully designed.

        Three observations about alert fatigue are load-bearing.

        First, alert fatigue is upstream. The remedy is in the design of the alert (cohort definition, threshold selection, workflow placement, format), not in clinician training. A clinician who is told to "pay more attention to the alerts" while the alerts continue to fire at the same noisy rate will adapt to the noise again within weeks.

        Second, alert fatigue spreads. A poorly designed alert in one workflow channel desensitizes the clinician to all alerts in that channel. The collateral damage to the rest of the CDS portfolio is one of the most underappreciated costs of a single bad alert.

        Third, alert fatigue is measurable. The override rate is the standard headline metric. An override rate above approximately 90% is the operational definition; an override rate climbing across months is the leading indicator that a deployed alert is becoming a fatigue source.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "12",
        "01",
        "The sepsis-alert worked example from Course 01",
        "Course 01 Track 1 introduced the picture of a clinical decision rule with the canonical 40-times-per-day sepsis-alert example. The alert-fatigue problem this track addresses is the same rule from the CDS-deployment side: the rule's parameters and threshold are the upstream cause, and the override rate is the downstream symptom.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The five rights of CDS

        The published framework for designing a CDS intervention that does not produce alert fatigue is the five rights: right information, right person, right format, right channel, right time. Each is a design dimension; failing any one is usually enough to make the alert ignored. The framework appears in the CDS Implementer's Guide (Osheroff et al.) and is the standard checklist used in CDS governance committees.
        """
    )
    return


@app.cell
def _(pd):
    five_rights_table = pd.DataFrame(
        [
            {
                "Right": "Right information",
                "Question to ask": "Is the recommendation evidence-based and specific to this patient at this moment?",
                "Failure mode": "Generic advisory that fires for every patient with a matching code. Clinician reads it once, learns it is non-specific, ignores it thereafter.",
            },
            {
                "Right": "Right person",
                "Question to ask": "Is the recipient the clinician who can act on the recommendation?",
                "Failure mode": "Alert fires to the inpatient hospitalist about an outpatient rheumatology recommendation. The recipient cannot act on it and routes it to the inbox of someone who never sees it.",
            },
            {
                "Right": "Right format",
                "Question to ask": "Is the recommendation presented as a card the clinician can accept with one click, rather than as a paragraph of text?",
                "Failure mode": "Six-line text alert with no accept button. Clinician reads (or skims), dismisses, no action taken.",
            },
            {
                "Right": "Right channel",
                "Question to ask": "Is the recommendation delivered through the channel the clinician will see it in, not buried in a sidebar or an after-the-fact inbox message?",
                "Failure mode": "Recommendation posted to a secondary tab the clinician opens twice a week.",
            },
            {
                "Right": "Right time",
                "Question to ask": "Is the recommendation delivered at the workflow moment the clinician is making the decision the recommendation is about?",
                "Failure mode": "Drug-allergy alert that fires at order-sign, after the clinician has spent two minutes constructing the order. The alert is now an interruption rather than a guidance.",
            },
        ]
    )
    five_rights_table.index = range(1, len(five_rights_table) + 1)
    five_rights_table.index.name = "row"
    five_rights_table
    return (five_rights_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Two operational guidelines for using the five-rights framework.

        First, the framework is a checklist, not a hierarchy. A passing alert hits all five. Failing any one is a reason to redesign before deployment, not a defect to be addressed later.

        Second, the framework is the right starting point for both the design of a new alert and the post-mortem of a noisy deployed one. An alert with a high override rate has failed at least one of the five rights; the post-mortem question is which one.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A CDS alert is a diagnostic test

        The most useful single reframe of CDS design is that an alert is a diagnostic test. The alert fires when a rule returns true; the rule is built to identify patients in a target state (developing sepsis, at risk of a flare, requiring a dose adjustment). Course 04 Track 3 introduced the 2x2 table and the prevalence-PPV relationship for diagnostic tests; the same math governs CDS alerts.

        The high-leverage consequence: at low target-state prevalence, a CDS alert with high sensitivity and high specificity can still have a very low PPV. The interactive below makes the relationship visible.
        """
    )
    return


@app.cell
def _(mo):
    prev_slider = mo.ui.slider(start=0.001, stop=0.20, step=0.001, value=0.02, label="Target-state prevalence among alertable patients", show_value=True)
    sens_slider = mo.ui.slider(start=0.50, stop=1.00, step=0.01, value=0.90, label="Alert sensitivity (true-positive rate)", show_value=True)
    spec_slider = mo.ui.slider(start=0.50, stop=1.00, step=0.01, value=0.85, label="Alert specificity (true-negative rate)", show_value=True)
    mo.vstack([prev_slider, sens_slider, spec_slider])
    return prev_slider, sens_slider, spec_slider


@app.cell
def _(mo, prev_slider, sens_slider, spec_slider):
    prev = prev_slider.value
    sens = sens_slider.value
    spec = spec_slider.value
    n = 1000
    n_pos = n * prev
    n_neg = n * (1 - prev)
    tp = n_pos * sens
    fn = n_pos * (1 - sens)
    tn = n_neg * spec
    fp = n_neg * (1 - spec)
    ppv = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    npv = tn / (tn + fn) if (tn + fn) > 0 else 0.0
    n_alerts = tp + fp
    fp_per_tp = fp / tp if tp > 0 else float("inf")
    mo.md(
        f"""
        **At prevalence {prev:.1%}, sensitivity {sens:.0%}, specificity {spec:.0%}** (per 1,000 alertable patients):

        - **True positives**: {tp:.1f}
        - **False positives**: {fp:.1f}
        - **True negatives**: {tn:.1f}
        - **False negatives**: {fn:.1f}
        - **Total alerts**: {n_alerts:.1f}
        - **PPV** (fraction of alerts that are real): **{ppv:.1%}**
        - **NPV**: {npv:.1%}
        - **False positives per true positive**: **{fp_per_tp:.1f}**

        Read the last number first. At low prevalence and realistic specificity, a CDS alert that fires for every detection produces many false-positive alerts for every true positive. A 90%-sensitive 85%-specific alert at 2% prevalence produces approximately 8 false-positive alerts for every true positive. After a clinician sees that ratio for two weeks, the alert is ignored.
        """
    )
    return fn, fp, fp_per_tp, n, n_alerts, n_neg, n_pos, npv, ppv, prev, sens, spec, tn, tp


@app.cell
def _(mo):
    mo.md(
        r"""
        Three operational consequences for CDS design.

        First, raising specificity is the highest-leverage move. PPV is exquisitely sensitive to specificity at low prevalence; a small specificity improvement produces a large PPV improvement. The CDS design effort should be focused on tightening the rule's specificity (excluding the patients the rule should not fire for) more than on chasing the last few percentage points of sensitivity.

        Second, narrowing the cohort raises prevalence. A rule that fires on every patient at chart open will operate at the population prevalence of the target state. A rule that fires only on a sub-cohort already known to be at higher risk (RA patients with rising CRP, septic-screen-positive patients) operates at higher local prevalence and therefore higher PPV at the same sensitivity and specificity.

        Third, the diagnostic-test framing applies to the choice of action, not only to the alert. A high-PPV alert that produces a low-cost suggested action can be deployed widely; a low-PPV alert can still be useful if the suggested action is low-cost and high-leverage (a one-click suggested order). The interaction of PPV with action cost determines what kind of intervention the alert should drive.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "12",
        "04",
        "Sensitivity, specificity, PPV from Course 04",
        "Course 04 Track 3 introduced the 2x2 table and the prevalence-PPV relationship. A CDS alert is a diagnostic test whose target state is the clinical event the alert is meant to surface; the same math governs the alert's positive predictive value at deployment.",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "12",
        "11",
        "DCA at the alert threshold",
        "Course 11 Track 5 introduced decision curve analysis. Track 4 of this course applies DCA directly at the alert-threshold-selection level: the threshold the alert fires at is the operating point on the DCA chart, and the question 'does this alert add net benefit at this threshold' is the question DCA was built to answer.",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "12",
        "17",
        "Workflow and human-factors aspects of CDS",
        "Course 17 (Workflow, safety, human factors) extends the alert-fatigue conversation into the broader sociotechnical system the alert sits inside. The Sittig-Singh 8-dimensional model the go-deeper links is the deeper version of the same framing.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        CDS is a three-point spectrum (passive alert / active recommendation / autonomous action). The right point depends on the rule, the workflow, and the cost of being wrong. The published five-rights framework (right information, right person, right format, right channel, right time) distinguishes designed CDS from alert-fatigue-producing CDS. Failing any of the five is usually enough to make the alert ignored. A CDS alert is a diagnostic test; the same low-prevalence-low-PPV math from Course 04 Track 3 governs the alert's positive predictive value at deployment. Raising specificity and narrowing the cohort to a higher-prevalence sub-population are the two highest-leverage design moves.

        Track 02 takes up CQL, the standards-based logic language the rule itself is written in. Track 03 takes up CDS Hooks, the standards-based delivery layer that gets the rule to the clinician at the right workflow moment.
        """
    )
    return


if __name__ == "__main__":
    app.run()
