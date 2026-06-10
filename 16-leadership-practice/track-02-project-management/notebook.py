"""Track 02: Project management for informatics.

The RA flare-risk CDS from the Course 12 capstone is approved and the
CMIO wants a project plan within two weeks. The track presents PMBOK's
five process groups, methodology fit (waterfall, Agile, Scrum, Kanban),
Gantt charts and the critical path, the RACI matrix and the one-A rule,
the scope/time/cost triangle, and the SDLC, all worked on the six-month
Helios deployment. Two interactives carry the track: a Gantt builder
that validates the dependency chain and a RACI builder that validates
ownership.

WASM-safe: no shared imports, no data files, no relative paths.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import pandas as pd

    return alt, mo, pd


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 02: Project management for informatics

        You have six months. The CMIO wants a project plan in two weeks. A project plan is three commitments in one document: what will ship (scope), when each piece happens and in what order (the schedule), and who does and who answers for each piece (ownership). The plan is also a negotiation instrument: when pressure arrives mid-project, the plan is what makes the cost of each option visible before anyone pays it.

        This track presents the toolkit that produces those commitments: PMBOK's five process groups as the shared vocabulary, methodology selection as a fit decision, the Gantt chart and its critical path, the RACI matrix, the scope/time/cost triangle that governs what gives under pressure, and the SDLC that names where the build sits inside the plan. The RA-CDS deployment is the worked example throughout.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            "**The running scenario.** In the Course 12 capstone you produced a CDS design brief for an RA flare-risk alert. At chart open (the patient-view CDS Hook), for patients with active rheumatoid arthritis, when the recent CRP trajectory and clinical context put the probability of a flare in the next 90 days above the 0.30 firing threshold, a card suggests scheduling a treatment-escalation conversation rather than waiting for the next routine visit. The AI Governance Committee approved the brief, and the CMIO's email arrived this morning: you are leading the implementation, and go-live is six months out. The deployment serves the 1,247-patient rheumatology panel at Helios Academic Medical Center. Ms. Reyes is in the cohort: her CRP run-up to 36.2 mg/L before adalimumab started is exactly the trajectory the alert exists to catch."
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The vocabulary: PMBOK's five process groups

        A project is a temporary effort with a defined start, a defined end, and a defined deliverable. The RA-CDS deployment qualifies: it begins with the CMIO's email and ends at full launch. The system that runs afterward is not a project, and Track 8 covers that distinction.

        PMBOK (the Project Management Body of Knowledge, the Project Management Institute's reference standard) organizes project work into five process groups. The groups are phases of attention, not strictly sequential phases of time: monitoring and controlling runs alongside executing from the first week.

        | Process group | What it contains | On the RA-CDS |
        |---|---|---|
        | **Initiating** | Authorize the project: name the sponsor, the purpose, the stakeholders, the success criteria. | The project charter (Track 1's artifact), with the CMIO as sponsor and the AI Governance approval on record. |
        | **Planning** | Commit to scope, schedule, budget, ownership, and risk handling. | This track's Gantt and RACI; Track 5's budget; the capstone's risk register. |
        | **Executing** | Do the work the plan commits to. | The months 2 to 3 technical build; training delivery in month 5. |
        | **Monitoring and controlling** | Measure progress against the plan and control changes to scope and schedule. | Weekly status against the Gantt; the scope decisions the triangle section below governs. |
        | **Closing** | Hand the deliverable to operations, release the team, record what was learned. | The transition to the Track 8 operations structure after full launch. |

        PMBOK also defines ten knowledge areas (scope, schedule, cost, quality, resources, communications, risk, procurement, stakeholders, integration). The process groups are the time axis of project work; the knowledge areas are the subject axis. This track works the scope, schedule, and resource cells of that grid. Track 5 covers cost; the capstone adds the risk register.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Four methodologies and the situation each fits

        Methodology selection is a fit decision, not an allegiance. Each of the four below was developed for a specific shape of work, and each fails predictably when applied to the wrong shape.

        | Methodology | Core mechanism | Fits | Fails when |
        |---|---|---|---|
        | **Waterfall** | Sequential phases with sign-off gates: requirements, design, build, test, deploy. | Fixed requirements and high change cost: EHR module rollouts, interface builds, anything anchored to freeze windows and training calendars. | Requirements are still being discovered, so the first real user feedback arrives after the budget is spent. |
        | **Agile** | Iterative delivery in short cycles; requirements are allowed to evolve between cycles. A value system (the 2001 Agile Manifesto), not a single method. | Novel analytics and model development, where the requirement is discovered by building. | The deliverable must be specified completely up front (a regulated interface, a contracted scope). |
        | **Scrum** | Agile formalized: fixed-length sprints, a prioritized backlog, a sprint goal, a review and retrospective each cycle. | Teams doing iterative work that benefits from cadence: model validation and tuning cycles. | Work arrives continuously as unpredictable single items rather than plannable batches. |
        | **Kanban** | A continuous-flow board (to do, in progress, done) with explicit work-in-progress limits; no fixed iterations. | Operations queues: support tickets, optimization requests, post-launch tuning. | The work is one large interdependent build with a fixed end date. |

        The RA-CDS deployment is a hybrid, which is the usual case in clinical informatics. The EHR integration build runs as waterfall: the CDS Hooks service work and the EHR build slots are sequenced against freeze windows and carry sign-off gates. Model validation and card-text tuning in months 4 and 5 run as Scrum sprints: two-week cycles against a defined backlog, with the five soft-launch rheumatologists as the review audience. The post-launch optimization queue runs as Kanban: requests arrive continuously, get prioritized continuously, and ship one at a time.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            "**Forward to Track 8 (implementation and operations).** The Kanban queue named above outlives the project. After full launch the project closes and the team disperses, but the optimization queue becomes a permanent operations structure with its own intake, triage, and cadence. Track 8 covers the deploy-and-run distinction and where the queue lives."
        ),
        kind="neutral",
    )
    return


@app.cell
def _(mo):
    quiz1 = mo.ui.radio(
        options=[
            "Waterfall: gather all the requests, specify a release, build it in phases",
            "Scrum: batch the requests into two-week sprints with a sprint goal",
            "Kanban: a continuous-flow queue with explicit work-in-progress limits",
            "None of these: reopen the project and re-baseline the Gantt",
        ],
        label=(
            "Eight weeks after full launch, requests arrive steadily: one rheumatologist wants the card to show the last three CRP values, another wants the dismiss-reason wording changed, the clinical informatics fellow proposes suppressing the card when a visit is already scheduled within 14 days. Each request is small, independent, and arrives unpredictably. Which methodology fits this work?"
        ),
    )
    quiz1
    return (quiz1,)


@app.cell
def _(mo, quiz1):
    if quiz1.value is None:
        _resp = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif quiz1.value.startswith("Kanban"):
        _resp = mo.callout(
            mo.md(
                "**Correct.** Continuous, unpredictable arrival of small independent items is the Kanban shape: a visible queue, work-in-progress limits, continuous prioritization, no fixed iterations. Scrum adds sprint-planning overhead that buys nothing when the items are independent and arrival is unplanned; waterfall batches the feedback away until a distant release. One caution: the suppression request changes alert behavior, so it enters the queue only after change control and AI Governance Committee sign-off. Track 8 covers that routing."
            ),
            kind="success",
        )
    else:
        _resp = mo.callout(
            mo.md(
                "**Reconsider the shape of the work.** The items are small, mutually independent, and arrive unpredictably. Waterfall and Scrum both impose batching (a specified release, a sprint goal) on work that has no natural batch, and re-baselining the Gantt treats operations as a project, which it is not. The continuous-flow shape is Kanban: queue the items, limit work in progress, prioritize continuously."
            ),
            kind="warn",
        )
    _resp
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The schedule: milestones, dependencies, the critical path

        A Gantt chart shows time horizontally and work vertically: each bar is an activity with a start and a duration, and the ordering encodes dependencies. Three terms carry the analytical weight.

        - **Milestone.** A zero-duration checkpoint that either happened or did not: rheumatology sign-off obtained, silent mode started, full launch reached. Milestones are what the CMIO reads; activities are what the team works.
        - **Dependency.** Activity B cannot start until activity A finishes. Dependencies are facts about the work, not preferences: validation cannot test a build that does not exist.
        - **Critical path.** The longest dependency-ordered chain through the plan. Any slip on the critical path slips go-live day for day. Activities off the path have slack; activities on it have none, and the project manager's attention belongs disproportionately to them.

        The six-month plan the CMIO expects:

        | Month | Milestone |
        |---|---|
        | 1 | Clinical content review (rheumatology sign-off on alert logic and card text) |
        | 2-3 | Technical build (CDS Hooks service integration, EHR build) |
        | 4 | Validation testing (silent mode: alert computes but does not display) |
        | 5 | User training + soft launch (5 rheumatologists) |
        | 6 | Full launch (all rheumatologists) |

        Every row depends on the one above it, so the critical path runs through the entire plan: a two-week slip in the build is a two-week slip in go-live unless something else gives. The triangle section below states what that something is.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Interactive: build the Gantt

        Six activities below; the month-5 row of the canonical table splits into two activities, user training and the soft launch, which run in parallel during month 5. Each activity has a start month and a duration. The defaults reproduce the canonical plan; the chart and the feedback react to every change.

        Run two experiments. First, compress the technical build to one month and read the flag. Second, move validation testing after full launch (a sequencing some real projects have effectively chosen under deadline pressure) and read the flag.
        """
    )
    return


@app.cell
def _(mo):
    _month_opts = {f"Month {_i}": _i for _i in range(1, 7)}
    _dur_opts = {"1 month": 1, "2 months": 2, "3 months": 3}
    review_start = mo.ui.dropdown(options=_month_opts, value="Month 1", label="Start")
    review_dur = mo.ui.dropdown(options=_dur_opts, value="1 month", label="Duration")
    build_start = mo.ui.dropdown(options=_month_opts, value="Month 2", label="Start")
    build_dur = mo.ui.dropdown(options=_dur_opts, value="2 months", label="Duration")
    valid_start = mo.ui.dropdown(options=_month_opts, value="Month 4", label="Start")
    valid_dur = mo.ui.dropdown(options=_dur_opts, value="1 month", label="Duration")
    train_start = mo.ui.dropdown(options=_month_opts, value="Month 5", label="Start")
    train_dur = mo.ui.dropdown(options=_dur_opts, value="1 month", label="Duration")
    soft_start = mo.ui.dropdown(options=_month_opts, value="Month 5", label="Start")
    soft_dur = mo.ui.dropdown(options=_dur_opts, value="1 month", label="Duration")
    launch_start = mo.ui.dropdown(options=_month_opts, value="Month 6", label="Start")
    launch_dur = mo.ui.dropdown(options=_dur_opts, value="1 month", label="Duration")
    mo.vstack(
        [
            mo.md("**1. Clinical content review**"),
            mo.hstack([review_start, review_dur], justify="start", gap=1),
            mo.md("**2. Technical build**"),
            mo.hstack([build_start, build_dur], justify="start", gap=1),
            mo.md("**3. Validation testing (silent mode)**"),
            mo.hstack([valid_start, valid_dur], justify="start", gap=1),
            mo.md("**4. User training**"),
            mo.hstack([train_start, train_dur], justify="start", gap=1),
            mo.md("**5. Soft launch (5 rheumatologists)**"),
            mo.hstack([soft_start, soft_dur], justify="start", gap=1),
            mo.md("**6. Full launch (all rheumatologists)**"),
            mo.hstack([launch_start, launch_dur], justify="start", gap=1),
        ]
    )
    return (
        build_dur, build_start, launch_dur, launch_start, review_dur, review_start,
        soft_dur, soft_start, train_dur, train_start, valid_dur, valid_start,
    )


@app.cell
def _(alt, build_dur, build_start, launch_dur, launch_start, mo, pd, review_dur, review_start, soft_dur, soft_start, train_dur, train_start, valid_dur, valid_start):
    plan_df = pd.DataFrame(
        [
            {"order": 1, "activity": "Clinical content review", "start": review_start.value, "months": review_dur.value},
            {"order": 2, "activity": "Technical build", "start": build_start.value, "months": build_dur.value},
            {"order": 3, "activity": "Validation testing (silent mode)", "start": valid_start.value, "months": valid_dur.value},
            {"order": 4, "activity": "User training", "start": train_start.value, "months": train_dur.value},
            {"order": 5, "activity": "Soft launch (5 rheumatologists)", "start": soft_start.value, "months": soft_dur.value},
            {"order": 6, "activity": "Full launch (all rheumatologists)", "start": launch_start.value, "months": launch_dur.value},
        ]
    )
    plan_df["end"] = plan_df["start"] + plan_df["months"]
    _bars = (
        alt.Chart(plan_df)
        .mark_bar(height=16, cornerRadius=3)
        .encode(
            y=alt.Y("activity:N", sort=alt.EncodingSortField(field="order", order="ascending"), title=""),
            x=alt.X("start:Q", axis=alt.Axis(tickMinStep=1, title="Month")),
            x2="end:Q",
            tooltip=["activity:N", "start:Q", "months:Q"],
        )
    )
    _deadline = alt.Chart(pd.DataFrame({"month": [7]})).mark_rule(strokeDash=[6, 4], color="firebrick").encode(x="month:Q")
    mo.vstack(
        [
            (_bars + _deadline).properties(width=560, height=210, title="The RA-CDS plan as you have set it"),
            mo.md(
                "_Each bar spans the months its activity occupies. The dashed line marks the end of month 6, the go-live commitment; a bar crossing it means the plan overruns the commitment._"
            ),
        ]
    )
    return (plan_df,)


@app.cell
def _(mo, plan_df):
    _p = {str(_r["activity"]): (int(_r["start"]), int(_r["start"]) + int(_r["months"])) for _i, _r in plan_df.iterrows()}
    _rev = _p["Clinical content review"]
    _bld = _p["Technical build"]
    _val = _p["Validation testing (silent mode)"]
    _trn = _p["User training"]
    _sft = _p["Soft launch (5 rheumatologists)"]
    _lch = _p["Full launch (all rheumatologists)"]
    _flags = []
    if _bld[0] < _rev[1]:
        _flags.append(
            "**The build starts before clinical content review completes.** The build implements the logic and card text that rheumatology signs off on in the review. Building first means building content that may not survive sign-off, and the rework adds time to the critical path."
        )
    if _val[0] < _bld[1]:
        _flags.append(
            "**Validation starts before the build completes.** Silent mode tests the production build against live chart-open traffic; it has nothing to test until the build exists."
        )
    if _val[0] >= _lch[0]:
        _flags.append(
            "**Validation is scheduled at or after full launch.** Silent mode exists to find the false fires before any clinician sees a card. Validating after launch makes the 1,247-patient panel the test environment."
        )
    if _trn[0] < _bld[1]:
        _flags.append(
            "**Training starts before the build completes.** Training on an unfinished build produces retraining when the card changes, and retraining costs more credibility than training."
        )
    if _trn[0] < _val[1]:
        _flags.append(
            "**Training starts before validation completes.** Silent mode is what proves the alert fires on the right patients; training clinicians on an unvalidated alert teaches a workflow the validation may still change."
        )
    if _sft[0] < _val[1]:
        _flags.append(
            "**The soft launch starts before validation completes.** Silent mode means no card displays, so a soft launch during it is a contradiction, and a soft launch before it shows live cards nobody has verified."
        )
    if _sft[0] < _trn[0]:
        _flags.append(
            "**The soft launch precedes training.** The five soft-launch users would see the card before anyone has shown them what it is and what acting on it means."
        )
    if _lch[0] < _sft[1]:
        _flags.append(
            "**Full launch begins before the soft launch completes.** The 5-user soft launch exists to surface workflow problems at a survivable scale; launching to all rheumatologists before it finishes discards that information."
        )
    if (_bld[1] - _bld[0]) < 2:
        _flags.append(
            "**A one-month technical build is unrealistic for this scope.** The CDS Hooks service integration and the EHR build each carry their own build-and-test cycle, and the integration-engine work queues against other projects' demands. The canonical estimate is two months, and it is not padded."
        )
    _latest = max(_e for _s, _e in _p.values())
    if _latest > 7:
        _flags.append(
            "**The plan overruns the six-month commitment.** Go-live dates anchor to training calendars and freeze windows, so a plan that ends after month 6 is a renegotiation with the CMIO, not a schedule."
        )
    if _flags:
        _result = mo.callout(mo.md("**The plan has problems:**\n\n" + "\n".join(f"- {_f}" for _f in _flags)), kind="warn")
    else:
        _result = mo.callout(
            mo.md(
                "**No sequencing violations.** The plan respects the dependency chain: review before build, build before silent validation, validation before training and the soft launch, soft launch before full launch, everything inside the six-month window. The capstone collects this timeline as section 3 of the implementation plan."
            ),
            kind="success",
        )
    _result
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The triangle: scope, time, cost

        Every project constraint reduces to three quantities: scope (what ships), time (when it ships), and cost (the resources spent shipping it). The triangle's rule: when one corner is fixed and pressure arrives, another corner gives. The corner that gives silently when none is allowed to give openly is quality.

        In healthcare IT, time is usually the fixed corner. A go-live date anchors to the training calendar (rooms booked, sessions scheduled, clinical coverage arranged), to EHR freeze windows (build changes prohibited around upgrades and high-census periods), and to the credibility cost of announcing a date twice. Compressing time is therefore rarely available, and buying time with cost rarely works either: onboarding a second EHR analyst mid-build consumes the first analyst's time before it returns any. Brooks's law states the general case: adding people to a late project makes it later.

        That leaves scope as the working margin. The disciplined response to mid-project pressure is to move scope out of the launch and into the post-launch queue, with a named owner and a committed review date. Deferral with a date is a plan; deferral without one is a quiet no.
        """
    )
    return


@app.cell
def _(mo):
    quiz2 = mo.ui.radio(
        options=[
            "Time: push go-live by three weeks to build the sparkline",
            "Cost: add a second EHR analyst so the sparkline ships at go-live",
            "Scope: launch without the sparkline and route it to the post-launch queue",
            "Nothing: absorb the work into the validation month without changing the plan",
        ],
        label=(
            "In month 4, the rheumatology chief asks that the card also display a DAS28 trend sparkline at launch. The build is complete and silent-mode validation is under way. Go-live is fixed. What gives?"
        ),
    )
    quiz2
    return (quiz2,)


@app.cell
def _(mo, quiz2):
    if quiz2.value is None:
        _resp2 = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif quiz2.value.startswith("Scope"):
        _resp2 = mo.callout(
            mo.md(
                "**Correct.** Time is anchored: the training calendar and the freeze windows do not move for a sparkline. Cost fails Brooks's law in month 4: a new analyst returns nothing before go-live. Absorbing the work silently is the worst answer, because reopening a completed build mid-validation invalidates the silent-mode run and the time comes out of testing depth, which is quality giving without anyone deciding it. Scope gives: launch without the sparkline, enter it in the optimization queue with the chief named as requester and a review date in the first post-launch cycle. The chief gets a commitment, the go-live keeps its date, and the validation stays valid."
            ),
            kind="success",
        )
    else:
        _resp2 = mo.callout(
            mo.md(
                "**Work the triangle.** Time is anchored to the training calendar and freeze windows; it does not move for a card enhancement. Cost cannot buy time this late: a second analyst onboards slower than the deadline arrives (Brooks's law). Absorbing the work silently reopens a completed build during validation, which invalidates the silent-mode run and takes the time out of testing depth: quality gives without anyone deciding it. The remaining corner is scope: defer the sparkline to the post-launch queue with a named owner and a committed review date."
            ),
            kind="warn",
        )
    _resp2
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Ownership: the RACI matrix

        The schedule says when; the RACI matrix says who. For each activity, the matrix assigns each role at most one of four letters.

        - **R, Responsible.** Does the work. At least one per activity, often several.
        - **A, Accountable.** Owns the outcome and answers for it. Exactly one per activity: the one-A rule. Two A's is a negotiation deferred to the worst possible moment; zero A's is an orphaned activity.
        - **C, Consulted.** Provides input before the work is done. Two-way communication.
        - **I, Informed.** Told after. One-way.

        Two failure patterns recur in real matrices. An A with no R is accountability for work nobody is assigned to do; the activity stalls while everyone assumes someone else has it. And an executive listed as R for build tasks is a planning smell: the CMIO sponsors the deployment, clears escalations, and reports upward; the CMIO does not build interfaces, and a matrix that says otherwise has not actually assigned the work.

        In the builder below, set the Accountable (one per activity, enforced by the dropdown) and the Responsible roles for each of the five RA-CDS activities. Roles you leave unmarked default to Consulted or Informed; the reference matrix in the artifact section fills those in.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            "**Callback to Track 1 (the working clinical informaticist).** Track 1 defined these roles operationally and mapped the committees above them. The RACI assigns activities to roles; the committee layer (AI Governance, EMR Optimization, IT Steering) sits above the matrix as approval gates, not as rows that do work."
        ),
        kind="neutral",
    )
    return


@app.cell
def _(mo):
    RACI_ROLES = [
        "You (the informaticist)",
        "CMIO",
        "EHR analyst",
        "Rheumatology chief",
        "AI Governance Committee",
    ]
    acc_logic = mo.ui.dropdown(options=RACI_ROLES, label="Accountable")
    resp_logic = mo.ui.multiselect(options=RACI_ROLES, label="Responsible")
    acc_build = mo.ui.dropdown(options=RACI_ROLES, label="Accountable")
    resp_build = mo.ui.multiselect(options=RACI_ROLES, label="Responsible")
    acc_card = mo.ui.dropdown(options=RACI_ROLES, label="Accountable")
    resp_card = mo.ui.multiselect(options=RACI_ROLES, label="Responsible")
    acc_train = mo.ui.dropdown(options=RACI_ROLES, label="Accountable")
    resp_train = mo.ui.multiselect(options=RACI_ROLES, label="Responsible")
    acc_monitor = mo.ui.dropdown(options=RACI_ROLES, label="Accountable")
    resp_monitor = mo.ui.multiselect(options=RACI_ROLES, label="Responsible")
    mo.vstack(
        [
            mo.md("**1. Write and validate the alert logic**"),
            mo.hstack([acc_logic, resp_logic], justify="start", gap=1),
            mo.md("**2. Build the EHR integration**"),
            mo.hstack([acc_build, resp_build], justify="start", gap=1),
            mo.md("**3. Design the card text**"),
            mo.hstack([acc_card, resp_card], justify="start", gap=1),
            mo.md("**4. Train the rheumatologists**"),
            mo.hstack([acc_train, resp_train], justify="start", gap=1),
            mo.md("**5. Monitor post-launch performance**"),
            mo.hstack([acc_monitor, resp_monitor], justify="start", gap=1),
        ]
    )
    return (
        RACI_ROLES, acc_build, acc_card, acc_logic, acc_monitor, acc_train,
        resp_build, resp_card, resp_logic, resp_monitor, resp_train,
    )


@app.cell
def _(RACI_ROLES, acc_build, acc_card, acc_logic, acc_monitor, acc_train, mo, resp_build, resp_card, resp_logic, resp_monitor, resp_train):
    _entries = [
        ("Write and validate the alert logic", acc_logic, resp_logic),
        ("Build the EHR integration", acc_build, resp_build),
        ("Design the card text", acc_card, resp_card),
        ("Train the rheumatologists", acc_train, resp_train),
        ("Monitor post-launch performance", acc_monitor, resp_monitor),
    ]
    _unassigned = [_n for _n, _a, _r in _entries if _a.value is None]
    _flags = []
    for _n, _a, _r in _entries:
        if _a.value is not None and not _r.value:
            _flags.append(
                f"**\"{_n}\" has an Accountable but nobody Responsible.** The one-A rule has a companion: every activity needs at least one R, or the accountability is for work nobody is doing."
            )
    _build_tasks = ("Write and validate the alert logic", "Build the EHR integration")
    for _n, _a, _r in _entries:
        if _n in _build_tasks and "CMIO" in (_r.value or []):
            _flags.append(
                f"**The CMIO is listed as Responsible for \"{_n}\".** The CMIO sponsors the deployment, arbitrates escalations, and reports upward. An executive marked R for build work signals a plan that has not actually assigned the work."
            )
    _cmio_a = sum(1 for _n, _a, _r in _entries if _a.value == "CMIO")
    if _cmio_a >= 3:
        _flags.append(
            f"**The CMIO is Accountable for {_cmio_a} of 5 activities.** Accountability placed above the level that can act on it recreates the orphaned matrix: the sponsor answers for the investment; the deployment lead answers for the activities."
        )
    if _unassigned:
        raci_feedback = mo.callout(
            mo.md(
                "_Assign an Accountable for each activity. Still unassigned: "
                + "; ".join(_unassigned)
                + ". The dropdown enforces at most one A; the one-A rule also forbids zero._"
            ),
            kind="neutral",
        )
    elif _flags:
        raci_feedback = mo.callout(mo.md("**Fix these before the matrix is usable:**\n\n" + "\n".join(f"- {_f}" for _f in _flags)), kind="warn")
    else:
        _lines = [
            "| Activity | " + " | ".join(RACI_ROLES) + " |",
            "|---|---|---|---|---|---|",
        ]
        for _n, _a, _r in _entries:
            _cells = []
            for _role in RACI_ROLES:
                _marks = []
                if _a.value == _role:
                    _marks.append("A")
                if _role in (_r.value or []):
                    _marks.append("R")
                _cells.append(", ".join(_marks))
            _lines.append("| " + _n + " | " + " | ".join(_cells) + " |")
        raci_feedback = mo.vstack(
            [
                mo.callout(
                    mo.md(
                        "**Structurally valid.** Every activity has exactly one Accountable, every Accountable has at least one Responsible, and no executive is doing build work. Structural validity is necessary, not sufficient: compare your assignment against the reference matrix in the artifact section below, which records the reasoning for where each A sits."
                    ),
                    kind="success",
                ),
                mo.md("\n".join(_lines)),
            ]
        )
    raci_feedback
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The SDLC: the build inside the plan

        The software development lifecycle (SDLC) names six phases every system passes through: requirements, design, implementation, verification, deployment, maintenance. The Gantt above is the SDLC with dates attached.

        | SDLC phase | On the RA-CDS |
        |---|---|
        | **Requirements** | The Course 12 design brief: the patient-view hook, the 0.30 threshold, the card, the cohort. The requirements were finished before the project started, which is why waterfall fits the build. |
        | **Design** | Month 1: clinical content review turns the brief into sign-off-ready alert logic and card text. |
        | **Implementation** | Months 2 to 3: the CDS Hooks service integration and the EHR build. |
        | **Verification** | Month 4: silent mode. The alert computes against live chart-open traffic, no card displays, and the team compares fires against chart review. |
        | **Deployment** | Months 5 to 6: training, the 5-user soft launch, full launch. |
        | **Maintenance** | Everything after: monitoring, retuning, the optimization queue (Track 8). The longest phase by far. |
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            "**Callback to Course 13 (research reproducibility).** Course 13's reproducibility discipline is the SDLC's verification phase applied to analytic work: a documented, re-runnable analysis stands to a finding as silent-mode testing stands to a build. Both exist because the cost of discovering a defect rises steeply with every phase it survives."
        ),
        kind="neutral",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The artifacts this track contributes

        The Course 16 capstone assembles the implementation plan you will hand the CMIO. This track contributes two of its sections.

        **Capstone section 2: the RACI matrix.** The reference matrix below is one defensible assignment; the builder above validates structure, and this table records the reasoning.

        | Activity | You (the informaticist) | CMIO | EHR analyst | Rheumatology chief | AI Governance Committee |
        |---|---|---|---|---|---|
        | Write and validate the alert logic | A, R | I | C | C | C |
        | Build the EHR integration | A | I | R | | I |
        | Design the card text | R | I | C | A | I |
        | Train the rheumatologists | A, R | I | | C | |
        | Monitor post-launch performance | A, R | I | R | I | C |

        Three assignments carry the reasoning. The build row separates A from R: you answer for the integration, the EHR analyst builds it. The card-text row moves the A to the rheumatology chief: the card speaks to the chief's clinicians, so the clinical owner answers for what it says, while you draft (R) and the analyst advises on what the card renderer supports (C). And the CMIO's column is all I: the sponsor is informed, escalated to when arbitration is needed, and never Responsible for build work.

        **Capstone section 3: the timeline.** The canonical six-month milestone table from the schedule section above, with the dependency chain intact: clinical content review (month 1), technical build (months 2-3), validation testing in silent mode (month 4), user training and the 5-rheumatologist soft launch (month 5), full launch (month 6). The capstone collects it with editable dates; the dependency logic the Gantt builder enforced is the part that must survive editing.

        Track 3 addresses the people who must change behavior for the same deployment to work. A colleague at another health system reports that 47% of their rheumatologists dismiss a similar alert every time it fires; the next track covers why that happens and what prevents it.
        """
    )
    return


if __name__ == "__main__":
    app.run()
