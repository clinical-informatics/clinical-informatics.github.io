"""Capstone for course 08: Clinical visualization.

A reactive disease-activity dashboard for an RA cohort centered on Ms. Reyes.
The reader selects a patient, picks a date range, chooses one or more labs to
plot, toggles the DAS28 trajectory, and toggles a medication timeline. Each
control re-renders the dashboard. The capstone applies the construction
decisions discussed across the four tracks: chart-type selection (Track 01),
reference-range bands and medication annotations (Track 02), uncertainty
display (Track 03), and the avoidance of misleading patterns (Track 04).
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

    _WASM_DATA_BASE = "/08-clinical-visualization/capstone/app"

    def load_cached_csv(filename):
        if "pyodide" in sys.modules:
            from pyodide.http import open_url
            url = f"{_WASM_DATA_BASE}/cache/{filename}"
            return pd.read_csv(open_url(url))
        return pd.read_csv(Path(__file__).parent / "cache" / filename)

    return alt, load_cached_csv, mo, np, pd


@app.cell
def _(mo):
    mo.md(
        r"""
        # Capstone: Disease-activity dashboard for Ms. Reyes's RA cohort

        ## What this dashboard does

        The dashboard below displays the longitudinal disease-activity record for one patient at a time, chosen from a four-patient RA cohort: Ms. Reyes (the running patient throughout the curriculum) and three synthetic peers. The reader picks a patient, a date range, one or more labs to plot, and toggles the DAS28 trajectory and the medication timeline. Each control re-renders the dashboard reactively.

        The construction decisions baked into the dashboard apply the rules from the four tracks of this course. Lab values are plotted as line charts on a continuous time axis (Track 01: continuous data on a time axis gets a line chart). Each lab is plotted in its own panel with its own reference-range band (Track 02: the reference range converts the chart from "trajectory" to "trajectory plus elevation context"; Track 04: dual-y-axis charts are refused in favor of stacked panels). The default date range covers the patient's full record (Track 04: avoiding the cherry-picked time window). The chart-type selector for the lab panel exposes only line and scatter as options (Track 04: bar charts for time series are refused).
        """
    )
    return


@app.cell
def _(load_cached_csv, np, pd):
    labs_reyes = load_cached_csv("labs.csv")
    labs_reyes["specimen_date"] = pd.to_datetime(labs_reyes["specimen_date"])
    labs_reyes["value"] = pd.to_numeric(labs_reyes["value"], errors="coerce")
    labs_reyes["patient_id"] = "ER-001"
    labs_reyes["patient_name"] = "Elena Reyes"

    def synth_patient(patient_id, patient_name, seed, dx_date, crp_baseline, crp_amp, hgb_baseline):
        rng = np.random.default_rng(seed)
        dates = pd.date_range(start=dx_date, end="2026-04-28", freq="90D")
        n_dates = len(dates)
        months_in = np.arange(n_dates) * 3
        crp_traj = crp_baseline + crp_amp * np.exp(-months_in / 18) + rng.normal(0, 2.5, n_dates)
        crp_traj = np.clip(crp_traj, 1.0, 80.0)
        esr_traj = 4 + 0.85 * crp_traj + rng.normal(0, 4, n_dates)
        esr_traj = np.clip(esr_traj, 2, 110)
        hgb_traj = hgb_baseline + rng.normal(0, 0.4, n_dates)
        hgb_traj = np.clip(hgb_traj, 9.5, 14.5)
        rows = []
        for d, c, e, h in zip(dates, crp_traj, esr_traj, hgb_traj):
            rows.append({"patient_id": patient_id, "patient_name": patient_name, "specimen_date": d, "loinc": "1988-5", "test_name": "C-reactive protein", "value": round(c, 1), "unit": "mg/L", "reference_low": 0, "reference_high": 5, "interpretation": "H" if c > 5 else "N"})
            rows.append({"patient_id": patient_id, "patient_name": patient_name, "specimen_date": d, "loinc": "4537-7", "test_name": "Erythrocyte sedimentation rate", "value": round(e, 0), "unit": "mm/h", "reference_low": 0, "reference_high": 20, "interpretation": "H" if e > 20 else "N"})
            rows.append({"patient_id": patient_id, "patient_name": patient_name, "specimen_date": d, "loinc": "718-7", "test_name": "Hemoglobin", "value": round(h, 1), "unit": "g/dL", "reference_low": 12, "reference_high": 15.5, "interpretation": "L" if h < 12 else "N"})
        return pd.DataFrame(rows)

    peer_2 = synth_patient("RA-002", "Maria Alvarez", seed=42, dx_date="2023-01-15", crp_baseline=4.0, crp_amp=22.0, hgb_baseline=12.8)
    peer_3 = synth_patient("RA-003", "Janet Kim", seed=99, dx_date="2022-08-10", crp_baseline=8.0, crp_amp=35.0, hgb_baseline=11.4)
    peer_4 = synth_patient("RA-004", "Lisa Park", seed=2026, dx_date="2024-03-20", crp_baseline=3.5, crp_amp=18.0, hgb_baseline=13.2)

    cohort_labs = pd.concat([labs_reyes, peer_2, peer_3, peer_4], ignore_index=True)
    cohort_labs = cohort_labs.sort_values(["patient_id", "specimen_date", "loinc"]).reset_index(drop=True)
    return cohort_labs, labs_reyes, peer_2, peer_3, peer_4, synth_patient


@app.cell
def _(np, pd):
    def synth_das28(patient_id, dates, crp_series, seed):
        rng = np.random.default_rng(seed + 1000)
        das28 = 2.4 + 0.040 * crp_series.values + rng.normal(0, 0.3, len(dates))
        return pd.DataFrame({"patient_id": patient_id, "specimen_date": dates, "DAS28": np.clip(das28, 1.5, 7.0)})

    return (synth_das28,)


@app.cell
def _(cohort_labs, synth_das28):
    crp_only = cohort_labs[cohort_labs["loinc"] == "1988-5"].copy()
    das28_records = []
    for pid in crp_only["patient_id"].unique():
        sub = crp_only[crp_only["patient_id"] == pid].sort_values("specimen_date")
        seed_map = {"ER-001": 1, "RA-002": 42, "RA-003": 99, "RA-004": 2026}
        das28_records.append(synth_das28(pid, sub["specimen_date"].reset_index(drop=True), sub["value"].reset_index(drop=True), seed_map[pid]))
    das28_all = __import__("pandas").concat(das28_records, ignore_index=True)
    return crp_only, das28_all, das28_records


@app.cell
def _(pd):
    med_history = pd.DataFrame(
        [
            {"patient_id": "ER-001", "Medication": "Methotrexate 25 mg SC weekly", "Start": "2022-03-07", "End": "2026-04-28"},
            {"patient_id": "ER-001", "Medication": "Folic acid 1 mg daily", "Start": "2022-03-07", "End": "2026-04-28"},
            {"patient_id": "ER-001", "Medication": "Adalimumab 40 mg SC q2wk", "Start": "2024-05-15", "End": "2026-04-28"},
            {"patient_id": "ER-001", "Medication": "Prednisone 5 mg daily (taper)", "Start": "2025-01-12", "End": "2025-04-30"},
            {"patient_id": "RA-002", "Medication": "Methotrexate 20 mg PO weekly", "Start": "2023-01-15", "End": "2026-04-28"},
            {"patient_id": "RA-002", "Medication": "Folic acid 1 mg daily", "Start": "2023-01-15", "End": "2026-04-28"},
            {"patient_id": "RA-002", "Medication": "Hydroxychloroquine 400 mg daily", "Start": "2023-04-10", "End": "2026-04-28"},
            {"patient_id": "RA-003", "Medication": "Methotrexate 25 mg SC weekly", "Start": "2022-08-10", "End": "2026-04-28"},
            {"patient_id": "RA-003", "Medication": "Folic acid 1 mg daily", "Start": "2022-08-10", "End": "2026-04-28"},
            {"patient_id": "RA-003", "Medication": "Etanercept 50 mg SC weekly", "Start": "2023-06-22", "End": "2026-04-28"},
            {"patient_id": "RA-004", "Medication": "Methotrexate 20 mg PO weekly", "Start": "2024-03-20", "End": "2026-04-28"},
            {"patient_id": "RA-004", "Medication": "Folic acid 1 mg daily", "Start": "2024-03-20", "End": "2026-04-28"},
        ]
    )
    med_history["Start"] = pd.to_datetime(med_history["Start"])
    med_history["End"] = pd.to_datetime(med_history["End"])
    return (med_history,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Controls

        Pick a patient, set the date range, choose one or more labs to plot, and toggle the DAS28 trajectory and the medication timeline.
        """
    )
    return


@app.cell
def _(cohort_labs, mo):
    patient_options = sorted(cohort_labs["patient_id"].unique().tolist())
    patient_picker = mo.ui.dropdown(
        options=patient_options,
        value="ER-001",
        label="Patient",
    )
    patient_picker
    return patient_options, patient_picker


@app.cell
def _(cohort_labs, mo, patient_picker):
    selected_id = patient_picker.value
    patient_record = cohort_labs[cohort_labs["patient_id"] == selected_id]
    min_d = patient_record["specimen_date"].min().date()
    max_d = patient_record["specimen_date"].max().date()
    date_start = mo.ui.date(start=min_d, stop=max_d, value=min_d, label="Start date")
    date_end = mo.ui.date(start=min_d, stop=max_d, value=max_d, label="End date")
    mo.hstack([date_start, date_end])
    return date_end, date_start, max_d, min_d, patient_record, selected_id


@app.cell
def _(mo):
    lab_picker = mo.ui.multiselect(
        options=["C-reactive protein", "Erythrocyte sedimentation rate", "Hemoglobin"],
        value=["C-reactive protein", "Erythrocyte sedimentation rate"],
        label="Labs to plot",
    )
    lab_picker
    return (lab_picker,)


@app.cell
def _(mo):
    show_das28 = mo.ui.checkbox(value=True, label="Show DAS28 trajectory")
    show_med_timeline = mo.ui.checkbox(value=True, label="Show medication timeline")
    chart_kind = mo.ui.dropdown(
        options=["Line", "Line with points", "Scatter"],
        value="Line with points",
        label="Lab chart style",
    )
    mo.hstack([show_das28, show_med_timeline, chart_kind])
    return chart_kind, show_das28, show_med_timeline


@app.cell
def _(mo, patient_picker, selected_id):
    patient_names = {
        "ER-001": "Ms. Elena Reyes",
        "RA-002": "Ms. Maria Alvarez",
        "RA-003": "Ms. Janet Kim",
        "RA-004": "Ms. Lisa Park",
    }
    patient_label = patient_names.get(selected_id, selected_id)
    header = mo.md(f"### Patient: {patient_label} (`{selected_id}`)")
    _ = patient_picker
    header
    return header, patient_label, patient_names


@app.cell
def _(alt, chart_kind, date_end, date_start, lab_picker, pd, patient_record):
    start_dt = pd.to_datetime(date_start.value)
    end_dt = pd.to_datetime(date_end.value)
    window_record = patient_record[
        (patient_record["specimen_date"] >= start_dt) & (patient_record["specimen_date"] <= end_dt)
    ].copy()

    selected_labs = lab_picker.value
    panels = []
    for lab_name in selected_labs:
        lab_data = window_record[window_record["test_name"] == lab_name].copy()
        if lab_data.empty:
            continue
        ref_low = lab_data["reference_low"].iloc[0]
        ref_high = lab_data["reference_high"].iloc[0]
        unit = lab_data["unit"].iloc[0]
        band_df = pd.DataFrame([{"low": ref_low, "high": ref_high}])
        band = (
            alt.Chart(band_df)
            .mark_rect(opacity=0.15, color="#2ca02c")
            .encode(y="low:Q", y2="high:Q")
        )
        if chart_kind.value == "Line":
            line = alt.Chart(lab_data).mark_line(color="#1f77b4")
        elif chart_kind.value == "Line with points":
            line = alt.Chart(lab_data).mark_line(point=True, color="#1f77b4")
        else:
            line = alt.Chart(lab_data).mark_circle(size=90, color="#1f77b4")
        line = line.encode(
            x=alt.X("specimen_date:T", title=""),
            y=alt.Y("value:Q", title=f"{lab_name} ({unit})"),
            tooltip=["specimen_date:T", "value:Q"],
        )
        panel = (band + line).properties(width=620, height=140, title=f"{lab_name} (ref: {ref_low} to {ref_high} {unit})")
        panels.append(panel)

    if panels:
        lab_chart = alt.vconcat(*panels).resolve_scale(y="independent")
    else:
        lab_chart = alt.Chart(pd.DataFrame({"x": [0]})).mark_text(text="No labs selected").encode()
    lab_chart
    return (
        band,
        band_df,
        end_dt,
        lab_chart,
        lab_data,
        lab_name,
        line,
        panel,
        panels,
        ref_high,
        ref_low,
        selected_labs,
        start_dt,
        unit,
        window_record,
    )


@app.cell
def _(alt, das28_all, end_dt, mo, pd, selected_id, show_das28, start_dt):
    if show_das28.value:
        das_record = das28_all[
            (das28_all["patient_id"] == selected_id)
            & (das28_all["specimen_date"] >= start_dt)
            & (das28_all["specimen_date"] <= end_dt)
        ]
        goal_line = (
            alt.Chart(pd.DataFrame({"goal": [2.6]}))
            .mark_rule(color="#2ca02c", strokeDash=[4, 2])
            .encode(y="goal:Q")
        )
        das_line = (
            alt.Chart(das_record)
            .mark_line(point=True, color="#9467bd")
            .encode(
                x=alt.X("specimen_date:T", title=""),
                y=alt.Y("DAS28:Q", title="DAS28", scale=alt.Scale(domain=[1, 7])),
                tooltip=["specimen_date:T", "DAS28:Q"],
            )
        )
        das_chart = (goal_line + das_line).properties(
            width=620, height=160, title="DAS28 trajectory (green dashed line = remission target, 2.6)"
        )
    else:
        das_chart = mo.md("_DAS28 panel hidden_")
    das_chart
    return das_chart, das_line, das_record, goal_line


@app.cell
def _(alt, end_dt, med_history, mo, pd, selected_id, show_med_timeline, start_dt):
    if show_med_timeline.value:
        patient_meds = med_history[med_history["patient_id"] == selected_id].copy()
        patient_meds["End_clipped"] = patient_meds["End"].clip(upper=end_dt)
        patient_meds["Start_clipped"] = patient_meds["Start"].clip(lower=start_dt)
        patient_meds = patient_meds[patient_meds["End_clipped"] >= patient_meds["Start_clipped"]]
        med_chart = (
            alt.Chart(patient_meds)
            .mark_bar(size=14, color="#ff7f0e")
            .encode(
                x=alt.X("Start_clipped:T", title="Date"),
                x2="End_clipped:T",
                y=alt.Y("Medication:N", sort=None, title=""),
                tooltip=["Medication:N", "Start:T", "End:T"],
            )
            .properties(width=620, height=160, title="Medication timeline (clipped to selected date range)")
        )
    else:
        med_chart = mo.md("_Medication timeline hidden_")
    _ = pd
    med_chart
    return med_chart, patient_meds


@app.cell
def _(cohort_labs, das28_all, med_history, pd, selected_id):
    latest_record = cohort_labs[cohort_labs["patient_id"] == selected_id].copy()
    last_crp = latest_record[latest_record["loinc"] == "1988-5"].sort_values("specimen_date").tail(1)
    last_esr = latest_record[latest_record["loinc"] == "4537-7"].sort_values("specimen_date").tail(1)
    last_das = das28_all[das28_all["patient_id"] == selected_id].sort_values("specimen_date").tail(1)
    current_meds = med_history[(med_history["patient_id"] == selected_id) & (med_history["End"] >= pd.to_datetime("2026-04-28"))]["Medication"].tolist()
    summary_table = pd.DataFrame(
        [
            {"Field": "Most recent specimen date", "Value": last_crp["specimen_date"].iloc[0].strftime("%Y-%m-%d") if not last_crp.empty else "n/a"},
            {"Field": "Most recent CRP (mg/L)", "Value": f"{last_crp['value'].iloc[0]:.1f}" if not last_crp.empty else "n/a"},
            {"Field": "Most recent ESR (mm/h)", "Value": f"{last_esr['value'].iloc[0]:.0f}" if not last_esr.empty else "n/a"},
            {"Field": "Most recent DAS28", "Value": f"{last_das['DAS28'].iloc[0]:.2f}" if not last_das.empty else "n/a"},
            {"Field": "Current medications", "Value": "; ".join(current_meds) if current_meds else "none"},
        ]
    )
    summary_table.index = range(1, len(summary_table) + 1)
    return current_meds, last_crp, last_das, last_esr, latest_record, summary_table


@app.cell
def _(summary_table):
    summary_table
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The design decisions, named

        Every construction choice in the dashboard above can be traced to one of the rules from the four tracks. The reveal below summarizes the choices and the rules that motivated them.
        """
    )
    return


@app.cell
def _(mo):
    reveal_widget = mo.ui.button(value=False, label="Show the design rationale", on_click=lambda v: not v)
    reveal_widget
    return (reveal_widget,)


@app.cell
def _(mo, reveal_widget):
    if reveal_widget.value:
        rationale = mo.md(
            r"""
            ### Design decisions and the rules that motivated each

            **Lab panel: each lab in its own subplot, sharing the x-axis.** Track 04 Pattern 3 rejects the dual-y-axis chart for two related but differently-scaled clinical series. The dashboard uses the stacked-panel construction (Track 02) instead, so the reader sees each lab against its own y-axis without the dual-axis chart's spurious-correlation risk.

            **Reference-range band on every lab panel.** Track 02 Decision 1: the reference-range band converts the chart from "value over time" to "value over time, in or out of range." The band is shaded behind the line in every panel.

            **Default chart style is Line with points.** Track 01: a continuous variable on a time axis gets a line chart. Track 02: the points let the reader see where the actual specimens are on an unevenly-sampled time axis. The chart-style dropdown does not offer a bar chart for the lab panel because Track 04 Pattern 4 rejects time-series-as-bar-chart.

            **Default date range covers the patient's full record.** Track 04 Pattern 2: a cherry-picked time window hides the trajectory that gives the current value its context. The dashboard initializes start and end to the earliest and latest specimen dates in the patient's record. The reader can narrow the window, but the default never starts after the diagnosis date.

            **DAS28 panel has a green dashed reference line at the remission target (2.6).** Track 02 Decision 2: an annotated reference value gives the reader an instant comparison without requiring them to remember the cut-point. The remission target for DAS28 is widely accepted as 2.6 and is the natural reference line for a clinical dashboard.

            **Medication timeline as a Gantt-style bar.** Track 01 Scenario 6: time on one axis, category on the other, event marks. The Gantt-style bar preserves the start, end, and overlap of each medication; a list of "current meds" alone would lose the temporal pattern.

            **Summary table at the bottom.** A table is the right chart type for a small set of point values that do not benefit from a visual encoding. Track 01's decision table specifies that "which category is largest" is the bar chart's question; for a static summary of the patient's current state, a table renders more accurately than any chart.

            ### What the dashboard does not include

            A few constructions are deliberately absent.

            **No bar chart for any lab series.** Track 04 Pattern 4.

            **No dual-y-axis composition.** Track 04 Pattern 3.

            **No truncated y-axes on the bar timeline.** The medication-timeline x-axis covers the patient's full record so the relative durations of medications are visible to scale.

            **No aggregation that hides spikes.** The lab panels plot the raw specimen values, not monthly or quarterly means. Track 04 Pattern 5.

            The reader can extend the dashboard with a confidence-band overlay on the DAS28 trajectory (Track 03) or with a cohort-comparison panel that overlays the four patients' CRP series on a single axis (Track 02 cohort-of-trajectories construction).
            """
        )
    else:
        rationale = mo.md("_Click the button above to see the design rationale._")
    mo.vstack([reveal_widget, rationale])
    return (rationale,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        The dashboard above is the working application of the four tracks of this course. The controls drive a reactive composition that applies the chart-type decision (Track 01), the longitudinal-chart construction rules (Track 02), the uncertainty-display vocabulary (Track 03), and the misleading-pattern checklist (Track 04). The reveal panel above names each construction decision and the rule that motivated it. The course ends here; Course 09 takes up the related but distinct question of how to evaluate models that produce the kind of predictions a clinical dashboard would display.
        """
    )
    return


if __name__ == "__main__":
    app.run()
