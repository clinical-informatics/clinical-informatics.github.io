"""Track 01: How claims data is structured.

A claim is the bill the provider sends to the payer for a service rendered.
The claim record is structured to satisfy billing and contractual
requirements, not to capture the clinical encounter. The track addresses
the structure, shows Ms. Reyes's 2024-01-08 office visit as the 7 claim
rows it actually produces in her claims data, and frames the clinical-vs-
claim gap that drives most of the common errors in claims-based research.
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

    _COURSE_TITLES = {
        "05": "EHR systems",
        "07": "Data wrangling and engineering",
        "14": "Interoperability and policy",
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

    _WASM_DATA_BASE = "/11-health-economics-data/track-01-claims-data/app"

    def load_cached_csv(filename):
        if "pyodide" in sys.modules:
            from pyodide.http import open_url
            url = f"{_WASM_DATA_BASE}/cache/{filename}"
            return pd.read_csv(open_url(url))
        return pd.read_csv(Path(__file__).parent / "cache" / filename)

    return load_cached_csv, mo, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 01: How claims data is structured

        ## The premise: a claim is the bill, not the encounter

        A claim is the structured record a provider sends to a payer to be paid for a service that was delivered. The claim has a date of service, the codes that identify what was done (CPT or HCPCS for procedures and services, ICD-10 for diagnoses), the place of service, the rendering provider's NPI, the units, and three dollar amounts (the amount the provider billed, the amount the payer's contract allows, and the amount the payer actually paid). The patient-responsibility amount is the difference between the allowed amount and the paid amount.

        The claim is not the clinical record. The claim records that a service was rendered and that it was billable; it does not record why the service was done, what was found, or what the clinician concluded. A query against the structured EHR returns the conclusion (the diagnosis on the problem list, the lab result); a query against the claims returns the bill that the visit produced. The two views overlap but are not interchangeable, and the gap is the source of most of the common errors in claims-based research.

        The track walks the structure of a claim, shows Ms. Reyes's 2024-01-08 office visit as the 7 claim rows it actually produces, and frames the institutional vs professional split, the 837 transaction-set background, and the clinical-vs-claim gap.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The fields a claim carries

        Every claim line has the same shape. The fields below appear on every line of every professional claim in the US.
        """
    )
    return


@app.cell
def _(pd):
    claim_fields = pd.DataFrame(
        [
            {"Field": "claim_id", "What it identifies": "The line-item identifier. One claim row per service rendered, not one claim per visit. A single visit produces several rows."},
            {"Field": "patient_id", "What it identifies": "The patient. In real claims data this is a payer-assigned member ID, not the EHR's MRN."},
            {"Field": "service_date", "What it identifies": "The date the service was rendered. The claim's natural time index."},
            {"Field": "place_of_service", "What it identifies": "A two-digit POS code (CMS Form 1500 field 24B). 11 is office; 21 is inpatient hospital; 22 is outpatient hospital; 23 is emergency department; 02 is telehealth-home."},
            {"Field": "provider_npi", "What it identifies": "The National Provider Identifier of the rendering clinician. Ten-digit numeric identifier issued by CMS."},
            {"Field": "cpt_or_hcpcs", "What it identifies": "The procedure code. CPT (Current Procedural Terminology, AMA) for most services; HCPCS Level II for supplies, drugs, and DME."},
            {"Field": "icd10", "What it identifies": "The diagnosis code that justifies the procedure. ICD-10-CM, US clinical modification."},
            {"Field": "units", "What it identifies": "How many units of the service were rendered (for drugs, the number of doses; for time-based codes, the number of 15-minute increments)."},
            {"Field": "allowed_amount", "What it identifies": "The amount the payer's contract with the provider permits as payment for this service. The reimbursement ceiling."},
            {"Field": "paid_amount", "What it identifies": "The amount the payer actually paid the provider. Equal to the allowed amount minus the patient-responsibility amount."},
            {"Field": "patient_responsibility", "What it identifies": "The amount the patient owes, as copay, coinsurance, or deductible. Equal to allowed_amount minus paid_amount."},
        ]
    )
    claim_fields.index = range(1, len(claim_fields) + 1)
    claim_fields.index.name = "row"
    claim_fields
    return (claim_fields,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three properties of the claim record are load-bearing.

        First, a visit produces multiple claim lines, one per billable service. A standard office visit that includes a 99214 evaluation-and-management code, three labs, and an ECG produces five claim lines, not one. Joining at the visit level requires grouping the claim lines by patient and service date.

        Second, the three dollar amounts always agree: `allowed = paid + patient_responsibility`. The billed amount (what the provider asked for) is usually higher than the allowed amount; the difference is the contractual write-off. The billed amount is rarely the relevant economic quantity.

        Third, every claim line has its own ICD-10 diagnosis. Most claims data systems also carry a primary diagnosis at the encounter level, but the line-level diagnosis is what justifies the specific service. The line-level diagnosis is sometimes different from the encounter-level diagnosis, especially for screening labs ordered alongside a primary visit.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Worked example: Reyes's 2024-01-08 office visit

        Ms. Reyes's January 2024 rheumatology visit produces 7 claim lines. The lines below are loaded directly from her `claims.csv` and rendered in the order they appear in the file.
        """
    )
    return


@app.cell
def _(load_cached_csv, pd):
    claims_all = load_cached_csv("claims.csv")
    claims_all["service_date"] = pd.to_datetime(claims_all["service_date"])
    reyes_jan8 = claims_all[claims_all["service_date"] == "2024-01-08"].copy().reset_index(drop=True)
    reyes_jan8.index = range(1, len(reyes_jan8) + 1)
    reyes_jan8[["claim_id", "cpt_or_hcpcs", "procedure_description", "icd10", "allowed_amount", "patient_responsibility", "paid_amount"]]
    return claims_all, reyes_jan8


@app.cell
def _(mo, reyes_jan8):
    total_allowed = float(reyes_jan8["allowed_amount"].sum())
    total_paid = float(reyes_jan8["paid_amount"].sum())
    total_pt_resp = float(reyes_jan8["patient_responsibility"].sum())
    mo.md(
        f"""
        **One visit, seven lines, three dollar totals.** Total allowed across the 7 lines: **${total_allowed:.2f}**. Total paid by the payer: **${total_paid:.2f}**. Total patient responsibility: **${total_pt_resp:.2f}**. Note that the patient owes nothing on six of the seven lines because they are labs (zero patient cost-share on this plan); the entire $30 patient-responsibility falls on the office-visit E/M code (CPT 99214) and represents the visit copay.
        """
    )
    return total_allowed, total_paid, total_pt_resp


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Institutional vs professional claims

        US claims come in two flavors that travel on two different forms with two different transaction sets.

        - **Professional claims** are submitted on CMS-1500 (the paper form) or the 837P EDI transaction set. One claim line per service rendered by a physician or other professional. Every claim row in Reyes's claims data is a professional claim.
        - **Institutional claims** are submitted on UB-04 (the paper form) or the 837I EDI transaction set. Institutional claims report charges from facilities (hospitals, ambulatory surgery centers, skilled nursing facilities). An institutional claim for a hospitalization typically rolls many services into a small number of lines, often one per revenue code per day.

        The two flavors are joined at the encounter level by the patient ID and the date range, but they answer different questions. A query for "what did this hospitalization cost" needs the institutional claims (the facility's charges); a query for "who saw the patient and what did they do" needs the professional claims (the consults, the imaging interpretations, the inpatient E/M visits). Both are needed for a complete cost-of-care picture.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A brief note on the EDI standards

        The claims data structure was not designed for analytics. It was designed in the 1990s as a structured replacement for the paper forms (CMS-1500 and UB-04) that providers had been mailing to payers for decades. The structured replacement is the X12 EDI 837 transaction set: 837P for professional, 837I for institutional, 837D for dental.

        The 837 specification is published by the Accredited Standards Committee X12. It is the canonical reference for the field-by-field structure of a claim. Most analysts never read the 837 spec directly; payers and clearinghouses transform 837 messages into flat tables (the shape of Reyes's `claims.csv`) before analysis. Knowing the 837 background is useful when a field's meaning is ambiguous, when a vendor's data dictionary refers to a loop or segment, or when the cleanest fix is at the EDI layer rather than downstream.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The clinical-vs-claim gap

        Four categories of question are best answered from the clinical EHR record, not from claims. A claims query for any of them will produce a structurally valid answer that is clinically wrong by an amount the query cannot expose.

        - **Severity of disease.** A claim says the patient has rheumatoid arthritis (ICD-10 M05.79). It does not say the patient has a DAS28 of 4.1 with active synovitis at 6 joints. A claim cannot rank patients by disease severity.
        - **Reason for a medication change.** A claim says the patient started adalimumab. It does not say the patient started adalimumab because MTX failed at 25 mg weekly with persistent CRP of 19. A claim cannot distinguish a planned escalation from a switch due to intolerance.
        - **Clinical context for a test.** A claim says a vitamin D level was drawn (CPT 82306). It does not say the test was ordered because the patient reported falls (relevant) or because it appeared on a routine wellness panel (less relevant for the same researcher).
        - **Outcome.** A claim says a patient had an infusion (CPT J0135). It does not say whether the infusion produced a clinical response or an adverse event. Claims-based outcome measures are proxies (re-hospitalization, drug switch, persistence) that may or may not reflect the clinical outcome of interest.

        Two operational consequences follow.

        First, claims-based research requires explicit operational definitions that translate the clinical question into claim-level criteria. The published methods literature (Sentinel, PCORnet, OHDSI cohort definitions) provides curated, validated operational definitions for many clinical conditions; these should be preferred over ad-hoc definitions in any high-stakes analysis.

        Second, when a clinical-record source is available alongside claims, the right architecture usually combines them: claims for the denominator and the cost side, EHR for the severity, the context, and the outcome. The Sentinel Common Data Model and the OMOP CDM are both designed for this kind of joint use.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "11",
        "05",
        "Claims as a secondary-use data source",
        "Course 05 Track 3 introduced the clinical data warehouse (CDW) as the analytic layer downstream of the operational EHR. Claims are the parallel analytic layer downstream of the billing operation. Most institutions maintain both a CDW and a claims database, and the high-quality analytic work joins them.",
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "11",
        "07",
        "OMOP / Sentinel vs claims structure",
        "Course 07 Track 2 introduced the OMOP CDM. Claims fit into OMOP cleanly: every claim line becomes a `cost` row plus the corresponding clinical-table row (`condition_occurrence`, `procedure_occurrence`, `drug_exposure`). The Sentinel CDM is claims-first by design and has a complementary structure. Either is a defensible target for a claims-research warehouse.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        A claim is the structured bill the provider sends to the payer. A claim has a fixed shape (line-item identifiers, dates, places of service, procedure and diagnosis codes, dollar amounts) and a defined separation from the clinical record. Reyes's 2024-01-08 office visit produces 7 claim lines: one E/M code plus 6 lab codes, with $30 in patient copay against the office visit and zero patient cost-share on the labs. The US claims ecosystem distinguishes professional from institutional claims (CMS-1500 / 837P vs UB-04 / 837I); both are needed for a complete cost-of-care picture. The clinical-vs-claim gap is the source of most claims-research errors; the remedy is to use curated operational definitions and, where possible, to join claims with the EHR record.

        Track 02 takes up the cost and utilization vocabulary that aggregates these line-level claim records into the measures (total cost of care, PMPM, utilization rates) that drive institutional and payer reporting.
        """
    )
    return


if __name__ == "__main__":
    app.run()
