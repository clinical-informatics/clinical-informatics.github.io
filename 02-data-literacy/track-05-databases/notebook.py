"""Track 05: What a database actually is.

A spreadsheet trusts you. A database doesn't. This notebook builds a
real in-memory clinical schema (three tables, six constraint types),
inserts valid data, then walks seven bad-insert scenarios. Some get
caught by the schema. A few sneak through. The diagnostic is *which
constraint did which job*, and which class of error remains the
application's responsibility because no constraint can catch it.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import sys
    from pathlib import Path

    _track_dir = Path(__file__).parent
    _course_dir = _track_dir.parent
    if str(_course_dir) not in sys.path:
        sys.path.insert(0, str(_course_dir))

    import sqlite3

    import marimo as mo
    import pandas as pd

    return mo, pd, sqlite3


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 05: What a database actually is

        ## A spreadsheet trusts you. A database doesn't.

        A spreadsheet is a tool that lets you type values into cells and do arithmetic. Anything goes. Type `forty-two` into a cell labeled "CRP" and the spreadsheet stores it, no complaints.

        A database is a system that *defines* what may go in each cell, refuses to store anything that violates the definition, and gives you efficient, concurrent ways to ask questions across what's stored. That refusal is the feature. Tracks 01 through 04 of this course were about cleaning data that should never have been allowed to ship in the first place. This track is about why a well-designed database wouldn't have let it ship.

        Five pieces:

        1. **The spreadsheet you inherited.** All the type, tidy, missingness, and join problems we have seen, in one flat file.
        2. **What a schema is.** The published contract: column names, types, allowed values, relationships.
        3. **The six constraint types.** Each one catches a different class of error at insert time.
        4. **The bad-insert demo.** A real in-memory SQLite database. Seven malformed rows. Watch which constraints catch which bugs, and which bugs slip through.
        5. **Forward to FHIR and OMOP.** Clinical informatics adds two layers on top of the relational model. Course 06 walks FHIR; course 07 walks OMOP.
        """
    )
    return


@app.cell
def _(mo, pd):
    spreadsheet = pd.DataFrame(
        {
            "patient_id": ["ER-001", "ER-001", "ER-002", "ER-003", None, "ER-002", "ER-004"],
            "patient_name": ["Reyes, Elena", "Reyes, E.", "Chen, May", "Williams, Tom", "Patel, Anika", "Chen, May", "Russo"],
            "date_of_birth": ["1974-02-09", "02/09/74", "1979-06-14", "1953-08-22", "1988-03-30", "1979-06-14", "2099-01-01"],
            "sex": ["F", "Female", "F", "M", "F", "F", "f"],
            "encounter_date": ["2024-04-17", "2024-04-17", "2024-05-30", "2024-06-04", "2024-06-25", "2024-09-04", "2024-08-12"],
            "loinc": ["1988-5", "1988-5", "1988-5", "1988-5", "1988-5", "1988-5", "1988-5"],
            "crp": [18.7, 18.7, 11.2, "<2.0", 9.4, 8.6, "twenty"],
        }
    )
    spreadsheet.index = range(1, len(spreadsheet) + 1)
    spreadsheet.index.name = "row"
    mo.vstack(
        [
            mo.md(
                "## 1. The spreadsheet you inherited\n\n"
                "Take the kind of flat extract Tracks 01 through 04 have been wrangling: one row per CRP, with patient demographics inlined. The spreadsheet allows everything. Count the problems before reading the callout below."
            ),
            mo.ui.table(spreadsheet, selection=None),
            mo.callout(
                mo.md(
                    "**Eight problems, all coexisting:**\n\n"
                    "1. Row 2 is a duplicate of row 1 (same patient, same lab, slightly different rendering).\n"
                    "2. Row 2's `date_of_birth` is in a different format from the rest (`02/09/74` vs `1974-02-09`).\n"
                    "3. Row 2's `patient_name` has been re-rendered (`Reyes, E.` vs `Reyes, Elena`).\n"
                    "4. Row 4's `crp` is the text `<2.0`, a sentinel from the assay.\n"
                    "5. Row 5 is missing `patient_id` (orphan observation).\n"
                    "6. Row 5's patient (Patel) appears nowhere else; we have no patient record for her.\n"
                    "7. Rows 1, 2 use `F`; row 2 also uses `Female`; row 7 uses `f` (categorical inconsistency).\n"
                    "8. Row 7's `date_of_birth` is 2099-01-01 (in the future); `crp` is the text `\"twenty\"`.\n\n"
                    "A database with the right constraints catches problems 4, 5, 7, and 8 at insert time, plus the duplicate at row 2 (if a uniqueness constraint is in place). The structural problems (different format, future birthday) need either a `CHECK` constraint or an application layer above the schema. The patient-without-a-record problem (row 5) is exactly the foreign-key problem."
                ),
                kind="warn",
            ),
        ]
    )
    return (spreadsheet,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2. What a schema is

        A **schema** is the published contract of a database: which tables exist, which columns each has, what type and constraints each column carries, and how the tables relate. It's written in **DDL** (Data Definition Language) using `CREATE TABLE` statements.

        Below is a minimal clinical schema with three tables. Read the code; the comments call out which constraint catches which class of bug.

        ```sql
        CREATE TABLE patient (
            patient_id    TEXT PRIMARY KEY,                         -- unique, not null
            patient_name  TEXT NOT NULL,                            -- required
            date_of_birth DATE NOT NULL,                            -- typed, required
            sex           TEXT NOT NULL
                CHECK (sex IN ('male','female','other','unknown'))  -- enforced value set
        );

        CREATE TABLE encounter (
            encounter_id   TEXT PRIMARY KEY,
            patient_id     TEXT NOT NULL
                REFERENCES patient(patient_id),                     -- foreign key: every
                                                                    -- encounter has a patient
            encounter_date DATE NOT NULL
        );

        CREATE TABLE observation (
            observation_id TEXT PRIMARY KEY,
            encounter_id   TEXT NOT NULL
                REFERENCES encounter(encounter_id),                 -- foreign key: every
                                                                    -- observation has an encounter
            loinc          TEXT NOT NULL,                           -- required code
            value_num      REAL,                                    -- typed numeric
            observed_at    TIMESTAMP NOT NULL,
            UNIQUE (encounter_id, loinc, observed_at)               -- no duplicate measurements
        );
        ```

        The schema is doing five jobs:

        - **Naming** tables and columns.
        - **Declaring types** (Track 01's question, answered definitively).
        - **Specifying required fields** with `NOT NULL`.
        - **Restricting allowed values** with `CHECK`.
        - **Declaring relationships** with `REFERENCES` (foreign keys).

        Any data violating the contract never lands in the database.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3. The six constraint types

        | # | Constraint | What it does | Class of bug it catches |
        |---|---|---|---|
        | 1 | **Type** (`TEXT`, `DATE`, `REAL`, `INTEGER`) | Rejects values that can't be parsed as the declared type | Track 01 type errors (`"twenty"` in a `REAL` column) |
        | 2 | **NOT NULL** | Requires the column to have a value | Track 03 structural blanks where a value is required |
        | 3 | **UNIQUE** | Values (or combinations) must be distinct | Duplicate rows, near-duplicates from flaky loaders |
        | 4 | **PRIMARY KEY** | The unique row identifier; combines NOT NULL + UNIQUE | "Two patients with the same MRN" |
        | 5 | **FOREIGN KEY** (`REFERENCES`) | Value must exist as a primary key in another table | Orphan rows (encounters without patients) |
        | 6 | **CHECK** | Arbitrary boolean condition that must hold | Value-set violations, range violations, cross-column rules |

        Below, we build this exact schema in an in-memory SQLite database and try to insert bad data.
        """
    )
    return


@app.cell
def _(sqlite3):
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE patient (
            patient_id    TEXT PRIMARY KEY,
            patient_name  TEXT NOT NULL,
            date_of_birth DATE NOT NULL,
            sex           TEXT NOT NULL CHECK (sex IN ('male','female','other','unknown'))
        );

        CREATE TABLE encounter (
            encounter_id   TEXT PRIMARY KEY,
            patient_id     TEXT NOT NULL REFERENCES patient(patient_id),
            encounter_date DATE NOT NULL
        );

        CREATE TABLE observation (
            observation_id TEXT PRIMARY KEY,
            encounter_id   TEXT NOT NULL REFERENCES encounter(encounter_id),
            loinc          TEXT NOT NULL,
            value_num      REAL,
            observed_at    TIMESTAMP NOT NULL,
            UNIQUE (encounter_id, loinc, observed_at)
        );
        """
    )

    cur.executemany(
        "INSERT INTO patient VALUES (?, ?, ?, ?)",
        [
            ("ER-001", "Reyes, Elena", "1974-02-09", "female"),
            ("ER-002", "Chen, May", "1979-06-14", "female"),
            ("ER-003", "Williams, Tom", "1953-08-22", "male"),
        ],
    )
    cur.executemany(
        "INSERT INTO encounter VALUES (?, ?, ?)",
        [
            ("ENC-A", "ER-001", "2024-04-17"),
            ("ENC-B", "ER-002", "2024-05-30"),
            ("ENC-C", "ER-003", "2024-06-04"),
        ],
    )
    cur.executemany(
        "INSERT INTO observation VALUES (?, ?, ?, ?, ?)",
        [
            ("OBS-1", "ENC-A", "1988-5", 18.7, "2024-04-17 09:14:00"),
            ("OBS-2", "ENC-B", "1988-5", 11.2, "2024-05-30 10:02:00"),
            ("OBS-3", "ENC-C", "1988-5", 6.4, "2024-06-04 08:30:00"),
        ],
    )
    conn.commit()
    return conn, cur


@app.cell
def _(conn, mo, pd):
    patient_df = pd.read_sql("SELECT * FROM patient", conn)
    encounter_df = pd.read_sql("SELECT * FROM encounter", conn)
    obs_df = pd.read_sql("SELECT * FROM observation", conn)
    patient_df.index = range(1, len(patient_df) + 1)
    patient_df.index.name = "row"
    encounter_df.index = range(1, len(encounter_df) + 1)
    encounter_df.index.name = "row"
    obs_df.index = range(1, len(obs_df) + 1)
    obs_df.index.name = "row"
    mo.vstack(
        [
            mo.md(
                "## 4. The database, populated with valid data\n\n"
                "Three patients, three encounters, three observations. All rows satisfy every constraint."
            ),
            mo.hstack(
                [
                    mo.vstack([mo.md("**patient**"), mo.ui.table(patient_df, selection=None)]),
                    mo.vstack([mo.md("**encounter**"), mo.ui.table(encounter_df, selection=None)]),
                ],
                widths=[1, 1],
            ),
            mo.md("**observation**"),
            mo.ui.table(obs_df, selection=None),
        ]
    )
    return encounter_df, obs_df, patient_df


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 5. The bad-insert demo

        Seven malformed rows. Pick one and watch what the database does. Some are caught at insert time. A few slip through. The diagnostic is which constraint did which job, and which class of error the schema cannot catch.
        """
    )
    return


@app.cell
def _(mo):
    bad_insert = mo.ui.radio(
        options=[
            "1. Insert CRP with value 'twenty' (text in a REAL column)",
            "2. Insert a patient with NULL date_of_birth",
            "3. Insert a second patient with patient_id ER-001 (duplicate primary key)",
            "4. Insert a patient with sex = 'F' (not in the CHECK value set)",
            "5. Insert an encounter for patient ER-999 (no such patient exists)",
            "6. Insert a duplicate CRP at the same encounter and timestamp",
            "7. Insert a patient with date_of_birth = '2099-01-01' (in the future)",
        ],
        value="1. Insert CRP with value 'twenty' (text in a REAL column)",
        label="Pick a bad-insert scenario",
    )
    bad_insert
    return (bad_insert,)


@app.cell
def _(bad_insert, conn, mo, pd):
    scenarios = {
        "1.": {
            "sql": "INSERT INTO observation VALUES ('OBS-X1', 'ENC-A', '1988-5', 'twenty', '2024-04-17 09:15:00')",
            "constraint": "Column type (`value_num REAL`)",
            "tier": "schema-type",
            "expected_outcome": (
                "**Not caught by SQLite.** SQLite is famously permissive about types: it has type *affinity* "
                "rather than strict types, so it will accept the text 'twenty' into a `REAL` column and just "
                "store it as a string. PostgreSQL, MySQL with strict mode, BigQuery, and most production databases "
                "**would reject this** with a type error. The lesson: types are a constraint *if the engine enforces them*. "
                "Check your database's type strictness; it varies."
            ),
        },
        "2.": {
            "sql": "INSERT INTO patient VALUES ('ER-998', 'Test, Patient', NULL, 'female')",
            "constraint": "`date_of_birth DATE NOT NULL`",
            "tier": "schema-not-null",
            "expected_outcome": (
                "**Caught.** The NOT NULL constraint on `date_of_birth` refuses any patient row without a DOB. "
                "Track 03 structural-blank problem, prevented at the schema layer instead of cleaned up later."
            ),
        },
        "3.": {
            "sql": "INSERT INTO patient VALUES ('ER-001', 'Duplicate, Person', '1990-01-01', 'female')",
            "constraint": "`patient_id PRIMARY KEY`",
            "tier": "schema-primary-key",
            "expected_outcome": (
                "**Caught.** The PRIMARY KEY constraint on `patient_id` forbids two rows with the same id. "
                "Without this, the duplicate-patient problem of row 2 in the spreadsheet above becomes a permanent "
                "data quality bug that every downstream join has to work around."
            ),
        },
        "4.": {
            "sql": "INSERT INTO patient VALUES ('ER-999', 'Test, Patient', '1990-01-01', 'F')",
            "constraint": "`CHECK (sex IN ('male','female','other','unknown'))`",
            "tier": "schema-check",
            "expected_outcome": (
                "**Caught.** The CHECK constraint enforces the FHIR-aligned value set. `'F'` is not in the allowed list. "
                "This is how a schema bakes in clinical value sets: the database refuses to accept anything outside them. "
                "The cleaning that Track 01 did at analysis time is done once, at insert time, by the schema."
            ),
        },
        "5.": {
            "sql": "INSERT INTO encounter VALUES ('ENC-X', 'ER-999', '2024-08-12')",
            "constraint": "`patient_id REFERENCES patient(patient_id)`",
            "tier": "schema-foreign-key",
            "expected_outcome": (
                "**Caught.** The foreign-key constraint refuses to create an encounter for a patient that doesn't exist. "
                "The orphan-row problem (Track 04's silent patient loss, viewed from the other side) is structurally impossible "
                "inside a foreign-key-constrained schema. The corresponding fact for the spreadsheet above: row 5's Patel had "
                "a CRP but no patient record, and no relational constraint allowed that to happen in the first place."
            ),
        },
        "6.": {
            "sql": "INSERT INTO observation VALUES ('OBS-X6', 'ENC-A', '1988-5', 19.0, '2024-04-17 09:14:00')",
            "constraint": "`UNIQUE (encounter_id, loinc, observed_at)`",
            "tier": "schema-unique",
            "expected_outcome": (
                "**Caught.** The composite UNIQUE constraint refuses a second observation with the same encounter, code, "
                "and timestamp as an existing one. A flaky loader that POSTs the same record twice cannot accidentally double the data."
            ),
        },
        "7.": {
            "sql": "INSERT INTO patient VALUES ('ER-997', 'FutureKid', '2099-01-01', 'female')",
            "constraint": "(no constraint exists for this)",
            "tier": "uncaught",
            "expected_outcome": (
                "**Not caught.** The schema as written has no constraint that forbids future birthdays. The row inserts. "
                "**This is the lesson.** Constraints catch what they are written to catch. The database designer didn't anticipate "
                "future birthdays, so the schema can't reject them. The fix is to add `CHECK (date_of_birth <= CURRENT_DATE)`. "
                "More generally: any class of bug you want caught at the schema layer has to be specified as a constraint. "
                "Bugs the schema doesn't know about are the **application's** responsibility to catch."
            ),
        },
    }

    key = bad_insert.value[:2]
    scenario = scenarios[key]

    # Try the insert
    rolled_back = False
    error_message = None
    rows_after = None
    try:
        conn.execute("SAVEPOINT bad_insert")
        conn.execute(scenario["sql"])
        # Special case: did the type-affinity issue actually insert?
        if scenario["tier"] == "schema-type":
            rows_after = pd.read_sql(
                "SELECT * FROM observation WHERE observation_id = 'OBS-X1'", conn
            )
        elif scenario["tier"] == "uncaught":
            rows_after = pd.read_sql(
                "SELECT * FROM patient WHERE patient_id = 'ER-997'", conn
            )
        # Roll back so subsequent runs see a clean database
        conn.execute("ROLLBACK TO SAVEPOINT bad_insert")
        conn.execute("RELEASE SAVEPOINT bad_insert")
        rolled_back = True
    except Exception as exc:
        error_message = str(exc)
        try:
            conn.execute("ROLLBACK TO SAVEPOINT bad_insert")
            conn.execute("RELEASE SAVEPOINT bad_insert")
        except Exception:
            pass

    sql_md = mo.md(f"**SQL attempted:**\n\n```sql\n{scenario['sql']}\n```")
    constraint_md = mo.md(f"**Constraint that should catch this:** {scenario['constraint']}")

    if error_message is None and rows_after is not None and len(rows_after) > 0:
        rows_display = rows_after.copy()
        rows_display.index = range(1, len(rows_display) + 1)
        rows_display.index.name = "row"
        outcome_md = mo.vstack(
            [
                mo.md("**Result: the row inserted.** Database state during the attempt (rolled back after to keep things clean):"),
                mo.ui.table(rows_display, selection=None),
            ]
        )
        callout_kind = "warn"
    elif error_message is None:
        outcome_md = mo.md("**Result: silent success.**")
        callout_kind = "warn"
    else:
        outcome_md = mo.md(f"**Database error (this is the database refusing the insert):**\n\n```\n{error_message}\n```")
        callout_kind = "success"

    interpretation = mo.callout(mo.md(scenario["expected_outcome"]), kind=callout_kind)

    mo.vstack([sql_md, constraint_md, outcome_md, interpretation])
    return (scenarios,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 6. What constraints don't catch

        Walk all seven scenarios. Six of them get caught, one of them (the type case in SQLite) slips through due to engine permissiveness, and the future-birthday case slips through because no constraint forbids it.

        That's the punchline. A schema is the *contract*, but the contract is only what the designer thought to write. Three classes of bug live above the schema layer:

        | Class | Example | Where it gets handled |
        |---|---|---|
        | **Constraints the designer didn't think of** | Future birthdays, discharge-before-admit, dose magnitudes off by 1000 | The application layer, or new `CHECK` constraints added later |
        | **Cross-system semantic mismatches** | One site's `loinc=30522-7` means hsCRP; another site uses `1988-5` to mean the same thing | A terminology layer (LOINC mappings, value-set services) |
        | **Real-world clinical bugs the data captured correctly** | The lab really was drawn after the patient died, because the time-of-death wasn't updated in the EHR | Process and governance, not the database |

        Every well-designed clinical database is the *intersection* of: schema constraints + application validation + terminology services + governance. The schema alone is the foundation; it isn't the whole building.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 7. Forward to FHIR and OMOP

        Clinical informatics adds two layers on top of the relational model this track has built. Both rest on the same ideas. Both add domain semantics the bare relational model doesn't carry.

        ### FHIR (course 06): an *interoperability* schema

        FHIR specifies clinical resources designed to *travel*. A `Patient` resource is not just any table with a primary key; it's a FHIR `Patient` resource with mandatory fields, allowed value sets, and a published JSON shape. The constraints that this track called `CHECK` show up in FHIR as **profiles** (US Core, mCODE, etc.) and **value set bindings**. The foreign keys show up as **references** between resources. The relational thinking is the same; the clinical semantics are layered on top.

        ### OMOP (course 07): an *analysis* schema

        OMOP CDM specifies a standardized clinical data warehouse schema: `person`, `visit_occurrence`, `condition_occurrence`, `drug_exposure`, `measurement`, `observation`. Same tables across every OHDSI-conformant institution, so an analysis written once works against any OMOP database. The constraints are the constraints this track introduced. The vocabulary is standardized (every concept gets an OMOP concept_id, mapped through a vocabulary server). The relational thinking is the same; the analytic semantics are layered on top.

        **Both rest on the relational rung.** Without the relational thinking in this track, FHIR feels like a lot of arbitrary clinical names, and OMOP feels like a lot of arbitrary table names. With it, both feel like clinical specializations of one underlying idea you now own.

        ## 8. What this leaves you

        Five things in place:

        1. **A database is a system that refuses to store data it can prove is wrong.** The refusal is the feature.
        2. **A schema is the published contract.** Tables, columns, types, constraints, relationships, all written down in DDL.
        3. **The six constraint types** (type, NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY, CHECK) cover most of the structural bugs that show up in clinical data.
        4. **Constraints catch what they are written to catch.** The classes of bug above the schema layer (cross-system semantics, real-world clinical surprises, things nobody anticipated) need governance, terminology, and application code, not just constraint declarations.
        5. **FHIR and OMOP are clinical specializations of the relational model.** Course 06 (FHIR) and course 07 (OMOP/SQL) build on this rung directly.

        Course 02 ends with the capstone, which takes everything you have built across the five tracks (typed, tidy, missingness-handled, joined, schema-aware) and applies it to a messy synthetic clinical export. After that, the curriculum moves to FHIR (06) and SQL plus OMOP (07).
        """
    )
    return


if __name__ == "__main__":
    app.run()
