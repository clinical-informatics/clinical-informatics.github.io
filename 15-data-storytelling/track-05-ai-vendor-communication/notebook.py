"""Track 05: Communicating with AI teams and vendors.

No visible code. The notebook presents the clinician-as-domain-expert
framing, names the three properties of good vendor questions (specific,
comparative, operational), runs the reader through five vendor scenarios
with weak-to-strong follow-up questions, and closes with a cross-reference
to Course 09's AI-evaluation framework.

WASM-safe: no shared imports, no data files, no relative paths.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    SCENARIOS = {
        "Scenario 1: The vendor claims AUC 0.82 across 250,000 patients.": {
            "context": (
                "The vendor's lead slide reads: \"Our sepsis-prediction model "
                "achieved an AUC of 0.82 across 250,000 patients from three "
                "academic medical centers.\" The room is paused for "
                "questions."
            ),
            "questions": {
                "A: \"That's impressive.\"": {
                    "rating": "Not a question.",
                    "analysis": (
                        "The default deference move. It signals attentiveness "
                        "without exercising clinical judgment. The vendor's "
                        "response will be the practiced confirmation that the "
                        "model is impressive; the room has learned nothing."
                    ),
                },
                "B: \"What was your training-set size?\"": {
                    "rating": "Closed question. Answer rehearsed.",
                    "analysis": (
                        "A specific question but one the vendor has practiced "
                        "the answer to (the same 250,000 figure or a larger "
                        "training number). It produces a number that does not "
                        "tell the room whether the model will work for them."
                    ),
                },
                "C: \"How does the AUC perform in subgroups, especially older adults with multiple comorbidities?\"": {
                    "rating": "Specific and clinically grounded.",
                    "analysis": (
                        "Specific about the subgroup of concern and grounded "
                        "in the clinician's knowledge of which subgroup the "
                        "institution cares about. The answer (assuming the "
                        "vendor has it) is informative; if the vendor does "
                        "not have it, the absence is informative."
                    ),
                },
                "D: \"How does the model's PPV at your recommended operational threshold compare to the rules-based alert we already have, in our patient population?\"": {
                    "rating": "Specific, comparative, operational.",
                    "analysis": (
                        "Specific (PPV at the operational threshold, not AUC "
                        "in the training cohort), comparative (against the "
                        "existing alert), and operational (in the "
                        "institution's patient population, not the vendor's). "
                        "This is the question that produces the most "
                        "informative answer: either a defensible comparison "
                        "the vendor has run, or an admission that the "
                        "comparison has not been run. Either result tells the "
                        "room what they need to know."
                    ),
                },
            },
        },
        "Scenario 2: The vendor cites validation at \"3 academic medical centers.\"": {
            "context": (
                "The vendor's deployment slide shows three logo blocks: a "
                "large East Coast academic medical center, a Midwestern "
                "academic medical center, and a West Coast academic medical "
                "center. The validation results are reported as pooled across "
                "the three sites."
            ),
            "questions": {
                "A: \"That sounds rigorous.\"": {
                    "rating": "Not a question.",
                    "analysis": (
                        "The default deference. The room learns nothing about "
                        "the heterogeneity between the three sites or the "
                        "relevance to the institution's own setting."
                    ),
                },
                "B: \"Were the academic centers similar to ours?\"": {
                    "rating": "Yes/no question.",
                    "analysis": (
                        "Closed. The vendor will say \"yes, they include "
                        "similar settings to yours\" without committing to a "
                        "specific comparison. The room has not learned how "
                        "the model performed at the most similar site or how "
                        "performance varied across sites."
                    ),
                },
                "C: \"What were the patient demographics at each site, and how did performance vary across sites?\"": {
                    "rating": "Specific about heterogeneity.",
                    "analysis": (
                        "Specific about the dimension that matters (demographics "
                        "and per-site variation). Forces the vendor to either "
                        "produce the per-site numbers (informative) or admit "
                        "that pooling was the analytic strategy (also "
                        "informative)."
                    ),
                },
                "D: \"Which of the three sites looks most like our patient population (insurance mix, language, comorbidity burden, acuity)? What was the model's performance at that site specifically?\"": {
                    "rating": "Specific, comparative, operational.",
                    "analysis": (
                        "Specific about the comparison the institution actually "
                        "cares about (the most similar site), comparative "
                        "(across-site differences), and operational (in the "
                        "form most relevant to the local deployment decision). "
                        "If the vendor cannot produce the most-similar-site "
                        "result, the institution has learned that the pooled "
                        "AUC may not transfer."
                    ),
                },
            },
        },
        "Scenario 3: The vendor demos the alert firing on three example patients.": {
            "context": (
                "The vendor's UI demo shows the alert firing on three example "
                "patients who all proceeded to develop severe sepsis within 12 "
                "hours. The cases are visually compelling and clinically "
                "plausible."
            ),
            "questions": {
                "A: \"Looks great.\"": {
                    "rating": "Not a question.",
                    "analysis": (
                        "Demo cases are selected; the room cannot learn from "
                        "them about the false-positive or false-negative "
                        "behavior of the alert. The default deference loses "
                        "the opportunity to surface what the demo did not "
                        "show."
                    ),
                },
                "B: \"Can we customize the alert thresholds?\"": {
                    "rating": "Configuration question, not a performance question.",
                    "analysis": (
                        "A reasonable practical question, but it does not "
                        "address the clinical-performance behavior of the "
                        "alert in failure modes. The vendor will say \"yes, "
                        "the thresholds are configurable\" without the room "
                        "learning whether the configuration space includes "
                        "settings that produce acceptable performance."
                    ),
                },
                "C: \"What does the workflow look like when the alert is wrong? How does a clinician override it, and what feedback loop captures the override?\"": {
                    "rating": "Operational and failure-mode-focused.",
                    "analysis": (
                        "Names the failure mode (the alert is wrong) and the "
                        "operational consequence (override and feedback loop). "
                        "Surfaces whether the vendor has thought about the "
                        "post-deployment learning loop. If the answer is "
                        "evasive, the institution knows the alert will not "
                        "improve in the field."
                    ),
                },
                "D: \"Show me an example of an alert that fired but the clinician overrode it. What was the patient's actual outcome? How did your model handle the disagreement?\"": {
                    "rating": "Specific, operational, demanding evidence.",
                    "analysis": (
                        "Asks for the case the demo did not show: the false-"
                        "positive. The follow-up (\"how did your model handle "
                        "the disagreement\") tests whether the vendor has a "
                        "story for model improvement in deployment. A vendor "
                        "who cannot produce a documented false-positive case "
                        "with a specified outcome has not deployed the model "
                        "at the depth needed to learn from it."
                    ),
                },
            },
        },
        "Scenario 4: The vendor cites their customer logos.": {
            "context": (
                "The vendor's customer slide shows logos for twelve major U.S. "
                "health systems and an aggregate claim of \"trusted by leading "
                "academic medical centers.\" The deployment scale is presented "
                "without operational detail."
            ),
            "questions": {
                "A: \"How long have you been working with them?\"": {
                    "rating": "Procedural question.",
                    "analysis": (
                        "A reasonable practical question that the vendor has "
                        "the answer to. It tells the room about the duration "
                        "of the relationship, not about the quality of the "
                        "deployment or the clinician experience."
                    ),
                },
                "B: \"How happy are they with the product?\"": {
                    "rating": "Vague and rehearsed.",
                    "analysis": (
                        "The vendor will produce a satisfaction figure or a "
                        "customer quote. Both are selected; neither tells the "
                        "room about the cases where the deployment was hard."
                    ),
                },
                "C: \"Can I talk to a clinician at one of those sites, not someone the vendor selects?\"": {
                    "rating": "Specific and demands access.",
                    "analysis": (
                        "Specific about the request (a clinician, not a "
                        "selected reference customer). Forces the vendor to "
                        "either facilitate the conversation (informative) or "
                        "refuse (also informative). A vendor who facilitates "
                        "access has nothing to hide; a vendor who refuses "
                        "should be assumed to."
                    ),
                },
                "D: \"Can I see a specific deployment that was de-implemented or substantially modified after going live? What were the lessons?\"": {
                    "rating": "Demands evidence of failure.",
                    "analysis": (
                        "Every honestly deployed product has at least one "
                        "site where it did not work as planned and was "
                        "modified or removed. A vendor with deployments at "
                        "twelve major systems has stories of difficult sites. "
                        "A vendor who cannot produce such a story is either "
                        "hiding it or has not deployed at the depth required "
                        "to encounter the realistic failure modes."
                    ),
                },
            },
        },
        "Scenario 5: The vendor proposes a $500K annual contract.": {
            "context": (
                "The vendor's pricing slide shows a $500,000 annual contract "
                "with three-year commitment, including model integration, "
                "support, and \"continuous performance monitoring.\" The "
                "performance-monitoring detail is described as \"included.\""
            ),
            "questions": {
                "A: \"That's a lot.\"": {
                    "rating": "Statement, not a question.",
                    "analysis": (
                        "The price is high but the question is the wrong one. "
                        "The room should be asking about the operational "
                        "guarantees that justify the price, not the price "
                        "itself."
                    ),
                },
                "B: \"What's included in the support?\"": {
                    "rating": "Configuration question.",
                    "analysis": (
                        "The vendor will produce a list of included items. "
                        "The list will not tell the room what happens when "
                        "the model performs worse in the institution's "
                        "population than expected."
                    ),
                },
                "C: \"If the model performs worse in our population than in the validation cohort, what's the contract mechanism?\"": {
                    "rating": "Operational and contract-grounded.",
                    "analysis": (
                        "Names the failure mode (performance drop in the local "
                        "population) and the operational consequence (the "
                        "contract mechanism). Forces the vendor to commit to a "
                        "performance guarantee or to acknowledge that there "
                        "is none."
                    ),
                },
                "D: \"What's the contract mechanism for monitoring performance drift, retraining, and de-implementation? Who pays for what in each case?\"": {
                    "rating": "Specific, operational, lifecycle-grounded.",
                    "analysis": (
                        "Covers the full deployment lifecycle (monitoring, "
                        "retraining, de-implementation) and forces the vendor "
                        "to commit to which party pays for each. A vendor who "
                        "has thought about deployment can answer this; a "
                        "vendor who has not will produce the contract's "
                        "boilerplate. The answer is the most efficient signal "
                        "of whether the vendor has the operational maturity "
                        "the institution needs."
                    ),
                },
            },
        },
    }

    return SCENARIOS, mo


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 05: Communicating with AI teams and vendors

        A vendor walks into a meeting with a 32-slide deck on their clinical-AI product. Three of those slides will be about model performance; the rest are about market opportunity, customer logos, and integration partners. The clinician in the room is being asked to evaluate whether the product makes sense for the institution. The default failure mode is to defer to the vendor's framing, which by design draws the reader's attention to the strongest claims and away from the weakest. This track covers the practice of the clinician as the domain expert in the room: the questions that surface what the vendor would prefer the buyer not see, the discipline of asking comparative questions rather than absolute ones, and the cross-reference to the AI-evaluation framework Course 09 built.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The clinician as the domain expert

        The vendor knows machine learning. The clinician knows when an AI-generated recommendation makes clinical sense and when it does not, what the workflow looks like at the bedside, what the institution's patient population actually is, and what good clinical work in that population looks like. The clinician's authority in the room comes from clinical expertise, not from technical deference.

        The most common failure mode is the inverse: the clinician treats the vendor as the expert and themselves as the layperson, asks the vendor questions about machine learning the vendor is prepared to answer, and does not ask the questions about clinical fit the vendor is not. The clinician's job in the meeting is to know what good clinical work looks like, and to ask the question that produces the most informative answer about whether the product supports that work.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Three properties of good vendor questions

        Three properties distinguish a question that produces an informative answer from a question that produces the vendor's practiced summary.

        - **Specific.** Asks about a precise mechanism rather than the marketing summary. Not "is your model accurate," but "what was the AUC in the subgroup with chronic kidney disease at your second validation site."
        - **Comparative.** Asks how a feature compares to an explicit alternative. Not "does your model detect sepsis," but "how does your model's PPV at the operational threshold compare to the existing rules-based alert at our institution."
        - **Operational.** Asks about what happens in failure modes. Not "what's your accuracy," but "when the model is wrong, what is the clinical workflow consequence and how is the error surfaced."

        A question that meets all three properties is hard for the vendor to deflect: the answer is either the specific operational comparison the institution wants, or an admission that the vendor does not have that comparison. Either result is informative.
        """
    )
    return


@app.cell
def _(SCENARIOS, mo):
    scenario_pick = mo.ui.dropdown(
        options=list(SCENARIOS.keys()),
        value=list(SCENARIOS.keys())[0],
        label="Scenario",
    )
    mo.vstack(
        [
            mo.md(
                "## Scenario-and-question exercise\n\n"
                "**Pick a scenario, then pick a follow-up question.** The reactive "
                "panel shows the rating and the analysis of what makes the "
                "question informative or evasive."
            ),
            scenario_pick,
        ]
    )
    return (scenario_pick,)


@app.cell
def _(SCENARIOS, mo, scenario_pick):
    _info = SCENARIOS[scenario_pick.value]
    mo.callout(
        mo.md(f"**Scenario context:** {_info['context']}"),
        kind="info",
    )
    return


@app.cell
def _(SCENARIOS, mo, scenario_pick):
    _questions = list(SCENARIOS[scenario_pick.value]["questions"].keys())
    question_pick = mo.ui.radio(
        options=_questions,
        label="Follow-up question",
    )
    question_pick
    return (question_pick,)


@app.cell
def _(SCENARIOS, mo, question_pick, scenario_pick):
    if question_pick.value is None:
        _resp = mo.callout(
            mo.md("_Pick a follow-up question._"), kind="neutral"
        )
    else:
        _info = SCENARIOS[scenario_pick.value]["questions"][question_pick.value]
        _kind = "success" if _info["rating"].startswith("Specific,") and "operational" in _info["rating"].lower() else "neutral"
        _body = (
            f"**Rating: {_info['rating']}**\n\n"
            f"{_info['analysis']}"
        )
        _resp = mo.callout(mo.md(_body), kind=_kind)
    _resp
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            **Cross-reference (Course 09, AI in medicine).** Course 09's five-dimension evaluation framework (training population, outcome definition, validation approach, calibration reporting, subgroup performance) is the substantive backing for the questions in this track. The vendor questions that produce the most informative answers are the ones that map cleanly to a Course 09 dimension: the subgroup-performance question, the validation-population-vs-deployment-population question, the calibration-at-the-operational-threshold question. The clinician asking those questions is not improvising; they are applying Course 09's framework to the vendor's claims, in the form a clinical conversation supports.
            """
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Where this goes next

        The course capstone takes the CDS design brief from Course 12 and produces two communication artifacts: a 2-minute verbal pitch for a CMO, and a one-page visual summary for clinical staff. The capstone is the synthesis of the five tracks: audience analysis, clear writing, narrative structure, visual presentation, and the practice of communicating across the technical-clinical interface. The artifacts are the kind that an actual clinical-informatics implementation team would produce for the actual approvals and rollouts that follow a CDS design.
        """
    )
    return


if __name__ == "__main__":
    app.run()
