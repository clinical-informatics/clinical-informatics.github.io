"""Track 05: When to trust a computer.

The four-question framework for any clinical algorithm: what was it
trained on, what does it optimize for, where does it fail, and who does
it fail for. Applied here to a fictional vendor's deterioration-
prediction score in a community-hospital setting.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 05: When to trust a computer

        ## The scenario.

        A vendor has come to your community hospital with a deterioration-prediction score. The pitch deck is glossy. The numbers it leads with:

        - **AUC 0.84** in their held-out validation cohort.
        - **Trained on 2.4 million encounter-snapshots** across twelve academic medical centers, 2017-2022.
        - **Outperforms NEWS by 14 AUC points and MEWS by 18.**
        - **Real-time scoring through a FHIR integration**, deployable in eight weeks.
        - **FDA-cleared** as a Class II clinical decision support tool.

        Your hospital is a 320-bed community facility. Your catchment is 35% Hispanic, 28% Black, 32% non-Hispanic white, 5% Asian and other. Mean age 68. You do not have a 24/7 rapid response team. Your EHR is from a different vendor than the development sites. The contract is in front of you, and the CMO wants your input by next week's CDS committee.

        You are not going to make this decision on the AUC.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The four questions.

        The fluency you've been building in Tracks 01-04 collapses into one short framework for any clinical algorithm someone hands you:

        1. **What was it trained on?**
        2. **What does it optimize for?**
        3. **Where does it fail?**
        4. **Who does it fail for?**

        You answer all four, or you accept that you are deploying by trust. The notebook walks each question against what the vendor's pitch deck actually says (and what it conspicuously doesn't). At the end you will make a recommendation.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1. What was it trained on?

        The vendor's slide on training data answers this in two sentences:

        > *"Two-point-four million encounter-snapshots across twelve academic medical centers, 2017 to 2022. Outcome defined as transfer to higher level of care."*

        Read the slide twice. What does it answer, and what does it leave open?
        """
    )
    return


@app.cell
def _(mo):
    q1 = mo.ui.multiselect(
        options=[
            "Twelve academic medical centers is a narrow institutional spectrum; your community hospital differs in case mix, staffing thresholds, and clinical practice patterns.",
            "'Transfer to higher level of care' is an institution-specific operational outcome rather than a clinical event; what triggers a transfer at an AMC is not what triggers one at a community hospital without a rapid response team.",
            "The 2017-2022 window spans the pre- and post-pandemic eras together; the model may have learned patterns that drifted during training and may not match the case mix of 2026.",
            "The 0.84 AUC came from a held-out subset of the same twelve institutions, not from external community-hospital validation; the number does not tell you how the model performs at your site.",
        ],
        label="Which of these are real concerns about the training data? Pick everything that applies.",
    )
    q1
    return (q1,)


@app.cell
def _(mo, q1):
    if not (q1.value or []):
        q1_resp = mo.callout(mo.md("_Pick at least one._"), kind="neutral")
    else:
        q1_resp = mo.callout(
            mo.md(
                "**All four are real concerns.** The pitch deck did not actually tell you what the model was trained on; it told you the headline. The right next ask of the vendor is for the full data sheet: inclusion and exclusion criteria, age range, the breakdown of admissions versus encounters, the precise outcome adjudication, the era-by-era patient counts, and the external-validation results in non-academic settings. If the vendor cannot produce that, the model's claim on your patients is weaker than the AUC number suggests."
            ),
            kind="success",
        )
    q1_resp
    return (q1_resp,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2. What does it optimize for?

        The vendor's slide on the prediction objective:

        > *"Predicts in-hospital deterioration in the next four hours. Default alert threshold set to balance sensitivity and specificity on the development cohort: 70% sensitivity at 92% specificity."*

        That sounds like a clean number. Read it the way you read DAS28 in Track 04: where do the choices come from, and what would change if they had been made differently?
        """
    )
    return


@app.cell
def _(mo):
    q2 = mo.ui.multiselect(
        options=[
            "The four-hour prediction horizon assumes a workflow that can act on a four-hour-ahead signal; without a rapid response team, your floor's actionable interval may be longer or shorter than four hours.",
            "'Balance sensitivity and specificity on the development cohort' doesn't tell you what cost ratio between false positives and false negatives produced the threshold; that ratio is the dial that determines alert volume.",
            "92% specificity sounds high, but at a typical deterioration prevalence of two to three percent on a medicine floor, that still means roughly two-thirds of fired alerts are false positives at the vendor default.",
            "The default threshold is the vendor's choice averaged across twelve academic sites; the right threshold for your floor is a separate hospital-specific decision that the vendor will not make for you.",
        ],
        label="Which of these are real concerns about the optimization target? Pick everything that applies.",
    )
    q2
    return (q2,)


@app.cell
def _(mo, q2):
    if not (q2.value or []):
        q2_resp = mo.callout(mo.md("_Pick at least one._"), kind="neutral")
    else:
        q2_resp = mo.callout(
            mo.md(
                "**All four.** The prediction horizon and the threshold together define what the model is actually doing in the workflow. The vendor's defaults were chosen for *their* reference institutions; neither your actionable interval nor your tolerance for false-positive load were part of the calibration. Two separate questions to take to the next meeting: what horizon matches what your nursing staff can act on, and what alert volume can your floor sustain without alert fatigue overwhelming the signal?"
            ),
            kind="success",
        )
    q2_resp
    return (q2_resp,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3. Where does it fail?

        The vendor's slide on robustness:

        > *"External validation at three additional academic medical centers showed AUCs between 0.81 and 0.83. Production drift monitoring is via monthly dashboards reporting input feature distributions."*

        Track 02 named five recurring sources of edge cases: phenotypic mimics, suppressed signals, off-cohort, off-window, missing data. Track 03 named leakage as a sixth, in the modeling sense. Read the slide against those.
        """
    )
    return


@app.cell
def _(mo):
    q3 = mo.ui.multiselect(
        options=[
            "External validation in three more academic centers tells you nothing about how the model performs at community hospitals, which is what you are.",
            "Monthly drift monitoring is reactive, not proactive; a feature distribution that shifts in week one shows up in your dashboard in week three, after it has already affected the alerts on your floor.",
            "All of the validation cohorts predate any post-pandemic patterns; nothing in the documented robustness data shows how the model handles 2025-2026 patients.",
            "There is no documented behavior for out-of-distribution patients (patients who don't resemble anyone in the training set); modern models produce a confident-looking number anyway.",
        ],
        label="Which of these are real concerns about failure modes? Pick everything that applies.",
    )
    q3
    return (q3,)


@app.cell
def _(mo, q3):
    if not (q3.value or []):
        q3_resp = mo.callout(mo.md("_Pick at least one._"), kind="neutral")
    else:
        q3_resp = mo.callout(
            mo.md(
                "**All four.** The vendor has reported on a narrow slice of where the model could fail: known sites, known era, in-distribution patients, retrospective evaluation. The deployment-relevant failure modes (community-hospital case mix, real-time drift, out-of-distribution patients, workflow-induced bias in the deployment data) are precisely the ones the documented robustness work did not interrogate. The right ask is for prospective evaluation in a community setting before your deployment, or a structured pilot that produces that evaluation on your data."
            ),
            kind="success",
        )
    q3_resp
    return (q3_resp,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 4. Who does it fail for?

        The vendor's slide on subgroup performance:

        > *"Subgroup analysis showed AUC of 0.83 across age, sex, and race subgroups in the development cohort."*

        That is one sentence about subgroup performance. What is it actually telling you, and what is it leaving out?
        """
    )
    return


@app.cell
def _(mo):
    q4 = mo.ui.multiselect(
        options=[
            "'AUC across race subgroups' is reported in aggregate, not broken out by race; you cannot tell whether a specific subgroup performed substantially worse.",
            "The development cohort's racial composition (likely majority non-Hispanic white at academic medical centers) does not match your catchment, which is 35% Hispanic.",
            "Subgroup performance was not reported by primary language, insurance class, or any SDOH variable; those are often where the largest disparities live.",
            "Discrimination (AUC) was reported but calibration by subgroup was not; a model can discriminate equally well across subgroups while systematically over- or under-predicting for one of them.",
        ],
        label="Which of these are real concerns about subgroup performance? Pick everything that applies.",
    )
    q4
    return (q4,)


@app.cell
def _(mo, q4):
    if not (q4.value or []):
        q4_resp = mo.callout(mo.md("_Pick at least one._"), kind="neutral")
    else:
        q4_resp = mo.callout(
            mo.md(
                "**All four.** This is the question most often skipped by vendors and most often responsible for the harms that show up after deployment. The Vyas and Obermeyer literature cited in Track 03 lives precisely here: the model designers had answers to questions 1 through 3, and no useful answer to question 4, and the harm was on the patients the answer did not exist for. The right ask is for subgroup-stratified discrimination AND calibration AND alert positive predictive value, broken out by the demographic and clinical subgroups present in your catchment, before deployment."
            ),
            kind="success",
        )
    q4_resp
    return (q4_resp,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Reading the four together.

        The four questions don't have to point at the same gap, and in this case they don't.

        - **Q1 (training).** The model's memory is academic-medical-center adults across a five-year window with an institution-specific outcome definition. Your population, your workflow, and your era are all outside that memory.
        - **Q2 (optimization).** The prediction horizon and threshold were chosen for the vendor's reference institutions and their workflow. Your floor's actionable interval and your alert tolerance have not been factored into the dial.
        - **Q3 (where it fails).** External validation was confined to more academic centers. Nothing has been documented about community-hospital performance, post-pandemic patterns, or out-of-distribution patients. Drift monitoring is reactive and monthly.
        - **Q4 (who it fails for).** Subgroup performance was reported in aggregate across race subgroups and not at all by language, insurance, or SDOH. Your catchment is 35% Hispanic and the development cohort was not.

        Each gap on its own might be deployable around. Together they tell you the same thing: you are being asked to deploy an experiment, and the vendor is offering you a contract rather than an experimental protocol.
        """
    )
    return


@app.cell
def _(mo):
    decision = mo.ui.radio(
        options=[
            "Deploy as the vendor configured it. The AUC is strong and the lift over NEWS/MEWS is meaningful.",
            "Adopt with local recalibration on the past year of your discharge data. Same model, retuned to your population.",
            "Pilot in one unit for six months with explicit subgroup performance monitoring and a written stopping rule before any broader deployment.",
            "Decline. The score is not ready for this hospital with what you currently know.",
        ],
        label="Given everything above, what is your recommendation to the CDS committee?",
    )
    decision
    return (decision,)


@app.cell
def _(decision, mo):
    if decision.value is None:
        d_resp = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif decision.value.startswith("Pilot in one unit"):
        d_resp = mo.callout(
            mo.md(
                "**Most defensible given what you know.** Multiple gaps across the four questions, but the model is not disqualified outright. The proportionate response is to pilot, in writing, with explicit subgroup performance monitoring (broken out by your catchment's specific subgroups, not the vendor's aggregate categories), a clear stopping rule (subgroup AUC below 0.70, calibration error above some threshold, alert PPV below some floor), and a duration that captures seasonality and at least one EHR-upgrade cycle. A pilot converts the four-question gaps into local evidence rather than letting them surface through patient harm."
            ),
            kind="success",
        )
    elif decision.value.startswith("Decline"):
        d_resp = mo.callout(
            mo.md(
                "**Also defensible.** If the pilot conditions cannot be negotiated (and they often cannot, with a vendor invested in protecting its headline AUC), declining is the right move. You can ask the vendor to come back after they have done the subgroup work and the external validation in a community setting that resembles yours. Some vendors will; many will not. Both outcomes are useful information about the vendor."
            ),
            kind="success",
        )
    elif decision.value.startswith("Adopt with local recalibration"):
        d_resp = mo.callout(
            mo.md(
                "**Partial.** Recalibration addresses Q1 and parts of Q2: the model's coefficients can be re-fit on your discharge data to match your case mix and your local outcome prevalence. What recalibration does not address is Q4 (subgroup performance has never been measured in your catchment) or Q3 (drift monitoring is still reactive and external validation is still academic-only). Recalibration belongs inside a pilot, not as a substitute for one. Recalibrate-and-deploy assumes the model's shape transfers to your population; the shape might be fine, but the question is how you would know before harming a patient."
            ),
            kind="warn",
        )
    else:
        d_resp = mo.callout(
            mo.md(
                "**No.** The vendor's AUC is on their patients at their institutions in their era. You don't know what the model does with patients who don't match the training distribution, and a third of your catchment does not. The lift over NEWS and MEWS was measured at the development sites; nothing about that lift transfers automatically to your hospital. Deploy-as-configured treats the four questions as window dressing, which is exactly the trap this track is designed to keep you out of."
            ),
            kind="warn",
        )
    d_resp
    return (d_resp,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What you did in this track.

        - You learned the four-question framework: training data, optimization target, where it fails, who it fails for.
        - You applied it to a vendor pitch deck and located the gaps the deck would not surface on its own.
        - You made a deployment recommendation grounded in the four questions, not in the headline AUC.

        Most CDS papers, vendor pitches, and FDA submissions lead with the AUC and a clean-sounding cohort description. Your job, given the moves you have now, is to read past all of that and answer the four questions yourself.

        ## What's next.

        **The course capstone.** A Socratic walkthrough where you design your own clinical decision rule, drawing on decomposition (Track 01), edge-case generation (Track 02), abstraction (Track 03), algorithmic reading (Track 04), and the trust framework (this track). The output is a written design document an implementation team could act on. That document is what fluency in computational thinking looks like applied to your own work, and it is the artifact you can carry into the next real CDS conversation you find yourself in.
        """
    )
    return


if __name__ == "__main__":
    app.run()
