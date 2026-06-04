"""Track 04: Presenting visuals to non-technical audiences.

No visible code. The notebook presents Ms. Reyes's CRP series across four
years, lets the reader pick an audience, and re-renders the same chart
with the annotations appropriate to that audience. Cross-references
Course 08 visualization principles applied to communication. Closes with
a quiz on annotation choice.

WASM-safe: no shared imports, no data files, no relative paths. Uses
altair (Pyodide-included) for chart rendering.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import pandas as pd

    import marimo as mo

    REYES_CRP = pd.DataFrame(
        [
            {"date": "2022-02-14", "crp": 42.1},
            {"date": "2022-05-22", "crp": 28.4},
            {"date": "2022-08-18", "crp": 19.2},
            {"date": "2022-11-09", "crp": 16.8},
            {"date": "2023-02-15", "crp": 22.5},
            {"date": "2023-05-23", "crp": 31.6},
            {"date": "2023-08-21", "crp": 26.9},
            {"date": "2023-11-13", "crp": 33.4},
            {"date": "2024-01-08", "crp": 36.2},
            {"date": "2024-04-17", "crp": 18.7},
            {"date": "2024-07-22", "crp": 14.1},
            {"date": "2024-10-30", "crp": 11.4},
            {"date": "2025-02-04", "crp": 13.8},
            {"date": "2025-05-12", "crp": 16.5},
            {"date": "2025-08-19", "crp": 14.9},
            {"date": "2025-11-21", "crp": 18.2},
            {"date": "2026-02-10", "crp": 21.4},
            {"date": "2026-04-28", "crp": 19.8},
        ]
    )
    REYES_CRP["date"] = pd.to_datetime(REYES_CRP["date"])

    MEDICATIONS = pd.DataFrame(
        [
            {"date": "2022-03-15", "label": "MTX started"},
            {"date": "2024-02-10", "label": "Adalimumab added"},
        ]
    )
    MEDICATIONS["date"] = pd.to_datetime(MEDICATIONS["date"])

    def build_chart(audience, df, meds):
        base = (
            alt.Chart(df)
            .mark_line(color="steelblue", point=True)
            .encode(
                x=alt.X("date:T", title="Date"),
                y=alt.Y("crp:Q", title="CRP (mg/L)", scale=alt.Scale(domain=[0, 50])),
            )
        )

        if audience.startswith("Technical"):
            return base.properties(width=600, height=300, title="CRP across the observation window")

        ref_band = (
            alt.Chart(pd.DataFrame({"low": [0], "high": [5]}))
            .mark_rect(opacity=0.18, color="seagreen")
            .encode(y="low:Q", y2="high:Q")
        )

        if audience.startswith("Clinical"):
            med_rules = (
                alt.Chart(meds)
                .mark_rule(color="firebrick", strokeDash=[4, 4])
                .encode(x="date:T")
            )
            med_text = (
                alt.Chart(meds)
                .mark_text(align="left", dx=5, dy=-180, color="firebrick", fontSize=11)
                .encode(x="date:T", text="label:N")
            )
            return (ref_band + base + med_rules + med_text).properties(
                width=600, height=300,
                title="CRP across treatment: reference range and medication changes annotated"
            )

        if audience.startswith("Executive"):
            highlight = (
                alt.Chart(pd.DataFrame({"start": ["2024-02-10"], "end": ["2026-04-28"]}))
                .transform_calculate(start="toDate(datum.start)", end="toDate(datum.end)")
                .mark_rect(opacity=0.12, color="goldenrod")
                .encode(x="start:T", x2="end:T")
            )
            headline = (
                alt.Chart(pd.DataFrame({"date": ["2024-08-01"], "y": [45], "text": ["CRP fell from peak 36 mg/L to 11 mg/L after biologic"]}))
                .transform_calculate(date="toDate(datum.date)")
                .mark_text(align="center", color="goldenrod", fontSize=12, fontWeight="bold")
                .encode(x="date:T", y="y:Q", text="text:N")
            )
            med_rules = (
                alt.Chart(meds)
                .mark_rule(color="firebrick", strokeDash=[4, 4])
                .encode(x="date:T")
            )
            return (ref_band + highlight + base + med_rules + headline).properties(
                width=600, height=300,
                title="Disease activity (CRP) before and after biologic added"
            )

        simple_meds = (
            alt.Chart(meds)
            .mark_rule(color="firebrick", strokeDash=[4, 4])
            .encode(x="date:T")
        )
        return (ref_band + base + simple_meds).properties(
            width=600, height=300,
            title="Your inflammation marker over time"
        )

    return MEDICATIONS, REYES_CRP, alt, build_chart, mo, pd


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 04: Presenting visuals to non-technical audiences

        A trajectory chart that an analyst reads instantly often goes unread by a non-technical audience presented with it for the first time. The audience does not know what they are looking at; the chart does not say. This track covers the practice of presenting a chart to an audience that has not seen one like it before, the small set of annotations that distinguishes a chart-as-evidence from a chart-as-rhetoric, and the discipline of removing every element that does not serve the specific message the chart is being used to make.

        The running example is Ms. Reyes's CRP series across four years (the running clinical case across the curriculum). The same data series is the basis of the chart for each audience; what changes is the annotation, the framing, and the rhetorical work the chart does.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Three properties of chart presentation

        Three properties are load-bearing for chart presentation to non-technical audiences.

        - **The chart must answer a stated question.** The presenter names the question the chart is going to answer (a single sentence) before the chart is shown; the audience reads the chart to verify the answer. The default failure mode is to show the chart and let the audience guess what question it is answering.
        - **The annotation must serve the question.** The reference range, the medication change, the highlight band, the value-at-a-point are added when they help the audience verify the answer; the legend, the gridlines, and the secondary axes are removed when they do not. Annotations that repeat what the chart already shows are deleted.
        - **The chart has one message.** A chart presented to a non-technical audience is a chart-as-rhetoric (a chart in service of a specific claim); the analyst's instinct to present "the data" and let the audience interpret is the default failure mode, because the audience does not have the analyst's framing.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Chart-as-evidence vs chart-as-rhetoric

        The same chart can serve two purposes.

        **Chart-as-evidence** presents the data and lets the reader draw the conclusion. The reader is expected to have the analytic vocabulary and the time to read the chart carefully. The academic-paper figure is the prototype: a small number of axes, no opinionated annotation, the legend on the side, the caption naming the data without naming the conclusion.

        **Chart-as-rhetoric** presents the data in service of a specific argument. The reader is not expected to do the analytic work; the chart is doing it. The executive-deck figure is the prototype: a single message conveyed by the chart's title, the annotation, and the highlight; everything that does not serve the message is removed.

        Both are legitimate. The communication-craft skill is to know which you are producing and to be honest about it. The same data series, rendered as evidence for an academic audience and as rhetoric for an executive audience, can be the same chart with different annotations; it can also be a different chart entirely.
        """
    )
    return


@app.cell
def _(mo):
    audience_pick = mo.ui.dropdown(
        options=[
            "Technical (engineers, data scientists, analysts)",
            "Clinical (clinicians, nurses, pharmacists)",
            "Executive (CMIO, CMO, CIO, CFO)",
            "Patient (patients and family members)",
        ],
        value="Technical (engineers, data scientists, analysts)",
        label="Audience for the chart",
    )
    audience_pick
    return (audience_pick,)


@app.cell
def _(MEDICATIONS, REYES_CRP, audience_pick, build_chart, mo):
    _chart = build_chart(audience_pick.value, REYES_CRP, MEDICATIONS)
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(audience_pick, mo):
    if audience_pick.value.startswith("Technical"):
        _body = (
            "**Technical rendering.** Minimal annotation. The data series is "
            "the substantive content; the technical reader has the vocabulary "
            "(CRP, the reference range, the typical RA trajectory) and the "
            "training to read the chart without rhetorical scaffolding. The "
            "title names the data ('CRP across the observation window') "
            "without naming the conclusion."
        )
    elif audience_pick.value.startswith("Clinical"):
        _body = (
            "**Clinical rendering.** The reference range (0 to 5 mg/L) is "
            "shown as a band so the clinician can see at a glance how far "
            "above normal each draw sits. The two medication-change events "
            "(methotrexate started, adalimumab added) are vertical rules with "
            "labels, so the clinician can connect the trajectory to the "
            "treatment history. The title now names the question ('CRP across "
            "treatment'), which is the question the clinical audience is "
            "implicitly asking when they read the chart."
        )
    elif audience_pick.value.startswith("Executive"):
        _body = (
            "**Executive rendering.** Same data, but the chart now does "
            "rhetorical work. The post-biologic window is highlighted as a "
            "background band, drawing the eye to the period the chart is "
            "arguing about. The headline annotation ('CRP fell from peak 36 "
            "mg/L to 11 mg/L after biologic') states the conclusion of the "
            "chart in language the executive can hold. The title names the "
            "question and the answer ('Disease activity before and after "
            "biologic'). An executive who reads only the title and the "
            "headline annotation has the substantive content; the chart is "
            "the supporting evidence."
        )
    else:
        _body = (
            "**Patient rendering.** The clinical vocabulary is removed from "
            "the title ('Your inflammation marker over time') without "
            "removing the substantive content (CRP is the marker; the trend "
            "is the message). The reference range is shown as the same "
            "band; the medication changes are shown as the same rules but "
            "without the labels (a patient can be told verbally what they "
            "are without the chart's space being given to text). The "
            "minimum-element chart respects the patient's attention without "
            "patronizing their intelligence."
        )
    mo.callout(mo.md(_body), kind="info")
    return


@app.cell
def _(mo):
    quiz = mo.ui.radio(
        options=[
            "Annotate every visit's exact CRP value with a small number above each point.",
            "Add the headline annotation \"CRP fell from peak 36 mg/L to 11 mg/L after biologic\" and shade the post-biologic window.",
            "Add a logarithmic-scale toggle and a polynomial regression line.",
            "Replace the line chart with a stacked bar chart of CRP by quarter.",
        ],
        label=(
            "You have 90 seconds in an executive briefing to show one chart "
            "of Ms. Reyes's CRP trajectory and make the case for funding "
            "continued biologic therapy. Which annotation choice serves the "
            "executive audience best?"
        ),
    )
    quiz
    return (quiz,)


@app.cell
def _(mo, quiz):
    if quiz.value is None:
        _resp = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif quiz.value.startswith("Add the headline annotation"):
        _resp = mo.callout(
            mo.md(
                "**Correct.** The executive audience needs the chart to "
                "convey the conclusion in 90 seconds. The headline annotation "
                "names the substantive message (the absolute reduction in CRP "
                "after biologic) and the highlight band draws the eye to the "
                "relevant window. The executive does not need every visit's "
                "value (they cannot act on that level of detail), and does "
                "not need a log scale or a regression line (those are "
                "technical-altitude annotations). The chart is now "
                "chart-as-rhetoric: it argues the case the briefing exists "
                "to make."
            ),
            kind="success",
        )
    elif quiz.value.startswith("Annotate every visit's exact CRP value"):
        _resp = mo.callout(
            mo.md(
                "**This is the technical-altitude annotation.** Per-point "
                "exact values let an analyst read the chart precisely, which "
                "is the wrong altitude for an executive audience that has 90 "
                "seconds and wants the message. Cluttering the chart with "
                "values the audience cannot act on makes the substantive "
                "message harder to find."
            ),
            kind="warn",
        )
    elif quiz.value.startswith("Add a logarithmic-scale toggle"):
        _resp = mo.callout(
            mo.md(
                "**The log scale and the regression line are technical "
                "moves.** They serve an analyst reading the chart as evidence; "
                "they do not serve an executive reading the chart for a "
                "decision. The executive audience needs the chart to argue "
                "the case; technical statistical apparatus distracts from "
                "the argument."
            ),
            kind="warn",
        )
    else:
        _resp = mo.callout(
            mo.md(
                "**A stacked bar chart of CRP by quarter is the wrong "
                "chart.** CRP is a continuous longitudinal variable; the line "
                "chart preserves the trajectory and the relationship to the "
                "medication-change event. A stacked bar by quarter buries "
                "both. The chart-type choice is the more important decision; "
                "an annotation cannot rescue a chart whose form does not "
                "match the data."
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

        Audience-shaped writing and audience-shaped visuals are the two surfaces of communication craft within the analyst's own work. The final track of this course addresses a different communication problem: the analyst as a participant in a meeting with an AI team or a vendor, where the questions the clinician asks are themselves the work. Track 05 covers the questions that surface what the vendor would prefer not to show, and the principle that the clinician's authority in the room comes from clinical expertise, not from technical deference.
        """
    )
    return


if __name__ == "__main__":
    app.run()
