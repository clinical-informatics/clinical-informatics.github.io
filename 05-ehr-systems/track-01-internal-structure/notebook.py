"""Track 01: How EHRs structure data internally.

The chart-side view of the EHR is one screen at a time. The database-side
view is a few hundred tables. This notebook walks the logical relational
structure on Ms. Reyes's synthetic Epic-style export, then walks the
physical storage layer that the relational structure sits on top of.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import json
    import sqlite3
    import sys
    import time
    import types
    from pathlib import Path

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

    # Read the Epic-style export. Works locally and in WASM. The Pyodide
    # branch uses a site-absolute path (resolved against the page origin),
    # which works identically in the main thread and in the marimo worker.
    # The build pipeline mirrors cache/ into the WASM export, with this file
    # symlinked from start-here/patients/elena-reyes/.
    if "pyodide" in sys.modules:
        from pyodide.http import open_url

        reyes = json.loads(
            open_url(
                "/05-ehr-systems/track-01-internal-structure/app/cache/ehr-export-epic.json"
            ).read()
        )
    else:
        reyes = json.loads(
            (Path(__file__).parent / "cache" / "ehr-export-epic.json").read_text()
        )

    return json, mo, pd, reyes, sqlite3, time, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 01: How EHRs structure data internally

        ## What you see on the chart is one row of one table

        Open Ms. Reyes's chart in any EHR and click **Medications**. You see three lines: methotrexate, adalimumab, folic acid. Each has a dose, a route, a frequency, a start date, a current status.

        That tidy list is not how the data is stored. The medications screen is rendered by a query that touches at least five tables: one for the medication order itself, one for the underlying drug entity, one for the route and the frequency lookups, one for the prescriber, and one for the patient that ties them all together. When you click **Allergies**, you get a different query touching a different set of tables. When you click **Problems**, another one.

        The EHR you use every day is a fast renderer in front of a relational database that follows the same rules as any other relational database. The renderer is good enough that most clinicians never have to think about the database. The price of that abstraction is that almost every interesting clinical-informatics question lives one layer below the renderer, and you cannot answer it without seeing the tables.

        This track has two halves. The first half is the logical view: tables, joins, the flowsheet pattern, and indexes. The second half is the physical view: where the tables actually live on disk, what storage tier they sit on, and what each storage choice buys clinically.

        We use Ms. Reyes's synthetic Epic-style export. Her PAT_ID in this export is `Z9847562` and her MRN is `ER-001`.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        # Part 1: The logical view

        ## What a relational EHR schema looks like

        Almost every operational EHR in the United States runs on a relational database underneath. Epic uses Caché (an object database that Epic accesses through SQL). Oracle Health (Cerner) uses Oracle. MEDITECH and Athenahealth use Microsoft SQL Server. The exact engine differs; the relational model does not.

        A *relational database* stores data in tables. Each table has rows and columns. Each row is a single fact (one patient, one encounter, one medication order, one lab result). Each column is one attribute of that fact. Tables connect to each other through *foreign keys*: a column in one table that points at the primary key of another.

        Below is what the schema behind Ms. Reyes's chart looks like, at the level you would see if you opened the data dictionary of a real Epic Clarity database. Eight tables; the arrows show foreign-key relationships. This is a small slice; a real production schema has hundreds.

        ```
        PATIENT (PAT_ID*, MRN, NAME, BIRTH_DATE, SEX, RACE, ETHNICITY, ...)
           |
           +---< ENCOUNTER (PAT_ENC_CSN_ID*, PAT_ID, CONTACT_DATE, DEPARTMENT, VISIT_PROV_ID, ...)
           |        |
           |        +---< LAB_RESULT (ORDER_PROC_ID*, PAT_ENC_CSN_ID, COMPONENT_ID, ORD_VALUE, ...)
           |        |
           |        +---< FLOWSHEET_VALUE (FLO_MEAS_ID*, PAT_ENC_CSN_ID, MEAS_VALUE, RECORDED_TIME, ...)
           |
           +---< PROBLEM_LIST (PROBLEM_LIST_ID*, PAT_ID, DX_ID, NOTED_DATE, STATUS, ...)
           |        |
           |        +--->  DIAGNOSIS (DX_ID*, DX_NAME, ICD10_LIST, ...)
           |
           +---< MEDICATION_ORDER (ORDER_MED_ID*, PAT_ID, RXNORM_CODE, DOSE, ROUTE, FREQUENCY, START_DATE, ...)
           |
           +---< ALLERGY (ALG_ID*, PAT_ID, ALLERGEN_NAME, REACTION, SEVERITY, ...)
        ```

        Read that schema and a few things should be visible:

        - **One table per kind of fact.** Patients in one. Encounters in another. Medications in a third. The EHR does not have a "Ms. Reyes table." It has a `PATIENT` row whose primary key is referenced by every other row about her.
        - **The patient identifier is everywhere.** `PAT_ID` (Epic's term for the internal patient identifier; the MRN is a separate human-facing identifier) appears as a foreign key on almost every other table.
        - **Encounters are the second axis.** Almost every clinical fact happened *during an encounter*. The `PAT_ENC_CSN_ID` foreign key is how labs and flowsheet values know which visit they belong to.
        - **Lookup tables exist for everything.** When the EHR records that an allergy reaction is *Rash*, it usually stores a code that points at a Rash row in a lookup table. The display string travels with the lookup, not the row.

        That last point is why exports of the same record from two different EHR vendors look completely different. The codes are vendor-specific. The decoded display strings are mostly the same. The shape of the data is *similar* because the relational model is similar, but every table name, every column name, and every code is different. That is why FHIR and OMOP exist. We come back to that in Tracks 02 and 03.

        Let's see what Ms. Reyes's row looks like in each of these tables.
        """
    )
    return


@app.cell
def _(mo, pd, reyes):
    patient_df = pd.DataFrame([reyes["PAT_ENC"]])[
        ["PAT_ID", "PAT_MRN_ID", "PAT_NAME", "BIRTH_DATE", "SEX_C_NAME", "RACE_C_NAME", "ETHNIC_GROUP_C_NAME"]
    ]
    patient_df.index = ["Reyes"]

    encounter_df = pd.DataFrame(reyes["ENCOUNTERS"])[
        ["PAT_ENC_CSN_ID", "PAT_ID", "CONTACT_DATE", "ENC_TYPE_C_NAME", "DEPARTMENT_NAME", "VISIT_PROV_NAME"]
    ]
    encounter_df.index = range(1, len(encounter_df) + 1)
    encounter_df.index.name = "row"

    med_df = pd.DataFrame(reyes["MEDICATIONS"])[
        ["ORDER_MED_ID", "PAT_ID", "MEDICATION_NAME", "DOSE", "DOSE_UNIT_C_NAME", "ROUTE_C_NAME", "FREQUENCY_C_NAME", "START_DATE", "RXNORM_CODE"]
    ]
    med_df.index = range(1, len(med_df) + 1)
    med_df.index.name = "row"

    problem_df = pd.DataFrame(reyes["PROBLEM_LIST"])[
        ["PROBLEM_LIST_ID", "PAT_ID", "DX_ID", "DX_NAME", "ICD10_LIST", "PROBLEM_STATUS_C_NAME", "NOTED_DATE"]
    ]
    problem_df.index = range(1, len(problem_df) + 1)
    problem_df.index.name = "row"

    allergy_df = pd.DataFrame(reyes["ALLERGIES"])[
        ["ALG_ID", "PAT_ID", "ALLERGEN_NAME", "REACTION", "SEVERITY_C_NAME", "STATUS_C_NAME"]
    ]
    allergy_df.index = range(1, len(allergy_df) + 1)
    allergy_df.index.name = "row"

    lab_df = pd.DataFrame(reyes["LAB_RESULTS"])[
        ["ORDER_PROC_ID", "PAT_ID", "RESULT_TIME", "COMPONENT_NAME", "ORD_VALUE", "REFERENCE_UNIT", "LOINC_CODE"]
    ]
    lab_df.index = range(1, len(lab_df) + 1)
    lab_df.index.name = "row"

    tables_view = mo.vstack([
        mo.md("### `PATIENT` table (one row for Ms. Reyes)"),
        mo.as_html(patient_df),
        mo.md("### `ENCOUNTER` table (four rows, each one a visit)"),
        mo.as_html(encounter_df),
        mo.md("### `MEDICATION_ORDER` table (three rows, one per active order)"),
        mo.as_html(med_df),
        mo.md("### `PROBLEM_LIST` table (three rows, one per active problem)"),
        mo.as_html(problem_df),
        mo.md("### `ALLERGY` table (one row)"),
        mo.as_html(allergy_df),
        mo.md("### `LAB_RESULT` table (five rows from her two recent visits)"),
        mo.as_html(lab_df),
    ])
    tables_view
    return allergy_df, encounter_df, lab_df, med_df, patient_df, problem_df


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What a click costs in SQL

        The medications screen in the EHR shows three lines, one per active drug. Behind that screen is a SQL query. Let's write it.

        In plain English: *for patient ER-001, show me every active medication order, with the drug name, dose, route, frequency, and prescribing provider*. That sentence is one line of clinician-speak. In SQL it is roughly this:

        ```sql
        SELECT
            m.MEDICATION_NAME,
            m.DOSE,
            m.DOSE_UNIT,
            m.ROUTE,
            m.FREQUENCY,
            m.START_DATE,
            p.PAT_NAME,
            e.CONTACT_DATE AS prescribed_at
        FROM   MEDICATION_ORDER m
        JOIN   PATIENT p          ON m.PAT_ID = p.PAT_ID
        LEFT JOIN ENCOUNTER e     ON m.ORDERING_ENC_ID = e.PAT_ENC_CSN_ID
        WHERE  p.PAT_MRN_ID = 'ER-001'
          AND  m.ORDER_STATUS = 'Active';
        ```

        Three tables. One inner join for the patient (we need her name to confirm we got the right person). One left join for the encounter (the order may or may not be tied to a specific visit in our schema). One filter on MRN and one on status. The EHR is doing some version of that query every time you load the screen, and it is doing it in milliseconds because the database has been tuned for exactly this pattern of access.

        Let's run it for real on Ms. Reyes's data. We load the tables into an in-memory SQLite database below and run the query against it.
        """
    )
    return


@app.cell
def _(allergy_df, encounter_df, lab_df, med_df, mo, pd, patient_df, problem_df, sqlite3):
    # Build an in-memory SQLite database from Ms. Reyes's data.
    conn = sqlite3.connect(":memory:")

    patient_df.rename(columns={"PAT_MRN_ID": "MRN"}).to_sql("PATIENT", conn, index=False)
    encounter_df.to_sql("ENCOUNTER", conn, index=False)
    med_df.rename(columns={"DOSE_UNIT_C_NAME": "DOSE_UNIT", "ROUTE_C_NAME": "ROUTE", "FREQUENCY_C_NAME": "FREQUENCY"}).assign(
        ORDER_STATUS="Active",
        ORDERING_ENC_ID=["ENC-300102", "ENC-300120", "ENC-300102"],
    ).to_sql("MEDICATION_ORDER", conn, index=False)
    problem_df.to_sql("PROBLEM_LIST", conn, index=False)
    allergy_df.to_sql("ALLERGY", conn, index=False)
    lab_df.to_sql("LAB_RESULT", conn, index=False)

    medications_sql = """
        SELECT
            m.MEDICATION_NAME,
            m.DOSE,
            m.DOSE_UNIT,
            m.ROUTE,
            m.FREQUENCY,
            m.START_DATE,
            p.PAT_NAME,
            e.CONTACT_DATE AS prescribed_at
        FROM   MEDICATION_ORDER m
        JOIN   PATIENT p          ON m.PAT_ID = p.PAT_ID
        LEFT JOIN ENCOUNTER e     ON m.ORDERING_ENC_ID = e.PAT_ENC_CSN_ID
        WHERE  p.MRN = 'ER-001'
          AND  m.ORDER_STATUS = 'Active';
    """
    medications_result = pd.read_sql(medications_sql, conn)
    medications_result.index = range(1, len(medications_result) + 1)
    medications_result.index.name = "row"

    meds_view = mo.vstack([
        mo.md("**Query output** (this is what the EHR renders as the three-line medications panel)"),
        mo.as_html(medications_result),
        mo.callout(
            mo.md(
                "Three rows out. Three table reads, three joins, one filter on MRN, one filter on status. "
                "The medications screen is the renderer turning these rows into a clean list. "
                "Multiply this pattern by every screen in the EHR and you have a fair sense of the workload "
                "the database is handling all day."
            ),
            kind="info",
        ),
    ])
    meds_view
    return conn, medications_result


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The flowsheet pattern: when the relational model bends

        Most of the EHR follows the relational model cleanly. One table per kind of fact, one row per instance, one column per attribute. Labs, medications, encounters, problems, allergies: all of these fit neatly into well-shaped tables.

        Then there is the flowsheet. Vital signs, intake and output, joint counts, pain scales, infusion-flow values, ventilator settings, the entire ICU monitoring trace. Thousands of distinct *kinds* of measurement, each captured at high frequency, each labeled differently in every department. If you tried to model that as one table per kind, you would have ten thousand tables and a schema that changes every time clinical operations adds a new flowsheet row.

        So every EHR uses a different pattern for flowsheets, called **entity-attribute-value** (EAV). One table. Three columns that carry the meaning: *what kind of measurement is this*, *what is the value*, *when was it recorded*. Every clinically distinct measurement becomes a row, not a column.

        Here is what Ms. Reyes's flowsheet rows from her 2026-02-10 visit look like:
        """
    )
    return


@app.cell
def _(mo, pd, reyes):
    flowsheet_df = pd.DataFrame(reyes["FLOWSHEET_VALUES"])
    flowsheet_df.index = range(1, len(flowsheet_df) + 1)
    flowsheet_df.index.name = "row"

    eav_demo = pd.DataFrame({
        "row_id": [1, 2, 3, 4, 5, 6],
        "patient_id": ["ER-001"] * 6,
        "encounter_id": ["ENC-300148"] * 6,
        "measurement_name": ["DAS28-CRP", "Tender joint count", "Swollen joint count", "Patient global VAS", "BP - Systolic", "BP - Diastolic"],
        "measurement_value": ["2.8", "2", "1", "32", "122", "76"],
        "recorded_time": ["2026-02-10 09:00", "2026-02-10 09:00", "2026-02-10 09:00", "2026-02-10 09:00", "2026-02-10 08:50", "2026-02-10 08:50"],
    })
    eav_demo.index = range(1, len(eav_demo) + 1)
    eav_demo.index.name = "row"

    flowsheet_view = mo.vstack([
        mo.md("**Ms. Reyes's flowsheet rows, 2026-02-10:**"),
        mo.as_html(flowsheet_df),
        mo.md(
            "Six rows for what a clinician sees as one assessment. The trade-off should be clear: "
            "the schema is flexible (we can add a new measurement kind without changing the table), "
            "but every query has to *unstack* the rows before it can do anything useful. "
            "Calculating DAS28 from the components, for example, means selecting four rows and pivoting them sideways."
        ),
        mo.md("### Why this matters for analytics"),
        mo.md(
            "Flowsheet data is the EAV anti-pattern done on purpose, because the alternative is unworkable. "
            "When you eventually pull this data into a clinical data warehouse (Track 03), one of the first "
            "things the warehouse does is *pivot* the EAV rows into a wide table you can actually analyze. "
            "The trade is the same trade every clinical data warehouse makes: pay flexibility on capture, "
            "buy back queryability on analysis."
        ),
    ])
    flowsheet_view
    return (flowsheet_df,)


@app.cell
def _(mo):
    eav_quiz = mo.ui.radio(
        options=[
            "Flowsheets store fewer rows than a strictly relational schema would.",
            "Flowsheets let clinical operations add a new measurement kind without a schema change.",
            "Flowsheets are easier to query than a strictly relational schema.",
            "Flowsheets are required by HIPAA for high-frequency measurements.",
        ],
        label="**Why does almost every EHR use the EAV (flowsheet) pattern for vitals and assessments?**",
    )
    eav_quiz
    return (eav_quiz,)


@app.cell
def _(eav_quiz, mo):
    mo.stop(eav_quiz.value is None, mo.md("_Choose an answer._"))
    correct1 = eav_quiz.value == "Flowsheets let clinical operations add a new measurement kind without a schema change."

    if correct1:
        eav_msg = (
            "Correct. The EAV pattern trades query convenience for schema flexibility. "
            "New flowsheet rows (a new pain scale, a new infusion-titration measurement) become new *rows* "
            "in a lookup table, not new *columns* in a wide table. Operations can configure them in minutes "
            "without involving the database team or risking downtime. The cost is paid every time analytics tries to use the data, "
            "which is why the data warehouse pivots it back out."
        )
    else:
        eav_msg = (
            "Not quite. The flowsheet pattern actually stores *more* rows than a strictly relational schema would, "
            "is generally *harder* to query (you have to pivot before you can analyze), and is not required by HIPAA. "
            "The reason it exists is operational flexibility: a new measurement kind is a new row in a lookup table, "
            "not a schema change. That is the trade EAV makes."
        )
    mo.callout(mo.md(eav_msg), kind="success" if correct1 else "warn")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Indexes: why "Reyes, Elena" is instant and "everyone on adalimumab" is not

        Try this in your head. You run an EHR for a 600-bed hospital. The `MEDICATION_ORDER` table has 80 million rows: every order written in your hospital over the last decade. Someone clicks Ms. Reyes's chart and the medications screen renders in under a second. Someone else asks "how many patients in our system are currently on adalimumab" and the answer takes four minutes.

        Both queries are reading the same table. The difference is **indexes**.

        An index is a separate data structure that lets the database find rows by a specific column without scanning the whole table. If the `MEDICATION_ORDER` table has an index on `PAT_ID`, finding *all rows for Reyes* is a tree lookup followed by a few page reads. Milliseconds. If there is no index on `RXNORM_CODE`, finding *all rows where RXNORM = 327361 (adalimumab)* is a full-table scan. 80 million row reads.

        Operational EHRs are aggressively indexed on the access patterns that the chart uses: patient identifier, encounter identifier, date ranges, provider identifier. They are usually *not* indexed on the access patterns that population queries use: drug codes, diagnosis codes, lab values. The reason is that every index you add slows down inserts and updates (because the index has to be maintained), and the operational EHR is fundamentally an insert and update workload. The chart writes a new flowsheet value every five minutes per ICU patient. Adding an index that the chart does not need is paying a tax forever for a query that runs occasionally.

        Below is a tiny version of this trade-off, on a 200,000-row synthetic medication table. We run the same query twice. Once without an index. Once with one.
        """
    )
    return


@app.cell
def _(mo, pd, sqlite3, time):
    # Build a 200k-row synthetic MEDICATION_ORDER table for the index demo.
    bench_conn = sqlite3.connect(":memory:")
    n = 200_000
    rxnorm_pool = ["1156665", "327361", "315966", "197361", "313988", "1191"]
    rxnorm_col = [rxnorm_pool[i % 6] for i in range(n)]
    pat_col = [f"PAT-{(i % 25_000):05d}" for i in range(n)]

    bench_df = pd.DataFrame({
        "ORDER_MED_ID": [f"RX-{i:07d}" for i in range(n)],
        "PAT_ID": pat_col,
        "RXNORM_CODE": rxnorm_col,
        "DOSE": [40 if r == "327361" else 25 for r in rxnorm_col],
    })
    bench_df.to_sql("MEDICATION_ORDER", bench_conn, index=False)

    def time_query(sql):
        start = time.perf_counter()
        out = pd.read_sql(sql, bench_conn)
        elapsed = (time.perf_counter() - start) * 1000.0
        return out, elapsed

    rxnorm_query = "SELECT COUNT(*) AS n FROM MEDICATION_ORDER WHERE RXNORM_CODE = '327361';"
    out_unindexed, t_unindexed = time_query(rxnorm_query)

    bench_conn.execute("CREATE INDEX idx_med_rxnorm ON MEDICATION_ORDER(RXNORM_CODE);")
    out_indexed, t_indexed = time_query(rxnorm_query)

    speedup = t_unindexed / t_indexed if t_indexed > 0 else float("inf")

    bench_view = mo.vstack([
        mo.md(
            f"""
            **Same query, run twice on a 200,000-row synthetic medication table.**

            Query: count every order with RXNORM 327361 (adalimumab). True answer: **{int(out_unindexed.iloc[0,0]):,}** rows.

            | Run | Configuration | Wall time |
            |---|---|---|
            | 1 | No index on RXNORM_CODE (full table scan) | **{t_unindexed:.1f} ms** |
            | 2 | After `CREATE INDEX idx_med_rxnorm ON MEDICATION_ORDER(RXNORM_CODE)` | **{t_indexed:.1f} ms** |

            Speedup from the index: roughly **{speedup:.0f}x** on this tiny demo.
            """
        ),
        mo.callout(
            mo.md(
                "On a production table with 80 million rows instead of 200,000, the unindexed scan would be "
                "many seconds and the indexed lookup would still be milliseconds. The qualitative shape of the "
                "trade is what matters: indexes are the lever that turns *find all patients on X* from a "
                "long-running batch job into an interactive query. The operational EHR is conservative about "
                "adding them because every index costs at insert time, and the chart is mostly inserting. "
                "This is one of the reasons research and population queries are usually run against a separate system, "
                "which is what Track 03 is about."
            ),
            kind="info",
        ),
    ])
    bench_view
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        # Part 2: The physical view

        ## Where the tables actually live

        The relational schema is the *logical* picture. A row of `MEDICATION_ORDER` is conceptually a row. Physically it is a sequence of bytes on storage, organized into *pages* (typically 8 or 16 kilobytes each), grouped into *extents*, stored in one or more *data files* that the database engine reads and writes. Those data files sit on a storage volume. That volume sits on one or more disks. Those disks sit somewhere physical: in a rack in the basement of the hospital, or in a hyperscaler's data center two states away.

        Every layer of that stack has trade-offs. The physical layer is where most of the cost lives and where most of the resilience lives, so understanding it is the difference between reading a vendor's architecture diagram with comprehension and reading it as marketing.

        Four physical-layer questions any informaticist should be able to ask:

        1. **Block storage or object storage?**
        2. **Solid-state or spinning disk, and is the hot data on the right tier?**
        3. **On-prem, cloud, or hybrid, and what is in scope for HIPAA?**
        4. **What is the backup, replication, and disaster-recovery posture?**

        We walk each one in turn.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Block versus object storage

        **Block storage** is the kind of storage a database wants. The storage volume looks to the operating system like a raw disk: you can write to any byte offset, you can update bytes in place, you can ask for the byte at offset 8,388,704 without reading anything else. Databases need this because they make small, scattered, low-latency updates: when the EHR writes a new flowsheet row, it is updating a single page in the middle of a 50-gigabyte data file. Block storage handles that natively. SAN and NAS are block (or block-like) storage architectures. In the cloud, the block-storage primitive is Amazon EBS or Azure Managed Disks or Google Persistent Disk.

        **Object storage** is the kind of storage a DICOM image or a clinical note PDF wants. The unit is an entire object: write the whole thing once, read the whole thing later, never update a byte in the middle. Objects are addressed by a key (a long string identifier) rather than by a filesystem path or a byte offset. Object storage scales cheaply to petabytes and is the default for archival and bulk-blob data. Amazon S3 is the canonical object store; Azure Blob Storage and Google Cloud Storage are the equivalents.

        Almost every clinical system uses both:

        - The operational EHR database lives on block storage.
        - DICOM images, scanned documents, ECG waveforms, audio recordings, and most note PDFs live on object storage.
        - Backups of the EHR database are usually written as object-storage blobs.

        | Use case | Storage type | Why |
        |---|---|---|
        | Operational EHR tables (`PATIENT`, `MEDICATION_ORDER`, ...) | Block | Small in-place updates, low latency |
        | DICOM studies in PACS | Object | Write once, read whole, scales cheaply |
        | Note PDFs, scanned documents | Object | Write once, read whole |
        | Database backups | Object | Immutable artifacts, low cost per TB |
        | Long-term analytics data lake (Track 03) | Object | Petabyte scale, parallel reads |
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Solid-state versus spinning disk, and the tiering question

        Three media show up in clinical storage architectures, with very different cost-per-terabyte and latency:

        | Media | Latency for a random 8 KB read | Cost per TB per year (order of magnitude) | Where it lives in the EHR |
        |---|---|---|---|
        | NVMe SSD | ~0.05 ms | $500 - $1,500 | Hot data: active EHR tables, recent encounters, the OLTP database itself |
        | SATA SSD or all-flash array | ~0.2 ms | $200 - $600 | Slightly warmer data: indexes, recent backups, recent PACS studies |
        | 7,200 RPM HDD | ~5 ms | $30 - $80 | Older PACS studies, archived records, secondary backups |
        | Tape (LTO-9) | seconds to minutes | $3 - $10 | Cold archives, regulatory retention, off-site DR copies |

        Two orders of magnitude separate hot SSD from cold HDD. Four orders separate hot SSD from tape. A 600-bed hospital cannot afford to keep its entire decade of PACS images on NVMe SSD, and it cannot afford to put the active EHR database on tape. The answer is **tiering**: hot data on fast storage, cold data on cheap storage, and an automated process (sometimes called *hierarchical storage management*, or HSM) that moves data between tiers based on age and access pattern.

        For a clinical informaticist, the practical questions are:

        - **What is the cutoff?** Most PACS systems keep two to five years of recent studies on flash and migrate older studies to cheaper tiers. The cutoff matters when a patient comes back after eight years and you need the old comparison study. Track 4 of this course walks the imaging side in detail.
        - **What is the recall latency for cold data?** Tape can take minutes to spool. Cold-tier cloud object storage (Amazon S3 Glacier Deep Archive, for example) can take hours to rehydrate. If your downtime tolerance for a comparison image is fifteen minutes, you cannot put it on tape.
        - **What is the recovery time objective for the database itself?** If the EHR database has to come back from an object-storage backup, the recovery is bottlenecked by the bandwidth between object storage and the recovery target. A 10 TB database from Amazon S3 at typical recovery speeds is hours, not minutes.

        Storage tiering is one of the most consequential places where finance, IT, and clinical operations have to agree on a trade. Cheaper tiers mean slower recall mean longer waits during a flare workup. Faster tiers mean a bigger storage bill. The right answer is the one where clinical operations has signed off on the recall latency for each tier.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### On-prem, cloud, or hybrid

        Twenty years ago every hospital ran its EHR on servers in its own basement. The big shift of the 2010s and 2020s is that an increasing share of clinical workloads now runs in cloud or hybrid configurations.

        **On-prem.** Servers and storage owned and operated by the hospital, sitting in a hospital-controlled data center. Total control. All compliance work happens inside the hospital's HIPAA-covered boundary. Costs are large upfront and largely fixed. Hardware refresh is the hospital's problem. Most legacy EHR deployments (especially older Epic and Cerner deployments) are still on-prem.

        **Cloud.** Workloads run in a hyperscaler's data center. The hyperscaler signs a Business Associate Agreement (BAA) with the hospital and operates within HIPAA scope for the services covered. Costs become operational expense rather than capital expense, and they scale up and down with workload. Epic introduced its hosted offering (Epic Hosted) in 2021; Oracle Health (Cerner) has been promoting its OCI-hosted offering since the Oracle acquisition in 2022.

        **Hybrid.** The most common production reality. The transactional EHR database may be on-prem; backups, PACS archives, analytics workloads, AI training pipelines, and disaster-recovery copies often run in the cloud. The boundary between on-prem and cloud is the place where most of the HIPAA work lives: every data path that crosses the boundary needs encryption in transit, the cloud destination needs encryption at rest, and the BAA needs to cover every service in the path.

        A short, blunt comparison:

        | Dimension | On-prem | Cloud | Hybrid |
        |---|---|---|---|
        | Up-front capital | High | None | Moderate |
        | Ongoing operating cost | Moderate, fixed | Variable, can be high | Both |
        | Elasticity (handle a spike) | Poor | Excellent | Decent for the cloud-side workloads |
        | Patch / refresh burden on the hospital | High | Low | Moderate |
        | Time-to-restore after a major incident | Depends on local DR | Depends on cloud DR | Depends on which side broke |
        | HIPAA scope | Hospital owns it | Hospital + BAA-covered cloud services | Both, with the boundary in the contract |
        | Vendor lock-in | Vendor-specific software, hospital-owned hardware | Vendor and cloud provider both | Both, with extra integration debt |

        The right answer for any given hospital is the one whose total cost, compliance posture, and reliability profile actually match how the institution operates. There is no universal answer. There is no universal wrong answer either.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Backup, replication, and disaster recovery

        Three terms that are easy to confuse and matter enormously when the EHR is down:

        - **Backup** is a point-in-time copy of the database, stored separately, intended to be restored if the live database is corrupted or destroyed. Backups are usually written every hour for transaction logs and every day for full snapshots, retained for a regulatory window (commonly seven years for clinical data).
        - **Replication** is a continuously updated mirror of the live database, kept on a second server or a second site. Replicas exist to keep the EHR available during a failure: if the primary server dies, traffic cuts over to the replica with seconds of data loss instead of hours.
        - **Disaster recovery** is the plan for what the hospital does when the entire primary site is unavailable. A second data center, a cloud DR target, documented runbooks, tested cutover procedures, recovery time objectives (RTO) and recovery point objectives (RPO) agreed with clinical operations.

        Two metrics any informaticist should know how to ask about:

        - **RPO** (recovery point objective): the maximum amount of data the hospital is willing to lose if a disaster strikes. An RPO of 5 minutes means transaction logs ship to the DR site every 5 minutes. An RPO of 24 hours means the DR site is a day behind.
        - **RTO** (recovery time objective): the maximum amount of time the hospital is willing to be without the EHR. An RTO of 30 minutes means the cutover plan has to bring an alternate environment up in 30 minutes. An RTO of 4 hours is much easier to engineer and much harder to live with at 3 AM.

        Both numbers cost money, and the RPO/RTO targets are clinical and operational decisions disguised as IT decisions. Clinical leadership needs to be in the conversation that sets them.
        """
    )
    return


@app.cell
def _(mo):
    storage_quiz = mo.ui.radio(
        options=[
            "Tier 1, NVMe SSD on-prem in the operational database server.",
            "Tier 2, all-flash SAN attached to the PACS server.",
            "Tier 3, 7,200 RPM HDD in a near-line array.",
            "Tier 4, object-storage cold-archive (Glacier Deep Archive equivalent).",
        ],
        label=(
            "**Ms. Reyes had a hand x-ray series in 2022 that you now want to compare to her new series this morning. "
            "The 2022 study is from her first rheumatology visit. The clinic radiologist wants the comparison view to load "
            "in under thirty seconds. Which storage tier should the 2022 study be on?**"
        ),
    )
    storage_quiz
    return (storage_quiz,)


@app.cell
def _(mo, storage_quiz):
    mo.stop(storage_quiz.value is None, mo.md("_Choose an answer._"))
    correct2 = storage_quiz.value.startswith("Tier 2,")

    if correct2:
        storage_msg = (
            "Right. Tier 2 (all-flash SAN attached to the PACS, or its cloud equivalent) is the right place "
            "for a several-year-old study that still has realistic clinical reuse. Tier 1 is wasted for cold "
            "imaging data, since the EHR's operational database needs that real estate. Tier 3 (spinning disk) "
            "can deliver the study but with multi-second latency that becomes painful when the radiologist is "
            "trying to scroll through a comparison. Tier 4 (cold-archive object storage) breaks the "
            "thirty-second SLA outright. The general PACS-tiering pattern is: recent studies on flash, "
            "three to five-year-old studies on warm tier (Tier 2), older studies on cheap tier with a documented "
            "recall latency that radiology has agreed to."
        )
    elif storage_quiz.value.startswith("Tier 1,"):
        storage_msg = (
            "Overkill. Tier 1 NVMe is the most expensive storage in the building. The operational EHR database "
            "needs it; a 4-year-old hand radiograph does not. Use Tier 1 for hot, frequently-mutated data and "
            "keep older PACS studies on warmer tiers like an all-flash SAN."
        )
    elif storage_quiz.value.startswith("Tier 3,"):
        storage_msg = (
            "Borderline. 7,200 RPM HDD can deliver the study, but multi-second seek latency makes the comparison "
            "view sluggish while a radiologist is trying to scroll. For a study that is realistically going to be "
            "compared against, Tier 2 (all-flash) is the conservative answer. Reserve Tier 3 for older studies "
            "that are recalled rarely."
        )
    else:
        storage_msg = (
            "Cold-archive object storage (Glacier Deep Archive and equivalents) typically has rehydration latency "
            "measured in hours, not seconds. It is the right tier for ten-year-old studies that you legally have to "
            "retain but practically never look at. A 2022 study with realistic clinical reuse needs a faster tier."
        )
    mo.callout(mo.md(storage_msg), kind="success" if correct2 else "warn")
    return


@app.cell
def _(mo, xref):
    xref.forward(
        from_course="05",
        to_course="07",
        topic="The same data, in a different shape, for a different job",
        body=(
            "We have been looking at the operational EHR: optimized for one patient at a time, indexed for "
            "the chart, tuned to insert quickly and update in place. The next track in this course (Track 03) "
            "introduces the *clinical data warehouse*, which is the same data laid out differently for "
            "population analytics. Course 07 (data wrangling and engineering) is where you actually "
            "manipulate that warehouse data: SQL from first principles, pandas, OMOP, graph databases. "
            "The mental shift starts here; the hands-on work is in course 07."
        ),
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Where this leaves you

        The operational EHR is structurally good at one thing: the chart. It is structurally bad at population queries, lossless export, and analytics. That is not a bug, it is the design discipline the operational system was built under. The schema, the indexing, the storage tiering, the backup posture are all downstream of that one priority.

        Track 02 picks up the historical question of how the messages between EHR systems got to where they are. Track 03 picks up the analytical-system question this track left hanging: where the population queries actually run.
        """
    )
    return


if __name__ == "__main__":
    app.run()