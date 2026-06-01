"""Track 02: CQL (Clinical Quality Language).

CQL is the standards-based language for writing the logic of a quality
measure or a clinical-decision rule. The track presents the motivation,
walks a published CQL fragment line by line, has the reader write a
simulated small CQL rule against a synthetic patient panel, and
addresses the VSAC value-set dependency CQL inherits.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import types

    import marimo as mo
    import numpy as np
    import pandas as pd

    _COURSE_TITLES = {
        "06": "Learn FHIR",
        "07": "Data wrangling and engineering",
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

    return mo, np, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 02: CQL (Clinical Quality Language)

        ## Why CQL exists

        Clinical-quality measures and clinical-decision rules are logic. They take a patient's clinical record as input and return whether the patient is in the measure's numerator, the measure's denominator, or neither; whether the rule's recommendation applies to this patient at this moment; whether the alert should fire.

        Historically, that logic was written separately at every institution. The same CMS quality measure for diabetic eye exam was implemented in Epic's reporting workbench at one hospital, in Cerner's analytics layer at another, and in a custom SQL script at a third. The three implementations would disagree on edge cases (a patient whose eye exam was outside the window by three days, a patient with a different diabetes-defining code), and the same patient would be in the numerator at one site and outside it at another. The rewrite was the source of most of the divergence, and the divergence was the source of most of the disagreement about what the measure was actually measuring.

        CQL exists to solve that problem. A CQL library is a named, versioned bundle of statements that any conformant CQL engine can execute against any FHIR-shaped clinical record. The same library, executed against the same patient, returns the same answer at every conformant site. The motivation is the same one that drives FHIR (data interoperability) and OMOP (data portability), applied to the layer above: logic interoperability.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## CQL structure

        A CQL library has four standard sections.

        ```cql
        library ExampleLibrary version '1.0.0'

        using FHIR version '4.0.1'

        include FHIRHelpers version '4.0.1' called FHIRHelpers

        valueset "Rheumatoid Arthritis": 'http://example.org/fhir/ValueSet/ra-diagnoses'

        context Patient

        define "Active RA Diagnosis":
            exists (
                [Condition: "Rheumatoid Arthritis"] C
                where C.clinicalStatus.coding[0].code = 'active'
            )
        ```

        The four sections, top to bottom:

        - **Library declaration.** Names and versions the library. Two libraries with the same name and the same version produce the same results everywhere they are executed.
        - **Using declarations.** Specifies which data model the library is written against. `using FHIR version '4.0.1'` says the library expects FHIR R4 resources as input.
        - **Value-set declarations.** Names value sets by their canonical URL. The actual code lists live in VSAC; the library references them by name.
        - **Define statements.** The library's named expressions. Each `define` block names an expression that returns a value (a boolean, a list of resources, a number). Other define blocks in the same library can reference one another by name.

        The `context Patient` line means every define block in the library is evaluated against one patient at a time. The library can then be executed once per patient in a cohort.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Reading published CQL: a CMS quality measure fragment

        Below is a representative fragment of a CMS quality measure (CMS122v12, Diabetes A1c Poor Control >9%, slightly simplified for clarity). The measure asks whether a diabetic patient had a most-recent HbA1c during the measurement period that was greater than 9% (the numerator: patients with poor glycemic control).

        ```cql
        library CMS122 version '12.0.0'

        using FHIR version '4.0.1'

        include FHIRHelpers version '4.0.1' called FHIRHelpers

        valueset "Diabetes": 'http://cts.nlm.nih.gov/fhir/ValueSet/2.16.840.1.113883.3.464.1003.103.12.1001'
        valueset "HbA1c Laboratory Test": 'http://cts.nlm.nih.gov/fhir/ValueSet/2.16.840.1.113883.3.464.1003.198.12.1013'

        parameter "Measurement Period" Interval<DateTime>

        context Patient

        define "Initial Population":
            AgeInYearsAt(start of "Measurement Period") between 18 and 75
            and exists (
                [Condition: "Diabetes"] D
                where D.clinicalStatus.coding[0].code = 'active'
            )

        define "Most Recent HbA1c":
            Last (
                [Observation: "HbA1c Laboratory Test"] O
                where O.effective during "Measurement Period"
                  and O.status in {'final', 'amended', 'corrected'}
                sort by effective.value
            )

        define "Numerator":
            "Most Recent HbA1c" is not null
            and "Most Recent HbA1c".value as Quantity > 9 '%'
        ```

        ### Line-by-line reading

        - **`library CMS122 version '12.0.0'`** names the measure and pins it to version 12. CMS122v12 has a specific definition; CMS122v11 has a slightly different one. The version pin is what guarantees the measure means the same thing across institutions and across years.
        - **`valueset "Diabetes"`** references the VSAC value set 2.16.840.1.113883.3.464.1003.103.12.1001. The actual code list (the ICD-10, SNOMED, and other codes that count as diabetes) lives in VSAC and is curated by the measure stewards. A site executing this measure does not redefine diabetes; it reads the published value set.
        - **`parameter "Measurement Period" Interval<DateTime>`** declares that the measure takes a date-range parameter (typically calendar year 2026). The same measure is executed against different periods for different reporting cycles.
        - **`define "Initial Population"`** identifies the patients who are eligible to be measured: ages 18 to 75 at the start of the period with an active diabetes diagnosis.
        - **`define "Most Recent HbA1c"`** retrieves each patient's most recent HbA1c result during the measurement period. The `Last(... sort by effective.value)` construction returns the last (most recent by effective date) Observation that matches.
        - **`define "Numerator"`** identifies patients with poor glycemic control: a most-recent HbA1c that exists and is above 9%.

        The library is short. It is also unambiguous. Any conformant CQL engine reading this library against the same FHIR-shaped patient record returns the same numerator-yes-or-no answer.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## CQL and FHIR

        CQL operates on the FHIR data model. The `using FHIR version '4.0.1'` declaration says the library expects FHIR resources as input; the resource types referenced in define blocks (`[Condition: ...]`, `[Observation: ...]`) are FHIR resource types as Course 06 introduced them.

        Three operational properties follow.

        First, every CQL retrieve expression returns a list of FHIR resources of the specified type filtered by a value set or by a code. `[Condition: "Diabetes"]` returns the patient's Conditions whose code is in the Diabetes value set. The retrieve is the basic building block of every CQL query.

        Second, CQL field access uses the same FHIR field names. `C.clinicalStatus.coding[0].code` walks the FHIR Condition resource's clinicalStatus field into its first coding's code value. A reader fluent in FHIR can read CQL field expressions without additional translation.

        Third, the library is portable to any data source that can be exposed as FHIR. An OMOP warehouse (Course 07) with a FHIR projection (a FHIR API on top of OMOP, several of which exist) can execute the same CQL library that an Epic site executes. The portability is the operational payoff of the FHIR-CQL-CDS-Hooks stack.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "12",
        "06",
        "FHIR resources as CQL's data model",
        "Course 06 Track 1 introduced the FHIR Patient, Condition, Observation, and MedicationRequest resources. CQL retrieves operate directly on these resources; the field expressions walk the FHIR fields by name. Reading CQL is fluent once the FHIR data model is fluent.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Value sets and VSAC

        A value set is a named list of codes that count as "the thing" for a specific purpose. The Diabetes value set referenced above is one specific authored list of ICD-10, SNOMED CT, and other codes that the CMS122 stewards have decided count as diabetes for the measure. A different value set (Diabetes for a registry, Diabetes for a different measure) might include slightly different codes.

        The Value Set Authority Center (VSAC), maintained by the NLM, is the canonical repository of authored value sets used in CQL and in CMS quality measures. Three operational properties of VSAC are load-bearing.

        - **Stable canonical URLs.** Every value set has a stable URL. The CQL library references the URL; the URL resolves to the current value set definition. The version of the value set the library uses is pinned by the URL.
        - **Steward-curated.** Each value set has a publishing organization (CMS, AHRQ, AMA, NCQA, others) responsible for its contents. The steward updates the codes when terminology changes (a new ICD-10 code, a retired SNOMED CT code) without the library needing to change.
        - **Public download.** Most value sets are publicly downloadable; the codes are not proprietary. A site that wants to execute a CQL library can resolve every referenced value set to its full code list without licensing concerns.

        When a value set is missing a code your institution uses, the library will fail to identify those patients silently. The remedy is to read the value set before executing the library and to request additions to the steward when local codes are missing.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "12",
        "07",
        "Value sets as the terminology dependency",
        "Course 07 Track 1 introduced the code-standard vocabularies (LOINC, SNOMED CT, ICD-10-CM, CPT, RxNorm). A VSAC value set is an authored list drawn from those vocabularies. CQL's value-set declarations are how the logic layer references the terminology layer; the same vocabulary discipline Course 07 covered applies upstream.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A simulated CQL rule on a 10-patient cohort

        The cohort below is a 10-patient synthetic panel. The CQL fragment is a small RA-flare-prediction rule (active RA diagnosis, CRP above a threshold, no recent biologic escalation). The threshold slider lets the reader change the CRP cut-point; the table updates reactively to show which patients the rule identifies.

        The actual CQL would be:

        ```cql
        define "At Risk Of Flare":
            exists (
                [Condition: "Rheumatoid Arthritis"] R
                where R.clinicalStatus.coding[0].code = 'active'
            )
            and "Most Recent CRP".value as Quantity > {threshold} 'mg/L'
            and not exists (
                [MedicationStatement: "TNF Inhibitors"] M
                where M.effectivePeriod.start > Today() - 30 days
            )
        ```

        The pandas computation below simulates the same logic against the synthetic patient panel.
        """
    )
    return


@app.cell
def _(pd):
    cohort = pd.DataFrame(
        [
            {"patient_id": "P001", "name": "Reyes, Elena", "active_ra": True, "recent_crp_mg_L": 14.3, "biologic_started_within_30d": False},
            {"patient_id": "P002", "name": "Alvarez, Maria", "active_ra": True, "recent_crp_mg_L": 8.2, "biologic_started_within_30d": False},
            {"patient_id": "P003", "name": "Kim, Janet", "active_ra": True, "recent_crp_mg_L": 22.1, "biologic_started_within_30d": True},
            {"patient_id": "P004", "name": "Park, Lisa", "active_ra": True, "recent_crp_mg_L": 4.8, "biologic_started_within_30d": False},
            {"patient_id": "P005", "name": "Chen, Wei", "active_ra": False, "recent_crp_mg_L": 18.0, "biologic_started_within_30d": False},
            {"patient_id": "P006", "name": "Garcia, Jose", "active_ra": True, "recent_crp_mg_L": 11.5, "biologic_started_within_30d": False},
            {"patient_id": "P007", "name": "Patel, Priya", "active_ra": True, "recent_crp_mg_L": 16.9, "biologic_started_within_30d": False},
            {"patient_id": "P008", "name": "Brown, Anna", "active_ra": True, "recent_crp_mg_L": 3.1, "biologic_started_within_30d": False},
            {"patient_id": "P009", "name": "Singh, Raj", "active_ra": True, "recent_crp_mg_L": 28.7, "biologic_started_within_30d": False},
            {"patient_id": "P010", "name": "Diaz, Carmen", "active_ra": True, "recent_crp_mg_L": 9.4, "biologic_started_within_30d": False},
        ]
    )
    cohort.index = range(1, len(cohort) + 1)
    return (cohort,)


@app.cell
def _(mo):
    crp_threshold = mo.ui.slider(start=3.0, stop=30.0, step=0.5, value=10.0, label="CRP threshold (mg/L) for at-risk-of-flare rule", show_value=True)
    crp_threshold
    return (crp_threshold,)


@app.cell
def _(cohort, crp_threshold):
    threshold = float(crp_threshold.value)
    rule_result = cohort.copy()
    rule_result["at_risk_of_flare"] = (
        rule_result["active_ra"]
        & (rule_result["recent_crp_mg_L"] > threshold)
        & ~rule_result["biologic_started_within_30d"]
    )
    return rule_result, threshold


@app.cell
def _(rule_result):
    rule_result
    return


@app.cell
def _(mo, rule_result, threshold):
    n_caught = int(rule_result["at_risk_of_flare"].sum())
    n_active_ra = int(rule_result["active_ra"].sum())
    rate = n_caught / len(rule_result) * 100
    mo.callout(
        mo.md(
            f"**At CRP threshold = {threshold:.1f} mg/L**, the rule identifies **{n_caught} of {len(rule_result)}** patients ({rate:.0f}% of the cohort, or {n_caught}/{n_active_ra} of the active-RA subset). Moving the slider changes the CRP cut-point and updates the result. Patient P003 is excluded by the biologic-started-within-30-days clause regardless of the threshold; P005 is excluded by the active-RA clause; both exclusions illustrate how a real CQL rule narrows the cohort by stacking criteria."
        ),
        kind="info",
    )
    return n_active_ra, n_caught, rate


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What the CQL idiom buys you, operationally

        Three operational consequences of the CQL approach for the institution.

        First, the same library can be tested against synthetic data in a sandbox before deployment. The CQL engine is independent of the EHR; the same library a deployed CDS service evaluates is the same library the test harness evaluates. A library that passes its tests in the sandbox produces the same answers in production.

        Second, the library can be updated centrally and republished. A CMS quality measure that changes for the next reporting cycle is republished as a new version of the same library. Sites pull the new version; their CDS services execute it without per-site re-implementation. The administrative cost of measure updates goes down materially.

        Third, the library is auditable. A regulator or a P&T committee asking "what does the rule do" is given the CQL source. The CQL is short and readable; the audit conversation centers on the rule's semantics rather than on which version of which institution's reporting workbench is in production.
        """
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "12",
        "06",
        "CQL as the layer above FHIR",
        "Course 06 covered FHIR (the data layer). CQL is the next layer up: logic written against FHIR. The FHIR resources Course 06 introduced are the input the CQL retrieve expressions operate on; the FHIR field names are the field expressions CQL field accesses use.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        CQL is the standards-based language for writing clinical-quality-measure and clinical-decision-rule logic. A CQL library is a named, versioned bundle of named expressions; the same library executes identically at any conformant site. CQL operates on the FHIR data model (Course 06) and depends on VSAC value sets (Course 07 vocabulary territory) for its terminology layer. The CMS122 fragment walked above is a representative published CQL measure; the small RA-flare rule above is a representative CDS rule. Three operational properties of CQL (sandbox-testable, centrally-republishable, auditable) make it the right rule-authoring layer for the modern CDS stack.

        Track 03 takes up CDS Hooks, the standards-based delivery layer that gets a CQL-implemented rule from a CDS service into the clinician's workflow at the right moment.
        """
    )
    return


if __name__ == "__main__":
    app.run()
