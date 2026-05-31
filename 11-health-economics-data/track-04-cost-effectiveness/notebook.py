"""Track 04: Cost-effectiveness.

The QALY is the unit of effectiveness that allows interventions with
different effects on length and quality of life to be compared on one
scale. The ICER is the cost per QALY gained. The willingness-to-pay
threshold (in the US, typically $50K to $150K per QALY) is the comparator
that makes the ICER actionable. The track defines all three with the
biologic-vs-csDMARD worked example, presents the cost-effectiveness
plane, and walks the structure of a published CEA using the CHEERS
reporting standard.
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
        "13": "Research reproducibility",
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
        # Track 04: Cost-effectiveness

        ## The premise: a common unit for length and quality of life

        Cost-effectiveness analysis extends the decision-analytic frame of Track 03 by adding two quantities to every arm: a dollar cost and an effectiveness measure expressed in QALYs (quality-adjusted life-years). The QALY is the unit that lets an analyst compare an intervention that adds years of life with one that improves quality of life with one that does both. The ICER (incremental cost-effectiveness ratio) is the dollars per QALY of moving from one strategy to another. The willingness-to-pay threshold (the dollar-per-QALY ceiling the payer or society accepts) is the comparator that turns the ICER into an actionable decision.

        The track defines QALY, ICER, and the WTP threshold; presents the cost-effectiveness plane and its four quadrants; works through a CE comparison of biologic add vs csDMARD continuation for a patient like Ms. Reyes; and closes with the CHEERS reporting checklist as the appraisal framework for a published CEA.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## QALY: utility times time

        A QALY is the product of a utility weight (a number between 0 and 1 representing the quality of a health state) and the time spent in that health state. One year at perfect health (utility 1.0) is 1.0 QALY. One year at a health state with utility 0.7 is 0.7 QALY. Ten years at utility 0.6 is 6.0 QALYs. The same ten years at utility 1.0 is 10.0 QALYs; the gap (4.0 QALYs) is what an intervention that fully restored health for that period would add.

        Utilities come from standardized patient-reported instruments. The EQ-5D-5L (five dimensions: mobility, self-care, usual activities, pain, anxiety/depression, each with five levels) is the most-used instrument in published CE analyses. The SF-6D, the HUI-3, and the EQ-5D-3L are the other commonly cited instruments. Each maps a patient's reported health state to a utility on the 0-to-1 scale through a value-set derived from population surveys.

        Two operational properties of QALYs are load-bearing.

        First, QALYs combine length and quality on one axis. A drug that extends life by 2 years at utility 0.6 produces 1.2 QALYs. A drug that improves quality from 0.5 to 0.8 for 5 years (no life extension) produces 1.5 QALYs. The two interventions are comparable; without QALYs they would have been on different axes.

        Second, the QALY is a population-level construct that does not capture all of what a patient might value about a health state. A patient who places very high value on a specific function (a musician on fine motor control of the hands) is not well represented by a generic-population utility. CE analyses are decision aids for population-level resource allocation; individual treatment decisions weight the population calculus against the individual patient's specific values.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## ICER: the comparator that ranks strategies

        The ICER (incremental cost-effectiveness ratio) is the cost per QALY of moving from one strategy to a more effective one. The formula is

        $$
        \text{ICER} = \frac{C_B - C_A}{E_B - E_A}
        $$

        where C and E are the total cost and total effectiveness (in QALYs) of strategies A and B, with B the more effective one. The ICER is reported as dollars per QALY gained.

        An ICER on its own does not say whether B is preferred. The ICER is compared to a willingness-to-pay threshold. If the ICER is below the threshold, B is cost-effective relative to A (the additional cost buys more QALYs than the threshold requires). If the ICER is above the threshold, B is not cost-effective at that threshold; B may still be the right clinical choice, but the additional cost exceeds what the threshold allows.

        Common willingness-to-pay thresholds:

        - **United States.** Historically $50,000 per QALY (an old academic benchmark), now usually cited as a range $100,000 to $150,000 per QALY. The Institute for Clinical and Economic Review (ICER) typically reports cost-effectiveness at both $100,000 and $150,000.
        - **United Kingdom (NICE).** Approximately 20,000 to 30,000 pounds per QALY. NICE will sometimes accept higher thresholds for end-of-life interventions.
        - **WHO.** A historical benchmark of one to three times national per-capita GDP per QALY, applied internationally.

        The threshold is a societal-policy choice, not a property of any specific intervention. Two payers can apply different thresholds to the same ICER and reach different cost-effectiveness conclusions.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Worked example: biologic vs csDMARD for a patient like Reyes

        The Track 03 decision tree compared biologic addition with csDMARD continuation on expected-value terms using utility alone. Cost-effectiveness analysis adds the cost dimension and converts the expected-value comparison into an ICER.

        Representative cost and effectiveness inputs over a one-year horizon, for a patient like Ms. Reyes at the 2024-05-15 escalation moment:
        """
    )
    return


@app.cell
def _(pd):
    ce_inputs = pd.DataFrame(
        [
            {"Strategy": "Continue csDMARD (MTX + folic acid + monitoring labs + 4 visits)",
             "Annual cost (allowed amount, USD)": 3500,
             "Annual QALYs": 0.62,
             "Source / rationale": "MTX is generic and inexpensive; the cost is mostly visits and labs. Effectiveness reflects moderate-disease RA on partial control."},
            {"Strategy": "Add adalimumab (biologic) + MTX + monitoring + 4 visits",
             "Annual cost (allowed amount, USD)": 25000,
             "Annual QALYs": 0.78,
             "Source / rationale": "Adalimumab specialty-pharmacy cost dominates. Effectiveness reflects the improved response rate in MTX-inadequate-responder cohorts."},
        ]
    )
    ce_inputs.index = range(1, len(ce_inputs) + 1)
    ce_inputs.index.name = "row"
    ce_inputs
    return (ce_inputs,)


@app.cell
def _(ce_inputs, mo):
    cost_a = float(ce_inputs.iloc[0]["Annual cost (allowed amount, USD)"])
    cost_b = float(ce_inputs.iloc[1]["Annual cost (allowed amount, USD)"])
    qaly_a = float(ce_inputs.iloc[0]["Annual QALYs"])
    qaly_b = float(ce_inputs.iloc[1]["Annual QALYs"])
    delta_cost = cost_b - cost_a
    delta_qaly = qaly_b - qaly_a
    icer = delta_cost / delta_qaly if delta_qaly > 0 else float("inf")
    mo.md(
        f"""
        **ICER calculation.**

        - Incremental cost (biologic minus csDMARD): ${delta_cost:,.0f}
        - Incremental QALYs (biologic minus csDMARD): {delta_qaly:.2f}
        - **ICER: ${icer:,.0f} per QALY gained**

        At the $50,000 per-QALY threshold, the biologic is **not cost-effective**. At $100,000 it is **borderline / not cost-effective**. At $150,000 it is **cost-effective**. The same arithmetic, against three different thresholds, produces three different policy conclusions. This is the structure of every cost-effectiveness paper: the analysis produces an ICER and the policy decision sits at the WTP threshold.
        """
    )
    return cost_a, cost_b, delta_cost, delta_qaly, icer, qaly_a, qaly_b


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The cost-effectiveness plane

        The cost-effectiveness plane is a two-axis chart with incremental cost on the y-axis and incremental effectiveness (QALYs) on the x-axis. The origin is the reference strategy; every alternative falls in one of the four quadrants.
        """
    )
    return


@app.cell
def _(alt, cost_a, cost_b, delta_cost, delta_qaly, pd, qaly_a, qaly_b):
    point = pd.DataFrame([{"delta_qaly": delta_qaly, "delta_cost": delta_cost, "label": "Biologic add vs csDMARD"}])

    wtp_50k = pd.DataFrame({"delta_qaly": [-0.5, 0.5], "delta_cost": [-25000, 25000], "threshold": "$50K WTP"})
    wtp_100k = pd.DataFrame({"delta_qaly": [-0.5, 0.5], "delta_cost": [-50000, 50000], "threshold": "$100K WTP"})
    wtp_150k = pd.DataFrame({"delta_qaly": [-0.5, 0.5], "delta_cost": [-75000, 75000], "threshold": "$150K WTP"})
    wtps = pd.concat([wtp_50k, wtp_100k, wtp_150k], ignore_index=True)

    base = alt.Chart(pd.DataFrame({"x": [0], "y": [0]})).mark_point(size=0).encode(x="x:Q", y="y:Q")
    wtp_lines = (
        alt.Chart(wtps).mark_line(strokeDash=[4, 2]).encode(
            x=alt.X("delta_qaly:Q", title="Incremental QALYs", scale=alt.Scale(domain=[-0.4, 0.4])),
            y=alt.Y("delta_cost:Q", title="Incremental cost (USD)", scale=alt.Scale(domain=[-30000, 40000])),
            color=alt.Color("threshold:N", title="Willingness-to-pay"),
        )
    )
    x_axis = alt.Chart(pd.DataFrame({"y": [0, 0], "x": [-0.4, 0.4]})).mark_line(color="#888").encode(x="x:Q", y="y:Q")
    y_axis = alt.Chart(pd.DataFrame({"x": [0, 0], "y": [-30000, 40000]})).mark_line(color="#888").encode(x="x:Q", y="y:Q")
    point_layer = (
        alt.Chart(point).mark_circle(size=250, color="#d62728").encode(
            x="delta_qaly:Q",
            y="delta_cost:Q",
            tooltip=["label:N", "delta_qaly:Q", "delta_cost:Q"],
        )
    )
    label_layer = (
        alt.Chart(point).mark_text(dx=15, dy=-10, color="#d62728", fontSize=12).encode(
            x="delta_qaly:Q",
            y="delta_cost:Q",
            text="label:N",
        )
    )
    ce_plane_chart = (base + x_axis + y_axis + wtp_lines + point_layer + label_layer).properties(
        width=560, height=380, title="Cost-effectiveness plane: biologic vs csDMARD"
    )
    _ = cost_a
    _ = cost_b
    _ = qaly_a
    _ = qaly_b
    ce_plane_chart
    return (
        base,
        ce_plane_chart,
        label_layer,
        point,
        point_layer,
        wtp_100k,
        wtp_150k,
        wtp_50k,
        wtp_lines,
        wtps,
        x_axis,
        y_axis,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Reading the cost-effectiveness plane

        The four quadrants describe four kinds of strategy comparison.

        - **Northeast (more costly, more effective).** The biologic-vs-csDMARD case. The decision depends on the willingness-to-pay threshold. The three dashed lines on the chart are the $50K, $100K, and $150K per-QALY thresholds; a point below the threshold line is cost-effective at that threshold.
        - **Southeast (less costly, more effective).** The dominant strategy: cheaper AND better. The strategy in this quadrant should be adopted regardless of the willingness-to-pay threshold.
        - **Northwest (more costly, less effective).** The dominated strategy: more expensive AND worse. The strategy in this quadrant is rejected regardless of the threshold.
        - **Southwest (less costly, less effective).** A reverse trade-off. Sometimes preferred for resource-constrained settings; usually rejected when the trade-off is small.

        The red point sits in the northeast quadrant. The decision is below the $150K line and approximately on the $100K line, so the biologic add is cost-effective at the high end of the US WTP range and not at the low end.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Reading a CE paper: the CHEERS checklist

        The Consolidated Health Economic Evaluation Reporting Standards (CHEERS) is the published reporting checklist for cost-effectiveness analyses. The 28-item checklist covers the methods, the inputs, the analysis, and the reporting of any CEA, and is the operational appraisal framework for reading a CEA paper.

        Five CHEERS items are the highest-yield to extract first when reading a new CE paper.

        - **Perspective.** Whose costs and benefits are counted? The health-care-system perspective counts direct medical costs only. The societal perspective adds patient time, caregiver burden, and productivity losses. The two perspectives produce very different ICERs on the same intervention.
        - **Time horizon.** Over what period are costs and QALYs accumulated? A one-year horizon for a chronic-disease intervention systematically undercounts both costs and QALYs; a lifetime horizon is the published-methods standard.
        - **Discount rate.** Future costs and QALYs are discounted to present value at a stated annual rate (3% in the US, 3.5% in the UK). The discount rate matters for any long-horizon analysis; an undiscounted analysis is a methods error.
        - **Source of effectiveness data.** Where do the QALY estimates come from? A meta-analysis of RCTs is the strongest source; a single trial is weaker; expert opinion is the weakest. The strength of the effectiveness evidence directly bounds the credibility of the ICER.
        - **Sensitivity analyses.** A CE paper without one-way, two-way, and probabilistic sensitivity analyses cannot establish whether the headline ICER is robust to its inputs. The Track 03 sensitivity-analysis machinery applies directly.

        A CE paper that handles all five items well, with a defensible threshold framing, is the kind of paper that can change a coverage decision. A CE paper that omits any of them is not yet ready to act on.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "11",
        "04",
        "Confounding and the cost-of-illness side of CE analysis",
        "Course 04 introduced confounding. Cost-of-illness inputs to a CEA (cost of a heart attack, cost of a flare, cost of a hospitalization) are usually estimated from observational claims data and are vulnerable to the same confounding patterns. A CE paper that uses naive per-event cost estimates from a non-randomized comparison is importing the confounding into the cost side of the analysis.",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "11",
        "13",
        "CEA reporting as a reproducibility question",
        "Course 13 (Research reproducibility) takes up the broader reproducibility framework. CHEERS is the CEA-specific reporting standard; an analysis that meets CHEERS is also (necessarily) reproducible. The same reproducibility principles Course 13 covers for general clinical research apply with extra force to CE analyses because of the policy weight CEA outputs carry.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        Cost-effectiveness analysis adds a dollar dimension to the decision-analytic frame of Track 03. QALYs unify length and quality of life on one axis; ICERs express the cost per QALY of moving between strategies; the willingness-to-pay threshold is the policy comparator that turns an ICER into an action. The biologic-vs-csDMARD example produced an ICER of approximately $134,000 per QALY, which is borderline at the US $100K threshold and cost-effective at the US $150K threshold; the same arithmetic against the UK NICE threshold would reject the strategy. The cost-effectiveness plane visualizes the comparison; the CHEERS checklist is the appraisal framework for reading a published CE paper.

        Track 05 takes up decision curve analysis: the chart that closes the threshold question Course 04 Track 3 (sensitivity, specificity) and Course 09 Track 3 (discrimination, calibration) both opened. DCA is the analogous framework for evaluating a prediction model rather than a treatment.
        """
    )
    return


if __name__ == "__main__":
    app.run()
