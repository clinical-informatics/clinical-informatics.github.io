"""Track 02: Training, validation, and overfitting.

A model that is evaluated on the same data it was trained on always looks
excellent because the model has memorized the data. The track defines the
train / validation / test split, demonstrates overfitting by plotting
training error and test error against model complexity (training error
goes to zero, test error climbs), defines generalization, and introduces
k-fold cross-validation.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import types

    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd

    _COURSE_TITLES = {
        "01": "Computational thinking",
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

    return alt, mo, np, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 02: Training, validation, and overfitting

        ## Why training error is a misleading number

        A trained model whose performance is measured on the same dataset that was used to train it always looks excellent. The training procedure adjusted the model's parameters to fit those specific examples; reporting the model's error on those same examples reports how successful the fit was, not how well the model generalizes.

        The track addresses the failure mode that follows from this observation. A model that is complex enough can fit any training set to arbitrarily low error and predict no new patient correctly. The remedy is to evaluate the model on patients it has not seen during training. The mechanism is the train / validation / test split, and the failure that motivates it is called overfitting.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The three-way split

        A clinical AI dataset is partitioned before training begins into three disjoint subsets.

        - **Training set.** The data the training procedure sees. The model's parameters are adjusted to fit these examples.
        - **Validation set.** Data held out from training. Used to compare candidate models, tune hyperparameters (model complexity, regularization strength, learning rate), and decide when to stop training.
        - **Test set.** Data held out from both training and validation. Used exactly once, after the final model has been chosen, to estimate how the model will perform on future patients.

        The three sets are disjoint by patient (not by row), so a patient who appears in the training set never appears in the validation or test set. A typical split is 70 / 15 / 15 by patient, with each subset stratified by the outcome so the prevalence is similar in all three.

        Two consequences are load-bearing.

        First, the test set is held in reserve. Looking at the test set during training or model selection contaminates the test estimate; the test performance no longer reflects how the model will do on truly new patients. The discipline of touching the test set exactly once is sometimes called "test-set hygiene" and is the single most violated rule in published clinical ML.

        Second, the validation set is used as many times as the modeler wants, but each use leaks a small amount of information from the validation set into the modeling decisions. After many tuning passes, the validation set acts more like a training set; the test set is the only honest estimate of out-of-sample performance.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Demonstrating overfitting: polynomial fits on a noisy series

        The simplest demonstration of overfitting uses one-dimensional polynomial regression. The true relationship between x and y is a smooth curve (a quadratic, in this case). The reader has 12 training points sampled from the true curve with noise, and a separate 200-point test set sampled from the same noisy process.

        For each model complexity (the polynomial degree, from 1 to 11), the training procedure picks the polynomial coefficients that minimize the squared error on the training set. The chart on the left shows the fitted curve on top of the training points. The chart on the right shows the training MSE and the test MSE as a function of polynomial degree. The two errors move in different directions as the degree grows.
        """
    )
    return


@app.cell
def _(np):
    rng = np.random.default_rng(seed=20260528)

    def true_function(x):
        return 0.6 + 0.4 * x - 0.15 * x ** 2

    n_train = 12
    n_test = 200
    train_x = np.linspace(-3, 3, n_train)
    train_y = true_function(train_x) + rng.normal(0, 0.5, n_train)
    test_x = rng.uniform(-3, 3, n_test)
    test_y = true_function(test_x) + rng.normal(0, 0.5, n_test)
    return n_test, n_train, rng, test_x, test_y, train_x, train_y, true_function


@app.cell
def _(mo):
    degree_slider = mo.ui.slider(start=1, stop=11, step=1, value=2, label="Polynomial degree (model complexity)", show_value=True)
    degree_slider
    return (degree_slider,)


@app.cell
def _(alt, degree_slider, np, pd, test_x, test_y, train_x, train_y, true_function):
    degree = degree_slider.value
    coeffs = np.polyfit(train_x, train_y, deg=degree)

    fit_pred_train = np.polyval(coeffs, train_x)
    fit_pred_test = np.polyval(coeffs, test_x)
    train_mse = float(np.mean((fit_pred_train - train_y) ** 2))
    test_mse = float(np.mean((fit_pred_test - test_y) ** 2))

    grid_x = np.linspace(-3.5, 3.5, 200)
    grid_y_fit = np.polyval(coeffs, grid_x)
    grid_y_true = true_function(grid_x)

    train_df = pd.DataFrame({"x": train_x, "y": train_y, "kind": "training point"})
    truth_df = pd.DataFrame({"x": grid_x, "y": grid_y_true, "kind": "true function"})
    fit_df = pd.DataFrame({"x": grid_x, "y": grid_y_fit, "kind": f"degree-{degree} fit"})

    fit_chart = (
        alt.Chart(truth_df).mark_line(color="#2ca02c", strokeDash=[4, 2]).encode(
            x=alt.X("x:Q", scale=alt.Scale(domain=[-3.5, 3.5])),
            y=alt.Y("y:Q", scale=alt.Scale(domain=[-3, 3])),
        )
        + alt.Chart(fit_df).mark_line(color="#d62728", strokeWidth=2).encode(
            x="x:Q",
            y="y:Q",
        )
        + alt.Chart(train_df).mark_circle(size=140, color="#1f77b4", opacity=0.9).encode(
            x="x:Q", y="y:Q",
        )
    ).properties(
        width=320, height=300, title=f"Degree-{degree} fit (red) over 12 training points (blue) and the true function (green dashed)"
    )

    err_summary = pd.DataFrame(
        [
            {"Quantity": "Training MSE", "Value": train_mse},
            {"Quantity": "Test MSE", "Value": test_mse},
            {"Quantity": "Test - Training (generalization gap)", "Value": test_mse - train_mse},
        ]
    )
    err_summary["Value"] = err_summary["Value"].round(3)
    err_summary.index = range(1, len(err_summary) + 1)
    return (
        coeffs,
        degree,
        err_summary,
        fit_chart,
        fit_df,
        fit_pred_test,
        fit_pred_train,
        grid_x,
        grid_y_fit,
        grid_y_true,
        test_mse,
        train_df,
        train_mse,
        truth_df,
    )


@app.cell
def _(fit_chart):
    fit_chart
    return


@app.cell
def _(err_summary):
    err_summary
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Move the slider above. Three patterns to verify by inspection.

        At degree 1, the model is too simple to capture the curve and both training and test error are high. The model underfits.

        At degree 2, the model matches the true function shape and both errors are low. The generalization gap (test minus training) is small.

        At degree 9, 10, or 11, the red curve passes through (or nearly through) every training point. Training error is near zero. Test error is much larger than the degree-2 case. The model is fitting the noise in the training set as if it were signal.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The training-vs-test curve, all degrees at once

        The chart below shows the training MSE and the test MSE plotted against polynomial degree from 1 to 11. The two curves cross the standard overfitting picture: training error decreases monotonically, test error has a U-shape (down to the optimum, then up).
        """
    )
    return


@app.cell
def _(alt, np, pd, test_x, test_y, train_x, train_y):
    sweep_rows = []
    for d in range(1, 12):
        c = np.polyfit(train_x, train_y, deg=d)
        tr_mse = float(np.mean((np.polyval(c, train_x) - train_y) ** 2))
        te_mse = float(np.mean((np.polyval(c, test_x) - test_y) ** 2))
        sweep_rows.append({"degree": d, "kind": "Training MSE", "MSE": tr_mse})
        sweep_rows.append({"degree": d, "kind": "Test MSE", "MSE": te_mse})
    sweep_df = pd.DataFrame(sweep_rows)

    sweep_chart = (
        alt.Chart(sweep_df)
        .mark_line(point=True)
        .encode(
            x=alt.X("degree:Q", title="Polynomial degree"),
            y=alt.Y("MSE:Q", title="Mean squared error", scale=alt.Scale(type="log")),
            color=alt.Color("kind:N", title=""),
            tooltip=["degree:Q", "kind:N", "MSE:Q"],
        )
        .properties(width=560, height=280, title="Training MSE vs Test MSE across polynomial degree (log-scale y)")
    )
    sweep_chart
    return d, sweep_chart, sweep_df, sweep_rows


@app.cell
def _(mo):
    mo.md(
        r"""
        The optimal degree (where the test curve bottoms out) is the right model complexity for this dataset. Picking the optimum requires the test curve, which requires a held-out test set. A modeler who only computes the training MSE would pick the highest-degree model (because training MSE always decreases with complexity) and ship a model that fits the noise.

        Generalization is the property that the test MSE is close to the training MSE. Overfitting is the failure of generalization; underfitting is the related failure in which both errors are high because the model is too simple to capture the signal at all.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Cross-validation: the workaround when the dataset is small

        The three-way split assumes the dataset is large enough that 15% of it (the validation set) is still a useful sample, and so is the 15% test set. A clinical AI dataset is often too small for this; a 200-patient cohort split into 140 / 30 / 30 has a 30-patient test set whose performance estimate has a wide confidence interval.

        K-fold cross-validation is the standard workaround. The data is split into k disjoint folds (typically 5 or 10). The model is trained on k-1 folds and evaluated on the held-out fold. The procedure is repeated k times so each fold is held out exactly once. The k held-out performance estimates are averaged to produce the cross-validated estimate.

        Cross-validation does not eliminate the need for a separate test set; it replaces the validation set. The pattern in clinical AI is then: training + cross-validation for model selection, test set used once at the end for the final performance estimate.

        Two cross-validation variants are worth knowing.

        - **Stratified k-fold** preserves the outcome prevalence in each fold. Required for any classification task with class imbalance (most clinical outcomes).
        - **Grouped k-fold** keeps all rows from a given patient in the same fold. Required when the dataset has multiple rows per patient (longitudinal labs, multiple encounters) so the model does not see the same patient in both training and validation.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What overfitting looks like in clinical AI

        The polynomial example is one-dimensional and visually obvious. Overfitting in a clinical AI model usually looks different on the surface.

        - A neural network with millions of parameters trained on a single-center 10,000-patient cohort can achieve internal-validation AUC of 0.95 and external-validation AUC of 0.70 on a different center's cohort.
        - A gradient-boosted classifier trained on EHR data can pick up on hospital-specific operational signals (the time of day a lab is drawn, the structure of the order set used) that are invisible at face value but explain most of the predictive performance and disappear at deployment.
        - A model whose feature set includes a variable computed after the outcome (the "label leakage" failure) can achieve near-perfect training and validation performance and deploy at random-chance performance.

        Each of these failures has the same root cause: the model's predictions reflect features of the training environment that do not transfer. The remedy is honest external validation: held-out data from a different center, a different time period, or a different population from the training cohort.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "09",
        "04",
        "Selection bias and overfitting are the same shape of problem",
        "Course 04 Track 2 introduced selection bias: when the analysis sample is not representative of the population the inference is meant to generalize to. Overfitting is the model-specific case: the model's parameters were chosen against a sample, and the model's performance reflects features of the sample that do not generalize to the population the model will be deployed against.",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "09",
        "13",
        "Test-set hygiene as a reproducibility problem",
        "Course 13 takes up the broader reproducibility framework. The test-set-hygiene rule (touch the test set exactly once) is a special case of the general rule that the data-analysis pipeline must be specified before the data is examined. The TRIPOD-AI checklist and PROBAST tool reference the same discipline at the model-reporting level.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        Training error is a misleading number because the training procedure was designed to minimize it. The honest model-quality estimate comes from a test set held out from training and used exactly once. The train / validation / test split operationalizes this for large datasets; k-fold cross-validation does the same job for small datasets. Overfitting is the failure mode in which a model with too many parameters fits the noise in the training set, achieves near-zero training error, and produces poor predictions on new patients. The remedy in every case is honest external validation.

        Track 03 takes up the two questions a held-out test set is used to answer: discrimination (does the model rank patients correctly?) and calibration (does the model produce probabilities that match observed outcomes?).
        """
    )
    return


if __name__ == "__main__":
    app.run()
