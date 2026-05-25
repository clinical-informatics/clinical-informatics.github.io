"""Track 01: Standards in the EHR.

Code standards are the agreement that a single clinical fact will be
recorded under a single identifier. Without that agreement, a query that
filters on one encoding silently omits rows that use any other encoding
for the same fact. This track presents the code standards that govern
data in a modern US clinical warehouse: which standard names which slice
of the record, where in the EHR each is stored, and how to construct
queries that survive vocabulary heterogeneity.
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
    import pandas as pd

    # Cross-reference helpers inlined from shared/cross_reference.py so the
    # WASM export is self-contained. Exposed as `xref` so call sites read
    # the same as in other courses.
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

    return mo, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 01: Standards in the EHR

        ## The purpose of code standards

        Clinical facts can be written in many ways. The order entry screen may record "CRP" in one record, "C-reactive protein" in another, and "C-reactive protein, serum" in a third. A query that filters the order text on the string "CRP" returns the first record and omits the others. The resulting cohort is incomplete by an amount that is not visible from the query itself.

        A code standard assigns one stable identifier to one clinical fact. Every system that conforms to the standard records the same identifier for that fact, regardless of how it appears in the user interface. A query that filters on the identifier returns every instance of the fact across every system that conforms.

        The remainder of this track defines the code standards present in a modern US clinical warehouse, identifies the EHR location of each, and specifies the failure modes that arise when a query filters on one vocabulary while the relevant data is encoded in another.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The standards present in a US clinical warehouse

        Each standard below governs a defined slice of the record. The table lists the standard, the slice it governs, the issuing body, a representative code, and the EHR location where the code appears in production data.
        """
    )
    return


@app.cell
def _(mo, pd):
    standards_table = pd.DataFrame(
        [
            {
                "Standard": "LOINC",
                "What it names": "Lab tests and clinical observations",
                "Issued by": "Regenstrief Institute",
                "Example": "1988-5 (C-reactive protein, serum/plasma)",
                "EHR location": "measurement / lab result tables",
            },
            {
                "Standard": "SNOMED CT",
                "What it names": "Clinical findings, problems, procedures, anatomy",
                "Issued by": "SNOMED International",
                "Example": "69896004 (Rheumatoid arthritis)",
                "EHR location": "problem list, structured assessments",
            },
            {
                "Standard": "ICD-10-CM",
                "What it names": "Billing diagnoses (US clinical modification)",
                "Issued by": "CDC / NCHS",
                "Example": "M05.79 (Rheumatoid arthritis with rheumatoid factor of multiple sites)",
                "EHR location": "claims, encounter diagnoses, problem list",
            },
            {
                "Standard": "CPT",
                "What it names": "Procedures and professional services (US billing)",
                "Issued by": "American Medical Association",
                "Example": "99214 (Office visit, established patient, moderate complexity)",
                "EHR location": "claims, charge capture, scheduling",
            },
            {
                "Standard": "RxNorm",
                "What it names": "Medications at the ingredient, dose, and product level",
                "Issued by": "US National Library of Medicine",
                "Example": "6851 (methotrexate)",
                "EHR location": "medication orders, e-prescribing, drug exposure tables",
            },
            {
                "Standard": "NDC",
                "What it names": "Dispensed drug products (manufacturer, dose, package)",
                "Issued by": "FDA",
                "Example": "0074-3799-02 (Humira 40 mg/0.8 mL pen, 2-pack)",
                "EHR location": "pharmacy dispense records, claims",
            },
        ]
    )
    standards_table.index = range(1, len(standards_table) + 1)
    standards_table.index.name = "row"
    standards_table
    return (standards_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three properties of the table above are load-bearing for the rest of this course.

        First, each standard governs a single slice. LOINC names a lab test. RxNorm names a medication. ICD-10-CM names a billing diagnosis. The slices overlap in clinical content (a SNOMED problem and an ICD-10-CM diagnosis can both record rheumatoid arthritis), and that overlap is the source of most cohort-definition errors.

        Second, a single visit produces facts in multiple vocabularies simultaneously. One encounter typically generates a SNOMED problem-list update, one or more ICD-10-CM encounter diagnoses, one or more CPT procedures, several LOINC-coded lab results, and one or more RxNorm-coded medication orders. These rows live in different tables and are joined together for analysis.

        Third, the identifiers are stable across institutions. LOINC 1988-5 refers to C-reactive protein in every institution that conforms to LOINC, in every country that conforms to LOINC. Vendor-internal codes, in contrast, are stable inside a single EHR installation and are not interpretable outside it.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Worked example: Reyes's first lab panel

        The four labs below were drawn from Ms. Reyes at her new-patient consult on 2022-02-14. The `LOINC` column is the universal identifier for each test. The `Local name` column is the human-readable label printed on the result.
        """
    )
    return


@app.cell
def _(pd):
    reyes_first_labs = pd.DataFrame(
        [
            {
                "LOINC": "1988-5",
                "Local name": "C-reactive protein",
                "Value": 42.1,
                "Unit": "mg/L",
                "Reference": "0 to 5",
                "Flag": "H",
            },
            {
                "LOINC": "4537-7",
                "Local name": "Erythrocyte sedimentation rate",
                "Value": 58,
                "Unit": "mm/h",
                "Reference": "0 to 20",
                "Flag": "H",
            },
            {
                "LOINC": "32218-7",
                "Local name": "Cyclic citrullinated peptide Ab (IgG)",
                "Value": 178,
                "Unit": "U/mL",
                "Reference": "0 to 20",
                "Flag": "H",
            },
            {
                "LOINC": "718-7",
                "Local name": "Hemoglobin",
                "Value": 11.6,
                "Unit": "g/dL",
                "Reference": "12 to 15.5",
                "Flag": "L",
            },
        ]
    )
    reyes_first_labs.index = range(1, len(reyes_first_labs) + 1)
    reyes_first_labs.index.name = "row"
    reyes_first_labs
    return (reyes_first_labs,)


@app.cell
def _(mo):
    mo.md(
        r"""
        The clinical interpretation of this panel is a seropositive RA presentation with active inflammation and a mild normocytic anemia, consistent with the rest of Reyes's record.

        The informatics consequence is the relevant point. To retrieve every CRP value Reyes has ever had, the correct filter is `LOINC = '1988-5'` against the measurement table. The filter returns every CRP record regardless of how the order screen labeled the test, and excludes adjacent tests such as high-sensitivity CRP (LOINC `30522-7`), which is a distinct measurement.

        A filter on the `Local name` column would return only the records whose label string matches. The result varies by site, by vendor release, and by the wording the ordering clinician selected. It is not a reproducible cohort definition.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The same clinical fact under multiple encodings

        Reyes's primary diagnosis is rheumatoid arthritis. The table below shows the encodings under which that single fact appears in different parts of her record.
        """
    )
    return


@app.cell
def _(pd):
    reyes_dx_encodings = pd.DataFrame(
        [
            {
                "Source": "Billing claim",
                "Standard": "ICD-10-CM",
                "Code": "M05.79",
                "Display text": "Rheumatoid arthritis with rheumatoid factor of multiple sites without organ or systems involvement",
            },
            {
                "Source": "Problem list",
                "Standard": "SNOMED CT",
                "Code": "69896004",
                "Display text": "Rheumatoid arthritis",
            },
            {
                "Source": "Legacy claim (pre-October 2015)",
                "Standard": "ICD-9-CM",
                "Code": "714.0",
                "Display text": "Rheumatoid arthritis",
            },
        ]
    )
    reyes_dx_encodings.index = range(1, len(reyes_dx_encodings) + 1)
    reyes_dx_encodings.index.name = "row"
    reyes_dx_encodings
    return (reyes_dx_encodings,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three identifiers correspond to one clinical concept. The naive query

        ```sql
        SELECT * FROM diagnoses WHERE icd10_code = 'M05.79'
        ```

        returns the billing claim, omits the problem-list entry (encoded in SNOMED), omits the legacy claim (encoded in ICD-9-CM), and omits the other ICD-10-CM codes in the M05 and M06 families that also describe rheumatoid arthritis. A defensible cohort definition for "any RA patient in our system" enumerates the set of codes that count as RA in every vocabulary the data uses.

        Two mechanisms produce that enumeration in practice:

        - **Curated value sets.** A clinician identifies the codes that count as the concept and records them in a value set. The US National Library of Medicine hosts the [Value Set Authority Center (VSAC)](https://vsac.nlm.nih.gov/), which publishes curated value sets authored by other teams.
        - **Crosswalks.** A standardized mapping asserts that ICD-10-CM `M05.79` corresponds to SNOMED `69896004`, which corresponds to ICD-9-CM `714.0`. The general source is the UMLS Metathesaurus from the National Library of Medicine. For data warehoused in OMOP (Track 02), the equivalent mappings are pre-loaded into the OMOP vocabulary tables and are queryable directly through [OHDSI Athena](https://athena.ohdsi.org/).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Common naming overlaps

        Four naming overlaps cause confusion in initial work with US clinical standards. Each is resolved by the distinction stated below.

        - **ICD-10-CM, ICD-10, and ICD-10-PCS are three different standards.** ICD-10 is the international diagnosis classification published by the World Health Organization. ICD-10-CM is the US clinical modification of ICD-10, with finer subcategories and additional codes. ICD-10-PCS is a separate US system for inpatient procedure coding and is unrelated to diagnoses. US claims use ICD-10-CM for diagnoses and ICD-10-PCS for inpatient procedures. International data sources typically use plain ICD-10.
        - **CPT and HCPCS are nested, not equivalent.** CPT covers procedures and professional services and is published by the AMA. HCPCS is a superset that includes all of CPT plus codes for supplies, durable medical equipment, ambulance services, and clinician-administered drugs. Medicare claims use HCPCS. Most non-Medicare claims use CPT directly.
        - **SNOMED CT and ICD-10-CM serve different functions.** SNOMED CT is a clinical terminology designed to record clinician reasoning at the level of detail clinical practice requires. ICD-10-CM is a billing classification that uses a smaller, US-specific set of codes selected to support reimbursement. The problem list usually carries SNOMED. Claims usually carry ICD-10-CM. The same condition may carry both codes on different rows of the record.
        - **RxNorm and NDC operate at different levels of abstraction.** RxNorm identifies a medication at the ingredient or formulation level (for example, methotrexate 25 mg/mL subcutaneous). NDC identifies a specific manufacturer's package (for example, the AbbVie 40 mg/0.8 mL adalimumab pen 2-pack). Prescriptions typically carry RxNorm. Pharmacy dispense records and medication claims typically carry NDC.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Standards-to-table mapping

        A query against a clinical warehouse first identifies the table that holds the fact of interest, then identifies the vocabulary that table speaks, then identifies the set of codes that count as the target concept in that vocabulary. The standard-to-table mapping below summarizes the EHR location of each standard in a typical US warehouse.

        - **LOINC** appears on rows of the lab result (or measurement) table. Each row carries a LOINC code identifying the test.
        - **SNOMED CT** appears on rows of the problem list. It also appears on structured assessment forms and on some encounter diagnosis records.
        - **ICD-10-CM** appears on rows of the encounter diagnosis table and on outbound claim records. It may be mirrored onto the problem list.
        - **CPT** appears on rows of the charge capture table and on outbound claim records.
        - **RxNorm** appears on rows of the medication order table and on the e-prescribing record.
        - **NDC** appears on rows of the pharmacy dispense table and on the medication claim record.

        A query that filters on the wrong table, or filters the right table on the wrong vocabulary, returns a syntactically valid result that is clinically incorrect.
        """
    )
    return


@app.cell
def _(mo):
    q1 = mo.ui.radio(
        options=[
            "LOINC, because labs are coded in LOINC.",
            "ICD-10-CM, because hemoglobin is on the problem list when it is low.",
            "SNOMED, because hemoglobin is a clinical finding.",
            "The standard depends on which column of which table the query targets.",
        ],
        label=(
            "A query is to return every hemoglobin value ever drawn on a patient. "
            "Which standard codes the relevant warehouse column?"
        ),
    )
    q1
    return (q1,)


@app.cell
def _(mo, q1):
    if q1.value is None:
        out1 = mo.md("_Pick one._")
    else:
        correct1 = q1.value.startswith("LOINC")
        out1 = mo.callout(
            mo.md(
                rf"""
                **{'Correct.' if correct1 else 'Not quite.'}**

                Hemoglobin is a lab result. Lab results in a clinical warehouse measurement table are coded with **LOINC**. The relevant LOINC for a serum hemoglobin is `718-7`. SNOMED and ICD-10-CM codes may also appear in the record (anemia as a problem-list entry, anemia as a billing diagnosis), but those entries record clinical interpretations of the lab value rather than the lab value itself. A query against the measurement table filtered on LOINC `718-7` returns the hemoglobin values. A query against the problem list for anemia returns a different question with a different answer.
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
            "Enumerate the SNOMED codes that count as RA and query the problem list.",
            "Enumerate the ICD-10-CM codes that count as RA and query the encounter diagnosis table.",
            "Enumerate both and query both tables, taking the union.",
            "Filter the order entry text field on the substring 'rheumatoid'.",
        ],
        label=(
            "A cohort definition is required: every patient with rheumatoid "
            "arthritis in the warehouse. Which approach is most defensible?"
        ),
    )
    q2
    return (q2,)


@app.cell
def _(mo, q2):
    if q2.value is None:
        out2 = mo.md("_Pick one._")
    else:
        correct2 = q2.value.startswith("Enumerate both")
        out2 = mo.callout(
            mo.md(
                rf"""
                **{'Correct.' if correct2 else 'Not quite.'}**

                A patient may carry RA on the problem list (SNOMED `69896004`) without an ICD-10-CM RA code on any claim. The reverse case also occurs: the billing record carries RA codes that the clinician never added to the problem list. A defensible cohort uses both tables, each filtered against a curated code set in the table's native vocabulary, with the union taken across tables. The substring search on free text is the least defensible option: a `LIKE '%rheumatoid%'` filter returns "non-rheumatoid factor positive" and "rheumatoid arthritis ruled out" along with the true positives. The avoidance of that failure mode is the reason coded vocabularies exist.
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

        Pick one of the two prompts below and write 4 to 6 sentences in the box that follows. Save what you write outside the browser; the box is a scratch pad, not persistent storage. When you are done, continue to `track-02-omop`.

        1. **A paper or report you read recently** named a clinical cohort, for example "patients with heart failure" or "patients on statins". Identify the vocabularies the authors would have needed to enumerate to construct that cohort. Specify what you would request from the authors before accepting the cohort definition as complete.

        2. **A vendor pitches an analytics tool** that consumes free-text problem-list strings and reports the prevalence of common conditions. State the structural failure mode of the approach and the addition you would require before deployment on production data.
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
        "OMOP is the next layer.",
        (
            "Code standards specify the identifier for an individual fact. They do "
            "not specify the table in which the fact is stored or the columns that "
            "describe it. Track 02 introduces OMOP, a fixed schema layered on top "
            "of the code standards. The same six core tables appear at every "
            "institution that adopts OMOP, with concept_ids drawn from the "
            "vocabularies presented above. Continue to `track-02-omop`."
        ),
    )
    return


if __name__ == "__main__":
    app.run()
