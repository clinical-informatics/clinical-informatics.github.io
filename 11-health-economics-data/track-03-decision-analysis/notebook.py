"""Track 03: Decision analysis.

A decision tree is two things at once: a picture of a clinical choice and a
math object that computes expected value per arm. The track defines both,
presents the biologic-vs-csDMARD choice for a patient like Ms. Reyes,
lets the reader move probability sliders and watch the expected values
move, and introduces one-way sensitivity analysis as the stability check.
The decision-tree dataclasses are inlined per the WASM rule against
shared.X imports.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import types
    from dataclasses import dataclass, field

    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd

    _COURSE_TITLES = {
        "01": "Computational thinking",
        "04": "Clinical epidemiology",
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

    # Decision-tree dataclasses inlined per WASM rule 1 against shared.X imports.
    @dataclass
    class Outcome:
        label: str
        probability: float
        utility: float

    @dataclass
    class Decision:
        label: str
        outcomes: list = field(default_factory=list)

        def expected_value(self):
            total_p = sum(o.probability for o in self.outcomes)
            if total_p <= 0:
                return 0.0
            return sum(o.probability * o.utility for o in self.outcomes) / total_p

    @dataclass
    class Tree:
        question: str
        decisions: list = field(default_factory=list)

        def add(self, decision):
            self.decisions.append(decision)
            return self

        def best(self):
            if not self.decisions:
                return None
            return max(self.decisions, key=lambda d: d.expected_value())

    return Decision, Outcome, Tree, alt, mo, np, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 03: Decision analysis

        ## A decision tree is a picture and math at once

        A decision tree represents a clinical choice as a structured object. The structure has three kinds of node. A decision node names the choice the clinician is making (biologic vs csDMARD, treat vs watch, admit vs send home). A chance node names a probabilistic outcome that follows from a decision (clinical response, partial response, no response, serious adverse event). A terminal node assigns a numerical value (utility, QALY, cost) to each outcome.

        The structure is at once a picture (a clinician can draw the tree on a whiteboard and trace each path with a colleague) and a math object (the expected value of each decision is the probability-weighted sum of the utilities of its outcomes). The picture supports clinical reasoning; the math object supports the comparison.

        The track defines both, applies them to the biologic-vs-csDMARD decision for a patient like Ms. Reyes, lets the reader move reactive probability sliders, and introduces one-way sensitivity analysis as the question of how stable the preferred strategy is under variation in any single probability.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The worked decision: biologic add vs csDMARD continuation

        Ms. Reyes, at her 2024-05-15 visit, had a DAS28 of 4.1 despite a year on MTX at 25 mg weekly. Her rheumatologist faced the canonical RA-treatment-escalation decision: add adalimumab (a TNF-inhibitor biologic), or continue csDMARD monotherapy with closer follow-up.

        The decision tree below structures the choice. Each arm has four outcomes (full response, partial response, no response, serious adverse event). Each outcome carries a probability (how likely is this outcome on this treatment?) and a utility (how desirable is this outcome on a 0 to 1 scale).

        The probabilities below come from a representative reading of the published RA-treatment literature. The utilities are illustrative, in the EQ-5D-derived range typical of RA cost-effectiveness studies.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Set the probabilities

        Move the sliders to change the probability of each outcome on each arm. The probabilities on each arm should sum to 1.0; if they do not, the expected-value calculation normalizes by the sum.
        """
    )
    return


@app.cell
def _(mo):
    bio_full_p = mo.ui.slider(start=0.0, stop=1.0, step=0.05, value=0.40, label="Biologic: probability of full response", show_value=True)
    bio_partial_p = mo.ui.slider(start=0.0, stop=1.0, step=0.05, value=0.35, label="Biologic: probability of partial response", show_value=True)
    bio_noresp_p = mo.ui.slider(start=0.0, stop=1.0, step=0.05, value=0.20, label="Biologic: probability of no response", show_value=True)
    bio_sae_p = mo.ui.slider(start=0.0, stop=0.20, step=0.01, value=0.05, label="Biologic: probability of serious adverse event", show_value=True)
    mo.vstack([
        mo.md("**Biologic arm probabilities**"),
        bio_full_p, bio_partial_p, bio_noresp_p, bio_sae_p,
    ])
    return bio_full_p, bio_noresp_p, bio_partial_p, bio_sae_p


@app.cell
def _(mo):
    cs_full_p = mo.ui.slider(start=0.0, stop=1.0, step=0.05, value=0.20, label="csDMARD: probability of full response", show_value=True)
    cs_partial_p = mo.ui.slider(start=0.0, stop=1.0, step=0.05, value=0.40, label="csDMARD: probability of partial response", show_value=True)
    cs_noresp_p = mo.ui.slider(start=0.0, stop=1.0, step=0.05, value=0.38, label="csDMARD: probability of no response", show_value=True)
    cs_sae_p = mo.ui.slider(start=0.0, stop=0.20, step=0.01, value=0.02, label="csDMARD: probability of serious adverse event", show_value=True)
    mo.vstack([
        mo.md("**csDMARD-continuation arm probabilities**"),
        cs_full_p, cs_partial_p, cs_noresp_p, cs_sae_p,
    ])
    return cs_full_p, cs_noresp_p, cs_partial_p, cs_sae_p


@app.cell
def _(mo):
    util_full = mo.ui.slider(start=0.5, stop=1.0, step=0.01, value=0.90, label="Utility of full response", show_value=True)
    util_partial = mo.ui.slider(start=0.3, stop=0.9, step=0.01, value=0.70, label="Utility of partial response", show_value=True)
    util_noresp = mo.ui.slider(start=0.2, stop=0.8, step=0.01, value=0.50, label="Utility of no response", show_value=True)
    util_sae = mo.ui.slider(start=0.0, stop=0.6, step=0.01, value=0.20, label="Utility of serious adverse event", show_value=True)
    mo.vstack([
        mo.md("**Utilities (0 = death, 1 = perfect health)**"),
        util_full, util_partial, util_noresp, util_sae,
    ])
    return util_full, util_noresp, util_partial, util_sae


@app.cell
def _(
    Decision,
    Outcome,
    Tree,
    bio_full_p,
    bio_noresp_p,
    bio_partial_p,
    bio_sae_p,
    cs_full_p,
    cs_noresp_p,
    cs_partial_p,
    cs_sae_p,
    util_full,
    util_noresp,
    util_partial,
    util_sae,
):
    tree = Tree("Add adalimumab vs continue csDMARD for an RA patient with DAS28 4.1 on MTX alone?")
    biologic = Decision("Add adalimumab (biologic)")
    biologic.outcomes = [
        Outcome("Full response", bio_full_p.value, util_full.value),
        Outcome("Partial response", bio_partial_p.value, util_partial.value),
        Outcome("No response", bio_noresp_p.value, util_noresp.value),
        Outcome("Serious adverse event", bio_sae_p.value, util_sae.value),
    ]
    csdmard = Decision("Continue csDMARD monotherapy")
    csdmard.outcomes = [
        Outcome("Full response", cs_full_p.value, util_full.value),
        Outcome("Partial response", cs_partial_p.value, util_partial.value),
        Outcome("No response", cs_noresp_p.value, util_noresp.value),
        Outcome("Serious adverse event", cs_sae_p.value, util_sae.value),
    ]
    tree.add(biologic).add(csdmard)
    return biologic, csdmard, tree


@app.cell
def _(pd, tree):
    _rows = []
    for _d in tree.decisions:
        for _o in _d.outcomes:
            _rows.append({
                "decision": _d.label,
                "outcome": _o.label,
                "probability": round(_o.probability, 3),
                "utility": round(_o.utility, 3),
                "contribution": round(_o.probability * _o.utility, 4),
            })
    outcomes_table = pd.DataFrame(_rows)
    outcomes_table.index = range(1, len(outcomes_table) + 1)
    return (outcomes_table,)


@app.cell
def _(outcomes_table):
    outcomes_table
    return


@app.cell
def _(pd, tree):
    _ev_rows = []
    for _d in tree.decisions:
        _p_total = sum(_o.probability for _o in _d.outcomes)
        _ev_rows.append({
            "decision": _d.label,
            "probability_total": round(_p_total, 3),
            "expected_value": round(_d.expected_value(), 4),
        })
    ev_table = pd.DataFrame(_ev_rows)
    ev_table.index = range(1, len(ev_table) + 1)
    return (ev_table,)


@app.cell
def _(ev_table):
    ev_table
    return


@app.cell
def _(mo, tree):
    winner = tree.best()
    if winner is None:
        verdict = mo.callout(mo.md("_No decisions defined yet._"), kind="neutral")
    else:
        loser = next(d for d in tree.decisions if d is not winner)
        gap = winner.expected_value() - loser.expected_value()
        verdict = mo.callout(
            mo.md(
                f"**At these inputs, {winner.label} has the higher expected value ({winner.expected_value():.3f} vs {loser.expected_value():.3f}).** The expected-value gap is {gap:.3f}. This is the value-maximizing choice for a population of patients with these probability and utility inputs; it does not by itself determine the right choice for any individual patient (which depends on the patient's own preferences, comorbidities, and contraindications)."
            ),
            kind="success",
        )
    verdict
    return gap, loser, verdict, winner


@app.cell
def _(mo):
    mo.md(
        r"""
        ## One-way sensitivity analysis

        The expected-value comparison above uses one specific set of probabilities. A real decision-analytic study has to ask how stable the preferred strategy is when any single probability is allowed to vary across its plausible range. This is one-way sensitivity analysis: hold every input fixed at its baseline except one, vary that one across a range, and chart the expected value of each decision as a function of the varied input. If the two expected-value curves cross within the plausible range, the preferred strategy is not stable; if they do not cross, the choice is robust to that input.

        The chart below performs the one-way sensitivity analysis on the probability of full response on the biologic arm. The other probabilities (partial response, no response, SAE on biologic; all four csDMARD outcomes) and all utilities are held at the slider values above.
        """
    )
    return


@app.cell
def _(
    Decision,
    Outcome,
    alt,
    bio_noresp_p,
    bio_partial_p,
    bio_sae_p,
    cs_full_p,
    cs_noresp_p,
    cs_partial_p,
    cs_sae_p,
    np,
    pd,
    util_full,
    util_noresp,
    util_partial,
    util_sae,
):
    full_p_grid = np.linspace(0.05, 0.95, 91)
    sweep_rows = []
    for p in full_p_grid:
        bio_arm = Decision("Add adalimumab (biologic)")
        bio_arm.outcomes = [
            Outcome("Full response", p, util_full.value),
            Outcome("Partial response", bio_partial_p.value, util_partial.value),
            Outcome("No response", bio_noresp_p.value, util_noresp.value),
            Outcome("Serious adverse event", bio_sae_p.value, util_sae.value),
        ]
        cs_arm = Decision("Continue csDMARD monotherapy")
        cs_arm.outcomes = [
            Outcome("Full response", cs_full_p.value, util_full.value),
            Outcome("Partial response", cs_partial_p.value, util_partial.value),
            Outcome("No response", cs_noresp_p.value, util_noresp.value),
            Outcome("Serious adverse event", cs_sae_p.value, util_sae.value),
        ]
        sweep_rows.append({"biologic_full_p": float(p), "decision": "Biologic", "expected_value": bio_arm.expected_value()})
        sweep_rows.append({"biologic_full_p": float(p), "decision": "csDMARD", "expected_value": cs_arm.expected_value()})
    sweep_df = pd.DataFrame(sweep_rows)
    sensitivity_chart = (
        alt.Chart(sweep_df).mark_line().encode(
            x=alt.X("biologic_full_p:Q", title="Biologic: probability of full response"),
            y=alt.Y("expected_value:Q", title="Expected value"),
            color=alt.Color("decision:N", title=""),
            tooltip=["biologic_full_p:Q", "decision:N", "expected_value:Q"],
        ).properties(width=560, height=300, title="One-way sensitivity: expected value as biologic-full-response probability varies")
    )
    sensitivity_chart
    return bio_arm, cs_arm, full_p_grid, p, sensitivity_chart, sweep_df, sweep_rows


@app.cell
def _(mo, sweep_df):
    bio_curve = sweep_df[sweep_df["decision"] == "Biologic"].sort_values("biologic_full_p").reset_index(drop=True)
    cs_curve = sweep_df[sweep_df["decision"] == "csDMARD"].sort_values("biologic_full_p").reset_index(drop=True)
    cs_ev = float(cs_curve["expected_value"].iloc[0])
    diffs = bio_curve["expected_value"] - cs_ev
    sign_changes = ((diffs.shift(1) * diffs) < 0).fillna(False)
    crossover_idx = sign_changes.idxmax() if sign_changes.any() else None
    if crossover_idx is not None and sign_changes.iloc[crossover_idx]:
        crossover_p = float(bio_curve["biologic_full_p"].iloc[crossover_idx])
        text = f"The two expected-value curves cross at a biologic full-response probability of approximately **{crossover_p:.2f}**. Below this value, csDMARD continuation has the higher expected value; above it, the biologic does. The published biologic full-response rate in MTX-inadequate-responder RA cohorts is approximately 0.40 to 0.50, so the biologic-add decision is value-maximizing at the typical clinical inputs."
    else:
        text = "Across the plausible range of biologic full-response probability, the two decisions do not cross. The preferred strategy is stable for this one-way variation."
    mo.callout(mo.md(text), kind="info")
    return bio_curve, crossover_idx, crossover_p, cs_curve, cs_ev, diffs, sign_changes, text


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What one-way sensitivity tells you

        Two things, plus one important limitation.

        First, the one-way sensitivity chart says whether the preferred strategy is stable across the plausible range of a single input. If the two curves do not cross, the choice is robust to that input; if they do, the cross-over point quantifies how much the input would have to change before the recommendation flipped. The cross-over point is the answer to "how confident do we need to be about this probability before the decision is determined?"

        Second, the slope of the difference between the two curves shows how sensitive the comparison is. A large slope means small changes in the input produce large expected-value differences; a small slope means the comparison is insensitive. A flat sensitivity chart is a sign that the decision is robust; a steep one is a sign that the decision depends on the input.

        The limitation: one-way sensitivity holds every other input fixed at its baseline. Real probabilistic decisions involve uncertainty in many inputs simultaneously, which is why the published methods literature also presents two-way sensitivity (vary two inputs jointly), tornado diagrams (rank inputs by their effect on the decision), and probabilistic sensitivity analysis (sample all inputs from their joint distributions and report the proportion of simulations in which each decision wins). All three extend the one-way picture.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "11",
        "01",
        "An algorithm as a procedure with parameters",
        "Course 01 introduced the picture of a clinical decision rule as a procedure with parameters. A decision tree is the same picture extended with explicit probabilities and utilities; the algorithm is now a function of those parameters, and the sensitivity-analysis machinery measures how robust the decision is to parameter variation.",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "11",
        "12",
        "Decision analysis at the CDS-rule level",
        "Course 12 (Clinical Decision Support) takes up the operational form of the same decision-analytic question: a CDS rule that fires at a particular threshold is implicitly making a decision-analytic comparison against the alternative of not firing. The decision-tree and DCA frameworks of this course are the analytic backbone of the CDS-rule design process.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        A decision tree represents a clinical choice as a structured object with decision nodes, chance nodes, and terminal-value assignments. The tree is at once a picture (which supports clinical reasoning) and a math object (which computes expected value per decision). The biologic-vs-csDMARD worked example shows the construction; the reactive sliders make the comparison sensitive to input choices; the one-way sensitivity chart shows whether the preferred strategy is robust. Tornado diagrams, two-way sensitivity, and probabilistic sensitivity analysis extend the one-way picture for higher-stakes decisions.

        Track 04 takes up cost-effectiveness analysis: the same decision-analytic frame extended with cost on one axis and QALYs on the other, with the willingness-to-pay threshold as the comparator that turns the ICER into an actionable decision.
        """
    )
    return


if __name__ == "__main__":
    app.run()
