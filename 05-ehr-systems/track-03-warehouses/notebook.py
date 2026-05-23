"""Track 03: Clinical data warehouses.

The analytical system that sits next to the operational EHR. OLTP vs
OLAP recap, ETL vs ELT, warehouse vs lake vs lakehouse, star schema, the
same data shown in EHR shape and CDW shape.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import sqlite3
    import time
    import types

    import marimo as mo
    import pandas as pd

    # Cross-reference helpers inlined from shared/cross_reference.py so the
    # WASM export is self-contained. Exposed as the `xref` namespace so the
    # call sites read the same as before.
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
        "13": "Research reproducibility",
        "14": "Interoperability policy",
        "15": "Data storytelling",
    }

    def _course_label(course_id):
        title = _COURSE_TITLES.get(course_id.split("-")[0])
        if title is None:
            return course_id
        return f"course {course_id.split('-')[0]}: {title}"

    def _xref_callback(from_course, to_course, topic, body):
        src = _course_label(to_course)
        return mo.callout(
            mo.vstack([mo.md(f"**Remember {topic} from {src}?**"), mo.md(body)]),
            kind="info",
        )

    def _xref_forward(from_course, to_course, topic, body):
        dst = _course_label(to_course)
        return mo.callout(
            mo.vstack([mo.md(f"**Forward to {dst}: {topic}**"), mo.md(body)]),
            kind="neutral",
        )

    xref = types.SimpleNamespace(callback=_xref_callback, forward=_xref_forward)

    return mo, pd, sqlite3, time, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 03: Clinical data warehouses

        ## What we left hanging in Track 01

        Track 01 ended with a structural observation: the operational EHR is built for one patient at a time, aggressively indexed for the chart, sparsely indexed for population queries. *Find all patients in our system currently on adalimumab* is a query the operational database is structurally bad at. *Find the average CRP in our seropositive RA cohort over the last twelve months* is worse.

        The field's answer is to build a second system, in parallel to the operational EHR, dedicated to those queries. That second system is called a **clinical data warehouse (CDW)**. It has different priorities: queries that scan millions of rows in seconds, joins across years of data, aggregations and group-bys that the chart never needs.

        This track has four parts:

        1. The transactional-versus-analytical distinction, recapped from course 00.
        2. ETL and ELT: how data gets from the EHR into the warehouse.
        3. Three storage architectures (warehouse, data lake, lakehouse) and what each is for.
        4. The star schema, walked on a synthetic CDW built from Ms. Reyes's data.

        The track gives you the vocabulary to read a vendor's analytical-architecture diagram and place every box on it.
        """
    )
    return


@app.cell
def _(mo, xref):
    xref.callback(
        from_course="05",
        to_course="00",
        topic="OLTP versus OLAP",
        body=(
            "Course 00 introduces the distinction at the field-orientation level. Two systems because two jobs. "
            "**OLTP (online transaction processing)** is the workload the operational EHR has: many small, fast, in-place writes; "
            "lookups by primary key; sub-second response; thousands of users at once. **OLAP (online analytical processing)** "
            "is the workload analytics has: a small number of large, scan-heavy reads; aggregations across millions of rows; "
            "occasional users with patient, multi-second tolerance. The two workloads want different indexes, different storage layouts, "
            "different hardware. The operational EHR is OLTP. The CDW is OLAP. **They are usually different physical systems running on different infrastructure**, "
            "and the bridge between them is the ETL pipeline below."
        ),
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## ETL and ELT: the bridge

        Data has to get from the operational EHR into the warehouse. The pattern is **ETL**:

        - **E**xtract data from the source system (the operational EHR, or one of its replicas).
        - **T**ransform the data: clean it, deduplicate, conform to standard codes, pivot the EAV flowsheet rows into wide tables, denormalize for query speed.
        - **L**oad the transformed data into the warehouse.

        ETL runs on a schedule (usually nightly, sometimes hourly, sometimes near-real-time). The output is the analytical-shaped tables that researchers and analysts actually query.

        The newer pattern is **ELT**, where the order changes:

        - **E**xtract from the source.
        - **L**oad the raw data into the warehouse first.
        - **T**ransform inside the warehouse, using its compute power.

        ELT became practical when warehouse storage got cheap enough to hold raw plus transformed data, and when warehouse engines (Snowflake, BigQuery, Redshift, Databricks) got powerful enough to transform at scale. ELT keeps the raw landing data around forever, which makes lineage tracing and back-fills much easier.

        The practical difference:

        | Pattern | Where transformation happens | When raw data is dropped | When you'd use it |
        |---|---|---|---|
        | ETL | On a separate processing server before loading | Immediately after T | Legacy CDW deployments; small footprints; strict pre-load validation |
        | ELT | Inside the warehouse, on raw landing tables | Kept indefinitely | Modern cloud warehouses; data lakes; when you want lineage and re-runs |

        Both names describe the *same three operations* in different order. The transformation step is where most of the clinical-data-quality work lives (Track 05 of this course).

        A real production pipeline is a dependency graph of ETL or ELT jobs orchestrated by a tool like Apache Airflow, Prefect, dbt, or Microsoft SSIS. The jobs read from one source, write to another, and each job's success or failure is monitored. A hospital running on Epic typically has hundreds of these jobs running nightly to keep the warehouse current.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Warehouse, lake, lakehouse: three storage architectures

        The word "warehouse" hides three distinct architectural patterns. They are all valid; each is right for different parts of the analytical workload.

        ### Data warehouse

        A traditional **data warehouse** is a relational database, often columnar, holding *schema-on-write* tables. Every load is preceded by a transformation that conforms the data to a pre-defined schema. The data inside the warehouse is clean, typed, deduplicated, and indexed for analytical queries. Vendor examples: Oracle Exadata, Microsoft SQL Server with columnstore, Snowflake, Amazon Redshift, Google BigQuery, Teradata, IBM Db2 Warehouse.

        A clinical-data-warehouse-specific vendor stack:

        - **Epic Caboodle** is Epic's own bundled CDW product. It ships with a defined star schema (one big fact table per clinical domain, surrounded by dimension tables) and a set of pre-built reports. Most Epic shops use it.
        - **Cerner CCL / HealtheIntent** is Oracle Health's equivalent stack.
        - **Custom CDW** is what many academic medical centers built before vendor offerings existed. A team of analysts maps the Clarity (Epic's operational schema) or Cerner Millennium replica into a hand-designed star schema. Custom CDWs are usually painful to maintain but flexible.

        ### Data lake

        A **data lake** is a large object-storage bucket holding *schema-on-read* files. You dump raw data into it (CSV, JSON, Parquet, log files, image files, FHIR bundles, ORU dumps, whatever) and impose schema at query time. Vendor examples: Amazon S3 with Athena, Azure Data Lake Storage with Synapse, Google Cloud Storage with BigQuery external tables.

        A lake is the right answer when:

        - You have many heterogeneous source formats.
        - You want to keep raw data around forever for lineage and re-runs.
        - You have machine-learning workloads that want raw signal, not pre-aggregated rows.
        - The cost per terabyte matters and the access patterns are scan-heavy and infrequent.

        Lakes were the natural home of the late-2010s analytics workloads driven by AI training pipelines. They are also harder to govern: without strong cataloging and metadata, a data lake degrades into a "data swamp" where nobody knows what each file means.

        ### Lakehouse

        A **lakehouse** is the architecture that emerged in 2020 trying to keep the best of both. It uses cheap object storage as the underlying physical layer (like a lake) but adds a transactional table layer on top that gives you warehouse-style schemas, ACID transactions, time travel, and indexes (like a warehouse). The table layer is something like Delta Lake, Apache Iceberg, or Apache Hudi. Vendor examples: Databricks Lakehouse (Delta), Snowflake with Iceberg tables, Microsoft Fabric.

        In a clinical context, lakehouses are increasingly the architecture of choice for new builds. They support both the OMOP / star-schema analytical workload *and* the AI-training workload from a single underlying storage layer.

        | Architecture | Storage primitive | Schema enforcement | Best fit |
        |---|---|---|---|
        | Data warehouse | Block storage, columnar tables | Schema on write | Reporting, dashboards, traditional BI |
        | Data lake | Object storage, raw files | Schema on read | Heterogeneous raw data, ML training, archival |
        | Lakehouse | Object storage + transactional table layer | Schema on write, lake economics | Modern unified analytics + ML, increasingly the default |

        Most hospitals run a hybrid. The warehouse holds the audited, governed, reportable views. The lake holds the raw landing and the AI-training corpora. The trend is toward lakehouse as the unifying layer.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The star schema

        The dominant logical design inside a clinical data warehouse is the **star schema**. The pattern is simple to describe and powerful in practice:

        - **One fact table per clinical domain.** Lab results, medication orders, encounters, claims, vital signs. Each row is one measurable event. Numeric measures, foreign keys to the dimensions, and very little else.
        - **Several dimension tables surrounding each fact.** Patient, provider, date, location, drug, lab test. Each dimension is small (thousands to millions of rows), descriptive, and changes slowly.
        - **The fact table is huge** (tens of millions to billions of rows). The dimensions are small. Queries join the fact to a few dimensions, filter, aggregate.

        Drawn:

        ```
                              dim_patient
                                  |
        dim_provider --- fact_lab_result --- dim_date
                                  |
                              dim_lab_test
        ```

        The star is the same family of design as Kimball-style dimensional modeling that the BI world has used since the 1990s. The clinical adaptation is that the dimensions and facts are explicitly named for clinical concepts, the codes are clinical codes, and the time grain is clinical time.

        Let's see Ms. Reyes's CRP value in both shapes side by side: the operational-EHR shape from Track 01 and the star-schema CDW shape.
        """
    )
    return


@app.cell
def _(mo, pd, sqlite3):
    # Build a tiny CDW with three dimensions and one fact, using Reyes's data.
    cdw_conn = sqlite3.connect(":memory:")

    dim_patient = pd.DataFrame([
        {"patient_key": 1, "mrn": "ER-001", "patient_name": "Reyes, Elena Maria",
         "birth_date": "1974-02-09", "sex": "F", "race": "White", "ethnicity": "Hispanic or Latino",
         "valid_from": "2022-02-14", "valid_to": "9999-12-31", "is_current": 1},
    ])
    dim_patient.to_sql("dim_patient", cdw_conn, index=False)

    dim_date = pd.DataFrame([
        {"date_key": 20240108, "calendar_date": "2024-01-08", "year": 2024, "quarter": 1, "month": 1, "day_of_week": "Monday"},
        {"date_key": 20260210, "calendar_date": "2026-02-10", "year": 2026, "quarter": 1, "month": 2, "day_of_week": "Tuesday"},
    ])
    dim_date.to_sql("dim_date", cdw_conn, index=False)

    dim_lab_test = pd.DataFrame([
        {"lab_test_key": 1, "loinc_code": "1988-5", "test_name": "C-reactive protein", "specimen_type": "Serum", "units": "mg/L", "normal_low": 0.0, "normal_high": 5.0},
        {"lab_test_key": 2, "loinc_code": "4537-7", "test_name": "Erythrocyte sedimentation rate", "specimen_type": "Whole blood", "units": "mm/h", "normal_low": 0.0, "normal_high": 20.0},
        {"lab_test_key": 3, "loinc_code": "32218-7", "test_name": "Cyclic citrullinated peptide IgG Ab", "specimen_type": "Serum", "units": "U/mL", "normal_low": 0.0, "normal_high": 20.0},
    ])
    dim_lab_test.to_sql("dim_lab_test", cdw_conn, index=False)

    fact_lab_result = pd.DataFrame([
        {"lab_result_key": 1001, "patient_key": 1, "date_key": 20240108, "lab_test_key": 1, "result_value": 36.2, "abnormal_flag": "H"},
        {"lab_result_key": 1002, "patient_key": 1, "date_key": 20240108, "lab_test_key": 2, "result_value": 51.0, "abnormal_flag": "H"},
        {"lab_result_key": 1003, "patient_key": 1, "date_key": 20240108, "lab_test_key": 3, "result_value": 154.0, "abnormal_flag": "H"},
        {"lab_result_key": 1004, "patient_key": 1, "date_key": 20260210, "lab_test_key": 1, "result_value": 21.4, "abnormal_flag": "H"},
        {"lab_result_key": 1005, "patient_key": 1, "date_key": 20260210, "lab_test_key": 2, "result_value": 33.0, "abnormal_flag": "H"},
    ])
    fact_lab_result.to_sql("fact_lab_result", cdw_conn, index=False)

    star_view = mo.vstack([
        mo.md("### `dim_patient` (one row per current patient state)"),
        mo.as_html(dim_patient),
        mo.md("### `dim_date` (one row per calendar day, decoded)"),
        mo.as_html(dim_date),
        mo.md("### `dim_lab_test` (one row per LOINC concept)"),
        mo.as_html(dim_lab_test),
        mo.md("### `fact_lab_result` (one row per result component)"),
        mo.as_html(fact_lab_result),
    ])
    star_view
    return (cdw_conn,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Notice the differences from the Track 01 schema:

        - **Surrogate keys instead of natural keys.** The `patient_key` is an arbitrary integer chosen by the warehouse, not the MRN. This makes joins cheap and handles the case where a patient's MRN changes (which happens during a merge). The MRN lives as an attribute on `dim_patient` but is not the join key.
        - **Date dimension is its own table.** Calendar dates are decoded into year, quarter, month, day-of-week so analytics can group by any of them without re-parsing strings.
        - **Lab test catalog is its own dimension.** The LOINC code, the test name, the units, and the reference range live on the dimension. The fact only carries the foreign key.
        - **The fact is narrow.** Five columns. The whole point is that the fact table is going to be tens of millions of rows, so every column counts.

        Now compare the same clinical question asked of both schemas.
        """
    )
    return


@app.cell
def _(cdw_conn, mo, pd):
    # Show side-by-side queries.
    cdw_query = """
        SELECT
            d.calendar_date,
            t.test_name,
            t.loinc_code,
            f.result_value,
            t.units,
            f.abnormal_flag
        FROM fact_lab_result f
        JOIN dim_patient p   ON f.patient_key = p.patient_key
        JOIN dim_date d      ON f.date_key = d.date_key
        JOIN dim_lab_test t  ON f.lab_test_key = t.lab_test_key
        WHERE p.mrn = 'ER-001'
          AND t.loinc_code = '1988-5'
          AND d.year IN (2024, 2026)
        ORDER BY d.calendar_date;
    """
    cdw_result = pd.read_sql(cdw_query, cdw_conn)
    cdw_result.index = range(1, len(cdw_result) + 1)
    cdw_result.index.name = "row"

    compare_view = mo.vstack([
        mo.md(
            r"""
            ### Same question, two systems

            **Question:** all CRP results for Ms. Reyes from 2024 onward.

            **Track 01 (operational EHR) version of the query:** had to join `LAB_RESULT` to `PATIENT`, then filter by MRN, then filter the result rows on `COMPONENT_NAME = 'CRP'` (because the operational schema stores the test name as a string on each row).

            **CDW (star schema) version of the query:**
            """
        ),
        mo.md("```sql\n" + cdw_query.strip() + "\n```"),
        mo.md("**Query output (the data this analytical view produces):**"),
        mo.as_html(cdw_result),
        mo.callout(
            mo.md(
                "Three things changed. The query is keyed on the LOINC code, not on a brittle string match. "
                "The date is filtered by year on `dim_date`, not by parsing a string column. The join through "
                "`dim_patient` lets the MRN itself change (during a merge, for example) without breaking historical "
                "fact rows. None of this matters for a single Reyes lookup. All of it matters when you ask the same "
                "question across 200,000 patients."
            ),
            kind="info",
        ),
    ])
    compare_view
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Common clinical CDW stacks

        Three production patterns to know:

        - **Vendor-bundled CDW.** Epic Caboodle, Oracle Cerner HealtheIntent, Athenahealth's analytics platform. The vendor ships the ETL, the schema, and a library of canned reports. Low effort to stand up. Locked to the vendor's chosen model.
        - **Custom hospital CDW.** A hand-built star schema on Microsoft SQL Server, Snowflake, or Redshift, populated by a custom ETL the analytics team owns. High effort to stand up and maintain. Maximum flexibility. Most academic medical centers have one.
        - **Standardized common data model.** **OMOP** (Observational Medical Outcomes Partnership), **PCORnet CDM**, **i2b2 / ACT**, or **Sentinel**. The hospital maps its source data into a shared schema designed by a research consortium. The payoff is that any tool written for that common data model works on your data. We get to OMOP in detail in course 07.

        Most academic medical centers run all three at once: the vendor-bundled CDW for operations, a custom CDW for institution-specific analytics, and an OMOP or PCORnet mart for federated research.

        ### How the layers stack

        ```
        Operational EHR (OLTP)            <- charting, orders, results
              |
              | ETL / ELT (nightly to near-real-time)
              v
        Vendor-bundled CDW (Caboodle, etc.)
              |
              | additional ETL
              v
        Custom hospital CDW (institution-owned)
              |
              | mapping ETL (concept-id-based)
              v
        OMOP / PCORnet research mart
              |
              v
        Federated analytics across networks
        ```

        Every arrow is a transformation, with attendant data-quality work and attendant data loss. Course 07's OMOP track says explicitly: no standard is lossless. Every step of this chain pays some loss. The point is that the gain (interoperability, query speed, federated research) is bigger than the loss, for the workloads that live downstream.
        """
    )
    return


@app.cell
def _(mo):
    cdw_quiz = mo.ui.radio(
        options=[
            "Schema on read; transform after loading; raw heterogeneous files preserved.",
            "Pre-defined star schema; ETL applies transformation before loading; clean clinical concepts only.",
            "Always built on a single vendor product such as Snowflake.",
            "Operational system with sub-second writes for the chart.",
        ],
        label=(
            "**A medical center wants to stand up an analytical environment that researchers can query with confidence, "
            "knowing the CRP rows have been deduplicated, the LOINC codes are conformed, and the patient identifiers "
            "have been merge-stabilized. Which architectural pattern fits best?**"
        ),
    )
    cdw_quiz
    return (cdw_quiz,)


@app.cell
def _(cdw_quiz, mo):
    mo.stop(cdw_quiz.value is None, mo.md("_Choose an answer._"))
    cdw_correct = cdw_quiz.value.startswith("Pre-defined star")

    if cdw_correct:
        cdw_feedback = (
            "Right. The traditional **data warehouse** with a star schema and schema-on-write ETL is the architecture that "
            "pre-cleans the data and gives researchers a stable, governed surface to query. Schema-on-read lakes are great "
            "for raw heterogeneous files and ML training but require every analyst to redo the cleanup. Vendor lock-in is an "
            "implementation detail, not the pattern. The operational EHR is the OLTP system the CDW is *replacing* for this workload."
        )
    elif cdw_quiz.value.startswith("Schema on read"):
        cdw_feedback = (
            "Close but not quite. Schema-on-read describes a **data lake**. Lakes are excellent for raw heterogeneous files "
            "and ML training workloads, but they push the cleanup work onto every analyst. For a researcher-facing analytical "
            "surface with conformed CRP rows and merge-stable patient identifiers, a pre-cleaned warehouse with a star schema "
            "is the conventional answer."
        )
    elif cdw_quiz.value.startswith("Always built"):
        cdw_feedback = (
            "Snowflake is one popular underlying engine, but it is not the architectural pattern. The pattern is the "
            "pre-defined star schema with schema-on-write ETL. That pattern runs on Snowflake, Redshift, BigQuery, Synapse, "
            "Microsoft SQL Server with columnstore, Oracle Exadata, and others."
        )
    else:
        cdw_feedback = (
            "Operational systems are the ones the warehouse pulls *from*, not the warehouse itself. Sub-second writes for the chart "
            "describe the OLTP workload; analytical environments are OLAP."
        )
    mo.callout(mo.md(cdw_feedback), kind="success" if cdw_correct else "warn")
    return


@app.cell
def _(xref):
    xref.forward(
        from_course="05",
        to_course="07",
        topic="Querying the warehouse",
        body=(
            "This track introduced the warehouse and showed you what its tables look like. Course 07 (Data wrangling and engineering) "
            "is where you actually work with one. Track 1 builds SQL from first principles on clinical data, Track 2 covers pandas, "
            "and Track 4 walks the OMOP common data model end to end (the standardized research mart pattern named above). "
            "If this track raised more questions about how the data gets shaped than answers, that is intentional. Course 07 picks them up."
        ),
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Where this leaves you

        Two systems because two jobs. The operational EHR is OLTP, optimized for the chart. The clinical data warehouse is OLAP, optimized for population queries. ETL or ELT moves data between them, transforming along the way. The dominant logical design inside the warehouse is the star schema. The dominant physical pattern in 2026 is increasingly the lakehouse.

        Track 04 is imaging informatics: how PACS and DICOM fit into the system above. Track 05 is real-world data quality, which is where the architectural story meets the messy clinical-data-on-the-ground story.
        """
    )
    return


if __name__ == "__main__":
    app.run()
