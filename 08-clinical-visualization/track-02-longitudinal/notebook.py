"""Track 02: Longitudinal and time-series data.

Disease activity over time. Ms. Reyes's CRP and ESR are loaded from her actual
lab series and rendered as a four-year trajectory. The track addresses three
decisions every longitudinal chart faces: whether to show a reference-range
band, whether to annotate the medication changes that explain inflections, and
whether to smooth the line. Each decision is shown with the chart it produces,
and the reader can toggle the band, the annotations, and the smoothing.
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
        "01": "Computational thinking",
        "04": "Clinical epidemiology",
        "07": "Data wrangling and engineering",
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

    _WASM_DATA_BASE = "/08-clinical-visualization/track-02-longitudinal/app"

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
        # Track 02: Longitudinal and time-series data

        ## What a longitudinal chart is asked to do

        Longitudinal clinical data has one variable on the y-axis and time on the x-axis. The chart is asked to show two things at once: the trajectory of the value, and the context that gives the trajectory meaning. The context is what distinguishes a clinically useful chart from a chart that is technically correct but uninterpretable.

        Three decisions determine the context. First, whether to show the laboratory reference range as a shaded band so the reader can see at a glance which values are in range. Second, whether to annotate the medication changes that explain the inflections in the curve. Third, whether to smooth the line so the trend is visible above the visit-to-visit noise.

        Each decision is addressed below using Ms. Reyes's CRP and ESR series, loaded directly from her lab record. The toggles at the bottom of the track let the reader produce the chart that any combination of decisions yields.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Ms. Reyes's CRP and ESR series

        The data comes from `start-here/patients/elena-reyes/labs.csv`. CRP is LOINC 1988-5; ESR is LOINC 4537-7. Both are measured at every clinic visit and both have a published reference range (CRP 0 to 5 mg/L; ESR 0 to 20 mm/h for an adult woman).
        """
    )
    return


@app.cell
def _(load_cached_csv, pd):
    labs_all = load_cached_csv("labs.csv")
    labs_all["specimen_date"] = pd.to_datetime(labs_all["specimen_date"])
    labs_all["value"] = pd.to_numeric(labs_all["value"], errors="coerce")
    reyes_crp = labs_all[labs_all["loinc"] == "1988-5"].copy().sort_values("specimen_date").reset_index(drop=True)
    reyes_esr = labs_all[labs_all["loinc"] == "4537-7"].copy().sort_values("specimen_date").reset_index(drop=True)
    reyes_crp[["specimen_date", "value", "unit", "interpretation"]].head(8)
    return labs_all, reyes_crp, reyes_esr


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The baseline chart: a line with no annotations

        The simplest possible longitudinal chart plots value against date with a line connecting the samples in time order. The chart below is the baseline. The trajectory is visible but the context is missing.
        """
    )
    return


@app.cell
def _(alt, reyes_crp):
    baseline_chart = (
        alt.Chart(reyes_crp)
        .mark_line(point=True, color="#1f77b4")
        .encode(
            x=alt.X("specimen_date:T", title="Specimen date"),
            y=alt.Y("value:Q", title="CRP (mg/L)"),
            tooltip=["specimen_date:T", "value:Q"],
        )
        .properties(
            width=620,
            height=260,
            title="Ms. Reyes: CRP over four years (baseline, no context)",
        )
    )
    baseline_chart
    return (baseline_chart,)


@app.cell
def _(mo):
    mo.md(
        r"""
        The baseline chart answers the trajectory question (CRP fell over the first year, climbed in 2024, stabilized by 2026). It does not answer the more useful clinical question: at which of those points was CRP elevated above the reference range, and what treatment changes explain the inflections?
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Decision 1: the reference-range band

        A laboratory reference range is the interval that contains the central 95% of values from a healthy population. CRP is 0 to 5 mg/L for an adult. Plotting the reference range as a shaded horizontal band converts the chart from "CRP over time" to "CRP over time, in or out of range." The two charts answer different questions and the reference-range band is required when the second question is the clinical one.

        The chart below adds the CRP reference range as a green band. Every point above the band is elevated; the points inside the band are normal.
        """
    )
    return


@app.cell
def _(alt, pd, reyes_crp):
    ref_range_band = pd.DataFrame([{"low": 0, "high": 5}])
    band_chart = (
        alt.Chart(ref_range_band)
        .mark_rect(opacity=0.15, color="#2ca02c")
        .encode(y="low:Q", y2="high:Q")
    )
    line_layer = (
        alt.Chart(reyes_crp)
        .mark_line(point=True, color="#1f77b4")
        .encode(
            x=alt.X("specimen_date:T", title="Specimen date"),
            y=alt.Y("value:Q", title="CRP (mg/L)"),
            tooltip=["specimen_date:T", "value:Q"],
        )
    )
    chart_with_band = (band_chart + line_layer).properties(
        width=620,
        height=260,
        title="Ms. Reyes CRP with reference-range band (green = 0 to 5 mg/L)",
    )
    chart_with_band
    return band_chart, chart_with_band, line_layer, ref_range_band


@app.cell
def _(mo):
    mo.md(
        r"""
        The reference-range band tells the reader that no value in the four-year series is in the normal range. Every value is elevated, and the chart now answers the elevation question at a glance. The band is one decoration, but it changes the chart's clinical content.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Decision 2: annotating medication changes

        The inflections in a disease-activity trajectory usually correspond to changes in treatment. Marking the medication changes on the chart with vertical reference lines, each labeled with what changed, lets the reader read the trajectory and the cause of each inflection at once.

        Ms. Reyes's treatment history has three load-bearing dates: methotrexate started 2022-03-07 (her diagnosis visit), adalimumab added 2024-05-15 (her DAS28 was still 4.1 despite a year on MTX), and a short prednisone taper from 2025-01-12 to 2025-04-30 (a self-limited flare during the second year on adalimumab).
        """
    )
    return


@app.cell
def _(alt, band_chart, line_layer, pd):
    med_events = pd.DataFrame(
        [
            {"date": "2022-03-07", "label": "MTX start"},
            {"date": "2024-05-15", "label": "Adalimumab add"},
            {"date": "2025-01-12", "label": "Prednisone taper"},
        ]
    )
    med_events["date"] = pd.to_datetime(med_events["date"])

    med_lines = (
        alt.Chart(med_events)
        .mark_rule(color="#d62728", strokeDash=[3, 3])
        .encode(x="date:T")
    )
    med_labels = (
        alt.Chart(med_events)
        .mark_text(align="left", dx=4, dy=-130, color="#d62728", fontSize=11)
        .encode(x="date:T", text="label:N")
    )
    annotated_chart = (band_chart + line_layer + med_lines + med_labels).properties(
        width=620,
        height=260,
        title="Ms. Reyes CRP with reference band and medication annotations",
    )
    annotated_chart
    return annotated_chart, med_events, med_labels, med_lines


@app.cell
def _(mo):
    mo.md(
        r"""
        The annotated chart now supports three readings of the same data: the trajectory (the line), the elevation context (the green band), and the treatment-driven explanation of each inflection (the red dashed lines). A clinician can read the chart in seconds and have the full picture of what happened.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Decision 3: smoothing the line

        Visit-to-visit lab variation has two components: real change in disease activity, and noise from specimen timing, assay precision, and acute confounders (a transient viral illness can raise CRP for several weeks). The raw line shows the value at each visit; a smoothed line shows the underlying trajectory the visits sample from. Both have a place; neither is universally correct.

        Three smoothing options are common in clinical charts. The raw line (no smoothing) preserves every data point and is the most faithful to the record. A rolling mean over a fixed window (3 or 5 visits) flattens single-visit excursions but lags behind real changes. A LOESS smoother (locally weighted regression) tracks slower trends without imposing a global shape but obscures inflection points that genuinely matter.

        The chart below shows all three options on Ms. Reyes's CRP series. The rolling mean is computed with a window of 3 visits, centered. The LOESS smoother is drawn from Altair's built-in `loess` transform.
        """
    )
    return


@app.cell
def _(alt, np, reyes_crp):
    crp_smoothed = reyes_crp.copy()
    crp_smoothed["rolling_mean"] = crp_smoothed["value"].rolling(window=3, min_periods=1, center=True).mean()

    raw_layer = (
        alt.Chart(crp_smoothed)
        .mark_line(point=True, color="#7f7f7f", opacity=0.4)
        .encode(
            x=alt.X("specimen_date:T", title="Specimen date"),
            y=alt.Y("value:Q", title="CRP (mg/L)"),
        )
    )
    rolling_layer = (
        alt.Chart(crp_smoothed)
        .mark_line(color="#1f77b4", strokeWidth=2)
        .encode(x="specimen_date:T", y="rolling_mean:Q")
    )
    loess_layer = (
        alt.Chart(crp_smoothed)
        .mark_line(color="#d62728", strokeWidth=2, strokeDash=[4, 2])
        .transform_loess("specimen_date", "value", bandwidth=0.4)
        .encode(x="specimen_date:T", y="value:Q")
    )
    smoothing_chart = (raw_layer + rolling_layer + loess_layer).properties(
        width=620,
        height=260,
        title="Ms. Reyes CRP: raw (gray), 3-visit rolling mean (blue), LOESS (red dashed)",
    )
    _ = np
    smoothing_chart
    return crp_smoothed, loess_layer, raw_layer, rolling_layer, smoothing_chart


@app.cell
def _(mo):
    mo.md(
        r"""
        Three observations follow from the smoothing chart.

        First, the raw line is the most faithful to the record and is the right choice when individual visits matter for the clinical reading.

        Second, the rolling mean visibly lags the raw line on the 2024 climb that corresponds to the adalimumab addition. Centered rolling means hide this lag better than trailing means but introduce a different distortion: a value at month 30 incorporates information from months 28 and 32, which the clinician at month 30 did not have.

        Third, the LOESS smoother shows the broad trajectory (down, up, down again) but smooths over the 2024 climb so much that the inflection at the adalimumab addition is no longer visible. The LOESS smoother answers a different question than the raw line. Use it when the question is the slow trend; use the raw line when the question is the inflection point.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A useful default for clinical longitudinal charts

        For a CRP or ESR series displayed to a clinician, a defensible default is the raw line, with the reference-range band shaded behind it and the load-bearing medication changes marked as vertical reference lines with text labels. Smoothing is added only if the visit-to-visit noise is so high that the underlying trajectory is obscured. The annotated chart above is the default. Most clinical longitudinal charts should look more or less like it.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Interactive: the three decisions, all toggles

        The toggles below let the reader produce any combination of the three decisions on Ms. Reyes's CRP series. Toggle the reference-range band, the medication annotations, and the smoothing option to see the chart that any combination yields.
        """
    )
    return


@app.cell
def _(mo):
    show_band = mo.ui.checkbox(value=True, label="Reference-range band (0 to 5 mg/L)")
    show_annotations = mo.ui.checkbox(value=True, label="Medication-change annotations")
    smoothing_option = mo.ui.dropdown(
        options=["None (raw)", "3-visit rolling mean", "LOESS"],
        value="None (raw)",
        label="Smoothing",
    )
    mo.vstack([show_band, show_annotations, smoothing_option])
    return show_annotations, show_band, smoothing_option


@app.cell
def _(alt, crp_smoothed, med_events, ref_range_band, show_annotations, show_band, smoothing_option):
    layers = []
    if show_band.value:
        layers.append(
            alt.Chart(ref_range_band)
            .mark_rect(opacity=0.15, color="#2ca02c")
            .encode(y="low:Q", y2="high:Q")
        )

    smoothing_label = smoothing_option.value
    if smoothing_label == "None (raw)":
        layers.append(
            alt.Chart(crp_smoothed)
            .mark_line(point=True, color="#1f77b4")
            .encode(
                x=alt.X("specimen_date:T", title="Specimen date"),
                y=alt.Y("value:Q", title="CRP (mg/L)"),
                tooltip=["specimen_date:T", "value:Q"],
            )
        )
    elif smoothing_label == "3-visit rolling mean":
        layers.append(
            alt.Chart(crp_smoothed)
            .mark_line(color="#7f7f7f", opacity=0.4)
            .encode(x="specimen_date:T", y="value:Q")
        )
        layers.append(
            alt.Chart(crp_smoothed)
            .mark_line(color="#1f77b4", strokeWidth=2)
            .encode(
                x=alt.X("specimen_date:T", title="Specimen date"),
                y=alt.Y("rolling_mean:Q", title="CRP (mg/L)"),
            )
        )
    else:
        layers.append(
            alt.Chart(crp_smoothed)
            .mark_line(color="#7f7f7f", opacity=0.4)
            .encode(x="specimen_date:T", y="value:Q")
        )
        layers.append(
            alt.Chart(crp_smoothed)
            .mark_line(color="#d62728", strokeWidth=2)
            .transform_loess("specimen_date", "value", bandwidth=0.4)
            .encode(
                x=alt.X("specimen_date:T", title="Specimen date"),
                y=alt.Y("value:Q", title="CRP (mg/L)"),
            )
        )

    if show_annotations.value:
        layers.append(
            alt.Chart(med_events).mark_rule(color="#d62728", strokeDash=[3, 3]).encode(x="date:T")
        )
        layers.append(
            alt.Chart(med_events)
            .mark_text(align="left", dx=4, dy=-130, color="#d62728", fontSize=11)
            .encode(x="date:T", text="label:N")
        )

    composed = alt.layer(*layers).properties(
        width=620,
        height=260,
        title="Reactive CRP chart",
    )
    composed
    return composed, layers, smoothing_label


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A note on time-axis pitfalls

        Two pitfalls are common on clinical time axes.

        Uneven sampling. Visits are not evenly spaced. A line connecting two points that are six months apart looks identical to a line connecting two points that are six weeks apart, even though the rate of change implied by the slope is very different. The remedy is to draw the sample points as filled circles on top of the line so the reader sees where the actual measurements are.

        Date-range truncation. A chart that begins on the date of the most recent treatment change omits the part of the trajectory that gives the change its meaning. The remedy is to set the x-axis range to cover the clinically relevant history (typically several years for a chronic disease), even when the most recent change is the immediate question. Track 04 returns to this in the discussion of misleading patterns.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## ESR as a second series on the same patient

        The same chart construction applied to ESR (LOINC 4537-7, reference 0 to 20 mm/h for an adult woman) yields a trajectory that mostly tracks the CRP trajectory but with two differences worth noting. ESR responds more slowly to a change in inflammation than CRP, and ESR is influenced by hemoglobin and serum proteins independently of acute-phase response. The two series rendered together (in two separate panels stacked vertically, sharing the x-axis) lets the reader see the agreement and the small discrepancies.
        """
    )
    return


@app.cell
def _(alt, med_events, pd, reyes_crp, reyes_esr):
    esr_band = pd.DataFrame([{"low": 0, "high": 20}])
    crp_panel = alt.layer(
        alt.Chart(pd.DataFrame([{"low": 0, "high": 5}]))
        .mark_rect(opacity=0.15, color="#2ca02c")
        .encode(y="low:Q", y2="high:Q"),
        alt.Chart(reyes_crp)
        .mark_line(point=True, color="#1f77b4")
        .encode(
            x=alt.X("specimen_date:T", title=""),
            y=alt.Y("value:Q", title="CRP (mg/L)"),
        ),
        alt.Chart(med_events).mark_rule(color="#d62728", strokeDash=[3, 3]).encode(x="date:T"),
    ).properties(width=620, height=180)

    esr_panel = alt.layer(
        alt.Chart(esr_band).mark_rect(opacity=0.15, color="#2ca02c").encode(y="low:Q", y2="high:Q"),
        alt.Chart(reyes_esr)
        .mark_line(point=True, color="#ff7f0e")
        .encode(
            x=alt.X("specimen_date:T", title="Specimen date"),
            y=alt.Y("value:Q", title="ESR (mm/h)"),
        ),
        alt.Chart(med_events).mark_rule(color="#d62728", strokeDash=[3, 3]).encode(x="date:T"),
    ).properties(width=620, height=180)

    two_panel_chart = alt.vconcat(crp_panel, esr_panel).properties(
        title="Ms. Reyes: CRP and ESR in stacked panels (correct two-series construction)"
    )
    two_panel_chart
    return crp_panel, esr_band, esr_panel, two_panel_chart


@app.cell
def _(mo):
    mo.md(
        r"""
        The stacked-panel construction is the correct way to display two related but differently-scaled clinical series. Each panel has its own y-axis, labeled in its own units, and the shared x-axis lets the reader read the two series in time alignment. The same data on a dual-y-axis chart (Track 04) is the misleading construction.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "08",
        "07",
        "Loading data from a cached CSV in the WASM build",
        "The lab series above is loaded from `cache/labs.csv`, which is a symlink to `start-here/patients/elena-reyes/labs.csv`. The site-absolute-URL pattern used by `load_cached_csv` is the same WASM pattern Course 07 uses for its OMOP CSVs.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        A clinically useful longitudinal chart shows the trajectory and the context. Three decisions determine the context: whether to draw the reference-range band, whether to annotate the medication changes that explain inflections, and whether to smooth the line. The recommended default for a CRP or ESR series is the raw line with the reference-range band shaded behind it and the load-bearing medication changes marked as vertical reference lines. Smoothing is added only when visit-to-visit noise obscures the underlying trajectory. Two related series on the same patient should be drawn in stacked panels sharing the x-axis, not on a dual-y-axis chart.

        Track 03 takes up the related question of how to display the uncertainty in the underlying value: when is a confidence band appropriate, when is a prediction band appropriate, and what does each one claim about the data.
        """
    )
    return


if __name__ == "__main__":
    app.run()
