"""Capstone for course 09: Critical appraisal of a vendor "RA flare predictor".

A Socratic six-step appraisal exercise. A vendor pitches the rheumatology
practice that cares for Ms. Reyes on an "RA flare predictor". The vendor
hands over a one-page sales sheet with five claims. The capstone applies the
five-dimension framework from Track 04 and the fairness questions from
Track 05 to each claim. The learner commits an answer for each step before
the reveal unlocks.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    # Socratic helpers, inlined per the WASM rule against shared.X imports.
    def commit_text(prompt, min_chars=40):
        widget = mo.ui.text_area(
            label=prompt,
            rows=6,
            full_width=True,
            placeholder="Take a few sentences. The reveal will not unlock until you do.",
        )

        def ready():
            value = widget.value or ""
            return len(value.strip()) >= min_chars

        return widget, ready

    def reveal(learner_value, ideal_answer, learner_label="Your answer"):
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
                            mo.md("**How we would think through this**"),
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
            placeholder=placeholder or "Take a few sentences. No reveal here. The reflection is the work.",
        )
        layout = mo.vstack(
            [
                widget,
                mo.callout(
                    mo.md("_There is no answer key for this one. The point is to make your reasoning explicit to yourself._"),
                    kind="neutral",
                ),
            ]
        )
        return widget, layout

    return commit_text, mo, reflection, reveal


@app.cell
def _(mo):
    mo.md(
        r"""
        # Capstone: Critical appraisal of a vendor "RA flare predictor"

        ## The scenario

        A vendor walks into the rheumatology practice that cares for Ms. Reyes. The pitch: their machine-learning product, the **RheumaPredict Flare Risk Score**, predicts the probability that an RA patient will experience a clinical flare within the next 90 days. The vendor offers a one-page sales sheet with five claims and proposes a six-month pilot.

        The practice has asked the clinical informaticist on staff (the reader) to evaluate the product before the pilot. The capstone is the appraisal. The reader works through the six steps below, committing an answer to each before the reveal unlocks.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            ### RheumaPredict Flare Risk Score: vendor sales sheet

            1. **Outcome.** Predicts "flare risk" within 90 days.
            2. **Training cohort.** Trained on 4,200 RA patients from a large academic medical center, 2018 to 2023.
            3. **Performance.** AUC 0.82 on the internal validation set.
            4. **Validation approach.** 80/20 train-test split on the academic-center cohort.
            5. **Other.** "Built with state-of-the-art deep learning techniques. FDA-cleared status pending."

            **Asking price.** $48,000 / year for the practice, plus $9 per patient per year.

            **Vendor recommendation.** Deploy as a CDS alert in the EHR; trigger the alert on chart open when the model score exceeds 0.40. The vendor projects "20 to 30% reduction in emergency-department visits within the first year."
            """
        ),
        kind="warn",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Step 1: outcome definition

        The vendor's outcome is "flare risk within 90 days." Critique this definition. What is missing, and what would you ask the vendor to clarify before any further evaluation?
        """
    )
    return


@app.cell
def _(commit_text):
    step1_widget, step1_ready = commit_text("Critique the outcome definition. What questions would you ask the vendor?")
    step1_widget
    return step1_ready, step1_widget


@app.cell
def _(mo, reveal, step1_ready, step1_widget):
    mo.stop(not step1_ready(), mo.md("_Write a few sentences above to unlock the reveal._"))
    reveal(
        step1_widget.value,
        """
        The definition "flare within 90 days" has three load-bearing ambiguities.

        **First, what counts as a flare?** ACR has no single operational flare definition. The Flare-RA score, the OMERACT flare definition, the DAS28 >= 1.2-point increase, the patient-reported "I am having a flare" question, and the rheumatologist's clinical judgment all label different patient-events as flares. A 90-day prediction window is meaningless until the label is specified.

        **Second, how was the label adjudicated?** Possibilities: extracted from a structured EHR field (rare), inferred from medication changes (proxy with confounders), inferred from ICD-10 codes (poor specificity for flare), adjudicated by chart review (better but expensive), patient-reported (likely available only at a research-active center). Each method introduces a different bias.

        **Third, what does the 90-day window refer to?** Days 0 to 90 from the prediction moment? Days 0 to 90 from the most recent visit? Days 0 to 90 from any encounter? A precise time origin is required to compare the prediction against an outcome.

        **What to ask the vendor.** (1) Exact operational definition of "flare" used as the training label. (2) The data source the label was extracted from and the adjudication procedure. (3) The exact time origin and time window. (4) The label prevalence in the training cohort. Without specific answers to all four, the rest of the appraisal cannot proceed.
        """,
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Step 2: training population

        The vendor reports "4,200 RA patients from a large academic medical center, 2018 to 2023." What questions does this raise about the fit between the training cohort and your practice's population?
        """
    )
    return


@app.cell
def _(commit_text):
    step2_widget, step2_ready = commit_text("What do you need to know about the training cohort?")
    step2_widget
    return step2_ready, step2_widget


@app.cell
def _(mo, reveal, step2_ready, step2_widget):
    mo.stop(not step2_ready(), mo.md("_Write a few sentences above to unlock the reveal._"))
    reveal(
        step2_widget.value,
        """
        Three categories of question follow from the brief description.

        **Demographics.** What is the cohort's distribution by race, sex, age, insurance type, and language? Is it similar to the practice's patient population? Ms. Reyes is 52, Hispanic, English- and Spanish-speaking, on commercial insurance. A model trained on a cohort with little representation of Hispanic patients on commercial insurance has not been evaluated on the patient population the practice cares for.

        **Clinical profile.** What fraction of the training cohort was on biologic therapy, on conventional DMARDs, on no DMARD? What was the median disease duration? What was the median DAS28? Ms. Reyes is on MTX plus adalimumab with moderate disease activity; a model trained predominantly on early-disease MTX-monotherapy patients will not have learned the dynamics relevant to her.

        **Healthcare-system context.** The training cohort came from an academic medical center. Academic centers see more refractory disease, more comorbidity, and have richer documentation than community practices. A model trained on academic data may pick up features (the structure of the order set, the timing of a rheumatology-fellow note) that are not present in the community practice's EHR and will not generalize.

        **What to ask the vendor.** (1) Full demographic breakdown with sample sizes per subgroup. (2) Clinical profile distribution. (3) Whether external validation has been performed on a community-practice cohort. If not, the practice's case-mix has not been tested against this model.
        """,
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Step 3: validation approach

        The vendor reports "AUC 0.82 on the internal validation set, 80/20 train-test split." What is wrong with this report?
        """
    )
    return


@app.cell
def _(commit_text):
    step3_widget, step3_ready = commit_text("Critique the validation approach. What is missing?")
    step3_widget
    return step3_ready, step3_widget


@app.cell
def _(mo, reveal, step3_ready, step3_widget):
    mo.stop(not step3_ready(), mo.md("_Write a few sentences above to unlock the reveal._"))
    reveal(
        step3_widget.value,
        """
        Three issues, in order of severity.

        **No external validation.** The 80/20 split is on the same cohort the model was trained on. Internal validation is the floor; an honest performance estimate requires evaluation against a cohort the model has not seen. For a single-academic-center model, the relevant external validation is on a community cohort (geographic and case-mix shift), a more recent cohort (temporal shift), and a different EHR vendor (data-pipeline shift). None of these is reported. The 0.82 AUC is almost certainly an overestimate of the model's performance at the practice that is considering adoption.

        **Splitting unit is not specified.** Was the 80/20 split done by patient or by encounter? If by encounter, the same patient could appear in both training and test sets and the AUC is inflated. Splitting by patient is the minimum acceptable practice for any longitudinal clinical model.

        **No confidence interval and no other discrimination metrics.** A single point estimate (AUC 0.82) without a confidence interval is insufficient. The AUC could be 0.82 with a CI of 0.79 to 0.85 (precise) or with a CI of 0.71 to 0.91 (uninformative). Additional discrimination metrics (sensitivity and specificity at the proposed alert threshold, PPV and NPV at the practice's expected flare prevalence) are also required for any deployment decision.

        **What to ask the vendor.** (1) Was the split by patient? (2) What is the 95% CI on the AUC? (3) What are sensitivity, specificity, PPV, and NPV at the proposed 0.40 threshold? (4) Is external validation available on a non-academic cohort? If not, the practice should require it before pilot deployment.
        """,
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Step 4: calibration

        The vendor does not report calibration. The proposed deployment fires an alert when the model score exceeds 0.40. Why is the calibration omission a load-bearing problem?
        """
    )
    return


@app.cell
def _(commit_text):
    step4_widget, step4_ready = commit_text("Why does the missing calibration report matter for the proposed alert deployment?")
    step4_widget
    return step4_ready, step4_widget


@app.cell
def _(mo, reveal, step4_ready, step4_widget):
    mo.stop(not step4_ready(), mo.md("_Write a few sentences above to unlock the reveal._"))
    reveal(
        step4_widget.value,
        """
        The proposed alert threshold of 0.40 is meaningful only if the model's stated probabilities track observed event rates. A miscalibrated model whose stated probabilities systematically over-shoot or under-shoot the truth will fire alerts at the wrong rate.

        **Two concrete failure modes follow.** Suppose the model is over-calibrated at the high end: when it says 0.40, the actual flare rate is 0.15. Then the 0.40 alert threshold is effectively a 0.15-actual-risk threshold; the alert will fire on patients whose true risk does not warrant the workflow burden, the override rate will climb, and the alert will be ignored within months (alert fatigue, Course 12 territory).

        Conversely, suppose the model is under-calibrated at the high end: when it says 0.40, the actual flare rate is 0.70. Then the 0.40 threshold is effectively a 0.70-actual-risk threshold; the alert will fail to fire on patients who are at substantial risk, and the predicted "20-30% ED-visit reduction" will not materialize because the alert is missing the patients it most needed to catch.

        **The clinician's actions depend on the probability.** A clinician told "this patient has a 40% chance of a flare in the next 90 days" plans differently than one told "this patient has a 10% chance" or "an 80% chance." If the number does not mean what the clinician thinks it means, every downstream decision is wrong.

        **What to ask the vendor.** (1) A calibration plot from the validation cohort. (2) The Brier score. (3) Calibration-in-the-large (mean predicted probability vs observed event rate). (4) The same calibration metrics on any external validation cohort. Without all four, the alert threshold cannot be set responsibly.
        """,
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Step 5: subgroup performance and fairness

        The vendor does not report subgroup performance. What subgroups would you require performance breakdowns on, and why?
        """
    )
    return


@app.cell
def _(commit_text):
    step5_widget, step5_ready = commit_text("Which subgroups need separate performance breakdowns, and what would you do if performance differs?")
    step5_widget
    return step5_ready, step5_widget


@app.cell
def _(mo, reveal, step5_ready, step5_widget):
    mo.stop(not step5_ready(), mo.md("_Write a few sentences above to unlock the reveal._"))
    reveal(
        step5_widget.value,
        """
        At least five subgroups warrant separate performance breakdowns for an RA flare predictor.

        - **Race and ethnicity.** RA prevalence, presentation, and treatment response differ across populations. The Obermeyer 2019 pattern (race-correlated proxy bias) is a documented risk for any clinical-prediction model.
        - **Sex.** RA is approximately 3:1 female; a model trained on a predominantly female cohort may perform poorly on the smaller male subgroup.
        - **Age.** Elderly-onset RA differs from working-age RA in presentation, biologic response, and comorbidity profile. The practice should require AUC and calibration in the elderly subgroup separately.
        - **Treatment regimen.** Patients on MTX monotherapy, on MTX + a TNFi, on a non-TNF biologic, and on JAKi may have very different flare dynamics. Ms. Reyes is on MTX + adalimumab; a model whose performance is dominated by MTX-monotherapy patients may not predict her flares well.
        - **Disease duration.** Early disease (< 2 years) and established disease (5+ years) have different flare patterns. The model's performance should be reported in both.

        **What to do if performance differs by subgroup.** Two options. (1) Restrict the deployment to the subgroups where the model performs adequately (define adequacy in advance: AUC >= 0.75 and calibration intercept within ±0.1 of zero, say). (2) Require the vendor to retrain or recalibrate on the local cohort with subgroup-stratified evaluation. Either path requires the subgroup-performance report to even start.

        **The minimum vendor request.** AUC and calibration plot reported separately for each subgroup above, with sample sizes per subgroup. If the vendor cannot or will not provide this, the appraisal answer is no.
        """,
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Step 6: adoption recommendation

        Pulling the previous five steps together, what is your recommendation to the practice? Adopt the pilot, defer adoption, or refuse adoption? What conditions would change your answer?
        """
    )
    return


@app.cell
def _(commit_text):
    step6_widget, step6_ready = commit_text("Make your recommendation. State the conditions that would change it.")
    step6_widget
    return step6_ready, step6_widget


@app.cell
def _(mo, reveal, step6_ready, step6_widget):
    mo.stop(not step6_ready(), mo.md("_Write a few sentences above to unlock the reveal._"))
    reveal(
        step6_widget.value,
        """
        **Defer adoption pending vendor responses.** The vendor's one-page sheet does not contain enough information to support a pilot decision. The conditions that would change the recommendation:

        - **Outcome definition** documented in operational form with the label-adjudication procedure stated.
        - **Training cohort** documented with full demographic and clinical breakdown.
        - **External validation** reported on a non-academic cohort with similar case-mix to the practice; AUC and calibration acceptable on that cohort.
        - **Calibration** reported with a plot, Brier score, and calibration-in-the-large, and acceptable at the proposed 0.40 threshold.
        - **Subgroup performance** reported for race, sex, age, treatment regimen, and disease duration, with AUC and calibration in each.
        - **Post-deployment monitoring plan** documented: who is responsible for monitoring subgroup performance after deployment, on what schedule, and what triggers a re-evaluation.

        With all six conditions met, a six-month pilot with explicit monitoring is reasonable. Without them, the projected "20-30% ED-visit reduction" is an unsupported marketing claim, and pilot deployment risks burning clinician trust on an alert that may not work.

        **The broader judgment.** A clinical informaticist's job is to be the institution's check on vendor claims. The vendor's sales sheet was not written to support a clinical informaticist's appraisal; it was written to support a procurement decision by someone without the informatics training to ask these questions. The appraisal value is in asking the questions, and in being willing to recommend deferral when the answers are not forthcoming.
        """,
    )
    return


@app.cell
def _(mo, reflection):
    refl_widget, refl_layout = reflection(
        "Reflection: which of the five appraisal dimensions felt hardest to evaluate from a vendor sales sheet alone? What experience or training would you want before having to make this call at your institution?",
        placeholder="Think about a real or plausible procurement decision. What would you actually do?",
    )
    refl_layout
    _ = mo
    return refl_layout, refl_widget


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            ### Go deeper

            The published reference frameworks most directly applicable to this appraisal are TRIPOD-AI (the AI-specific extension of the TRIPOD prediction-model reporting guideline) and PROBAST (the prediction-model risk-of-bias tool). Both are linked from the Track 04 go-deeper. The Wynants et al. 2020 BMJ systematic review of COVID-19 prediction models is the most-cited published example of the framework being applied at scale; Sendak et al. 2020 on the Duke Sepsis Watch deployment is the most-cited example of a clinical AI rollout that took the appraisal questions seriously from the start.

            The fairness questions are addressed in detail in the Track 05 go-deeper. The Obermeyer et al. 2019 Science paper on algorithmic bias is the load-bearing clinical case.

            For the vendor-negotiation context specifically, the NIST AI Risk Management Framework and the FDA's evolving guidance on AI/ML-based Software as a Medical Device are the documents to cite in a procurement conversation.
            """
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        The capstone applied the Track 04 appraisal framework and the Track 05 fairness questions to a hypothetical vendor pitch. Six steps walked the outcome definition, the training population, the validation approach, the calibration, the subgroup performance, and the final adoption recommendation. The recommended outcome in every commit-then-reveal step was the same: defer the pilot until the missing dimensions are documented. The capstone is the operational form of the clinical informaticist's role at procurement: ask the questions, recommend deferral when the answers are not there, and require documentation before any patient is exposed to the model.

        Course 09 closes here. Course 10 (NLP and clinical text) takes up the language-processing side of clinical AI in the dimension this course only touched at the LLM intersection.
        """
    )
    return


if __name__ == "__main__":
    app.run()
