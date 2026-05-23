"""Track 05: Study designs.

The five-question framework is the spine: name the exposure, name the
outcome, locate the point of observation, name what is being measured,
identify the time component. The first interactive walks the five
questions and returns the matching design. The second draws Kaplan-Meier
curves for two arms under either a clean proportional-hazards scenario
or a curves-cross scenario, with the log-rank p-value computed manually
and the HR interpretation flipped based on whether the proportional-
hazards assumption is plausible.
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

    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd
    from scipy import stats

    rng = np.random.default_rng(20260519)
    return alt, mo, np, pd, rng, stats


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 05: Study designs

        ## Which design could have produced this evidence

        Ms. Reyes's rheumatologist asks: *do RA patients on biologics get more serious infections than those on csDMARDs alone?* The answer depends entirely on the design that produced the evidence.

        - A randomized trial assigned biologic vs csDMARD at random and followed patients for 3 years. Crude infection rates are unbiased estimates of the causal effect.
        - A prospective registry followed real-world RA patients chosen by their rheumatologists. Crude rates are confounded by indication (sicker patients tend to get biologics), and only measured confounders can be adjusted away.
        - A retrospective claims database identified patients on biologics vs csDMARDs in 2022 and counted hospitalizations through 2025. Same logical structure as the prospective registry, but the data were collected for billing and you get what was billed.
        - A case-control study sampled patients hospitalized for serious infection and asked about prior biologic exposure. Gives an odds ratio. Cannot estimate incidence.
        - A cross-sectional survey at one rheum clinic on one day asked patients about both their current biologic status and any infection in the past year. Gives a snapshot association. Cannot establish temporal sequence.
        - A case series described five RA patients who developed serious infections after starting a TNFi. Hypothesis-generating only.

        All six designs answer questions about RA and infection. They give different answers because they ask different questions and admit different biases. This track is about which is which.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1. The six designs

        | Design | What it does | What it gives you | Where it fails |
        |---|---|---|---|
        | **Randomized controlled trial** | Investigators assign exposure at random; follow forward | Unbiased causal effect estimate (within the trial population) | Expensive, slow, narrow eligibility; results may not generalize |
        | **Prospective cohort** | Investigators identify patients by exposure; follow forward | Incidence rates, RR, HR, association with temporal ordering | Confounding (only measured confounders can be adjusted) |
        | **Retrospective cohort** | Same as prospective but uses pre-existing data (EHR, claims) | Faster, cheaper; same measures as prospective | Data quality (was collected for non-research reasons); residual confounding |
        | **Case-control** | Sample by outcome; ask about prior exposure | Odds ratio (efficient for rare outcomes) | Cannot estimate incidence or risk directly; recall and selection bias |
        | **Cross-sectional** | Measure exposure and outcome simultaneously | Prevalence, snapshot associations | No temporal sequence; cannot establish causation; cannot estimate incidence |
        | **Case series** | Describe one or a few patients | Hypothesis-generating | No comparison group; cannot estimate any rate |

        Most of clinical-paper reading is figuring out which row of this table you are on, then matching the claim to what that row's design can support.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2. The five-question framework

        Answer these five and the design is a lookup.

        1. **What is the exposure?** A treatment, a clinical state, a risk factor?
        2. **What is the outcome?** A diagnosis, an event, a value?
        3. **Where is the point of observation?** Do you assign the exposure (RCT), follow patients who already have it (cohort), or look back from people who have the outcome (case-control)?
        4. **What are we measuring?** Prevalence, incidence, association, causation, time-to-event?
        5. **Is there a time component?** Are patients followed forward through time, or is everything captured at one moment?

        The interactive below walks these five and returns the matching design plus the reasoning.
        """
    )
    return


@app.cell
def _(mo):
    exposure_q = mo.ui.radio(
        options=[
            "Assigned at random by the investigator",
            "A pre-existing treatment, condition, or characteristic",
            "Recalled by the patient (or extracted from records) after the outcome",
            "Measured at the same moment as the outcome",
        ],
        label="1. How is the exposure observed?",
        value="A pre-existing treatment, condition, or characteristic",
    )
    direction_q = mo.ui.radio(
        options=[
            "Identify by exposure, follow forward to the outcome",
            "Identify by outcome, look backward to the exposure",
            "Measure both at the same moment, no follow-up",
            "Describe one or a small number of patients",
        ],
        label="2. What is the direction of observation?",
        value="Identify by exposure, follow forward to the outcome",
    )
    data_q = mo.ui.radio(
        options=[
            "Collected prospectively as the study runs",
            "Already exists in EHR, registry, or claims data",
            "Not applicable (RCT or single patients)",
        ],
        label="3. Where does the data come from?",
        value="Collected prospectively as the study runs",
    )
    measure_q = mo.ui.radio(
        options=[
            "Causal effect of the exposure on the outcome",
            "Incidence rate, RR, or HR (time-honoring)",
            "Odds ratio (for a rare outcome)",
            "Prevalence or snapshot association",
            "Hypothesis-generating description",
        ],
        label="4. What are we measuring?",
        value="Incidence rate, RR, or HR (time-honoring)",
    )
    time_q = mo.ui.radio(
        options=[
            "Patients are followed over time (person-time exists)",
            "Everything is observed at one moment (no follow-up)",
        ],
        label="5. Is there a time component?",
        value="Patients are followed over time (person-time exists)",
    )

    mo.vstack([exposure_q, direction_q, data_q, measure_q, time_q])
    return data_q, direction_q, exposure_q, measure_q, time_q


@app.cell
def _(data_q, direction_q, exposure_q, measure_q, mo, time_q):
    def _recommend(exposure, direction, data, measure, time):
        # Case series first (small number of patients).
        if direction.startswith("Describe one"):
            return (
                "Case series (or case report)",
                "A description of one or a small number of patients is by construction a case series. No comparison group, no rates, no causal claims. Use to flag a novel observation; design a different study to test the hypothesis."
            )

        # RCT.
        if exposure.startswith("Assigned at random"):
            return (
                "Randomized controlled trial (RCT)",
                "Random assignment of the exposure makes the arms exchangeable in expectation, which means the crude comparison estimates the causal effect of the exposure on the outcome. RCTs are the cleanest evidence about causation. Generalizability beyond the trial's eligibility criteria is a separate question the design does not answer."
            )

        # Cross-sectional.
        if (time.startswith("Everything is observed at one moment")
            or direction.startswith("Measure both at the same moment")):
            return (
                "Cross-sectional study",
                "Exposure and outcome measured at the same moment, with no follow-up, is by construction cross-sectional. The design is right for prevalence and for associations at a moment; it is wrong for causation (the temporal sequence between exposure and outcome cannot be established) and wrong for incidence (no person-time)."
            )

        # Case-control.
        if direction.startswith("Identify by outcome"):
            return (
                "Case-control study",
                "Sampling by outcome and looking back to exposure is case-control. The design is efficient for rare outcomes where a cohort would need to follow too many people for too long. It gives an odds ratio (not a risk ratio, because the case-to-control ratio is chosen by the investigator, not driven by population prevalence). Recall bias and the choice of controls are the two perennial threats."
            )

        # Cohort (prospective or retrospective).
        if direction.startswith("Identify by exposure"):
            if data.startswith("Already exists"):
                return (
                    "Retrospective cohort study",
                    "Identify patients by exposure status in pre-existing data (EHR, registry, claims), then follow them forward through historical records to the outcome. Same analytic structure as a prospective cohort and the same measures (incidence, RR, HR). The data were collected for clinical or administrative purposes, so the variables you wanted may not all be there; residual confounding is the central threat."
                )
            return (
                "Prospective cohort study",
                "Identify patients by exposure status, then collect outcome data going forward. Gives incidence rates, RR, and HR; the temporal sequence is clean by construction. Confounding by indication (or any unmeasured factor that drives both exposure and outcome) is the central threat. Cross-reference to Track 02 on bias."
            )

        # Fallback for combinations that do not match any clean pattern.
        return (
            "Design does not fit the basic six cleanly",
            "The combination of answers does not point to a single canonical design. Consider whether the study is actually a nested case-control inside a cohort, an ecological study, or a more complex design (cluster RCT, stepped wedge, regression discontinuity)."
        )

    _design, _reasoning = _recommend(
        exposure_q.value,
        direction_q.value,
        data_q.value,
        measure_q.value,
        time_q.value,
    )

    mo.callout(
        mo.md(
            rf"""
            **Recommended design:** {_design}

            **Reasoning:** {_reasoning}
            """
        ),
        kind="success",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3. Longitudinal designs: person-time enables incidence

        Tracks 1 and 2 introduced the incidence rate and the hazard ratio. Those measures need *follow-up time*. A cross-sectional design captures no follow-up and therefore cannot give either.

        **Person-time** is the sum of the time each patient was at risk in the study. A patient followed for 3 years contributes 3 person-years; a patient who had the outcome at year 1 contributes 1 person-year (and stops contributing once the event occurs); a patient who dropped out at month 6 contributes 0.5 person-years. The incidence rate's denominator is total person-time, which is why the rate honors unequal follow-up while cumulative incidence does not.

        **Prospective vs retrospective cohort** is a question of *when the data were collected*, not what design produces. A prospective cohort defines the cohort at baseline and waits. A retrospective cohort reconstructs the same kind of cohort from historical data. Both give incidence, rate, HR, and RR over a time window. The retrospective version is constrained by what was recorded; the prospective version is constrained by what you can afford to wait for.

        Cross-reference to Track 1: the BSRBR cohort study reported in Galloway 2011 used person-years to compute incidence rates of serious infection per 1000 person-years across anti-TNF and csDMARD arms, with an HR for the comparison. The next interactive replicates that kind of analysis in synthetic data.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 4. Survival analysis: KM, censoring, log-rank, HR

        Survival analysis handles time-to-event outcomes with unequal follow-up. The conceptual moves:

        **The Kaplan-Meier estimator** answers: at each time T, what fraction of the original cohort is still event-free? The curve starts at 1.0 (everyone event-free at time 0) and steps down each time an event occurs. Step size is proportional to the fraction of currently-at-risk patients who had the event at that time. A patient who is censored (left the study without having the event) is removed from the at-risk pool but does not cause a step.

        **Censoring is the trickiest idea.** A censored patient is *not* a patient who did not have the event. A censored patient is a patient we do not know about past the censoring time. The KM estimator assumes censoring is independent of the event of interest (a censored patient's future risk is the same as a non-censored patient still at risk at that time). When sicker patients drop out and we treat their dropouts as censoring, the estimator is biased upward (it makes the survival look better than it is).

        **Tick marks on a KM curve indicate censored patients.** A curve dropping off into the future with several tick marks just before should be read with caution; the trailing portion is based on a small at-risk pool.

        **The log-rank test** compares whole curves. At each unique event time, it asks whether events are distributed across groups in proportion to each group's at-risk pool. Summed across all event times, the test gives a chi-square statistic and a p-value. It is the standard unadjusted comparison of two survival curves.

        **The hazard ratio summarizes the comparison into one number.** Cox proportional-hazards regression gives an HR per unit of exposure, with optional covariate adjustment. The HR's plain-English reading: "events are happening X times as fast in group A as in group B, at every moment of follow-up." That depends on the **proportional-hazards (PH) assumption**: the hazard ratio is constant over time. When the assumption holds, the HR is a useful summary. When it fails (the curves cross, fan out, or converge), the HR averages over time in a way that obscures the story.

        The interactive below shows both: a clean PH scenario (the HR is a real summary) and a curves-cross scenario (the HR averages to nothing meaningful).
        """
    )
    return


@app.cell
def _(mo):
    scenario_q = mo.ui.radio(
        options=[
            "Proportional hazards (clean HR)",
            "PH violation (curves cross)",
        ],
        label="Pick a survival scenario:",
        value="Proportional hazards (clean HR)",
    )
    scenario_q
    return (scenario_q,)


@app.cell
def _(alt, mo, np, pd, scenario_q, stats):
    def _make_arm_exponential(rate, n_arm, seed_offset, horizon=5.0, censor_min=2.0):
        _rng_local = np.random.default_rng(20260601 + seed_offset)
        _t_event = _rng_local.exponential(1.0 / rate, n_arm)
        _t_censor = _rng_local.uniform(censor_min, horizon, n_arm)
        _t_obs = np.minimum(_t_event, _t_censor)
        _e_obs = (_t_event <= _t_censor).astype(int)
        return _t_obs, _e_obs

    def _make_arm_piecewise(early_rate, late_rate, breakpoint, n_arm, seed_offset,
                            horizon=5.0, censor_min=2.0):
        _rng_local = np.random.default_rng(20260601 + seed_offset)
        _t_event = np.empty(n_arm)
        for _i in range(n_arm):
            _t_e = _rng_local.exponential(1.0 / early_rate)
            if _t_e < breakpoint:
                _t_event[_i] = _t_e
            else:
                _t_event[_i] = breakpoint + _rng_local.exponential(1.0 / late_rate)
        _t_censor = _rng_local.uniform(censor_min, horizon, n_arm)
        _t_obs = np.minimum(_t_event, _t_censor)
        _e_obs = (_t_event <= _t_censor).astype(int)
        return _t_obs, _e_obs

    def _km(time_arr, event_arr):
        _df = pd.DataFrame({"t": time_arr, "e": event_arr}).sort_values("t").reset_index(drop=True)
        _n_at_risk = len(_df)
        _s = 1.0
        _curve_t = [0.0]
        _curve_s = [1.0]
        _cens_t = []
        _cens_s = []
        for _t in sorted(_df["t"].unique()):
            _at_t = _df[_df["t"] == _t]
            _ev = int((_at_t["e"] == 1).sum())
            _ce = int((_at_t["e"] == 0).sum())
            if _ev > 0:
                _s = _s * (1.0 - _ev / _n_at_risk)
                _curve_t.append(float(_t))
                _curve_s.append(_s)
            for _j in range(_ce):
                _cens_t.append(float(_t))
                _cens_s.append(_s)
            _n_at_risk -= len(_at_t)
        return (np.array(_curve_t), np.array(_curve_s),
                np.array(_cens_t), np.array(_cens_s))

    def _log_rank(t_a, e_a, t_b, e_b):
        _times = np.concatenate([t_a, t_b])
        _events = np.concatenate([e_a, e_b])
        _groups = np.concatenate([np.zeros(len(t_a), dtype=int),
                                  np.ones(len(t_b), dtype=int)])
        _df = pd.DataFrame({"t": _times, "e": _events, "g": _groups}).sort_values("t").reset_index(drop=True)
        _sum_oe = 0.0
        _sum_v = 0.0
        for _t in sorted(_df.loc[_df["e"] == 1, "t"].unique()):
            _at_t = _df[_df["t"] == _t]
            _d_a = int(((_at_t["g"] == 0) & (_at_t["e"] == 1)).sum())
            _d = int((_at_t["e"] == 1).sum())
            _n_a_t = int(((_df["t"] >= _t) & (_df["g"] == 0)).sum())
            _n_b_t = int(((_df["t"] >= _t) & (_df["g"] == 1)).sum())
            _n_t = _n_a_t + _n_b_t
            if _n_t <= 1 or _d == 0:
                continue
            _e_exp = _n_a_t * _d / _n_t
            _v = (_n_a_t * _n_b_t * _d * (_n_t - _d)) / (_n_t * _n_t * (_n_t - 1))
            _sum_oe += _d_a - _e_exp
            _sum_v += _v
        if _sum_v == 0:
            return 0.0, 1.0
        _z2 = _sum_oe ** 2 / _sum_v
        _p = float(1.0 - stats.chi2.cdf(_z2, df=1))
        return float(_z2), _p

    def _irr(t_a, e_a, t_b, e_b):
        _pt_a = float(t_a.sum())
        _pt_b = float(t_b.sum())
        _ev_a = int(e_a.sum())
        _ev_b = int(e_b.sum())
        if _pt_a == 0 or _pt_b == 0 or _ev_a == 0:
            return float("nan"), float("nan"), float("nan")
        _rate_a = _ev_a / _pt_a
        _rate_b = _ev_b / _pt_b
        return _rate_b / _rate_a, _rate_a, _rate_b

    # Build the two arms based on the scenario picker.
    _n = 150 if scenario_q.value.startswith("Proportional") else 120
    if scenario_q.value.startswith("Proportional"):
        _t_a, _e_a = _make_arm_exponential(0.30, _n, seed_offset=0)
        _t_b, _e_b = _make_arm_exponential(0.30 * 1.8, _n, seed_offset=10)
        _label_a = "csDMARD"
        _label_b = "TNFi"
        _scenario_note = (
            "Both arms are simulated under a constant hazard: csDMARD at 0.30 events "
            "per person-year, TNFi at 0.54 events per person-year (a true HR of 1.8). "
            "Patients are censored at administratively-set times between years 2 and 5. "
            "The proportional-hazards assumption holds by construction; the HR is a "
            "real summary of the difference between the arms."
        )
    else:
        _t_a, _e_a = _make_arm_exponential(0.25, _n, seed_offset=20)
        _t_b, _e_b = _make_arm_piecewise(0.55, 0.08, 1.0, _n, seed_offset=30)
        _label_a = "csDMARD"
        _label_b = "TNFi (early-risk pattern)"
        _scenario_note = (
            "The csDMARD arm has a constant hazard of 0.25 events per person-year. "
            "The TNFi arm has a *time-varying* hazard: 0.55 events per person-year for "
            "the first 12 months on therapy, dropping to 0.08 events per person-year "
            "thereafter (the pattern Galloway 2011 BSRBR documented for anti-TNF "
            "infection risk). The hazard ratio is **not constant** over time; the "
            "proportional-hazards assumption fails. A single Cox HR averages over "
            "time in a way that misses the early-risk story."
        )

    _curve_a = _km(_t_a, _e_a)
    _curve_b = _km(_t_b, _e_b)
    _z2, _p = _log_rank(_t_a, _e_a, _t_b, _e_b)
    _irr_val, _rate_a, _rate_b = _irr(_t_a, _e_a, _t_b, _e_b)

    # Survival-curve dataframe. Step-after interpolation makes the
    # canonical descending staircase.
    _curve_rows = []
    for _t, _s in zip(_curve_a[0], _curve_a[1]):
        _curve_rows.append({"time": float(_t), "survival": float(_s), "group": _label_a})
    for _t, _s in zip(_curve_b[0], _curve_b[1]):
        _curve_rows.append({"time": float(_t), "survival": float(_s), "group": _label_b})
    _curve_df = pd.DataFrame(_curve_rows)

    _cens_rows = []
    for _t, _s in zip(_curve_a[2], _curve_a[3]):
        _cens_rows.append({"time": float(_t), "survival": float(_s), "group": _label_a})
    for _t, _s in zip(_curve_b[2], _curve_b[3]):
        _cens_rows.append({"time": float(_t), "survival": float(_s), "group": _label_b})
    _cens_df = pd.DataFrame(_cens_rows)

    _km_lines = (
        alt.Chart(_curve_df)
        .mark_line(interpolate="step-after", strokeWidth=2.5)
        .encode(
            x=alt.X("time:Q", title="Time (years)", scale=alt.Scale(domain=[0, 5])),
            y=alt.Y("survival:Q", title="Fraction event-free", scale=alt.Scale(domain=[0, 1])),
            color=alt.Color(
                "group:N",
                title="Arm",
                scale=alt.Scale(
                    domain=[_label_a, _label_b],
                    range=["#1f77b4", "#d62728"],
                ),
            ),
        )
    )
    _km_ticks = (
        alt.Chart(_cens_df)
        .mark_tick(thickness=2, size=10)
        .encode(
            x="time:Q",
            y="survival:Q",
            color=alt.Color("group:N", legend=None),
        )
    )
    _km_chart = (
        alt.layer(_km_lines, _km_ticks)
        .properties(width=620, height=320, title="Kaplan-Meier survival curves (ticks = censored patients)")
    )

    _interp = (
        "**Both tests agree, and the HR is a useful summary.** The two arms are "
        f"separated cleanly. The crude rate ratio ({_irr_val:.2f}) is close to the "
        "true HR (1.80) baked into the data, with the small difference reflecting "
        "sampling variability at n=150 per arm. A Cox model on this data would "
        "report a similar HR with a confidence interval excluding 1."
        if scenario_q.value.startswith("Proportional")
        else "**The HR averages over time and misses the story.** The crude rate "
             f"ratio is {_irr_val:.2f}, essentially 1.0, and the log-rank p-value "
             f"is {_p:.3f} (not significant). A reader who saw only those numbers "
             "would conclude TNFi has no effect on infection. But the curves cross: "
             "TNFi has a *higher* hazard during the first 12 months (early infection "
             "risk on biologic induction) and a *lower* hazard thereafter (once "
             "patients stabilize). A single HR cannot describe two different effects "
             "depending on time. Report the curves themselves, and consider a "
             "time-stratified analysis or a non-PH model."
    )

    mo.vstack([
        mo.md(_scenario_note),
        mo.as_html(_km_chart),
        mo.md(rf"""
        ### Summary statistics

        | Measure | {_label_a} | {_label_b} |
        |---|---|---|
        | n | {_n} | {_n} |
        | events | {int(_e_a.sum())} | {int(_e_b.sum())} |
        | person-years | {_t_a.sum():.1f} | {_t_b.sum():.1f} |
        | rate per person-year | {_rate_a:.3f} | {_rate_b:.3f} |

        | Comparison | Value |
        |---|---|
        | Crude rate ratio ({_label_b} vs {_label_a}) | **{_irr_val:.2f}** |
        | Log-rank chi-square | {_z2:.2f} |
        | Log-rank p-value | **{_p:.4f}** |

        {_interp}
        """),
    ])
    return


@app.cell
def _(mo):
    q1 = mo.ui.radio(
        options=[
            "Randomized controlled trial.",
            "Prospective cohort.",
            "Retrospective cohort.",
            "Case-control study.",
            "Cross-sectional study.",
        ],
        label=(
            "You want to estimate the 5-year incidence of serious infection "
            "in RA patients on TNFi using existing data from a national "
            "rheumatology registry that recorded biologic exposure at "
            "enrollment in 2018 and tracked hospitalizations through 2023. "
            "Which design is this?"
        ),
    )
    q1
    return (q1,)


@app.cell
def _(mo, q1):
    if q1.value is None:
        out1 = mo.md("_Pick one._")
    else:
        correct1 = q1.value.startswith("Retrospective cohort")
        out1 = mo.callout(
            mo.md(
                rf"""
                **{'Correct.' if correct1 else 'Not quite.'}**

                The five-question walk: (1) exposure is a pre-existing treatment (biologic at enrollment); (2) the direction is identify-by-exposure then follow forward to outcome; (3) the data already exist in the registry by the time the study starts; (4) the question is 5-year incidence (a time-honoring measure requiring person-years); (5) there is a time component (5-year follow-up). That points to a **retrospective cohort study**. Same analytic structure as a prospective cohort and the same measures (incidence, RR, HR). The "retrospective" label is just about when the data were collected relative to study planning; the study itself looks forward through historical records.
                """
            ),
            kind="success" if correct1 else "warn",
        )
    out1
    return


@app.cell
def _(mo):
    q2 = mo.ui.radio(
        options=[
            "Patient 7 did not have the event, so they survived.",
            "Patient 7 had the event at some time after their last follow-up.",
            "Patient 7 left the study at the censoring time; their event status after that is unknown.",
            "Patient 7's data should be excluded from the analysis.",
        ],
        label=(
            "A Kaplan-Meier curve shows a tick mark on the TNFi arm at "
            "month 18 for Patient 7. The Patient 7 row in the dataset has "
            "time = 18 months, event = 0. What does this mean about Patient 7?"
        ),
    )
    q2
    return (q2,)


@app.cell
def _(mo, q2):
    if q2.value is None:
        out2 = mo.md("_Pick one._")
    else:
        correct2 = q2.value.startswith("Patient 7 left the study at the censoring time")
        out2 = mo.callout(
            mo.md(
                rf"""
                **{'Correct.' if correct2 else 'Not quite.'}**

                The censor tick at month 18 means Patient 7's follow-up ended at 18 months *without* the event having occurred *up to that point*. It does not mean Patient 7 survived (they may have had the event at month 19, the day after their last visit, and we would not know). It also does not mean they should be excluded; their 18 months of event-free follow-up are real information and contribute to the at-risk pool through that time. The KM estimator handles this by removing Patient 7 from the at-risk denominator after month 18 but assuming their future risk would have been the same as the other still-at-risk patients. Censoring is *not* the same as "no event"; it is "we ran out of follow-up." Most KM-curve misreadings come from collapsing the two.
                """
            ),
            kind="success" if correct2 else "warn",
        )
    out2
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Reflection

        Pick one of the two prompts below and write 4 to 6 sentences in the box that follows. Save what you write outside the browser; the box is a scratch pad, not persistent storage. When you are done, continue to the course capstone.

        1. **Take a clinical paper you've read recently** that reports a hazard ratio. Look at its Kaplan-Meier figure. Do the curves diverge in a roughly parallel way, or do they cross or fan out? Does the reported HR plausibly summarize the comparison, or does the figure tell a different story than the headline number?

        2. **You're asked to design a study** to test whether a new biologic causes a higher rate of opportunistic infection than standard care. List two reasons you'd prefer a retrospective cohort to a prospective cohort (and two reasons you'd prefer the opposite). What would each choice cost you?
        """
    )
    return


@app.cell
def _(mo):
    reflection = mo.ui.text_area(
        placeholder="Write 4-6 sentences here. Your text stays in your browser; copy it out if you want to keep it.",
        rows=8,
        full_width=True,
    )
    reflection
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            r"""
            **Go deeper** is in `track-05-study-designs/go-deeper.md`. Course 04 closes with a Socratic capstone: given a synthetic observational RA dataset, identify the three biggest threats to validity in a naive analysis and propose how you would address each one.
            """
        ),
        kind="info",
    )
    return


if __name__ == "__main__":
    app.run()
