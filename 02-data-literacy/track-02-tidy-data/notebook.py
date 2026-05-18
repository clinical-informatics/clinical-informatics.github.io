"""Track 02: Tidy data.

Track 01 fixed each column's type. This track fixes each row's shape.
Three ideas: the one rule of tidy data (each row an observation, each
column a variable, each cell one value), the four shapes of untidy data
that show up in clinical extracts, and what `melt` and `pivot` actually
do. Then a reactive reshape: Ms. Reyes's medication list in two of the
four untidy shapes at once, cleaned into a tidy table step by step.
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

    import re

    import marimo as mo
    import pandas as pd

    return mo, pd, re


@app.cell
def _(mo):
    mo.md(r"""
    # Track 02: Tidy data

    ## The shape problem

    A medication list comes back as one row per patient with twelve columns named `med1` through `med12`, mostly empty. A flowsheet exports as one row per timestamp with eighty columns, one per vital sign, mostly null. A claims pull has the diagnosis and the procedure glued into one cell with a slash between them.

    None of these are *wrong*. The values are accurate. The column types might be right. The shape is wrong, and the wrong shape costs more time downstream than every other data problem combined: every filter is a regex, every aggregation is a loop, every plot is a Frankenstein call.

    This track is about getting clinical data into the one shape that makes every subsequent move short. Three ideas, then a reshape.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. The one rule of tidy data

    A dataset is **tidy** when three things are true at once:

    1. **Each row is one observation.** One specimen, one visit, one med exposure, one fact.
    2. **Each column is one variable.** One thing being measured, one attribute, one identifier.
    3. **Each cell holds one value.** Not two facts glued together. Not a list. Not a free-text blob.

    The rule is from Hadley Wickham's 2014 paper. Naming it didn't invent the shape; it gave analysts a vocabulary to say "this is tidy" or "this is not" out loud. Most of what follows is applying the rule.

    Below is a tidy table. Three rows, four columns, each cell holds one value, the row is the observation. Compare it to the untidy variants on the next screen.
    """)
    return


@app.cell
def _(mo, pd):
    tidy_example = pd.DataFrame(
        {
            "patient_id": ["ER-001", "ER-001", "ER-001"],
            "medication": ["Methotrexate", "Adalimumab", "Folic acid"],
            "dose_mg": [25, 40, 1],
            "frequency": ["weekly", "q2wk", "daily"],
        }
    )
    tidy_example.index = range(1, len(tidy_example) + 1)
    tidy_example.index.name = "row"
    mo.vstack(
        [
            mo.md("**Tidy.** One row per medication exposure. One value per cell."),
            mo.ui.table(tidy_example, selection=None),
            mo.callout(
                mo.md(
                    "From this shape, every analysis is short: filter by route, group by medication class, compute total dose per patient, plot dose over time. Try the same questions on the untidy versions below."
                ),
                kind="info",
            ),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 2. Wide and long, defined

    Before the four shapes, the vocabulary. The words **wide** and **long** describe two shapes the same data can take. They get thrown around as if everyone knows what they mean. Most people don't.

    A **wide** table has **one row per entity** (a patient, a visit, a timestamp) and **one column per attribute** of that entity. Adding a new attribute (an extra lab, an extra vital sign) adds a *new column*. The row count is fixed by how many entities you have.

    A **long** table has **one row per measurement**, usually three columns: the entity identifier, the attribute name, and the value. Adding a new attribute adds *new rows*. The column count is fixed at three.

    Concretely, the same four blood pressures for one patient over one shift:

    | shape | layout |
    |---|---|
    | wide | `time | bp_sys | bp_dia` with four rows |
    | long | `time | measurement | value` with eight rows (one per measurement) |

    Same data. Different shape. **Neither shape is universally tidy.** Tidiness is about whether the *row* matches the *observation unit your analysis is iterating over*.

    - Plotting all vital signs colored by which vital → the observation is a measurement → **long is tidy**.
    - Computing a per-visit summary across multiple labs → the observation is a visit → **wide is tidy**.

    Most clinical data ships wide because that's what spreadsheets look like; most analyses want long because that's what plotting and grouping libraries expect. The shape problem is almost always: the data shipped wide and the analysis needs long, or vice versa.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 3. The four shapes of untidy data

    Each of these four shapes is a real export you might receive. Each one breaks one of the tidy rules in a characteristic way. For each, you'll see the untidy version and the tidy target side by side.

    | # | Shape | Definition | Which tidy rule it breaks |
    |---|---|---|---|
    | 1 | **Values-as-columns** | The column headers are *values* of an underlying variable, not separate variables. Six columns named for six vital signs are six values of one variable (vital sign identity). | "Each column is one variable." |
    | 2 | **Long-when-you-need-wide** | Each row is one (entity, attribute, value) triple, but the analysis treats the *entity* as the observation. The attributes need to be side-by-side columns. | "Each row is one observation," for the unit of analysis you actually have. |
    | 3 | **Multi-fact cell** | A single cell holds two or more semantically distinct facts glued into one string. `25 mg SC weekly` is four facts in one cell. | "Each cell holds one value." |
    | 4 | **Repeating groups** | A one-to-many relationship has been flattened into numbered columns (`med1`, `med2`, `med3`, ...). The numbered columns are the same variable repeated. | "Each column is one variable." |
    """)
    return


@app.cell
def _(mo, pd):
    wide_vitals = pd.DataFrame(
        {
            "time": ["08:00", "12:00", "16:00", "20:00"],
            "hr": [88, 92, 84, 86],
            "bp_sys": [132, 138, 128, 130],
            "bp_dia": [84, 86, 80, 82],
            "temp": [37.1, 37.4, 37.2, 37.0],
            "rr": [16, 18, 16, 17],
            "spo2": [98, 97, 98, 98],
        }
    )
    wide_vitals_display = wide_vitals.copy()
    wide_vitals_display.index = range(1, len(wide_vitals_display) + 1)
    wide_vitals_display.index.name = "row"

    tidy_vitals = wide_vitals.melt(
        id_vars=["time"],
        value_vars=["hr", "bp_sys", "bp_dia", "temp", "rr", "spo2"],
        var_name="vital_sign",
        value_name="value",
    ).sort_values(["time", "vital_sign"]).reset_index(drop=True)
    tidy_vitals_display = tidy_vitals.copy()
    tidy_vitals_display.index = range(1, len(tidy_vitals_display) + 1)
    tidy_vitals_display.index.name = "row"

    mo.vstack(
        [
            mo.md(
                "### Shape 1: values-as-columns\n\n"
                "**Definition.** The column headers (`hr`, `bp_sys`, `bp_dia`, `temp`, `rr`, `spo2`) are not six different things being measured. They are six *values* of one underlying variable: **vital sign identity**. The real variable here is *which vital sign*, and the table has hidden it inside the column names.\n\n"
                "**Tidy rule violated.** _Each column is one variable._\n\n"
                "**Real example.** A flowsheet export from any modern EHR. One row per timestamp; one column per kind of vital. This shape ships out of Epic, Cerner, athena, and every nursing flowsheet you have ever seen.\n\n"
                "**Untidy (what you receive).** Wide. 4 rows × 7 columns."
            ),
            mo.ui.table(wide_vitals_display, selection=None),
            mo.md(
                "**Tidy (what the analysis wants).** Long. 24 rows × 3 columns. "
                "One row per (time, vital_sign) measurement. `vital_sign` is now a column, not a column name. "
                "Same data, no information added or lost; the shape changed."
            ),
            mo.ui.table(tidy_vitals_display.head(12), selection=None),
            mo.md("_(Twelve of twenty-four tidy rows shown; the remaining twelve continue the same pattern across 16:00 and 20:00.)_"),
            mo.callout(
                mo.md(
                    "**The reshape move.** `wide_vitals.melt(id_vars=['time'], var_name='vital_sign', value_name='value')`. From the tidy form, mean blood pressure across the shift is `tidy_vitals.groupby('vital_sign')['value'].mean()`. One line. Section 4 below explains what `melt` actually does."
                ),
                kind="info",
            ),
        ]
    )
    return tidy_vitals, wide_vitals


@app.cell
def _(mo, pd):
    long_labs = pd.DataFrame(
        {
            "date": ["2024-04-17"] * 3 + ["2024-07-22"] * 3 + ["2024-10-30"] * 3,
            "test": ["CRP", "ESR", "ALT"] * 3,
            "value": [18.7, 29, 38, 14.1, 24, 32, 11.4, 22, 32],
        }
    )
    long_labs_display = long_labs.copy()
    long_labs_display.index = range(1, len(long_labs_display) + 1)
    long_labs_display.index.name = "row"

    tidy_labs_wide = long_labs.pivot(
        index="date", columns="test", values="value"
    ).reset_index()
    tidy_labs_wide.columns.name = None
    tidy_labs_wide = tidy_labs_wide[["date", "CRP", "ESR", "ALT"]]
    tidy_labs_wide_display = tidy_labs_wide.copy()
    tidy_labs_wide_display.index = range(1, len(tidy_labs_wide_display) + 1)
    tidy_labs_wide_display.index.name = "row"

    mo.vstack(
        [
            mo.md(
                "### Shape 2: long-when-you-need-wide\n\n"
                "**Definition.** Each row holds one (date, test, value) triple. That is tidy *if* your analysis iterates over individual lab results. If your analysis iterates over *visits* (asking 'on April 17, was CRP up while ESR stayed flat?'), then each visit's three labs belong side by side, not stacked across three rows.\n\n"
                "**Tidy rule violated.** _Each row is one observation_, when the observation unit your analysis cares about is the visit. Long is tidy when the observation is the measurement; wide is tidy when the observation is the visit. Same data, two valid shapes, only one of them fits the question you are asking.\n\n"
                "**Real example.** A lab-results extract from a CDW with one row per resulted lab. Great for tracking lab trends per test over time. Painful when the analyst wants to compute a flare-day summary (CRP up, ESR up, ALT stable) where each visit is one row.\n\n"
                "**Untidy (what you receive).** Long. 9 rows × 3 columns. The variable `test` is its own column."
            ),
            mo.ui.table(long_labs_display, selection=None),
            mo.md(
                "**Tidy (what the per-visit analysis wants).** Wide. 3 rows × 4 columns. "
                "Each row is one visit. The three labs are columns. Now you can write `df['CRP'] > df['ESR'] / 2` and ask flare-pattern questions row by row."
            ),
            mo.ui.table(tidy_labs_wide_display, selection=None),
            mo.callout(
                mo.md(
                    "**The reshape move.** `long_labs.pivot(index='date', columns='test', values='value')`. The unique values of `test` (CRP, ESR, ALT) become column names; the values fill in the cells."
                ),
                kind="info",
            ),
        ]
    )
    return long_labs, tidy_labs_wide


@app.cell
def _(mo, pd):
    glued_meds = pd.DataFrame(
        {
            "medication": ["Methotrexate", "Adalimumab", "Folic acid"],
            "dose_route": ["25 mg SC weekly", "40 mg SC q2wk", "1 mg PO daily"],
        }
    )
    glued_meds.index = range(1, len(glued_meds) + 1)
    glued_meds.index.name = "row"

    tidy_split_meds = pd.DataFrame(
        {
            "medication": ["Methotrexate", "Adalimumab", "Folic acid"],
            "dose_value": [25, 40, 1],
            "dose_unit": ["mg", "mg", "mg"],
            "route": ["SC", "SC", "PO"],
            "frequency": ["weekly", "q2wk", "daily"],
        }
    )
    tidy_split_meds.index = range(1, len(tidy_split_meds) + 1)
    tidy_split_meds.index.name = "row"

    mo.vstack(
        [
            mo.md(
                "### Shape 3: multi-fact cell\n\n"
                "**Definition.** A single cell holds two or more semantically distinct facts glued into one string. The cell `25 mg SC weekly` is four facts: magnitude (`25`), unit (`mg`), route (`SC`), frequency (`weekly`). The cell looks like one column's worth of information; it is actually four.\n\n"
                "**Tidy rule violated.** _Each cell holds one value._\n\n"
                "**Real example.** Almost every freetext med-list cell from a paper-form-derived EHR field. Also: diagnosis cells that hold `M05.79 / seropositive RA without organ involvement` (code and text in one), address cells holding street-city-state-zip together, demographics cells holding `52F` for age-and-sex.\n\n"
                "**Untidy (what you receive).** Each `dose_route` cell holds four facts."
            ),
            mo.ui.table(glued_meds, selection=None),
            mo.md(
                "**Tidy (what the analysis wants).** Four columns, one fact each. Now `tidy_split_meds[tidy_split_meds['route'] == 'SC']` filters the subcutaneous medications without a regex; `tidy_split_meds['dose_value'].sum()` makes arithmetic sense."
            ),
            mo.ui.table(tidy_split_meds, selection=None),
            mo.callout(
                mo.md(
                    "**The reshape move.** Not melt, not pivot. A `str.extract` with a regular expression: "
                    "`glued_meds['dose_route'].str.extract(r'([0-9.]+)\\s+(\\w+)\\s+(\\w+)\\s+(.+)')`. "
                    "Real-world variants (`25mg`, `subq` vs `SC`) defeat naive splits, so the parser has to anticipate them. The shape problem and the type problem combine here: until you split, you cannot type."
                ),
                kind="info",
            ),
        ]
    )
    return (tidy_split_meds,)


@app.cell
def _(mo, pd):
    repeating_meds = pd.DataFrame(
        {
            "patient": ["ER-001", "ER-002", "ER-003"],
            "med1": ["MTX", "MTX", "MTX"],
            "dose1": ["25 mg", "20 mg", "15 mg"],
            "med2": ["Adalimumab", "", "Sulfasalazine"],
            "dose2": ["40 mg", "", "1000 mg"],
            "med3": ["Folic acid", "", "Folic acid"],
            "dose3": ["1 mg", "", "1 mg"],
            "med4": ["", "", "Prednisone"],
            "dose4": ["", "", "5 mg"],
        }
    )
    repeating_meds.index = range(1, len(repeating_meds) + 1)
    repeating_meds.index.name = "row"

    tidy_repeating_meds = pd.DataFrame(
        {
            "patient": [
                "ER-001", "ER-001", "ER-001",
                "ER-002",
                "ER-003", "ER-003", "ER-003", "ER-003",
            ],
            "medication": [
                "MTX", "Adalimumab", "Folic acid",
                "MTX",
                "MTX", "Sulfasalazine", "Folic acid", "Prednisone",
            ],
            "dose": [
                "25 mg", "40 mg", "1 mg",
                "20 mg",
                "15 mg", "1000 mg", "1 mg", "5 mg",
            ],
        }
    )
    tidy_repeating_meds.index = range(1, len(tidy_repeating_meds) + 1)
    tidy_repeating_meds.index.name = "row"

    mo.vstack(
        [
            mo.md(
                "### Shape 4: repeating groups\n\n"
                "**Definition.** A one-to-many relationship (one patient can have many medications) has been flattened into numbered columns: `med1`, `med2`, `med3`, `med4`. The numbered suffix is the giveaway. These four columns are not four different variables; they are the *same* variable (medication name) repeated four times, because the export had to flatten a list into a fixed-width row.\n\n"
                "**Tidy rule violated.** _Each column is one variable._ `med1` is not a different concept from `med2`; both hold a medication name.\n\n"
                "**Real example.** Almost every form-based registry export. Tumor staging tables with `metastasis_site_1`, `metastasis_site_2`, ... Family-history forms with `relative_1_dx`, `relative_2_dx`, ... Allergy lists with `allergen_a`, `allergen_b`, .... The shape is the result of cramming a list into a spreadsheet.\n\n"
                "**Important.** The empty cells in the untidy form are not missing values. They are structural placeholders saying 'this patient had fewer than four medications.' Track 03 distinguishes these from real missing data: a Track 03 missing value is a value that *should be* there; a Track 02 structural blank is a row that *should not be* there.\n\n"
                "**Untidy (what you receive).** 3 rows × 9 columns. Mostly empty for patients with fewer medications."
            ),
            mo.ui.table(repeating_meds, selection=None),
            mo.md(
                "**Tidy (what the analysis wants).** One row per medication exposure. Patient ER-001 has three rows. Patient ER-002 has one row. Patient ER-003 has four rows. Total: 8 rows, not 12. The empty placeholder cells disappear because nothing was missing; the rows just didn't exist."
            ),
            mo.ui.table(tidy_repeating_meds, selection=None),
            mo.callout(
                mo.md(
                    "**The reshape move.** A `melt` to stack `med1..med4` into one `medication` column, plus a parallel `melt` for `dose1..dose4`, joined on patient. Filter out the empty placeholder rows. The Section 5 reshape lab walks this exact move on a larger version of this table."
                ),
                kind="info",
            ),
        ]
    )
    return (tidy_repeating_meds,)


@app.cell
def _(mo):
    mo.md(r"""
    ## 4. What `melt` and `pivot` actually do

    You have already seen the two operations in action above (Shapes 1 and 2). Now the names.

    - **`melt` turns wide into long.** Picks a set of columns, stacks them into two new columns (one naming where each value came from, one holding the value), and repeats the `id_vars` for each new row. That's what got us from the 4×7 `wide_vitals` to the 24×3 `tidy_vitals` in Shape 1.
    - **`pivot` turns long into wide.** Picks one column to spread out, turns its unique values into new column names. That's what got us from the 9×3 `long_labs` to the 3×4 `tidy_labs_wide` in Shape 2.

    The two are inverses. A `melt` then a matching `pivot` returns the original.

    **One important caveat: duplicates.** `pivot` requires exactly one value per (index, column) pair. If the same patient had two CRPs drawn on the same day for some reason, `pivot` errors. In clinical data, duplicates always happen, so `pivot_table(aggfunc="mean")` is the safer default. It does the same reshape but aggregates ties instead of refusing.

    **The other two shapes** (multi-fact cell, repeating groups) need different tools. Multi-fact cells need a parser (`str.extract` with a regex). Repeating groups need two parallel `melt`s and a filter to drop the structural blanks. The next section walks the repeating-groups case end to end.
    """)
    return


@app.cell
def _(mo):
    pick_quiz = mo.ui.radio(
        options=[
            "Leave the table as it is and use a separate plotting call for each vital sign.",
            "Pivot the table so each timestamp becomes a column, with one row per vital sign.",
            "Melt the table so each row is one (time, vital_sign, value) triple.",
            "Split the table into six separate per-vital DataFrames and concatenate them.",
        ],
        label=(
            "An ICU researcher pulls a flowsheet export with one row per fifteen-minute "
            "interval and one column per vital sign (hr, bp_sys, bp_dia, temp, rr, spo2). "
            "She wants to plot all six vital signs on one chart over time, color-coded by "
            "vital sign. Which reshape is the right next move?"
        ),
    )
    pick_quiz
    return (pick_quiz,)


@app.cell
def _(mo, pick_quiz):
    if pick_quiz.value is None:
        pick_quiz_feedback = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif pick_quiz.value.startswith("Melt the table so each row is one"):
        pick_quiz_feedback = mo.callout(
            mo.md(
                "**Correct.** The plotting libraries (Altair, ggplot, seaborn) all expect long-format input "
                "where 'the thing being colored' is its own column. The long form lets you say `color='vital_sign'` "
                "in one parameter. The pivot option goes the wrong way; the leave-it-alone option works but "
                "produces six separate plot calls and inconsistent styling; the split-and-concatenate option is "
                "what people do when they don't know `melt` exists, and the result is the same as the melt "
                "with more steps."
            ),
            kind="success",
        )
    else:
        pick_quiz_feedback = mo.callout(
            mo.md(
                "**Not quite.** Long format is what every plotting library expects when you want to color, facet, or group by a categorical variable. "
                "Pivoting goes the wrong direction (wider, not longer). Leaving the table as is forces a separate plot call per vital. "
                "Splitting into six DataFrames is the long form arrived at by hand, which is what `melt` does in one line."
            ),
            kind="warn",
        )
    pick_quiz_feedback
    return (pick_quiz_feedback,)


@app.cell
def _(mo):
    mo.md(r"""
    ## 5. Reshape Ms. Reyes's medication list

    A real-looking export of Ms. Reyes's medications and four other RA patients, with two shape problems at once: the repeating-groups shape (`med1`, `med2`, `med3`, `med4`) **and** the two-facts-in-one-cell shape (dose-and-route glued). The task is to walk this table to tidy and watch each move land.

    The interactive panel below has three checkboxes. Toggle them in order. Each move applies on top of the previous one, and the result table updates reactively.
    """)
    return


@app.cell
def _(mo, pd):
    untidy_meds = pd.DataFrame(
        {
            "patient_id": ["ER-001", "ER-002", "ER-003", "ER-004", "ER-005"],
            "med1_name": [
                "Methotrexate", "Methotrexate", "Methotrexate",
                "Methotrexate", "Methotrexate",
            ],
            "med1_dose_route": [
                "25 mg SC weekly", "20 mg PO weekly", "15 mg PO weekly",
                "25 mg SC weekly", "12.5 mg PO weekly",
            ],
            "med2_name": [
                "Adalimumab", "", "Sulfasalazine", "Etanercept", "Hydroxychloroquine",
            ],
            "med2_dose_route": [
                "40 mg SC q2wk", "", "1000 mg PO BID", "50 mg SC weekly", "200 mg PO BID",
            ],
            "med3_name": [
                "Folic acid", "Folic acid", "Folic acid", "Folic acid", "Folic acid",
            ],
            "med3_dose_route": [
                "1 mg PO daily", "1 mg PO daily", "1 mg PO daily",
                "1 mg PO daily", "5 mg PO weekly",
            ],
            "med4_name": ["", "", "Prednisone", "", "Prednisone"],
            "med4_dose_route": ["", "", "5 mg PO daily", "", "10 mg PO daily"],
        }
    )
    untidy_display = untidy_meds.copy()
    untidy_display.index = range(1, len(untidy_display) + 1)
    untidy_display.index.name = "row"
    mo.vstack(
        [
            mo.md("**The export, as inherited.** Five patients across nine columns, two shape problems stacked."),
            mo.ui.table(untidy_display, selection=None),
        ]
    )
    return (untidy_meds,)


@app.cell
def _(mo):
    step1 = mo.ui.checkbox(
        label="Step 1: collapse the med1/med2/med3/med4 columns into one row per (patient, slot)",
        value=False,
    )
    step2 = mo.ui.checkbox(
        label="Step 2: drop the empty placeholder rows (patients who had fewer than four medications)",
        value=False,
    )
    step3 = mo.ui.checkbox(
        label="Step 3: split dose_route into dose_value, dose_unit, route, frequency",
        value=False,
    )
    mo.vstack([step1, step2, step3])
    return step1, step2, step3


@app.cell
def _(mo, pd, re, step1, step2, step3, untidy_meds):
    df = untidy_meds.copy()
    explanation_lines = []

    if step1.value:
        name_cols = ["med1_name", "med2_name", "med3_name", "med4_name"]
        dose_cols = ["med1_dose_route", "med2_dose_route", "med3_dose_route", "med4_dose_route"]
        names_long = df.melt(
            id_vars=["patient_id"],
            value_vars=name_cols,
            var_name="slot",
            value_name="medication",
        )
        names_long["slot"] = names_long["slot"].str.replace("_name", "", regex=False)
        doses_long = df.melt(
            id_vars=["patient_id"],
            value_vars=dose_cols,
            var_name="slot",
            value_name="dose_route",
        )
        doses_long["slot"] = doses_long["slot"].str.replace("_dose_route", "", regex=False)
        df = names_long.merge(doses_long, on=["patient_id", "slot"])
        df = df[["patient_id", "slot", "medication", "dose_route"]]
        explanation_lines.append(
            "**After Step 1.** Two `melt` calls (one for the name columns, one for the dose columns), "
            "joined on (patient_id, slot). Each patient now has four rows, one per slot. "
            f"Table is now **{len(df)} rows × {df.shape[1]} columns**. The repeating-group shape is gone."
        )

    if step2.value and step1.value:
        before = len(df)
        df = df[df["medication"].astype(str).str.strip() != ""].copy()
        df = df.drop(columns=["slot"]).reset_index(drop=True)
        explanation_lines.append(
            f"**After Step 2.** Dropped {before - len(df)} empty placeholder rows. "
            "These were never measurements; they were the export's way of saying 'this patient had fewer than four medications.' "
            f"Table is now **{len(df)} rows × {df.shape[1]} columns**. The slot column is gone because we don't care about it anymore (it was an artifact of the wide shape, not a clinical fact)."
        )

    if step3.value and step2.value and step1.value:
        def _parse_dose(s):
            s = str(s).strip()
            m = re.match(r"^([0-9.]+)\s*(mg|mcg|g|units?)\s+(\S+)\s+(.+)$", s)
            if m:
                dose_value, dose_unit, route, frequency = m.groups()
                return pd.Series({
                    "dose_value": float(dose_value),
                    "dose_unit": dose_unit,
                    "route": route,
                    "frequency": frequency.strip(),
                })
            return pd.Series({
                "dose_value": float("nan"),
                "dose_unit": None,
                "route": None,
                "frequency": s,
            })
        parsed = df["dose_route"].apply(_parse_dose)
        df = pd.concat([df.drop(columns=["dose_route"]), parsed], axis=1)
        explanation_lines.append(
            "**After Step 3.** One regex parses the dose-route string into four columns. Cells that don't match the expected pattern (none in this synthetic data, "
            "but expect roughly 5% on a real export) fall through with `dose_value=NaN` and the original string preserved in `frequency` for inspection. "
            f"Table is now **{len(df)} rows × {df.shape[1]} columns**, with every cell holding one fact."
        )

    df_display = df.copy()
    df_display.index = range(1, len(df_display) + 1)
    df_display.index.name = "row"

    if explanation_lines:
        narrative = mo.callout(mo.md("\n\n".join(explanation_lines)), kind="info")
    else:
        narrative = mo.callout(
            mo.md("_Toggle the steps above in order. Each one applies on top of the previous._"),
            kind="neutral",
        )

    mo.vstack(
        [
            mo.ui.table(df_display, selection=None),
            narrative,
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 6. Why this matters for what comes next

    The tidy version of the medication table is the shape every subsequent track expects.

    - **Track 03 (missingness).** "What's missing" only makes sense once empty placeholder rows are gone. In the untidy version, `med4_name` was empty for three patients; that wasn't missing data, that was a structural blank. The tidy version has no structural blanks. Whatever is empty now is genuinely missing.
    - **Track 04 (joins).** To join the medication table to the lab table, you need a `(patient_id, medication)` join key. The untidy version doesn't have a medication column to join on. Joins assume tidy inputs.
    - **Track 05 (databases).** The schema for a `medication_exposure` table looks exactly like the tidy version: one row per exposure, columns named `patient_id`, `medication`, `dose_value`, `dose_unit`, `route`, `frequency`. Tidy data is the shape a relational database would have stored it in if anyone had asked.

    The chain stacks: typed (Track 01), tidy (this track), missing-handled (Track 03), joined (Track 04), schema-backed (Track 05). Each step assumes the prior step is in place.
    """)
    return


if __name__ == "__main__":
    app.run()
