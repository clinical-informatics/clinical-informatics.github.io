"""Track 07: Strategic planning and IT portfolio management.

Why the RA-CDS won its funding quarter. The track traces an IT request
from institutional mission and vision through SWOT, the multi-year
roadmap, the capital-cycle calendar, and the run/grow/transform
portfolio view, with a reactive portfolio-prioritization matrix over
eight synthetic Helios initiatives. The artifact is the
strategic-alignment statement the capstone collects as section 8 of
the implementation plan.

WASM-safe: no shared imports, no data files, all data inline.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import pandas as pd

    INITIATIVES = [
        {
            "initiative": "RA flare-risk CDS implementation (your request)",
            "label": "RA-CDS",
            "category": "Grow",
            "value": 8,
            "effort": 5,
            "risk_reduction": 3,
            "capital_k": 240,
        },
        {
            "initiative": "ED sepsis alert refresh (retuning, value-set update)",
            "label": "Sepsis refresh",
            "category": "Run",
            "value": 6,
            "effort": 3,
            "risk_reduction": 5,
            "capital_k": 120,
        },
        {
            "initiative": "RA registry expansion to the three community partners",
            "label": "Registry",
            "category": "Grow",
            "value": 6,
            "effort": 4,
            "risk_reduction": 2,
            "capital_k": 180,
        },
        {
            "initiative": "Patient-portal self-scheduling module",
            "label": "Portal scheduling",
            "category": "Grow",
            "value": 7,
            "effort": 6,
            "risk_reduction": 2,
            "capital_k": 400,
        },
        {
            "initiative": "Data-warehouse migration (on-prem CDW to cloud)",
            "label": "DW migration",
            "category": "Transform",
            "value": 9,
            "effort": 9,
            "risk_reduction": 4,
            "capital_k": 1500,
        },
        {
            "initiative": "Ambient-documentation pilot (two clinics)",
            "label": "Ambient doc",
            "category": "Transform",
            "value": 7,
            "effort": 7,
            "risk_reduction": 2,
            "capital_k": 350,
        },
        {
            "initiative": "Pharmacy IV-workflow system replacement",
            "label": "Pharmacy IV",
            "category": "Run",
            "value": 5,
            "effort": 6,
            "risk_reduction": 7,
            "capital_k": 600,
        },
        {
            "initiative": "Security hardening program (MFA everywhere, PAM)",
            "label": "Security program",
            "category": "Run",
            "value": 6,
            "effort": 5,
            "risk_reduction": 10,
            "capital_k": 450,
        },
    ]
    return INITIATIVES, alt, mo, pd


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 07: Strategic planning and IT portfolio management

        The IT Steering Committee at Helios Academic Medical Center meets quarterly. At the winter meeting, four months before the CMIO's congratulations email, your RA flare-risk CDS was one of 14 funding requests on the agenda: alert projects, infrastructure migrations, module purchases, a security program. The committee funded some, deferred others, and killed two. The RA-CDS won.

        It won on strategic alignment, not technical merit. The AI Governance Committee had already judged the model; IT Steering judges whether a request advances the institution's stated mission, where it sits in the IT portfolio, and whether its money arrives through the right cycle at the right time. This track reconstructs how the RA-CDS won, and what the same machinery does to the requests that lose.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            **The running scenario.** In the Course 12 capstone you produced a CDS design brief for an RA flare-risk alert. At chart open (the `patient-view` CDS Hook), for patients with active rheumatoid arthritis, when the recent CRP trajectory and clinical context put the probability of a flare in the next 90 days above the 0.30 firing threshold, a card suggests scheduling a treatment-escalation conversation rather than waiting for the next routine visit. The AI Governance Committee approved the brief, and this morning the CMIO's email made you the implementation lead with go-live six months out. The rheumatology panel holds 1,247 patients with RA. Ms. Reyes is one of them: her CRP run-up to 36.2 mg/L before adalimumab started is exactly the trajectory the alert exists to catch.
            """
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Mission, vision, and why an IT request must trace to them

        A mission statement says what the institution exists to do. A vision statement says what it intends to become. Helios states its mission as measurably improving the health of the communities it serves through outstanding care, discovery, and education, and its current strategic plan commits the system to two headline priorities: clinical outcomes that can be demonstrated, and value, meaning the cost at which those outcomes are delivered.

        IT strategy is not a separate strategy. Every durable IT plan is a derivation: the institution's mission and strategic priorities at the top, the IT capabilities that serve them in the middle, the funded initiatives at the bottom. A request that can state its mission link in one sentence gives the committee a reason to rank it. A request that cannot is asking the committee to spend institutional capital on something the institution has not said it wants, and it loses, however good the technology.

        The RA-CDS mission link takes one sentence: earlier treatment escalation in active RA reduces uncontrolled flares (the outcomes priority) and avoids $4K to $6K of utilization per flare averted (the value priority). When you wrote the funding request, that sentence came first.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## SWOT: locating the institution before planning for it

        SWOT analysis names the institution's internal strengths and weaknesses and its external opportunities and threats. The internal pair describes what the institution can do today; the external pair describes what the environment will reward or punish. Strategy work begins here because a roadmap built for an institution that does not exist fails on contact with the build queue.

        The worked SWOT for Helios's clinical-informatics position:

        | | Helpful | Harmful |
        |---|---|---|
        | **Internal** | **Strengths.** A mature EHR with an established build team. Working governance committees (AI Governance, EMR Optimization, IT Steering) that can review and approve without improvising process. | **Weaknesses.** A BI report backlog measured in months. Integration-engineer scarcity: two engineers serve the whole system, and every interface project queues behind them. |
        | **External** | **Opportunities.** The CDS Hooks infrastructure built for the RA-CDS is reusable by other service lines. Payer quality bonuses increasingly reward documented treat-to-target care. | **Threats.** Vendor lock-in narrowing future options. Ransomware targeting health systems. Clinician burnout from accumulated alert load. |

        The SWOT positions the RA-CDS precisely. It builds on both strengths (the EHR build team, the committees that already approved it), exploits both opportunities (it creates the reusable CDS infrastructure; it documents treat-to-target escalation), and touches one threat directly: it adds an alert to the load that is burning clinicians out, which is why the funding request had to name its override-rate monitoring plan rather than hope nobody asked.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The multi-year roadmap: sequenced commitments, not a wish list

        An IT roadmap covers a 3-year horizon and is refreshed annually. The refresh matters as much as the horizon: year 1 is firm, year 2 is planned, year 3 is directional, and every year the window slides forward one year with the new information the last year produced.

        The difference between a roadmap and a wish list is structural. A roadmap entry has a sequence position, named dependencies, and a funding source. A wish list entry has enthusiasm. The Helios roadmap that came out of last year's refresh:

        | Year | Committed work | Depends on |
        |---|---|---|
        | Year 1 (current) | RA flare-risk CDS go-live. Security hardening phase 1 (MFA rollout). ED sepsis alert refresh. | Fall capital approval; CDS Hooks service build. |
        | Year 2 | Data-warehouse migration begins (a 2-year capital line). RA registry expansion to the community partners. Security hardening phase 2 (privileged access management). | Phase 1 MFA completion; an integration-engineer hire. |
        | Year 3 | Data-warehouse migration completes. Ambient-documentation scale-up decision from pilot results. Pharmacy IV-workflow replacement. | Year 2 pilot results; warehouse cutover. |

        Read the dependency column. The registry expansion waits a year not because it lacks merit but because the integration engineers it needs are committed to the warehouse migration. Sequencing is the honest form of prioritization: it says when, not only whether.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Capital planning and the calendar that decides timing

        Capital money moves on a fixed annual cycle, and the cycle is unforgiving. At Helios, as at most health systems:

        | When | What happens |
        |---|---|
        | September to October | Capital requests for the next fiscal year are submitted with scoring justification. |
        | November to January | Finance and IT Steering score and rank the requests. |
        | February to March | Executive leadership sets the capital envelope; the ranked list is cut to fit it. |
        | April to June | The board approves the capital budget. |
        | July 1 | The fiscal year begins; approved funds release. |

        Miss the fall window and the request waits a full year, because the budget it would have entered is already closed. The RA-CDS's $240K one-time cost was submitted in the fall cycle, scored through the winter, and released July 1; the AI Governance approval and the CMIO's email both sit downstream of that calendar. The $60K per year of ongoing maintenance never touched this cycle at all: it is operating expense and enters the operating budget instead.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            "**Callback to Track 05: Financial management.** Track 05 distinguished capital (capex: one-time, depreciated, board-approved through the capital cycle) from operating (opex: ongoing, annual). The RA-CDS request had to be split accordingly: $240K of build, validation, and training as a capital ask in the fall cycle, $60K per year of monitoring, retuning, and report maintenance as a permanent operating line. A request that mixes the two reads as unscoreable and gets sent back."
        ),
        kind="neutral",
    )
    return


@app.cell
def _(mo):
    quiz1 = mo.ui.radio(
        options=[
            "IT Steering can vote it into this quarter's portfolio, so July funding is realistic.",
            "The realistic path is the fall submission window, which funds the fiscal year beginning about 16 months from now; anything earlier requires the contingency reserve or an executive decision to displace an already-approved item.",
            "Reclassify the project as operating expense so the capital calendar does not apply.",
            "Send it directly to the board finance committee, which can add unscored items in the spring.",
        ],
        label=(
            "It is March. The rheumatology chief proposes a $300K musculoskeletal-ultrasound "
            "image-integration project and asks you to get it funded by July 1, when the next "
            "fiscal year begins. Capital requests for that fiscal year were submitted last fall, "
            "and the board approves the capital budget this spring. What do you tell the chief?"
        ),
    )
    quiz1
    return (quiz1,)


@app.cell
def _(mo, quiz1):
    if quiz1.value is None:
        quiz1_feedback = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif quiz1.value.startswith("The realistic path"):
        quiz1_feedback = mo.callout(
            mo.md(
                "**Correct.** The fiscal year starting in July is already funded from last fall's requests; a March request missed that window by five months. Its first regular opportunity is the coming fall cycle, which funds the fiscal year after, roughly 16 months out. The two genuine exceptions are expensive: contingency reserves exist for failures and mandates, not new ideas, and displacing an approved item spends the chief's political capital against whoever owned the displaced project. The operational lesson is to surface requests before the fall window, which is why the strategic-planning conversation with department chiefs happens in summer."
            ),
            kind="success",
        )
    else:
        quiz1_feedback = mo.callout(
            mo.md(
                "**Check the calendar again.** The capital budget the chief wants to draw from was assembled from last fall's submissions and is in board approval now; quarterly IT Steering meetings prioritize within the approved envelope, they do not add to it. Reclassifying a $300K build as operating expense fails because accounting policy, not preference, sets the capex threshold, and splitting the cost to dodge it is an audit finding. The board finance committee approves the ranked list; it does not accept unscored walk-ins. The realistic answer is the fall window for the following fiscal year, unless the chief wants to spend contingency reserve or displace an approved project, both of which carry costs of their own."
            ),
            kind="warn",
        )
    quiz1_feedback
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The IT portfolio: run, grow, transform

        IT portfolio management treats the institution's IT investments as a managed portfolio, balanced the way a financial portfolio is balanced, rather than as a backlog served in arrival order. The standard categories:

        - **Run.** Investments that keep current operations safe and working: the security program, the pharmacy IV-workflow replacement, the sepsis alert refresh. Run spending is not optional; deferred run work becomes outages and incidents.
        - **Grow.** Investments that extend current capability to more value: the RA-CDS, the portal scheduling module, the registry expansion. Grow is where most clinical-informatics requests live.
        - **Transform.** Investments that change what the institution can do at all: the warehouse migration, the ambient-documentation pilot. High value, high effort, long horizon, and the first category cut when budgets tighten, so it needs portfolio protection.

        Health systems typically find 60 to 70 percent of IT spend already committed to run before any new request is heard. The portfolio question is never "is this project good," it is "what mix of run, grow, and transform serves the strategy, and which good projects do we therefore decline." The portfolio review recurs at IT Steering each quarter, and its honest outputs include kill and defer decisions recorded in the minutes, not only approvals. Track 01 placed IT Steering as the owner of this decision.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Interactive: the portfolio-prioritization matrix

        Of the 14 requests on the winter agenda, eight cleared intake screening and arrived pre-scored. Each carries a strategic-value score (1 to 10: strength of the mission link and expected benefit), an effort-and-cost score (1 to 10: build effort, integration load, disruption), a risk-reduction score (1 to 10: how much institutional risk the initiative retires), a portfolio category, and a capital ask. The agenda packet:

        | Initiative | Category | Strategic value | Effort and cost | Risk reduction | Capital ask |
        |---|---|---|---|---|---|
        | RA flare-risk CDS (your request) | Grow | 8 | 5 | 3 | $240K |
        | ED sepsis alert refresh | Run | 6 | 3 | 5 | $120K |
        | RA registry expansion | Grow | 6 | 4 | 2 | $180K |
        | Patient-portal self-scheduling | Grow | 7 | 6 | 2 | $400K |
        | Data-warehouse migration | Transform | 9 | 9 | 4 | $1,500K |
        | Ambient-documentation pilot | Transform | 7 | 7 | 2 | $350K |
        | Pharmacy IV-workflow replacement | Run | 5 | 6 | 7 | $600K |
        | Security hardening program | Run | 6 | 5 | 10 | $450K |

        The committee's real work is choosing the weights. Set how much the portfolio rewards strategic value and risk reduction and how much it penalizes effort, then set the capital ceiling for the cycle. The composite score is (value weight x strategic value) + (risk weight x risk reduction) - (effort weight x effort). The scatter, the ranked list, and the fund/defer line all move with your settings. Total asks come to $3,840K, so any realistic ceiling forces deferrals.
        """
    )
    return


@app.cell
def _(mo):
    w_value = mo.ui.slider(start=0, stop=5, step=1, value=5, label="Weight on strategic value", show_value=True)
    w_effort = mo.ui.slider(start=0, stop=5, step=1, value=3, label="Weight on effort and cost (penalty)", show_value=True)
    w_risk = mo.ui.slider(start=0, stop=5, step=1, value=1, label="Weight on risk reduction", show_value=True)
    ceiling_pick = mo.ui.dropdown(
        options={
            "$1.0M": 1000,
            "$1.5M": 1500,
            "$2.0M": 2000,
            "$3.0M": 3000,
            "No ceiling (fund everything)": 1_000_000,
        },
        value="$2.0M",
        label="Capital ceiling for this cycle",
    )
    mo.vstack([w_value, w_effort, w_risk, ceiling_pick])
    return ceiling_pick, w_effort, w_risk, w_value


@app.cell
def _(INITIATIVES, ceiling_pick, pd, w_effort, w_risk, w_value):
    _rows = []
    for _ini in INITIATIVES:
        _score = (
            w_value.value * _ini["value"]
            - w_effort.value * _ini["effort"]
            + w_risk.value * _ini["risk_reduction"]
        )
        _rows.append({**_ini, "score": _score})
    _df = pd.DataFrame(_rows).sort_values("score", ascending=False, kind="mergesort").reset_index(drop=True)
    _committed = 0
    _decisions = []
    for _cap in _df["capital_k"]:
        if _committed + _cap <= ceiling_pick.value:
            _committed += _cap
            _decisions.append("Fund")
        else:
            _decisions.append("Defer")
    _df["decision"] = _decisions
    portfolio_df = _df[
        ["initiative", "label", "category", "value", "effort", "risk_reduction", "capital_k", "score", "decision"]
    ]
    portfolio_df.index = range(1, len(portfolio_df) + 1)
    portfolio_df.index.name = "rank"
    return (portfolio_df,)


@app.cell
def _(alt, mo, portfolio_df):
    _base = alt.Chart(portfolio_df.reset_index()).encode(
        x=alt.X("effort:Q", scale=alt.Scale(domain=[0, 10]), title="Effort and cost (1 to 10)"),
        y=alt.Y("value:Q", scale=alt.Scale(domain=[0, 10]), title="Strategic value (1 to 10)"),
    )
    _points = _base.mark_circle(opacity=0.85).encode(
        color=alt.Color("category:N", title="Portfolio category"),
        size=alt.Size("capital_k:Q", title="Capital ask ($K)", scale=alt.Scale(range=[120, 1400])),
        tooltip=[
            alt.Tooltip("initiative:N", title="Initiative"),
            alt.Tooltip("category:N", title="Category"),
            alt.Tooltip("value:Q", title="Strategic value"),
            alt.Tooltip("effort:Q", title="Effort and cost"),
            alt.Tooltip("risk_reduction:Q", title="Risk reduction"),
            alt.Tooltip("capital_k:Q", title="Capital ($K)"),
            alt.Tooltip("score:Q", title="Composite score"),
            alt.Tooltip("decision:N", title="Decision"),
        ],
    )
    _labels = _base.mark_text(dy=-16, fontSize=11).encode(text="label:N")
    _chart = (_points + _labels).properties(
        width=560,
        height=360,
        title="The IT Steering agenda as a portfolio: value vs effort",
    )
    mo.vstack(
        [
            _chart,
            mo.md(
                "Each point is one funding request, placed by its effort-and-cost score (right is harder) and its strategic-value score (up is more aligned). Color is the portfolio category; point size is the capital ask. The upper-left region holds the easy wins; the upper-right holds the transform bets that need multi-year protection; the lower-right is where requests go to be declined."
            ),
        ]
    )
    return


@app.cell
def _(portfolio_df):
    portfolio_df.drop(columns=["label"])
    return


@app.cell
def _(ceiling_pick, mo, portfolio_df, w_risk):
    _ra_rank = int(portfolio_df.index[portfolio_df["label"] == "RA-CDS"][0])
    _ra_decision = portfolio_df.loc[portfolio_df["label"] == "RA-CDS", "decision"].iloc[0]
    _sec_rank = int(portfolio_df.index[portfolio_df["label"] == "Security program"][0])
    _funded = portfolio_df[portfolio_df["decision"] == "Fund"]
    _deferred = portfolio_df[portfolio_df["decision"] == "Defer"]
    _funded_total = int(_funded["capital_k"].sum())
    _no_ceiling = ceiling_pick.value >= 1_000_000
    _ceiling_label = "no ceiling" if _no_ceiling else f"${ceiling_pick.value / 1000:.1f}M"

    _parts = []
    _parts.append(
        f"**Where the RA-CDS lands.** Strategic value 8 at effort 5: high alignment at moderate effort, the upper-middle of the chart. At your current weights it ranks {_ra_rank} of 8 and is {'funded' if _ra_decision == 'Fund' else 'deferred'}. The position is no accident; the mission link (outcomes and value), the reusable CDS infrastructure, and the modest $240K ask were all built into the request before it reached this table."
    )
    if _sec_rank == 1:
        _parts.append(
            "**The security program tops your ranking.** It treats no patient, improves no outcome metric, and wins anyway, because its risk-reduction score is the highest on the agenda and your weights count risk. One ransomware event erases more value than the rest of this portfolio creates. The portfolio view makes that argument visible and quantitative; without it, the program loses every anecdote-versus-anecdote fight against projects with patients in them."
        )
    elif w_risk.value == 0:
        _parts.append(
            f"**Your portfolio is blind to risk.** With the risk weight at zero, the security program falls to rank {_sec_rank}, behind requests with better stories, and nothing in the scoring will ever argue for it. A portfolio weighted only on value and effort systematically starves run-category risk work until an incident reprices it. Raise the risk weight and watch where the program goes."
        )
    else:
        _parts.append(
            f"**Watch the security program.** It currently ranks {_sec_rank}. Its strategic-value score is ordinary but its risk-reduction score (10) is the highest on the agenda; raise the risk weight and it climbs toward the top even though it treats no patient. The portfolio view exists to make that argument visible."
        )
    if _no_ceiling:
        _parts.append(
            "**No ceiling is set.** Everything is funded, which means nothing was prioritized: this is the wish list, not a portfolio. Real cycles have an envelope. Set a ceiling and the ranked list acquires a funding line, and the items below it become explicit defer decisions."
        )
    else:
        _deferred_names = ", ".join(_deferred["label"].tolist()) if len(_deferred) else "none"
        _parts.append(
            f"**Under the {_ceiling_label} ceiling.** {len(_funded)} of 8 requests are funded (${_funded_total}K committed); deferred: {_deferred_names}. A deferral recorded in the minutes with a roadmap slot is a sequencing decision; a deferral with neither is a polite kill, and the committee owes the requester clarity about which one it made."
        )
    if "DW migration" in _deferred["label"].tolist():
        _parts.append(
            "**The warehouse migration deferred.** A $1,500K transform initiative rarely fits under a single cycle's remaining envelope, and skipping it every quarter on that basis is how transform work dies. The portfolio answer is a dedicated multi-year capital line, which is where the Helios roadmap put it: year 2, with the dependency named."
        )
    mo.callout(mo.md("\n\n".join(_parts)), kind="info")
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            "**Forward to Course 22: Security.** The security program's risk-reduction score of 10 compresses a threat landscape this course does not cover: ransomware against health systems, the patient-safety consequences of EHR downtime, and the economics that make PHI a high-value target. Course 22 treats that landscape in full, including why MFA and privileged access management rank where they do on any serious risk register."
        ),
        kind="neutral",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The CI lead as portfolio steward

        Delivering the RA-CDS makes you a project leader. The portfolio view assigns you a second role: steward of the clinical-informatics slice of the institution's IT investments, including the ones that compete with yours.

        The steward's work is visible at three moments. When gastroenterology asks to extend the alert infrastructure to IBD (the request Track 01 routed to IT Steering), the steward's contribution is an honest scoring of the request, not advocacy for their own service line, and, if the integration engineers are already committed, the recommendation to slot it into next year's roadmap refresh rather than pretend it can start now. When the quarterly review shows an initiative underperforming its business case, the steward argues for the kill decision even when the initiative has a sympathetic owner. And when the portfolio drifts all-grow because grow requests have the best stories, the steward defends the run and transform allocations that no department chief will champion.

        Arguing for the right things to not do is the half of the job that the project-delivery role never teaches. The committee remembers who scored their own request honestly; that memory is what your next request draws on.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The artifact: the strategic-alignment statement

        Every concept in this track compresses into a four-field statement that travels with the RA-CDS into the implementation plan:

        | Field | RA-CDS entry |
        |---|---|
        | **Mission link** | Advances Helios's outcomes-and-value priorities: earlier treatment escalation in active RA reduces uncontrolled flares (outcomes) and avoids $4K to $6K of utilization per flare averted (value), within the treat-to-target standard of care. |
        | **SWOT position** | Builds on strengths (mature EHR build team, working governance committees). Exploits opportunities (creates reusable CDS Hooks infrastructure; documents treat-to-target care that payer quality programs reward). Manages one named threat: it adds to alert load, so override-rate monitoring and a retuning path are part of the commitment, not an afterthought. |
        | **Portfolio category** | Grow. Extends existing EHR and CDS capability to new clinical value; first reuse candidate already identified (gastroenterology, pending IT Steering scoring at the next roadmap refresh). |
        | **Capital-cycle timing** | $240K one-time cost approved in last fall's capital cycle, released July 1. $60K per year ongoing enters the operating budget at go-live. First portfolio review at IT Steering 12 months after launch, with the override rate and flare-aversion KPIs as the performance evidence. |

        The capstone collects this statement as section 8 of the implementation plan you hand the CMIO.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Where this goes next

        The portfolio decision funds a project; the project ends at go-live; the system then runs for years. Track 08 covers the deploy-and-run reality on the other side of that line: the command center, the change-control board, support tiers, downtime procedures, and the operations plan that keeps the RA-CDS working after everyone stops calling it a project.
        """
    )
    return


if __name__ == "__main__":
    app.run()
