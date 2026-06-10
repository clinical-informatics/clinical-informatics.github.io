"""Track 04: Healthcare quality improvement and operations management.

Three months after the RA-CDS full launch, the CMO asks for a one-page
dashboard. The track covers the Model for Improvement and PDSA (with a
worked cycle on the card text), Lean and the DOWNTIME wastes, Six Sigma
DMAIC, run charts and control charts as the QI measurement system (with
an interactive 24-week override-rate series), the Triple and Quadruple
Aim, the KPI taxonomy and the external measurement frameworks, and a
KPI-selector exercise. The artifact is the KPI dashboard mockup with
target thresholds, collected by the course capstone.

WASM-safe: no shared imports, no data files, deterministic synthetic data.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd

    return alt, mo, np, pd


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 04: Healthcare quality improvement and operations management

        Three months after the RA-CDS reached full launch, the CMO's request arrives: "One page on the flare alert. How is it doing?" The request is a measurement-design problem. Two decisions determine whether the page earns its two minutes of executive attention: which numbers belong on it, and how the reader can tell whether a number's movement is signal or noise.

        This track covers the quality-improvement methods behind both decisions. The Model for Improvement and the PDSA cycle supply the testing discipline. Lean and Six Sigma supply the operations vocabulary. Run charts and control charts supply the measurement system that separates real change from noise. The KPI taxonomy and the external measurement frameworks supply the selection criteria. The artifact at the end is the one-page KPI dashboard mockup the course capstone collects.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            **Where the project stands.** In the Course 12 capstone you produced the design brief for an RA flare-risk alert: at chart open (the patient-view CDS Hook), for patients with active rheumatoid arthritis, when the recent CRP trajectory and clinical context put the probability of a flare in the next 90 days above the 0.30 firing threshold, a card suggests scheduling a treatment-escalation conversation rather than waiting for the next routine visit. The AI Governance Committee approved the brief, and the CMIO handed you the implementation with a six-month runway. The cohort is the 1,247-patient rheumatology panel at Helios Academic Medical Center; Ms. Reyes is in it, and her CRP run-up to 36.2 mg/L before adalimumab started is exactly the trajectory the alert exists to catch. Full launch completed on schedule at month 6 (the Track 2 timeline). This track sits three months after that.
            """
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Model for Improvement

        The Model for Improvement, developed by Associates in Process Improvement and carried into healthcare by the Institute for Healthcare Improvement (IHI), is the default QI method in American hospitals. It consists of three questions and a testing cycle.

        | IHI question | Applied to the RA-CDS |
        |---|---|
        | **What are we trying to accomplish?** (the aim) | Patients with rising flare risk get a treatment-escalation conversation within days of the signal, instead of at the next routine visit. Stated with a number and a date: median alert-to-conversation interval of 14 days or less by month 12 after launch. |
        | **How will we know that a change is an improvement?** (the measures) | Override rate, percentage of alerts acted on, median days from alert to escalation conversation, 90-day flare rate among alerted patients. Defined before the change ships, not after. |
        | **What change can we make that will result in improvement?** (the changes) | Candidates: card-text revisions, threshold tuning, a scheduling shortcut on the card itself, reserved escalation slots in the rheumatology templates. |

        An aim names the clinical change the alert exists to produce, stated so that failure would be detectable. "Deploy the alert" does not qualify: deployment is an activity, and an activity can complete while the clinical change never happens.

        The testing cycle is **PDSA**: Plan (the change, the prediction, the data to collect), Do (run the test at small scale), Study (compare the result against the prediction), Act (adopt the change, adapt it and test again, or abandon it). The cycle's discipline is its scale: one change, few users, short horizon, explicit prediction. A failed PDSA costs a week; a failed big-bang revision costs the deployment's credibility.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### A worked PDSA: the card text

        During the month-5 soft launch (5 rheumatologists), the override rate ran at 71%, above the 50 to 70% band the design brief planned for. Huddle feedback said the card read like a model output, not a clinical message. One full cycle:

        | Phase | What happened |
        |---|---|
        | **Plan** | Revise the card detail text to lead with the patient's own CRP trajectory rather than the model's probability output. Prediction: the override rate among the 5 soft-launch users falls below 65% within three weeks. Data to collect: weekly override rate per user, one-line feedback at the Friday huddle. |
        | **Do** | The EHR analyst deployed the revised text to the 5 soft-launch users at the start of the second soft-launch week. No other change shipped during the window. |
        | **Study** | The override rate fell from 71% to 64% over three weeks, meeting the prediction. Two of the five users asked for the most recent CRP value and collection date on the card face. |
        | **Act** | Adapt: keep the trajectory-first framing, add the most recent CRP value and date, run one more soft-launch week, then adopt the combined text for full launch. |

        Adopt, adapt, and abandon are the only three exits from a PDSA cycle; this one exited through adapt, and the adapted text shipped at full launch. Cycles continue after go-live. The control-chart interactive below shows the effect of a later cycle: a card-text revision deployed at the end of week 15 after full launch.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Lean for healthcare

        Lean is the Toyota-derived operations philosophy: maximize the value delivered to the customer (in healthcare, the patient) and remove everything that does not contribute to it. Four Lean tools recur in informatics work.

        - **5S** (sort, set in order, shine, standardize, sustain): workplace organization, applied to digital workplaces. The Helios alert inventory is a 5S target: retire dead alerts, name the live ones consistently, assign each an owner, review the inventory on a schedule. The EMR Optimization Committee's alert-design standards are the standardize step.
        - **Value-stream mapping**: diagram every step between a triggering event and the delivered value, with the elapsed time of each, then classify each step as value-adding or waiting. For the RA-CDS the stream runs from CRP resulting to escalation conversation held. Most of the elapsed time is waiting between steps, and the alert targets the longest wait: the gap between the signal appearing and anyone seeing it.
        - **Gemba walks**: go to where the work happens and watch. For an informaticist this means sitting in rheumatology clinic watching the card appear at chart open, not reading override statistics in a conference room. The week-15 card revision in the interactive below came from a gemba observation, not from the dashboard.
        - **A3 problem-solving**: the one-page structured problem document (background, current condition, target condition, root-cause analysis, countermeasures, plan, follow-up), named for the paper size. The constraint is the single page: a problem that cannot be stated on one page is not yet understood. Track 6 applies the same one-page discipline to executive communication.

        Lean names eight wastes, with the acronym DOWNTIME. Each has a clinical-informatics form.

        | Waste | Clinical-informatics example |
        |---|---|
        | **D**efects | The alert fires on a patient without active RA: a cohort value-set defect that generates investigation work downstream. |
        | **O**verproduction | A nightly report nobody opens; alerts on patients who already have an escalation visit scheduled. |
        | **W**aiting | A CRP results on Monday and the signal sits unseen until the chart is next opened weeks later. The BI request queue is institutional waiting. |
        | **N**on-utilized talent | The EHR analyst hand-pulling charts for a report a scheduled query could produce; rheumatologists doing data entry a flowsheet could structure. |
        | **T**ransportation | The override-rate extract exported to a spreadsheet, emailed, and re-imported into a slide deck instead of read from the warehouse. |
        | **I**nventory | The backlog: unworked optimization tickets, unreviewed tuning requests, dashboards built but never validated. |
        | **M**otion | Seven clicks between the card and the order set it recommends. Every extra click is motion waste paid at clinic speed. |
        | **E**xtra-processing | The same joint count documented in the flowsheet and re-typed into the note; a report manually reformatted every month because the template was never fixed. |
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Six Sigma and DMAIC

        Six Sigma is the defect-reduction discipline developed at Motorola: define a defect precisely, measure the process's defect rate, and reduce variation until defects are rare. Its project structure is **DMAIC**: Define (the problem, the customer, the defect), Measure (baseline performance with a validated measurement), Analyze (find the root causes of variation), Improve (change the process), Control (hold the gain with monitoring and response rules).

        The fit question separates the two methods. DMAIC suits stable, high-volume processes with a countable defect and a measurement system worth the investment: laboratory turnaround time, barcode-scan compliance, claims-denial rates. The Model for Improvement suits iterative learning under uncertainty, where the next change is not knowable in advance: most CDS deployments, including this one. The two are complements rather than rivals. The RA-CDS program runs on PDSA cycles, and the control chart that holds the gain after each adopted change is DMAIC's Control phase in everything but name.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Run charts and control charts

        A dashboard number without its time series invites the wrong question ("is 58% good or bad?"). The right question is whether the process producing the number has changed. Run charts and control charts answer it.

        A **run chart** is the time series with a center line at the **median** of the plotted points. Three probability-based rules identify **special-cause variation**, change unlikely to come from a stable process:

        - **Shift**: six or more consecutive points on the same side of the median.
        - **Trend**: five or more consecutive points all ascending or all descending.
        - **Astronomical point**: a point obviously distinct from the rest. Judgment in a run chart; the control chart formalizes it.

        A **control chart** adds **control limits** at roughly 3 sigma above and below the center line, computed from the process's own variation. A stable process stays inside its limits and meets no rule: it shows **common-cause variation**, the noise inherent in the process. A point outside the limits, or a rule violation, is special cause: something happened.

        The distinction carries the management consequence. Reacting to common-cause variation as if it were signal is **tampering**, Deming's term, and tampering makes a stable process worse: the manager who demands an explanation for every downtick teaches the team to manufacture explanations and to adjust a process that did not change. The load-bearing claim of this section: a dashboard number presented without its time series and limits invites tampering. Course 04 built the underlying measurement thinking (variation, distributions, what one draw from a noisy process can and cannot say); a control chart is that thinking operationalized for managers.

        ### The override-rate series

        The chart below plots 24 weeks of the RA-CDS override rate after full launch. At the end of week 15 a card-text revision (the third PDSA cycle, prompted by a gemba observation) deployed to all users. The control limits are computed from weeks 1 to 15, the period before the planned change, and frozen there: limits computed across a known intervention would smear two different processes into one set of limits. Toggle the chart elements and read the series each way.
        """
    )
    return


@app.cell
def _(np, pd):
    _rng = np.random.default_rng(16)
    _rates = np.round(np.concatenate([62.0 + _rng.normal(0.0, 2.2, 15), 53.5 + _rng.normal(0.0, 2.2, 9)]), 1)
    median_value = float(np.median(_rates))
    _bmean = float(_rates[:15].mean())
    _bstd = float(_rates[:15].std(ddof=1))
    ucl_value = round(_bmean + 3.0 * _bstd, 1)
    lcl_value = round(_bmean - 3.0 * _bstd, 1)

    _sides = [1 if _r > median_value else (-1 if _r < median_value else 0) for _r in _rates]
    _shift = [False] * 24
    _i = 0
    while _i < 24:
        if _sides[_i] == 0:
            _i += 1
            continue
        _j = _i
        while _j < 24 and _sides[_j] == _sides[_i]:
            _j += 1
        if _j - _i >= 6:
            for _k in range(_i, _j):
                _shift[_k] = True
        _i = _j

    _trend = [False] * 24
    for _dirn in (1, -1):
        _start = 0
        for _t in range(1, 25):
            _cont = _t < 24 and (_rates[_t] - _rates[_t - 1]) * _dirn > 0
            if not _cont:
                if _t - _start >= 5:
                    for _k in range(_start, _t):
                        _trend[_k] = True
                _start = _t

    _astro = [bool(_r > ucl_value or _r < lcl_value) for _r in _rates]
    override_df = pd.DataFrame({"week": range(1, 25), "override_rate": _rates, "shift_flag": _shift, "trend_flag": _trend, "astro_flag": _astro})
    override_df["signal"] = np.where(
        override_df[["shift_flag", "trend_flag", "astro_flag"]].any(axis=1), "special cause", "common cause"
    )
    return lcl_value, median_value, override_df, ucl_value


@app.cell
def _(mo):
    show_median = mo.ui.switch(label="Show the median (run-chart center line)", value=False)
    show_limits = mo.ui.switch(label="Show the control limits (3 sigma, frozen at weeks 1 to 15)", value=False)
    mark_special = mo.ui.switch(label="Mark special-cause points", value=False)
    mo.vstack([show_median, show_limits, mark_special])
    return mark_special, show_limits, show_median


@app.cell
def _(alt, lcl_value, mark_special, median_value, override_df, pd, show_limits, show_median, ucl_value):
    _x = alt.X("week:Q", title="Week after full launch", scale=alt.Scale(domain=[1, 24]), axis=alt.Axis(tickMinStep=1))
    _y = alt.Y("override_rate:Q", title="Override rate (%)", scale=alt.Scale(domain=[45, 72]))
    _tt = [
        alt.Tooltip("week:Q", title="week"),
        alt.Tooltip("override_rate:Q", title="override %"),
        alt.Tooltip("signal:N", title="signal"),
    ]
    _base = alt.Chart(override_df)
    _line = _base.mark_line(color="#4c78a8").encode(x=_x, y=_y)
    if mark_special.value:
        _color = alt.Color(
            "signal:N", title="",
            scale=alt.Scale(domain=["common cause", "special cause"], range=["#4c78a8", "#d62728"]),
        )
        _pts = _base.mark_point(filled=True, size=75).encode(x=_x, y=_y, tooltip=_tt, color=_color)
    else:
        _pts = _base.mark_point(filled=True, size=75, color="#4c78a8").encode(x=_x, y=_y, tooltip=_tt)
    _layers = [_line, _pts]
    _layers.append(alt.Chart(pd.DataFrame({"week": [15.5]})).mark_rule(color="#888888", strokeDash=[5, 4]).encode(x="week:Q"))
    _layers.append(
        alt.Chart(pd.DataFrame({"week": [15.7], "y": [71.0], "label": ["card-text revision"]}))
        .mark_text(align="left", fontSize=11, color="#666666").encode(x="week:Q", y="y:Q", text="label:N")
    )
    if show_median.value:
        _layers.append(alt.Chart(pd.DataFrame({"y": [median_value]})).mark_rule(color="#2ca02c").encode(y="y:Q"))
    if show_limits.value:
        _layers.append(alt.Chart(pd.DataFrame({"y": [ucl_value, lcl_value]})).mark_rule(color="#d62728", strokeDash=[2, 3]).encode(y="y:Q"))
    alt.layer(*_layers).properties(width=620, height=320, title="RA-CDS override rate, weeks 1 to 24 after full launch")
    return


@app.cell
def _(lcl_value, mark_special, median_value, mo, override_df, show_limits, show_median, ucl_value):
    _below = override_df.loc[override_df["shift_flag"] & (override_df["override_rate"] < median_value), "week"]
    _above = override_df.loc[override_df["shift_flag"] & (override_df["override_rate"] > median_value), "week"]
    _n_astro = int(override_df["astro_flag"].sum())
    _trend_weeks = override_df.loc[override_df["trend_flag"], "week"]
    _parts = [
        "The chart shows the weekly share of RA-CDS firings dismissed without the suggested action, across the first 24 weeks after full launch. The dashed vertical line marks the card-text revision deployed at the end of week 15."
    ]
    if not (show_median.value or show_limits.value or mark_special.value):
        _parts.append(
            "Read bare, the series invites anecdote: the eye anchors on the most recent move and the loudest point. Switch on the median to apply the run-chart rules."
        )
    if show_median.value:
        _parts.append(
            f"The green line is the median of all 24 weeks ({median_value:.1f}%). Weeks {int(_below.min())} to {int(_below.max())} sit below it, {len(_below)} consecutive points; six or more on one side is the shift rule, so the pattern is special cause. Weeks {int(_above.min())} to {int(_above.max())} form the mirror run above the median: a step change in mid-series splits the all-weeks median between the two processes, and both sides register the shift."
        )
    if show_limits.value:
        _parts.append(
            f"The red dashed lines are the control limits ({lcl_value}% and {ucl_value}%), computed from weeks 1 to 15 (the pre-change process) and frozen. {_n_astro} post-revision points sit below the lower limit: astronomical points by the formal rule."
        )
    if mark_special.value:
        _parts.append(
            f"The red points satisfy at least one rule: the shift (weeks {int(_below.min())} to {int(_below.max())} below the median, with the mirror run of weeks {int(_above.min())} to {int(_above.max())} above it), the trend (weeks {int(_trend_weeks.min())} to {int(_trend_weeks.max())} fall consecutively), and the 3-sigma rule ({_n_astro} points below the lower limit). The rules agree, the change point coincides with the deployed revision, and the direction is the intended one. The verdict: special cause, attributable, desirable. The operational move now is to recompute the center line and limits from the post-revision weeks and monitor the new process against them."
        )
    _kind = "success" if mark_special.value else "info"
    mo.callout(mo.md("\n\n".join(_parts)), kind=_kind)
    return


@app.cell
def _(mo):
    quiz1 = mo.ui.radio(
        options=[
            "Special cause: two consecutive points below the median mean the process improved; find the cause and standardize it.",
            "Common cause: no rule is met, and two points below the median is expected variation from a stable process.",
            "A trend: the process was drifting downward well before the week-15 revision.",
            "A measurement defect: a stable process cannot move two points in one week.",
        ],
        label=(
            "With the median visible, weeks 9 and 10 sit below it before the series returns above. "
            "The rheumatology chief emails: \"override is down two weeks running. Whatever you changed, keep it going.\" "
            "Nothing changed in those weeks. The correct reading of weeks 9 and 10:"
        ),
    )
    quiz1
    return (quiz1,)


@app.cell
def _(mo, quiz1):
    if quiz1.value is None:
        _fb1 = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif quiz1.value.startswith("Common cause"):
        _fb1 = mo.callout(
            mo.md(
                "**Correct.** The shift rule needs six or more consecutive points on one side of the median; the trend rule needs five or more consecutive falls; both points sit inside the control limits. Two points below the median meets no rule, so the chart says the process did not change. Crediting a cause anyway is tampering in the flattering direction: it teaches the team to claim noise as improvement, and the same logic will charge them with failure on the next two-week run above the median. The reply to the chief is the chart itself, with the rules annotated, which also builds the habit of asking the chart before asking the team."
            ),
            kind="success",
        )
    else:
        _fb1 = mo.callout(
            mo.md(
                "**Apply the rules, not the impression.** The shift rule needs six or more consecutive points on one side of the median (weeks 9 and 10 are two). The trend rule needs five or more consecutive falls (the dip reverses immediately). Both points sit inside the control limits, so no astronomical point. A stable process produces runs like this routinely; reading them as improvement, defect, or drift is the tampering reflex the chart exists to prevent."
            ),
            kind="warn",
        )
    _fb1
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The Triple Aim and the Quadruple Aim

        IHI's **Triple Aim** names the three simultaneous goals of health-system improvement: better population health, better experience of care, and lower per-capita cost. The **Quadruple Aim** adds the work life of the people delivering care, added because workforce burnout was consuming the gains of the first three. Some institutions carry equity as a fifth aim; Helios reports it as a stratification within each of the four.

        The RA-CDS maps onto all four, and the dashboard should witness each:

        | Aim | RA-CDS measure |
        |---|---|
        | Population health | 90-day flare rate among alerted patients; moderate-to-severe disease-activity prevalence at 12 months. |
        | Experience of care | Median days from alert to escalation conversation; PROM completion on the RA panel. |
        | Per-capita cost | Utilization averted per flare prevented. A moderate-to-severe RA flare carries roughly $4K to $6K in additional utilization; Track 5 does the arithmetic. |
        | Clinician experience | Override burden and alert volume per rheumatologist; quarterly satisfaction with the alert. |

        An intervention that advances three aims by degrading the fourth (an alert that prevents flares while exhausting the clinicians who receive it) has not improved the system. The fourth row is the one informatics teams most often leave off the dashboard, and it predicts the deployment's survival.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The KPIs informaticists own

        Institutional dashboards carry a standard KPI set. The informaticist's relationship to each is operational: the numbers come out of systems informaticists build, and their validity depends on data capture informaticists design.

        | KPI | What it measures | The informaticist's stake |
        |---|---|---|
        | HCAHPS | Patient experience of inpatient care, via the CMS-mandated survey. | Sampling and submission plumbing; linking scores to units and service lines. |
        | 30-day readmission | Unplanned readmissions within 30 days of discharge. | Index-admission logic, transfer handling, exclusion rules. |
        | Mortality O/E | Observed deaths over expected deaths, expected from risk-adjustment models. | The E: documentation and coding completeness drive the expected-mortality model. |
        | Length of stay (LOS) | Days per admission, usually reported observed over expected. | Bed-event timestamps; observation-vs-inpatient classification. |
        | Alert override rate | Share of CDS firings dismissed without the suggested action. | Owned end to end: definition, capture, reporting, tuning. |
        | Time-to-result | Order-to-result interval for labs and imaging. | Interface timestamps across LIS, RIS, and EHR. |
        | Structured-data-capture rate | Share of a clinical fact documented in structured fields rather than free text. | Form and flowsheet design; the rate caps what eCQMs and registries can compute. |
        | Portal activation | Share of patients with an active portal account. | Enrollment workflow, proxy access, equity monitoring. |
        | PROM completion | Share of eligible patients completing patient-reported outcome measures. | Delivery timing, reminder logic, in-visit vs portal capture. |
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Process vs outcome, leading vs lagging

        Two distinctions organize KPI selection.

        **Process vs outcome.** A process KPI measures whether the intended activity happened: override rate, percentage of alerts acted on. An outcome KPI measures whether the clinical state changed: mean DAS28 across the cohort, flare rate. Process measures respond quickly and are directly actionable; outcome measures are the point. A dashboard of pure process measures shows activity without impact; a dashboard of pure outcome measures shows impact with no handle to turn.

        **Leading vs lagging.** A leading indicator moves early enough to act on; a lagging indicator confirms, too late to steer. "Percentage of eligible patients with treat-to-target intensification within 90 days" leads: it moves within a quarter and predicts the disease-activity result. "Moderate-to-severe disease-activity prevalence at 12 months" lags: it is the result. A dashboard with no leading indicators delivers its first honest reading around month 9, far too late to steer.

        The **balanced scorecard** (Kaplan and Norton) guards against one-dimensional measurement by requiring four perspectives: financial, customer (in healthcare, the patient), internal process, and learning and growth. The RA-CDS one-pager maps onto it directly: averted-flare utilization (financial), flare rate and time-to-conversation (patient), override and acted-on rates (internal process), training completion and PDSA cycles run per quarter (learning and growth). A scorecard whose quadrants disagree is reporting honestly: the disagreement is the information the four perspectives exist to expose.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The external measurement frameworks

        Four frameworks generate most of the quality-measure work assigned to a health-system informaticist.

        | Framework | What it is | Who reports | Why it exists |
        |---|---|---|---|
        | **HEDIS** | NCQA's measure set for health plans: effectiveness of care, access, utilization. | Health plans (the payer side), with data often demanded from providers. | Plan accreditation and purchaser comparison; payer quality bonuses run through it. |
        | **MIPS** | CMS's Merit-based Incentive Payment System: quality, cost, improvement activities, promoting interoperability. | Individual clinicians and groups billing Medicare Part B. | Adjusts Medicare payment up or down based on performance. |
        | **eCQMs** | Electronic clinical quality measures: measure logic computed directly from structured EHR data. | Hospitals and clinicians, through certified EHR technology, into CMS programs. | Replaces manual chart abstraction with computation. Validity is capped by the structured-data capture underneath, which is the informaticist's part. |
        | **Hospital IQR** | CMS's hospital inpatient quality reporting program. | Hospitals, on the inpatient side. | Ties the annual Medicare payment update to reporting and feeds public reporting on Care Compare. |

        The working consequence: every framework's number is computed from data capture and measure logic someone has to design, validate, and maintain. That someone is the informaticist, which is why the quality department and the informatics team share a backlog.
        """
    )
    return


@app.cell
def _(mo):
    quiz2 = mo.ui.radio(
        options=[
            "HEDIS",
            "MIPS",
            "eCQMs reported through certified EHR technology",
            "Hospital inpatient quality reporting (IQR)",
        ],
        label=(
            "Helios's largest commercial payer offers the medical group a quality bonus tied to the share "
            "of the payer's RA members on disease-modifying therapy. Which framework does that bonus run through?"
        ),
    )
    quiz2
    return (quiz2,)


@app.cell
def _(mo, quiz2):
    if quiz2.value is None:
        _fb2 = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif quiz2.value == "HEDIS":
        _fb2 = mo.callout(
            mo.md(
                "**Correct.** A commercial payer's quality bonus runs through HEDIS, the payer-side measure set: the plan is measured on its membership, and it passes the incentive (and the data demands) down to provider groups. MIPS is CMS's clinician-side program for Medicare Part B, hospital IQR covers the inpatient side, and an eCQM is a computation mechanism rather than a bonus program, though the plan may accept eCQM-derived data as evidence."
            ),
            kind="success",
        )
    else:
        _fb2 = mo.callout(
            mo.md(
                "**Check who holds the measure.** The bonus comes from a commercial payer and is computed on the payer's member population, which is the HEDIS structure: NCQA's plan-side measure set, with incentives and data requests passed down to provider groups. MIPS is CMS's clinician-side program, hospital IQR is CMS's inpatient program, and an eCQM is a computation mechanism, not a payer bonus program."
            ),
            kind="warn",
        )
    _fb2
    return


@app.cell
def _(mo):
    mo.vstack(
        [
            mo.md(
                r"""
                ## Dashboards are informatics artifacts

                A dashboard is a designed product with an audience, a refresh cadence, a data lineage, an owner, and a retirement plan: the same lifecycle discipline as the alert itself. Three design rules carry from this track. Every number appears with its time series and limits, never as a lone point estimate (the anti-tampering rule). Every KPI carries a stated target and a named owner. And the page answers the audience's decision, which for the CMO is "intervene, watch, or celebrate," not "browse."
                """
            ),
            mo.callout(
                mo.md(
                    "**Callback to Course 08: Clinical visualization.** Course 08 covers the visual craft underneath the one-pager: chart-type selection, uncertainty display, and the misleading patterns (truncated axes, cherry-picked windows) that quality dashboards are notorious for. This track decides what goes on the page; Course 08 decides how it is drawn."
                ),
                kind="neutral",
            ),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Build the one-pager: the KPI selector

        Below are 20 candidate KPIs for the RA-CDS dashboard. Each carries hidden tags: process or outcome, leading or lagging, and whether the RA-CDS can credibly claim it. Select the 5 to 7 you would put in front of the CMO. The feedback evaluates the mix, then reveals the tags and target thresholds for your selection.
        """
    )
    return


@app.cell
def _(mo):
    KPI_CATALOG = {
        "Alert override rate": {"type": "process", "timing": "leading", "scope": "RA-CDS", "target": "within the 50 to 70% band on the weekly control chart"},
        "Alerts fired per week": {"type": "process", "timing": "leading", "scope": "RA-CDS", "target": "4 to 8 per week (about 310 patients alerted per year)"},
        "Percentage of alerts acted on": {"type": "process", "timing": "leading", "scope": "RA-CDS", "target": "40% or higher"},
        "Median days from alert to escalation conversation": {"type": "process", "timing": "leading", "scope": "RA-CDS", "target": "14 days or fewer"},
        "Treat-to-target intensification within 90 days (eligible patients)": {"type": "process", "timing": "leading", "scope": "RA-CDS", "target": "50% or higher"},
        "CDS service response time (p95)": {"type": "process", "timing": "leading", "scope": "RA-CDS", "target": "under 2 seconds"},
        "Alerts fired on patients without active RA": {"type": "process", "timing": "leading", "scope": "RA-CDS", "target": "under 2% of firings"},
        "Structured joint-count capture rate at rheumatology visits": {"type": "process", "timing": "leading", "scope": "RA-CDS", "target": "80% or higher"},
        "PROM completion rate on the RA panel": {"type": "process", "timing": "leading", "scope": "RA-CDS", "target": "60% or higher"},
        "Rheumatologist training completion": {"type": "process", "timing": "leading", "scope": "RA-CDS", "target": "100% before card access"},
        "Portal activation rate on the RA panel": {"type": "process", "timing": "leading", "scope": "RA-CDS", "target": "70% or higher"},
        "90-day flare rate among alerted patients": {"type": "outcome", "timing": "lagging", "scope": "RA-CDS", "target": "below the matched pre-launch baseline by month 12"},
        "Moderate-to-severe disease-activity prevalence at 12 months": {"type": "outcome", "timing": "lagging", "scope": "RA-CDS", "target": "10% relative reduction"},
        "Mean DAS28 across the cohort": {"type": "outcome", "timing": "lagging", "scope": "RA-CDS", "target": "downward trend across quarters"},
        "RA-flare ED visits and admissions per 100 patient-years": {"type": "outcome", "timing": "lagging", "scope": "RA-CDS", "target": "15% reduction by month 12"},
        "Rheumatologist satisfaction with the alert": {"type": "outcome", "timing": "leading", "scope": "RA-CDS", "target": "3.5 of 5 or higher on the quarterly survey"},
        "HCAHPS top-box communication score": {"type": "outcome", "timing": "lagging", "scope": "system-level", "target": "system scorecard; not attributable to the RA-CDS"},
        "30-day all-cause readmission rate": {"type": "outcome", "timing": "lagging", "scope": "system-level", "target": "system scorecard; not attributable to the RA-CDS"},
        "Hospital mortality O/E ratio": {"type": "outcome", "timing": "lagging", "scope": "system-level", "target": "system scorecard; not attributable to the RA-CDS"},
        "Average inpatient length of stay": {"type": "outcome", "timing": "lagging", "scope": "system-level", "target": "system scorecard; not attributable to the RA-CDS"},
    }
    kpi_pick = mo.ui.multiselect(
        options=list(KPI_CATALOG.keys()),
        label="Select 5 to 7 KPIs for the one-page RA-CDS dashboard",
        full_width=True,
    )
    kpi_pick
    return KPI_CATALOG, kpi_pick


@app.cell
def _(KPI_CATALOG, kpi_pick, mo, pd):
    _sel = list(kpi_pick.value or [])
    if not _sel:
        _out = mo.callout(mo.md("_Select KPIs above to evaluate the mix._"), kind="neutral")
    else:
        _n = len(_sel)
        _types = {KPI_CATALOG[_k]["type"] for _k in _sel}
        _timings = {KPI_CATALOG[_k]["timing"] for _k in _sel}
        _system = [_k for _k in _sel if KPI_CATALOG[_k]["scope"] == "system-level"]
        _issues = []
        if _n < 5:
            _issues.append(
                f"**Too few ({_n}).** A one-pager holds 5 to 7. Below five, the page cannot cover process and outcome at once, and the CMO will ask what you are not showing."
            )
        if _n > 7:
            _issues.append(
                f"**Too many ({_n}).** A one-pager holds 5 to 7. At {_n}, every number gets a glance and none gets a decision; the surplus belongs in the appendix the CMO never opens."
            )
        if _types == {"process"}:
            _issues.append(
                "**All process.** The CMO sees activity, not impact: alerts fired, alerts acted on, capture rates. At least one outcome measure (flare rate, disease-activity prevalence) has to anchor the page to the clinical change the alert exists to produce."
            )
        if _types == {"outcome"}:
            _issues.append(
                "**All outcome.** Impact with no handle to turn. When the flare rate disappoints, the page offers no process measure to say where the chain broke: firing, action, or scheduling."
            )
        if "leading" not in _timings:
            _issues.append(
                "**No leading indicators.** Everything on this page confirms after the fact. The first honest reading arrives around month 9, far too late to steer; the override and acted-on rates would have warned by week 4."
            )
        if _system:
            _issues.append(
                "**Attribution problem: "
                + ", ".join(_system)
                + ".** These move with hundreds of forces across the institution; a one-page RA-CDS dashboard cannot credibly claim them. They belong on the system scorecard, not here."
            )
        if _issues:
            _verdict = mo.callout(mo.md("\n\n".join(_issues)), kind="warn")
        else:
            _verdict = mo.callout(
                mo.md(
                    f"**The mix works.** {_n} KPIs, process and outcome both present, at least one leading indicator for early warning, and nothing the RA-CDS cannot credibly claim. Pair each number with its time series and limits on the page itself; the table below shows the revealed tags and targets."
                ),
                kind="success",
            )
        _preview = pd.DataFrame(
            [{"KPI": _k, "type": KPI_CATALOG[_k]["type"], "timing": KPI_CATALOG[_k]["timing"], "target": KPI_CATALOG[_k]["target"]} for _k in _sel]
        )
        _preview.index = range(1, len(_preview) + 1)
        _preview.index.name = "row"
        _out = mo.vstack([_verdict, mo.md("**Dashboard preview, tags and targets revealed:**"), _preview])
    _out
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The artifact: the KPI dashboard mockup

        This track's artifact is the one-page KPI dashboard mockup with target thresholds. The worked version below is the reference answer to the CMO's request; the course capstone collects this mockup, with your own selection and targets, as the KPI section of the implementation plan.

        | KPI | Type | Timing | Target | Display |
        |---|---|---|---|---|
        | Alert override rate | process | leading | within the 50 to 70% band | weekly control chart |
        | Percentage of alerts acted on | process | leading | 40% or higher | weekly run chart |
        | Median days from alert to escalation conversation | process | leading | 14 days or fewer | monthly run chart |
        | Treat-to-target intensification within 90 days | process | leading | 50% or more of eligible patients | quarterly run chart |
        | 90-day flare rate among alerted patients | outcome | lagging | below matched pre-launch baseline by month 12 | quarterly control chart |
        | Rheumatologist satisfaction with the alert | outcome | leading | 3.5 of 5 or higher | quarterly survey trend |

        Every row displays as a time series with its center line and limits, per the anti-tampering rule. The page footer names the data lineage (the warehouse marts each number comes from) and the owner, who is you.

        Two threads continue from here. Track 5 prices what this dashboard observes: the averted flares feed the ROI model, and the monitoring that keeps these numbers trustworthy is a recurring budget line. Track 8 operates it: the monthly operations review reads this page, and a week-15-style shift routes to QI investigation, not to the help-desk queue.
        """
    )
    return


if __name__ == "__main__":
    app.run()
