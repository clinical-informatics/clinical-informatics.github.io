"""Track 01: The working clinical informaticist: roles, scope, day-to-day.

No visible code. The notebook covers the operational reality of the
informatics roles (CMIO, CNIO, CRIO, informatics director, EHR analyst,
clinical data scientist, health IT staff), reporting lines and the
dual-reporting design behind the CMIO-vs-CIO tension, the six interfaces
informatics serves, the Helios committee landscape, and the who-decides-what
matrix for clinical AI and CDS work. The interactive is a decision-routing
exercise across six RA-CDS deployment decisions. The artifact is the
project charter the capstone collects as section 1 of the implementation
plan.

WASM-safe: no shared imports, no data files, no network calls.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    ROUTE_OPTIONS = [
        "You (the implementation lead)",
        "CMIO",
        "CIO / IT operations",
        "AI Governance Committee",
        "IT Steering Committee",
        "EMR Optimization Committee",
        "Pharmacy & Therapeutics",
        "Rheumatology chief",
        "Quality & Safety Committee",
    ]

    OWNER_NOTES = {
        "You (the implementation lead)": (
            "You run the project day to day and triage operational defects, "
            "but you hold no formal decision rights over governance, design "
            "standards, or platform resources."
        ),
        "CMIO": (
            "The CMIO sponsors the project and carries escalations to the "
            "executive level; the CMIO is rarely the formal owner of an "
            "individual design or governance decision."
        ),
        "CIO / IT operations": (
            "The CIO's chain owns platform stability and the allocation of "
            "shared technical resources, and nothing else in the deployment."
        ),
        "AI Governance Committee": (
            "AI Governance owns sign-off on model behavior: approval for "
            "local use, threshold changes, retraining."
        ),
        "IT Steering Committee": (
            "IT Steering owns portfolio prioritization and capital: which "
            "projects run and in what order, never how a single alert is "
            "built or worded."
        ),
        "EMR Optimization Committee": (
            "EMR Optimization owns build slotting and alert design "
            "standards: how alerts look, read, and behave in the EHR."
        ),
        "Pharmacy & Therapeutics": (
            "P&T owns medication-use policy and is consulted whenever a "
            "system artifact recommends a change in drug therapy."
        ),
        "Rheumatology chief": (
            "The rheumatology chief owns the clinical content: whether the "
            "alert's logic and recommendation are right for the "
            "department's patients."
        ),
        "Quality & Safety Committee": (
            "Quality & Safety owns harm monitoring and investigation once a "
            "patient-safety question has been raised."
        ),
    }

    ROUTE_SCENARIOS = [
        {
            "text": (
                "The flare-risk model was trained at another institution. "
                "Who approves its use on Helios patients?"
            ),
            "answer": "AI Governance Committee",
            "why": (
                "AI Governance owns approval of any model acting on Helios "
                "patients, and external provenance raises the "
                "transportability question directly: case mix, assay "
                "behavior, and documentation patterns differ across "
                "institutions, so local validation precedes local use. The "
                "committee approved the design brief on this authority, and "
                "any later threshold change or retraining returns to it. If "
                "the committee and the clinical owner disagree, the CMIO "
                "carries the dispute to the CMO."
            ),
        },
        {
            "text": (
                "Two rheumatologists reviewing the draft card find the text "
                "too prescriptive and want it reworded. Who owns changing it?"
            ),
            "answer": "EMR Optimization Committee",
            "why": (
                "Card wording is an alert design question, and alert design "
                "standards belong to EMR Optimization. The change still "
                "requires rheumatology sign-off, because the department owns "
                "whether the revised wording is clinically right. The logic "
                "and the 0.30 threshold are untouched, so AI Governance is "
                "not re-engaged: the routing follows what changed."
            ),
        },
        {
            "text": (
                "The card recommends treatment intensification. Beyond "
                "rheumatology, which body must review the recommendation "
                "before launch?"
            ),
            "answer": "Pharmacy & Therapeutics",
            "why": (
                "P&T reviews it as a consulted party. Any system artifact "
                "that recommends intensifying drug therapy touches "
                "medication-use policy, so P&T sees the card before launch "
                "and flags formulary or safety conflicts. Consulted is the "
                "operative word: P&T cannot redesign the alert, and "
                "rheumatology retains clinical ownership of the "
                "recommendation."
            ),
        },
        {
            "text": (
                "Gastroenterology has seen the design brief and wants the "
                "same alert infrastructure for IBD flare risk. Who decides "
                "whether to extend it?"
            ),
            "answer": "IT Steering Committee",
            "why": (
                "Extending the infrastructure to a second department is a "
                "portfolio decision: new scope, new resources, a new place "
                "in the build queue. Portfolio prioritization is IT "
                "Steering's mandate, and Track 7 covers how such a request "
                "is scored against everything else on the agenda. Saying "
                "yes inside the RA project would be scope creep; the "
                "charter's scope line exists to force the request onto IT "
                "Steering's agenda."
            ),
        },
        {
            "text": (
                "The CDS service needs two days of integration-engine work "
                "in month 3, and the engine team is committed to a "
                "laboratory-interface migration. Who arbitrates between the "
                "competing demands?"
            ),
            "answer": "CIO / IT operations",
            "why": (
                "The integration engine is a shared platform resource, and "
                "the CIO owns its allocation. You request the time through "
                "IT operations; if the engine team's other commitments put "
                "the go-live at risk, the escalation runs through the CMIO, "
                "who argues clinical priority at the CMO-CIO executive "
                "level. The one move that fails is negotiating laterally "
                "with the engine team yourself: a commitment extracted "
                "without the CIO's chain behind it will not survive the "
                "next competing demand."
            ),
        },
        {
            "text": (
                "A rheumatologist reports that the alert fired on a patient "
                "who does not have RA. Who triages first?"
            ),
            "answer": "You (the implementation lead)",
            "why": (
                "You triage first: reproduce the firing, inspect the cohort "
                "definition (a value-set defect is the likely cause), and "
                "classify the severity. Track 8 covers the support tiers "
                "this routes through. The escalation trigger is harm: if "
                "the misfire changed care, the question leaves the ticket "
                "queue and goes to Quality & Safety. Triage and harm review "
                "are different jobs with different owners, and conflating "
                "them either buries a safety signal or convenes a committee "
                "for a configuration bug."
            ),
        },
    ]
    return OWNER_NOTES, ROUTE_OPTIONS, ROUTE_SCENARIOS, mo


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 01: The working clinical informaticist

        The CMIO's email is open on your screen: "Congratulations. You're leading the implementation. Go-live is six months out. Let me know what you need." Before you reply, three questions need answers. Who is on your team, and what does each role do in a working week? Who do you report to while you run this, and who do they report to? And which committees have to weigh in on the deployment, at which points, with what authority? This track answers all three for Helios Academic Medical Center, the 720-bed Boston academic medical center where the deployment runs. The org chart is fictional; the structure is the one most US health systems use.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            **The running scenario.** In the Course 12 capstone you produced a CDS design brief for an RA flare-risk alert. At chart open (the patient-view CDS Hook), for patients with active rheumatoid arthritis, when the recent CRP trajectory and clinical context put the probability of a flare in the next 90 days above the 0.30 firing threshold, a card suggests scheduling a treatment-escalation conversation rather than waiting for the next routine visit. The AI Governance Committee approved the brief. The CMIO's email arrived this morning; go-live is six months out. The rheumatology panel holds 1,247 patients with RA, and Ms. Reyes is in the cohort: her CRP run-up to 36.2 mg/L before adalimumab started is exactly the trajectory the alert exists to catch.
            """
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The roles, operationally

        Course 0 Track 6 introduced the titles. This track covers what each role does in a working week, because the deployment will require you to ask specific people for specific things, and the asks fail when they go to the wrong role.

        | Role | What the role does |
        |---|---|
        | **CMIO** (chief medical information officer) | Senior physician executive accountable for the clinical use of information systems. Sponsors clinical IT projects, owns clinical content direction, argues the clinical case in capital and platform decisions. Your sponsor on the RA-CDS. |
        | **CNIO** (chief nursing information officer) | The same accountability on the nursing side: nursing documentation, barcode medication administration, nursing workflow in the EHR. A separate role because nurses are the largest clinical workforce and their workflows are distinct. |
        | **CRIO** (chief research information officer) | Research informatics: the research data warehouse, cohort discovery, biobank linkage, and the regulatory boundary between care data and research use. Outside the RA-CDS chain unless the deployment generates research data. |
        | **Informatics director** | Runs the informatics team as an operation: intake, prioritization within committed scope, staffing, delivery. Translates the CMIO's direction into assigned work. |
        | **Informatics / EHR analyst** | The build layer. Configures the EHR, builds alerts, order sets, and registries, tests against requirements, documents changes. The person who will wire the CDS Hooks service into the EHR. |
        | **Clinical data scientist** | Builds and validates models and analytics. Built the flare-risk model; owns its local validation and its monitoring design. |
        | **Health IT (infrastructure) staff** | Servers, network, identity, the integration engine, the service desk. Report through the CIO, not through informatics. Every informatics deployment depends on their capacity. |

        The distinction that matters most for your reply to the CMIO: the analyst builds, the director assigns, the CMIO sponsors. A request for two days of analyst time goes to the director. A request for executive backing goes to the CMIO. Reversing the two wastes a week.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A working week

        Three of these roles structure your next six months. The table sketches a representative week for each.

        | | CMIO | Informatics director | EHR analyst |
        |---|---|---|---|
        | **Meetings** | Weekly 1:1 with the CMO; biweekly with the CIO; sponsor check-ins across 6 to 10 active projects | Weekly project-status reviews; staffing and intake triage; vendor calls | Daily team stand-up; working sessions with clinical subject-matter experts |
        | **Build and review work** | Reviews escalated design decisions; signs off on clinical content direction | Reviews build plans, test results, and change requests before they reach a committee | Builds and tests alert configurations, order sets, and interface connections; documents every change |
        | **Escalations** | Arbitrates clinical-priority vs platform conflicts at the executive level | First stop for stuck projects and resource conflicts; escalates to the CMIO what a director cannot resolve | Raises blockers to the director; routes defects into the support queue |
        | **Committee sessions** | Chairs EMR Optimization; sits on AI Governance, IT Steering, and Quality & Safety | Presents build items at EMR Optimization; staffs the AI Governance agenda | Rarely attends; prepares the artifacts committees review |

        Read the table as a routing guide. The RA-CDS will generate work in all twelve cells, and each piece of it has exactly one right starting row.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Reporting lines and why they are drawn that way

        Reporting lines come in two kinds. A **solid line** is formal authority: who writes the evaluation, sets the budget, and can reassign the role. A **dotted line** is structured obligation without authority: a standing duty to coordinate, inform, and align.

        The standard placements:

        - The **CMIO** reports solid-line to the **CMO** and dotted-line to the **CIO**. The clinical chain owns the role; the IT chain has a guaranteed seat in its work.
        - The **CNIO** reports to the **CNO**, mirroring the CMIO's placement on the nursing side.
        - The **CRIO** reports to the **chief research officer**, with a dotted line to IT.

        Dual reporting exists because informatics work is permanently two-sided: every decision has a clinical face (does this serve patient care) and a platform face (can the systems sustain it). The solid line to the clinical chain keeps the role's incentives anchored to care. The dotted line to IT keeps the role from making platform commitments IT cannot honor.

        The same design creates the field's classic boundary problem. The CMIO argues clinical priority; the CIO argues platform stability; both are right, by mandate. When the RA-CDS build needs integration-engine time during the CIO's stability freeze, neither can overrule the other, and the conflict resolves where the two chains meet: the executive table. The structure is deliberate. It forces clinical-vs-platform tradeoffs upward, to the level with authority over both, instead of letting them be settled quietly by whichever side happens to control the resource.
        """
    )
    return


@app.cell
def _(mo):
    quiz1 = mo.ui.radio(
        options=[
            (
                "The CMO outranks the CIO, so the CMIO can have the freeze "
                "overruled."
            ),
            (
                "It gives the clinical case an advocate whose standing does "
                "not depend on the IT chain: the CMIO argues clinical "
                "priority through the clinical chain, the CIO argues "
                "stability through the IT chain, and the conflict resolves "
                "at the level with authority over both."
            ),
            (
                "It removes the need to coordinate with IT; the clinical "
                "chain can schedule the engine work directly."
            ),
            (
                "It does not matter; reporting lines are administrative and "
                "have no effect on how conflicts resolve."
            ),
        ],
        label=(
            "Mid-build, the CIO freezes all integration-engine work for a "
            "platform-stability remediation. Your RA-CDS build needs two "
            "days of engine work to stay on schedule. Why does the CMIO's "
            "solid line to the CMO, rather than to the CIO, matter here?"
        ),
    )
    quiz1
    return (quiz1,)


@app.cell
def _(mo, quiz1):
    if quiz1.value is None:
        _resp = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif quiz1.value.startswith("It gives the clinical case"):
        _resp = mo.callout(
            mo.md(
                "**Correct.** The dual-reporting design routes the conflict "
                "upward instead of sideways. The CMIO cannot order the "
                "engine team to work (no authority in the IT chain), and "
                "the CIO cannot order the clinical case dropped (no "
                "authority over clinical priority). Each argues through its "
                "own chain, and the tradeoff is decided at the executive "
                "level, where one table holds authority over both care and "
                "platform. The solid line to the CMO guarantees the "
                "clinical case arrives at that table with standing, rather "
                "than as a subordinate request inside the IT chain it is "
                "arguing against."
            ),
            kind="success",
        )
    else:
        _resp = mo.callout(
            mo.md(
                "**Reconsider.** The solid line to the CMO does not let "
                "anyone overrule the freeze, and it does not remove the "
                "need to coordinate with IT; both chains keep their "
                "mandates. Its function is standing. If the CMIO reported "
                "to the CIO, the clinical case for the RA-CDS would be a "
                "subordinate request inside the chain whose stability "
                "mandate it is arguing against. Because the CMIO reports to "
                "the CMO, the clinical case travels its own chain and meets "
                "the platform case at the executive level, where one table "
                "holds authority over both and can decide the tradeoff "
                "openly."
            ),
            kind="warn",
        )
    _resp
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The six interfaces

        Informatics holds a working interface to six constituencies. Each wants something specific from informatics, and the deployment stalls when informatics fails to supply it. Each holds something informatics needs, and the deployment stalls when informatics fails to ask for it.

        | Interface | What they want from informatics | What informatics needs from them |
        |---|---|---|
        | **Clinical operations** | Systems that fit workflow; alert burden held down; problems fixed fast | Workflow truth (how the work is actually done), clinical champions, content sign-off |
        | **IT** | Clear requirements, realistic timelines, no surprise scope | Integration-engine time, environments, infrastructure capacity, security review |
        | **Research** | Clean data access, cohort tooling, honest provenance | Methods rigor, validation partnership, grant-funded informatics effort |
        | **Finance** | Quantified benefit, defensible budgets, predictable spend | Budget lines, capital sponsorship, FTE approval |
        | **C-suite** | One-page answers, risk surfaced early, initiatives that trace to strategy | Sponsorship, decision rights, arbitration when priorities conflict |
        | **Board** | Assurance on quality, safety, security, and fiduciary stewardship | The governance mandate that makes committee decisions binding |

        For the RA-CDS, four of the six activate immediately: clinical operations (rheumatology sign-off), IT (the CDS Hooks integration), finance (the budget Track 5 builds), and the C-suite (the CMIO's sponsorship). Research and the board stay quiet unless the deployment generates publishable evaluation data or a reportable safety event.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The committees and when each weighs in

        Helios runs six committees with authority over some part of the RA-CDS deployment. Course 03 Track 5 covered governance structures in principle; this table is the structure in operation.

        | Committee | Owns | When it weighs in on the RA-CDS |
        |---|---|---|
        | **AI Governance Committee** | Sign-off on model behavior: approval for clinical use, threshold changes, retraining | Already approved the design brief. Re-engaged for any change to the model or the 0.30 threshold, and for the local validation read-out before launch |
        | **IT Steering Committee** | Portfolio prioritization and capital | Slotted the project into the build calendar. Decides any extension of the infrastructure to another department |
        | **EMR Optimization Committee** | Build slotting and alert design standards | Reviews the card design and wording against alert standards during the build months |
        | **Pharmacy & Therapeutics** | Medication-use policy | Consulted before launch: the card recommends treatment intensification |
        | **Quality & Safety Committee** | Harm monitoring and investigation | Receives the silent-mode validation report; takes any post-launch harm signal |
        | **Rheumatology department** | Clinical ownership of the alert | Signs off on alert logic and card text in month 1; its clinicians train in month 5 |

        One absence matters: no committee owns the project. Committees own decisions. The project is owned by you, sponsored by the CMIO, and it moves by bringing the right decision to the right committee at the right time.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Who decides what

        The committee table answers where; this matrix answers who, for the decision types that recur in clinical AI, CDS, and analytics work. The project charter at the end of this track cites the matrix as its governance path.

        | Decision | Decides | Consulted | If contested, escalates to |
        |---|---|---|---|
        | Approve a model for local clinical use | AI Governance Committee | Rheumatology, you | CMO |
        | Change the firing threshold or retrain | AI Governance Committee | Rheumatology chief, clinical data scientist | CMO |
        | Card text and alert design standards | EMR Optimization Committee | Rheumatology (sign-off required) | CMIO |
        | Whether the recommendation is clinically right | Rheumatology department | P&T | CMO |
        | Portfolio slot; extension to other departments | IT Steering Committee | CMIO, CIO | Capital planning / CEO |
        | Shared platform resources (integration engine, environments) | CIO / IT operations | You | CMIO, to the CMO-CIO executive level |
        | Harm-signal investigation | Quality & Safety Committee | You, rheumatology | CMO and the board's quality committee |

        Two properties of the matrix are load-bearing. First, you appear in the Consulted column and never in the Decides column: the implementation lead routes decisions and supplies evidence but holds no formal decision rights. Second, every escalation path ends at a clinical executive or a body with clinical authority. The structure encodes the premise of the deployment: a clinical intervention delivered through technology, governed accordingly.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Exercise: route the decision

        The org chart below is Helios in compact form. Six deployment decisions follow; for each, pick the owner. The feedback explains the routing and the escalation path.

        ```
        Board of Trustees
         |- Quality committee of the board
         |- CEO
             |- CMO (chief medical officer)
             |    |- CMIO  [dotted line to CIO]
             |    |    |- Informatics director
             |    |         |- EHR analysts, clinical data scientists, CI fellow
             |    |- Rheumatology department chief
             |- CIO (chief information officer)
             |    |- Health IT: infrastructure, integration engine, security,
             |       service desk
             |- CNO (chief nursing officer)
             |    |- CNIO
             |- CFO
             |- Chief research officer
                  |- CRIO  [dotted line to IT]

        Cross-cutting committees: AI Governance, IT Steering, EMR Optimization,
        Pharmacy & Therapeutics, Quality & Safety
        ```
        """
    )
    return


@app.cell
def _(ROUTE_OPTIONS, ROUTE_SCENARIOS, mo):
    route1 = mo.ui.dropdown(options=ROUTE_OPTIONS, label="Owner")
    route2 = mo.ui.dropdown(options=ROUTE_OPTIONS, label="Owner")
    route3 = mo.ui.dropdown(options=ROUTE_OPTIONS, label="Owner")
    route4 = mo.ui.dropdown(options=ROUTE_OPTIONS, label="Owner")
    route5 = mo.ui.dropdown(options=ROUTE_OPTIONS, label="Owner")
    route6 = mo.ui.dropdown(options=ROUTE_OPTIONS, label="Owner")
    _widgets = [route1, route2, route3, route4, route5, route6]
    _items = []
    for _i, _s in enumerate(ROUTE_SCENARIOS):
        _items.append(mo.md(f"**Scenario {_i + 1}.** {_s['text']}"))
        _items.append(_widgets[_i])
    mo.vstack(_items)
    return route1, route2, route3, route4, route5, route6


@app.cell
def _(
    OWNER_NOTES,
    ROUTE_SCENARIOS,
    mo,
    route1,
    route2,
    route3,
    route4,
    route5,
    route6,
):
    _picks = [
        route1.value,
        route2.value,
        route3.value,
        route4.value,
        route5.value,
        route6.value,
    ]
    _items = []
    for _i, (_s, _p) in enumerate(zip(ROUTE_SCENARIOS, _picks)):
        if _p is None:
            _items.append(
                mo.callout(
                    mo.md(
                        f"**Scenario {_i + 1}.** Pick an owner above to see "
                        "the routing."
                    ),
                    kind="neutral",
                )
            )
        elif _p == _s["answer"]:
            _items.append(
                mo.callout(
                    mo.md(f"**Scenario {_i + 1}: correct.** {_s['why']}"),
                    kind="success",
                )
            )
        else:
            _items.append(
                mo.callout(
                    mo.md(
                        f"**Scenario {_i + 1}: reconsider.** "
                        f"{OWNER_NOTES[_p]} {_s['why']}"
                    ),
                    kind="warn",
                )
            )
    mo.vstack(_items)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The artifact: the project charter

        Every track in this course produces one artifact for the implementation plan; the capstone collects them. Track 1's artifact is the **project charter**: the one-page document that establishes what the project is, who authorized it, and how its decisions route. A charter is signed before detailed planning starts, because every later artifact (the timeline, the budget, the KPI dashboard) inherits its scope and governance path from this page.

        The charter for the RA-CDS, worked:

        | Field | Entry |
        |---|---|
        | **Purpose** | Reduce the delay between a rising flare risk and a treatment-escalation conversation for RA patients at Helios Academic Medical Center, by presenting a patient-view CDS card when the predicted 90-day flare probability exceeds 0.30. |
        | **Scope** | The 1,247-patient rheumatology RA panel at the academic medical center. One hook (patient-view), one card (schedule a treatment-escalation conversation). Out of scope: other departments, other hooks, automated ordering. Extension requests route to IT Steering. |
        | **Sponsor** | The CMIO. |
        | **Stakeholders** | Rheumatology department (clinical owner); informatics director and EHR analysts (build); clinical data scientist (model validation and monitoring); health IT (integration engine, infrastructure); P&T (consulted on the intensification recommendation); Quality & Safety (harm monitoring); finance (budget). |
        | **Governance and approval path** | AI Governance Committee: model approval (granted) and any future model or threshold change. EMR Optimization Committee: card design and alert standards. Rheumatology: clinical sign-off on logic and text. IT Steering: portfolio slot and any scope extension. Quality & Safety: silent-mode validation report and post-launch harm monitoring. |
        | **Success criteria** | Full launch to all rheumatologists at month 6. Local validation completed in silent mode before any card displays. Alert logic and card text carry rheumatology sign-off. Measurable performance targets (firing rate, override rate, action rate) defined before launch; Track 4 builds them. No unresolved harm signal at launch. |

        The capstone collects this charter as section 1 of the implementation plan. Tracks 2 through 8 fill in what the charter only names: the timeline behind "month 6," the budget behind the stakeholder list, the KPIs behind the success criteria.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Where this goes next

        The charter commits you to a six-month delivery without saying how the six months are spent. Track 02 builds the plan: the process groups, the methodology choice (the RA-CDS runs waterfall, Scrum, and Kanban at once, each where it fits), the Gantt chart with its critical path, and the RACI matrix that turns the role descriptions above into accountability.
        """
    )
    return


if __name__ == "__main__":
    app.run()
