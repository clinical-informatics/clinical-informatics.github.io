"""Decision curve analysis plot for clinical-informatics.

Decision curve analysis (DCA) is the unifying tool of this curriculum.
It sits at the intersection of test performance, decision making, and
clinical value. The DCA plot answers: across the range of thresholds a
real clinician might use, does *using this model or test* produce more
net benefit than the two trivial alternatives (treat everyone, or
treat no one)?

The plot has three curves:

- **Treat all.** The net benefit if everyone is treated regardless of risk.
- **Treat none.** The net benefit baseline, always zero.
- **Use the model.** The net benefit if we treat patients above the
  threshold and leave others alone.

A model is useful at threshold t if its curve is above both alternatives.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def net_benefit_at_threshold(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    threshold: float,
) -> float:
    """Net benefit of using the model at this threshold."""
    y_true = np.asarray(y_true).astype(int)
    y_prob = np.asarray(y_prob).astype(float)

    n = len(y_true)
    if n == 0 or threshold >= 1.0:
        return 0.0

    predicted_positive = y_prob >= threshold
    tp = int(np.sum(predicted_positive & (y_true == 1)))
    fp = int(np.sum(predicted_positive & (y_true == 0)))

    weight = threshold / (1.0 - threshold)
    return (tp / n) - (fp / n) * weight


def net_benefit_treat_all(y_true: np.ndarray, threshold: float) -> float:
    """Net benefit if everyone is treated."""
    y_true = np.asarray(y_true).astype(int)
    n = len(y_true)
    if n == 0 or threshold >= 1.0:
        return 0.0
    p = float(np.mean(y_true))
    weight = threshold / (1.0 - threshold)
    return p - (1 - p) * weight


def dca_data(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    thresholds: np.ndarray | None = None,
) -> pd.DataFrame:
    if thresholds is None:
        thresholds = np.linspace(0.01, 0.99, 99)
    rows = []
    for t in thresholds:
        rows.append(
            {
                "threshold": float(t),
                "model": net_benefit_at_threshold(y_true, y_prob, float(t)),
                "treat_all": net_benefit_treat_all(y_true, float(t)),
                "treat_none": 0.0,
            }
        )
    return pd.DataFrame(rows)


def render(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    *,
    intervention_label: str = "treat",
    no_intervention_label: str = "don't treat",
):
    """Render the DCA plot and a plain-English interpretation."""
    import altair as alt
    import marimo as mo

    data = dca_data(y_true, y_prob)
    long = data.melt(
        id_vars="threshold",
        value_vars=["model", "treat_all", "treat_none"],
        var_name="strategy",
        value_name="net_benefit",
    )
    label_map = {
        "model": "Use the model",
        "treat_all": f"{intervention_label.capitalize()} everyone",
        "treat_none": f"{no_intervention_label.capitalize()} everyone",
    }
    long["strategy"] = long["strategy"].map(label_map)

    chart = (
        alt.Chart(long)
        .mark_line()
        .encode(
            x=alt.X("threshold:Q", title="Threshold probability"),
            y=alt.Y(
                "net_benefit:Q",
                title="Net benefit",
                scale=alt.Scale(domain=[-0.05, max(0.4, long["net_benefit"].max() * 1.05)]),
            ),
            color=alt.Color("strategy:N", title=""),
        )
        .properties(width=520, height=360, title="Decision curve analysis")
    )

    win_idx = data["model"] > data[["treat_all", "treat_none"]].max(axis=1)
    win_thresholds = data.loc[win_idx, "threshold"]
    if len(win_thresholds) > 0:
        lo, hi = float(win_thresholds.min()), float(win_thresholds.max())
        win_text = (
            f"The model creates more net benefit than either alternative between "
            f"thresholds of **{lo:.0%}** and **{hi:.0%}**. Outside that range, you'd be "
            f"better off either treating everyone or treating no one."
        )
    else:
        win_text = (
            "At every threshold shown, the model is no better than the better of the two "
            "trivial alternatives. That's not necessarily disqualifying, but it should make "
            "you ask what value the model adds."
        )

    prose = (
        "**How to read this chart.** The X axis is the threshold probability, "
        "the probability above which you'd act (treat, alert, refer). The Y axis is net benefit, "
        "scaled so that treating no one is always zero. A strategy that produces higher net benefit "
        "is preferred at that threshold.\n\n"
        f"{win_text}\n\n"
        "DCA matters because it asks the question clinicians actually face: at the threshold "
        "I'd act on, does this tool produce more good than harm?"
    )

    return mo.vstack([mo.as_html(chart), mo.callout(mo.md(prose), kind="info")])
