"""Track 04: Common misleading patterns.

Five patterns that produce charts a clinician would believe but that
misrepresent the data: a truncated y-axis that exaggerates a small change,
a cherry-picked time window that hides a longer trend, a dual axis that
implies a correlation the data does not support, a time series rendered as
a bar chart that loses the temporal cue, and monthly aggregation that hides
intra-month spikes. Each pattern is shown as a side-by-side pair on Ms.
Reyes's lab series.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import sys
    import types
    from pathlib import Path

    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd

    _COURSE_TITLES = {
        "03": "Privacy, ethics, and governance",
        "11": "Health economics data",
        "15": "Data storytelling",
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

    _WASM_DATA_BASE = "/08-clinical-visualization/track-04-misleading-patterns/app"

    def load_cached_csv(filename):
        if "pyodide" in sys.modules:
            from pyodide.http import open_url
            url = f"{_WASM_DATA_BASE}/cache/{filename}"
            return pd.read_csv(open_url(url))
        return pd.read_csv(Path(__file__).parent / "cache" / filename)

    return alt, load_cached_csv, mo, np, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 04: Common misleading patterns

        ## Charts that are technically correct and clinically misleading

        Every datum on the charts in this track is correct. None of the values are fabricated, mis-recorded, or transposed. Yet each chart misleads the reader about what the underlying data shows. The misrepresentation is in the chart construction, not in the data.

        The five patterns below cover most cases in published clinical literature, vendor marketing materials, and EHR dashboards. Each is presented as a side-by-side pair: the misleading construction on the left, the honest construction of the same data on the right. The data in every pair is Ms. Reyes's lab record (or a derived series from it), loaded from the same CSV used in Tracks 02 and 03.
        """
    )
    return


@app.cell
def _(load_cached_csv, pd):
    labs_all = load_cached_csv("labs.csv")
    labs_all["specimen_date"] = pd.to_datetime(labs_all["specimen_date"])
    labs_all["value"] = pd.to_numeric(labs_all["value"], errors="coerce")
    reyes_crp = labs_all[labs_all["loinc"] == "1988-5"].copy().sort_values("specimen_date").reset_index(drop=True)
    reyes_hgb = labs_all[labs_all["loinc"] == "718-7"].copy().sort_values("specimen_date").reset_index(drop=True)
    return labs_all, reyes_crp, reyes_hgb


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Pattern 1: the truncated y-axis

        A y-axis that does not begin at zero exaggerates the visual size of a small absolute change. The same change on a y-axis that begins at zero is shown to scale and looks far less dramatic.

        The chart on the left below shows Ms. Reyes's CRP between 2025-08-19 and 2026-04-28 (a five-point window with values ranging from about 5 to 8 mg/L). The y-axis starts at 5 mg/L. The visual impression is that CRP has approximately doubled.

        The chart on the right shows the same five values with the y-axis starting at zero. The visual impression is now correct: CRP has moved a small amount in absolute terms within an already-elevated range.
        """
    )
    return


@app.cell
def _(alt, reyes_crp):
    crp_recent = reyes_crp[reyes_crp["specimen_date"] >= "2025-08-19"].copy()

    truncated_chart = (
        alt.Chart(crp_recent)
        .mark_line(point=True, color="#d62728")
        .encode(
            x=alt.X("specimen_date:T", title=""),
            y=alt.Y("value:Q", title="CRP (mg/L)", scale=alt.Scale(domain=[5, 8.5])),
        )
        .properties(width=280, height=220, title="Misleading: y starts at 5")
    )
    honest_chart = (
        alt.Chart(crp_recent)
        .mark_line(point=True, color="#2ca02c")
        .encode(
            x=alt.X("specimen_date:T", title=""),
            y=alt.Y("value:Q", title="CRP (mg/L)", scale=alt.Scale(domain=[0, 50])),
        )
        .properties(width=280, height=220, title="Honest: y starts at 0, full range")
    )
    truncated_pair = alt.hconcat(truncated_chart, honest_chart)
    truncated_pair
    return crp_recent, honest_chart, truncated_chart, truncated_pair


@app.cell
def _(mo):
    mo.md(
        r"""
        The rule on truncated y-axes is conditional, not absolute. For bar charts the rule is unconditional: a bar's height encodes its value, so the y-axis must begin at zero. For line charts the rule is weaker; the line's slope encodes the rate of change, and a y-axis that begins above zero can be defensible if the chart's purpose is to show small changes near the upper end of the range. The chart author has to be explicit about which purpose the chart serves, and the chart's title and axis label should make the truncation visible at a glance.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Pattern 2: the cherry-picked time window

        A chart that begins at a date chosen to make the current value look favorable misleads about the underlying trajectory. The same data over a longer window shows the change in context.

        The chart on the left shows Ms. Reyes's CRP only from May 2024 (the adalimumab addition) through April 2026. The trajectory looks dramatic: CRP fell from about 20 mg/L to about 6 mg/L.

        The chart on the right shows the same series alongside the prior 27 months. The dramatic fall is real, but it is preceded by an earlier rise, and the earlier portion of the chart shows that CRP has been elevated throughout the entire four-year record. The current value of 6 mg/L is still above the reference range upper limit of 5 mg/L.
        """
    )
    return


@app.cell
def _(alt, reyes_crp):
    cherry_window = reyes_crp[reyes_crp["specimen_date"] >= "2024-05-15"].copy()

    cherry_picked = (
        alt.Chart(cherry_window)
        .mark_line(point=True, color="#d62728")
        .encode(
            x=alt.X("specimen_date:T", title=""),
            y=alt.Y("value:Q", title="CRP (mg/L)", scale=alt.Scale(domain=[0, 50])),
        )
        .properties(width=280, height=220, title="Misleading: post-adalimumab only")
    )
    full_window = (
        alt.Chart(reyes_crp)
        .mark_line(point=True, color="#2ca02c")
        .encode(
            x=alt.X("specimen_date:T", title=""),
            y=alt.Y("value:Q", title="CRP (mg/L)", scale=alt.Scale(domain=[0, 50])),
        )
        .properties(width=280, height=220, title="Honest: full four-year record")
    )
    cherry_pair = alt.hconcat(cherry_picked, full_window)
    cherry_pair
    return cherry_pair, cherry_picked, cherry_window, full_window


@app.cell
def _(mo):
    mo.md(
        r"""
        The cherry-picked-window pattern is the most common misleading chart in vendor marketing material. A vendor demonstrating a CDS tool can show only the months in which the tool's recommended action was followed and only the patients who improved. The same chart with the full denominator (every patient, every month) typically shows a much smaller effect. The remedy is to require that the x-axis cover the natural clinical history (typically the entire treatment period or several years for a chronic disease), even when the most recent change is the immediate question.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Pattern 3: the dual-y-axis chart

        Two variables with unrelated natural scales plotted against two y-axes that share an x-axis. The visual impression of correlation is determined by where the chart author chose to start and end each y-axis, not by the data.

        The chart on the left shows CRP (mg/L, axis from 0 to 50) and hemoglobin (g/dL, axis from 10 to 14) on dual y-axes. The two lines visually move together; a clinician might conclude that CRP and hemoglobin are inversely related in this patient.

        The chart on the right shows the same data as two separate panels stacked vertically, each with its own y-axis explicitly labeled. The CRP trajectory and the hemoglobin trajectory are now read separately. The visual correlation has disappeared because it was never in the data; it was an artifact of the dual-axis chart's chosen scales.
        """
    )
    return


@app.cell
def _(alt, pd, reyes_crp, reyes_hgb):
    crp_line = (
        alt.Chart(reyes_crp)
        .mark_line(point=True, color="#1f77b4")
        .encode(
            x=alt.X("specimen_date:T", title=""),
            y=alt.Y("value:Q", title="CRP (mg/L)", scale=alt.Scale(domain=[0, 50])),
        )
    )
    hgb_line = (
        alt.Chart(reyes_hgb)
        .mark_line(point=True, color="#d62728", strokeDash=[4, 2])
        .encode(
            x="specimen_date:T",
            y=alt.Y("value:Q", title="Hemoglobin (g/dL)", scale=alt.Scale(domain=[10, 14])),
        )
    )
    dual_axis_misleading = alt.layer(crp_line, hgb_line).resolve_scale(y="independent").properties(
        width=280,
        height=240,
        title="Misleading: dual y-axes",
    )

    crp_panel = (
        alt.Chart(reyes_crp)
        .mark_line(point=True, color="#1f77b4")
        .encode(
            x=alt.X("specimen_date:T", title=""),
            y=alt.Y("value:Q", title="CRP (mg/L)"),
        )
        .properties(width=280, height=110)
    )
    hgb_panel = (
        alt.Chart(reyes_hgb)
        .mark_line(point=True, color="#d62728")
        .encode(
            x=alt.X("specimen_date:T", title=""),
            y=alt.Y("value:Q", title="Hemoglobin (g/dL)"),
        )
        .properties(width=280, height=110)
    )
    honest_two_panel = alt.vconcat(crp_panel, hgb_panel).properties(
        title="Honest: stacked panels, separate axes"
    )

    dual_axis_pair = alt.hconcat(dual_axis_misleading, honest_two_panel)
    _ = pd
    dual_axis_pair
    return (
        crp_line,
        crp_panel,
        dual_axis_misleading,
        dual_axis_pair,
        hgb_line,
        hgb_panel,
        honest_two_panel,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
        The general rule on dual-y-axis charts is to avoid them. The stacked-panel construction shown on the right is the correct way to display two related but differently-scaled clinical series. The only exception is when the two variables have a natural shared scale (for instance, two related lab values measured in the same units) or when the chart's explicit purpose is to compare ratios of changes rather than absolute values. The exception is rare in clinical work and the default should be to refuse the dual-y-axis construction.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Pattern 4: time series as a bar chart

        A bar chart treats time as a sequence of discrete categories. A line chart treats time as a continuous axis. For longitudinal lab data sampled at irregular intervals, the bar chart loses the temporal cue: the reader cannot see how rapidly the value is changing because the spacing of the bars is set by the chart's layout, not by the elapsed time between samples.

        The chart on the left shows Ms. Reyes's CRP as a bar chart. Each specimen date is one bar of uniform width. The chart on the right shows the same data as a line chart with the time axis at proper scale. The 2024 climb is far more visible on the line chart, because the line's slope encodes the rate of change.
        """
    )
    return


@app.cell
def _(alt, reyes_crp):
    crp_bars = reyes_crp.copy()
    crp_bars["date_str"] = crp_bars["specimen_date"].dt.strftime("%Y-%m-%d")

    bar_misleading = (
        alt.Chart(crp_bars)
        .mark_bar()
        .encode(
            x=alt.X("date_str:N", title="", axis=alt.Axis(labelAngle=-45, labelFontSize=8)),
            y=alt.Y("value:Q", title="CRP (mg/L)"),
        )
        .properties(width=320, height=240, title="Misleading: time as bars")
    )
    line_honest = (
        alt.Chart(reyes_crp)
        .mark_line(point=True, color="#2ca02c")
        .encode(
            x=alt.X("specimen_date:T", title=""),
            y=alt.Y("value:Q", title="CRP (mg/L)"),
        )
        .properties(width=320, height=240, title="Honest: time on a continuous axis")
    )
    bar_pair = alt.hconcat(bar_misleading, line_honest)
    bar_pair
    return bar_misleading, bar_pair, crp_bars, line_honest


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Pattern 5: aggregation that hides intra-window spikes

        A chart that aggregates a high-frequency signal into a monthly or quarterly mean hides excursions that occur within the aggregation window. For an alert-rate dashboard tracking a CDS alert that fires throughout the day, monthly aggregation can make a workflow-disrupting daily spike invisible.

        The synthetic series below simulates daily alert counts over 90 days. Most days the alert fires 10 to 30 times. On three days in the middle of the period, the alert fires more than 200 times because a downstream EHR change misconfigured the trigger. The chart on the left shows the monthly mean; the spike is averaged into the surrounding 27 days and barely registers. The chart on the right shows the daily series; the three spike days are visible immediately.
        """
    )
    return


@app.cell
def _(alt, np, pd):
    rng = np.random.default_rng(seed=20260527)
    dates = pd.date_range(start="2026-01-01", periods=90, freq="D")
    counts = rng.integers(low=8, high=30, size=90)
    counts[40] = 240
    counts[41] = 220
    counts[42] = 195
    daily_df = pd.DataFrame({"date": dates, "alert_count": counts})
    daily_df["month"] = daily_df["date"].dt.to_period("M").astype(str)
    monthly_df = daily_df.groupby("month", as_index=False)["alert_count"].mean()
    monthly_df["alert_count_mean"] = monthly_df["alert_count"].round(1)

    monthly_chart = (
        alt.Chart(monthly_df)
        .mark_bar(color="#d62728")
        .encode(
            x=alt.X("month:N", title=""),
            y=alt.Y("alert_count_mean:Q", title="Daily alert mean", scale=alt.Scale(domain=[0, 250])),
            tooltip=["month:N", "alert_count_mean:Q"],
        )
        .properties(width=280, height=220, title="Misleading: monthly mean")
    )
    daily_chart = (
        alt.Chart(daily_df)
        .mark_line(color="#2ca02c")
        .encode(
            x=alt.X("date:T", title=""),
            y=alt.Y("alert_count:Q", title="Daily alert count", scale=alt.Scale(domain=[0, 250])),
            tooltip=["date:T", "alert_count:Q"],
        )
        .properties(width=280, height=220, title="Honest: daily count")
    )
    aggregation_pair = alt.hconcat(monthly_chart, daily_chart)
    aggregation_pair
    return (
        aggregation_pair,
        counts,
        daily_chart,
        daily_df,
        dates,
        monthly_chart,
        monthly_df,
        rng,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
        The aggregation pattern is the most insidious of the five because the misleading chart is often produced unintentionally by a sound impulse (smooth out the noise, summarize at a clinically meaningful interval). The remedy is not to forbid aggregation but to show the raw series alongside the aggregated one whenever the aggregation could hide events that matter. For an alert-rate dashboard, the daily series should always be available as a drill-down from the monthly summary.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A note on intent

        Misleading charts are produced for several reasons. Some are deliberate (a vendor cherry-picks a time window to make a product look effective). Most are not (an analyst aggregates a daily signal into a monthly mean because the monthly view looks cleaner). The five patterns above are not accusations of bad faith; they are recurring construction errors that a careful chart author has to actively avoid. The honest chart in each pair is the chart a clinical author would default to with no further effort. The misleading chart is what is produced when the author optimizes for visual drama, for cleanness, or for a particular reading of the data.
        """
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "08",
        "15",
        "Communicating about charts with non-technical audiences",
        "Course 15 (Data storytelling) addresses the related question of how to present a chart to a clinical or executive audience. The construction rules in this track are necessary but not sufficient; the chart still has to be explained, annotated, and contextualized for the audience reading it.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        Five recurring construction errors produce charts that are technically correct and clinically misleading. The truncated y-axis exaggerates small absolute changes. The cherry-picked time window hides the trajectory that gives the current value its context. The dual-y-axis chart implies a correlation the data does not support. The time series as a bar chart loses the temporal cue. Aggregation that smooths a daily signal into a monthly mean hides intra-window spikes that may be the clinically important events.

        The honest construction of each pattern is shown alongside the misleading one. None of the patterns require the chart author to lie about any value; all of them can be produced by an author who is not actively guarding against the pattern. The next step in the course is the capstone, where the reader assembles a clinical dashboard for an RA cohort and has to apply all of the construction decisions discussed across the four tracks.
        """
    )
    return


if __name__ == "__main__":
    app.run()
