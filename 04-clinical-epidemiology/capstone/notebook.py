"""Capstone for course 04: Clinical epidemiology.

Six-step Socratic walk-through of an observational RA registry. The
learner is asked to define the question, identify the three biggest
threats to validity, propose mitigations, and write the analysis plan
they would actually run. The final cell auto-assembles their six
written answers into a one-page committee memo.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    return mo, np, pd


@app.cell
def _(mo):
    # Socratic helpers inlined from shared/socratic.py so the WASM export is
    # self-contained. Pyodide cannot import sibling modules from the source
    # tree, so the live-site export needs the helpers defined in the notebook
    # itself. Mirrors the API of start-here/shared/socratic.py.

    def scenario(title, body):
        return mo.vstack(
            [
                mo.md(f"## {title}"),
                mo.callout(mo.md(body), kind="info"),
            ]
        )

    def commit_text(prompt, *, min_chars=40):
        widget = mo.ui.text_area(
            label=prompt,
            rows=6,
            full_width=True,
            placeholder="Take a few sentences. The reveal won't unlock until you do.",
        )

        def _ready():
            value = widget.value or ""
            return len(value.strip()) >= min_chars

        return widget, _ready

    def reveal(learner_value, ideal_answer, *, learner_label="Your answer"):
        learner_display = learner_value if learner_value else "_(no answer yet)_"
        return mo.hstack(
            [
                mo.callout(
                    mo.vstack(
                        [
                            mo.md(f"**{learner_label}**"),
                            mo.md(str(learner_display)),
                        ]
                    ),
                    kind="neutral",
                ),
                mo.callout(
                    mo.vstack(
                        [
                            mo.md("**How we'd think through this**"),
                            mo.md(ideal_answer),
                        ]
                    ),
                    kind="success",
                ),
            ],
            widths="equal",
        )

    def reflection(prompt, placeholder=""):
        widget = mo.ui.text_area(
            label=prompt,
            rows=5,
            full_width=True,
            placeholder=placeholder
            or "Take a few sentences. No reveal here. The reflection is the work.",
        )
        layout = mo.vstack(
            [
                widget,
                mo.callout(
                    mo.md(
                        "_There's no answer key for this one. The point isn't to be right. "
                        "It's to make your reasoning explicit to yourself._"
                    ),
                    kind="neutral",
                ),
            ]
        )
        return widget, layout

    def go_deeper(body):
        return mo.callout(
            mo.vstack(
                [
                    mo.md("### Go deeper"),
                    mo.md(body),
                ]
            ),
            kind="info",
        )

    return commit_text, go_deeper, reflection, reveal, scenario


@app.cell
def _(mo):
    mo.md(
        r"""
        # Capstone: Clinical epidemiology

        ## The request on your desk

        A staff rheumatologist hands you a 4-page summary of the **Mercy Community Rheumatology Registry**: a single-site community-hospital registry of RA patients tracked for up to three years. The registry holds 812 enrolled patients. She wants to know whether TNFi exposure increases the rate of serious infection, and she wants something defensible to present at next month's quality committee. She has heard about the Galloway 2011 BSRBR result and wants to know whether the local data tells the same story.

        She offers a one-paragraph framing: "compare the two arms, calculate the hazard ratio, and write up the answer." She is hoping for a clean number she can put on a slide.

        **Your job.** Walk her through the analysis you would actually run, naming the three biggest threats to validity that a naive arms-comparison would miss, the mitigations you would apply to each, and what the final analysis plan would look like. Six Socratic steps. The committee memo at the end is assembled from your writing.

        Below is a 30-row sample drawn from the registry so you can see what is in the data. Ms. Reyes is **Patient RA-012**. The full registry has 812 rows with the same column structure.
        """
    )
    return


@app.cell
def _(np, pd):
    # 30-row sample from the Mercy Community Rheumatology Registry. Hand-built
    # so the threats are visible in the data: TNFi arm enriched for severity
    # (higher baseline DAS28, more prednisone, longer duration), several TNFi
    # serious-infection events clustered in the first 6 months on therapy
    # (the Galloway BSRBR early-risk pattern), and a few dropouts in both arms.
    # Reyes is RA-012.
    rows = [
        # patient_id, age, sex, seropositive, duration_yrs, baseline_DAS28, prednisone, treatment, followup_yrs, serious_infection, time_to_infection_mo, dropped_out
        ("RA-001", 64, "F", True,  6.2, 5.8, True,  "TNFi",    1.8, 1, 4.0, 0),
        ("RA-002", 52, "F", True,  3.1, 4.7, False, "TNFi",    3.0, 0, None, 0),
        ("RA-003", 71, "M", True,  9.5, 6.1, True,  "TNFi",    0.4, 1, 4.5, 0),
        ("RA-004", 47, "F", False, 1.8, 3.2, False, "csDMARD", 3.0, 0, None, 0),
        ("RA-005", 58, "F", True,  4.0, 4.4, True,  "TNFi",    2.7, 1, 8.0, 0),
        ("RA-006", 39, "M", True,  2.2, 4.0, False, "csDMARD", 3.0, 0, None, 0),
        ("RA-007", 68, "F", True,  11.0, 5.5, True, "TNFi",    1.0, 0, None, 1),
        ("RA-008", 54, "F", False, 2.6, 3.9, False, "csDMARD", 3.0, 0, None, 0),
        ("RA-009", 73, "M", True,  8.4, 5.7, True,  "TNFi",    0.3, 1, 3.5, 0),
        ("RA-010", 45, "F", True,  1.5, 3.6, False, "csDMARD", 3.0, 0, None, 0),
        ("RA-011", 60, "F", True,  5.3, 4.6, False, "csDMARD", 2.5, 1, 14.0, 0),
        ("RA-012", 52, "F", True,  4.0, 4.1, False, "TNFi",    3.0, 0, None, 0),  # Ms. Reyes
        ("RA-013", 66, "F", True,  7.2, 5.0, True,  "TNFi",    2.3, 1, 5.5, 0),
        ("RA-014", 49, "M", False, 1.0, 3.0, False, "csDMARD", 3.0, 0, None, 0),
        ("RA-015", 56, "F", True,  3.5, 4.3, True,  "TNFi",    2.9, 0, None, 0),
        ("RA-016", 72, "F", True,  10.2, 5.9, True, "TNFi",    1.2, 0, None, 1),
        ("RA-017", 42, "F", False, 1.2, 3.1, False, "csDMARD", 3.0, 0, None, 0),
        ("RA-018", 51, "F", True,  4.5, 4.2, False, "TNFi",    3.0, 0, None, 0),
        ("RA-019", 65, "M", True,  6.0, 4.9, True,  "TNFi",    1.6, 1, 5.0, 0),
        ("RA-020", 38, "F", False, 0.8, 2.8, False, "csDMARD", 3.0, 0, None, 0),
        ("RA-021", 70, "F", True,  9.0, 5.4, True,  "TNFi",    0.5, 0, None, 1),
        ("RA-022", 55, "F", True,  3.8, 4.0, False, "TNFi",    2.8, 0, None, 0),
        ("RA-023", 46, "M", False, 1.5, 3.3, False, "csDMARD", 3.0, 0, None, 0),
        ("RA-024", 63, "F", True,  5.5, 4.8, True,  "csDMARD", 3.0, 1, 22.0, 0),
        ("RA-025", 41, "F", True,  1.0, 3.4, False, "csDMARD", 3.0, 0, None, 0),
        ("RA-026", 59, "F", True,  4.7, 4.5, True,  "TNFi",    2.6, 1, 4.0, 0),
        ("RA-027", 50, "M", False, 2.0, 3.5, False, "csDMARD", 3.0, 0, None, 0),
        ("RA-028", 67, "F", True,  7.8, 5.3, True,  "TNFi",    1.9, 0, None, 0),
        ("RA-029", 44, "F", True,  1.7, 3.7, False, "csDMARD", 3.0, 0, None, 0),
        ("RA-030", 57, "F", True,  4.2, 4.2, False, "TNFi",    3.0, 0, None, 0),
    ]

    cols = [
        "patient_id", "age", "sex", "seropositive", "disease_duration_yrs",
        "baseline_DAS28", "prednisone", "treatment", "followup_yrs",
        "serious_infection", "time_to_infection_mo", "dropped_out",
    ]
    registry = pd.DataFrame(rows, columns=cols)
    registry.index = range(1, len(registry) + 1)
    registry.index.name = "row"

    # Headline crude numbers (a naive analyst's first computation).
    _tnfi = registry[registry["treatment"] == "TNFi"]
    _csd = registry[registry["treatment"] == "csDMARD"]
    n_tnfi = len(_tnfi)
    n_csd = len(_csd)
    ev_tnfi = int(_tnfi["serious_infection"].sum())
    ev_csd = int(_csd["serious_infection"].sum())
    pt_tnfi = float(_tnfi["followup_yrs"].sum())
    pt_csd = float(_csd["followup_yrs"].sum())
    rate_tnfi = ev_tnfi / pt_tnfi if pt_tnfi > 0 else float("nan")
    rate_csd = ev_csd / pt_csd if pt_csd > 0 else float("nan")
    crude_irr = rate_tnfi / rate_csd if rate_csd > 0 else float("nan")

    return (
        crude_irr, ev_csd, ev_tnfi, n_csd, n_tnfi, pt_csd, pt_tnfi,
        rate_csd, rate_tnfi, registry,
    )


@app.cell
def _(crude_irr, ev_csd, ev_tnfi, mo, n_csd, n_tnfi, pt_csd, pt_tnfi, rate_csd, rate_tnfi, registry):
    mo.vstack([
        mo.md(rf"""
        ### The 30-row sample

        {mo.as_html(registry)}

        **Codebook.**

        - `disease_duration_yrs`: years since RA diagnosis at registry enrollment.
        - `baseline_DAS28`: 28-joint disease activity score at enrollment (the standard measure in RA). Higher = more disease activity. The EULAR cutoffs are remission below 2.6, low activity 2.6 to 3.2, moderate 3.2 to 5.1, high above 5.1.
        - `prednisone`: chronic oral corticosteroid use at enrollment.
        - `treatment`: csDMARD = conventional synthetic DMARD alone (usually methotrexate). TNFi = TNF inhibitor on top of the csDMARD.
        - `followup_yrs`: total observed follow-up time in the registry.
        - `serious_infection`: 1 if a hospitalization-requiring infection occurred during follow-up, 0 otherwise.
        - `time_to_infection_mo`: months from registry enrollment to the infection (blank if no event).
        - `dropped_out`: 1 if the patient left the registry before the planned 3-year follow-up ended.

        **The naive number** the rheumatologist is hoping for:

        - csDMARD arm: {ev_csd} events in {pt_csd:.1f} person-years = **{rate_csd:.3f} per person-year**.
        - TNFi arm: {ev_tnfi} events in {pt_tnfi:.1f} person-years = **{rate_tnfi:.3f} per person-year**.
        - Crude incidence-rate ratio (TNFi vs csDMARD): **{crude_irr:.2f}**.

        That is the number the naive analysis would put on a slide. The next six steps are about why you would not stop there.
        """),
    ])
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Step 1 of 6: Define the question and the target estimand

        Before any analysis, name *exactly* what causal question this analysis is trying to answer. Is the target estimand the causal effect of TNFi initiation on serious infection rate in the general RA population? In the patients in this registry? Something narrower?

        Also name what design *could* answer that question cleanly, if you had unlimited resources. Doing so explicitly is what lets you see what the observational analysis is *not*.

        Write at least a short paragraph. The reveal opens at 80 characters.
        """
    )
    return


@app.cell
def _(commit_text):
    step1_widget, step1_ready = commit_text(
        "Your question definition and target estimand",
        min_chars=80,
    )
    step1_widget
    return step1_ready, step1_widget


@app.cell
def _(mo, reveal, step1_ready, step1_widget):
    mo.stop(
        not step1_ready(),
        mo.callout(
            mo.md("_Write at least a short paragraph above. The reveal opens after you do._"),
            kind="neutral",
        ),
    )

    ideal_1 = (
        "**The target estimand** is the causal effect of TNFi initiation (vs continued csDMARD only) on the rate of serious infection over a defined window of follow-up, in adults with RA who would be candidates for either treatment under usual rheumatologic care. The word *causal* is the load-bearing part: a number that mixes the TNFi effect with the patient-selection effects of why someone got TNFi is not what the committee asked for, even if the rheumatologist did not name the distinction.\n\n"
        "**The design that could answer this cleanly** is a randomized trial: enroll RA patients who are candidates for either, randomly assign TNFi vs continued csDMARD, follow forward for serious infection. Randomization breaks the link between exposure assignment and patient severity, so the crude comparison estimates the causal effect (within the trial population). The Mercy registry is *not* that design. Patients in the TNFi arm got TNFi because their rheumatologists decided they should, and that decision was informed by the same factors that themselves drive infection risk (disease activity, comorbidity, frailty, prior infection history). The registry can produce an *association*; the work of the rest of this capstone is figuring out how much of that association is plausibly causal and what threatens that interpretation.\n\n"
        "**A narrower acceptable target** is the average treatment effect among the treated: the effect of TNFi in the patients who actually received it, holding fixed who they are. That is what stratification, regression, and inverse-probability weighting attempt to estimate; the target trial they would emulate is a trial restricted to patients who look like the TNFi arm. Be honest about which estimand you are targeting; it changes the analysis and it changes the interpretation."
    )

    reveal(step1_widget.value, ideal_1, learner_label="Your question definition")
    return (ideal_1,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Step 2 of 6: Threat 1, confounding by indication

        Apply Track 02. What variables in the registry plausibly drive both treatment choice AND infection risk? Draw the DAG (mentally or on paper). Which adjustments would block the backdoor paths, and which would do the opposite? Predict the direction in which the crude IRR is biased.

        Write at least a paragraph.
        """
    )
    return


@app.cell
def _(commit_text):
    step2_widget, step2_ready = commit_text(
        "Your confounding analysis",
        min_chars=100,
    )
    step2_widget
    return step2_ready, step2_widget


@app.cell
def _(mo, reveal, step2_ready, step2_widget):
    mo.stop(
        not step2_ready(),
        mo.callout(
            mo.md("_Write at least a paragraph above. The reveal opens at 100 characters._"),
            kind="neutral",
        ),
    )

    ideal_2 = (
        "**This is confounding by indication, the perennial threat in observational pharmacoepidemiology.** Sicker patients get more aggressive treatment AND have worse outcomes, so the more aggressive treatment looks worse than it really is.\n\n"
        "**Confounders that are measured in this registry.**\n\n"
        "- **`baseline_DAS28`.** A direct disease-severity proxy. Higher DAS28 drives the rheumatologist toward TNFi (step-up therapy) AND independently increases infection risk (sicker patients have more infections). Common cause of treatment and outcome. *Adjust for it.*\n"
        "- **`prednisone`.** Steroid use also marks active disease, AND it directly suppresses immune function. Common cause structure on both legs. *Adjust for it.*\n"
        "- **`disease_duration_yrs`.** Longer-duration patients accumulate damage and step up through more agents over time. Plausibly a confounder via severity. *Adjust for it.*\n"
        "- **`age` and `seropositive`.** Both are baseline characteristics that influence both treatment choice (sero-positive moderate-to-severe RA is the prototype for biologic eligibility) and infection risk (older age increases infection risk). *Adjust for them.*\n\n"
        "**Confounders that are NOT in this dataset (and matter).** Smoking, frailty (independent of age), prior serious infection history, depression, BMI, diabetes, CKD, chronic lung disease. Each plausibly drives both treatment and infection risk. *Cannot be adjusted away* in this dataset; an E-value sensitivity analysis is the right tool for bounding their potential impact.\n\n"
        "**Mediators that you would NOT adjust for.** Anything downstream of TNFi exposure that itself influences infection: drug-induced neutropenia (see Track 02's mediator example), reduced disease activity in the months following TNFi initiation, weight changes. Adjusting for these would block the very causal path you are trying to measure (per Track 02).\n\n"
        "**Direction of the crude bias.** In this dataset the TNFi arm is enriched for severity (higher baseline DAS28, more prednisone, longer duration on average). All of those drive infection independently of TNFi. The crude TNFi-vs-csDMARD comparison **overstates** the harmful effect of TNFi. The adjusted estimate should be lower than the crude IRR, and may be substantially lower."
    )

    reveal(step2_widget.value, ideal_2, learner_label="Your confounding analysis")
    return (ideal_2,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Step 3 of 6: Threat 2, selection bias and loss to follow-up

        Apply Track 02's selection-bias and collider vocabulary, plus Track 05 on cohort design. Who is *in* this registry vs the underlying RA population at Mercy? Who *leaves* the registry differentially before the end of follow-up? Where does either pattern open a backdoor path or condition on a collider, and what does that do to the estimate?
        """
    )
    return


@app.cell
def _(commit_text):
    step3_widget, step3_ready = commit_text(
        "Your selection-bias and loss-to-follow-up analysis",
        min_chars=100,
    )
    step3_widget
    return step3_ready, step3_widget


@app.cell
def _(mo, reveal, step3_ready, step3_widget):
    mo.stop(
        not step3_ready(),
        mo.callout(
            mo.md("_Write at least a paragraph above. The reveal opens at 100 characters._"),
            kind="neutral",
        ),
    )

    ideal_3 = (
        "**Two distinct mechanisms, both at the cohort's edges.**\n\n"
        "**Entry selection: who got into the registry.** Registry enrollment is voluntary and is initiated by the rheumatologist at a clinic visit. The patients who enroll are *not* a random sample of RA patients in the catchment. Plausible enrollment drivers: more engaged patients, patients with more clinic visits (often the sicker ones), patients on novel therapies whose rheumatologists want to track outcomes (a TNFi bias toward enrollment). If enrollment depends on BOTH the exposure (TNFi-treated patients more likely enrolled) AND something that predicts the outcome (severity), the registry conditions on something downstream of both, which is collider conditioning by another name. The estimate is biased even after adjustment for measured confounders, because the unmeasured selection mechanism is not in the model.\n\n"
        "**Exit selection: who leaves before three years.** The `dropped_out` column in the sample shows several patients lost before the planned follow-up. KM and incidence-rate analyses handle these as censored. *But* censoring is assumed to be independent of the outcome (Track 05's KM assumption). If TNFi patients drop out because of an early adverse event (an infection in month 4 leads to discontinuing the biologic and disengaging from the rheum clinic), and that dropout looks the same in the data as an administrative censor at month 4, the analysis under-counts events in the TNFi arm and biases the IRR downward. Informative censoring is the technical name.\n\n"
        "**The selection DAG.** Severity → TNFi assignment. Severity → enrollment in registry. TNFi assignment → early adverse event → dropout. Restricting analysis to *enrolled* patients (the only data you have) and treating dropouts as administratively censored (the default of the analysis) opens at least one backdoor path the adjustment can't close.\n\n"
        "**Mitigations.** For entry selection: characterize the registry against the underlying clinic population (age, sex, disease duration, treatment mix) to establish how representative it is; report the comparison as a limitation; if a sampling-weight target exists (the Mercy clinic roster), reweight to it. For exit selection: code dropout reasons when possible, treat dropouts differently from administrative censors, run sensitivity analyses with different missingness assumptions (MAR vs MNAR per Course 02's vocabulary), and report the IRR under the bracketing assumptions. The lower bound is the answer assuming TNFi dropouts had immediate infections; the upper bound is the answer assuming dropouts had no events. The truth is between."
    )

    reveal(step3_widget.value, ideal_3, learner_label="Your selection-bias analysis")
    return (ideal_3,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Step 4 of 6: Threat 3, non-proportional hazards

        Apply Tracks 04 and 05. Look at the `time_to_infection_mo` column for the TNFi arm. What pattern do you see in *when* the events occur? What does that pattern do to a single, time-averaged hazard ratio? What analysis would handle it correctly?
        """
    )
    return


@app.cell
def _(commit_text):
    step4_widget, step4_ready = commit_text(
        "Your non-proportional-hazards analysis",
        min_chars=80,
    )
    step4_widget
    return step4_ready, step4_widget


@app.cell
def _(mo, reveal, step4_ready, step4_widget):
    mo.stop(
        not step4_ready(),
        mo.callout(
            mo.md("_Write at least a paragraph above. The reveal opens at 80 characters._"),
            kind="neutral",
        ),
    )

    ideal_4 = (
        "**The TNFi events cluster in the first 6 months.** Looking at the `time_to_infection_mo` column for the TNFi serious-infection events in the sample: 4.0, 4.5, 8.0, 3.5, 5.5, 5.0, 4.0. Six of seven events occurred within 6 months of TNFi initiation, which is the Galloway 2011 BSRBR pattern: the elevated infection risk on anti-TNF concentrates in the early months after initiation, then attenuates. The csDMARD events in the sample (rows 11 and 24) occurred at 14 and 22 months, distributed across the follow-up window.\n\n"
        "**What that pattern does to a single Cox HR.** Cox proportional-hazards regression averages the hazard ratio over time. If TNFi has a high hazard ratio in months 0-6 and a near-null hazard ratio thereafter, a single HR will summarize this as an intermediate value that describes neither period accurately. The proportional-hazards assumption fails, which means the HR no longer has its plain-English reading of 'events happen X times as fast in TNFi at every moment.' Track 05's KM curves-cross demo is exactly this scenario.\n\n"
        "**What to do instead.**\n"
        "- **Time-stratified analysis.** Split follow-up into 0-6 months and 6+ months. Report two HRs. The early-period HR is the clinically interesting number (the early-induction infection risk). The late-period HR tests whether the elevated risk is sustained.\n"
        "- **Piecewise (time-varying) Cox regression.** Fit a Cox model with TNFi-by-time interaction, treating the hazard ratio as a step function with a breakpoint at 6 months (or fit a continuous time interaction).\n"
        "- **Test the PH assumption directly.** Schoenfeld residuals plot will show a non-flat pattern over time when PH fails; report the test (e.g., the `survival::cox.zph` style diagnostic) alongside the HR.\n"
        "- **KM curves with number-at-risk table.** Show the figure. A reader can see curves cross or fan out where a single HR would hide it.\n\n"
        "Report both the time-averaged HR (if you must give a single number) and the time-stratified HRs, and be explicit that the proportional-hazards assumption fails."
    )

    reveal(step4_widget.value, ideal_4, learner_label="Your non-proportional-hazards analysis")
    return (ideal_4,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Step 5 of 6: Propose mitigations

        Now collect the mitigations. For each of the three threats (confounding, selection bias / informative censoring, non-proportional hazards), name the specific analytic moves you would actually run, and the residual limitation each move cannot fix. Be explicit about what the analysis can and cannot say.
        """
    )
    return


@app.cell
def _(commit_text):
    step5_widget, step5_ready = commit_text(
        "Your mitigation plan",
        min_chars=120,
    )
    step5_widget
    return step5_ready, step5_widget


@app.cell
def _(mo, reveal, step5_ready, step5_widget):
    mo.stop(
        not step5_ready(),
        mo.callout(
            mo.md("_Write your mitigation plan above. The reveal opens at 120 characters._"),
            kind="neutral",
        ),
    )

    ideal_5 = (
        "**Mitigation menu, per threat.**\n\n"
        "**Threat 1, confounding by indication.**\n"
        "- *Multivariable Cox regression* adjusting for age, sex, seropositive, disease duration, baseline DAS28, and prednisone use at enrollment. Report HR with a 95% CI. This is the standard mitigation and the one the committee will expect.\n"
        "- *Propensity-score methods.* Estimate the probability of receiving TNFi given the same covariate set, then either match TNFi-treated to csDMARD-treated patients on the propensity score or use inverse-probability-of-treatment weighting (IPW). Both approaches estimate the same target estimand more flexibly than a single regression and let you assess covariate balance after weighting.\n"
        "- *E-value sensitivity analysis* (VanderWeele) for *unmeasured* confounding. Reports the minimum strength of association an unmeasured confounder would have to have with both treatment and outcome to explain away the observed HR. The right tool for naming what is left after measured-confounder adjustment.\n"
        "- *Residual limitation.* Unmeasured confounders (smoking, frailty, prior infections, BMI, comorbidities) remain. The E-value bounds the impact but does not fix the problem.\n\n"
        "**Threat 2, selection bias and informative censoring.**\n"
        "- *Characterize the registry vs the clinic.* Pull the underlying Mercy clinic roster (age, sex, disease duration, current treatment) and show how the registry compares. Report the comparison as a baseline-table column.\n"
        "- *Code dropout reasons* when possible. If the EHR has structured dropout reasons, separate administrative drop (moved away, end of follow-up) from clinical drop (adverse event, treatment failure). Treat clinical drops as informative when running the analysis.\n"
        "- *Sensitivity analyses bracketing missing-not-at-random scenarios.* Compute the IRR under two extreme assumptions: every TNFi dropout had an event at the time of dropout (worst case for TNFi); no TNFi dropout had an event (best case for TNFi). Report the bracket as the range the true effect plausibly falls in.\n"
        "- *Residual limitation.* The selection mechanism cannot be fully recovered from a registry that does not contain the non-enrolled patients. The brackets bound the uncertainty; they do not eliminate it.\n\n"
        "**Threat 3, non-proportional hazards.**\n"
        "- *Time-stratified analysis* with a 6-month breakpoint, reporting two HRs (0-6 mo, 6+ mo).\n"
        "- *Plot Kaplan-Meier curves with a number-at-risk table.* The figure itself is the most honest summary when PH fails.\n"
        "- *Test the PH assumption* with Schoenfeld residuals; report the test result alongside the HR.\n"
        "- *Residual limitation.* Even with time stratification, the early-period HR is estimated on small numbers (most events happen there, but follow-up is short), so the CI is wide. Pre-specify the breakpoint to avoid post-hoc justification.\n\n"
        "**What you cannot fix in this analysis at all.** This is a single-site community registry with 812 patients and three years of follow-up. The result will not generalize to other settings without explicit external validation. Pre-specify that limitation in the methods, and make external generalizability a follow-up project."
    )

    reveal(step5_widget.value, ideal_5, learner_label="Your mitigation plan")
    return (ideal_5,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Step 6 of 6: Write the analysis plan

        Write the one-paragraph analysis plan you would put on the front page of the protocol you hand to the rheumatologist. Name the target estimand, the design, the primary analysis, the sensitivity analyses, and the limitations you will pre-specify. This is the document the committee will read first.
        """
    )
    return


@app.cell
def _(commit_text):
    step6_widget, step6_ready = commit_text(
        "Your one-paragraph analysis plan",
        min_chars=200,
    )
    step6_widget
    return step6_ready, step6_widget


@app.cell
def _(mo, reveal, step6_ready, step6_widget):
    mo.stop(
        not step6_ready(),
        mo.callout(
            mo.md("_Write the analysis plan above. The reveal opens at 200 characters._"),
            kind="neutral",
        ),
    )

    ideal_6 = (
        "**Analysis plan: Mercy Community Rheumatology Registry, TNFi and serious infection.**\n\n"
        "We will estimate the causal effect of TNFi initiation versus continued csDMARD on the rate of hospitalization-requiring serious infection among adults with RA enrolled in the Mercy Community Rheumatology Registry between 2022 and 2025, with up to three years of follow-up. The primary analysis is a multivariable Cox proportional-hazards regression adjusting for age, sex, seropositivity, RA duration, baseline DAS28, and chronic prednisone use at enrollment, reporting an adjusted hazard ratio with a 95% confidence interval. Because the Galloway BSRBR literature documents a time-varying TNFi infection risk that concentrates in the first six months, we will pre-specify time-stratified analyses with a six-month breakpoint and report two HRs (0-6 mo, 6+ mo), test the proportional-hazards assumption via Schoenfeld residuals, and present Kaplan-Meier curves with a number-at-risk table. For unmeasured confounding (smoking, frailty, prior infections, BMI, comorbidities), we will report an E-value (VanderWeele) quantifying the minimum strength an unmeasured confounder would need to have to explain away the observed effect. For informative censoring driven by treatment-related dropout, we will conduct bracketing sensitivity analyses under best-case and worst-case missing-not-at-random assumptions. We will pre-specify that the registry is not a random sample of the Mercy clinic population, characterize the difference in a baseline-table column, and acknowledge limited generalizability outside the registry. The plan will be circulated to the quality committee before any analysis is run, to avoid the selective-reporting trap that the analysis itself is meant to expose.\n\n"
        "*That paragraph is what the front of the protocol looks like. The rheumatologist asked for a number; the work of this analysis is to produce a number that earns the framing it carries.*"
    )

    reveal(step6_widget.value, ideal_6, learner_label="Your analysis plan")
    return (ideal_6,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Synthesis: assemble the committee memo

        Below is the analysis-plan memo, assembled from your written answers. Read it as a draft of what you would hand the rheumatologist before any analysis runs. Edit it in the box at the bottom into the final version.
        """
    )
    return


@app.cell
def _(mo, step1_widget, step2_widget, step3_widget, step4_widget, step5_widget, step6_widget):
    memo = (
        "## Analysis plan: Mercy Community Rheumatology Registry\n\n"
        "**Author:** Clinical informatics representative (you).\n\n"
        "**Question:** Does TNFi increase serious infection rate compared with csDMARD-only treatment in adults with RA in this registry?\n\n"
        "**Summary recommendation:** Run a multivariable, time-stratified, sensitivity-analysis-supported observational analysis with pre-specified limitations. Do not put a single time-averaged hazard ratio on a slide as the headline number.\n\n"
        "---\n\n"
        "### 1. Question and target estimand\n\n"
        f"{step1_widget.value or '_[your Step 1 writing]_'}\n\n"
        "### 2. Threat 1: confounding by indication\n\n"
        f"{step2_widget.value or '_[your Step 2 writing]_'}\n\n"
        "### 3. Threat 2: selection bias and informative censoring\n\n"
        f"{step3_widget.value or '_[your Step 3 writing]_'}\n\n"
        "### 4. Threat 3: non-proportional hazards\n\n"
        f"{step4_widget.value or '_[your Step 4 writing]_'}\n\n"
        "### 5. Mitigation menu\n\n"
        f"{step5_widget.value or '_[your Step 5 writing]_'}\n\n"
        "### 6. Pre-specified analysis plan\n\n"
        f"{step6_widget.value or '_[your Step 6 writing]_'}\n\n"
        "---\n\n"
        "### What this memo commits us to\n\n"
        "- Multivariable Cox regression adjusting for measured confounders (age, sex, seropositive, RA duration, baseline DAS28, chronic prednisone).\n"
        "- Time-stratified analysis with a 6-month breakpoint; two HRs reported.\n"
        "- Kaplan-Meier curves with number-at-risk table; Schoenfeld residual test of the PH assumption.\n"
        "- E-value sensitivity analysis for unmeasured confounding.\n"
        "- Bracketing sensitivity analyses for informative censoring.\n"
        "- Baseline-table comparison of registry vs underlying clinic population.\n"
        "- All decisions pre-specified before analysis runs.\n\n"
        "*Ready to send to the rheumatologist. Edit in the box below if you want to revise the recommendation language.*"
    )

    mo.md(memo)
    return (memo,)


@app.cell
def _(memo, mo):
    final_memo = mo.ui.text_area(
        label="Final memo (edit as needed)",
        value=memo,
        rows=24,
        full_width=True,
    )
    final_memo
    return (final_memo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Reflection

        What surprised you most in walking through this analysis? Or: when you have done observational analyses in the past, which of these three threats did you address the least carefully, and what would change about your next analysis?
        """
    )
    return


@app.cell
def _(reflection):
    _reflection_widget, reflection_layout = reflection(
        "Your reflection on this analysis.",
    )
    reflection_layout
    return (reflection_layout,)


@app.cell
def _(go_deeper, mo):
    closing = mo.vstack(
        [
            mo.md(
                r"""
                ---

                ## What this leaves you

                The five-track framework of Course 04 is now in your hands, applied to a single concrete observational analysis:

                1. **Frequency and association measures** (Track 1): the incidence rate and the hazard ratio are the right vocabulary for time-to-event outcomes with unequal follow-up.
                2. **Bias and DAGs** (Track 2): confounding by indication is the perennial threat in pharmacoepidemiology; the DAG lets you decide what to adjust for and what not to.
                3. **Diagnostic test performance** (Track 3): not directly in play here, but the same 2x2 vocabulary appears in CDS evaluation (Course 12) and decision curve analysis (Course 11).
                4. **Basic statistical tests** (Track 4): the variable-type-by-variable-type framework; CI carries the magnitude information the p-value collapses.
                5. **Study designs** (Track 5): the five-question design-picker, person-time as the denominator of incidence and HR, Kaplan-Meier intuition, and the proportional-hazards assumption.

                Course 09 (AI in medicine) will deepen the validity questions for predictive models. Course 11 (health economics) brings decision curve analysis as the unifying framework for "at what threshold does this intervention create net benefit?" Course 12 (clinical decision support) is where the work of this course is tested under deployment.
                """
            ),
            go_deeper(
                "If you write this plan for a real registry analysis on your institution's docket, you have done the work this course was designed to prepare you for. The pre-specified protocol is the contribution; the resulting paper is the proof you can apply it."
            ),
        ]
    )
    closing
    return (closing,)


if __name__ == "__main__":
    app.run()
