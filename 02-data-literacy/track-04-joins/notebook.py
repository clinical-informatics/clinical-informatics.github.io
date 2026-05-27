"""Track 04: Joins, the central skill.

Every clinical analysis is a join. The mechanics are simple; the trap is
what you don't see. This notebook covers the four basic joins (inner,
left, right, full outer) plus the anti-join on a real-looking RA cohort,
then exposes the silent patient loss problem with a reactive UI. The
many-to-many row explosion gets its own demo at the end.
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

    import marimo as mo
    import pandas as pd

    return mo, pd


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 04: Joins, the central skill

        ## Every clinical analysis is a join

        Demographics joined to labs. Labs joined to medications. Medications joined to outcomes. The data lives in different tables because that is how databases store it; the analysis needs it together because that is how clinical questions are asked.

        The mechanics are simple. Four lines of pandas per join. The trap is what you don't see: every join silently drops the patients who don't match. By the time you reach the analysis cohort, the number on the slide is not the number you started with, and the patients you lost may differ from the patients you kept in clinically meaningful ways.

        This track is the central data-wrangling skill. Five pieces:

        1. **What a join is**, mechanically.
        2. **Join keys**, what makes one work.
        3. **The four basic joins** (inner, left, right, full outer), each on a real-looking RA cohort.
        4. **The silent patient loss problem**, watchable on a reactive UI, and the anti-join diagnostic that surfaces it.
        5. **Many-to-many joins** and the row explosion they produce.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1. What a join is

        A **join** takes two tables that share a column and produces a new table where the rows are matched on that column. The shared column is the **join key**.

        Below is the smallest possible example. Two tables. Three rows of demographics, four rows of labs. Joined on `patient_id`.
        """
    )
    return


@app.cell
def _(mo, pd):
    demo_tiny = pd.DataFrame(
        {
            "patient_id": ["ER-001", "ER-002", "ER-003"],
            "age": [52, 38, 67],
            "sex": ["F", "F", "M"],
        }
    )
    demo_tiny.index = range(1, len(demo_tiny) + 1)
    demo_tiny.index.name = "row"

    labs_tiny = pd.DataFrame(
        {
            "patient_id": ["ER-001", "ER-001", "ER-002", "ER-002"],
            "date": ["2024-04-17", "2024-07-22", "2024-05-30", "2024-09-04"],
            "crp": [18.7, 14.1, 11.2, 8.6],
        }
    )
    labs_tiny.index = range(1, len(labs_tiny) + 1)
    labs_tiny.index.name = "row"

    joined_tiny = demo_tiny.reset_index(drop=True).merge(
        labs_tiny.reset_index(drop=True), on="patient_id", how="inner"
    )
    joined_tiny.index = range(1, len(joined_tiny) + 1)
    joined_tiny.index.name = "row"

    mo.vstack(
        [
            mo.hstack(
                [
                    mo.vstack([mo.md("**Demographics.**"), mo.ui.table(demo_tiny, selection=None)]),
                    mo.vstack([mo.md("**Labs.**"), mo.ui.table(labs_tiny, selection=None)]),
                ],
                widths=[1, 1],
            ),
            mo.md("**Joined on `patient_id`** (inner join):"),
            mo.ui.table(joined_tiny, selection=None),
            mo.callout(
                mo.md(
                    "Notice two things. **ER-001 appears twice** in the result because they had two labs; the demographics row was repeated to pair with each lab (one-to-many). "
                    "**ER-003 has disappeared entirely** because they have no labs. The inner join kept only the rows where the key matched in both tables."
                ),
                kind="info",
            ),
        ]
    )
    return demo_tiny, joined_tiny, labs_tiny


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2. Join keys

        The join key is the column (or columns) used to match rows. For a join to behave sensibly:

        - **The key must mean the same thing in both tables.** Two MRN columns that both say `ER-001` must refer to the same patient. If one table's `patient_id` came from Epic and the other from a study registry, they may not match even when they look the same. The patient-matching problem is a real thing.
        - **The key must be the same type** (Track 01). A `patient_id` stored as integer in one table and as text in another won't match even when the values are identical. `1001 != "1001"`.
        - **The key should be unique in at least one table** if you want a clean one-to-many result. Both sides having duplicates produces the row explosion at the end of this track.

        A **composite key** is multiple columns joined together. To match a specific encounter rather than a patient, join on `(patient_id, encounter_date)`. To match a specific lab result, join on `(patient_id, specimen_date, loinc_code)`. Composite keys are the norm in real clinical data, not the exception.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3. The four basic joins

        Same data, four different join types. Below is a 6-patient RA cohort with corresponding labs. Three patients have labs; one has labs but isn't in the demographics extract (a real-world data quality bug); two are in demographics but have no labs.

        Watch the result table change as the join type changes.
        """
    )
    return


@app.cell
def _(mo, pd):
    demo = pd.DataFrame(
        {
            "patient_id": ["ER-001", "ER-002", "ER-003", "ER-004", "ER-005"],
            "name": ["Reyes, Elena", "Chen, May", "Williams, Tom", "Patel, Anika", "Russo, Marco"],
            "age": [52, 47, 73, 38, 29],
            "sex": ["F", "F", "M", "F", "M"],
        }
    )

    labs = pd.DataFrame(
        {
            "patient_id": ["ER-001", "ER-002", "ER-002", "ER-005", "ER-006", "ER-006"],
            "date": [
                "2024-04-17", "2024-05-30", "2024-09-04",
                "2024-08-12", "2024-06-19", "2024-10-22",
            ],
            "crp": [18.7, 11.2, 8.6, 9.2, 24.3, 19.7],
        }
    )

    demo_display = demo.copy()
    demo_display.index = range(1, len(demo_display) + 1)
    demo_display.index.name = "row"
    labs_display = labs.copy()
    labs_display.index = range(1, len(labs_display) + 1)
    labs_display.index.name = "row"

    mo.vstack(
        [
            mo.hstack(
                [
                    mo.vstack(
                        [
                            mo.md("**Table A: demographics** (5 patients, ER-001 through ER-005)."),
                            mo.ui.table(demo_display, selection=None),
                        ]
                    ),
                    mo.vstack(
                        [
                            mo.md("**Table B: labs** (6 rows across 4 unique patients; note ER-006 appears in labs but not demographics)."),
                            mo.ui.table(labs_display, selection=None),
                        ]
                    ),
                ],
                widths=[1, 1],
            ),
            mo.callout(
                mo.md(
                    "**Patients in demographics only (no labs):** ER-003 (Williams), ER-004 (Patel). "
                    "**Patients in labs only (no demographics):** ER-006. "
                    "**Patients in both:** ER-001, ER-002, ER-005."
                ),
                kind="info",
            ),
        ]
    )
    return demo, demo_display, labs, labs_display


@app.cell
def _(mo):
    join_type = mo.ui.radio(
        options=[
            "inner (keep only matched rows)",
            "left (keep all demographics; null labs where no match)",
            "right (keep all labs; null demographics where no match)",
            "outer (keep everything from both sides)",
            "anti, demographics side (patients in demographics with NO labs)",
            "anti, labs side (lab rows for patients NOT in demographics)",
        ],
        value="inner (keep only matched rows)",
        label="Pick a join type",
    )
    join_type
    return (join_type,)


@app.cell
def _(demo, join_type, labs, mo, pd):
    if join_type.value.startswith("inner"):
        result = demo.merge(labs, on="patient_id", how="inner")
        explanation = (
            "**Inner join.** Keep only rows whose `patient_id` appears in *both* tables. "
            "Three patients survive (ER-001, ER-002, ER-005). Two are dropped from demographics (ER-003, ER-004). One lab row is dropped (ER-006). "
            "Total result rows: 4 (because ER-002 has two labs, each gets its own row paired with the demographics)."
        )
        kind = "info"
    elif join_type.value.startswith("left"):
        result = demo.merge(labs, on="patient_id", how="left")
        explanation = (
            "**Left join.** Keep every row from demographics. Attach labs where they exist; null where they don't. "
            "ER-003 and ER-004 appear with null `date` and `crp` (they're in the cohort, they just have no labs). "
            "ER-006 does NOT appear because they're not in demographics. "
            "This is the right join for 'all cohort patients, with labs where available.'"
        )
        kind = "info"
    elif join_type.value.startswith("right"):
        result = demo.merge(labs, on="patient_id", how="right")
        explanation = (
            "**Right join.** Keep every row from labs. Attach demographics where they match; null where they don't. "
            "ER-006's two lab rows appear with null `name`, `age`, `sex` (lab data exists but demographics are missing for this patient). "
            "ER-003 and ER-004 do NOT appear (they have demographics but no labs). "
            "Right joins are rare in practice; flipping the table order and using `left` is the convention."
        )
        kind = "info"
    elif join_type.value.startswith("outer"):
        result = demo.merge(labs, on="patient_id", how="outer")
        explanation = (
            "**Full outer join.** Keep every row from both sides. Fill nulls where the match is missing. "
            "Every patient in either table appears in the result. Useful for reconciliation: 'show me every patient who's anywhere, and flag which side they came from.' "
            "Less useful for analysis, because the result mixes 'no labs' nulls with 'no demographics' nulls and you have to think about both."
        )
        kind = "info"
    elif join_type.value.startswith("anti, demographics"):
        result = demo[~demo["patient_id"].isin(labs["patient_id"])].copy()
        explanation = (
            "**Anti-join, demographics side.** The patients who are in your cohort but have NO labs in the export. "
            "ER-003 (Williams) and ER-004 (Patel) appear. "
            "**This is the diagnostic move.** Run this before publishing a cohort size. If these patients differ systematically from the rest of the cohort (older, sicker, one specific site), the inner join you would otherwise run produces a biased analysis cohort."
        )
        kind = "warn"
    else:
        result = labs[~labs["patient_id"].isin(demo["patient_id"])].copy()
        explanation = (
            "**Anti-join, labs side.** The lab rows for patients NOT in your demographics extract. "
            "ER-006 appears twice (two lab rows). "
            "These are likely a data quality bug: patients whose labs landed in the export but whose demographics didn't. Worth investigating before treating them as 'missing data.' Maybe the demographics extract missed a site. Maybe the join key was wrong (an MRN format mismatch). Maybe it's correct and they're patients from a different cohort. The fix is rarely 'drop them silently.'"
        )
        kind = "warn"

    result_display = result.reset_index(drop=True).copy()
    result_display.index = range(1, len(result_display) + 1)
    result_display.index.name = "row"

    unique_patients = result["patient_id"].dropna().unique() if "patient_id" in result.columns else []
    n_rows = len(result)
    n_unique = len(unique_patients)

    mo.vstack(
        [
            mo.md(f"**Result.** {n_rows} rows. {n_unique} unique patients."),
            mo.ui.table(result_display, selection=None),
            mo.callout(mo.md(explanation), kind=kind),
        ]
    )
    return n_rows, n_unique, result, result_display


@app.cell
def _(mo):
    join_quiz = mo.ui.radio(
        options=[
            "Inner join. We only want patients with complete data.",
            "Left join, with demographics as the left table. We want every cohort patient in the result, with labs where available.",
            "Right join, with labs as the right table. We want every lab even if demographics are missing.",
            "Full outer join. We want everything.",
        ],
        label=(
            "You are running the primary analysis of a 200-patient registry of RA disease activity. "
            "Your demographics table has all 200 patients. Your labs table has CRPs for 178 of them. "
            "The primary outcome is 'percent of patients in remission at 12 months,' which requires linking "
            "demographics to labs. Which join is the honest choice for the primary analysis cohort?"
        ),
    )
    join_quiz
    return (join_quiz,)


@app.cell
def _(join_quiz, mo):
    if join_quiz.value is None:
        join_quiz_feedback = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif join_quiz.value.startswith("Left join"):
        join_quiz_feedback = mo.callout(
            mo.md(
                "**Correct.** The primary analysis is over the cohort of 200, not the subset of 178 who have labs. "
                "A left join with demographics on the left keeps all 200 patients and shows null CRP for the 22 who are missing labs. "
                "Then the analysis can decide how to handle those 22 explicitly (Track 03: impute, drop with justification, or report separately) instead of having them silently disappear. "
                "The inner join would have produced a denominator of 178, and 'percent in remission' computed over 178 is not the same as the same percent computed over 200. The difference is the silent patient loss."
            ),
            kind="success",
        )
    else:
        join_quiz_feedback = mo.callout(
            mo.md(
                "**Not quite.** The honest move when the cohort is defined by demographics is a **left join with demographics as the left table**. "
                "An inner join silently drops the 22 patients without labs, and 'percent in remission' computed over the remaining 178 is not the same number as the same percent over the cohort of 200. "
                "A right join is backwards (you'd be defining the cohort by who happens to have labs). "
                "A full outer join brings in lab rows for patients NOT in your cohort, which isn't what you want either."
            ),
            kind="warn",
        )
    join_quiz_feedback
    return (join_quiz_feedback,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 4. The silent patient loss problem

        The most common cohort-shrinkage scenario, exhibited on a realistic chain of joins. We start with 200 cohort patients, then join to labs, then to medications, then to outcomes. Each step silently drops patients who don't match.
        """
    )
    return


@app.cell
def _(mo, pd):
    chain = pd.DataFrame(
        {
            "step": [
                "1. Starting cohort (demographics)",
                "2. Inner join to labs (drop patients with no CRP in export)",
                "3. Inner join to medications (drop patients with no med record)",
                "4. Inner join to 12-month outcomes (drop patients lost to follow-up)",
            ],
            "patients_in_result": [200, 178, 142, 117],
            "patients_lost_this_step": [0, 22, 36, 25],
            "running_loss_pct": [0.0, 11.0, 29.0, 41.5],
        }
    )
    chain.index = range(1, len(chain) + 1)
    chain.index.name = "row"
    mo.vstack(
        [
            mo.ui.table(chain, selection=None),
            mo.callout(
                mo.md(
                    "**The reported analysis cohort is 117 patients, not 200.** Any rate computed over this 117 is a rate among patients who survived every join. "
                    "If the 83 lost patients differ from the 117 retained (sicker, less engaged, from one specific site), the analysis is biased in a direction the reader cannot see from the methods section.\n\n"
                    "**The fix is not to avoid inner joins.** The fix is to *measure the loss at every step* via the anti-join, and report it. The mature version of this table also has a column 'characteristics of lost patients' (mean age, sex distribution, mean prior CRP) so the reader can judge whether the loss is plausibly random."
                ),
                kind="warn",
            ),
        ]
    )
    return (chain,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Try it: run the anti-join

        Below the 5-patient cohort from Section 3. Toggle the checkbox to run the anti-join move (using `~isin`) and see which cohort patients would be silently lost if you ran an inner join to labs.
        """
    )
    return


@app.cell
def _(mo):
    show_antijoin = mo.ui.checkbox(
        label="Run the anti-join: which demographics rows would be lost on an inner join to labs?",
        value=False,
    )
    show_antijoin
    return (show_antijoin,)


@app.cell
def _(demo, labs, mo, show_antijoin):
    if show_antijoin.value:
        lost = demo[~demo["patient_id"].isin(labs["patient_id"])].copy()
        lost.index = range(1, len(lost) + 1)
        lost.index.name = "row"
        if len(lost) == 0:
            content = mo.callout(
                mo.md("No patients lost. Every demographics row has at least one matching lab. (Lucky cohort.)"),
                kind="success",
            )
        else:
            content = mo.vstack(
                [
                    mo.md(f"**{len(lost)} patients would be silently lost** on an inner join to labs:"),
                    mo.ui.table(lost, selection=None),
                    mo.callout(
                        mo.md(
                            "These are the patients to investigate before you publish a cohort count. "
                            "If they're older, sicker, or from a specific subgroup, the inner join you would have run produces a biased analysis. "
                            "The anti-join shows you the bias before you bake it into the analysis."
                        ),
                        kind="warn",
                    ),
                ]
            )
    else:
        content = mo.md("_Toggle the checkbox to run the anti-join._")
    content
    return (content,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 5. Many-to-many joins: the row explosion

        A join on a key that is unique in *both* tables produces clean one-to-one rows. A join on a key that is unique in one and repeated in the other (the common case) produces clean one-to-many rows. When the key is repeated on *both* sides, you get the Cartesian product: every row on the left matches every row on the right with the same key.

        Concrete example: one patient (ER-001) with three medications and three conditions. The two tables look fine. Joined on `patient_id` alone, the result has 3 × 3 = 9 rows for ER-001, and most of them are clinically nonsense.
        """
    )
    return


@app.cell
def _(mo, pd):
    meds = pd.DataFrame(
        {
            "patient_id": ["ER-001", "ER-001", "ER-001"],
            "medication": ["MTX", "Adalimumab", "Folic acid"],
        }
    )
    conditions = pd.DataFrame(
        {
            "patient_id": ["ER-001", "ER-001", "ER-001"],
            "condition": ["RA", "Anemia", "HTN"],
        }
    )
    exploded = meds.merge(conditions, on="patient_id", how="inner")

    meds_d = meds.copy()
    meds_d.index = range(1, len(meds_d) + 1)
    meds_d.index.name = "row"
    cond_d = conditions.copy()
    cond_d.index = range(1, len(cond_d) + 1)
    cond_d.index.name = "row"
    exp_d = exploded.copy()
    exp_d.index = range(1, len(exp_d) + 1)
    exp_d.index.name = "row"

    mo.vstack(
        [
            mo.hstack(
                [
                    mo.vstack([mo.md("**meds** (3 rows)"), mo.ui.table(meds_d, selection=None)]),
                    mo.vstack([mo.md("**conditions** (3 rows)"), mo.ui.table(cond_d, selection=None)]),
                ],
                widths=[1, 1],
            ),
            mo.md("**Joined on `patient_id` alone:** 3 × 3 = 9 rows for one patient."),
            mo.ui.table(exp_d, selection=None),
            mo.callout(
                mo.md(
                    "Half the rows are clinically nonsense (\"ER-001 taking MTX for HTN\" is in the result, even though nobody prescribed MTX for HTN). "
                    "The output table looks plausible until you check: ER-001 now appears nine times. "
                    "A naive aggregation over this table (mean CRP, total med count, condition prevalence) is wrong by a factor of (n_meds × n_conditions) per patient.\n\n"
                    "**The fix:** keep the join's grain explicit. Either join on a composite key that's unique on at least one side (`(patient_id, encounter_date)`), or aggregate before joining (\"medication list per patient\" as a single row, deduplicated), or never join these two tables directly (the medication-for-condition link is its own clinical fact and needs its own table). The wrong fix is to drop duplicates after the fact, because that hides the structural error instead of correcting it."
                ),
                kind="warn",
            ),
        ]
    )
    return cond_d, conditions, exp_d, exploded, meds, meds_d


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 6. What this leaves you

        Five things in place:

        1. **A join combines two tables on a shared key.** Inner keeps matched rows. Left keeps the left side. Right keeps the right side. Full outer keeps everything. Same operation, four different decisions about unmatched rows.
        2. **The anti-join is the diagnostic** for silent patient loss. Run it at every step of a join chain before reporting cohort numbers.
        3. **The silent patient loss problem is the most common cohort-size surprise** in clinical data. The fix is measurement plus deliberate decisions, not avoiding inner joins.
        4. **Composite keys are normal.** A clean clinical join is almost always `(patient_id, encounter_date)` or `(patient_id, specimen_date, loinc_code)`, not just `patient_id`.
        5. **Many-to-many joins explode the row count** when the key is non-unique on both sides. Always know the unique key on each table before joining.

        Track 05 continues from here. Once joins are second nature, the next question is: *what was the table designed for?* Joins behave the way they do because of schema decisions the database designer made. Track 05 covers the schema layer that makes the joins work, with a forward pointer to FHIR and OMOP for the standardized clinical versions.
        """
    )
    return


if __name__ == "__main__":
    app.run()
