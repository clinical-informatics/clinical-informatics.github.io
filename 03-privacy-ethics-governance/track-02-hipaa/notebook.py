"""Track 02: HIPAA and beyond.

HIPAA is the floor, not the ceiling. This notebook walks PHI, covered
entities, the two de-identification paths (Safe Harbor and Expert
Determination), the Limited Data Set + DUA middle path, IRB basics, and
the layers beyond HIPAA (state laws, 42 CFR Part 2, GDPR, the
apps/wearables gap). The interactive piece is a pathway selector that
asks about a proposed use case and recommends the appropriate regulatory
path with a one-paragraph rationale.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import sys
    from pathlib import Path

    _track_dir = Path(__file__).parent
    _course_dir = _track_dir.parent
    if str(_course_dir) not in sys.path:
        sys.path.insert(0, str(_course_dir))

    import marimo as mo
    import pandas as pd

    return mo, pd


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 02: HIPAA and beyond

        ## The floor, not the ceiling

        Track 01 built the threat model. Track 02 walks the regulatory response.

        HIPAA is the United States federal floor for clinical data handling. It sets minimum requirements for what entities may do with Protected Health Information, how they must protect it, and under what circumstances they may share it. The framework is necessary; it is rarely sufficient. Institutions impose stricter standards, states layer additional laws, international partners require GDPR compliance, and large categories of health data (apps, wearables, employer wellness programs) sit outside HIPAA's reach entirely.

        This track has five jobs:

        1. **Name the vocabulary** that runs every HIPAA conversation: PHI, covered entities, business associates, the four pillars.
        2. **Walk the two de-identification paths** the Privacy Rule provides: Safe Harbor (mechanical) and Expert Determination (actuarial).
        3. **Explain the Limited Data Set + Data Use Agreement middle path**, which is the operational sweet spot for most secondary-use clinical research.
        4. **Cover IRB basics**: when review is required, what "exempt" means, what determines exempt vs expedited vs full review.
        5. **Survey the layers beyond HIPAA**: state laws, 42 CFR Part 2, GDPR, the apps/wearables gap.

        Then a pathway selector for working through a concrete use case.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1. The vocabulary

        | Term | Definition |
        |---|---|
        | **PHI (Protected Health Information)** | Health information that is *individually identifiable* and held or transmitted by a *covered entity* or *business associate*. Three pieces: individually identifiable, health-related, held by a regulated entity. |
        | **Covered Entity (CE)** | Healthcare providers (almost all hospitals, clinics, physicians); health plans (insurers, Medicare, Medicaid, employer-sponsored); healthcare clearinghouses. |
        | **Business Associate (BA)** | A person or entity that performs functions for a CE involving the use or disclosure of PHI. Examples: billing services, cloud EHR vendors, research analytics consultants. Bound by a Business Associate Agreement (BAA). |
        | **Privacy Rule** | What uses/disclosures of PHI are permitted, what requires authorization, what de-identification means. |
        | **Security Rule** | Administrative, physical, and technical safeguards for electronic PHI. |
        | **Breach Notification Rule** | What constitutes a breach and how it must be reported (to individuals, HHS, sometimes the media). |
        | **Enforcement Rule** | How the Office for Civil Rights investigates and penalizes violations. |

        The critical scoping question: **is this data PHI?** That determines whether HIPAA applies at all. The same blood pressure reading is PHI when stored in an EHR and not PHI when stored in your Apple Watch. The regulatory framework follows the institution, not the data.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2. The two de-identification paths

        The Privacy Rule defines two methods by which PHI can be de-identified. After de-identification, the data is no longer PHI and can be shared more freely.

        ### Safe Harbor: the eighteen-category checklist

        Remove all of these eighteen categories, and the resulting dataset is considered de-identified:

        1. Names (including initials)
        2. Geographic subdivisions smaller than a state (street, city, county, ZIP) **with a 3-digit ZIP exception** for ZIPs over 20,000 population
        3. All elements of dates (except year) tied to an individual; ages over 89 aggregated to "90 or older"
        4. Telephone numbers
        5. Vehicle identifiers
        6. Fax numbers
        7. Device identifiers
        8. Email addresses
        9. Web URLs
        10. Social Security numbers
        11. IP addresses
        12. Medical record numbers
        13. Biometric identifiers (fingerprints, voice prints)
        14. Health plan beneficiary numbers
        15. Full-face photographs
        16. Account numbers
        17. Any other unique identifying number, characteristic, or code
        18. Certificate or license numbers

        Plus a **residual catch-all**: the covered entity must have no actual knowledge that residual information could identify the individual.

        **Trade-off.** Safe Harbor is mechanical and easy to verify. It is conservative on data utility: full dates of service are gone (so longitudinal analyses by month or week are impossible), ages over 89 are aggregated (a sizable portion of clinical research subjects), and ZIPs are coarsened. For many research questions, Safe Harbor strips out the variables that drive the analysis.

        ### Expert Determination: the actuarial path

        An alternative: a qualified expert (typically a PhD statistician with privacy expertise) certifies that the re-identification risk is "very small" under defined attack scenarios, applying generally accepted statistical and scientific principles. The expert documents methods, assumptions, and the residual risk.

        **Trade-off.** Expert Determination is more expensive than Safe Harbor (an engagement, not a checklist) and produces a more utility-preserving dataset. Large research data networks (TriNetX, several major academic CDWs) typically operate on Expert-Determined datasets.

        ### When each one fits

        | Use case | Path |
        |---|---|
        | Quick public release of summary statistics | Safe Harbor |
        | Internal QI analysis where dates of service don't matter | Safe Harbor |
        | Longitudinal cohort analysis with dates of service | Expert Determination, or LDS + DUA |
        | Geographic analysis at the county level | Expert Determination, or LDS + DUA |
        | Cross-institutional research network | Expert Determination (typically) |
        | Subgroup analysis on patients over 89 | Expert Determination |
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3. Limited Data Sets and Data Use Agreements

        A **Limited Data Set (LDS)** keeps *some* identifiers that Safe Harbor strips (full dates of service, city, state, ZIP, 89+ ages) but still removes the direct identifiers. An LDS is still PHI under HIPAA.

        An LDS can be shared for research, public health, or healthcare operations **only under a Data Use Agreement (DUA)**, which must:

        - Name the **specific purposes** for which the data may be used.
        - Name the **people and entities** permitted to receive and use the data.
        - **Prohibit re-identification** attempts.
        - Require **appropriate safeguards**.
        - Require **reporting** of unauthorized uses or disclosures.
        - Require the recipient to ensure **subcontractors** also follow these terms.

        ### Why this is the operational sweet spot

        For most secondary-use clinical research, the LDS + DUA path is the practical answer:

        - Preserves dates of service (essential for almost all longitudinal analysis).
        - Allows ZIP-level geographic analysis.
        - Treats patients over 89 as a real population.
        - Avoids the Safe Harbor conservatism while staying under HIPAA's clear procedural framework.
        - Avoids the cost of an Expert Determination engagement.

        The cost is the **contractual layer**: the DUA must be in place, signed by both parties, before the data moves. Institutions have standard DUAs for this purpose. The signing is often the rate-limiting step for a research project.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 4. IRB basics

        IRB (Institutional Review Board) review is required for **human-subjects research**. HIPAA and the Common Rule (45 CFR 46) interact: an IRB can waive the requirement for individual HIPAA authorization for research under specific conditions, and an IRB review is itself a HIPAA-compliant disclosure pathway.

        ### The four categories of review

        | Category | When it applies | What review looks like |
        |---|---|---|
        | **Not human-subjects research** | QI projects, internal operational analyses, public health surveillance, education evaluations | Often no IRB review needed; some institutions require a determination letter |
        | **Exempt** | Research on existing de-identified data, certain educational or anonymous-survey research | IRB determines that the research is exempt from full review |
        | **Expedited** | Minimal-risk research that doesn't qualify for exemption | Reviewed by a single IRB member; faster timeline |
        | **Full board** | Greater-than-minimal-risk research | Reviewed by the full IRB at a convened meeting |

        ### The common clinical-informatics scenario

        Research using de-identified EHR data is **often exempt** but not always. Exemption depends on whether the dataset is truly de-identified (Track 01's distinction lands here) and on what activities the research includes (publication of identifiable case reports breaks exemption; pure analysis usually does not).

        The right move is to **get an exemption determination from your local IRB rather than to assume it.** The cost of a determination letter is small; the cost of conducting research that turns out to need IRB review without it is large.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 5. Beyond HIPAA

        HIPAA is the floor. The relevant layers above and outside it:

        | Layer | What it adds |
        |---|---|
        | **California CCPA / CPRA** | Privacy rights for California consumers across all categories of personal data, including health data not covered by HIPAA (apps, wellness). Individual rights to access, delete, opt out of sale. |
        | **Illinois BIPA** | Specific protections for biometric identifiers. Significant litigation history. |
        | **Washington MHMDA (2023)** | First state law specifically targeting consumer health data outside HIPAA. Apps, wellness trackers, location data near healthcare facilities. |
        | **Texas, NY, CT, CO, VA, ...** | Each adds layered protections beyond the federal floor. The list is growing every year. |
        | **42 CFR Part 2** | Stricter federal framework for substance use disorder treatment records. Requires specific written consent for each disclosure, even between healthcare providers. Substantially aligned with HIPAA in 2024 rule changes but remains distinct. |
        | **GDPR (EU)** | Health data is a special category requiring explicit consent or specific legal bases. Broader individual rights (access, correction, erasure, portability). Substantial fines. Applies to any organization processing EU residents' data. |
        | **The apps/wearables gap** | HIPAA does not cover health data collected directly by consumers (Apple Watch, Fitbit, period trackers, 23andMe, wellness apps). Post-Dobbs, several states have moved to fill this gap; federal action has lagged. |

        For a clinical informatics project, **all of these layers can apply simultaneously**. A multi-site study with California subjects, EU subjects, substance-use-disorder content, and a wearables data source has to satisfy HIPAA, CCPA, GDPR, 42 CFR Part 2, the wearable's TOS, and the device manufacturer's regulatory framework. The job isn't to memorize all of them; the job is to know which layers exist so you ask the right questions when the project crosses them.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 6. Pathway selector

        Describe a proposed use of clinical data. The selector recommends the appropriate regulatory pathway with a rationale.
        """
    )
    return


@app.cell
def _(mo):
    is_ce = mo.ui.radio(
        options=[
            "Yes, the data is held by a covered entity or business associate",
            "No, the data is from a consumer app, wearable, or non-CE source",
            "Mixed: some PHI sources, some non-PHI sources",
        ],
        value="Yes, the data is held by a covered entity or business associate",
        label="1. Is the data PHI in the HIPAA sense?",
    )
    purpose = mo.ui.radio(
        options=[
            "Research (formal study with a defined question, intended for publication or regulatory submission)",
            "Quality improvement (internal evaluation of care delivery)",
            "Public health surveillance (mandated reporting or population-health monitoring)",
            "Healthcare operations (internal analytics, financial reporting, payer activities)",
            "Direct clinical care (treatment, payment, operations under HIPAA TPO)",
        ],
        value="Research (formal study with a defined question, intended for publication or regulatory submission)",
        label="2. What is the purpose?",
    )
    needs_dates = mo.ui.checkbox(
        label="3. Does the analysis require dates of service finer than year (admission date, lab date, encounter date)?",
        value=False,
    )
    needs_zip = mo.ui.checkbox(
        label="4. Does the analysis require ZIP code finer than the 3-digit Safe Harbor allowance?",
        value=False,
    )
    needs_elderly = mo.ui.checkbox(
        label="5. Does the analysis include patients aged 90 or older as a distinct group?",
        value=False,
    )
    needs_identifiable = mo.ui.checkbox(
        label="6. Does the analysis require identifiable patient data (e.g., re-contact, linkage to external identifiable sources)?",
        value=False,
    )
    international = mo.ui.checkbox(
        label="7. Does the cohort include EU residents or other international subjects?",
        value=False,
    )
    sud_data = mo.ui.checkbox(
        label="8. Does the data include substance use disorder treatment records (42 CFR Part 2 territory)?",
        value=False,
    )

    mo.vstack(
        [
            is_ce,
            purpose,
            needs_dates,
            needs_zip,
            needs_elderly,
            needs_identifiable,
            international,
            sud_data,
        ]
    )
    return (
        international,
        is_ce,
        needs_dates,
        needs_elderly,
        needs_identifiable,
        needs_zip,
        purpose,
        sud_data,
    )


@app.cell
def _(
    international,
    is_ce,
    mo,
    needs_dates,
    needs_elderly,
    needs_identifiable,
    needs_zip,
    purpose,
    sud_data,
):
    if is_ce.value.startswith("No,"):
        recommendation = (
            "**Outside HIPAA scope.** The data isn't PHI in the HIPAA sense, so the HIPAA paths don't directly apply. "
            "BUT: state consumer-health-data laws (Washington MHMDA, California CCPA/CPRA, Illinois BIPA depending on data type) "
            "likely do apply. The wearable or app's terms of service govern. If subjects consented to a specific use, the consent "
            "form is the contract; using the data for anything else may need re-consent."
        )
        kind = "info"
    elif is_ce.value.startswith("Mixed:"):
        recommendation = (
            "**Layered framework.** The PHI portion requires one of the HIPAA paths (see below for the recommendation on the PHI part). "
            "The non-PHI portion still falls under state consumer-health-data laws and the source's TOS. "
            "**The harder question** is whether linking the two crosses a threshold (e.g., does merging wearable data with EHR data make the wearable data PHI? Often yes, once it's held by the covered entity)."
        )
        kind = "info"
    elif purpose.value.startswith("Direct clinical care"):
        recommendation = (
            "**HIPAA TPO (Treatment, Payment, Operations).** Direct clinical care, payment activities, and routine healthcare operations are permitted uses of PHI under HIPAA "
            "without specific patient authorization. No de-identification path needed; no DUA needed. Standard Notice of Privacy Practices applies."
        )
        kind = "success"
    elif purpose.value.startswith("Quality improvement"):
        recommendation = (
            "**Likely HIPAA operations + possibly not human-subjects research.** Internal QI projects often qualify as healthcare operations under HIPAA and as not-human-subjects-research under the Common Rule. "
            "Get an IRB determination letter to confirm. If the QI work is intended for publication, the IRB may classify it as research, in which case the recommendation shifts to the Research path."
        )
        kind = "info"
    elif purpose.value.startswith("Public health"):
        recommendation = (
            "**HIPAA public-health disclosure.** HIPAA permits disclosures to public-health authorities for mandated reporting and surveillance without patient authorization. "
            "The PHI is shared with the public-health authority under the public-health disclosure provision, not under a de-identification path. State laws layer on top."
        )
        kind = "info"
    elif purpose.value.startswith("Healthcare operations"):
        recommendation = (
            "**HIPAA TPO (operations).** Internal analytics, financial reporting, and payer activities are permitted uses of PHI under HIPAA's Operations category. No de-identification or DUA required for internal use. "
            "If the analytics work is contracted to an external vendor, a Business Associate Agreement is required."
        )
        kind = "success"
    elif needs_identifiable.value:
        recommendation = (
            "**Identifiable PHI + IRB approval + HIPAA authorization (or waiver).** The research needs the actual identities, so de-identification paths don't apply. "
            "The path is: (1) IRB protocol approval; (2) either individual HIPAA authorization from each subject, or an IRB-granted waiver of authorization when the research couldn't be done otherwise and privacy risk is minimal; (3) a data security plan that meets the Security Rule."
        )
        kind = "warn"
    elif not (needs_dates.value or needs_zip.value or needs_elderly.value):
        recommendation = (
            "**Safe Harbor de-identification.** The analysis doesn't need dates of service finer than year, doesn't need sub-3-digit ZIP, and doesn't need 90+ patients as a distinct group. "
            "Safe Harbor is the right choice: mechanical, cheap, fully procedural. Remove the 18 categories of identifiers, satisfy the residual catch-all (no actual knowledge of remaining identifying combinations), and the dataset is no longer PHI. "
            "IRB exemption determination is typically straightforward for research on Safe-Harbor-de-identified data."
        )
        kind = "success"
    else:
        recommendation = (
            "**Limited Data Set + Data Use Agreement, OR Expert Determination.**\n\n"
            "The analysis needs one or more of: dates of service finer than year, ZIP finer than 3-digit, or 90+ patients as a distinct group. Safe Harbor is too restrictive.\n\n"
            "**Limited Data Set + DUA** is the operational sweet spot when:\n"
            "- the research is being conducted within an institution that has standard DUA templates,\n"
            "- the additional fields the LDS preserves (full dates, ZIP, 90+) are sufficient for the analysis, and\n"
            "- the recipient can sign a DUA and abide by it.\n\n"
            "**Expert Determination** is the right path when:\n"
            "- the dataset is being released to a research network or to the public,\n"
            "- a DUA-bound recipient framework is not feasible, or\n"
            "- the residual data after Safe Harbor is too utility-degraded but the dataset still needs to be classified as de-identified (no longer PHI).\n\n"
            "IRB exemption determination is typically still available for both paths, since the data is no longer PHI in the HIPAA sense."
        )
        kind = "info"

    extra_layers = []
    if international.value:
        extra_layers.append(
            "**GDPR also applies.** Health data is a special category requiring explicit consent or another specific legal basis. Individual rights (access, correction, erasure, portability) extend further than HIPAA. The DPO/DPA framework needs to be coordinated with the local privacy office."
        )
    if sud_data.value:
        extra_layers.append(
            "**42 CFR Part 2 also applies.** Substance use disorder treatment records require specific written consent for each disclosure, even between healthcare providers. The 2024 rule changes brought this framework closer to HIPAA, but specific consent and redisclosure prohibitions are still distinct from the HIPAA TPO permissions."
        )
    if is_ce.value.startswith("Yes") and not (
        purpose.value.startswith("Direct")
        or purpose.value.startswith("Healthcare operations")
        or purpose.value.startswith("Public health")
    ):
        extra_layers.append(
            "**State law also applies.** California CCPA/CPRA, Washington MHMDA, Illinois BIPA, and a growing list of state frameworks layer additional requirements (consumer rights, biometric protections, disclosure requirements). Check the subjects' state of residence and apply the strictest applicable framework."
        )

    main_callout = mo.callout(mo.md(recommendation), kind=kind)
    if extra_layers:
        layers_callout = mo.callout(
            mo.md("**Additional layers to apply:**\n\n" + "\n\n".join(extra_layers)),
            kind="warn",
        )
        pathway_output = mo.vstack([main_callout, layers_callout])
    else:
        pathway_output = main_callout
    pathway_output
    return (pathway_output,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 7. What this leaves you

        Five things in place:

        1. **The vocabulary.** PHI, covered entity, business associate, the four pillars. The minimum vocabulary for any conversation with a privacy officer.
        2. **The two de-identification paths.** Safe Harbor (mechanical, conservative on utility, cheap) and Expert Determination (actuarial, utility-preserving, expensive). When to choose each.
        3. **The LDS + DUA middle path.** The operational sweet spot for most secondary-use clinical research. Preserves the variables that matter (dates, ZIP, 90+) under a contractual framework.
        4. **IRB categories.** Not human-subjects research, exempt, expedited, full board. The right move is to get a determination from your local IRB, not to assume.
        5. **The layers beyond HIPAA.** State laws (CCPA, BIPA, MHMDA), 42 CFR Part 2, GDPR, the apps/wearables gap. HIPAA-compliant is necessary; it is rarely sufficient.

        Track 03 takes the ethics layer that sits on top of the legal layer. Most research that is HIPAA-compliant is also ethically defensible, but the categories of "legal" and "right" are not identical, and Track 03 walks the gap.
        """
    )
    return


if __name__ == "__main__":
    app.run()
