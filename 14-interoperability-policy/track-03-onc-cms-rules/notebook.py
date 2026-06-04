"""Track 03: ONC and CMS interoperability rules.

No visible code. The notebook presents the four federal rules that converge
on FHIR R4 (the 2020 ONC Cures Act Final Rule, the 2024 HTI-1 Final Rule,
the 2020 CMS Patient Access Final Rule, and the 2024 Advancing
Interoperability and Improving Prior Authorization Final Rule), runs the
reader through ten requirements and asks which rule each lives in, and
closes on the USCDI evolution that determines what those APIs carry.

WASM-safe: no shared imports, no data files, no relative paths.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    REQUIREMENTS = {
        "Standardized FHIR R4 patient-access API for certified EHRs": {
            "rule": "ONC Cures Act Final Rule (2020)",
            "analysis": (
                "The 2020 Cures Act Final Rule's Conditions and Maintenance of "
                "Certification require certified EHRs to provide a FHIR R4 API for "
                "patient and population services. The API is the certification "
                "criterion 170.315(g)(10) (the standardized API for patient and "
                "population services). HTI-1 (2024) extended the data scope but "
                "did not change the API requirement itself."
            ),
        },
        "SMART App Launch (OAuth 2.0) authorization for patient access to certified EHRs": {
            "rule": "ONC Cures Act Final Rule (2020)",
            "analysis": (
                "The 170.315(g)(10) certification criterion adopted the SMART App "
                "Launch Implementation Guide as the authorization mechanism for the "
                "patient-access API. The SMART flow Course 06 Track 5 covered is the "
                "same OAuth 2.0 authorization-code flow that certified EHRs are now "
                "required to support."
            ),
        },
        "USCDI v3 as the certified data set for certified health IT": {
            "rule": "ONC HTI-1 Final Rule (2024)",
            "analysis": (
                "HTI-1 advanced the certified-EHR data set from USCDI v1 (the 2020 "
                "Final Rule baseline) to USCDI v3, with timelines for certified IT "
                "developers to update their products. Subsequent rulemaking (since "
                "USCDI v4, v5, v6) continues the advancement on an annual cadence."
            ),
        },
        "Decision Support Intervention (DSI) source attribute disclosures for predictive models in certified EHRs": {
            "rule": "ONC HTI-1 Final Rule (2024)",
            "analysis": (
                "HTI-1 added the DSI transparency requirements. Certified developers "
                "that integrate DSIs (rule-based or predictive, including AI/ML) into "
                "their products must disclose specified source attributes for each DSI: "
                "intervention name, purpose, data inputs, intended use, output type, "
                "training population, performance characteristics, and subgroup "
                "performance. The requirements are the algorithmic-transparency floor "
                "Course 09 connects to."
            ),
        },
        "CMS-regulated payers must operate a Patient Access API for enrollee claims and clinical data": {
            "rule": "CMS Interoperability and Patient Access Final Rule (CMS-9115-F, 2020)",
            "analysis": (
                "CMS-9115-F requires CMS-regulated payers (Medicare Advantage, "
                "Medicaid managed care, CHIP managed care, ACA exchange plans) to "
                "operate a Patient Access API on FHIR R4. The API gives enrollees "
                "programmatic access to their claims data and a subset of clinical "
                "data; SMART on FHIR is the authorization mechanism."
            ),
        },
        "CMS-regulated payers must publish a Provider Directory API": {
            "rule": "CMS Interoperability and Patient Access Final Rule (CMS-9115-F, 2020)",
            "analysis": (
                "CMS-9115-F also requires a Provider Directory API on FHIR R4, "
                "exposing the payer's network providers (name, NPI, specialty, "
                "address, electronic contact) to third-party apps and tools, without "
                "the access controls the Patient Access API has."
            ),
        },
        "Payers must support Payer-to-Payer data exchange when an enrollee changes plans": {
            "rule": "CMS Interoperability and Patient Access Final Rule (CMS-9115-F, 2020)",
            "analysis": (
                "The 2020 rule established the Payer-to-Payer exchange requirement "
                "with USCDI data classes carried over from the prior plan. The 2024 "
                "CMS-0057-F rule expanded the exchange to include the prior "
                "authorization information and put the exchange on a FHIR-based "
                "specification."
            ),
        },
        "Payers must operate a Prior Authorization API exposing requirements and decisions on FHIR": {
            "rule": "CMS Advancing Interoperability and Improving Prior Authorization Final Rule (CMS-0057-F, 2024)",
            "analysis": (
                "CMS-0057-F requires CMS-regulated payers to operate a FHIR-based "
                "Prior Authorization API that exposes prior-authorization "
                "requirements, automates submission, and returns decisions in "
                "structured form. Effective dates start in 2026 and 2027. The "
                "specification is built on the HL7 Da Vinci Prior Authorization "
                "Support (PAS) IG."
            ),
        },
        "Payers must operate a Provider Access API exposing enrollee data to in-network providers": {
            "rule": "CMS Advancing Interoperability and Improving Prior Authorization Final Rule (CMS-0057-F, 2024)",
            "analysis": (
                "CMS-0057-F added a Provider Access API that exposes enrollee "
                "claims and clinical data to a provider currently treating the "
                "patient, on FHIR R4. The mechanism complements the Patient Access "
                "API by giving providers a programmatic route to payer data without "
                "going through the patient."
            ),
        },
        "Certified IT developers must not engage in information-blocking practices as a condition of certification": {
            "rule": "ONC Cures Act Final Rule (2020)",
            "analysis": (
                "The Conditions and Maintenance of Certification in the 2020 Final "
                "Rule include an information-blocking condition: certified IT "
                "developers must attest that they do not engage in practices that "
                "constitute information blocking. A finding of blocking can result "
                "in decertification, in addition to the civil monetary penalties "
                "under the 2023 OIG rule."
            ),
        },
    }

    RULES = [
        "ONC Cures Act Final Rule (2020)",
        "ONC HTI-1 Final Rule (2024)",
        "CMS Interoperability and Patient Access Final Rule (CMS-9115-F, 2020)",
        "CMS Advancing Interoperability and Improving Prior Authorization Final Rule (CMS-0057-F, 2024)",
    ]

    return REQUIREMENTS, RULES, mo


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 03: ONC and CMS interoperability rules

        Why did FHIR adoption accelerate so rapidly between 2020 and 2024? The technical case for FHIR R4 over HL7 v2 had been clear for several years. The proximate cause of acceleration was regulatory: four federal rules from two HHS agencies converged on FHIR R4 and on a shared baseline data set (USCDI). The 2020 ONC Cures Act Final Rule and the 2020 CMS Interoperability and Patient Access Final Rule together made FHIR R4 the required wire format for certified EHRs and for CMS-regulated payers, and the 2024 HTI-1 Final Rule and CMS-0057-F extended the data scope and the use cases. This track presents the four rules, the convergence framing, and the path from the rules to the FHIR resources Course 06 covered.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The four rules at a glance

        Two HHS agencies issue the rules that mandate interoperability. ONC governs certified health IT (the EHR and EHR-adjacent products that providers buy). CMS governs Medicare and Medicaid (the largest payer relationships in the country, plus the qualified health plans on the ACA exchanges). Both have current rules that mandate FHIR R4.

        | Year | Rule | Agency | What it covers |
        |---|---|---|---|
        | 2020 | **ONC Cures Act Final Rule** (45 CFR Part 170, 171) | ONC | Information blocking definition and exceptions; Conditions and Maintenance of Certification; the 170.315(g)(10) standardized API for patient and population services (FHIR R4 + SMART). |
        | 2024 | **ONC HTI-1 Final Rule** | ONC | USCDI v3 baseline (now extended); Decision Support Intervention transparency for AI and rule-based CDS in certified EHRs; updates to the information-blocking exceptions. |
        | 2020 | **CMS Interoperability and Patient Access Final Rule** (CMS-9115-F) | CMS | Patient Access API, Provider Directory API, Payer-to-Payer exchange for CMS-regulated payers (Medicare Advantage, Medicaid managed care, CHIP managed care, ACA exchanges). FHIR R4 + SMART. |
        | 2024 | **CMS Advancing Interoperability and Improving Prior Authorization Final Rule** (CMS-0057-F) | CMS | Prior Authorization API, Provider Access API, expanded Payer-to-Payer API. FHIR R4. Effective dates 2026 and 2027. |
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The convergence on FHIR R4

        Both regulatory tracks point at the same wire format and the same baseline data set. Two structural reasons explain why.

        **The standard had to be the same to be useful.** A patient-access API exposed by a certified EHR and a Patient Access API exposed by a CMS-regulated payer have to speak the same protocol if a patient app is going to talk to both. FHIR R4 was already the practical choice; the regulations cemented it across the two endpoint classes.

        **The data set had to be the same to be portable.** USCDI defines what an EHR or a payer has to be able to expose; the same data classes appear on both the certified-EHR side (the 170.315(g)(10) API) and the payer side (the Patient Access API). A patient app that fetches "all my conditions" from an EHR and from a payer gets two structurally compatible answers.

        This is the regulatory dual that produced the 2020 to 2024 FHIR adoption curve. The technical merit of FHIR was a precondition; the convergent regulatory mandate is what made adoption a reimbursement-tied requirement rather than an option.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            **Cross-reference (Course 06, FHIR).** Every API the rules mandate is built on the FHIR resources Course 06 covered. The 170.315(g)(10) certification API exposes Patient, Observation, Condition, MedicationRequest, AllergyIntolerance, Procedure, and the rest of the USCDI-aligned resources from Tracks 1, 2, and 3 of that course. The SMART App Launch flow from Track 5 of Course 06 is the authorization mechanism for both the ONC patient-access API and the CMS Patient Access API. Implementation guides (Track 4 of Course 06) are the concrete specification for each FHIR-based API the rules require, and the relationship of US Core (Course 06 Track 4) to USCDI is direct: US Core is the FHIR profiling of USCDI data classes for U.S. certified IT.
            """
        ),
        kind="info",
    )
    return


@app.cell
def _(REQUIREMENTS, RULES, mo):
    requirement_pick = mo.ui.dropdown(
        options=list(REQUIREMENTS.keys()),
        value=list(REQUIREMENTS.keys())[0],
        label="Requirement",
    )
    rule_pick = mo.ui.dropdown(
        options=RULES,
        value=RULES[0],
        label="Which rule mandates this?",
    )
    mo.vstack(
        [
            mo.md(
                "## Match the requirement to the rule\n\n"
                "**Pick a requirement, then pick the rule you think mandates it.** "
                "The reactive panel below confirms the right rule and walks the "
                "specific provision."
            ),
            requirement_pick,
            rule_pick,
        ]
    )
    return requirement_pick, rule_pick


@app.cell
def _(REQUIREMENTS, mo, requirement_pick, rule_pick):
    _info = REQUIREMENTS[requirement_pick.value]
    _correct = _info["rule"]
    _chosen = rule_pick.value
    if _chosen == _correct:
        _verdict = f"**Correct: {_correct}.**"
        _kind = "success"
    else:
        _verdict = f"**The right rule is {_correct}.** (You picked {_chosen}.)"
        _kind = "warn"
    mo.callout(
        mo.md(f"{_verdict} {_info['analysis']}"),
        kind=_kind,
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The USCDI baseline: what the APIs carry

        The rules mandate the wire format and the authorization mechanism, but the substantive data set is USCDI (United States Core Data for Interoperability). USCDI evolves on roughly an annual cadence, with each version adding data classes that respond to clinical and policy demand. The version history is the operational measure of what an EHR or a payer has to be able to expose.

        | Version | Year | Notable additions |
        |---|---|---|
        | v1 | 2020 | The original baseline. Patient demographics, allergies, problems, procedures, medications, immunizations, laboratory results, vital signs, smoking status, clinical notes, and the encounter context. |
        | v2 | 2021 | Sexual orientation, gender identity, encounter information. |
        | v3 | 2022 | Social determinants of health, health insurance information, related-person data. |
        | v4 | 2023 | Substance use, advance directives, encounter detail expansions. |
        | v5 | 2024 | Behavioral health data classes, expanded clinical notes, expanded SDOH. |
        | v6 | July 2025 | Encounter outcome, immunization administration detail, expanded patient-reported outcomes. |
        | v7 (draft) | early 2026 | Forthcoming data classes responding to AI-output structuring and additional behavioral health detail. |

        The advancement to a new USCDI version becomes a binding requirement when an ONC rulemaking (HTI-1, HTI-2, or a subsequent rule) adopts that version as the certification baseline. Adoption typically lags publication by 12 to 24 months, and full availability in production EHRs typically lags adoption by another 12 to 36 months as vendors update certified products.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Where this goes next

        The U.S. policy framework is one configuration of the broader interoperability problem. Track 04 puts it in context with the European Union framework (GDPR plus the European Health Data Space) and the United Kingdom approach (a single-payer system with a universal patient identifier). The international comparison clarifies which features of the U.S. framework are policy choices and which are constraints of the U.S. legal and market structure.
        """
    )
    return


if __name__ == "__main__":
    app.run()
