"""Track 04: Evaluating CDS.

A CDS intervention is a clinical intervention. The track combines the
DCA framework from Course 11 Track 5 (alert threshold as operating
point) with the before-and-after study-design framework from Course 04
Track 5 (interrupted time series), and closes with the four-category
unintended-consequences checklist every CDS evaluation should report.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import types

    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd

    _COURSE_TITLES = {
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

    return alt, mo, np, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 04: Evaluating CDS

        ## The premise

        A CDS intervention is a clinical intervention. It changes what clinicians do, which changes what happens to patients. The same evaluation discipline that applies to drugs (does it work? how well? for whom? at what cost? with what harms?) applies to alerts.

        The track combines two analytic frames the curriculum has already built. Course 11 Track 5 introduced decision curve analysis (DCA): a chart that says, at the threshold a clinician would actually act on, does the model add net benefit over treating everyone or treating no one. Applied to CDS, the question becomes: at the threshold the alert fires at, does the alert add net benefit over no-alert or fire-on-everyone. Course 04 Track 5 introduced study designs (interrupted time series, controlled before-after, segmented regression). Applied to CDS, the question becomes: when we turned the alert on, did the clinical outcome change in a way that cannot be explained by background trends.

        The two frames together are the operational core of CDS evaluation. The track closes with the unintended-consequences checklist that distinguishes a complete evaluation from a partial one.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## DCA at the alert threshold

        Course 11 Track 5 derived net benefit at a threshold as

        $$
        \text{NB}(t) = \frac{\text{TP}}{n} - \frac{\text{FP}}{n} \cdot \frac{t}{1 - t}
        $$

        and constructed the three-curve chart (use the model / treat all / treat none). Applied to a CDS alert, the three curves become: fire the alert at threshold t, fire the alert on everyone (constantly informational banner), fire the alert on no one. The model is the CDS rule; the threshold is the alert's firing threshold.

        Three operational decisions follow.

        First, the operating threshold is the load-bearing parameter. A rule with excellent discrimination (high AUC) can still produce a noisy alert if the threshold is set wrong. DCA gives the threshold range over which the alert adds value; the deployment threshold should sit inside that range.

        Second, the operating threshold determines the alert volume. At a low threshold the alert fires often (catches more true positives, produces more false positives). At a high threshold it fires rarely (catches fewer true positives, produces fewer false positives). The DCA chart and the volume calculation together determine where the operating point should sit.

        Third, the operating threshold determines the alert's clinical action profile. A high-PPV alert (high threshold) can drive an active recommendation or autonomous action. A lower-PPV alert (lower threshold) is appropriate only as a passive flag or an informational card. The threshold choice and the spectrum-point choice from Track 01 are coupled.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Before-and-after study designs for CDS rollout

        The CDS go-live is the intervention; the clinical outcome on the affected cohort is the outcome. Three study designs apply.
        """
    )
    return


@app.cell
def _(pd):
    designs_table = pd.DataFrame(
        [
            {
                "Design": "Simple before-after",
                "What it does": "Compares the outcome rate during a baseline period to the outcome rate after the CDS went live.",
                "Strengths": "Easy to set up. Uses data the institution already has.",
                "Weaknesses": "Cannot distinguish the alert's effect from background trends. A declining mortality rate in the year of go-live could be the alert or could be an unrelated improvement (better triage, EHR transition, seasonal pattern).",
            },
            {
                "Design": "Interrupted time series (ITS)",
                "What it does": "Measures the outcome at many time points before and after go-live; fits a regression with an interruption term at go-live to separate the level change (immediate effect) from the slope change (sustained effect).",
                "Strengths": "Distinguishes the intervention from background trends if the time series is long enough. The most-used CDS-evaluation design in the published literature.",
                "Weaknesses": "Requires a long enough baseline (typically 12+ months) and post-period (typically 6+ months). Sensitive to seasonality and external events.",
            },
            {
                "Design": "Controlled before-after / stepped wedge",
                "What it does": "Rolls out the CDS across institutional units in a staggered schedule; each unit is its own before-after, and unrolled-yet units serve as concurrent controls.",
                "Strengths": "The strongest non-randomized design for CDS. Controls for institution-wide trends. Allows the rollout to proceed while the evaluation runs.",
                "Weaknesses": "Requires institutional coordination to stagger the rollout. The analysis is more complex than ITS.",
            },
        ]
    )
    designs_table.index = range(1, len(designs_table) + 1)
    designs_table.index.name = "row"
    designs_table
    return (designs_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Two operational rules for picking the design.

        First, prefer ITS over simple before-after whenever the time series is available. Most modern EHRs can produce the monthly or weekly outcome counts that ITS requires. The increment in design quality is large; the increment in analysis difficulty is modest.

        Second, prefer the stepped-wedge design when the institution can stagger the rollout across units (floors, services, hospitals). The randomization at the unit level controls for many sources of confounding that ITS cannot.

        The two rules together implicitly rule out the most common CDS evaluation: the simple two-period before-after with no time-series, no control, no statistical adjustment. The evidence value of such a design is low; the evidence value of an ITS or stepped-wedge is high. The publication norms in the CDS literature increasingly require one of the latter.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A small ITS example: alert rollout and override rate

        The chart below shows a synthetic interrupted time series. The monthly count of inappropriate orders (the outcome the alert was designed to prevent) is plotted across 24 months. The CDS alert went live at month 12. The fitted regression has a level term (immediate drop at go-live) and a slope term (change in trend).
        """
    )
    return


@app.cell
def _(alt, np, pd):
    its_rng = np.random.default_rng(seed=20260601)
    months = np.arange(1, 25)
    intercept = 80
    baseline_slope = -1.5
    level_change = -25
    post_slope_change = 0.5
    expected = []
    for m in months:
        post = 1 if m >= 12 else 0
        post_time = max(m - 11, 0)
        e = intercept + baseline_slope * m + level_change * post + post_slope_change * post_time
        expected.append(e)
    expected = np.array(expected)
    noise = its_rng.normal(0, 4, len(months))
    counts = np.maximum(0, np.round(expected + noise))
    its_df = pd.DataFrame({"month": months, "count": counts.astype(int), "period": ["pre" if m < 12 else "post" for m in months]})
    fit_df = pd.DataFrame({"month": months, "fit": expected, "period": ["pre" if m < 12 else "post" for m in months]})
    return baseline_slope, counts, expected, fit_df, intercept, its_df, its_rng, level_change, months, noise, post_slope_change


@app.cell
def _(alt, fit_df, its_df, pd):
    rule_x = pd.DataFrame({"month": [11.5], "rule": ["alert go-live"]})
    chart = (
        alt.Chart(its_df).mark_circle(size=80, color="#1f77b4").encode(
            x=alt.X("month:Q", title="Month"),
            y=alt.Y("count:Q", title="Monthly count of inappropriate orders"),
            tooltip=["month:Q", "count:Q"],
        )
        + alt.Chart(fit_df).mark_line(color="#d62728").encode(
            x="month:Q",
            y="fit:Q",
            detail="period:N",
        )
        + alt.Chart(rule_x).mark_rule(color="#888", strokeDash=[4, 2]).encode(x="month:Q")
        + alt.Chart(rule_x).mark_text(align="left", dx=4, dy=-130, color="#888", fontSize=11).encode(x="month:Q", text="rule:N")
    ).properties(width=580, height=320, title="Interrupted time series: inappropriate orders before and after CDS go-live")
    chart
    return chart, rule_x


@app.cell
def _(mo):
    mo.md(
        r"""
        Three observations from the synthetic chart.

        First, the level change (the immediate drop at month 12) is the alert's immediate effect on the outcome. A simple before-after would compare the pre-period mean to the post-period mean; ITS isolates the level term specifically.

        Second, the slope change (the change in the trend line's slope at month 12) is the alert's sustained effect. A positive slope change in the post-period would mean the alert's effect wore off (clinicians learned to override; the inappropriate-order rate climbed back). A negative slope change would mean the alert's effect grew (clinicians changed their default ordering behavior; the rate continued to decline). The synthetic series above shows a small positive post-slope-change, consistent with a partial wearing-off effect.

        Third, the baseline trend matters. A baseline that was already declining would have continued to decline without the alert; the post-period decline alone overstates the alert's effect. ITS adjusts for the baseline trend by construction; simple before-after does not.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The unintended-consequences checklist

        A CDS evaluation that reports only the primary outcome is incomplete. Four categories of unintended consequence appear frequently enough in the CDS literature to warrant a checklist.
        """
    )
    return


@app.cell
def _(pd):
    consequences_table = pd.DataFrame(
        [
            {
                "Category": "Workflow disruption",
                "What it looks like": "The alert adds time per encounter, slows order entry, lengthens the average visit. Clinicians compensate by closing chart sections faster, skipping documentation, or rescheduling.",
                "How to measure": "Time-motion study before and after rollout, or EHR-audit-log analysis of the time between order initiation and order signing.",
            },
            {
                "Category": "Equity impact",
                "What it looks like": "The alert's true-positive rate differs across patient subgroups (race, sex, language, payer). Subgroups under-flagged by the alert get less of the intervention; subgroups over-flagged get more.",
                "How to measure": "Subgroup-stratified analysis of the alert's PPV and fire rate against the patient outcome of interest. Course 09 Track 5 introduced the fairness-metric trade-offs.",
            },
            {
                "Category": "Automation bias",
                "What it looks like": "Clinicians follow the alert's recommendation when it is wrong, or fail to act when the alert does not fire even though they otherwise would have. The clinician's clinical judgment is partially replaced by the alert's judgment.",
                "How to measure": "Cases where the alert recommended an action that was clinically wrong (per chart review) and the clinician followed the alert anyway. Counts where the alert did not fire on cases that should have been flagged and the clinician also did not act.",
            },
            {
                "Category": "Alert-fatigue spillover",
                "What it looks like": "The new alert displaces attention from other alerts in the same channel. The override rate on adjacent alerts climbs after the new alert goes live, even though the adjacent alerts themselves have not changed.",
                "How to measure": "Override rates on other alerts at patient-view (or whatever the shared channel is) measured before and after rollout. Sittig-Singh 8-dimensional model formalizes this in the sociotechnical category.",
            },
        ]
    )
    consequences_table.index = range(1, len(consequences_table) + 1)
    consequences_table.index.name = "row"
    consequences_table
    return (consequences_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three operational rules for the unintended-consequences check.

        First, the check is required, not optional. A CDS evaluation paper that does not address the four categories above is incomplete; a CDS deployment that does not monitor them post-rollout is incomplete operations.

        Second, the equity check is the highest-leverage of the four. A CDS deployment with disparate subgroup performance can entrench or worsen existing disparities. The subgroup-stratified analysis the Course 09 Track 5 fairness vocabulary requires applies directly here.

        Third, the alert-fatigue-spillover check is the most often overlooked. A new alert that performs well on its own primary outcome can still be net-harmful if it degrades the rest of the alert portfolio. The override-rate-on-adjacent-alerts measurement is short, cheap, and high-value.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "12",
        "11",
        "DCA at the alert threshold",
        "Course 11 Track 5 introduced decision curve analysis. The application here is direct: the alert's firing threshold is the operating point on the DCA chart; the chart tells you the threshold range over which the alert adds net benefit. The threshold inside the range that maximizes net benefit is the threshold the alert should fire at.",
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "12",
        "04",
        "Interrupted time series and before-after designs",
        "Course 04 Track 5 introduced the study-design vocabulary. The CDS-rollout case is the canonical application of ITS and stepped-wedge designs; the same design considerations Course 04 raised (baseline length, seasonality, concurrent control) apply directly here.",
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "12",
        "09",
        "Subgroup performance and fairness",
        "Course 09 Track 5 introduced the four entry points for bias and the subgroup-performance vocabulary. The equity-impact item in the unintended-consequences checklist applies that vocabulary at the deployed-alert level: the alert is a model in the wild, and its subgroup PPV and fire rate determine the equity of the deployment.",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "12",
        "17",
        "Sociotechnical evaluation of CDS",
        "Course 17 (Workflow, safety, human factors) extends the alert-fatigue and workflow-disruption material into the broader sociotechnical-systems framework. The Sittig-Singh 8-dimensional model is the deeper version of the unintended-consequences checklist; CDS evaluation papers in the safety literature increasingly map their findings against the 8 dimensions.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        A CDS intervention is a clinical intervention. The two analytic frames the rest of the curriculum has built apply directly: DCA from Course 11 Track 5 determines the alert's firing threshold by maximizing net benefit; ITS or stepped-wedge designs from Course 04 Track 5 measure the alert's effect on the clinical outcome after rollout. The unintended-consequences checklist (workflow disruption, equity impact, automation bias, alert-fatigue spillover) is what distinguishes a complete CDS evaluation from a partial one; the equity item draws directly on Course 09 Track 5.

        Track 05 takes up the governance and human side: who decides what CDS gets built, who decides what gets retired, what the regulatory landscape looks like, and the vendor-evaluation checklist for any new CDS tool an institution is considering.
        """
    )
    return


if __name__ == "__main__":
    app.run()
