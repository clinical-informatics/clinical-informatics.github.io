"""Track 03: How computers represent and store data ("data at rest").

Plain English orientation. No code visible. Bits and bytes, then data
structures at concept level (tables, trees, graphs, key-value), then the
four file types most clinical data lives in (TXT, CSV, JSON, XML), then
the file vs database distinction, then relational concept, then OLTP vs
OLAP from the health-system standpoint. Closes with a pick-the-right-
format exercise across four clinical scenarios.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 03: How computers represent and store data

        ## Why this track exists.

        Most clinical informatics conversations turn on a question that sounds technical and is actually plain language: where is the data, and what shape is it in? When the EHR is slow on Tuesday morning, the right person to ask depends on whether the bottleneck is the database, the network, or the application. When a research request takes nine weeks, the reason usually lives in a difference between two storage systems that were designed for different jobs. When a vendor says their tool can ingest "any format," they mean it can read four of them.

        This track gives you the vocabulary for those conversations. No code, no schemas. The track names the four file types most of clinical data lives in, sketches the difference between a file and a database, and explains why every health system has two big databases instead of one.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## Bits and bytes.")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        At the bottom of every clinical system is the same substrate as every other computer system: **bits**. A bit is a single piece of information that can be in one of two states (0 or 1). Eight bits make a **byte**. A byte can hold one letter, or a small number, or a single piece of color information.

        The CRP value **36.2** is, in memory, a particular pattern of bits. The character string **"36.2"** is a *different* pattern of bits that displays the same way on a screen. They are not the same thing, and the difference shows up the first time someone tries to compute an average across a column where some cells stored the value as a number and others stored it as text. The average that comes back is wrong, no warning is raised, and the rest of the analysis is downstream of a number that nobody trusts.

        That distinction (number-as-number versus number-as-text) is the most common single source of quietly wrong clinical analyses. The deeper Course 02 (data literacy) builds the muscle around it; for now hold the idea that the same value can be stored in more than one way, and the way matters.

        Everything else in this track is the field's attempt to organize those bits into shapes that match the clinical world.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Data structures at concept level.

        Four shapes do most of the work. Each one matches a part of clinical reality.

        Click each one to read what it looks like and what clinical data lives in it.
        """
    )
    return


@app.cell
def _(mo):
    shape_picker = mo.ui.radio(
        options=[
            "Tables: rows and columns.",
            "Trees: parent-child hierarchies.",
            "Graphs: networks of relationships.",
            "Key-value: a dictionary you look things up in.",
        ],
        label="Pick a data structure.",
        value="Tables: rows and columns.",
    )
    shape_picker
    return (shape_picker,)


@app.cell
def _(mo, shape_picker):
    if shape_picker.value is None:
        shape_view = mo.md("")
    elif shape_picker.value.startswith("Tables"):
        shape_view = mo.callout(
            mo.md(
                "**Tables.** A grid of rows and columns. Every row is one record; every column "
                "is one fact about each record. Ms. Reyes's lab history is a table: one row per "
                "lab result, with columns for the date, the test name, the value, the unit, and "
                "the reference range. The vast majority of clinical data the field handles starts "
                "or ends in a table at some point. SQL is the language built around querying "
                "tables; spreadsheets are tables; the EHR's underlying database is a collection "
                "of tables with millions of rows each. When a piece of clinical data feels "
                "naturally rectangular, it usually is."
            ),
            kind="info",
        )
    elif shape_picker.value.startswith("Trees"):
        shape_view = mo.callout(
            mo.md(
                "**Trees.** A parent-child hierarchy. The clinical example everyone meets first "
                "is the **problem list**, which is built on top of SNOMED CT: the concept "
                "*rheumatoid arthritis* sits under *inflammatory arthropathy*, which sits under "
                "*arthropathy*, which sits under *disorder of joint*, all the way up to *clinical "
                "finding*. ICD-10-CM is also tree-shaped (M06.9 *Rheumatoid arthritis, unspecified* "
                "sits under M06 *Other rheumatoid arthritis*, which sits under M05-M14 "
                "*Inflammatory polyarthropathies*). Trees show up anywhere the field needs to ask "
                "*is this concept a kind of that concept*: terminology systems, anatomical "
                "hierarchies, the organizational structure of a health system."
            ),
            kind="info",
        )
    elif shape_picker.value.startswith("Graphs"):
        shape_view = mo.callout(
            mo.md(
                "**Graphs.** A network of relationships, where the relationships are as important "
                "as the things being related. The classic clinical example is a **drug-interaction "
                "network**: every medication is a node; every known interaction is an edge between "
                "two nodes; the question *does this combination interact* becomes a traversal "
                "through the graph. Another example is a **knowledge graph** of clinical concepts: "
                "*rheumatoid arthritis* connects to *methotrexate* through the relationship "
                "*may-be-treated-with* and to *anti-CCP* through *commonly-associated-finding*. "
                "Graphs handle problems where the shape of the relationships matters and a table "
                "would force you to pick an arbitrary direction. Course 07 Track 5 of the "
                "curriculum returns to graphs at the working level."
            ),
            kind="info",
        )
    else:
        shape_view = mo.callout(
            mo.md(
                "**Key-value.** A dictionary. You give the system a key (a name or identifier) "
                "and it gives you back a value (the thing the key points to). Clinical examples: "
                "a **FHIR Bundle's index** lets you look up *Patient/123* and get back the patient "
                "resource directly without scanning a table. A **session cache** in MyChart lets "
                "the page look up *this user's last viewed lab* without a database query. The "
                "shape is simple and very fast for problems where you know exactly what you "
                "are looking for. Key-value stores back most of the modern web."
            ),
            kind="info",
        )
    shape_view
    return (shape_view,)


@app.cell
def _(mo):
    mo.md(
        r"""
        The four shapes are not exclusive. A FHIR Bundle is a key-value structure on the outside (each resource has an ID you can look up) that contains tree-shaped resources (the Patient resource has nested fields), some of which contain table-shaped collections (Observation components), some of which reference other resources to form a graph (the Observation references the Patient who references the Practitioner). Real clinical systems compose all four.

        The point of naming the shapes is not to taxonomize. It is to make the next two questions natural: *what shape is this clinical thing*, and *what storage tool fits that shape*.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## File types.")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Most clinical data, once it leaves the EHR's internal database, lives in one of four file types. The first thing to notice is that this is fewer than you would expect. Every vendor brochure mentions a dozen formats; in practice you will meet these four constantly and the others rarely.

        Pick each one to read the one-screen version of what it is, what it is for, where it wins, and where it loses.
        """
    )
    return


@app.cell
def _(mo):
    file_picker = mo.ui.radio(
        options=[
            "TXT: plain text.",
            "CSV: comma-separated values.",
            "JSON: nested key-value pairs.",
            "XML: nested tagged elements.",
        ],
        label="Pick a file type.",
        value="TXT: plain text.",
    )
    file_picker
    return (file_picker,)


@app.cell
def _(file_picker, mo):
    if file_picker.value is None:
        file_view = mo.md("")
    elif file_picker.value.startswith("TXT"):
        file_view = mo.callout(
            mo.md(
                "**TXT.** Plain text. No structure beyond the line break. A clinical example is "
                "any free-text note: a discharge summary, a progress note, the body of an email. "
                "A small TXT file in a clinical workflow looks like:\n\n"
                "```\nDate: 2024-01-08\nPatient: Reyes, Elena (ER-001)\n\n"
                "S: Pt c/o increased AM stiffness x 3 wks, ~45 min duration. \n"
                "   Hands and feet involved. Denies fever, weight loss, new rashes.\n"
                "O: CRP 36.2, ESR 51. DAS28 4.3. 3 swollen MCPs L > R.\n"
                "A: Likely moderate flare on stable biologic regimen.\n"
                "P: Increase MTX to 25 mg SC weekly, recheck CRP in 6 wks.\n```\n\n"
                "**Strengths.** Universally readable. Every editor opens it. Email and the file "
                "system know how to handle it. Diff tools work cleanly on it.\n\n"
                "**Weaknesses.** No machine-readable structure. Pulling *CRP value* out of the "
                "block above requires natural language processing or a brittle regex. Two notes "
                "with the same content but different formatting are not comparable without work.\n\n"
                "**Where it shows up clinically.** Clinical notes (until they are structured), "
                "README files, log output, configuration files, and the body of nearly every "
                "FHIR or CDA payload before it is parsed into a richer format."
            ),
            kind="info",
        )
    elif file_picker.value.startswith("CSV"):
        file_view = mo.callout(
            mo.md(
                "**CSV.** Comma-separated values. The lingua franca of tabular data exchange. "
                "A small CSV from Ms. Reyes's lab history looks like:\n\n"
                "```\nspecimen_date,test_name,value,unit\n"
                "2024-01-08,C-reactive protein,36.2,mg/L\n"
                "2024-01-08,Erythrocyte sedimentation rate,51,mm/h\n"
                "2023-11-13,C-reactive protein,33.4,mg/L\n"
                "2023-11-13,Hemoglobin,11.8,g/dL\n```\n\n"
                "**Strengths.** Trivial to read and write. Every tool supports it (Excel, R, "
                "Python, relational databases, statistics packages). Easy to inspect by eye. The "
                "format itself is documented in two sentences.\n\n"
                "**Weaknesses.** Cannot represent nesting (a patient with multiple addresses "
                "needs a separate addresses CSV). The format has no built-in type information: "
                "the column says *value*, but whether that value is a number, a string, or a "
                "date is up to the reader to figure out. Commas inside a field require quoting "
                "rules that different tools sometimes interpret differently.\n\n"
                "**Where it shows up clinically.** Every data export from an EHR with a *download "
                "as CSV* button. Most claims data exchanges. The flat-file export of any registry. "
                "Many quality measure submissions. CSV is the format that will not go away because "
                "everyone can read it without thinking."
            ),
            kind="info",
        )
    elif file_picker.value.startswith("JSON"):
        file_view = mo.callout(
            mo.md(
                "**JSON.** Nested key-value pairs. The web's data format. A small clinical JSON "
                "looks like:\n\n"
                "```\n{\n  \"resourceType\": \"Observation\",\n  \"id\": \"crp-2024-01-08\",\n"
                "  \"status\": \"final\",\n  \"code\": {\n    \"coding\": [\n      {\n"
                "        \"system\": \"http://loinc.org\",\n        \"code\": \"1988-5\",\n"
                "        \"display\": \"C-reactive protein\"\n      }\n    ]\n  },\n"
                "  \"subject\": { \"reference\": \"Patient/ER-001\" },\n"
                "  \"effectiveDateTime\": \"2024-01-08T07:42:00Z\",\n"
                "  \"valueQuantity\": { \"value\": 36.2, \"unit\": \"mg/L\" }\n}\n```\n\n"
                "**Strengths.** Handles nested structure naturally (a value plus its unit plus "
                "its coding system plus its patient reference, all in one object). Lightweight. "
                "Every modern programming language has built-in support. Human-readable enough "
                "to debug by eye. The format every modern API speaks.\n\n"
                "**Weaknesses.** The format itself does not enforce a schema: a JSON document "
                "either parses or does not, but it cannot tell you that the *valueQuantity* "
                "field should always have both a value and a unit. Schema enforcement is added "
                "by external tools (FHIR profiles, JSON Schema).\n\n"
                "**Where it shows up clinically.** FHIR's primary serialization. Almost every "
                "modern clinical API request and response. Most third-party patient-facing app "
                "integrations. The format that won most new clinical data work in the 2010s and "
                "2020s because the web won."
            ),
            kind="info",
        )
    else:
        file_view = mo.callout(
            mo.md(
                "**XML.** Nested elements wrapped in verbose tags. The older interoperability "
                "standard. A small CDA snippet looks like:\n\n"
                "```\n<observation classCode=\"OBS\" moodCode=\"EVN\">\n"
                "  <code code=\"1988-5\" codeSystem=\"2.16.840.1.113883.6.1\"\n"
                "        displayName=\"C-reactive protein\"/>\n"
                "  <effectiveTime value=\"20240108074200\"/>\n"
                "  <value xsi:type=\"PQ\" value=\"36.2\" unit=\"mg/L\"/>\n"
                "</observation>\n```\n\n"
                "**Strengths.** Strong schema validation (XML Schema can enforce required "
                "elements, types, value sets). Namespaces and extensions are first-class. "
                "Document-oriented use cases (the entire HL7 CDA standard, parts of HL7 v3, "
                "older EHR exports) are XML-native.\n\n"
                "**Weaknesses.** Heavier than JSON for the same content. Less ergonomic for "
                "modern web APIs. The verbosity is real: a CDA document for a single visit can "
                "be tens of thousands of characters of tags around a few hundred characters of "
                "content.\n\n"
                "**Where it shows up clinically.** Anywhere CDA or HL7 v3 is in use (which is "
                "many places, because HITECH-era exchanges were built on CDA). Most CMS quality "
                "submissions until very recently. ONC's older certification artifacts. Some "
                "lab and imaging integrations. XML is not going away; it is no longer the "
                "first choice for new work."
            ),
            kind="info",
        )
    file_view
    return (file_view,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The honest comparison.

        - **JSON won most new work because the web won.** Every modern API, every patient-facing app, every FHIR endpoint defaults to JSON. If you are building something new in 2025, the default is JSON.
        - **XML still appears anywhere CDA or older HL7 is in use.** That is not a small number of places. The HITECH-era exchanges were built on it and are still running.
        - **CSV is forever.** Nothing has displaced it for the *give me a table I can open in Excel* use case, and nothing will.
        - **TXT is for things humans read.** When the structure does not matter, TXT is the right answer. Most of clinical text (the notes themselves) is still TXT under whatever wrapper carries it.

        The mistake to avoid is treating the format as the substance. The same CRP value of 36.2 mg/L can be carried in any of the four formats above without losing its clinical meaning. The format is a packaging choice. Different packages travel through different pipes; the pipe determines the package more often than the content does.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## File vs database.

        A **file** is a single document that lives somewhere on disk. You open it, you read it, you save it back. Files are good at the things you would expect: storing a single complete object, moving it around, archiving it, emailing it.

        A **database** is a system that holds many records and supports asking questions across them. Where files give you persistence (the data survives a system restart), databases give you three additional things files do not.

        - **Constraints.** A database can enforce that a *Patient* must have a date of birth, that a *Medication* must have a code from a controlled vocabulary, that a *Lab Result* cannot have a unit of *mg/dL* when the test is CRP. A folder full of CSVs cannot enforce any of those.
        - **Concurrency.** A database can have a hundred clinicians writing notes at the same time without anyone overwriting anyone else. A single CSV file shared on a network drive cannot.
        - **Query optimization.** A database can answer *show me all CRPs above 30 in patients with RA over the last year* in milliseconds across millions of rows. The same question against a folder of CSVs requires loading every file into memory and scanning each one.

        Every EHR runs on a database. Every clinical data warehouse is a database. Every registry of meaningful size is a database. Files are how data moves *between* databases or *between* humans; databases are where the data actually lives during the time it is in use.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Relational databases.

        The default kind of database for clinical work, and for most other work, is a **relational database**. It is a database whose contents are organized as tables (the *relations* in *relational*), with **keys** that link rows in one table to rows in another.

        A relational EHR database has a *Patient* table with one row per patient. It has an *Encounter* table with one row per visit, where each encounter row carries a *Patient_ID* that points back to the patient. It has an *Observation* table with one row per lab result, where each observation carries an *Encounter_ID* that points back to the encounter and a *Patient_ID* that points back to the patient.

        The pointers are what *relational* means. They are why pulling all of Ms. Reyes's labs in 2024 is one short query (start at her row in *Patient*, follow the keys outward through *Encounter* and *Observation*, keep what falls inside the date range) instead of an open-ended search.

        Course 02 Track 5 of the curriculum returns to relational databases at the concept level. Course 07 Track 1 returns to them in SQL, the language that queries them. For Course 0 it is enough to name the shape: tables linked by keys, queryable at speed.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## OLTP vs OLAP.")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Every health system of any size runs at least two big databases. They look similar from a distance and are designed for opposite jobs. The distinction has a name in the field, **OLTP vs OLAP**, and naming it is what unlocks why every health system has both and why the rules for talking to each are different.

        - **OLTP.** Online **Transaction** Processing. The database underneath the EHR. It is built for clinical operations: write the order now, read the lab now, file the note now, page the on-call now. Each operation touches a small number of records and has to return immediately. The database is optimized for **many small writes and reads, with single-record access patterns**. It is the system that is up at 2 a.m. when the resident pages the cardiology fellow and pulls up the EKG.
        - **OLAP.** Online **Analytical** Processing. The clinical data warehouse, sitting alongside the EHR. It is built for analytic queries: show me ten years of CRP across the entire RA cohort, compute readmission rates by service for the last quarter, count how many patients on a biologic also had a serious infection in the next year. Each query touches millions of records and is allowed to take seconds or minutes. The database is optimized for **few large reads, with aggregation across many records**.

        Why two databases? Because the optimizations conflict.

        - An OLTP database is indexed and structured to make *find me Ms. Reyes's most recent CRP* a millisecond operation. The same structure makes *average all CRPs across every patient ever* a forty-minute operation that locks up the database for clinical users while it runs.
        - An OLAP database is structured to make the cohort query fast. The same structure makes individual-patient lookup slower, and the database is usually a day or so out of date because it gets refreshed overnight, which would be unacceptable for clinical work.

        **The two systems exist because the two jobs cannot share one database.** Asking a research question against the OLTP database during a busy weekday is what slows the EHR for everyone else on the floor. Asking a clinical question against the OLAP database is what gets you yesterday's labs and last week's medications.

        Course 05 Track 3 of the curriculum is the deep dive on clinical data warehouses. For Course 0, the takeaway is that when somebody says *the data warehouse* and somebody else says *the EHR*, they are not talking about the same database, and the difference is not casual. It is the design of the field's storage layer.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Database languages.

        Most relational databases speak **SQL** (Structured Query Language). SQL is by far the dominant language for asking questions of structured clinical data, and Course 07 Track 1 of the curriculum builds it from first principles using Ms. Reyes's records. For Course 0 it is enough to know that the language exists and is the default.

        Other query languages exist for other shapes:

        - **NoSQL databases** (a category that includes document stores, key-value stores, and graph databases) have their own query languages, each adapted to the shape of data they hold.
        - **FHIR has its own search API**, which looks like a URL with parameters rather than a SQL statement. The same question (*give me CRPs for patient X in the last year*) is asked differently depending on whether you are asking SQL against a CDW or FHIR against an EHR endpoint.
        - **CQL (Clinical Quality Language)** is a domain-specific language for expressing clinical logic against FHIR data, used heavily for quality measures and clinical decision support. Course 12 Track 2 returns to it.

        The plurality of query languages is not chaos. Each one fits a specific shape of data. The chooser is rarely *which language do I prefer*; it is *what shape is the data in, and what language is the right one for that shape*.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## One more.")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Pick the right format.

        Four clinical artifacts. Pick the format that best fits each one. There is sometimes more than one defensible answer; the explanation will tell you the trade-off when there is.
        """
    )
    return


@app.cell
def _(mo):
    options_list = [
        "TXT (plain text)",
        "CSV (rows and columns)",
        "JSON (nested key-value)",
        "XML (nested tagged elements)",
        "A relational database (rows and tables, queryable)",
    ]
    discharge_pick = mo.ui.radio(
        options=options_list,
        label=(
            "1. A discharge summary the inpatient team writes for the patient's PCP. "
            "It is mostly narrative (history, hospital course, plan), with a short structured "
            "medication list at the end. The PCP needs to read it on his phone or print it."
        ),
    )
    discharge_pick
    return discharge_pick, options_list


@app.cell
def _(discharge_pick, mo):
    if discharge_pick.value is None:
        d_resp = mo.md("")
    elif discharge_pick.value.startswith("TXT"):
        d_resp = mo.callout(
            mo.md(
                "**Reasonable in practice.** A discharge summary is mostly narrative. TXT (or a "
                "PDF rendering of TXT-equivalent content) is what the PCP usually reads. The "
                "downside is that the structured medication list at the end is harder to extract "
                "back out programmatically, which is why many health systems also ship a parallel "
                "structured representation (a FHIR DocumentReference with the narrative attached) "
                "alongside the human-readable copy. The clinical artifact the PCP reads on his "
                "phone is TXT-equivalent. The artifact the receiving EHR ingests is something else."
            ),
            kind="success",
        )
    elif discharge_pick.value.startswith("XML"):
        d_resp = mo.callout(
            mo.md(
                "**Historically correct.** A Continuity of Care Document, the format most "
                "discharge summaries shipped in during the HITECH era, is XML. The PCP did not "
                "read the XML; the EHR rendered it as narrative on the screen. So XML is right "
                "for the over-the-wire format and not right for what the PCP actually reads. "
                "Either answer can be defended depending on whose problem you are solving."
            ),
            kind="success",
        )
    elif discharge_pick.value.startswith("JSON"):
        d_resp = mo.callout(
            mo.md(
                "**Reasonable for the new world.** A FHIR DocumentReference containing a "
                "narrative discharge summary plus a structured medication list is JSON. That is "
                "what most modern systems would ship. The PCP still reads a rendered version, "
                "not the raw JSON. So the answer depends on whether the question is about what "
                "the data is in flight or what the human reads."
            ),
            kind="success",
        )
    else:
        d_resp = mo.callout(
            mo.md(
                "**Not the typical choice.** CSV is awkward for a narrative document; you can "
                "cram the text into a single cell, but the structure does not fit. A relational "
                "database is the destination after the document is parsed; it is not the format "
                "for shipping the document itself. TXT, JSON, or XML are the realistic choices "
                "depending on whether you are answering for the human reader or for the receiving "
                "system."
            ),
            kind="warn",
        )
    d_resp
    return (d_resp,)


@app.cell
def _(mo, options_list):
    lab_pick = mo.ui.radio(
        options=options_list,
        label=(
            "2. The single lab result for Ms. Reyes's CRP on 2024-01-08, traveling from the lab's "
            "analyzer into the EHR, with the LOINC code, the value, the unit, the timestamp, and "
            "the patient reference attached."
        ),
    )
    lab_pick
    return (lab_pick,)


@app.cell
def _(lab_pick, mo):
    if lab_pick.value is None:
        l_resp = mo.md("")
    elif lab_pick.value.startswith("JSON"):
        l_resp = mo.callout(
            mo.md(
                "**Yes, for any modern integration.** A FHIR Observation resource is the right "
                "shape: nested fields for the value plus the unit plus the coding system plus the "
                "patient reference, all in one object. Lab analyzers built before the FHIR era "
                "would have emitted HL7 v2 (which is its own pipe-delimited format, not in this "
                "list), but the modern answer is JSON over a FHIR endpoint."
            ),
            kind="success",
        )
    elif lab_pick.value.startswith("XML"):
        l_resp = mo.callout(
            mo.md(
                "**Possible, but not the modern default.** An HL7 v3 observation or a CDA "
                "snippet would be XML. Newer integrations skip straight to FHIR JSON for the same "
                "content."
            ),
            kind="success",
        )
    elif lab_pick.value.startswith("CSV"):
        l_resp = mo.callout(
            mo.md(
                "**Not for a single in-flight result.** CSV is great for batches of lab results "
                "in a flat export. For a single result moving from the analyzer into the EHR in "
                "real time, with rich metadata attached, you want the nesting that JSON or XML "
                "give you."
            ),
            kind="warn",
        )
    elif lab_pick.value.startswith("TXT"):
        l_resp = mo.callout(
            mo.md(
                "**No.** TXT has no structure, and this artifact is heavily structured (value, "
                "unit, LOINC, patient reference, timestamp). You would lose the structure on the "
                "way in and have to reconstruct it on the other side."
            ),
            kind="warn",
        )
    else:
        l_resp = mo.callout(
            mo.md(
                "**Where it ends up, not the format it travels in.** The result will live in the "
                "EHR's relational database after ingestion. The question is the format on the "
                "wire, and that is JSON (FHIR) for a modern integration."
            ),
            kind="warn",
        )
    l_resp
    return (l_resp,)


@app.cell
def _(mo, options_list):
    bundle_pick = mo.ui.radio(
        options=options_list,
        label=(
            "3. A complete FHIR Bundle containing Ms. Reyes's patient resource, her conditions, "
            "her medications, her lab results, her encounters, and the referenced practitioners, sent "
            "as a single payload to a research collaborator who has agreed to receive it."
        ),
    )
    bundle_pick
    return (bundle_pick,)


@app.cell
def _(bundle_pick, mo):
    if bundle_pick.value is None:
        b_resp = mo.md("")
    elif bundle_pick.value.startswith("JSON"):
        b_resp = mo.callout(
            mo.md(
                "**Yes.** FHIR's primary serialization is JSON, and a Bundle is the resource type "
                "designed exactly for *send me everything about this patient in one document*. "
                "XML serialization of FHIR also exists for sites that need it; JSON is the "
                "default."
            ),
            kind="success",
        )
    elif bundle_pick.value.startswith("XML"):
        b_resp = mo.callout(
            mo.md(
                "**Allowed by the spec.** FHIR supports an XML serialization. In practice almost "
                "all modern recipients prefer JSON. If your collaborator's tooling is XML-native "
                "(some research informatics pipelines still are), the XML serialization is a "
                "valid choice."
            ),
            kind="success",
        )
    elif bundle_pick.value.startswith("CSV"):
        b_resp = mo.callout(
            mo.md(
                "**Wrong shape.** A Bundle is a nested structure with resources that reference "
                "each other. CSV cannot represent the nesting or the references without breaking "
                "it into many tables, which loses the *one document* property the recipient is "
                "expecting."
            ),
            kind="warn",
        )
    elif bundle_pick.value.startswith("TXT"):
        b_resp = mo.callout(
            mo.md(
                "**No.** TXT loses all structure. The recipient asked for a Bundle, which is by "
                "definition a structured artifact."
            ),
            kind="warn",
        )
    else:
        b_resp = mo.callout(
            mo.md(
                "**Not for sending a single payload.** A database is something you query; the "
                "collaborator does not get query access to your EHR. What you send them is a "
                "Bundle, which is JSON (or XML)."
            ),
            kind="warn",
        )
    b_resp
    return (b_resp,)


@app.cell
def _(mo, options_list):
    claims_pick = mo.ui.radio(
        options=options_list,
        label=(
            "4. A year of claims data for the entire rheumatology practice (about 12,000 claims), "
            "shipped from the health system to a population-health analytics vendor who will "
            "compute cost and utilization metrics across the cohort."
        ),
    )
    claims_pick
    return (claims_pick,)


@app.cell
def _(claims_pick, mo):
    if claims_pick.value is None:
        c_resp = mo.md("")
    elif claims_pick.value.startswith("CSV"):
        c_resp = mo.callout(
            mo.md(
                "**Yes, for the typical workflow.** A year of claims is a large flat table: one "
                "row per claim, with columns for the patient, the date of service, the CPT code, "
                "the diagnosis codes, the charged amount, the paid amount, and so on. CSV is the "
                "format every analytics tool will ingest without ceremony. The vendor will load "
                "it into their own database on receipt; the format on the wire is CSV."
            ),
            kind="success",
        )
    elif claims_pick.value.startswith("A relational"):
        c_resp = mo.callout(
            mo.md(
                "**Where it ends up, not the format it travels in.** The analytics vendor will "
                "load the data into their own relational database. The wire format is almost "
                "always CSV (or a closely related flat-file format like Parquet for larger "
                "volumes)."
            ),
            kind="warn",
        )
    elif claims_pick.value.startswith("JSON"):
        c_resp = mo.callout(
            mo.md(
                "**Possible, not typical.** You could ship the same data as JSON, with one "
                "object per claim. In practice claims data is so rectangular that CSV is the "
                "default and JSON is overkill. The bigger volumes also push toward CSV's denser "
                "encoding."
            ),
            kind="warn",
        )
    elif claims_pick.value.startswith("XML"):
        c_resp = mo.callout(
            mo.md(
                "**Possible historically, not typical now.** Some older claims exchanges used "
                "XML. Newer analytics integrations default to CSV (or Parquet)."
            ),
            kind="warn",
        )
    else:
        c_resp = mo.callout(
            mo.md(
                "**No.** TXT throws away the columnar structure that makes claims data analyzable. "
                "The vendor would need to parse it back out, which is what CSV gives them for "
                "free."
            ),
            kind="warn",
        )
    c_resp
    return (c_resp,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The pattern under the answers.

        Two questions usually decide the format.

        - **How structured is the content, and how nested is the structure?** Flat tables (claims, bulk labs) want CSV. Single rich objects with nested fields (a FHIR Observation, a FHIR Bundle) want JSON or XML. Free narrative wants TXT.
        - **Who is reading it and what tools do they already speak?** If the receiver is a human, render to TXT or PDF. If the receiver is a modern API, JSON. If the receiver runs on the older HL7 toolchain, XML. If the receiver is a spreadsheet jockey, CSV.

        The format almost never gets chosen because it is theoretically best for the content. It gets chosen because it is what the pipe between the two systems already carries. Most of the format-choice arguments in clinical informatics turn out to be arguments about pipes, not about formats.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What you did in this track.

        - Named the four data structures (tables, trees, graphs, key-value) and matched each one to the kind of clinical data it holds.
        - Covered the four file types (TXT, CSV, JSON, XML) the field actually uses, with a one-screen example of each and an honest sense of where each one wins.
        - Distinguished file from database, and named the three things a database buys you that a folder of files does not (constraints, concurrency, query optimization).
        - Sketched a relational database as tables linked by keys.
        - Named **OLTP vs OLAP**: the EHR is transactional, the CDW is analytical, the two databases exist because the two jobs cannot share one.
        - Picked the right format for four clinical artifacts and noticed the pattern in the answers.

        ## What's next.

        **Track 04: How computers move data.** The data at rest in this track has to move between systems to be useful. The next track names the network architecture clinical data travels through: client-server, the hospital LAN behind the firewall, the public internet, HTTP and REST and APIs at concept level, on-prem versus cloud, and the security boundaries the field treats as serious.
        """
    )
    return


if __name__ == "__main__":
    app.run()
