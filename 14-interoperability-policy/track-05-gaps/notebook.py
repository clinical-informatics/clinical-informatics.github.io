"""Track 05: Where the gaps still are.

No visible code. The notebook names the three load-bearing remaining gaps
in the U.S. interoperability framework (patient matching, USCDI cadence,
HTI-1 DSI enforcement infrastructure), runs the reader through a reactive
deep-dive on each, and closes on the cross-cutting theme that standards
lag clinical practice.

WASM-safe: no shared imports, no data files, no relative paths.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    GAPS = {
        "Absent national patient identifier (patient matching)": {
            "current_state": (
                "The United States has no national patient identifier. HIPAA Section "
                "1173(b) in 1996 authorized one and directed HHS to adopt one. An "
                "appropriations rider added to every HHS appropriations bill since "
                "fiscal year 1999 prohibits HHS from spending appropriated funds on "
                "developing or implementing it. The result is that cross-organizational "
                "matching relies on probabilistic algorithms over combinations of "
                "demographics (name, date of birth, address, phone, partial SSN). "
                "Published match rates between health systems range from 50% to 90% "
                "depending on data quality and algorithm choice; the unmatched fraction "
                "becomes a duplicate record on one or both sides."
            ),
            "policy_mechanism": (
                "Three mechanisms partially compensate for the absent identifier. "
                "TEFCA (Track 02) provides a coordinated cross-network identity-"
                "matching framework managed by The Sequoia Project as the Recognized "
                "Coordinating Entity. ONC has periodically issued patient-matching "
                "algorithm guidance and conducts ongoing research. Private "
                "initiatives (the CommonWell-Carequality framework, vendor-specific "
                "EMPI tools) operate at the network level. None of the three closes "
                "the structural gap that the identifier prohibition creates."
            ),
            "trajectory": (
                "The appropriations rider has been challenged each Congress since "
                "approximately 2019; the House has voted to remove it on multiple "
                "occasions but the Senate has not. Industry coalitions (CHIME, AHA, "
                "AHIMA) continue to advocate for removal. The likely near-term "
                "trajectory is continued reliance on TEFCA and probabilistic matching, "
                "with the structural problem unresolved into the 2030s. EHDS pressure "
                "may indirectly accelerate the U.S. conversation through cross-border "
                "matching requirements."
            ),
        },
        "USCDI cadence vs clinical need": {
            "current_state": (
                "USCDI evolves on a roughly annual cadence (v1 in 2020, v2 in 2021, "
                "v3 in 2022, v4 in 2023, v5 in 2024, v6 in July 2025, with v7 in "
                "draft in early 2026). Each version adds data classes that respond to "
                "clinical and policy demand: social determinants in v3, behavioral "
                "health in v5, encounter outcomes in v6. The data classes that lag "
                "are those that require new standards work or new consensus: "
                "AI-model outputs, longitudinal patient-reported outcomes at "
                "population scale, harmonized SDOH at population scale."
            ),
            "policy_mechanism": (
                "ONC's annual USCDI maintenance cycle is the mechanism. The cycle: "
                "ASTP/ONC publishes a draft USCDI version, takes comments, finalizes "
                "the new version, then incorporates the new version into a "
                "rulemaking (HTI-1, HTI-2, etc.) that makes it the certification "
                "baseline. Each step adds 12 to 24 months of delay; certified-EHR "
                "vendor implementation adds another 12 to 36 months. The result is "
                "that a clinical need identified today shows up in production EHRs "
                "in 2 to 5 years."
            ),
            "trajectory": (
                "The cadence is unlikely to accelerate significantly without "
                "structural change to the rulemaking process. The data classes "
                "currently in draft or under consideration (AI-model outputs, "
                "structured care plans, expanded patient-reported outcomes) will "
                "appear in USCDI v7 and v8 over the next two to four years. The gap "
                "between the standards-floor and the clinical state-of-the-art will "
                "persist."
            ),
        },
        "HTI-1 DSI requirements vs enforcement infrastructure": {
            "current_state": (
                "HTI-1 (Track 03) introduced the Decision Support Intervention "
                "requirements: certified developers that integrate DSIs (rule-based "
                "or predictive, including AI/ML) into their products must disclose "
                "specified source attributes for each DSI. The disclosures cover "
                "intervention name, purpose, data inputs, intended use, output type, "
                "training population, performance characteristics, and subgroup "
                "performance. The substantive requirements are in place. The "
                "enforcement infrastructure (the audit mechanisms, the OIG "
                "referrals, the civil monetary penalties applied to algorithmic "
                "non-disclosure specifically) is still being built out as of 2026."
            ),
            "policy_mechanism": (
                "ONC enforces through certification review (a developer's certified "
                "product can be decertified for non-compliance). OIG enforces against "
                "developers and HIEs for information-blocking-style practices, which "
                "may include systematic non-disclosure of DSI source attributes. The "
                "two enforcement pathways are nominally in place but have not "
                "produced significant case law specifically on DSI disclosure. The "
                "compliance landscape is in the early phase that information-blocking "
                "enforcement was in 2020 to 2022."
            ),
            "trajectory": (
                "The likely 2026 to 2028 trajectory is the first wave of audits and "
                "complaints. Vendors that integrated AI features without disclosure "
                "in 2024 to 2025 are the first cohort the requirements apply to; the "
                "first enforcement actions will set the practical compliance floor. "
                "Course 09's evaluation framework becomes increasingly important as "
                "the disclosure requirements give clinicians and procurement "
                "committees the structured information to evaluate."
            ),
        },
    }

    return GAPS, mo


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 05: Where the gaps still are

        After the Cures Act, after HTI-1 and HTI-2, after TEFCA's QHIN network became operational, and after USCDI reached v6 in 2025 with v7 in draft, what does an interop-curious clinician still find broken? The honest answer is patient matching, the slow USCDI cadence relative to clinical need, and the AI-transparency provisions that HTI-1 created but that enforcement infrastructure has not yet caught up to. This track names each remaining gap, the policy mechanism that addresses or partially addresses each, and the realistic trajectory through the late 2020s.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The three gaps at a glance

        Three gaps remain operationally significant after the major rulemakings of 2020 and 2024.

        | Gap | Status | Why it remains |
        |---|---|---|
        | **Patient matching** | Unresolved. Match rates 50% to 90% across health systems. | HIPAA in 1996 authorized a national patient identifier; an appropriations rider has prevented its funding every fiscal year since 1999. |
        | **USCDI cadence** | Improving on a one-year clock, lagging clinical need by 2 to 5 years. | The rulemaking-implementation-vendor-deployment chain adds 24 to 60 months between identifying a data class need and it appearing in certified EHRs. |
        | **HTI-1 DSI enforcement** | Substantive rule in place; enforcement infrastructure still being built. | The DSI transparency rule took effect in 2024; the audit, complaint, and penalty pathways are operating at low volume as of 2026. |

        Each gap connects to a separate policy mechanism with a separate trajectory. The reactive deep-dive below covers each one.
        """
    )
    return


@app.cell
def _(GAPS, mo):
    gap_pick = mo.ui.dropdown(
        options=list(GAPS.keys()),
        value=list(GAPS.keys())[0],
        label="Gap",
    )
    mo.vstack(
        [
            mo.md(
                "## Reactive deep-dive\n\n"
                "**Pick a gap.** The reactive panel below covers the current state, "
                "the policy mechanism that addresses it (in part or in full), and "
                "the realistic trajectory through the late 2020s."
            ),
            gap_pick,
        ]
    )
    return (gap_pick,)


@app.cell
def _(GAPS, gap_pick, mo):
    _info = GAPS[gap_pick.value]
    _body = (
        f"### {gap_pick.value}\n\n"
        "**Current state**\n\n"
        f"{_info['current_state']}\n\n"
        "**Policy mechanism**\n\n"
        f"{_info['policy_mechanism']}\n\n"
        "**Trajectory through the late 2020s**\n\n"
        f"{_info['trajectory']}"
    )
    mo.callout(mo.md(_body), kind="neutral")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A cross-cutting theme: standards lag clinical practice

        The three gaps differ in cause but share a structural feature. Each one is a case in which the standards layer and the policy layer move on a slower clock than the clinical practice they govern. Patient matching has been a known problem for thirty years; USCDI's data-class gaps are years behind documented clinical workflows; the HTI-1 DSI requirements were finalized in 2024 for AI features that had been integrated into EHRs from 2018 onward. The lag is structural to a multi-agency, multi-stakeholder regulatory framework, and the practical consequence is that an informaticist working in any of these areas is operating against a moving target where the regulatory floor is several years behind the practical question.

        This is the recurring substrate of policy work: the rules describe a state the field has already passed through, and the working informaticist's job is partly to anticipate where the rules will eventually catch up to.
        """
    )
    return


@app.cell
def _(mo):
    trajectory_quiz = mo.ui.radio(
        options=[
            "Patient matching, because TEFCA and the Sequoia framework are closing the gap on a 2026 to 2028 trajectory.",
            "USCDI cadence, because the annual maintenance cycle and the v7 draft will largely close the standards-floor gap.",
            "HTI-1 DSI enforcement, because the first wave of audits and OIG referrals in 2026 to 2028 will produce the case law that sets the compliance floor.",
            "None of the three is likely to close before 2030; each has structural barriers that the policy mechanisms only partially address.",
        ],
        label=(
            "Which of the three gaps is most likely to be substantially closed by "
            "the end of the decade through the policy mechanisms already in motion?"
        ),
    )
    trajectory_quiz
    return (trajectory_quiz,)


@app.cell
def _(mo, trajectory_quiz):
    if trajectory_quiz.value is None:
        _resp = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif trajectory_quiz.value.startswith("HTI-1 DSI enforcement"):
        _resp = mo.callout(
            mo.md(
                "**This is the most defensible reading.** The HTI-1 DSI substantive "
                "requirements are in place; the question is enforcement infrastructure, "
                "which is the kind of capacity that builds out within a few years once "
                "the first audits and OIG referrals create the compliance template. By "
                "the late 2020s the framework is likely to have produced specific case "
                "law on DSI disclosure that sets the practical floor for certified "
                "developers. The patient-matching gap is structurally harder (the "
                "appropriations rider is not on a timeline). The USCDI cadence gap is "
                "structural to the rulemaking process. The DSI enforcement gap is "
                "the most likely to close in this window."
            ),
            kind="success",
        )
    elif trajectory_quiz.value.startswith("Patient matching"):
        _resp = mo.callout(
            mo.md(
                "**Patient matching is unlikely to close by 2030 through the current "
                "mechanisms alone.** TEFCA and the Sequoia framework improve "
                "cross-organizational matching, but they operate over the same "
                "probabilistic algorithms; without a national patient identifier, "
                "the structural gap remains. The appropriations rider that has "
                "prevented identifier funding every fiscal year since 1999 has not "
                "been removed, and removal is not on a clear timeline. The realistic "
                "trajectory is continued reliance on TEFCA and probabilistic matching "
                "into the 2030s, not closure."
            ),
            kind="warn",
        )
    elif trajectory_quiz.value.startswith("USCDI cadence"):
        _resp = mo.callout(
            mo.md(
                "**The USCDI cadence gap is structural to the rulemaking process.** "
                "The annual maintenance cycle closes specific data-class gaps over "
                "time, and v6 and v7 add useful classes. The gap between the "
                "standards floor and clinical state-of-the-art is unlikely to "
                "narrow significantly by 2030, because the rulemaking, certification, "
                "and vendor-deployment chain remains 24 to 60 months long. The gap "
                "is improvable but not closeable through the current mechanisms."
            ),
            kind="warn",
        )
    else:
        _resp = mo.callout(
            mo.md(
                "**Plausibly defensible, but probably too pessimistic on at least one "
                "of the three.** The patient-matching gap is structurally hard and "
                "the USCDI cadence gap is structural, so neither is likely to close "
                "by 2030. The HTI-1 DSI enforcement gap is the most likely of the "
                "three to substantially close, because the enforcement infrastructure "
                "is the kind of capacity that builds out within a few years once the "
                "first audits and OIG referrals create the compliance template."
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

        Track 05 named the gaps; the course capstone applies the full policy framework to three real-shaped scenarios in which a patient cannot get their records, a researcher cannot access a vendor dataset, and a vendor restricts data. Each scenario asks the reader to identify the applicable policy (Cures Act, HIPAA, CMS rule, EHDS, NHS), what the policy requires, and what recourse exists. The capstone is where the five tracks of the course assemble into the practical analytic move a clinician or informaticist would make when handed one of these situations.
        """
    )
    return


if __name__ == "__main__":
    app.run()
