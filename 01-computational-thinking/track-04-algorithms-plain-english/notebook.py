"""Track 04: Algorithms in plain English.

An algorithm is a finite list of named operations on named inputs. Most
clinical scores share a common skeleton (transformed and weighted inputs,
summed, with cutoffs added on top). This notebook walks DAS28 line by
line on Ms. Elena Reyes's most recent values.

You move sliders for her TJC28, SJC28, CRP, and patient global
assessment; each step's contribution to the score updates live. By the
end you should be able to read any published clinical score the same
way.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import math
    import marimo as mo
    import pandas as pd
    return math, mo, pd


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 04: Algorithms in plain English

        ## What the word actually means.

        The word **algorithm** sounds like a black box, so we treat it like one. The thing the word actually means is small: a finite list of named operations on named inputs. Every clinical score is one of these: CHA₂DS₂-VASc, Wells, Centor, qSOFA, MELD, APGAR, the Glasgow Coma Scale, DAS28. They differ in which inputs they take and which operations they perform, but they share a skeleton: take a few inputs, transform each one in a defined way, weight the transformed values, sum them, and compare the sum against a clinical cutoff.

        The worked example for this track is **DAS28**, the rheumatology standard for rheumatoid arthritis disease activity. It takes four inputs (tender joint count out of twenty-eight assessed joints, swollen joint count out of the same twenty-eight, an acute-phase reactant, and a patient global assessment) and produces a continuous score with conventional cutoffs for remission, low, moderate, and high disease activity. We're using DAS28 as the worked example because it lives on the curriculum's running patient (Ms. Reyes has seropositive RA), because it's small enough to walk end to end in one notebook, and because its weighted-and-transformed-sum skeleton is the same skeleton almost every other published clinical score uses. Read it once and you can read all of them.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The four inputs.

        DAS28 takes exactly four inputs about the patient. That's a Track-03-abstraction result in itself: a measure of a chronic systemic disease has decided to ignore every other data point about the patient (age, sex, every other lab, medication history, imaging, prior flare frequency) and still produces a clinically useful number.

        - **TJC28 (tender joint count).** The number of tender joints out of the twenty-eight assessed: PIPs, MCPs, wrists, elbows, shoulders, and knees, bilaterally. Integer, 0 to 28.
        - **SJC28 (swollen joint count).** Same twenty-eight joints assessed for swelling. Integer, 0 to 28.
        - **CRP (C-reactive protein).** The acute-phase reactant. Continuous, mg/L. (The other common version of the score uses ESR.)
        - **PGA (patient global assessment).** The patient's own rating of overall disease activity. Visual analog scale, 0 to 100 mm.

        Ms. Reyes's most recent visit gives us TJC28 = 6, SJC28 = 3, CRP = 6 mg/L, PGA = 40. The sliders below start at those values; move them to see what DAS28 would be for a different patient or a different visit.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The formula.

        DAS28-CRP is exactly this:

        ```
        DAS28-CRP = 0.56 × √TJC28
                  + 0.28 × √SJC28
                  + 0.36 × ln(CRP + 1)
                  + 0.014 × PGA
                  + 0.96
        ```

        Five terms, four of which come from a slider and the fifth a constant. We'll walk each one. Move the sliders to change Ms. Reyes's inputs and watch the contribution table update.
        """
    )
    return


@app.cell
def _(mo):
    tjc = mo.ui.slider(start=0, stop=28, step=1, value=6,  label="Tender joint count (TJC28)", show_value=True)
    sjc = mo.ui.slider(start=0, stop=28, step=1, value=3,  label="Swollen joint count (SJC28)", show_value=True)
    crp = mo.ui.slider(start=0, stop=100, step=0.5, value=6, label="CRP (mg/L)", show_value=True)
    pga = mo.ui.slider(start=0, stop=100, step=1, value=40, label="Patient global assessment (0 to 100 mm VAS)", show_value=True)
    mo.vstack([tjc, sjc, crp, pga])
    return crp, pga, sjc, tjc


@app.cell
def _(crp, math, mo, pd, pga, sjc, tjc):
    tjc_val = tjc.value
    sjc_val = sjc.value
    crp_val = crp.value
    pga_val = pga.value

    tjc_contrib = 0.56 * math.sqrt(tjc_val)
    sjc_contrib = 0.28 * math.sqrt(sjc_val)
    crp_contrib = 0.36 * math.log(crp_val + 1)
    pga_contrib = 0.014 * pga_val
    constant = 0.96

    das28 = tjc_contrib + sjc_contrib + crp_contrib + pga_contrib + constant

    rows = [
        {
            "step": "Tender joint count",
            "math": f"0.56 × √{tjc_val} = 0.56 × {math.sqrt(tjc_val):.2f}",
            "contribution": f"{tjc_contrib:.2f}",
        },
        {
            "step": "Swollen joint count",
            "math": f"0.28 × √{sjc_val} = 0.28 × {math.sqrt(sjc_val):.2f}",
            "contribution": f"{sjc_contrib:.2f}",
        },
        {
            "step": "CRP",
            "math": f"0.36 × ln({crp_val:.1f} + 1) = 0.36 × {math.log(crp_val + 1):.2f}",
            "contribution": f"{crp_contrib:.2f}",
        },
        {
            "step": "Patient global assessment",
            "math": f"0.014 × {pga_val}",
            "contribution": f"{pga_contrib:.2f}",
        },
        {
            "step": "Constant",
            "math": "(intercept, always 0.96)",
            "contribution": f"{constant:.2f}",
        },
    ]
    contribution_table = pd.DataFrame(rows)

    if das28 < 2.6:
        interp = "Remission"
        kind = "success"
    elif das28 <= 3.2:
        interp = "Low disease activity"
        kind = "info"
    elif das28 <= 5.1:
        interp = "Moderate disease activity"
        kind = "warn"
    else:
        interp = "High disease activity"
        kind = "warn"

    score_block = mo.vstack(
        [
            mo.ui.table(contribution_table, selection=None),
            mo.callout(
                mo.md(
                    f"**DAS28-CRP = {das28:.2f}**\n\n"
                    f"Interpretation (EULAR thresholds): **{interp}**."
                ),
                kind=kind,
            ),
        ]
    )
    score_block
    return (
        constant,
        contribution_table,
        crp_contrib,
        crp_val,
        das28,
        interp,
        kind,
        pga_contrib,
        pga_val,
        rows,
        score_block,
        sjc_contrib,
        sjc_val,
        tjc_contrib,
        tjc_val,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What each line is doing.

        Look at the table while you read this. The contribution numbers move with the sliders.

        **Tender joints: `0.56 × √TJC28`.** The square root is doing diminishing-returns work. Going from 0 to 4 tender joints adds a lot to the score (√0 = 0, √4 = 2). Going from 16 to 20 adds much less (√16 = 4, √20 ≈ 4.47). The clinical reading is that the first few tender joints carry most of the signal; once the patient is already polyarticular, additional joints don't move disease activity proportionally. The weight (0.56) is the largest in the formula, which says the model thinks tender joints matter more per unit than any other single input.

        **Swollen joints: `0.28 × √SJC28`.** Same diminishing-returns shape, half the weight. The original DAS28 regression found that swelling carries less per-unit signal than tenderness, possibly because it is more variable across examiners and because tenderness captures the patient's own pain experience while swelling is observer-dependent. Move the SJC slider and you'll notice the contribution changes more slowly than TJC's.

        **CRP: `0.36 × ln(CRP + 1)`.** The natural log is order-of-magnitude compression. CRP can plausibly span three orders of magnitude in inflammatory disease (under 1, around 10, over 100). A logarithm collapses that range into a manageable scale where the difference between 1 and 10 is the same size as the difference between 10 and 100. The `+1` is a numerical convenience that lets the function be evaluated at CRP = 0 without diverging. The weight (0.36) is moderate.

        **Patient global assessment: `0.014 × PGA`.** The identity transformation (no square root, no log), with a tiny weight. Move the PGA slider from 0 to 100; the contribution moves from 0 to 1.4. The PGA mostly functions as a fine-tuning input in DAS28. Some clinicians read this weight as "the patient's voice barely matters to the score," and there is a small literature making exactly that critique. The point for now is that you can read the weight directly off the formula.

        **The constant (0.96).** The intercept. A fixed baseline added regardless of inputs. It exists because the regression that produced DAS28 was fit on a population in which the average score wasn't centered at zero. The constant pulls the scale into the range where the original cutoffs land. It has no clinical interpretation on its own.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The cutoffs are a separate decision.

        The formula gives you a number. The number gets interpreted using clinical cutoffs:

        | DAS28-CRP | Category |
        |---|---|
        | < 2.6 | Remission |
        | 2.6 to 3.2 | Low disease activity |
        | > 3.2 to 5.1 | Moderate disease activity |
        | > 5.1 | High disease activity |

        These thresholds are **not part of the math.** They are a separate clinical convention. The original DAS28 cutoffs were derived for the ESR version of the score; many practices use the same thresholds for DAS28-CRP despite a small revision literature suggesting different ones for the CRP version would be more appropriate (Fleischmann 2017, others). Treat-to-target guidelines (Smolen 2016) use these thresholds for treatment-intensification decisions; that is the deployment context that makes the cutoff choice consequential.

        The reading move: when you see a clinical score with a category interpretation, ask two questions separately:
        1. Where does the *number* come from? (The formula.)
        2. Where does the *category boundary* come from? (The cutoff, derived separately, sometimes contested.)

        Treating the two as one thing is how a contestable threshold sneaks into a treatment-intensification decision.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Reading any clinical score.

        You can now do this with any published clinical score: CHA₂DS₂-VASc, Wells, Centor, qSOFA, MELD, APGAR, Glasgow Coma Scale, HAS-BLED, Framingham, ASCVD risk, MEWS, NEWS. Read each line and ask:

        1. **What is the transformation doing?** Identity, square root, log, indicator, or some piecewise threshold? Each shape has a clinical reading.
        2. **Why is the weight the size it is?** What does it imply about the relative importance of this input? What would change if it were doubled or halved?
        3. **What happens at the edges?** What does the line do when its input is zero, missing, or at its maximum? Look at it on a slider.
        4. **Where does this weight come from?** Was it fit on a particular population, a particular era, a particular outcome definition? The same formula can fit a different patient population poorly.

        If you can answer all four for every line, you understand the score. If you can't, you are running it on faith. That has been the default for most clinical scores for decades; the move of this track is making it not the default for you.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## One more.")
    return


@app.cell
def _(mo):
    quiz = mo.ui.radio(
        options=[
            "Treats each additional prior exacerbation as adding the same risk.",
            "Diminishing returns: early exacerbations contribute more per unit than later ones.",
            "Sets a hard threshold at one or more prior exacerbations.",
            "Converts a discrete count into a probability.",
        ],
        label=(
            "Suppose a research group proposes a new asthma exacerbation risk score with the formula: "
            "ARS = 0.5 × √(prior_year_exacerbations) + 0.3 × ln(eosinophil_count + 1) + 0.02 × age + 1.4. "
            "What is the `0.5 × √(prior_year_exacerbations)` term doing?"
        ),
    )
    quiz
    return (quiz,)


@app.cell
def _(mo, quiz):
    if quiz.value is None:
        quiz_response = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif quiz.value.startswith("Diminishing returns"):
        quiz_response = mo.callout(
            mo.md(
                "**Yes.** The square root means the difference between zero and four prior exacerbations contributes more (√4 = 2) than the difference between sixteen and twenty (√20 minus √16 is about 0.47). "
                "Clinically that reads as a model assumption that the first one or two exacerbations carry the most signal about an unstable phenotype, and additional exacerbations beyond that confirm what's already known rather than escalating risk linearly. The same reasoning applies to the TJC term in DAS28."
            ),
            kind="success",
        )
    elif quiz.value.startswith("Treats each additional"):
        quiz_response = mo.callout(
            mo.md(
                "**No.** That description matches the identity transformation (`x` going in unchanged), not the square root. With identity, the contribution would scale linearly with the count. Square root compresses higher counts: √16 to √20 is a much smaller move than √0 to √4."
            ),
            kind="warn",
        )
    elif quiz.value.startswith("Sets a hard threshold"):
        quiz_response = mo.callout(
            mo.md(
                "**No.** A threshold would look like an indicator function (the term contributes a fixed amount if the count is at or above some cutoff, zero otherwise). Square root is continuous; every count contributes something, and the shape of the contribution is smooth."
            ),
            kind="warn",
        )
    else:
        quiz_response = mo.callout(
            mo.md(
                "**No.** Square root is a transformation, not a probability map. The score after summing the terms could be passed through a logistic function elsewhere in the pipeline to produce a probability, but the square root itself only compresses the input."
            ),
            kind="warn",
        )
    quiz_response
    return (quiz_response,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What you did in this track.

        - You read DAS28 line by line and watched each step's contribution change with the sliders.
        - You named the work each transformation is doing: square root for diminishing returns on joint counts, log for order-of-magnitude compression on CRP, identity for the PGA.
        - You separated the formula (which produces a number) from the cutoff (which interprets the number into a clinical category). These are different decisions made by different people on different evidence.
        - You picked up a four-question framework for reading any published clinical score.

        Decomposition (Track 01) made the parts visible. Edge cases (Track 02) showed where they break. Abstraction (Track 03) chose what to keep. Algorithmic reading (this track) made the kept-and-combined version inspectable. That is most of computational thinking applied to clinical decision rules.

        ## What's next.

        **Track 05: When to trust a computer.** The four-question framework: what was it trained on, what does it optimize for, where does it fail, and who does it fail for? Applied to a fictional hospital deterioration score. The course's capstone (Socratic walkthrough designing your own clinical decision rule) follows after.
        """
    )
    return


if __name__ == "__main__":
    app.run()
