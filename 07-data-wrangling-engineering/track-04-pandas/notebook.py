"""Track 04: pandas, the post-extraction analytic layer.

A SQL query against the OMOP warehouse returns a flat tabular cohort.
The downstream analytic work (tidying, per-patient summaries,
time-since-event computations, comparisons across groups) typically
happens in a DataFrame library outside the database. This track covers
that layer in pandas, identifies the alternatives (DuckDB, polars,
dplyr) and the situations each is better suited to, and demonstrates
the canonical operations on the same synthetic RA cohort used in
Track 03.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import sys
    import types
    from pathlib import Path

    import marimo as mo
    import numpy as np
    import pandas as pd

    # Cross-reference helpers inlined from shared/cross_reference.py.
    _COURSE_TITLES = {
        "00": "Foundations of clinical informatics",
        "01": "Computational thinking",
        "02": "Data literacy",
        "03": "Privacy, ethics, and governance",
        "04": "Clinical epidemiology",
        "05": "EHR systems",
        "06": "Learn FHIR",
        "07": "Data wrangling and engineering",
        "08": "Clinical visualization",
        "09": "AI in medicine",
        "10": "NLP and clinical text",
        "11": "Health economics data",
        "12": "Clinical decision support",
    }

    def _course_label(course_id):
        title = _COURSE_TITLES.get(course_id.split("-")[0])
        return f"Course {course_id}: {title}" if title else f"Course {course_id}"

    def _xref_callback(from_course, to_course, topic, body):
        return mo.callout(
            mo.md(
                f"**Callback to {_course_label(to_course)}.** {topic}\n\n{body}"
            ),
            kind="neutral",
        )

    def _xref_forward(from_course, to_course, topic, body):
        return mo.callout(
            mo.md(
                f"**Forward to {_course_label(to_course)}.** {topic}\n\n{body}"
            ),
            kind="neutral",
        )

    xref = types.SimpleNamespace(callback=_xref_callback, forward=_xref_forward)
    return mo, np, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 04: pandas, the post-extraction analytic layer

        ## What pandas is and what role it serves

        **pandas** is a Python library for working with tabular data. The central object it provides is the **DataFrame**, which is a table in memory: rows are records (typically one row per patient, per visit, or per measurement), and columns are named attributes (such as `person_id`, `value_as_number`, `measurement_date`). Every operation in this track is a transformation of a DataFrame into another DataFrame.

        The role pandas plays in the analytic stack sits one layer above SQL. A SQL query against the OMOP warehouse (Track 03) returns a flat tabular result. The result is the analytic cohort: typically a few hundred to a few hundred thousand rows, small enough to fit in the analyst's RAM. The bulk of the analytic work begins once that cohort is in the analyst's hands.

        Operations that follow extraction include:

        - **Tidying** the cohort: renaming columns, dropping rows that fail a quality check, converting columns from text to typed values.
        - **Computing per-patient summaries**: the last value of a lab, the mean of a measure over a time window, the count of events per patient.
        - **Computing time-since-event columns**: days since index date, age at first treatment, time on therapy.
        - **Reshaping between wide and long forms**: pivoting one-row-per-measurement into one-column-per-measurement-type, or the reverse.
        - **Joining the cohort to additional tables** that did not need to be queried in the original extraction.

        These operations are all expressible in SQL too. The reason most analysts move the cohort out of SQL at this point is that the iteration cycle is faster in a DataFrame library: a small change to a per-patient summary does not require re-running the warehouse query, and intermediate results are easier to inspect interactively. The choice of DataFrame library is the subject of the next section.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Tool choice

        Four widely used libraries fill the post-extraction analytic role. Each has a distinct profile.
        """
    )
    return


@app.cell
def _(pd):
    tool_comparison = pd.DataFrame(
        [
            {
                "Tool": "pandas",
                "Language": "Python",
                "Execution model": "Eager, in-memory",
                "Strengths": "Largest ecosystem; most documentation; widely taught; first-class marimo support",
                "When to use it": "Default Python choice. Cohort fits in RAM. Interactive analysis.",
            },
            {
                "Tool": "DuckDB",
                "Language": "SQL (Python bindings)",
                "Execution model": "Lazy, columnar, runs directly over CSV/Parquet/Arrow",
                "Strengths": "Reads files without loading them entirely into RAM; very fast on warehouse-shaped data",
                "When to use it": "Cohort is larger than RAM. SQL-shaped operations on data already at rest in files.",
            },
            {
                "Tool": "polars",
                "Language": "Python (also Rust, R)",
                "Execution model": "Lazy, parallel, columnar",
                "Strengths": "Significantly faster than pandas for grouped operations; lazy planner optimizes queries",
                "When to use it": "pandas is too slow. Pipeline runs repeatedly on the same data shape.",
            },
            {
                "Tool": "dplyr",
                "Language": "R",
                "Execution model": "Eager, in-memory (or lazy with dbplyr)",
                "Strengths": "Concise verb-based grammar; integrates with R's statistical ecosystem",
                "When to use it": "Downstream work is in R. Working with collaborators who use R.",
            },
        ]
    )
    tool_comparison.index = range(1, len(tool_comparison) + 1)
    tool_comparison.index.name = "row"
    tool_comparison
    return (tool_comparison,)


@app.cell
def _(mo):
    mo.md(
        r"""
        The choice of tool depends on data size, on the team's existing language, and on the shape of the downstream work. pandas is used in this course because it is the most common Python option, the most thoroughly documented, and the easiest to demonstrate in a marimo notebook. The operations demonstrated below are available with minor syntactic differences in DuckDB, polars, and dplyr; the choice of library does not change the underlying analytic logic.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The cohort used in this track

        The synthetic cohort from Track 03 is reconstructed below as pandas DataFrames. Reyes is `person_id = 1001`; person_ids 2001 through 2009 are the synthetic cohort. The construction uses the same fixed seed as Track 03, so the values are identical to those used in the SQL queries there.
        """
    )
    return


@app.cell
def _(np, pd):
    _rng = np.random.default_rng(20260524)

    _person_ids = [1001] + list(range(2001, 2010))
    _treatment = {
        1001: "TNFi", 2001: "csDMARD", 2002: "csDMARD", 2003: "TNFi",
        2004: "csDMARD", 2005: "TNFi", 2006: "csDMARD", 2007: "TNFi",
        2008: "csDMARD", 2009: "TNFi",
    }

    _person_rows = []
    for _pid in _person_ids:
        _person_rows.append({
            "person_id": _pid,
            "gender_concept_id": 8532,
            "year_of_birth": int(_rng.integers(1950, 1990)) if _pid != 1001 else 1974,
            "treatment_group": _treatment[_pid],
        })
    person = pd.DataFrame(_person_rows)

    _meas_rows = []
    for _pid in _person_ids:
        _crp_high = float(_rng.uniform(20, 60))
        _crp_low = float(_rng.uniform(2, 12))
        _crp_dates = [
            pd.Timestamp("2022-02-14") + pd.Timedelta(days=int(_rng.integers(0, 90))),
            pd.Timestamp("2024-01-08") + pd.Timedelta(days=int(_rng.integers(0, 120))),
        ]
        for _date, _value in zip(_crp_dates, [_crp_high, _crp_low]):
            _meas_rows.append({
                "person_id": _pid,
                "measurement_concept_id": 3010156,
                "measurement_date": _date.strftime("%Y-%m-%d"),
                "value_as_number": round(_value, 1),
                "unit_source_value": "mg/L",
            })
    measurement = pd.DataFrame(_meas_rows)

    _obs_rows = []
    for _pid in _person_ids:
        _baseline = float(_rng.uniform(4.5, 6.0))
        if _treatment[_pid] == "TNFi":
            _followup = float(_rng.uniform(2.4, 3.6))
        else:
            _followup = float(_rng.uniform(3.4, 5.2))
        for _date_str, _value in [
            ("2022-03-07", _baseline),
            ("2024-01-08", _followup),
        ]:
            _obs_rows.append({
                "person_id": _pid,
                "observation_concept_id": 40766949,
                "observation_date": _date_str,
                "value_as_number": round(_value, 2),
            })
    observation = pd.DataFrame(_obs_rows)

    return measurement, observation, person


@app.cell
def _(person):
    person_display = person.copy()
    person_display.index = range(1, len(person_display) + 1)
    person_display.index.name = "row"
    person_display
    return (person_display,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Ten patients, balanced between treatment groups. The DataFrame columns are the same as the OMOP `person` table columns from Track 02, plus a `treatment_group` label that was derived from the `drug_exposure` table in the SQL extraction.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## groupby and aggregate

        **groupby** is pandas's mechanism for "compute X per group." The operation has three steps, the same three SQL's `GROUP BY` performs.

        1. **Split.** pandas sorts the rows of the DataFrame into groups according to the value of one or more columns. If the grouping column is `treatment_group`, the result is one pile of rows per unique treatment group value.
        2. **Apply.** A summarizing function (mean, count, max, sum, standard deviation) is run on a chosen column within each pile.
        3. **Combine.** The per-group results are stacked back into a single DataFrame with one row per group.

        The cell below performs all three on the observation DataFrame. The clinical question is "what is the mean DAS28 in each treatment group at each visit." The grouping columns are `treatment_group` and `observation_date`; the summarized column is `value_as_number` (the DAS28 score); the summarizing functions are count, mean, and standard deviation.

        Before the groupby runs, the observation table has to gain a `treatment_group` column. The observation table does not carry that label natively; the label lives on the person table. Attaching it is the job of the `merge` call that opens the cell. The `merge` step is the subject of the next section, but the call here is straightforward.

        The pandas chain below reads, line by line, as:

        - `observation.merge(person[["person_id", "treatment_group"]], on="person_id")`. Combine the observation DataFrame with the person DataFrame (taking only the `person_id` and `treatment_group` columns from person). Each observation row gains a `treatment_group` column copied from the matching person row.
        - `.groupby(["treatment_group", "observation_date"])`. Sort the joined rows into one group per (treatment group, observation date) combination.
        - `["value_as_number"]`. Restrict the per-group computation to the DAS28 score column.
        - `.agg(["count", "mean", "std"])`. Compute three summary numbers per group: the patient count, the mean, the standard deviation.
        - `.round(2)`. Round all numeric values to two decimals.
        - `.reset_index()`. Convert the grouping output (which carries the group keys as a special index) into a regular DataFrame with the group keys as ordinary columns.
        - `.rename(columns={"count": "n", "mean": "mean_das28", "std": "sd_das28"})`. Give the three aggregate columns human-readable names.
        """
    )
    return


@app.cell
def _(observation, person):
    obs_with_group = observation.merge(person[["person_id", "treatment_group"]], on="person_id")
    das28_summary = (
        obs_with_group
        .groupby(["treatment_group", "observation_date"])["value_as_number"]
        .agg(["count", "mean", "std"])
        .round(2)
        .reset_index()
        .rename(columns={"count": "n", "mean": "mean_das28", "std": "sd_das28"})
    )
    das28_summary.index = range(1, len(das28_summary) + 1)
    das28_summary.index.name = "row"
    das28_summary
    return das28_summary, obs_with_group


@app.cell
def _(mo):
    mo.md(
        r"""
        The result has four rows, one per (treatment group, visit date) combination. Each row carries `n` (the count of patients in the group at that visit), `mean_das28` (the average DAS28 in the group), and `sd_das28` (the standard deviation around that mean).

        Clinical reading. Both treatment groups entered the cohort with similar baseline DAS28 in March 2022 (means just above 5, in the high-activity range). By the January 2024 follow-up, the TNFi group's mean DAS28 has dropped substantially (into the low-activity range); the csDMARD-only group's mean has dropped modestly (into the moderate range). This is the expected pattern: adding a biologic to methotrexate produces more disease-activity reduction than methotrexate alone in patients with active RA.

        Three operations chained together to produce this result.

        - **`merge`** joined the observation table to the person table on `person_id`. Each observation row gained a `treatment_group` column copied from the matching person row.
        - **`groupby(["treatment_group", "observation_date"])`** partitioned the rows into the four (treatment, visit) groups; `.agg(["count", "mean", "std"])` computed three summary numbers per group.
        - **`.reset_index()`** flattened the grouping output into a regular DataFrame, and **`.rename`** gave the aggregate columns human-readable names.

        This is exactly the answer the Track 03 SQL `GROUP BY` query returned, computed in pandas instead. The choice between SQL and pandas at this step is the subject of a later section.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## merge: combining tables on a key

        **merge** is pandas's version of a SQL `JOIN`. The operation takes two DataFrames and combines them row by row, using a shared column (the **key**) as the lookup. For every row in the left DataFrame, merge looks for matching rows in the right DataFrame where the key column is equal, and attaches the right-side columns to the left row.

        In clinical analytics, the typical merge is "I have a per-measurement table, and I need a per-patient attribute on each measurement row." The measurement table has `person_id`; the person table has `person_id` plus the desired attribute (treatment group, age, sex). Merging the two on `person_id` produces a per-measurement table that also carries the per-patient attribute.

        The example earlier in this notebook used `merge` casually to attach treatment labels for the groupby. The operation deserves its own section because join correctness is a leading source of analytic errors. Course 02 Track 04 covered the four join types and the silent-patient-loss pattern; the same rules apply here.

        The cell below merges the measurement table (CRP rows) with person to attach treatment group. The default `how="inner"` is used: only rows whose key value appears in both tables are kept. This is the right default when both sides should already contain the same `person_id` values, but every merge should be verified by checking the row count before and after, because a join with the wrong key or with duplicates can produce a result whose row count silently differs from the input.

        The merge call reads as:

        - `measurement.merge(...)`. Start with the measurement DataFrame as the left side of the merge.
        - `person[["person_id", "treatment_group"]]`. Use the person DataFrame as the right side, but take only the `person_id` and `treatment_group` columns (avoiding the import of irrelevant person columns into the result).
        - `on="person_id"`. Match left and right rows whose `person_id` values are equal.
        - `how="inner"`. Keep only rows whose `person_id` exists in both tables. (Alternatives: `how="left"` keeps every left row even if the right side has no match; `how="right"` does the reverse; `how="outer"` keeps everything from both sides.)

        The cell after this one runs the row-count sanity check.
        """
    )
    return


@app.cell
def _(measurement, person):
    crp_with_group = measurement.merge(
        person[["person_id", "treatment_group"]],
        on="person_id",
        how="inner",
    )
    crp_with_group_display = crp_with_group.copy()
    crp_with_group_display.index = range(1, len(crp_with_group_display) + 1)
    crp_with_group_display.index.name = "row"
    crp_with_group_display
    return crp_with_group, crp_with_group_display


@app.cell
def _(crp_with_group, measurement, mo):
    rows_before = len(measurement)
    rows_after = len(crp_with_group)
    mo.callout(
        mo.md(
            f"**Row count check.** measurement (left) had **{rows_before} rows**; merged result has **{rows_after} rows**. "
            "Equal counts indicate that every measurement row found a matching person row. "
            "A drop in row count would indicate patients in measurement who do not exist in person; an increase would indicate duplicates on the join key."
        ),
        kind="info" if rows_before == rows_after else "warn",
    )
    return rows_after, rows_before


@app.cell
def _(mo):
    mo.md(
        r"""
        Three checks should accompany every merge.

        - **Row count before and after.** An inner join can silently drop rows; a left join can silently introduce NULLs. The row count is the cheapest sanity check.
        - **Join-key uniqueness.** A `one-to-many` join produces more rows than the left side started with. If `person.person_id` is supposed to be unique (one row per patient), `person["person_id"].is_unique` should be `True` before the join.
        - **NULL handling.** If the join is `left` and the right side may be missing rows, the columns from the right side will contain NaN for unmatched left rows. Downstream aggregations may silently exclude or include these NaNs depending on the aggregate function.

        The pandas-specific syntax differs from SQL, but the failure modes are identical to those covered in Course 02 Track 04.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Dates: parse, compute, compare

        Dates arrive from a warehouse export as text strings. A column called `measurement_date` that contains the value `"2022-02-14"` is, as far as Python is concerned, a column of strings. Comparison operators (`<`, `>`, `=`) work on strings but compare them character by character, not chronologically; arithmetic operators do not work on them at all.

        The most common pandas error in clinical analytics is filtering or doing arithmetic on a column that looks like a date but is stored as text. A query for "measurements after 2024-01-01" works only by accident, because the ISO-8601 format (`YYYY-MM-DD`) happens to sort lexicographically in the same order as the underlying dates. The same query against a `MM/DD/YYYY` column returns silently wrong results.

        The fix is one line: convert the column to a true datetime type once, immediately after the data lands, and operate on the typed column for everything downstream. The pandas function for the conversion is `pd.to_datetime`. After conversion, comparison, subtraction, and groupby on the date column all behave as expected.

        The two cells below demonstrate the fix. The first converts `measurement_date` to datetime and shows the before-and-after dtype. The second uses the converted column to compute `days_since_baseline` for each row, where the baseline is March 7, 2022 (Reyes's first DMARD prescription date in the synthetic cohort).

        The conversion cell reads as:

        - `crp_typed = crp_with_group.copy()`. Make a copy of the DataFrame so the original is not mutated.
        - `crp_typed["measurement_date"] = pd.to_datetime(crp_typed["measurement_date"])`. Replace the `measurement_date` column with the datetime-typed version of itself. `pd.to_datetime` parses each string into a Timestamp object; the resulting column has dtype `datetime64[ns]` instead of `object`.

        The days-since-baseline cell reads as:

        - `baseline_date = pd.Timestamp("2022-03-07")`. Define a single Timestamp for the reference date.
        - `crp_with_time["days_since_baseline"] = (crp_with_time["measurement_date"] - baseline_date).dt.days`. Subtract the baseline from each row's measurement date (the result is a Timedelta column), then use the `.dt.days` accessor to extract the integer day count.
        - `crp_with_time["years_since_baseline"] = (crp_with_time["days_since_baseline"] / 365.25).round(2)`. Divide days by 365.25 to express the same duration in years, rounded to 2 decimals.
        """
    )
    return


@app.cell
def _(crp_with_group, pd):
    crp_typed = crp_with_group.copy()
    crp_typed["measurement_date"] = pd.to_datetime(crp_typed["measurement_date"])
    type_check = pd.DataFrame(
        [
            {"column": "measurement_date (before)", "dtype": "object (string)"},
            {"column": "measurement_date (after)", "dtype": str(crp_typed["measurement_date"].dtype)},
        ]
    )
    type_check.index = range(1, len(type_check) + 1)
    type_check.index.name = "row"
    type_check
    return crp_typed, type_check


@app.cell
def _(crp_typed, pd):
    baseline_date = pd.Timestamp("2022-03-07")
    crp_with_time = crp_typed.copy()
    crp_with_time["days_since_baseline"] = (
        crp_with_time["measurement_date"] - baseline_date
    ).dt.days
    crp_with_time["years_since_baseline"] = (
        crp_with_time["days_since_baseline"] / 365.25
    ).round(2)
    crp_with_time_display = crp_with_time[
        ["person_id", "treatment_group", "measurement_date",
         "value_as_number", "days_since_baseline", "years_since_baseline"]
    ].copy()
    crp_with_time_display.index = range(1, len(crp_with_time_display) + 1)
    crp_with_time_display.index.name = "row"
    crp_with_time_display
    return baseline_date, crp_with_time, crp_with_time_display


@app.cell
def _(mo):
    mo.md(
        r"""
        Three operations did the work.

        - `pd.to_datetime` converted the text column to a true datetime dtype. After conversion, comparisons and arithmetic on the column produce the expected results; before conversion, `'2024-01-08' < '2024-02-01'` happens to compare correctly only because ISO-8601 strings sort lexicographically, while `'01-08-2024' < '02-01-2024'` would silently produce the wrong answer.
        - Subtracting two datetimes produced a Timedelta column; `.dt.days` extracted the integer day count.
        - Dividing by 365.25 produced years. The same convention was used in the SQL `julianday(end) - julianday(start)) / 365.25` formula in Track 03.

        The pattern (convert once at the boundary, then operate on the typed column) is the same one Course 02 Track 01 demonstrated for numeric columns stored as text. Type conversion at the data boundary is the single most reliable habit for avoiding silent errors downstream.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Reactive per-patient summary

        The slider below sets a CRP threshold. The summary cell beneath it rebuilds whenever the slider moves, showing the count and mean CRP of patients in each treatment group whose most recent CRP is at or above the chosen threshold.

        The reactivity demonstrates the canonical shape of interactive clinical analytics: a parameter changes (the threshold), a per-patient computation re-runs against the cohort (each patient's most-recent CRP is compared to the threshold), the filter rebuilds the subgroup (patients above the threshold), and a group-level summary updates (count and mean per treatment group). Production tools such as ATLAS, Cytel's cohort builders, and the Stanford STARR dashboards expose the same pattern with more controls and against larger cohorts; the underlying steps are the same as in the cell below.

        The pandas chain in the next cell reads as:

        - `most_recent_crp = (crp_with_group.sort_values(["person_id", "measurement_date"], ascending=[True, False]).groupby("person_id").head(1)...)`. Sort the CRP rows so that within each patient the most recent measurement is first, then take the first row per patient. The result is one row per patient carrying that patient's most recent CRP date and value.
        - `.rename(columns={"value_as_number": "most_recent_crp"})`. Rename for readability.
        - `cohort = person[["person_id", "treatment_group"]].merge(most_recent_crp, on="person_id")`. Attach the most-recent-CRP column to the per-patient demographic table.
        - `above_threshold = cohort[cohort["most_recent_crp"] >= float(crp_threshold.value)]`. Filter the per-patient table to patients whose most-recent CRP meets the slider value.
        - `summary = above_threshold.groupby("treatment_group").agg(n_above_threshold=("person_id", "count"), mean_crp=("most_recent_crp", "mean")).round(1).reset_index()`. Group the surviving patients by treatment, count them, average their CRP, and flatten the result into a regular DataFrame.

        Every line above re-runs each time the slider moves. The shape of the result stays the same (one row per treatment group); the numbers in each row update.
        """
    )
    return


@app.cell
def _(mo):
    crp_threshold = mo.ui.slider(
        start=0, stop=60, step=2, value=20,
        label="CRP threshold (mg/L)",
        show_value=True, full_width=True,
    )
    crp_threshold
    return (crp_threshold,)


@app.cell
def _(crp_threshold, crp_with_group, mo, person):
    most_recent_crp = (
        crp_with_group
        .sort_values(["person_id", "measurement_date"], ascending=[True, False])
        .groupby("person_id")
        .head(1)
        [["person_id", "value_as_number"]]
        .rename(columns={"value_as_number": "most_recent_crp"})
    )
    cohort = (
        person[["person_id", "treatment_group"]]
        .merge(most_recent_crp, on="person_id")
    )
    above_threshold = cohort[cohort["most_recent_crp"] >= float(crp_threshold.value)]
    summary = (
        above_threshold
        .groupby("treatment_group")
        .agg(n_above_threshold=("person_id", "count"),
             mean_crp=("most_recent_crp", "mean"))
        .round(1)
        .reset_index()
    )
    summary.index = range(1, len(summary) + 1)
    summary.index.name = "row"
    mo.vstack([
        mo.md(
            f"**Threshold:** CRP >= {float(crp_threshold.value):.0f} mg/L. "
            f"**Patients above threshold:** {len(above_threshold)} of {len(cohort)}."
        ),
        summary,
    ])
    return above_threshold, cohort, most_recent_crp, summary


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The same operation in pandas and in SQL

        The most-recent-CRP query was written in SQL in Track 03 as a window function. The pandas equivalent uses `sort_values` followed by `groupby(...).head(1)`. The two are shown side by side below.

        SQL form (Track 03):

        ```sql
        SELECT person_id, measurement_date, value_as_number
        FROM (
            SELECT person_id, measurement_date, value_as_number,
                ROW_NUMBER() OVER (
                    PARTITION BY person_id
                    ORDER BY measurement_date DESC
                ) AS rn
            FROM measurement
            WHERE measurement_concept_id = 3010156
        )
        WHERE rn = 1;
        ```

        pandas form (this track):

        ```python
        (measurement
            .query("measurement_concept_id == 3010156")
            .sort_values(["person_id", "measurement_date"], ascending=[True, False])
            .groupby("person_id")
            .head(1))
        ```

        The two queries return the same rows. The analytic logic is identical: partition the measurement rows by patient, sort each patient's rows by date with the most recent first, keep only the most recent row per patient.

        The choice between them is operational, not analytic. When the data is in the warehouse and the cohort is large (tens or hundreds of thousands of rows), the SQL form runs on the warehouse engine and returns only the per-patient result rows. The full measurement table never leaves the warehouse. When the cohort is already extracted and sits in a DataFrame on the analyst's machine, the pandas form is shorter, reads more directly in a notebook, and avoids a second round-trip to the warehouse. In production analytic pipelines, the typical pattern is to do as much filtering and aggregation in SQL as possible (to keep the data transfer small), then move to pandas for the iterative analytic work that follows.
        """
    )
    return


@app.cell
def _(mo):
    q1 = mo.ui.radio(
        options=[
            "pandas, because the analysis is iterative and the cohort fits in memory.",
            "DuckDB, because it reads CSV files without loading them entirely into RAM.",
            "polars, because lazy evaluation parallelizes the per-patient operations.",
            "pandas, but only because the team already uses pandas; either DuckDB or polars would also work.",
        ],
        label=(
            "A 10-million-row CSV export from an OMOP warehouse needs a "
            "per-patient last-value computation, run once for a single "
            "analysis. The file does not fit in the analyst's RAM. Which "
            "tool fits the situation best?"
        ),
    )
    q1
    return (q1,)


@app.cell
def _(mo, q1):
    if q1.value is None:
        out1 = mo.md("_Pick one._")
    else:
        correct1 = q1.value.startswith("DuckDB")
        out1 = mo.callout(
            mo.md(
                rf"""
                **{'Correct.' if correct1 else 'Not quite.'}**

                DuckDB is the right fit for this constraint. It reads CSV (and Parquet, and Arrow) directly from disk and executes SQL queries over the file without first loading the whole file into RAM. The same per-patient last-value query that would run as a window function in SQL on the warehouse runs identically in DuckDB on the local CSV. pandas would attempt to load the full file at the start of the operation and would fail; polars supports lazy execution and would handle the size, but for a single one-off analysis the DuckDB SQL form is the shortest path. The first option (pandas) is wrong because the cohort does not fit in memory. The fourth option understates DuckDB's specific advantage in this scenario.
                """
            ),
            kind="success" if correct1 else "warn",
        )
    out1
    return


@app.cell
def _(mo):
    q2 = mo.ui.radio(
        options=[
            "Convert measurement_date to a true datetime once, immediately after loading.",
            "Filter on the string `'>= \\'2024-01-01\\''`; pandas handles the comparison correctly.",
            "Use `pd.to_datetime` inside the filter expression every time a comparison is made.",
            "Sort the column lexicographically and trust that ISO-8601 strings sort correctly.",
        ],
        label=(
            "A clinical analysis filters a measurement DataFrame for rows "
            "where measurement_date is on or after 2024-01-01. The column is "
            "currently stored as text. Which approach is most reliable?"
        ),
    )
    q2
    return (q2,)


@app.cell
def _(mo, q2):
    if q2.value is None:
        out2 = mo.md("_Pick one._")
    else:
        correct2 = q2.value.startswith("Convert")
        out2 = mo.callout(
            mo.md(
                rf"""
                **{'Correct.' if correct2 else 'Not quite.'}**

                Converting at the boundary is the only reliable approach. After conversion, every downstream comparison, arithmetic operation, and groupby on the date column behaves as expected. Comparing strings (the second and fourth options) happens to produce correct results when the strings are in ISO-8601 format (`YYYY-MM-DD`) because that format sorts lexicographically in the same order as the underlying dates, but the moment the column contains any other format (`MM/DD/YYYY`, `DD-MM-YYYY`, mixed conventions across sites) the silent-wrong-answer mode arrives. Calling `pd.to_datetime` inside every filter (the third option) works but is slow and clutters every downstream line; converting once removes the issue from the rest of the analysis.
                """
            ),
            kind="success" if correct2 else "warn",
        )
    out2
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Reflection

        Pick one of the two prompts below and write 4 to 6 sentences in the box that follows. Save what you write outside the browser; the box is a scratch pad, not persistent storage. When you are done, continue to `track-05-graph-databases`.

        1. **An analytic pipeline you have written or used** combined SQL extraction with a downstream DataFrame layer. Identify the boundary: which operations stayed in SQL, and which moved to the DataFrame layer. State the criterion the team used to draw that boundary. If you had to redraw it today, would the boundary move in either direction?

        2. **A new collaborator** plans to keep the entire analysis in pandas, loading the full OMOP warehouse tables into memory. State the operational risks of that approach. Identify the size of cohort at which the approach starts to fail in your environment, and the alternative tool you would recommend as the cohort grows.
        """
    )
    return


@app.cell
def _(mo):
    reflection = mo.ui.text_area(
        placeholder="Write 4-6 sentences here. Your text stays in your browser; copy it out if you want to keep it.",
        rows=8,
        full_width=True,
    )
    reflection
    return


@app.cell
def _(mo, xref):
    xref.forward(
        "07-data-wrangling-engineering",
        "07-data-wrangling-engineering",
        "Graph databases are the final concept of this course.",
        (
            "The extraction-and-analysis pipeline covered in Tracks 03 and 04 "
            "handles the cohort questions that fit a tabular shape. A small "
            "set of clinically interesting questions are not naturally "
            "tabular: care-team networks, medication-transition sequences, "
            "ontology traversal across SNOMED's is-a hierarchy. Track 05 "
            "introduces graph databases as the data model that fits those "
            "questions, presents the vocabulary (nodes, edges, traversal), "
            "and shows one worked example. The presentation is conceptual; "
            "no installation is required. Continue to "
            "`track-05-graph-databases`."
        ),
    )
    return


if __name__ == "__main__":
    app.run()
