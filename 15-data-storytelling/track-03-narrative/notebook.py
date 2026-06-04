"""Track 03: Building a narrative.

No visible code. The notebook presents the three-part Finding-Implication-
Recommendation structure on a synthetic RA-flare-CDS scenario (cross-ref
to Course 12), runs the reader through weak-vs-strong rewrites of each
part, displays the assembled best version, and closes with a quiz on a
common failure mode.

WASM-safe: no shared imports, no data files, no relative paths.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    PARTS = {
        "Finding (what the data shows)": {
            "Level 1: vague": {
                "text": "There was an increase in flares.",
                "analysis": (
                    "The claim is directional but not specific, not sourced, "
                    "and not quantified. A reader cannot verify it or weight "
                    "it against other findings. The default failure mode for "
                    "the finding part of a narrative is to state the direction "
                    "without the magnitude or the source."
                ),
            },
            "Level 2: hedged, no number": {
                "text": "The flare rate appears to be rising.",
                "analysis": (
                    "Slightly better than vague (the metric is named) but the "
                    "hedging (\"appears to be\") and the missing number leave "
                    "the reader without enough to act. The finding should "
                    "stand on the data, not on the writer's hedged confidence "
                    "in the data."
                ),
            },
            "Level 3: specific, quantified, sourced": {
                "text": (
                    "Across the rheumatology service, the rate of "
                    "moderate-to-severe RA flares rose from 12 to 19 per 100 "
                    "patient-quarters between 2024 Q2 and 2025 Q2."
                ),
                "analysis": (
                    "Better. The metric is specific, the source (rheumatology "
                    "service), the magnitude (12 to 19), the unit (per 100 "
                    "patient-quarters), and the time window (2024 Q2 to 2025 "
                    "Q2) are all present. A reader can verify and weight this "
                    "claim. The remaining gap is the underlying mechanism, "
                    "which the next level supplies."
                ),
            },
            "Level 4: with the mechanism and the certainty stance": {
                "text": (
                    "Across the rheumatology service, the rate of "
                    "moderate-to-severe RA flares rose from 12 to 19 per 100 "
                    "patient-quarters between 2024 Q2 and 2025 Q2, a 60% "
                    "relative increase (p = 0.003). The increase is "
                    "concentrated in patients with biologic dosing intervals "
                    "longer than scheduled, which is the operational signal."
                ),
                "analysis": (
                    "Best. The substantive finding leads, the magnitude is "
                    "expressed two ways (absolute and relative) so different "
                    "audiences can hold it, the certainty stance is "
                    "specific (p = 0.003 named without dominating), and the "
                    "underlying mechanism (extended dosing intervals) "
                    "connects the finding to the eventual recommendation. "
                    "The reader has the substantive content and the "
                    "operational handle."
                ),
            },
        },
        "Implication (what the finding means)": {
            "Level 1: vague": {
                "text": "This means we have a flare problem.",
                "analysis": (
                    "The claim is too high-altitude to be useful. \"A flare "
                    "problem\" does not name the consequence to anyone "
                    "specific. The implication has to be specific to a "
                    "domain (clinical, financial, regulatory) for the "
                    "audience to act on it."
                ),
            },
            "Level 2: vague but clinical": {
                "text": "These flares are clinically important.",
                "analysis": (
                    "\"Clinically important\" is a placeholder term that "
                    "audiences who already believe the writer will accept "
                    "and audiences who do not will discount. The implication "
                    "should name the concrete consequence that produces the "
                    "clinical importance."
                ),
            },
            "Level 3: specific clinical consequence": {
                "text": (
                    "Each flare results in additional clinic visits, "
                    "diagnostic testing, and prednisone exposure, with "
                    "associated cost and adverse-event burden."
                ),
                "analysis": (
                    "Better. The concrete consequences are named: clinic "
                    "visits, diagnostic testing, prednisone exposure, "
                    "adverse events. A reader can see the cost-benefit "
                    "picture. The remaining gap is the quantification of "
                    "the consequence, which is what makes the implication "
                    "land for an executive audience."
                ),
            },
            "Level 4: quantified consequence tied to executive concerns": {
                "text": (
                    "Each moderate-to-severe flare costs the system about "
                    "$4,800 in additional utilization (clinic visits, "
                    "diagnostics, prednisone management). The 60% increase "
                    "implies approximately $480,000 in additional annual "
                    "utilization across the rheumatology cohort, plus the "
                    "patient-experience and adverse-event burden the cost "
                    "figure does not capture."
                ),
                "analysis": (
                    "Best. The implication is quantified for the executive "
                    "audience (a dollar figure), connected to the finding's "
                    "magnitude (the 60% increase), and supplemented with "
                    "the non-quantifiable burden (patient experience and "
                    "adverse events) without being subsumed by it. An "
                    "executive reader has the financial case and the "
                    "non-financial caveat in the same paragraph."
                ),
            },
        },
        "Recommendation (what to do)": {
            "Level 1: not actionable": {
                "text": "We should look into this.",
                "analysis": (
                    "The recommendation does not name an action, an owner, "
                    "a timeframe, or a success criterion. It signals "
                    "concern without producing a decision the audience can "
                    "approve or decline. The default failure mode for the "
                    "recommendation is to be the kind of statement that "
                    "the listener can agree with without changing anything."
                ),
            },
            "Level 2: action without specificity": {
                "text": "The team should consider implementing an alert.",
                "analysis": (
                    "An action is named (implementing an alert) but the "
                    "specifics are absent: which team, what alert, in what "
                    "population, with what success criterion. \"The team "
                    "should consider\" is a particularly common construction "
                    "in clinical-informatics writing that signals "
                    "non-commitment without saying so."
                ),
            },
            "Level 3: specific action and population": {
                "text": (
                    "Build a CDS alert that flags patients on biologics "
                    "with a dosing interval longer than scheduled, before "
                    "their next clinic visit, owned by the rheumatology CDS "
                    "working group."
                ),
                "analysis": (
                    "Better. The action is specific (build a CDS alert), the "
                    "population is specific (biologics, extended dosing "
                    "interval), the workflow timing is specific (before "
                    "their next visit), and the owner is named "
                    "(rheumatology CDS working group). An executive can "
                    "approve this. The remaining gap is the time horizon "
                    "and the success criterion."
                ),
            },
            "Level 4: action, population, timeframe, success criterion": {
                "text": (
                    "Build a CDS alert with the design specified in the "
                    "attached brief; pilot in the rheumatology service for "
                    "6 months starting Q1 2026; owner: rheumatology CDS "
                    "working group, accountable to the CMIO. Success "
                    "criterion: a 30% reduction in moderate-to-severe flares "
                    "in the alert-exposed cohort at the 6-month evaluation, "
                    "with override rate at or below 60%."
                ),
                "analysis": (
                    "Best. Action, population, timeframe, owner, "
                    "accountability, and success criterion are all named. An "
                    "executive can approve or decline based on a specific "
                    "set of expectations. A 6-month evaluation with a "
                    "30%-reduction success criterion and a 60%-override "
                    "ceiling is the kind of recommendation a CMIO can defend "
                    "in a budget discussion or a risk-committee review."
                ),
            },
        },
    }

    return PARTS, mo


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 03: Building a narrative

        Data alone does not persuade. A 30-day in-hospital mortality reduction from 5.7% to 4.5% is a finding; the case for funding the intervention's continued operation is a narrative built from that finding. The default failure mode is to present the finding, expect the audience to draw the implications, and then ask for the action. The audience almost never connects the three steps on its own. This track covers the three-part structure (finding, implication, recommendation) that turns a finding into a recommendation an audience can act on.

        The running example throughout is a rheumatology-flare-monitoring scenario: across the rheumatology service, the rate of moderate-to-severe RA flares has risen, and a CDS alert is the proposed response. The scenario is the cross-reference to the Course 12 capstone, which produced the CDS design brief this kind of narrative would carry.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Three parts of the structure are load-bearing

        Each part is necessary; weak storytelling typically omits the implication and jumps from finding to recommendation, which leaves the listener unable to verify the logic.

        - **Finding.** What the data shows. The craft move is to state it specifically, with the source, the quantification, and the uncertainty, in language the audience can hold.
        - **Implication.** What the finding means for the listener's domain (clinical practice, financial position, regulatory posture). The craft move is to make the implication explicit, because the audience's domain expertise is what allows them to verify the logic but the writer's framing is what aligns the implication with the action being asked for.
        - **Recommendation.** What the audience should do. The craft move is to name the action specifically, time-bind it, and assign it to a person or a body. A recommendation without an owner is a statement of preference; a recommendation without a success criterion is a statement of hope.

        The clinical story is what gives the data its meaning. Ms. Reyes's CRP series across four years is data; the story is the patient with seropositive RA whose disease activity rose, who switched to a biologic, and whose inflammation came under control. The story is what makes the data memorable and actionable; the data alone is rarely persuasive on its own.
        """
    )
    return


@app.cell
def _(PARTS, mo):
    part_pick = mo.ui.dropdown(
        options=list(PARTS.keys()),
        value=list(PARTS.keys())[0],
        label="Part",
    )
    mo.vstack(
        [
            mo.md(
                "## Weak-vs-strong: pick a part, pick a strength level\n\n"
                "**Pick a part of the narrative**, then **pick a strength level** "
                "below. The reactive panel shows the version and the analysis "
                "of what makes it weak or strong."
            ),
            part_pick,
        ]
    )
    return (part_pick,)


@app.cell
def _(PARTS, mo, part_pick):
    _levels = list(PARTS[part_pick.value].keys())
    level_pick = mo.ui.radio(
        options=_levels,
        label="Strength level",
    )
    level_pick
    return (level_pick,)


@app.cell
def _(PARTS, level_pick, mo, part_pick):
    if level_pick.value is None:
        _resp = mo.callout(
            mo.md("_Pick a strength level._"), kind="neutral"
        )
    else:
        _info = PARTS[part_pick.value][level_pick.value]
        _kind = "success" if level_pick.value.startswith("Level 4") else "neutral"
        _body = (
            f"**{level_pick.value}**\n\n"
            f"> {_info['text']}\n\n"
            f"**Analysis:** {_info['analysis']}"
        )
        _resp = mo.callout(mo.md(_body), kind=_kind)
    _resp
    return


@app.cell
def _(PARTS, mo):
    _finding = PARTS["Finding (what the data shows)"]["Level 4: with the mechanism and the certainty stance"]["text"]
    _implication = PARTS["Implication (what the finding means)"]["Level 4: quantified consequence tied to executive concerns"]["text"]
    _recommendation = PARTS["Recommendation (what to do)"]["Level 4: action, population, timeframe, success criterion"]["text"]
    _body = (
        "## The assembled best version\n\n"
        "The three Level-4 parts assembled into a single narrative paragraph. "
        "This is the kind of paragraph that opens a CDS proposal a CMIO can "
        "approve, or a budget memo a CFO can fund.\n\n"
        f"> **Finding.** {_finding}\n\n"
        f"> **Implication.** {_implication}\n\n"
        f"> **Recommendation.** {_recommendation}\n\n"
        "The three sentences together are about 130 words. The audience has "
        "the substantive finding, the financial and clinical implication, and "
        "the specific action with a success criterion. A reader who stops "
        "after the recommendation paragraph can make the decision; everything "
        "that follows in the memo is supporting evidence."
    )
    mo.md(_body)
    return


@app.cell
def _(mo):
    quiz = mo.ui.radio(
        options=[
            "The paragraph omits the finding's source and the quantification of the increase.",
            "The paragraph omits the implication, jumping from finding directly to recommendation.",
            "The paragraph omits the recommendation, leaving the listener with the finding alone.",
            "The paragraph fails to name an owner for the recommended action.",
        ],
        label=(
            "A colleague's draft reads: \"Moderate-to-severe RA flares have "
            "risen 60% in the past year. We should build a CDS alert for "
            "patients on biologics with extended dosing intervals.\" Which "
            "of the four narrative-structure problems below is the load-"
            "bearing failure of this paragraph?"
        ),
    )
    quiz
    return (quiz,)


@app.cell
def _(mo, quiz):
    if quiz.value is None:
        _resp = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif quiz.value.startswith("The paragraph omits the implication"):
        _resp = mo.callout(
            mo.md(
                "**Correct.** The paragraph has a quantified finding (60% "
                "increase) and a specific recommendation (CDS alert for "
                "biologic patients with extended dosing intervals). The gap "
                "is the implication: nothing in the paragraph tells the "
                "audience why a CDS alert is the right response, or what "
                "happens if the response is not built. A reader who agrees "
                "with the finding may still disagree with the recommendation, "
                "because the logic between them is left implicit. The "
                "load-bearing missing piece is the implication."
            ),
            kind="success",
        )
    elif quiz.value.startswith("The paragraph omits the finding's source"):
        _resp = mo.callout(
            mo.md(
                "**The source and quantification are not the load-bearing "
                "failure here.** The paragraph does name the quantification "
                "(60% increase in moderate-to-severe flares), even if it does "
                "not name the source. The structural gap is the missing "
                "implication, which leaves the listener unable to verify the "
                "logic between the finding and the recommendation."
            ),
            kind="warn",
        )
    elif quiz.value.startswith("The paragraph omits the recommendation"):
        _resp = mo.callout(
            mo.md(
                "**The recommendation is present.** \"Build a CDS alert for "
                "patients on biologics with extended dosing intervals\" is the "
                "recommendation. The structural gap is the implication "
                "between the finding (60% increase) and the recommendation "
                "(CDS alert); the listener does not know why the flare rate "
                "matters financially or clinically, and so cannot fully "
                "evaluate the proposal."
            ),
            kind="warn",
        )
    else:
        _resp = mo.callout(
            mo.md(
                "**The owner-and-timeframe gap is real but secondary to the "
                "implication gap.** A reader who agrees with the finding-to-"
                "recommendation logic can ask about the owner; a reader who "
                "does not see the logic will not get that far. The "
                "load-bearing failure in the paragraph as written is the "
                "missing implication."
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

        A narrative carried in prose is one form. Most clinical-informatics communication also carries the finding in a chart, and the chart often does the work of conveying the magnitude and the trajectory that the prose summarizes. Track 04 covers the practice of presenting visuals to non-technical audiences, the small set of annotations that distinguishes a chart-as-evidence from a chart-as-rhetoric, and the discipline of removing every element that does not serve the specific message the chart is being used to make.
        """
    )
    return


if __name__ == "__main__":
    app.run()
