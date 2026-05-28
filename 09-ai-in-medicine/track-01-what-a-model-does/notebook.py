"""Track 01: What a model actually does.

A clinical AI model is a function: inputs in (patient features), output out
(a score, a probability, or a class label). The track defines the function,
separates training from prediction, and presents a small readmission scoring
example with reactive sliders so the reader can move each input feature and
see the score respond. No math is required; the goal is to make the function
visible.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import math
    import types

    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd

    _COURSE_TITLES = {
        "01": "Computational thinking",
        "04": "Clinical epidemiology",
        "12": "Clinical decision support",
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

    return alt, math, mo, np, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 01: What a model actually does

        ## A clinical model is a function

        A clinical AI model is a function. Inputs go in (patient features), one output comes out (a score, a probability, or a class label). The function has the same form for the simplest hand-built rule and for the largest deep neural network. What changes between models is the complexity of the function and the size of the dataset used to fit its parameters.

        The track defines the function, separates training from prediction, and presents a small readmission scoring example with reactive sliders so the reader can move each input feature and see the score respond. No math is required; the goal is to make the function visible.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Inputs, the function, the output

        A clinical AI model is shaped like this:

        ```
        inputs:    patient features (age, lab values, prior admissions, ...)
                                |
                                v
        function:  a fixed mathematical mapping with adjustable parameters
                                |
                                v
        output:    a single score, probability, or class label
        ```

        The function is fixed in form before any data is seen. The parameters of the function are adjusted during training so that the function's output on the training inputs is close to the known training labels. Once training is finished, the function is frozen and used to score new patients.

        Three properties of this picture are load-bearing.

        First, the function takes a fixed set of inputs. A model trained to take age, prior admissions, and days since discharge will not accept a fourth feature (like serum sodium) without retraining. The inputs are part of the model's contract.

        Second, the function produces one output per inference. The shape of the output is fixed in advance (a single probability, a vector of class probabilities, a scalar score). A model trained to predict 30-day readmission cannot also predict 1-year mortality without a separate model.

        Third, the parameters are adjusted by an automated training procedure, not chosen by a human. A clinician writing a hand-built rule (if `HR > 100 and temp > 38.5` then alert) sets the thresholds personally. A trained model has parameters chosen by an optimization algorithm against a labeled dataset; nobody picked the specific numbers.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A worked example: a small readmission scoring function

        The function below is a hand-set linear scoring rule for 30-day hospital readmission. It takes three inputs (the patient's age, their number of prior admissions in the last 12 months, and the days since their most recent discharge) and produces a single probability between 0 and 1.

        The function has four parameters (an intercept and one weight per input feature). The parameter values shown below are the result that a training procedure would produce on a representative readmission dataset; they were chosen here by hand for illustration.
        """
    )
    return


@app.cell
def _(mo, pd):
    parameters_table = pd.DataFrame(
        [
            {"Parameter": "Intercept", "Value": -2.40, "Meaning": "Baseline log-odds of readmission for a hypothetical reference patient"},
            {"Parameter": "Weight on age", "Value": 0.025, "Meaning": "Log-odds change per additional year of age"},
            {"Parameter": "Weight on prior admissions", "Value": 0.55, "Meaning": "Log-odds change per additional prior admission in the last 12 months"},
            {"Parameter": "Weight on recent discharge", "Value": 1.30, "Meaning": "Log-odds added when the patient was discharged within the last 7 days"},
        ]
    )
    parameters_table.index = range(1, len(parameters_table) + 1)
    parameters_table.index.name = "row"
    parameters_table
    return (parameters_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        The function combines the inputs with the parameters as a weighted sum (the linear part), then squashes the sum into a probability between 0 and 1 (the sigmoid part). The sigmoid is a fixed function that has no parameters; it just maps any real number to a probability.

        Move the sliders below to set a patient's three features. The function produces a readmission probability that updates instantly. Each component of the calculation is shown so the function is visible at every step.
        """
    )
    return


@app.cell
def _(mo):
    age_slider = mo.ui.slider(start=18, stop=95, step=1, value=58, label="Age (years)", show_value=True)
    prior_slider = mo.ui.slider(start=0, stop=6, step=1, value=1, label="Prior admissions in last 12 months", show_value=True)
    days_slider = mo.ui.slider(start=0, stop=30, step=1, value=10, label="Days since most recent discharge", show_value=True)
    mo.vstack([age_slider, prior_slider, days_slider])
    return age_slider, days_slider, prior_slider


@app.cell
def _(age_slider, days_slider, math, mo, prior_slider):
    age_val = age_slider.value
    prior_val = prior_slider.value
    days_val = days_slider.value

    recent_indicator = 1 if days_val <= 7 else 0

    intercept = -2.40
    w_age = 0.025
    w_prior = 0.55
    w_recent = 1.30

    age_contrib = w_age * age_val
    prior_contrib = w_prior * prior_val
    recent_contrib = w_recent * recent_indicator

    logit = intercept + age_contrib + prior_contrib + recent_contrib
    probability = 1 / (1 + math.exp(-logit))

    calc_summary = mo.md(
        f"""
        **The function applied to this patient:**

        - Age contribution: `0.025 * {age_val}` = {age_contrib:+.3f}
        - Prior-admissions contribution: `0.55 * {prior_val}` = {prior_contrib:+.3f}
        - Recent-discharge indicator (1 if days <= 7, else 0): `1.30 * {recent_indicator}` = {recent_contrib:+.3f}
        - Intercept: {intercept:+.3f}
        - **Sum (logit)**: {logit:+.3f}
        - **Sigmoid(logit) = predicted probability**: **{probability:.3f}** (= {probability * 100:.1f}%)
        """
    )
    calc_summary
    return (
        age_contrib,
        age_val,
        calc_summary,
        days_val,
        intercept,
        logit,
        prior_contrib,
        prior_val,
        probability,
        recent_contrib,
        recent_indicator,
        w_age,
        w_prior,
        w_recent,
    )


@app.cell
def _(mo, probability):
    if probability < 0.10:
        risk_label = "Low"
        kind = "success"
    elif probability < 0.25:
        risk_label = "Moderate"
        kind = "info"
    else:
        risk_label = "High"
        kind = "warn"
    interp = mo.callout(
        mo.md(f"**Risk label at the chosen threshold:** {risk_label} (probability {probability:.2f}). The threshold for the label is a separate decision from the function output; Track 03 takes it up explicitly."),
        kind=kind,
    )
    interp
    return interp, kind, risk_label


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What just happened, and what it generalizes to

        The function above has four parameters and three inputs. A large neural-network classifier has tens of millions of parameters and hundreds or thousands of inputs. The picture is the same: inputs combine with parameters, the result is squashed into a probability, the probability is the model's prediction.

        Three observations follow.

        First, a model that has not been trained is a function whose parameter values are arbitrary. A model that has been trained is a function whose parameter values have been chosen by an optimization procedure against a labeled dataset. The mathematical form is the same in both cases; what training produces is the specific numbers.

        Second, the model's contract is the inputs and the output. A model trained to take three features cannot accept a fourth without retraining. A model trained to produce a probability cannot be reinterpreted as producing a class label without an explicit threshold choice. Each input the model accepts and each output it produces are decisions baked into the model when training started.

        Third, the model's confidence in its output is a property of the function and the training data, not of the patient. A model can produce a probability of 0.92 with absolute confidence about a patient who is unlike any patient in the training set; the probability is a number the function produced, not a statement about reality. Track 04 takes up the appraisal questions a clinician should ask before trusting a model output.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What training is, in one paragraph

        Training is the procedure that picks the parameter values. The input to training is a labeled dataset (many patients, each with their feature values and the known outcome). The procedure adjusts the parameters one small step at a time so that the function's prediction on each training patient gets closer to that patient's known outcome. After many passes through the dataset, the parameters reach a configuration in which the function's predictions are, on average, close to the known outcomes.

        Three things to notice about training. First, training never produces a function that is correct on every patient; it produces a function that is on average close on the patients in the training set. Second, training produces a different function each time it is run on a different dataset; the same model architecture trained on two cohorts will have two sets of parameter values. Third, training depends on the choice of loss function (the precise measure of "close to the known outcome"); the loss function is a modeling choice with consequences, not a neutral default.

        Track 02 takes up the central failure mode of training: a function that has parameter values that fit the training set extremely well and fit any patient outside the training set very poorly. The failure mode has a name (overfitting) and a standard set of mitigations.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Demystifying the labels

        Two pieces of vocabulary often produce more confusion than clarity in clinical conversations about AI.

        **"The model learned X."** A model does not learn in the cognitive sense. The training procedure adjusts numerical parameters so the function's output is closer to the known labels. The procedure has no representation of why a feature is associated with the outcome and no representation of cause. A more precise phrasing: "the model's parameters were adjusted so that feature X is weighted positively in the prediction."

        **"The model is intelligent."** A trained model is a function whose parameters were picked by an optimization procedure. The function applies the same arithmetic to every input regardless of whether the input resembles anything in the training set. Intelligence is not the right vocabulary for what the function does. A more precise phrasing: "the function produces an output that, on patients similar to the training set, tends to be close to the true outcome."

        The same is true of the word "predict." A model's output is the value of a fixed function applied to inputs; the value happens to be informative about the outcome when the patient is similar to the training set. The output is not a forecast in the meteorological sense and is not a guarantee of any kind.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "09",
        "01",
        "Decomposing a clinical decision rule",
        "Course 01 Track 1 introduced the picture of a clinical rule as a function of inputs to an output. The model in this track is the same picture, with the parameters of the function adjusted by an automated training procedure rather than picked by a clinician.",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "09",
        "12",
        "When the model becomes a CDS alert",
        "Course 12 takes up the case in which a trained model is wired into the EHR as a clinical decision support alert. The model output (the probability) and the alert threshold (the decision to fire) are separated. The five rights of CDS govern the alert, not the model.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        A clinical AI model is a function. Inputs in, parameters apply, output out. The form of the function is fixed before training; the parameter values are picked by an automated training procedure against a labeled dataset. Once training is finished, the function is frozen and used to score new patients.

        Track 02 takes up the central failure mode of training: overfitting. Track 03 takes up the two model-quality questions (discrimination and calibration) that determine whether a trained model's outputs can be acted on clinically.
        """
    )
    return


if __name__ == "__main__":
    app.run()
