"""Track 05: Governance structures.

Decisions get made somewhere. This notebook walks the map of governance
bodies (IRB, privacy, compliance, data governance, AI/ML governance,
vendor management, clinical informatics steering, security, legal), the
question of decision rights, the clinician's seat at the table, the
contract layer where most of the actual policy lives, patient and
community representation, two case studies (Project Nightingale as a
governance failure, Duke Sepsis Watch as a model case), and a project
router that lists which governance bodies should weigh in on a proposed
clinical-data project.
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
        # Track 05: Governance structures

        ## Decisions get made somewhere

        Tracks 01 through 04 of this course built the analytic frameworks. The threat model says what we are defending against. The legal framework says what the floor is. The ethical framework says what the floor is missing. The equity framework says what bias looks like and how it gets baked in.

        None of those frameworks deploys itself. Some person, at some committee, on some Wednesday afternoon, approves the IRB protocol, signs the DUA, accepts the vendor contract, and certifies the deployment plan. **That committee is the unit of governance.** This track is about how the committees actually work, who sits on them, and where the clinician's voice belongs.

        Five pieces:

        1. **The map of governance bodies.**
        2. **Decision rights**: who gets to say yes or no, on what dimension.
        3. **The clinician's role**: which seat to ask for, what to bring.
        4. **Vendor contracts**: where most of the actual policy lives.
        5. **Patient and community representation**: who speaks for the patients.

        Then two case studies (Project Nightingale and Duke Sepsis Watch) and a project router.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1. The map of governance bodies

        A modern academic medical center has many committees that touch clinical-data projects. The relevant ones, in roughly the order a project might encounter them:

        | Body | Decides | Who sits |
        |---|---|---|
        | **IRB** | Whether activity is research; whether informed consent can be waived; whether privacy safeguards are adequate; whether vulnerable populations are protected | Faculty researchers, clinicians, ethicists, biostatisticians, community/unaffiliated members, legal counsel |
        | **Privacy office** | Whether a use of PHI is HIPAA-compliant; whether de-identification is adequate; what DUAs and BAAs are required | Privacy officer, privacy analysts, legal counsel |
        | **Compliance** | Whether the institution meets regulatory obligations across privacy, security, billing, fraud, anti-kickback, research integrity | Chief compliance officer, compliance analysts, legal counsel |
        | **Data governance committee** | Who can access institutional data, for what purposes; data stewardship; what extracts can leave the institution | Chief Data Officer, data stewards per source system, informatics leadership, compliance |
        | **AI/ML governance committee** | Whether a proposed AI/ML tool can be developed, validated, or deployed; whether vendor AI partnerships are acceptable; post-deployment monitoring | Clinical informatics lead, data scientists, clinician (often CMIO), compliance/legal, sometimes patient representatives |
        | **Vendor management / procurement** | Whether contracts can be signed; what terms required; vendor security and privacy posture | Procurement, contract attorneys, IT security, privacy |
        | **Clinical informatics steering** | EHR changes; CDS approval; tool integration with clinical workflows | CMIO, CNIO, informatics directors, specialty leads, IT operations |
        | **Security / CISO office** | Whether a system meets security requirements; encryption, logging, monitoring; vendor security posture | CISO, security engineers, infrastructure architects |
        | **Legal / OGC** | Contract enforceability; institutional exposure; alignment with applicable law | Attorneys |

        Most clinical-data projects need approval from several of these, not just one. The next section is about why that turns out to be harder than it sounds.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2. Decision rights: where the dirty secret lives

        In principle, the committees above have clearly delineated authority. In practice, **the boundaries are blurry**, and the same project often touches several committees with no single owner.

        Worked example: a proposed pilot of a vendor AI tool for predicting inpatient deterioration.

        | Question | Which committee owns it? |
        |---|---|
        | Is it research? | IRB (if yes); ambiguous if framed as QI or operations |
        | Does it touch PHI? | Privacy office |
        | Does it require a contract? | Vendor management + legal |
        | Does it integrate with the EHR? | Clinical informatics steering |
        | Is it an AI tool? | AI/ML governance |
        | Does it affect clinical workflow? | CMIO and departmental leadership |
        | Are there equity considerations? | **(often nobody)** |

        The last row is the most telling. **In most institutions, "the equity review" doesn't have an obvious home.** It may live in the AI governance committee if there is one; it may live nowhere if there isn't. The same is true for the *ethical* review beyond what HIPAA and the IRB cover.

        The dirty secret of clinical-data governance is that **some questions have no clear owner**, and projects either stall (because no one steps up) or proceed (because no one stops them). Both failure modes are common.

        The fix: **explicitly name the decision rights** before the project starts. Who decides what, on what timeline, with what backstop. A one-page decision matrix circulated to all involved committees is a small investment that prevents most of the downstream chaos.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3. The clinician's role

        Most of the committees on the map are not staffed by working clinicians. The IRB and the AI governance committee usually have one or two; the privacy office, compliance, vendor management, legal, and security usually do not.

        This matters for two reasons:

        - **Clinical context is hard to get right without clinicians.** "Does this tool fit the workflow?" "Does this label measure what it claims to measure?" "Does this alert make clinical sense?" These questions need working knowledge of the workflow that the committee may not have.
        - **The downstream consequences of governance decisions land on clinicians.** When a tool is deployed and alerts inappropriately, the clinician deals with the alert fatigue. When a vendor contract limits future flexibility, the clinician deals with the limitation. When an equity issue isn't caught at deployment, the clinician sees the disparate impact in their patients.

        The practical move: **ask for a seat**, on whichever committee touches the work you care about. Most institutions are receptive; clinicians who volunteer for governance committees are often welcomed because the committees know they need clinical input.

        ### What to bring to the seat

        1. **Workflow reality.** What the day actually looks like for the clinicians the tool will affect.
        2. **Outcome literacy.** What the outcome metric the tool optimizes actually means, and whether it captures what matters. (Track 04's label-bias frame.)
        3. **Subgroup awareness.** Which patients the tool might fail on, and whether anyone has checked.
        4. **Communication clarity.** Plain-English translation of clinical questions for non-clinical committee members.
        5. **Skepticism without obstruction.** The committee needs critical input, not a veto. The best clinical representatives say "yes, with these conditions" more often than "no."
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 4. Vendor contracts: where the actual policy lives

        A vendor contract for a clinical AI tool runs 60-200 pages. Most committee members have not read it. The contract is the actual policy that will govern the deployment.

        Terms that matter clinically:

        | Term | Why it matters |
        |---|---|
        | **Data ownership** | Who owns the records, derived models, labeled data, metadata about clinical use? |
        | **Data use limitations** | Can the vendor use this institution's data to improve products sold to other customers? |
        | **Model update notification** | If the model is silently updated, does the institution learn about it? Validate against the new version? |
        | **Performance monitoring obligations** | Who monitors post-deployment? What's the reporting cadence? What triggers a review? |
        | **Subgroup performance reporting** | Is the vendor obligated to report stratified performance? At what cadence? |
        | **Termination and offboarding** | If the institution terminates, does the vendor delete the data? Retain extracts? Keep derived models? |
        | **Liability and indemnification** | Who is liable for a clinical mis-prediction that causes harm? |
        | **Auditing rights** | Can the institution audit the vendor's data handling? On what notice? |
        | **Subcontractor flow-down** | Do the vendor's subcontractors follow these terms? |

        The clinician on the governance committee doesn't need to be a contract lawyer. The clinician needs to ask, on each of these, "what does our contract say, and is that what we want it to say?" **Silence is the default, and the default favors the vendor.**
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 5. Patient and community representation

        Who speaks for the patients?

        - **Unaffiliated IRB members.** Required by the Common Rule, one per IRB. Often a single voice across many protocols.
        - **Patient and Family Advisory Councils (PFACs).** Common; often consulted on workflow and experience, less often on data and AI.
        - **Community advisory boards.** Common in research networks serving specific communities. The Havasupai case (Track 03) is an example of what they prevent when they work, and what happens when they're bypassed.
        - **Patient representatives on AI governance.** Increasing but still uncommon. Institutions that have done this report it changes the conversation substantively.

        The right question isn't "is there a patient on the committee" (often yes, in some form). The right question is "**does that voice have actual influence on the decision?**" Tokens are common; influence is rarer.

        Institutions doing this best treat patient representation as a real governance role: paid, prepared, briefed in advance, given voting rights, supported with appropriate background materials. Institutions doing it worst treat patient representation as a symbolic checkbox. The difference is visible in retrospect.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 6. Two case studies

        ### Project Nightingale (Google + Ascension, 2019): governance failure

        Track 03 covered the ethics; the governance failure is specific.

        - The partnership was **contractually** compliant (BAA in place; HIPAA-permitted).
        - The partnership was **institutionally** compliant (signed by the relevant authorities).
        - The partnership was **not socially disclosed**. Patients weren't told; clinicians weren't told; the public wasn't told.
        - The discovery was via Wall Street Journal investigation, not via the institution's own transparency processes.

        The failure is that **no committee was responsible for asking "should this be disclosed?"** The legal and contracting committees said yes to the contract. Nobody owned the disclosure decision. Nobody noticed that the BAA framework was being used at a scale and intimacy the BAA was not designed for. The committee structure existed; the decision rights for the *novel* dimension of the partnership did not.

        **Lesson.** Governance committees can be individually competent and collectively miss the point. When a project is **new in kind** (the first vendor partnership at this scale; the first model deployment of this type), the standing committees may not have anyone whose job it is to think about the novelty. The fix is to elevate "is anything new about this?" as a governance question, and to require an answer.

        ### Duke Sepsis Watch: governance done well

        Sendak, Gao, Brajer, Balu, et al. published a series of papers (2017-2020) on the development and deployment of Sepsis Watch, an AI-based deterioration prediction tool deployed in production at Duke. What made it a model case:

        - **Multi-stakeholder development.** Clinicians, data scientists, and operations people worked jointly from the start. Clinical leadership wasn't consulted after the fact.
        - **Integration governance.** The tool integrated into the existing rapid-response workflow, not as a parallel alerting system. The committee responsible for rapid-response workflow had authority over the integration.
        - **Post-deployment monitoring.** Continuous monitoring with regular reports back to clinical and administrative leadership. Disparate-impact analyses by race and other subgroups were part of the monitoring plan.
        - **Documented decisions.** Deployment plan, validation results, monitoring plan, and modification history are documented in published work.
        - **Tied to organizational quality goals.** The tool was operationally accountable to a sepsis mortality reduction target.

        **Lesson.** Governance is something you can do well or badly, and the differences are visible in retrospect. Duke chose to do it well, and the tool has held up.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 7. Project router

        Describe a proposed clinical-data project. The router produces a list of governance bodies that should weigh in, a representative question from each, and a flag for where the missing decision rights probably are.
        """
    )
    return


@app.cell
def _(mo):
    p_research = mo.ui.checkbox(
        label="The project is research (defined question, intended for publication or regulatory submission)",
        value=True,
    )
    p_phi = mo.ui.checkbox(
        label="The project touches PHI (held by a covered entity or business associate)",
        value=True,
    )
    p_contract = mo.ui.checkbox(
        label="The project requires a contract with an external vendor or partner",
        value=False,
    )
    p_ehr = mo.ui.checkbox(
        label="The project integrates with the EHR or affects clinical workflow",
        value=False,
    )
    p_ai = mo.ui.checkbox(
        label="The project develops, validates, or deploys an AI/ML model or CDS tool",
        value=False,
    )
    p_subgroups = mo.ui.checkbox(
        label="The project may have differential effects across patient subgroups (race, sex, age, insurance, language)",
        value=True,
    )
    p_commercial = mo.ui.checkbox(
        label="The project has a commercial dimension (data licensing, vendor partnership, deployed product)",
        value=False,
    )
    p_novel = mo.ui.checkbox(
        label="The project is new-in-kind for this institution (first of its scale, type, or partnership structure)",
        value=False,
    )

    mo.vstack(
        [
            p_research,
            p_phi,
            p_contract,
            p_ehr,
            p_ai,
            p_subgroups,
            p_commercial,
            p_novel,
        ]
    )
    return p_ai, p_commercial, p_contract, p_ehr, p_novel, p_phi, p_research, p_subgroups


@app.cell
def _(
    mo,
    p_ai,
    p_commercial,
    p_contract,
    p_ehr,
    p_novel,
    p_phi,
    p_research,
    p_subgroups,
):
    bodies = []

    if p_research.value:
        bodies.append(
            (
                "**IRB**",
                "Is this exempt, expedited, or full-board review? Can individual authorization be waived? "
                "Are privacy safeguards adequate? Are vulnerable populations protected? "
                "What's the post-research data retention plan?",
            )
        )

    if p_phi.value:
        bodies.append(
            (
                "**Privacy office**",
                "Is the use of PHI HIPAA-compliant? Is de-identification adequate (Safe Harbor, Expert Determination, or LDS with DUA)? "
                "Are state laws also applicable (CCPA, MHMDA, BIPA, GDPR)? "
                "What audit trails are required?",
            )
        )

    if p_phi.value or p_contract.value:
        bodies.append(
            (
                "**Compliance**",
                "Does this meet institutional policy and external regulation? "
                "Are billing, anti-kickback, and Stark implications addressed? "
                "Is the documentation defensible to an external audit?",
            )
        )

    bodies.append(
        (
            "**Data governance committee**",
            "Who is permitted to access the data, for what purposes? "
            "Are data stewards from each source system consulted? "
            "What's the data quality validation plan?",
        )
    )

    if p_ai.value:
        bodies.append(
            (
                "**AI/ML governance committee**",
                "Has subgroup-stratified performance been reported? Is the label a good proxy for the construct? "
                "What's the post-deployment monitoring plan? Who is accountable when the model degrades? "
                "What's the model update notification policy?",
            )
        )

    if p_contract.value:
        bodies.append(
            (
                "**Vendor management + legal**",
                "What does the contract say about data ownership, use limitations, model update notification, "
                "performance monitoring, termination and offboarding, liability, and audit rights? "
                "Is the BAA in place? Are subcontractors flow-down covered?",
            )
        )

    if p_ehr.value:
        bodies.append(
            (
                "**Clinical informatics steering (CMIO)**",
                "Does this integrate cleanly with the existing workflow? Will it produce alert fatigue? "
                "How will end users be communicated to? Is the change reversible if it doesn't work?",
            )
        )

    if p_phi.value or p_contract.value:
        bodies.append(
            (
                "**Security / CISO**",
                "Are data flows encrypted, logged, and monitored? Does the vendor's security posture meet "
                "institutional standards? What's the breach response plan? What auditing access does the institution have?",
            )
        )

    if p_contract.value or p_commercial.value:
        bodies.append(
            (
                "**Legal / OGC**",
                "Is the contract enforceable and aligned with institutional risk tolerance? "
                "Are there state-law issues that affect the structure of the agreement? "
                "What's the institution's exposure?",
            )
        )

    bodies_table = mo.md(
        "### Governance bodies that should weigh in\n\n"
        + "\n\n".join([f"- {b[0]}: {b[1]}" for b in bodies])
    )

    # Identify the likely gaps
    gaps = []
    if p_subgroups.value and not p_ai.value:
        gaps.append(
            "**Equity review has no clear owner.** The project may have differential effects by subgroup, "
            "but there's no AI governance committee to receive that review. Where will the subgroup analysis "
            "land? Who is responsible for monitoring disparate impact post-implementation?"
        )
    if p_subgroups.value and p_ai.value:
        gaps.append(
            "**Equity review needs explicit ownership inside AI/ML governance.** Most institutional AI committees "
            "are weak on subgroup-stratified performance reporting and post-deployment monitoring of disparate impact. "
            "Explicitly name who runs the subgroup analyses, on what cadence, with what triggers for action."
        )
    if p_commercial.value:
        gaps.append(
            "**Patient/community disclosure has no clear owner.** Commercial dimensions (data licensing, vendor "
            "partnerships, deployed products) often skip the patient-disclosure question entirely. The Project "
            "Nightingale failure mode lives here. Who is responsible for disclosing the project to the patient "
            "population whose data is involved?"
        )
    if p_novel.value:
        gaps.append(
            "**Novelty review has no clear owner.** New-in-kind projects are where standing committees miss the point, "
            "because the standing committees were built for the previous kind of project. Explicitly elevate the "
            "question 'is anything new about this, and which committee owns the new dimension?' Often the answer is "
            "a temporary cross-functional working group with a written charter and a sunset date."
        )
    if p_ai.value and not p_ehr.value:
        gaps.append(
            "**Deployment context review has no clear owner.** A standalone AI tool deployed outside the EHR may "
            "bypass clinical informatics steering entirely. Without that, alert fatigue, workflow disruption, and "
            "communication-to-users questions go unowned. Who owns these for a non-EHR deployment?"
        )

    if gaps:
        gaps_md = mo.callout(
            mo.md("### Likely governance gaps\n\n" + "\n\n".join(gaps)),
            kind="warn",
        )
    else:
        gaps_md = mo.callout(
            mo.md(
                "**No immediate gaps surfaced from the dimensions described.** That doesn't mean none exist; "
                "it means the obvious ones aren't lit up. Worth running the project past each named committee "
                "and asking 'what question do you wish someone else had asked here?'"
            ),
            kind="info",
        )

    closing = mo.callout(
        mo.md(
            "**The output above is the agenda for the first conversation, not the decision.** Use it to map "
            "your project against the committees that need to weigh in, identify likely gaps, and structure "
            "the routing. The decision still belongs to the committees; this is the rehearsal that helps you "
            "show up prepared."
        ),
        kind="info",
    )

    mo.vstack([bodies_table, gaps_md, closing])
    return bodies, bodies_table, closing, gaps, gaps_md


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 8. The five governance questions to ask

        A practical checklist:

        1. **Who decides yes/no?** Name the committee or individual whose approval is required. If you can't name them, that's the first gap.
        2. **What's the decision being made?** Approval to start, approval to deploy, approval to renew, approval to expand. Each is a different decision; conflating them is how projects accumulate scope without anyone signing off on the new scope.
        3. **Who is in the room?** Clinicians? Patient representatives? Compliance? IT? The committee composition is the prediction of which questions will get asked and which will get missed.
        4. **What's in the contract?** Read the contract terms that matter clinically (Section 4). Ask "is that what we want?" on each.
        5. **What's the post-implementation review plan?** Who monitors, on what cadence, with what trigger for re-review? A deployed system without ongoing oversight is a system that will drift.

        ## 9. What this leaves you

        Five things in place:

        1. **The map.** IRB, privacy, compliance, data governance, AI/ML governance, vendor management, clinical informatics, security, legal. Each owns a slice of any project.
        2. **The dirty secret.** Decision rights are blurry, equity reviews often have no owner, and projects either stall or proceed depending on who pays attention.
        3. **The clinician's role.** Ask for a seat. Bring workflow reality, outcome literacy, subgroup awareness, communication clarity, and skepticism-without-obstruction.
        4. **The contract layer.** Most of the actual policy lives in the BAA, the MSA, the DUA, the SLA. The committee approves the policy; the contract IS the policy. Read the contracts.
        5. **Patient representation.** Tokens vs influence. The institutions doing this best pay, prepare, brief, and give voting rights.

        The course capstone takes a proposed research project and walks it through the full framework: privacy threat model (Track 01), legal review (Track 02), ethical analysis (Track 03), equity review (Track 04), and governance routing (this track). The Socratic format is the standard for question-based capstones in this curriculum: commit-then-reveal, with the work being the commitment, not the reveal.
        """
    )
    return


if __name__ == "__main__":
    app.run()
