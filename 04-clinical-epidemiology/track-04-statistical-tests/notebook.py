"""Track 04: Basic statistical tests.

"Which test do I run?" is the wrong starting question. This notebook
walks the variable-type-by-variable-type framework: name the exposure,
the outcome, the group structure, and (when the outcome is continuous)
the parametric vs non-parametric decision. The first interactive is a
live decision-tree that returns the right test plus the reasoning. The
second runs t-test and Mann-Whitney on the same skewed and approximately
normal datasets to show the trade-off. The third puts a sample-size
slider against a fixed effect to show what a CI carries that a p-value
collapses.
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
    from scipy import stats

    rng = np.random.default_rng(20260519)
    return alt, mo, np, pd, rng, stats


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 04: Basic statistical tests

        ## Read the variables before you pick the test

        Ms. Reyes's CRP at baseline was 16 mg/L. Twelve weeks after starting adalimumab, it was 6 mg/L. Across her registry cohort (n = 28), the mean baseline was 18.4 mg/L and the mean 12-week value was 7.1 mg/L. *Is that change statistically meaningful?*

        Most clinicians answer that by trying to remember which test goes with this kind of scenario. The thinking move is the other way around. Name the variables first, and the test follows from a lookup table.

        Three things to identify before anything else:

        1. **The exposure (or grouping) variable.** Categorical (two arms, three arms, treatment vs control, sex) or continuous (a dose, a lab value, an age)?
        2. **The outcome variable.** Continuous (a lab value, a score)? Categorical (event yes/no)? Ordinal (stage I-IV, Likert)? Time-to-event (with censoring)? Count (events per patient)?
        3. **The group structure.** One sample, two independent, two paired, or three or more?

        For Reyes's CRP question: categorical exposure (baseline vs 12-week, the same patients), continuous outcome (CRP value), two paired measurements per patient. That puts you on the "paired t-test or Wilcoxon signed-rank" row of the matrix below. The parametric vs non-parametric choice is the only remaining decision.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1. The pairings matrix

        Most of clinical statistics is a lookup indexed by the three variable answers, with one extra question (parametric vs non-parametric) when the outcome is continuous.

        | Exposure | Outcome | Group structure | Recommended test |
        |---|---|---|---|
        | Categorical | Continuous | One sample | One-sample t-test (or one-sample Wilcoxon) |
        | Categorical | Continuous | Two independent | Independent t-test (or Mann-Whitney U) |
        | Categorical | Continuous | Two paired | Paired t-test (or Wilcoxon signed-rank) |
        | Categorical | Continuous | More than two independent | One-way ANOVA (or Kruskal-Wallis) |
        | Continuous | Continuous | (n/a) | Pearson correlation or linear regression (or Spearman) |
        | Categorical | Categorical | (any) | Chi-square (or Fisher's exact for small cells) |
        | Continuous | Categorical | (n/a) | Logistic regression |
        | Any | Ordinal | (>2 categories) | Ordinal logistic regression (or Mann-Whitney for 2 indep groups) |
        | Categorical | Time-to-event | (any) | Log-rank (unadjusted) or Cox regression (adjusted) |
        | Continuous | Time-to-event | (n/a) | Cox regression |
        | Any | Count | (any) | Poisson regression (or negative binomial when overdispersed) |

        The interactive below walks the four questions and gives back the test plus the one-line reasoning. Use it as a checker for any analysis you read.
        """
    )
    return


@app.cell
def _(mo):
    exposure_q = mo.ui.radio(
        options=["Categorical", "Continuous"],
        label="What is the exposure (or grouping) variable?",
        value="Categorical",
    )
    outcome_q = mo.ui.radio(
        options=["Continuous", "Categorical", "Ordinal", "Time-to-event", "Count"],
        label="What is the outcome variable?",
        value="Continuous",
    )
    groups_q = mo.ui.radio(
        options=[
            "One sample (vs reference)",
            "Two independent groups",
            "Two paired measurements",
            "More than two independent groups",
            "Not applicable (continuous exposure)",
        ],
        label="What is the group structure?",
        value="Two paired measurements",
    )
    paramnp_q = mo.ui.radio(
        options=[
            "Parametric (approximately normal, large enough, no extreme outliers)",
            "Non-parametric (skewed, small, ordinal, or outlier-heavy)",
        ],
        label="If the outcome is continuous: parametric or non-parametric?",
        value="Parametric (approximately normal, large enough, no extreme outliers)",
    )

    mo.md(
        rf"""
        ## 2. The live decision-tree

        Answer the four questions. The recommendation below updates as you change any answer.

        {mo.as_html(mo.vstack([exposure_q, outcome_q, groups_q, paramnp_q]))}
        """
    )
    return exposure_q, groups_q, outcome_q, paramnp_q


@app.cell
def _(exposure_q, groups_q, mo, outcome_q, paramnp_q):
    def _recommend(exposure, outcome, groups, parametric):
        is_param = parametric.startswith("Parametric")
        if outcome == "Continuous":
            if exposure == "Continuous":
                if is_param:
                    return (
                        "Pearson correlation or simple linear regression",
                        "Two continuous variables: the relationship is summarized by a correlation coefficient or a regression slope. Pearson and linear regression assume an approximately linear relationship and roughly normal residuals."
                    )
                return (
                    "Spearman rank correlation",
                    "Two continuous variables, but the assumptions for Pearson do not hold. Spearman correlates the ranks instead and is robust to outliers and monotone non-linear shapes."
                )
            if groups == "One sample (vs reference)":
                return (
                    ("One-sample t-test" if is_param else "One-sample Wilcoxon signed-rank"),
                    "One group's continuous values compared against a fixed reference (a normative mean, a regulatory threshold). The parametric form uses the mean; the non-parametric form uses the ranks of the differences from the reference."
                )
            if groups == "Two independent groups":
                return (
                    ("Independent two-sample t-test" if is_param else "Mann-Whitney U (Wilcoxon rank-sum)"),
                    "Two independent groups (separate patients), continuous outcome. The t-test compares means; Mann-Whitney compares the rank distributions and is robust to outliers and skew."
                )
            if groups == "Two paired measurements":
                return (
                    ("Paired t-test" if is_param else "Wilcoxon signed-rank"),
                    "Two measurements on the same patients (baseline and follow-up, or two methods on the same sample). Work with the within-patient differences. The parametric form assumes those differences are approximately normal; the non-parametric form ranks them."
                )
            if groups == "More than two independent groups":
                return (
                    ("One-way ANOVA" if is_param else "Kruskal-Wallis"),
                    "Three or more independent groups, continuous outcome. ANOVA partitions variance to test whether at least one group mean differs from the others; Kruskal-Wallis is the rank-based analog. If significant, follow up with pairwise post-hoc tests (Tukey HSD for parametric, Dunn for non-parametric)."
                )
            return (
                "Mixed-effects or repeated-measures model",
                "More complex structure than the simple cases. Consider a mixed model with a random effect for patient (or cluster) and a fixed effect for the exposure."
            )
        if outcome == "Categorical":
            if exposure == "Categorical":
                return (
                    "Chi-square test (or Fisher's exact for small expected cells)",
                    "Categorical exposure x categorical outcome makes a contingency table. Chi-square works when expected cell counts are all at least 5. Use Fisher's exact when expected cells drop below 5 (small samples or rare outcomes)."
                )
            return (
                "Logistic regression",
                "Continuous exposure with a binary outcome. Logistic regression models log-odds of the outcome as a linear function of the exposure. The slope exponentiates to an odds ratio per unit of exposure."
            )
        if outcome == "Ordinal":
            if exposure == "Categorical" and groups == "Two independent groups":
                return (
                    "Mann-Whitney U on the ordinal values",
                    "Two independent groups, ordinal outcome (Likert score, disease activity category). Mann-Whitney treats the categories as ranks and is the standard non-parametric two-group test for ordinal outcomes."
                )
            return (
                "Ordinal logistic regression (proportional odds model)",
                "Outcome has more than two ordered categories. Proportional-odds logistic regression preserves the ordering and reports a single odds ratio across cumulative cut-points."
            )
        if outcome == "Time-to-event":
            if exposure == "Categorical":
                return (
                    "Log-rank test (unadjusted) or Cox regression (adjusted)",
                    "Time until an event, with patients censored when follow-up ends. Log-rank compares survival curves between groups without adjustment; Cox regression gives a hazard ratio and accepts covariate adjustment. See Track 05 for the survival-analysis intuition."
                )
            return (
                "Cox proportional-hazards regression",
                "Continuous exposure with a time-to-event outcome. Cox regression gives a hazard ratio per unit of the exposure, assuming the hazards are proportional over time."
            )
        if outcome == "Count":
            return (
                "Poisson regression (or negative binomial when overdispersed)",
                "Counts of events per patient (admissions, exacerbations) over a defined follow-up window. Poisson regression models the rate; negative binomial allows for variance higher than the mean (overdispersion), which is the usual situation in clinical data."
            )
        return (
            "Variable structure not covered by the basic matrix",
            "The combination falls outside the standard four-question framework. Consider a more flexible regression model (generalized linear model, mixed model) or consult a statistician."
        )

    _test, _reasoning = _recommend(
        exposure_q.value, outcome_q.value, groups_q.value, paramnp_q.value
    )

    mo.callout(
        mo.md(
            rf"""
            **Recommended test:** {_test}

            **Reasoning:** {_reasoning}
            """
        ),
        kind="success",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3. Parametric vs non-parametric

        Parametric tests use the **mean** of the sample and assume a distributional shape (usually approximately normal). Non-parametric tests use the **ranks** of the sample and make no shape assumption.

        The reflex to install: **non-parametric is the safer default when you do not have strong evidence the distribution is approximately normal**. The cost of using a non-parametric test when the data are normal is small (a slight loss of power). The cost of using a parametric test when the data are not normal can be much larger, because the mean is sensitive to outliers and the t-test trusts the mean.

        The interactive below makes this concrete. The same statistical question (does TNFi lower CRP in this small registry cohort?) is run twice, once on a skewed CRP-like dataset with a single outlier and once on an approximately normal dataset with the same group sizes and a similar effect.
        """
    )
    return


@app.cell
def _(mo):
    scenario_picker = mo.ui.radio(
        options=["Skewed (CRP-like, with an outlier)", "Approximately normal"],
        label="Pick a data shape:",
        value="Skewed (CRP-like, with an outlier)",
    )
    scenario_picker
    return (scenario_picker,)


@app.cell
def _(alt, mo, np, pd, scenario_picker, stats):
    _scenario = scenario_picker.value

    if _scenario.startswith("Skewed"):
        # Skewed CRP-like (LogNormal). Seed chosen so the outlier is
        # visible and the t-test fails to detect what Mann-Whitney sees.
        _rng = np.random.default_rng(20260540)
        _n = 10
        _a = _rng.lognormal(mean=2.8, sigma=1.5, size=_n)
        _b = _rng.lognormal(mean=1.5, sigma=1.0, size=_n)
        _label_a = "Untreated"
        _label_b = "TNFi"
        _unit = "CRP (mg/L)"
        _note = (
            "These values are skewed: the untreated arm has a single large outlier "
            "(~689 mg/L) that drags the mean far above the median. The t-test trusts "
            "the means; Mann-Whitney compares the ranks and is unaffected."
        )
    else:
        # Approximately normal CRP-like values with the same n.
        _rng = np.random.default_rng(20260602)
        _n = 10
        _a = _rng.normal(loc=20, scale=6, size=_n)
        _b = _rng.normal(loc=14, scale=6, size=_n)
        _label_a = "Untreated"
        _label_b = "TNFi"
        _unit = "CRP (mg/L)"
        _note = (
            "These values are approximately normal: no extreme outliers, similar "
            "spread in both arms. The t-test and Mann-Whitney see roughly the same "
            "thing, with the t-test slightly more powerful (lower p) because its "
            "assumptions hold."
        )

    _t_res = stats.ttest_ind(_a, _b)
    _mw_res = stats.mannwhitneyu(_a, _b, alternative="two-sided")

    _summary_df = pd.DataFrame({
        "Group": [_label_a, _label_b],
        "n": [len(_a), len(_b)],
        "mean": [_a.mean(), _b.mean()],
        "median": [np.median(_a), np.median(_b)],
        "min": [_a.min(), _b.min()],
        "max": [_a.max(), _b.max()],
    })

    _data_df = pd.DataFrame({
        "group": [_label_a] * len(_a) + [_label_b] * len(_b),
        "value": np.concatenate([_a, _b]),
    })

    _strip = (
        alt.Chart(_data_df)
        .mark_circle(size=80, opacity=0.7)
        .encode(
            x=alt.X("value:Q", title=_unit),
            y=alt.Y("group:N", title=None),
            color=alt.Color("group:N", legend=None),
        )
        .properties(width=620, height=140, title=f"{_unit} by arm")
    )

    _interpretation = (
        "**Both tests agree.** When the data are approximately normal, "
        "the parametric and non-parametric tests reach similar conclusions, "
        "with the t-test slightly more powerful."
        if not _scenario.startswith("Skewed")
        else "**The two tests disagree.** Mann-Whitney's small p-value picks up "
             "the rank-based difference that the t-test misses. The t-test sees "
             "a large variance in the untreated arm (driven by the outlier) and "
             "concludes the means are not reliably different. If you had reported "
             "only the t-test, you would have missed an effect that is visible in "
             "the medians and the strip plot."
    )

    mo.vstack([
        mo.md(_note),
        mo.as_html(_strip),
        mo.md(rf"""
        ### Summary statistics

        {mo.as_html(_summary_df.round(2))}

        ### Test results

        | Test | p-value |
        |---|---|
        | Independent t-test (parametric, uses means) | **{_t_res.pvalue:.3f}** |
        | Mann-Whitney U (non-parametric, uses ranks) | **{_mw_res.pvalue:.3f}** |

        {_interpretation}
        """),
    ])
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 4. The CI carries information the p-value collapses

        A p-value answers one specific question: *if the null hypothesis were true and we repeated this experiment many times, what fraction of the time would we see a result at least this extreme?* That is useful but limited. It does not tell you the size of the effect, only whether it is far enough from zero to be unlikely under the null.

        A 95% confidence interval gives the same calculation done differently: the range of effect sizes consistent with the data at the conventional threshold. The CI carries three things the p-value does not:

        - **Direction** (the sign of the interval).
        - **Magnitude** (how big the effect could be).
        - **Precision** (how wide the interval is).

        The interactive below holds the true underlying effect fixed at 0.30 (a small-to-moderate Cohen's d) and varies the sample size. Watch the p-value shrink toward zero while the CI tightens toward the true effect. Both move, but the CI moves with information attached.
        """
    )
    return


@app.cell
def _(mo):
    n_slider = mo.ui.slider(
        start=5, stop=500, step=5, value=20,
        label="Patients per group",
        show_value=True, full_width=True,
    )
    n_slider
    return (n_slider,)


@app.cell
def _(alt, mo, n_slider, np, pd, stats):
    _true_effect = 0.30  # Cohen's d-like effect size
    _common_sd = 1.0
    _n_per = int(n_slider.value)

    # Fixed seed so the demo is reproducible across slider moves.
    _sim_rng = np.random.default_rng(20260522)
    _a = _sim_rng.normal(0.0, _common_sd, _n_per)
    _b = _sim_rng.normal(_true_effect, _common_sd, _n_per)

    _t_res = stats.ttest_ind(_a, _b, equal_var=False)
    _observed_diff = float(_b.mean() - _a.mean())
    _se = float(np.sqrt(_a.var(ddof=1) / _n_per + _b.var(ddof=1) / _n_per))
    _df = float(_t_res.df)
    _t_crit = float(stats.t.ppf(0.975, _df))
    _ci_lo = _observed_diff - _t_crit * _se
    _ci_hi = _observed_diff + _t_crit * _se
    _ci_width = _ci_hi - _ci_lo

    # CI strip plot.
    _ci_df = pd.DataFrame({
        "estimate": [_observed_diff],
        "lo": [_ci_lo],
        "hi": [_ci_hi],
        "label": [f"observed effect, n = {_n_per}"],
    })

    _ci_axis = alt.Scale(domain=[-1.5, 1.5])
    _ci_bar = (
        alt.Chart(_ci_df)
        .mark_rule(strokeWidth=3, color="#2ca02c")
        .encode(
            x=alt.X("lo:Q", title="effect size (Group B - Group A)", scale=_ci_axis),
            x2="hi:Q",
            y=alt.Y("label:N", title=None),
        )
    )
    _ci_point = (
        alt.Chart(_ci_df)
        .mark_circle(size=180, color="#2ca02c")
        .encode(x="estimate:Q", y="label:N")
    )
    _null_line = (
        alt.Chart(pd.DataFrame({"x": [0.0]}))
        .mark_rule(strokeDash=[4, 4], color="gray")
        .encode(x="x:Q")
    )
    _truth_line = (
        alt.Chart(pd.DataFrame({"x": [_true_effect]}))
        .mark_rule(color="black", strokeWidth=1)
        .encode(x="x:Q")
    )
    _ci_chart = (
        alt.layer(_null_line, _truth_line, _ci_bar, _ci_point)
        .properties(width=600, height=120)
    )

    _crosses_zero = (_ci_lo < 0 < _ci_hi)
    _interpretation = (
        f"At n = {_n_per} per group, the observed mean difference is "
        f"{_observed_diff:+.3f}, the p-value is **{_t_res.pvalue:.4f}**, "
        f"and the 95% confidence interval is **[{_ci_lo:+.3f}, {_ci_hi:+.3f}]** "
        f"(width {_ci_width:.3f}). "
        + (
            "The CI crosses zero, so the data are consistent with no effect, "
            "with a small negative effect, and with a moderately large positive "
            "effect. The point estimate may still be informative for future studies, "
            "but on its own, this experiment cannot rule out the null."
            if _crosses_zero
            else "The CI excludes zero, so the data are inconsistent with the null "
                 "of no effect at the conventional threshold. More importantly, "
                 f"the interval [{_ci_lo:+.3f}, {_ci_hi:+.3f}] tells you the range "
                 f"of plausible effect sizes, which is what a clinical reader needs "
                 "to decide whether the effect is large enough to matter."
        )
    )

    mo.vstack([
        mo.md(rf"""
        **True effect built into the data:** 0.30 (dashed line at zero is the null; solid line is the truth).
        """),
        mo.as_html(_ci_chart),
        mo.md(_interpretation),
        mo.md("""
        Drag the slider from n = 5 to n = 500 and watch two things at once:

        - **The p-value falls** from "not significant" at small n to "highly significant" at large n.
        - **The CI tightens** around the true effect of 0.30, regardless of the p-value.

        At small n, two studies seeing the same effect could report opposite "significance" verdicts based on luck of the draw. At large n, the CI converges to the truth. The CI is the thing that carries the precision; the p-value is a coarse summary of whether the CI crosses zero.
        """),
    ])
    return


@app.cell
def _(mo):
    q1 = mo.ui.radio(
        options=[
            "Paired t-test (or Wilcoxon signed-rank if data are skewed).",
            "Independent t-test (or Mann-Whitney if data are skewed).",
            "Chi-square test, treating CRP as high/low.",
            "Cox regression, because there is a time component.",
        ],
        label=(
            "You measured CRP at baseline and at 12 weeks on TNFi in the "
            "same 28 patients. You want to know whether CRP changed. "
            "Which test?"
        ),
    )
    q1
    return (q1,)


@app.cell
def _(mo, q1):
    if q1.value is None:
        out1 = mo.md("_Pick one._")
    else:
        correct1 = q1.value.startswith("Paired t-test")
        out1 = mo.callout(
            mo.md(
                rf"""
                **{'Correct.' if correct1 else 'Not quite.'}**

                The variables are: categorical exposure (baseline vs 12-week, the same patients), continuous outcome (CRP), two paired measurements per patient. That puts you on the "paired t-test or Wilcoxon signed-rank" row of the matrix. The parametric vs non-parametric choice is the only remaining decision, and because CRP is skewed in most clinical cohorts, Wilcoxon signed-rank is usually the safer pick. An independent t-test would be wrong here because it would treat baseline and follow-up as if they were measurements from different patients, throwing away the pairing information.
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
            "The two trials disagree about whether the drug works.",
            "Trial A found an effect; Trial B did not.",
            "Trial A and Trial B are consistent; Trial B is just smaller.",
            "Trial A's p-value is wrong because the CI crosses zero.",
        ],
        label=(
            "Trial A (n = 500/arm) reports a hazard ratio of 0.85 (95% CI 0.74-0.97, "
            "p = 0.02). Trial B (n = 80/arm) reports a hazard ratio of 0.83 (95% CI "
            "0.62-1.10, p = 0.19) on the same intervention. What is the best reading?"
        ),
    )
    q2
    return (q2,)


@app.cell
def _(mo, q2):
    if q2.value is None:
        out2 = mo.md("_Pick one._")
    else:
        correct2 = q2.value.startswith("Trial A and Trial B are consistent")
        out2 = mo.callout(
            mo.md(
                rf"""
                **{'Correct.' if correct2 else 'Not quite.'}**

                The two point estimates (0.85 and 0.83) are essentially identical. The two CIs overlap heavily: Trial A's [0.74, 0.97] sits inside Trial B's [0.62, 1.10]. The trials saw the same effect; Trial B simply had less data, which widened its CI past the null and pushed its p-value above 0.05. Reading these as "disagreeing" because one reaches significance and the other does not is the single most common p-value misinterpretation in the clinical literature. The right reading is "Trial B's CI is consistent with Trial A's effect estimate; the difference in significance is a difference in sample size, not in truth." This is the principle that confidence intervals make easy to see and p-values make easy to miss.
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

        Pick one of the two prompts below and write 4 to 6 sentences in the box that follows. Save what you write outside the browser; the box is a scratch pad, not persistent storage. When you are done, continue to `track-05-study-designs`.

        1. **Pull a clinical paper you've read recently.** Name the exposure variable, the outcome variable, and the group structure. Was the test the authors ran the one the matrix would have picked? If not, what could have justified the divergence?

        2. **A vendor reports** that their new biomarker has a p-value of 0.04 for predicting 30-day readmission. What three pieces of information would you ask for before treating that as a positive result? (Hint: the CI is one of them. What are the other two?)
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
            **Go deeper** is in `track-04-statistical-tests/go-deeper.md`. The next track (`track-05-study-designs`) walks longitudinal designs, the Kaplan-Meier intuition, the log-rank test, and a five-question design-picker that reframes "which study should I run?" as a lookup in the same way this track reframed "which test should I run?"
            """
        ),
        kind="info",
    )
    return


if __name__ == "__main__":
    app.run()
