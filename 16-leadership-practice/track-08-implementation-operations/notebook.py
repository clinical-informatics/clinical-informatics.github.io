"""Track 08: Implementation and operations of clinical information systems.

No visible code. The notebook presents the deploy-and-run distinction,
go-live command-center operations, the change-control board (standard vs
normal vs emergency changes, the AI Governance gate on model-behavior
changes), the L1/L2/L3 support-tier structure with SLAs, downtime
procedures, the release and optimization cadence, and sunset/retirement,
all on the RA flare-risk alert from the Course 12 capstone. The interactive
is an eight-scenario ticket-routing exercise; the artifact is the
post-go-live operations plan the capstone collects as section 9.

WASM-safe: no shared imports, no data files, no relative paths.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    ROUTE_OPTIONS = [
        "L1: help desk",
        "L2: application analyst",
        "L3: builder / vendor escalation",
        "Change-control board",
        "Quality & Safety escalation",
        "Not a ticket tier: another pathway",
    ]

    TICKETS = [
        {
            "text": (
                "A rheumatologist calls the help desk: \"How do I dismiss "
                "this card?\""
            ),
            "answer": "L1: help desk",
            "also": [],
            "feedback": (
                "A how-do-I question has a scripted answer and a "
                "knowledge-base article; L1 resolves it at first contact. "
                "The frequency of the question is the second finding: the "
                "same question forty times in a month is a usability "
                "defect, and L1's call log feeds that signal to the "
                "optimization queue."
            ),
        },
        {
            "text": (
                "The alert fired on a patient with psoriatic arthritis, "
                "not RA."
            ),
            "answer": "L2: application analyst",
            "also": ["L3: builder / vendor escalation"],
            "feedback": (
                "L2 reproduces the misfire and triages it. Here the cohort "
                "value set turns out to include a code it should not, "
                "which is a build defect: L3 corrects it, and the "
                "correction enters change control as a normal change. The "
                "triage step exists because most misfire reports "
                "are workflow or data-entry findings, and L2 separates "
                "those from true defects before an engineer is engaged."
            ),
        },
        {
            "text": (
                "A rheumatologist requests that the firing threshold drop "
                "from 0.30 to 0.20: \"I want to see more of these.\""
            ),
            "answer": "Change-control board",
            "also": [],
            "feedback": (
                "The edit is one field in a configuration file; the effect "
                "is a different intervention with a higher alert burden "
                "and a different false-positive mix. A model-behavior "
                "change requires AI Governance Committee sign-off in "
                "addition to change-control review. The request itself is "
                "welcome evidence that a clinician trusts the alert; the "
                "routing protects the whole panel from a one-clinician "
                "configuration edit."
            ),
        },
        {
            "text": (
                "The CDS service timed out for 40 minutes this morning; no "
                "cards displayed. Charts opened normally."
            ),
            "answer": "L3: builder / vendor escalation",
            "also": ["Quality & Safety escalation"],
            "feedback": (
                "An outage of the service is an incident: L3 owns the root "
                "cause (service, network, or integration engine), and the "
                "fail-silent design worked as specified because charts "
                "still opened. A second route runs in parallel: Quality & "
                "Safety owns the harm question. Which eligible patients' "
                "charts opened during the gap, and would the card have "
                "fired? The silent-mode infrastructure from month 4 of the "
                "build can replay the window and answer it."
            ),
        },
        {
            "text": (
                "A new rheumatology fellow needs access to the panel and "
                "asks who grants it."
            ),
            "answer": "L1: help desk",
            "also": [],
            "feedback": (
                "Access provisioning into an existing security class is a "
                "pre-approved standard change with a documented procedure; "
                "L1 executes it. No board, no analyst, no engineer. "
                "Standard changes exist so that routine, repeatable work "
                "moves at help-desk speed while remaining audited."
            ),
        },
        {
            "text": (
                "After the EHR quarterly upgrade, the card renders with a "
                "truncated action-button label."
            ),
            "answer": "L2: application analyst",
            "also": [],
            "feedback": (
                "L2 confirms and reproduces the rendering defect; the fix "
                "itself is small. The durable finding is a regression-test "
                "gap: the upgrade cycle's test suite did not include card "
                "rendering, so the next upgrade could break it again. "
                "Adding the rendering check to the regression suite goes "
                "through change control as the lasting correction."
            ),
        },
        {
            "text": (
                "A patient asks her rheumatologist why the care team got "
                "an alert about her; the rheumatologist forwards the "
                "question to you."
            ),
            "answer": "Not a ticket tier: another pathway",
            "also": [],
            "feedback": (
                "A patient's question about an algorithm in her care is "
                "clinical communication, not a support ticket. The "
                "rheumatologist answers the patient; your contribution is "
                "a plain-language description of what the alert is and is "
                "not, written for the patient audience Course 15 defined. "
                "Patient-facing transparency about algorithmic tools is a "
                "design question in its own right; Course 19 addresses it."
            ),
        },
        {
            "text": (
                "The month-3 report shows the override rate moved from "
                "about 60% to 85% across two weeks."
            ),
            "answer": "Not a ticket tier: another pathway",
            "also": [],
            "feedback": (
                "A two-week shift of that size is the Track 4 control "
                "chart speaking: a signal, not a ticket. Investigate "
                "before retuning (Track 3: resistance is information). "
                "What changed two weeks ago? The quarterly upgrade and its "
                "truncated action button are a candidate cause: a card "
                "whose button does not work gets dismissed. QI signals "
                "route to investigation through the measurement system, "
                "never into the support queue."
            ),
        },
    ]

    return ROUTE_OPTIONS, TICKETS, mo


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 08: Implementation and operations of clinical information systems

        Go-live day, 07:00. The command center opens. Six months from now, nobody will remember the project; they will know only whether the system works every day. This track specifies what runs between those two points: the command center and its exit criteria, the change-control board, the support tiers, the downtime procedures, the release and optimization cadence, and, eventually, retirement.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            r"""
            **The running scenario.** In the Course 12 capstone you produced a CDS design brief for an RA flare-risk alert: at chart open (the `patient-view` CDS Hook), for patients with active rheumatoid arthritis, when the recent CRP trajectory and clinical context put the probability of a flare in the next 90 days above the 0.30 firing threshold, a card suggests scheduling a treatment-escalation conversation rather than waiting for the next routine visit. The AI Governance Committee approved the brief, and the CMIO gave you six months to go-live. The six months have run. The build is live at Helios Academic Medical Center, the rheumatology panel holds 1,247 patients with RA, and Ms. Reyes is in the cohort: her CRP run-up to 36.2 mg/L before adalimumab started is exactly the trajectory the alert exists to catch.
            """
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A project ends; a system runs

        The project that built the RA-CDS has a charter, a timeline, a budget, and an end date. The system it produced has none of those: it has users, defects, upgrades, outages, and a retirement date nobody has scheduled yet. Day-2 operations, everything after the go-live stabilizes, is where a clinical information system lives for 95% of its lifespan, and it is where the system's reputation is set. Clinicians do not remember that the build finished on schedule; they remember whether the card was wrong last Tuesday.

        Four things change at the project-to-operations boundary, and each needs a named owner before the project team disbands:

        - **Funding** moves from the project budget to the operating budget (Track 5): monitoring, retuning, and report maintenance are now line items, not milestones.
        - **Governance** moves from project steering to change control: decisions are no longer "is this in scope" but "is this change safe to make on a live clinical system."
        - **Staffing** moves from builders to support tiers: the people who answer the phone are no longer the people who wrote the logic.
        - **Measurement** moves from milestones to KPIs and SLAs (Track 4): progress is replaced by performance.

        A deployment that plans the build and not the run hands the operations organization a problem instead of a system.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The go-live command center

        The command center is the temporary structure that absorbs the first weeks of operation, when issue volume is highest and the support tiers are not yet practiced. A hospital-wide EHR go-live staffs a physical room with dozens of people for weeks. A department-scoped CDS go-live warrants the same structure at smaller scale: a staffed channel, a short roster, the same cadence and exit criteria. The structure is the load-bearing part, not the headcount.

        **The roster** for the RA-CDS command center:

        | Role | Who, for the RA-CDS |
        |---|---|
        | Command-center lead | You. Owns the issue board, the stand-ups, and the escalation decisions. |
        | At-the-elbow support | Two trained superusers rotating through the rheumatology clinics during sessions. |
        | Application analyst (L2) | The EHR analyst who did the build, reachable all day. |
        | Builder / engineer (L3) | The CDS-service engineer on call; the integration engineer reachable. |
        | Vendor line | The EHR vendor's support contact, with the contract's escalation terms at hand. |
        | Clinical lead | The rheumatology chief or a designated attending, for clinical judgment calls. |

        **The cadence:** stand-ups at 07:00, 12:00, and 16:30. Each stand-up reviews the issue board by severity; every open issue leaves with an owner, a next action, and a due time. Severity levels make triage a rule rather than an argument:

        | Severity | Definition | RA-CDS example | Response |
        |---|---|---|---|
        | Sev1 | System down or active patient-safety exposure | A service defect that blocks chart open for rheumatology | All hands, immediately; the lead owns communication outward |
        | Sev2 | Major function degraded; a workaround exists | No cards displayed for 40 minutes; charts still open | Response within 30 minutes; incident tracked to root cause |
        | Sev3 | Single-user or low-impact defect | One workstation renders the card with a truncated button | Within one business day, through the standard tiers |
        | Sev4 | Cosmetic issue or enhancement request | A rheumatologist wants the card reworded | Logged to the optimization queue; not an incident |

        **The exit criteria** are written before go-live, so the decision to close the command center is a check against stated conditions rather than a judgment call. For the RA-CDS: five consecutive business days with no Sev1 or Sev2; ticket arrival at or below the projected steady state (about five per week at this scope) and falling; every open ticket owned inside the standard tiers with an SLA; at-the-elbow support withdrawn without a ticket spike the following week; sign-off from the rheumatology clinical lead; and a written handoff to the standard support organization covering known issues, workarounds, the regression-test suite, and the contact tree.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The change-control board

        Live clinical systems fail most often immediately after someone changes them. Change control exists to force the questions that the person making a "small" change does not ask alone: what consumes this field, what fires off this interface, what is the rollback if the change is wrong. An unreviewed one-line edit to a live clinical system is how outages happen, and the size of the edit predicts nothing about the size of the consequence.

        The board classifies every change into one of three types. Classification follows risk and review path, never the size of the diff:

        | Change type | Definition | Approval path | RA-CDS examples |
        |---|---|---|---|
        | **Standard** | Pre-approved, low-risk, routine, with a documented repeatable procedure | None per instance; the category is approved once and audited | Adding a new fellow to the existing user security class; the monthly server patch inside the maintenance window |
        | **Normal** | Material risk or novelty; assessed case by case | The board: risk assessment, test evidence, rollback plan, scheduled window | Revising the card text after a soft-launch PDSA; repointing the service at a new CRP result interface |
        | **Emergency** | Required now to resolve an outage or an active patient-safety exposure | Expedited approval by a designated approver; full documentation and board review after the fact | Disabling the card's order action while it misroutes referrals |

        One rule sits on top of the three types for the RA-CDS. Any change that alters model behavior (the firing threshold, the input features, the cohort value set, retraining on new data) requires **AI Governance Committee sign-off in addition to change-control review**. Lowering the threshold from 0.30 to 0.20 is one field in a configuration file, and it changes who the alert fires on, the alert burden per clinician, and the false-positive mix across the whole panel. The configuration is small; the intervention is different.

        The board also owns the **freeze window**: defined periods when normal changes are not scheduled, typically the go-live stabilization period itself, the EHR vendor's quarterly upgrade window, and high-census periods the institution designates. Emergency changes remain available during a freeze; the freeze restricts elective ones.
        """
    )
    return


@app.cell
def _(mo):
    quiz1 = mo.ui.radio(
        options=[
            (
                "Standard change: a one-line correction is exactly the "
                "routine, low-risk case the standard category exists for."
            ),
            (
                "Normal change: submit the risk assessment and rollback "
                "plan to the change-control board for its weekly meeting."
            ),
            (
                "Emergency change: expedited approval now, full "
                "documentation and board review afterward."
            ),
        ],
        label=(
            "Wednesday, 14:20, three weeks after full launch. The EHR "
            "analyst discovers that the card's action button queues a "
            "referral to dermatology instead of rheumatology: a mapping "
            "defect introduced by Tuesday's quarterly upgrade. The fix is "
            "a one-line mapping correction. Classify the change."
        ),
    )
    quiz1
    return (quiz1,)


@app.cell
def _(mo, quiz1):
    if quiz1.value is None:
        _resp = mo.callout(mo.md("_Pick a classification._"), kind="neutral")
    elif quiz1.value.startswith("Emergency change"):
        _resp = mo.callout(
            mo.md(
                "**Correct.** Classification follows risk and review path, "
                "not the size of the edit. The defect is live and actively "
                "misrouting referrals: every click queues the wrong "
                "specialty, and the cost of waiting for the weekly board "
                "is measured in misdirected orders. The emergency path "
                "still has structure: a designated approver authorizes the "
                "change before it goes in, the fix is tested as far as the "
                "situation allows, and the board reviews the full "
                "documentation after the fact. The second finding is the "
                "regression-test gap: a quarterly upgrade changed your "
                "build's behavior, so the upgrade suite gains a test that "
                "would have caught this."
            ),
            kind="success",
        )
    else:
        _resp = mo.callout(
            mo.md(
                "**Reconsider the classification.** Standard means "
                "pre-approved and repeatable: a defect fix to live "
                "clinical logic is neither, and the size of the edit is "
                "irrelevant to the category. Normal means the risk "
                "tolerates the board's calendar: a defect actively "
                "misrouting referrals does not. The defect qualifies for "
                "the emergency path: expedited approval by a designated "
                "approver, the fix applied now, full documentation and "
                "board review afterward. The durable correction is adding "
                "card-action mapping to the upgrade regression suite."
            ),
            kind="warn",
        )
    _resp
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Support tiers and the SLA

        Once the command center closes, support runs through three tiers. Tickets route by the nature of the fix required: knowledge routes to L1, configuration and investigation to L2, code to L3.

        | Tier | Who | What routes there | SLA example |
        |---|---|---|---|
        | **L1** | Help desk, working from scripts and a knowledge base | Password and access requests, how-do-I questions, first-contact triage of everything else | 80% of contacts resolved at first contact; 15-minute callback on the rest |
        | **L2** | Application analysts | Configuration questions, build investigation, reproducing reported defects, workflow questions | Acknowledgment within 4 business hours; resolution targets by severity |
        | **L3** | Builders, integration engineers, the vendor | Code and model defects, interface failures, anything requiring a change to the build (which then enters change control) | Engaged by L2 escalation; resolution targets by severity |

        A **service-level agreement** states the response and resolution targets per severity in advance, so "how fast" is a commitment rather than a per-ticket negotiation. The SLA is also the measurement instrument for the support organization itself: missed SLAs are a Track 4 time series.

        Two kinds of events are not tickets at all, and the routing discipline has to recognize them. **Changes** belong to the change-control board, however casually they arrive ("can you drop the threshold a bit?"). **Signals** belong to governance and the measurement system: harm questions route to Quality & Safety, and QI patterns route to investigation through the Track 4 control charts. The exercise below tests all three distinctions.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Downtime, planned and unplanned

        Planned downtime is scheduled unavailability: maintenance windows, upgrades, migrations, all announced and staged. Unplanned downtime is failure: hardware, network, interface, or security incident. Course 05 Track 1 defined the two numbers that govern recovery: **RPO** (how much data the institution accepts losing) and **RTO** (how long it accepts being down). Those numbers, written into the architecture and the vendor contract long before any outage, determine what the recovery procedure can promise.

        Every downtime procedure has four components:

        1. **Downtime forms.** Pre-staged paper workflows for ordering, documentation, and medication administration, kept current with the live build. Stale forms are a defect.
        2. **Read-only shadow access.** A business-continuity copy of the chart, updated near real time, so clinicians can see the record while writes are down.
        3. **The recovery sequence.** Restore in dependency order (infrastructure, database, application, interfaces), verify each layer before starting the next, and declare uptime explicitly rather than letting users discover it.
        4. **Reconciliation.** Back-entry of the paper record with late-entry flags, verification of orders placed during the downtime, and a check on what the queued interfaces deliver when they catch up. Restoration without reconciliation leaves the chart silently incomplete.

        The RA-CDS has its own entry in the downtime plan, and it is a design commitment: **fail silent and safe**. When the EHR cannot reach the CDS service, the chart opens without a card; the timeout is part of the build, and a stale or wrong card is worse than no card. Writing the fail mode into the operations plan turns a 40-minute service outage into an incident with a severity level instead of a mystery. The harm review afterward belongs to Quality & Safety: which eligible patients' charts opened during the gap, and would the card have fired? The silent-mode month of the build (month 4: the alert computed but did not display) created exactly the replay capability that answers that question.

        Course 22 covers the hard case: a security incident turns unplanned downtime from hours into days or weeks, and the recovery sequence acquires a forensic step that ordinary failure does not have.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Releases, upgrades, and the optimization queue

        Two release streams touch the RA-CDS, on two calendars.

        **The vendor's stream.** The EHR vendor ships quarterly upgrades on its calendar, not yours, and each one can change the substrate under your build. The defense is a **regression-test suite** owned by your team and run in the upgrade's test environment every cycle: the card renders completely, the action button maps to the right order, the prefetch returns what the service expects, the hook fires on chart open. The suite grows by accretion; every defect an upgrade causes becomes a test the next upgrade must pass.

        **Your stream.** The CDS service has its own releases: bug fixes, performance work, and model retraining. A retrain is a release with an extra gate. The change-control board reviews it as a normal change, and AI Governance signs off on it as a model-behavior change, with the validation evidence attached.

        Go-live ends the build queue, not the work. Track 2 assigned the post-launch work to a **Kanban queue**, and this is where that queue lives: card-text refinements, threshold-review requests (which exit the queue into governance), training refreshers, and enhancement requests that survive triage. The queue has three intake sources: tickets reclassified as enhancements, L1 frequency signals (the same how-do-I question forty times is a usability defect, not forty tickets), and the Track 4 dashboard. A monthly optimization review with the rheumatology clinical lead prioritizes the queue; requests from other departments to extend the infrastructure are not queue items at all but portfolio requests for IT Steering (Track 7).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Sunset and retirement

        Systems end: replaced by a vendor module, absorbed in a platform consolidation, or retired when the clinical need changes. Retirement is an operations task with its own checklist: interfaces disconnected in dependency order, access ended, licenses closed out, monitoring removed.

        The data outlives the application. Medical-record retention obligations run years past decommissioning (state rules commonly require 7 to 10 years for adult records, longer for minors), and the alert's audit trail (what fired, for whom, at what threshold, and what the clinician did) is part of the legal record. Three retention patterns exist: migrate the data into the successor system, extract it to an archive, or keep the application alive read-only. Read-only legacy access is the most common pattern and the most quietly expensive: an unpatched legacy application kept for occasional lookups is a security liability for as long as it runs (Course 22).

        For the RA-CDS, the operations plan writes the retirement terms in advance. If Helios licenses the hypothetical vendor flare module from Track 5 in year 4, the plan states what is kept: the firing history, the override history, and the model versions and thresholds in force at each date.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Route the tickets

        Eight events from the first quarter after full launch. For each, pick the routing. Some are tickets, some are changes, and some are not tickets at all. The principle under test: routing follows the nature of the response required, never the channel the report arrived through.
        """
    )
    return


@app.cell
def _(ROUTE_OPTIONS, TICKETS, mo):
    ticket1 = mo.ui.dropdown(options=ROUTE_OPTIONS, label="Routing")
    ticket2 = mo.ui.dropdown(options=ROUTE_OPTIONS, label="Routing")
    ticket3 = mo.ui.dropdown(options=ROUTE_OPTIONS, label="Routing")
    ticket4 = mo.ui.dropdown(options=ROUTE_OPTIONS, label="Routing")
    ticket5 = mo.ui.dropdown(options=ROUTE_OPTIONS, label="Routing")
    ticket6 = mo.ui.dropdown(options=ROUTE_OPTIONS, label="Routing")
    ticket7 = mo.ui.dropdown(options=ROUTE_OPTIONS, label="Routing")
    ticket8 = mo.ui.dropdown(options=ROUTE_OPTIONS, label="Routing")

    _widgets = [
        ticket1, ticket2, ticket3, ticket4,
        ticket5, ticket6, ticket7, ticket8,
    ]
    _stack = []
    for _i, _w in enumerate(_widgets, start=1):
        _stack.append(
            mo.md(f"**Scenario {_i}.** {TICKETS[_i - 1]['text']}")
        )
        _stack.append(_w)
    mo.vstack(_stack)
    return (
        ticket1,
        ticket2,
        ticket3,
        ticket4,
        ticket5,
        ticket6,
        ticket7,
        ticket8,
    )


@app.cell
def _(
    TICKETS,
    mo,
    ticket1,
    ticket2,
    ticket3,
    ticket4,
    ticket5,
    ticket6,
    ticket7,
    ticket8,
):
    _widgets = [
        ticket1, ticket2, ticket3, ticket4,
        ticket5, ticket6, ticket7, ticket8,
    ]
    _blocks = []
    _n_answered = 0
    _n_correct = 0
    for _i, (_w, _t) in enumerate(zip(_widgets, TICKETS), start=1):
        if _w.value is None:
            _blocks.append(
                mo.callout(
                    mo.md(f"**Scenario {_i}.** Pick a routing above."),
                    kind="neutral",
                )
            )
            continue
        _n_answered += 1
        if _w.value == _t["answer"]:
            _n_correct += 1
            _blocks.append(
                mo.callout(
                    mo.md(
                        f"**Scenario {_i}. Correct: {_t['answer']}.** "
                        f"{_t['feedback']}"
                    ),
                    kind="success",
                )
            )
        elif _w.value in _t["also"]:
            _n_correct += 1
            _blocks.append(
                mo.callout(
                    mo.md(
                        f"**Scenario {_i}. Defensible: {_w.value}; the "
                        f"primary routing is {_t['answer']}.** "
                        f"{_t['feedback']}"
                    ),
                    kind="success",
                )
            )
        else:
            _blocks.append(
                mo.callout(
                    mo.md(
                        f"**Scenario {_i}. Not {_w.value}: this routes to "
                        f"{_t['answer']}.** {_t['feedback']}"
                    ),
                    kind="warn",
                )
            )
    if _n_answered == 8:
        _summary = mo.md(
            f"**{_n_correct} of 8 routed correctly.** Routing follows the "
            "nature of the response required: knowledge to L1, "
            "configuration and investigation to L2, code to L3, changes "
            "to the board, harm questions to Quality & Safety, and "
            "signals to the measurement system. The channel a report "
            "arrives through never determines the route."
        )
    else:
        _summary = mo.md(f"_{_n_answered} of 8 scenarios routed so far._")
    mo.vstack(_blocks + [_summary])
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The artifact: the post-go-live operations plan

        The capstone collects an operations plan as section 9 of the implementation plan. The worked version for the RA-CDS has five components, each one a commitment made before go-live rather than improvised after it.

        **1. Command-center exit criteria.** Five consecutive business days with no Sev1 or Sev2; ticket arrival at or below about five per week and falling; all open tickets owned in the standard tiers with SLAs; at-the-elbow support withdrawn without a subsequent ticket spike; rheumatology clinical-lead sign-off; written handoff to the standard support organization.

        **2. Support tiers and SLAs.** L1 help desk: how-do-I questions and access provisioning, 80% first-contact resolution. L2 application analyst: configuration and defect triage, acknowledgment within 4 business hours. L3 builder and vendor escalation: code, model, and interface defects, resolution targets by severity. Missed-SLA rates reported monthly as a Track 4 time series.

        **3. Change-control rules.** Standard, normal, and emergency change definitions as above, with the freeze windows named. The AI Governance gate stated explicitly: changes to the firing threshold, the input features, the cohort value set, or the model weights require AI Governance Committee sign-off in addition to board review.

        **4. Downtime procedures.** The fail-silent commitment: when the EHR cannot reach the CDS service, the chart opens without a card, never with a stale one. Service outages are Sev2 incidents with L3 root-cause ownership; every outage triggers a Quality & Safety replay of the gap using the silent-mode infrastructure. EHR-wide downtime follows the institutional procedure (forms, read-only shadow, recovery sequence, reconciliation), and the alert resumes only after the reconciled data is verified current.

        **5. Optimization-queue cadence.** A Kanban queue with three intake sources (reclassified tickets, L1 frequency signals, the KPI dashboard), reviewed monthly with the rheumatology clinical lead. Threshold and model-change requests exit the queue into governance; cross-department extension requests exit to IT Steering.

        An implementation plan without this section commits the institution to a go-live and to nothing after it.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Where this goes next

        This track completes the eight track artifacts. The capstone assembles the project charter (Track 1), the RACI and the timeline (Track 2), the change-management plan (Track 3), the KPI dashboard (Track 4), the budget and ROI (Track 5), the executive pitch (Track 6), the strategic-alignment statement (Track 7), and this operations plan, plus a new risk register, into the implementation plan the CMIO asked for on day one. Two later courses extend the operational threads: Course 17 treats the sociotechnical and workflow side of operating clinical systems, and Course 22 treats security operations and incident response, including the security incident as the hard case of unplanned downtime.
        """
    )
    return


if __name__ == "__main__":
    app.run()
