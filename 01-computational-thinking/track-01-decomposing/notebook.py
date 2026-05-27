"""Track 01: Decomposing a clinical problem.

The first move of computational thinking is one you already make without
naming it: decomposition. You take a tangled problem and break it into
named parts you can examine one at a time.

In this notebook you'll apply decomposition to a sepsis alert that fires
forty times a day. You'll name its parts, run the spec against a real-
feeling census, and finish able to point at the specific piece that
needs to change.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    return mo, pd


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 01: Decomposing a clinical problem

        ## The scenario.

        Tuesday morning on the medicine service. Your inbox holds forty unread sepsis alerts since midnight. You open the first one. POD 1 ACL repair, in for routine pain control, expectedly tachycardic and febrile. You close it. You scroll to the next. Same hospital, different patient, similar story.

        By ten a.m. you've stopped opening them. The alert is doing exactly what it was told to do. So why is it useless?

        That question is the work of this track.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## What's your first move?")
    return


@app.cell
def _(mo):
    first_move = mo.ui.radio(
        options=[
            "Turn the alert off until someone fixes it.",
            "Call IT and tell them the alert is broken.",
            "Look at a handful of alerts and figure out what they have in common.",
            "Ignore the alert. The patients I need to worry about, I'll catch myself.",
        ],
        label="It's the second day of this. What do you do first?",
    )
    first_move
    return (first_move,)


@app.cell
def _(first_move, mo):
    if first_move.value is None:
        response = mo.callout(
            mo.md("_Pick something. There is no wrong answer; the exercise is to notice what you did._"),
            kind="neutral",
        )
    elif first_move.value.startswith("Look at a handful"):
        response = mo.callout(
            mo.md(
                "**Yes.** And notice the move you just made. You took a single object "
                "(\"the alert is broken\") and started splitting it into smaller things "
                "(\"what do these alerts share\"). That move is the whole subject of this "
                "track. We'll come back to it in a moment."
            ),
            kind="success",
        )
    else:
        response = mo.callout(
            mo.md(
                "**Fair.** That's a real option, and on a busy service it might even be the right one "
                "today. But notice what it doesn't do: it doesn't get you closer to fixing the alert. "
                "The move that does is the third option, which is the subject of this track. Take one "
                "big confused thing (\"the alert is broken\") and split it into smaller named things "
                "you can examine. Try clicking that one to see where it leads."
            ),
            kind="warn",
        )
    response
    return (response,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The move has a name.

        Splitting a tangled problem into named parts you can examine one at a time is called **decomposition**. It's the first move of computational thinking.

        You use it constantly. When a patient tells you they "haven't been feeling well," you don't take that in as a single object. You decompose: pain or not, where, character, onset, evolution. Each piece has its own answer, and the decomposition is what lets the encounter go anywhere.

        The same move works on a misbehaving alert. "The sepsis alert is broken" is a problem nobody can fix. "The cohort definition includes post-op patients in their first forty-eight hours, who reliably present with sympathetic arousal and atelectatic fevers, and the rule fires on them" is a problem someone can fix.

        Now let's apply it.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The alert spec.

        The actual specification, in plain English:

        > *Among all adult inpatients, fire an alert when the patient's most recent heart rate is above 100 beats per minute **and** the most recent temperature is above 38.5°C.*

        Read it twice. Then we'll take it apart.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## What are the parts?")
    return


@app.cell
def _(mo):
    parts_selector = mo.ui.multiselect(
        options=[
            "The kind of patient the rule looks at (the cohort)",
            "The data points the rule checks (the signals)",
            "The cutoffs above which a signal counts (the thresholds)",
            "The time window the data has to come from",
            "The system the data is pulled from (lab, flowsheet, order entry, vendor score)",
            "The moment the alert actually fires (continuously, every 15 minutes, on chart open)",
            "The name of the hospital",
            "The day of the week",
        ],
        label="Which of these are real parts of the alert spec above? Pick all that apply.",
    )
    parts_selector
    return (parts_selector,)


@app.cell
def _(mo, parts_selector):
    chosen = set(parts_selector.value or [])
    correct = {
        "The kind of patient the rule looks at (the cohort)",
        "The data points the rule checks (the signals)",
        "The cutoffs above which a signal counts (the thresholds)",
        "The time window the data has to come from",
        "The system the data is pulled from (lab, flowsheet, order entry, vendor score)",
        "The moment the alert actually fires (continuously, every 15 minutes, on chart open)",
    }
    if not chosen:
        parts_response = mo.callout(
            mo.md("_Pick at least one. You can change your mind after seeing the answer._"),
            kind="neutral",
        )
    elif chosen == correct:
        parts_response = mo.callout(
            mo.md(
                "**That's all six.** These six parts cover most clinical decision rules you'll meet. "
                "Some rules are smaller (a Wells score for pulmonary embolism is cohort, signals, and "
                "thresholds, and nothing else). Some are bigger. But this is the working list, and we'll "
                "treat it as the canonical decomposition for the rest of the curriculum."
            ),
            kind="success",
        )
    else:
        parts_response = mo.callout(
            mo.md(
                "**Close.** Six of the eight options above are real parts of any clinical decision rule. "
                "The other two (the hospital's name and the day of the week) are not parts of the **spec**. "
                "They might affect the rule's behavior in practice, but they're not what the rule itself "
                "checks. The six real parts:\n\n"
                "1. The **cohort** (which patients the rule runs on)\n"
                "2. The **signals** (which data points it checks)\n"
                "3. The **thresholds** (what value of each signal counts)\n"
                "4. The **time window** (over what period the signals have to be satisfied)\n"
                "5. The **data source** (where each signal comes from)\n"
                "6. The **trigger moment** (when the rule actually fires)\n"
            ),
            kind="warn",
        )
    parts_response
    return chosen, correct, parts_response


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Run the rule against real-feeling data.

        The medicine floor census this morning. Twelve patients. Each row shows the most recent heart rate, the most recent temperature, the service, and the clinical ground truth you'd settle on at the end of the workup. The right-most column shows whether the rule from the spec above (HR > 100 AND temp > 38.5°C) is currently firing.
        """
    )
    return


@app.cell
def _(pd):
    patients = pd.DataFrame(
        [
            {"patient": "Ortiz, H.",    "age": 78, "service": "Medicine",        "hr": 112, "temp_c": 38.9, "actual": "Septic (urosepsis, bacteremic)"},
            {"patient": "King, D.",     "age": 34, "service": "Ortho (POD 1)",   "hr": 108, "temp_c": 38.6, "actual": "POD 1 ACL: sympathetic arousal, atelectasis"},
            {"patient": "Park, L.",     "age": 67, "service": "Oncology",        "hr":  94, "temp_c": 37.6, "actual": "Neutropenic on FOLFIRINOX, afebrile"},
            {"patient": "Greer, W.",    "age": 56, "service": "Surgery (POD 2)", "hr": 102, "temp_c": 38.7, "actual": "POD 2 lap chole: atelectatic fever"},
            {"patient": "Choi, D.",     "age": 71, "service": "Medicine",        "hr": 118, "temp_c": 39.1, "actual": "Septic (CAP)"},
            {"patient": "Hall, M.",     "age": 45, "service": "Medicine",        "hr": 125, "temp_c": 37.9, "actual": "Alcohol withdrawal (CIWA peaking)"},
            {"patient": "Park, A.",     "age": 60, "service": "Medicine",        "hr": 105, "temp_c": 38.7, "actual": "FNHTR, 30 min after pRBC"},
            {"patient": "Boone, J.",    "age": 88, "service": "Medicine",        "hr":  96, "temp_c": 37.4, "actual": "Septic (UTI), delirium-only presentation, on metoprolol"},
            {"patient": "Sullivan, B.", "age": 33, "service": "OB (PPD 2)",      "hr": 102, "temp_c": 38.6, "actual": "Lactational engorgement"},
            {"patient": "Nguyen, T.",   "age": 52, "service": "Medicine",        "hr":  88, "temp_c": 37.1, "actual": "CHF exacerbation, diuresed, awaiting discharge"},
            {"patient": "Patel, R.",    "age": 67, "service": "Medicine",        "hr":  99, "temp_c": 38.1, "actual": "Viral URI"},
            {"patient": "Vega, J.",     "age": 41, "service": "Medicine",        "hr": 121, "temp_c": 38.7, "actual": "Septic (cholangitis, biliary source)"},
        ]
    )
    return (patients,)


@app.cell
def _(mo, patients):
    initial = patients.copy()
    initial["alert?"] = ((initial["hr"] > 100) & (initial["temp_c"] > 38.5)).map(
        lambda x: "FIRES" if x else ""
    )
    display_cols = ["patient", "age", "service", "hr", "temp_c", "actual", "alert?"]
    mo.ui.table(initial[display_cols], selection=None)
    return display_cols, initial


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Read that closely.

        The rule fires on seven of the twelve patients on this floor. **Three** are truly septic. The other four are SIRS-positive for entirely non-infectious reasons: POD 1 sympathetic arousal, POD 2 atelectatic fever, FNHTR thirty minutes after a unit of pRBCs, and lactational engorgement.

        And a quieter problem. **Boone**, 88, septic from a UTI now presenting as delirium, doesn't fire the rule at all. HR 96 because he's on metoprolol and his chronotropic response is flat. The rule asked about an absolute HR threshold, not whether he had any reserve to draw on.

        Scale this across an inpatient census in real time and you have your inbox. **The rule is doing exactly what it was told.** The specification is the problem.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Where is the problem?

        Decomposition lets you point at the part that needs to change instead of throwing out the whole thing. Try the four adjustments below and watch the count shift. The table re-runs as soon as you move anything.
        """
    )
    return


@app.cell
def _(mo):
    hr_threshold = mo.ui.slider(
        start=80, stop=140, step=1, value=100,
        label="HR threshold (a value above this counts)",
        show_value=True,
    )
    temp_threshold = mo.ui.slider(
        start=37.0, stop=40.0, step=0.1, value=38.5,
        label="Temperature threshold in °C (a value above this counts)",
        show_value=True,
    )
    exclude_postop = mo.ui.checkbox(
        value=False,
        label="Exclude post-op patients in the first 48 hours",
    )
    require_infection_context = mo.ui.checkbox(
        value=False,
        label="Require an infection-related diagnosis or pending culture in the chart",
    )
    controls = mo.vstack([hr_threshold, temp_threshold, exclude_postop, require_infection_context])
    controls
    return controls, exclude_postop, hr_threshold, require_infection_context, temp_threshold


@app.cell
def _(
    display_cols,
    exclude_postop,
    hr_threshold,
    mo,
    patients,
    require_infection_context,
    temp_threshold,
):
    df = patients.copy()
    df["postop"] = df["service"].str.contains("POD") | df["service"].str.contains("PPD")
    df["has_infection_context"] = df["actual"].str.contains(
        "UTI|pneumonia|cholangitis|URI|CAP|urosepsis|bacteremic|abscess|cellulitis|MRSA",
        regex=True, case=False,
    )
    df["meets_vitals"] = (df["hr"] > hr_threshold.value) & (df["temp_c"] > temp_threshold.value)
    df["fires"] = df["meets_vitals"]
    if exclude_postop.value:
        df["fires"] = df["fires"] & ~df["postop"]
    if require_infection_context.value:
        df["fires"] = df["fires"] & df["has_infection_context"]
    df["alert?"] = df["fires"].map(lambda x: "FIRES" if x else "")

    truly_septic = df["actual"].str.contains("Septic", regex=True, case=False)
    fires_count = int(df["fires"].sum())
    true_pos = int((df["fires"] & truly_septic).sum())
    false_pos = int((df["fires"] & ~truly_septic).sum())
    missed = int((~df["fires"] & truly_septic).sum())

    if fires_count == 0:
        summary_md = (
            "**With these settings, the rule fires on nobody on this floor.** "
            f"It also misses **{missed}** of the four truly septic patients. "
            "You've achieved perfect specificity at the cost of any utility. Loosen something."
        )
    else:
        summary_md = (
            f"**Current settings: the rule fires on {fires_count} of the 12 patients on the census.** "
            f"Of those, **{true_pos}** are truly septic and **{false_pos}** are not. "
            f"The rule also **misses {missed}** of the four truly septic patients on the floor."
        )

    reactive_block = mo.vstack(
        [
            mo.ui.table(df[display_cols], selection=None),
            mo.callout(
                mo.md(summary_md + "\n\nChange one slider or checkbox at a time. Notice which part actually moves the numbers."),
                kind="info",
            ),
        ]
    )
    reactive_block
    return (
        df,
        false_pos,
        fires_count,
        missed,
        reactive_block,
        summary_md,
        true_pos,
        truly_septic,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What you probably noticed.

        - **Moving the HR or temperature threshold** trades one error class for another. Tighten them and you start missing real sepsis. Loosen them and you're back where you started. Threshold work matters but cannot fix a rule that's looking at the wrong things.
        - **Excluding post-op patients in their first 48 hours** drops the POD 1 ACL, the POD 2 lap chole, and the PPD 2 OB patient. Three false positives gone, no true positives lost on this census. A clean cohort win.
        - **Requiring infection-related diagnosis or pending culture** is a signal change. The rule now demands chart context, not just vital signs. It's the largest single drop in false positives you can make from here.

        Different parts of the rule carry different leverage. A small change in the right part is worth more than a large change in the wrong one. That is the payoff of decomposition: it tells you which lever to pull.
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
            "The threshold for HR is too high; we're missing real sepsis.",
            "The cohort is too broad; the rule shouldn't run on post-op patients in their first day.",
            "The time window is wrong; the rule is looking at the wrong period.",
            "The signals are insufficient; the rule needs more than HR and temperature.",
        ],
        label=(
            "Two months later, on rounds, a nurse pulls you aside: "
            "'It still fires every morning on my ortho post-ops, and we're still missing the older folks who go septic without ever mounting a tachycardic response.' "
            "Which single part of the rule is the bigger problem for her **ortho post-ops firing every morning** complaint?"
        ),
    )
    quiz
    return (quiz,)


@app.cell
def _(mo, quiz):
    if quiz.value is None:
        quiz_response = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif quiz.value.startswith("The cohort"):
        quiz_response = mo.callout(
            mo.md(
                "**Yes.** The *ortho post-ops every morning* complaint is a cohort problem. The rule is being asked to make a judgment about patients it should not be examining in the first place. "
                "Her *missing the older folks* complaint is a different problem with a different lever. That one is a signal problem (the rule is not asking about the right things for those patients) and we'll come back to it in Track 02."
            ),
            kind="success",
        )
    elif quiz.value.startswith("The threshold"):
        quiz_response = mo.callout(
            mo.md(
                "**Not for that complaint.** Threshold changes might help with the missed cases (the older folks who never mount a tachycardia), but for the post-op patients firing every morning, the rule is doing what it was told. You don't want a different threshold there. You want the rule not to be looking at those patients at all. That is a cohort question."
            ),
            kind="warn",
        )
    elif quiz.value.startswith("The time"):
        quiz_response = mo.callout(
            mo.md(
                "**Not quite.** Time windows do matter (a rule looking at vitals from three days ago will fire on patients who have long since stabilized), but the ortho-post-ops-every-morning pattern is about *who* the rule is looking at, not *when*. The orthopedic patient on POD 1 has tachycardia that is real and current; it just isn't from sepsis. That is a cohort problem."
            ),
            kind="warn",
        )
    else:
        quiz_response = mo.callout(
            mo.md(
                "**That's the right answer for the second half of her complaint, not the first.** Adding signals (chart context, lactate, infection-related orders) is what catches the older folks. But for *ortho post-ops firing every morning*, the cleanest fix is to narrow who the rule examines: those patients should not trigger the rule in their first day regardless of their vitals. Cohort, not signals."
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

        - Took a single confused thing ("the alert is broken") and split it into six named parts.
        - Ran the rule against a real-feeling census and located where the false positives and false negatives live.
        - Moved one part of the rule at a time and noticed which parts carry leverage and which don't.

        That sequence (split into named parts, change one part at a time, watch what shifts) is decomposition. The rest of this course is variations on it.

        ## What's next.

        **Track 02: Patterns, rules, and edge cases.** Every clinical rule is a pattern, and every pattern has edge cases. Track 02 takes the rule you finish this notebook with, stacks candidate changes onto it, and watches the catalogue of edge cases regenerate. Track 02 closes with a working rule plus a written catalogue of the patients it gets wrong. That is what a fielded rule actually looks like.
        """
    )
    return


if __name__ == "__main__":
    app.run()
