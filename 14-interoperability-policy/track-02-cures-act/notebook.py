"""Track 02: 21st Century Cures Act.

No visible code. The notebook presents the Cures Act Section 4004 statutory
definition, lists the ten current information-blocking exceptions, and runs
the reader through ten realistic scenarios in which one of the original
eight exceptions applies or no exception applies.

WASM-safe: no shared imports, no data files, no relative paths.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    SCENARIOS = {
        "A hospital declines to release a patient's records to a community-practice provider who has not signed the hospital's data-use agreement. The agreement is reasonable, addresses a real privacy concern, and is offered uniformly to every recipient.": {
            "exception": "Privacy",
            "analysis": (
                "The Privacy Exception permits practices that protect an individual's "
                "privacy when a sub-exception applies (a precondition not satisfied, a "
                "specific privacy law requires the practice, the individual has requested "
                "the restriction, or the actor's published privacy policies justify the "
                "practice). A reasonable, non-discriminatory DUA addressing a real privacy "
                "concern falls within the precondition sub-exception. An unreasonable or "
                "selectively applied DUA would not."
            ),
        },
        "An EHR vendor takes the patient-access API offline at 03:00 local time for 45 minutes to apply a security patch. During the window, third-party patient apps cannot fetch new data.": {
            "exception": "Security",
            "analysis": (
                "The Security Exception covers practices reasonably necessary to address "
                "security risks to the actor's IT, including time-limited maintenance to "
                "apply security patches. The practice must be tailored to the specific "
                "risk and limited in scope. A 45-minute patching window during low-use "
                "hours meets the tailoring standard."
            ),
        },
        "A practice declines to release records about a 14-year-old patient to a parent. State law gives the minor the right to consent to and protect the confidentiality of behavioral-health visits, and the visit being requested falls under that protection.": {
            "exception": "Privacy",
            "analysis": (
                "The Privacy Exception's precondition-not-satisfied sub-exception covers "
                "practices required by state or other applicable privacy law. When state "
                "law gives a minor the right to confidentiality for specific categories of "
                "care, withholding records that disclose those visits is required by the "
                "applicable law and therefore not blocking."
            ),
        },
        "A health system charges a research team $5,000 for a custom data extraction; the fee is documented as 40 hours of analyst time at the institutional rate plus storage and transfer costs.": {
            "exception": "Fees",
            "analysis": (
                "The Fees Exception permits cost-based, non-discriminatory fees that "
                "recover actual costs of providing the service, where the service is not "
                "a required electronic access pathway. A custom extraction requiring "
                "analyst time and infrastructure falls within the exception when the fee "
                "is documented at the actual cost of providing the service. A flat fee "
                "unrelated to cost would not."
            ),
        },
        "A vendor cannot deliver a non-USCDI data class (a sub-specialty registry data element) in the requested FHIR resource because the EHR does not capture the element in structured form anywhere in the system.": {
            "exception": "Infeasibility",
            "analysis": (
                "The Infeasibility Exception applies when fulfilling a request is "
                "technically not feasible, the actor has documented the infeasibility, "
                "and has offered alternatives where possible. A data element that does "
                "not exist in structured form in the source system meets the infeasibility "
                "standard. The actor still must respond to the requestor within 10 business "
                "days with a written explanation."
            ),
        },
        "A behavioral-health clinician declines to release psychotherapy session notes to the patient on documented clinical judgment that release at this point is likely to cause significant psychological harm.": {
            "exception": "Preventing Harm",
            "analysis": (
                "The Preventing Harm Exception permits practices reasonably necessary to "
                "prevent harm to the patient or to another person, provided the practice "
                "is tailored to the specific risk and the actor reasonably believes the "
                "harm is likely. Documenting the clinical judgment is what supports the "
                "exception under audit. HIPAA's separate psychotherapy-notes protections "
                "are aligned with this exception."
            ),
        },
        "A clinic responds to a records request by sending a CDA Continuity of Care Document instead of the requested FHIR Bundle, citing the EHR's current export capabilities. The CDA contains the same clinical content the request asked for.": {
            "exception": "Content and Manner",
            "analysis": (
                "The Content and Manner Exception permits an actor to fulfill a request "
                "in an alternative manner when the manner requested is not available, "
                "provided the alternative meets the standards in the regulation (a "
                "preferred standard, in production technical specifications, etc.) and is "
                "delivered in a timely manner. A CCD-for-FHIR substitution that delivers "
                "the same clinical content falls within the exception when the CCD is a "
                "permitted alternative format and the request is responded to within the "
                "required timeframe."
            ),
        },
        "A vendor charges a one-time fee to license a custom code system the EHR uses for a niche specialty registry. The fee is non-discriminatory and applied uniformly to every third party that wishes to interpret the codes.": {
            "exception": "Licensing",
            "analysis": (
                "The Licensing Exception permits licensing of interoperability elements "
                "(value sets, custom code systems, interface specifications) on "
                "reasonable, cost-based, and non-discriminatory terms. A one-time "
                "non-discriminatory fee for a custom code-system license meets the "
                "standard when the fee reflects the cost of supporting the licensing "
                "infrastructure."
            ),
        },
        "A hospital flatly refuses to send records to a specialist office because the specialist group competes with the hospital's employed specialists.": {
            "exception": "No exception applies",
            "analysis": (
                "Competitive concern is not within any exception. The practice is a clear "
                "case of information blocking: a deliberate restriction on electronic "
                "exchange undertaken because the recipient is a competitor. The hospital "
                "is the actor; the practice fails the effects-based definition; no "
                "exception covers it. This is the operational case the prohibition was "
                "written to address."
            ),
        },
        "An EHR vendor offers API access only through their proprietary app marketplace, charging $25,000 annually for third-party app inclusion regardless of app size or use.": {
            "exception": "No exception applies",
            "analysis": (
                "The Fees Exception requires fees to be cost-based; a flat $25,000 annual "
                "fee unrelated to actual cost of providing API access does not meet the "
                "standard. The Licensing Exception requires licensing terms to be "
                "reasonable and non-discriminatory; the practice may meet the uniformity "
                "test but not the reasonableness test. The practice interferes with the "
                "patient and provider use of third-party apps that the API certification "
                "criteria require to be accessible; it is information blocking by the "
                "developer."
            ),
        },
    }

    EXCEPTIONS_FOR_PICKER = [
        "Preventing Harm",
        "Privacy",
        "Security",
        "Infeasibility",
        "Health IT Performance",
        "Content and Manner",
        "Fees",
        "Licensing",
        "No exception applies",
    ]

    return EXCEPTIONS_FOR_PICKER, SCENARIOS, mo


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 02: 21st Century Cures Act

        The 21st Century Cures Act is a 2016 federal law that, alongside its FDA-reform and NIH-funding provisions, contained the statutory move the field had been describing for a decade without a name. Section 4004 of the Act prohibits information blocking and authorizes the Department of Health and Human Services to define the prohibition operationally. The 2020 ONC Cures Act Final Rule implements Section 4004, cataloguing the exceptions that distinguish blocking from legitimate restriction. This track presents the statute, the exceptions, and the question this regulatory framework forces every actor to answer: when a request is restricted or unfulfilled, which exception covers the practice, or does none?
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Section 4004 in plain English

        Section 4004 of the Cures Act adds new sub-sections to the Public Health Service Act (specifically 42 U.S.C. 300jj-52) that do three things.

        - **Define information blocking.** A practice by a health IT developer, health information network, health information exchange, or healthcare provider that, except as required by law or covered by an exception, is likely to interfere with the access, exchange, or use of electronic health information.
        - **Authorize implementing rules.** The Secretary of HHS, through ONC and OIG, is directed to issue rules that identify reasonable and necessary activities not considered information blocking (the exceptions) and to establish civil monetary penalties for developers and HIEs found to have engaged in blocking.
        - **Define knowledge standards.** Different actors carry different knowledge standards. Health IT developers, exchanges, and HIEs are liable when they engage in a practice that they "know or should know" is likely to interfere; healthcare providers are liable when they engage in a practice that they "know" is likely to interfere or that is "unreasonable."

        The statute is the upstream source; the operational form of the prohibition lives in ONC's regulations at 45 CFR Part 171.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The information-blocking exceptions

        ONC's 2020 Cures Act Final Rule catalogued eight exceptions. HTI-1 (the 2024 update) added two more, bringing the current total to ten. The eight original exceptions are the operational core of the framework; the two HTI-1 additions cover edges the original rule did not address.

        ### Original eight (2020 Cures Act Final Rule)

        | # | Exception | What it permits |
        |---|---|---|
        | 1 | **Preventing Harm** | Practices reasonably necessary to prevent harm to the patient or to another person, tailored to the specific risk. |
        | 2 | **Privacy** | Practices required by other privacy laws (state or federal), responsive to individual choice, or otherwise protecting privacy where conditions in the exception are met. |
        | 3 | **Security** | Practices reasonably necessary to address security risks to the actor's IT, tailored to the specific risk. |
        | 4 | **Infeasibility** | Practices where fulfilling a request is technically not feasible. Requires written explanation to the requestor within 10 business days. |
        | 5 | **Health IT Performance** | Time-limited practices necessary to maintain or improve the performance of health IT, planned and communicated. |
        | 6 | **Content and Manner** | Permitted alternative content or delivery format when the requested form is not available, provided the alternative meets specified standards. |
        | 7 | **Fees** | Cost-based, non-discriminatory fees for permitted services. Required electronic access services are largely outside the exception. |
        | 8 | **Licensing** | Licensing of interoperability elements (value sets, code systems, specifications) on reasonable, cost-based, non-discriminatory terms. |

        ### Added by HTI-1 (2024)

        | # | Exception | What it permits |
        |---|---|---|
        | 9 | **Protecting Care Access** | Practices reasonably necessary to mitigate risks to patients or providers when access to lawful care (notably reproductive-health care) could create legal or safety risk. |
        | 10 | **TEFCA Manner** | Permits use of TEFCA exchange as a valid manner of fulfilling a request, even when other manners might also be requested. |

        Each exception has its own conditions; meeting the exception requires meeting every condition the regulation specifies. Reading the regulation at 45 CFR Part 171 is the operational practice.
        """
    )
    return


@app.cell
def _(EXCEPTIONS_FOR_PICKER, SCENARIOS, mo):
    scenario_pick = mo.ui.dropdown(
        options=list(SCENARIOS.keys()),
        value=list(SCENARIOS.keys())[0],
        label="Scenario",
    )
    exception_pick = mo.ui.dropdown(
        options=EXCEPTIONS_FOR_PICKER,
        value=EXCEPTIONS_FOR_PICKER[0],
        label="Which exception covers this practice?",
    )
    mo.vstack(
        [
            mo.md(
                "## Match a scenario to an exception\n\n"
                "**Pick a scenario, then pick the exception you think covers it (or "
                "\"No exception applies\" for a clear blocking case).** The reactive "
                "panel below confirms the right reading and walks the reasoning."
            ),
            scenario_pick,
            exception_pick,
        ]
    )
    return exception_pick, scenario_pick


@app.cell
def _(SCENARIOS, exception_pick, mo, scenario_pick):
    _info = SCENARIOS[scenario_pick.value]
    _correct = _info["exception"]
    _chosen = exception_pick.value
    if _chosen == _correct:
        _verdict = f"**Correct: {_correct}.**"
        _kind = "success"
    else:
        _verdict = f"**The right reading is {_correct}.** (You picked {_chosen}.)"
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
        ## What changed in practice, and what did not

        The Cures Act information-blocking provisions, with the 2020 Final Rule giving them operational form and the 2023 OIG rule attaching civil monetary penalties, changed several things that were observable within two or three years.

        - **API access pricing**. Charges for setting up standardized patient-access APIs largely disappeared from vendor contracts; the previous $20,000 to $100,000 setup fees became defensively cost-based or non-existent.
        - **Patient-portal scope**. Test results, clinical notes, and imaging reports became visible to patients on release (the "open notes" provisions effectively required by the Final Rule), changing the patient-facing portal from a partial view to a substantively complete one.
        - **Third-party app access**. SMART on FHIR app launch became a baseline expectation rather than a negotiated vendor feature. App marketplaces remained, but the gating fees on app inclusion came under scrutiny.

        Several things did not change.

        - **State consent law variation**. Twenty-some states retain consent requirements stricter than HIPAA for behavioral-health, HIV, and substance-use information; the Cures Act did not preempt these.
        - **Patient matching**. The 1999 appropriations rider on a national patient identifier remained in place, leaving cross-organizational matching to probabilistic algorithms (Track 05).
        - **The 42 CFR Part 2 substance-use disclosure framework**. Part 2 was amended separately in 2020 and 2024; the alignment with HIPAA and the Cures Act is closer than before but not complete.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Where this goes next

        The Cures Act is the statute. The Cures Act Final Rule and HTI-1 are the ONC implementing regulations. The CMS Interoperability and Patient Access Final Rule and the 2024 Advancing Interoperability and Improving Prior Authorization Final Rule are the parallel payer-facing implementing regulations from CMS. Track 03 covers all four rules together, the standards they require, and the convergence on FHIR R4 that produced the 2020-to-2024 adoption curve.
        """
    )
    return


if __name__ == "__main__":
    app.run()
