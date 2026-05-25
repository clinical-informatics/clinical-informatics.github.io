"""Track 02: OMOP Common Data Model.

OMOP is a fixed schema for clinical data: the same six core tables at
every institution that adopts it, with values drawn from a shared
vocabulary indexed by concept_id. Track 01 covered the code standards
that name individual facts; this track presents the schema that
organizes those facts into a queryable warehouse and the vocabulary
layer that resolves codes to a single canonical identifier. The full
worked example is Ms. Reyes's record mapped to OMOP CDM v5.4.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import io
    import json
    import sys
    import types
    from pathlib import Path

    import marimo as mo
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

    # WASM-aware loader: reads a CSV from this track's cache/ directory
    # locally, or fetches from the site-absolute URL of the deployed cache
    # when running in marimo's Pyodide WASM runtime.
    _WASM_DATA_BASE = "/07-data-wrangling-engineering/track-02-omop/app"

    def load_cached_csv(name, **read_csv_kwargs):
        if "pyodide" in sys.modules:
            from pyodide.http import open_url
            url = _WASM_DATA_BASE + "/cache/" + name
            return pd.read_csv(io.StringIO(open_url(url).read()), **read_csv_kwargs)
        return pd.read_csv(Path(__file__).parent / "cache" / name, **read_csv_kwargs)

    return load_cached_csv, mo, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 02: OMOP Common Data Model

        ## The schema problem OMOP solves

        Track 01 specified the code standards that name individual clinical facts. A code standard guarantees that one lab test, one diagnosis, or one medication carries the same identifier across every institution that conforms to the standard. It does not guarantee anything about the table in which the fact is stored or the columns that describe it.

        Two institutions that adopt LOINC for labs may store lab results in completely different table structures. One uses a single wide table; the other uses a narrow event table joined to a separate value table. A SQL query written for one will not run against the other. A research consortium that wants to ask "what was the median CRP value at first RA visit across our ten member institutions" cannot do so without rewriting the query ten times.

        The OMOP Common Data Model is the schema-level standard layered on top of the code standards. It defines a fixed set of tables with fixed column names and types, with each clinical fact stored as a row whose code value is a concept_id drawn from a shared vocabulary. Every institution that adopts OMOP stores its data in the same tables under the same column names, with the same concept_ids for the same facts. A query written once at one institution runs unchanged at the other ten.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The six core clinical tables

        OMOP CDM v5.4 defines about forty tables in total. Six of them carry the bulk of the clinical content. The remainder are vocabulary tables, metadata tables, and tables for derived facts (drug eras, condition eras, cohorts). The six core tables are listed below.
        """
    )
    return


@app.cell
def _(pd):
    core_tables = pd.DataFrame(
        [
            {
                "Table": "person",
                "One row per": "Person",
                "Stores": "Demographics: gender, year of birth, race, ethnicity",
            },
            {
                "Table": "visit_occurrence",
                "One row per": "Encounter",
                "Stores": "The visit: type (outpatient / inpatient / emergency), start and end, location, provider",
            },
            {
                "Table": "condition_occurrence",
                "One row per": "Diagnosis recorded",
                "Stores": "The condition recorded during a visit, with concept_id, source code, and dates",
            },
            {
                "Table": "drug_exposure",
                "One row per": "Drug exposure period",
                "Stores": "Each known exposure: drug concept_id, start, end, route, days supply, refills",
            },
            {
                "Table": "measurement",
                "One row per": "Lab or vital sign result",
                "Stores": "Quantitative results: concept_id of the test, value, unit, reference range",
            },
            {
                "Table": "observation",
                "One row per": "Other recorded finding",
                "Stores": "Everything that does not fit the above: composite scores, allergies, social history, qualifiers",
            },
        ]
    )
    core_tables.index = range(1, len(core_tables) + 1)
    core_tables.index.name = "row"
    core_tables
    return (core_tables,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three properties of this design are load-bearing.

        First, the schema is fixed. Every OMOP-conformant institution stores its data in tables of these exact names with these exact columns. A query written against one OMOP database runs against any other.

        Second, every row in every clinical table carries one or more `concept_id` columns. The concept_id is an integer drawn from the OMOP vocabulary that uniquely identifies the clinical fact in the row. Two rows from two institutions that record the same fact carry the same concept_id, regardless of how the fact was encoded in either source EHR.

        Third, every clinical table also stores the source code that was mapped to produce the concept_id. The columns named `<thing>_source_value` and `<thing>_source_concept_id` preserve the original encoding. Source provenance is never discarded.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## person: demographics

        The `person` table holds one row per individual. Reyes's row is shown below.
        """
    )
    return


@app.cell
def _(load_cached_csv):
    person = load_cached_csv("person.csv")
    person.index = range(1, len(person) + 1)
    person.index.name = "row"
    person
    return (person,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three columns deserve attention.

        - `person_id` is the OMOP-internal identifier for Reyes. Every other table joins back to person on this column.
        - `gender_concept_id = 8532`. Concept 8532 is the OMOP vocabulary identifier for "Female". A different institution that records gender on Reyes will store the same integer in the same column. The original source string "Female" is preserved in `gender_source_value`.
        - `birth_datetime = 1974-02-09T00:00:00`. Date of birth is stored as both component columns (`year_of_birth`, `month_of_birth`, `day_of_birth`) and a full datetime. The component columns are required; the full datetime is optional, used when time-of-birth precision is needed.

        The `*_source_value` columns hold the original strings from the source EHR. Source provenance is preserved alongside the standardized concept_id.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## visit_occurrence: encounters

        Every clinical encounter is one row. Reyes's first five visits are shown below.
        """
    )
    return


@app.cell
def _(load_cached_csv):
    visit = load_cached_csv("visit_occurrence.csv")
    visit_display = visit[
        ["visit_occurrence_id", "person_id", "visit_concept_id",
         "visit_start_date", "visit_end_date", "visit_source_value"]
    ].head(5)
    visit_display.index = range(1, len(visit_display) + 1)
    visit_display.index.name = "row"
    visit_display
    return visit, visit_display


@app.cell
def _(mo):
    mo.md(
        r"""
        Each visit carries a `visit_concept_id` that names the visit type. The integer `9202` is the OMOP concept for "Outpatient visit", which is what Reyes's visits to her rheumatologist are. The full set of visit_concept_id values is small and well-defined: outpatient, inpatient, emergency, telehealth, observation, long-term care, and a few others.

        The two dates (`visit_start_date` and `visit_end_date`) record the encounter span. For an outpatient visit they are usually the same day. For an inpatient stay they bracket the admission and discharge. The free-text `visit_source_value` preserves the wording used in the source system ("New patient consult", "Office visit"), which is informative for audit but not used in standardized queries.

        The clinical tables that follow (condition_occurrence, drug_exposure, measurement, observation) all join back to visit_occurrence on `visit_occurrence_id` when the fact was recorded during a specific encounter.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## condition_occurrence: diagnoses

        Each diagnosis recorded in the chart is one row. The dual concept_id structure is most visible here.
        """
    )
    return


@app.cell
def _(load_cached_csv):
    condition = load_cached_csv("condition_occurrence.csv")
    condition_display = condition[
        ["condition_occurrence_id", "condition_concept_id",
         "condition_start_date", "condition_source_value",
         "condition_source_concept_id", "visit_occurrence_id"]
    ]
    condition_display.index = range(1, len(condition_display) + 1)
    condition_display.index.name = "row"
    condition_display
    return condition, condition_display


@app.cell
def _(mo):
    mo.md(
        r"""
        Rows 1, 4, 5, and 6 are four separate occurrences of Reyes's rheumatoid arthritis diagnosis, recorded at different visits. All four carry the same `condition_concept_id = 4138406`. This is the OMOP standard concept for "Rheumatoid arthritis - multiple sites and rheumatoid factor present", which is the OMOP vocabulary's canonical concept for the underlying clinical entity.

        All four rows also carry the same `condition_source_value = M05.79` and `condition_source_concept_id = 45567145`. The source value is the ICD-10-CM code that the EHR recorded; the source concept_id is the OMOP vocabulary's representation of that ICD-10-CM code itself, distinct from the standardized SNOMED-aligned concept that downstream queries should use.

        The dual representation is the central OMOP design choice. The source columns preserve the EHR encoding for audit and for queries that need to know the original code. The standardized column (`condition_concept_id`) is the column that downstream cohort queries filter on, because that column is comparable across institutions regardless of which source vocabulary each institution used.

        Row 2 is a separate finding (anemia, ICD-10-CM D63.8, OMOP standard concept 4108412). Row 3 is a longstanding finding (penicillin allergy history, ICD-10-CM Z88.0) that predates the visit data and is stored without a visit_occurrence_id.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## drug_exposure: medications

        Each known drug exposure is one row, with start and end dates, route, and the standardized RxNorm-aligned drug concept_id.
        """
    )
    return


@app.cell
def _(load_cached_csv):
    drug = load_cached_csv("drug_exposure.csv")
    drug_display = drug[
        ["drug_exposure_id", "drug_concept_id",
         "drug_exposure_start_date", "drug_exposure_end_date",
         "days_supply", "drug_source_value", "route_source_value"]
    ]
    drug_display.index = range(1, len(drug_display) + 1)
    drug_display.index.name = "row"
    drug_display
    return drug, drug_display


@app.cell
def _(mo):
    mo.md(
        r"""
        Reyes is on three chronic medications. Row 1 is the methotrexate she started at her first office visit. Row 2 is the adalimumab added in January 2024 when methotrexate alone proved insufficient. Row 3 is the folic acid supplementation paired with methotrexate. Row 4 is the one short prednisone taper she received during a 2025 flare; it is the only row with a non-empty `drug_exposure_end_date`, because the rest are ongoing chronic medications.

        Three columns are worth noting.

        - `drug_concept_id` is the standardized RxNorm-aligned identifier. Concept 1503297 is methotrexate at the ingredient level. The same integer would be used for every methotrexate prescription written at any OMOP-conformant institution.
        - `days_supply` is the prescribed duration of the supplied quantity. Chronic medications often have `days_supply` of 28 or 30 per prescription, with refills_remaining recorded separately.
        - `drug_source_value` preserves the original free-text order string. The free text is informative for audit and for understanding intent (the prednisone row shows the taper schedule embedded in the order text), but downstream analyses filter on `drug_concept_id`.

        The route columns work the same way as the drug columns: `route_concept_id` is the OMOP standardized identifier; `route_source_value` is the original free text.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## measurement: lab results and vital signs

        Each lab result and each numeric vital sign is one row. Reyes's measurements are shown below; the table has more columns in production OMOP than are useful here, so the display selects the central ones.
        """
    )
    return


@app.cell
def _(load_cached_csv):
    measurement = load_cached_csv("measurement.csv")
    measurement_display = measurement[
        ["measurement_id", "measurement_concept_id", "measurement_date",
         "value_as_number", "unit_source_value", "range_low", "range_high",
         "measurement_source_value"]
    ]
    measurement_display.index = range(1, len(measurement_display) + 1)
    measurement_display.index.name = "row"
    measurement_display
    return measurement, measurement_display


@app.cell
def _(mo):
    mo.md(
        r"""
        Each row carries a `measurement_concept_id` that names the test. The integers map to LOINC: concept 3010156 is "C-reactive protein", concept 3015632 is "Erythrocyte sedimentation rate", concept 3007220 is the anti-CCP antibody, concept 3009596 is hemoglobin. The `measurement_source_value` column preserves the LOINC code as a string (`1988-5`, `4537-7`, etc.), which is the encoding the source EHR used. The standardized concept_id is the column downstream queries filter on.

        Three other columns deserve attention.

        - `value_as_number` holds the numeric result. For non-numeric results (positive, negative, present, absent), a separate column `value_as_concept_id` would hold an OMOP concept for the categorical value, and `value_as_number` would be empty.
        - `unit_source_value` holds the unit string from the source system. A separate column `unit_concept_id` (not displayed) holds the standardized unit concept. Production OMOP queries filter on `unit_concept_id` to compare values across institutions, because the source string varies ("mg/L", "mg/l", "milligrams per liter").
        - `range_low` and `range_high` record the reference range that applied at the time the result was reported. Reference ranges drift over time as labs change methods, so they are stored on the row rather than looked up at query time.

        Production OMOP measurement tables also carry `operator_concept_id` for results expressed as inequalities (greater than 100, less than 0.05). Reyes's data does not exercise that column.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## observation: everything else

        The `observation` table holds clinical facts that do not fit cleanly into the four tables above. Composite scores, allergies, social-history items, and structured assessments live here.
        """
    )
    return


@app.cell
def _(load_cached_csv):
    observation = load_cached_csv("observation.csv")
    observation_display = observation[
        ["observation_id", "observation_concept_id", "observation_date",
         "value_as_number", "value_as_string", "observation_source_value"]
    ]
    observation_display.index = range(1, len(observation_display) + 1)
    observation_display.index.name = "row"
    observation_display
    return observation, observation_display


@app.cell
def _(mo):
    mo.md(
        r"""
        Rows 1 through 4 are the four DAS28-CRP values Reyes has had recorded, each carrying `observation_concept_id = 40766949` (the OMOP concept for "DAS28-CRP"). The numeric score is stored in `value_as_number`. The trajectory across the four rows (4.1, 2.9, 2.6, 2.8) is the disease-activity history clinicians would read off the chart.

        Row 5 is a free-text observation of penicillin allergy, stored in `value_as_string` because the recorded value is qualitative.

        Row 6 is a social-history element (occupation: Accountant), also stored as string. The reason these are not in `condition_occurrence` is that they are not diagnoses; the reason they are not in `measurement` is that they are not numeric lab results. The `observation` table is the holding location for any clinical fact whose shape does not match the more specific tables.

        The placement of DAS28 in `observation` rather than `measurement` is a convention call by the source EHR's OMOP ETL team. Some ETLs place composite clinical scores in `measurement`. The OMOP convention is permissive on this point; the relevant downstream query simply filters on `concept_id = 40766949` regardless of which table the row lives in. In practice, queries that need clinical scores often `UNION` measurement and observation to handle both conventions.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The vocabulary layer

        The `concept_id` columns above all draw from a single global vocabulary table maintained by OHDSI. The vocabulary table contains roughly 9 million concepts spanning every code system OMOP supports (LOINC, SNOMED, RxNorm, ICD-10-CM, ICD-9-CM, CPT, HCPCS, NDC, and dozens more). A sample of the concepts referenced in Reyes's record is shown below.
        """
    )
    return


@app.cell
def _(pd):
    reyes_concept_lookup = pd.DataFrame(
        [
            {"concept_id": 8532, "vocabulary_id": "Gender", "concept_name": "FEMALE", "standard_concept": "S"},
            {"concept_id": 8527, "vocabulary_id": "Race", "concept_name": "White", "standard_concept": "S"},
            {"concept_id": 9202, "vocabulary_id": "Visit", "concept_name": "Outpatient Visit", "standard_concept": "S"},
            {"concept_id": 4138406, "vocabulary_id": "SNOMED", "concept_name": "Rheumatoid arthritis - multiple sites", "standard_concept": "S"},
            {"concept_id": 45567145, "vocabulary_id": "ICD10CM", "concept_name": "Rheumatoid arthritis with rheumatoid factor of multiple sites without organ or systems involvement", "standard_concept": ""},
            {"concept_id": 4108412, "vocabulary_id": "SNOMED", "concept_name": "Anemia", "standard_concept": "S"},
            {"concept_id": 3010156, "vocabulary_id": "LOINC", "concept_name": "C-reactive protein [Mass/volume] in Serum or Plasma", "standard_concept": "S"},
            {"concept_id": 3015632, "vocabulary_id": "LOINC", "concept_name": "Erythrocyte sedimentation rate by Westergren method", "standard_concept": "S"},
            {"concept_id": 1503297, "vocabulary_id": "RxNorm", "concept_name": "methotrexate", "standard_concept": "S"},
            {"concept_id": 1119119, "vocabulary_id": "RxNorm", "concept_name": "adalimumab", "standard_concept": "S"},
            {"concept_id": 40766949, "vocabulary_id": "LOINC", "concept_name": "DAS28-CRP", "standard_concept": "S"},
        ]
    )
    reyes_concept_lookup.index = range(1, len(reyes_concept_lookup) + 1)
    reyes_concept_lookup.index.name = "row"
    reyes_concept_lookup
    return (reyes_concept_lookup,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three columns are decisive.

        - `concept_id` is the unique integer identifier. Every clinical row in every clinical table carries a concept_id drawn from this vocabulary.
        - `vocabulary_id` records the source vocabulary that contributed the concept. LOINC-derived concepts are in the LOINC vocabulary; SNOMED-derived concepts are in the SNOMED vocabulary; ICD-10-CM-derived concepts are in the ICD10CM vocabulary.
        - `standard_concept` is the flag that controls whether a concept is the canonical representation of its clinical entity. The value `"S"` marks the concept as standard. The empty value marks the concept as non-standard (sometimes also flagged `"C"` for classification concepts). For conditions, drugs, and observations, the OHDSI convention is that the SNOMED concept is standard and the ICD-10-CM concept is non-standard; for labs, the LOINC concept is standard.

        The standard-concept distinction explains the dual encoding in Reyes's `condition_occurrence` rows. The ICD-10-CM concept 45567145 sits in `condition_source_concept_id`, preserving the source encoding. The SNOMED-aligned concept 4138406 sits in `condition_concept_id`, providing the standard representation that comparable queries across institutions filter on. The OMOP vocabulary maintains the mapping between the two through a separate `concept_relationship` table.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Worked example: trace one raw EHR row to its OMOP row

        The two-row trace below shows the same clinical fact (Reyes's CRP value from the new-patient consult) as it appears in the source EHR row and as it appears in the corresponding OMOP measurement row.
        """
    )
    return


@app.cell
def _(pd):
    crp_trace = pd.DataFrame(
        [
            {
                "Layer": "Source EHR lab row",
                "Test identifier": "1988-5 (LOINC code as a string)",
                "Test name": "C-Reactive Protein",
                "Value": 42.1,
                "Unit": "mg/L",
                "Date": "2022-02-14",
                "Patient ID": "ER-001 (EHR medical record number)",
            },
            {
                "Layer": "OMOP measurement row",
                "Test identifier": "3010156 (measurement_concept_id)",
                "Test name": "(stored separately in concept table; not on the row)",
                "Value": 42.1,
                "Unit": "8840 (unit_concept_id; source 'mg/L' in unit_source_value)",
                "Date": "2022-02-14 (measurement_date)",
                "Patient ID": "1001 (person_id)",
            },
        ]
    )
    crp_trace.index = range(1, len(crp_trace) + 1)
    crp_trace.index.name = "row"
    crp_trace
    return (crp_trace,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Four changes happened in the ETL from source row to OMOP row.

        1. **Patient identifier.** The EHR medical record number `ER-001` was replaced with the OMOP `person_id = 1001`. The mapping between EHR MRN and OMOP person_id is held in a separate location table or in the ETL's lookup mappings.
        2. **Test identifier.** The LOINC code `1988-5` was looked up in the OMOP vocabulary and stored as its concept_id `3010156`. The original LOINC string is preserved in `measurement_source_value`.
        3. **Unit.** The unit string `mg/L` was looked up in the OMOP unit vocabulary and stored as `unit_concept_id = 8840`. The original string is preserved in `unit_source_value`.
        4. **Test name.** The free-text test name is not stored on the row at all. The name is retrieved by joining `measurement_concept_id` to the OMOP `concept` table when needed for display.

        Everything else on the row (the numeric value, the date) is copied through. The ETL preserves source provenance in the `*_source_*` columns while attaching standardized identifiers in the corresponding `*_concept_id` columns.
        """
    )
    return


@app.cell
def _(mo):
    q1 = mo.ui.radio(
        options=[
            "It exists for two-way audit between the OMOP row and the source EHR row.",
            "It exists so that queries can filter on the source vocabulary when needed.",
            "Both of the above.",
            "It is a vestigial column with no current use.",
        ],
        label=(
            "Why does OMOP store both `condition_concept_id` and "
            "`condition_source_concept_id` on every row in the "
            "condition_occurrence table?"
        ),
    )
    q1
    return (q1,)


@app.cell
def _(mo, q1):
    if q1.value is None:
        out1 = mo.md("_Pick one._")
    else:
        correct1 = q1.value.startswith("Both")
        out1 = mo.callout(
            mo.md(
                rf"""
                **{'Correct.' if correct1 else 'Not quite.'}**

                The dual representation serves both purposes. Source provenance is preserved for audit and for any downstream verification against the original EHR record. The source concept_id is also queryable: a study that specifically requires ICD-10-CM-coded rows (for billing analysis, for example) can filter on `condition_source_concept_id` while ignoring the standardized column. The standardized `condition_concept_id` is the column used for cross-institution queries because it normalizes across the source vocabularies any single institution may have used.
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
            "measurement",
            "observation",
            "Either, depending on the source EHR's ETL convention.",
            "condition_occurrence, because DAS28 indicates active rheumatoid arthritis.",
        ],
        label=(
            "Reyes's DAS28-CRP scores are stored under concept_id 40766949. "
            "Which OMOP table contains them in production warehouses?"
        ),
    )
    q2
    return (q2,)


@app.cell
def _(mo, q2):
    if q2.value is None:
        out2 = mo.md("_Pick one._")
    else:
        correct2 = q2.value.startswith("Either")
        out2 = mo.callout(
            mo.md(
                rf"""
                **{'Correct.' if correct2 else 'Not quite.'}**

                The OMOP convention is permissive on the placement of composite clinical scores. Some institutions' ETLs place DAS28 in `measurement` because it is a quantitative score; others (including the convention used in Reyes's record) place it in `observation` because it is a calculated composite rather than a directly measured value. Queries that aim to be portable across OMOP installations typically `UNION` the measurement and observation tables filtered by concept_id, which returns the row from whichever table the local ETL chose. The `condition_occurrence` option is wrong because a clinical score is not a diagnosis; the table holds the condition entity (rheumatoid arthritis), not the activity score for that condition.
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

        Pick one of the two prompts below and write 4 to 6 sentences in the box that follows. Save what you write outside the browser; the box is a scratch pad, not persistent storage. When you are done, continue to `track-03-sql`.

        1. **An institutional cohort study you are familiar with** defined its cohort using EHR data. Specify how the cohort definition would change if the data were stored in OMOP rather than the source EHR. Identify what would become easier, what would become more constrained, and which decisions the OMOP standardization layer would force the team to make explicit.

        2. **A vendor presents a data platform** that ingests EHR data, applies "standardization", and exposes it for analysis. State the questions you would ask to determine whether the standardization layer is OMOP-conformant, an in-house equivalent, or simply a relabeling of the source EHR's schema.
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
        "The extraction layer is SQL.",
        (
            "The warehouse is now defined: six standardized clinical tables, "
            "each row carrying concept_ids drawn from a global vocabulary. "
            "Track 03 introduces SQL as the extraction language. Each query "
            "demonstrated in Track 03 begins with a clinical question, then "
            "constructs the SQL that returns the corresponding cohort or "
            "summary from the OMOP-shaped warehouse defined here. Continue "
            "to `track-03-sql`."
        ),
    )
    return


if __name__ == "__main__":
    app.run()
