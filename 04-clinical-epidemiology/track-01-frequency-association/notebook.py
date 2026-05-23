"""Track 01: Measures of frequency and association.

Most clinicians can recite the definitions of incidence, prevalence,
relative risk, odds ratio, and hazard ratio. Few can tell you, in plain
English, when each one is the right number to compute and what changes
when the cohort changes. This notebook is a thinking course, not a stats
course: every measure is defined inline, every formula is shown
operating on a real synthetic cohort of RA patients, and the cohort
itself is interactive so the learner can watch the measures shift as
they narrow it.
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

    rng = np.random.default_rng(20260518)
    return alt, mo, np, pd, rng


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 01: Measures of frequency and association

        ## Five measures

        Five measures appear in nearly every clinical paper. Each answers a slightly different question, and each has its own denominator.

        - **Prevalence.** How many people have the condition *right now*.
        - **Incidence.** How many people *develop* the condition over a defined period.
        - **Risk ratio (RR).** How much more likely exposed people are to develop the outcome than unexposed people.
        - **Odds ratio (OR).** How much higher the *odds* are in exposed people than unexposed. The output of case-control studies and logistic regression.
        - **Hazard ratio (HR).** How much faster (or slower) the outcome occurs over time in exposed people than unexposed.

        Confusing them is one of the most common ways clinical papers get misread.

        This track uses a synthetic cohort of 2,000 patients with rheumatoid arthritis, followed for three years, half on a TNF inhibitor and half on conventional synthetic DMARDs alone. The clinical question: *does the TNF inhibitor cohort have more serious infections than the conventional-DMARD cohort?*

        Ms. Reyes (52F, seropositive RA, on MTX + adalimumab) is in there somewhere. The interactivity at the end lets you narrow the cohort and see what shifts.
        """
    )
    return


@app.cell
def _(np, pd, rng):
    # Synthetic RA cohort, n=2000, 3-year follow-up, two treatment arms.
    n = 2000

    age = rng.normal(58, 12, n).clip(25, 85)
    sex = rng.choice(["F", "M"], size=n, p=[0.75, 0.25])
    seropositive = rng.random(n) < 0.70
    disease_duration_yrs = rng.gamma(2.0, 2.5, n).clip(0.5, 25)

    # Half on csDMARD alone, half on csDMARD + TNFi biologic.
    treatment = rng.choice(["csDMARD", "TNFi"], size=n, p=[0.5, 0.5])

    # Generate time-to-serious-infection.
    # Baseline hazard ~0.04 per year (≈12% 3-year risk).
    # Effects: TNFi HR≈1.6, age +1.04/yr above 50, seropositive HR≈1.2.
    age_eff = np.exp(0.04 * (age - 50))
    sero_eff = np.where(seropositive, 1.20, 1.00)
    tnfi_eff = np.where(treatment == "TNFi", 1.60, 1.00)
    rate = 0.040 * age_eff * sero_eff * tnfi_eff

    # Exponential time to event in years.
    t_event = rng.exponential(1.0 / rate)
    censor_at = 3.0

    serious_infection = t_event <= censor_at
    followup_yrs = np.where(serious_infection, t_event, censor_at)

    cohort = pd.DataFrame({
        "patient_id": [f"RA-{i+1:04d}" for i in range(n)],
        "age": age.round(0).astype(int),
        "sex": sex,
        "seropositive": seropositive,
        "disease_duration_yrs": disease_duration_yrs.round(1),
        "treatment": treatment,
        "followup_yrs": followup_yrs.round(2),
        "serious_infection": serious_infection,
    })
    cohort.index = range(1, len(cohort) + 1)
    cohort.index.name = "row"
    return (cohort,)


@app.cell
def _(cohort, mo):
    mo.md(
        rf"""
        ## The cohort we will work with

        Two thousand patients with rheumatoid arthritis. Half on a conventional synthetic DMARD only (think methotrexate). Half on a TNF inhibitor on top of methotrexate. Followed for up to three years. The outcome is *serious infection*: an infection requiring hospitalization.

        First eight rows so you have the shape in your head:

        {mo.as_html(cohort.head(8))}

        Total cohort: {len(cohort):,}. csDMARD arm: {(cohort['treatment']=='csDMARD').sum():,}. TNFi arm: {(cohort['treatment']=='TNFi').sum():,}. Serious infections during follow-up: {int(cohort['serious_infection'].sum())}.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1. Prevalence vs incidence: the time question

        The two simplest measures are also the two most often confused. The difference is entirely about *time*.

        **Prevalence** is a snapshot. "How many of my patients have RA *right now*?" It is a proportion: people with the condition divided by the total population, at a moment in time. Prevalence answers a *load* question. How many hospital beds do I need? How many infusion chairs? How big is this problem in my clinic this morning?

        **Incidence** is a flow. "How many *new* cases of serious infection happened in my RA cohort *over the past year*?" It needs a *denominator* that captures *time at risk*. Incidence answers a *rate* question. Is the rate going up? Is this exposure speeding things up?

        Two ways to count incidence, and which one you use matters:

        - **Cumulative incidence** (a.k.a. *risk*). New cases divided by people at risk at the start of the period. A proportion. "Over 3 years, 18 out of 100 patients got pneumonia, so 3-year cumulative incidence is 18%."
        - **Incidence rate**. New cases divided by total person-time observed. A rate with units of per-person-year. "We saw 18 pneumonias across 240 person-years of follow-up, so the incidence rate is 7.5 per 100 person-years." Incidence rate is what you want when follow-up is unequal across patients, which it almost always is in real cohorts.

        Why the distinction matters: if half your cohort drops out at year 1, cumulative incidence underestimates the risk for anyone who stuck around, and the rate is the only honest summary.
        """
    )
    return


@app.cell
def _(cohort, mo):
    # Compute prevalence and incidence on the full cohort.
    total_n = len(cohort)
    n_event = int(cohort["serious_infection"].sum())
    cum_inc = n_event / total_n
    person_yrs = cohort["followup_yrs"].sum()
    inc_rate = n_event / person_yrs

    # Prevalence example: seropositive RA among the cohort.
    n_sero = int(cohort["seropositive"].sum())
    prev_sero = n_sero / total_n

    mo.md(
        rf"""
        ### Applied to our cohort

        **Prevalence of seropositive RA in this cohort:** {n_sero:,} of {total_n:,} = **{prev_sero:.1%}**. This is a snapshot. It does not care when anyone became seropositive; it asks how many *are* right now.

        **3-year cumulative incidence of serious infection:** {n_event:,} events / {total_n:,} at-risk patients at the start = **{cum_inc:.1%}**. This is the simple risk number. It is the right number for talking to a patient about their next three years if they entered the cohort today and you can assume nobody drops out.

        **Incidence rate of serious infection:** {n_event:,} events / {person_yrs:,.0f} person-years = **{inc_rate*100:.1f} per 100 person-years**. This is the rate. It honors the fact that patients who had their infection at month six contributed six months of follow-up, while patients who finished the three years uninfected contributed all 36 months. The two numbers carry the same information when follow-up is complete; they diverge when it isn't.
        """
    )
    return cum_inc, inc_rate, n_event, person_yrs, prev_sero, total_n


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2. Risk ratio (RR): the headline number from a cohort study

        Two groups, exposed and unexposed. Each has a risk of the outcome over some defined period. The **risk ratio** is just one divided by the other.

        $$\text{RR} = \frac{\text{risk in exposed}}{\text{risk in unexposed}}$$

        - RR = 1: same risk.
        - RR > 1: exposure increases the risk.
        - RR < 1: exposure decreases the risk.

        RR is the most clinically intuitive measure of association. "Patients on the new drug are 1.5 times as likely to have a serious infection over three years" is something you can say at the bedside.

        Two warnings the rest of medicine gets wrong:

        1. **RR collapses time.** It is a comparison of two cumulative incidences over the same fixed interval. You cannot compute it cleanly if follow-up is unequal. Use the hazard ratio for that.
        2. **A large RR on a tiny absolute risk is still a tiny absolute risk.** A doubling of a 1-in-10,000 risk is still 2 in 10,000. Always look at the *absolute* numbers before reacting to the *relative* number.
        """
    )
    return


@app.cell
def _(cohort, mo):
    # Compute 3-year RR for TNFi vs csDMARD.
    exp = cohort[cohort["treatment"] == "TNFi"]
    unexp = cohort[cohort["treatment"] == "csDMARD"]
    risk_exp = exp["serious_infection"].mean()
    risk_unexp = unexp["serious_infection"].mean()
    rr_full = risk_exp / risk_unexp
    rd_full = risk_exp - risk_unexp  # risk difference (absolute)

    mo.md(
        rf"""
        ### Applied to our cohort

        Risk of serious infection over 3 years:

        - **csDMARD arm:** {int(unexp['serious_infection'].sum()):,} / {len(unexp):,} = {risk_unexp:.1%}
        - **TNFi arm:** {int(exp['serious_infection'].sum()):,} / {len(exp):,} = {risk_exp:.1%}

        **Risk ratio (TNFi vs csDMARD):** {risk_exp:.3f} / {risk_unexp:.3f} = **{rr_full:.2f}**

        **Risk difference (absolute):** {risk_exp:.1%} - {risk_unexp:.1%} = **{rd_full*100:+.1f} percentage points**

        A clinician would translate that as: "across three years, the TNFi arm had a {rr_full:.2f}-fold higher risk of serious infection, an absolute difference of about {rd_full*100:.1f} per 100 patients treated." Notice that the relative number sounds bigger than the absolute number feels. Always show both.
        """
    )
    return rd_full, rr_full


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3. Odds ratio (OR): when you cannot compute risk directly

        **Odds** is a different way of expressing probability. If 10 of 50 patients had the event, the *risk* is 10/50 = 0.20. The *odds* is 10/40 = 0.25 (events divided by non-events, not events divided by total). Odds and risk move together but they are not the same number.

        The **odds ratio** is the ratio of two odds:

        $$\text{OR} = \frac{\text{odds in exposed}}{\text{odds in unexposed}}$$

        Why does odds-anything exist? Two reasons.

        1. **Case-control studies.** You sample people *by outcome*: you grab 200 patients with serious infection (cases) and 200 patients without (controls), then look back at exposures. You *cannot* compute risk this way; you chose the cases-to-controls ratio yourself. But you can still compute odds in each group and compare them. The OR is the only association measure a case-control study can give you.

        2. **Logistic regression.** Every logistic-regression coefficient is on the log-odds scale. Exponentiate the coefficient and you have an OR. This is why so many papers report ORs even when the data would have supported an RR. It is a property of the model the authors chose, not always a property of the design.

        **The rare-disease approximation.** When the outcome is uncommon (say, under 10% in both groups), OR ≈ RR. When the outcome is common, the OR exaggerates: an OR of 2 might correspond to an RR of 1.4. Clinicians routinely misread common-outcome ORs as if they were RRs. They aren't.
        """
    )
    return


@app.cell
def _(cohort, mo):
    # Compute OR alongside RR.
    exp_ = cohort[cohort["treatment"] == "TNFi"]
    unexp_ = cohort[cohort["treatment"] == "csDMARD"]
    a = int(exp_["serious_infection"].sum())  # exposed cases
    b = len(exp_) - a  # exposed non-cases
    c = int(unexp_["serious_infection"].sum())  # unexposed cases
    d = len(unexp_) - c  # unexposed non-cases

    or_full = (a * d) / (b * c)
    rr_recomputed = (a / (a + b)) / (c / (c + d))

    mo.md(
        rf"""
        ### Applied to our cohort

        The 2x2 table for treatment vs serious infection over 3 years:

        |             | Serious infection | No serious infection | Total |
        |---|---|---|---|
        | **TNFi**     | {a:,} | {b:,} | {a+b:,} |
        | **csDMARD**  | {c:,} | {d:,} | {c+d:,} |

        - **Odds in TNFi arm:** {a} / {b} = {a/b:.3f}
        - **Odds in csDMARD arm:** {c} / {d} = {c/d:.3f}
        - **Odds ratio:** ({a} × {d}) / ({b} × {c}) = **{or_full:.2f}**
        - **Risk ratio (for comparison):** **{rr_recomputed:.2f}**

        Our outcome is uncommon enough that OR and RR are not far apart, but OR is slightly larger. If you reported the OR in conversation as if it were an RR, you would overstate the relative effect. In a case-control design this OR would have been the only number you could compute; here it's a property of how someone might have analyzed the data, not of the study design.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 4. Hazard ratio (HR): when timing matters

        Risk and odds collapse time. Both treat "an event by year 3" and "an event at month 2" as the same thing. Often you care about *when* the event happened, not just whether it happened. That is the survival-analysis question, and the **hazard ratio** is its answer.

        The **hazard** at a given time is the instantaneous rate of the event happening at that moment, given the patient has made it that far. The hazard ratio compares two hazards:

        $$\text{HR} = \frac{\text{hazard in exposed}}{\text{hazard in unexposed}}$$

        It is usually estimated with a Cox proportional-hazards model. The *proportional-hazards assumption* says the ratio is constant over time. The exposed group is consistently, say, 1.5x as fast to event as the unexposed group, for the whole follow-up window. When the assumption fails (the survival curves cross, or fan out), the HR loses its plain-English meaning.

        **What an HR is and isn't:**

        - HR 1.6 ≈ "events are happening 60% faster in the exposed group, at any given moment."
        - HR is *not* an RR. It is a ratio of rates, not risks. If you really want a 3-year risk number, compute the cumulative incidence directly or read it off a Kaplan-Meier curve.
        - HR is what to report when follow-up time differs between patients (almost always the case), when you care about *when* events happen, and when you want to censor patients who haven't had the event yet.
        """
    )
    return


@app.cell
def _(cohort, mo, np):
    # Crude rate-based HR estimate: incidence-rate ratio between arms.
    # (A full Cox would require lifelines; the incidence-rate ratio is
    # the right intuition and matches the proportional-hazards setup
    # we baked into the data generator.)
    exp_h = cohort[cohort["treatment"] == "TNFi"]
    unexp_h = cohort[cohort["treatment"] == "csDMARD"]

    rate_exp = exp_h["serious_infection"].sum() / exp_h["followup_yrs"].sum()
    rate_unexp = unexp_h["serious_infection"].sum() / unexp_h["followup_yrs"].sum()
    hr_full = rate_exp / rate_unexp

    # Wald-style 95% CI for log-rate-ratio.
    a_e = int(exp_h["serious_infection"].sum())
    a_u = int(unexp_h["serious_infection"].sum())
    se_log = np.sqrt(1/a_e + 1/a_u)
    log_hr = np.log(hr_full)
    ci_lo = np.exp(log_hr - 1.96 * se_log)
    ci_hi = np.exp(log_hr + 1.96 * se_log)

    mo.md(
        rf"""
        ### Applied to our cohort

        Incidence rates by arm:

        - **csDMARD:** {a_u} events over {unexp_h['followup_yrs'].sum():.0f} person-years = {rate_unexp*100:.1f} per 100 person-years.
        - **TNFi:** {a_e} events over {exp_h['followup_yrs'].sum():.0f} person-years = {rate_exp*100:.1f} per 100 person-years.

        **Incidence-rate ratio (≈ HR under proportional hazards):** **{hr_full:.2f}** (95% CI {ci_lo:.2f} to {ci_hi:.2f})

        Read this as: "the TNFi arm has events {hr_full:.2f} times as fast as the csDMARD arm, with a confidence interval that excludes 1." A Cox model on this data (with the same proportional-hazards setup we used to generate it) would give a very similar number; an incidence-rate ratio is the right intuition for the HR when proportional hazards holds.

        We now have all five measures sitting in one place. The interactive cohort builder below lets you watch them shift.
        """
    )
    return


@app.cell
def _(mo):
    age_filter = mo.ui.checkbox(label="Age ≥ 60 only", value=False)
    sero_filter = mo.ui.checkbox(label="Seropositive only", value=False)
    sex_filter = mo.ui.checkbox(label="Female only", value=False)
    duration_filter = mo.ui.checkbox(label="Long-duration RA (>5 years)", value=False)

    mo.md(
        rf"""
        ## 5. Watch the measures shift as the cohort narrows

        Each checkbox below filters the cohort. As you add filters, every measure recomputes. Watch which ones change a lot, which ones change a little, and which ones become impossible to compute.

        {mo.as_html(mo.hstack([age_filter, sero_filter, sex_filter, duration_filter]))}
        """
    )
    return age_filter, duration_filter, sero_filter, sex_filter


@app.cell
def _(age_filter, cohort, duration_filter, np, sero_filter, sex_filter):
    filt = cohort.copy()
    if age_filter.value:
        filt = filt[filt["age"] >= 60]
    if sero_filter.value:
        filt = filt[filt["seropositive"]]
    if sex_filter.value:
        filt = filt[filt["sex"] == "F"]
    if duration_filter.value:
        filt = filt[filt["disease_duration_yrs"] > 5]

    def safe_measures(df):
        if len(df) == 0:
            return None
        exp = df[df["treatment"] == "TNFi"]
        unexp = df[df["treatment"] == "csDMARD"]
        if len(exp) == 0 or len(unexp) == 0:
            return None

        out = {"n": len(df), "n_exp": len(exp), "n_unexp": len(unexp)}
        out["n_events_total"] = int(df["serious_infection"].sum())
        out["py_total"] = df["followup_yrs"].sum()

        risk_e = exp["serious_infection"].mean() if len(exp) else np.nan
        risk_u = unexp["serious_infection"].mean() if len(unexp) else np.nan
        out["risk_exp"] = risk_e
        out["risk_unexp"] = risk_u
        out["rr"] = risk_e / risk_u if risk_u > 0 else np.nan
        out["rd"] = risk_e - risk_u

        a = int(exp["serious_infection"].sum())
        b = len(exp) - a
        c = int(unexp["serious_infection"].sum())
        d = len(unexp) - c
        out["a"], out["b"], out["c"], out["d"] = a, b, c, d
        out["or"] = (a * d) / (b * c) if (b > 0 and c > 0) else np.nan

        py_e = exp["followup_yrs"].sum()
        py_u = unexp["followup_yrs"].sum()
        rate_e = a / py_e if py_e > 0 else np.nan
        rate_u = c / py_u if py_u > 0 else np.nan
        out["rate_exp"] = rate_e
        out["rate_unexp"] = rate_u
        out["hr"] = rate_e / rate_u if (rate_u and rate_u > 0) else np.nan
        out["py_exp"] = py_e
        out["py_unexp"] = py_u

        return out

    m = safe_measures(filt)
    return filt, m


@app.cell
def _(filt, m, mo):
    if m is None:
        view = mo.callout(
            mo.md(
                "**Empty cohort.** The filters you picked produced an empty arm. Loosen one."
            ),
            kind="warn",
        )
    else:
        prev_filt = (filt["seropositive"].sum() / len(filt)) if len(filt) else 0
        view = mo.md(
            rf"""
            ### Filtered cohort: {m['n']:,} patients ({m['n_exp']:,} TNFi, {m['n_unexp']:,} csDMARD)

            | Measure | Value | Plain-English reading |
            |---|---|---|
            | **Prevalence** (seropositive RA within this filtered cohort) | {prev_filt:.1%} | snapshot proportion |
            | **3-year cumulative incidence** of serious infection | {m['n_events_total']/m['n']:.1%} | new cases / starting cohort |
            | **Incidence rate** | {m['n_events_total']/m['py_total']*100:.1f} per 100 PY | new cases / person-time |
            | **Risk ratio (TNFi vs csDMARD)** | {m['rr']:.2f} | risk in exposed ÷ risk in unexposed |
            | **Risk difference** | {m['rd']*100:+.1f} pp | absolute extra risk per 100 |
            | **Odds ratio** | {m['or']:.2f} | odds in exposed ÷ odds in unexposed |
            | **Hazard ratio (rate ratio)** | {m['hr']:.2f} | how much faster events happen in exposed |

            **2x2 table on this filtered cohort:**

            |  | Serious infection | No infection |
            |---|---|---|
            | TNFi | {m['a']} | {m['b']} |
            | csDMARD | {m['c']} | {m['d']} |

            Person-years: TNFi {m['py_exp']:.0f}, csDMARD {m['py_unexp']:.0f}.
            """
        )
    view
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### What to notice as you toggle filters

        Pause on these as you click around:

        - **Prevalence moves the most when you change the definition of the cohort.** That is the whole point: prevalence is a property of the slice you draw. Restrict to seropositive patients and prevalence of seropositive RA jumps to 100%, by construction.
        - **Cumulative incidence of serious infection rises when you restrict to older patients.** Because in this synthetic cohort (as in real life) age is the strongest driver of infection risk.
        - **RR and HR can move in different directions.** As you narrow the cohort, the *baseline risk* in the csDMARD group changes, and an RR computed against a smaller baseline can swing more than the underlying rate ratio. The HR (rate ratio) is more stable because it adjusts for follow-up time.
        - **OR creeps further from RR when events become common.** Restrict to old, seropositive patients and the cumulative incidence climbs; watch OR pull away from RR.
        - **At small cell counts, everything gets noisy.** When the filtered cohort gets to a few hundred patients, the estimates start to bounce. That is not a bug; that is the curve of how much information a cohort actually carries.
        """
    )
    return


@app.cell
def _(mo):
    q1 = mo.ui.radio(
        options=[
            "Prevalence",
            "Incidence rate",
            "Risk ratio",
            "Odds ratio",
            "Hazard ratio",
        ],
        label=(
            "You enrolled 800 RA patients, followed them up for variable lengths "
            "of time (some 6 months, some 4 years) because of staggered enrollment. "
            "You want one number that captures how often serious infections happen "
            "in the cohort, honoring that follow-up time is unequal. Which measure?"
        ),
    )
    q1
    return (q1,)


@app.cell
def _(mo, q1):
    if q1.value is None:
        out1 = mo.md("_Pick one._")
    else:
        correct1 = q1.value == "Incidence rate"
        out1 = mo.callout(
            mo.md(
                rf"""
                **{'Correct.' if correct1 else 'Not quite.'}**

                **Incidence rate** is the only one of these that uses *person-time* in the denominator. That is the entire point of the rate vs the risk: the rate honors unequal follow-up. Cumulative incidence (a *risk*) treats everyone as if they had the same look-back window. RR, OR, and HR are *comparisons between groups*, not summaries of a single cohort.
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
            "RR ≈ OR because the outcome is rare here",
            "OR > RR because the outcome is common here",
            "They will be equal by construction",
            "You cannot say without seeing the confidence intervals",
        ],
        label=(
            "A paper reports a 40% cumulative incidence of post-operative atelectasis "
            "in both arms of a trial, with an odds ratio of 1.8 for the intervention. "
            "What can you say about the relationship between this OR and the RR you "
            "would have gotten from the same data?"
        ),
    )
    q2
    return (q2,)


@app.cell
def _(mo, q2):
    if q2.value is None:
        out2 = mo.md("_Pick one._")
    else:
        correct2 = q2.value == "OR > RR because the outcome is common here"
        out2 = mo.callout(
            mo.md(
                rf"""
                **{'Correct.' if correct2 else 'Not quite.'}**

                A 40% cumulative incidence is *not rare*. When the outcome is common, **the OR always exaggerates the RR**. An OR of 1.8 here probably corresponds to an RR closer to 1.4. This is one of the most common misreadings in the literature: clinicians read a logistic-regression OR and quote it as if it were a relative risk, and at common-outcome rates that reading inflates the effect.
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

        Pick one of the two prompts below and write 4 to 6 sentences in the box that follows. Save what you write somewhere outside the browser. Nothing here is graded or persisted; the box is a scratch pad that lets you compose the answer in place. When you are done, continue to `track-02-bias`.

        1. **Take a paper you have read recently** (clinical trial or observational). Which of the five measures does it report? Was it the right one for the question the authors were asking? If they had been forced to report a different one, would the paper's headline have changed?

        2. **A vendor is selling your hospital an "infection risk score" that flags inpatients.** They report an OR of 3.5 for high-score vs low-score predicting bloodstream infection. The outcome occurs in about 8% of inpatients in their validation cohort. What do you ask them?
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
            **Go deeper** is in `track-01-frequency-association/go-deeper.md`. The next track (`track-02-bias`) takes a small dataset and adds a confounder, and shows the effect estimate flip.
            """
        ),
        kind="info",
    )
    return


if __name__ == "__main__":
    app.run()
