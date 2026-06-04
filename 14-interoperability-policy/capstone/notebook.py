"""Capstone for course 14: Interoperability policy.

The reader applies the policy framework built across Tracks 01 through 05
to three real-shaped scenarios: a patient cannot get her records, a
researcher cannot access a dataset on non-discriminatory terms, a vendor
restricts data through fees and marketplace structures. For each scenario,
three commit-then-reveal questions: which policy framework applies, what
it requires, and what recourse exists. The final cells assemble the nine
answers and a reflection into a downloadable Markdown policy brief.

WASM-safe: no shared imports, no data files, no relative paths.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    MIN_CHARS = 30

    IDEALS = {
        "A_policy": (
            "Two policy frameworks apply at once. **HIPAA Privacy Rule at 45 CFR "
            "164.524** establishes the right of access: an individual is entitled "
            "to a copy of their protected health information in the designated "
            "record set, in the form requested when readily producible, within 30 "
            "days. **21st Century Cures Act information-blocking provisions** "
            "(Tracks 01 and 02) prohibit practices likely to interfere with access, "
            "exchange, or use of electronic health information. The 2020 ONC Cures "
            "Act Final Rule's Conditions and Maintenance of Certification (Track 03) "
            "require certified EHRs to expose a standardized FHIR R4 patient-access "
            "API (170.315(g)(10)). Health System A is operating a certified EHR; the "
            "patient portal that omits labs and imaging suggests the (g)(10) API is "
            "either disabled, misconfigured, or not exposed to the patient app. The "
            "\"system doesn't do that\" response is the operational marker that the "
            "blocking practice exists at the system level, not at the patient-portal "
            "level."
        ),
        "A_requirement": (
            "HIPAA requires Health System A to provide the records within 30 days "
            "(45 CFR 164.524(b)(2)), in electronic form if readily producible, free "
            "or at a reasonable cost-based fee for the copy. The Cures Act and the "
            "ONC Final Rule require the certified EHR to expose patient-accessible "
            "electronic data through the standardized API. The patient must be able "
            "to authorize a third-party app (or the new oncologist's office at Health "
            "System B, through their certified EHR) to fetch the data via the API. "
            "A six-week non-response is itself a violation of the 30-day requirement; "
            "the paper-form-only policy applied at the patient-access level (when the "
            "certified API exists) is itself an information-blocking practice and a "
            "Conditions-of-Certification concern for the health system."
        ),
        "A_recourse": (
            "Three recourse pathways exist, and the patient can pursue them in "
            "parallel. **OCR complaint** for the HIPAA right-of-access violation "
            "(OCR has pursued right-of-access enforcement aggressively since "
            "approximately 2019 with monetary settlements). **ONC information-"
            "blocking complaint** at the healthit.gov complaint portal; provider "
            "complaints route through CMS for disincentives administered through "
            "Medicare quality programs (Promoting Interoperability). **Have Health "
            "System B's records team request electronically** through the certified "
            "API, which under the Cures Act framework should be the standard pathway "
            "regardless of Health System A's paper workflow. Internal escalation to "
            "Health System A's patient ombudsperson or HIM leadership is often the "
            "fastest practical path; the formal complaints establish the regulatory "
            "record and create the enforcement file."
        ),
        "B_policy": (
            "Three frameworks apply. **HIPAA's research provisions at 45 CFR "
            "164.512(i)** govern research with PHI: with an IRB-approved protocol, "
            "Dr. M has the authorization piece covered. **The Cures Act information-"
            "blocking provisions** apply if the practices restrict access or impose "
            "non-cost-based fees; the differential pricing and the publication-"
            "rights condition each implicate the Fees and Licensing exceptions. "
            "**State research-data-sharing law and institutional research-conduct "
            "policy** typically require non-discrimination in data access for "
            "IRB-approved studies, separately from federal frameworks. The "
            "differential pricing based on whether the researcher is internal or "
            "external to Health System C is on its face the kind of practice each "
            "framework is concerned with."
        ),
        "B_requirement": (
            "The **Fees Exception** requires fees to be cost-based, non-"
            "discriminatory, and not designed to interfere with access. Different "
            "fees for the same extraction depending on whether the requester is "
            "internal or external is on its face discriminatory and likely fails "
            "the exception, regardless of how the fee is documented. The "
            "**Licensing Exception** requires licensing of interoperability "
            "elements (or in this case licensing of the data product) to be on "
            "reasonable and non-discriminatory terms; conditioning a $5,000 "
            "discount on a publication-rights surrender is neither reasonable nor "
            "non-discriminatory. Internal researchers receiving the same "
            "extractions at no charge is the evidence the fee is not actually "
            "cost-based."
        ),
        "B_recourse": (
            "Four recourse paths exist. **Internal escalation** through the "
            "university's research administration to Health System C's research-"
            "data leadership, with the differential-pricing documentation. **ONC "
            "information-blocking complaint** at healthit.gov; provider complaints "
            "route through CMS for disincentives. **Institutional research-conduct "
            "review** through the university's IRB or research-integrity office. "
            "**State research-data-sharing law where applicable** (state IRBs and "
            "state attorneys general have intervened in similar cases). Practical "
            "advice: the internal-escalation route via formal research "
            "administration is usually fastest because the discrimination pattern "
            "is documentable through the comparison with internal-researcher fees, "
            "and an institutional response avoids the multi-year federal-complaint "
            "timeline."
        ),
        "C_policy": (
            "Two frameworks apply. **The Cures Act information-blocking provisions** "
            "(Tracks 01 and 02): the practices described (the $35K API integration "
            "fee, the 30% marketplace revenue share, the withheld documentation, "
            "the suggestion to buy the vendor's own care-management module) "
            "implicate the Fees and Licensing exceptions, and the practices fail "
            "the cost-based, non-discriminatory tests of both exceptions. **The "
            "ONC Conditions and Maintenance of Certification** (Track 03): "
            "certified IT developers must support the 170.315(g)(10) standardized "
            "API; the API specification (US Core) does not permit withholding "
            "sub-resource documentation as \"trade secret.\" Withholding "
            "documentation that the certification criterion implicitly requires to "
            "be available is itself a blocking practice and a Conditions-of-"
            "Certification violation."
        ),
        "C_requirement": (
            "The **Fees Exception** requires the developer's fee for the "
            "standardized API to be cost-based and limited to specified service "
            "categories; a $35,000 certification fee that recovers more than actual "
            "cost is a clear failure. The **Licensing Exception** requires "
            "reasonable, non-discriminatory terms for licensing interoperability "
            "elements; a 30% marketplace revenue share is rent-extraction, not "
            "cost-based licensing. The withholding of documentation conflicts "
            "directly with the ONC Conditions of Certification, which require the "
            "(g)(10) API to be both implemented and usable by third-party "
            "applications. The suggestion that Health System D purchase the "
            "vendor's own module is the operational signature of the conduct the "
            "Cures Act was written to prevent: the developer steers the customer "
            "toward its own product by making third-party integration expensive."
        ),
        "C_recourse": (
            "Three recourse paths exist. **ONC information-blocking complaint** at "
            "healthit.gov; developer complaints route to OIG for investigation. "
            "The 2023 OIG Final Rule sets civil monetary penalties at up to "
            "$1,000,000 per violation against developers and HIEs, which is the "
            "financial backstop the prohibition rests on. **ONC certification "
            "review**: ONC may suspend or revoke the developer's certification for "
            "systematic Conditions-of-Certification violations, which is "
            "commercially significant for any vendor whose revenue depends on "
            "selling certified IT to providers. **Private antitrust action**: the "
            "conduct described (tying, exclusive dealing on marketplace access, "
            "leveraging API control to steer customers to the developer's own "
            "module) has antitrust dimensions independently of the information-"
            "blocking framework. Coordination with industry peers facing the same "
            "conduct from the same developer materially strengthens any complaint. "
            "The OIG route is usually most effective near-term; the antitrust "
            "route is slower but has occasionally produced significant settlements."
        ),
    }

    return IDEALS, MIN_CHARS, mo


@app.cell
def _(mo):
    mo.md(
        r"""
        # Capstone: Apply the policy framework to three scenarios

        Three real-shaped scenarios. Each scenario asks you to make the policy-fluent move a clinician or informaticist would make on being handed the situation: identify the applicable policy framework, name what the framework requires, and identify the recourse pathways available. The reactive reveal compares your analysis with how a policy-fluent reviewer would think through the same scenario, and the final cell assembles your nine answers (plus a closing reflection) into a downloadable Markdown policy brief.

        Each question is gated by a 30-character minimum: write a substantive answer for each before the reveal.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            ### Scenario A: A patient cannot get her records

            **Janet Walsh** (synthetic patient) is a 47-year-old breast-cancer survivor. She was treated at Health System A in the Midwest (2022 to 2023) with surgery, chemotherapy, and radiation. She relocated to the Pacific Northwest in March 2024 and established care with a new oncologist at Health System B.

            Since June 2024, she has been trying to have her records released from Health System A to her new oncologist's office.

            - Health System A directed her to fill out a paper records-request form by mail.
            - She submitted the form in July 2024. As of October 2024, she has received no records and no written response.
            - When she called for follow-up, she was told the request is "in processing."
            - When she asked specifically about electronic release through the patient portal or a FHIR API, she was told "our system doesn't do that."
            - Her patient portal at Health System A displays visit summaries only; it does not expose the laboratory results, the pathology reports, or the imaging reports she needs her new oncologist to see.
            - Health System A is a large academic medical center, accepts Medicare, and is on the latest certified version of a major EHR.

            Your task: identify the applicable policy framework, what that framework requires of Health System A, and what recourse Janet has.
            """
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    sa_q1 = mo.ui.text_area(
        label="A.1 Which policy framework applies, and how?",
        placeholder=(
            "Name the federal and state frameworks that bear on the situation, and "
            "the specific provisions within each that apply."
        ),
        rows=4,
        full_width=True,
    )
    sa_q2 = mo.ui.text_area(
        label="A.2 What does the framework require of Health System A?",
        placeholder=(
            "State the specific obligations on the health system, with timeframes "
            "and form requirements where applicable."
        ),
        rows=4,
        full_width=True,
    )
    sa_q3 = mo.ui.text_area(
        label="A.3 What recourse does Janet have, in order of practical effect?",
        placeholder=(
            "Name the regulatory and practical pathways, including the agencies, "
            "and order them by likely speed and effectiveness."
        ),
        rows=4,
        full_width=True,
    )
    mo.vstack(
        [
            mo.md("### Your analysis of Scenario A"),
            sa_q1,
            sa_q2,
            sa_q3,
        ]
    )
    return sa_q1, sa_q2, sa_q3


@app.cell
def _(IDEALS, MIN_CHARS, mo, sa_q1, sa_q2, sa_q3):
    _texts = [sa_q1.value, sa_q2.value, sa_q3.value]
    _all_committed = all(
        t and len(t) >= MIN_CHARS for t in _texts
    )
    if not _all_committed:
        _resp = mo.callout(
            mo.md(
                f"_Commit at least {MIN_CHARS} characters per question to see how "
                "a policy-fluent reviewer would think through Scenario A._"
            ),
            kind="neutral",
        )
    else:
        _resp = mo.vstack(
            [
                mo.md("### Reveal: Scenario A"),
                mo.callout(
                    mo.md(f"**Your A.1 (policy framework)**\n\n{sa_q1.value}"),
                    kind="info",
                ),
                mo.callout(
                    mo.md(
                        f"**How we'd think through A.1**\n\n{IDEALS['A_policy']}"
                    ),
                    kind="success",
                ),
                mo.callout(
                    mo.md(f"**Your A.2 (requirement)**\n\n{sa_q2.value}"),
                    kind="info",
                ),
                mo.callout(
                    mo.md(
                        f"**How we'd think through A.2**\n\n{IDEALS['A_requirement']}"
                    ),
                    kind="success",
                ),
                mo.callout(
                    mo.md(f"**Your A.3 (recourse)**\n\n{sa_q3.value}"),
                    kind="info",
                ),
                mo.callout(
                    mo.md(
                        f"**How we'd think through A.3**\n\n{IDEALS['A_recourse']}"
                    ),
                    kind="success",
                ),
            ]
        )
    _resp
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            ### Scenario B: A researcher cannot access a dataset on non-discriminatory terms

            **Dr. Maria Chen** (synthetic) is a faculty researcher at State University, an institution affiliated with Health System C through a teaching-and-research relationship. She has IRB approval to study outcomes in rheumatoid arthritis patients on biologic therapy, using EHR data on 1,500 RA patients followed at Health System C's rheumatology clinic over 2020 to 2025.

            In February 2026, she submitted a data-access request to Health System C's Research Data Office. As of June 2026:

            - The Research Data Office quoted her a $40,000 fee covering analyst time, infrastructure, and "data licensing."
            - The Office offered a $5,000 discount if she signs an "open access" clause giving Health System C the right to publish or distribute the de-identified dataset, including derived results.
            - Dr. Chen is a State University employee, not a Health System C employee.
            - Two other faculty researchers, both employed by Health System C, have received comparable RA-cohort extractions at no charge during the same period, both with the same level of IRB oversight.
            - Dr. Chen's IRB-approved protocol does not contemplate Health System C as a co-publisher or as a downstream distributor of the dataset.

            Your task: identify the applicable policy framework, what the framework requires, and what recourse Dr. Chen has.
            """
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    sb_q1 = mo.ui.text_area(
        label="B.1 Which policy framework applies, and how?",
        placeholder=(
            "Name the federal frameworks, the HIPAA-side and Cures-Act-side "
            "provisions, and the institutional or state research-conduct "
            "frameworks that bear on the situation."
        ),
        rows=4,
        full_width=True,
    )
    sb_q2 = mo.ui.text_area(
        label="B.2 What does the framework require of Health System C?",
        placeholder=(
            "State which information-blocking exception the practice would have "
            "to fall within to be defensible, and why the practice as described "
            "does not meet the exception."
        ),
        rows=4,
        full_width=True,
    )
    sb_q3 = mo.ui.text_area(
        label="B.3 What recourse does Dr. Chen have, in order of practical effect?",
        placeholder=(
            "Name the institutional, regulatory, and legal pathways, and order "
            "them by likely speed and effectiveness."
        ),
        rows=4,
        full_width=True,
    )
    mo.vstack(
        [
            mo.md("### Your analysis of Scenario B"),
            sb_q1,
            sb_q2,
            sb_q3,
        ]
    )
    return sb_q1, sb_q2, sb_q3


@app.cell
def _(IDEALS, MIN_CHARS, mo, sb_q1, sb_q2, sb_q3):
    _texts = [sb_q1.value, sb_q2.value, sb_q3.value]
    _all_committed = all(
        t and len(t) >= MIN_CHARS for t in _texts
    )
    if not _all_committed:
        _resp = mo.callout(
            mo.md(
                f"_Commit at least {MIN_CHARS} characters per question to see how "
                "a policy-fluent reviewer would think through Scenario B._"
            ),
            kind="neutral",
        )
    else:
        _resp = mo.vstack(
            [
                mo.md("### Reveal: Scenario B"),
                mo.callout(
                    mo.md(f"**Your B.1 (policy framework)**\n\n{sb_q1.value}"),
                    kind="info",
                ),
                mo.callout(
                    mo.md(
                        f"**How we'd think through B.1**\n\n{IDEALS['B_policy']}"
                    ),
                    kind="success",
                ),
                mo.callout(
                    mo.md(f"**Your B.2 (requirement)**\n\n{sb_q2.value}"),
                    kind="info",
                ),
                mo.callout(
                    mo.md(
                        f"**How we'd think through B.2**\n\n{IDEALS['B_requirement']}"
                    ),
                    kind="success",
                ),
                mo.callout(
                    mo.md(f"**Your B.3 (recourse)**\n\n{sb_q3.value}"),
                    kind="info",
                ),
                mo.callout(
                    mo.md(
                        f"**How we'd think through B.3**\n\n{IDEALS['B_recourse']}"
                    ),
                    kind="success",
                ),
            ]
        )
    _resp
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            ### Scenario C: A vendor restricts third-party integration

            **Health System D** (synthetic regional health system, 12 hospitals, 1,400-bed network) selected a third-party care-management app to integrate with their certified EHR. The app uses the certified 170.315(g)(10) FHIR API for read access and a separate vendor-provided write API for care-plan updates.

            The EHR vendor (call them **EHR-X**, a major certified IT developer) has responded to the integration request as follows:

            - A one-time **$35,000 API integration certification fee** for the third-party app.
            - The third-party app must be listed in EHR-X's proprietary app marketplace, which takes a **30% revenue share** on the third-party app's subscription fees from Health System D and from any other client.
            - EHR-X has **withheld the API documentation** for the FHIR sub-resource that carries the care-plan data the app needs, citing "proprietary trade secret."
            - EHR-X has suggested that Health System D **purchase EHR-X's own care-management module** ($120,000 per year), which would not require the third-party integration or the marketplace fee.

            Your task: identify the applicable policy framework, what it requires of EHR-X, and what recourse Health System D has.
            """
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    sc_q1 = mo.ui.text_area(
        label="C.1 Which policy framework applies, and how?",
        placeholder=(
            "Name the Cures Act information-blocking provisions and the ONC "
            "Conditions of Certification, and identify which of the practices "
            "implicate which framework."
        ),
        rows=4,
        full_width=True,
    )
    sc_q2 = mo.ui.text_area(
        label="C.2 What does the framework require of EHR-X?",
        placeholder=(
            "State which exceptions EHR-X would have to invoke to defend each "
            "practice, and why each fails."
        ),
        rows=4,
        full_width=True,
    )
    sc_q3 = mo.ui.text_area(
        label="C.3 What recourse does Health System D have, in order of practical effect?",
        placeholder=(
            "Name the regulatory and legal pathways available against EHR-X, "
            "including the enforcement structure that gives the prohibition teeth."
        ),
        rows=4,
        full_width=True,
    )
    mo.vstack(
        [
            mo.md("### Your analysis of Scenario C"),
            sc_q1,
            sc_q2,
            sc_q3,
        ]
    )
    return sc_q1, sc_q2, sc_q3


@app.cell
def _(IDEALS, MIN_CHARS, mo, sc_q1, sc_q2, sc_q3):
    _texts = [sc_q1.value, sc_q2.value, sc_q3.value]
    _all_committed = all(
        t and len(t) >= MIN_CHARS for t in _texts
    )
    if not _all_committed:
        _resp = mo.callout(
            mo.md(
                f"_Commit at least {MIN_CHARS} characters per question to see how "
                "a policy-fluent reviewer would think through Scenario C._"
            ),
            kind="neutral",
        )
    else:
        _resp = mo.vstack(
            [
                mo.md("### Reveal: Scenario C"),
                mo.callout(
                    mo.md(f"**Your C.1 (policy framework)**\n\n{sc_q1.value}"),
                    kind="info",
                ),
                mo.callout(
                    mo.md(
                        f"**How we'd think through C.1**\n\n{IDEALS['C_policy']}"
                    ),
                    kind="success",
                ),
                mo.callout(
                    mo.md(f"**Your C.2 (requirement)**\n\n{sc_q2.value}"),
                    kind="info",
                ),
                mo.callout(
                    mo.md(
                        f"**How we'd think through C.2**\n\n{IDEALS['C_requirement']}"
                    ),
                    kind="success",
                ),
                mo.callout(
                    mo.md(f"**Your C.3 (recourse)**\n\n{sc_q3.value}"),
                    kind="info",
                ),
                mo.callout(
                    mo.md(
                        f"**How we'd think through C.3**\n\n{IDEALS['C_recourse']}"
                    ),
                    kind="success",
                ),
            ]
        )
    _resp
    return


@app.cell
def _(mo):
    reflection_input = mo.ui.text_area(
        label=(
            "Across the three scenarios, what is the structural feature that "
            "makes each of them an information-blocking question rather than a "
            "purely technical or contractual question? Write a short paragraph; "
            "this is for you."
        ),
        placeholder=(
            "This reflection is included in the assembled policy brief but no "
            "ideal answer is revealed; the writing itself is the point."
        ),
        rows=4,
        full_width=True,
    )
    mo.vstack(
        [
            mo.md("## Closing reflection"),
            reflection_input,
        ]
    )
    return (reflection_input,)


@app.cell
def _(
    mo,
    reflection_input,
    sa_q1,
    sa_q2,
    sa_q3,
    sb_q1,
    sb_q2,
    sb_q3,
    sc_q1,
    sc_q2,
    sc_q3,
):
    brief = f"""# Policy analysis brief: three interoperability scenarios

_Produced from the Course 14 capstone. Three scenarios, three analytic questions each, plus a closing reflection. The brief is a starting deliverable for an institutional policy office, a CMIO/CMIO-adjacent committee, or a regulatory-affairs team responding to one of these situations._

## Scenario A: A patient cannot get her records

**A.1 Policy framework**

{sa_q1.value or '_(not yet committed)_'}

**A.2 Requirement**

{sa_q2.value or '_(not yet committed)_'}

**A.3 Recourse**

{sa_q3.value or '_(not yet committed)_'}

## Scenario B: A researcher cannot access a dataset on non-discriminatory terms

**B.1 Policy framework**

{sb_q1.value or '_(not yet committed)_'}

**B.2 Requirement**

{sb_q2.value or '_(not yet committed)_'}

**B.3 Recourse**

{sb_q3.value or '_(not yet committed)_'}

## Scenario C: A vendor restricts third-party integration

**C.1 Policy framework**

{sc_q1.value or '_(not yet committed)_'}

**C.2 Requirement**

{sc_q2.value or '_(not yet committed)_'}

**C.3 Recourse**

{sc_q3.value or '_(not yet committed)_'}

## Closing reflection

{reflection_input.value or '_(not yet committed)_'}

---

_Generated from the Course 14 capstone notebook. This brief is the starting deliverable for the team handling one of these situations. It does not replace the actual policy work; it specifies what that work is and what artifacts it produces._
"""
    mo.md(
        "## The assembled policy-analysis brief\n\n"
        "The Markdown below assembles your nine answers and the reflection into "
        "a single document. The download button at the end exports it as a `.md` "
        "file that a policy office or governance committee can read directly."
    )
    return (brief,)


@app.cell
def _(brief, mo):
    mo.md(brief)
    return


@app.cell
def _(brief, mo):
    download = mo.download(
        data=brief.encode("utf-8"),
        filename="interoperability-policy-analysis-brief.md",
        label="Download the policy-analysis brief as Markdown",
    )
    download
    return (download,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Closing

        The three scenarios in this capstone are practical applications of the framework Tracks 01 through 05 built. The same analytic move appears in each: identify the framework (Cures Act, HIPAA, ONC certification, CMS rule, GDPR, or state law), name the specific provision that applies, name the recourse pathway the provision exists to enable. The reader who has produced the brief above can sit on a hospital governance committee, in a research-administration meeting, or across the table from a vendor representative, and run the same analytic move on whichever situation the meeting is actually about. That is the practice this course exists to teach.
        """
    )
    return


if __name__ == "__main__":
    app.run()
