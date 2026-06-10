"""Track 05: Financial management for informaticists.

The CFO needs the RA-CDS budget by Friday. The track defines the two
health-system budgets (capital and operating), itemizes the deployment's
one-time and ongoing costs, defines ROI, NPV, and TCO, presents vendor
contract economics and the build-vs-buy comparison, and centers on a
reactive 5-year ROI calculator for the RA flare-risk alert.

WASM-safe: no shared imports, no data files, no network calls. Every
figure is a literal value computed inline.
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
        # Track 05: Financial management for informaticists

        The CFO's email is two sentences: "I need the RA-CDS budget before Friday's close of the operating plan. Include what it costs and what Helios gets back." The question has four parts, and each part has its own instrument. Which budget the money comes from is the capital-vs-operating question. What the deployment costs is the line-item question, and the honest version of it covers five years, not one. What Helios gets back is the benefit model. Whether the return justifies the spend is the ROI and NPV question, computed over an explicit horizon at a stated discount rate.

        This track defines each instrument, applies it to the RA-CDS, and ends with the budget artifact the capstone collects.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            **The running scenario.** In the Course 12 capstone you produced the design brief for an RA flare-risk alert: at chart open (the patient-view CDS Hook), for patients with active rheumatoid arthritis, when the recent CRP trajectory and clinical context put the probability of a flare in the next 90 days above the 0.30 firing threshold, a card suggests scheduling a treatment-escalation conversation rather than waiting for the next routine visit. The AI Governance Committee approved the brief, and the CMIO put you in charge of the implementation, with go-live six months out. The deployment serves the 1,247-patient RA panel at Helios Academic Medical Center. Ms. Reyes is in the cohort: her CRP run-up to 36.2 mg/L before adalimumab started is exactly the trajectory the alert exists to catch.
            """
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Two budgets: capital and operating

        A health system runs two budgets, approved by different people on different calendars.

        **Capital expenditure (capex)** pays for assets: purchases made once that deliver value over multiple years. Buildings, imaging equipment, perpetual software licenses, and major system builds are capital. Accounting spreads the cost over the asset's useful life (depreciation), and the spend is approved through the capital-planning cycle, typically once per fiscal year against a fixed capital pool.

        **Operating expenditure (opex)** pays for running the organization this year: salaries, subscriptions, maintenance fees, supplies. Operating dollars recur, are consumed within the fiscal year, and live in a department's annual operating budget.

        The classification decides which approval path a request takes, which committee hears it, and when the money becomes available. A capital request that misses the fall submission window waits a full year. An operating line, once added, recurs: a $60K annual maintenance commitment is a $300K five-year commitment, and the CFO reads it that way.

        Where the common informatics line items land:

        | Line item | Usual classification | Why |
        |---|---|---|
        | Perpetual software license | Capital | Creates a multi-year asset, depreciated over its useful life. |
        | SaaS subscription | Operating | A recurring fee; no asset appears on the books. |
        | Internal FTE time on a build | Capital, often | Labor that creates internal-use software can be capitalized during the development phase. The same analyst's hours after go-live are operating. |
        | Vendor maintenance fee | Operating | Recurring; sustains the asset rather than creating it. |
        | Training at go-live | Mixed | Initial training is often bundled into the capitalized project; refresher training is operating. |
        | Post-go-live monitoring and retuning | Operating | Recurring work that keeps the system performing. |

        Fiscal-year planning runs months ahead of the spending. Operating budgets are assembled department by department in the spring for the fiscal-year start (July 1 or October 1 in most systems). Capital requests are submitted in the fall and ranked against every other request in the systemwide pool. The informaticist who wants money in the next fiscal year is writing budget justifications two or three quarters before the first dollar moves.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            **Forward to Track 7: Strategic planning and IT portfolio management.** The capital pool is finite, and the requests against it are ranked by the IT Steering Committee as a portfolio decision. Track 7 covers the capital-cycle calendar in detail, including what happens to a request that surfaces in March asking for June funding.
            """
        ),
        kind="neutral",
    )
    return


@app.cell
def _(mo):
    quiz1 = mo.ui.radio(
        options=[
            "Capital: it belongs to the RA-CDS project",
            "Operating: it recurs every year and sustains the asset rather than creating it",
            "Neither: internal labor does not appear in either budget",
        ],
        label=(
            "The $60K per year for monitoring, retuning, and report maintenance "
            "after go-live: which budget does it come from?"
        ),
    )
    quiz1
    return (quiz1,)


@app.cell
def _(mo, quiz1):
    if quiz1.value is None:
        _resp = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif quiz1.value.startswith("Operating"):
        _resp = mo.callout(
            mo.md(
                "**Correct.** The maintenance line recurs, is consumed within each "
                "fiscal year, and keeps an existing asset performing, so it is "
                "operating expenditure. Build-phase labor takes the opposite "
                "classification: internal FTE time that creates the "
                "software can often be capitalized during the development phase, so "
                "the same analyst's hours land in capital during the build and in "
                "operating after go-live. The classification matters because it "
                "decides which approval cycle the money rides and whose budget "
                "absorbs it every year afterward."
            ),
            kind="success",
        )
    else:
        _resp = mo.callout(
            mo.md(
                "**Reconsider the timing and the recurrence.** The monitoring and "
                "retuning work happens every year for as long as the alert runs, "
                "and it sustains an asset that already exists rather than creating "
                "a new one. Recurring, asset-sustaining spend is operating "
                "expenditure. Internal labor absolutely appears in budgets: during "
                "the build phase it can often be capitalized (it is creating the "
                "asset), and after go-live it is operating."
            ),
            kind="warn",
        )
    _resp
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The RA-CDS budget: line items

        The one-time implementation cost is about $240K, spent across the six-month timeline from Track 2. The breakdown:

        | One-time line item | When | Estimate |
        |---|---|---|
        | Informaticist time (0.5 FTE across the six-month build, fully loaded) | Months 1 to 6 | $60K |
        | EHR analyst time (1.0 FTE, fully loaded) | Months 2 to 5 | $70K |
        | CDS Hooks service build and integration-engine work | Months 2 to 3 | $65K |
        | Validation testing in silent mode | Month 4 | $20K |
        | Training development and delivery | Month 5 | $25K |
        | **Total one-time** | | **$240K** |

        The ongoing cost is about $60K per year for as long as the alert runs:

        | Annual line item | Estimate |
        |---|---|
        | Performance monitoring and report maintenance | $25K |
        | Model retuning and revalidation | $20K |
        | Infrastructure and integration upkeep | $15K |
        | **Total annual** | **$60K** |

        Fully loaded FTE cost (salary plus benefits plus overhead) is the right basis for the labor lines; budgeting bare salary understates labor cost by 30 to 40%. The estimates above are planning figures, stated to the nearest $5K, which is the appropriate precision for a pre-approval budget.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Total cost of ownership

        The $240K build is the visible cost. It is also the minority of what the RA-CDS costs. **Total cost of ownership (TCO)** is the full cost of a system over a stated period: acquisition or build, integration, training, maintenance, infrastructure, and eventually decommissioning. Over five years the RA-CDS TCO is $240K plus five years at $60K, or **$540K**. The build is 44% of the total. The majority arrives after go-live, in $60K annual increments that someone's operating budget must absorb.

        Underbudgeting the ongoing line is the most common informatics budgeting error. The symptom appears a year later as a retuning queue nobody is funded to work and a monitoring dashboard nobody is paid to read. Track 8 covers the post-go-live operations this money pays for; the budgeting lesson here is that approval of the build without commitment of the run funds approves half a system.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## ROI and NPV

        **Return on investment (ROI)** is the ratio of net benefit to cost over an explicit horizon:

        ```
        ROI = (benefit - cost) / cost
        ```

        The horizon matters as much as the ratio. A project that loses money over one year can return 40% over five; quoting an ROI without its horizon is quoting a speed without units. For clinical IT the standard horizon is 3 to 5 years; this track uses 5.

        A dollar received next year is worth less than a dollar today, because today's dollar could be earning a return elsewhere in the meantime. The **discount rate** prices that opportunity cost; this track uses 3%, the rate conventional in health-economic analyses. **Net present value (NPV)** discounts each year's net cash flow back to today and sums them:

        ```
        NPV = CF0 + CF1/(1+r) + CF2/(1+r)^2 + ... + CF5/(1+r)^5
        ```

        where CFt is the net cash flow (benefit minus cost) in year t and r is the discount rate. A positive NPV means the project returns more than the same dollars earning r elsewhere; a negative NPV means the dollars are better deployed at the opportunity-cost rate. Raising the discount rate lowers the NPV of any project whose benefits arrive later than its costs, which describes essentially all clinical IT: the costs are front-loaded and the benefits accrue over years.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The benefit side

        Costs are knowable; benefits are modeled. The RA-CDS benefit model has four factors, each an explicit, defensible assumption:

        - **Patients alerted per year.** About 310 of the 1,247-patient panel cross the 0.30 firing threshold in a year.
        - **Share of alerts acted on.** The default is 40%: the realistic post-rollout action rate the Track 3 change-management work exists to protect.
        - **Flares averted per 100 acted-on alerts.** The default is 25. Acting early does not avert every flare; this factor is the clinical effectiveness of the escalation conversation the card prompts.
        - **Cost per flare averted.** A moderate-to-severe RA flare costs roughly $4K to $6K in additional utilization (urgent visits, imaging, steroid courses, occasional admission). The default is $5K.

        At the defaults: 310 alerts, 124 acted on, about 31 flares averted, and a gross annual benefit of about $155K.

        One question the CFO will ask before any other: who captures the averted utilization? Under fee-for-service, avoided urgent visits and admissions are mostly the payer's savings, and the benefit line is a quality argument rather than hard institutional dollars. Under risk-bearing contracts (the ACO arrangements from Course 0), Helios keeps a share of what it avoids spending, and the benefit line is real money. The budget should state which contracting reality it assumes; this model assumes the RA panel sits largely under risk-bearing contracts.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The ROI calculator

        Seven inputs determine the financial case. The defaults are the canonical RA-CDS assumptions. Every output below (the cash-flow table, the cumulative-benefit chart, the verdict) updates as the sliders move.
        """
    )
    return


@app.cell
def _(mo):
    alerted = mo.ui.slider(start=100, stop=600, step=10, value=310, label="Patients alerted per year", show_value=True)
    acted_pct = mo.ui.slider(start=10, stop=80, step=5, value=40, label="Share of alerts acted on (%)", show_value=True)
    averted_per_100 = mo.ui.slider(start=5, stop=50, step=5, value=25, label="Flares averted per 100 acted-on alerts", show_value=True)
    flare_cost = mo.ui.slider(start=4000, stop=6000, step=250, value=5000, label="Cost per flare averted ($)", show_value=True)
    onetime_cost = mo.ui.slider(start=150_000, stop=400_000, step=10_000, value=240_000, label="One-time implementation cost ($)", show_value=True)
    maintenance = mo.ui.slider(start=30_000, stop=120_000, step=5_000, value=60_000, label="Annual maintenance ($)", show_value=True)
    discount_rate = mo.ui.slider(start=0.0, stop=8.0, step=0.5, value=3.0, label="Discount rate (%)", show_value=True)
    mo.vstack([
        mo.md("**Inputs**"),
        alerted,
        acted_pct,
        averted_per_100,
        flare_cost,
        onetime_cost,
        maintenance,
        discount_rate,
    ])
    return (
        acted_pct,
        alerted,
        averted_per_100,
        discount_rate,
        flare_cost,
        maintenance,
        onetime_cost,
    )


@app.cell
def _(
    acted_pct,
    alerted,
    averted_per_100,
    discount_rate,
    flare_cost,
    maintenance,
    onetime_cost,
    pd,
):
    _r = discount_rate.value / 100
    acted_n = alerted.value * acted_pct.value / 100
    flares_averted = acted_n * averted_per_100.value / 100
    gross_benefit = flares_averted * flare_cost.value

    _rows = []
    _cums = []
    _cumulative = 0.0
    for _year in range(6):
        _benefit = 0.0 if _year == 0 else gross_benefit
        _cost = float(onetime_cost.value) if _year == 0 else float(maintenance.value)
        _net = _benefit - _cost
        _dnet = _net / (1 + _r) ** _year
        _cumulative += _dnet
        _cums.append(_cumulative)
        _rows.append({
            "year": _year,
            "benefit": int(round(_benefit)),
            "cost": int(round(_cost)),
            "net": int(round(_net)),
            "discounted_net": int(round(_dnet)),
            "cumulative_net": int(round(_cumulative)),
        })
    cashflow = pd.DataFrame(_rows)
    cashflow.index = range(1, len(cashflow) + 1)
    cashflow.index.name = "row"

    npv_5y = _cums[-1]
    pv_benefits = sum(gross_benefit / (1 + _r) ** _t for _t in range(1, 6))
    pv_costs = onetime_cost.value + sum(maintenance.value / (1 + _r) ** _t for _t in range(1, 6))
    roi_5y = (pv_benefits - pv_costs) / pv_costs

    breakeven_year = None
    payback_months = None
    for _t in range(1, 6):
        _prev = _cums[_t - 1]
        _curr = _cums[_t]
        if _prev < 0 and _curr >= 0:
            _frac = -_prev / (_curr - _prev)
            breakeven_year = (_t - 1) + _frac
            payback_months = int(round(12 * breakeven_year))
            break
    return (
        acted_n,
        breakeven_year,
        cashflow,
        flares_averted,
        gross_benefit,
        npv_5y,
        payback_months,
        roi_5y,
    )


@app.cell
def _(cashflow, mo):
    mo.vstack([
        mo.md("### Year-by-year cash flow"),
        cashflow,
        mo.md(
            "_All figures in dollars. Year 0 is the build year: the one-time cost "
            "lands and no benefit accrues. Years 1 to 5 are operating years: the "
            "gross benefit arrives, the maintenance cost recurs, and each year's "
            "net flow is discounted back to today. The last column is the running "
            "total of discounted net flows; its final value is the 5-year NPV._"
        ),
    ])
    return


@app.cell
def _(alt, breakeven_year, cashflow, mo, pd):
    _line = (
        alt.Chart(cashflow)
        .mark_line(point=True)
        .encode(
            x=alt.X("year:Q", title="Year (0 = build year)", axis=alt.Axis(tickCount=6)),
            y=alt.Y("cumulative_net:Q", title="Cumulative discounted net benefit ($)"),
            tooltip=["year:Q", "cumulative_net:Q"],
        )
    )
    _zero = (
        alt.Chart(pd.DataFrame({"y": [0]}))
        .mark_rule(strokeDash=[4, 4], color="gray")
        .encode(y="y:Q")
    )
    if breakeven_year is None:
        _fig = alt.layer(_line, _zero)
        _caption = (
            "_The line is the running total of discounted net cash flows from the "
            "build year (year 0) through operating year 5. The dashed gray rule "
            "marks zero. The line stays below it across the whole horizon: at "
            "these inputs the project has not paid for itself by the end of "
            "year 5._"
        )
    else:
        _be_rule = (
            alt.Chart(pd.DataFrame({"x": [breakeven_year]}))
            .mark_rule(color="firebrick")
            .encode(x="x:Q")
        )
        _fig = alt.layer(_line, _zero, _be_rule)
        _caption = (
            "_The line is the running total of discounted net cash flows from the "
            "build year (year 0) through operating year 5. The dashed gray rule "
            "marks zero; the red vertical rule marks the break-even point, where "
            "cumulative discounted benefit first covers everything spent so far._"
        )
    _fig = _fig.properties(
        width=560,
        height=300,
        title="Cumulative discounted net benefit, years 0 to 5",
    )
    mo.vstack([_fig, mo.md(_caption)])
    return


@app.cell
def _(acted_n, flares_averted, gross_benefit, mo, npv_5y, payback_months, roi_5y):
    _npv_str = f"-${abs(npv_5y):,.0f}" if npv_5y < 0 else f"${npv_5y:,.0f}"
    if payback_months is None:
        _verdict = mo.callout(
            mo.md(
                f"**At these inputs the project does not pay back within 5 years.** "
                f"About {acted_n:.0f} acted-on alerts avert about "
                f"{flares_averted:.0f} flares per year, a gross annual benefit of "
                f"${gross_benefit:,.0f}; the 5-year NPV is {_npv_str} and the "
                f"discounted 5-year ROI is {roi_5y * 100:.0f}%. The levers, in "
                f"order of leverage: the action rate and the flares-averted rate "
                f"multiply the entire benefit side; the maintenance line compounds "
                f"across all five years; the one-time cost hits once. A negative "
                f"NPV at honest inputs is information: renegotiate scope, cost, or "
                f"expectations before the IT Steering Committee does it for you."
            ),
            kind="warn",
        )
    else:
        _verdict = mo.callout(
            mo.md(
                f"**At these inputs the project pays for itself.** About "
                f"{acted_n:.0f} acted-on alerts avert about {flares_averted:.0f} "
                f"flares per year, a gross annual benefit of ${gross_benefit:,.0f}. "
                f"The 5-year NPV is {_npv_str}, the discounted 5-year ROI is "
                f"{roi_5y * 100:.0f}%, and break-even arrives about month "
                f"{payback_months} after go-live. The action rate is the "
                f"highest-leverage input: it multiplies the entire benefit side, "
                f"and it is a clinical-adoption number, not a technical one. "
                f"Track 3's change-management plan protects the benefit side of "
                f"this calculation; every dismissed alert subtracts from it."
            ),
            kind="success",
        )
    _verdict
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Vendor contract economics

        The RA-CDS was built internally, so the budget above is a build budget. Most clinical systems are bought, and a bought system's economics follow the contract.

        **Licensing models.** Three dominate. Per-user (per-seat) licensing scales with the clinician count and suits departmental tools. Per-bed licensing scales with hospital size and is common for inpatient enterprise systems. Flat enterprise licensing buys unlimited internal use for a negotiated sum and suits systemwide platforms. A 720-bed academic center with a large ambulatory footprint prices very differently under per-bed and per-user terms, which is why the licensing model is a negotiation item, not a list price.

        **Maintenance fees.** Vendor maintenance typically runs 18 to 22% of the license price per year, covering support, patches, and upgrades. At 20%, five years of maintenance equals the license: the effective price roughly doubles over the first five years, before integration and internal staffing are counted.

        **Build vs buy for the RA-CDS.** A vendor flare-risk module exists, hypothetically, at $150K plus 20% annual maintenance. The comparison:

        | | Build (the chosen path) | Vendor module (hypothetical) |
        |---|---|---|
        | One-time | $240K internal build | $150K license + $60K integration, local validation, training |
        | Ongoing | $60K/yr monitoring, retuning, infrastructure | $30K/yr maintenance (20% of license) + $15K/yr internal monitoring |
        | 5-year TCO | $540K | $435K |
        | Threshold and retuning control | Internal: AI Governance signs off on changes | Vendor release cycle; configurability varies by contract |
        | Exit cost | Low | Termination terms, data egress, and replacement cost |

        The sticker gap ($150K against $240K) narrows once integration, validation, and internal monitoring are priced in. The residual difference buys control: AI Governance owns the firing threshold and the retuning calendar on the built system, while the vendor's release cycle owns them on the bought one. Local validation does not disappear with a purchase order: an externally trained model must still be validated on Helios patients before it touches the 1,247-patient panel, and the contract must say who pays when retuning is needed.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            **Callback to Course 11: Health economics through data (Tracks 3 and 4).** This track prices the RA-CDS in dollars for an institutional decision: cost-benefit analysis, with ROI and NPV as the summary statistics. Course 11 Tracks 3 and 4 price clinical strategies in health: cost-effectiveness and cost-utility analysis, with cost per QALY gained measured against a willingness-to-pay threshold. The two frames answer different questions and can disagree. A deployment can clear the CFO's ROI bar while buying QALYs at an unattractive price, or fail to pay for itself in institutional dollars while being excellent value for health. The CFO's Friday deadline is a cost-benefit question; a P&T or coverage decision about the escalation therapies the card recommends is a cost-effectiveness question.
            """
        ),
        kind="neutral",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The artifact: the budget estimate with the 5-year ROI

        The Course 16 capstone assembles the implementation plan you will hand the CMIO. This track contributes the budget section. At the canonical assumptions, the artifact reads:

        | Field | Value |
        |---|---|
        | One-time implementation cost | $240K (informaticist and EHR-analyst FTE time, CDS-service build, validation, training delivery) |
        | Annual ongoing cost | $60K (monitoring, retuning, report maintenance, infrastructure) |
        | 5-year TCO | $540K |
        | Benefit model | 310 patients alerted/yr, 40% acted on, 25 flares averted per 100 acted-on alerts, $5K per flare averted |
        | Annual gross benefit | $155K |
        | Discount rate | 3% |
        | 5-year NPV | about $195K |
        | Discounted 5-year ROI | about 38% |
        | Payback | about month 32 after go-live |

        The budget travels with its assumptions. The CFO will probe the action rate and the per-flare cost first; a budget that states them as named, adjustable inputs survives that meeting, and a budget that presents a bare NPV does not. The capstone collects this estimate as the budget-and-ROI section of the implementation plan, alongside the project charter (Track 1) and the timeline and RACI (Track 2).
        """
    )
    return


if __name__ == "__main__":
    app.run()
