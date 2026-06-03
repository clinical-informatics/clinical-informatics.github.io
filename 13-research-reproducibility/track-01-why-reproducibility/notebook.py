"""Track 01: Why reproducibility matters.

No visible code. The notebook defines the reproducible / replicable / robust
distinction, presents the replication crisis, and uses an interactive
garden-of-forking-paths demonstration on a small synthetic RA trial to show
how defensible analytic choices move a result across the p < 0.05 line.

WASM-safe: no shared imports, no data files, pure-Python statistics inlined.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    # Synthetic two-arm RA dataset, inlined so the notebook runs in the browser.
    # Each row: (arm, DAS28 reduction at 12 weeks, at 24 weeks, seropositive, completed protocol)
    # T = adalimumab added to methotrexate; C = methotrexate alone.
    _DATA = [
        ("T", 0.6, 1.0, 1, 1), ("T", 0.2, 0.9, 1, 1), ("T", 1.3, 1.8, 1, 1),
        ("T", 0.1, 0.4, 0, 1), ("T", 0.7, 1.6, 1, 1), ("T", 1.1, 2.0, 1, 1),
        ("T", 0.0, 0.3, 0, 0), ("T", 0.5, 1.1, 1, 1), ("T", 0.4, 0.7, 1, 1),
        ("T", 0.9, 1.7, 1, 1), ("T", -0.2, 0.2, 0, 0), ("T", 0.8, 1.5, 1, 1),
        ("C", 0.4, 0.8, 1, 1), ("C", 0.5, 0.7, 1, 1), ("C", 0.2, 0.6, 0, 1),
        ("C", 0.7, 1.0, 1, 1), ("C", 0.3, 0.9, 1, 1), ("C", 0.1, 0.3, 0, 0),
        ("C", 0.6, 0.8, 1, 1), ("C", 0.2, 0.7, 1, 1), ("C", 0.5, 0.6, 0, 1),
        ("C", 0.8, 1.1, 1, 1), ("C", -0.1, 0.2, 0, 0), ("C", 0.3, 0.9, 1, 1),
    ]

    def forking_result(window, exclusion, subgroup):
        import math

        def _betacf(a, b, x):
            MAXIT, EPS, FPMIN = 200, 3e-12, 1e-30
            qab, qap, qam = a + b, a + 1, a - 1
            c, d = 1.0, 1.0 - qab * x / qap
            if abs(d) < FPMIN:
                d = FPMIN
            d = 1.0 / d
            h = d
            for m in range(1, MAXIT + 1):
                m2 = 2 * m
                aa = m * (b - m) * x / ((qam + m2) * (a + m2))
                d = 1.0 + aa * d
                if abs(d) < FPMIN:
                    d = FPMIN
                c = 1.0 + aa / c
                if abs(c) < FPMIN:
                    c = FPMIN
                d = 1.0 / d
                h *= d * c
                aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
                d = 1.0 + aa * d
                if abs(d) < FPMIN:
                    d = FPMIN
                c = 1.0 + aa / c
                if abs(c) < FPMIN:
                    c = FPMIN
                d = 1.0 / d
                de = d * c
                h *= de
                if abs(de - 1.0) < EPS:
                    break
            return h

        def _betai(a, b, x):
            if x <= 0:
                return 0.0
            if x >= 1:
                return 1.0
            lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
            bt = math.exp(lbeta + a * math.log(x) + b * math.log(1.0 - x))
            if x < (a + 1) / (a + b + 2):
                return bt * _betacf(a, b, x) / a
            return 1.0 - bt * _betacf(b, a, 1.0 - x) / b

        col = 1 if window == "12 weeks" else 2
        rows = _DATA
        if exclusion == "Protocol completers only":
            rows = [r for r in rows if r[4] == 1]
        if subgroup == "Seropositive patients only":
            rows = [r for r in rows if r[3] == 1]
        tv = [r[col] for r in rows if r[0] == "T"]
        cv = [r[col] for r in rows if r[0] == "C"]
        nx, ny = len(tv), len(cv)
        mx, my = sum(tv) / nx, sum(cv) / ny
        vx = sum((v - mx) ** 2 for v in tv) / (nx - 1)
        vy = sum((v - my) ** 2 for v in cv) / (ny - 1)
        se = math.sqrt(vx / nx + vy / ny)
        t = (mx - my) / se
        df = (vx / nx + vy / ny) ** 2 / (
            (vx / nx) ** 2 / (nx - 1) + (vy / ny) ** 2 / (ny - 1)
        )
        p = _betai(df / 2.0, 0.5, df / (df + t * t))
        return {"nT": nx, "nC": ny, "diff": mx - my, "p": p}

    return forking_result, mo


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 01: Why reproducibility matters

        A landmark preclinical cancer paper is cited a thousand times. A pharmaceutical team spends two years and several million dollars trying to build on it. The result will not come back. When the team asks the original laboratory for the data and the analysis steps, what arrives is a figure, a methods paragraph, and no way to rerun anything.

        This is the ordinary form of the problem, and it is expensive. Amgen scientists reported in 2012 that they could confirm only 6 of 53 landmark preclinical cancer studies. The Open Science Collaboration repeated 100 published psychology experiments in 2015 and reproduced the original significant result in roughly a third of them. The point of this course is the set of practices that prevent a clinical-research project from joining those numbers.

        This first track does two things: it pins down what the word "reproducibility" actually means, and it shows the single most common way a published result becomes untrustworthy without anyone committing fraud.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## One word doing the work of three

        "Reproducibility" is used loosely for three distinct properties. Keeping them separate is the first skill.

        | Property | The question it answers | What you need |
        |---|---|---|
        | **Reproducible** | Given your data and your code, do I get your result? | The same data, the same analysis steps |
        | **Replicable** | If I run your study again with new data, do I reach your conclusion? | A new cohort, the same protocol |
        | **Robust** | Does your conclusion survive a different defensible analysis of the same data? | The same data, different analytic choices |

        Reproducibility is about the computational pipeline. Replicability is about the science. Robustness is about whether the finding depended on one specific chain of choices. A clinical-research result that lacks any of the three is fragile, but they fail for different reasons and the fixes are different.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            **Reproducible is not the same as correct.** An analysis can be perfectly reproducible and still wrong: the code faithfully reruns and returns the same biased estimate every time. Reproducibility is a necessary property, not a sufficient one. It is what makes an error *findable*. A result no one can rerun cannot be checked, corrected, or built on, which is why reproducibility comes first even though it does not, by itself, make a finding true.
            """
        ),
        kind="warn",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The most common way a result goes wrong

        Fraud is rare. The common failure is quieter, and it does not feel like misconduct from the inside. Consider an analysis of whether adding a biologic to methotrexate improves disease activity in an RA cohort. The analyst faces a series of choices, each individually defensible:

        - **The outcome window.** Measure the DAS28 reduction at 12 weeks, or at 24 weeks?
        - **Who to include.** Everyone randomized, or only the patients who completed the protocol?
        - **Which patients to analyze.** The whole cohort, or the seropositive patients in whom the biologic is most expected to work?

        Each of these is a reasonable decision a thoughtful clinician could defend. The interactive below runs the actual analysis under whichever combination of choices you select, on a fixed synthetic dataset of 24 patients. The data never change. Only the choices change.
        """
    )
    return


@app.cell
def _(mo):
    window = mo.ui.dropdown(
        options=["12 weeks", "24 weeks"],
        value="12 weeks",
        label="Outcome window",
    )
    exclusion = mo.ui.dropdown(
        options=["All randomized patients", "Protocol completers only"],
        value="All randomized patients",
        label="Who to include",
    )
    subgroup = mo.ui.dropdown(
        options=["Whole cohort", "Seropositive patients only"],
        value="Whole cohort",
        label="Which patients to analyze",
    )
    mo.vstack(
        [
            mo.md("**Choose the analysis.** Every option is individually defensible."),
            window,
            exclusion,
            subgroup,
        ]
    )
    return exclusion, subgroup, window


@app.cell
def _(exclusion, forking_result, mo, subgroup, window):
    _r = forking_result(window.value, exclusion.value, subgroup.value)
    _sig = _r["p"] < 0.05
    _verdict = (
        "**statistically significant** (p < 0.05)"
        if _sig
        else "**not statistically significant** (p ≥ 0.05)"
    )
    _kind = "success" if _sig else "neutral"
    mo.callout(
        mo.md(
            f"""
            ### Result under these choices

            Treatment arm: {_r['nT']} patients. Control arm: {_r['nC']} patients.

            Mean DAS28 reduction, treatment minus control: **{_r['diff']:+.2f} points**.

            Two-sided p-value: **{_r['p']:.3f}**. This result is {_verdict}.
            """
        ),
        kind=_kind,
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What just happened

        The honest pre-specified analysis (12-week window, all randomized patients, whole cohort) returns a difference of about 0.16 points with a p-value near 0.31. There is no detectable effect. An analyst who wanted a positive result, and who had not committed to an analysis in advance, could switch to the 24-week window, restrict to the seropositive subgroup, and arrive at a p-value near 0.01. Same patients, same measurements, opposite conclusion.

        Three named patterns describe this:

        - **Researcher degrees of freedom.** The many small, defensible analytic choices that together let an analyst (consciously or not) steer toward a desired answer.
        - **p-hacking.** Trying analytic variations until one crosses p < 0.05, then reporting only that one.
        - **HARKing.** Hypothesizing After the Results are Known: presenting the seropositive-subgroup finding as though it had been the hypothesis all along.

        None of these requires dishonesty. They happen one reasonable decision at a time. The structural defense is **pre-registration**: recording the primary outcome and the analysis plan in a time-stamped public record *before* the data are analyzed, so the analysis cannot be retrofitted to the result. The reproducibility defense, which the rest of this course builds, is that every choice is documented and the whole pipeline can be rerun and inspected by someone else.
        """
    )
    return


@app.cell
def _(mo):
    crisis_quiz = mo.ui.radio(
        options=[
            "It is reproducible but probably not replicable.",
            "It is replicable but not reproducible.",
            "It is neither reproducible nor replicable.",
            "It is robust.",
        ],
        label=(
            "A published RA analysis ships its dataset and a script. You run the script on the dataset "
            "and get exactly the paper's numbers. You then notice the headline finding came from a "
            "24-week seropositive-subgroup analysis that was not the pre-registered primary outcome, and "
            "the pre-registered 12-week whole-cohort analysis was null. How would you describe this result?"
        ),
    )
    crisis_quiz
    return (crisis_quiz,)


@app.cell
def _(crisis_quiz, mo):
    if crisis_quiz.value is None:
        _resp = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif crisis_quiz.value.startswith("It is reproducible but probably not"):
        _resp = mo.callout(
            mo.md(
                "**Correct.** You reran the code on the data and got the same numbers, so the analysis is "
                "reproducible. But the finding lives on a post-hoc subgroup and window that were not "
                "pre-specified, and the pre-registered primary was null, so there is little reason to expect "
                "a fresh cohort to replicate it. This is the exact case where reproducibility and correctness "
                "come apart: the pipeline is sound, the inference is not."
            ),
            kind="success",
        )
    elif crisis_quiz.value.startswith("It is replicable but not reproducible"):
        _resp = mo.callout(
            mo.md(
                "**The two labels are reversed.** You did rerun the code and reproduce the numbers, so it is "
                "reproducible by definition. Replicability is the open question, and the post-hoc subgroup "
                "finding is exactly the kind that tends not to replicate in a new cohort."
            ),
            kind="warn",
        )
    elif crisis_quiz.value.startswith("It is neither"):
        _resp = mo.callout(
            mo.md(
                "**Half right.** Replicability is doubtful, yes. But you reran the script and got the paper's "
                "numbers, which is the definition of reproducible. The problem is not that the pipeline fails "
                "to rerun; it is that a reproducible pipeline produced an inference that probably will not hold up."
            ),
            kind="warn",
        )
    else:
        _resp = mo.callout(
            mo.md(
                "**No.** Robustness means the conclusion survives different defensible analyses of the same "
                "data. Here the conclusion flips between the pre-registered primary (null) and the post-hoc "
                "subgroup (significant), which is the opposite of robust."
            ),
            kind="warn",
        )
    _resp
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Where this course goes

        Reproducibility is the property that makes every other check possible. The remaining tracks build the practices that produce it:

        - **Track 02** organizes a data project so it can be rerun at all.
        - **Track 03** keeps the complete history of the project with version control, so no analysis decision is silently lost.
        - **Track 04** documents where the data came from and what was done to it, so the chain from raw record to published number is reconstructable.
        - **Track 05** covers what to share, and which reporting guideline forces the missing details into the open before publication.

        The capstone audits a synthetic published analysis that did none of this, and produces the documentation plan that would fix it.
        """
    )
    return


if __name__ == "__main__":
    app.run()
