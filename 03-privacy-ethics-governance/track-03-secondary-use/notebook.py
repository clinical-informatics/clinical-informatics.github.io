"""Track 03: Secondary use of clinical data.

A patient consents to a blood draw. The resulting row passes through the
EHR, the CDW, a research extract, an AI training set, a conference
benchmark. The patient consented to the first step. This notebook is
about the rest. Five pieces: the primary/secondary distinction; the gap
between legal permission and ethical defensibility (with the Lacks,
Havasupai, and Project Nightingale cases); consent, broad consent, and
waivers; the five-dimensional ethical risk framework; and the
commercial-vs-academic-vs-translational archetypes. The interactive
piece is a scenario analyzer that walks the five dimensions on six
realistic secondary-use scenarios.
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
        # Track 03: Secondary use of clinical data

        ## The path the data actually takes

        A patient consents to a blood draw. Her rheumatologist needs to monitor CRP. The lab runs the test, the value goes into the EHR, and her care proceeds. That is what she consented to.

        Then the row in the lab table flows into the CDW. From the CDW it flows into a research extract for a retrospective cohort study, IRB-waived because the data is de-identified. The same row flows into a vendor analytics partnership the institution signed to develop predictive models. The same row flows into a public benchmark dataset released at a machine learning conference. The same row flows into the training set of a commercial AI tool that the institution then licenses back from the vendor for clinical deployment.

        Every step in that chain may be legally permitted under HIPAA. None of those steps was what the patient consented to at the moment of the blood draw.

        That gap is what this track is about.

        Five pieces:

        1. **The primary/secondary distinction.** What "everything else" actually contains.
        2. **The legal/ethical gap.** Three landmark cases (Lacks, Havasupai, Project Nightingale).
        3. **Consent, broad consent, and waivers.** What patients are actually being asked.
        4. **Five dimensions of ethical risk.** A framework you can apply to any proposed use.
        5. **Commercial vs academic vs translational.** Where the data goes matters.

        Then a scenario analyzer.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1. Primary use vs secondary use

        **Primary use** is the use the data was collected for: caring for the patient who produced it. The CRP was drawn to monitor her RA. The diagnosis was coded to bill the encounter. The note was written to document the visit.

        **Secondary use** is everything else. In modern clinical informatics, "everything else" covers a lot:

        | Category | What it looks like | Who benefits |
        |---|---|---|
        | **Quality improvement** | Internal evaluation of sepsis bundle compliance | The institution; future patients at the institution |
        | **Healthcare operations** | Financial reporting, utilization analysis, payer activities | The institution; the payer |
        | **Public health surveillance** | State reporting, infectious-disease tracking | The public |
        | **Academic research** | A published cohort study on diabetes complications | The research community; future patients (eventually) |
        | **Translational research** | Linking observational data to biomarker discovery | The research community; future patients |
        | **AI/ML model training** | Building a deterioration predictor on historical encounters | The institution; the vendor (if external) |
        | **Commercial product development** | Pharma access to data for drug development | The pharmaceutical company; future patients (eventually); shareholders |
        | **Public benchmark releases** | A de-identified dataset shared at a conference | The ML research community |

        A row in a CRP table can pass through several of these in succession. The patient consented to none of them at the moment of the blood draw.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2. Why legal and ethical don't coincide

        Track 02 walked HIPAA. HIPAA's TPO (Treatment, Payment, Operations) permission is broad. "Healthcare operations" includes quality assessment, developing clinical guidelines, business planning, and general administrative activities. Most secondary use within a covered entity fits one of those categories.

        But the framework was written in 1996. It assumes a world where clinical data is used by the institution that collected it. That assumption has loosened. Three cases show what happens when the framework's permissions are honored but the assumptions don't hold.

        ### Henrietta Lacks and HeLa (1951 to today)

        Henrietta Lacks, a Black woman with cervical cancer treated at Johns Hopkins in 1951. A tumor sample was taken without her knowledge (the norm at the time). The cells turned out to grow indefinitely in culture; they became the most widely used cell line in biomedical research, underpinning the polio vaccine, IVF, the human genome project, and dozens of Nobel-winning discoveries.

        Her family didn't learn of HeLa for two decades. They received no compensation, no recognition, no say in how the cells were used. The 2013 NIH-Lacks Family Agreement finally gave the family input into HeLa genome access decisions, sixty-two years after the cells were taken.

        **The thread.** What was permitted in 1951 was not what would be permitted today, but the underlying lesson holds: when data outlives the moment of collection and accrues large value, the people whose bodies produced it have no standing unless governance was built in from the start.

        ### Havasupai Diabetes Project (1990s to 2010)

        The Havasupai Tribe consented to blood collection at Arizona State University for type 2 diabetes research. The samples were also used (without specific consent) for studies of schizophrenia, inbreeding, and migration patterns. Some findings contradicted Tribal religious narratives about origin. All of the studies used samples for purposes the donors hadn't agreed to.

        After years of litigation, ASU returned the samples and paid the Tribe $700,000.

        **The thread.** Consent isn't a blank check. Specific-purpose collections cannot be silently repurposed. The Revised Common Rule's broad-consent provisions (2018) were partly a response to this case.

        ### Project Nightingale (Google + Ascension, 2019)

        Ascension partnered with Google to migrate data infrastructure to Google Cloud. The arrangement gave Google access to medical records of tens of millions of patients across 21 states for the purpose of building clinical-assistance software. The partnership was disclosed in a Wall Street Journal investigation, not in a public announcement. Patients were not told.

        Legally: Ascension and Google argued the arrangement was a Business Associate relationship under HIPAA, with a Business Associate Agreement in place. The argument was correct as a matter of HIPAA.

        Publicly: the response was sharply negative. The HHS Office for Civil Rights opened an investigation. Congressional committees demanded answers. The case became the canonical example of HIPAA-compliant practice that nonetheless violated the social contract.

        **The thread.** The Business Associate category was written in 1996 for the billing service and the transcription company. It now covers cloud partnerships that fundamentally restructure who has access to patient records, with what tools, for what purposes. The legal definition hasn't been updated; the practical implications have changed substantially.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3. Consent, broad consent, and waivers

        ### What patients actually consent to at intake

        A patient signs three to five forms at most outpatient intake visits:

        - **Notice of Privacy Practices** acknowledgment. Describes (in dense legal language) what the institution may do with PHI under HIPAA TPO and what needs authorization. Most patients don't read it.
        - **Financial responsibility** agreement.
        - **Treatment consent** for the planned care.
        - **Research consent** for specific protocols (if applicable).
        - **Broad consent** for "future research" use of leftover specimens/data (if the institution uses one).

        The first three are reasonably understood. The fourth is study-specific. The fifth (broad consent) is the contested one.

        ### Broad consent

        The Revised Common Rule (2018) added explicit provisions for broad consent: a patient can give blanket consent for future research use of identifiable data and specimens, *provided* the consent describes the categories of research and the institution honors those categories.

        Broad consent buys flexibility (reduces re-consent burden for every new study). It also potentially buys patient trust over time, **if** the institution honors the described categories. The Havasupai case shows what happens when it doesn't.

        ### IRB waivers of consent

        An IRB can waive the requirement for individual consent for research using PHI when four conditions are met:

        1. The research involves no more than minimal risk to subjects.
        2. The waiver will not adversely affect the rights and welfare of subjects.
        3. The research could not practicably be carried out without the waiver.
        4. Subjects will be provided with additional pertinent information after participation, where appropriate.

        These criteria are tight on paper. In practice they are met routinely for retrospective EHR research, because individually consenting tens of thousands of past patients is not practicable. The waiver is the default operational path for most secondary-use research on existing data.

        The honest framing: the waiver is a **trade**. The research couldn't happen without it; the patients can't realistically have been asked. The trade is defensible only if the research is genuinely valuable to a group that includes the patients, and doesn't expose them to harm. The IRB enforces the trade procedurally. The ethical defensibility depends on whether the trade was honest.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 4. The five dimensions of ethical risk

        A framework for evaluating any proposed secondary use. None are binary; all are sliders.

        ### 1. Consent-expectation fit

        Does the proposed use match what a reasonable patient would have expected when they consented to care? "Internal QI" fits intuitively. "Pharma deal for drug development" does not.

        **Operational check.** If you described the proposed use to a sample of the patients whose data is involved, what fraction would say "that's what I thought my data was for?"

        ### 2. Public vs commercial benefit balance

        Where does the benefit accrue? Public-health study published openly → public. Model sold commercially → company and its customers. The same dataset can support both, but the framing matters.

        **Not** a "commercial is bad" framing. Drug development is commercial; new drugs benefit patients. The framing should be honest about who benefits and how much.

        ### 3. Equity

        Whose data, whose interests?

        - **Inclusion equity.** Is the dataset representative of the population the work will affect?
        - **Burden equity.** Are the costs (privacy risk, opportunity costs) fairly distributed?
        - **Benefit equity.** Will the results help the population the data came from?

        A model trained on white patients at AMCs, deployed in safety-net hospitals serving Black patients, fails all three.

        ### 4. Transparency

        Could a patient find out what's happening with their data if they wanted to?

        Project Nightingale failed this one. The partnership was disclosed by journalists, not by the institutions. HIPAA didn't require disclosure; the trust framework, in retrospect, did.

        Transparency can be at multiple levels: institutional disclosure (a public statement), individual notice (a letter to affected patients), ongoing reporting (annual transparency reports). The wrong level is none.

        ### 5. Reversibility

        Can a patient withdraw their data if they object?

        - Broad consent: typically yes, with limits on data already used.
        - Waiver of consent: typically no.
        - Data sold under a DUA: depends on DUA terms; partner often retains extracts.
        - Data used to train a deployed model: the model often cannot be untrained.

        Low reversibility is not automatically wrong; some research needs locked-in data. But it increases the importance of every other dimension, because the patient has no recourse.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 5. Commercial vs academic vs translational

        Where the data goes matters. The destination changes the ethical analysis even when the dataset is the same.

        | Archetype | Typical ethical risk profile |
        |---|---|
        | **Internal QI** | Low across dimensions when scope is clear |
        | **Academic publication** | Low to medium; depends on whether research benefits the patient population |
        | **Cross-institutional research network** (TriNetX, OHDSI, AllOfUs) | Medium; depends on governance and consent process |
        | **Public benchmark release** | Medium; once released, cannot recall. Equity in who can use it matters. |
        | **Pharma research partnership** | Medium-high; commercial benefit framing requires explicit disclosure |
        | **Vendor analytics partnership** | High; other vendor customers may benefit from learnings derived from this institution's patients |
        | **Model deployment with vendor branding** | High; patients whose data trained it have no stake in continued use |

        The framework isn't to rule out high-risk archetypes. The framework requires that high-risk archetypes carry proportionate disclosure, consent, governance, and benefit-sharing.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 6. Scenario analyzer

        Six realistic secondary-use scenarios. Pick one. Score risk along each of the five dimensions before clicking through to the worked analysis. The point isn't to produce a number; it's to make the dimensions visible.
        """
    )
    return


@app.cell
def _(mo):
    scenario_pick = mo.ui.dropdown(
        options=[
            "1. Internal QI on sepsis bundle compliance",
            "2. Academic publication: retrospective cohort on diabetes complications",
            "3. Hospital sells de-identified data to a pharma company for drug development",
            "4. Vendor partnership: cloud AI company processes records to build a clinical-assist tool",
            "5. Conference benchmark: de-identified chest X-rays released to ML researchers worldwide",
            "6. Genetic data collected for cardiovascular study repurposed for population genetics",
        ],
        value="1. Internal QI on sepsis bundle compliance",
        label="Pick a scenario to analyze",
    )
    scenario_pick
    return (scenario_pick,)


@app.cell
def _(mo):
    scenario_details = {
        "1.": {
            "description": (
                "**The setup.** A 600-bed academic medical center analyzes 24 months of inpatient records "
                "to evaluate compliance with the 3-hour and 6-hour sepsis bundles. The work is done by the "
                "internal quality and safety office using already-de-identified data on institutional servers. "
                "Results are presented at the hospital's quality committee and used to redesign the sepsis "
                "order set. No publication is planned, no external party has access, and no individual "
                "patients are re-contacted."
            ),
            "fit": (
                "**HIGH fit.** Patients who came to this hospital reasonably expected their hospital to use "
                "their care data to improve the hospital's sepsis care. This is the central case for what "
                "HIPAA's TPO operations carve-out was designed to permit, and it matches reasonable patient "
                "expectations almost exactly."
            ),
            "public_vs_commercial": (
                "**Public/internal.** Benefit accrues to future patients at the same institution. No commercial "
                "party benefits. No external publication."
            ),
            "equity": (
                "**Aligned.** The patient population whose data is used is the same population the redesigned "
                "order set will serve. Inclusion, burden, and benefit equity all align."
            ),
            "transparency": (
                "**Adequate.** Disclosure is via the Notice of Privacy Practices, which describes operations "
                "uses. The quality committee's findings are typically reported in institutional channels. "
                "No special transparency mechanism is needed for an internal QI project of this scope."
            ),
            "reversibility": (
                "**Low but appropriate.** Patients cannot withdraw individual records from an internal "
                "operations analysis (which is fine; that's not the threshold for this kind of work)."
            ),
            "verdict": (
                "**Overall: low risk across all five dimensions.** This is the canonical use case for HIPAA "
                "operations. No additional ethical review is typically required beyond the institution's "
                "standard QI governance. The interesting question is what gets *added* to make it interesting "
                "from this baseline (publication intent makes it academic research; an external vendor makes "
                "it a partnership; a deployed AI tool makes it product development)."
            ),
        },
        "2.": {
            "description": (
                "**The setup.** A faculty researcher at the same institution conducts a retrospective cohort "
                "study using de-identified EHR data on diabetic patients, 2018-2024, examining the relationship "
                "between SGLT2 inhibitor adoption and downstream cardiovascular outcomes. The work is "
                "IRB-approved under expedited review with a waiver of individual authorization. Results "
                "will be submitted to a peer-reviewed cardiology journal."
            ),
            "fit": (
                "**Medium-high fit.** Patients at an academic medical center generally understand that their "
                "data may be used in research, and most surveys show patients support de-identified research "
                "use. The IRB waiver of authorization is operating as designed (research couldn't be practicably "
                "done with individual consent; minimal risk; data are de-identified). The fit is solid but "
                "imperfect because the patients weren't specifically asked about *this* study."
            ),
            "public_vs_commercial": (
                "**Public.** Results will be peer-reviewed and openly published. If the findings are useful, "
                "they inform clinical practice broadly. No commercial party benefits directly."
            ),
            "equity": (
                "**Depends on cohort.** If the academic medical center's patients are demographically "
                "representative of patients who will be affected by the findings (e.g., predominantly insured, "
                "predominantly white in many AMC settings), the equity scoring is medium. If the cohort is "
                "unrepresentative of the populations most affected by diabetes complications, the equity "
                "score drops and the discussion section needs to address generalizability explicitly."
            ),
            "transparency": (
                "**Adequate.** IRB review is itself a transparency mechanism; the protocol is on file; the "
                "publication makes the work public. The patient population is not individually notified, but "
                "the operations of the IRB system are well-publicized."
            ),
            "reversibility": (
                "**Low.** Once a paper is published, the analysis cannot be unpublished. Individual patients "
                "cannot withdraw retroactively. This is normal for waiver-of-authorization research and the "
                "trade-off is what the IRB review is supposed to police."
            ),
            "verdict": (
                "**Overall: low-medium risk.** The IRB waiver framework is doing its job. The interesting "
                "questions are equity (is the cohort representative of who the findings affect?) and whether "
                "the institution communicates to its broader patient community that this kind of research "
                "happens routinely with their data. Both are improvable beyond the baseline of 'IRB approved.'"
            ),
        },
        "3.": {
            "description": (
                "**The setup.** The same institution licenses a de-identified extract of 200,000 patient records "
                "(demographics, diagnoses, medications, lab values, encounter data) to a major pharmaceutical "
                "company for ten years. The pharma company will use the data for drug development research. "
                "Patients are not notified. The arrangement is governed by a DUA. The institution receives "
                "$5 million."
            ),
            "fit": (
                "**Low fit.** Most patients, asked directly, do not expect that their de-identified records "
                "have been sold to a pharma company. Survey data on this kind of arrangement consistently "
                "show patient discomfort, even when the arrangement is HIPAA-compliant. The Notice of Privacy "
                "Practices may technically permit the disclosure (some institutions disclose 'sales' of "
                "de-identified data; many do not). The legal compliance does not close the expectation gap."
            ),
            "public_vs_commercial": (
                "**Highly commercial.** The primary beneficiary is the pharma company and its shareholders. "
                "Eventual drugs may benefit patients, but the route is long, uncertain, and mediated by "
                "the company's commercial strategy. The institution receives a direct payment."
            ),
            "equity": (
                "**Mixed.** Inclusion equity depends on the dataset's representativeness. Burden equity is "
                "skewed: the patients bear the privacy risk; the institution and the company capture the "
                "benefit. Benefit equity is uncertain: drugs benefit patients eventually, but not necessarily "
                "the patients whose data was used."
            ),
            "transparency": (
                "**Typically low.** Most institutional data-licensing arrangements are not disclosed "
                "individually to affected patients. Some institutions list partnerships at a high level on "
                "their websites; many do not. The arrangement may be HIPAA-compliant and still essentially "
                "invisible to the people whose data is involved."
            ),
            "reversibility": (
                "**Very low.** The DUA typically grants the pharma company the right to retain and use the "
                "data for the contracted term. Individual patients cannot withdraw. The institution may "
                "be unable to recover the data if the partner is acquired or the partnership ends."
            ),
            "verdict": (
                "**Overall: high risk.** Legally permissible; ethically contested. The path to improvement "
                "involves explicit institutional disclosure (a public listing of partnerships; a population-level "
                "notice through the patient portal), benefit sharing (a portion of the licensing revenue "
                "directed to patient-facing services), and structured patient consultation (a patient advisory "
                "board involved in approving partnerships). The DUA-and-de-identification framework is the "
                "minimum; it is not sufficient to close the trust gap."
            ),
        },
        "4.": {
            "description": (
                "**The setup.** Same institution enters into a partnership with a cloud-based AI vendor. "
                "Identifiable PHI flows to the vendor (governed by a Business Associate Agreement) for the "
                "purpose of building a clinical-assistance tool. The vendor will deploy the tool back at the "
                "institution. Whether the vendor uses learnings from this institution's data to improve "
                "products sold to other customers is described in the BAA but not in patient-facing materials. "
                "Patients are not individually notified; the partnership is described at a high level on the "
                "institution's website."
            ),
            "fit": (
                "**Low fit.** This is approximately the Project Nightingale fact pattern. Reasonable patients "
                "would not expect their identifiable records to be processed by an external technology company. "
                "The legal framework (BAA) permits it. The expectation gap is substantial."
            ),
            "public_vs_commercial": (
                "**Mixed but heavily commercial.** The tool will eventually benefit clinical workflows at the "
                "institution (clinical benefit). The vendor benefits commercially (product development, "
                "future sales). Patients' data is the input; the vendor's business and the institution's "
                "operations are the outputs."
            ),
            "equity": (
                "**Concerning.** Inclusion equity depends on the institution's patient mix. Burden equity is "
                "skewed (patients carry the privacy risk; the vendor captures the data advantage). Benefit "
                "equity depends on whether the deployed tool actually helps the patients whose data trained "
                "it, and whether the vendor's other customers (potentially safety-net hospitals serving "
                "different populations) get a tool that wasn't trained on their patients."
            ),
            "transparency": (
                "**Inadequate by post-Nightingale standards.** A high-level website description is the bare "
                "minimum and was insufficient in the Nightingale case. Individual patient notification, "
                "ongoing reporting on what the vendor is learning and building, and a clear public statement "
                "of what 'learnings' from this institution's data may go into the vendor's other products "
                "are all reasonable transparency commitments."
            ),
            "reversibility": (
                "**Very low.** Once data has been processed by the vendor and used to train models, the "
                "models cannot be untrained. The vendor may retain derived insights even after the partnership "
                "ends. Individual patients have no withdrawal pathway."
            ),
            "verdict": (
                "**Overall: high risk.** The HHS investigation of Project Nightingale specifically tested "
                "whether this archetype was HIPAA-compliant; the answer was substantially yes. The public "
                "reaction made clear that 'HIPAA-compliant' was not sufficient. The improvements that close "
                "the trust gap involve substantive disclosure, explicit limits on what the vendor may do with "
                "the data outside the institution, ongoing reporting, and ideally a patient advisory board "
                "with real decision-making authority."
            ),
        },
        "5.": {
            "description": (
                "**The setup.** The institution releases a de-identified dataset of 500,000 chest X-rays "
                "(paired with diagnoses and demographics) at a major machine learning conference for "
                "community algorithm development. The dataset is freely downloadable; the institution does "
                "not control downstream use. The dataset was Expert-Determined for de-identification. "
                "Researchers, companies, and hobbyists worldwide can download and use it for any purpose."
            ),
            "fit": (
                "**Mixed.** Patients reasonably expected their X-rays to be used for their care and possibly "
                "for institutional research. They probably did not specifically envision the X-rays being "
                "distributed to global ML research communities. The de-identification is technically rigorous "
                "(Expert-Determined), but the loss of control over downstream use is qualitatively different "
                "from a one-off research project."
            ),
            "public_vs_commercial": (
                "**Both.** Academic researchers benefit (free public dataset advances the field). Commercial "
                "entities that download and train models on the data also benefit. The dataset enables an "
                "uncountable number of derivative works. Some will be public good; some will be private "
                "products."
            ),
            "equity": (
                "**Substantial concerns.** Public benchmark datasets enable algorithm development globally. "
                "If the X-rays come from one institution's predominantly white patient population, then "
                "every model trained on them inherits that bias and may be deployed against populations the "
                "dataset doesn't represent. This is the canonical equity concern with public benchmark "
                "releases, and the literature documents it well."
            ),
            "transparency": (
                "**High at the dataset level.** The release is public; the methods are typically documented. "
                "Individual patients are not notified, but the institution's release is itself a transparent "
                "act."
            ),
            "reversibility": (
                "**Zero.** Once a public dataset is released, it cannot be recalled. Copies circulate "
                "permanently. No individual withdrawal is possible. This is the most irreversible archetype "
                "in the menu."
            ),
            "verdict": (
                "**Overall: medium-high risk, with the zero-reversibility as the dominant factor.** Public "
                "benchmark releases are valuable for the research community and have produced enormous progress. "
                "They also bake in the dataset's biases into every downstream model in perpetuity. The "
                "improvements: rigorous documentation of the dataset's population (datasheet), explicit "
                "limitations on appropriate use, ongoing community-level reporting on derivative models, and "
                "ideally a release governance committee that has assessed the equity implications before release."
            ),
        },
        "6.": {
            "description": (
                "**The setup.** A biobank holds blood samples from a 1990s cardiovascular cohort study. The "
                "original consent was specific to cardiovascular research. A new investigator wants to use "
                "the samples for population genetics work studying migration patterns and ancestry. The IRB "
                "is asked to approve the new use as covered by the original consent's general 'future related "
                "research' language. Some of the donors have died; many have moved; re-consent is not practicable."
            ),
            "fit": (
                "**Low fit.** This is approximately the Havasupai fact pattern. The original consent was "
                "specific. The proposed use is different in kind, not just in detail. Even if the consent's "
                "'future related research' language is read broadly, population genetics work has a different "
                "purpose, a different community of researchers, and potentially different cultural implications "
                "than the cardiovascular research the donors agreed to."
            ),
            "public_vs_commercial": (
                "**Public.** The work is academic. But the framing matters less than the consent question here."
            ),
            "equity": (
                "**Substantial concerns.** Population genetics work on specific populations has produced "
                "findings that some communities have found offensive or contradictory to important cultural "
                "narratives. The original consent didn't anticipate this category of research; the donor "
                "communities haven't been consulted about whether they want it conducted on their samples."
            ),
            "transparency": (
                "**The IRB process is the transparency mechanism.** But the IRB is being asked to decide "
                "on behalf of the donors; some of those donors may have specific objections to this kind of "
                "research that they didn't articulate at the original consent. Consultation with the donor "
                "communities (not just the donors as individuals) is the missing transparency layer."
            ),
            "reversibility": (
                "**Low.** Once the samples are used and results are published, the analysis cannot be "
                "unpublished. Re-consent for withdrawal is the standard mechanism, and it is not practicable here."
            ),
            "verdict": (
                "**Overall: high risk.** This is the Havasupai scenario in everything but the specifics. "
                "The improvements: community-level consultation (not just individual re-consent), explicit "
                "scope limitation in the original consent language for future collections (so this question "
                "doesn't arise in 20 years for the current cohort), and IRB practice that doesn't treat broad "
                "consent language as a blank check. The ASU settlement, 20 years on, suggests that 'IRB "
                "approved it' is not the end of the conversation."
            ),
        },
    }
    return (scenario_details,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Score your assessment, then reveal

        For each dimension, score the scenario before clicking through. The reveal will tell you whether your read matches the worked analysis; either way, the dimensions are what matter, not the score.
        """
    )
    return


@app.cell
def _(mo):
    score_fit = mo.ui.radio(
        options=["High", "Medium", "Low"],
        label="Consent-expectation fit",
        value="Medium",
    )
    score_public = mo.ui.radio(
        options=["Public", "Mixed", "Commercial"],
        label="Public vs commercial benefit",
        value="Mixed",
    )
    score_equity = mo.ui.radio(
        options=["Aligned", "Mixed", "Concerning"],
        label="Equity",
        value="Mixed",
    )
    score_transparency = mo.ui.radio(
        options=["High", "Adequate", "Inadequate"],
        label="Transparency",
        value="Adequate",
    )
    score_reversibility = mo.ui.radio(
        options=["High", "Medium", "Low"],
        label="Reversibility (can the patient withdraw?)",
        value="Medium",
    )
    show_reveal = mo.ui.checkbox(
        label="Show the worked analysis",
        value=False,
    )

    mo.vstack(
        [
            score_fit,
            score_public,
            score_equity,
            score_transparency,
            score_reversibility,
            show_reveal,
        ]
    )
    return (
        score_equity,
        score_fit,
        score_public,
        score_reversibility,
        score_transparency,
        show_reveal,
    )


@app.cell
def _(mo, scenario_details, scenario_pick, show_reveal):
    key = scenario_pick.value[:2]
    s = scenario_details[key]

    if not show_reveal.value:
        analysis_view = mo.vstack(
            [
                mo.md("**Scenario details:**\n\n" + s["description"]),
                mo.callout(
                    mo.md(
                        "_Score the dimensions above, then toggle 'Show the worked analysis' to compare with the reveal._"
                    ),
                    kind="neutral",
                ),
            ]
        )
    else:
        analysis_view = mo.vstack(
            [
                mo.md("**Scenario details:**\n\n" + s["description"]),
                mo.md("---"),
                mo.md("### Worked analysis"),
                mo.md("**1. Consent-expectation fit.** " + s["fit"]),
                mo.md("**2. Public vs commercial benefit.** " + s["public_vs_commercial"]),
                mo.md("**3. Equity.** " + s["equity"]),
                mo.md("**4. Transparency.** " + s["transparency"]),
                mo.md("**5. Reversibility.** " + s["reversibility"]),
                mo.md("---"),
                mo.callout(mo.md(s["verdict"]), kind="info"),
            ]
        )
    analysis_view
    return (analysis_view,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 7. What this leaves you

        Five things in place:

        1. **The primary/secondary distinction.** Care is primary; everything else is secondary. "Everything else" is most of modern clinical informatics.
        2. **Three case studies you should be able to summarize.** Henrietta Lacks (governance for legacy datasets), Havasupai (consent is not a blank check), Project Nightingale (HIPAA-compliant is not the same as trust-preserving).
        3. **Consent vocabulary.** Specific consent, broad consent, IRB waiver. The waiver is the operational default for retrospective EHR research; it is a defensible trade only when it is honest.
        4. **The five-dimension framework.** Consent-expectation fit, public vs commercial benefit, equity, transparency, reversibility. Apply it to every proposed secondary use.
        5. **The destination matters.** Internal QI, academic publication, pharma deal, vendor partnership, public benchmark, and model deployment are different ethical questions even with the same de-identified data underneath.

        Track 04 picks up algorithmic fairness, where the equity dimension of this framework becomes the dominant one and where most of the contested AI use cases live. Track 05 closes with governance: who is actually in the room when these decisions get made, and what the clinician's role is.
        """
    )
    return


if __name__ == "__main__":
    app.run()
