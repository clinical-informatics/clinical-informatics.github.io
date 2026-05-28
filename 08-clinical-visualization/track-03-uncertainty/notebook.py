"""Track 03: Visualizing uncertainty.

Three uncertainty objects are defined and contrasted on the same dataset: the
standard error of the mean, the confidence interval, and the prediction
interval. Each makes a different claim about the data and each draws a
different band on a chart. The notebook shows the three side by side on Ms.
Reyes's CRP rolling mean, and the confidence-level slider lets the reader
watch the bands widen as the chosen coverage rises from 50% to 99%.
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
    from scipy import stats

    _COURSE_TITLES = {
        "04": "Clinical epidemiology",
        "09": "AI in medicine",
        "11": "Health economics data",
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

    _WASM_DATA_BASE = "/08-clinical-visualization/track-03-uncertainty/app"

    def load_cached_csv(filename):
        if "pyodide" in sys.modules:
            from pyodide.http import open_url
            url = f"{_WASM_DATA_BASE}/cache/{filename}"
            return pd.read_csv(open_url(url))
        return pd.read_csv(Path(__file__).parent / "cache" / filename)

    return alt, load_cached_csv, mo, np, pd, stats, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 03: Visualizing uncertainty

        ## Three uncertainty objects, three different claims

        A chart that displays a sample mean alongside a band labeled "95% CI" answers a different question than the same chart with a band labeled "95% prediction interval." The two bands have different widths and represent different claims about the data. A reader who treats them as interchangeable will misread the chart.

        Three uncertainty objects appear most often on clinical charts. Each one is defined below in terms of the question it answers, the chart it produces, and the data it makes a claim about.
        """
    )
    return


@app.cell
def _(mo, pd):
    uncertainty_table = pd.DataFrame(
        [
            {
                "Object": "Standard error of the mean (SE)",
                "Question it answers": "How precise is our estimate of the population mean?",
                "Width formula": "sd / sqrt(n)",
                "Shrinks with": "Larger sample size",
            },
            {
                "Object": "Confidence interval (CI) for the mean",
                "Question it answers": "What range plausibly contains the population mean?",
                "Width formula": "mean ± t * SE, at chosen coverage",
                "Shrinks with": "Larger sample size; lower coverage",
            },
            {
                "Object": "Prediction interval (PI) for a future observation",
                "Question it answers": "What range plausibly contains a single next observation?",
                "Width formula": "mean ± t * sd * sqrt(1 + 1/n)",
                "Shrinks with": "Larger sample size (only weakly); lower coverage",
            },
        ]
    )
    uncertainty_table.index = range(1, len(uncertainty_table) + 1)
    uncertainty_table.index.name = "row"
    mo.vstack([
        mo.md("### The three objects, in one table"),
        uncertainty_table,
    ])
    return (uncertainty_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three properties of the table are load-bearing.

        First, the CI shrinks toward zero as the sample size grows. With enough observations, the chart author is highly confident about the population mean.

        Second, the PI does not shrink toward zero. Even with infinite observations, a single future value still varies. The PI is always wider than the CI on the same data at the same coverage.

        Third, all three objects depend on the chosen coverage level. A 99% CI is wider than a 95% CI which is wider than a 50% CI on the same data. The coverage level is a chart-author decision; the data alone does not specify it.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The working dataset: Ms. Reyes's CRP in 2024 to 2026

        The 10 most recent CRP values from Ms. Reyes's lab record, covering the period from January 2024 (just before the adalimumab addition) through April 2026, form the working dataset. The chart below shows the values themselves, and the table below it reports the sample mean, the sample standard deviation, and the sample size that feed the uncertainty calculations.
        """
    )
    return


@app.cell
def _(alt, load_cached_csv, np, pd):
    labs_all = load_cached_csv("labs.csv")
    labs_all["specimen_date"] = pd.to_datetime(labs_all["specimen_date"])
    labs_all["value"] = pd.to_numeric(labs_all["value"], errors="coerce")
    reyes_crp_all = labs_all[labs_all["loinc"] == "1988-5"].copy().sort_values("specimen_date").reset_index(drop=True)
    crp_recent = reyes_crp_all.tail(10).reset_index(drop=True)

    crp_recent_chart = (
        alt.Chart(crp_recent)
        .mark_circle(size=120, color="#1f77b4")
        .encode(
            x=alt.X("specimen_date:T", title="Specimen date"),
            y=alt.Y("value:Q", title="CRP (mg/L)"),
            tooltip=["specimen_date:T", "value:Q"],
        )
        .properties(
            width=560,
            height=220,
            title="Ms. Reyes CRP: 10 most recent values (the working dataset for this track)",
        )
    )

    n = len(crp_recent)
    mean_val = crp_recent["value"].mean()
    sd_val = crp_recent["value"].std(ddof=1)
    se_val = sd_val / np.sqrt(n)
    sample_stats = pd.DataFrame(
        [
            {"Statistic": "n", "Value": f"{n}"},
            {"Statistic": "mean (mg/L)", "Value": f"{mean_val:.2f}"},
            {"Statistic": "sd (mg/L)", "Value": f"{sd_val:.2f}"},
            {"Statistic": "SE of the mean (mg/L)", "Value": f"{se_val:.2f}"},
        ]
    )
    sample_stats.index = range(1, len(sample_stats) + 1)
    crp_recent_chart
    return (
        crp_recent,
        crp_recent_chart,
        labs_all,
        mean_val,
        n,
        reyes_crp_all,
        sample_stats,
        sd_val,
        se_val,
    )


@app.cell
def _(sample_stats):
    sample_stats
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Three displays of the same uncertainty

        The chart below shows the sample mean as a horizontal line and three different uncertainty bands around it: the SE band (narrowest), the 95% CI (wider), and the 95% prediction interval (widest). Each band makes a different claim about the data. All three are drawn from the same 10 values.
        """
    )
    return


@app.cell
def _(alt, crp_recent, mean_val, n, np, pd, sd_val, se_val, stats):
    t_95 = stats.t.ppf(0.975, df=n - 1)
    ci_low = mean_val - t_95 * se_val
    ci_high = mean_val + t_95 * se_val
    pi_half = t_95 * sd_val * np.sqrt(1 + 1 / n)
    pi_low = mean_val - pi_half
    pi_high = mean_val + pi_half
    se_low = mean_val - se_val
    se_high = mean_val + se_val

    x_min = crp_recent["specimen_date"].min()
    x_max = crp_recent["specimen_date"].max()

    band_rows = pd.DataFrame(
        [
            {"label": "SE band (mean +/- SE)", "low": se_low, "high": se_high, "color": "#7f7f7f"},
            {"label": "95% CI for the mean", "low": ci_low, "high": ci_high, "color": "#1f77b4"},
            {"label": "95% prediction interval", "low": pi_low, "high": pi_high, "color": "#d62728"},
        ]
    )
    band_rows["x_min"] = x_min
    band_rows["x_max"] = x_max

    band_layer = (
        alt.Chart(band_rows)
        .mark_rect(opacity=0.18)
        .encode(
            x="x_min:T",
            x2="x_max:T",
            y="low:Q",
            y2="high:Q",
            color=alt.Color("label:N", scale=alt.Scale(domain=band_rows["label"].tolist(), range=band_rows["color"].tolist())),
        )
    )
    mean_layer = (
        alt.Chart(pd.DataFrame({"mean": [mean_val]}))
        .mark_rule(color="black", strokeWidth=2)
        .encode(y="mean:Q")
    )
    points_layer = (
        alt.Chart(crp_recent)
        .mark_circle(size=120, color="black")
        .encode(
            x="specimen_date:T",
            y=alt.Y("value:Q", title="CRP (mg/L)"),
            tooltip=["specimen_date:T", "value:Q"],
        )
    )
    three_band_chart = (band_layer + mean_layer + points_layer).properties(
        width=560,
        height=300,
        title="Sample mean (black line) with SE band, 95% CI, and 95% prediction interval",
    )
    three_band_chart
    return (
        band_layer,
        band_rows,
        ci_high,
        ci_low,
        mean_layer,
        pi_half,
        pi_high,
        pi_low,
        points_layer,
        se_high,
        se_low,
        t_95,
        three_band_chart,
        x_max,
        x_min,
    )


@app.cell
def _(ci_high, ci_low, mean_val, mo, pi_high, pi_low, se_high, se_low):
    width_summary = mo.md(
        f"""
        For Ms. Reyes's 10 most recent CRP values (mean = {mean_val:.2f} mg/L), the three bands are:

        - **SE band**: {se_low:.2f} to {se_high:.2f} mg/L
        - **95% CI for the mean**: {ci_low:.2f} to {ci_high:.2f} mg/L
        - **95% prediction interval**: {pi_low:.2f} to {pi_high:.2f} mg/L

        The 95% CI is the right band to display when the question is "what is Ms. Reyes's average CRP in this period." The 95% prediction interval is the right band to display when the question is "what is the plausible range of her next CRP value." The SE band is rarely the right display on its own; it is a building block for the CI rather than a claim about the data.
        """
    )
    width_summary
    return (width_summary,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The confidence-level slider

        The bands above all use 95% as the chosen coverage. The coverage is a chart-author decision and not a property of the data. The slider below lets the reader vary the coverage from 50% to 99% and watch the CI and prediction-interval bands widen as the coverage rises. The point estimate (the black line) does not move; the uncertainty around it does.
        """
    )
    return


@app.cell
def _(mo):
    coverage_slider = mo.ui.slider(start=50, stop=99, step=1, value=95, label="Coverage (%)", show_value=True)
    coverage_slider
    return (coverage_slider,)


@app.cell
def _(
    alt,
    coverage_slider,
    crp_recent,
    mean_val,
    n,
    np,
    pd,
    sd_val,
    se_val,
    stats,
    x_max,
    x_min,
):
    coverage_frac = coverage_slider.value / 100
    alpha = 1 - coverage_frac
    t_cov = stats.t.ppf(1 - alpha / 2, df=n - 1)
    ci_low_cov = mean_val - t_cov * se_val
    ci_high_cov = mean_val + t_cov * se_val
    pi_half_cov = t_cov * sd_val * np.sqrt(1 + 1 / n)
    pi_low_cov = mean_val - pi_half_cov
    pi_high_cov = mean_val + pi_half_cov

    band_rows_cov = pd.DataFrame(
        [
            {"label": f"{coverage_slider.value}% CI for the mean", "low": ci_low_cov, "high": ci_high_cov, "color": "#1f77b4"},
            {"label": f"{coverage_slider.value}% prediction interval", "low": pi_low_cov, "high": pi_high_cov, "color": "#d62728"},
        ]
    )
    band_rows_cov["x_min"] = x_min
    band_rows_cov["x_max"] = x_max

    cov_band_layer = (
        alt.Chart(band_rows_cov)
        .mark_rect(opacity=0.2)
        .encode(
            x="x_min:T",
            x2="x_max:T",
            y="low:Q",
            y2="high:Q",
            color=alt.Color("label:N", scale=alt.Scale(domain=band_rows_cov["label"].tolist(), range=band_rows_cov["color"].tolist())),
        )
    )
    cov_mean_layer = (
        alt.Chart(pd.DataFrame({"mean": [mean_val]}))
        .mark_rule(color="black", strokeWidth=2)
        .encode(y="mean:Q")
    )
    cov_points_layer = (
        alt.Chart(crp_recent)
        .mark_circle(size=120, color="black")
        .encode(
            x="specimen_date:T",
            y=alt.Y("value:Q", title="CRP (mg/L)", scale=alt.Scale(domain=[-5, 35])),
            tooltip=["specimen_date:T", "value:Q"],
        )
    )
    coverage_chart = (cov_band_layer + cov_mean_layer + cov_points_layer).properties(
        width=560,
        height=300,
        title=f"CRP mean with {coverage_slider.value}% CI (blue) and {coverage_slider.value}% prediction interval (red)",
    )
    coverage_chart
    return (
        alpha,
        band_rows_cov,
        ci_high_cov,
        ci_low_cov,
        cov_band_layer,
        cov_mean_layer,
        cov_points_layer,
        coverage_chart,
        coverage_frac,
        pi_half_cov,
        pi_high_cov,
        pi_low_cov,
        t_cov,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
        Two patterns are visible as the slider moves.

        The CI band widens with coverage but stays narrow even at 99%. The CI describes uncertainty about the population mean; with 10 observations clustered fairly tightly, the mean is well-estimated.

        The prediction interval widens faster and is wider than the CI at every coverage level. The PI describes the range of a single future observation; even with infinite observations of the past, a single new observation has its own variability. The PI never collapses to a point.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Distinguishing the reference range from the prediction interval

        The laboratory reference range and the prediction interval are easy to confuse and have to be kept distinct.

        The reference range is population-level and concerns a healthy reference cohort. CRP 0 to 5 mg/L means that 95% of healthy adults have a CRP in that range; it is the appropriate band to ask "is this value abnormal for the population."

        The prediction interval is individual-level and concerns the patient whose history generated it. Ms. Reyes's 95% PI is approximately 5 to 23 mg/L on her recent data; it is the appropriate band to ask "is her next value consistent with her own recent history."

        Both bands have a place. A clinician interpreting a new CRP of 18 mg/L should ask both questions. The reference range says the value is elevated (above 5). The patient-level PI says the value is consistent with her own recent trajectory (inside 5 to 23). The two answers together are the clinical reading.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "08",
        "04",
        "Confidence intervals vs p-values",
        "Course 04 Track 4 makes the case that the CI is more useful than the point estimate or the p-value for the clinical decision a chart is asked to support. The display rule here (always draw a band, choose the coverage level explicitly, label the band by what it claims about the data) operationalizes that argument visually.",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "08",
        "09",
        "Discrimination vs calibration as a visual uncertainty problem",
        "The uncertainty in a binary classifier (course 09) is displayed using the ROC curve (discrimination) and the calibration plot (probability reliability). Both are uncertainty visualizations, with a parallel structure to the CI/PI distinction: discrimination is about the model's confidence at a chosen threshold; calibration is about how well the model's stated probabilities track observed frequencies.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A note on what to choose when

        The chart should display the band that answers the question the chart is asked. A clinical dashboard for an individual patient should display the prediction interval around the patient's recent values; the dashboard answers "what is consistent with this patient's own history?" A research figure for a published cohort study should display the confidence interval around the sample mean; the figure answers "what is the population mean and how precisely is it estimated?" A laboratory report should display the reference range (typically as a band or a flag); the report answers "is this value in or out of the healthy adult range?"

        Picking the wrong band is one of the most common errors in clinical visualization. The remedy is to write down the question the chart is asked before constructing it, and to choose the uncertainty object that answers that question.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        Three uncertainty objects appear on clinical charts: the standard error of the mean, the confidence interval for the mean, and the prediction interval for a future observation. Each makes a different claim about the data and produces a band of different width on the chart. The CI shrinks toward zero with sample size; the PI does not. The chosen coverage level is a chart-author decision and the slider above demonstrates the bands widening as the chosen coverage rises. The reference range is a fourth band a clinical chart often shows, and it has to be kept distinct from the PI: the reference range concerns the population, the PI concerns the individual patient.

        Track 04 takes up the next question: when the chart author makes choices in display, axis range, or aggregation level that produce a chart that is technically correct but misleading.
        """
    )
    return


if __name__ == "__main__":
    app.run()
