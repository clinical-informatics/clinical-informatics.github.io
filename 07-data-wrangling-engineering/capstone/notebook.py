"""Capstone for Course 07: Data wrangling and engineering.

Three messy raw data files arrive from the source EHR. The capstone
maps them to OMOP shape, then runs three clinical queries against the
mapped output, one query per analytic layer the course covered:
cohort definition in SQL (Track 03), per-patient summary in pandas
(Track 04), and a sequence question that exposes the kind of problem
graph databases are designed for (Track 05). Code standards (Track 01)
and OMOP CDM (Track 02) supply the targets the mapping aims at.

The capstone is structured as a sequence of Socratic prompts:
commit a written answer, then reveal the worked solution. The intent
is to make the analytic decisions explicit before the code shows the
mechanics.
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
            mo.md(f"**Callback to {_course_label(to_course)}.** {topic}\n\n{body}"),
            kind="neutral",
        )

    def _xref_forward(from_course, to_course, topic, body):
        return mo.callout(
            mo.md(f"**Forward to {_course_label(to_course)}.** {topic}\n\n{body}"),
            kind="neutral",
        )

    xref = types.SimpleNamespace(callback=_xref_callback, forward=_xref_forward)

    # Socratic helpers inlined from shared/socratic.py so the WASM export
    # is self-contained.
    def commit_text(prompt, *, min_chars=40):
        widget = mo.ui.text_area(
            label=prompt,
            rows=6,
            full_width=True,
            placeholder="Write your answer here. The sample solution unlocks once you commit.",
        )

        def _ready():
            v = widget.value or ""
            return len(v.strip()) >= min_chars

        return widget, _ready

    def reveal(learner_value, ideal_answer, *, learner_label="Your answer"):
        return mo.vstack(
            [
                mo.callout(
                    mo.md(f"**{learner_label}.**\n\n{learner_value or '_(empty)_'}"),
                    kind="neutral",
                ),
                mo.callout(
                    mo.md(f"**Sample solution.**\n\n{ideal_answer}"),
                    kind="info",
                ),
            ]
        )

    return commit_text, mo, np, pd, reveal, sqlite3, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Capstone: from raw EHR data to a clinical answer

        ## Scenario

        Three raw data files arrive from the source EHR for a small rheumatology cohort. The files do not conform to OMOP shape, the codes are not consistent, and the dates are stored as text in multiple formats. The analytic team needs to map the files into an OMOP-shaped database and then answer three clinical questions against the mapped output.

        This capstone follows the same sequence the course presented: first the standards layer (which codes count for what), then the OMOP mapping (what tables get which rows), then the extraction and analysis layers (SQL and pandas), and finally a question whose shape begins to look like the graph problems Track 05 introduced.

        The work is presented as a series of Socratic prompts. Each prompt asks for a written answer first, then unlocks a worked solution for comparison.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The three raw input files

        File 1 is a lab export. Each row is one lab result. The values are stored as text because the source system reports below-detection-limit results as inequality strings ("<2.0"). Dates are in `MM/DD/YYYY` format because that is what the export tool defaulted to.
        """
    )
    return


@app.cell
def _(pd):
    raw_labs = pd.DataFrame(
        [
            {"mrn": "ER-001", "test_code": "1988-5",  "test_name": "CRP",                 "value": "42.1",  "unit": "mg/L",  "date": "02/14/2022"},
            {"mrn": "ER-001", "test_code": "4537-7",  "test_name": "ESR",                 "value": "58",    "unit": "mm/h",  "date": "02/14/2022"},
            {"mrn": "ER-001", "test_code": "32218-7", "test_name": "anti-CCP",            "value": "178",   "unit": "U/mL",  "date": "02/14/2022"},
            {"mrn": "ER-001", "test_code": "1988-5",  "test_name": "CRP",                 "value": "36.2",  "unit": "mg/L",  "date": "01/08/2024"},
            {"mrn": "ER-001", "test_code": "1988-5",  "test_name": "CRP",                 "value": "<2.0",  "unit": "mg/L",  "date": "05/12/2025"},
            {"mrn": "ER-002", "test_code": "1988-5",  "test_name": "CRP",                 "value": "28.5",  "unit": "mg/L",  "date": "06/03/2022"},
            {"mrn": "ER-002", "test_code": "1988-5",  "test_name": "CRP",                 "value": "14.1",  "unit": "mg/L",  "date": "12/19/2023"},
            {"mrn": "ER-003", "test_code": "1988-5",  "test_name": "CRP",                 "value": "51.4",  "unit": "mg/L",  "date": "03/22/2022"},
            {"mrn": "ER-003", "test_code": "1988-5",  "test_name": "CRP",                 "value": "8.9",   "unit": "mg/L",  "date": "11/05/2024"},
            {"mrn": "ER-004", "test_code": "1988-5",  "test_name": "CRP",                 "value": "19.7",  "unit": "mg/L",  "date": "04/10/2023"},
            {"mrn": "ER-004", "test_code": "1988-5",  "test_name": "CRP",                 "value": "12.4",  "unit": "mg/L",  "date": "09/18/2024"},
            {"mrn": "ER-005", "test_code": "1988-5",  "test_name": "C-reactive protein",  "value": "45.0",  "unit": "mg/L",  "date": "08/01/2022"},
            {"mrn": "ER-005", "test_code": "1988-5",  "test_name": "C-reactive protein",  "value": "7.2",   "unit": "mg/L",  "date": "02/15/2024"},
        ]
    )
    raw_labs.index = range(1, len(raw_labs) + 1)
    raw_labs.index.name = "row"
    raw_labs
    return (raw_labs,)


@app.cell
def _(mo):
    mo.md(
        r"""
        File 2 is a medications log. Each row is one prescription order. The drug name is free text from the order entry screen, with no structured drug code attached. Dates use `MM/DD/YYYY` again. The end_date is blank for ongoing prescriptions, which is the convention this source EHR uses.
        """
    )
    return


@app.cell
def _(pd):
    raw_meds = pd.DataFrame(
        [
            {"mrn": "ER-001", "drug_name": "methotrexate 25mg SC weekly",     "start": "03/07/2022", "end": ""},
            {"mrn": "ER-001", "drug_name": "folic acid 1mg PO daily",         "start": "03/07/2022", "end": ""},
            {"mrn": "ER-001", "drug_name": "adalimumab 40mg SC q14d",         "start": "01/08/2024", "end": ""},
            {"mrn": "ER-001", "drug_name": "prednisone 15-10-5 mg PO taper",  "start": "11/21/2025", "end": "12/06/2025"},
            {"mrn": "ER-002", "drug_name": "methotrexate 15mg SC weekly",     "start": "06/05/2022", "end": ""},
            {"mrn": "ER-002", "drug_name": "folic acid 1mg PO daily",         "start": "06/05/2022", "end": ""},
            {"mrn": "ER-003", "drug_name": "methotrexate 20mg SC weekly",     "start": "03/25/2022", "end": ""},
            {"mrn": "ER-003", "drug_name": "etanercept 50mg SC weekly",       "start": "11/10/2024", "end": ""},
            {"mrn": "ER-004", "drug_name": "methotrexate 20mg SC weekly",     "start": "04/12/2023", "end": ""},
            {"mrn": "ER-005", "drug_name": "methotrexate 25mg SC weekly",     "start": "08/03/2022", "end": ""},
            {"mrn": "ER-005", "drug_name": "infliximab 5 mg/kg IV q8w",       "start": "02/20/2024", "end": ""},
        ]
    )
    raw_meds.index = range(1, len(raw_meds) + 1)
    raw_meds.index.name = "row"
    raw_meds
    return (raw_meds,)


@app.cell
def _(mo):
    mo.md(
        r"""
        File 3 is the encounter file. The visit_type column carries the source EHR's internal codes (OFF for office visit, TEL for telehealth, INP for inpatient). The diagnosis column carries ICD-10-CM codes as text. Each row is one encounter with the primary diagnosis attached.
        """
    )
    return


@app.cell
def _(pd):
    raw_encounters = pd.DataFrame(
        [
            {"mrn": "ER-001", "visit_id": "V100",  "visit_type": "OFF", "visit_date": "02/14/2022", "primary_dx": "M05.79"},
            {"mrn": "ER-001", "visit_id": "V101",  "visit_type": "OFF", "visit_date": "03/07/2022", "primary_dx": "M05.79"},
            {"mrn": "ER-001", "visit_id": "V102",  "visit_type": "OFF", "visit_date": "01/08/2024", "primary_dx": "M05.79"},
            {"mrn": "ER-001", "visit_id": "V103",  "visit_type": "TEL", "visit_date": "05/12/2025", "primary_dx": "M05.79"},
            {"mrn": "ER-002", "visit_id": "V200",  "visit_type": "OFF", "visit_date": "06/03/2022", "primary_dx": "M06.9"},
            {"mrn": "ER-002", "visit_id": "V201",  "visit_type": "OFF", "visit_date": "06/05/2022", "primary_dx": "M06.9"},
            {"mrn": "ER-002", "visit_id": "V202",  "visit_type": "OFF", "visit_date": "12/19/2023", "primary_dx": "M06.9"},
            {"mrn": "ER-003", "visit_id": "V300",  "visit_type": "OFF", "visit_date": "03/22/2022", "primary_dx": "M05.79"},
            {"mrn": "ER-003", "visit_id": "V301",  "visit_type": "OFF", "visit_date": "03/25/2022", "primary_dx": "M05.79"},
            {"mrn": "ER-003", "visit_id": "V302",  "visit_type": "OFF", "visit_date": "11/10/2024", "primary_dx": "M05.79"},
            {"mrn": "ER-004", "visit_id": "V400",  "visit_type": "OFF", "visit_date": "04/10/2023", "primary_dx": "M06.00"},
            {"mrn": "ER-004", "visit_id": "V401",  "visit_type": "OFF", "visit_date": "04/12/2023", "primary_dx": "M06.00"},
            {"mrn": "ER-005", "visit_id": "V500",  "visit_type": "OFF", "visit_date": "08/01/2022", "primary_dx": "M05.79"},
            {"mrn": "ER-005", "visit_id": "V501",  "visit_type": "OFF", "visit_date": "08/03/2022", "primary_dx": "M05.79"},
            {"mrn": "ER-005", "visit_id": "V502",  "visit_type": "OFF", "visit_date": "02/20/2024", "primary_dx": "M05.79"},
            {"mrn": "ER-005", "visit_id": "V503",  "visit_type": "INP", "visit_date": "07/14/2025", "primary_dx": "L03.115"},
        ]
    )
    raw_encounters.index = range(1, len(raw_encounters) + 1)
    raw_encounters.index.name = "row"
    raw_encounters
    return (raw_encounters,)


@app.cell
def _(commit_text):
    step1_widget, step1_ready = commit_text(
        "**Step 1: the mapping plan.** "
        "Write the mapping plan in 4 to 6 sentences. For each of the three "
        "input files, state which OMOP table the rows will land in, which "
        "columns of the source file will need standardization (codes, units, "
        "dates), and which OMOP concept_ids you will need to look up before "
        "the mapping can run. Identify at least one input row whose mapping "
        "is ambiguous and state how you would resolve the ambiguity.",
        min_chars=180,
    )
    step1_widget
    return step1_ready, step1_widget


@app.cell
def _(mo, reveal, step1_ready, step1_widget):
    mo.stop(
        not step1_ready(),
        mo.md("_Write the mapping plan above. The sample solution unlocks when you commit._"),
    )
    reveal(
        step1_widget.value,
        (
            "The lab export maps to **measurement**. Each row already carries "
            "a LOINC code in the `test_code` column, so the standardization "
            "needed is the LOINC-to-concept_id lookup (LOINC 1988-5 -> "
            "concept 3010156, and so on), the conversion of the `date` column "
            "from MM/DD/YYYY to ISO format, and the handling of the `<2.0` "
            "value, which is a below-detection-limit result and should land in "
            "`value_as_number` with `operator_concept_id` recording the "
            "less-than relationship.\n\n"
            "The medications log maps to **drug_exposure**. The "
            "standardization needed is the free-text-to-RxNorm lookup on "
            "`drug_name` (parsing the active ingredient out of strings like "
            "'methotrexate 25mg SC weekly' is the central work), the same "
            "MM/DD/YYYY-to-ISO date conversion, and the conversion of empty "
            "`end` values to NULL for the OMOP ongoing-exposure convention.\n\n"
            "The encounter file maps to **visit_occurrence** (one row per "
            "visit) and to **condition_occurrence** (one row per primary "
            "diagnosis attached to a visit). The vendor visit-type codes "
            "(OFF, TEL, INP) need lookup to OMOP visit concept_ids (9202, "
            "5083, 9201). The ICD-10-CM codes in `primary_dx` need lookup to "
            "OMOP condition concept_ids.\n\n"
            "**Ambiguous row.** The L03.115 diagnosis on encounter V503 "
            "(cellulitis of right lower limb) appears unrelated to the RA "
            "cohort but is a primary diagnosis on an inpatient visit. "
            "Resolution: include it as a condition_occurrence row regardless. "
            "Cohort definition belongs in the downstream query, not in the "
            "mapping; the mapping should preserve every fact."
        ),
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Mapping the raw files to OMOP shape

        The cell below performs the mapping. The result is five OMOP-shaped DataFrames (person, visit_occurrence, condition_occurrence, drug_exposure, measurement) loaded into an in-memory SQLite database, ready for the three clinical queries that follow.
        """
    )
    return


@app.cell
def _(pd, raw_encounters, raw_labs, raw_meds, sqlite3):
    # Patient identifier mapping: MRN to OMOP person_id
    _mrn_to_pid = {
        "ER-001": 1001, "ER-002": 2001, "ER-003": 2002,
        "ER-004": 2003, "ER-005": 2004,
    }

    # OMOP person table: one row per patient
    person = pd.DataFrame([
        {"person_id": _pid, "gender_concept_id": 8532, "year_of_birth": 1974,
         "race_concept_id": 8527, "person_source_value": _mrn}
        for _mrn, _pid in _mrn_to_pid.items()
    ])

    # OMOP visit_occurrence table
    _visit_type_to_concept = {"OFF": 9202, "TEL": 5083, "INP": 9201}
    _visit_rows = []
    _visit_id_seq = 5001
    _visit_lookup = {}
    for _, _r in raw_encounters.iterrows():
        _omop_visit_id = _visit_id_seq
        _visit_id_seq += 1
        _visit_lookup[_r["visit_id"]] = _omop_visit_id
        _visit_rows.append({
            "visit_occurrence_id": _omop_visit_id,
            "person_id": _mrn_to_pid[_r["mrn"]],
            "visit_concept_id": _visit_type_to_concept[_r["visit_type"]],
            "visit_start_date": pd.to_datetime(_r["visit_date"], format="%m/%d/%Y").strftime("%Y-%m-%d"),
            "visit_end_date":   pd.to_datetime(_r["visit_date"], format="%m/%d/%Y").strftime("%Y-%m-%d"),
            "visit_source_value": _r["visit_type"],
        })
    visit_occurrence = pd.DataFrame(_visit_rows)

    # OMOP condition_occurrence: one row per primary diagnosis per visit
    _icd_to_concept = {
        "M05.79": 4138406,
        "M06.9":  4297653,
        "M06.00": 4309217,
        "L03.115": 4079651,
    }
    _condition_rows = []
    _cond_id_seq = 6001
    for _, _r in raw_encounters.iterrows():
        _condition_rows.append({
            "condition_occurrence_id": _cond_id_seq,
            "person_id": _mrn_to_pid[_r["mrn"]],
            "condition_concept_id": _icd_to_concept.get(_r["primary_dx"], 0),
            "condition_start_date": pd.to_datetime(_r["visit_date"], format="%m/%d/%Y").strftime("%Y-%m-%d"),
            "condition_source_value": _r["primary_dx"],
            "visit_occurrence_id": _visit_lookup[_r["visit_id"]],
        })
        _cond_id_seq += 1
    condition_occurrence = pd.DataFrame(_condition_rows)

    # OMOP drug_exposure
    def _drug_to_concept(name):
        _name = name.lower()
        if "methotrexate" in _name: return 1503297
        if "adalimumab"   in _name: return 1119119
        if "etanercept"   in _name: return 1151789
        if "infliximab"   in _name: return 1151287
        if "prednisone"   in _name: return 975125
        if "folic acid"   in _name: return 1714165
        return 0
    _drug_rows = []
    _drug_id_seq = 7001
    for _, _r in raw_meds.iterrows():
        _drug_rows.append({
            "drug_exposure_id": _drug_id_seq,
            "person_id": _mrn_to_pid[_r["mrn"]],
            "drug_concept_id": _drug_to_concept(_r["drug_name"]),
            "drug_exposure_start_date": pd.to_datetime(_r["start"], format="%m/%d/%Y").strftime("%Y-%m-%d"),
            "drug_exposure_end_date": (
                pd.to_datetime(_r["end"], format="%m/%d/%Y").strftime("%Y-%m-%d")
                if _r["end"] != "" else None
            ),
            "drug_source_value": _r["drug_name"],
        })
        _drug_id_seq += 1
    drug_exposure = pd.DataFrame(_drug_rows)

    # OMOP measurement
    _loinc_to_concept = {"1988-5": 3010156, "4537-7": 3015632, "32218-7": 3007220}
    _meas_rows = []
    _meas_id_seq = 8001
    for _, _r in raw_labs.iterrows():
        _value_str = str(_r["value"]).strip()
        if _value_str.startswith("<"):
            _value_num = float(_value_str.lstrip("<"))
            _operator = 4171756  # OMOP concept for "Less than"
        else:
            _value_num = float(_value_str)
            _operator = None
        _meas_rows.append({
            "measurement_id": _meas_id_seq,
            "person_id": _mrn_to_pid[_r["mrn"]],
            "measurement_concept_id": _loinc_to_concept.get(_r["test_code"], 0),
            "measurement_date": pd.to_datetime(_r["date"], format="%m/%d/%Y").strftime("%Y-%m-%d"),
            "value_as_number": _value_num,
            "unit_source_value": _r["unit"],
            "measurement_source_value": _r["test_code"],
            "operator_concept_id": _operator,
        })
        _meas_id_seq += 1
    measurement = pd.DataFrame(_meas_rows)

    # Load into in-memory SQLite for the SQL query in step 3
    con = sqlite3.connect(":memory:")
    person.to_sql("person", con, if_exists="replace", index=False)
    visit_occurrence.to_sql("visit_occurrence", con, if_exists="replace", index=False)
    condition_occurrence.to_sql("condition_occurrence", con, if_exists="replace", index=False)
    drug_exposure.to_sql("drug_exposure", con, if_exists="replace", index=False)
    measurement.to_sql("measurement", con, if_exists="replace", index=False)
    return condition_occurrence, con, drug_exposure, measurement, person, visit_occurrence


@app.cell
def _(condition_occurrence, drug_exposure, measurement, mo, person, visit_occurrence):
    mo.md(
        f"""
        **Mapping complete.** Five OMOP tables loaded:

        - person: **{len(person)} rows**
        - visit_occurrence: **{len(visit_occurrence)} rows**
        - condition_occurrence: **{len(condition_occurrence)} rows**
        - drug_exposure: **{len(drug_exposure)} rows**
        - measurement: **{len(measurement)} rows**
        """
    )
    return


@app.cell
def _(condition_occurrence):
    co_display = condition_occurrence.copy()
    co_display.index = range(1, len(co_display) + 1)
    co_display.index.name = "row"
    co_display
    return (co_display,)


@app.cell
def _(commit_text):
    step2_widget, step2_ready = commit_text(
        "**Step 2: cohort definition.** "
        "Write the SQL (in prose if you prefer, or as a SQL skeleton) that "
        "defines the RA cohort against the OMOP tables above. Identify the "
        "exact OMOP concept_ids you would filter on, the table the filter "
        "targets, and how you would handle the L03.115 row that survived the "
        "mapping but is not RA. State whether the cohort should be defined "
        "as 'any patient with at least one RA diagnosis' or as 'patients "
        "whose primary diagnosis is RA at the majority of their visits' and "
        "justify the choice.",
        min_chars=200,
    )
    step2_widget
    return step2_ready, step2_widget


@app.cell
def _(con, mo, pd, reveal, step2_ready, step2_widget):
    mo.stop(
        not step2_ready(),
        mo.md("_Write the cohort definition above. The worked SQL unlocks when you commit._"),
    )

    _sql_cohort = """
        SELECT DISTINCT person_id
        FROM condition_occurrence
        WHERE condition_concept_id IN (4138406, 4297653, 4309217)
        ORDER BY person_id;
    """
    _cohort = pd.read_sql_query(_sql_cohort, con)
    _cohort.index = range(1, len(_cohort) + 1)
    _cohort.index.name = "row"

    reveal(
        step2_widget.value,
        (
            "The cohort filter is on `condition_occurrence.condition_concept_id` "
            "in the set of concepts representing RA "
            "(4138406 for M05.79, 4297653 for M06.9, 4309217 for M06.00). "
            "`SELECT DISTINCT person_id` collapses multiple diagnosis rows per "
            "patient into the unique patient set. The L03.115 (cellulitis) row "
            "is correctly excluded because its concept_id is not in the RA set. "
            "The 'any patient with at least one RA diagnosis' definition is the "
            "standard choice for an RA registry; the 'majority of visits' "
            "alternative would exclude patients whose RA is managed primarily "
            "outside the rheumatology clinic, which is not what we want.\n\n"
            "Worked SQL:\n\n"
            "```sql\n"
            "SELECT DISTINCT person_id\n"
            "FROM condition_occurrence\n"
            "WHERE condition_concept_id IN (4138406, 4297653, 4309217)\n"
            "ORDER BY person_id;\n"
            "```\n\n"
            f"**Result:** {len(_cohort)} patients in the RA cohort."
        ),
    )
    return


@app.cell
def _(commit_text):
    step3_widget, step3_ready = commit_text(
        "**Step 3: per-patient summary.** "
        "Write the pandas operations (in prose) that produce a one-row-per-"
        "patient summary with the most recent CRP value, the date of that "
        "value, and the number of days since the patient's last visit. "
        "Identify the dtype conversion that has to happen first, the "
        "groupby-and-sort sequence that returns the most recent CRP, and "
        "the merge that attaches the most-recent-visit-date column.",
        min_chars=180,
    )
    step3_widget
    return step3_ready, step3_widget


@app.cell
def _(measurement, mo, pd, reveal, step3_ready, step3_widget, visit_occurrence):
    mo.stop(
        not step3_ready(),
        mo.md("_Write the pandas plan above. The worked code unlocks when you commit._"),
    )

    _meas = measurement.copy()
    _meas["measurement_date"] = pd.to_datetime(_meas["measurement_date"])
    _crp = _meas[_meas["measurement_concept_id"] == 3010156]
    _recent_crp = (
        _crp
        .sort_values(["person_id", "measurement_date"], ascending=[True, False])
        .groupby("person_id")
        .head(1)
        [["person_id", "measurement_date", "value_as_number"]]
        .rename(columns={
            "measurement_date": "most_recent_crp_date",
            "value_as_number":  "most_recent_crp",
        })
    )
    _visits = visit_occurrence.copy()
    _visits["visit_start_date"] = pd.to_datetime(_visits["visit_start_date"])
    _last_visit = (
        _visits
        .sort_values(["person_id", "visit_start_date"], ascending=[True, False])
        .groupby("person_id")
        .head(1)
        [["person_id", "visit_start_date"]]
        .rename(columns={"visit_start_date": "last_visit_date"})
    )
    _summary = _recent_crp.merge(_last_visit, on="person_id")
    _summary["days_since_last_visit"] = (
        pd.Timestamp("2026-05-24") - _summary["last_visit_date"]
    ).dt.days
    _summary.index = range(1, len(_summary) + 1)
    _summary.index.name = "row"

    _reveal_widget = reveal(
        step3_widget.value,
        (
            "Three operations chain together. First, convert "
            "`measurement_date` and `visit_start_date` from text to datetime; "
            "every downstream comparison and arithmetic relies on the typed "
            "columns. Second, filter the measurement table to CRP rows "
            "(concept_id 3010156), sort by (person_id ascending, "
            "measurement_date descending), and take the first row per "
            "person with `groupby(person_id).head(1)`. Third, do the same "
            "sort-and-head against `visit_occurrence` to get each patient's "
            "most recent visit date, then `merge` the two per-person results "
            "on `person_id`. Subtract a fixed observation cutoff from the "
            "last visit date to get `days_since_last_visit`.\n\n"
            "**Worked pandas:**\n\n"
            "```python\n"
            "# Step A: convert dates and isolate CRP rows.\n"
            "meas = measurement.copy()\n"
            "meas['measurement_date'] = pd.to_datetime(meas['measurement_date'])\n"
            "crp = meas[meas['measurement_concept_id'] == 3010156]\n"
            "\n"
            "# Step B: most recent CRP per patient.\n"
            "recent_crp = (\n"
            "    crp\n"
            "    .sort_values(['person_id', 'measurement_date'],\n"
            "                 ascending=[True, False])\n"
            "    .groupby('person_id').head(1)\n"
            "    [['person_id', 'measurement_date', 'value_as_number']]\n"
            "    .rename(columns={\n"
            "        'measurement_date': 'most_recent_crp_date',\n"
            "        'value_as_number':  'most_recent_crp',\n"
            "    })\n"
            ")\n"
            "\n"
            "# Step C: most recent visit per patient.\n"
            "visits = visit_occurrence.copy()\n"
            "visits['visit_start_date'] = pd.to_datetime(visits['visit_start_date'])\n"
            "last_visit = (\n"
            "    visits\n"
            "    .sort_values(['person_id', 'visit_start_date'],\n"
            "                 ascending=[True, False])\n"
            "    .groupby('person_id').head(1)\n"
            "    [['person_id', 'visit_start_date']]\n"
            "    .rename(columns={'visit_start_date': 'last_visit_date'})\n"
            ")\n"
            "\n"
            "# Step D: combine, then compute days-since-visit.\n"
            "summary = recent_crp.merge(last_visit, on='person_id')\n"
            "summary['days_since_last_visit'] = (\n"
            "    pd.Timestamp('2026-05-24') - summary['last_visit_date']\n"
            ").dt.days\n"
            "```\n\n"
            "**Reading the chain.**\n\n"
            "- `pd.to_datetime(...)` converts the text date columns to true datetime so that subtraction and comparisons work as expected (Track 04's date-boundary rule).\n"
            "- `crp = meas[meas['measurement_concept_id'] == 3010156]` filters down to CRP rows only.\n"
            "- The `recent_crp` block sorts each patient's CRP rows newest-first and keeps the top row per patient, leaving one row per patient with the most recent CRP date and value.\n"
            "- The `last_visit` block does the same against the visit table.\n"
            "- `merge(... on='person_id')` joins the two per-patient tables side by side; subtracting two datetimes gives a Timedelta whose `.dt.days` accessor yields the integer day count.\n\n"
            "Result below."
        ),
    )
    mo.vstack([_reveal_widget, mo.callout(_summary, kind="info")])
    return


@app.cell
def _(commit_text):
    step4_widget, step4_ready = commit_text(
        "**Step 4: the sequence question.** "
        "For each patient in the cohort, list the sequence of therapy "
        "regimen changes: when did the patient start their first csDMARD, "
        "and when (if ever) did they add or switch to a TNFi? Describe how "
        "you would compute this in SQL or pandas, and identify the point at "
        "which a graph data model would make the query more natural. State "
        "what the graph nodes and edges would be in that formulation.",
        min_chars=200,
    )
    step4_widget
    return step4_ready, step4_widget


@app.cell
def _(drug_exposure, mo, pd, reveal, step4_ready, step4_widget):
    mo.stop(
        not step4_ready(),
        mo.md("_Write the sequence-question answer above. The worked solution unlocks when you commit._"),
    )

    _csdmards = {1503297}                # methotrexate (csDMARD)
    _tnfis = {1119119, 1151789, 1151287} # adalimumab, etanercept, infliximab

    _de = drug_exposure.copy()
    _de["drug_exposure_start_date"] = pd.to_datetime(_de["drug_exposure_start_date"])

    _first_csdmard = (
        _de[_de["drug_concept_id"].isin(_csdmards)]
        .sort_values(["person_id", "drug_exposure_start_date"])
        .groupby("person_id")
        .head(1)
        [["person_id", "drug_concept_id", "drug_exposure_start_date"]]
        .rename(columns={
            "drug_concept_id": "first_csdmard_concept_id",
            "drug_exposure_start_date": "first_csdmard_date",
        })
    )
    _first_tnfi = (
        _de[_de["drug_concept_id"].isin(_tnfis)]
        .sort_values(["person_id", "drug_exposure_start_date"])
        .groupby("person_id")
        .head(1)
        [["person_id", "drug_concept_id", "drug_exposure_start_date"]]
        .rename(columns={
            "drug_concept_id": "first_tnfi_concept_id",
            "drug_exposure_start_date": "first_tnfi_date",
        })
    )
    _sequence = _first_csdmard.merge(_first_tnfi, on="person_id", how="left")
    _sequence["days_csdmard_to_tnfi"] = (
        _sequence["first_tnfi_date"] - _sequence["first_csdmard_date"]
    ).dt.days
    _sequence.index = range(1, len(_sequence) + 1)
    _sequence.index.name = "row"

    _reveal_widget = reveal(
        step4_widget.value,
        (
            "The tabular form is approachable for two regimen lines: filter "
            "`drug_exposure` to csDMARDs, take the earliest per patient; "
            "filter to TNFis, take the earliest per patient; left-merge the "
            "two so patients who never received a TNFi appear with NULL TNFi "
            "columns; compute the gap in days. This works for the two-step "
            "csDMARD-to-TNFi pattern.\n\n"
            "**Worked pandas:**\n\n"
            "```python\n"
            "csdmards = {1503297}                  # methotrexate\n"
            "tnfis    = {1119119, 1151789, 1151287}  # adalimumab, etanercept, infliximab\n"
            "\n"
            "de = drug_exposure.copy()\n"
            "de['drug_exposure_start_date'] = pd.to_datetime(de['drug_exposure_start_date'])\n"
            "\n"
            "# Earliest csDMARD exposure per patient.\n"
            "first_csdmard = (\n"
            "    de[de['drug_concept_id'].isin(csdmards)]\n"
            "    .sort_values(['person_id', 'drug_exposure_start_date'])\n"
            "    .groupby('person_id').head(1)\n"
            "    [['person_id', 'drug_concept_id', 'drug_exposure_start_date']]\n"
            "    .rename(columns={\n"
            "        'drug_concept_id': 'first_csdmard_concept_id',\n"
            "        'drug_exposure_start_date': 'first_csdmard_date',\n"
            "    })\n"
            ")\n"
            "\n"
            "# Earliest TNFi exposure per patient (NULL if none).\n"
            "first_tnfi = (\n"
            "    de[de['drug_concept_id'].isin(tnfis)]\n"
            "    .sort_values(['person_id', 'drug_exposure_start_date'])\n"
            "    .groupby('person_id').head(1)\n"
            "    [['person_id', 'drug_concept_id', 'drug_exposure_start_date']]\n"
            "    .rename(columns={\n"
            "        'drug_concept_id': 'first_tnfi_concept_id',\n"
            "        'drug_exposure_start_date': 'first_tnfi_date',\n"
            "    })\n"
            ")\n"
            "\n"
            "sequence = first_csdmard.merge(first_tnfi, on='person_id', how='left')\n"
            "sequence['days_csdmard_to_tnfi'] = (\n"
            "    sequence['first_tnfi_date'] - sequence['first_csdmard_date']\n"
            ").dt.days\n"
            "```\n\n"
            "**Reading the chain.**\n\n"
            "- `csdmards` and `tnfis` are Python sets of the RxNorm-aligned drug concept_ids that count as each class.\n"
            "- `de['drug_concept_id'].isin(csdmards)` produces a boolean column that is True where the exposure row is a csDMARD; using that boolean to index `de` keeps only the csDMARD rows. Same pattern for TNFis.\n"
            "- `sort_values + groupby.head(1)` returns the earliest csDMARD exposure per patient, then the earliest TNFi exposure per patient.\n"
            "- `merge(..., how='left')` keeps every csDMARD patient even if they never received a TNFi. The TNFi columns appear as NaT (the datetime equivalent of NaN) for those patients, and the `days_csdmard_to_tnfi` for them is also NaT.\n"
            "- Subtracting two datetime columns yields a Timedelta column; `.dt.days` extracts the integer day count.\n\n"
            "**Where the graph data model fits.** The pandas above answers the two-step csDMARD-to-TNFi question. The query becomes awkward in SQL or pandas as the question scales. 'For each patient, list every regimen change in order, including switches between TNFis, brief steroid bursts, and additions of JAK inhibitors' is a path-length-unknown query across the patient's medication history. In Cypher the same question is a single MATCH with a variable-length path along `:NEXT_REGIMEN` edges. The graph nodes would be `(:RegimenEpoch {start, end, drugs})` per patient; the edges would be `:NEXT_REGIMEN` connecting each epoch to the next. The variable-length operator handles arbitrary-length sequences in one line.\n\n"
            "Result below."
        ),
    )
    mo.vstack([_reveal_widget, mo.callout(_sequence, kind="info")])
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Reflection on the assembled pipeline

        The capstone covered one analytic project across four layers in sequence. The same shape recurs in essentially every clinical informatics project against EHR data.

        - **Standards (Track 01)** identified the vocabularies the raw data was already using and the lookups required to standardize them. The LOINC codes were already in the labs export; the ICD-10-CM codes were already in the encounter file; the drug strings needed parsing and RxNorm lookup.
        - **OMOP (Track 02)** specified the target shape: which rows go in which table, which columns hold standardized concept_ids, which preserve source provenance. The mapping cell did the actual rewriting.
        - **SQL extraction (Track 03)** answered the cohort question against the OMOP-shaped tables in three lines of SQL.
        - **pandas analysis (Track 04)** answered the per-patient summary question against the same data, with the dtype-conversion-at-the-boundary discipline preventing date-comparison bugs.
        - **Graph (Track 05)** appeared at the moment the analytic question became path-shaped. The two-step csDMARD-to-TNFi computation fit pandas; the general regimen-history question did not.

        The pipeline you built is the same one that runs in production at every OMOP-conformant institution, with the source files replaced by warehouse extracts and the cohort sizes replaced by millions of rows.
        """
    )
    return


@app.cell
def _(mo):
    final_reflection = mo.ui.text_area(
        label=(
            "Write a paragraph naming the one decision in this pipeline you "
            "were least sure of, and what additional information would have "
            "made you more confident."
        ),
        rows=6,
        full_width=True,
        placeholder="No reveal on this one. The reflection is the work.",
    )
    final_reflection
    return (final_reflection,)


if __name__ == "__main__":
    app.run()
