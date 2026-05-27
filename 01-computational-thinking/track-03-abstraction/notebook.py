"""Track 03: Abstraction (what to ignore).

Decomposition (Track 01) takes a rule apart. Patterns and edge cases
(Track 02) put it back together while watching the trades. Abstraction
is the third move: the discipline of choosing what to leave out.

This notebook works through a 30-day readmission risk model. You read a
catalogue of candidate features, pick the ones that go in, and watch a
deployment memo regenerate live with the equity, leakage, and
missingness consequences of your choices.
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
        # Track 03: Abstraction (what to ignore)

        ## The scenario.

        Your CMO has pulled you into a meeting. The data team is building a 30-day readmission risk score for case management to pilot in six weeks. The data warehouse can give you anything in the chart. The first cut from the data scientist has eight hundred candidate features. He is pleased with the AUC.

        Among the eight hundred: self-reported race, the census-tract Area Deprivation Index, the patient's relationship status as captured by social-work intake, whether a discharge prescription was filled at an in-network pharmacy in the seventy-two hours after discharge, and a dozen flowsheet fields that are missing more than half the time. The data scientist says the more features the better. The CMO wants your clinical input by Friday.

        Your job at this meeting is to decide what stays in the model and what gets dropped. **That decision is the move.**
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The naive instinct.

        The first impulse, especially if you trust the data scientist, is to leave the eight hundred features in. They came out of a chart; somebody put them there for a reason; the model's AUC is up; let the algorithm decide what matters.

        That instinct is wrong, and the reasons are the subject of this track. The short version, before we make it concrete:

        1. **The bigger the model, the harder it is to audit.** When the model fails in production, and it will, someone has to figure out which feature drifted. Eight hundred features means eight hundred potential failure modes. No human holds that in their head.
        2. **The bigger the model, the harder it is to explain.** Case management is being asked to act on this score. They will not act on a score they don't understand. "It uses eight hundred features, but trust us" is the answer that gets your model quietly ignored on the floor.
        3. **The bigger the model, the bigger the equity surface.** Every demographic or social feature is a potential pathway for the model to operationalize a structural inequity. The more there are, the less likely anyone is to notice when one of them is doing the wrong thing.
        4. **The bigger the model, the more fragile to data quality.** Every feature is a dependency on a data source. EHR upgrades, vendor migrations, flowsheet redesigns: any of them can quietly degrade a feature your model is leaning on. With eight hundred features, you can't tell when something has shifted.

        The discipline is not to include everything. The discipline is to choose deliberately which small set of features the model actually needs, and to document why each one is in or out.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The move has a name.

        Choosing what to leave out is **abstraction**. It is the third move of computational thinking and the move that makes a clinical model deployable.

        - Decomposition (Track 01) asks: *what are the parts of this thing?*
        - Abstraction asks: *which parts can I throw away?*

        The two work together. You decompose to make the parts visible. You abstract to make them few enough to manage. A model that has been decomposed without being abstracted is exhaustive but unusable. A model that has been abstracted without being decomposed first is parsimonious by accident.

        Every feature you include is a debt: data quality, drift, monitoring, explanation, equity surveillance. Every feature you exclude is a bet: that the model will work without it. Make both calls deliberately.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Five categories of features to consider dropping.

        Each has a separate reason. Knowing which category a feature falls into is most of the work of deciding.

        1. **Leaky features.** Data points that include information available only after the outcome. The classic 30-day readmission example is the patient's 7-day follow-up attendance: that fact lives inside the time window the model is supposed to predict, and its predictive power is largely an artifact. Leaky features inflate offline metrics and quietly fail in deployment. Leakage is a bug.
        2. **Equity-flagged features.** Race, ZIP code, insurance class, ADI, primary language. They carry signal because they proxy for structural inequity. Including them without explicit justification means the model encodes that inequity. Including them with justification ("we use ADI as an SDOH proxy because the deployment goal is to direct social-work resources, not to ration clinical attention") is sometimes appropriate. The default to avoid is including them because the AUC went up.
        3. **High-missingness features.** A feature missing more than forty or fifty percent of the time is effectively absent in deployment. The model is running on the imputation strategy, not the captured signal.
        4. **Redundant features.** Two features that capture the same underlying signal don't both belong. Pick one. The duplicate is debt without payoff.
        5. **Cosmetic features.** Features that look predictive in isolation but contribute nothing once the right features are in. They add audit obligation and monitoring burden without buying performance.

        Now let's apply this to a real-feeling feature list.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The candidate features.

        Sixteen candidates have made it through a first cut. Each row tells you the feature, its category, the predictive signal it carries (qualitative, since you don't have an evaluation set in front of you), and the flags it has earned in the catalogue.

        - **eq** means equity-flagged. The feature is correlated with structural inequity and including it requires explicit written justification.
        - **leak** means leakage. The data point is not reliably available at scoring time, and its offline performance is partly an artifact.
        - **missing %** is the proportion of the development cohort where the feature is unrecorded.

        Read the catalogue before you start picking.
        """
    )
    return


@app.cell
def _(pd):
    features = pd.DataFrame(
        [
            {"feature": "Age at admission",                                       "category": "Core clinical",     "predictive": "strong",   "equity": "",   "leakage": "",     "missing_pct": 0},
            {"feature": "Sex",                                                    "category": "Core clinical",     "predictive": "moderate", "equity": "",   "leakage": "",     "missing_pct": 0},
            {"feature": "Self-reported race",                                     "category": "Demographic",       "predictive": "moderate", "equity": "eq", "leakage": "",     "missing_pct": 3},
            {"feature": "Insurance class (Medicaid/Medicare/private/uninsured)",  "category": "Demographic",       "predictive": "moderate", "equity": "eq", "leakage": "",     "missing_pct": 1},
            {"feature": "Prior 6-month admissions",                               "category": "Utilization",       "predictive": "strong",   "equity": "",   "leakage": "",     "missing_pct": 0},
            {"feature": "Prior 6-month ED visits",                                "category": "Utilization",       "predictive": "strong",   "equity": "",   "leakage": "",     "missing_pct": 0},
            {"feature": "Charlson comorbidity index",                             "category": "Comorbidity",       "predictive": "strong",   "equity": "",   "leakage": "",     "missing_pct": 0},
            {"feature": "Active CHF diagnosis",                                   "category": "Comorbidity",       "predictive": "moderate", "equity": "",   "leakage": "",     "missing_pct": 0},
            {"feature": "Current LOS (index admission)",                          "category": "Index admission",   "predictive": "strong",   "equity": "",   "leakage": "",     "missing_pct": 0},
            {"feature": "ICU stay during current admission",                      "category": "Index admission",   "predictive": "moderate", "equity": "",   "leakage": "",     "missing_pct": 0},
            {"feature": "Discharge against medical advice",                       "category": "Index admission",   "predictive": "moderate", "equity": "",   "leakage": "",     "missing_pct": 0},
            {"feature": "Discharge disposition (home / SNF / rehab)",             "category": "Index admission",   "predictive": "moderate", "equity": "",   "leakage": "",     "missing_pct": 0},
            {"feature": "Functional status (Katz/Barthel) at discharge",          "category": "Social/functional", "predictive": "strong",   "equity": "",   "leakage": "",     "missing_pct": 60},
            {"feature": "Housing instability flag",                               "category": "Social/functional", "predictive": "moderate", "equity": "eq", "leakage": "",     "missing_pct": 70},
            {"feature": "Attended 7-day post-discharge follow-up",                "category": "Post-discharge",    "predictive": "strong",   "equity": "",   "leakage": "leak", "missing_pct": 12},
            {"feature": "Filled discharge Rx within 72 hours",                    "category": "Post-discharge",    "predictive": "strong",   "equity": "",   "leakage": "leak", "missing_pct": 18},
        ]
    )
    return (features,)


@app.cell
def _(features, mo):
    catalogue_view = features.rename(columns={"missing_pct": "missing %"})
    mo.ui.table(catalogue_view, selection=None)
    return (catalogue_view,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Build your feature list.

        Pick the features that belong in the model. The deployment memo below regenerates as you change the selection.

        There is no scoring rubric here. The reasoning is what matters, not the count. Every inclusion and every exclusion should have a defensible answer when a reviewer asks why.
        """
    )
    return


@app.cell
def _(features, mo):
    picker = mo.ui.multiselect(
        options=features["feature"].tolist(),
        label="Features included in your model:",
    )
    picker
    return (picker,)


@app.cell
def _(features, mo, picker):
    selected_names = set(picker.value or [])
    selected = features[features["feature"].isin(selected_names)].reset_index(drop=True)

    n = len(selected)
    n_equity = int((selected["equity"] == "eq").sum())
    n_leakage = int((selected["leakage"] == "leak").sum())
    n_high_missing = int((selected["missing_pct"] > 40).sum())

    equity_names = selected[selected["equity"] == "eq"]["feature"].tolist()
    leakage_names = selected[selected["leakage"] == "leak"]["feature"].tolist()
    missing_rows = selected[selected["missing_pct"] > 40]
    missing_names = [
        f"{row['feature']} ({int(row['missing_pct'])}% missing)"
        for _, row in missing_rows.iterrows()
    ]

    if n == 0:
        memo = mo.callout(
            mo.md("_Pick at least one feature above to see the memo regenerate._"),
            kind="neutral",
        )
    else:
        size_note = (
            "A model with fewer than six features is probably underspecified. "
            "A model with more than twenty-five is probably unauditable. "
            f"Your set sits at **{n}**."
        )
        if n < 6 or n > 25:
            size_kind = "warn"
        else:
            size_kind = "info"

        if n_leakage > 0:
            leak_kind = "warn"
            leak_md = (
                f"**Leakage-flagged features in your set: {n_leakage}.** "
                "These features contain information that is not reliably available at scoring time. "
                "They will inflate your offline performance and quietly fail in deployment. "
                "Remove them before evaluation. Leakage is a bug.\n\n"
                + "\n".join(f"- {nm}" for nm in leakage_names)
            )
        else:
            leak_kind = "success"
            leak_md = "**Leakage-flagged features in your set: 0.** No leakage problems detected."

        if n_equity > 0:
            eq_kind = "warn"
            eq_md = (
                f"**Equity-flagged features in your set: {n_equity}.** "
                "These features carry real signal partly because they proxy for structural inequity. "
                "Including any of them requires explicit written justification: what is the deployment goal, "
                "who is the intended beneficiary, and how is the team going to monitor for disparate impact across subgroups?\n\n"
                + "\n".join(f"- {nm}" for nm in equity_names)
            )
        else:
            eq_kind = "success"
            eq_md = "**Equity-flagged features in your set: 0.** Nothing here requires equity justification at the feature-selection level. (You still owe subgroup performance monitoring at the model level.)"

        if n_high_missing > 0:
            miss_kind = "warn"
            miss_md = (
                f"**High-missingness features in your set: {n_high_missing}.** "
                "These features are missing in more than forty percent of the development cohort. In deployment the model "
                "will be running on the imputation strategy, not the underlying signal. Either commit to active capture "
                "(an operational ask, not a modeling one) or drop the feature.\n\n"
                + "\n".join(f"- {nm}" for nm in missing_names)
            )
        else:
            miss_kind = "success"
            miss_md = "**High-missingness features in your set: 0.** Every selected feature is reliably captured."

        memo = mo.vstack(
            [
                mo.callout(mo.md(f"**Feature count: {n}.** {size_note}"), kind=size_kind),
                mo.callout(mo.md(leak_md), kind=leak_kind),
                mo.callout(mo.md(eq_md), kind=eq_kind),
                mo.callout(mo.md(miss_md), kind=miss_kind),
            ]
        )

    memo
    return memo, n, n_equity, n_high_missing, n_leakage, selected


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A real opinionated model.

        The **LACE index** (van Walraven and colleagues) predicts 30-day readmission or death using four variables:

        | LACE | What it stands for | Closest analogue in our catalogue |
        |---|---|---|
        | **L** | Length of stay (current admission) | Current LOS (index admission) |
        | **A** | Acuity of admission (emergent vs elective) | (proxied by ICU stay during current admission) |
        | **C** | Charlson comorbidity index | Charlson comorbidity index |
        | **E** | Emergency department visits in the past 6 months | Prior 6-month ED visits |

        Four features. Discriminates approximately as well as many 200-feature models for the same outcome. It is in real production use across many health systems because it is small enough to be in real production use.

        The HOSPITAL score uses seven variables. PARR-30 uses around twelve. The pattern across published clinical readmission scores that have actually been deployed is consistent: small. The argument from the parsimony literature is that for most clinical prediction problems, an interpretable model in the four-to-twelve-feature range performs comparably to a black-box model with two orders of magnitude more inputs, and the gap is mostly accounting noise.

        Notice what LACE leaves out: demographics, social factors, post-discharge data, anything from the discharge medication list. Each exclusion is a deliberate abstraction call.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What you probably noticed.

        - **Leakage flags are bugs, not stylistic choices.** The 7-day-follow-up and Rx-fill-within-72h features both look like the most predictive variables in the catalogue. They are. But they're predictive because they overlap the outcome window. Including them gives you a model that performs well on retrospective data and silently underperforms in deployment, where the leaky variable isn't observable at scoring time.
        - **Equity-flagged features are not categorically banned, but they are categorically expensive.** Including race or ADI demands a written justification and a subgroup performance monitoring commitment. The discipline isn't to remove them on principle. The discipline is to refuse to include them without a documented reason and a monitoring plan.
        - **High-missingness features are silent dead weight.** They contribute mostly through the imputation strategy. If you're depending on functional status at sixty percent missingness, you're depending on the imputation, not the captured signal.
        - **Feature count alone is not the trade.** Six well-chosen features beat thirty mediocre ones. But twenty-five or more is almost always a sign that nobody has done the abstraction work yet.

        The deployment-ready feature list is not the one with the highest offline AUC. It is the one whose every feature you can defend, monitor, and explain.
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
            "The 14-feature model is more accurate; parsimony reduces overfitting.",
            "The 240-feature model is too complex to audit, explain to case management, or monitor for drift and disparate subgroup performance.",
            "The 240-feature model probably includes leaky features that are inflating its AUC.",
            "The 14-feature model runs faster in production.",
        ],
        label=(
            "Your data team's first cut at the readmission model used 240 features and got an offline AUC of 0.84. "
            "After your feature-selection pass, the model is down to 14 features with AUC 0.81. "
            "The data scientist argues that the larger model is better because the AUC is higher. "
            "What is the strongest deployment-readiness argument for the 14-feature version?"
        ),
    )
    quiz
    return (quiz,)


@app.cell
def _(mo, quiz):
    if quiz.value is None:
        quiz_response = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif quiz.value.startswith("The 240-feature model is too complex to audit"):
        quiz_response = mo.callout(
            mo.md(
                "**Yes.** The 0.03 AUC gap is real, and the data scientist is not wrong that it exists. But the gap is meaningless if the larger model cannot be deployed against a real workflow. "
                "A 240-feature model cannot be explained to case management. It cannot be monitored for drift on any per-feature basis a human can interpret. It cannot be audited when (not if) it starts giving systematically different recommendations for one subgroup. "
                "Those failures are not aesthetic complaints; they are blocking deployment requirements. The 14-feature model is the deployable model. The AUC gap is a tax you pay for being able to run, monitor, and explain the thing."
            ),
            kind="success",
        )
    elif quiz.value.startswith("The 14-feature model is more accurate"):
        quiz_response = mo.callout(
            mo.md(
                "**Wrong direction on the math.** Parsimony does not generally raise offline AUC; it usually lowers it slightly. The argument for parsimony is not that the smaller model is more accurate, but that it is deployable, auditable, and monitorable. Those are different goods."
            ),
            kind="warn",
        )
    elif quiz.value.startswith("The 240-feature model probably includes leaky features"):
        quiz_response = mo.callout(
            mo.md(
                "**Possibly true, and if true, important.** A 240-feature model from a large data warehouse will frequently contain at least one leaky feature, and a 0.03 AUC gap is the right order of magnitude for what a single leaky feature can buy. "
                "But this is a hypothesis that requires investigation, not the strongest argument you can make in the room today. The argument that doesn't depend on inspecting the feature list is the auditability and monitorability one."
            ),
            kind="warn",
        )
    else:
        quiz_response = mo.callout(
            mo.md(
                "**True but trivial.** Compute cost is the cheapest thing in the building. The strongest argument is about what humans can do with the model after it ships."
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

        - You named the cost of including a feature (data quality, drift, monitoring, explanation, equity surveillance) and the bet involved in excluding one.
        - You learned the five categories that earn a feature its way off a model: leaky, equity-flagged, high-missingness, redundant, cosmetic.
        - You built a feature list against a real-feeling readmission scenario and watched the deployment memo regenerate as you adjusted what was in.
        - You saw what a real opinionated published model looks like: small.

        Decomposition (Track 01), pattern recognition with edge cases (Track 02), and abstraction (this track) are the three moves of computational thinking. They are the moves clinicians make implicitly. The work of this course is making them explicit and applying them on purpose.

        ## What's next.

        **Track 04: Algorithms in plain English.** A worked algorithm (DAS28) walked line by line. You will see what a small, well-abstracted clinical algorithm actually does with its inputs, and you'll watch the score update as you move sliders for tender-joint count, swollen-joint count, CRP, and patient global assessment. After Track 04 you will be able to read any published clinical score line by line, point at each operation, and ask: what is this step doing, and what would happen if it were doing something else?
        """
    )
    return


if __name__ == "__main__":
    app.run()
