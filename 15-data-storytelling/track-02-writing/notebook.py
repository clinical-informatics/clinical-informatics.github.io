"""Track 02: Writing about data clearly.

No visible code. The notebook presents the three properties of clear data
writing (headline number, uncertainty in language that holds, throat-
clearing removal), runs the reader through a sentence-rewrite exercise on
three real-shaped academic-style sentences, and closes with a quiz on
identifying the failed rewrite.

WASM-safe: no shared imports, no data files, no relative paths.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    SENTENCES = {
        "Sentence 1: jargon-heavy academic style": {
            "original": (
                "Multivariable logistic-regression analysis controlling for "
                "age, sex, Charlson comorbidity index, and prior 30-day "
                "admissions demonstrated a statistically significant "
                "association between the implementation of the sepsis "
                "decision support intervention and 30-day in-hospital "
                "mortality (adjusted odds ratio 0.78, 95% confidence interval "
                "0.62 to 0.97, p = 0.024)."
            ),
            "rewrites": {
                "A: \"The model showed something significant. Mortality went down.\"": {
                    "rating": "Too short and too imprecise.",
                    "analysis": (
                        "The rewrite removes the statistics but does not "
                        "preserve the substantive finding. A reader cannot act "
                        "on this; they do not know by how much, in whom, or "
                        "with what uncertainty. Plain English is not the same "
                        "as oversimplified; the precision the analysis "
                        "produced still has to be conveyed."
                    ),
                },
                "B: \"The sepsis CDS reduced mortality.\"": {
                    "rating": "Substantive direction, but the headline number is missing.",
                    "analysis": (
                        "The claim is now substantive but unquantified. The "
                        "single most useful sentence in any data communication "
                        "is the one that contains the headline number; this "
                        "rewrite leaves that sentence to be inferred. A reader "
                        "who stops here knows the direction of the finding "
                        "but not its magnitude."
                    ),
                },
                "C: \"After adjustment for age, sex, comorbidity, and prior admissions, the sepsis CDS was associated with a 22% relative reduction in 30-day mortality (95% CI 3% to 38%, p=0.024).\"": {
                    "rating": "Better. The substantive claim leads and the uncertainty is named.",
                    "analysis": (
                        "The headline number (22% relative reduction) leads; "
                        "the adjustment is named without dominating; the "
                        "confidence interval and p-value are present without "
                        "being the subject of the sentence. The remaining "
                        "issue is altitude: the relative-risk framing is "
                        "abstract for a non-statistician reader. The best "
                        "rewrite uses an absolute reduction instead."
                    ),
                },
                "D: \"The sepsis CDS reduced 30-day deaths by about 1 per 100 admissions, in a model that adjusted for age, comorbidity, and prior admissions. The reduction is statistically clear (p=0.024) and consistent across subgroups.\"": {
                    "rating": "Best. The substantive finding leads in language a non-statistician can hold.",
                    "analysis": (
                        "The headline is an absolute reduction (1 per 100 "
                        "admissions), which a non-statistician reader can "
                        "translate into the cohort-level effect "
                        "(approximately 150 lives saved across 12,400 "
                        "admissions). The statistical uncertainty is "
                        "summarized as \"statistically clear\" with the "
                        "p-value parenthetical; the subgroup statement adds "
                        "the robustness claim without elaborating. This is "
                        "what plain English for a non-statistician audience "
                        "looks like; the precision is preserved, the "
                        "vocabulary is the reader's."
                    ),
                },
            },
        },
        "Sentence 2: throat-clearing": {
            "original": (
                "It is important to note that, while the data suggest a "
                "possible reduction in mortality, the results should be "
                "interpreted with appropriate caution given the limitations "
                "of an observational design."
            ),
            "rewrites": {
                "A: \"Take this with a grain of salt.\"": {
                    "rating": "Too colloquial, and the substantive finding has been deleted.",
                    "analysis": (
                        "The rewrite removes the throat-clearing but also "
                        "removes the finding. A reader who stops at this "
                        "sentence has no claim to evaluate; the caution stands "
                        "alone without anything to be cautious about."
                    ),
                },
                "B: \"The data suggest mortality went down, with the caveat that this was observational.\"": {
                    "rating": "Better. The finding leads, but the caveat is generic.",
                    "analysis": (
                        "The finding now leads, which is the load-bearing "
                        "move. The caveat (\"this was observational\") is "
                        "specific enough to be informative but does not say "
                        "what the caveat implies for the reader's decision. "
                        "A reader who reads this still does not know whether "
                        "to act."
                    ),
                },
                "C: \"Mortality fell by 1.2 percentage points; the design was observational, so the effect could be confounded by factors we did not measure.\"": {
                    "rating": "Better still. The finding is quantified and the limitation is specific.",
                    "analysis": (
                        "The headline number leads; the limitation is named "
                        "specifically (confounding by unmeasured factors); "
                        "the reader has the substantive content and the "
                        "characteristic caveat without the throat-clearing "
                        "machinery of the original."
                    ),
                },
                "D: \"Mortality fell by 1.2 percentage points. The observational design means a confounder we did not measure could explain the result, though the pre-specified adjustments make this less likely.\"": {
                    "rating": "Best. Finding, specific limitation, specific reassurance.",
                    "analysis": (
                        "The headline number leads; the limitation is named; "
                        "the specific reassurance (\"pre-specified "
                        "adjustments make this less likely\") tells the "
                        "reader what to think about the limitation. The "
                        "rewrite turns the original's vague caution into a "
                        "specific epistemic stance the reader can use to "
                        "calibrate their own confidence in the finding."
                    ),
                },
            },
        },
        "Sentence 3: uncertainty-burying": {
            "original": (
                "The intervention may potentially be associated with "
                "improvements in patient outcomes, although further "
                "investigation is warranted."
            ),
            "rewrites": {
                "A: \"The intervention helped patients but we need more research.\"": {
                    "rating": "Imprecise on both ends.",
                    "analysis": (
                        "\"Helped patients\" is too vague to be evaluated, "
                        "and \"we need more research\" is the standard "
                        "throat-clearing close. The rewrite is shorter than "
                        "the original but no more substantively useful."
                    ),
                },
                "B: \"There was an association between the intervention and improved outcomes.\"": {
                    "rating": "More precise, but still does not name the magnitude.",
                    "analysis": (
                        "\"Association\" is the correct epistemic move (it "
                        "names the correlational nature of the finding), but "
                        "without the magnitude the sentence still asks the "
                        "reader to take the finding on the writer's "
                        "authority. The headline number is what makes the "
                        "finding usable."
                    ),
                },
                "C: \"The intervention reduced 30-day mortality by 1.2 percentage points.\"": {
                    "rating": "Better. The finding is quantified and stated plainly.",
                    "analysis": (
                        "The substantive finding leads with the headline "
                        "number. A reader can act on this. The remaining "
                        "issue is that the reader does not know what would "
                        "strengthen the finding; the next sentence should "
                        "name what better evidence would look like."
                    ),
                },
                "D: \"The intervention reduced 30-day mortality by 1.2 percentage points. A larger or randomized trial would tighten the estimate; the current point estimate is the best evidence we have.\"": {
                    "rating": "Best. The finding leads, and the path to better evidence is named.",
                    "analysis": (
                        "The headline leads; the limitation is named "
                        "specifically (the trial would tighten the estimate, "
                        "not invalidate it); the reassurance is explicit "
                        "(\"the best evidence we have\"). The reader has "
                        "enough to act now and enough to evaluate any future "
                        "claim that supersedes this one."
                    ),
                },
            },
        },
    }

    return SENTENCES, mo


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 02: Writing about data clearly

        A draft sentence reads: "Multivariable logistic-regression analysis controlling for age, sex, Charlson comorbidity index, and prior 30-day admissions demonstrated a statistically significant association between the implementation of the sepsis decision support intervention and 30-day in-hospital mortality (adjusted odds ratio 0.78, 95% confidence interval 0.62 to 0.97, p = 0.024)." The sentence is technically correct and difficult to act on. This track covers the craft of writing the same finding in language a non-statistician executive or non-statistician clinician can use, without surrendering the precision the underlying analysis requires.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Three properties of clear data writing

        Three properties are load-bearing for clear writing about data.

        - **The headline number is the substantive finding.** The single most useful sentence in any data communication is the one that contains the headline number. The number is a change a reader could act on (an absolute reduction, a relative reduction, a count, a dollar number), not the test statistic or the analytic procedure that produced it.
        - **Uncertainty is reported in language the reader can hold.** A 95% confidence interval has a precise statistical meaning that most readers do not have the training to interpret. The communication-craft move is to convey the same statistical uncertainty in language a non-statistician reader can act on (a range stated plainly, a worst-case stated plainly, a robustness statement stated plainly).
        - **Throat-clearing is deleted.** The phrases that delay the substantive content of a sentence ("It is important to note that," "What I want to say is," "One thing worth pointing out") waste the reader's attention in the early sentences when attention is highest. Deleting them and leading with the substantive claim is the single most reliable craft move in writing about data.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Sentence-rewrite exercise

        Three sentences below are real-shaped academic-style writing about data. Each comes with four candidate rewrites, ranked from worst to best. Pick a sentence, pick a rewrite, and read the analysis of why the rewrite works or fails. The exercise is more useful when you read all four rewrites for one sentence before picking the one you would actually use.
        """
    )
    return


@app.cell
def _(SENTENCES, mo):
    sentence_pick = mo.ui.dropdown(
        options=list(SENTENCES.keys()),
        value=list(SENTENCES.keys())[0],
        label="Sentence",
    )
    sentence_pick
    return (sentence_pick,)


@app.cell
def _(SENTENCES, mo, sentence_pick):
    _info = SENTENCES[sentence_pick.value]
    mo.callout(
        mo.md(f"**Original sentence:** {_info['original']}"),
        kind="info",
    )
    return


@app.cell
def _(SENTENCES, mo, sentence_pick):
    _rewrites = list(SENTENCES[sentence_pick.value]["rewrites"].keys())
    rewrite_pick = mo.ui.radio(
        options=_rewrites,
        label="Pick a rewrite",
    )
    rewrite_pick
    return (rewrite_pick,)


@app.cell
def _(SENTENCES, mo, rewrite_pick, sentence_pick):
    if rewrite_pick.value is None:
        _resp = mo.callout(
            mo.md("_Pick a rewrite._"), kind="neutral"
        )
    else:
        _info = SENTENCES[sentence_pick.value]["rewrites"][rewrite_pick.value]
        _kind = "success" if _info["rating"].startswith("Best") else "neutral"
        _body = (
            f"**Rating: {_info['rating']}**\n\n"
            f"{_info['analysis']}"
        )
        _resp = mo.callout(mo.md(_body), kind=_kind)
    _resp
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Uncertainty in language that holds

        The hardest sentence-level move in writing about data is conveying statistical uncertainty in language a non-statistician reader can act on. Three approaches work for most clinical-informatics communication.

        - **State the central estimate plainly; quantify the range as a parenthetical.** "The intervention reduced 30-day mortality by 1.2 percentage points (the underlying analysis is consistent with a reduction between 0.3 and 2.1 percentage points)." The central estimate is the headline; the range is the calibration.
        - **State the worst-plausible case.** "The intervention reduced 30-day mortality by 1.2 percentage points; if the true effect is at the pessimistic end of what the analysis can support, the reduction is 0.3 percentage points (about 35 lives across this cohort)." The worst-plausible case is what an executive needs to defend the decision when the political wind changes.
        - **State the comparison to a meaningful threshold.** "The intervention reduced 30-day mortality by 1.2 percentage points; the reduction is large enough to clear any reasonable willingness-to-pay threshold for the operating cost." The threshold is the action level; the comparison resolves the action question.

        The three are not exclusive; a careful sentence uses one or two together. The failure mode is reciting the confidence interval as the conclusion ("the 95% CI was 0.62 to 0.97"), which leaves the action question with the reader.
        """
    )
    return


@app.cell
def _(mo):
    quiz = mo.ui.radio(
        options=[
            "\"After adjustment for several patient-level covariates, the sepsis decision support intervention was associated with a statistically significant reduction in 30-day in-hospital mortality, with adjusted odds ratio 0.78 (95% CI 0.62 to 0.97, p=0.024); the magnitude of the association was consistent across pre-specified subgroups.\"",
            "\"The sepsis CDS reduced 30-day mortality by 1.2 percentage points (about 1 fewer death per 100 admissions). The analysis adjusted for age, sex, comorbidity, and prior admissions; the reduction was consistent in every subgroup we examined. The observational design means a confounder we did not measure could explain the result, though the pre-specified adjustments make this less likely.\"",
            "\"The intervention may potentially be associated with improvements in patient outcomes. While the data suggest a possible reduction, the results should be interpreted with appropriate caution, and further investigation is warranted to confirm these findings.\"",
            "\"The intervention worked. Mortality dropped meaningfully across the entire study period. Results were robust to multiple sensitivity analyses and to alternative specifications, providing strong evidence that the program should be continued.\"",
        ],
        label=(
            "You are writing the executive summary for a sepsis CDS evaluation "
            "for a CFO who is deciding whether to fund the next fiscal year. "
            "Which of the four sentences below is the strongest opener?"
        ),
    )
    quiz
    return (quiz,)


@app.cell
def _(mo, quiz):
    if quiz.value is None:
        _resp = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif quiz.value.startswith("\"The sepsis CDS reduced 30-day mortality by 1.2"):
        _resp = mo.callout(
            mo.md(
                "**Correct.** The sentence leads with the headline number (1.2 "
                "percentage points, translated into the absolute count) in "
                "language a CFO can hold; the adjustments are named without "
                "dominating; the limitation is specific (confounding by "
                "unmeasured factors); the reassurance is specific (the "
                "pre-specified adjustments). The CFO has the substantive "
                "finding and the characteristic limitation in the first three "
                "sentences and can act on the content. This is the executive-"
                "summary opener for a financial decision."
            ),
            kind="success",
        )
    elif quiz.value.startswith("\"After adjustment"):
        _resp = mo.callout(
            mo.md(
                "**The relative-risk framing is wrong for a CFO.** The "
                "sentence is correct, but \"adjusted odds ratio 0.78\" is "
                "abstract for an executive reader. The statistical content "
                "leads instead of the substantive finding; the CFO who reads "
                "this sentence has to do the translation work themselves, and "
                "many will simply stop reading. The rewrite that leads with "
                "the absolute reduction (1.2 percentage points, about 1 per "
                "100 admissions) is the stronger opener."
            ),
            kind="warn",
        )
    elif quiz.value.startswith("\"The intervention may potentially"):
        _resp = mo.callout(
            mo.md(
                "**This is the throat-clearing failure.** \"May potentially\" "
                "is hedging-on-hedging; \"appropriate caution\" and \"further "
                "investigation is warranted\" are the standard closing phrases "
                "of an academic paper. A CFO reading this sentence does not "
                "know what the intervention did, by how much, or whether to "
                "fund it. The opening sentence has to lead with the "
                "substantive finding."
            ),
            kind="warn",
        )
    else:
        _resp = mo.callout(
            mo.md(
                "**The sentence overstates the certainty.** \"Worked,\" "
                "\"meaningfully,\" \"strong evidence\" do work that the data "
                "do not support without the specific numbers. An executive "
                "reader who has been shown overstated claims before will "
                "discount this sentence on instinct. The rewrite that leads "
                "with the absolute reduction and names the observational "
                "limitation explicitly is more credible, not less."
            ),
            kind="warn",
        )
    _resp
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Where this goes next

        Clear sentences are the unit; the next move is to assemble those sentences into a narrative that turns the finding into a recommendation the audience can act on. Track 03 covers the three-part structure (finding, implication, recommendation) and the clinical story that gives the data its meaning.
        """
    )
    return


if __name__ == "__main__":
    app.run()
