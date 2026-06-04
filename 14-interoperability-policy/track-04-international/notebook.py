"""Track 04: The international landscape.

No visible code. The notebook presents the GDPR framework as it applies to
health data, the UK NHS approach, and the European Health Data Space, and
runs the reader through a feature-by-feature comparison of the U.S., EU,
and UK frameworks on seven structurally significant questions.

WASM-safe: no shared imports, no data files, no relative paths.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    FEATURES = {
        "Lawful basis to process health data for clinical care": {
            "us": (
                "HIPAA permits use and disclosure of protected health information "
                "for treatment, payment, and healthcare operations (TPO) without "
                "patient authorization. The TPO permission is broad and is the "
                "operational default for most clinical processing."
            ),
            "eu": (
                "GDPR requires both an Article 6 lawful basis (most commonly "
                "\"provision of health or social care or treatment,\" Article 6(1)(c) "
                "or (e)) and an Article 9 condition (most commonly Article 9(2)(h) "
                "for healthcare provision). The two-step structure is what makes "
                "GDPR stricter than HIPAA on this dimension."
            ),
            "uk": (
                "UK GDPR plus the Data Protection Act 2018 mirrors the EU two-step "
                "structure. NHS clinical processing typically uses Article 6(1)(e) "
                "(public task) and Article 9(2)(h) (healthcare provision). Section 251 "
                "of the NHS Act 2006 provides a route to set aside the common-law "
                "duty of confidentiality for specific approved processing."
            ),
        },
        "National patient identifier": {
            "us": (
                "None. HIPAA Section 1173(b) in 1996 authorized one, but an annual "
                "appropriations rider has prevented its funding every fiscal year "
                "since 1999. Cross-organizational matching relies on probabilistic "
                "algorithms over demographics, with match rates between 50% and 90% "
                "depending on data quality (Track 05)."
            ),
            "eu": (
                "Varies by member state. Most member states have national patient "
                "identifiers used within their national health systems; some use "
                "general national identifiers (Sweden's personnummer, France's "
                "INS-NIR). EHDS does not impose a single EU-wide identifier but "
                "requires interoperability across the member-state identifiers."
            ),
            "uk": (
                "The NHS Number: a universal 10-digit identifier assigned to every "
                "patient in England and Wales (Scotland and Northern Ireland have "
                "equivalent national IDs). Assigned at birth or first NHS contact, "
                "used across all NHS services. Cross-organizational matching is "
                "trivial relative to the U.S. case."
            ),
        },
        "Right to data portability": {
            "us": (
                "HIPAA right of access (45 CFR 164.524) requires covered entities "
                "to provide a copy of records on request, including in electronic "
                "form where readily producible, within 30 days. The Cures Act "
                "extends this with the Patient Access API (Track 03)."
            ),
            "eu": (
                "GDPR Article 20 grants a right to data portability for data "
                "processed on consent or contract: the individual can request the "
                "data in a structured, commonly used, machine-readable format and "
                "have it transmitted to another controller. The right has limits "
                "for data processed under other lawful bases."
            ),
            "uk": (
                "UK GDPR Article 20 mirrors EU GDPR Article 20. The NHS App "
                "provides a practical implementation pathway for the patient-side "
                "portability of clinical data."
            ),
        },
        "Right to erasure of health records (right to be forgotten)": {
            "us": (
                "HIPAA does not provide a general right to have records erased; "
                "records are kept per state retention requirements (often six to "
                "ten years). Patients may request amendments; the covered entity "
                "may agree or refuse with documented reasons."
            ),
            "eu": (
                "GDPR Article 17 provides a right to erasure, but Article 17(3) "
                "carves out exceptions for processing necessary for healthcare "
                "(Article 9(2)(h)) and for public-interest archiving and research. "
                "Most clinical records cannot be erased under these exceptions, "
                "though the right exists in principle."
            ),
            "uk": (
                "UK GDPR Article 17 mirrors EU. NHS retention schedules (the NHS "
                "Records Management Code of Practice) specify retention periods "
                "that override the general erasure right for clinical records."
            ),
        },
        "Cross-border health data exchange framework": {
            "us": (
                "TEFCA (Track 02 of this course) is the U.S. framework, currently "
                "domestic only. Cross-border exchange to the EU is governed by "
                "adequacy decisions (the EU has not granted a general adequacy "
                "decision to the U.S.; the Data Privacy Framework applies to "
                "specific certified U.S. entities)."
            ),
            "eu": (
                "EHDS (Track 04, this notebook) creates a common framework for "
                "health data exchange across EU member states under common "
                "technical standards (the European Electronic Health Record "
                "Exchange Format) and Health Data Access Bodies."
            ),
            "uk": (
                "The UK is not in the EHDS (post-Brexit). The UK has an EU "
                "adequacy decision under GDPR, allowing data flows. UK-EU health "
                "data exchange operates under separate national arrangements."
            ),
        },
        "Separation of primary use (care) from secondary use (research)": {
            "us": (
                "Not formally separated at federal level. HIPAA's research provisions "
                "(45 CFR 164.512(i)) sit alongside TPO. The Common Rule governs "
                "research with human subjects through IRBs. The two regimes are "
                "interrelated rather than separated."
            ),
            "eu": (
                "EHDS makes the separation explicit. Primary use (clinical care, "
                "patient access across borders) is governed by one set of provisions "
                "with one Health Data Access Body. Secondary use (research, public "
                "health, policy) is governed by a separate set of provisions with a "
                "separate body. The structural separation is the operational "
                "innovation of EHDS."
            ),
            "uk": (
                "The UK does not have an EHDS-style formal separation, though the "
                "Health Research Authority and NHS Digital governance arrangements "
                "function similarly in practice. The 2023 Goldacre Review pushed "
                "for clearer Trusted Research Environment frameworks for secondary use."
            ),
        },
        "Information-blocking-style prohibition": {
            "us": (
                "The 21st Century Cures Act information-blocking provisions "
                "(Tracks 01 and 02), with the ONC Cures Act Final Rule and OIG "
                "enforcement. The U.S. framework is the most developed example of "
                "this kind of prohibition in any major jurisdiction."
            ),
            "eu": (
                "No direct GDPR-level equivalent. EHDS will impose interoperability "
                "obligations on member states and on health IT developers in the "
                "EU, but the structure is mandate-based rather than "
                "blocking-prohibition-based."
            ),
            "uk": (
                "No statutory equivalent. NHS procurement standards effectively "
                "mandate interoperability through certified-IT requirements rather "
                "than through a blocking prohibition."
            ),
        },
    }

    return FEATURES, mo


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 04: The international landscape

        A clinician comparing U.S. and EU health-data law often expects the comparison to reduce to HIPAA vs GDPR, with the EU being stricter. The reality has more structure. The structural differences are what determine how each system actually operates in practice and what an interoperability policy can or cannot mandate on top of the legal floor. This track covers the GDPR framework as it applies to health data, the UK NHS approach (a single-payer system with a universal patient identifier and a national integration platform), and the European Health Data Space (EHDS), the 2025 EU regulation that creates a common framework for primary and secondary use of health data across member states.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## GDPR Articles 6 and 9: the two-step structure

        GDPR applies to all processing of personal data of EU residents, regardless of where the processor is located. The structural feature that distinguishes GDPR from HIPAA is the **two-step lawful-basis requirement** for health data.

        **Article 6 lawful basis.** All processing of personal data must rest on one of six lawful bases: consent, performance of a contract, legal obligation, vital interests, public task, or legitimate interests. For clinical care, the most common Article 6 basis is public task (Article 6(1)(e)) for public-system providers, or contract (Article 6(1)(b)) for private providers, or legal obligation (Article 6(1)(c)).

        **Article 9 condition for special category data.** Health data is special category data under Article 9. Processing of special category data is prohibited by default. The prohibition is lifted only when one of ten conditions in Article 9(2) is met. The condition most commonly relied on for clinical care is **Article 9(2)(h)**: necessary for the provision of health or social care or treatment, by or under the responsibility of a professional subject to professional secrecy.

        The two-step requirement is what makes GDPR structurally stricter than HIPAA on health data. HIPAA's broad TPO permission is closer to a single permission for clinical processing; GDPR requires identifying and documenting two separate justifications. The Article 9(2)(j) research condition and the Article 9(2)(i) public-health condition are the routes to processing for secondary use; both come with additional requirements (Member State law authorizing the processing, safeguards).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The UK NHS approach: a national identifier and a national integration platform

        The UK National Health Service (NHS) is a single-payer system covering nearly all clinical care in England, with parallel systems in Scotland (NHS Scotland), Wales (NHS Wales), and Northern Ireland (HSC). The operational features that distinguish the UK from the U.S. on interoperability:

        - **The NHS Number.** A universal 10-digit identifier assigned to every patient in England and Wales at birth or first NHS contact, used across all NHS services. Scotland and Northern Ireland have equivalent national IDs (the CHI Number and the H&C Number). The patient-matching problem that occupies Track 05 of this course is largely absent: the NHS Number is the matching key.
        - **The Spine.** A central infrastructure for patient data exchange across NHS providers, operated by NHS England (which absorbed NHS Digital in 2023). The Spine carries the Personal Demographics Service (the canonical record of every patient), the Summary Care Record (the patient-portable clinical summary), and the messaging infrastructure for prescriptions and referrals.
        - **The NHS App.** The patient-facing front end to the Spine, providing a unified portal for booking appointments, viewing records, and managing prescriptions across providers.
        - **The Federated Data Platform.** A more recent initiative (2023+) for secondary-use analytics across NHS data; an analytics layer above the Spine.

        The UK approach to interoperability is **mandate-through-procurement**: NHS England specifies what certified IT must do, and IT vendors that wish to sell into the NHS conform. The mechanism is closer to a single-payer leveraging market power than to the statutory information-blocking prohibition of the U.S. Cures Act.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The European Health Data Space: primary use and secondary use as separate regimes

        The European Health Data Space (EHDS) is the EU regulation, in force since March 2025, that creates a common framework for both primary and secondary use of health data across EU member states. The implementation timeline runs through 2035, with the first operational milestones at 2027 (primary use for some data classes) and 2029 (secondary use).

        Two structural innovations of EHDS deserve attention.

        **Formal separation of primary and secondary use.** EHDS treats clinical care and secondary use (research, public health surveillance, policy-making, regulatory) as distinct regimes, with different rights for the individual, different access mechanisms, and different national bodies. Each member state designates a Digital Health Authority for primary use and a Health Data Access Body for secondary use; the two have separate governance.

        **The European Electronic Health Record Exchange Format (EEHRxF).** A common technical standard that member-state EHR systems must support to participate in cross-border exchange. The format is built on HL7 FHIR R4 with EU-specific profiles; the structural choice mirrors the U.S. choice of FHIR R4 (Track 03), with different IGs.

        The EHDS framework does not impose a single EU-wide patient identifier, but it does require member-state identifiers to be exchangeable. The Cures-Act-style information-blocking prohibition has no direct EHDS equivalent; EHDS works through interoperability mandates on certified IT and on member-state systems.
        """
    )
    return


@app.cell
def _(FEATURES, mo):
    feature_pick = mo.ui.dropdown(
        options=list(FEATURES.keys()),
        value=list(FEATURES.keys())[0],
        label="Feature",
    )
    mo.vstack(
        [
            mo.md(
                "## Compare U.S., EU (GDPR), and UK (NHS) on a feature\n\n"
                "**Pick a feature.** The reactive panel below shows how each "
                "jurisdiction handles it, with the structural differences identified."
            ),
            feature_pick,
        ]
    )
    return (feature_pick,)


@app.cell
def _(FEATURES, feature_pick, mo):
    _info = FEATURES[feature_pick.value]
    _body = (
        f"### {feature_pick.value}\n\n"
        "**United States (HIPAA + Cures Act)**\n\n"
        f"{_info['us']}\n\n"
        "**European Union (GDPR + EHDS)**\n\n"
        f"{_info['eu']}\n\n"
        "**United Kingdom (UK GDPR + NHS)**\n\n"
        f"{_info['uk']}"
    )
    mo.callout(mo.md(_body), kind="neutral")
    return


@app.cell
def _(mo):
    int_quiz = mo.ui.radio(
        options=[
            "GDPR requires both an Article 6 lawful basis and an Article 9 condition for processing health data; HIPAA's TPO permission requires neither.",
            "EHDS imposes a Cures-Act-style information-blocking prohibition across the EU.",
            "The UK has no national patient identifier and relies on probabilistic matching.",
            "The U.S. Cures Act and the EU EHDS both formally separate primary and secondary use of health data.",
        ],
        label=(
            "Which of the following accurately characterizes a structural difference "
            "between the U.S., EU, and UK health-data frameworks?"
        ),
    )
    int_quiz
    return (int_quiz,)


@app.cell
def _(int_quiz, mo):
    if int_quiz.value is None:
        _resp = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif int_quiz.value.startswith("GDPR requires both"):
        _resp = mo.callout(
            mo.md(
                "**Correct.** This is the operational difference. GDPR Article 6 "
                "names the lawful basis (a public task, a contract, or another of "
                "the six grounds), and Article 9 names the special-category "
                "condition (most commonly 9(2)(h) for healthcare provision). HIPAA's "
                "TPO permission rolls all of this into a single broad permission for "
                "treatment, payment, and healthcare operations. The two-step "
                "structure is what makes GDPR substantively stricter than HIPAA on "
                "health-data processing."
            ),
            kind="success",
        )
    elif int_quiz.value.startswith("EHDS imposes"):
        _resp = mo.callout(
            mo.md(
                "**Not accurate.** EHDS is built on interoperability mandates "
                "(certified IT requirements, the European Electronic Health Record "
                "Exchange Format, Health Data Access Bodies), not on a Cures-Act-"
                "style information-blocking prohibition. There is no direct EHDS "
                "equivalent to the U.S. blocking statute. The U.S. Cures Act remains "
                "the most developed example of this kind of prohibition in any "
                "major jurisdiction."
            ),
            kind="warn",
        )
    elif int_quiz.value.startswith("The UK has no national"):
        _resp = mo.callout(
            mo.md(
                "**Not accurate.** The UK has the NHS Number (a universal 10-digit "
                "identifier for every patient in England and Wales, with equivalents "
                "in Scotland and Northern Ireland). The NHS Number largely solves "
                "the cross-organizational patient-matching problem that occupies "
                "Track 05 of this course. The country without a national patient "
                "identifier is the United States; HIPAA Section 1173(b) authorized "
                "one in 1996 but an appropriations rider has prevented its funding "
                "every fiscal year since 1999."
            ),
            kind="warn",
        )
    else:
        _resp = mo.callout(
            mo.md(
                "**Not accurate.** EHDS formally separates primary and secondary "
                "use of health data (each with a distinct national body and a "
                "distinct set of provisions). The U.S. framework does not have an "
                "equivalent formal separation; HIPAA's research provisions sit "
                "alongside TPO under the same regulation, and the Common Rule "
                "governs human-subjects research separately. The structural "
                "separation is one of EHDS's operational innovations."
            ),
            kind="warn",
        )
    _resp
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Where this goes next

        Comparing the U.S., EU, and UK frameworks surfaces which features of the U.S. configuration are deliberate choices and which are constraints of the U.S. legal and market structure. Track 05 picks up the U.S.-specific gaps that the international comparison highlights: the absent national patient identifier (the most obvious structural lag relative to the UK and the EU member states), the USCDI cadence relative to clinical need, and the HTI-1 AI-transparency provisions whose enforcement infrastructure is still being built.
        """
    )
    return


if __name__ == "__main__":
    app.run()
