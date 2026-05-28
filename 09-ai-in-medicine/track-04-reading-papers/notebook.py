"""Track 04: Reading an AI paper critically.

A five-dimension framework for the critical appraisal of a clinical AI
prediction model: training population, outcome definition, validation
approach, calibration reporting, and subgroup performance. The track
applies the framework to a worked published-pattern case and provides an
interactive checklist the reader can apply to a paper of their own
choosing.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import types

    import marimo as mo
    import pandas as pd

    _COURSE_TITLES = {
        "03": "Privacy, ethics, and governance",
        "04": "Clinical epidemiology",
        "13": "Research reproducibility",
    }

    def _course_label(course_id):
        title = _COURSE_TITLES.get(course_id.split("-")[0])
        return f"Course {course_id}: {title}" if title else f"Course {course_id}"

    def _xref_callback(from_course, to_course, topic, body):
        return mo.callout(
            mo.md(f"**Callback to {_course_label(to_course)}.** {topic}\n\n{body}"),
            kind="neutral",
        )

    def _xref_forward(from_course, to_course, topic, body):
        return mo.callout(
            mo.md(f"**Forward to {_course_label(to_course)}.** {topic}\n\n{body}"),
            kind="neutral",
        )

    xref = types.SimpleNamespace(callback=_xref_callback, forward=_xref_forward)

    return mo, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 04: Reading an AI paper critically

        ## The appraisal question

        A published clinical AI paper presents a model with stated performance, a recommended use case, and (sometimes) a vendor or institution behind it. The clinical informaticist's job is to decide whether the model can be trusted at this institution, on these patients, in this workflow.

        The decision rests on five dimensions of the paper. Each is addressed below with the question to ask, the data the paper should provide, and the failure pattern that indicates the dimension was not handled well. The five dimensions are the practical core of the TRIPOD-AI reporting guideline and the PROBAST risk-of-bias tool; reading either one in full is the deeper version of this track.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The five dimensions, in one table
        """
    )
    return


@app.cell
def _(pd):
    framework_table = pd.DataFrame(
        [
            {
                "Dimension": "1. Training population",
                "Question to ask": "Who, where, and when?",
                "What the paper should say": "Cohort source (single center, multi-center, registry), enrollment dates, inclusion and exclusion criteria, demographics, outcome prevalence.",
                "Common failure": "A single-academic-center cohort from 5+ years ago presented as a general model for current US practice.",
            },
            {
                "Dimension": "2. Outcome definition",
                "Question to ask": "What is the label, and how was it adjudicated?",
                "What the paper should say": "The precise operationalization (ICD-10 codes, lab thresholds, clinician adjudication, structured registry entry), the time window, the proxy used if the true outcome is unobservable.",
                "Common failure": "An outcome defined by a billing code that captures the wrong thing (the Obermeyer 2019 case used healthcare cost as a proxy for healthcare need, which embedded a race bias).",
            },
            {
                "Dimension": "3. Validation approach",
                "Question to ask": "Was the model evaluated on data it had not seen?",
                "What the paper should say": "Train / validation / test split or cross-validation, with the splitting unit (patient, not row). For high-stakes models, an external validation on a different center, time period, or population.",
                "Common failure": "Internal validation only (the test set comes from the same hospital, year, and patient population as the training set). Performance drops 10 to 30 AUC points on external validation, but no external validation was reported.",
            },
            {
                "Dimension": "4. Calibration reporting",
                "Question to ask": "Did the paper report calibration, or only discrimination?",
                "What the paper should say": "A calibration plot and the Brier score, calibration intercept and slope, or at minimum the mean predicted probability against the observed event rate (calibration-in-the-large).",
                "Common failure": "AUC is reported, calibration is not. Most clinical AI papers historically fall into this pattern; the omission means the model's stated probabilities cannot be acted on.",
            },
            {
                "Dimension": "5. Subgroup performance",
                "Question to ask": "How does the model perform within race, sex, age, and other relevant subgroups?",
                "What the paper should say": "AUC and calibration reported separately within each subgroup of interest, with sample sizes per subgroup.",
                "Common failure": "Overall AUC reported, no subgroup breakdown. A model with overall AUC 0.85 can have AUC 0.65 in the smallest subgroup; the gap is invisible from the overall number.",
            },
        ]
    )
    framework_table.index = range(1, len(framework_table) + 1)
    framework_table.index.name = "row"
    framework_table
    return (framework_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three properties of the framework are load-bearing.

        First, the dimensions are not interchangeable. A paper that handles the training population perfectly but does not report calibration is missing a load-bearing piece. The five together are the appraisal; any one missing is a reason to defer adoption until the gap is filled.

        Second, each dimension has a question the paper either answers or does not. The reviewer's job is to extract the answer if it is there and to flag the omission if it is not. Many published papers do not address every dimension; that is the appraisal output, not a defect of the framework.

        Third, the framework is necessary but not sufficient for adoption. A paper that passes every dimension can still be a poor fit for the local institution (different case-mix, different EHR vocabulary, different workflow). The framework filters out the papers that are not worth deploying anywhere; it does not certify the papers that pass for any specific deployment.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A worked appraisal: the "ICU mortality predictor"

        A hypothetical paper presents an ICU mortality prediction model with the following abstract (representative of common patterns in the published clinical AI literature):

        > **Background.** ICU mortality remains difficult to predict from admission features alone. We developed a deep learning model to predict in-hospital mortality from the first 24 hours of ICU data.
        >
        > **Methods.** We trained a recurrent neural network on data from 38,000 ICU admissions at our academic medical center between 2014 and 2019. We split the data 80/20 by admission. The model was trained on the 80% and evaluated on the 20%.
        >
        > **Results.** The model achieved an AUC of 0.89 (95% CI 0.87 to 0.91) on the held-out test set. The model outperformed the SAPS-II score (AUC 0.78).
        >
        > **Conclusions.** Our deep learning model substantially outperforms a standard ICU severity score and should be considered for clinical implementation.

        The appraisal below applies the five-dimension framework to this abstract.
        """
    )
    return


@app.cell
def _(pd):
    appraisal_table = pd.DataFrame(
        [
            {
                "Dimension": "1. Training population",
                "What the paper says": "38,000 ICU admissions at one academic medical center, 2014 to 2019.",
                "Assessment": "Partial. Inclusion and exclusion criteria are not stated. Demographics not reported in the abstract. Single-center design limits generalizability. The 2014 to 2019 window predates the COVID era and predates several common ICU practice changes.",
            },
            {
                "Dimension": "2. Outcome definition",
                "What the paper says": "In-hospital mortality.",
                "Assessment": "Partial. The outcome label appears clear (binary, observable). The time horizon (in-hospital, not 28-day or 90-day) is specified. The definition of when the prediction window opens and closes is not stated; this matters because a model trained on the first 24 hours can leak information from interventions (intubation, vasopressor start) that are themselves correlated with death.",
            },
            {
                "Dimension": "3. Validation approach",
                "What the paper says": "80/20 split by admission. No external validation.",
                "Assessment": "Insufficient. The 80/20 split is on admissions, not patients, so the same patient could appear in both training and test sets (a frequent ICU patient leaks across the split). No external validation against a different center is reported. The 0.89 AUC is the internal-validation number and is likely to drop 5 to 15 points on external data.",
            },
            {
                "Dimension": "4. Calibration reporting",
                "What the paper says": "Nothing about calibration.",
                "Assessment": "Failed. The abstract reports AUC only. There is no Brier score, no calibration plot, no calibration intercept or slope, and no calibration-in-the-large statistic. The model's probabilities cannot be acted on clinically until calibration is documented.",
            },
            {
                "Dimension": "5. Subgroup performance",
                "What the paper says": "Nothing about subgroups.",
                "Assessment": "Failed. The abstract reports overall AUC only. No race, sex, age, or service-line breakdown is reported. The model may perform far below 0.89 in a subgroup of clinical importance (the youngest patients, the post-cardiac-arrest cohort, the oncology service), and the abstract gives no way to tell.",
            },
        ]
    )
    appraisal_table.index = range(1, len(appraisal_table) + 1)
    appraisal_table.index.name = "row"
    appraisal_table
    return (appraisal_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The appraisal verdict

        The paper as abstracted earns a partial pass on the first two dimensions, an insufficient mark on the third, and a failure on the fourth and fifth. The recommended next step is not adoption. The recommended next steps are, in order: ask the authors for the calibration plot and the subgroup AUCs (both are usually available and were simply omitted from publication), ask for external validation if the institution considering adoption is not the institution that trained the model, and ask for a documented validation against the local case-mix before any clinical deployment.

        A model with AUC 0.89 from a single-center 2014 to 2019 cohort, with no calibration and no subgroup breakdown, is not ready for clinical deployment. The AUC number does not by itself answer the appraisal question.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Interactive checklist

        Use the checklist below when reading a clinical AI paper. Each checkbox represents one of the five dimensions, in operational form. The summary panel at the bottom updates as boxes are checked and reports the number of dimensions the paper handled adequately.
        """
    )
    return


@app.cell
def _(mo):
    chk_pop = mo.ui.checkbox(value=False, label="Training population is specified (source, dates, inclusion/exclusion, demographics, outcome prevalence)")
    chk_outcome = mo.ui.checkbox(value=False, label="Outcome label is precisely operationalized (codes, thresholds, adjudication, time window)")
    chk_val_split = mo.ui.checkbox(value=False, label="Train / validation / test split is by patient (not by row) and the unit is specified")
    chk_external = mo.ui.checkbox(value=False, label="External validation is reported (different center, time period, or population from training)")
    chk_calib = mo.ui.checkbox(value=False, label="Calibration is reported (calibration plot, Brier score, or calibration-in-the-large)")
    chk_subgroup = mo.ui.checkbox(value=False, label="Subgroup AUC and calibration are reported (race, sex, age, and other relevant strata)")
    mo.vstack([
        mo.md("**Check the boxes the paper actually satisfies.**"),
        chk_pop,
        chk_outcome,
        chk_val_split,
        chk_external,
        chk_calib,
        chk_subgroup,
    ])
    return (
        chk_calib,
        chk_external,
        chk_outcome,
        chk_pop,
        chk_subgroup,
        chk_val_split,
    )


@app.cell
def _(
    chk_calib,
    chk_external,
    chk_outcome,
    chk_pop,
    chk_subgroup,
    chk_val_split,
    mo,
):
    items = [
        ("Training population", chk_pop.value),
        ("Outcome definition", chk_outcome.value),
        ("Validation split unit", chk_val_split.value),
        ("External validation", chk_external.value),
        ("Calibration", chk_calib.value),
        ("Subgroup performance", chk_subgroup.value),
    ]
    n_checked = sum(1 for _, v in items if v)
    n_total = len(items)
    missing = [name for name, v in items if not v]
    if n_checked == n_total:
        verdict_kind = "success"
        verdict_text = "All six items satisfied. The paper meets the appraisal framework. The next step is to verify the model fits the local case-mix and workflow before deployment."
    elif n_checked >= 4:
        verdict_kind = "info"
        verdict_text = f"{n_checked} of {n_total} items satisfied. Ask the authors (or the vendor) for the missing items before adoption: {', '.join(missing)}."
    elif n_checked >= 2:
        verdict_kind = "warn"
        verdict_text = f"Only {n_checked} of {n_total} items satisfied. The paper is not ready for adoption. Missing items: {', '.join(missing)}."
    else:
        verdict_kind = "danger"
        verdict_text = f"Only {n_checked} of {n_total} items satisfied. Defer adoption and treat the published number as preliminary. Missing items: {', '.join(missing)}."
    verdict = mo.callout(mo.md(f"**Checklist score: {n_checked} / {n_total}.** {verdict_text}"), kind=verdict_kind)
    verdict
    return items, missing, n_checked, n_total, verdict, verdict_kind, verdict_text


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A note on what the framework does not do

        The five-dimension framework is necessary but not sufficient for adoption. A paper that scores 6 of 6 on the checklist can still be a poor fit for the local institution. The local appraisal questions extend the published-paper appraisal in three directions.

        - **Local case-mix.** Does the institution adopting the model have a patient population sufficiently similar to the training population? A model trained on a tertiary academic center will not transfer to a community hospital without re-validation.
        - **Local data availability.** Are the features the model requires available in the local EHR, in the right vocabulary, with similar measurement timing? A model that requires a structured "code-status" field will fail at an institution that records code status in free-text notes.
        - **Local workflow.** Does the proposed alert moment, action, and user fit the existing workflow? The appraisal framework does not address this; Course 12 (CDS) takes it up explicitly.

        The published appraisal is the filter that determines whether to invest further effort in local validation. The local validation is the additional work the appraisal does not replace.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "09",
        "03",
        "Outcome-definition bias and the proxy problem",
        "Course 03 introduced the bias question. Dimension 2 of this framework (outcome definition) is where most label-choice bias enters; the Obermeyer 2019 paper documented the most-cited clinical case (healthcare cost as a proxy for healthcare need encoded a race bias that the algorithm then operationalized).",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "09",
        "13",
        "TRIPOD-AI as a reporting standard",
        "Course 13 (Research reproducibility) takes up the broader reporting-standards landscape. TRIPOD-AI is the AI-specific extension of the TRIPOD checklist for prediction-model studies; it operationalizes the five-dimension framework at the level a journal reviewer or a regulatory submission would require.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        Five dimensions determine whether a published clinical AI paper can be acted on: the training population, the outcome definition, the validation approach, the calibration reporting, and the subgroup performance. Each has a question to ask and a published-pattern failure mode to recognize. The worked appraisal of the "ICU mortality predictor" abstract showed how the framework rules out a model that reports only AUC, only internal validation, and no subgroup breakdown. The interactive checklist makes the framework reusable for any new paper.

        Track 05 takes up the related question of bias, fairness, and clinical risk. The subgroup-performance dimension of the framework is where bias becomes visible; Track 05 addresses where bias enters the pipeline upstream and what to do about it.
        """
    )
    return


if __name__ == "__main__":
    app.run()
