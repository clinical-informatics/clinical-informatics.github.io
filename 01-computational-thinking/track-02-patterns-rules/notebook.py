"""Track 02: Patterns, rules, and edge cases.

A clinical decision rule is a pattern. It works because most patients in
its target population share a phenotype, and a single specification
covers all of them. It fails on the patients who don't, and producing
those failures on purpose is the work of this track.

You'll take the rule from Track 01 and stack candidate changes onto it
one at a time. Each change catches a class of patients you were missing
and misses a class of patients you were catching. The trade is the
lesson.
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
        # Track 02: Patterns, rules, and edge cases

        ## Where we left off.

        You finished Track 01 with a working sepsis rule. The basic specification still says HR > 100 and temp > 38.5°C, but you tightened it with two changes that paid off on the medicine floor census: exclude post-op patients in their first forty-eight hours, and require chart evidence of an infectious source. Alert volume dropped. The false-positive rate dropped harder. The nurses stopped paging you about the rule.

        Two months later, on rounds, one of them pulls you aside.

        > "It's still missing the older folks who go septic without ever mounting a tachycardic response. And yesterday it fired on a guy who'd just had a seizure. Lactate of four, looked terrible. Was post-ictal."

        You did everything right. The rule is still wrong, differently wrong, in ways the Track 01 changes couldn't have anticipated. That is the subject of this track.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A rule is a pattern.

        Every clinical decision rule, score, or alert is a pattern. *"Adult inpatients meeting two SIRS criteria with chart evidence of an infectious source are likely septic."* That one sentence covers thousands of patients with broadly the same phenotype.

        The point is the abstraction. If you had to write a separate rule per patient, you wouldn't have a rule. You'd have a chart. A pattern lets you cover the regular cases with one specification and reserve the irregular ones for clinical judgment. The whole leverage of CDS comes from the abstraction holding.

        The trouble is which patients are which.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Where patterns break.

        Edge cases come from a short list of recurring sources. Keep the list in mind; we'll generate cases against it in the next section.

        1. **Phenotypic mimics.** Different processes producing the same surface signs. Sedative-hypnotic withdrawal, perioperative SIRS, drug fever, atelectasis, FNHTR, postprandial thermogenesis. SIRS-positive vitals from non-infectious causes.
        2. **Suppressed signals.** Pharmacology or chronic physiology muting the signal the rule depends on. Beta-blockade flattening heart rate. Scheduled antipyretics masking fever. Cirrhotic baseline hypothermia. Chronic corticosteroids attenuating the febrile response.
        3. **Off-cohort patients.** The rule is being run on patients it was not validated for. A medicine-cohort rule applied across every floor at the hospital.
        4. **Off-window data.** The signal is real but in the wrong period. The patient was febrile yesterday and has been afebrile for eighteen hours. The rule sees the older reading.
        5. **Missing data.** The rule cannot see what isn't recorded. The absence is frequently informative (no one thought of it), but the rule treats it as silence.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Today's census.

        The medicine floor census from Track 01, expanded with three new admits the day team picked up. The "actual" column is the clinical ground truth: the diagnosis you'd settle on at the end of the workup. The "alert?" column reflects the rule as you left it in Track 01:

        > **Adult medicine inpatient, not post-op within 48 hours, HR > 100 AND temp > 38.5°C, with chart evidence of an infectious source.**

        Read the new admits carefully. Each is in the census to expose a specific kind of pattern break.
        """
    )
    return


@app.cell
def _(pd):
    patients = pd.DataFrame(
        [
            {"patient": "Ortiz, H.",    "age": 78, "service": "Medicine",        "hr": 112, "temp_c": 38.9, "sbp":  96, "lactate": 3.2,  "actual": "Septic (urosepsis, bacteremic)"},
            {"patient": "King, D.",     "age": 34, "service": "Ortho (POD 1)",   "hr": 108, "temp_c": 38.6, "sbp": 128, "lactate": None, "actual": "POD 1 ACL: sympathetic arousal, atelectasis"},
            {"patient": "Park, L.",     "age": 67, "service": "Oncology",        "hr":  94, "temp_c": 37.6, "sbp": 122, "lactate": None, "actual": "Neutropenic on FOLFIRINOX, afebrile"},
            {"patient": "Greer, W.",    "age": 56, "service": "Surgery (POD 2)", "hr": 102, "temp_c": 38.7, "sbp": 118, "lactate": None, "actual": "POD 2 lap chole: atelectatic fever"},
            {"patient": "Choi, D.",     "age": 71, "service": "Medicine",        "hr": 118, "temp_c": 39.1, "sbp":  92, "lactate": 4.1,  "actual": "Septic (CAP)"},
            {"patient": "Hall, M.",     "age": 45, "service": "Medicine",        "hr": 125, "temp_c": 37.9, "sbp": 148, "lactate": 2.8,  "actual": "Alcohol withdrawal (CIWA peaking)"},
            {"patient": "Park, A.",     "age": 60, "service": "Medicine",        "hr": 105, "temp_c": 38.7, "sbp": 124, "lactate": None, "actual": "FNHTR, 30 min after pRBC"},
            {"patient": "Boone, J.",    "age": 88, "service": "Medicine",        "hr":  96, "temp_c": 37.4, "sbp":  88, "lactate": 2.4,  "actual": "Septic (UTI), delirium-only presentation, on metoprolol"},
            {"patient": "Sullivan, B.", "age": 33, "service": "OB (PPD 2)",      "hr": 102, "temp_c": 38.6, "sbp": 118, "lactate": None, "actual": "Lactational engorgement"},
            {"patient": "Nguyen, T.",   "age": 52, "service": "Medicine",        "hr":  88, "temp_c": 37.1, "sbp": 124, "lactate": None, "actual": "CHF exacerbation, diuresed, awaiting discharge"},
            {"patient": "Patel, R.",    "age": 67, "service": "Medicine",        "hr":  99, "temp_c": 38.1, "sbp": 132, "lactate": None, "actual": "Viral URI"},
            {"patient": "Vega, J.",     "age": 41, "service": "Medicine",        "hr": 121, "temp_c": 38.7, "sbp":  90, "lactate": 3.5,  "actual": "Septic (cholangitis, biliary source)"},
            {"patient": "Yamamoto, K.", "age": 73, "service": "Medicine",        "hr": 110, "temp_c": 38.8, "sbp": 102, "lactate": 1.4,  "actual": "Septic (urosepsis, normolactatemic)"},
            {"patient": "Walsh, P.",    "age": 52, "service": "Medicine",        "hr": 104, "temp_c": 38.6, "sbp": 130, "lactate": 4.2,  "actual": "Post-ictal: type B lactic acidosis, no infection"},
            {"patient": "Brown, A.",    "age": 65, "service": "Medicine",        "hr": 102, "temp_c": 38.7, "sbp": 108, "lactate": 1.8,  "actual": "ED admit, evolving picture, cultures not yet drawn"},
        ]
    )
    return (patients,)


@app.cell
def _(mo, patients):
    initial = patients.copy()
    initial["postop"] = initial["service"].str.contains("POD") | initial["service"].str.contains("PPD")
    initial["has_infection_context"] = initial["actual"].str.contains(
        "UTI|pneumonia|cholangitis|URI|CAP|urosepsis|bacteremic|abscess|cellulitis|MRSA",
        regex=True, case=False,
    )
    initial["fires"] = (
        (initial["hr"] > 100)
        & (initial["temp_c"] > 38.5)
        & ~initial["postop"]
        & initial["has_infection_context"]
    )
    initial["alert?"] = initial["fires"].map(lambda x: "FIRES" if x else "")
    display_cols = ["patient", "age", "service", "hr", "temp_c", "sbp", "lactate", "actual", "alert?"]
    mo.ui.table(initial[display_cols], selection=None)
    return display_cols, initial


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Read the census against the five sources.

        - **Boone** is a *suppressed-signal* false negative. UTI driving his delirium, but metoprolol has flattened any chronotropic response and his temperature curve has been ablated by years of atypical aging physiology. HR 96, temp 37.4. The rule's pattern requires he look septic the way younger patients look septic. He doesn't.
        - **Brown** is a *missing-data* false negative. Clinically she's septic (the ED clinician is going to write that on the H&P in another hour), but no cultures have been drawn yet and no infection diagnosis is in the chart. The infection-context check, which saved you from many Track 01 false positives, can't see her workup yet.
        - **Yamamoto** is a *normolactatemic-presentation* true positive that the basic rule still catches. We will revisit her when we add a lactate-based alternative below; not every septic patient mounts a lactic acidosis.
        - **Walsh** would fire the basic vitals rule (HR 104, temp 38.6) but is filtered out correctly by the infection-context check. He is post-ictal with a type B lactic acidosis; nothing about him is infectious. He becomes interesting when we propose loosening the rule.

        Four of fifteen fire the current rule, and all four are truly septic. Tracking how we got there is the whole story of Track 01.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Three candidate changes.

        Three changes are on the table. Each is a real proposal you might see in a CDS design meeting. Toggle any combination; the census re-runs as you change them.

        1. **Lactate alternative** (loosening, OR-branch). Fire even without high fever if lactate > 2 mmol/L AND (HR > 90 OR SBP < 100). The clinical motivation is to catch patients with end-organ stress whose vitals don't meet the basic SIRS phenotype, often because of beta-blockade or autonomic blunting.
        2. **qSOFA-style alternative** (loosening, OR-branch). Fire if any two of {HR > 110, SBP < 100, AMS in the chart}. Sensitive to organ dysfunction in patients who would otherwise miss SIRS-based criteria. Closer to Sepsis-3 thinking than to SIRS.
        3. **Sustained-criteria requirement** (tightening). Suppress firings where the most recent vitals are only borderline above threshold, on the grounds that those are often transient elevations after ambulation, anxiety, or a single artifactual reading. Implemented here by filtering out HR values within 5 bpm of 100 and temperatures within 0.3°C of 38.5.

        After each toggle, watch the catalogue below the census change. Notice which patients move into and out of each bucket. That is the trade.
        """
    )
    return


@app.cell
def _(mo):
    lactate_alt = mo.ui.checkbox(
        value=False,
        label="Lactate alternative: also fire when lactate > 2 AND (HR > 90 OR SBP < 100)",
    )
    qsofa_alt = mo.ui.checkbox(
        value=False,
        label="qSOFA-style alternative: also fire when any 2 of (HR > 110, SBP < 100, AMS)",
    )
    sustained = mo.ui.checkbox(
        value=False,
        label="Sustained criteria: suppress borderline single-snapshot firings",
    )
    mo.vstack([lactate_alt, qsofa_alt, sustained])
    return lactate_alt, qsofa_alt, sustained


@app.cell
def _(display_cols, lactate_alt, mo, patients, qsofa_alt, sustained):
    df = patients.copy()
    df["postop"] = df["service"].str.contains("POD") | df["service"].str.contains("PPD")
    df["has_infection_context"] = df["actual"].str.contains(
        "UTI|pneumonia|cholangitis|URI|CAP|urosepsis|bacteremic|abscess|cellulitis|MRSA",
        regex=True, case=False,
    )
    df["has_ams"] = df["actual"].str.contains("delirium|AMS|altered", regex=True, case=False)

    basic = (df["hr"] > 100) & (df["temp_c"] > 38.5)
    fires = basic

    if lactate_alt.value:
        lac = df["lactate"].fillna(0)
        fires = fires | ((lac > 2) & ((df["hr"] > 90) | (df["sbp"] < 100)))

    if qsofa_alt.value:
        crit_a = df["hr"] > 110
        crit_b = df["sbp"] < 100
        crit_c = df["has_ams"]
        fires = fires | (
            crit_a.astype(int) + crit_b.astype(int) + crit_c.astype(int) >= 2
        )

    if sustained.value:
        borderline = (
            ((df["hr"] > 100) & (df["hr"] <= 105))
            | ((df["temp_c"] > 38.5) & (df["temp_c"] <= 38.8))
        )
        fires = fires & ~borderline

    fires = fires & ~df["postop"] & df["has_infection_context"]
    df["fires"] = fires
    df["alert?"] = df["fires"].map(lambda x: "FIRES" if x else "")

    truly_septic = df["actual"].str.contains("Septic|evolving picture", regex=True, case=False)
    fires_count = int(df["fires"].sum())
    true_pos = int((df["fires"] & truly_septic).sum())
    false_pos = int((df["fires"] & ~truly_septic).sum())
    missed = int((~df["fires"] & truly_septic).sum())

    summary = mo.callout(
        mo.md(
            f"**Current rule fires on {fires_count} of 15.** "
            f"Of those, **{true_pos} truly septic, {false_pos} not.** "
            f"The rule **misses {missed}** truly septic patients on the floor."
        ),
        kind="info",
    )

    mo.vstack(
        [
            mo.ui.table(df[display_cols], selection=None),
            summary,
        ]
    )
    return df, false_pos, fires_count, missed, true_pos, truly_septic


@app.cell
def _(df, mo, truly_septic):
    flagged_correctly = df[df["fires"] & truly_septic][["patient", "age", "actual"]]
    flagged_wrongly = df[df["fires"] & ~truly_septic][["patient", "age", "actual"]]
    missed_silently = df[~df["fires"] & truly_septic][["patient", "age", "actual"]]

    catalogue = mo.vstack(
        [
            mo.md("### The catalogue, as the rule stands."),
            mo.md(
                "Three lists, regenerated each time you toggle a change. These are what a fielded rule's documentation actually looks like."
            ),
            mo.md("**Caught correctly** (true positives):"),
            mo.ui.table(flagged_correctly, selection=None) if len(flagged_correctly) else mo.callout(mo.md("_None right now._"), kind="warn"),
            mo.md("**Wrongly flagged** (false positives, with the phenotypic mimic responsible):"),
            mo.ui.table(flagged_wrongly, selection=None) if len(flagged_wrongly) else mo.callout(mo.md("_None right now._"), kind="success"),
            mo.md("**Missed** (false negatives, with the reason the rule can't see them):"),
            mo.ui.table(missed_silently, selection=None) if len(missed_silently) else mo.callout(mo.md("_None right now._"), kind="success"),
        ]
    )
    catalogue
    return catalogue, flagged_correctly, flagged_wrongly, missed_silently


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What you saw, restated.

        - **Lactate alternative on:** Boone moves from "missed" to "caught." His lactate of 2.4, HR 96, and SBP of 88 trigger the OR-branch. The basic SIRS phenotype could never have caught him; pharmacologic blunting put him outside it. Walsh would fire the lactate branch on numbers alone (lactate 4.2, HR 104), but the infection-context filter you brought forward from Track 01 still excludes him. So far the trade looks free, because the Track 01 tightening is doing real work in the background.
        - **qSOFA-style alternative on:** Boone fires for a different reason now (SBP < 100 + AMS in chart). Yamamoto and other normolactatemic septic patients with HR > 110 and SBP < 100 can also fire. The risk surface this opens up is patients with two-of-three organ-dysfunction criteria who are critically ill but not infected (cardiogenic shock, large PE, hemorrhage). On this census, the infection-context filter is doing the heavy lifting; in a real deployment, you'd want to revisit it.
        - **Sustained criteria on:** Vega and Yamamoto are at risk of being suppressed because their temperatures sit at 38.7 and 38.8, just inside the "borderline" window. The clean intention (don't fire on a single artifactual reading) ends up trading sensitivity for septic patients whose lowest fever happened to be right at the threshold.

        **Brown stays missed under every combination of toggles.** That is the point of having her on the census. The infection-context check, which earned its keep in Track 01, is now a load-bearing source of false negatives for patients whose workup is too early. The cleanest fix for Brown is not another condition. It is a different cohort logic: fire her case differently in the first hour after admission, before the rule has any signal at all to lean on. That is a Track 03 problem.
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
            "Raise the lactate threshold from > 2 to > 4 to filter out the noisier elevations.",
            "Remove the lactate alternative; the false positives aren't worth the catch.",
            "Keep the lactate alternative as-is and accept the new false positives as the cost of catching beta-blocked patients.",
            "Keep the lactate alternative, but require it AND chart evidence of an infectious source before the rule fires.",
        ],
        label=(
            "A month after you turn the lactate alternative on, post-deployment monitoring shows two new patterns. "
            "First, the rule is catching three or four more truly septic patients per week, mostly beta-blocked elderly with urosepsis. Good. "
            "Second, it's also firing on patients with type B lactic acidosis from metformin, post-arrest, and post-ictal states, with otherwise unremarkable vitals. "
            "Which change is the cleanest fix?"
        ),
    )
    quiz
    return (quiz,)


@app.cell
def _(mo, quiz):
    if quiz.value is None:
        quiz_response = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif quiz.value.startswith("Keep the lactate alternative, but require it AND chart evidence"):
        quiz_response = mo.callout(
            mo.md(
                "**Yes.** The lactate alternative is doing real work for the patients it was designed for, and you don't want to lose that. The false positives share a property: none of them have an infectious source in the chart. Tightening the alternative with the same infection-context check you already use on the basic rule preserves the catch for beta-blocked septic patients (who DO have an infectious source) and filters out the type B lactic acidosis crowd (who don't). This is the trade. You accept that you'll still miss a Brown-like patient whose source hasn't been worked up yet, and you document it in the catalogue."
            ),
            kind="success",
        )
    elif quiz.value.startswith("Raise the lactate threshold"):
        quiz_response = mo.callout(
            mo.md(
                "**Partially right but it's the wrong lever.** A higher lactate threshold reduces noise, sure, but post-arrest patients can run lactates of six or seven without infection, and post-ictal patients can hit five. The type B lactic acidosis differentials are not noise; they're real elevations from non-infectious physiology. The lever that actually separates them from septic patients is the infection-context check, not the lactate value."
            ),
            kind="warn",
        )
    elif quiz.value.startswith("Remove the lactate alternative"):
        quiz_response = mo.callout(
            mo.md(
                "**Possible, but you'd be giving up the beta-blocked-elderly catch, which was the whole reason you added the alternative.** This is the 'throw the rule out' default that decomposition was supposed to save you from. The catalogue tells you the alternative is doing real work; the question is how to gate it, not whether to keep it."
            ),
            kind="warn",
        )
    else:
        quiz_response = mo.callout(
            mo.md(
                "**That's the laissez-faire answer, and sometimes it's right.** But you have an obvious, low-cost lever available: the infection-context check that you already use on the basic rule. Applying it to the lactate alternative preserves the catch you care about and filters the false positives by their shared property (non-infectious lactic acidosis). Accept the residual false positives once you've used your cheap levers, not before."
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

        - You named the five recurring sources of edge cases: phenotypic mimics, suppressed signals, off-cohort patients, off-window data, and missing data.
        - You generated specific patients against that list, not by waiting for them to appear in production.
        - You stacked candidate changes onto the rule and watched the catalogue regenerate: what the rule started catching, what it started missing, and which trades you accepted by turning each change on.
        - You finished with a working rule plus a written catalogue of the patients it gets wrong. That is what a fielded rule actually looks like.

        ## What's next.

        **Track 03: Abstraction (what to ignore).** A rule that keeps growing in conditions to handle new edge cases eventually becomes unreadable and impossible to monitor. The next move isn't always to add. Sometimes it's to deliberately leave something out. Abstraction is the third move of computational thinking, and it's the move that lets a rule scale without collapsing under its own weight.
        """
    )
    return


if __name__ == "__main__":
    app.run()
