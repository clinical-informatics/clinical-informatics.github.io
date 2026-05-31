"""Capstone for course 11: Decision tree for the RA treatment choice.

The reader assembles a decision tree for the biologic-vs-csDMARD choice in
a patient like Ms. Reyes, with the cost dimension added (the ICER from
Track 04) and a one-way sensitivity sweep over any chosen input (the
sensitivity machinery from Track 03). The output is the kind of artifact
a pharmacy and therapeutics committee would actually use in a formulary
decision.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    from dataclasses import dataclass, field

    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd

    # Decision-tree dataclasses inlined per WASM rule 1.
    @dataclass
    class Outcome:
        label: str
        probability: float
        utility: float

    @dataclass
    class Decision:
        label: str
        outcomes: list = field(default_factory=list)
        annual_cost: float = 0.0

        def expected_value(self):
            total_p = sum(o.probability for o in self.outcomes)
            if total_p <= 0:
                return 0.0
            return sum(o.probability * o.utility for o in self.outcomes) / total_p

    return Decision, Outcome, alt, mo, np, pd


@app.cell
def _(mo):
    mo.md(
        r"""
        # Capstone: Decision tree for the RA treatment choice

        ## The exercise

        Build a decision-analytic model for the biologic-vs-csDMARD treatment escalation choice in a patient like Ms. Reyes at the 2024-05-15 visit (DAS28 4.1 despite a year on MTX at 25 mg weekly). The model has three layers, each addressed by one block of reactive controls below.

        - **Clinical inputs.** Probability of each outcome on each treatment arm.
        - **Utility inputs.** Utility of each outcome on the 0-to-1 scale.
        - **Cost inputs.** Annual allowed cost per arm.

        The model produces expected value per arm, the ICER for the biologic vs csDMARD comparison, the cost-effectiveness verdict at each of three WTP thresholds, and a one-way sensitivity chart that shows whether the preferred strategy is stable as any chosen input varies.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Clinical inputs: probabilities per arm
        """
    )
    return


@app.cell
def _(mo):
    bio_full = mo.ui.slider(start=0.0, stop=1.0, step=0.05, value=0.40, label="Biologic: P(full response)", show_value=True)
    bio_partial = mo.ui.slider(start=0.0, stop=1.0, step=0.05, value=0.35, label="Biologic: P(partial response)", show_value=True)
    bio_no = mo.ui.slider(start=0.0, stop=1.0, step=0.05, value=0.20, label="Biologic: P(no response)", show_value=True)
    bio_sae = mo.ui.slider(start=0.0, stop=0.20, step=0.01, value=0.05, label="Biologic: P(serious adverse event)", show_value=True)
    mo.vstack([bio_full, bio_partial, bio_no, bio_sae])
    return bio_full, bio_no, bio_partial, bio_sae


@app.cell
def _(mo):
    cs_full = mo.ui.slider(start=0.0, stop=1.0, step=0.05, value=0.20, label="csDMARD: P(full response)", show_value=True)
    cs_partial = mo.ui.slider(start=0.0, stop=1.0, step=0.05, value=0.40, label="csDMARD: P(partial response)", show_value=True)
    cs_no = mo.ui.slider(start=0.0, stop=1.0, step=0.05, value=0.38, label="csDMARD: P(no response)", show_value=True)
    cs_sae = mo.ui.slider(start=0.0, stop=0.20, step=0.01, value=0.02, label="csDMARD: P(serious adverse event)", show_value=True)
    mo.vstack([cs_full, cs_partial, cs_no, cs_sae])
    return cs_full, cs_no, cs_partial, cs_sae


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Utility and cost inputs
        """
    )
    return


@app.cell
def _(mo):
    u_full = mo.ui.slider(start=0.5, stop=1.0, step=0.01, value=0.90, label="Utility of full response", show_value=True)
    u_partial = mo.ui.slider(start=0.3, stop=0.9, step=0.01, value=0.70, label="Utility of partial response", show_value=True)
    u_no = mo.ui.slider(start=0.2, stop=0.8, step=0.01, value=0.50, label="Utility of no response", show_value=True)
    u_sae = mo.ui.slider(start=0.0, stop=0.6, step=0.01, value=0.20, label="Utility of serious adverse event", show_value=True)
    mo.vstack([u_full, u_partial, u_no, u_sae])
    return u_full, u_no, u_partial, u_sae


@app.cell
def _(mo):
    cost_bio = mo.ui.slider(start=10000, stop=40000, step=1000, value=25000, label="Biologic arm: annual cost (USD)", show_value=True)
    cost_cs = mo.ui.slider(start=1500, stop=8000, step=500, value=3500, label="csDMARD arm: annual cost (USD)", show_value=True)
    mo.vstack([cost_bio, cost_cs])
    return cost_bio, cost_cs


@app.cell
def _(
    Decision,
    Outcome,
    bio_full,
    bio_no,
    bio_partial,
    bio_sae,
    cost_bio,
    cost_cs,
    cs_full,
    cs_no,
    cs_partial,
    cs_sae,
    u_full,
    u_no,
    u_partial,
    u_sae,
):
    bio_arm = Decision(label="Add adalimumab (biologic)", annual_cost=float(cost_bio.value))
    bio_arm.outcomes = [
        Outcome("Full response", bio_full.value, u_full.value),
        Outcome("Partial response", bio_partial.value, u_partial.value),
        Outcome("No response", bio_no.value, u_no.value),
        Outcome("Serious adverse event", bio_sae.value, u_sae.value),
    ]
    cs_arm = Decision(label="Continue csDMARD monotherapy", annual_cost=float(cost_cs.value))
    cs_arm.outcomes = [
        Outcome("Full response", cs_full.value, u_full.value),
        Outcome("Partial response", cs_partial.value, u_partial.value),
        Outcome("No response", cs_no.value, u_no.value),
        Outcome("Serious adverse event", cs_sae.value, u_sae.value),
    ]
    return bio_arm, cs_arm


@app.cell
def _(bio_arm, cs_arm, mo, pd):
    arms_table = pd.DataFrame(
        [
            {"Arm": bio_arm.label, "Expected utility (QALYs / year)": round(bio_arm.expected_value(), 3), "Annual cost (USD)": int(bio_arm.annual_cost)},
            {"Arm": cs_arm.label, "Expected utility (QALYs / year)": round(cs_arm.expected_value(), 3), "Annual cost (USD)": int(cs_arm.annual_cost)},
        ]
    )
    arms_table.index = range(1, len(arms_table) + 1)
    arms_table.index.name = "row"
    mo.vstack([mo.md("### Per-arm summary"), arms_table])
    return (arms_table,)


@app.cell
def _(bio_arm, cs_arm, mo):
    delta_cost = bio_arm.annual_cost - cs_arm.annual_cost
    delta_qaly = bio_arm.expected_value() - cs_arm.expected_value()
    if delta_qaly > 0:
        icer = delta_cost / delta_qaly
        icer_str = f"${icer:,.0f} per QALY gained"
    elif delta_qaly < 0:
        icer = delta_cost / delta_qaly
        icer_str = f"${icer:,.0f} per QALY (biologic loses QALYs; csDMARD dominates if delta_cost is positive)"
    else:
        icer = float("inf")
        icer_str = "undefined (no QALY difference)"

    if delta_qaly > 0:
        v50 = "cost-effective" if icer < 50_000 else "not cost-effective"
        v100 = "cost-effective" if icer < 100_000 else "not cost-effective"
        v150 = "cost-effective" if icer < 150_000 else "not cost-effective"
    else:
        v50 = v100 = v150 = "biologic is dominated or trivially preferred; ICER framing does not apply"

    mo.md(
        f"""
        ### ICER and cost-effectiveness verdict

        - Incremental cost (biologic vs csDMARD): **${delta_cost:,.0f}**
        - Incremental QALYs: **{delta_qaly:.3f}**
        - **ICER**: {icer_str}

        Cost-effectiveness verdict at three WTP thresholds:

        | WTP threshold | Verdict |
        |---|---|
        | $50,000 / QALY | **{v50}** |
        | $100,000 / QALY | **{v100}** |
        | $150,000 / QALY | **{v150}** |
        """
    )
    return delta_cost, delta_qaly, icer, icer_str, v100, v150, v50


@app.cell
def _(mo):
    mo.md(
        r"""
        ## One-way sensitivity sweep

        Pick which input to vary. The chart sweeps that input across its plausible range while holding every other input fixed at its current slider value. The two expected-utility curves show how the comparison shifts; the cross-over annotation (when present) marks the value at which the preferred strategy flips.
        """
    )
    return


@app.cell
def _(mo):
    sweep_target = mo.ui.dropdown(
        options=[
            "Biologic: P(full response)",
            "Biologic: P(serious adverse event)",
            "csDMARD: P(full response)",
            "Utility of full response",
            "Utility of no response",
        ],
        value="Biologic: P(full response)",
        label="Vary this input across its plausible range",
    )
    sweep_target
    return (sweep_target,)


@app.cell
def _(
    Decision,
    Outcome,
    bio_arm,
    bio_no,
    bio_partial,
    bio_sae,
    cs_arm,
    cs_full,
    cs_no,
    cs_partial,
    cs_sae,
    np,
    pd,
    sweep_target,
    u_full,
    u_no,
    u_partial,
    u_sae,
):
    target = sweep_target.value
    if target == "Biologic: P(full response)":
        grid = np.linspace(0.05, 0.95, 91)
        x_label = "Biologic: P(full response)"
    elif target == "Biologic: P(serious adverse event)":
        grid = np.linspace(0.0, 0.20, 81)
        x_label = "Biologic: P(serious adverse event)"
    elif target == "csDMARD: P(full response)":
        grid = np.linspace(0.05, 0.60, 56)
        x_label = "csDMARD: P(full response)"
    elif target == "Utility of full response":
        grid = np.linspace(0.5, 1.0, 51)
        x_label = "Utility of full response"
    else:
        grid = np.linspace(0.2, 0.8, 61)
        x_label = "Utility of no response"

    sweep_rows = []
    for v in grid:
        if target == "Biologic: P(full response)":
            b_outs = [
                Outcome("Full response", float(v), u_full.value),
                Outcome("Partial response", bio_partial.value, u_partial.value),
                Outcome("No response", bio_no.value, u_no.value),
                Outcome("Serious adverse event", bio_sae.value, u_sae.value),
            ]
            c_outs = list(cs_arm.outcomes)
        elif target == "Biologic: P(serious adverse event)":
            b_outs = [
                Outcome("Full response", bio_arm.outcomes[0].probability, u_full.value),
                Outcome("Partial response", bio_partial.value, u_partial.value),
                Outcome("No response", bio_no.value, u_no.value),
                Outcome("Serious adverse event", float(v), u_sae.value),
            ]
            c_outs = list(cs_arm.outcomes)
        elif target == "csDMARD: P(full response)":
            b_outs = list(bio_arm.outcomes)
            c_outs = [
                Outcome("Full response", float(v), u_full.value),
                Outcome("Partial response", cs_partial.value, u_partial.value),
                Outcome("No response", cs_no.value, u_no.value),
                Outcome("Serious adverse event", cs_sae.value, u_sae.value),
            ]
        elif target == "Utility of full response":
            b_outs = [
                Outcome("Full response", bio_arm.outcomes[0].probability, float(v)),
                Outcome("Partial response", bio_partial.value, u_partial.value),
                Outcome("No response", bio_no.value, u_no.value),
                Outcome("Serious adverse event", bio_sae.value, u_sae.value),
            ]
            c_outs = [
                Outcome("Full response", cs_full.value, float(v)),
                Outcome("Partial response", cs_partial.value, u_partial.value),
                Outcome("No response", cs_no.value, u_no.value),
                Outcome("Serious adverse event", cs_sae.value, u_sae.value),
            ]
        else:
            b_outs = [
                Outcome("Full response", bio_arm.outcomes[0].probability, u_full.value),
                Outcome("Partial response", bio_partial.value, u_partial.value),
                Outcome("No response", bio_no.value, float(v)),
                Outcome("Serious adverse event", bio_sae.value, u_sae.value),
            ]
            c_outs = [
                Outcome("Full response", cs_full.value, u_full.value),
                Outcome("Partial response", cs_partial.value, u_partial.value),
                Outcome("No response", cs_no.value, float(v)),
                Outcome("Serious adverse event", cs_sae.value, u_sae.value),
            ]
        b_arm = Decision(label="Biologic", annual_cost=bio_arm.annual_cost)
        b_arm.outcomes = b_outs
        c_arm = Decision(label="csDMARD", annual_cost=cs_arm.annual_cost)
        c_arm.outcomes = c_outs
        sweep_rows.append({"input": float(v), "arm": "Biologic", "expected_utility": b_arm.expected_value()})
        sweep_rows.append({"input": float(v), "arm": "csDMARD", "expected_utility": c_arm.expected_value()})
    sweep_df = pd.DataFrame(sweep_rows)
    return c_outs, b_outs, b_arm, c_arm, grid, sweep_df, sweep_rows, target, v, x_label


@app.cell
def _(alt, sweep_df, x_label):
    sensitivity_chart = (
        alt.Chart(sweep_df).mark_line().encode(
            x=alt.X("input:Q", title=x_label),
            y=alt.Y("expected_utility:Q", title="Expected utility (QALYs / year)"),
            color=alt.Color("arm:N", title=""),
            tooltip=["input:Q", "arm:N", "expected_utility:Q"],
        ).properties(width=580, height=320, title=f"One-way sensitivity: expected utility as {x_label} varies")
    )
    sensitivity_chart
    return (sensitivity_chart,)


@app.cell
def _(mo, sweep_df, x_label):
    pivot = sweep_df.pivot(index="input", columns="arm", values="expected_utility").reset_index()
    pivot["diff"] = pivot["Biologic"] - pivot["csDMARD"]
    pivot["sign"] = pivot["diff"].apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
    sign_changes = pivot["sign"].diff().fillna(0) != 0
    crossover = pivot.loc[sign_changes, "input"]
    if len(crossover) > 0:
        cross_val = float(crossover.iloc[0])
        text = f"**Cross-over point.** The two expected-utility curves cross at {x_label} approximately equal to **{cross_val:.3f}**. Below this value, one arm is preferred; above it, the other. The cross-over point is the answer to 'how confident do we need to be about this input before the recommendation is determined?'"
    else:
        text = f"**No cross-over.** Across the swept range of {x_label}, the same arm dominates throughout. The preferred strategy is robust to one-way variation in this input."
    mo.callout(mo.md(text), kind="info")
    return cross_val, crossover, pivot, sign_changes, text


@app.cell
def _(mo):
    mo.md(
        r"""
        ## How to use the artifact

        Three operational guidelines for taking this kind of decision-analytic output to a P&T or formulary committee.

        First, report the headline ICER, the WTP-threshold verdicts, and at least one informative sensitivity chart. The committee needs to see whether the recommendation is robust; an ICER reported without sensitivity is incomplete.

        Second, identify the inputs the committee is most uncertain about and run the sensitivity chart on those. The point of one-way sensitivity is to surface where the committee's clinical judgment most affects the result; the most-uncertain inputs are the ones to chart.

        Third, document the input sources. The credibility of the decision-analytic output is the credibility of the inputs. A model with industry-funded effectiveness inputs, expert-opinion utilities, and chargemaster-derived costs has different standing than one with meta-analytic effectiveness, EQ-5D-derived utilities, and allowed-amount costs. The committee should see the input provenance, not just the headline.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Reflection

        Two reflection questions for the reader. There is no reveal; writing the answers is the work.
        """
    )
    return


@app.cell
def _(mo):
    refl_threshold = mo.ui.text_area(
        label="1. The cost-effectiveness verdicts at $50K, $100K, and $150K above are different. Which threshold would you use to drive a formulary recommendation at your institution, and what factors determine that choice (payer mix, equity considerations, institutional history)?",
        rows=4,
        full_width=True,
        placeholder="Think about the local context that shapes the threshold decision.",
    )
    refl_uncertainty = mo.ui.text_area(
        label="2. Which input above are you least certain about? If you ran a probabilistic sensitivity analysis (sampling all inputs from their distributions), would you expect the cost-effectiveness conclusion to change?",
        rows=4,
        full_width=True,
        placeholder="Identify the input that most determines the result.",
    )
    mo.vstack([
        refl_threshold,
        refl_uncertainty,
        mo.callout(
            mo.md("_There is no answer key. The reflection is the work._"),
            kind="neutral",
        ),
    ])
    return refl_threshold, refl_uncertainty


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            ### Go deeper

            The Detsky et al. *Primer on Medical Decision Analysis* series in Medical Decision Making and Hunink et al. *Decision Making in Health and Medicine* (linked from the Track 03 go-deeper) are the standard references for decision-tree construction at the level this capstone exercises. The CHEERS reporting checklist (linked from the Track 04 go-deeper) is the operational appraisal framework for the full cost-effectiveness analysis the capstone implicitly performs. The ICER (Institute for Clinical and Economic Review) published value-assessment reports are real-world worked examples of the same kind of analysis applied to specific clinical decisions.
            """
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        The capstone assembled the decision-analytic frame of Track 03, the cost-effectiveness machinery of Track 04, and the sensitivity-analysis discipline of both into a reactive end-to-end exercise on the biologic-vs-csDMARD choice. The reader produced an ICER, a cost-effectiveness verdict at three WTP thresholds, and a one-way sensitivity chart for any chosen input, with a cross-over point flagged when the preferred strategy shifts. The artifact is the kind of decision-analytic output a P&T or formulary committee would actually use; the operational guidelines above describe how to take it to that committee.

        Course 11 closes here. Course 12 (Clinical decision support) takes up the operational form of every decision the capstone surfaced: how to wire a decision into the EHR as a CDS alert that fires at a chosen threshold.
        """
    )
    return


if __name__ == "__main__":
    app.run()
