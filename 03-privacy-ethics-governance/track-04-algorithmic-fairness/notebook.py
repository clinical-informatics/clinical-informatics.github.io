"""Track 04: Algorithmic fairness and equity.

Algorithms are not neutral. This notebook walks the five places bias
enters a clinical algorithm, three landmark clinical cases (Obermeyer
2019, Vyas et al 2020, the pulse oximeter), the fairness-metric
impossibility result (Kleinberg, Mullainathan, Raghavan 2016), and the
seven questions to ask of any model. The interactive piece is a
synthetic deterioration predictor with subgroup-stratified performance:
move the threshold, watch the subgroup sensitivity/specificity/PPV
diverge, and see the impossibility result manifest in real numbers.
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

    rng = np.random.default_rng(20260517)
    return alt, mo, np, pd, rng


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 04: Algorithmic fairness and equity

        ## Algorithms are not neutral

        A clinical decision rule, a risk score, a deployed AI tool: all of them are *decisions, encoded*. The people who built them made choices. Whose data trained it. Which outcome to predict. Which features to include. Which threshold to recommend. Each choice shapes who benefits and who doesn't. When the choices are made carelessly, the resulting tool inherits the disparities of the system that produced it.

        This track is the working clinician's framework for evaluating any clinical algorithm. Six pieces:

        1. **The five places bias enters.** Training data, labels, features, deployment context, feedback loops.
        2. **The Obermeyer 2019 case.** The most-cited demonstration of label bias in clinical AI.
        3. **Vyas et al 2020.** Race correction in clinical algorithms (eGFR, VBAC, spirometry, more).
        4. **The pulse oximeter case.** A device, not an ML model, but the same structural failure.
        5. **Fairness metrics and the impossibility result.** Why "fair" cannot be one thing.
        6. **The seven questions.** A checklist for any vendor pitch or published model.

        Then a subgroup-stratified deterioration predictor that lets you watch the impossibility result happen.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1. The five places bias enters

        A clinical algorithm is the end of a pipeline. Bias can enter at any of five points.

        | # | Where | What it looks like | Documented example |
        |---|---|---|---|
        | 1 | **Training data** | Population in the training set differs from the deployment population | Dermatology AI trained on light-skinned subjects, performing poorly on darker skin (Adamson 2018) |
        | 2 | **Labels** | The outcome variable is a biased proxy for the construct that matters | Predicting cost as a proxy for need (Obermeyer 2019) |
        | 3 | **Features** | Inputs encode protected characteristics directly or indirectly | Race correction in eGFR delaying nephrology referral for Black patients (Vyas 2020) |
        | 4 | **Deployment context** | Model used outside the population, workflow, or regime it was validated in | Sepsis prediction tools that fail when ported across institutions |
        | 5 | **Feedback loops** | Model decisions shape future training data, concentrating bias | A model that under-alerts on a subgroup remains poorly tuned to that subgroup on retraining |

        Each of these has been documented in the clinical literature. The next sections walk three of them with the specifics.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2. Obermeyer 2019: label bias as the canonical case

        Published in *Science*, October 2019. Most-cited demonstration of clinical-algorithm bias.

        ### The setup

        A commercial population-health-management algorithm, used across the United States to flag patients for additional care management resources, ranked patients by a "risk score." Patients above a threshold were enrolled in care management programs.

        The **label** the algorithm trained on was **total healthcare costs** in the prior year, on the theory that costlier patients are sicker patients.

        ### The finding

        The researchers compared the algorithm's risk score against actual measures of illness severity (active chronic conditions, recent hospitalizations). At any given risk score:

        - **Black patients had 26.3% more active chronic conditions** than White patients with the same score.
        - The algorithm therefore *underestimated* illness severity for Black patients at any given level of need.
        - Correcting the label (predicting "active chronic conditions" instead of "cost") would more than double the proportion of Black patients flagged for the care-management program, from **17.7% to 46.5%**.

        ### The mechanism

        Black patients receive lower healthcare spending than White patients with equivalent illness severity. The mechanism is structural: access barriers, less time with providers, less specialist referral, less diagnostic workup, less aggressive management. None of these are about the patient's biology; all of them are about the system's treatment of the patient.

        The algorithm learned "low cost = healthy." Because cost is correlated with race (downstream of the system's behavior), the algorithm effectively learned "Black = healthy" *relative to equivalently sick White patients*. The algorithm was technically well-calibrated against its label (cost). It was severely biased against the construct that mattered (need).

        ### The general lesson

        **The most insidious bias in clinical algorithms is in labels, not features.** Removing "race" from the feature list does nothing about a bias that lives in the outcome variable. Any algorithm whose label is cost, length of stay, readmission, billing code, or any administratively-collected outcome is at risk of label bias in the same direction.

        The question to ask: **"What is this model learning to predict, and is that the same thing as what you care about?"**
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3. Vyas et al 2020: race correction in clinical algorithms

        Published in *NEJM*, August 2020. A review of clinical algorithms that explicitly use "race" as an input variable.

        ### The cases

        Representative examples from the review:

        | Algorithm | What the race correction did | Documented downstream effect |
        |---|---|---|
        | **eGFR (MDRD / CKD-EPI 2009)** | Boosted estimated GFR for Black patients on the basis of assumed higher muscle mass | Delayed nephrology referral, transplant listing, and dialysis initiation for Black patients with CKD |
        | **VBAC success calculator** | Lowered predicted success of vaginal birth after cesarean for Black and Hispanic women | More repeat cesareans for those groups |
        | **ASCVD risk (Pooled Cohort Equations 2013)** | Race-stratified equations producing different risk estimates | More statin prescriptions for Black patients (contested implications) |
        | **Lung function reference equations** | Lower "normal" spirometry values for Black patients | Under-diagnosis of lung disease in Black patients |
        | **STS thoracic surgery risk** | Adjusted risk by race for cardiothoracic surgery candidates | Affected surgical decision-making |

        ### The framework question

        For every race-corrected algorithm, ask: **What biological mechanism is "race" actually standing in for?**

        Three honest answers:

        - **Real biological correlate** (e.g., a specific allele frequency that varies by ancestry). The race correction may be defensible if the mechanism is documented and the correction operationalizes it correctly. Sickle cell disease screening recommendations use ancestry information in a defensible way.
        - **Environmental or socioeconomic correlate.** "Race" is doing the work of differential exposure, differential access, or differential socioeconomic status. The correction *captures* the disparity rather than *addressing* it; replacing race with the actual mechanism (income, exposure, access) is the better path.
        - **Unmotivated artifact of historical fitting.** No mechanism, just an empirical fit on data that reflected past discrimination. These corrections perpetuate the discrimination as a "biological" finding. Most of the corrections in the Vyas review fall here.

        ### Since 2020

        Multiple specialty societies have removed or revised race-corrected algorithms. The 2021 CKD-EPI equation removes the race coefficient. The VBAC calculator was revised to remove race in 2021. The cleanup is ongoing across pulmonology, hematology, and other specialties.

        The general lesson: any time race is in a feature list, the question is *not* "is the correction empirically supported on the validation data?" The question is "**what mechanism is it standing in for, and is the downstream effect ethically defensible?**"
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 4. The pulse oximeter case

        Not a learned ML model. A clinical device with the same structural failure.

        ### What the data shows

        Sjoding, Dickson, Iwashyna, Gay, and Valley, *NEJM*, December 2020. The team compared pulse-oximeter readings against simultaneous arterial blood gas measurements in two cohorts (over 10,000 paired measurements at Michigan, then over 37,000 in a multicenter cohort).

        Key finding: among patients with pulse-oximeter readings of **92-96%** (the clinically normal-to-borderline range):

        - **Black patients had occult hypoxemia (true SpO2 < 88%) at 11.7% of measurements.**
        - **White patients had occult hypoxemia at 3.6% of measurements.**

        Black patients were roughly **three times more likely** to have clinically significant hypoxemia that the pulse oximeter missed.

        ### The mechanism

        Pulse oximetry uses light absorption through the skin and underlying tissue. Melanin in darker skin absorbs more of the relevant wavelengths, biasing the calculation upward. The devices were calibrated and validated on predominantly light-skinned populations. The bias has been known in smaller studies for decades; the 2020 paper made it visible at scale during COVID, when oxygenation was the gating decision for hospital admission and ICU placement.

        ### Why this case sits with the ML cases

        Pulse oximetry isn't a "model" in the ML sense. But the failure pattern is identical to Obermeyer and Vyas:

        - A tool validated on a non-representative population.
        - Deployed broadly under the assumption that the validation generalized.
        - Bias was structural and undetectable at the individual level (the SpO2 readout shows you 94% whether you're a White or Black patient).
        - The bias was visible only when performance was stratified by subgroup and compared against ground truth.

        The lesson for AI: every clinical algorithm, device, or rule that was validated on a non-representative population is suspect on the population it was not validated on, until proven otherwise. Stratify by subgroup before deploying.
        """
    )
    return


@app.cell
def _(mo):
    case_quiz = mo.ui.radio(
        options=[
            "Training data: the cohort was unrepresentative of the deployment population.",
            "Labels: the outcome variable was a biased proxy for what the algorithm should have measured.",
            "Features: a protected characteristic or its proxy was an input.",
            "Deployment context: the model was used outside the regime where it was validated.",
            "Feedback loops: the model's own decisions concentrated bias on retraining.",
        ],
        label=(
            "An academic medical center deploys a sepsis-alert tool trained on its own historical inpatient "
            "data. The tool predicts ICU transfer within 24 hours as its outcome. On post-deployment audit, "
            "the tool alerts on Medicare and commercially-insured patients at a 19% rate but on Medicaid "
            "patients at a 9% rate, with equivalent post-deployment mortality across groups. "
            "Which of the five sources of bias most likely explains the disparity?"
        ),
    )
    case_quiz
    return (case_quiz,)


@app.cell
def _(case_quiz, mo):
    if case_quiz.value is None:
        case_quiz_feedback = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif case_quiz.value.startswith("Labels"):
        case_quiz_feedback = mo.callout(
            mo.md(
                "**Correct.** The label is **ICU transfer within 24 hours**, used as a proxy for **clinical deterioration**. "
                "ICU transfer depends on the patient's actual deterioration, *and* on bed availability, *and* on unit culture, *and* on insurance status. "
                "Medicaid patients may be transferred to the ICU at lower rates for any given severity (because of differential staffing, less assertive escalation, or insurance-driven discharge planning). "
                "The model learned 'Medicaid = lower ICU transfer rate' as if it meant 'Medicaid = lower deterioration', when the truth is closer to 'Medicaid = different downstream care'. "
                "This is structurally identical to the Obermeyer 2019 case: a biased label produces a biased model that is well-calibrated against the label and ethically catastrophic against the construct."
            ),
            kind="success",
        )
    else:
        case_quiz_feedback = mo.callout(
            mo.md(
                "**Not quite.** The structure of the scenario points at the **label**: the outcome 'ICU transfer within 24 hours' is being used as a proxy for the construct 'clinical deterioration'. "
                "If those two things diverge by insurance group (because Medicaid patients are transferred to the ICU at different rates than commercially insured patients for any given severity), the model's predictions inherit that divergence. "
                "Training data, features, deployment, and feedback loops could all contribute in real cases, but the dominant failure mode here matches the Obermeyer 2019 pattern: a biased label produces a biased model that *looks* well-calibrated against itself."
            ),
            kind="warn",
        )
    case_quiz_feedback
    return (case_quiz_feedback,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 5. Fairness metrics and the impossibility result

        Several reasonable definitions of "the model is fair":

        | Metric | What it means |
        |---|---|
        | **Demographic parity** | The model predicts positive at the same rate across groups |
        | **Equal opportunity** | The true positive rate (sensitivity) is equal across groups |
        | **Equalized odds** | Both true positive rate AND false positive rate are equal across groups |
        | **Calibration** | A 30% risk score means a 30% actual outcome rate, in every group |
        | **Predictive parity** | Positive predictive value (PPV) is equal across groups |

        Each one looks reasonable on its own. The hard fact, from Kleinberg, Mullainathan, and Raghavan (arXiv 2016):

        > Any non-trivial model **cannot** satisfy calibration, equal false-positive rate, *and* equal false-negative rate simultaneously, **unless the base rates of the outcome are equal across groups**.

        This is an **impossibility result**. When subgroup base rates differ (which is almost always true in clinical data), you have to pick. The choice of which fairness criterion to optimize is itself a value judgment.

        The next cell makes this happen in real numbers. A synthetic deterioration predictor. Two subgroups with somewhat different base rates of deterioration. Move the threshold. Watch what changes.
        """
    )
    return


@app.cell
def _(np, pd, rng):
    n_per_group = 2000
    # Group A: baseline cohort, base rate of deterioration 12%
    # Group B: higher-base-rate cohort, base rate of deterioration 24%
    # The deterioration model is the same for both groups: a logistic function of a continuous severity score
    # that the model captures imperfectly.
    sev_a = rng.normal(0.0, 1.0, size=n_per_group)
    sev_b = rng.normal(0.7, 1.0, size=n_per_group)  # Group B has higher mean severity

    # True deterioration probability driven by severity
    def true_p(sev, intercept):
        return 1.0 / (1.0 + np.exp(-(intercept + 1.4 * sev)))

    p_a = true_p(sev_a, intercept=-2.3)
    p_b = true_p(sev_b, intercept=-2.3)

    y_a = (rng.uniform(size=n_per_group) < p_a).astype(int)
    y_b = (rng.uniform(size=n_per_group) < p_b).astype(int)

    # Model score is a noisy version of severity (the model isn't perfect)
    score_a = sev_a + rng.normal(0, 0.4, size=n_per_group)
    score_b = sev_b + rng.normal(0, 0.4, size=n_per_group)

    # Bring scores onto a comparable 0-1 scale via the logistic
    score_a_p = 1.0 / (1.0 + np.exp(-score_a))
    score_b_p = 1.0 / (1.0 + np.exp(-score_b))

    cohort = pd.DataFrame(
        {
            "group": (["A"] * n_per_group) + (["B"] * n_per_group),
            "score": np.concatenate([score_a_p, score_b_p]),
            "y_true": np.concatenate([y_a, y_b]),
        }
    )
    base_rate_a = float(y_a.mean())
    base_rate_b = float(y_b.mean())
    return base_rate_a, base_rate_b, cohort


@app.cell
def _(base_rate_a, base_rate_b, mo):
    mo.md(
        f"""
        ### The synthetic cohort

        - **Group A:** 2,000 patients, base rate of deterioration **{base_rate_a*100:.1f}%**.
        - **Group B:** 2,000 patients, base rate of deterioration **{base_rate_b*100:.1f}%**.

        Both groups are scored by the *same* model, which is a noisy function of an underlying severity score. The model is **identically miscalibrated for both groups** in absolute terms; the only thing that differs is the **base rate** of the outcome.

        The slider below sets the alert threshold. Patients with score above the threshold are flagged. Watch the subgroup TPR (sensitivity), FPR, and PPV diverge.
        """
    )
    return


@app.cell
def _(mo):
    threshold = mo.ui.slider(
        start=0.1,
        stop=0.9,
        step=0.02,
        value=0.5,
        label="Alert threshold (score above which the model flags a patient)",
        show_value=True,
    )
    threshold
    return (threshold,)


@app.cell
def _(alt, cohort, mo, pd, threshold):
    t = threshold.value
    rows = []
    for group in ["A", "B"]:
        sub = cohort[cohort["group"] == group]
        n = len(sub)
        n_pos = int(sub["y_true"].sum())
        n_neg = n - n_pos
        flagged = sub["score"] > t
        tp = int(((flagged) & (sub["y_true"] == 1)).sum())
        fp = int(((flagged) & (sub["y_true"] == 0)).sum())
        fn = int(((~flagged) & (sub["y_true"] == 1)).sum())
        tn = int(((~flagged) & (sub["y_true"] == 0)).sum())
        tpr = tp / n_pos if n_pos > 0 else 0.0
        fpr = fp / n_neg if n_neg > 0 else 0.0
        ppv = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        npv = tn / (tn + fn) if (tn + fn) > 0 else 0.0
        flag_rate = (tp + fp) / n
        rows.append(
            {
                "group": group,
                "base_rate": round(n_pos / n, 3),
                "flagged": tp + fp,
                "flag_rate": round(flag_rate, 3),
                "TPR (sensitivity)": round(tpr, 3),
                "FPR": round(fpr, 3),
                "PPV": round(ppv, 3),
                "NPV": round(npv, 3),
            }
        )
    metrics = pd.DataFrame(rows)
    metrics_display = metrics.copy()
    metrics_display.index = range(1, len(metrics_display) + 1)
    metrics_display.index.name = "row"

    # Build the score-distribution histogram for visualization.
    # Layer density + threshold line first, then facet by group (faceted charts can't be layered after the fact).
    plot_data = cohort.copy()
    plot_data["outcome"] = plot_data["y_true"].map({1: "deteriorated", 0: "did not"})

    density = (
        alt.Chart()
        .transform_density(
            "score",
            groupby=["outcome"],
            as_=["score", "density"],
            extent=[0, 1],
            bandwidth=0.03,
        )
        .mark_area(opacity=0.4)
        .encode(
            x=alt.X("score:Q", title="Model score"),
            y=alt.Y("density:Q", title="Density"),
            color=alt.Color(
                "outcome:N",
                scale=alt.Scale(
                    domain=["deteriorated", "did not"], range=["#D1495B", "#2E86AB"]
                ),
            ),
        )
    )

    threshold_line = (
        alt.Chart(pd.DataFrame({"t": [t]}))
        .mark_rule(color="black", strokeDash=[4, 4], size=2)
        .encode(x="t:Q")
    )

    combined_chart = (
        alt.layer(density, threshold_line, data=plot_data)
        .facet(row=alt.Row("group:N", title="Group"))
        .properties(title=f"Score distributions per group (dashed line = threshold {t:.2f})")
    )

    # Compare metrics across groups
    diffs_md = mo.md(
        f"""
        ### Subgroup-stratified metrics at threshold {t:.2f}

        **TPR difference (sensitivity, Group B minus Group A):** {metrics.iloc[1]['TPR (sensitivity)'] - metrics.iloc[0]['TPR (sensitivity)']:+.3f}.

        **FPR difference (Group B minus Group A):** {metrics.iloc[1]['FPR'] - metrics.iloc[0]['FPR']:+.3f}.

        **PPV difference (Group B minus Group A):** {metrics.iloc[1]['PPV'] - metrics.iloc[0]['PPV']:+.3f}.

        **Flag-rate difference (Group B minus Group A):** {metrics.iloc[1]['flag_rate'] - metrics.iloc[0]['flag_rate']:+.3f}.
        """
    )

    interpretation = (
        "**Notice that you cannot make every metric equal across the two groups by moving the threshold.** "
        "If the base rates differ (and here they do, by about 12 percentage points), then:\n\n"
        "- A threshold that equalizes flag rates (demographic parity) will unequalize TPR and FPR.\n"
        "- A threshold that equalizes TPR (equal opportunity) will unequalize PPV.\n"
        "- A threshold that equalizes PPV will unequalize TPR.\n\n"
        "**This is the Kleinberg impossibility result, visible in your slider.** No threshold makes all of "
        "the metrics equal across groups. The choice of which to prioritize is a value judgment about which "
        "kind of error is worse for which patients. *Pretending there is a neutral choice is itself a choice.*"
    )

    panel = mo.vstack(
        [
            mo.ui.table(metrics_display, selection=None),
            combined_chart,
            diffs_md,
            mo.callout(mo.md(interpretation), kind="info"),
        ]
    )
    panel
    return (panel,)


@app.cell
def _(mo):
    mo.md(
        r"""
        **Things to try.** Walk the threshold to different values:

        1. **Threshold around 0.3.** Both groups have high flag rates. TPRs are high. PPVs differ by group.
        2. **Threshold around 0.5.** Closer to the default. TPRs differ; FPRs differ; PPV is closer in absolute terms but still unequal.
        3. **Threshold around 0.7.** Only the highest-risk patients are flagged. TPRs are now low and very different between the groups. PPV is high. Flag rates collapse.

        **The point:** at no threshold are TPR, FPR, and PPV all equal across the two groups. The base-rate difference forces the trade-off. The impossibility result is not abstract; it is operative every time someone proposes a clinical-prediction tool and reports aggregate performance metrics without subgroup stratification.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 6. The seven questions

        A checklist for any vendor pitch, any published model, any CDS tool proposed for your institution:

        1. **What is the label?** What is it actually a proxy for? Is the proxy biased? (Obermeyer's question.)
        2. **What's the training population?** Who is in it, and who is missing? Where was the data collected?
        3. **What features are inputs?** Do any encode protected characteristics indirectly? Is "race" explicit, and if so, what mechanism is it standing in for? (Vyas's question.)
        4. **Has subgroup performance been reported?** Sensitivity, specificity, PPV, calibration by race, sex, age, insurance status, language, site of care. *If only aggregate metrics are reported, that is itself a finding.*
        5. **Where will this be deployed?** Is the deployment cohort represented in training and validation? What is the institution's plan for monitoring deployment performance?
        6. **What fairness criterion is being optimized?** Demographic parity, equal opportunity, calibration, predictive parity. The choice should be deliberate and explicit. (Kleinberg's question.)
        7. **What is the post-deployment monitoring plan?** How will you know if the model is degrading on a subgroup? Who is responsible for the corrective action?

        **If a vendor cannot answer five of these seven, the conversation is not ready for the deployment phase.**
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 7. What this leaves you

        Six things in place:

        1. **The five places bias enters.** Training data, labels, features, deployment context, feedback loops. Each documented in the literature.
        2. **The Obermeyer label-bias case.** Cost as a proxy for need. The most-cited demonstration that bias often lives in the outcome variable, not the features.
        3. **The Vyas race-correction review.** eGFR, VBAC, spirometry, ASCVD. Race as a feature requires a documented biological mechanism; most documented cases lacked one.
        4. **The pulse oximeter case.** A device, not an ML model, but the same structural failure. Validation cohort representativeness is a fairness question for everything.
        5. **The fairness-metric impossibility result.** Kleinberg, Mullainathan, and Raghavan 2016. When base rates differ, the standard fairness criteria are mutually incompatible. The choice is a value judgment.
        6. **The seven questions.** A practical checklist for any model, applied before deployment, with audit logs to prove it was applied.

        Track 05 closes the course with governance: who is in the room when these decisions get made, what the clinician's role is, and how the patient population gets representation in decisions about their own data.

        After this course, the equity questions in this track show up again in course 09 (AI in Medicine), which goes deeper on the ML mechanics, and course 12 (Clinical Decision Support), which addresses deployment in workflow. The framework here is the rung that makes those courses legible.
        """
    )
    return


if __name__ == "__main__":
    app.run()
