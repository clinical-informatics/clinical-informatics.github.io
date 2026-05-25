"""Track 03: SQL, the extraction layer.

The OMOP warehouse from Track 02 is now treated as a source. SQL is the
language the warehouse speaks. Each section of this notebook begins
with a clinical question, then constructs the SQL that returns the
corresponding cohort, summary, or per-person rollup against an in-memory
SQLite database built from Ms. Reyes plus a small synthetic RA cohort,
all in OMOP shape.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import sqlite3
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
    return mo, np, pd, sqlite3, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 03: SQL, the extraction layer

        ## The role of SQL in the analytic stack

        Track 02 defined the OMOP warehouse as a fixed schema of six core clinical tables, each carrying concept_ids drawn from a shared vocabulary. The warehouse is the source. The analytic question is downstream: a clinical cohort, a per-person summary, a comparison between treatment groups, a time-to-event analysis.

        SQL is the language used to extract the cohort or the summary from the warehouse. Every modern clinical data warehouse exposes a SQL interface, regardless of the underlying database engine (PostgreSQL, SQL Server, BigQuery, Snowflake, Databricks SQL). A SQL query written against an OMOP-conformant warehouse is portable across engines with at most minor syntactic adjustment.

        The structure of every analytic project against the warehouse is the same: state the clinical question, identify the OMOP tables that hold the relevant facts, write the SQL that joins and filters those tables to produce the answer. Each section of this track demonstrates that sequence on one clinical question.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The synthetic warehouse used in this track

        An in-memory SQLite database is built below. It holds Reyes plus a synthetic RA cohort of nine additional patients, all in OMOP shape. The data is small enough to display in full, large enough to demonstrate aggregations and joins.

        The build uses a fixed seed so the data is reproducible. The schema and concept_ids match the OMOP CDM v5.4 conventions from Track 02.
        """
    )
    return


@app.cell
def _(np, pd, sqlite3):
    # Build a synthetic OMOP-shaped warehouse: Reyes (person_id 1001) plus
    # nine additional RA patients (person_ids 2001-2009). Five are on
    # csDMARD monotherapy (methotrexate); five are on TNFi added to
    # methotrexate (Reyes plus four). All have an RA condition_occurrence
    # row, baseline and follow-up DAS28, and two CRP measurements each.
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
            "race_concept_id": 8527,
            "ethnicity_concept_id": int(_rng.choice([38003563, 38003564])),
        })
    person = pd.DataFrame(_person_rows)

    _condition_rows = []
    _condition_id = 6001
    for _pid in _person_ids:
        _start = pd.Timestamp("2022-01-01") + pd.Timedelta(days=int(_rng.integers(0, 365)))
        _condition_rows.append({
            "condition_occurrence_id": _condition_id,
            "person_id": _pid,
            "condition_concept_id": 4138406,
            "condition_start_date": _start.strftime("%Y-%m-%d"),
            "condition_source_value": "M05.79",
        })
        _condition_id += 1
    condition_occurrence = pd.DataFrame(_condition_rows)

    _drug_rows = []
    _drug_id = 7001
    for _pid in _person_ids:
        # Methotrexate for everyone (csDMARD baseline)
        _mtx_start = pd.Timestamp("2022-03-01") + pd.Timedelta(days=int(_rng.integers(0, 365)))
        _drug_rows.append({
            "drug_exposure_id": _drug_id,
            "person_id": _pid,
            "drug_concept_id": 1503297,
            "drug_exposure_start_date": _mtx_start.strftime("%Y-%m-%d"),
            "drug_exposure_end_date": None,
        })
        _drug_id += 1
        # Adalimumab added for the TNFi arm
        if _treatment[_pid] == "TNFi":
            _ada_start = _mtx_start + pd.Timedelta(days=int(_rng.integers(180, 540)))
            _drug_rows.append({
                "drug_exposure_id": _drug_id,
                "person_id": _pid,
                "drug_concept_id": 1119119,
                "drug_exposure_start_date": _ada_start.strftime("%Y-%m-%d"),
                "drug_exposure_end_date": None,
            })
            _drug_id += 1
    drug_exposure = pd.DataFrame(_drug_rows)

    _meas_rows = []
    _meas_id = 8001
    for _pid in _person_ids:
        # Two CRP values per patient: one elevated, one closer to range
        _crp_high = float(_rng.uniform(20, 60))
        _crp_low = float(_rng.uniform(2, 12))
        _crp_dates = [
            pd.Timestamp("2022-02-14") + pd.Timedelta(days=int(_rng.integers(0, 90))),
            pd.Timestamp("2024-01-08") + pd.Timedelta(days=int(_rng.integers(0, 120))),
        ]
        for _date, _value in zip(_crp_dates, [_crp_high, _crp_low]):
            _meas_rows.append({
                "measurement_id": _meas_id,
                "person_id": _pid,
                "measurement_concept_id": 3010156,
                "measurement_date": _date.strftime("%Y-%m-%d"),
                "value_as_number": round(_value, 1),
                "unit_source_value": "mg/L",
            })
            _meas_id += 1
    measurement = pd.DataFrame(_meas_rows)

    _obs_rows = []
    _obs_id = 9001
    for _pid in _person_ids:
        # Baseline DAS28 (higher) and follow-up DAS28 (lower if TNFi, mixed if csDMARD)
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
                "observation_id": _obs_id,
                "person_id": _pid,
                "observation_concept_id": 40766949,
                "observation_date": _date_str,
                "value_as_number": round(_value, 2),
                "observation_source_value": "DAS28-CRP",
            })
            _obs_id += 1
    observation = pd.DataFrame(_obs_rows)

    # Visit_occurrence: two visits per person to keep the GROUP BY example honest
    _visit_rows = []
    _visit_id = 5001
    for _pid in _person_ids:
        for _date_str in ["2022-03-07", "2024-01-08"]:
            _visit_rows.append({
                "visit_occurrence_id": _visit_id,
                "person_id": _pid,
                "visit_concept_id": 9202,
                "visit_start_date": _date_str,
                "visit_end_date": _date_str,
            })
            _visit_id += 1
    # Add a few telehealth visits to make the GROUP BY meaningful
    for _pid in _person_ids[:4]:
        _visit_rows.append({
            "visit_occurrence_id": _visit_id,
            "person_id": _pid,
            "visit_concept_id": 5083,  # OMOP concept for Telehealth
            "visit_start_date": "2023-06-15",
            "visit_end_date": "2023-06-15",
        })
        _visit_id += 1
    visit_occurrence = pd.DataFrame(_visit_rows)

    # Load all six tables into in-memory SQLite
    con = sqlite3.connect(":memory:")
    person.to_sql("person", con, if_exists="replace", index=False)
    visit_occurrence.to_sql("visit_occurrence", con, if_exists="replace", index=False)
    condition_occurrence.to_sql("condition_occurrence", con, if_exists="replace", index=False)
    drug_exposure.to_sql("drug_exposure", con, if_exists="replace", index=False)
    measurement.to_sql("measurement", con, if_exists="replace", index=False)
    observation.to_sql("observation", con, if_exists="replace", index=False)
    return condition_occurrence, con, drug_exposure, measurement, observation, person, visit_occurrence


@app.cell
def _(mo, person):
    mo.md(
        f"""
        ## Warehouse contents

        The in-memory database contains six tables (person, visit_occurrence, condition_occurrence, drug_exposure, measurement, observation) populated with {len(person)} patients. All standardized columns use the OMOP v5.4 concept_id conventions from Track 02. Reyes is `person_id = 1001`; the synthetic cohort uses person_ids 2001 through 2009.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What SQL is and what each clause does

        SQL (Structured Query Language) is the language a database understands when you ask it a question. A SQL query is a written sentence that names the table to look in, the rows to keep, and the columns to return. The database reads the sentence, finds the matching rows, and returns them as a result set.

        Four clauses do the bulk of the work in this track. Each is defined below in the order it would appear in a typical query.

        - **`SELECT`** names the columns the query should return. `SELECT person_id, value_as_number` returns two columns; `SELECT *` returns every column.
        - **`FROM`** names the table the query reads from. `FROM measurement` reads from the measurement table.
        - **`WHERE`** filters rows. Only rows for which the WHERE condition is true are kept. `WHERE measurement_concept_id = 3010156` keeps only the CRP measurement rows.
        - **`JOIN`** combines two tables row by row on a shared column. When the question requires data from two tables (for example, a per-patient summary that needs both demographic data from `person` and lab values from `measurement`), a JOIN attaches the matching row from one table to each row of the other.
        - **`GROUP BY`** collapses many rows into one row per group. If the question is "how many lab results does each patient have," a `GROUP BY person_id` produces one row per patient. The collapse must be accompanied by an **aggregate function** (`COUNT`, `AVG`, `MAX`, `SUM`) that says how to summarize the rows in each group.
        - **`ORDER BY`** sorts the result. Does not change which rows are returned, only the order in which they appear.

        Two more constructs appear in this track and are introduced where they are needed.

        - **Window functions** (`ROW_NUMBER`, `RANK`, `LAG`) compute a value for each row using a window of related rows. They are the SQL way to ask "for each patient, what is the most recent value" or "what was the previous lab result."
        - **Common Table Expressions** (the `WITH ... AS (...)` block) define named sub-queries that can be referenced in the main query. They make a multi-step query readable by separating the steps.

        The end of every SQL query is a result set: a table of rows and columns. The number of rows depends on the question. A cohort definition returns one row per patient. A summary returns one row per group. A row-level join returns one row per matched pair. The shape of the result is the analyst's first sanity check that the query asked the question intended.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Question 1: How many visits of each type are in the warehouse?

        The clinical question is a count. The warehouse holds many visit rows; each row carries a `visit_concept_id` that names the visit type (outpatient, telehealth, inpatient, and so on). To answer the question, the visit rows need to be sorted into piles by `visit_concept_id`, and then the rows in each pile need to be counted.

        That two-step (sort into piles, count each pile) is exactly what SQL's `GROUP BY` plus an aggregate function does. `GROUP BY visit_concept_id` performs the sort; `COUNT(*)` performs the count.

        The query below reads, clause by clause, as:

        - `SELECT visit_concept_id, COUNT(*) AS n_visits`. Return two columns: the visit type, and the count of rows in each group, named `n_visits` so the column has a readable label.
        - `FROM visit_occurrence`. Read from the visit_occurrence table.
        - `GROUP BY visit_concept_id`. Sort the rows into one group per visit type.
        - `ORDER BY n_visits DESC`. Return the groups ordered by count, largest first.
        """
    )
    return


@app.cell
def _(con, pd):
    _sql_q1 = """
        SELECT
            visit_concept_id,
            COUNT(*) AS n_visits
        FROM visit_occurrence
        GROUP BY visit_concept_id
        ORDER BY n_visits DESC;
    """
    result_q1 = pd.read_sql_query(_sql_q1, con)
    result_q1.index = range(1, len(result_q1) + 1)
    result_q1.index.name = "row"
    result_q1
    return (result_q1,)


@app.cell
def _(mo):
    mo.md(
        r"""
        The result has two rows because two visit types are present in the warehouse: `9202` (Outpatient Visit) and `5083` (Telehealth Visit). The `n_visits` column gives the count for each. The outpatient count is roughly five times the telehealth count, which matches the data generator: every patient has two outpatient visits, and four patients have one telehealth visit added.

        This is the most common kind of query a clinical analyst writes as a first look at unfamiliar data. The shape of the result (number of categories present, relative counts) tells the team what visit types the warehouse actually contains, before any analysis is built that assumes a particular set. The same query also catches ETL problems: if a visit_concept_id appears in the result that the team did not anticipate, the source EHR is producing visit types that the ETL is mapping in a way no one has reviewed.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Question 2: Who are the RA patients in the warehouse?

        This is a **cohort definition**: a query that produces the list of patients meeting an inclusion criterion. Cohort definition is the most common analytic query in clinical informatics, because almost every downstream analysis (a per-patient summary, a treatment comparison, a survival analysis) begins by selecting the patients to include.

        The clinical question is "which patients in the warehouse have rheumatoid arthritis." Translating into warehouse terms: the `condition_occurrence` table holds one row per diagnosis recorded in the chart; each row carries a `condition_concept_id` that names the diagnosis. The OMOP standard concept for "rheumatoid arthritis with rheumatoid factor in multiple sites" is `4138406`. Filtering on that concept_id returns every row recording that diagnosis.

        One detail. A patient who has been seen many times may have many RA diagnosis rows in the table, one per visit on which RA was recorded. The question asks for distinct patients, not distinct rows, so the query uses `SELECT DISTINCT person_id` to collapse multiple diagnosis rows from the same patient into a single result row.

        The query below reads as:

        - `SELECT DISTINCT person_id`. Return the `person_id` column, with duplicates collapsed so each patient appears at most once.
        - `FROM condition_occurrence`. Read from the condition_occurrence table.
        - `WHERE condition_concept_id = 4138406`. Keep only the rows whose `condition_concept_id` is the OMOP standard concept for rheumatoid arthritis.
        - `ORDER BY person_id`. Sort the resulting patient IDs in ascending order for readability.
        """
    )
    return


@app.cell
def _(con, pd):
    _sql_q2 = """
        SELECT DISTINCT person_id
        FROM condition_occurrence
        WHERE condition_concept_id = 4138406
        ORDER BY person_id;
    """
    ra_cohort = pd.read_sql_query(_sql_q2, con)
    ra_cohort.index = range(1, len(ra_cohort) + 1)
    ra_cohort.index.name = "row"
    ra_cohort
    return (ra_cohort,)


@app.cell
def _(mo):
    mo.md(
        r"""
        The result is 10 rows, one per patient identifier. These are the 10 person_ids that meet the inclusion criterion. Every patient in this synthetic warehouse has an RA diagnosis recorded, so the cohort equals the full population; in a production warehouse with many other conditions present, the same query would return only the patients with at least one row matching the RA concept_id.

        The cohort definition above is intentionally minimal. A clinically defensible RA cohort against a real OMOP warehouse should enumerate the full set of RA concept_ids that count, not only `4138406`. Other valid RA-related SNOMED concepts include juvenile rheumatoid arthritis, rheumatoid arthritis without rheumatoid factor, and several other variants in the M05 and M06 ICD-10-CM families. The standard approach is to use a curated value set (a list of concept_ids authored and validated by clinicians for the purpose of identifying RA) rather than a single concept_id. Curated RA value sets are published in the PheKB and VSAC repositories described in Track 01.

        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Question 3: What is the mean baseline DAS28 by treatment group?

        This question is harder than the first two because it requires three sub-questions to be answered first.

        1. **What treatment group does each patient belong to?** A patient is "TNFi" if the drug_exposure table contains a TNFi drug exposure for that patient; "csDMARD" otherwise. This is a per-patient label derived from the drug_exposure table.
        2. **What is each patient's baseline DAS28?** The observation table holds every DAS28 measurement each patient ever had. The baseline is the earliest one. This is also a per-patient value, derived from the observation table.
        3. **What is the average baseline DAS28 within each treatment group?** Once each patient carries both a treatment label and a baseline DAS28 value, the average is computed per group.

        SQL has a mechanism for stating multi-step queries readably: the **Common Table Expression** (CTE), written as a `WITH ... AS (...)` block. Each CTE is a named sub-query whose result can be referenced by name in the main query, the same way a regular table can be. CTEs do not change what the query returns; they make the query readable by separating the steps.

        The query below uses two CTEs (`treatment` for sub-question 1, `baseline_das28` for sub-question 2) and a final `GROUP BY` for sub-question 3. Read it in three parts.

        **The `treatment` CTE** assigns each patient a treatment group label.

        - `SELECT p.person_id, CASE WHEN EXISTS (...) THEN 'TNFi' ELSE 'csDMARD' END AS treatment_group`. Return two columns for each patient: their `person_id`, and a label that depends on the result of the `EXISTS` check.
        - `EXISTS (SELECT 1 FROM drug_exposure d WHERE d.person_id = p.person_id AND d.drug_concept_id = 1119119)`. True if at least one row in drug_exposure has this patient's person_id and the adalimumab concept_id (`1119119`); false otherwise.
        - `FROM person p`. Iterate over every row of the person table.

        **The `baseline_das28` CTE** picks each patient's earliest DAS28 measurement.

        - The inner `SELECT` adds a row number `rn` to each DAS28 measurement, with the window `PARTITION BY person_id ORDER BY observation_date` numbering each patient's measurements in chronological order (1 = earliest).
        - The outer `SELECT` keeps only the rows where `rn = 1`, leaving one row per patient with that patient's baseline DAS28 value.

        **The main query** combines the two CTEs and produces the group-level summary.

        - `FROM treatment t JOIN baseline_das28 b ON b.person_id = t.person_id`. For each row in `treatment`, attach the matching row from `baseline_das28` so each patient carries both the treatment label and the baseline DAS28.
        - `GROUP BY t.treatment_group`. Sort the joined rows into one group per treatment label.
        - `SELECT t.treatment_group, COUNT(*) AS n_patients, ROUND(AVG(b.das28), 2) AS mean_baseline_das28`. For each group, return the label, the patient count, and the average baseline DAS28 rounded to 2 decimals.
        """
    )
    return


@app.cell
def _(con, pd):
    _sql_q3 = """
        WITH treatment AS (
            SELECT
                p.person_id,
                CASE
                    WHEN EXISTS (
                        SELECT 1 FROM drug_exposure d
                        WHERE d.person_id = p.person_id
                          AND d.drug_concept_id = 1119119
                    )
                    THEN 'TNFi'
                    ELSE 'csDMARD'
                END AS treatment_group
            FROM person p
        ),
        baseline_das28 AS (
            SELECT
                person_id,
                value_as_number AS das28
            FROM (
                SELECT
                    person_id,
                    value_as_number,
                    ROW_NUMBER() OVER (
                        PARTITION BY person_id
                        ORDER BY observation_date
                    ) AS rn
                FROM observation
                WHERE observation_concept_id = 40766949
            )
            WHERE rn = 1
        )
        SELECT
            t.treatment_group,
            COUNT(*) AS n_patients,
            ROUND(AVG(b.das28), 2) AS mean_baseline_das28
        FROM treatment t
        JOIN baseline_das28 b ON b.person_id = t.person_id
        GROUP BY t.treatment_group
        ORDER BY t.treatment_group;
    """
    result_q3 = pd.read_sql_query(_sql_q3, con)
    result_q3.index = range(1, len(result_q3) + 1)
    result_q3.index.name = "row"
    result_q3
    return (result_q3,)


@app.cell
def _(mo):
    mo.md(
        r"""
        The result has two rows, one per treatment group. The `n_patients` column shows how many patients ended up in each group; `mean_baseline_das28` shows the mean baseline DAS28 across patients in that group.

        Clinical reading. Both arms entered the synthetic cohort with high disease activity (DAS28 above 5.1 marks high activity by EULAR criteria; 3.2 to 5.1 marks moderate; below 3.2 marks low). The means come in just above 5 because the synthetic data places baseline DAS28 between 4.5 and 6.0 for every patient. In a real study, the meaningful comparison would be between baseline values and follow-up values; the baseline comparison establishes that the two arms were similar at the start, which is a precondition for attributing later differences to the treatment.

        Three SQL constructs did the work and are worth naming, because each recurs in other clinical queries.

        - **`CASE WHEN EXISTS (...)`** asks "does any row satisfying a condition exist for this patient." The `treatment` CTE uses it to label each patient as TNFi if any drug exposure row for that patient has the adalimumab concept_id, csDMARD otherwise. This is the standard OMOP pattern for "any patient ever exposed to drug X."
        - **`ROW_NUMBER() OVER (PARTITION BY person_id ORDER BY observation_date)`** numbers each patient's DAS28 measurements in chronological order (1 for the earliest, 2 for the next, and so on). The outer query keeps only rows where the row number equals 1, leaving the earliest DAS28 per patient. This is the most common SQL pattern for "first" or "most recent" per patient.
        - **`JOIN ... GROUP BY ... AVG(...)`** combines the two per-patient CTEs into one row per patient with both pieces of information, then collapses to one row per treatment group with the per-group average.

        The general shape (one CTE per per-patient piece of information, then JOIN + GROUP BY for the group-level summary) is the structure of almost every per-group clinical summary written against OMOP.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Question 4: What is the most recent CRP for each patient?

        "Most recent value per patient" is a query shape that recurs constantly in clinical analytics: last hemoglobin before transfusion, last serum creatinine before contrast, last DAS28 before therapy change. The SQL construct designed for it is the **window function**.

        A window function looks at the table, partitions it into groups (in this case, one group per patient), orders the rows within each group (in this case, by measurement date with the most recent first), and assigns a row number to each. The construct used below is `ROW_NUMBER() OVER (PARTITION BY person_id ORDER BY measurement_date DESC)`. After the row numbers are assigned, the outer query keeps only the rows where `rn = 1`, leaving exactly one row per patient: the most recent measurement.

        Window functions are distinct from `GROUP BY` aggregations in one important way: they do not collapse the row count. A `GROUP BY person_id` produces one row per patient and loses access to the individual measurement_date and value of any specific row. A window function leaves every row in place and adds a computed column. Quiz 1 below pulls this distinction out explicitly.

        The query below reads as a two-stage pipeline.

        **Inner query** (inside the parentheses): label every CRP measurement with its rank within its patient.

        - `SELECT person_id, measurement_date, value_as_number, ROW_NUMBER() OVER (PARTITION BY person_id ORDER BY measurement_date DESC) AS rn`. Return the three measurement columns plus a new `rn` column whose value is the row's position in its patient's date-descending list (1 = most recent for that patient, 2 = second most recent, and so on).
        - `FROM measurement WHERE measurement_concept_id = 3010156`. Only consider CRP measurement rows.

        **Outer query**: keep only the most recent row per patient.

        - `SELECT person_id, measurement_date, value_as_number AS most_recent_crp_mg_per_L`. Return three columns from the inner result, renaming the value column for readability.
        - `WHERE rn = 1`. Keep only the rows the inner query labeled as most recent.
        - `ORDER BY person_id`. Sort the result by patient ID.
        """
    )
    return


@app.cell
def _(con, pd):
    _sql_q4 = """
        SELECT
            person_id,
            measurement_date,
            value_as_number AS most_recent_crp_mg_per_L
        FROM (
            SELECT
                person_id,
                measurement_date,
                value_as_number,
                ROW_NUMBER() OVER (
                    PARTITION BY person_id
                    ORDER BY measurement_date DESC
                ) AS rn
            FROM measurement
            WHERE measurement_concept_id = 3010156
        )
        WHERE rn = 1
        ORDER BY person_id;
    """
    result_q4 = pd.read_sql_query(_sql_q4, con)
    result_q4.index = range(1, len(result_q4) + 1)
    result_q4.index.name = "row"
    result_q4
    return (result_q4,)


@app.cell
def _(mo):
    mo.md(
        r"""
        The result has 10 rows, one per patient. Each row carries the patient's most recent CRP value and the date it was measured. The clinical reading is straightforward: this is the answer a rheumatologist would want at the bedside, summarizing the most current inflammatory marker per patient in the cohort.

        The pattern generalizes immediately to other "most recent" questions. The structure is:

        - `PARTITION BY <patient-key>` defines the per-patient groups.
        - `ORDER BY <date-column> DESC` puts the most recent row first within each group.
        - `WHERE rn = 1` keeps only the most recent row per patient.

        Substituting `ORDER BY ... ASC` returns the earliest per patient (the baseline). Replacing `WHERE rn = 1` with `WHERE rn <= 3` returns the three most recent. Replacing the date column with a different ordering column ranks rows by that column instead.

        An older pattern that predates window-function support in SQL uses `MAX(measurement_date)` in a subquery and joins back to the measurement table. The two return the same rows. The window-function form is shorter, runs faster on most modern engines, and is the convention in OMOP analytics code written in the last several years.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Question 5: How many patient-years of TNFi exposure does each group represent?

        "Patient-years" is the standard denominator for incidence rates. Course 04 Track 01 introduced the concept: if 10 patients are followed for 1 year each, the cohort has accumulated 10 patient-years; if 20 patients are followed for 6 months each, the cohort has also accumulated 10 patient-years. Person-time honors the fact that follow-up is unequal across patients in most real studies.

        For a drug-exposure question, patient-years answers "how long has the cohort, collectively, been on this drug." The number is used as the denominator in incidence-rate calculations like "infections per patient-year on TNFi." A larger denominator is one of the two ways an incidence rate can fall (the other being a smaller numerator).

        The OMOP `drug_exposure` table holds one row per exposure period with `drug_exposure_start_date` and `drug_exposure_end_date`. Patient-time is the sum of `(end_date - start_date)` across all rows for the drug of interest, converted from days to years by dividing by 365.25.

        Two SQL details need handling. First, when an exposure is ongoing (the patient is still on the drug today), the end_date is NULL. Arithmetic on a NULL produces NULL, which would silently drop the patient from the sum. The query uses `COALESCE(end_date, '2026-05-24')` to substitute a fixed observation cutoff in place of NULL. Second, SQLite stores dates as text; the `julianday()` function converts a date to a number representing days, which lets the arithmetic happen.

        The query below reads in two parts.

        **The `adalimumab_exposure` CTE** prepares the input rows.

        - `SELECT person_id, drug_exposure_start_date AS start_date, COALESCE(drug_exposure_end_date, '2026-05-24') AS end_date`. For each matching drug exposure row, return the patient, the start date, and the end date (substituting today's cutoff date when the end is NULL).
        - `FROM drug_exposure WHERE drug_concept_id = 1119119`. Only consider rows for adalimumab.

        **The main query** sums the durations.

        - `SELECT COUNT(DISTINCT person_id) AS n_patients`. Count the unique patients in the CTE (each patient is counted once even if they have multiple exposure rows).
        - `ROUND(SUM(julianday(end_date) - julianday(start_date)) / 365.25, 2) AS adalimumab_patient_years`. For each row, convert both dates to day numbers, subtract to get the duration in days, sum across all rows, divide by 365.25 to convert days to years, round to 2 decimals.
        - `FROM adalimumab_exposure`. Read from the CTE just defined.
        """
    )
    return


@app.cell
def _(con, pd):
    _sql_q5 = """
        WITH adalimumab_exposure AS (
            SELECT
                person_id,
                drug_exposure_start_date AS start_date,
                COALESCE(drug_exposure_end_date, '2026-05-24') AS end_date
            FROM drug_exposure
            WHERE drug_concept_id = 1119119
        )
        SELECT
            COUNT(DISTINCT person_id) AS n_patients,
            ROUND(SUM(julianday(end_date) - julianday(start_date)) / 365.25, 2)
                AS adalimumab_patient_years
        FROM adalimumab_exposure;
    """
    result_q5 = pd.read_sql_query(_sql_q5, con)
    result_q5.index = range(1, len(result_q5) + 1)
    result_q5.index.name = "row"
    result_q5
    return (result_q5,)


@app.cell
def _(mo):
    mo.md(
        r"""
        The result has one row with two values: `n_patients` is the count of patients ever exposed to adalimumab, and `adalimumab_patient_years` is the total person-time those patients accumulated on the drug.

        Clinical reading. Five of the ten patients in the cohort have ever been on adalimumab. The patient-year total tells the team the size of the denominator they would use if they wanted to compute an incidence rate (for example, serious infections per patient-year on TNFi). The denominator alone does not answer the clinical question; it is the input the numerator queries divide into.

        Three SQL patterns in this query recur in any OMOP exposure analysis.

        - **`COALESCE(end_date, cutoff)`** substitutes a fixed value when the end_date is NULL. Without it, ongoing exposures would silently contribute zero patient-time, and the total would understate exposure by the entire duration of every currently-on-treatment patient.
        - **`julianday(date)`** converts a date to a continuous numeric day count, so that subtraction gives a duration in days. Different SQL engines have different functions for this (`DATE_DIFF` in BigQuery, `EXTRACT(EPOCH FROM ...)` in PostgreSQL); the underlying operation is the same.
        - **`COUNT(DISTINCT person_id) ... SUM(duration)`** in the same query returns both the patient count and the patient-time. This is the canonical numerator-and-denominator pair for an incidence-rate calculation.

        The same query against a real OMOP warehouse would replace the hardcoded cutoff date with the patient's `observation_period_end_date` (the OMOP-idiomatic per-patient cutoff) and would group by `drug_concept_id` if the analysis spanned multiple drugs.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Reactive cohort builder

        The cell below is the first interactive cohort definition in the course. Three controls (minimum most-recent CRP, minimum baseline DAS28, treatment group) determine the cohort. Whenever a control is adjusted, the cell below it re-runs the SQL query with the new filter values and displays the resulting cohort.

        The interaction makes the relationship between a cohort definition and the resulting patient set tangible. Tighter inclusion criteria produce smaller cohorts; looser criteria produce larger cohorts. The same shape is what production cohort design tools (OHDSI's ATLAS being the canonical example) expose, with a richer set of controls and a SQL query that runs against a production warehouse rather than this in-memory database.
        """
    )
    return


@app.cell
def _(mo):
    crp_min = mo.ui.slider(
        start=0, stop=60, step=2, value=0,
        label="Minimum most-recent CRP (mg/L)",
        show_value=True, full_width=True,
    )
    das28_min = mo.ui.slider(
        start=0.0, stop=6.0, step=0.5, value=0.0,
        label="Minimum baseline DAS28",
        show_value=True, full_width=True,
    )
    tx_group = mo.ui.radio(
        options=["Any", "TNFi", "csDMARD"],
        label="Treatment group",
        value="Any",
    )
    mo.vstack([crp_min, das28_min, tx_group])
    return crp_min, das28_min, tx_group


@app.cell
def _(con, crp_min, das28_min, mo, pd, tx_group):
    _treatment_filter = ""
    if tx_group.value == "TNFi":
        _treatment_filter = (
            "AND EXISTS ("
            "  SELECT 1 FROM drug_exposure d "
            "  WHERE d.person_id = p.person_id AND d.drug_concept_id = 1119119"
            ")"
        )
    elif tx_group.value == "csDMARD":
        _treatment_filter = (
            "AND NOT EXISTS ("
            "  SELECT 1 FROM drug_exposure d "
            "  WHERE d.person_id = p.person_id AND d.drug_concept_id = 1119119"
            ")"
        )

    _sql_cohort = f"""
        WITH recent_crp AS (
            SELECT person_id, value_as_number AS crp
            FROM (
                SELECT person_id, value_as_number,
                    ROW_NUMBER() OVER (PARTITION BY person_id ORDER BY measurement_date DESC) AS rn
                FROM measurement
                WHERE measurement_concept_id = 3010156
            )
            WHERE rn = 1
        ),
        baseline_das28 AS (
            SELECT person_id, value_as_number AS das28
            FROM (
                SELECT person_id, value_as_number,
                    ROW_NUMBER() OVER (PARTITION BY person_id ORDER BY observation_date ASC) AS rn
                FROM observation
                WHERE observation_concept_id = 40766949
            )
            WHERE rn = 1
        )
        SELECT
            p.person_id,
            ROUND(r.crp, 1) AS most_recent_crp,
            ROUND(b.das28, 2) AS baseline_das28
        FROM person p
        JOIN recent_crp r ON r.person_id = p.person_id
        JOIN baseline_das28 b ON b.person_id = p.person_id
        WHERE r.crp >= {float(crp_min.value)}
          AND b.das28 >= {float(das28_min.value)}
          {_treatment_filter}
        ORDER BY p.person_id;
    """
    cohort_result = pd.read_sql_query(_sql_cohort, con)
    cohort_result.index = range(1, len(cohort_result) + 1)
    cohort_result.index.name = "row"
    summary = mo.md(
        f"**Cohort size:** {len(cohort_result)} patients of 10 in the warehouse."
    )
    mo.vstack([summary, cohort_result])
    return cohort_result, summary


@app.cell
def _(mo):
    q1 = mo.ui.radio(
        options=[
            "GROUP BY collapses rows; window functions add a column to each row without collapsing.",
            "Window functions are faster than GROUP BY.",
            "Window functions support COUNT; GROUP BY does not.",
            "GROUP BY runs first; window functions run after.",
        ],
        label=(
            "What is the structural difference between a `GROUP BY` aggregation "
            "and a window function?"
        ),
    )
    q1
    return (q1,)


@app.cell
def _(mo, q1):
    if q1.value is None:
        out1 = mo.md("_Pick one._")
    else:
        correct1 = q1.value.startswith("GROUP BY collapses")
        out1 = mo.callout(
            mo.md(
                rf"""
                **{'Correct.' if correct1 else 'Not quite.'}**

                `GROUP BY` collapses multiple rows into one row per group. A query that groups by `person_id` returns one row per patient, regardless of how many rows that patient had in the source table. A window function leaves the row count unchanged and adds a computed value to each row. The window's `PARTITION BY` clause defines the group used for the computation, and the `ORDER BY` clause defines the row ordering within the group. The most-recent-CRP query in this track uses `ROW_NUMBER() OVER (PARTITION BY person_id ORDER BY measurement_date DESC)` to label each patient's measurements 1, 2, 3, then filters to `rn = 1` to keep only the most recent. The same task expressed with `GROUP BY` would require a self-join, because `GROUP BY` cannot return the date and the value of the row it selected; it can only return aggregates over the group.
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
            "Patients with NULL end dates would be excluded from the sum entirely.",
            "Patients with NULL end dates would be counted as having zero days of exposure.",
            "The query would error.",
            "Nothing would change; SQLite treats NULL dates as today by default.",
        ],
        label=(
            "The patient-years query for adalimumab used "
            "`COALESCE(drug_exposure_end_date, '2026-05-24')`. What would "
            "happen if that COALESCE were removed?"
        ),
    )
    q2
    return (q2,)


@app.cell
def _(mo, q2):
    if q2.value is None:
        out2 = mo.md("_Pick one._")
    else:
        correct2 = q2.value.startswith("Patients with NULL end dates would be excluded")
        out2 = mo.callout(
            mo.md(
                rf"""
                **{'Correct.' if correct2 else 'Not quite.'}**

                In SQL, an arithmetic operation involving NULL returns NULL. Subtracting `julianday(NULL)` from any date yields NULL; `SUM` over a set that includes NULLs ignores the NULLs and reports the sum of the non-NULL values. Patients with ongoing exposure (NULL `drug_exposure_end_date`) would therefore contribute nothing to the patient-time sum, and the result would understate exposure by the entire duration of ongoing treatment. The `COALESCE` substitutes a fixed cutoff date when the end_date is NULL, so ongoing exposures are correctly accumulated from start to the cutoff. The `COUNT(DISTINCT person_id)` in the same query would be unaffected, which would mask the underestimate from a casual reader.
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

        Pick one of the two prompts below and write 4 to 6 sentences in the box that follows. Save what you write outside the browser; the box is a scratch pad, not persistent storage. When you are done, continue to `track-04-pandas`.

        1. **An analytic question from your own work** required pulling data from a clinical warehouse. State the question, name the OMOP tables that would carry the relevant facts, and sketch (in prose, not SQL) the joins and filters that would produce the answer. Identify the one query construct from this track (cohort filter, GROUP BY aggregation, window function, date arithmetic) that does the central work.

        2. **A clinical colleague proposes** that an analyst should "just give me a spreadsheet with all the data." Explain why writing the SQL query against the warehouse is preferable to exporting the full warehouse to a spreadsheet, in terms a clinical reader will accept. Identify the failure mode of the spreadsheet approach and the operational risk of bypassing the SQL extraction step.
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
        "The post-extraction layer is pandas.",
        (
            "SQL returns a flat tabular result from the warehouse. The result "
            "is the analytic cohort. Track 04 introduces pandas as the language "
            "used for the analysis that follows extraction: tidying, "
            "per-patient summaries, time-since-event calculations, and "
            "comparisons across groups. The same operations are also available "
            "in DuckDB, polars, and dplyr; pandas is used in this course "
            "because it is the most common Python option and reads well in a "
            "notebook. Continue to `track-04-pandas`."
        ),
    )
    return


if __name__ == "__main__":
    app.run()
