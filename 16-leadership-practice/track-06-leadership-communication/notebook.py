"""Track 06: Leadership and communication.

No visible code. The notebook covers the four leadership styles and the
situational case for switching among them, executive communication (BLUF,
the what / so what / now what structure, the one-page discipline),
interest-based negotiation, and the clinical informatics career path as
orientation. The load-bearing interactive is a 3-slide executive-pitch
builder for presenting the RA-CDS deployment to the Helios Board of
Trustees, with per-slide feedback and a reactive assembled deck.

WASM-safe: no shared imports, no data files, no relative paths.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    PITCH_ASKS = {
        "Approve the deployment of the RA flare-risk alert.": {
            "ok": False,
            "feedback": "**Wrong body.** The deployment is already approved: the AI Governance Committee approved the design brief and the CMIO chartered the implementation. Asking the board to re-approve an operational decision confuses governance layers (Track 1) and invites the board into decisions its committees already own. The first question from a well-run board is \"why are you bringing us this?\"",
            "slide": "**Slide 1: the ask.** Approve deployment of the RA flare-risk alert in rheumatology.\n\n- Alert suggests a treatment-escalation conversation at chart open\n- Go-live planned in six months",
        },
        "Approve $240K in capital for the build.": {
            "ok": False,
            "feedback": "**Already committed, and the wrong owner.** The one-time build cost of about $240K was committed through the IT Steering Committee's portfolio process when the project was chartered (Tracks 5 and 7). The board of a 720-bed academic medical center does not approve items at this scale, and re-asking signals that the presenter does not know which body owns which decision.",
            "slide": "**Slide 1: the ask.** Approve $240K in capital for the alert build.\n\n- Covers FTE time, CDS-service build, validation, and training delivery",
        },
        "Endorse the ongoing operating commitment of about $60K per year that keeps the alert running.": {
            "ok": True,
            "feedback": "**The right ask.** The recurring commitment is the decision that outlives the project, and it is the one executive bodies most often under-scrutinize: the build is visible, the run cost is permanent (Track 5 covers total cost of ownership). Asking the board to endorse the operating line matches its fiduciary role and protects the program when budget season arrives.",
            "slide": "**Slide 1: the ask.** Endorse the ongoing operating commitment for the RA flare-risk alert: about $60K per year for monitoring, retuning, and report maintenance after go-live.\n\n- One-time build of about $240K already committed through the IT portfolio process\n- Go-live in six months; rheumatology is the clinical owner",
        },
        "Informational only: no action requested.": {
            "ok": False,
            "feedback": "**A wasted slot.** An informational briefing is legitimate board business, but a 10-minute slot with no ask spends the scarcest resource in the room, board attention, without converting it into commitment. A real ask exists here: the ongoing operating commitment. Make it. If a briefing is genuinely informational, BLUF still applies: state in the first sentence the one thing the board should retain.",
            "slide": "**Slide 1: for information.** Status briefing on the RA flare-risk alert; no action requested.\n\n- Build on schedule; go-live in six months",
        },
    }

    PITCH_EVIDENCE = {
        "Model performance: the discrimination and calibration statistics from validation.": {
            "ok": False,
            "feedback": "**Fails the altitude rule.** Course 15 Track 1's rule: match the altitude to the audience. A board of trustees cannot act on a discrimination statistic; the AUC answers a question (can the model rank risk?) the board is not asking. The validation detail lives in the AI Governance record and earns one sentence if a trustee asks.",
            "slide": "**Slide 2: the evidence.** The flare-risk model discriminates well on retrospective validation, with acceptable calibration across risk strata.\n\n- Validation reviewed and approved by the AI Governance Committee",
        },
        "The financial case: the five-year NPV of the program under the approved budget.": {
            "ok": False,
            "feedback": "**Board-relevant, but the supporting line, not the headline.** A hospital board is a fiduciary for a mission as well as a balance sheet. An evidence slide that leads with NPV invites the board to weigh a clinical-quality intervention as a financial instrument, and a five-year NPV of about $195K is small enough to lose on those terms. Lead with the patient outcome; put the NPV underneath it.",
            "slide": "**Slide 2: the evidence.** The program returns a positive five-year NPV under the approved budget.\n\n- Build $240K; run cost $60K per year; break-even near month 31\n- Five-year NPV about $195K at a 3% discount rate",
        },
        "Patient impact: about 31 fewer flares per year across the 1,247-patient RA panel, and what a flare costs.": {
            "ok": True,
            "feedback": "**The right headline.** Flares averted is the outcome the program exists to produce, it is concrete at board altitude, and it carries both frames the board governs on: mission (patients spared a flare) and margin ($4K to $6K of added utilization per flare). One patient sentence, a CRP run-up like Ms. Reyes's caught at chart open, makes it specific without a single statistic the board cannot use. The NPV belongs on this slide as the supporting line.",
            "slide": "**Slide 2: the evidence.** About 31 moderate-to-severe flares averted per year across Helios's 1,247-patient RA panel.\n\n- A flare costs the patient weeks of uncontrolled disease activity and the system $4K to $6K in added utilization\n- A CRP run-up like Ms. Reyes's (36.2 mg/L before adalimumab started) is now caught at chart open, months before the next routine visit\n- Annual benefit about $155K against $60K operating; five-year NPV about $195K",
        },
        "Adoption: the expected alert override rate against peer benchmarks.": {
            "ok": False,
            "feedback": "**A process metric in an outcome slot.** The override rate tells you whether clinicians act on the alert, not whether patients are better off (Track 4 draws the process-vs-outcome line). On a board slide it reads as internal plumbing. It belongs on the CMO's monthly dashboard and in the risk slide's mitigation line, not as the evidence headline.",
            "slide": "**Slide 2: the evidence.** We project an override rate near 60%, in line with peer benchmarks for well-tuned CDS.\n\n- Override rate tracked monthly on the CMO dashboard",
        },
    }

    PITCH_RISKS = {
        "No material risks: the model is validated and the AI Governance Committee approved it.": {
            "ok": False,
            "feedback": "**Destroys credibility.** Every trustee in the room has watched an IT project fail. A no-risk slide signals either naivety or concealment, and it converts the rest of the pitch into testimony to be cross-examined. Validation and governance approval reduce risk; they do not eliminate adoption risk, model drift, or operational failure.",
            "slide": "**Slide 3: the risk.** No material risks anticipated: the model is validated and governance approval is complete.",
        },
        "The one material risk: adoption, quantified from peer experience, with mitigation and an owner.": {
            "ok": True,
            "feedback": "**The right risk slide.** One material risk, quantified from peer experience, with a mitigation the board can verify later and a named owner for the deactivation decision. The board needs evidence that you know the biggest risk and have instrumented it; the full register stays with the project team.",
            "slide": "**Slide 3: the risk.** Adoption. At a peer system, 47% of rheumatologists dismiss a similar alert every time it fires.\n\n- Mitigation: champion-led soft launch with 5 rheumatologists in month 5\n- Override rate on the monthly dashboard from day one\n- The AI Governance Committee owns a deactivation trigger if the alert is ignored or causes harm",
        },
        "The full risk register: all eight project risks with likelihood and impact scores.": {
            "ok": False,
            "feedback": "**Wrong altitude.** The register is a real artifact (the capstone builds one) and the board should hear that it exists and who reviews it. Reading it aloud spends the 10 minutes on items the board cannot act on and buries the one risk that matters. Name the material risk; reference the register in a sentence.",
            "slide": "**Slide 3: the risk.** The project register tracks eight risks: integration-engine capacity, value-set drift, threshold retuning, training decay, regression-test gaps, model drift on local data, scope creep, and security.",
        },
        "Standard assurance: risks exist, as with any IT project, and will be managed per standard procedures.": {
            "ok": False,
            "feedback": "**Generic reassurance reads as evasion.** It gives the board nothing to evaluate and nothing to follow up on. A specific risk with an owner and a monitoring plan builds more credibility than no risk at all: the board learns that you have looked, found the material risk, and instrumented it.",
            "slide": "**Slide 3: the risk.** As with any IT project, risks exist and will be managed according to Helios standard procedures.",
        },
    }

    return PITCH_ASKS, PITCH_EVIDENCE, PITCH_RISKS, mo


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 06: Leadership and communication

        Next month's Board of Trustees agenda allocates you 10 minutes to present the RA flare-risk alert. The chair's instruction is specific: three slides maximum. Ten minutes in front of a board compresses everything this track covers into one task: choosing a leadership behavior to match the moment, ordering a message so the decision survives interruption, and negotiating from interests rather than positions.

        This track covers four leadership styles and the situational case for switching among them, executive communication (BLUF, the what / so what / now what structure, the one-page discipline), interest-based negotiation through a live conflict from the deployment, and the clinical informatics career path as orientation. The interactive is the pitch itself: you choose what goes on each of the three slides, and the assembled deck renders with feedback.
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
        ## Leadership styles: a choice of behavior, not a personality

        Leadership style is a behavior chosen for a specific team and task, not a fixed trait of the leader. Four named styles cover most of what the deployment requires, and the deployment requires all four at different points.

        | Style | Mechanism | In an informatics setting | Where it fits the RA-CDS deployment |
        |---|---|---|---|
        | **Transformational** | Motivates through a shared vision of a changed future; connects individual effort to purpose. | Framing the alert as treat-to-target made operational rather than one more popup; public credit for the team's work. | The skeptical rheumatology department in months 1 and 5: content review and training run on persuasion, not authority. |
        | **Transactional** | Sets explicit expectations and deliverables, monitors progress, corrects deviations, rewards completion. | Build checklists, deadline tracking, daily stand-ups, issue-closure rates. | Cutover week and the month-4 validation window, when the task list is explicit and slippage is expensive. |
        | **Servant** | Removes obstacles and absorbs friction so the team can do its work. | Securing the integration-engine slot the EHR analyst is blocked on; shielding the build from scope requests; taking escalations personally. | The build team in months 2 and 3. |
        | **Situational** | Diagnoses the team's competence and commitment for the task at hand, then matches direction and support to that diagnosis. | Directing a new fellow closely on a validation task while delegating card-text revision to the experienced analyst. | The whole deployment: it is the rule for selecting among the other three. |

        The situational case is the load-bearing one: the right style follows the team's task maturity and the urgency of the moment, not the leader's personality. A leader who is transformational by temperament and nothing else will inspire the build team while its task list slips; a leader who is transactional by temperament and nothing else will manage the skeptical rheumatology department into open resistance. One deployment, run well, uses all four styles, sometimes in the same week.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Executive communication: BLUF and the one-page discipline

        BLUF (bottom line up front) is the ordering rule for executive communication: the conclusion and the ask come first, and the support follows in descending order of importance. The convention comes from military staff writing, where the reader may be interrupted at any line. It inverts the structure clinical training rewards: a journal article holds its conclusion until after methods and results; an executive document leads with it. An executive audience reads or listens until interrupted, and BLUF prices the interruption: whatever the clock cuts off, the decision has already been heard.

        The **what / so what / now what** structure is BLUF operationalized into three moves.

        | Move | The question it answers | The RA-CDS content |
        |---|---|---|
        | **What** | What is true, or what happened? | The flare-risk alert goes live in rheumatology in six months; the build is on schedule. |
        | **So what** | Why does it matter to this audience? | About 31 flares averted per year across 1,247 patients, at $4K to $6K of added utilization each; $60K per year to run. |
        | **Now what** | What decision or action is requested? | Endorse the ongoing operating commitment. |

        The one-page discipline completes the set: an executive document that does not fit on one page is unfinished thinking. The page carries the what, the so what, and the now what; an appendix carries the detail for the reader who asks for it. The 3-slide ceiling on the board pitch is the same discipline applied to a deck.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            **Course 15 covers the craft underneath this section.** Track 1 (audience) defines the altitude rule the pitch builder below enforces; Track 2 covers writing about data in language an executive can act on; Track 3's narrative structure (finding, implication, recommendation) is what / so what / now what under another name.
            """
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    quiz1 = mo.ui.radio(
        options=[
            "The same three slides, delivered faster.",
            "Slide 2 only: the evidence is the strongest material.",
            (
                "The ask in the first sentence, one line of evidence, the "
                "one material risk, and an offer of the full deck in the "
                "board packet."
            ),
            (
                "Request deferral to next quarter's meeting, where the "
                "full 10 minutes is available."
            ),
        ],
        label=(
            "The board agenda overruns and the chair cuts your 10-minute "
            "slot to 3 minutes, starting now. Which version do you deliver?"
        ),
    )
    quiz1
    return (quiz1,)


@app.cell
def _(mo, quiz1):
    if quiz1.value is None:
        _resp = mo.callout(mo.md("_Choose an answer._"), kind="neutral")
    elif quiz1.value.startswith("The ask in the first sentence"):
        _resp = mo.callout(
            mo.md(
                "**Correct.** BLUF exists for the compressed case. A pitch "
                "ordered ask-first degrades gracefully: at 3 minutes the "
                "board still hears the decision, the strongest line of "
                "support, and the material risk, and the packet carries the "
                "rest. The faster-slides version loses the ask to the clock "
                "the moment a trustee asks a question. Evidence-only "
                "informs without converting attention into a decision. "
                "Deferral costs a quarter, and if the operating budget "
                "closes before the next meeting, it costs the ask itself "
                "(Track 7 covers that calendar)."
            ),
            kind="success",
        )
    else:
        _resp = mo.callout(
            mo.md(
                "**Reconsider the ordering.** The test of an executive "
                "pitch is what survives compression. Delivering the same "
                "deck faster gambles the ask against the clock and the "
                "first question. Evidence alone informs the board without "
                "asking it for anything, which wastes the slot. Deferral "
                "costs a quarter and, near budget season, possibly the "
                "operating line itself. The version that works states the "
                "ask in the first sentence, gives one line of evidence and "
                "the one material risk, and offers the full deck in the "
                "board packet: BLUF applied under pressure."
            ),
            kind="warn",
        )
    _resp
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Conflict and negotiation: positions and interests

        A position is what a party says it wants; an interest is the need underneath it. Positional bargaining trades concessions on stated demands and converges, when it converges at all, on a split that satisfies nobody. Interest-based negotiation names the needs underneath the demands and searches for terms that satisfy them. The distinction is the core of principled negotiation as Fisher and Ury framed it, and it is the single most useful negotiation move available to a working informaticist.

        The deployment's live example: in the month-1 clinical content review, the rheumatology chief opens with "we will not have another alert in this clinic." That is a position, and arguing against it produces a win/lose outcome: alert or no alert. The interest underneath is "do not waste my clinicians' time." Naming the interest reframes the negotiation from *whether* to *under what conditions*: a 0.30 firing threshold tuned so that most cards that fire warrant action, a card at chart open rather than an interruptive modal, a soft launch limited to 5 rheumatologists, and an override-rate dashboard with a deactivation trigger the chief can see. Each term answers the interest. None of them concedes the position.

        | Party | Position (stated) | Interest (underneath) | Terms that satisfy the interest |
        |---|---|---|---|
        | Rheumatology chief | "We will not have another alert." | Do not waste my clinicians' time. | Tuned threshold, non-interruptive card, soft launch, visible deactivation trigger. |
        | CIO | "No unplanned integration work mid-cycle." | Platform stability and a managed queue. | The integration-engine work scheduled inside the build window through the IT queue, escalated via the CMIO if it slips (Track 1). |
        | CFO | "No new recurring headcount." | Predictable, capped ongoing cost. | A fixed $60K-per-year operating line with monitoring and retuning inside it, no incremental FTE request. |

        Most informatics conflicts are resource conflicts stated in clinical or technical language. The governance routes from Track 1 are the structural resolution mechanism; interest-naming is the interpersonal one. Use both.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The 3-slide board pitch

        A board of trustees is the most executive audience in the building: fiduciaries, mostly non-clinicians, governing on mission, margin, and material risk. Three slides at board altitude do three jobs. Slide 1 states the ask, because BLUF puts the decision first. Slide 2 carries the evidence at the altitude the board can act on. Slide 3 names the material risk and its mitigation, because a board that hears no risk stops believing the evidence.

        Build the deck below. Each choice returns feedback on the reasoning, and the assembled deck renders underneath.
        """
    )
    return


@app.cell
def _(PITCH_ASKS, mo):
    slide1_pick = mo.ui.radio(
        options=list(PITCH_ASKS.keys()),
        label="Slide 1: the ask. What do you put in front of the board?",
    )
    mo.vstack([mo.md("### Slide 1: the ask"), slide1_pick])
    return (slide1_pick,)


@app.cell
def _(PITCH_ASKS, mo, slide1_pick):
    if slide1_pick.value is None:
        _resp = mo.callout(mo.md("_Choose an ask._"), kind="neutral")
    else:
        _opt = PITCH_ASKS[slide1_pick.value]
        _resp = mo.callout(
            mo.md(_opt["feedback"]),
            kind="success" if _opt["ok"] else "warn",
        )
    _resp
    return


@app.cell
def _(PITCH_EVIDENCE, mo):
    slide2_pick = mo.ui.radio(
        options=list(PITCH_EVIDENCE.keys()),
        label="Slide 2: the evidence. Which headline carries the case?",
    )
    mo.vstack([mo.md("### Slide 2: the evidence"), slide2_pick])
    return (slide2_pick,)


@app.cell
def _(PITCH_EVIDENCE, mo, slide2_pick):
    if slide2_pick.value is None:
        _resp = mo.callout(mo.md("_Choose a headline._"), kind="neutral")
    else:
        _opt = PITCH_EVIDENCE[slide2_pick.value]
        _resp = mo.callout(
            mo.md(_opt["feedback"]),
            kind="success" if _opt["ok"] else "warn",
        )
    _resp
    return


@app.cell
def _(PITCH_RISKS, mo):
    slide3_pick = mo.ui.radio(
        options=list(PITCH_RISKS.keys()),
        label="Slide 3: the risk. What does the board hear about what could go wrong?",
    )
    mo.vstack([mo.md("### Slide 3: the risk"), slide3_pick])
    return (slide3_pick,)


@app.cell
def _(PITCH_RISKS, mo, slide3_pick):
    if slide3_pick.value is None:
        _resp = mo.callout(mo.md("_Choose a risk statement._"), kind="neutral")
    else:
        _opt = PITCH_RISKS[slide3_pick.value]
        _resp = mo.callout(
            mo.md(_opt["feedback"]),
            kind="success" if _opt["ok"] else "warn",
        )
    _resp
    return


@app.cell
def _(PITCH_ASKS, PITCH_EVIDENCE, PITCH_RISKS, mo, slide1_pick, slide2_pick, slide3_pick):
    if None in (slide1_pick.value, slide2_pick.value, slide3_pick.value):
        _out = mo.callout(
            mo.md(
                "_The assembled deck renders here once all three slides "
                "are chosen._"
            ),
            kind="neutral",
        )
    else:
        _picks = [
            ("Slide 1", PITCH_ASKS[slide1_pick.value]),
            ("Slide 2", PITCH_EVIDENCE[slide2_pick.value]),
            ("Slide 3", PITCH_RISKS[slide3_pick.value]),
        ]
        _weak = [_name for _name, _opt in _picks if not _opt["ok"]]
        if not _weak:
            _verdict = (
                "**Verdict.** This deck survives the 10-minute slot and "
                "the 3-minute compression: the ask leads, the evidence "
                "sits at board altitude, and the risk slide builds "
                "credibility instead of spending it."
            )
            _kind = "success"
        else:
            _verdict = (
                f"**Verdict.** Slides at board altitude: {3 - len(_weak)} "
                f"of 3. Rework {', '.join(_weak)}: the feedback under "
                "each choice states what the board needs instead."
            )
            _kind = "warn"
        _deck_md = "\n\n---\n\n".join(
            ["## The assembled deck"]
            + [_opt["slide"] for _name, _opt in _picks]
            + [_verdict]
        )
        _out = mo.callout(mo.md(_deck_md), kind=_kind)
    _out
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The career path: orientation, not board prep

        The clinical informatics certification pathway has four components, and the working informaticist is asked about them constantly: by trainees, by recruiters, by their own CMIO.

        - **AMIA 10x10.** Continuing-education courses run by AMIA with university partners, named for the 2005 goal of training 10,000 informaticists by 2010. An entry point for clinicians evaluating the field. Continuing education, not certification.
        - **Clinical informatics fellowship.** ACGME-accredited, a minimum of 24 months, open to physicians who have completed residency in any ABMS specialty. The practice pathway closed with the 2025 exam cycle, so the fellowship is the route to board eligibility.
        - **The ABPM certification exam.** Clinical informatics is a board subspecialty administered jointly by the American Board of Preventive Medicine and the American Board of Pathology: pathologists apply through ABPath, physicians from every other specialty through ABPM. The exam blueprint includes the Leading and Managing Change domain, about 20% of the exam, the domain this course maps to.
        - **Continuing certification.** ABPM's Continuing Certification Program (CCP, the successor to maintenance of certification) maintains the credential through ongoing CME and assessment requirements.

        One honest statement about scope: this curriculum maps to much of the ABPM content outline, and Course 16 addresses the Leading and Managing Change domain directly, but it is not a board-prep product. Board preparation requires the official exam content outline, timed question practice, and the operational exposure a fellowship provides. This curriculum's job is to make the field's concepts usable at work; the go-deeper resources for this track include the certifying board's own pages.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The artifact: the executive-pitch summary

        The track's artifact is the three-slide pitch in summary form: the ask, the evidence, the risk. The worked version for the RA-CDS:

        | Slide | Content |
        |---|---|
        | **The ask** | Endorse the ongoing operating commitment: about $60K per year for monitoring, retuning, and report maintenance after go-live. The $240K build is committed; the run cost is the decision that outlives the project. |
        | **The evidence** | About 31 moderate-to-severe flares averted per year across the 1,247-patient RA panel, at $4K to $6K of added utilization per flare: an annual benefit near $155K against $60K operating, break-even near month 31, and a five-year NPV of about $195K under the Track 5 budget assumptions. One patient sentence: a CRP run-up like Ms. Reyes's 36.2 mg/L is now caught at chart open. |
        | **The risk** | Adoption: at a peer system, 47% of rheumatologists dismiss a similar alert every time it fires. Mitigation: champion-led soft launch with 5 rheumatologists in month 5, override rate on the monthly dashboard, and a deactivation trigger owned by the AI Governance Committee. |

        The capstone collects this three-field summary as the executive-pitch section of the implementation plan. The budget figures come from Track 5, the governance names from Track 1, and the adoption-risk number from Track 3.

        Track 7 covers the strategic layer underneath the pitch: why the RA-CDS won a portfolio slot at the IT Steering Committee in the first place, and the capital-cycle calendar the budget facts depend on.
        """
    )
    return


if __name__ == "__main__":
    app.run()
