"""Calibration plot component for clinical-informatics.

A well-discriminating model can still be clinically useless. Calibration
asks: when the model says "30% chance," is the patient admitted 30% of
the time? Or 5%? Or 60%?

This component plots a calibration curve, reports the Brier score, and
explains what both mean in plain English.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def brier_score(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    """Mean squared error between predicted probabilities and outcomes."""
    y_true = np.asarray(y_true).astype(float)
    y_prob = np.asarray(y_prob).astype(float)
    return float(np.mean((y_prob - y_true) ** 2))


def calibration_data(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    n_bins: int = 10,
) -> pd.DataFrame:
    """Compute per-bin observed vs predicted probabilities."""
    y_true = np.asarray(y_true).astype(int)
    y_prob = np.asarray(y_prob).astype(float)

    bins = np.linspace(0, 1, n_bins + 1)
    idx = np.digitize(y_prob, bins) - 1
    idx = np.clip(idx, 0, n_bins - 1)

    rows = []
    for b in range(n_bins):
        mask = idx == b
        n = int(np.sum(mask))
        if n == 0:
            continue
        predicted = float(np.mean(y_prob[mask]))
        observed = float(np.mean(y_true[mask]))
        rows.append(
            {
                "bin": b,
                "predicted_probability": predicted,
                "observed_probability": observed,
                "n": n,
            }
        )
    return pd.DataFrame(rows)


def render(y_true: np.ndarray, y_prob: np.ndarray, *, n_bins: int = 10):
    """Render the calibration plot, Brier score, and an interpretation panel."""
    import altair as alt
    import marimo as mo

    cal = calibration_data(y_true, y_prob, n_bins=n_bins)
    brier = brier_score(y_true, y_prob)

    diag = pd.DataFrame({"x": [0, 1], "y": [0, 1]})

    points = (
        alt.Chart(cal)
        .mark_circle(size=120, color="#1f77b4")
        .encode(
            x=alt.X("predicted_probability:Q", title="Predicted probability"),
            y=alt.Y("observed_probability:Q", title="Observed rate"),
            tooltip=["bin", "predicted_probability", "observed_probability", "n"],
        )
    )
    line = (
        alt.Chart(diag)
        .mark_line(strokeDash=[5, 5], color="#888")
        .encode(x="x:Q", y="y:Q")
    )
    chart = (line + points).properties(
        width=420, height=360, title="Calibration: predicted vs observed"
    )

    prose = (
        f"**Brier score: {brier:.4f}** (lower is better; the perfect score is 0).\n\n"
        "The dashed diagonal is perfect calibration: when the model says 30%, the outcome rate is 30%. "
        "Each blue dot is a bin of patients. Dots above the line mean the model is *under-predicting* "
        "the outcome at that probability. Dots below mean it's *over-predicting.*\n\n"
        "A model can have great discrimination (it ranks the high-risk patients above the low-risk ones) "
        "and still be off here. That matters because clinicians act on the number, not on the rank."
    )

    return mo.vstack([mo.as_html(chart), mo.callout(mo.md(prose), kind="info")])
