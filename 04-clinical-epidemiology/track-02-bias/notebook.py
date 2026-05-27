"""Track 02: Bias.

The number you see in a paper can be the wrong number. This notebook
names the three families of bias (selection, information, confounding),
introduces DAGs as the visual grammar, and presents what happens when
the analysis adjusts for a confounder, a mediator, or a collider. The
same 2,000-patient RA cohort from Track 01 is reused, with prednisone
co-use explicitly tracked so the confounded estimate is visible as it
moves.
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
        # Track 02: Bias

        ## The number you see can be the wrong number

        Track 01 left us with a single working number: a hazard ratio of about 1.60 for serious infection on a TNF inhibitor versus a conventional synthetic DMARD. We computed it on a clean synthetic cohort where we *knew* the true causal effect was 1.60, because we baked it in. In the real world the truth is hidden, and the number that comes out of the analysis says whatever the design and the model force it to say.

        This track makes three things explicit:

        1. The three classical families of bias (selection, information, confounding) and how each corrupts an estimate.
        2. The visual grammar (DAGs) for reasoning about bias before doing any math.
        3. The three roles a covariate can play (confounder, mediator, collider) and what happens when you adjust for each one.

        We reuse the 2,000-patient RA cohort from Track 01, with one variable added back in that Track 01 quietly hid: **prednisone co-use**. Prednisone is a confounder of the TNFi-infection question. Once it is on the diagram, the crude number we computed in Track 01 starts to look different from the truth.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1. The three families of bias

        **Selection bias** is when the way patients enter or leave the study depends on both the exposure and the outcome. Examples: studying current heart-failure patients misses the ones who died early (incidence-prevalence bias); patients who choose a new therapy are systematically healthier than those who don't (healthy-user bias); studying hospitalized patients distorts associations because having two conditions makes you more likely to be admitted (Berkson's bias, structurally a collider problem we revisit below).

        **Information bias** is when the *measurement* of exposure, outcome, or covariate is systematically wrong. Examples: mothers of children with congenital anomalies recall pregnancy exposures more completely than mothers of healthy children (recall bias); patients on a new immunosuppressant get more lab draws, so infections that would have gone unnoticed get caught only in that arm (surveillance bias); chart-abstraction of "serious infection" is adjudicated more thoroughly in the experimental arm of a trial than in the control arm (ascertainment bias).

        **Confounding** is when a variable that is a cause of the outcome is also associated with the exposure, but is not on the causal pathway between them. The crude exposure-outcome association then mixes the real effect of the exposure with the effect of the confounder. The single most consequential example in observational drug research is *confounding by indication*: sicker patients get more aggressive therapy AND have worse outcomes, so the therapy looks worse than it is.

        This notebook focuses on confounding because confounding is where DAGs are most useful and where adjustment decisions actually live. Selection bias and information bias are usually fought at the design stage. Confounding is fought partly at design (randomization, restriction, matching) and partly at analysis (stratification, regression, propensity scores), and the analysis decisions are where most clinicians make their reading mistakes.
        """
    )
    return


@app.cell
def _(np, pd, rng):
    # Track 01 cohort, rebuilt with prednisone explicit and treatment
    # assignment depending on prednisone. The true causal HR for TNFi
    # remains 1.60 (same as Track 01). Crude analysis will inflate it.
    n = 2000

    age = rng.normal(58, 12, n).clip(25, 85)
    sex = rng.choice(["F", "M"], size=n, p=[0.75, 0.25])
    seropositive = rng.random(n) < 0.70
    disease_duration_yrs = rng.gamma(2.0, 2.5, n).clip(0.5, 25)

    # Prednisone use, proxying disease severity: more sero, longer
    # duration → more likely on chronic steroids. Overall about 35%.
    p_pred = 0.18 + 0.20 * seropositive + 0.15 * (disease_duration_yrs > 5)
    p_pred = p_pred.clip(0.05, 0.85)
    prednisone = rng.random(n) < p_pred

    # Treatment assignment confounded by prednisone:
    # P(TNFi | pred) = 0.80, P(TNFi | no pred) = 0.30.
    p_tnfi = np.where(prednisone, 0.80, 0.30)
    treatment = np.where(rng.random(n) < p_tnfi, "TNFi", "csDMARD")

    # Hazard model: baseline 0.030/yr, age effect, sero 1.20x, TNFi 1.60x
    # (the true causal effect), prednisone 1.80x (direct biological effect).
    age_eff = np.exp(0.04 * (age - 50))
    sero_eff = np.where(seropositive, 1.20, 1.00)
    tnfi_eff = np.where(treatment == "TNFi", 1.60, 1.00)
    pred_eff = np.where(prednisone, 1.80, 1.00)
    rate = 0.030 * age_eff * sero_eff * tnfi_eff * pred_eff

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
        "prednisone": prednisone,
        "treatment": treatment,
        "followup_yrs": followup_yrs.round(2),
        "serious_infection": serious_infection,
    })
    cohort.index = range(1, len(cohort) + 1)
    cohort.index.name = "row"
    return (cohort,)


@app.cell
def _(cohort, mo):
    n_pred = int(cohort["prednisone"].sum())
    n_tnfi = int((cohort["treatment"] == "TNFi").sum())
    n_pred_tnfi = int(((cohort["prednisone"]) & (cohort["treatment"] == "TNFi")).sum())
    n_nopred_tnfi = int(((~cohort["prednisone"]) & (cohort["treatment"] == "TNFi")).sum())
    p_tnfi_given_pred = n_pred_tnfi / max(n_pred, 1)
    p_tnfi_given_nopred = n_nopred_tnfi / max(len(cohort) - n_pred, 1)

    mo.md(
        rf"""
        ## 2. The cohort, with the confounder visible

        Same 2,000 patients as Track 01, with one column added: `prednisone` (chronic low-dose oral corticosteroid for disease control). About a third of patients are on prednisone. Sicker patients (seropositive, long-duration) are more likely to be on prednisone, and rheumatologists are more likely to step those patients up to a TNFi.

        The first eight rows:

        {mo.as_html(cohort.head(8))}

        Totals: {len(cohort):,} patients; {n_pred:,} on prednisone ({n_pred/len(cohort):.0%}); {n_tnfi:,} on TNFi ({n_tnfi/len(cohort):.0%}); {int(cohort['serious_infection'].sum())} serious infections during follow-up.

        **The relationship between prednisone and TNFi assignment** is the confounding mechanism. In this cohort:

        - P(TNFi | on prednisone) = **{p_tnfi_given_pred:.0%}**
        - P(TNFi | not on prednisone) = **{p_tnfi_given_nopred:.0%}**

        Patients on prednisone are about {p_tnfi_given_pred / p_tnfi_given_nopred:.1f} times as likely to be on a TNFi as patients not on prednisone. Prednisone also independently increases infection risk. Those two facts together are the textbook ingredients for confounding.
        """
    )
    return


@app.cell
def _(cohort):
    # Crude incidence-rate ratio (TNFi vs csDMARD), ignoring prednisone.
    def irr(df, exposure_col, exposure_val, control_val, event_col, py_col):
        exp = df[df[exposure_col] == exposure_val]
        unexp = df[df[exposure_col] == control_val]
        a = int(exp[event_col].sum())
        c = int(unexp[event_col].sum())
        py_e = float(exp[py_col].sum())
        py_u = float(unexp[py_col].sum())
        if py_e == 0 or py_u == 0 or c == 0:
            return None
        rate_e = a / py_e
        rate_u = c / py_u
        return {
            "a": a, "c": c,
            "py_exp": py_e, "py_unexp": py_u,
            "rate_exp": rate_e, "rate_unexp": rate_u,
            "irr": rate_e / rate_u,
        }

    crude = irr(cohort, "treatment", "TNFi", "csDMARD",
                "serious_infection", "followup_yrs")

    # Stratum-specific IRRs, separately within prednisone strata.
    stratum_no = irr(cohort[~cohort["prednisone"]], "treatment", "TNFi",
                     "csDMARD", "serious_infection", "followup_yrs")
    stratum_yes = irr(cohort[cohort["prednisone"]], "treatment", "TNFi",
                      "csDMARD", "serious_infection", "followup_yrs")

    # Mantel-Haenszel pooled IRR across the two prednisone strata.
    # MH-IRR = sum_k (a_k * PY_unexp_k / PY_total_k)
    #       / sum_k (c_k * PY_exp_k / PY_total_k).
    num = 0.0
    den = 0.0
    for s in (stratum_no, stratum_yes):
        py_total = s["py_exp"] + s["py_unexp"]
        num += s["a"] * s["py_unexp"] / py_total
        den += s["c"] * s["py_exp"] / py_total
    mh_irr = num / den

    estimates = {
        "crude": crude,
        "stratum_no": stratum_no,
        "stratum_yes": stratum_yes,
        "mh_irr": mh_irr,
    }
    return (estimates,)


@app.cell
def _(estimates, mo):
    e = estimates
    crude_hr = e["crude"]["irr"]
    s_no = e["stratum_no"]["irr"]
    s_yes = e["stratum_yes"]["irr"]
    mh = e["mh_irr"]

    mo.md(
        rf"""
        ## 3. The crude estimate is inflated. Stratifying fixes it.

        We baked the true TNFi effect into the data generator: hazard ratio 1.60. Watch what the analysis says.

        | Analysis | Hazard ratio (TNFi vs csDMARD) | What it says |
        |---|---|---|
        | **Crude** (ignore prednisone) | **{crude_hr:.2f}** | events are happening {crude_hr:.1f}x as fast in the TNFi arm overall |
        | Stratum: **not on prednisone** | {s_no:.2f} | within this stratum, prednisone doesn't confound: the within-stratum estimate approaches the truth |
        | Stratum: **on prednisone** | {s_yes:.2f} | same idea, within the other stratum |
        | **Mantel-Haenszel pooled** | **{mh:.2f}** | weighted average of the two stratum-specific estimates: this is the adjusted answer |

        The crude analysis would have you tell a patient that TNFi is associated with about a {crude_hr:.1f}-fold higher rate of serious infection. The truth is closer to 1.6. The {crude_hr - mh:.1f} units of excess come entirely from prednisone: TNFi patients are over-represented among prednisone users, prednisone independently increases infection risk, and the crude analysis hands the prednisone effect to the TNFi column.

        This is the central move in confounding adjustment. The within-stratum estimates carry the unconfounded information; the pooled estimate aggregates them; the crude estimate mixes them with the imbalance in the confounder.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 4. DAGs: the visual grammar

        A directed acyclic graph (DAG) is the canonical tool for reasoning about which covariates to adjust for. Three pieces:

        - **Nodes** are variables.
        - **Directed edges** (arrows) are causal effects. An arrow from A to B means A causes B. This is the *causal* claim, not a correlation.
        - **Paths** are sequences of edges. A *causal path* follows arrows from exposure to outcome. A *backdoor path* is a non-causal path from exposure to outcome that starts with an arrow pointing *into* the exposure.

        The "acyclic" requirement means no variable can cause itself through any chain of arrows. The asymmetry of cause and effect is the whole point.

        Two structural rules:

        1. To estimate a clean exposure-outcome effect, *all backdoor paths must be closed*. You close a backdoor path by conditioning on a node along it.
        2. Conditioning is not always good. The same operation that closes one path can *open* another. The role the variable plays determines which.

        The three roles every variable can play (relative to exposure E and outcome Y):
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Three roles, three diagrams

        **Confounder** (common cause of E and Y). Adjust for it.

        ```text
                      prednisone
                       /      \
                      v        v
                    TNFi -----> infection
        ```

        **Mediator** (on the causal path from E to Y). Do NOT adjust if you want the total effect.

        ```text
                  TNFi --->  immunosuppression  --->  infection
        ```

        **Collider** (common effect of two variables, one of which is E or upstream of it, and one of which is Y or upstream of it). Conditioning on the collider INDUCES a spurious association.

        ```text
                  TNFi ---.                      .--- infection
                           \                    /
                            v                  v
                                hospitalization
        ```

        The three diagrams look superficially similar (three nodes plus a fourth). What changes is the direction of the arrows. That change is what determines whether adjusting for the fourth variable fixes bias, removes the effect you wanted, or creates bias that wasn't there.
        """
    )
    return


@app.cell
def _(mo):
    conf_slider = mo.ui.slider(
        start=0.0, stop=0.65, step=0.05, value=0.50,
        label="Strength of confounding (P(TNFi | pred) minus P(TNFi | no pred))",
        show_value=True,
        full_width=True,
    )

    mo.md(
        rf"""
        ## 5. Watch the crude estimate move as confounding gets stronger

        The slider below controls the *strength of the confounding*: specifically, the gap between P(TNFi | on prednisone) and P(TNFi | not on prednisone). When the gap is 0, prednisone has no relationship to treatment assignment; there is no confounding; crude and adjusted estimates agree. When the gap is large, prednisone strongly predicts treatment; crude over-states the TNFi effect by a lot; the adjusted estimate stays near the truth.

        The underlying covariates (age, sex, sero, duration, prednisone status, baseline rate) stay fixed across slider values. Only treatment assignment and the events that follow from it are re-drawn.

        {mo.as_html(conf_slider)}
        """
    )
    return (conf_slider,)


@app.cell
def _(conf_slider, mo, np, pd):
    # Re-simulate at the slider's confounding strength. Fix covariates by
    # seeding a fresh RNG with a stable seed, so the only thing that
    # varies as the slider moves is the treatment-assignment probability.
    sim_rng = np.random.default_rng(20260519)

    n_sim = 2000
    age_sim = sim_rng.normal(58, 12, n_sim).clip(25, 85)
    sero_sim = sim_rng.random(n_sim) < 0.70
    duration_sim = sim_rng.gamma(2.0, 2.5, n_sim).clip(0.5, 25)
    p_pred_sim = 0.18 + 0.20 * sero_sim + 0.15 * (duration_sim > 5)
    p_pred_sim = p_pred_sim.clip(0.05, 0.85)
    pred_sim = sim_rng.random(n_sim) < p_pred_sim

    # Slider value is the gap; split it symmetrically around 0.50.
    gap = float(conf_slider.value)
    p_tnfi_pred = 0.50 + gap / 2
    p_tnfi_nopred = 0.50 - gap / 2
    p_tnfi_sim = np.where(pred_sim, p_tnfi_pred, p_tnfi_nopred)

    treat_rng = np.random.default_rng(20260520)
    tnfi_sim = treat_rng.random(n_sim) < p_tnfi_sim
    treatment_sim = np.where(tnfi_sim, "TNFi", "csDMARD")

    rate_sim = (
        0.030
        * np.exp(0.04 * (age_sim - 50))
        * np.where(sero_sim, 1.20, 1.00)
        * np.where(tnfi_sim, 1.60, 1.00)
        * np.where(pred_sim, 1.80, 1.00)
    )
    event_rng = np.random.default_rng(20260521)
    t_sim = event_rng.exponential(1.0 / rate_sim)
    inf_sim = t_sim <= 3.0
    fu_sim = np.where(inf_sim, t_sim, 3.0)

    df_sim = pd.DataFrame({
        "treatment": treatment_sim,
        "prednisone": pred_sim,
        "serious_infection": inf_sim,
        "followup_yrs": fu_sim,
    })

    def _irr(df):
        e = df[df["treatment"] == "TNFi"]
        u = df[df["treatment"] == "csDMARD"]
        if len(e) == 0 or len(u) == 0:
            return None
        py_e = e["followup_yrs"].sum()
        py_u = u["followup_yrs"].sum()
        a = int(e["serious_infection"].sum())
        c = int(u["serious_infection"].sum())
        if py_e == 0 or py_u == 0 or c == 0:
            return None
        return (a / py_e) / (c / py_u)

    def _mh(df):
        num = 0.0
        den = 0.0
        for pred_val in (False, True):
            sub = df[df["prednisone"] == pred_val]
            e = sub[sub["treatment"] == "TNFi"]
            u = sub[sub["treatment"] == "csDMARD"]
            if len(e) == 0 or len(u) == 0:
                continue
            a = int(e["serious_infection"].sum())
            c = int(u["serious_infection"].sum())
            py_e = e["followup_yrs"].sum()
            py_u = u["followup_yrs"].sum()
            py_total = py_e + py_u
            if py_total == 0 or c == 0:
                continue
            num += a * py_u / py_total
            den += c * py_e / py_total
        if den == 0:
            return None
        return num / den

    crude_sim = _irr(df_sim)
    mh_sim = _mh(df_sim)

    crude_str = f"{crude_sim:.2f}" if crude_sim is not None else "n/a"
    mh_str = f"{mh_sim:.2f}" if mh_sim is not None else "n/a"

    mo.md(
        rf"""
        **At a confounding strength of {gap:.2f}** (P(TNFi | pred) = {p_tnfi_pred:.0%}, P(TNFi | no pred) = {p_tnfi_nopred:.0%}):

        | Estimate | Value |
        |---|---|
        | True causal HR (built into the data) | 1.60 |
        | **Crude HR** (no adjustment) | **{crude_str}** |
        | **MH-adjusted HR** (stratified on prednisone) | **{mh_str}** |

        Slide all the way left (strength = 0): both estimates agree near the truth. Slide right: the crude pulls away while the adjusted stays put. The slider is showing what confounding *is*: the divergence between what the data say crudely and what the data would say if you controlled for the right thing.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 6. The role-picker: confounder vs mediator vs collider

        Same three-node picture, three different stories. Below is a small synthetic example for each role. Pick a role, see the DAG, see the crude estimate, see what happens when you "adjust for" the third variable. The lesson is different in each case.
        """
    )
    return


@app.cell
def _(mo):
    role_picker = mo.ui.radio(
        options=["Confounder", "Mediator", "Collider"],
        label="Pick a role for the covariate:",
        value="Confounder",
    )
    role_picker
    return (role_picker,)


@app.cell
def _(mo, np, pd, role_picker):
    role = role_picker.value

    if role == "Confounder":
        # Reuse the main RA cohort logic in miniature so the role-picker
        # is self-contained.
        rng_c = np.random.default_rng(20260601)
        nc = 1500
        pred_c = rng_c.random(nc) < 0.40
        p_tnfi_c = np.where(pred_c, 0.80, 0.30)
        tnfi_c = rng_c.random(nc) < p_tnfi_c
        rate_c = (
            0.10
            * np.where(tnfi_c, 1.60, 1.00)
            * np.where(pred_c, 1.80, 1.00)
        )
        # 1-year horizon for a quick risk read.
        t_c = rng_c.exponential(1.0 / rate_c)
        inf_c = t_c <= 1.0

        df_c = pd.DataFrame({
            "tnfi": tnfi_c, "pred": pred_c, "inf": inf_c,
        })

        # Crude risk ratio.
        r_e = df_c.loc[df_c["tnfi"], "inf"].mean()
        r_u = df_c.loc[~df_c["tnfi"], "inf"].mean()
        rr_crude_c = r_e / r_u

        # Stratified within prednisone strata; report the within-stratum
        # ratios and the pooled estimate.
        stratum_results = []
        for pv, label in [(False, "no prednisone"), (True, "on prednisone")]:
            sub = df_c[df_c["pred"] == pv]
            re_ = sub.loc[sub["tnfi"], "inf"].mean()
            ru_ = sub.loc[~sub["tnfi"], "inf"].mean()
            stratum_results.append((label, re_, ru_, re_ / ru_, len(sub)))

        # Simple weighted-average risk ratio across strata, weighted by
        # stratum size. Adequate for the pedagogy here.
        total = sum(s[4] for s in stratum_results)
        rr_adj_c = sum(s[3] * s[4] for s in stratum_results) / total

        body = rf"""
        ### Role: Confounder

        ```text
                      prednisone
                       /      \
                      v        v
                    TNFi -----> infection
        ```

        **The story.** Prednisone is a marker of disease severity. Severe RA patients are more likely to be on prednisone AND more likely to be stepped up to a TNFi. Prednisone also independently raises infection risk. Prednisone is a *common cause* of treatment assignment and outcome, so it confounds the TNFi-infection question.

        **The numbers** (n = {nc}, 1-year risk of serious infection):

        | Analysis | Risk in TNFi | Risk in csDMARD | Risk ratio |
        |---|---|---|---|
        | **Crude** (ignore prednisone) | {r_e:.1%} | {r_u:.1%} | **{rr_crude_c:.2f}** |
        | Within {stratum_results[0][0]} (n = {stratum_results[0][4]}) | {stratum_results[0][1]:.1%} | {stratum_results[0][2]:.1%} | {stratum_results[0][3]:.2f} |
        | Within {stratum_results[1][0]} (n = {stratum_results[1][4]}) | {stratum_results[1][1]:.1%} | {stratum_results[1][2]:.1%} | {stratum_results[1][3]:.2f} |
        | **Adjusted** (stratum-size-weighted pooled) | | | **{rr_adj_c:.2f}** |

        **The lesson.** Adjusting for a confounder removes bias. The crude estimate ({rr_crude_c:.2f}) is misleadingly large; the adjusted estimate ({rr_adj_c:.2f}) is close to the true effect (1.60) we baked in. *This is the case where adjustment is the right move.*
        """
        out = mo.md(body)

    elif role == "Mediator":
        # TNFi causes TNFi-induced neutropenia in a subset of patients;
        # neutropenia is what causes serious infection. All of TNFi's
        # effect on infection runs through the neutropenia node, so
        # adjusting for neutropenia zeroes out the apparent TNFi effect.
        rng_m = np.random.default_rng(20260602)
        nm = 1500
        tnfi_m = rng_m.random(nm) < 0.50
        p_neut = np.where(tnfi_m, 0.45, 0.12)
        neutropenia = rng_m.random(nm) < p_neut
        p_inf_m = np.where(neutropenia, 0.42, 0.06)
        inf_m = rng_m.random(nm) < p_inf_m

        df_m = pd.DataFrame({
            "tnfi": tnfi_m, "neutropenia": neutropenia, "inf": inf_m,
        })

        # Crude TNFi-infection risk ratio.
        r_e_m = df_m.loc[df_m["tnfi"], "inf"].mean()
        r_u_m = df_m.loc[~df_m["tnfi"], "inf"].mean()
        rr_crude_m = r_e_m / r_u_m

        # Within-stratum risk ratios. The mediator carries the full
        # effect, so within each level of the mediator the TNFi-infection
        # association should be near 1.0.
        med_strata = []
        for nv, label in [(False, "no neutropenia"), (True, "neutropenia")]:
            sub = df_m[df_m["neutropenia"] == nv]
            if len(sub) == 0:
                continue
            re = sub.loc[sub["tnfi"], "inf"].mean()
            ru = sub.loc[~sub["tnfi"], "inf"].mean()
            if ru > 0:
                med_strata.append((label, re, ru, re / ru, len(sub)))

        total_m = sum(s[4] for s in med_strata)
        rr_adj_m = sum(s[3] * s[4] for s in med_strata) / total_m

        p_neut_tnfi = neutropenia[tnfi_m].mean()
        p_neut_cs = neutropenia[~tnfi_m].mean()

        body = rf"""
        ### Role: Mediator

        ```text
                TNFi --->  neutropenia  --->  serious infection
        ```

        **The story.** A subset of TNFi-treated patients develop drug-induced neutropenia. Neutropenia is the proximate cause of serious infection. In this simplified model, TNFi has *no* direct effect on infection that bypasses neutropenia; the entire TNFi-infection association runs through that one node.

        In this synthetic cohort, {p_neut_tnfi:.0%} of TNFi-treated patients develop neutropenia versus {p_neut_cs:.0%} of csDMARD patients. Neutropenic patients have a 42% risk of serious infection; non-neutropenic patients have a 6% risk.

        **The numbers** (n = {nm}):

        | Analysis | Risk in TNFi | Risk in csDMARD | Risk ratio |
        |---|---|---|---|
        | **Crude** (ignore neutropenia) | {r_e_m:.1%} | {r_u_m:.1%} | **{rr_crude_m:.2f}** |
        | Within {med_strata[0][0]} (n = {med_strata[0][4]}) | {med_strata[0][1]:.1%} | {med_strata[0][2]:.1%} | {med_strata[0][3]:.2f} |
        | Within {med_strata[1][0]} (n = {med_strata[1][4]}) | {med_strata[1][1]:.1%} | {med_strata[1][2]:.1%} | {med_strata[1][3]:.2f} |
        | **Adjusted** (stratum-size-weighted pooled) | | | **{rr_adj_m:.2f}** |

        **The lesson.** Adjusting for a mediator zeroes out the very effect you were trying to measure. The crude estimate ({rr_crude_m:.2f}) is the *total* TNFi effect on infection, which is the clinically relevant number. The within-stratum estimates are near 1.0 because, once you know a patient's neutropenia status, treatment carries no additional information about their infection risk. A reader who saw only the adjusted estimate would conclude TNFi has no effect on infection, when in this cohort it more than doubles the risk through the mediator. *This is the case where adjustment is the wrong move when your question is the total effect.*
        """
        out = mo.md(body)

    else:  # Collider
        # TNFi and infection are independent in the source population.
        # Both increase the probability of being admitted to the rheum
        # referral center. Restricting to admitted patients induces a
        # negative TNFi-infection association.
        rng_co = np.random.default_rng(20260603)
        nco = 3000
        tnfi_co = rng_co.random(nco) < 0.50
        inf_co = rng_co.random(nco) < 0.18  # independent of treatment
        p_hosp = 0.05 + 0.35 * tnfi_co + 0.55 * inf_co
        p_hosp = np.clip(p_hosp, 0.0, 0.98)
        hosp_co = rng_co.random(nco) < p_hosp

        df_co = pd.DataFrame({
            "tnfi": tnfi_co, "inf": inf_co, "hosp": hosp_co,
        })

        # Full-population (unconditioned) risk ratio: should be near 1.0.
        r_e_co = df_co.loc[df_co["tnfi"], "inf"].mean()
        r_u_co = df_co.loc[~df_co["tnfi"], "inf"].mean()
        rr_full = r_e_co / r_u_co

        # Conditioned on hospitalized: TNFi-infection association moves.
        df_hosp = df_co[df_co["hosp"]]
        r_e_h = df_hosp.loc[df_hosp["tnfi"], "inf"].mean()
        r_u_h = df_hosp.loc[~df_hosp["tnfi"], "inf"].mean()
        rr_hosp = r_e_h / r_u_h

        n_hosp = int(df_co["hosp"].sum())

        body = rf"""
        ### Role: Collider

        ```text
                  TNFi ---.                      .--- infection
                           \                    /
                            v                  v
                                hospitalization
        ```

        **The story.** TNFi and serious infection are *independent* in the source RA population (we set the true effect to zero in this dataset). Both make a patient more likely to be admitted to the rheumatology referral center: TNFi because of monitoring intensity, infection because it requires admission. A researcher who studies only the admitted-patient registry has *conditioned on a collider*.

        **The numbers** (n = {nco} total, of whom {n_hosp:,} are hospitalized):

        | Population | Risk in TNFi | Risk in csDMARD | Risk ratio |
        |---|---|---|---|
        | **Source population** (true effect) | {r_e_co:.1%} | {r_u_co:.1%} | **{rr_full:.2f}** |
        | **Restricted to hospitalized** | {r_e_h:.1%} | {r_u_h:.1%} | **{rr_hosp:.2f}** |

        **The lesson.** In the source population, the risk ratio is essentially 1.0: no association between TNFi and infection. Restricting the analysis to hospitalized patients produces a risk ratio of {rr_hosp:.2f}, a *spurious* negative association. The bias was created entirely by the act of conditioning. *This is the case where adjustment creates bias where none existed.*

        This is the structural form of Berkson's paradox, M-bias, and "selection on a post-treatment variable." Whenever you find yourself "restricting to" or "controlling for" a variable that lies downstream of both the exposure and the outcome, pause and draw the DAG.
        """
        out = mo.md(body)

    out
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 7. Now read it back

        Two short quizzes covering what to do when you encounter a covariate in a paper or a vendor's model description.
        """
    )
    return


@app.cell
def _(mo):
    q1 = mo.ui.radio(
        options=[
            "Confounder. The adjustment moved the estimate toward the truth.",
            "Mediator. The adjustment removed the effect we wanted to measure.",
            "Collider. The adjustment created bias that wasn't there.",
            "Cannot tell without more information.",
        ],
        label=(
            "A trial reports the unadjusted in-hospital mortality of a new sepsis "
            "alert is 22% in the alert arm vs 25% in the control arm. After "
            "adjusting for ICU transfer, the alert arm mortality looks 18% vs "
            "20% in the controls. ICU transfer happens AFTER the alert fires "
            "and is influenced both by the alert and by clinical deterioration. "
            "What role does ICU transfer play here, and what is the adjustment doing?"
        ),
    )
    q1
    return (q1,)


@app.cell
def _(mo, q1):
    if q1.value is None:
        out1 = mo.md("_Pick one._")
    else:
        correct1 = q1.value.startswith("Collider")
        out1 = mo.callout(
            mo.md(
                rf"""
                **{'Correct.' if correct1 else 'Not quite.'}**

                ICU transfer is influenced by *both* the alert (whether it fired) AND by clinical deterioration (which is on the path to mortality). That makes it a **collider** between treatment and outcome. Adjusting for ICU transfer (or restricting to non-transferred patients, or stratifying on it) opens a path that should have stayed closed and biases the alert effect. The "adjusted" mortality difference is structurally distorted relative to the unadjusted one. The right move would be to *not* adjust for ICU transfer (or to handle it explicitly with a mediation analysis if the question is specifically about the direct effect that bypasses the ICU). A useful heuristic: be suspicious of "adjustments" for post-treatment variables.
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
            "Confounder, adjust for it.",
            "Mediator, do not adjust for it.",
            "Collider, do not adjust for it.",
            "Neutral covariate, the choice doesn't matter.",
        ],
        label=(
            "An observational study of methotrexate vs leflunomide in RA wants "
            "to estimate the effect of treatment choice on liver toxicity. The "
            "investigators have a measure of baseline disease activity (DAS28 "
            "at the time of treatment initiation). Disease activity influences "
            "what the rheumatologist prescribes (sicker patients tend to start "
            "on MTX in this practice) and also independently affects liver "
            "function over time. What role does baseline disease activity play?"
        ),
    )
    q2
    return (q2,)


@app.cell
def _(mo, q2):
    if q2.value is None:
        out2 = mo.md("_Pick one._")
    else:
        correct2 = q2.value.startswith("Confounder")
        out2 = mo.callout(
            mo.md(
                rf"""
                **{'Correct.' if correct2 else 'Not quite.'}**

                Baseline disease activity is a *common cause* of both the exposure (treatment choice) and the outcome (liver toxicity). It is measured BEFORE treatment starts, so it cannot be a mediator or a collider relative to this exposure. That makes it a **confounder** in the classical sense. Failing to adjust for it would mean the crude treatment comparison is contaminated by the fact that the two arms differ at baseline. This is confounding by indication: the most common form of confounding in observational pharmacoepidemiology.
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

        Pick one of the two prompts below and write 4 to 6 sentences in the box that follows. Save what you write outside the browser; the box is a scratch pad, not persistent storage. When you are done, continue to `track-03-diagnostic-test`.

        1. **A clinical paper you've read recently** adjusted for a list of covariates. For each covariate the authors named, sketch (mentally or on paper) which role it plays in their DAG. Were any of them post-treatment? Were any of them potential mediators? Would you have adjusted for the same set?

        2. **A vendor is selling your hospital a model** that predicts post-operative pneumonia. The model is "adjusted for" length of stay. What is the DAG question you'd ask them before allowing it into a clinical workflow?
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
            **Go deeper** is in `track-02-bias/go-deeper.md`. The next track (`track-03-diagnostic-test`) builds the 2x2 table and the Bayesian intuition exercise: sliders for sensitivity, specificity, and prevalence drive a reactive PPV, and you watch positive predictive value collapse as prevalence drops.
            """
        ),
        kind="info",
    )
    return


if __name__ == "__main__":
    app.run()