"""Track 01: Data types and why they matter.

The first thing to ask of any column in a clinical dataset is "what type is
this?" Most analyses go wrong because that question never got asked. This
notebook walks four ideas with Ms. Reyes's labs as the substrate: numbers
vs text (with the CRP-stored-as-text bug made concrete), dates as the
special nightmare, categories and codes, and a five-question audit routine
for spotting type errors in real-looking data.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import io
    import json
    import sys
    from pathlib import Path

    import marimo as mo
    import numpy as np
    import pandas as pd

    _WASM_DATA_BASE = "/02-data-literacy/track-01-data-types/app"

    def load_cached_csv(name, **read_csv_kwargs):
        """Read a CSV from this track's cache/ directory. Works locally
        (reads from disk) and in marimo's WASM runtime (fetches from the
        site-absolute URL of the deployed cache).
        """
        if "pyodide" in sys.modules:
            from pyodide.http import open_url
            url = _WASM_DATA_BASE + "/cache/" + name
            return pd.read_csv(io.StringIO(open_url(url).read()), **read_csv_kwargs)
        return pd.read_csv(Path(__file__).parent / "cache" / name, **read_csv_kwargs)

    return load_cached_csv, mo, np, pd


@app.cell
def _(mo):
    mo.md(r"""
    # Track 01: Data types and why they matter

    ## The most common reason clinical analyses are quietly wrong

    Read a CSV in. Filter to a cohort. Compute a summary. The number comes out plausibly. The cohort is the right size. The mean of CRP is twenty-something. Life proceeds.

    Now imagine a parallel universe where the lab system reported five of Ms. Reyes's hemoglobin values as the text string `"<2.0"` instead of the number `2.0`, because the analyzer flags values below the lower limit of quantification that way. The cell still says hemoglobin. The column still reads in. The mean still comes out. The mean is wrong, in a direction nobody can see, by an amount nobody can quantify, and no error message ever fired.

    That is what this track is about. Every column has a **type**. The type is the rule the column follows for what its values mean and what operations on them are legal. When the type quietly disagrees with what the analysis assumes, the analysis quietly breaks.

    Four ideas, then an audit:

    1. The four data types you actually use in clinical work.
    2. Numbers vs text, walked on Ms. Reyes's CRP column.
    3. Dates as the special nightmare.
    4. Categories and codes.

    And at the end, a five-question routine for auditing a messy synthetic export.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. The four data types

    Most clinical columns are some flavor of one of four types. The list is not exhaustive (booleans, geographic shapes, hierarchical objects, blobs), but four covers most of what shows up day to day.

    | Type | What it stores | What operations make sense | Where it shows up clinically |
    |---|---|---|---|
    | **Numeric** | A number you can compute on | mean, median, sum, difference, ratio | CRP, ESR, hemoglobin, age, joint counts |
    | **Text** | Free narrative | length, substring search, concatenation | HPI, assessment, social history |
    | **Date / timestamp** | A point on the calendar | order, difference (interval), grouping by year/month | specimen_date, visit date, dob, dispense date |
    | **Categorical** | A value from a fixed allowed set, often coded | counts within each level, group-by | sex, race, encounter class, diagnosis code, lab name |

    The audit move is to look at each column and ask two questions: **what type is this column claiming to be, and what type does the clinical concept actually need it to be?** Most type bugs live in the gap between those two answers.
    """)
    return


@app.cell
def _(load_cached_csv, mo, pd):
    labs = load_cached_csv("labs.csv")
    types_table = pd.DataFrame(
        {
            "column": labs.columns,
            "pandas dtype": [str(t) for t in labs.dtypes],
            "first value": [repr(labs[c].iloc[0]) for c in labs.columns],
        }
    )
    mo.vstack(
        [
            mo.md(
                "Here is what `pandas.read_csv` decided about each column when it read in Ms. Reyes's lab file:"
            ),
            mo.ui.table(types_table, selection=None),
            mo.callout(
                mo.md(
                    "**The pandas dtype is the type pandas inferred from the first thousand or so rows. It is a guess. Sometimes it is wrong. Sometimes it is right for now and wrong after the next data refresh.**"
                ),
                kind="info",
            ),
        ]
    )
    return (labs,)


@app.cell
def _(mo):
    mo.md(r"""
    Two things to notice. `value` is `float64`, which is what we want for a measurement column. `specimen_date` is `object`, which is the pandas word for "I'm storing this as text because I'm not sure what else to do with it." That dates default to text on read is one of the most reliable sources of bugs in clinical Python. We will deal with it in a moment.

    ## 2. The CRP-stored-as-text bug

    Same column. Same patient. Same eighteen measurements. We will read the column twice. Once cleanly, and once after a synthetic copy-paste from a vendor export has dropped the text token `"<2.0"` into three of the cells (a real thing that happens when an analyzer reports values below its lower limit of quantification as text).
    """)
    return


@app.cell
def _(labs, mo, np, pd):
    crp_clean = labs[labs["test_name"] == "C-reactive protein"][["specimen_date", "value"]].copy()
    crp_clean = crp_clean.reset_index(drop=True)

    crp_polluted = crp_clean.copy()
    crp_polluted["value"] = crp_polluted["value"].astype(object)
    # corrupt the three lowest values to make the silent-drop bias visible
    crp_polluted.loc[[10, 11, 12], "value"] = "<2.0"

    side_by_side = pd.DataFrame(
        {
            "specimen_date": crp_clean["specimen_date"],
            "value (clean)": crp_clean["value"],
            "value (with three '<2.0' cells)": crp_polluted["value"],
        }
    )

    clean_mean = float(np.mean(crp_clean["value"]))
    try:
        polluted_mean = pd.to_numeric(crp_polluted["value"]).mean()
        polluted_status = f"mean = {polluted_mean:.2f} (this would error in stricter tools)"
    except Exception as exc:  # noqa: BLE001
        polluted_status = f"errored. The message was: `{exc}`"

    polluted_silent_drop = (
        pd.to_numeric(crp_polluted["value"], errors="coerce").mean()
    )

    mo.vstack(
        [
            mo.md("**Two parallel CRP columns. Same eighteen specimens.**"),
            mo.ui.table(side_by_side, selection=None),
            mo.md(
                f"""
                **Clean column.** dtype `float64`. Mean of CRP across the cohort = **{clean_mean:.2f} mg/L**.

                **Polluted column.** dtype `object` (text). Three of the eighteen cells are now the string `"<2.0"`.

                - If you force a numeric conversion: {polluted_status}.
                - If you tell the conversion to silently drop offenders (`errors="coerce"`): mean = **{polluted_silent_drop:.2f} mg/L**, computed over **{int((pd.to_numeric(crp_polluted['value'], errors='coerce').notna()).sum())} of 18** values.
                """
            ),
            mo.callout(
                mo.md(
                    "**The silent-drop version is the dangerous one.** It returns a plausible number. It is computed over fifteen specimens instead of eighteen. The three values it dropped were the lowest. The mean shifts up. No warning fires. The CRP trajectory in the slide deck reads worse than the patient's actual trajectory."
                ),
                kind="warn",
            ),
        ]
    )
    return


@app.cell
def _(mo):
    type_quiz = mo.ui.radio(
        options=[
            "The program throws a TypeError and refuses to compute anything.",
            "The program returns a plausible mean computed over a quietly smaller sample.",
            "The program computes the correct mean because pandas auto-converts numeric-looking strings.",
            "The program returns NaN for every operation on the column.",
        ],
        label=(
            "Which of these is the most common failure mode when a numeric column "
            "accidentally contains text?"
        ),
    )
    type_quiz
    return (type_quiz,)


@app.cell
def _(mo, type_quiz):
    if type_quiz.value is None:
        type_quiz_feedback = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif type_quiz.value.startswith("The program returns a plausible mean"):
        type_quiz_feedback = mo.callout(
            mo.md(
                "**Correct.** The TypeError version is the safe one because it tells you something is wrong. "
                "The plausible-mean-over-fewer-rows version is the one that ships to the slide deck. "
                "`pandas.to_numeric(..., errors='coerce')` and similar 'be permissive' patterns are everywhere "
                "in clinical pipelines, and they all have this failure mode. The fix is to handle the non-numeric "
                "values on purpose, not to coerce them away silently."
            ),
            kind="success",
        )
    else:
        type_quiz_feedback = mo.callout(
            mo.md(
                "**Not quite.** The TypeError option is what stricter tools do, and it's the safest outcome because it tells you something is wrong. "
                "The auto-convert option doesn't happen by default (pandas reads the whole column as text once any non-numeric cell appears). "
                "The all-NaN option happens with some tools but not with the default `errors='coerce'` behavior. "
                "The dangerous case, the one that ships, is the plausible mean computed over a quietly smaller sample."
            ),
            kind="warn",
        )
    type_quiz_feedback
    return (type_quiz_feedback,)


@app.cell
def _(mo):
    mo.md(r"""
    ## 3. Dates: the special nightmare

    Dates look like text. They behave like text in some operations and like numbers in others. They have at least six common written formats. Two of those formats are ambiguous: in `03/04/2024`, is the third the day or the month? It depends on the country the parser thinks it's in, and "the country the parser thinks it's in" is not a property the data carries.

    Below are five ways the same specimen date for Ms. Reyes might be written, and what each one parses to.
    """)
    return


@app.cell
def _(mo, pd):
    _raw_dates = [
        ("ISO 8601, what we want", "2024-04-17"),
        ("US convention", "04/17/2024"),
        ("EU convention", "17/04/2024"),
        ("Ambiguous, parser-dependent", "04/05/2024"),
        ("Free text from a discharge summary", "April 17, 2024"),
        ("Excel that drifted", "2024-04-16T23:00:00-01:00"),
    ]
    _date_rows = []
    for _label, _raw in _raw_dates:
        try:
            _parsed_default = str(pd.to_datetime(_raw))
        except Exception as _exc:  # noqa: BLE001
            _parsed_default = f"error: {_exc}"
        try:
            _parsed_dayfirst = str(pd.to_datetime(_raw, dayfirst=True))
        except Exception as _exc:  # noqa: BLE001
            _parsed_dayfirst = f"error: {_exc}"
        _date_rows.append(
            {
                "what the cell looks like": _raw,
                "format flavor": _label,
                "parsed (default, US-first)": _parsed_default,
                "parsed (dayfirst=True, EU-first)": _parsed_dayfirst,
            }
        )
    dates_table = pd.DataFrame(_date_rows)
    mo.vstack(
        [
            mo.ui.table(dates_table, selection=None),
            mo.callout(
                mo.md(
                    "**Look at the row marked 'Ambiguous, parser-dependent'.** "
                    "The same six-character string parses to April 5 under US conventions and to May 4 under EU conventions. "
                    "Nothing in the cell tells you which one is right. Nothing throws an error. The clinical conclusion is just off by a month for every ambiguous cell in the column. "
                    "And `04/13/2024` is fine in both conventions because there is no thirteenth month, which gives the spot-check a false reassurance: half the rows look identical between the two parsings, so the half that disagree go unnoticed."
                ),
                kind="warn",
            ),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    **The Excel-drifted row** is its own genre. The original specimen date was April 17 at the start of the day in clinic-local time. Somewhere between the lab system, the spreadsheet, and the export pipeline, a time zone disagreement shifted the timestamp back into the prior calendar day. Time zones change the calendar date for two hours every night. A pipeline that hands dates around as timestamps with mixed time zone information will lose, on average, one out of every twelve dates to this drift. None of them throw.

    The fix is to handle dates the way you would handle a controlled substance:

    - Use ISO 8601 (`YYYY-MM-DD`) end to end, written without time zone unless you actually need the timestamp.
    - Parse explicitly with a format string (`pd.to_datetime(col, format="%Y-%m-%d")`), not by hoping.
    - When parsing fails, look at the offending cells before deciding how to handle them.
    - If you need a timestamp, write the time zone alongside it (`Europe/London`, not "UTC + 1") so daylight saving time is somebody else's problem.

    The notebook above used `pd.to_datetime` with default behavior to make the failure modes visible. In production work, the default behavior is what you want to avoid.
    """)
    return


@app.cell
def _(mo):
    date_quiz = mo.ui.radio(
        options=[
            "All dates parse correctly because pandas auto-detects the format.",
            "Site A dates parse correctly. All Site B dates fail with an error.",
            "Site A dates parse correctly. Site B dates parse, but every Site B date where the day is 12 or less gets the day and month swapped silently.",
            "All dates fail to parse because pandas does not infer date formats.",
        ],
        label=(
            "A clinical research analyst loads a CSV from two different sites. Site A "
            "writes dates as YYYY-MM-DD. Site B writes dates as DD/MM/YYYY. The analyst "
            "calls pd.to_datetime() with default settings. Which dates parse incorrectly "
            "without warning?"
        ),
    )
    date_quiz
    return (date_quiz,)


@app.cell
def _(date_quiz, mo):
    if date_quiz.value is None:
        date_quiz_feedback = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif date_quiz.value.startswith("Site A dates parse correctly. Site B dates parse, but"):
        date_quiz_feedback = mo.callout(
            mo.md(
                "**Correct.** Pandas defaults to US-first month/day order. A Site B row of `03/04/2024` "
                "parses as March 4, 2024 instead of April 3, 2024. Rows where the day exceeds 12 "
                "(13/04/2024 and so on) cannot be interpreted as month/day, so they either fail "
                "or fall through, depending on version. The dangerous rows are the ones that "
                "succeeded silently. The fix is to pass an explicit format string per site."
            ),
            kind="success",
        )
    else:
        date_quiz_feedback = mo.callout(
            mo.md(
                "**Not quite.** Pandas does infer formats, but the inference defaults to US month-first ordering. "
                "Site B's day-first dates fall through with the day and month silently swapped on every row where the day is 12 or less. "
                "Rows where the day exceeds 12 either error or fall through depending on pandas version. "
                "The dangerous rows are the ones that succeeded with the wrong interpretation, not the ones that errored. "
                "The fix is to parse with an explicit per-site format string."
            ),
            kind="warn",
        )
    date_quiz_feedback
    return (date_quiz_feedback,)


@app.cell
def _(mo):
    mo.md(r"""
    ## 4. Categories and codes

    Most non-numeric clinical data is not free text. It's categorical, meaning it draws from a fixed set of allowed values. Sex. Race. Encounter class. Diagnosis. Medication. Specimen type. Each of these has a **value set**: the list of values the column is allowed to take.

    Same fact, different encodings. The seven cells below all say "this patient is female." If they end up in the same column without being reconciled, "what fraction of the cohort is female" is unanswerable, because at least four of them won't match each other on a string comparison.
    """)
    return


@app.cell
def _(mo, pd):
    sex_encodings = pd.DataFrame(
        {
            "system": [
                "free text",
                "free text",
                "free text",
                "free text (whitespace)",
                "Epic Clarity (`SEX_C`)",
                "Cerner Millennium (`sex_cd`)",
                "FHIR R4 `Patient.gender`",
            ],
            "value as written": ["Female", "F", "f", "Female ", "2", "362", "female"],
            "meaning": ["female"] * 7,
        }
    )
    mo.vstack(
        [
            mo.ui.table(sex_encodings, selection=None),
            mo.md(
                "A naive `df['sex'].value_counts()` on a merged table of these seven rows reports seven distinct values. "
                "A correctly written analysis reports one."
            ),
            mo.callout(
                mo.md(
                    "**This is what a coding system buys you.** A coding system is a published vocabulary that names allowed values and what each one means. "
                    "FHIR's `Patient.gender` is `{male, female, other, unknown}`, lowercase, no whitespace. "
                    "LOINC is a coding system for lab tests. SNOMED CT for clinical findings. ICD-10-CM for billable diagnoses. RxNorm for medications. UCUM for units of measure. "
                    "A column whose values come from a coding system is unambiguous; a column whose values come from 'whatever the EHR happened to render in the export' is not."
                ),
                kind="info",
            ),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    Codes also get the same lab represented in multiple ways. The `test_name` column in Ms. Reyes's `labs.csv` is "C-reactive protein" written out. The `loinc` column next to it is `1988-5`. The two say the same thing. The first is human-friendly text. The second is a coded value from the LOINC system.

    When you exchange labs across institutions, only the second one travels safely. "C-reactive protein" might be spelled "CRP" at one site, "C-reactive protein, high sensitivity" at another (which is a different test!), or "C reactive protein" at a third. LOINC `1988-5` is the same code at every site that uses LOINC. The text is for humans; the code is for the analysis. Both columns exist because the table needs to be readable by both.

    The clinical informatics rule is: **trust the code column, render the text column.** If the two ever disagree, the code wins and the text is wrong.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 5. The five-question audit

    Now we put the four ideas together. Below is a synthetic export of a small RA cohort's CRP labs that you might inherit at the start of a project. Eight columns, sixteen rows, mostly plausible-looking. Some columns are correct. Some have type errors hiding in plain sight.

    Run the five-question audit on the column dropdown. The questions are:

    1. **What type does the column claim to be?** What did `read_csv` decide?
    2. **What type does the column need to be?** What is the clinical concept stored in this column?
    3. **Where are the offenders?** If the two disagree, which rows are responsible?
    4. **Why is each offender there?** Typo, sentinel value, mixed units, wrong column, real missing, or something else?
    5. **What is the fix?** Drop, replace, separate, or escalate.

    The notebook walks the first column for you. The second is yours to audit, with the answer revealed when you commit one.
    """)
    return


@app.cell
def _(mo, pd):
    audit = pd.DataFrame(
        {
            "patient_id": [
                "ER-001", "ER-002", "ER-003", "ER-001", "ER-004",
                "ER-002", "ER-003", "ER-001", "ER-005", "ER-002",
                "ER-003", "ER-001", "ER-004", "ER-002", "ER-005",
                "ER-003",
            ],
            "specimen_date": [
                "2024-04-17", "2024-04-18", "04/19/2024", "2024-05-22", "5/3/2024",
                "2024-05-30", "2024-06-04", "2024-06-25", "June 7, 2024", "2024-07-12",
                "2024-07-18", "2024-07-30", "08/14/24", "2024-08-19", "2024-08-21",
                "2024-09-02",
            ],
            "test_name": [
                "C-reactive protein", "C-reactive protein", "CRP", "C-reactive protein",
                "C-reactive protein (high sensitivity)", "C-reactive protein", "C-reactive protein",
                "C-reactive protein", "C-reactive protein", "C-reactive protein",
                "C reactive protein", "C-reactive protein", "C-reactive protein",
                "C-reactive protein", "C-reactive protein", "C-reactive protein",
            ],
            "loinc": [
                "1988-5", "1988-5", "1988-5", "1988-5", "30522-7",
                "1988-5", "1988-5", "1988-5", "1988-5", "1988-5",
                "1988-5", "1988-5", "1988-5", "1988-5", "1988-5", "1988-5",
            ],
            "value": [
                "18.7", "12.4", "9.8", "14.1", "0.34",
                "11.2", "8.6", "11.4", "21.5 mg/L", "10.8",
                "7.9", "13.8", "<5.0", "6.4", "missing", "9.2",
            ],
            "unit": [
                "mg/L", "mg/L", "mg/L", "mg/L", "mg/L",
                "mg/L", "mg/L", "mg/L", "", "mg/L",
                "mg/L", "mg/L", "mg/L", "mg/L", "mg/L", "mg/L",
            ],
            "interpretation": [
                "H", "H", "H", "H", "N",
                "H", "H", "H", "H", "H",
                "H", "H", "N", "H", "", "H",
            ],
            "patient_sex": [
                "Female", "F", "Female", "Female", "f",
                "F", "Female", "Female", "Female ", "F",
                "Female", "Female", "F", "Female", "2", "F",
            ],
        }
    )
    audit.index = range(1, len(audit) + 1)
    audit.index.name = "row"
    mo.vstack(
        [
            mo.md(
                "**Inherited export. Audit this.** Rows are numbered from 1 to 16 in the leftmost column for easy reference in the reveal below."
            ),
            mo.ui.table(audit, selection=None),
        ]
    )
    return (audit,)


@app.cell
def _(audit, mo, pd):
    audit_types = pd.DataFrame(
        {
            "column": audit.columns,
            "pandas dtype": [str(t) for t in audit.dtypes],
        }
    )
    mo.vstack(
        [
            mo.md(
                "**What `read_csv` decided about each column.** Walk this against your own answer to question 2: what should the column be?"
            ),
            mo.ui.table(audit_types, selection=None),
        ]
    )
    return


@app.cell
def _(mo):
    sample_walk = mo.md(
        r"""
        ### Sample audit: `value`

        **1. What type does the column claim to be?** `object` (text).

        **2. What type does the column need to be?** Numeric. CRP is a continuous measurement in mg/L; the column needs to support `mean`, `median`, range, and threshold comparisons.

        **3. Where are the offenders?** Three rows.
        - Row 9: `"21.5 mg/L"`. A unit got pasted into the value cell.
        - Row 13: `"<5.0"`. Sentinel value for "below limit of quantification."
        - Row 15: `"missing"`. A missing-value placeholder written as a word.

        **4. Why is each offender there?**
        - Row 9: probably a copy-paste from a flowsheet that rendered "value + unit" together. The unit also lives in the `unit` column already; splitting "21.5" out and dropping the duplicated unit is the fix.
        - Row 13: a real measurement that the lab couldn't quantify. This is a data-recording convention from the analyzer. Replace with `5.0` (the LLOQ) and flag, replace with `NaN`, or keep as a censored value. Pick on purpose.
        - Row 15: a missing value with a non-standard placeholder. Convert to `NaN`. This is Track 03 territory.

        **5. What is the fix?**
        ```python
        # 1) strip the leaked unit
        df.loc[df["value"].str.contains("mg/L", na=False), "value"] = (
            df["value"].str.replace(" mg/L", "", regex=False)
        )

        # 2) handle the LLOQ sentinel explicitly
        df["value_below_lloq"] = df["value"] == "<5.0"
        df.loc[df["value_below_lloq"], "value"] = "5.0"

        # 3) treat the "missing" string as missing
        df["value"] = df["value"].replace({"missing": pd.NA})

        # 4) finally, convert to numeric
        df["value"] = pd.to_numeric(df["value"], errors="raise")
        ```

        Note `errors="raise"`. After we've handled the known offenders, a remaining text cell is a surprise, and we want it to surface as an error rather than be silently dropped.
        """
    )

    sample_walk
    return


@app.cell
def _(audit, mo):
    pick_col = mo.ui.dropdown(
        options=[c for c in audit.columns if c != "value"],
        value="specimen_date",
        label="Pick a column to audit. The reveal opens after you write at least one full sentence.",
    )
    pick_col
    return (pick_col,)


@app.cell
def _(mo):
    user_audit = mo.ui.text_area(
        placeholder=(
            "Question 1: what type does pandas say this column is?\n"
            "Question 2: what type does it need to be?\n"
            "Question 3: where are the offenders?\n"
            "Question 4: why are they there?\n"
            "Question 5: what's the fix?"
        ),
        rows=10,
        full_width=True,
        label="Your audit (one full sentence minimum to unlock the reveal)",
    )
    user_audit
    return (user_audit,)


@app.cell
def _(mo, pick_col, user_audit):
    raw = user_audit.value or ""
    mo.stop(
        len(raw.strip()) < 40,
        mo.callout(
            mo.md(
                "_Write a sentence or two about the column you picked, then the reveal will open below._"
            ),
            kind="neutral",
        ),
    )

    reveals = {
        "patient_id": mo.md(
            r"""
            **Sample audit: `patient_id`.**

            1. **Claim:** `object` (text).
            2. **Need:** Categorical or text. A patient identifier is not a number you do math on; "average patient ID" is meaningless. Storing it as text is correct.
            3. **Offenders:** none on type. But this column also doesn't have a coding system attached. `ER-001` is an MRN-shaped string; another site's `ER-001` may be a different patient. In a multi-site study, you'd want either a globally unique identifier or a `(system, id)` pair, not a bare `ER-001`.
            4. **Why:** local MRN exports default to bare strings.
            5. **Fix:** if multi-site, add an `identifier_system` column or build a `(system, value)` tuple. If single-site, fine as is, but document the assumption.
            """
        ),
        "specimen_date": mo.md(
            r"""
            **Sample audit: `specimen_date`.**

            1. **Claim:** `object` (text).
            2. **Need:** Date. We sort on it, group by month for trend plots, take differences between consecutive specimens.
            3. **Offenders:** at least four rows.
                - Row 3: `"04/19/2024"`. US-style format mixed in with ISO.
                - Row 5: `"5/3/2024"`. Ambiguous: May 3 in US, March 5 in EU.
                - Row 9: `"June 7, 2024"`. Free text.
                - Row 13: `"08/14/24"`. Two-digit year.
            4. **Why:** these came from at least two different upstream systems, each writing dates its own way. The free-text row probably came from a discharge summary that got OCR'd into the export.
            5. **Fix:** parse with an explicit per-source format if you know the source, or use `pd.to_datetime(..., errors="coerce")` and **then immediately list the rows that became NaT** so you can fix them by hand. Never let the silent coercion ship to analysis. End state: a single `datetime64[ns]` column in ISO 8601.
            """
        ),
        "test_name": mo.md(
            r"""
            **Sample audit: `test_name`.**

            1. **Claim:** `object` (text).
            2. **Need:** Categorical, drawn from a value set (the lab names in scope for the study).
            3. **Offenders:** four rows have name variants for what should be one lab.
                - "C-reactive protein" (most rows).
                - "CRP" (row 3): abbreviation.
                - "C reactive protein" (row 11): missing hyphen.
                - "C-reactive protein (high sensitivity)" (row 5): actually a *different* lab. hsCRP and CRP have different reference ranges and different LOINC codes. The `loinc` column for row 5 is `30522-7`, which is hsCRP. The `value` of `0.34` for that row is plausible as hsCRP and impossibly low as standard CRP.
            4. **Why:** site-specific text rendering, and one row that was a different test altogether.
            5. **Fix:** **trust the code, render the text.** Group by `loinc`, not by `test_name`. The row 5 hsCRP either needs to be analyzed separately or scaled, depending on your study. Either way, don't merge hsCRP and CRP rows just because the text-string column matches.
            """
        ),
        "loinc": mo.md(
            r"""
            **Sample audit: `loinc`.**

            1. **Claim:** `object` (text).
            2. **Need:** Categorical code from the LOINC value set. Storing as text is correct because LOINC codes are not numbers you compute on (they happen to look numeric, but the dash-separated check digit is not arithmetic).
            3. **Offenders:** one row.
                - Row 5: `30522-7` (hsCRP) is not the same lab as `1988-5` (CRP). The test_name column for that row was also flagged in the prior audit.
            4. **Why:** an hsCRP order got pulled into a CRP cohort because the text name was similar.
            5. **Fix:** filter on `loinc == "1988-5"` before summarizing. If you want both labs, treat them as separate measurements with a join key of (patient, date) and a value column per lab.
            """
        ),
        "unit": mo.md(
            r"""
            **Sample audit: `unit`.**

            1. **Claim:** `object` (text).
            2. **Need:** Categorical, ideally from UCUM. Units must agree across rows before any aggregation is legal.
            3. **Offenders:** one row.
                - Row 9: `""` (empty string). The unit got dropped because someone pasted "21.5 mg/L" into the value column instead.
            4. **Why:** upstream entry error.
            5. **Fix:** after you separate the leaked unit out of `value` (see the worked example for `value`), the unit cell for row 9 fills back in as `"mg/L"`. Then check the whole column for uniformity. If even one row says `"mg/dL"` while the rest say `"mg/L"`, you must convert before averaging. UCUM rules: `mg/L` and `mg/dL` differ by a factor of 10.
            """
        ),
        "interpretation": mo.md(
            r"""
            **Sample audit: `interpretation`.**

            1. **Claim:** `object` (text).
            2. **Need:** Categorical, from the small set `{N (normal), L (low), H (high), HH (critical high), LL (critical low)}`. These are flag values, typically from HL7 Table 0078.
            3. **Offenders:** one row.
                - Row 15: `""` (empty). Missing flag.
            4. **Why:** the corresponding value column for row 15 was the string `"missing"`. When the value is missing, the interpretation is missing too. This is a Track 03 problem (different kinds of missingness; this one is informative).
            5. **Fix:** convert empty strings to `NaN` and decide how to handle the missing-flag rows separately from rows with values. Critically, the missing-flag *should not* be replaced with `"N"`. That would silently re-classify missing measurements as normal.
            """
        ),
        "patient_sex": mo.md(
            r"""
            **Sample audit: `patient_sex`.**

            1. **Claim:** `object` (text).
            2. **Need:** Categorical from a defined value set (FHIR R4 would say `{male, female, other, unknown}`, lowercase, no whitespace).
            3. **Offenders:** at least three distinct encodings.
                - "Female" (most rows).
                - "F" (multiple rows).
                - "f" (row 5): lowercase variant.
                - "Female " (row 9): trailing whitespace.
                - "2" (row 15): Epic-style numeric code from `SEX_C`.
            4. **Why:** the export pulled from at least two upstream systems and didn't normalize.
            5. **Fix:** map all variants to the FHIR set during ingest. After mapping, this column has one allowed value (`female`) across all sixteen rows. Then audit: are there any other values in the source that the mapping missed?
            """
        ),
    }
    reveal = reveals.get(pick_col.value, mo.md("_pick a column above_"))
    reveal
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Where this leaves you

    Four ideas in place:

    1. **Every column has a type, and the type is the rule for what operations are legal.** The type defaults pandas (or Excel, or SQL, or your EHR's research warehouse) infers are guesses. Sometimes the guesses are wrong in ways no error message will tell you.
    2. **A numeric column quietly turning into a text column** is the single most common type bug in clinical analyses. It looks like the same column. It computes a plausible mean. The mean is wrong. The fix is to handle the non-numeric values on purpose, not to coerce them silently.
    3. **Dates are their own nightmare.** Use ISO 8601 end to end. Parse explicitly with a format string. When parsing fails, look at the failing cells before deciding what to do.
    4. **Categorical columns need a value set, and ideally a coding system.** Without one, the same fact ends up written multiple ways and the cohort can't be counted. With one, you trust the code, render the text, and merge on the code.

    Track 02 picks up from here. Once your columns have the right types, the next question is: **is each cell holding one fact?** Untidy clinical data fails that test in characteristic ways, and reshaping it is the most-used clinical data wrangling move that isn't joins.
    """)
    return


if __name__ == "__main__":
    app.run()
