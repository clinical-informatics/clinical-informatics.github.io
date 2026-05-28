"""Track 01: Choosing the right chart type.

The chart type is not a stylistic choice. It is a decision determined by the
shape of the data and the question the chart is asked to answer. This track
defines the decision, presents six clinical scenarios with the chart that
fits each one, contrasts three common mismatches against the right chart,
and closes with an interactive selector that plots Ms. Reyes's 2022 CRP
series in four different chart types so the contrast is visible.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import json
    import sys
    import types
    from pathlib import Path

    import altair as alt
    import marimo as mo
    import pandas as pd

    _COURSE_TITLES = {
        "00": "Foundations of clinical informatics",
        "02": "Data literacy",
        "04": "Clinical epidemiology",
        "05": "EHR systems",
        "07": "Data wrangling and engineering",
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

    _WASM_DATA_BASE = "/08-clinical-visualization/track-01-chart-types/app"

    def load_cached_csv(filename):
        if "pyodide" in sys.modules:
            from pyodide.http import open_url
            url = f"{_WASM_DATA_BASE}/cache/{filename}"
            return pd.read_csv(open_url(url))
        return pd.read_csv(Path(__file__).parent / "cache" / filename)

    return alt, json, load_cached_csv, mo, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 01: Choosing the right chart type

        ## The chart is a decision, not a style

        Every clinical chart is one of three things. It compares values across categories, it shows how a value changes along an ordered axis (most often time), or it shows how values are distributed across a range. The chart type is determined by which of those three the chart is asked to do and by the data type of the variables involved.

        A chart whose type does not match the question it is asked to answer misleads even when each individual datum on it is correct. A pie chart with eight categories misleads about which category is largest; a bar chart of a continuous lab trajectory misleads about whether the value is changing; a 3D bar chart misleads about the relative heights of the bars. The track that follows specifies the decision and presents the chart types that fit each clinical use.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The decision: data type to chart type

        The table below maps the combinations a clinical chart most commonly faces to the chart type that fits each one. The right column names the chart; the middle column states the question the chart answers.
        """
    )
    return


@app.cell
def _(pd):
    decision_table = pd.DataFrame(
        [
            {
                "Variables": "One continuous variable, no ordering",
                "Question the chart answers": "How are the values distributed?",
                "Chart type": "Histogram or density plot",
            },
            {
                "Variables": "One continuous variable on a time axis",
                "Question the chart answers": "How does the value change over time?",
                "Chart type": "Line chart",
            },
            {
                "Variables": "One categorical variable with counts",
                "Question the chart answers": "Which category is largest?",
                "Chart type": "Bar chart, sorted descending",
            },
            {
                "Variables": "One categorical variable, two or three categories, parts of a whole",
                "Question the chart answers": "What proportion is each category?",
                "Chart type": "Stacked bar (single bar) or 100% stacked",
            },
            {
                "Variables": "Two continuous variables, one observation each",
                "Question the chart answers": "Is one variable associated with the other?",
                "Chart type": "Scatter plot",
            },
            {
                "Variables": "One continuous variable, split by one categorical variable",
                "Question the chart answers": "How does the distribution differ across groups?",
                "Chart type": "Box plot, violin plot, or stripplot",
            },
            {
                "Variables": "Two categorical variables with counts",
                "Question the chart answers": "How does count differ across the combinations?",
                "Chart type": "Heatmap or grouped bar chart",
            },
            {
                "Variables": "Time on one axis, category on the other, event marks",
                "Question the chart answers": "When did each event occur for each category?",
                "Chart type": "Timeline or swimlane (Gantt-style)",
            },
        ]
    )
    decision_table.index = range(1, len(decision_table) + 1)
    decision_table.index.name = "row"
    decision_table
    return (decision_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three properties of the table are load-bearing for the rest of the course.

        First, the decision is determined by the data and the question, not by the author's preference. Two clinicians presented with the same dataset and the same question should select the same chart type. A clinician who selects a different chart type is asking a different question of the data.

        Second, a pie chart appears in the table only for the case of two or three categories that exhaust a whole. With four or more slices, the human visual system cannot rank slices reliably by area, and a sorted bar chart answers the same question with much higher accuracy.

        Third, a bar chart and a line chart are not interchangeable on the time axis. A bar chart treats time as a sequence of categorical bins; the visual encoding of the bar's height is the value within that bin. A line chart treats time as a continuous axis; the visual encoding of position along the line is the trajectory. The two charts answer different questions, and the right answer for clinical longitudinal data is almost always the line chart.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Six clinical scenarios with the chart that fits each one

        Each scenario below names a clinical question, identifies the data shape, and shows the chart that answers it. The intent is to make the data-to-chart decision concrete on the kinds of data a clinician actually encounters.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Scenario 1: a lab value over time for one patient

        Question: how has Ms. Reyes's CRP changed over four years? Data shape: one continuous variable on a time axis. Chart type: line chart.
        """
    )
    return


@app.cell
def _(alt, load_cached_csv, pd):
    labs_all = load_cached_csv("labs.csv")
    labs_all["specimen_date"] = pd.to_datetime(labs_all["specimen_date"])
    reyes_crp = labs_all[labs_all["loinc"] == "1988-5"].copy()
    reyes_crp["value"] = pd.to_numeric(reyes_crp["value"])

    scenario_1_chart = (
        alt.Chart(reyes_crp)
        .mark_line(point=True)
        .encode(
            x=alt.X("specimen_date:T", title="Specimen date"),
            y=alt.Y("value:Q", title="CRP (mg/L)"),
            tooltip=["specimen_date:T", "value:Q"],
        )
        .properties(
            width=600,
            height=260,
            title="Ms. Reyes: CRP over four years (line chart, correct)",
        )
    )
    scenario_1_chart
    return labs_all, reyes_crp, scenario_1_chart


@app.cell
def _(mo):
    mo.md(
        r"""
        The line chart preserves the temporal cue. The reader sees that CRP fell over the first year of treatment, climbed in 2024 around the addition of adalimumab, and stabilized in the low-elevated range by 2026.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Scenario 2: count of patients by disease category

        Question: among the 200 patients in an RA clinic, how many have which comorbidity? Data shape: one categorical variable with counts. Chart type: bar chart sorted descending.
        """
    )
    return


@app.cell
def _(alt, pd):
    comorbidity_counts = pd.DataFrame(
        [
            {"Comorbidity": "Hypertension", "Patients": 92},
            {"Comorbidity": "Hyperlipidemia", "Patients": 78},
            {"Comorbidity": "Type 2 diabetes", "Patients": 41},
            {"Comorbidity": "Depression", "Patients": 36},
            {"Comorbidity": "Osteoporosis", "Patients": 28},
            {"Comorbidity": "COPD", "Patients": 17},
            {"Comorbidity": "Chronic kidney disease", "Patients": 14},
            {"Comorbidity": "Atrial fibrillation", "Patients": 9},
        ]
    )

    scenario_2_chart = (
        alt.Chart(comorbidity_counts)
        .mark_bar()
        .encode(
            x=alt.X("Patients:Q", title="Patients"),
            y=alt.Y("Comorbidity:N", sort="-x", title=""),
            tooltip=["Comorbidity:N", "Patients:Q"],
        )
        .properties(
            width=520,
            height=240,
            title="RA clinic cohort: comorbidity counts (sorted bar, correct)",
        )
    )
    scenario_2_chart
    return comorbidity_counts, scenario_2_chart


@app.cell
def _(mo):
    mo.md(
        r"""
        The sorted bar chart makes the rank trivial to read. The visual encoding of bar length is position-based, which is the most accurately decoded of the visual channels.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Scenario 3: distribution of a continuous variable across a cohort

        Question: how is age distributed in the 200-patient RA clinic? Data shape: one continuous variable, no ordering. Chart type: histogram.
        """
    )
    return


@app.cell
def _(alt, pd):
    import numpy as np
    rng = np.random.default_rng(seed=20260527)
    ages = rng.normal(loc=58, scale=14, size=200).clip(min=18, max=92).round().astype(int)
    age_df = pd.DataFrame({"Age": ages})

    scenario_3_chart = (
        alt.Chart(age_df)
        .mark_bar()
        .encode(
            x=alt.X("Age:Q", bin=alt.Bin(step=5), title="Age (years)"),
            y=alt.Y("count():Q", title="Patients"),
            tooltip=["count():Q"],
        )
        .properties(
            width=520,
            height=240,
            title="RA clinic cohort: age distribution (histogram, correct)",
        )
    )
    scenario_3_chart
    return age_df, ages, np, rng, scenario_3_chart


@app.cell
def _(mo):
    mo.md(
        r"""
        The histogram shows the central tendency (around age 60), the spread, and the tail toward older patients. A pie chart of age groups, or a line chart with age on the x-axis and count on the y-axis, would both obscure the shape that the histogram surfaces directly.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Scenario 4: two continuous variables at one moment

        Question: in the 200-patient cohort at last visit, is DAS28 score associated with CRP? Data shape: two continuous variables, one observation per patient. Chart type: scatter plot.
        """
    )
    return


@app.cell
def _(alt, np, pd, rng):
    n = 200
    crp_values = rng.lognormal(mean=2.0, sigma=0.8, size=n).clip(min=0.5, max=120)
    das28_values = 2.0 + 0.045 * crp_values + rng.normal(0, 0.7, size=n)
    das28_values = np.clip(das28_values, 1.5, 7.5)
    crp_das28 = pd.DataFrame({"CRP_mg_L": crp_values, "DAS28": das28_values})

    scenario_4_chart = (
        alt.Chart(crp_das28)
        .mark_circle(opacity=0.5)
        .encode(
            x=alt.X("CRP_mg_L:Q", title="CRP (mg/L)"),
            y=alt.Y("DAS28:Q", title="DAS28 score"),
            tooltip=["CRP_mg_L:Q", "DAS28:Q"],
        )
        .properties(
            width=520,
            height=240,
            title="RA cohort at last visit: CRP vs DAS28 (scatter, correct)",
        )
    )
    scenario_4_chart
    return crp_das28, crp_values, das28_values, n, scenario_4_chart


@app.cell
def _(mo):
    mo.md(
        r"""
        The scatter plot answers the association question directly. A line chart would imply that the patients are ordered along the CRP axis in a meaningful sequence; they are not. A bar chart would aggregate the patients into bins and lose the per-patient resolution that the scatter preserves.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Scenario 5: one continuous variable split by a categorical variable

        Question: do CRP values differ between patients on methotrexate alone and patients on methotrexate plus a TNF inhibitor? Data shape: one continuous variable, split by one categorical variable. Chart type: box plot.
        """
    )
    return


@app.cell
def _(alt, np, pd, rng):
    n_per_group = 80
    crp_mtx = rng.lognormal(mean=2.4, sigma=0.7, size=n_per_group).clip(min=0.5, max=120)
    crp_mtx_tnfi = rng.lognormal(mean=1.7, sigma=0.8, size=n_per_group).clip(min=0.5, max=120)
    treatment_df = pd.concat(
        [
            pd.DataFrame({"Treatment": "MTX alone", "CRP_mg_L": crp_mtx}),
            pd.DataFrame({"Treatment": "MTX + TNFi", "CRP_mg_L": crp_mtx_tnfi}),
        ]
    )

    scenario_5_chart = (
        alt.Chart(treatment_df)
        .mark_boxplot(extent="min-max")
        .encode(
            x=alt.X("Treatment:N", title=""),
            y=alt.Y("CRP_mg_L:Q", title="CRP (mg/L)"),
            color=alt.Color("Treatment:N", legend=None),
        )
        .properties(
            width=420,
            height=260,
            title="RA cohort: CRP by treatment (box plot, correct)",
        )
    )
    scenario_5_chart
    return crp_mtx, crp_mtx_tnfi, n_per_group, scenario_5_chart, treatment_df


@app.cell
def _(mo):
    mo.md(
        r"""
        The box plot shows the median, the interquartile range, and the spread for each treatment group on a common y-axis. A pair of bar charts showing the means would lose all information about the distribution.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Scenario 6: events on a time axis, one row per medication

        Question: when did Ms. Reyes start and stop each medication? Data shape: time on one axis, category on the other, event marks. Chart type: timeline (Gantt-style).
        """
    )
    return


@app.cell
def _(alt, pd):
    med_timeline = pd.DataFrame(
        [
            {"Medication": "Methotrexate 25 mg SC weekly", "Start": "2022-03-07", "End": "2026-04-28"},
            {"Medication": "Folic acid 1 mg daily", "Start": "2022-03-07", "End": "2026-04-28"},
            {"Medication": "Adalimumab 40 mg SC q2wk", "Start": "2024-05-15", "End": "2026-04-28"},
            {"Medication": "Prednisone 5 mg daily (taper)", "Start": "2025-01-12", "End": "2025-04-30"},
            {"Medication": "Naproxen 500 mg BID PRN", "Start": "2022-03-07", "End": "2024-05-15"},
        ]
    )
    med_timeline["Start"] = pd.to_datetime(med_timeline["Start"])
    med_timeline["End"] = pd.to_datetime(med_timeline["End"])

    scenario_6_chart = (
        alt.Chart(med_timeline)
        .mark_bar(size=14)
        .encode(
            x=alt.X("Start:T", title="Date"),
            x2="End:T",
            y=alt.Y("Medication:N", sort=None, title=""),
            tooltip=["Medication:N", "Start:T", "End:T"],
        )
        .properties(
            width=600,
            height=200,
            title="Ms. Reyes: medication timeline (Gantt-style, correct)",
        )
    )
    scenario_6_chart
    return med_timeline, scenario_6_chart


@app.cell
def _(mo):
    mo.md(
        r"""
        The timeline preserves the duration and the overlap. A clinician looking at this chart can see at a glance that adalimumab was added in May 2024 while methotrexate continued, and that naproxen was stopped at the same time. A bar chart of total days on each medication would lose the temporal pattern entirely.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Three mismatches that mislead

        Each mismatch below shows the misleading chart and the chart that should have been drawn instead. The data is identical in each pair. The visual difference between the two is the cost of the mismatch.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Mismatch 1: a pie chart for eight categories

        The same comorbidity data from Scenario 2, rendered as a pie chart. With eight slices, ranking by area is unreliable. The reader cannot tell at a glance which of hypertension and hyperlipidemia is larger, or how the four smallest categories compare with one another.
        """
    )
    return


@app.cell
def _(alt, comorbidity_counts):
    pie_mismatch = (
        alt.Chart(comorbidity_counts)
        .mark_arc()
        .encode(
            theta=alt.Theta("Patients:Q"),
            color=alt.Color("Comorbidity:N"),
            tooltip=["Comorbidity:N", "Patients:Q"],
        )
        .properties(
            width=360,
            height=300,
            title="Comorbidity counts as a pie chart (misleading)",
        )
    )
    pie_mismatch
    return (pie_mismatch,)


@app.cell
def _(mo):
    mo.md(
        r"""
        The sorted bar chart from Scenario 2 ranks the same data without ambiguity. The rule is unconditional for four or more categories: replace the pie with a sorted bar.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Mismatch 2: a bar chart for a longitudinal lab value

        The same CRP series from Scenario 1, rendered as a bar chart. The bar chart treats each specimen date as a discrete bin and breaks the visual cue that the values are sampled from a continuous trajectory. The reader can no longer see the decline-then-rise-then-stabilize shape that the line chart surfaces.
        """
    )
    return


@app.cell
def _(alt, reyes_crp):
    bar_mismatch = (
        alt.Chart(reyes_crp)
        .mark_bar()
        .encode(
            x=alt.X("specimen_date:T", title="Specimen date"),
            y=alt.Y("value:Q", title="CRP (mg/L)"),
            tooltip=["specimen_date:T", "value:Q"],
        )
        .properties(
            width=600,
            height=260,
            title="Ms. Reyes CRP as a bar chart (misleading)",
        )
    )
    bar_mismatch
    return (bar_mismatch,)


@app.cell
def _(mo):
    mo.md(
        r"""
        The line chart from Scenario 1 preserves the trajectory. The rule is unconditional for continuous longitudinal data sampled at irregular intervals: use a line chart with points marked at the sample dates.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Mismatch 3: dual-y-axis on two unrelated scales

        Two variables with no shared natural scale (CRP in mg/L and DAS28 score, unit-less) plotted against two y-axes that share an x-axis. The visual impression of correlation is determined by where the chart author chose to start and end each y-axis, not by the data.
        """
    )
    return


@app.cell
def _(alt, np, pd, reyes_crp, rng):
    reyes_das28 = pd.DataFrame(
        {
            "specimen_date": reyes_crp["specimen_date"].values,
            "DAS28": (2.5 + 0.030 * reyes_crp["value"].values + rng.normal(0, 0.25, len(reyes_crp))).clip(1.5, 6.5),
        }
    )
    crp_line = (
        alt.Chart(reyes_crp)
        .mark_line(color="#1f77b4", point=True)
        .encode(
            x=alt.X("specimen_date:T", title="Specimen date"),
            y=alt.Y("value:Q", title="CRP (mg/L)", scale=alt.Scale(domain=[0, 50])),
        )
    )
    das_line = (
        alt.Chart(reyes_das28)
        .mark_line(color="#d62728", point=True, strokeDash=[4, 2])
        .encode(
            x="specimen_date:T",
            y=alt.Y("DAS28:Q", title="DAS28 score", scale=alt.Scale(domain=[2, 6])),
        )
    )
    dual_axis_mismatch = alt.layer(crp_line, das_line).resolve_scale(y="independent").properties(
        width=600,
        height=260,
        title="CRP and DAS28 on dual y-axes (misleading)",
    )
    dual_axis_mismatch
    return crp_line, das_line, dual_axis_mismatch, reyes_das28


@app.cell
def _(mo):
    mo.md(
        r"""
        The honest alternative is two separate panels stacked vertically, sharing the x-axis but each with its own y-axis explicitly labeled, or a scatter plot of one variable against the other if association is the question. Dual-y-axis charts are addressed in detail in Track 04 as one of the recurring misleading patterns.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Interactive: the same data, four chart types

        The selector below plots Ms. Reyes's 2022 CRP series (four data points, the first year of treatment) in four chart types. Three of them are mismatches for this data; one is the right answer. Switch among them and confirm by inspection that only one preserves the trajectory clearly.
        """
    )
    return


@app.cell
def _(mo):
    chart_picker = mo.ui.dropdown(
        options=["Line chart", "Bar chart", "Scatter plot", "Pie chart"],
        value="Line chart",
        label="Chart type",
    )
    chart_picker
    return (chart_picker,)


@app.cell
def _(alt, chart_picker, mo, pd, reyes_crp):
    crp_2022 = reyes_crp[reyes_crp["specimen_date"].dt.year == 2022].copy()
    crp_2022["date_str"] = crp_2022["specimen_date"].dt.strftime("%Y-%m-%d")

    chart_type = chart_picker.value
    if chart_type == "Line chart":
        rendered = (
            alt.Chart(crp_2022)
            .mark_line(point=True)
            .encode(
                x=alt.X("specimen_date:T", title="Specimen date"),
                y=alt.Y("value:Q", title="CRP (mg/L)"),
                tooltip=["specimen_date:T", "value:Q"],
            )
            .properties(width=520, height=240, title="Line chart")
        )
        note = "Line chart. Correct. The trajectory and the spacing between specimens are both visible."
    elif chart_type == "Bar chart":
        rendered = (
            alt.Chart(crp_2022)
            .mark_bar()
            .encode(
                x=alt.X("date_str:N", title="Specimen date"),
                y=alt.Y("value:Q", title="CRP (mg/L)"),
                tooltip=["date_str:N", "value:Q"],
            )
            .properties(width=520, height=240, title="Bar chart")
        )
        note = "Bar chart. Misleading. The dates are treated as discrete categories and the time axis is no longer continuous."
    elif chart_type == "Scatter plot":
        rendered = (
            alt.Chart(crp_2022)
            .mark_circle(size=120)
            .encode(
                x=alt.X("specimen_date:T", title="Specimen date"),
                y=alt.Y("value:Q", title="CRP (mg/L)"),
                tooltip=["specimen_date:T", "value:Q"],
            )
            .properties(width=520, height=240, title="Scatter plot")
        )
        note = "Scatter plot. Defensible but suboptimal. The temporal cue is preserved by the x-axis, but the visual line that connects the samples is missing; the reader has to construct it mentally."
    else:
        rendered = (
            alt.Chart(crp_2022)
            .mark_arc()
            .encode(
                theta="value:Q",
                color="date_str:N",
                tooltip=["date_str:N", "value:Q"],
            )
            .properties(width=320, height=280, title="Pie chart")
        )
        note = "Pie chart. Wrong. CRP values at different specimen dates are not parts of a whole. The chart implies a part-to-whole relationship that does not exist in the data."

    mo.vstack([rendered, mo.callout(mo.md(note), kind="info")])
    return chart_type, crp_2022, note, rendered


@app.cell
def _(mo, xref):
    xref.forward(
        "08",
        "11",
        "Decision curve analysis (DCA) as a specialized chart type",
        "DCA is a chart type designed to answer one question (does acting on this test improve net benefit at a given threshold?). It is the clinical chart that does not fit the data-type-to-chart-type decision because it encodes a clinical-utility framework rather than the raw data shape. Course 11 introduces it.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        The chart type is determined by the data type and the question the chart answers. The decision table above maps the common combinations to the chart that fits each one. Six clinical scenarios specify the right chart for the kinds of data clinicians actually encounter. Three mismatches (the multi-slice pie, the longitudinal bar, the dual-axis) misrepresent the same data the right chart would render correctly.

        Track 02 addresses the chart type that carries most clinical longitudinal data (the line chart) in detail: reference-range bands, medication-change annotations, and smoothing decisions are each addressed there.
        """
    )
    return


if __name__ == "__main__":
    app.run()
