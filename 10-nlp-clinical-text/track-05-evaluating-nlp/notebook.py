"""Track 05: Evaluating NLP tools.

Precision, recall, F1 in plain English, with the explicit mapping to PPV
and sensitivity from Course 04. Strict vs lenient span matching. Inter-
annotator agreement. The cost-asymmetry argument that clinical NLP
usually prioritizes recall. A reactive demonstration computes precision,
recall, and F1 on a small annotated set as the prediction threshold
moves.
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

    return alt, mo, np, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 05: Evaluating NLP tools

        ## The evaluation question

        Any NLP tool is evaluated against a gold-standard annotation. The gold standard is a corpus that human annotators have marked up with the labels the tool is supposed to produce. The tool's output is then compared against the gold; the comparison produces three numbers that summarize performance: precision (of the tool's predictions, what fraction the gold also marked), recall (of the gold's annotations, what fraction the tool found), and F1 (the harmonic mean of the two).

        The numbers are the same numbers Course 04 introduced under different vocabulary. The track makes the mapping explicit, addresses the operational decisions that change which number comes out (strict vs lenient span matching, the inter-annotator agreement that bounds the achievable performance, the cost asymmetry between false positives and false negatives in clinical use), and closes with a reactive demonstration on a small synthetic annotated dataset.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Precision, recall, F1

        The three numbers are defined as follows. Consider a corpus with a known gold-standard annotation. Apply the NLP tool to the corpus and collect its predictions. Compare the predictions to the gold one at a time. Each comparison produces a true positive (the prediction matches a gold annotation), a false positive (the prediction does not match any gold annotation), or a false negative (the gold has an annotation the prediction did not produce).

        From the three counts:

        - **Precision** = true positives / (true positives + false positives). The fraction of the tool's predictions that were correct.
        - **Recall** = true positives / (true positives + false negatives). The fraction of the gold annotations the tool found.
        - **F1** = 2 * (precision * recall) / (precision + recall). The harmonic mean of precision and recall.

        F1 is the harmonic mean rather than the arithmetic mean because the harmonic mean penalizes the case where one of the two numbers is much lower than the other. A tool with precision 1.0 and recall 0.1 has arithmetic mean 0.55 (misleadingly high) and F1 0.18 (which correctly reflects that the tool is missing 90% of the gold annotations).
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "10",
        "04",
        "Precision is PPV; recall is sensitivity",
        "Course 04 Track 3 introduced sensitivity and PPV in the diagnostic-test framework. The NLP vocabulary names the same two quantities differently: precision = PPV (of what was flagged, how much was real?), recall = sensitivity (of what was real, how much was flagged?). The 2x2 table from Course 04 maps onto the NLP confusion matrix one-to-one; only the row and column labels change.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Strict vs lenient span matching

        A clinical NER prediction is a typed span: a start offset, an end offset, the surface text, and an entity type. Comparing a prediction against a gold span requires deciding what counts as a match. Two definitions are in common use.

        - **Strict (exact-span) matching.** A prediction matches a gold span only if both the start and end offsets are identical and the entity type matches. "methotrexate" predicted at characters 100-112 matches a gold annotation at characters 100-112 of type MEDICATION. A prediction at characters 99-112 does not match (the start offset is off by one).
        - **Lenient (overlap-span) matching.** A prediction matches a gold span if they overlap by at least one character and the entity type matches. The same characters-99-112 prediction would match a gold at characters 100-112 under lenient matching because they share 12 characters.

        Strict matching is the stricter standard and produces lower F1 numbers. Lenient matching is the more forgiving standard and produces higher F1 numbers on the same predictions. The published n2c2 and i2b2 shared-task papers usually report both because the strict-vs-lenient gap quantifies how much of the system's performance is in the entity-detection step versus the precise-boundary step.

        For most clinical downstream uses, lenient matching is the more clinically relevant number. A pipeline that extracts "methotrexate" at characters 99-112 and a pipeline that extracts the same drug at 100-112 are equally useful for downstream use. For published technical comparisons, strict matching is the convention because it is more discriminating.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Inter-annotator agreement: the gold is not perfectly gold

        Any gold-standard corpus was produced by human annotators. Different annotators applying the same guidelines to the same text often disagree on edge cases. The inter-annotator agreement (IAA) measures the level of disagreement; it is the practical upper bound on the system performance an NLP tool can achieve on that corpus.

        Two IAA metrics appear most often.

        - **Pairwise F1.** Compute F1 treating one annotator's annotations as the gold and the other annotator's as the prediction. Pairwise F1 on the same task and the same guidelines is typically 0.80 to 0.90 for clinical NER, lower for relation extraction (0.70 to 0.85), lower still for assertion / negation status (0.65 to 0.80).
        - **Cohen's kappa.** A chance-corrected agreement coefficient. Kappa of 1.0 is perfect agreement; 0.0 is chance-level agreement; 0.6 to 0.8 is considered "substantial" agreement in the published literature.

        The implication for system evaluation: a model that achieves 0.85 F1 against a gold whose IAA is 0.86 may be performing at human level for that task. Reporting model F1 as a fraction of the IAA (relative to inter-annotator agreement) is the more honest framing for clinical NLP results.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The cost-asymmetry argument

        In clinical applications, false negatives often cost more than false positives. A drug-allergy extractor that misses an allergy in the chart can contribute to a wrong-drug event; a drug-allergy extractor that over-flags can produce alert fatigue but rarely leads to a wrong action. The cost of the missed entity is therefore typically higher than the cost of the spurious entity.

        Three consequences follow.

        - **Recall is usually prioritized over precision.** A clinical NLP system tuned for production usually aims for high recall at the expense of some precision, then handles the precision side with a downstream filter (clinician review, rule-based post-processing, a second-pass confirmation model).
        - **F1 may not be the right summary.** F1 weights precision and recall equally. For a recall-prioritized task, the F-beta score (F-beta = (1 + beta^2) * precision * recall / (beta^2 * precision + recall)) with beta > 1 (typically beta = 2, the F2 score) weights recall higher. Clinical NLP evaluation papers occasionally report F2 alongside F1.
        - **The downstream cost has to be made explicit.** What is the cost of a missed entity in this application, and what is the cost of a spurious entity? The relative costs determine the threshold at which the system should operate, which determines which point on the precision-recall trade-off curve is the right one. The reactive demonstration below makes the trade-off visible.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Reactive demonstration: precision-recall on a small annotated set

        The synthetic corpus below has 200 candidate entity mentions. The gold-standard annotation marks 60 of them as true entities (positives) and 140 as not-entities (negatives). The "model" assigns a confidence score to each candidate (higher means the model believes the candidate is more likely to be a true entity). The threshold slider sets which scores cross over into predictions; predictions are then compared against the gold to compute precision, recall, and F1.

        Move the slider and watch the three numbers change.
        """
    )
    return


@app.cell
def _(np):
    eval_rng = np.random.default_rng(seed=20260528)
    n_pos = 60
    n_neg = 140
    pos_scores = eval_rng.beta(a=4, b=2, size=n_pos)
    neg_scores = eval_rng.beta(a=2, b=5, size=n_neg)
    return eval_rng, n_neg, n_pos, neg_scores, pos_scores


@app.cell
def _(mo):
    threshold_slider = mo.ui.slider(
        start=0.05, stop=0.95, step=0.01, value=0.50,
        label="Prediction threshold (a candidate becomes a prediction if its score >= threshold)",
        show_value=True,
    )
    threshold_slider
    return (threshold_slider,)


@app.cell
def _(neg_scores, pos_scores, threshold_slider):
    t = float(threshold_slider.value)
    tp = int((pos_scores >= t).sum())
    fp = int((neg_scores >= t).sum())
    fn = int((pos_scores < t).sum())
    tn = int((neg_scores < t).sum())
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    f2 = 5 * precision * recall / (4 * precision + recall) if (4 * precision + recall) else 0.0
    return f1, f2, fn, fp, precision, recall, t, tn, tp


@app.cell
def _(f1, f2, fn, fp, mo, precision, recall, t, tn, tp):
    mo.md(
        f"""
        **At threshold {t:.2f}**:

        - True positives: **{tp}**
        - False positives: **{fp}**
        - False negatives: **{fn}**
        - True negatives: **{tn}**

        | Metric | Value |
        |---|---|
        | Precision (= PPV) | **{precision:.3f}** |
        | Recall (= sensitivity) | **{recall:.3f}** |
        | F1 | **{f1:.3f}** |
        | F2 (recall-weighted) | **{f2:.3f}** |
        """
    )
    return


@app.cell
def _(alt, neg_scores, np, pd, pos_scores):
    thresholds = np.linspace(0.05, 0.95, 91)
    rows = []
    for t_grid in thresholds:
        tp_grid = int((pos_scores >= t_grid).sum())
        fp_grid = int((neg_scores >= t_grid).sum())
        fn_grid = int((pos_scores < t_grid).sum())
        p_grid = tp_grid / (tp_grid + fp_grid) if (tp_grid + fp_grid) else 0.0
        r_grid = tp_grid / (tp_grid + fn_grid) if (tp_grid + fn_grid) else 0.0
        f1_grid = 2 * p_grid * r_grid / (p_grid + r_grid) if (p_grid + r_grid) else 0.0
        rows.append({"threshold": t_grid, "metric": "Precision", "value": p_grid})
        rows.append({"threshold": t_grid, "metric": "Recall", "value": r_grid})
        rows.append({"threshold": t_grid, "metric": "F1", "value": f1_grid})
    sweep_df = pd.DataFrame(rows)

    metric_chart = (
        alt.Chart(sweep_df).mark_line().encode(
            x=alt.X("threshold:Q", title="Prediction threshold"),
            y=alt.Y("value:Q", title="Score", scale=alt.Scale(domain=[0, 1])),
            color=alt.Color("metric:N", title=""),
            tooltip=["threshold:Q", "metric:N", "value:Q"],
        ).properties(width=560, height=300, title="Precision, recall, F1 across threshold")
    )
    metric_chart
    return f1_grid, fn_grid, fp_grid, metric_chart, p_grid, r_grid, rows, sweep_df, t_grid, thresholds, tp_grid


@app.cell
def _(mo):
    mo.md(
        r"""
        Three patterns are visible.

        First, precision rises with threshold. At a strict threshold the model only emits predictions for the candidates it is most confident about; almost all of them are correct.

        Second, recall falls with threshold. At a strict threshold the model misses many true positives because their scores fall below the cut-off.

        Third, F1 has a peak somewhere in the middle. The peak is where the precision-recall trade-off is most balanced. For a recall-prioritized clinical use, the operating point would be left of the F1 peak (lower threshold, higher recall, lower precision); for a precision-prioritized use, the operating point would be right of the peak.
        """
    )
    return


@app.cell
def _(alt, neg_scores, np, pd, pos_scores):
    pr_rows = []
    for t_pr in np.linspace(0.05, 0.95, 91):
        tp_pr = int((pos_scores >= t_pr).sum())
        fp_pr = int((neg_scores >= t_pr).sum())
        fn_pr = int((pos_scores < t_pr).sum())
        p_pr = tp_pr / (tp_pr + fp_pr) if (tp_pr + fp_pr) else 0.0
        r_pr = tp_pr / (tp_pr + fn_pr) if (tp_pr + fn_pr) else 0.0
        pr_rows.append({"recall": r_pr, "precision": p_pr})
    pr_df = pd.DataFrame(pr_rows)

    pr_chart = (
        alt.Chart(pr_df).mark_line(color="#1f77b4").encode(
            x=alt.X("recall:Q", title="Recall (= sensitivity)", scale=alt.Scale(domain=[0, 1])),
            y=alt.Y("precision:Q", title="Precision (= PPV)", scale=alt.Scale(domain=[0, 1])),
        ).properties(width=400, height=320, title="Precision-Recall curve")
    )
    pr_chart
    return fn_pr, fp_pr, p_pr, pr_chart, pr_df, pr_rows, r_pr, t_pr, tp_pr


@app.cell
def _(mo):
    mo.md(
        r"""
        The precision-recall curve above is the same shape as the ROC curve from Course 04, plotted in a different coordinate system. The PR curve is more informative than the ROC curve when the positive class is much smaller than the negative class (the common case in clinical NER, where most candidates are not entities). Most clinical NLP evaluation papers report the PR curve alongside or instead of the ROC curve for this reason.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "10",
        "04",
        "ROC curve, sensitivity, specificity from Course 04",
        "Course 04 Track 3 introduced the ROC curve. The PR curve here is the same ranking information plotted against recall (= sensitivity) and precision (= PPV) instead of against the false-positive rate. The PR curve is preferred when positive class prevalence is low, which is the standard situation in clinical NER.",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "10",
        "12",
        "Evaluating a CDS rule that includes an NLP layer",
        "Course 12 takes up CDS evaluation. A CDS rule that depends on an NLP extraction (the patient declined a screening per the note, the chart documents a code-status change) inherits the NLP layer's precision and recall. The CDS evaluation has to report both the rule's own performance and the upstream NLP performance, with the joint behavior the actually-deployed system will exhibit.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        Any NLP tool is evaluated against a gold-standard annotation. The three standard summary numbers are precision (PPV), recall (sensitivity), and F1 (their harmonic mean). The Course 04 sensitivity-and-PPV vocabulary maps one-to-one onto the NLP precision-and-recall vocabulary; the F1 summary is the recall side of the same Course-04 trade-off. Strict span matching produces lower F1 than lenient span matching; inter-annotator agreement bounds the F1 a system can achieve; cost asymmetry in clinical applications usually argues for prioritizing recall over precision and for operating at a lower-than-F1-optimal threshold. The reactive demonstration made the precision-recall trade-off visible on a synthetic 200-candidate set; the precision-recall curve is the standard summary chart for clinical NLP performance.

        This is the last track of the course. The capstone takes up the end-to-end exercise: build a structured representation of Ms. Reyes's record from her 8 notes using a pre-built NLP pipeline, contrast it with the structured EHR fields, and quantify what was lost when only the structured fields were queried.
        """
    )
    return


if __name__ == "__main__":
    app.run()
