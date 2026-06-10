"""Track 03: Change management.

The RA-CDS build is on schedule; a warning from a peer institution
(47% of their rheumatologists dismiss a similar alert every time it
fires) frames the question. The notebook presents why technical-only
deployments fail, Lewin's three phases, Kotter's 8 steps applied to
the RA-CDS rollout, ADKAR at the individual level, the four pillars
of sustainable change, resistance-as-information, and the Sepsis
Watch case study, then runs a five-dimension change-readiness
assessment and closes with the change-management plan the Course 16
capstone collects.

WASM-safe: marimo-only imports, no data files, no network calls.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    READINESS_GUIDANCE = {
        "Clinical champion buy-in": (
            "Raising this score means a named champion rather than agreement "
            "in principle: the rheumatology chief presents the alert at the "
            "department meeting, a respected skeptic is recruited onto the "
            "coalition, and the champion's name is on the rollout "
            "communication instead of yours."
        ),
        "Training plan completeness": (
            "Raising this score means case-based sessions on realistic cards "
            "(what the 0.30 probability threshold means, what the suggested "
            "action does, when dismissing is correct), at-the-elbow support "
            "scheduled for the soft-launch weeks, and a one-page reference "
            "inside the workflow. An emailed PDF scores a 1."
        ),
        "Workflow fit": (
            "Raising this score means shadowing rheumatologists at chart "
            "open, confirming the escalation conversation can be scheduled "
            "in two clicks from the card, and verifying the card does not "
            "stack with the other chart-open alerts. Workflow fit is "
            "established by observation in the clinic, at the elbow."
        ),
        "Sustainment plan": (
            "Raising this score means a named post-go-live owner, a monthly "
            "override-rate review on a control chart (Track 04), a "
            "low-friction feedback channel for clinicians, and a retuning "
            "path that runs through the AI Governance Committee. A "
            "sustainment plan that consists of \"IT will monitor it\" "
            "scores a 2."
        ),
        "Equity considerations": (
            "Raising this score means checking alert rates and model "
            "performance across language, race and ethnicity, and payer "
            "before launch, confirming the soft-launch clinics do not "
            "exclude the panels with the highest disease burden, and adding "
            "subgroup views to the monitoring plan. Course 03 and Course 09 "
            "supply the audit frame."
        ),
    }
    return READINESS_GUIDANCE, mo


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 03: Change management

        The build is on schedule. The CDS Hooks service passed integration testing, the card renders correctly in the EHR test environment, and the Track 02 timeline is holding. Then a colleague at another health system, one year into a similar flare-risk deployment, sends a warning: 47% of their rheumatologists hit dismiss every time the CDS fires. The model was validated and the build was clean; the deployment failed anyway. This track covers why that happens and what prevents it: change management, the discipline of moving an organization, and the individuals inside it, from current behavior to new behavior deliberately.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            **The running scenario.** In the Course 12 capstone you produced the design brief for an RA flare-risk alert: at chart open (the `patient-view` CDS Hook), for patients with active rheumatoid arthritis, when the recent CRP trajectory and clinical context put the probability of a flare in the next 90 days above the 0.30 firing threshold, a card suggests scheduling a treatment-escalation conversation rather than waiting for the next routine visit. The AI Governance Committee approved the brief, and the CMIO assigned you the implementation with go-live six months out. The deployment runs at Helios Academic Medical Center, whose rheumatology panel holds 1,247 patients with RA. Ms. Reyes is in the cohort: her CRP run-up to 36.2 mg/L before adalimumab started is exactly the trajectory the alert exists to catch.
            """
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Why technical-only deployments fail

        A CDS alert is software embedded in a social system: clinicians with habits and status hierarchies, clinic schedules with no slack, and a department culture with opinions about being told what to do by a model. Sociotechnical systems theory states the consequence plainly: the unit that succeeds or fails is the combined social and technical system, never the technical artifact alone. A deployment plan that engineers the artifact and leaves the social half to chance has planned roughly half the deployment.

        The colleague's 47% dismiss rate is the standard signature of this failure mode. Nothing in their system was broken. The alert computed a defensible probability and rendered a well-designed card; the rheumatologists, who had been given no reason to trust the model, no workflow that absorbed the card, and no colleague who vouched for either, dismissed it as a matter of routine. Course 12 Track 1 established the base rates: published override rates for interruptive CDS run 49 to 96 percent, and a technically sound alert falls in that range by default unless the deployment does deliberate work to escape it.

        This track treats sociotechnical theory at concept level only. Course 17 Track 6 treats it at depth, including the Sittig and Singh eight-dimension model.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Three frameworks, three altitudes

        Change management has produced dozens of named frameworks. Three cover the working informaticist's needs, and they operate at different altitudes.

        **Lewin's unfreeze, change, refreeze** is the oldest and names the shape every deliberate change shares. *Unfreeze*: destabilize the current equilibrium, because people who consider the status quo tenable will not move. *Change*: transition to the new behavior, with support, while performance temporarily dips. *Refreeze*: stabilize the new behavior so the system does not relax back to the old equilibrium. The model's age shows (modern clinical systems rarely refreeze; the next change arrives first), but the three-phase shape survives inside every later framework: Kotter's steps 1 to 4 are an elaborated unfreeze, steps 5 to 7 are the change, and step 8 is the refreeze.

        **Kotter's 8 steps** operate at the organization level: what the institution must do, in sequence. **ADKAR** operates at the individual level: what each rheumatologist must come to have, in sequence. The two complement each other. An organization can execute Kotter competently and still fail one clinician at a time, and ADKAR names where.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Kotter's 8 steps, applied to the RA-CDS

        The table applies each step to the rollout you are leading. The right-hand column is the track's working material: it returns at the end of the notebook as the change-management plan.

        | # | Step | What it requires | Applied to the RA-CDS |
        |---|---|---|---|
        | 1 | Establish urgency | A shared, evidence-grounded case that the status quo is failing | The treat-to-target gap: registry studies repeatedly find that a third to a half of RA patients with moderate or high disease activity leave the qualifying visit without treatment escalation. Ms. Reyes's CRP ran to 36.2 mg/L before adalimumab started. The alert exists because the escalation conversation routinely happens one visit too late. |
        | 2 | Build a guiding coalition | A small group with the authority, credibility, and skill to carry the change | The rheumatology chief (clinical authority), the EMR optimization lead (build authority), and one respected skeptic from the department. The skeptic matters most: colleagues who distrust the model will watch what the skeptic does. |
        | 3 | Form a strategic vision | A one-sentence picture of the changed state | "Flare risk is acted on at the visit where the data justify it, instead of being discovered at the next one." Every rollout decision should trace to that sentence. |
        | 4 | Communicate the vision | Repetition through channels the audience already attends | The chief presents at the department meeting; the card text restates the vision in its own words; the soft-launch users tell their own stories. The informaticist's broadcast email is the weakest channel available. |
        | 5 | Empower action, remove barriers | Make the new behavior cheaper than the old one | The card's suggested action (schedule the escalation conversation) executes in two clicks. If acting on the card takes six clicks and a phone call, the dismiss button wins on workload alone. |
        | 6 | Generate short-term wins | Visible, early, unambiguous evidence the change works | The month 5 soft launch with 5 rheumatologists: each accepted card that becomes an escalation visit is a countable win, reported to the department weekly. |
        | 7 | Sustain acceleration | Spend the credibility of early wins before declaring victory | Full launch at month 6 with the soft-launch users as peer references; training extended to the full department; the feedback channel kept open; measurement continued past go-live. |
        | 8 | Anchor in culture | The new behavior becomes how the department practices | Responding to the card becomes part of the standard visit workflow; incoming fellows learn it during onboarding; the override-rate review becomes a standing department-meeting item. |

        Two steps deserve emphasis. Step 2 is the one most often skipped in informatics deployments: the build team substitutes itself for the coalition, and the department experiences the alert as something IT did to them. Step 6 is the reason the Track 02 timeline holds a month 5 soft launch: five rheumatologists generate countable wins before the full department is asked to change.
        """
    )
    return


@app.cell
def _(mo):
    quiz1 = mo.ui.radio(
        options=[
            "Step 1: no sense of urgency was established.",
            "Step 2: no guiding coalition; no respected clinician carried the change.",
            "Step 6: no short-term wins were generated.",
            "Step 8: the new behavior was never anchored in the culture.",
        ],
        label=(
            "A peer institution deployed a technically flawless heart-failure "
            "medication-titration alert. The logic was validated, latency was "
            "excellent, and the kickoff email cited the titration-gap "
            "literature. Training was a PDF emailed to the department. No "
            "clinician was recruited to carry the change. At month 3 the "
            "override rate was 84% and the medical director asked for the "
            "alert to be retired. Which omission best explains the outcome?"
        ),
    )
    quiz1
    return (quiz1,)


@app.cell
def _(mo, quiz1):
    if quiz1.value is None:
        _resp = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif quiz1.value.startswith("Step 2"):
        _resp = mo.callout(
            mo.md(
                "**Correct.** Urgency was at least attempted (the kickoff "
                "email cited the literature), but no person with clinical "
                "credibility carried the change. With no coalition, every "
                "later step ran through the weakest available channel: the "
                "project team itself. The emailed PDF is a second, related "
                "failure; in ADKAR terms it delivers neither Knowledge (a "
                "PDF does not teach a workflow) nor Ability (nobody "
                "practiced under clinical conditions). Steps 6 and 8 were "
                "never reached: a deployment that fails at step 2 does not "
                "survive long enough for short-term wins or culture "
                "anchoring to matter."
            ),
            kind="success",
        )
    else:
        _resp = mo.callout(
            mo.md(
                "**Reconsider the sequence.** Steps 6 and 8 cannot be the "
                "load-bearing omission because the deployment never got far "
                "enough for either to apply, and urgency was attempted, "
                "however weakly, in the kickoff email. The omission that "
                "determined the outcome is step 2: no guiding coalition. "
                "Without a respected clinician carrying the change, the "
                "department experienced the alert as an external imposition, "
                "and the emailed-PDF training (an ADKAR Knowledge and "
                "Ability failure) had no credible voice behind it."
            ),
            kind="warn",
        )
    _resp
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## ADKAR: the individual level

        Organizations do not adopt alerts; individual rheumatologists do, one at a time. ADKAR (Prosci's framework: Awareness, Desire, Knowledge, Ability, Reinforcement) names the five things each individual must have, in order, before the new behavior is reliable. The order matters: training (Knowledge) delivered to a clinician with no Desire produces a clinician who can articulate precisely why they are dismissing the card.

        | Element | The individual's question | RA-CDS rollout action |
        |---|---|---|
        | **Awareness** | Why is this change happening? | The chief presents the treat-to-target gap and the Helios panel's own escalation numbers at the department meeting, before anyone sees a card. |
        | **Desire** | What is in it for me, and do I choose to participate? | Frame the card as recovered visit time: it surfaces the escalation case before the visit instead of mid-visit. The respected skeptic states, in their own words, why they joined the coalition. |
        | **Knowledge** | How do I do the new behavior? | Case-based training on realistic cards: what the 90-day flare probability means, what the suggested action does, and when dismissing is the correct response. |
        | **Ability** | Can I do it under clinical conditions? | At-the-elbow support during the month 5 soft launch; the two-click scheduling path verified in the live workflow, under a full session load. |
        | **Reinforcement** | What keeps the behavior from decaying? | Monthly override-rate feedback to the department, individual audit-and-feedback for outliers, and visible credit for escalations the alert caught. |

        The diagnostic use is the practical one. When a specific rheumatologist is not using the alert, locate the missing element rather than repeating the whole rollout at them. A clinician who never heard the case for the change has an Awareness gap; one who heard it and rejects it has a Desire gap; one who accepts it but fumbles the workflow has a Knowledge or Ability gap; one who used it for a month and stopped has a Reinforcement gap. Each gap has a different fix, and only one of those fixes is more training.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The four pillars of sustainable change

        Frameworks describe the campaign. The four pillars describe what must be true on the ground for the change to survive month 7, after the project team has moved on.

        | Pillar | What it covers | RA-CDS instance |
        |---|---|---|
        | **Workflow** | The new behavior physically fits the moment it occupies | The `patient-view` card arrives at chart open; the suggested action executes in two clicks; the card does not stack with the existing chart-open alert load. |
        | **Culture** | Department norms treat the new behavior as good practice | Chief endorsement, the skeptic's public reasoning, peer stories from the soft launch, and no tolerance for "the model is IT's problem" framing. |
        | **Training** | Users know the behavior and can perform it under load | Case-based sessions, at-the-elbow support in soft launch, a one-page reference inside the workflow. |
        | **Sustainment** | Someone owns the change after go-live | A named post-go-live owner, the monthly override review, a feedback channel, and a retuning path through the AI Governance Committee. |

        A deployment can be strong on three pillars and still decay. Training without sustainment produces a good first month and a slow relapse. Workflow fit without culture produces correct mechanics nobody believes in. The pillars are a conjunction: the weakest one sets the outcome, which is the logic the readiness assessment below operationalizes.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Resistance is information

        The 47% dismiss rate at the colleague's institution is a measurement, and the first obligation is to find out what it measures. An override aggregates at least four distinct signals, each with a different fix.

        | What the dismissal means | Problem class | The fix |
        |---|---|---|
        | "This patient is not flaring." | Model performance (false positive) | Threshold and model review, routed through the AI Governance Committee. |
        | "I already know this patient is flaring." | Timing and redundancy | Fire earlier in the trajectory, or suppress when escalation is already planned. |
        | "I agree, and the suggested action does not fit this visit." | Workflow | Redesign the card's action, leave the model alone. |
        | "I do not trust a model on this." | Trust | Coalition work, transparency about the validation, the skeptic's voice. |

        Retuning the threshold treats only the first row. Retuning in response to the other three makes the alert quieter without making it better, and it discards the most useful data the deployment produces. The operational rule: investigate before retuning. Structured override-reason capture on the card (one click, four reasons) plus five short interviews during soft launch will classify the signal at almost no cost.

        Course 12 Track 1 covers the alert-fatigue evidence underneath this rule. Track 04 of this course adds the measurement discipline: the override rate belongs on a control chart, where a real shift can be distinguished from week-to-week noise.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Sepsis Watch case: documented twice

        The Sepsis Watch deployment at Duke University Hospital is the best-documented change-management case in clinical AI, because it was documented twice by different disciplines.

        **Sendak et al. (JMIR Medical Informatics, 2020)** is the implementation paper: what was built. A deep learning model scored every emergency department patient for sepsis risk every five minutes. The design choice that mattered most was organizational: the scores surfaced on a dashboard monitored by rapid response team (RRT) nurses, who called the ED physician when a patient crossed threshold, rather than as an interruptive alert in the physician's workflow. The paper documents the model, the threshold decisions, the workflow, and the governance review. Course 12 introduced it as a CDS-evaluation reference.

        **Elish and Watkins (Repairing Innovation, Data & Society, 2020)** is the ethnography of the same deployment: what it took to make it work. The system functioned because of labor the architecture diagrams do not show. The RRT nurses invented and refined the phone scripts that let a nurse tell an attending physician that a model was worried about a patient, across a professional status boundary, without triggering a conflict. They learned when to lead with the score and when never to mention the model at all. They absorbed, continuously, the friction of a workflow that crossed organizational lines. Elish and Watkins name this **repair work**: the ongoing, mostly invisible labor of integrating an innovation into a social system.

        Two lessons transfer directly to the RA-CDS. First, the deployment plan is a hypothesis about workflow, and the people inside the workflow finish the design; the plan should expect and welcome that, which is half the purpose of the month 5 soft launch. Second, integration labor is real work done by identifiable people. If the change-management plan does not name who does it, it will be extracted invisibly from whoever is nearest, and the deployment will depend on goodwill it never budgeted for.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The change-readiness assessment

        The instrument below is the track's interactive and a tool to reuse on real deployments. Five dimensions, each scored 1 (absent) to 5 (fully in place). The total runs 5 to 25 and maps to a launch recommendation: below 15, do not launch; 15 to 19, soft launch with monitoring; 20 to 25, ready to deploy.

        Score the RA-CDS rollout as it stands today: the technical build is on schedule, the rheumatology chief has agreed in principle to support the rollout, training is drafted but not scheduled, and nobody has been named to own the alert after go-live. The feedback names the weakest dimension and states what raising it would require.
        """
    )
    return


@app.cell
def _(mo):
    champion_slider = mo.ui.slider(
        1, 5, value=3, label="Clinical champion buy-in", show_value=True
    )
    training_slider = mo.ui.slider(
        1, 5, value=3, label="Training plan completeness", show_value=True
    )
    workflow_slider = mo.ui.slider(
        1, 5, value=3, label="Workflow fit", show_value=True
    )
    sustainment_slider = mo.ui.slider(
        1, 5, value=3, label="Sustainment plan", show_value=True
    )
    equity_slider = mo.ui.slider(
        1, 5, value=3, label="Equity considerations", show_value=True
    )
    mo.vstack(
        [
            champion_slider,
            training_slider,
            workflow_slider,
            sustainment_slider,
            equity_slider,
        ]
    )
    return (
        champion_slider,
        equity_slider,
        sustainment_slider,
        training_slider,
        workflow_slider,
    )


@app.cell
def _(
    READINESS_GUIDANCE,
    champion_slider,
    equity_slider,
    mo,
    sustainment_slider,
    training_slider,
    workflow_slider,
):
    _scores = {
        "Clinical champion buy-in": champion_slider.value,
        "Training plan completeness": training_slider.value,
        "Workflow fit": workflow_slider.value,
        "Sustainment plan": sustainment_slider.value,
        "Equity considerations": equity_slider.value,
    }
    _total = sum(_scores.values())

    if _total < 15:
        _verdict = "Do not launch."
        _kind = "danger"
        _band_note = (
            "A total below 15 means the social half of the deployment is "
            "not built. Launching now reproduces the colleague's 47% "
            "dismiss rate locally; the technical build being on schedule "
            "does not change that arithmetic."
        )
    elif _total <= 19:
        _verdict = "Soft launch with monitoring."
        _kind = "warn"
        _band_note = (
            "A total of 15 to 19 supports the month 5 soft launch with 5 "
            "rheumatologists, under explicit monitoring (override-reason "
            "capture, weekly review), with the weak dimensions raised "
            "before the month 6 full launch."
        )
    else:
        _verdict = "Ready to deploy."
        _kind = "success"
        _band_note = (
            "A total of 20 or above supports proceeding to full launch on "
            "the Track 02 timeline. Keep the monitoring anyway: a readiness "
            "score describes the start of the change, and Reinforcement is "
            "the element that decays."
        )

    _min_score = min(_scores.values())
    _weakest = [d for d, s in _scores.items() if s == _min_score]
    if _min_score == 5:
        _guidance = (
            "No weak dimension remains at this scoring. The residual risk "
            "is overconfidence: a 25 from the project team's own "
            "self-assessment deserves a second scoring by someone outside "
            "the team, ideally the respected skeptic."
        )
    else:
        _lines = "\n".join(
            f"- **{_d}** (scored {_min_score}). {READINESS_GUIDANCE[_d]}"
            for _d in _weakest
        )
        _label = (
            "Weakest dimensions" if len(_weakest) > 1 else "Weakest dimension"
        )
        _guidance = f"{_label}:\n\n{_lines}"

    _body = (
        f"**Readiness score: {_total} / 25. {_verdict}**\n\n"
        f"{_band_note}\n\n{_guidance}"
    )
    _out = mo.callout(mo.md(_body), kind=_kind)
    _out
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The artifact: the change-management plan

        Each track of this course produces one artifact for the Course 16 capstone, the implementation plan you will hand the CMIO. Track 03's artifact is the **change-management plan**: Kotter's 8 steps applied to the RA-CDS in the form the table above worked out, with the coalition named (the rheumatology chief, the EMR optimization lead, the respected skeptic), the vision sentence written, the month 5 soft-launch wins defined as countable events (accepted cards that become escalation visits, reported weekly), and the anchoring mechanism specified (the alert as part of the standard visit workflow, the override review as a standing department-meeting item). The readiness assessment travels with the plan: a launch recommendation with the weak dimensions named is the honest cover sheet for any change plan.

        The capstone collects this plan as section 4 of the implementation plan. Track 04 supplies what the plan's Reinforcement step consumes: the measurement system (run charts, control charts, and the KPI dashboard) that tells you whether the change held.
        """
    )
    return


if __name__ == "__main__":
    app.run()
