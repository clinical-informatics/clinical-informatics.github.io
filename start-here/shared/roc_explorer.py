"""ROC explorer for clinical-informatics.

The most reused interactive component in the curriculum.

It shows three views of the same thing, side by side:

- A 2x2 table at the current threshold
- The full ROC curve, with the current threshold marked
- A plain-English interpretation panel that updates with every move

Use this in the epidemiology course (first appearance), AI course
(deepened with model probabilities), and CDS course (revisited for
threshold setting).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class ROCData:
    """A bundle of thresholds, sensitivities, and specificities."""

    thresholds: np.ndarray
    sensitivities: np.ndarray
    specificities: np.ndarray
    auc: float


def roc_from_scores(y_true: np.ndarray, y_score: np.ndarray) -> ROCData:
    """Compute ROC points from binary labels and model scores."""
    from sklearn.metrics import roc_auc_score, roc_curve

    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    auc = float(roc_auc_score(y_true, y_score))
    return ROCData(
        thresholds=thresholds,
        sensitivities=tpr,
        specificities=1 - fpr,
        auc=auc,
    )


def two_by_two(
    y_true: np.ndarray,
    y_score: np.ndarray,
    threshold: float,
) -> dict[str, int | float]:
    """Compute the 2x2 table and derived metrics at a given threshold."""
    y_true = np.asarray(y_true).astype(int)
    y_score = np.asarray(y_score).astype(float)
    y_pred = (y_score >= threshold).astype(int)

    tp = int(np.sum((y_pred == 1) & (y_true == 1)))
    fp = int(np.sum((y_pred == 1) & (y_true == 0)))
    tn = int(np.sum((y_pred == 0) & (y_true == 0)))
    fn = int(np.sum((y_pred == 0) & (y_true == 1)))

    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    ppv = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    npv = tn / (tn + fn) if (tn + fn) > 0 else 0.0

    return {
        "TP": tp,
        "FP": fp,
        "TN": tn,
        "FN": fn,
        "sensitivity": sensitivity,
        "specificity": specificity,
        "PPV": ppv,
        "NPV": npv,
    }


def explore(
    y_true: np.ndarray,
    y_score: np.ndarray,
    *,
    score_label: str = "model score",
    positive_label: str = "disease present",
    negative_label: str = "disease absent",
):
    """Render the full interactive ROC explorer.

    Parameters
    ----------
    y_true:
        Binary truth labels (0 / 1).
    y_score:
        Continuous scores or probabilities.
    score_label:
        How to describe the score in plain English.
    positive_label, negative_label:
        Plain-English labels for the two classes.
    """
    import marimo as mo
    import altair as alt

    y_true = np.asarray(y_true).astype(int)
    y_score = np.asarray(y_score).astype(float)

    roc = roc_from_scores(y_true, y_score)
    score_min = float(np.min(y_score))
    score_max = float(np.max(y_score))

    threshold = mo.ui.slider(
        start=score_min,
        stop=score_max,
        step=(score_max - score_min) / 100,
        value=(score_min + score_max) / 2,
        label=f"Alert threshold (on the {score_label})",
        show_value=True,
    )

    def render():
        t = float(threshold.value)
        stats = two_by_two(y_true, y_score, t)

        roc_df = pd.DataFrame(
            {
                "false_positive_rate": 1 - roc.specificities,
                "sensitivity": roc.sensitivities,
            }
        )
        marker = pd.DataFrame(
            [
                {
                    "false_positive_rate": 1 - stats["specificity"],
                    "sensitivity": stats["sensitivity"],
                }
            ]
        )
        diag = pd.DataFrame(
            {"false_positive_rate": [0, 1], "sensitivity": [0, 1]}
        )

        roc_chart = (
            alt.Chart(roc_df)
            .mark_line()
            .encode(x="false_positive_rate:Q", y="sensitivity:Q")
            .properties(width=360, height=300, title=f"ROC curve (AUC = {roc.auc:.3f})")
        )
        diag_chart = alt.Chart(diag).mark_line(strokeDash=[4, 4], color="#888").encode(
            x="false_positive_rate:Q", y="sensitivity:Q"
        )
        marker_chart = (
            alt.Chart(marker)
            .mark_point(size=200, color="red", filled=True)
            .encode(x="false_positive_rate:Q", y="sensitivity:Q")
        )
        chart = roc_chart + diag_chart + marker_chart

        tbl = pd.DataFrame(
            [
                {"": "Test positive", positive_label: stats["TP"], negative_label: stats["FP"]},
                {"": "Test negative", positive_label: stats["FN"], negative_label: stats["TN"]},
            ]
        )

        prose = (
            f"At a threshold of **{t:.2f}**, the test catches "
            f"**{stats['sensitivity']:.0%}** of patients who have the condition (sensitivity), "
            f"and correctly clears **{stats['specificity']:.0%}** of patients who don't (specificity). "
            f"Among patients who test positive, **{stats['PPV']:.0%}** actually have the condition (PPV). "
            f"Among patients who test negative, **{stats['NPV']:.0%}** actually don't (NPV).\n\n"
            "Move the slider. Watch what happens to PPV when you make the threshold stricter."
        )

        return mo.vstack(
            [
                threshold,
                mo.hstack(
                    [
                        mo.vstack(
                            [
                                mo.md("**2x2 table at this threshold**"),
                                mo.ui.table(tbl, selection=None),
                            ]
                        ),
                        mo.as_html(chart),
                    ],
                    widths="equal",
                ),
                mo.callout(mo.md(prose), kind="info"),
            ]
        )

    return render
