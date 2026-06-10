"""Capstone for course 16: the RA-CDS implementation plan.

Building capstone. The reader assembles the eight track artifacts
(project charter, RACI matrix, six-month timeline, change-management
plan, KPI dashboard, budget and 5-year ROI, executive-pitch summary,
strategic-alignment statement, post-go-live operations plan) plus a new
risk register into the implementation plan they would hand the CMIO.
Outputs: the full plan and a derived one-page executive summary, each
downloadable as Markdown.

WASM-safe: no shared imports, no data files, no network calls.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd

    import marimo as mo
    return mo, pd


@app.cell
def _():
    DEFAULTS = {
        "purpose": "Reduce the delay between a rising flare risk and a treatment-escalation conversation for RA patients at Helios Academic Medical Center, by presenting a patient-view CDS card when the predicted 90-day flare probability exceeds 0.30.",
        "scope": "The 1,247-patient rheumatology RA panel at Helios Academic Medical Center. One hook (patient-view), one card (schedule a treatment-escalation conversation). Out of scope: other departments, other hooks, automated ordering. Extension requests route to IT Steering.",
        "sponsor": "The CMIO.",
        "stakeholders": "Rheumatology department (clinical owner); informatics director and EHR analysts (build); clinical data scientist (model validation and monitoring); health IT (integration engine, infrastructure); P&T (consulted on the intensification recommendation); Quality & Safety (harm monitoring); finance (budget).",
        "governance": "AI Governance Committee: model approval (granted) and any future model or threshold change. EMR Optimization Committee: card design and alert standards. Rheumatology: clinical sign-off on logic and text. IT Steering: portfolio slot and any scope extension. Quality & Safety: silent-mode validation report and post-launch harm monitoring.",
        "success": "Full launch to all rheumatologists at month 6. Local validation completed in silent mode before any card displays. Alert logic and card text carry rheumatology sign-off. Measurable targets for firing rate, override rate, and action rate defined before launch (section 5 sets them). No unresolved harm signal at launch.",
        "raci": (
            "| Activity | You (the informaticist) | CMIO | EHR analyst | Rheumatology chief | AI Governance Committee |\n"
            "|---|---|---|---|---|---|\n"
            "| Write and validate the alert logic | A, R | I | C | C | C |\n"
            "| Build the EHR integration | A | I | R | | I |\n"
            "| Design the card text | R | I | C | A | I |\n"
            "| Train the rheumatologists | A, R | I | | C | |\n"
            "| Monitor post-launch performance | A, R | I | R | I | C |\n\n"
            "Validation rules: exactly one A per activity; every A has at least one R; the CMIO is never R for build tasks. A blank cell means no involvement."
        ),
        "timeline": (
            "| Month | Milestone |\n"
            "|---|---|\n"
            "| 1 | Clinical content review (rheumatology sign-off on alert logic and card text) |\n"
            "| 2-3 | Technical build (CDS Hooks service integration, EHR build) |\n"
            "| 4 | Validation testing (silent mode: alert computes but does not display) |\n"
            "| 5 | User training + soft launch (5 rheumatologists) |\n"
            "| 6 | Full launch (all rheumatologists) |\n\n"
            "Dependency chain: review precedes build; build precedes validation; validation precedes training and the soft launch; the soft launch precedes full launch. Methodology: hybrid. Waterfall for the EHR integration build, Scrum sprints for validation and tuning, Kanban for the post-launch optimization queue (section 9)."
        ),
        "change": (
            "1. Urgency: a third to a half of RA patients with moderate or high disease activity leave the qualifying visit without escalation. Ms. Reyes's CRP run-up to 36.2 mg/L is the local instance.\n"
            "2. Coalition: the rheumatology chief, the EMR optimization lead, and one respected skeptic from the department.\n"
            "3. Vision: flare risk is acted on at the visit where the data justify it, instead of being discovered at the next one.\n"
            "4. Communication: through the chief at the department meeting, not by informaticist email.\n"
            "5. Barrier removal: the two-click scheduling path from the patient-view card.\n"
            "6. Short-term wins: accepted cards that become escalation visits during the month 5 soft launch (5 rheumatologists), reported weekly.\n"
            "7. Sustained acceleration: the month 6 full launch, with soft-launch users as peer references.\n"
            "8. Anchoring: the alert is part of the standard visit workflow, fellow onboarding covers it, and the override-rate review is a standing department-meeting item.\n\n"
            "Readiness cover sheet: clinical champion buy-in, training plan completeness, workflow fit, sustainment plan, and equity considerations, each scored 1 to 5. Below 15: do not launch. 15 to 19: soft launch with monitoring. 20 to 25: ready to deploy. Overrides are investigated before any retuning; retuning requests route through the AI Governance Committee."
        ),
        "kpi_targets": (
            "| KPI | Type | Timing | Target | Display |\n"
            "|---|---|---|---|---|\n"
            "| Alert override rate | Process | Leading | Within the 50 to 70% band | Weekly control chart |\n"
            "| Percentage of alerts acted on | Process | Leading | 40% or higher | Weekly run chart |\n"
            "| Median days from alert to escalation conversation | Process | Leading | 14 days or fewer | Monthly run chart |\n"
            "| Treat-to-target intensification within 90 days | Process | Leading | 50% or more of eligible patients | Quarterly run chart |\n"
            "| 90-day flare rate among alerted patients | Outcome | Lagging | Below matched pre-launch baseline by month 12 | Quarterly control chart |\n"
            "| Rheumatologist satisfaction with the alert | Outcome | Leading | 3.5 of 5 or higher | Quarterly survey trend |\n\n"
            "Display rule: every number appears as a time series with center line and limits. Footer: data lineage and owner named on the page."
        ),
        "ask": "Endorse the ongoing operating commitment of about $60K per year for the RA flare-risk alert. The $240K one-time build is already committed through the IT Steering portfolio process; the board is not asked to approve capital or the deployment.",
        "evidence": "About 31 moderate-to-severe flares averted per year across the 1,247-patient Helios RA panel, at $4K to $6K of added utilization per flare. Annual gross benefit about $155K against $60K operating; break-even near month 31; five-year NPV about $195K at the 3% discount rate. One patient sentence: a CRP run-up like Ms. Reyes's 36.2 mg/L, caught at chart open instead of at the next routine visit.",
        "risk": "Adoption. At a peer system, 47% of rheumatologists dismiss a similar alert every time it fires. Mitigation: the month 5 champion-led soft launch with 5 rheumatologists, the override rate on the monthly dashboard, and a deactivation trigger owned by the AI Governance Committee.",
        "strategy": (
            "Mission link: the RA-CDS advances Helios's outcomes-and-value priorities. Earlier treatment escalation in active RA reduces uncontrolled flares (outcomes) and avoids $4K to $6K of utilization per flare averted (value), within treat-to-target care.\n"
            "SWOT position: builds on strengths (a mature EHR build team, working governance committees), exploits opportunities (reusable CDS Hooks infrastructure, payer quality bonuses for documented treat-to-target care), and manages one named threat: the alert adds to alert load, so override-rate monitoring and a retuning path are part of the commitment.\n"
            "Capital-cycle timing: the $240K one-time cost was approved in last fall's capital cycle and releases July 1; the $60K per year ongoing cost enters the operating budget at go-live; first portfolio review at IT Steering 12 months after launch, with the override-rate and flare-aversion KPIs as performance evidence.\n"
            "Portfolio note: gastroenterology IBD reuse is the first extension candidate, pending IT Steering scoring at the next roadmap refresh."
        ),
        "ops": (
            "Command-center exit criteria: five consecutive business days with no Sev1 or Sev2; ticket arrival at or below about five per week and falling; all open tickets owned in the standard tiers with SLAs; at-the-elbow support withdrawn without a subsequent ticket spike; rheumatology clinical-lead sign-off; written handoff to standard support.\n"
            "Support tiers and SLAs: L1 help desk (80% first-contact resolution, 15-minute callback); L2 application analysts (acknowledgment within 4 business hours); L3 builders and vendor escalation (resolution targets by severity). Missed-SLA rates report monthly as a time series.\n"
            "Change control: standard, normal, and emergency change classes; freeze windows for go-live stabilization, the vendor quarterly upgrade window, and designated high-census periods. Any change to the 0.30 firing threshold, the input features, the cohort value set, or the model weights requires AI Governance Committee sign-off in addition to change-control board review.\n"
            "Downtime: fail silent. When the EHR cannot reach the CDS service, the chart opens without a card, never with a stale card. Service outages are Sev2 incidents with L3 root-cause ownership and a Quality & Safety replay of the gap using the month 4 silent-mode infrastructure. Institutional downtime follows the forms, read-only shadow, recovery sequence, and reconciliation procedure.\n"
            "Optimization queue: the Kanban queue with three intake sources (reclassified tickets, L1 frequency signals, the KPI dashboard), reviewed monthly with the rheumatology clinical lead. Threshold and model requests exit to AI Governance; cross-department extension requests exit to IT Steering."
        ),
    }

    KPI_TAGS = {
        "Alert override rate": ("process", "leading", True),
        "Percentage of alerts acted on": ("process", "leading", True),
        "Median days from alert to escalation conversation": ("process", "leading", True),
        "Treat-to-target intensification within 90 days (eligible patients)": ("process", "leading", True),
        "90-day flare rate among alerted patients": ("outcome", "lagging", True),
        "Rheumatologist satisfaction with the alert": ("outcome", "leading", True),
        "Alerts fired per week": ("process", "leading", True),
        "CDS service response time (p95)": ("process", "leading", True),
        "Alerts fired on patients without active RA": ("process", "leading", True),
        "Structured joint-count capture rate at rheumatology visits": ("process", "leading", True),
        "PROM completion rate on the RA panel": ("process", "leading", True),
        "Portal activation rate on the RA panel": ("process", "leading", True),
        "Rheumatologist training completion": ("process", "leading", True),
        "Mean DAS28 across the cohort": ("outcome", "lagging", True),
        "Moderate-to-severe disease-activity prevalence at 12 months": ("outcome", "lagging", True),
        "RA-flare ED visits and admissions per 100 patient-years": ("outcome", "lagging", True),
        "HCAHPS top-box communication score": ("outcome", "lagging", False),
        "30-day all-cause readmission rate": ("outcome", "lagging", False),
        "Hospital mortality O/E ratio": ("outcome", "lagging", False),
        "Average inpatient length of stay": ("outcome", "lagging", False),
    }
    KPI_OPTIONS = list(KPI_TAGS)
    KPI_REFERENCE = KPI_OPTIONS[:6]

    OWNER_OPTIONS = [
        "You (implementation lead)",
        "CMIO",
        "EHR analyst",
        "Rheumatology chief",
        "AI Governance Committee",
        "IT Steering Committee",
        "Quality & Safety Committee",
        "CIO / IT operations",
    ]
    LEVEL_SCORE = {"Low": 1, "Medium": 2, "High": 3}

    RISKS = [
        {"name": "Clinician rejection / alert fatigue", "like": "High", "imp": "High", "owner": "Rheumatology chief",
         "mit": "Champion-led month 5 soft launch; override rate on the weekly control chart; investigate before retuning."},
        {"name": "Model degradation on local data", "like": "Medium", "imp": "High", "owner": "AI Governance Committee",
         "mit": "Quarterly performance review against the month 4 silent-mode baseline; threshold and model changes gated by AI Governance."},
        {"name": "Integration-engine resource loss", "like": "Medium", "imp": "Medium", "owner": "CIO / IT operations",
         "mit": "Escalation through the CMIO when clinical priority conflicts with competing IT work; schedule slack in the month 2 to 3 build."},
        {"name": "Scope creep from other departments", "like": "High", "imp": "Medium", "owner": "IT Steering Committee",
         "mit": "Charter scope names one hook and one card; extension requests route to IT Steering, not to the build team."},
        {"name": "Training decay with staff turnover", "like": "Medium", "imp": "Medium", "owner": "You (implementation lead)",
         "mit": "Alert orientation in fellow onboarding; the override-rate review as a standing department-meeting item."},
        {"name": "Security or privacy incident", "like": "Low", "imp": "High", "owner": "CIO / IT operations",
         "mit": "The CDS service runs inside the Helios security boundary; incidents follow the institutional response plan (Course 22 covers the depth)."},
    ]
    return DEFAULTS, KPI_OPTIONS, KPI_REFERENCE, KPI_TAGS, LEVEL_SCORE, OWNER_OPTIONS, RISKS


@app.cell
def _(mo):
    mo.md(
        r"""
        # Capstone: Assemble the RA-CDS implementation plan

        The eight tracks of this course each produced one artifact for the RA-CDS deployment. This capstone assembles them, adds the one artifact no track built (the risk register), and produces the implementation plan you would hand the CMIO. Two documents come out of the notebook: the full plan and a one-page executive summary derived from your inputs, each downloadable as Markdown.

        Every field below arrives carrying the worked entry its track produced. Keep an entry, sharpen it, or replace it; the assembled plan at the bottom of the notebook updates with every edit. A field left untouched contributes its worked entry, so the plan is complete from the first render.
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
        ## Section 1: the project charter (Track 1)

        The charter establishes what the project is, who authorized it, and how its decisions route. Every later section inherits its scope and governance path from this page. Track 1 worked the six fields below; the charter deliberately defers the timeline detail to section 3, the budget to section 6, and the KPI targets to section 5.
        """
    )
    return


@app.cell
def _(DEFAULTS, mo):
    charter_purpose = mo.ui.text_area(label="Purpose", placeholder=DEFAULTS["purpose"], rows=3, full_width=True)
    charter_scope = mo.ui.text_area(label="Scope", placeholder=DEFAULTS["scope"], rows=3, full_width=True)
    charter_sponsor = mo.ui.text(label="Sponsor", placeholder=DEFAULTS["sponsor"], full_width=True)
    charter_stakeholders = mo.ui.text_area(label="Stakeholders", placeholder=DEFAULTS["stakeholders"], rows=4, full_width=True)
    charter_governance = mo.ui.text_area(label="Governance and approval path", placeholder=DEFAULTS["governance"], rows=4, full_width=True)
    charter_success = mo.ui.text_area(label="Success criteria", placeholder=DEFAULTS["success"], rows=4, full_width=True)
    mo.vstack([charter_purpose, charter_scope, charter_sponsor, charter_stakeholders, charter_governance, charter_success])
    return charter_governance, charter_purpose, charter_scope, charter_sponsor, charter_stakeholders, charter_success


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Section 2: the RACI matrix (Track 2)

        Five activities crossed with five roles. The validation rules from Track 2 hold: exactly one A per activity, every A has at least one R, and the CMIO is never R for build tasks. The matrix is editable as a Markdown table.
        """
    )
    return


@app.cell
def _(DEFAULTS, mo):
    raci_input = mo.ui.text_area(label="RACI matrix (Markdown table)", value=DEFAULTS["raci"], rows=11, full_width=True)
    raci_input
    return (raci_input,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Section 3: timeline and milestones (Track 2)

        The canonical six-month table, editable. The dependency chain and the hybrid methodology note travel with it: the go-live deadline anchors the end of month 6, so a slip anywhere on the chain costs scope, not time.
        """
    )
    return


@app.cell
def _(DEFAULTS, mo):
    timeline_input = mo.ui.text_area(label="Timeline and milestones (Markdown table)", value=DEFAULTS["timeline"], rows=12, full_width=True)
    timeline_input
    return (timeline_input,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Section 4: the change-management plan (Track 3)

        Kotter's eight steps applied to the RA-CDS, plus the readiness cover sheet from Track 3's assessment. The operational rule on overrides stands: resistance is information, so investigate before retuning.
        """
    )
    return


@app.cell
def _(DEFAULTS, mo):
    change_input = mo.ui.text_area(label="Change-management plan", placeholder=DEFAULTS["change"], rows=14, full_width=True)
    change_input
    return (change_input,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Section 5: the KPI dashboard (Track 4)

        Select 5 to 7 KPIs from the 20-item catalog. Four catalog entries are system-level distractors the RA-CDS cannot move. The targets table below the selector carries Track 4's reference dashboard; the display rule is the anti-tampering rule: every number appears as a time series with center line and limits, never as a bare number.
        """
    )
    return


@app.cell
def _(DEFAULTS, KPI_OPTIONS, KPI_REFERENCE, mo):
    kpi_select = mo.ui.multiselect(options=KPI_OPTIONS, value=KPI_REFERENCE, label="Dashboard KPIs (pick 5 to 7)", full_width=True)
    kpi_targets = mo.ui.text_area(label="Targets and display (Markdown table)", value=DEFAULTS["kpi_targets"], rows=12, full_width=True)
    mo.vstack([kpi_select, kpi_targets])
    return kpi_select, kpi_targets


@app.cell
def _(KPI_TAGS, kpi_select, mo):
    _sel = list(kpi_select.value)
    _notes = []
    if not _sel:
        _fb = mo.callout(mo.md("Select KPIs above to check the mix."), kind="neutral")
    else:
        _distractors = [_k for _k in _sel if not KPI_TAGS[_k][2]]
        _types = {KPI_TAGS[_k][0] for _k in _sel}
        _timings = {KPI_TAGS[_k][1] for _k in _sel}
        if len(_sel) < 5 or len(_sel) > 7:
            _notes.append(f"A one-page dashboard holds 5 to 7 KPIs; {len(_sel)} selected.")
        if _distractors:
            _notes.append("Not attributable to the RA-CDS: " + "; ".join(_distractors) + ". These are system-level measures the alert cannot move.")
        if _types == {"process"}:
            _notes.append("All process measures: the CMO sees activity, not impact. Add at least one outcome.")
        if "leading" not in _timings:
            _notes.append("No leading indicator: the dashboard gives no early warning before the lagging outcomes mature around month 9.")
        if _notes:
            _fb = mo.callout(mo.md("**Check the mix.** " + " ".join(_notes)), kind="warn")
        else:
            _fb = mo.callout(
                mo.md("**Workable selection.** Size fits a one-pager, every KPI is attributable, and the mix carries both process and outcome with at least one leading indicator."),
                kind="success",
            )
    _fb
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Section 6: budget and 5-year ROI (Track 5)

        The canonical money facts at their defaults reproduce Track 5's computed outputs: 5-year NPV about $195K, discounted 5-year ROI about 38% (PV benefits minus PV costs, over PV costs), payback near month 32 after go-live. Year 0 is the build year (one-time cost, no benefit); benefits begin in year 1 and run through year 5. Track 5's build-vs-buy comparison travels with the budget as a note in the assembled plan: a hypothetical vendor flare-risk module totals $435K over five years ($150K license, $30K per year maintenance, $60K integration and validation, $15K per year internal monitoring) against the build's $540K TCO, and the residual difference buys threshold and retuning control.
        """
    )
    return


@app.cell
def _(mo):
    budget_onetime = mo.ui.number(start=100_000, stop=500_000, step=10_000, value=240_000, label="One-time implementation cost ($)")
    budget_annual = mo.ui.number(start=20_000, stop=150_000, step=5_000, value=60_000, label="Annual ongoing cost ($)")
    budget_alerted = mo.ui.slider(start=100, stop=600, step=10, value=310, label="Patients alerted per year", show_value=True)
    budget_acted = mo.ui.slider(start=10, stop=80, step=5, value=40, label="Percent of alerts acted on", show_value=True)
    budget_averted = mo.ui.slider(start=5, stop=50, step=5, value=25, label="Flares averted per 100 acted-on alerts", show_value=True)
    budget_flare_cost = mo.ui.slider(start=4_000, stop=6_000, step=250, value=5_000, label="Cost per flare averted ($)", show_value=True)
    budget_discount = mo.ui.slider(start=0.0, stop=7.0, step=0.5, value=3.0, label="Discount rate (%)", show_value=True)
    mo.vstack(
        [
            mo.hstack([budget_onetime, budget_annual], justify="start", gap=2),
            budget_alerted,
            budget_acted,
            budget_averted,
            budget_flare_cost,
            budget_discount,
        ]
    )
    return budget_acted, budget_alerted, budget_annual, budget_averted, budget_discount, budget_flare_cost, budget_onetime


@app.cell
def _(budget_acted, budget_alerted, budget_annual, budget_averted, budget_discount, budget_flare_cost, budget_onetime, mo):
    _flares = budget_alerted.value * (budget_acted.value / 100) * (budget_averted.value / 100)
    _benefit = _flares * budget_flare_cost.value
    _r = budget_discount.value / 100
    _pv_benefits = sum(_benefit / (1 + _r) ** _t for _t in range(1, 6))
    _pv_costs = budget_onetime.value + sum(budget_annual.value / (1 + _r) ** _t for _t in range(1, 6))
    _npv = _pv_benefits - _pv_costs
    _roi = _npv / _pv_costs if _pv_costs else 0.0
    _cum = -float(budget_onetime.value)
    _payback = None
    for _t in range(1, 6):
        _net = (_benefit - budget_annual.value) / (1 + _r) ** _t
        if _payback is None and _net > 0 and _cum + _net >= 0:
            _payback = round(12 * ((_t - 1) + (-_cum) / _net))
        _cum += _net
    _payback_text = f"month {_payback} after go-live" if _payback else "beyond month 60 at these inputs"
    roi_facts = {
        "onetime": f"${budget_onetime.value:,.0f}",
        "annual": f"${budget_annual.value:,.0f}",
        "tco": f"${budget_onetime.value + 5 * budget_annual.value:,.0f}",
        "alerted": f"{budget_alerted.value:.0f}",
        "acted": f"{budget_acted.value:.0f}%",
        "averted": f"{budget_averted.value:.0f}",
        "flare_cost": f"${budget_flare_cost.value:,.0f}",
        "flares": f"{_flares:.0f}",
        "benefit": f"${_benefit:,.0f}",
        "discount": f"{budget_discount.value:g}%",
        "npv": f"${_npv:,.0f}",
        "roi": f"{_roi * 100:.0f}%",
        "payback": _payback_text,
    }
    mo.callout(
        mo.md(
            f"At these inputs: {roi_facts['flares']} flares averted per year, {roi_facts['benefit']} annual gross benefit, "
            f"5-year NPV {roi_facts['npv']}, discounted 5-year ROI {roi_facts['roi']}, payback at {roi_facts['payback']}."
        ),
        kind="neutral",
    )
    return (roi_facts,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Section 7: the executive-pitch summary (Track 6)

        Three slides for the Board of Trustees, BLUF order: the ask is slide 1, not slide 3. The evidence slide carries the benefit model and one patient sentence; the risk slide names adoption and its mitigation, because a risk slide that says "no risks" destroys credibility.
        """
    )
    return


@app.cell
def _(DEFAULTS, mo):
    pitch_ask = mo.ui.text_area(label="Slide 1: the ask", placeholder=DEFAULTS["ask"], rows=3, full_width=True)
    pitch_evidence = mo.ui.text_area(label="Slide 2: the evidence", placeholder=DEFAULTS["evidence"], rows=4, full_width=True)
    pitch_risk = mo.ui.text_area(label="Slide 3: the risk", placeholder=DEFAULTS["risk"], rows=3, full_width=True)
    mo.vstack([pitch_ask, pitch_evidence, pitch_risk])
    return pitch_ask, pitch_evidence, pitch_risk


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Section 8: strategic alignment (Track 7)

        The RA-CDS was one of 14 requests at the winter IT Steering meeting and won its funding on strategic alignment, not technical merit. The statement records the mission link, the SWOT position, and the capital-cycle timing; the dropdown records the portfolio category in the run / grow / transform taxonomy.
        """
    )
    return


@app.cell
def _(DEFAULTS, mo):
    strat_statement = mo.ui.text_area(label="Strategic-alignment statement", placeholder=DEFAULTS["strategy"], rows=10, full_width=True)
    strat_category = mo.ui.dropdown(options=["Run", "Grow", "Transform"], value="Grow", label="Portfolio category")
    mo.vstack([strat_statement, strat_category])
    return strat_category, strat_statement


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Section 9: the post-go-live operations plan (Track 8)

        Five fields: command-center exit criteria, support tiers and SLAs, change-control rules (including the AI Governance gate on any model-behavior change), downtime procedures (the fail-silent commitment), and the optimization-queue cadence. The project ends at month 6; this section is what runs afterward.
        """
    )
    return


@app.cell
def _(DEFAULTS, mo):
    ops_input = mo.ui.text_area(label="Post-go-live operations plan", placeholder=DEFAULTS["ops"], rows=16, full_width=True)
    ops_input
    return (ops_input,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Section 10: the risk register (new in this capstone)

        No track built this artifact; every track named risks. The register scores each risk as likelihood times impact (low = 1, medium = 2, high = 3) and assigns one owner. Six risks are predefined with their mitigations on file; the ranked table below the controls re-sorts as you score. Add a seventh risk of your own: a register that only contains the risks someone else predicted is not yet yours.
        """
    )
    return


@app.cell
def _(OWNER_OPTIONS, RISKS, mo):
    def _lik(_v):
        return mo.ui.dropdown(options=["Low", "Medium", "High"], value=_v, label="Likelihood")

    def _impd(_v):
        return mo.ui.dropdown(options=["Low", "Medium", "High"], value=_v, label="Impact")

    def _ownd(_v):
        return mo.ui.dropdown(options=OWNER_OPTIONS, value=_v, label="Owner")

    r1_like, r1_imp, r1_own = _lik(RISKS[0]["like"]), _impd(RISKS[0]["imp"]), _ownd(RISKS[0]["owner"])
    r2_like, r2_imp, r2_own = _lik(RISKS[1]["like"]), _impd(RISKS[1]["imp"]), _ownd(RISKS[1]["owner"])
    r3_like, r3_imp, r3_own = _lik(RISKS[2]["like"]), _impd(RISKS[2]["imp"]), _ownd(RISKS[2]["owner"])
    r4_like, r4_imp, r4_own = _lik(RISKS[3]["like"]), _impd(RISKS[3]["imp"]), _ownd(RISKS[3]["owner"])
    r5_like, r5_imp, r5_own = _lik(RISKS[4]["like"]), _impd(RISKS[4]["imp"]), _ownd(RISKS[4]["owner"])
    r6_like, r6_imp, r6_own = _lik(RISKS[5]["like"]), _impd(RISKS[5]["imp"]), _ownd(RISKS[5]["owner"])
    _controls = [
        (r1_like, r1_imp, r1_own),
        (r2_like, r2_imp, r2_own),
        (r3_like, r3_imp, r3_own),
        (r4_like, r4_imp, r4_own),
        (r5_like, r5_imp, r5_own),
        (r6_like, r6_imp, r6_own),
    ]
    _rows = []
    for _i, (_risk, _trio) in enumerate(zip(RISKS, _controls), start=1):
        _rows.append(mo.md(f"**Risk {_i}: {_risk['name']}.** Mitigation on file: {_risk['mit']}"))
        _rows.append(mo.hstack(list(_trio), justify="start", gap=2))
    mo.vstack(_rows)
    return (
        r1_imp, r1_like, r1_own,
        r2_imp, r2_like, r2_own,
        r3_imp, r3_like, r3_own,
        r4_imp, r4_like, r4_own,
        r5_imp, r5_like, r5_own,
        r6_imp, r6_like, r6_own,
    )


@app.cell
def _(OWNER_OPTIONS, mo):
    risk7_name = mo.ui.text(
        label="Risk 7: your seventh risk",
        placeholder="Example: CRP result latency from the regional reference lab delays the trajectory feature for about 8% of panel visits.",
        full_width=True,
    )
    risk7_like = mo.ui.dropdown(options=["Low", "Medium", "High"], value="Medium", label="Likelihood")
    risk7_imp = mo.ui.dropdown(options=["Low", "Medium", "High"], value="Medium", label="Impact")
    risk7_own = mo.ui.dropdown(options=OWNER_OPTIONS, value="You (implementation lead)", label="Owner")
    mo.vstack([risk7_name, mo.hstack([risk7_like, risk7_imp, risk7_own], justify="start", gap=2)])
    return risk7_imp, risk7_like, risk7_name, risk7_own


@app.cell
def _(
    LEVEL_SCORE,
    RISKS,
    mo,
    pd,
    r1_imp, r1_like, r1_own,
    r2_imp, r2_like, r2_own,
    r3_imp, r3_like, r3_own,
    r4_imp, r4_like, r4_own,
    r5_imp, r5_like, r5_own,
    r6_imp, r6_like, r6_own,
    risk7_imp, risk7_like, risk7_name, risk7_own,
):
    _controls = [
        (r1_like, r1_imp, r1_own),
        (r2_like, r2_imp, r2_own),
        (r3_like, r3_imp, r3_own),
        (r4_like, r4_imp, r4_own),
        (r5_like, r5_imp, r5_own),
        (r6_like, r6_imp, r6_own),
    ]
    _entries = []
    for _risk, (_l, _m, _o) in zip(RISKS, _controls):
        _entries.append({"Risk": _risk["name"], "Likelihood": _l.value, "Impact": _m.value, "Owner": _o.value, "Mitigation": _risk["mit"]})
    if risk7_name.value.strip():
        _entries.append({
            "Risk": risk7_name.value.strip(),
            "Likelihood": risk7_like.value,
            "Impact": risk7_imp.value,
            "Owner": risk7_own.value,
            "Mitigation": "Define with the owner before go-live.",
        })
    for _e in _entries:
        _e["Score"] = LEVEL_SCORE[_e["Likelihood"]] * LEVEL_SCORE[_e["Impact"]]
    _entries.sort(key=lambda _e: (-_e["Score"], -LEVEL_SCORE[_e["Likelihood"]]))
    top_risk = _entries[0]["Risk"]
    top_risk_owner = _entries[0]["Owner"]
    top_risk_mit = _entries[0]["Mitigation"]
    _df = pd.DataFrame(_entries, columns=["Risk", "Likelihood", "Impact", "Score", "Owner", "Mitigation"])
    _df.index = range(1, len(_df) + 1)
    _df.index.name = "rank"
    _header = "| Rank | Risk | Likelihood | Impact | Score | Owner | Mitigation |\n|---|---|---|---|---|---|---|"
    _md_rows = "\n".join(
        f"| {_i} | {_e['Risk']} | {_e['Likelihood']} | {_e['Impact']} | {_e['Score']} | {_e['Owner']} | {_e['Mitigation']} |"
        for _i, _e in enumerate(_entries, start=1)
    )
    risk_md = _header + "\n" + _md_rows
    mo.vstack(
        [
            mo.md("The register, ranked by score. The top row is the risk the plan spends its mitigation attention on first."),
            _df,
        ]
    )
    return risk_md, top_risk, top_risk_mit, top_risk_owner


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The assembled implementation plan

        The document below collects all ten sections. It updates with every edit above and downloads as `ra-cds-implementation-plan.md`.
        """
    )
    return


@app.cell
def _(
    DEFAULTS,
    KPI_REFERENCE,
    KPI_TAGS,
    change_input,
    charter_governance,
    charter_purpose,
    charter_scope,
    charter_sponsor,
    charter_stakeholders,
    charter_success,
    kpi_select,
    kpi_targets,
    mo,
    ops_input,
    pitch_ask,
    pitch_evidence,
    pitch_risk,
    raci_input,
    risk_md,
    roi_facts,
    strat_category,
    strat_statement,
    timeline_input,
):
    _purpose = charter_purpose.value or DEFAULTS["purpose"]
    _scope = charter_scope.value or DEFAULTS["scope"]
    _sponsor = charter_sponsor.value or DEFAULTS["sponsor"]
    _stakeholders = charter_stakeholders.value or DEFAULTS["stakeholders"]
    _governance = charter_governance.value or DEFAULTS["governance"]
    _success = charter_success.value or DEFAULTS["success"]
    _raci = raci_input.value or DEFAULTS["raci"]
    _timeline = timeline_input.value or DEFAULTS["timeline"]
    _change = change_input.value or DEFAULTS["change"]
    _kpis = list(kpi_select.value) or KPI_REFERENCE
    _kpi_bullets = "\n".join(f"- {_k} ({KPI_TAGS[_k][0]}, {KPI_TAGS[_k][1]})" for _k in _kpis)
    _targets = kpi_targets.value or DEFAULTS["kpi_targets"]
    _ask = pitch_ask.value or DEFAULTS["ask"]
    _evidence = pitch_evidence.value or DEFAULTS["evidence"]
    _risk = pitch_risk.value or DEFAULTS["risk"]
    _strategy = strat_statement.value or DEFAULTS["strategy"]
    _ops = ops_input.value or DEFAULTS["ops"]
    plan = f"""# RA-CDS implementation plan: Helios Academic Medical Center

_Prepared for the CMIO by the implementation lead. RA flare-risk alert: patient-view hook, 0.30 firing threshold, 90-day flare window, 1,247-patient rheumatology RA panel, six-month go-live._

## 1. Project charter

- **Purpose.** {_purpose}
- **Scope.** {_scope}
- **Sponsor.** {_sponsor}
- **Stakeholders.** {_stakeholders}
- **Governance and approval path.** {_governance}
- **Success criteria.** {_success}

## 2. RACI matrix

{_raci}

## 3. Timeline and milestones

{_timeline}

## 4. Change-management plan

{_change}

## 5. KPI dashboard

{_kpi_bullets}

{_targets}

## 6. Budget and 5-year ROI

- One-time implementation cost: {roi_facts['onetime']}
- Annual ongoing cost: {roi_facts['annual']}
- 5-year TCO: {roi_facts['tco']}
- Benefit model: {roi_facts['alerted']} patients alerted per year; {roi_facts['acted']} of alerts acted on; {roi_facts['averted']} flares averted per 100 acted-on alerts; {roi_facts['flare_cost']} per flare averted.
- Annual gross benefit: {roi_facts['benefit']} ({roi_facts['flares']} flares averted per year).
- Computed at a {roi_facts['discount']} discount rate (year 0 is the build year; benefits run years 1 through 5): 5-year NPV {roi_facts['npv']}; discounted 5-year ROI {roi_facts['roi']} (PV benefits minus PV costs, over PV costs); payback at {roi_facts['payback']}.
- Build vs buy: a hypothetical vendor flare-risk module totals $435K over five years against the build's {roi_facts['tco']} TCO at the inputs above. The residual difference buys control: AI Governance owns the firing threshold and the retuning calendar on the built system.

## 7. Executive-pitch summary (3 slides)

- **Slide 1, the ask.** {_ask}
- **Slide 2, the evidence.** {_evidence}
- **Slide 3, the risk.** {_risk}

## 8. Strategic alignment

**Portfolio category:** {strat_category.value}.

{_strategy}

## 9. Post-go-live operations plan

{_ops}

## 10. Risk register

Scoring: likelihood times impact; low = 1, medium = 2, high = 3.

{risk_md}

---

_Generated from the Course 16 capstone notebook. This plan assembles the eight track artifacts of Course 16 plus the risk register into the deliverable the CMIO's email asked for: the document an implementation team could execute._
"""
    mo.md(plan)
    return (plan,)


@app.cell
def _(mo, plan):
    plan_download = mo.download(
        data=plan.encode("utf-8"),
        filename="ra-cds-implementation-plan.md",
        label="Download the implementation plan as Markdown",
    )
    plan_download
    return (plan_download,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The one-page executive summary

        Derived automatically from the ask, the charter purpose, the budget computation, the KPI selection, and the top-ranked risk. BLUF order: the executive who stops after the first line still has the ask. It downloads separately as `ra-cds-implementation-plan-executive-summary.md`.
        """
    )
    return


@app.cell
def _(DEFAULTS, KPI_REFERENCE, RISKS, charter_purpose, kpi_select, mo, pitch_ask, pitch_risk, roi_facts, top_risk, top_risk_mit, top_risk_owner):
    _ask = pitch_ask.value or DEFAULTS["ask"]
    _purpose = charter_purpose.value or DEFAULTS["purpose"]
    _risk = pitch_risk.value or DEFAULTS["risk"]
    if top_risk == RISKS[0]["name"]:
        _top_text = _risk
    else:
        _top_text = f"Owner: {top_risk_owner}. Mitigation on file: {top_risk_mit}"
    _kpis = list(kpi_select.value) or KPI_REFERENCE
    _lead_kpis = "; ".join(_kpis[:3])
    exec_summary = f"""# RA-CDS implementation plan: executive summary

**Bottom line.** {_ask}

**What.** {_purpose} Go-live is six months out: clinical content review in month 1, technical build in months 2 to 3, silent-mode validation in month 4, training and a 5-rheumatologist soft launch in month 5, full launch in month 6.

**So what.** {roi_facts['flares']} moderate-to-severe flares averted per year across the 1,247-patient panel at {roi_facts['flare_cost']} per flare. Annual gross benefit {roi_facts['benefit']} against {roi_facts['annual']} ongoing cost; 5-year NPV {roi_facts['npv']} at a {roi_facts['discount']} discount rate; discounted 5-year ROI {roi_facts['roi']}; payback at {roi_facts['payback']}.

**Now what.** Performance reports on {len(_kpis)} KPIs, led by: {_lead_kpis}. Every number displays as a time series with center line and limits. First portfolio review at IT Steering 12 months after launch.

**Top risk.** {top_risk}. {_top_text}

---

_Generated from the Course 16 capstone notebook. One page, BLUF-structured, derived from the implementation plan above._
"""
    mo.md(exec_summary)
    return (exec_summary,)


@app.cell
def _(exec_summary, mo):
    exec_download = mo.download(
        data=exec_summary.encode("utf-8"),
        filename="ra-cds-implementation-plan-executive-summary.md",
        label="Download the executive summary as Markdown",
    )
    exec_download
    return (exec_download,)


@app.cell
def _(mo):
    reflection = mo.ui.text_area(
        label="Which section of this plan are you least confident in, and what would you want to learn before handing it to a real CMIO?",
        rows=5,
        full_width=True,
    )
    mo.vstack(
        [
            mo.md(
                r"""
                ## Closing reflection

                Nothing is revealed after this answer; writing it is the point.
                """
            ),
            reflection,
        ]
    )
    return (reflection,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Where this sits in the curriculum

        Course 16 closes the working-informaticist arc. Courses 0 through 15 built the technical and analytic competencies; this course turned them into the job: leading a deployment from charter to day-2 operations. The implementation plan above is the artifact of that turn, the way the Course 12 design brief was the artifact of the technical arc.

        The remaining courses extend specific operational threads. Course 17 treats the workflow, safety, and human-factors discipline behind sections 4 and 9 at depth. Course 18 widens the panel view behind the 1,247-patient registry to population health. Course 19 covers the patient-facing data the alert's cohort will increasingly draw on. Course 21 covers the ancillary systems the integration engine connects. Course 22 covers the security operations behind risk 6.
        """
    )
    return


if __name__ == "__main__":
    app.run()
