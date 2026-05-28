"""Track 03: Discrimination vs calibration.

A clinical model has two quality questions and they are independent.
Discrimination asks whether the model ranks high-risk patients above
low-risk patients (summarized by AUC, visualized by the ROC curve).
Calibration asks whether the probabilities the model produces match the
observed event rates at those probabilities (summarized by the Brier
score, visualized by the calibration plot). The track presents an
interactive ROC explorer alongside the calibration plot, then contrasts
two models with the same AUC but very different calibration.
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
        "11": "Health economics data",
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

    # ROC helpers, inlined per the WASM rule against shared.X imports.
    def roc_curve_points(y_true, y_score):
        order = np.argsort(-y_score, kind="stable")
        y_sorted = np.asarray(y_true)[order]
        scores_sorted = np.asarray(y_score)[order]
        positives = float(y_sorted.sum())
        negatives = float(len(y_sorted) - positives)
        tpr_list = [0.0]
        fpr_list = [0.0]
        thr_list = [float(scores_sorted.max()) + 1e-9]
        tp = 0.0
        fp = 0.0
        prev_score = None
        for label, s in zip(y_sorted, scores_sorted):
            if prev_score is not None and s != prev_score:
                tpr_list.append(tp / positives if positives else 0.0)
                fpr_list.append(fp / negatives if negatives else 0.0)
                thr_list.append(float(s))
            if label == 1:
                tp += 1
            else:
                fp += 1
            prev_score = s
        tpr_list.append(tp / positives if positives else 0.0)
        fpr_list.append(fp / negatives if negatives else 0.0)
        thr_list.append(float(scores_sorted.min()) - 1e-9)
        return np.array(fpr_list), np.array(tpr_list), np.array(thr_list)

    def auc_from_roc(fpr, tpr):
        return float(np.trapz(tpr, fpr))

    def two_by_two(y_true, y_score, threshold):
        y_true_arr = np.asarray(y_true).astype(int)
        y_pred = (np.asarray(y_score) >= threshold).astype(int)
        tp = int(((y_pred == 1) & (y_true_arr == 1)).sum())
        fp = int(((y_pred == 1) & (y_true_arr == 0)).sum())
        tn = int(((y_pred == 0) & (y_true_arr == 0)).sum())
        fn = int(((y_pred == 0) & (y_true_arr == 1)).sum())
        sens = tp / (tp + fn) if (tp + fn) else 0.0
        spec = tn / (tn + fp) if (tn + fp) else 0.0
        ppv = tp / (tp + fp) if (tp + fp) else 0.0
        npv = tn / (tn + fn) if (tn + fn) else 0.0
        return {"TP": tp, "FP": fp, "TN": tn, "FN": fn, "sensitivity": sens, "specificity": spec, "PPV": ppv, "NPV": npv}

    def brier_score(y_true, y_prob):
        return float(np.mean((np.asarray(y_prob) - np.asarray(y_true).astype(float)) ** 2))

    def calibration_table(y_true, y_prob, n_bins=10):
        bins = np.linspace(0, 1, n_bins + 1)
        idx = np.clip(np.digitize(y_prob, bins) - 1, 0, n_bins - 1)
        rows = []
        for b in range(n_bins):
            mask = idx == b
            n = int(mask.sum())
            if n == 0:
                continue
            rows.append(
                {
                    "bin": b,
                    "predicted": float(np.mean(np.asarray(y_prob)[mask])),
                    "observed": float(np.mean(np.asarray(y_true)[mask].astype(float))),
                    "n": n,
                }
            )
        return pd.DataFrame(rows)

    return (
        alt,
        auc_from_roc,
        brier_score,
        calibration_table,
        mo,
        np,
        pd,
        roc_curve_points,
        two_by_two,
        xref,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 03: Discrimination vs calibration

        ## Two quality questions, and they are independent

        A trained clinical model has two quality questions and they are independent of one another.

        **Discrimination**: does the model rank the patients who will experience the outcome above the patients who will not? Discrimination is summarized by the area under the ROC curve (AUC) and visualized by the ROC curve itself. It is the question that asks: if I picked two patients at random, one who develops the outcome and one who does not, would the model give the first a higher score?

        **Calibration**: do the probabilities the model produces match the observed event rates among the patients assigned those probabilities? Calibration is summarized by the Brier score and visualized by the calibration plot. It is the question that asks: among all the patients the model gave a 30% probability, did 30% of them actually develop the outcome?

        The two questions are independent. A model can rank patients perfectly (AUC 1.0) and produce wildly miscalibrated probabilities. A model with mediocre discrimination (AUC 0.65) can have excellent calibration. Clinicians act on the probability the model produces, not on the rank, and the calibration question is therefore the one that determines whether the model's outputs are clinically usable.
        """
    )
    return


@app.cell
def _(mo, xref):
    callback = xref.callback(
        "09",
        "04",
        "ROC curve, sensitivity, specificity, PPV, NPV",
        "Course 04 Track 3 introduced the 2x2 table and the ROC curve as the construction for a diagnostic test. The construction here is the same; what changes is that the score is the output of a trained model rather than a single diagnostic test, and the AUC and threshold are the levers a clinical informaticist pulls when adopting a model.",
    )
    callback
    return (callback,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The working dataset and the two models

        The working dataset is a 1,000-patient synthetic RA cohort with a binary outcome ("flare in the next 6 months") and a single underlying risk variable. Two models are evaluated on it.

        - **Model A** produces calibrated probabilities. The probability it outputs for a given patient is close to that patient's true risk.
        - **Model B** produces the same patient ranking as Model A but transforms its probabilities (it squashes high probabilities down and stretches low probabilities up, so most predictions cluster around 0.3 to 0.5 even when the true risk is near 0 or near 1).

        Because the two models produce the same ranking, their AUCs are identical. Because the probabilities differ, the calibration plots and Brier scores diverge.
        """
    )
    return


@app.cell
def _(np, pd):
    n_patients = 1000
    rng = np.random.default_rng(seed=20260528)
    feature = rng.normal(0, 1, n_patients)

    true_logit = -1.2 + 1.8 * feature
    true_risk = 1 / (1 + np.exp(-true_logit))

    outcomes = (rng.uniform(size=n_patients) < true_risk).astype(int)

    model_a_prob = true_risk.copy()

    def squash(p, k=2.5):
        center = 0.4
        return center + (p - center) / k

    model_b_prob = np.clip(squash(true_risk, k=2.5), 0.01, 0.99)

    cohort_df = pd.DataFrame(
        {
            "patient_id": np.arange(1, n_patients + 1),
            "feature": feature,
            "true_risk": true_risk,
            "outcome": outcomes,
            "model_a_probability": model_a_prob,
            "model_b_probability": model_b_prob,
        }
    )
    overall_event_rate = float(outcomes.mean())
    return (
        cohort_df,
        feature,
        model_a_prob,
        model_b_prob,
        n_patients,
        outcomes,
        overall_event_rate,
        rng,
        squash,
        true_logit,
        true_risk,
    )


@app.cell
def _(cohort_df, mo, overall_event_rate):
    mo.md(
        f"""
        Cohort size: **{len(cohort_df)} patients**. Overall observed event rate: **{overall_event_rate:.1%}**. The first few rows below show the two models' probabilities side by side for the same patients.
        """
    )
    return


@app.cell
def _(cohort_df):
    cohort_df.head(8).round(3)
    return


@app.cell
def _(auc_from_roc, model_a_prob, model_b_prob, outcomes, roc_curve_points):
    fpr_a, tpr_a, thr_a = roc_curve_points(outcomes, model_a_prob)
    fpr_b, tpr_b, thr_b = roc_curve_points(outcomes, model_b_prob)
    auc_a = auc_from_roc(fpr_a, tpr_a)
    auc_b = auc_from_roc(fpr_b, tpr_b)
    return auc_a, auc_b, fpr_a, fpr_b, thr_a, thr_b, tpr_a, tpr_b


@app.cell
def _(auc_a, auc_b, mo):
    mo.md(
        f"""
        ### The AUCs are identical

        Model A AUC: **{auc_a:.3f}**. Model B AUC: **{auc_b:.3f}**.

        The ranking is preserved by the monotonic transformation applied to produce Model B, so both models would receive the same score on any discrimination metric. A reviewer who reads only the AUC would conclude the two models are equivalent.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The ROC explorer (Model A)

        The slider below sets the alert threshold on Model A's probability output. The 2x2 table, ROC curve marker, and plain-English summary update reactively. The ROC curve is fixed; the marker moves along it as the threshold changes.
        """
    )
    return


@app.cell
def _(mo):
    threshold_slider = mo.ui.slider(start=0.05, stop=0.95, step=0.01, value=0.30, label="Alert threshold on Model A probability", show_value=True)
    threshold_slider
    return (threshold_slider,)


@app.cell
def _(alt, auc_a, fpr_a, model_a_prob, outcomes, pd, threshold_slider, tpr_a, two_by_two):
    t = float(threshold_slider.value)
    stats_a = two_by_two(outcomes, model_a_prob, t)
    roc_df_a = pd.DataFrame({"fpr": fpr_a, "tpr": tpr_a})
    diag_df = pd.DataFrame({"fpr": [0, 1], "tpr": [0, 1]})
    marker_df_a = pd.DataFrame(
        [{"fpr": 1 - stats_a["specificity"], "tpr": stats_a["sensitivity"]}]
    )
    roc_chart_a = (
        alt.Chart(roc_df_a).mark_line(color="#1f77b4").encode(
            x=alt.X("fpr:Q", title="1 - Specificity (false-positive rate)"),
            y=alt.Y("tpr:Q", title="Sensitivity"),
        )
        + alt.Chart(diag_df).mark_line(strokeDash=[4, 4], color="#888").encode(x="fpr:Q", y="tpr:Q")
        + alt.Chart(marker_df_a).mark_point(size=200, color="red", filled=True).encode(x="fpr:Q", y="tpr:Q")
    ).properties(width=360, height=320, title=f"ROC curve, Model A (AUC = {auc_a:.3f}); red dot is the chosen threshold")
    roc_chart_a
    return diag_df, marker_df_a, roc_chart_a, roc_df_a, stats_a, t


@app.cell
def _(pd, stats_a):
    tbl_a = pd.DataFrame(
        [
            {"": "Test positive", "Flare": stats_a["TP"], "No flare": stats_a["FP"]},
            {"": "Test negative", "Flare": stats_a["FN"], "No flare": stats_a["TN"]},
        ]
    )
    tbl_a
    return (tbl_a,)


@app.cell
def _(mo, stats_a, t):
    interp_a = mo.callout(
        mo.md(
            f"At a threshold of **{t:.2f}**, the model catches **{stats_a['sensitivity']:.0%}** of patients who flare (sensitivity), and correctly clears **{stats_a['specificity']:.0%}** of patients who do not (specificity). Among patients the model labels positive, **{stats_a['PPV']:.0%}** actually flare (PPV). Among patients it labels negative, **{stats_a['NPV']:.0%}** actually do not (NPV)."
        ),
        kind="info",
    )
    interp_a
    return (interp_a,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The calibration plots, side by side

        The two calibration plots below use the same 1,000 patients and the same outcomes. The only difference is the probability the model produces for each patient. Each blue dot is one decile bin of the predicted-probability axis; the y-axis is the observed event rate within that bin.

        Perfect calibration is the dashed diagonal. Points above the diagonal mean the model is under-predicting the outcome at that probability; points below mean it is over-predicting.
        """
    )
    return


@app.cell
def _(
    alt,
    brier_score,
    calibration_table,
    model_a_prob,
    model_b_prob,
    outcomes,
    pd,
):
    cal_a = calibration_table(outcomes, model_a_prob, n_bins=10)
    cal_b = calibration_table(outcomes, model_b_prob, n_bins=10)
    brier_a = brier_score(outcomes, model_a_prob)
    brier_b = brier_score(outcomes, model_b_prob)
    diag = pd.DataFrame({"x": [0, 1], "y": [0, 1]})

    cal_chart_a = (
        alt.Chart(diag).mark_line(strokeDash=[5, 5], color="#888").encode(x="x:Q", y="y:Q")
        + alt.Chart(cal_a).mark_circle(size=140, color="#1f77b4").encode(
            x=alt.X("predicted:Q", title="Predicted probability", scale=alt.Scale(domain=[0, 1])),
            y=alt.Y("observed:Q", title="Observed event rate", scale=alt.Scale(domain=[0, 1])),
            tooltip=["bin:Q", "predicted:Q", "observed:Q", "n:Q"],
        )
    ).properties(width=320, height=320, title=f"Model A calibration (Brier = {brier_a:.3f})")

    cal_chart_b = (
        alt.Chart(diag).mark_line(strokeDash=[5, 5], color="#888").encode(x="x:Q", y="y:Q")
        + alt.Chart(cal_b).mark_circle(size=140, color="#d62728").encode(
            x=alt.X("predicted:Q", title="Predicted probability", scale=alt.Scale(domain=[0, 1])),
            y=alt.Y("observed:Q", title="Observed event rate", scale=alt.Scale(domain=[0, 1])),
            tooltip=["bin:Q", "predicted:Q", "observed:Q", "n:Q"],
        )
    ).properties(width=320, height=320, title=f"Model B calibration (Brier = {brier_b:.3f})")

    cal_side_by_side = alt.hconcat(cal_chart_a, cal_chart_b)
    cal_side_by_side
    return (
        brier_a,
        brier_b,
        cal_a,
        cal_b,
        cal_chart_a,
        cal_chart_b,
        cal_side_by_side,
        diag,
    )


@app.cell
def _(brier_a, brier_b, mo):
    mo.md(
        f"""
        Model A's calibration plot tracks the diagonal closely; the model's stated probabilities match the observed event rates within each bin. Brier score: **{brier_a:.3f}**.

        Model B's calibration plot is compressed toward the middle. The model says 0.40 to the highest-risk patients but those patients flare at 70% or higher; the model also says 0.40 to the lowest-risk patients but those patients flare at 10% or lower. Brier score: **{brier_b:.3f}** (higher is worse).

        The two models have identical AUCs because they rank the patients identically. They produce very different probabilities. A clinician acting on a 0.40 probability from Model B would treat a patient who actually has a 70% risk as if she had a 40% risk; a clinician acting on a 0.40 from Model A would be reading the actual risk correctly.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Why this matters at the bedside

        A clinical decision support alert fires when the model probability crosses a chosen threshold. The threshold is set against the model's stated probability, not against the underlying truth. A miscalibrated model whose stated probabilities are too low will fire fewer alerts than the threshold-setter intended; a miscalibrated model whose stated probabilities are too high will fire more.

        The same is true of risk communication. A patient told "your risk is 30%" by a miscalibrated model is told a number that does not match her actual situation. The patient's downstream decisions (whether to accept a procedure, whether to start a medication, whether to change her behavior) are made on the basis of the number the model produced. If the number is wrong by a factor of two, the downstream decisions are wrong.

        Calibration is the necessary condition for the model output to be a probability in the clinical sense, rather than a score. A model whose output is interpreted as a probability without calibration evidence is being misused.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Calibration-in-the-large vs calibration-in-the-small

        Calibration is reported at two levels.

        **Calibration-in-the-large** is the single comparison between the mean predicted probability and the overall event rate. A model whose mean predicted probability is 0.18 against an actual event rate of 0.30 has poor calibration-in-the-large; it is systematically under-predicting. Calibration-in-the-large can be reported as a single number; it is the standard first check.

        **Calibration-in-the-small** (sometimes called moderate calibration) is the per-bin comparison the calibration plot displays. A model can have perfect calibration-in-the-large (the means agree) and very poor calibration-in-the-small (the model over-predicts at low risk and under-predicts at high risk in equal amounts that cancel out in the mean).

        Both are required for a useful clinical model. Calibration-in-the-large is necessary but not sufficient. The calibration plot is the standard sufficient check; the Brier score summarizes it in one number.
        """
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "09",
        "11",
        "Decision curve analysis closes the threshold question",
        "Course 11 takes up decision curve analysis (DCA). DCA reframes the discrimination-and-calibration question into a single net-benefit chart that shows whether acting on the model at a chosen threshold produces more net benefit than treating everyone, treating no one, or following the standard of care. DCA depends on calibration; a miscalibrated model produces a DCA curve that is itself uninterpretable.",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "09",
        "12",
        "Threshold setting in CDS",
        "Course 12 takes up the operational question of what threshold to set when wiring a model into the EHR as a CDS alert. The threshold determines the firing rate, the override rate, and the workflow impact; the model's calibration determines whether the threshold means what the threshold-setter thinks it means.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        A clinical model has two independent quality questions. Discrimination (does the model rank correctly?) is summarized by AUC and visualized by the ROC curve. Calibration (do the probabilities match observed rates?) is summarized by the Brier score and visualized by the calibration plot. The track demonstrated two models with identical AUC and very different calibration on the same 1,000-patient cohort. The clinical consequence: a clinician acts on the probability the model produces, not on the rank, and the calibration question is therefore the one that determines clinical usability.

        Track 04 takes up the broader appraisal framework for a published clinical AI paper. The discrimination and calibration questions are two of the five dimensions that framework addresses.
        """
    )
    return


if __name__ == "__main__":
    app.run()
