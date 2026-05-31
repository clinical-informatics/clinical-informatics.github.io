"""Track 05: Decision curve analysis.

DCA is the chart that closes the threshold question Course 04 Track 3
(sensitivity, specificity, PPV) and Course 09 Track 3 (discrimination,
calibration) both opened. DCA asks: at the probability threshold a
clinician would act on, does using this model produce more net benefit
than the two trivial alternatives (treat everyone, treat no one)? The
track defines net benefit, derives the three-curve plot, applies it to a
synthetic RA flare-prediction model, and connects DCA forward to the CDS
course. The DCA helpers are inlined per the WASM rule.
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

    # DCA helpers inlined per WASM rule 1 against shared.X imports.
    def net_benefit_at_threshold(y_true, y_prob, threshold):
        y_true_arr = np.asarray(y_true).astype(int)
        y_prob_arr = np.asarray(y_prob).astype(float)
        n = len(y_true_arr)
        if n == 0 or threshold >= 1.0:
            return 0.0
        predicted_positive = y_prob_arr >= threshold
        tp = int(np.sum(predicted_positive & (y_true_arr == 1)))
        fp = int(np.sum(predicted_positive & (y_true_arr == 0)))
        weight = threshold / (1.0 - threshold)
        return (tp / n) - (fp / n) * weight

    def net_benefit_treat_all(y_true, threshold):
        y_true_arr = np.asarray(y_true).astype(int)
        n = len(y_true_arr)
        if n == 0 or threshold >= 1.0:
            return 0.0
        prevalence = float(np.mean(y_true_arr))
        weight = threshold / (1.0 - threshold)
        return prevalence - (1 - prevalence) * weight

    def dca_data(y_true, y_prob, thresholds=None):
        if thresholds is None:
            thresholds = np.linspace(0.01, 0.99, 99)
        records = []
        for t in thresholds:
            records.append({
                "threshold": float(t),
                "model": net_benefit_at_threshold(y_true, y_prob, float(t)),
                "treat_all": net_benefit_treat_all(y_true, float(t)),
                "treat_none": 0.0,
            })
        return pd.DataFrame(records)

    return alt, dca_data, mo, net_benefit_at_threshold, net_benefit_treat_all, np, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 05: Decision curve analysis

        ## The question DCA answers

        A clinical prediction model produces a probability. A clinical decision support rule fires when the probability crosses a chosen threshold. The threshold is the load-bearing parameter; the model's discrimination (Course 04 Track 3, Course 09 Track 3) and calibration (Course 09 Track 3) are necessary but not sufficient to answer the operational question: at the threshold a clinician would actually act on, does using the model produce more clinical benefit than the two trivial alternatives (treat everyone, treat no one)?

        Decision curve analysis is the chart that answers this question. It takes a model's predictions on a held-out cohort, computes a single net-benefit number for each candidate threshold across all three strategies (use the model, treat all, treat none), and plots all three curves on one axis. The model is useful at threshold t if its curve is above both alternatives at t.

        The track defines net benefit, derives the three-curve construction, applies it to a synthetic RA flare-prediction model, and connects DCA forward to the operational question the CDS course (Course 12) takes up.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Net benefit

        Net benefit at threshold t is defined as

        $$
        \text{NB}(t) = \frac{\text{TP}}{n} - \frac{\text{FP}}{n} \cdot \frac{t}{1 - t}
        $$

        where TP and FP are the counts of true and false positives at threshold t and n is the cohort size. The first term is the rate of true positives the model catches at this threshold. The second term penalizes the false positives by a weight that reflects how harmful a false positive is relative to a true positive at this threshold.

        The weight (the t / (1 - t) factor) is the load-bearing trick of DCA. It encodes the clinician's implicit harm-benefit ratio: a clinician who chooses to act at threshold t is, by that choice, accepting that the harm of acting on a non-disease patient is no greater than t / (1 - t) times the benefit of acting on a disease patient. At t = 0.10 the weight is 0.11 (false positives are nearly free); at t = 0.50 the weight is 1.0 (false positives cost as much as true positives are worth); at t = 0.80 the weight is 4.0 (false positives are very expensive). DCA uses each threshold's own implicit harm-benefit ratio to score the model, the treat-all strategy, and the treat-none strategy on a common scale.

        Two trivial strategies anchor the chart.

        - **Treat none.** Net benefit is identically 0 at every threshold. No true positives caught, no false positives produced.
        - **Treat all.** Net benefit is `prevalence - (1 - prevalence) * (t / (1 - t))`. Acts as the upper baseline at low thresholds (when the harm of false positives is small) and drops below zero at high thresholds (when false positives become prohibitively expensive).

        A useful model has a net-benefit curve that is above both trivial alternatives at the threshold a clinician would actually use.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A worked example: a synthetic RA flare-prediction model

        The cohort below is a 1,000-patient synthetic dataset with a binary outcome (flare in the next 90 days). The flare prevalence is 25%. The synthetic model has good discrimination (AUC approximately 0.85). The DCA chart below shows the three curves; the slider lets the reader explore the model's behavior at any threshold.
        """
    )
    return


@app.cell
def _(np):
    rng = np.random.default_rng(seed=20260530)
    n_cohort = 1000
    flare_prevalence = 0.25
    n_flare = int(round(n_cohort * flare_prevalence))
    n_noflare = n_cohort - n_flare

    flare_scores = np.clip(rng.beta(a=5, b=4, size=n_flare), 0.01, 0.99)
    noflare_scores = np.clip(rng.beta(a=2.5, b=6, size=n_noflare), 0.01, 0.99)
    y_true = np.concatenate([np.ones(n_flare, dtype=int), np.zeros(n_noflare, dtype=int)])
    y_prob = np.concatenate([flare_scores, noflare_scores])
    return (
        flare_prevalence,
        flare_scores,
        n_cohort,
        n_flare,
        n_noflare,
        noflare_scores,
        rng,
        y_prob,
        y_true,
    )


@app.cell
def _(alt, dca_data, pd, y_prob, y_true):
    dca_df = dca_data(y_true, y_prob)
    long = dca_df.melt(
        id_vars="threshold",
        value_vars=["model", "treat_all", "treat_none"],
        var_name="strategy",
        value_name="net_benefit",
    )
    long["strategy"] = long["strategy"].map({
        "model": "Use the model",
        "treat_all": "Treat everyone",
        "treat_none": "Treat no one",
    })

    dca_chart = (
        alt.Chart(long).mark_line().encode(
            x=alt.X("threshold:Q", title="Threshold probability"),
            y=alt.Y(
                "net_benefit:Q",
                title="Net benefit",
                scale=alt.Scale(domain=[-0.05, 0.30]),
            ),
            color=alt.Color("strategy:N", title=""),
            tooltip=["threshold:Q", "strategy:N", "net_benefit:Q"],
        ).properties(width=580, height=320, title="Decision curve analysis: RA flare prediction (1,000-patient cohort)")
    )
    _ = pd
    dca_chart
    return dca_chart, dca_df, long


@app.cell
def _(dca_df, mo):
    win_mask = dca_df["model"] > dca_df[["treat_all", "treat_none"]].max(axis=1)
    if win_mask.any():
        lo = float(dca_df.loc[win_mask, "threshold"].min())
        hi = float(dca_df.loc[win_mask, "threshold"].max())
        chart_text = f"The model produces more net benefit than either trivial alternative across thresholds from approximately **{lo:.0%}** to **{hi:.0%}**. Inside this range, using the model is preferred to either treating everyone or treating no one. Outside this range, the trivial alternative (treat-all on the low end, treat-none on the high end) is at least as good as the model."
    else:
        chart_text = "The model does not produce more net benefit than the better trivial alternative at any threshold shown. The model is not adding value over the trivial strategies."
    mo.callout(mo.md(chart_text), kind="info")
    return chart_text, hi, lo, win_mask


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Reactive threshold inspection

        The slider below sets a single threshold; the chart and the per-threshold net-benefit table report what the model would do at that threshold compared to the two trivial alternatives.
        """
    )
    return


@app.cell
def _(mo):
    threshold_slider = mo.ui.slider(start=0.05, stop=0.95, step=0.01, value=0.30, label="Threshold probability", show_value=True)
    threshold_slider
    return (threshold_slider,)


@app.cell
def _(net_benefit_at_threshold, net_benefit_treat_all, pd, threshold_slider, y_prob, y_true):
    t = float(threshold_slider.value)
    nb_model = net_benefit_at_threshold(y_true, y_prob, t)
    nb_all = net_benefit_treat_all(y_true, t)
    nb_none = 0.0
    decision_table = pd.DataFrame(
        [
            {"Strategy": "Use the model (act if probability >= threshold)", "Net benefit": round(nb_model, 4)},
            {"Strategy": "Treat everyone", "Net benefit": round(nb_all, 4)},
            {"Strategy": "Treat no one", "Net benefit": round(nb_none, 4)},
        ]
    )
    decision_table.index = range(1, len(decision_table) + 1)
    return decision_table, nb_all, nb_model, nb_none, t


@app.cell
def _(decision_table):
    decision_table
    return


@app.cell
def _(mo, nb_all, nb_model, nb_none, t):
    best_label, best_value = max(
        [("model", nb_model), ("treat_all", nb_all), ("treat_none", nb_none)],
        key=lambda pair: pair[1],
    )
    pretty = {"model": "the model", "treat_all": "treating everyone", "treat_none": "treating no one"}[best_label]
    mo.callout(
        mo.md(
            f"At a threshold of **{t:.2f}**, the highest net benefit comes from **{pretty}** (NB = {best_value:.4f}). This is the strategy a payer or a CDS-design committee operating at exactly this threshold should adopt."
        ),
        kind="success",
    )
    return best_label, best_value, pretty


@app.cell
def _(mo):
    mo.md(
        r"""
        ## How to read a DCA chart

        Two operational rules.

        First, identify the threshold range a clinician would actually use. A flare-prediction model that would fire a CDS alert at a 30% probability is operating around threshold 0.30; only the DCA behavior in the vicinity of 0.30 is clinically relevant. DCA over the full 0 to 1 range is informative but the interpretation should center on the operating range.

        Second, compare the model's curve against the higher of the two trivial alternatives at that threshold. The model has to beat the better trivial alternative to add value; beating only the worse alternative is not enough. At low thresholds (under 0.15 in many clinical settings), treat-all is often the strong alternative; at high thresholds, treat-none becomes strong. The model has to clear the higher of the two at the operating threshold to justify deployment.

        DCA does not by itself say whether the model should be deployed. It says whether the model adds value over the trivial alternatives at the threshold the deployment would use. The deployment decision still requires the workflow, equity, and operational considerations Course 12 takes up.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "11",
        "04",
        "Sensitivity, specificity, PPV at a threshold",
        "Course 04 Track 3 introduced the 2x2 table and the ROC curve. DCA is the unified framework that takes a chosen threshold (the implicit harm-benefit ratio) and converts the 2x2 counts into a single comparable net-benefit number. The model's ROC curve summarizes its discrimination across all thresholds; the DCA chart summarizes its clinical value across all thresholds.",
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "11",
        "09",
        "Calibration and the meaning of the threshold",
        "Course 09 Track 3 introduced the discrimination-vs-calibration distinction. DCA requires calibrated probabilities to be interpreted at face value: an alert that fires at threshold 0.30 is meaningful only if the patients flagged actually have outcome rates near 30%. A miscalibrated model's DCA chart is itself uninterpretable; calibrate the model first, then apply DCA.",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "11",
        "12",
        "DCA as the operational threshold question for CDS",
        "Course 12 (Clinical Decision Support) takes up the operational question of what threshold to set when wiring a model into the EHR as an alert. DCA is the analytic engine of that question: the threshold that maximizes net benefit on a held-out cohort is the threshold the CDS rule should fire at, subject to the workflow, equity, and override-rate considerations Course 12 covers.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        Decision curve analysis is the chart that closes the threshold question Course 04 Track 3 and Course 09 Track 3 both opened. Net benefit at a threshold uses the threshold itself as the implicit harm-benefit weight, allowing the model, the treat-all strategy, and the treat-none strategy to be scored on a common scale. The model is useful at threshold t if its curve is above both trivial alternatives at t. The worked example showed an RA flare-prediction model adding net benefit across a range of clinically realistic thresholds (approximately 5% to 60%) and falling below the trivial alternatives at very low and very high thresholds. DCA requires calibrated probabilities and complements but does not replace the workflow, equity, and operational considerations of CDS deployment.

        Track 06 takes up the broader question of reading outcomes data critically: the value-based-care vocabulary, the common confounders in health-economics research, and the CHEERS checklist as the appraisal framework for any cost-effectiveness paper.
        """
    )
    return


if __name__ == "__main__":
    app.run()
