"""Track 03: Diagnostic test performance.

The 2x2 table is the central object. Sensitivity, specificity, PPV, NPV,
and likelihood ratios are five views of the same four cells. This
notebook makes the relationships visible: sliders for sens/spec/prev
drive a live 2x2 with PPV/NPV/LR+/LR- computed in place; an ROC
explorer puts two synthetic anti-CCP-style distributions on the same
axes as a threshold slider and shows the trade-off as the cutoff moves.
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

    rng = np.random.default_rng(20260519)
    return alt, mo, np, pd, rng


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 03: Diagnostic test performance

        ## The number that comes back depends on what you thought before you ordered it

        A 52-year-old woman with three months of bilateral MCP and PIP swelling comes to your rheumatology clinic. The clinical picture fits inflammatory polyarthritis; your pre-test probability for RA is high, maybe 50%. You order anti-CCP.

        The result you get back is the same number whichever clinic she walked into. What changes from clinic to clinic is what that number *means*. The same positive anti-CCP that confidently confirms RA in your rheumatology clinic is barely diagnostic at all in a population screening setting, and the reason is arithmetic, not biology.

        This track makes that arithmetic visible. The 2x2 table is the central object. Sensitivity, specificity, PPV, NPV, and likelihood ratios are five different views of the same four cells. The first interactive lets you slide sensitivity, specificity, and prevalence and watch all the derived measures update. The second is an ROC explorer: two synthetic anti-CCP distributions, a threshold slider, and three live panels showing the distributions, the 2x2 table, and the ROC curve with a dot at the current threshold.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1. The 2x2 table

        Two binary variables: the patient's true disease state (RA present vs absent, by some reference standard) and the test result (positive vs negative). Every patient lands in exactly one of the four cells.

        |                         | RA present       | RA absent        |
        |-------------------------|------------------|------------------|
        | **Test positive**       | True positive (TP)    | False positive (FP)   |
        | **Test negative**       | False negative (FN)   | True negative (TN)    |

        The five measures we care about are all ratios of cells in this table. Two read the columns (properties of the test); two read the rows (properties of the test in this population); the likelihood ratios collapse them into one number that updates pre-test probability.

        - **Sensitivity** = TP / (TP + FN). Read the RA-present column. The fraction of RA patients who test positive. A property of the test.
        - **Specificity** = TN / (TN + FP). Read the RA-absent column. The fraction of non-RA patients who test negative. A property of the test.
        - **PPV** = TP / (TP + FP). Read the test-positive row. The fraction of positive tests that are true positives. Depends on prevalence.
        - **NPV** = TN / (TN + FN). Read the test-negative row. The fraction of negative tests that are true negatives. Depends on prevalence.
        - **LR+** = sens / (1 - spec). How much a positive test multiplies pre-test odds. Test-only.
        - **LR-** = (1 - sens) / spec. How much a negative test multiplies pre-test odds. Test-only.

        Sens and spec do not move with prevalence. PPV and NPV do. The next cell lets you put numbers on that claim.
        """
    )
    return


@app.cell
def _(mo):
    sens_slider = mo.ui.slider(
        start=0.05, stop=0.99, step=0.01, value=0.67,
        label="Sensitivity", show_value=True, full_width=True,
    )
    spec_slider = mo.ui.slider(
        start=0.05, stop=0.99, step=0.01, value=0.95,
        label="Specificity", show_value=True, full_width=True,
    )
    prev_slider = mo.ui.slider(
        start=0.005, stop=0.95, step=0.005, value=0.30,
        label="Prevalence", show_value=True, full_width=True,
    )

    mo.md(
        rf"""
        ## 2. Slide the three knobs

        Default values are the operating point of anti-CCP in a rheumatology referral clinic: sensitivity 67%, specificity 95%, RA prevalence about 30%. Move them and watch the 2x2 table and the derived measures update.

        {mo.as_html(mo.vstack([sens_slider, spec_slider, prev_slider]))}
        """
    )
    return prev_slider, sens_slider, spec_slider


@app.cell
def _(mo, prev_slider, sens_slider, spec_slider):
    # Cell-private (underscore-prefixed) to avoid marimo cross-cell collisions.
    _n_total = 10000
    _sens = sens_slider.value
    _spec = spec_slider.value
    _prev = prev_slider.value

    _diseased = round(_n_total * _prev)
    _not_diseased = _n_total - _diseased
    _tp = round(_diseased * _sens)
    _fn = _diseased - _tp
    _tn = round(_not_diseased * _spec)
    _fp = _not_diseased - _tn

    _ppv = _tp / (_tp + _fp) if (_tp + _fp) > 0 else float("nan")
    _npv = _tn / (_tn + _fn) if (_tn + _fn) > 0 else float("nan")
    _lr_pos = _sens / (1 - _spec) if _spec < 1 else float("inf")
    _lr_neg = (1 - _sens) / _spec if _spec > 0 else float("inf")

    def _fmt(x, pct=False):
        if x != x:
            return "n/a"
        if x == float("inf"):
            return "∞"
        return f"{x*100:.1f}%" if pct else f"{x:.2f}"

    mo.md(
        rf"""
        ### A cohort of 10,000 patients at this prevalence

        | | RA present | RA absent | Row total |
        |---|---|---|---|
        | **Test positive** | {_tp:,} (TP) | {_fp:,} (FP) | {_tp + _fp:,} |
        | **Test negative** | {_fn:,} (FN) | {_tn:,} (TN) | {_fn + _tn:,} |
        | **Column total** | {_diseased:,} | {_not_diseased:,} | {_n_total:,} |

        | Measure | Value | Reads which part of the table |
        |---|---|---|
        | Sensitivity | {_fmt(_sens, pct=True)} | TP / (TP + FN), the RA-present column |
        | Specificity | {_fmt(_spec, pct=True)} | TN / (TN + FP), the RA-absent column |
        | **PPV** | **{_fmt(_ppv, pct=True)}** | TP / (TP + FP), the test-positive row |
        | **NPV** | **{_fmt(_npv, pct=True)}** | TN / (TN + FN), the test-negative row |
        | LR+ | {_fmt(_lr_pos)} | sens / (1 - spec) |
        | LR- | {_fmt(_lr_neg)} | (1 - sens) / spec |

        Move the prevalence slider while leaving sens and spec fixed. Sens, spec, LR+, and LR- do not move. PPV and NPV both move. PPV moves *a lot*.
        """
    )
    return


@app.cell
def _(mo):
    # Bayesian collapse table at fixed anti-CCP-like sens/spec across
    # a wide prevalence range. Wrap the loop in a function so its locals
    # don't leak to marimo's top-level cell scope.
    def _build_collapse_rows():
        sens_fixed = 0.67
        spec_fixed = 0.95
        prevalences = [0.005, 0.01, 0.05, 0.10, 0.30, 0.50]
        rows = []
        for p in prevalences:
            n = 100000
            d = round(n * p)
            nd = n - d
            tp = round(d * sens_fixed)
            fp = round(nd * (1 - spec_fixed))
            fn = d - tp
            tn = nd - fp
            ppv = tp / (tp + fp) if (tp + fp) > 0 else float("nan")
            npv = tn / (tn + fn) if (tn + fn) > 0 else float("nan")
            rows.append((p, tp, fp, ppv, npv))
        return rows

    rows_md = "\n        ".join(
        rf"| {p*100:.1f}% | {tp:,} | {fp:,} | **{ppv*100:.1f}%** | {npv*100:.2f}% |"
        for (p, tp, fp, ppv, npv) in _build_collapse_rows()
    )

    mo.md(
        rf"""
        ## 3. The Bayesian collapse, in numbers

        Hold the test fixed at sensitivity 67%, specificity 95% (the anti-CCP operating point). Vary only the prevalence of RA in the population the test is being used on. Each row below is the same 100,000-patient cohort with that prevalence.

        | RA prevalence | True positives | False positives | **PPV** | NPV |
        |---|---|---|---|---|
        {rows_md}

        Read the PPV column from bottom to top. At a 50% pre-test probability (highly selected rheumatology clinic), a positive anti-CCP is essentially confirmatory (PPV ≈ 93%). At 5% (general practice joint-pain workup), the same positive is barely better than a coin flip (PPV ≈ 41%). At 0.5% (population screening of asymptomatic adults), most positives are false (PPV ≈ 6%).

        The test got no worse. The denominator changed. At low prevalence, the false-positive arithmetic dominates because there are so many more non-diseased people in the population than diseased people. This is the single most-missed point in clinical diagnostics, and it is the reason "context-free test ordering" produces false-positive workups at scale.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 4. Likelihood ratios: the bedside form of Bayes

        Likelihood ratios collapse sensitivity and specificity into two numbers that turn pre-test probability into post-test probability. The arithmetic is:

        > post-test odds = pre-test odds × LR

        Odds and probability are interchangeable (odds = p / (1 - p), so probability = odds / (1 + odds)).

        - **LR+** = sens / (1 - spec). How much a positive test multiplies the odds of disease.
        - **LR-** = (1 - sens) / spec. How much a negative test multiplies the odds of disease.

        For anti-CCP at sens 67%, spec 95%: **LR+ ≈ 13** and **LR- ≈ 0.35**.

        **Worked example on Ms. Reyes.** She arrives at the rheumatology clinic with bilateral symmetric small-joint synovitis. Your pre-test probability for RA is about 50%, so pre-test odds = 1.0.

        - If anti-CCP comes back **positive**: post-test odds = 1.0 × 13 = 13. Post-test probability = 13 / 14 ≈ **93%**. The positive confirms what you already suspected.
        - If anti-CCP comes back **negative**: post-test odds = 1.0 × 0.35 = 0.35. Post-test probability = 0.35 / 1.35 ≈ **26%**. A negative anti-CCP at this pretest probability does *not* rule RA out; you still have a 1-in-4 chance.

        McGee's 2002 bedside rule for the round-number version of this calculation: an LR+ of 2, 5, or 10 adds about 15, 30, or 45 percentage points to pre-test probability; an LR- of 0.5, 0.2, or 0.1 subtracts the same amounts. Round numbers, no calculator. The mental model: an LR+ of at least 5 or an LR- of at most 0.2 is *meaningfully changing the answer*; anything closer to 1 is decorative.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 5. ROC curves: when the test result is a continuous number

        Most "tests" are not really binary. Anti-CCP returns a titer in U/mL; troponin returns a continuous level; a risk score returns a number. Someone has picked a cutoff to turn the number into a yes/no result, and the choice of cutoff trades sensitivity for specificity.

        The **ROC curve** plots that trade-off. The x-axis is 1 - specificity (the false-positive rate); the y-axis is sensitivity. Each point on the curve is one possible cutoff. The curve always passes through (0, 0) (cutoff so high nobody tests positive) and (1, 1) (cutoff so low everybody tests positive).

        The shape of the curve tells you how well the test separates diseased from non-diseased patients. A perfect test goes straight up to (0, 1) and across to (1, 1). A useless test lies on the diagonal.

        The **area under the curve (AUC)** summarizes the shape into one number. The geometric reading: AUC is the probability that a randomly chosen diseased patient has a higher test value than a randomly chosen non-diseased patient. AUC 0.5 means coin flip; AUC 1.0 means perfect ordering. Published anti-CCP meta-analyses report AUC around 0.94. The synthetic distributions below are calibrated for visible overlap (so the ROC curve and the trade-off are easy to see on one screen), not for an exact match to published anti-CCP, and produce an AUC closer to 0.86.

        The next cell builds the synthetic anti-CCP-style data and the ROC sweep that the threshold slider will move through.
        """
    )
    return


@app.cell
def _(np, pd, rng):
    # Synthetic anti-CCP-style distributions.
    # RA-positive patients: anti-CCP titer ~ Normal(26, 16), clipped at 0.
    # Joint-pain controls without RA: anti-CCP ~ Normal(9, 6), clipped at 0.
    # AUC of these synthetic distributions is ~0.86; default cutoff
    # of 20 U/mL gives sens ~68% and spec ~97%, close to published
    # anti-CCP performance.
    n_d = 500
    n_nd = 500

    diseased_vals = np.clip(rng.normal(26, 16, n_d), 0.0, None)
    non_diseased_vals = np.clip(rng.normal(9, 6, n_nd), 0.0, None)

    # Pre-compute the ROC sweep once.
    thresholds = np.linspace(0, 100, 401)
    sens_arr = np.array([(diseased_vals > t).mean() for t in thresholds])
    spec_arr = np.array([(non_diseased_vals <= t).mean() for t in thresholds])
    fpr_arr = 1 - spec_arr

    # AUC via Mann-Whitney (probability that a random diseased value
    # exceeds a random non-diseased value).
    auc = float((diseased_vals[:, None] > non_diseased_vals[None, :]).mean())

    # Binned histogram data for the distribution plot.
    max_val = float(max(diseased_vals.max(), non_diseased_vals.max()))
    bin_edges = np.linspace(0, max_val, 31)
    d_counts, _ = np.histogram(diseased_vals, bins=bin_edges)
    nd_counts, _ = np.histogram(non_diseased_vals, bins=bin_edges)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    hist_df = pd.DataFrame({
        "anti_ccp": np.concatenate([bin_centers, bin_centers]),
        "count": np.concatenate([d_counts, nd_counts]),
        "group": ["RA"] * len(bin_centers) + ["no RA"] * len(bin_centers),
    })

    roc_df = pd.DataFrame({
        "fpr": fpr_arr,
        "sens": sens_arr,
        "threshold": thresholds,
    }).sort_values("fpr").reset_index(drop=True)

    roc_data = {
        "diseased": diseased_vals,
        "non_diseased": non_diseased_vals,
        "n_d": n_d,
        "n_nd": n_nd,
        "auc": auc,
        "hist_df": hist_df,
        "roc_df": roc_df,
        "max_val": max_val,
    }
    return (roc_data,)


@app.cell
def _(mo, roc_data):
    threshold_slider = mo.ui.slider(
        start=0.0, stop=80.0, step=1.0, value=20.0,
        label="Cutoff for calling the test positive (U/mL)",
        show_value=True, full_width=True,
    )

    mo.md(
        rf"""
        ## 6. ROC explorer

        The two histograms below are the synthetic anti-CCP distributions: {roc_data["n_d"]} RA patients and {roc_data["n_nd"]} controls with joint pain but no RA. AUC of these distributions is **{roc_data["auc"]:.3f}**. Move the cutoff slider; the threshold line, the 2x2, and the dot on the ROC curve all update.

        {mo.as_html(threshold_slider)}
        """
    )
    return (threshold_slider,)


@app.cell
def _(alt, mo, pd, roc_data, threshold_slider):
    # Underscore-prefixed locals so marimo treats them as cell-private.
    _t = float(threshold_slider.value)
    _d = roc_data["diseased"]
    _nd = roc_data["non_diseased"]

    _tp = int((_d > _t).sum())
    _fn = int((_d <= _t).sum())
    _fp = int((_nd > _t).sum())
    _tn = int((_nd <= _t).sum())

    _sens_t = _tp / (_tp + _fn) if (_tp + _fn) > 0 else 0.0
    _spec_t = _tn / (_tn + _fp) if (_tn + _fp) > 0 else 0.0
    _fpr_t = 1 - _spec_t

    _hist_chart = (
        alt.Chart(roc_data["hist_df"])
        .mark_bar(opacity=0.6)
        .encode(
            x=alt.X("anti_ccp:Q", title="anti-CCP (U/mL)"),
            y=alt.Y("count:Q", title="patients per bin"),
            color=alt.Color(
                "group:N",
                title="group",
                scale=alt.Scale(
                    domain=["RA", "no RA"],
                    range=["#d62728", "#1f77b4"],
                ),
            ),
        )
    )
    _threshold_rule = (
        alt.Chart(pd.DataFrame({"t": [_t]}))
        .mark_rule(color="black", strokeWidth=2)
        .encode(x="t:Q")
    )
    _dist_chart = (
        alt.layer(_hist_chart, _threshold_rule)
        .properties(width=620, height=220, title=f"Distributions with cutoff at {_t:.0f} U/mL")
    )

    _diag_df = pd.DataFrame({"fpr": [0, 1], "sens": [0, 1]})
    _diag = (
        alt.Chart(_diag_df)
        .mark_line(strokeDash=[4, 4], color="lightgray")
        .encode(x="fpr:Q", y="sens:Q")
    )
    _roc_line = (
        alt.Chart(roc_data["roc_df"])
        .mark_line(color="#2ca02c", strokeWidth=2)
        .encode(
            x=alt.X("fpr:Q", title="False positive rate (1 - specificity)", scale=alt.Scale(domain=[0, 1])),
            y=alt.Y("sens:Q", title="Sensitivity", scale=alt.Scale(domain=[0, 1])),
        )
    )
    _current_dot = (
        alt.Chart(pd.DataFrame({"fpr": [_fpr_t], "sens": [_sens_t]}))
        .mark_circle(size=220, color="black")
        .encode(x="fpr:Q", y="sens:Q")
    )
    _roc_chart = (
        alt.layer(_diag, _roc_line, _current_dot)
        .properties(width=380, height=380, title=f"ROC curve (AUC = {roc_data['auc']:.3f})")
    )

    _ppv_t = _tp / (_tp + _fp) if (_tp + _fp) > 0 else float("nan")
    _npv_t = _tn / (_tn + _fn) if (_tn + _fn) > 0 else float("nan")

    def _fmt_pct(x):
        return "n/a" if x != x else f"{x*100:.1f}%"

    _summary_md = mo.md(
        rf"""
        ### At cutoff {_t:.0f} U/mL

        |  | RA present | RA absent |
        |---|---|---|
        | **Test +** | {_tp} | {_fp} |
        | **Test −** | {_fn} | {_tn} |

        | Measure | Value |
        |---|---|
        | Sensitivity | **{_sens_t*100:.1f}%** |
        | Specificity | **{_spec_t*100:.1f}%** |
        | PPV (in this synthetic) | {_fmt_pct(_ppv_t)} |
        | NPV (in this synthetic) | {_fmt_pct(_npv_t)} |

        PPV and NPV here reflect the 1:1 mix of cases and controls in the synthetic, not a real-world prevalence. In a real cohort you would re-weight these by the prevalence in your setting.
        """
    )

    mo.vstack([
        mo.as_html(_dist_chart),
        mo.as_html(_roc_chart),
        _summary_md,
    ])
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            r"""
            **Forward to course 09: AI in medicine.** The ROC curve and AUC summarize *discrimination*: how well the test (or a model) orders patients. A well-discriminating test can still be badly *calibrated*, meaning the probability it assigns to each patient is systematically wrong. Calibration is a separate property and a separate plot. Course 09 takes that distinction apart. Course 11 (decision curve analysis) returns to the operating-point question: at what cutoff does the test create net clinical benefit?
            """
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    q1 = mo.ui.radio(
        options=[
            "PPV will be high; the test is essentially confirmatory.",
            "PPV will be low; most positives will be false positives.",
            "NPV will be low; most negatives will be missed cases.",
            "Sensitivity will drop because the population changed.",
        ],
        label=(
            "An employer-mandated screening program for an asymptomatic "
            "workforce uses a test with sens 90% and spec 95% to screen "
            "for a condition with a population prevalence of 0.5%. "
            "What is most likely to happen?"
        ),
    )
    q1
    return (q1,)


@app.cell
def _(mo, q1):
    if q1.value is None:
        out1 = mo.md("_Pick one._")
    else:
        correct1 = q1.value.startswith("PPV will be low")
        out1 = mo.callout(
            mo.md(
                rf"""
                **{'Correct.' if correct1 else 'Not quite.'}**

                With sens 90% and spec 95% at a prevalence of 0.5%, the 2x2 in 100,000 people: 500 with disease (450 true positives, 50 false negatives) and 99,500 without (4,975 false positives, 94,525 true negatives). PPV = 450 / (450 + 4,975) = **8.3%**. The test isn't bad. The population is. Sensitivity and specificity are properties of the test and don't move with prevalence; what moves is the predictive value. Asymptomatic screening of low-prevalence populations produces large numbers of false positives even with sensitive, specific tests, which is why mass screening programs need to think hard about downstream workup burden.
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
            "About 50% (essentially unchanged).",
            "About 70% (modest increase).",
            "About 85% (substantial increase).",
            "About 95% (essentially confirmatory).",
        ],
        label=(
            "A patient has a 30% pre-test probability for the condition. "
            "The test comes back positive. The test has LR+ = 10. "
            "What is the approximate post-test probability?"
        ),
    )
    q2
    return (q2,)


@app.cell
def _(mo, q2):
    if q2.value is None:
        out2 = mo.md("_Pick one._")
    else:
        correct2 = q2.value.startswith("About 85%")
        out2 = mo.callout(
            mo.md(
                rf"""
                **{'Correct.' if correct2 else 'Not quite.'}**

                Pre-test odds = 0.30 / 0.70 = 0.43. Post-test odds = 0.43 × 10 = 4.3. Post-test probability = 4.3 / 5.3 = **81%**. McGee's bedside shortcut gives the same answer faster: LR+ of 10 adds about 45 percentage points to a pre-test probability, so 30% + 45% = 75%, close enough for clinical thinking. Either way the post-test probability is in the 75% to 85% range, a substantial jump from 30%, but not "essentially confirmatory" the way LR+ of 10 from a 50% pre-test would be (which would land near 91%).
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

        Pick one of the two prompts below and write 4 to 6 sentences in the box that follows. Save what you write outside the browser; the box is a scratch pad, not persistent storage. When you are done, continue to `track-04-statistical-tests`.

        1. **The next test you order** in clinic: what is your pre-test probability *before* you order it, and what would the result need to be (positive vs negative) to actually change what you do? If the answer is "nothing would change my management," reconsider ordering.

        2. **A vendor's diagnostic** reports sens 88%, spec 92%, AUC 0.91 in their validation cohort. What three questions would you ask before letting it into your clinical workflow? (Hint: where was the validation cohort drawn from? What prevalence will the test see in your setting? What is the operating point in their plot, and is that the cutoff you would pick?)
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
            **Go deeper** is in `track-03-diagnostic-test/go-deeper.md`. The next track (`track-04-statistical-tests`) reframes the "which test do I run?" question as a variable-type-by-variable-type framework: think first about what the exposure and outcome variables are, then layer on parametric vs non-parametric.
            """
        ),
        kind="info",
    )
    return


if __name__ == "__main__":
    app.run()