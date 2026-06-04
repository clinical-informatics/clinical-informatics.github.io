"""Track 01: Why policy exists.

No visible code. The notebook defines information blocking, presents the
HITECH precondition that produced the policy demand, and runs the reader
through eight realistic scenarios in which a practice may or may not meet
the statutory definition of information blocking.

WASM-safe: no shared imports, no data files, no relative paths.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    SCENARIOS = {
        "A vendor charges $50,000 to set up a patient-access FHIR API endpoint for a primary-care practice with 8,000 patients.": {
            "blocking": True,
            "analysis": (
                "The Fees Exception allows reasonable, cost-based fees for certain "
                "services. A $50,000 setup fee for a standardized patient-access API "
                "that ONC requires the vendor to support is not cost-based; it is "
                "rent-extraction on a mandated capability. The Fees Exception does not "
                "apply. This is information blocking by the developer."
            ),
        },
        "A specialist requests records from another primary-care practice using a paper fax form; the records arrive three weeks later in PDF.": {
            "blocking": True,
            "analysis": (
                "Fax-only release when electronic exchange is technically available is "
                "itself an interference with electronic access. The Cures Act's "
                "information-blocking definition covers practices likely to interfere "
                "with access, exchange, or use of electronic health information; the "
                "blocking practice is the disposition of the request, not the technology "
                "of the responding system. No exception applies. The responding practice "
                "is the actor."
            ),
        },
        "A hospital declines to send laboratory results to a competing health system that has not signed the hospital's data-use agreement, where the agreement is reasonable and offered on the same terms to every requester.": {
            "blocking": False,
            "analysis": (
                "Requiring a reasonable data-use agreement before disclosing protected "
                "health information to a recipient may fall within the Privacy Exception "
                "if the agreement reflects a legitimate privacy or security concern, is "
                "tailored to the specific risk, and is offered on non-discriminatory "
                "terms. A reasonable DUA applied uniformly meets this standard. An "
                "unreasonable or discriminatory DUA would not."
            ),
        },
        "A practice refuses to give a patient a copy of their own records because the patient has an outstanding balance for prior visits.": {
            "blocking": True,
            "analysis": (
                "The HIPAA right of access (45 CFR 164.524) prohibits conditioning a "
                "patient's right to access their own records on payment for healthcare "
                "services. The Cures Act information-blocking provisions reinforce this: "
                "a balance-due withholding is not within any exception. The practice is "
                "also a HIPAA Privacy Rule violation, which has its own enforcement "
                "pathway through OCR."
            ),
        },
        "An EHR vendor provides FHIR API access to third-party apps only if the app developer pays an annual $25,000 registration fee, applied uniformly to every app.": {
            "blocking": True,
            "analysis": (
                "Uniform application does not by itself satisfy the Fees Exception. The "
                "exception permits cost-based, non-discriminatory fees that recover "
                "actual costs of the service. A flat $25,000 annual fee for app "
                "registration on an established platform is rarely cost-based, and the "
                "fee structure interferes with patient and provider use of third-party "
                "apps, which the API certification criteria require to be accessible."
            ),
        },
        "A research-grant team requests a complete EHR extract for 1,200 rheumatoid-arthritis patients. The health system charges a $3,500 cost-recovery fee covering analyst time and infrastructure for the custom extraction.": {
            "blocking": False,
            "analysis": (
                "Cost-based recovery fees for non-required services (such as bulk "
                "research extractions that require analyst time) are permitted under the "
                "Fees Exception if the fee is reasonable, cost-based, and applied "
                "non-discriminatorily. A $3,500 fee for a 1,200-patient extraction with "
                "analyst time included falls within the exception. The fee for the "
                "required electronic services (the patient-access API) would still need "
                "to meet the cost-based standard separately."
            ),
        },
        "A behavioral-health clinician declines to release session notes to a patient on the clinician's documented clinical judgment that release at this point is likely to cause significant psychological harm.": {
            "blocking": False,
            "analysis": (
                "The Preventing Harm Exception permits practices reasonably necessary to "
                "prevent harm to the patient or to another person, provided the practice "
                "is tailored to the specific risk and the actor reasonably believes the "
                "harm is likely to occur. Behavioral-health clinicians retain the "
                "prerogative the HIPAA Privacy Rule already grants for psychotherapy "
                "notes; the Cures Act exception aligns with that authority. Documenting "
                "the clinical judgment is what supports the exception under audit."
            ),
        },
        "A hospital takes four weeks to respond to a records request because the EHR vendor's bulk-export tool runs only as a monthly batch. The hospital is on the latest certified version of the EHR.": {
            "blocking": True,
            "analysis": (
                "The four-week delay is the operational effect of the practice; the "
                "underlying cause may sit with the vendor (a configuration that runs "
                "export only monthly is interfering with electronic access) or with the "
                "hospital (a policy that queues requests). Both actors may be subject to "
                "investigation. The Infeasibility Exception is narrowly applied and does "
                "not cover routine operational delays. Routine technical limitations "
                "that interfere with timely access fall within the prohibition."
            ),
        },
    }

    return SCENARIOS, mo


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 01: Why policy exists

        A clinician asks for a patient's laboratory results from another health system. The records arrive only by fax, three weeks later, in PDF, unreadable in the EHR's external-document tab. None of this is a technical limitation; the technical capability to exchange the data exists on both sides. It is a set of choices that one or more parties made. The 21st Century Cures Act, signed in 2016 and implemented through ONC's Cures Act Final Rule in 2020, gave that set of choices a federal name: **information blocking**. This track covers what the term names, the precondition that produced it, who was benefiting from the status quo, and why the policy response took the form it did.

        The structural defense against information blocking is the rest of this course. Tracks 02 and 03 cover the statutes and rules that prohibit it; Track 04 places the U.S. response in international context; Track 05 names what is still broken.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Information blocking, defined operationally

        The 21st Century Cures Act Section 4004 defines information blocking, and ONC's 2020 Final Rule at 45 CFR Part 171 implements the definition. The operational form:

        > A practice by a health IT developer, health information network, health information exchange, or healthcare provider that, except as required by law or covered by an exception, is **likely to interfere with the access, exchange, or use of electronic health information**.

        Three features of the definition deserve attention. The definition is **effects-based**: a practice that interferes with electronic access can be information blocking even when no malicious intent is documented. It applies to **four actor classes** (developers, networks, HIEs, providers), with somewhat different knowledge and enforcement standards for each. And it operates against **electronic health information**, the statutory term that USCDI (Track 03) makes operational.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The HITECH precondition

        Information blocking is the problem federal policy named in 2016, but it could only become a problem worth naming because the precondition existed: the data was electronic and present in nearly every clinical setting. The HITECH Act of 2009 funded the Meaningful Use incentive program (Medicare and Medicaid paid clinicians and hospitals to adopt and use certified EHRs), and the adoption curve that followed is what made information blocking a federal-policy question rather than a market curiosity.

        | Year | Office-based physician EHR adoption | Hospital EHR adoption |
        |---|---|---|
        | 2008 (pre-HITECH) | 17% | 9% |
        | 2014 | 75% | 96% |
        | 2021 | 88% | 96% |

        (Figures from ONC's Health IT Dashboard, rounded.) By the mid-2010s, the data existed in standards-conformant systems. The remaining barriers to its movement were therefore by definition policy and economic, not technical. That is the framing the Cures Act response was built on.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Who was benefiting from the status quo

        Naming a policy problem is a useful exercise because the analysis surfaces who is benefiting from the current arrangement. Two parties were structurally on the gaining side of the pre-2020 status quo.

        **Health-IT developers** were on the gaining side when access to their data was a billable service rather than a mandated capability. Charging a setup fee for an API endpoint, charging app developers for marketplace access, charging providers for export tooling: each was a revenue stream that depended on data being hard to move.

        **Healthcare providers** were on the gaining side when their patient records did not flow easily to competing health systems. A patient who could not get their records out also could not switch providers easily; data friction was a soft form of patient retention. The information-asymmetry argument applied to providers as well as to developers.

        The Cures Act prohibition does not require proof that either party intended harm. It targets the practices that produce the effects, regardless of whether the producer was acting on a deliberate strategy or simply pricing a product as before.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Three properties are load-bearing

        Three structural properties of the information-blocking prohibition are load-bearing for the rest of the course.

        | Property | What it means | Why it matters |
        |---|---|---|
        | **Statutory** | The definition lives in 21st Century Cures Act Section 4004; the implementing rule is at 45 CFR Part 171. | Federal agencies have direct authority to act. The prohibition does not depend on private litigation. |
        | **Effects-based** | A practice is identified by whether it is likely to interfere, not by whether the actor intended to interfere. | Enforcement does not require proof of motive. Routine practices that have the effect of blocking can be enforced against. |
        | **Penalized** | The 2023 OIG Final Rule sets civil monetary penalties at up to $1,000,000 per violation against developers and HIEs. Provider disincentives are administered by CMS through Medicare programs. | The prohibition has financial teeth. The economic cost of blocking now appears on the balance sheet. |
        """
    )
    return


@app.cell
def _(SCENARIOS, mo):
    scenario_pick = mo.ui.dropdown(
        options=list(SCENARIOS.keys()),
        value=list(SCENARIOS.keys())[0],
        label="Scenario",
    )
    disposition_pick = mo.ui.radio(
        options=[
            "Information blocking (no exception applies)",
            "Not information blocking (an exception applies, or the practice is not within the definition)",
        ],
        label="Disposition",
    )
    mo.vstack(
        [
            mo.md(
                "## Practice scenarios\n\n"
                "**Pick a scenario, then decide whether the practice meets the "
                "information-blocking definition.** The reactive panel below confirms "
                "the right reading and walks the reasoning."
            ),
            scenario_pick,
            disposition_pick,
        ]
    )
    return disposition_pick, scenario_pick


@app.cell
def _(SCENARIOS, disposition_pick, mo, scenario_pick):
    _info = SCENARIOS[scenario_pick.value]
    _correct_blocking = _info["blocking"]
    _chosen = disposition_pick.value
    if _chosen is None:
        _resp = mo.callout(
            mo.md("_Pick a disposition._"), kind="neutral"
        )
    else:
        _chose_blocking = _chosen.startswith("Information blocking")
        if _chose_blocking == _correct_blocking:
            _verdict = "**Correct.**"
            _kind = "success"
        else:
            _verdict = (
                "**Not quite.** The right reading is "
                + ("**information blocking.**" if _correct_blocking else "**not information blocking.**")
            )
            _kind = "warn"
        _resp = mo.callout(
            mo.md(f"{_verdict} {_info['analysis']}"),
            kind=_kind,
        )
    _resp
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Where this goes next

        The scenarios above turn on the exceptions: the categorized practices that do not meet the information-blocking definition. Track 02 covers the statute (21st Century Cures Act Section 4004) that defines the prohibition and the ten exceptions ONC has now catalogued (eight in the original 2020 Final Rule, plus the TEFCA Manner and Protecting Care Access exceptions added through HTI-1 in 2024). Reading the exceptions in detail is the prerequisite for reading any complaint, any defense, or any compliance memorandum the rest of this course's policy framework produces.
        """
    )
    return


if __name__ == "__main__":
    app.run()
