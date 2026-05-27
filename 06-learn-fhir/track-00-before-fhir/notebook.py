"""Track 0: Before FHIR (no code).

Four foundational ideas before any FHIR vocabulary: data has three
shapes (spreadsheet, database, document); the web is three boring
agreements layered together (HTTP, REST, JSON); healthcare data
standards layer rather than replace each other (HL7 v2, CDA, FHIR);
and "interoperability" is at least five distinct layers, not one
thing.

The notebook closes with a diagnosis. Ms. Elena Reyes has two
synthetic EHR exports in this curriculum: one shaped like Epic
Clarity, one shaped like Cerner Millennium. The exercise presents four
real differences between them and asks for a classification of each.
The track closes with a layer-naming habit for any "the two systems
can't talk" complaint: name, with specificity, which layer the
problem is living at.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    return mo, pd


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 0: Before FHIR (no code)

        ## Two exports. Same patient. Same morning.

        Ms. Elena Reyes is the curriculum's running patient: 52, seropositive RA on MTX plus adalimumab, four years into therapy. She has one record in real life; she has two in this curriculum, because her data has been exported from two different EHR vendors.

        One export is shaped like Epic Clarity. The other is shaped like Cerner Millennium. Same patient, same recent visit, same lab values, same medications. The exports look almost nothing alike. Below is the way each one represents her name and her MRN.
        """
    )
    return


@app.cell
def _(mo):
    epic_snippet = mo.md(
        r"""
        **Epic-style export (excerpt).**

        ```json
        "PAT_ENC": {
          "PAT_ID":         "Z9847562",
          "PAT_MRN_ID":     "ER-001",
          "PAT_NAME":       "Reyes, Elena Maria",
          "PAT_FIRST_NAME": "Elena",
          "PAT_LAST_NAME":  "Reyes",
          "BIRTH_DATE":     "1974-02-09",
          "SEX_C":          2,
          "SEX_C_NAME":     "Female"
        }
        ```
        """
    )

    cerner_snippet = mo.md(
        r"""
        **Cerner-style export (excerpt).**

        ```json
        "person": {
          "person_id":   78463921,
          "name_last":   "Reyes",
          "name_first":  "Elena",
          "name_middle": "Maria",
          "birth_dt_tm": "1974-02-09T00:00:00",
          "sex_cd":      362,
          "sex_disp":    "Female"
        },
        "person_alias": [
          {"alias_pool_disp": "MRN",       "alias": "ER-001"},
          {"alias_pool_disp": "Person ID", "alias": "78463921"}
        ]
        ```
        """
    )
    mo.hstack([epic_snippet, cerner_snippet], widths=[1, 1])
    return cerner_snippet, epic_snippet


@app.cell
def _(mo):
    mo.md(
        r"""
        Take ten seconds and look at the two blocks. The same facts are in both. They are written in different shapes, different field names, and different code values, and that is before either record has left the vendor's database. The work of this track is making sense of why.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## What's the same fact, written differently?")
    return


@app.cell
def _(mo):
    matchups = mo.ui.multiselect(
        options=[
            "Epic `PAT_MRN_ID` is the same fact as Cerner `person_alias[].alias` where `alias_pool_disp` is 'MRN'",
            "Epic `BIRTH_DATE` is the same fact as Cerner `birth_dt_tm`",
            "Epic `SEX_C_NAME` is the same fact as Cerner `sex_disp`",
            "Epic `SEX_C` (value 2) is the same code as Cerner `sex_cd` (value 362)",
            "Epic `PAT_ID` is the same fact as Cerner `person_id`",
            "Epic `PAT_NAME` is the same field as Cerner `name_last`",
        ],
        label="Which of the pairings above are storing the same fact about Ms. Reyes? Pick all that apply.",
    )
    matchups
    return (matchups,)


@app.cell
def _(matchups, mo):
    chosen = set(matchups.value or [])
    same_fact = {
        "Epic `PAT_MRN_ID` is the same fact as Cerner `person_alias[].alias` where `alias_pool_disp` is 'MRN'",
        "Epic `BIRTH_DATE` is the same fact as Cerner `birth_dt_tm`",
        "Epic `SEX_C_NAME` is the same fact as Cerner `sex_disp`",
        "Epic `PAT_ID` is the same fact as Cerner `person_id`",
    }
    not_same_fact = {
        "Epic `SEX_C` (value 2) is the same code as Cerner `sex_cd` (value 362)",
        "Epic `PAT_NAME` is the same field as Cerner `name_last`",
    }

    if not chosen:
        feedback = mo.callout(
            mo.md("_Pick at least one. The exercise is to notice which fields hold the same fact even when their names disagree._"),
            kind="neutral",
        )
    elif chosen == same_fact:
        feedback = mo.callout(
            mo.md(
                "**Right.** Four pairs name the same fact in different field names:\n\n"
                "- `PAT_MRN_ID` and `person_alias[].alias` (MRN) both equal `ER-001`.\n"
                "- `BIRTH_DATE` and `birth_dt_tm` both refer to 1974-02-09 (Cerner adds a midnight timestamp).\n"
                "- `SEX_C_NAME` and `sex_disp` both equal 'Female'.\n"
                "- `PAT_ID` and `person_id` are both the vendor's internal patient identifier (just different numbers because the two vendors assign their own).\n\n"
                "The other two are traps. `SEX_C = 2` (Epic) and `sex_cd = 362` (Cerner) are **different codes** for the same concept, each from a vendor-specific code system. The strings 'Female' agree; the codes do not. And `PAT_NAME` is a single full-name string in Epic, not the same field as Cerner's `name_last`, which only holds the surname."
            ),
            kind="success",
        )
    else:
        missing = same_fact - chosen
        extras = chosen & not_same_fact
        parts = ["**Close.** A few notes:"]
        if missing:
            parts.append("\nThese pairs **do** store the same fact and should be picked:")
            for m in sorted(missing):
                parts.append(f"\n- {m}")
        if extras:
            parts.append("\nThese pairs **do not** match cleanly and should be unchecked:")
            for e in sorted(extras):
                parts.append(f"\n- {e}")
            parts.append(
                "\n\n`SEX_C` = 2 in Epic and `sex_cd` = 362 in Cerner are different vendor codes that happen to map to the same display string 'Female'. The strings agree; the codes don't. `PAT_NAME` in Epic is a single full-name string, not the same field as Cerner's `name_last`, which only holds the surname."
            )
        feedback = mo.callout(mo.md("".join(parts)), kind="warn")
    feedback
    return chosen, feedback, not_same_fact, same_fact


@app.cell
def _(mo):
    mo.md(
        r"""
        Hold that example in mind. Six fields, four real matches, two near-misses. Even at the level of a patient's name and sex, two production EHR vendors store the same facts under different names, with different code values, in different structural shapes. This is before we have asked about anything as complicated as a lab result.

        The next four sections are the foundation underneath the rest of the FHIR course. None of them mention a single FHIR resource. They are the ideas you need first.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Idea 1. Data has three shapes.

        When someone says "the patient's data," they can mean three different things. The difference is load-bearing for the rest of this course.

        - **Spreadsheet shape.** One fact per cell, every row the same columns. Good at homogeneous rows; terrible at attaching different kinds of fact to the same row.
        - **Database shape.** Several tables, each holding a different kind of row, linked by stable identifiers. Good at heterogeneous related facts; terrible at moving the data out without a lossy export.
        - **Document shape.** A single self-contained record with internal structure. Good at crossing system boundaries; not where you do bulk analytics.

        Ms. Reyes's most recent CRP, 21.4 mg/L drawn 2026-02-10 at the rheumatology clinic, can be written in all three shapes. Toggle below.
        """
    )
    return


@app.cell
def _(mo):
    shape_pick = mo.ui.radio(
        options=["Spreadsheet shape", "Database shape", "Document shape"],
        value="Spreadsheet shape",
        label="Show this CRP value in which shape?",
    )
    shape_pick
    return (shape_pick,)


@app.cell
def _(mo, shape_pick):
    if shape_pick.value == "Spreadsheet shape":
        body = mo.md(
            r"""
**Spreadsheet shape (CSV row).**

```
date,        patient_id, test, value, units, flag, lab_facility
2026-02-10,  ER-001,     CRP,  21.4,  mg/L,  H,    Bay Reference Lab
```

One row, fixed columns. To answer "what was Ms. Reyes's CRP at her last visit," you sort by `date`, filter by `patient_id` and `test`, take the last row. Adding a second kind of fact about the same draw (e.g., the corresponding swollen joint count from that visit) means a second file or a wider table.
"""
        )
    elif shape_pick.value == "Database shape":
        body = mo.md(
            r"""
**Database shape (linked tables).**

```
PATIENTS                            ENCOUNTERS                          OBSERVATIONS
| patient_id | name        |        | encounter_id | patient_id | date|        | obs_id | encounter_id | code | value | units |
| ER-001     | Reyes, E.   |        | ENC-300148   | ER-001     | 2026-02-10 |   | OBS-CRP-26 | ENC-300148 | 1988-5 | 21.4 | mg/L |
```

Three tables, linked by IDs. To answer the same question you `JOIN OBSERVATIONS` to `ENCOUNTERS` on `encounter_id`, join again to `PATIENTS` on `patient_id`, filter to the CRP code, sort by date. The structure expresses relationships (this CRP belongs to this encounter, which belongs to this patient). The price is that to move the data, you need every related row from every related table.
"""
        )
    else:
        body = mo.md(
            r"""
**Document shape (a self-contained record).**

```json
{
  "resourceType": "Observation",
  "id": "OBS-CRP-26",
  "subject":      { "reference": "Patient/ER-001" },
  "encounter":    { "reference": "Encounter/ENC-300148" },
  "effectiveDateTime": "2026-02-10T08:30:00-05:00",
  "code":  {
    "coding": [{ "system": "http://loinc.org", "code": "1988-5", "display": "C reactive protein" }]
  },
  "valueQuantity": {
    "value": 21.4, "unit": "mg/L", "system": "http://unitsofmeasure.org", "code": "mg/L"
  },
  "interpretation": [
    { "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation", "code": "H" }] }
  ]
}
```

A single JSON object. It points at the patient and the encounter by **reference** (the same idea as a database foreign key, but written into the document itself), names the code with the system it came from (LOINC), and names the unit with the system it came from (UCUM). You can hand this object to another system and it has the whole story without needing access to your database. This is the shape FHIR resources take.
"""
        )

    mo.callout(body, kind="info")
    return (body,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Each shape solves a different problem. Spreadsheets move bulk homogeneous data cheaply. Databases keep heterogeneous facts internally consistent. Documents cross system boundaries.

        FHIR is **document-shaped on the wire and database-shaped conceptually**. The thing you send across the network is a JSON object (document). The references inside it point at other JSON objects (foreign keys, database thinking). The combination is what lets FHIR move data without losing the relationships.
        """
    )
    return


@app.cell
def _(mo):
    shape_quiz = mo.ui.radio(
        options=[
            "Spreadsheet shape (a CSV).",
            "Database shape (linked tables in a relational system).",
            "Document shape (a self-contained record with internal structure).",
        ],
        label=(
            "A pharmaceutical company is running a registry of 8,000 RA patients. Each quarter, each participating site needs to submit the latest DAS28 score for every active patient in their cohort. The submissions all have the same columns and feed a research database. Which shape best fits this submission step?"
        ),
    )
    shape_quiz
    return (shape_quiz,)


@app.cell
def _(mo, shape_quiz):
    if shape_quiz.value is None:
        shape_quiz_response = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif shape_quiz.value.startswith("Spreadsheet"):
        shape_quiz_response = mo.callout(
            mo.md(
                "**Yes.** Each row has the same columns (site, patient ID, visit date, DAS28). The submission is homogeneous and bulk. The spreadsheet shape is exactly what registry submissions look like in practice. The registry's internal database is a different shape, but the boundary across organizations is a spreadsheet because it travels cheaply and parses anywhere."
            ),
            kind="success",
        )
    elif shape_quiz.value.startswith("Database"):
        shape_quiz_response = mo.callout(
            mo.md(
                "**Not quite for this step.** The registry itself almost certainly stores the data in database shape, but the cross-organization submission rarely looks like \"here is a copy of my database.\" It looks like a CSV upload to the registry's portal. For ingest-from-many-sites of one homogeneous fact, the spreadsheet shape wins on portability and parser availability."
            ),
            kind="warn",
        )
    else:
        shape_quiz_response = mo.callout(
            mo.md(
                "**Not for this step.** Document shape would be the right choice if each submission was a rich heterogeneous record (the full record for a patient with all their visits, labs, and notes, sent as one object). For a homogeneous quarterly DAS28 dump across many sites, that's overkill: the document overhead per row would dwarf the row itself. CSV is the cheapest right answer."
            ),
            kind="warn",
        )
    shape_quiz_response
    return (shape_quiz_response,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Idea 2. The web is three boring agreements layered together.

        The web works because almost everyone agreed on a small number of things. Three of them matter for FHIR. None of them are clever.

        **HTTP.** A client (a browser, a phone, an app on a clinician's iPad) sends a *request*. A server sends back a *response*. Each request has a method (what you want to do), an address (what you want to do it to), some headers, and optionally a body.

        **REST.** The things in your system are *resources*. Each resource has a *stable address*. The actions on a resource are the HTTP methods.

        **JSON.** A way of writing structured data down so that any modern programming language can parse it. The whole language is: objects in curly braces, lists in square brackets, key-value pairs, strings, numbers, booleans, null.

        That is most of what underlies FHIR. The clinical content on top of it is hard. The web layer underneath it is not.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The restaurant analogy.

        It is a slightly tired analogy. It works.

        You walk into a restaurant. You make a **request** by telling the waiter what you want ("the salmon, please"). The waiter walks back to the kitchen, finds it, and returns with a **response** (a plate). Sometimes the response is "we're out of salmon" or "you can't sit here without a reservation" or "the kitchen is on fire," which are all valid responses, just with different status codes.

        The menu is the **REST resource model**. Every dish has a stable name. You can ask for any dish on the menu using the same kind of request. New dishes get added to the menu without anyone having to invent a new way of ordering. To replace your order, you don't invent "salmon-replace;" you say "replace what I ordered with the duck," which is the same verb structure (replace) on the same address (your table).

        The receipt at the end is the **JSON**. A compact, readable, structured record of exactly what happened. You can hand it to your accountant or your insurance company, and they can read it without calling the restaurant.

        The four HTTP methods you'll meet in FHIR map to restaurant moves cleanly enough that the comparison is useful, not cute.
        """
    )
    return


@app.cell
def _(pd):
    restaurant = pd.DataFrame(
        [
            {"HTTP method": "GET",    "Restaurant move": "Read the menu. Read your current order. Read the bill.",
             "Notes": "Asks for data. Should not change anything. Safe to retry."},
            {"HTTP method": "POST",   "Restaurant move": "Place a new order with the kitchen.",
             "Notes": "Creates a new thing. The server picks the new thing's address (table 4, order #58)."},
            {"HTTP method": "PUT",    "Restaurant move": "Replace what's at table 4 with this new order.",
             "Notes": "Replaces the thing at a known address with the version you sent."},
            {"HTTP method": "DELETE", "Restaurant move": "Cancel the order at table 4.",
             "Notes": "Removes the thing at the address."},
        ]
    )
    restaurant
    return (restaurant,)


@app.cell
def _(mo):
    verb_quiz = mo.ui.radio(
        options=[
            "GET /Observation/OBS-CRP-26",
            "POST /Observation with the new resource in the body",
            "PUT /Observation/OBS-CRP-26 with the corrected resource in the body",
            "DELETE /Observation/OBS-CRP-26",
        ],
        label=(
            "Ms. Reyes's CRP was entered into the EHR on 2026-02-10. Yesterday a lab tech realized the result was misread off the printout and the correct value is actually 24.1, not 21.4. The system records this CRP at address `Observation/OBS-CRP-26`. Which HTTP request fixes the existing record?"
        ),
    )
    verb_quiz
    return (verb_quiz,)


@app.cell
def _(mo, verb_quiz):
    if verb_quiz.value is None:
        verb_response = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif verb_quiz.value.startswith("PUT"):
        verb_response = mo.callout(
            mo.md(
                "**Right.** `PUT` replaces the thing at a known address with the version you sent. The CRP record already exists at `Observation/OBS-CRP-26`, so the correct request is `PUT /Observation/OBS-CRP-26` with the corrected resource as the body. In a real system this would also create a new entry in the resource's history (FHIR keeps versions automatically), so the original 21.4 wouldn't be lost; it would just no longer be the current version."
            ),
            kind="success",
        )
    elif verb_quiz.value.startswith("POST"):
        verb_response = mo.callout(
            mo.md(
                "**Close, but no.** `POST` creates a **new** resource. If you `POST` a corrected CRP, you now have two CRP observations from the same draw, the original wrong one and the corrected one. The clinical chart shows both. To fix an existing resource at a known address, you replace it with `PUT` (or, in some workflows, mark the original as entered-in-error and add a corrected one, but that's a content-level decision; the HTTP verb for in-place replacement is still `PUT`)."
            ),
            kind="warn",
        )
    elif verb_quiz.value.startswith("GET"):
        verb_response = mo.callout(
            mo.md(
                "**No.** `GET` only reads. It can't change a stored value. You'd use `GET` to confirm the wrong value is there before correcting it, but the correction itself needs a write verb."
            ),
            kind="warn",
        )
    else:
        verb_response = mo.callout(
            mo.md(
                "**Not quite.** `DELETE` removes the resource entirely. You'd be deleting the CRP rather than correcting it. In a clinical chart that's almost never the right move; the audit trail wants 'here is what was originally recorded, and here is the correction.' `PUT` with the corrected resource is the standard answer."
            ),
            kind="warn",
        )
    verb_response
    return (verb_response,)


@app.cell
def _(mo):
    mo.md(
        r"""
        That is most of what you need to read FHIR URLs and responses for the rest of this course. The full HTTP specification is bigger; the FHIR-relevant subset is essentially the four verbs above plus a handful of status codes (200, 201, 404, 401, 403, 500) you'll meet in Track 2 when you actually query a FHIR server.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Idea 3. Health data standards layer; they don't replace.

        There is a temptation to tell this history as if FHIR is the answer and everything before was a mistake. It sounds wrong to anyone who has worked in a hospital still running on the previous standards (every hospital, currently).

        Each of the three major health data standards solved a real problem with the tools available at the time. None of them have been retired. They layer on top of each other in modern systems.
        """
    )
    return


@app.cell
def _(pd):
    history = pd.DataFrame(
        [
            {
                "Standard": "HL7 v2",
                "Year": "1989",
                "Shape": "Pipe-delimited messages.",
                "Problem it solved": "Move a lab result from the lab system into the EHR, fast, over the slow networks of the late 1980s.",
                "Still doing what it was built for?": "Yes, everywhere. Most lab results in most hospitals still arrive via v2.",
            },
            {
                "Standard": "CDA",
                "Year": "2005",
                "Shape": "XML clinical documents.",
                "Problem it solved": "Share a complete clinical document (e.g. a discharge summary) between two organizations that don't share an EHR.",
                "Still doing what it was built for?": "Yes. CCD documents still carry most Direct messaging and Meaningful Use exchange.",
            },
            {
                "Standard": "FHIR",
                "Year": "2014 (R4 stable 2019)",
                "Shape": "JSON resources, RESTful API.",
                "Problem it solved": "Let new applications read and write clinical data with the same tools used to build everything else on the modern web.",
                "Still doing what it was built for?": "Yes, and growing fast. CDS Hooks, SMART on FHIR, ONC/CMS interop rules all live here.",
            },
        ]
    )
    history
    return (history,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Hold this in mind: HL7 v2 is the messaging layer inside a hospital. CDA is the document layer between organizations. FHIR is the API layer for new applications. The three coexist, often in the same hospital, often even in the same workflow. A FHIR API in front of a clinical data warehouse can be (and often is) populated by HL7 v2 messages arriving in the back.

        Knowing which standard carries which traffic is most of what "how does data move in this hospital" actually answers.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Idea 4. Paper chart → EHR → FHIR is a continuity story.

        Each step kept what was useful from the previous one and added a new layer.

        **Paper chart.** Structured by physical layout. The labs section was the labs section because someone clipped them there. Single site (one chart per institution), single author per page, queryable only by reading, movable only by photocopy and mail. The structure was in the *paper itself*.

        **EHR.** Structured by vendor schema. Single site per vendor instance (your Epic does not talk to the Cerner across town without effort), multi-author with audit trail, queryable inside the vendor's tools, movable only with custom integration. The structure is in the *database schema*, which is the vendor's.

        **FHIR.** Structured by a shared specification. Multi-site by design (resource IDs are URLs, the API is RESTful), queryable by anyone with HTTP, movable by definition. The structure is in the *specification*, which is public, free, and the same for everyone.

        Each shape kept being useful. The paper chart is still in active use in some long-term care and resource-limited settings. The EHR is still the right shape for in-system documentation. FHIR is the right shape for the boundary: getting data out of a system, into another system, into a third-party app, out for research. It is not the end state. It is the current state of the boundary layer.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Where interoperability actually breaks.

        The word "interoperability" gets used as if it is one thing. It is at least five things, layered on top of each other. When two systems "can't talk," the question to ask is *which of these layers* is the problem. Most arguments about interop stall because nobody has named the layer.

        | # | Layer | What it means | A failure here looks like |
        |---|---|---|---|
        | 1 | **Transport** | Can the two systems reach each other on a network? | Connection timeout, TLS handshake failure, 401 Unauthorized. |
        | 2 | **Format** | Do they parse the same serialization? JSON vs XML vs HL7 v2 pipes. | "Unexpected character at position 47." |
        | 3 | **Structure** | Are the same facts in the same places? | "I'm looking for the MRN in `PAT_MRN_ID` and there's nothing there." |
        | 4 | **Terminology** | Are the codes the same? | "The diagnosis code came in as SNOMED 239791008; my system only understands ICD-10." |
        | 5 | **Content** | Did the sender capture what the receiver wants? | "There is no anti-CCP in the record you sent me. We need it." |

        FHIR (and US Core, mCODE, and the implementation guides covered in later tracks) addresses layers 2, 3, and partially 4. Layer 1 is the network team's job. Layer 5 is a workflow problem that no standard can solve by itself.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Diagnose four real differences.

        The capstone of this track. Ms. Reyes's Epic and Cerner exports differ in many places. Four of those differences are worth walking deliberately. For each one, decide which of the five layers above the difference lives at.

        Take your time. The point of the exercise is to be able to do this on a real interoperability complaint at work, where naming the layer is most of the path to a fix.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Difference 1. Identifier structure.

        **Epic** stores Ms. Reyes's MRN as a top-level field on the patient encounter object:
        ```json
        "PAT_ENC": {
          "PAT_MRN_ID": "ER-001",
          ...
        }
        ```

        **Cerner** stores the same MRN as an entry inside an array of identifiers, each tagged with a pool:
        ```json
        "person_alias": [
          {"alias_pool_disp": "MRN",       "alias": "ER-001"},
          {"alias_pool_disp": "Person ID", "alias": "78463921"}
        ]
        ```

        The value `ER-001` is identical in both. The path to get to it is not.
        """
    )
    return


@app.cell
def _(mo):
    diff1 = mo.ui.radio(
        options=[
            "Transport. The systems can't reach each other.",
            "Format. One is JSON and the other isn't.",
            "Structure. Same fact, different path to find it.",
            "Terminology. Different codes for the same concept.",
            "Content. The fact isn't captured on one side.",
        ],
        label="Which layer does Difference 1 live at?",
    )
    diff1
    return (diff1,)


@app.cell
def _(diff1, mo):
    if diff1.value is None:
        diff1_response = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif diff1.value.startswith("Structure"):
        diff1_response = mo.callout(
            mo.md(
                "**Right. Structure.** Both records have the MRN. Both are JSON (same format). Both contain `ER-001` as a string (same value, no terminology issue). The fact is captured on both sides (no content gap). What differs is **where in the document** the fact lives. Epic puts it at one address, Cerner at another. A receiver expecting Epic's path finds nothing in Cerner's record, and vice versa, even though the data is sitting right there.\n\nFHIR addresses this by specifying exactly where each fact lives in each resource. In FHIR R4, every patient identifier sits in `Patient.identifier[]`, an array of objects with a system (URI naming the assigning authority) and a value. Senders comply with that structure; receivers know where to look. The Cerner-style flexibility of an array of identifiers turns out to be the right shape; the Epic-style top-level scalar is the shape that doesn't survive moving across systems."
            ),
            kind="success",
        )
    elif diff1.value.startswith("Terminology"):
        diff1_response = mo.callout(
            mo.md(
                "**Not quite.** Terminology problems are about which code system you're using (SNOMED vs ICD-10, etc.). Here the *value* of the MRN is the same string `ER-001` on both sides, and there's no code system involved (an MRN is a local identifier, not a coded concept). The problem is where in the document the value lives. That is the **structure** layer."
            ),
            kind="warn",
        )
    elif diff1.value.startswith("Format"):
        diff1_response = mo.callout(
            mo.md(
                "**No.** Both exports are JSON. A JSON parser handles both without complaint. The problem starts after parsing succeeds: the parsed Cerner record has no `PAT_MRN_ID` key, even though the MRN is in there. That's a **structure** problem, not a format problem."
            ),
            kind="warn",
        )
    elif diff1.value.startswith("Content"):
        diff1_response = mo.callout(
            mo.md(
                "**No.** The MRN is captured in both records. A content problem would be one side not capturing the MRN at all. Here both sides have it; they just store it in different places. That's the **structure** layer."
            ),
            kind="warn",
        )
    else:
        diff1_response = mo.callout(
            mo.md(
                "**No.** Transport is the network layer: connection failures, TLS, auth. Both records are sitting in front of you, so transport already worked. The problem starts in how the data is laid out inside the records. That's the **structure** layer."
            ),
            kind="warn",
        )
    diff1_response
    return (diff1_response,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Difference 2. Diagnosis coding.

        **Epic** codes Ms. Reyes's RA primarily in ICD-10:
        ```json
        "PROBLEM_LIST": [{
          "DX_NAME":    "Seropositive erosive rheumatoid arthritis",
          "ICD10_LIST": "M05.79"
        }]
        ```

        **Cerner** codes the same diagnosis primarily in SNOMED CT, with ICD-10 alongside:
        ```json
        "problem": [{
          "nomenclature_disp":      "Rheumatoid arthritis, seropositive",
          "source_vocabulary_disp": "SNOMED CT",
          "source_identifier":      "239791008",
          "icd10":                  "M05.79"
        }]
        ```

        Both records say Ms. Reyes has seropositive RA. The clinical fact is identical. The way that fact is represented as a code differs: Epic leads with ICD-10 `M05.79`, Cerner leads with SNOMED CT `239791008`.
        """
    )
    return


@app.cell
def _(mo):
    diff2 = mo.ui.radio(
        options=[
            "Transport. The systems can't reach each other.",
            "Format. One is JSON and the other isn't.",
            "Structure. Same fact, different path to find it.",
            "Terminology. Different codes for the same concept.",
            "Content. The fact isn't captured on one side.",
        ],
        label="Which layer does Difference 2 live at?",
    )
    diff2
    return (diff2,)


@app.cell
def _(diff2, mo):
    if diff2.value is None:
        diff2_response = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif diff2.value.startswith("Terminology"):
        diff2_response = mo.callout(
            mo.md(
                "**Right. Terminology.** Two different coding systems (ICD-10 and SNOMED CT) describe the same clinical concept (seropositive RA). The receiver might understand one and not the other, or might need a mapping table to translate between them.\n\nThis is also a case where the structure layer is intentionally not the answer: both records have a 'diagnosis code' field, the receiver knows where to look. What the receiver doesn't necessarily have is the vocabulary to interpret `239791008` if they only speak ICD-10. FHIR addresses this with the `coding[]` array on coded fields, where the sender can include the same concept in multiple coding systems at once (an ICD-10 entry **and** a SNOMED CT entry, both pointing at the same concept). Value sets in implementation guides like US Core then say 'for this slot, send at least these codings.' Tracks 4 and 5 develop this."
            ),
            kind="success",
        )
    elif diff2.value.startswith("Structure"):
        diff2_response = mo.callout(
            mo.md(
                "**Close, but not the primary problem here.** Yes, the structure differs slightly (Cerner nests the code under `source_vocabulary_disp` plus `source_identifier`, Epic just puts the ICD-10 string under `ICD10_LIST`). But the load-bearing difference is which **code system** is used. Even if the structure were identical, the receiver still has to decide whether to look up `239791008` in SNOMED or `M05.79` in ICD-10. That decision is the **terminology** layer."
            ),
            kind="warn",
        )
    elif diff2.value.startswith("Content"):
        diff2_response = mo.callout(
            mo.md(
                "**No.** The diagnosis is captured on both sides. Cerner even includes the ICD-10 alongside its SNOMED code, so technically the receiver has both. The problem is that the **primary** code each vendor uses comes from a different vocabulary. That's the **terminology** layer."
            ),
            kind="warn",
        )
    elif diff2.value.startswith("Format"):
        diff2_response = mo.callout(
            mo.md(
                "**No.** Both records are JSON, and the diagnosis appears in both. The interesting difference is which vocabulary is leading: ICD-10 in Epic, SNOMED in Cerner. That's the **terminology** layer."
            ),
            kind="warn",
        )
    else:
        diff2_response = mo.callout(
            mo.md(
                "**No.** Transport is the network layer. The records are sitting in front of you. The interesting question is whether the receiver understands the **code** the sender chose. That's the **terminology** layer."
            ),
            kind="warn",
        )
    diff2_response
    return (diff2_response,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Difference 3. Reference range units for ESR.

        Ms. Reyes's ESR at her 2026 visit is 33 mm/h in both records. The reference range upper bound is 20. The units, written out, look like this:

        **Epic.**
        ```json
        { "COMPONENT_NAME": "ESR", "ORD_VALUE": "33", "REFERENCE_UNIT": "mm/h", "REFERENCE_HIGH": "20" }
        ```

        **Cerner.**
        ```json
        { "event_cd_disp": "ESR (Sed Rate, Westergren)", "result_val": "33",
          "result_units_disp": "mm/hr", "normal_high": 20 }
        ```

        Epic writes the unit as `mm/h`. Cerner writes it as `mm/hr`. The numeric value, the test, and the reference range upper bound agree.
        """
    )
    return


@app.cell
def _(mo):
    diff3 = mo.ui.radio(
        options=[
            "Transport. The systems can't reach each other.",
            "Format. One is JSON and the other isn't.",
            "Structure. Same fact, different path to find it.",
            "Terminology. Different codes for the same concept.",
            "Content. The fact isn't captured on one side.",
        ],
        label="Which layer does Difference 3 live at?",
    )
    diff3
    return (diff3,)


@app.cell
def _(diff3, mo):
    if diff3.value is None:
        diff3_response = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif diff3.value.startswith("Terminology"):
        diff3_response = mo.callout(
            mo.md(
                "**Right. Terminology.** Units of measure are a terminology problem hiding in plain sight. The international standard FHIR uses for units is UCUM (Unified Code for Units of Measure), maintained by the Regenstrief Institute. UCUM's canonical code for 'millimeters per hour' is `mm/h`. Epic happens to write it the UCUM way. Cerner writes `mm/hr`, which is **not a valid UCUM code**; it is the colloquial English abbreviation.\n\nThis is the most common kind of terminology failure: a human-readable string that looks identical until a validating receiver rejects it because it doesn't match the controlled vocabulary. FHIR Observations use `valueQuantity.code` for the UCUM code and `valueQuantity.unit` for the human-readable string. If both are sent, the receiver can validate the code and display the string. Skipping the code (or sending an invalid one) is the failure mode."
            ),
            kind="success",
        )
    elif diff3.value.startswith("Format"):
        diff3_response = mo.callout(
            mo.md(
                "**Not quite.** Both records are valid JSON. The strings `mm/h` and `mm/hr` are both legal JSON string values; the parser doesn't complain. The receiver's *unit validator* complains, and that complaint is about which **vocabulary** the unit string belongs to (the UCUM controlled vocabulary, vs free-text English abbreviations). That makes this a **terminology** problem."
            ),
            kind="warn",
        )
    elif diff3.value.startswith("Structure"):
        diff3_response = mo.callout(
            mo.md(
                "**Not quite.** Yes, the field names differ (`REFERENCE_UNIT` vs `result_units_disp`), so there is also a structure layer issue here. But the **interesting** difference is which controlled vocabulary the unit string is drawn from. Even if the field names were identical, sending `mm/hr` would fail UCUM validation; sending `mm/h` would pass. That's the **terminology** layer."
            ),
            kind="warn",
        )
    elif diff3.value.startswith("Content"):
        diff3_response = mo.callout(
            mo.md(
                "**No.** Both records capture the unit. The problem is that the unit *string* in one record is not a valid code in the controlled vocabulary (UCUM) the receiver may insist on. That's a **terminology** layer issue."
            ),
            kind="warn",
        )
    else:
        diff3_response = mo.callout(
            mo.md(
                "**No.** Transport is the network. Both records have arrived. The unit string difference is a vocabulary problem (UCUM vs colloquial), which is the **terminology** layer."
            ),
            kind="warn",
        )
    diff3_response
    return (diff3_response,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Difference 4. Anti-CCP nowhere in the Cerner record.

        Epic's lab section includes Ms. Reyes's anti-CCP result from 2024:

        ```json
        { "ORDER_PROC_ID": "LAB-400003", "COMPONENT_NAME": "Anti-CCP",
          "ORD_VALUE": "154", "REFERENCE_UNIT": "U/mL", "LOINC_CODE": "32218-7",
          "RESULT_TIME": "2024-01-08T09:15:00-05:00" }
        ```

        Cerner's `clinical_event` array, in this synthetic export, contains only her 2026 visit and never includes anti-CCP. The receiver, an RA monitoring app that wants longitudinal anti-CCP for risk-stratification, asks the Cerner system for it and there is nothing to return.
        """
    )
    return


@app.cell
def _(mo):
    diff4 = mo.ui.radio(
        options=[
            "Transport. The systems can't reach each other.",
            "Format. One is JSON and the other isn't.",
            "Structure. Same fact, different path to find it.",
            "Terminology. Different codes for the same concept.",
            "Content. The fact isn't captured on one side.",
        ],
        label="Which layer does Difference 4 live at?",
    )
    diff4
    return (diff4,)


@app.cell
def _(diff4, mo):
    if diff4.value is None:
        diff4_response = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif diff4.value.startswith("Content"):
        diff4_response = mo.callout(
            mo.md(
                "**Right. Content.** This is the layer no standard can fix by itself. The anti-CCP result is not in the Cerner record because the Cerner export, as configured at this site, didn't pull historical labs from before 2026. Mapping does not help. Vocabulary translation does not help. The fact is not there to map or translate.\n\nThis is the layer where the work is at the sender: configuring the export to include historical labs, or running a workflow that captures anti-CCP in the first place. FHIR can guarantee that *if* a sender has the data, the receiver knows where to find it and how to read it. FHIR cannot guarantee that the sender captured the data in the first place. That's what implementation guides like US Core address from a different angle: they say 'for this profile to claim conformance, you must capture and expose these fields.' Without that, content is a contractual problem, not a technical one."
            ),
            kind="success",
        )
    elif diff4.value.startswith("Structure"):
        diff4_response = mo.callout(
            mo.md(
                "**Not quite.** A structure problem means the data is there but the receiver can't find it. Here the receiver searches in every reasonable place in the Cerner record and the anti-CCP result is genuinely **not there**. There is nothing to find. That's the **content** layer: the sender didn't capture (or didn't include) what the receiver wants."
            ),
            kind="warn",
        )
    elif diff4.value.startswith("Terminology"):
        diff4_response = mo.callout(
            mo.md(
                "**No.** A terminology problem would be the anti-CCP result being there but coded with a system the receiver doesn't understand. Here the result is **not in the record at all**. No code, no value, no field. That is the **content** layer."
            ),
            kind="warn",
        )
    elif diff4.value.startswith("Format"):
        diff4_response = mo.callout(
            mo.md(
                "**No.** Both records are JSON. The Cerner record parses fine. The anti-CCP just isn't anywhere inside it. That's a **content** layer issue."
            ),
            kind="warn",
        )
    else:
        diff4_response = mo.callout(
            mo.md(
                "**No.** Transport is the network. Cerner's record arrived. The thing inside the record that the receiver wants (anti-CCP) isn't captured. That's the **content** layer."
            ),
            kind="warn",
        )
    diff4_response
    return (diff4_response,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What FHIR actually fixes, by layer.

        Four differences. Three different layers. Each one suggests a different kind of fix.
        """
    )
    return


@app.cell
def _(pd):
    fixes = pd.DataFrame(
        [
            {
                "Layer": "Transport",
                "Example we saw": "(not in this exercise, but: a connection timeout, a 401 Unauthorized)",
                "Who fixes it": "Network and security teams.",
                "How FHIR helps": "Standardizes on HTTPS plus OAuth (SMART on FHIR, Track 5). Doesn't replace network plumbing, but removes ambiguity about which protocol to use.",
            },
            {
                "Layer": "Format",
                "Example we saw": "(not in this exercise, but: HL7 v2 pipes vs CDA XML vs FHIR JSON)",
                "Who fixes it": "Whoever owns the parser.",
                "How FHIR helps": "Defines JSON (and equivalently XML and RDF) as the wire formats. One parser on each side covers every resource.",
            },
            {
                "Layer": "Structure",
                "Example we saw": "Difference 1: MRN at top level vs inside an alias array.",
                "Who fixes it": "Standard authors and implementation guide authors.",
                "How FHIR helps": "Specifies exactly where each fact lives in each resource. `Patient.identifier[]` is the only place a patient identifier goes.",
            },
            {
                "Layer": "Terminology",
                "Example we saw": "Difference 2 (SNOMED vs ICD-10), Difference 3 (UCUM vs colloquial units).",
                "Who fixes it": "Standards bodies that maintain the vocabularies, plus implementers who choose what to send.",
                "How FHIR helps": "Coded fields allow multiple codings at once (you can send the SNOMED **and** the ICD-10 for the same concept). Value sets in implementation guides say which codings are required for which slot.",
            },
            {
                "Layer": "Content",
                "Example we saw": "Difference 4: anti-CCP not captured in the Cerner export.",
                "Who fixes it": "The sender, by changing what they capture, configure, or expose.",
                "How FHIR helps": "Implementation guides (US Core, mCODE, etc., Track 4) declare 'to claim conformance to this profile, you must capture and expose these fields.' If the sender doesn't capture them, they don't get to claim conformance.",
            },
        ]
    )
    fixes
    return (fixes,)


@app.cell
def _(mo):
    mo.md(
        r"""
        The shape of the question matters. The next time someone says "the two systems can't talk to each other," the move is:

        1. Find the specific complaint. Not "the integration is broken;" something like "the receiver is showing the diagnosis as `M05.79` but we send `239791008`."
        2. Pin it to one of the five layers. (In that example: terminology.)
        3. The fix lives with whoever owns that layer.

        That move is most of how interoperability conversations get unstuck.
        """
    )
    return


@app.cell
def _(mo):
    reflection = mo.ui.text_area(
        placeholder="Two or three sentences. No grading; the exercise is writing it.",
        rows=4,
        full_width=True,
        label=(
            "Before this track, where did you implicitly think interoperability "
            "problems lived? What part of the five-layer view surprised you, if any?"
        ),
    )
    mo.vstack(
        [
            reflection,
            mo.callout(
                mo.md("_No answer key here. The reflection is the work._"),
                kind="neutral",
            ),
        ]
    )
    return (reflection,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What you did in this track.

        - You put four foundational ideas in place before meeting a single FHIR resource: data has three shapes (spreadsheet, database, document); the web is three boring agreements (HTTP, REST, JSON); health data standards layer (HL7 v2 still moves the lab traffic inside hospitals, CDA still moves the documents between organizations, FHIR is the new boundary layer); and the paper-chart-to-EHR-to-FHIR continuity is a story about each step keeping what was useful and adding a new layer.
        - You traced four real differences between Ms. Reyes's Epic-style and Cerner-style exports and named which interoperability layer each one lives at: structure, terminology, terminology, content.
        - You gained a five-layer framework for diagnosing any "the two systems can't talk to each other" complaint.

        That last piece is the move worth keeping. Most interop arguments at work are arguments about which of the five layers is broken. As soon as someone names the layer, the conversation can move.

        ## What's next.

        **Track 1: FHIR fundamentals.** Resources, references, bundles, and the terminology systems FHIR uses (LOINC for labs, SNOMED CT for clinical findings, RxNorm for medications). The vocabulary will start coming fast. The structure underneath is what you just put in place.
        """
    )
    return


if __name__ == "__main__":
    app.run()
