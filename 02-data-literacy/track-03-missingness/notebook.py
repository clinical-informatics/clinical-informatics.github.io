"""Track 03: Null values and missingness.

A blank cell is a question. This notebook is about answering it. Five
pieces: what a null actually is across systems, the four clinical causes
of missingness, MCAR/MAR/MNAR with concrete examples and a slider that
shows the bias each one produces, the imputation menu (mean, LOCF,
regression, MICE, missing-as-indicator) applied to the same biased data
to see which methods recover the truth, and a drop-or-keep decision
framework for columns and rows.
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
        # Track 03: Null values and missingness

        ## A blank cell is a question

        Read a CSV in. Compute the mean of CRP. Plausible number. Slide deck. Done.

        Now back up. Six rows had no CRP. Why? Nobody asked. The number you reported is the mean of the *non-missing* CRPs, which is the same as the mean of the cohort's CRPs only when the missing patients look like the non-missing patients. They almost never do.

        This track is about the question. Five pieces:

        1. **What a null actually is**, across pandas, SQL, FHIR, and the CSV your CDW gave you.
        2. **The four clinical causes** of missing data.
        3. **MCAR, MAR, MNAR**: three kinds of missingness, with concrete clinical examples, watched on a slider.
        4. **Imputation**: the menu of options (mean, LOCF, regression, multiple imputation, missing-as-indicator) and what each one assumes.
        5. **Drop or keep**: when to drop a row, when to drop a column, when to keep missingness as its own variable.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1. What a null actually is

        A **null** is the placeholder a system uses to mean "no value here." That's the definition. The complication is that every system you touch uses a slightly different placeholder.

        | System | What "missing" looks like | Special behavior to know about |
        |---|---|---|
        | **SQL** | `NULL` | `NULL = NULL` evaluates to `NULL`, not `true`. Use `IS NULL`, never `= NULL`. Three-valued logic: true, false, null. Joins and filters silently drop null rows unless you handle them. |
        | **pandas numeric** | `NaN` (numpy) | `NaN != NaN` is `True`. Use `pd.isna(x)`. Aggregations skip NaN by default. |
        | **pandas datetime** | `NaT` | Same idea, datetime flavor. |
        | **pandas object** | `None` | The Python null. Sometimes coexists with `NaN` in the same column; `pd.isna()` catches both. |
        | **FHIR** | Field absent, OR `dataAbsentReason` extension | The extension lets the sender say *why* it's missing: `unknown`, `asked-but-unknown`, `temp-unknown`, `not-asked`, `masked`, `unsupported`, `as-text`, `error`, `not-a-number`. Nine reasons, all different. |
        | **Your CDW export** | Whatever the exporter wrote | `""`, `NA`, `N/A`, `NULL`, `None`, `nan`, `Unknown`, `.`, `9999`, `999`, `-1`, `--`, sometimes a single space `" "`. |

        **The first cleaning move on any inherited dataset** is to convert every "missing-like" string to a proper null:

        ```python
        df = pd.read_csv(path, na_values=["NA", "NULL", "None", "Unknown", ".", "9999", ""])
        ```

        After this, your tool's null is the only kind of null you have to reason about.
        """
    )
    return


@app.cell
def _(mo, pd):
    null_demo = pd.DataFrame(
        {
            "specimen_date": ["2024-04-17", "2024-07-22", "2024-10-30", "2025-02-04", "2025-05-12"],
            "crp_as_received": ["18.7", "NA", "11.4", "<2.0", "Unknown"],
            "crp_after_na_values": [18.7, None, 11.4, "<2.0", None],
        }
    )
    null_demo.index = range(1, len(null_demo) + 1)
    null_demo.index.name = "row"
    mo.vstack(
        [
            mo.md(
                "**Worked example.** Same five CRP cells, raw export vs. after `na_values=['NA','Unknown']`. "
                "Rows 2 and 5 are now proper nulls. Row 4 (`<2.0`) is still text because it's a sentinel value, not a missing-marker. That distinction (Track 01) lands here too: the sentinel encodes that the value was *below the assay's limit*, not that the value is unknown. Two different things, both worth handling on purpose."
            ),
            mo.ui.table(null_demo, selection=None),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2. The four clinical causes of missing data

        Before the statistical framework, the practical one. A missing cell in a clinical extract comes from one of four causes (often in combination):

        | # | Cause | What happened | Informative? |
        |---|---|---|---|
        | 1 | **Not ordered** | The rheumatologist didn't repeat anti-CCP because the 2022 result was already positive. | Yes. The absence tells you the prior was trusted. |
        | 2 | **Ordered, not done** | Lab was ordered, patient left before draw, specimen hemolyzed, tech missed it. | No. The absence is unrelated to what the value would have been. |
        | 3 | **Done but not exported** | The value resulted in the EHR, but the cohort-export script's join didn't match. | No. Pipeline bug, not clinical missingness. |
        | 4 | **Below limit of quantification** | The analyzer reports "below 2.0" and the export drops the row (or stores it as text). | Yes. The absence is the value being low. |

        These four causes look identical in the data. The cell is empty. The framework in Section 3 is how you tell them apart for inferential purposes.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3. MCAR, MAR, MNAR

        Donald Rubin's 1976 framework. Three categories. Each one with a definition, a clinical example, and what happens to a complete-case analysis under it.

        ### MCAR: Missing Completely At Random

        **Definition.** Whether a value is missing has nothing to do with anything: not the value itself, not the other variables you've observed. The missingness mechanism is a coin flip.

        **Clinical example.** Specimen hemolysis. A subset of CBCs are rejected because the sample got handled wrong in transit. There's no clinical signal in which CBCs hemolyze; it's a property of the transport, not the patient. *Approximately* MCAR.

        **Under MCAR.** The patients with missing values are a random sample. Complete-case analysis is unbiased. Multiple imputation works. Mean imputation roughly works (with a variance penalty).

        **Why it's almost never the right assumption clinically.** MCAR requires *no* clinical signal predicts missingness. Sicker patients miss visits. Healthier patients skip follow-up labs. Patients with insurance changes get re-coded mid-study. There's always something.

        ### MAR: Missing At Random

        **Definition.** Whether a value is missing depends on other variables you *did* observe, but not on the missing value itself once you condition on what you observed.

        **Clinical example.** Ms. Reyes hypothetically misses her July CRP because she rescheduled the appointment due to a job change. The "missing" is correlated with employment status (observable in social history) but not with the CRP value she would have had. Conditioning on employment status, the missingness is random. That's MAR.

        **Under MAR.** Complete-case is biased *in general*. The bias can be removed by conditioning on the observed variables. Multiple imputation, inverse probability weighting, and regression imputation all rest on MAR.

        **The most common honest assumption.** Most clinical missingness has structure other variables in your data can describe. MAR is the modal real-world case.

        ### MNAR: Missing Not At Random

        **Definition.** Whether a value is missing depends on the missing value itself. The reason this CRP isn't in the data is the same reason it would have mattered.

        **Clinical examples.**

        - **Below limit of quantification.** A CRP analyzer reports "below 2.0" as missing. The value is missing *because it was very low*. The mean of the non-missing CRPs overstates inflammation.
        - **Patients who stop coming to clinic because they feel well.** Disease-activity scores are missing for patients in remission, who don't see a reason to come back. Mean DAS28 across the cohort, computed on the non-missing values, overstates disease activity.
        - **Adverse-event monitoring.** Patients are less likely to report embarrassing or stigmatized adverse events. The missing reports are not a random subset.

        **Under MNAR.** Complete-case is biased. Imputation that assumes MAR is also biased (it cannot recover information that's missing for a reason tied to the missing value itself). Sensitivity analysis is the honest tool: bound how bad the bias could be under different assumptions.
        """
    )
    return


@app.cell
def _(mo):
    mech_quiz = mo.ui.radio(
        options=[
            "MCAR. The dropout is just patients losing motivation; nothing to do with their disease.",
            "MAR. The dropout depends on observed variables like prior visit count and travel distance.",
            "MNAR. The dropout depends on disease activity itself, which is the variable being measured.",
            "It cannot be classified without more information.",
        ],
        label=(
            "An RA registry collects DAS28 scores every six months. Patients who reach remission "
            "(DAS28 < 2.6) stop coming back at three times the rate of patients with active disease. "
            "The registry reports the mean DAS28 across all visits to track population-level disease "
            "burden. Which missingness mechanism best describes the patients with missing follow-up DAS28?"
        ),
    )
    mech_quiz
    return (mech_quiz,)


@app.cell
def _(mech_quiz, mo):
    if mech_quiz.value is None:
        mech_quiz_feedback = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif mech_quiz.value.startswith("MNAR."):
        mech_quiz_feedback = mo.callout(
            mo.md(
                "**Correct.** The reason the follow-up DAS28 is missing (the patient is in remission) is the same thing "
                "DAS28 is measuring (their disease activity). The missingness depends on the value itself. The reported "
                "mean DAS28 will overstate disease activity, because the patients who would have had the lowest DAS28 "
                "values are systematically the ones who dropped out. No amount of conditioning on observed covariates "
                "(prior visits, distance, age) fixes this, because the relevant variable (their current DAS28) is the "
                "one that's missing."
            ),
            kind="success",
        )
    else:
        mech_quiz_feedback = mo.callout(
            mo.md(
                "**Not quite.** The decisive question for MNAR: *does whether the value is missing depend on the value itself?* "
                "Here, patients in remission (DAS28 < 2.6) are three times more likely to skip follow-up. The missingness depends "
                "on the disease activity score, which is the variable being measured. That's MNAR. The MCAR option requires no "
                "signal at all; the MAR option requires the signal to live in observed variables you can condition on; this case "
                "has the signal in the missing values themselves."
            ),
            kind="warn",
        )
    mech_quiz_feedback
    return (mech_quiz_feedback,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 4. Watching the bias appear

        Below is a synthetic cohort of 200 RA patients with a known true mean CRP. Each patient's CRP value depends on their age (a little) and their underlying disease activity (a lot). We know the truth because we generated the data.

        Now toss some values into the missing bucket under three different mechanisms and watch what happens to the estimate.
        """
    )
    return


@app.cell
def _(np, pd, rng):
    n_patients = 200
    ages = rng.uniform(25, 80, size=n_patients)
    activity = rng.normal(loc=0, scale=1, size=n_patients)
    crp = 18.0 + 0.30 * (ages - 50) + 8.0 * activity + rng.normal(0, 3, size=n_patients)
    crp = np.clip(crp, 0.1, None)

    cohort = pd.DataFrame(
        {
            "patient_id": [f"PT-{i:03d}" for i in range(n_patients)],
            "age": ages,
            "disease_activity": activity,
            "crp": crp,
        }
    )
    true_mean = float(cohort["crp"].mean())
    return cohort, n_patients, true_mean


@app.cell
def _(mo):
    pct_missing = mo.ui.slider(
        start=0,
        stop=60,
        step=5,
        value=30,
        label="Percent of CRP values to drop",
        show_value=True,
    )
    mechanism = mo.ui.radio(
        options=[
            "MCAR (drop random rows)",
            "MAR (drop more often when age is high)",
            "MNAR (drop more often when CRP itself is low)",
        ],
        value="MCAR (drop random rows)",
        label="Missingness mechanism",
    )
    mo.vstack([pct_missing, mechanism])
    return mechanism, pct_missing


@app.cell
def _(alt, cohort, mechanism, mo, np, pct_missing, rng, true_mean):
    frac = pct_missing.value / 100.0
    n = len(cohort)
    target_missing = int(frac * n)

    if mechanism.value.startswith("MCAR"):
        prob_missing = np.full(n, frac)
    elif mechanism.value.startswith("MAR"):
        age_pct = (cohort["age"] - cohort["age"].min()) / (cohort["age"].max() - cohort["age"].min())
        weights = age_pct.values ** 2
        weights = weights / weights.sum() if weights.sum() > 0 else np.full(n, 1 / n)
        prob_missing = weights * target_missing
        prob_missing = np.clip(prob_missing, 0, 1)
    else:
        crp_pct = (cohort["crp"].max() - cohort["crp"]) / (cohort["crp"].max() - cohort["crp"].min())
        weights = crp_pct.values ** 2
        weights = weights / weights.sum() if weights.sum() > 0 else np.full(n, 1 / n)
        prob_missing = weights * target_missing
        prob_missing = np.clip(prob_missing, 0, 1)

    draws = rng.uniform(0, 1, size=n)
    is_missing = draws < prob_missing

    observed_df = cohort.copy()
    observed_df["crp_observed"] = np.where(is_missing, np.nan, observed_df["crp"])
    observed_df["status"] = np.where(is_missing, "missing", "observed")

    observed_mean = float(np.nanmean(observed_df["crp_observed"]))
    bias = observed_mean - true_mean
    n_observed = int((~is_missing).sum())

    plot_df = observed_df[["age", "crp", "status"]].copy()
    chart = (
        alt.Chart(plot_df)
        .mark_circle(size=70, opacity=0.75)
        .encode(
            x=alt.X("age:Q", title="Age (years)", scale=alt.Scale(domain=[20, 85])),
            y=alt.Y("crp:Q", title="True CRP (mg/L)"),
            color=alt.Color(
                "status:N",
                scale=alt.Scale(
                    domain=["observed", "missing"], range=["#2E86AB", "#D1495B"]
                ),
                legend=alt.Legend(title="In the analysis?"),
            ),
        )
        .properties(width=560, height=320, title="Each dot is one patient. Red dots are the ones that 'went missing'.")
    )

    summary_md = mo.md(
        f"""
        **True mean CRP across the full 200-patient cohort:** {true_mean:.2f} mg/L (we know this because we generated the data).

        **Observed mean** (mean of the {n_observed} patients still in the analysis after the missingness was applied): **{observed_mean:.2f} mg/L**.

        **Bias** (observed minus true): **{bias:+.2f} mg/L**.
        """
    )

    mechanism_takeaway = {
        "MCAR (drop random rows)": (
            "**MCAR.** Red dots are scattered evenly across the age range and the CRP range. The observed mean is close to the true mean, give or take sampling noise. "
            "**Complete-case is honest** under MCAR. The cost is only smaller N (wider confidence intervals)."
        ),
        "MAR (drop more often when age is high)": (
            "**MAR.** Red dots cluster on the older patients (high age). Because age is correlated with CRP in this synthetic cohort (older = slightly higher CRP), the observed mean is biased *downward*: the high-CRP elderly patients are the ones we lost. "
            "**Complete-case is biased**, but the bias can be corrected by conditioning on age (multiple imputation, IPW, regression imputation). Critically, age is fully observed, so the correction is possible."
        ),
        "MNAR (drop more often when CRP itself is low)": (
            "**MNAR.** Red dots cluster at the *bottom* of the CRP axis. The patients we lost are the ones with low CRP, exactly the values the analysis needs to know about to get an unbiased mean. "
            "The observed mean is biased *upward*, often substantially. **No imputation method that uses only observed variables can fix this**, because the relevant variable (the missing CRP) is the one whose values are systematically gone. The honest tools are sensitivity analysis and going back for more data."
        ),
    }
    takeaway = mo.callout(mo.md(mechanism_takeaway[mechanism.value]), kind="warn")

    mo.vstack([summary_md, chart, takeaway])
    return is_missing, observed_df, observed_mean


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 5. Imputation: the menu

        Imputation means filling in the missing cells with plausible values, then proceeding with the analysis. Every method has a name, an assumption, and a characteristic failure mode.

        | # | Method | What it does | Assumption | Failure mode |
        |---|---|---|---|---|
        | 1 | **Mean / median** | Fill each missing cell with the column's mean | Roughly MCAR | Reduces variance. Inflates type 1 error. |
        | 2 | **LOCF** | Copy the patient's last observed value forward (longitudinal) | The patient stayed the same | Creates phantom plateaus. FDA has criticized as primary analysis. |
        | 3 | **Regression** | Predict missing value from other variables | MAR | Underestimates uncertainty (no spread in predictions). |
        | 4 | **MICE (multiple imputation)** | Generate many imputed datasets, pool results | MAR | Doesn't fix MNAR. Implementation choices matter. |
        | 5 | **Missing-as-indicator** | Don't impute. Add a `crp_missing` flag column. | Missingness is signal | Loses the value. Works only for models that handle it. |
        | 6 | **Inverse probability weighting** | Reweight the complete cases by 1 / probability of being observed | MAR | Different paradigm; needs a good missingness model. |

        Below: apply each method to the same biased data from above. See which methods recover the truth and which don't.
        """
    )
    return


@app.cell
def _(mo):
    imp_method = mo.ui.radio(
        options=[
            "1. Complete-case (drop the rows)",
            "2. Mean imputation",
            "3. Regression imputation (predict from age, the only observed covariate)",
            "4. Multiple imputation (simplified MICE, 5 draws, age as predictor)",
            "5. Missing-as-indicator (no value imputed; reports mean of observed plus the indicator)",
        ],
        value="1. Complete-case (drop the rows)",
        label="Pick an imputation method to apply to the data above",
    )
    imp_method
    return (imp_method,)


@app.cell
def _(cohort, imp_method, mo, np, observed_df, rng, true_mean):
    df = observed_df.copy()
    is_missing_now = df["crp_observed"].isna()
    n_missing_now = int(is_missing_now.sum())

    if imp_method.value.startswith("1."):
        method_mean = float(np.nanmean(df["crp_observed"]))
        method_n = int((~is_missing_now).sum())
        method_note = (
            "Complete-case analysis drops the missing rows entirely. The estimate is just the mean of the observed rows. "
            "Unbiased under MCAR; biased in the direction of the values you lost under MAR and MNAR."
        )
    elif imp_method.value.startswith("2."):
        filled = df["crp_observed"].copy()
        observed_mean_now = filled.mean()
        filled = filled.fillna(observed_mean_now)
        method_mean = float(filled.mean())
        method_n = len(df)
        method_note = (
            "Every missing cell gets the observed-mean value. By construction the imputed mean equals the observed mean. "
            "Mean imputation doesn't 'fix' bias; it just lets you keep the N. Variance is artificially compressed because every imputed cell sits exactly at the mean."
        )
    elif imp_method.value.startswith("3."):
        obs = df[~is_missing_now]
        x_obs = np.column_stack([np.ones(len(obs)), obs["age"].values])
        y_obs = obs["crp_observed"].values
        beta, *_ = np.linalg.lstsq(x_obs, y_obs, rcond=None)
        missing_subset = df[is_missing_now]
        x_missing = np.column_stack([np.ones(len(missing_subset)), missing_subset["age"].values])
        predicted = x_missing @ beta
        filled = df["crp_observed"].copy()
        filled.loc[is_missing_now] = predicted
        method_mean = float(filled.mean())
        method_n = len(df)
        method_note = (
            "Regression imputation predicts each missing CRP from the patient's age (the observed covariate) using a model "
            "trained on the observed rows, then fills those predictions in. **Note:** `disease_activity` is part of what drives "
            "CRP in this synthetic cohort, but we're treating it as unobserved here, the way underlying disease severity often "
            "is in real registries. Under MAR this corrects most of the bias. Under MNAR it does not, because the unobserved "
            "thing driving missingness (the CRP value itself) is exactly what we're trying to recover."
        )
    elif imp_method.value.startswith("4."):
        obs = df[~is_missing_now]
        x_obs = np.column_stack([np.ones(len(obs)), obs["age"].values])
        y_obs = obs["crp_observed"].values
        beta, *_ = np.linalg.lstsq(x_obs, y_obs, rcond=None)
        residuals = y_obs - x_obs @ beta
        residual_sd = float(residuals.std(ddof=2))
        missing_subset = df[is_missing_now]
        x_missing = np.column_stack([np.ones(len(missing_subset)), missing_subset["age"].values])
        predicted = x_missing @ beta
        n_draws = 5
        draw_means = []
        for _ in range(n_draws):
            noise = rng.normal(0, residual_sd, size=len(predicted))
            filled = df["crp_observed"].copy()
            filled.loc[is_missing_now] = predicted + noise
            draw_means.append(float(filled.mean()))
        method_mean = float(np.mean(draw_means))
        method_n = len(df)
        method_note = (
            f"Multiple imputation (a simplified 5-draw version of MICE). Each missing CRP gets {n_draws} different plausible "
            f"values, drawn from the regression model's posterior. Run the analysis on each completed dataset, pool the means "
            f"via Rubin's rules. The per-draw means were {[round(x, 2) for x in draw_means]}. "
            "Unbiased under MAR; still biased under MNAR. The advantage over a single regression imputation is honest "
            "uncertainty: each imputed cell has a different value across draws, which means the pooled confidence interval "
            "reflects the real uncertainty about what those missing values were."
        )
    else:
        method_mean = float(np.nanmean(df["crp_observed"]))
        method_n = int((~is_missing_now).sum())
        method_note = (
            "Missing-as-indicator: leave the missing values empty, but add a binary `crp_missing` column the model can use. "
            f"The reported mean of the observed values is {method_mean:.2f} (same as complete-case). "
            f"The added information is that {n_missing_now} patients have `crp_missing = True`. "
            "Tree models, regularized regressions, and FHIR's `dataAbsentReason` extension can all use this. "
            "Plain linear regression cannot."
        )

    bias_method = method_mean - true_mean

    if abs(bias_method) < 0.5:
        kind = "success"
        verdict = "recovers the truth closely"
    elif abs(bias_method) < 2.0:
        kind = "info"
        verdict = "partly corrects the bias"
    else:
        kind = "warn"
        verdict = "does not fix the bias"

    summary = mo.md(
        f"""
        **True mean CRP:** {true_mean:.2f} mg/L.

        **Estimated mean after this imputation:** {method_mean:.2f} mg/L, based on N = {method_n}.

        **Residual bias:** {bias_method:+.2f} mg/L. _This method {verdict}._

        {method_note}
        """
    )
    callout = mo.callout(summary, kind=kind)
    callout
    return bias_method, method_mean


@app.cell
def _(mo):
    mo.md(
        r"""
        **What the five methods produce under each mechanism:**

        - **Under MCAR:** complete-case is fine. Every imputation method works. The differences are about variance, not bias.
        - **Under MAR:** complete-case is biased. Mean imputation is also biased (same as complete-case for the mean). Regression imputation and multiple imputation correct the bias. Missing-as-indicator preserves the bias in the observed mean but adds the indicator as model input.
        - **Under MNAR:** *no* method that uses only observed variables fixes the bias. Regression imputation and MICE both reduce it slightly (because age and disease_activity are correlated with CRP), but they cannot recover what's gone. The honest tools are sensitivity analysis ("how bad could this bias be under different MNAR assumptions?") and going back to get the data.

        This is the punchline. Imputation is not a black box that "fixes missing data." Imputation is a *modeling assumption*, and the assumption only holds when the mechanism cooperates.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 6. Drop or keep? A decision framework

        Imputation is the late-stage question. The earlier question, which determines what imputation you even need, is: *should this column or row be in the analysis at all?*

        ### Drop a column when:

        | Reason | Threshold (rule of thumb, not a rule) |
        |---|---|
        | Critical missingness in a load-bearing column | >50% missing in the variable the analysis needs |
        | Non-essential, included from the export by default | Any missingness; the column isn't needed |
        | So corrupted that imputation isn't credible | E.g. 60% missing + 30% miscoded |
        | Duplicate of a more complete column | Two CRP columns, one 90% one 30% complete; keep the 90% |

        ### Keep a column when:

        | Reason | What you do about the missingness |
        |---|---|
        | Load-bearing for the question | Impute, document the choice |
        | Missingness itself is informative | Add a missing-indicator column |
        | Rare but predictive | Drop from the main analysis; keep for subgroup analyses |

        ### Drop rows (complete-case) when:

        | Condition | Defensible? |
        |---|---|
        | Missingness plausibly MCAR | Yes |
        | Cohort large enough to absorb the loss (e.g. 5% of 10,000) | Yes |
        | Quick descriptive characterization, not inferential | Yes, with disclosure |
        | Missingness patterned (MAR or MNAR) | No |
        | Cohort small | No; imputation preserves N |

        The "what fraction missing is too much?" question has no fixed answer. The right rule is: *how much work do I need the rest of the dataset to do, and is that credible?* Imputing half a column from the rest is asking the rest to do too much. Imputing 5% of a column when you have rich predictors of the missing pattern is fine.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 7. The inventory routine

        When you inherit a clinical dataset, before you analyze it:

        1. **Convert all missing-like strings to proper nulls.** `pd.read_csv(..., na_values=["NA","NULL","Unknown",".","9999",""])`.
        2. **Compute the missingness rate per column.** A two-line summary table: how much is missing, where.
        3. **Look at the missing rows.** Cluster by site, time period, subgroup? If yes, missingness is structured.
        4. **Ask whoever knows the data.** "These two hundred rows have missing CRP. What happened?" The answer often surfaces causes 1 through 4 from Section 2.
        5. **Decide drop or keep per column** (Section 6 framework).
        6. **Decide drop rows or impute** (Section 6 framework).
        7. **If imputing, pick a method on purpose** (Section 5 menu).
        8. **Document every decision in plain English.** "We dropped `serum_iron` because 67% missing and not load-bearing for the disease-activity analysis." That sentence is the audit trail.

        ## What this leaves you

        Five things in place:

        1. **A null is not a value.** It's an absence with a cause. Identify the cause before the analysis, not after.
        2. **MCAR, MAR, MNAR** are three categories of cause. Plain English, clinical examples. Each one has a characteristic bias.
        3. **The bias is real and watchable.** The slider above made it visible. Mean of the cohort is not the mean of the observed; the gap is the bias; the gap depends on which mechanism is generating the missingness.
        4. **Imputation is a modeling assumption, not a black box.** The assumption is usually MAR. Under MNAR, no observed-data imputation method fully corrects the bias, and the honest tools are sensitivity analysis and going back to collect more data.
        5. **Drop or keep is a principled decision, not a default.** Each column and each row gets a decision with a stated reason. The reasons go in the methods section, not the appendix.

        Track 04 continues from here. Joins are where missingness gets multiplicative: a left-joined table has missing rows on the right side, and figuring out whether those nulls are MCAR or MNAR is the same framework applied to a different shape of data.
        """
    )
    return


if __name__ == "__main__":
    app.run()
