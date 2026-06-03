"""Track 04: Data provenance and documentation.

No visible code. The notebook presents the three components of data
provenance (lineage, transformation log, data dictionary), uses Ms. Reyes's
real synthetic CRP series to demonstrate that four defensible choices for
"baseline CRP" yield very different values, and shows the data-dictionary
and transformation-log entries that make a column self-describing.

WASM-safe: no shared imports, no data files, no relative paths.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    REYES_CRP = [
        {"date": "2022-02-14", "value": 42.1, "context": "pre-diagnosis workup; 3 months of symptoms"},
        {"date": "2022-05-22", "value": 28.4, "context": "post-diagnosis; MTX started"},
        {"date": "2022-08-18", "value": 19.2, "context": "MTX titration"},
        {"date": "2022-11-09", "value": 16.8, "context": "MTX 25 mg + folic acid"},
        {"date": "2023-02-15", "value": 22.5, "context": "flare; oral steroid burst"},
        {"date": "2023-05-23", "value": 31.6, "context": "MTX-only inadequate"},
        {"date": "2023-08-21", "value": 26.9, "context": "biologic discussion"},
        {"date": "2023-11-13", "value": 33.4, "context": "DAS28 trending up"},
        {"date": "2024-01-08", "value": 36.2, "context": "pre-biologic decision visit"},
        {"date": "2024-04-17", "value": 18.7, "context": "8 weeks on adalimumab"},
        {"date": "2024-07-22", "value": 14.1, "context": "good response"},
        {"date": "2024-10-30", "value": 11.4, "context": "best response to date"},
        {"date": "2025-02-04", "value": 13.8, "context": "stable"},
        {"date": "2025-05-12", "value": 16.5, "context": "mild rise"},
        {"date": "2025-08-19", "value": 14.9, "context": "stable"},
        {"date": "2025-11-21", "value": 18.2, "context": "viral illness 2 weeks prior"},
        {"date": "2026-02-10", "value": 21.4, "context": "interval flare"},
        {"date": "2026-04-28", "value": 19.8, "context": "current visit"},
    ]

    def compute_baseline(strategy, series):
        import datetime

        if strategy == "Earliest available draw":
            chosen = series[0]
            note = (
                "The earliest draw on record. Includes the pre-diagnosis workup, "
                "which is rarely the right choice for an analysis of disease activity "
                "on treatment."
            )
        elif strategy == "First draw after diagnosis":
            chosen = next(s for s in series if s["date"] >= "2022-03-01")
            note = (
                "First draw after the diagnosis date (2022-03). Excludes the "
                "workup-era draw. The right choice for an analysis indexed at "
                "diagnosis."
            )
        elif strategy == "Pre-biologic (last draw before adalimumab start)":
            chosen = max(
                (s for s in series if s["date"] < "2024-02-01"),
                key=lambda s: s["date"],
            )
            note = (
                "Last draw before adalimumab started (2024-02). The right choice "
                "for an analysis evaluating the biologic's effect on inflammation."
            )
        else:
            target = datetime.date.fromisoformat("2024-04-01")
            chosen = min(
                series,
                key=lambda s: abs(
                    (datetime.date.fromisoformat(s["date"]) - target).days
                ),
            )
            note = (
                "Draw closest to the study enrollment date (2024-04). The standard "
                "choice for an analysis indexed at enrollment."
            )
        n_after = sum(1 for s in series if s["date"] > chosen["date"])
        return chosen["date"], chosen["value"], n_after, note

    return REYES_CRP, compute_baseline, mo


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 04: Data provenance and documentation

        You are asked for the baseline CRP for Ms. Reyes. Below is what you find in her chart: eighteen CRP draws across four years. The question is which one is "the" baseline. Four defensible choices yield baseline values ranging from 18.7 to 42.1 mg/L, a factor of more than two. Every subsequent analysis depends on which value was picked. Three years from now no one (including you) will remember which one it was unless it was written down at the time.

        Data provenance is the structural answer. Provenance is the written record of where the data came from, what was done to it, and which choices were made along the way. It lives outside the code, in plain English, and it is what makes a column of numbers self-describing. The track presents the three components of provenance, demonstrates the baseline-choice problem on Ms. Reyes's actual CRP series, and shows the two documentation artifacts that record the choices.
        """
    )
    return


@app.cell
def _(REYES_CRP, mo):
    _header = f"{'date':<10}  {'CRP (mg/L)':<10}  clinical context"
    _rule = "-" * 78
    _rows = [
        f"{r['date']:<10}  {r['value']:<10.1f}  {r['context']}"
        for r in REYES_CRP
    ]
    _series = "\n".join([_header, _rule] + _rows)
    _body = (
        "## Ms. Reyes's CRP series\n\n"
        "Eighteen draws over four years. The reference range is 0 to 5 mg/L. "
        "Diagnosis was March 2022, methotrexate started then, adalimumab added in "
        "February 2024, study enrollment in April 2024.\n\n"
        f"```\n{_series}\n```\n"
    )
    mo.md(_body)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Three components of provenance

        Provenance documents three things, separately. Each component answers a different question, and the three are not interchangeable.

        | Component | Question it answers | Form it takes |
        |---|---|---|
        | **Lineage** | Where did this dataset come from? What source records, on what date, under what query? | A note at the top of the dataset, or a metadata file. |
        | **Transformation log** | What was done to the source data to produce this dataset? | A run order of named scripts plus a one-line description of each. |
        | **Data dictionary** | What does each column mean, in what units, with what allowed values, derived how? | One row per column. |

        Lineage answers "where did this come from." The transformation log answers "what was done to it." The data dictionary answers "what does each column mean now." A dataset that has any one of the three without the other two is partially documented.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A worked example: which draw is "baseline"?

        Ms. Reyes was diagnosed with seropositive RA in March 2022, started methotrexate then, and was switched to adalimumab plus methotrexate in February 2024. She enrolled in an observational study of biologic response in April 2024. Four definitions of her "baseline CRP" are all defensible. Each rests on a different choice of indexing point, and each is the right answer for a different analytic question.
        """
    )
    return


@app.cell
def _(mo):
    strategy = mo.ui.dropdown(
        options=[
            "Earliest available draw",
            "First draw after diagnosis",
            "Pre-biologic (last draw before adalimumab start)",
            "Closest draw to study enrollment (2024-04)",
        ],
        value="Earliest available draw",
        label="Baseline definition",
    )
    mo.vstack(
        [
            mo.md(
                "**Pick a baseline definition.** Each gives a different value."
            ),
            strategy,
        ]
    )
    return (strategy,)


@app.cell
def _(REYES_CRP, compute_baseline, mo, strategy):
    _d, _v, _n, _note = compute_baseline(strategy.value, REYES_CRP)
    _body = (
        "### Baseline draw under this strategy\n\n"
        f"**Date:** {_d}  \n"
        f"**Value:** {_v} mg/L (reference range 0 to 5 mg/L)  \n"
        f"**Follow-up draws available:** {_n}\n\n"
        f"{_note}"
    )
    mo.callout(mo.md(_body), kind="neutral")
    return


@app.cell
def _(REYES_CRP, compute_baseline, mo):
    _strategies = [
        "Earliest available draw",
        "First draw after diagnosis",
        "Pre-biologic (last draw before adalimumab start)",
        "Closest draw to study enrollment (2024-04)",
    ]
    _rows = []
    for _s in _strategies:
        _d, _v, _n, _ = compute_baseline(_s, REYES_CRP)
        _rows.append(f"| {_s} | {_d} | {_v} mg/L | {_n} |")
    _tbl = "\n".join(_rows)
    _body = (
        "## What if a different choice had been made\n\n"
        "The four defensible strategies, side by side. Same patient, same chart, "
        "four very different baselines.\n\n"
        "| Strategy | Date chosen | Baseline CRP | Follow-up draws available |\n"
        "|---|---|---|---|\n"
        f"{_tbl}\n\n"
        "Whichever strategy is right for a given study, the four are not "
        "interchangeable, and the values are separated by a factor of more "
        "than two. A paper that reports a baseline value without saying which "
        "strategy produced it has not defined its baseline."
    )
    mo.md(_body)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Two artifacts hold the provenance

        The interactive above changed the answer by changing the input. The structural answer is to record the definition (and the units, and the cohort criteria, and the source mapping) in a place the next reader will find. Two artifacts hold that record. The data dictionary documents each column of the analysis dataset. The transformation log documents the steps that produced the dataset.

        ### Data dictionary

        One row per column. The `crp_baseline` column from Ms. Reyes's analysis dataset in data-dictionary form:

        | Field | Value |
        |---|---|
        | **Column** | `crp_baseline` |
        | **Description** | Baseline serum C-reactive protein for the index analysis. |
        | **Definition of baseline** | Closest available CRP draw within 90 days of the study enrollment date (2024-04), looking backward first then forward. |
        | **Units** | mg/L |
        | **Reference range** | 0 to 5 mg/L (institutional cutoff). |
        | **Allowed values** | Non-negative real. The cleaning script drops rows with negative or zero values as entry errors (2 rows dropped). |
        | **Assay** | Standard CRP, central lab. High-sensitivity CRP results from a different LOINC code were excluded. |
        | **Below detection limit** | Values reported as `<0.5 mg/L` were recoded to `0.25 mg/L` (midpoint of the lower-limit interval). 11 rows recoded. |
        | **Source field** | `LAB_RESULT.value_num` in the EHR export, joined on `lab_code = '1988-5'` (LOINC for CRP). |
        | **Derivation** | Direct copy from source; no unit conversion (the source reports mg/L). |
        | **Missingness** | Missing if no qualifying CRP draw exists in the 90-day window. 14 of 1,247 patients excluded. |

        ### Transformation log

        One entry per script that touches the dataset, in the order the scripts run. The CRP column's transformation log:

        ```
        01-clean-labs.py        2024-01-09  Parse date column to date type. Drop 2
                                            rows with CRP recorded as negative
                                            (entry errors). Recode 11 below-detection
                                            values to 0.25 mg/L. Exclude rows whose
                                            lab_code is the high-sensitivity assay.
        02-build-cohort.py      2024-01-11  Filter to the RA cohort (n=1247). Pull the
                                            CRP draw closest to enrollment (2024-04)
                                            within +/- 90 days; backward preferred.
                                            Exclude 14 patients with no draw in window.
        03-make-figures.py      2024-01-16  Aggregate CRP by week. Median + IQR (not
                                            mean) because the distribution is
                                            right-skewed. See commit 4d09c87.
        ```

        The log is the run order of the named scripts, with a one-line description of what each script does and a back-reference to the commit (Track 03) that explains why. The code is the operational definition; the log is the human-readable index into the code.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            **Cross-reference (Course 07, OMOP). No standard is lossless.** The OMOP capstone of Course 07 closes on the reflection that mapping an EHR record into the OMOP common data model loses information: a free-text severity collapses into a categorical concept, a local lab code maps to a LOINC that does not exactly match, a unit is coerced, a measurement context is dropped. The work of provenance is to document what was lost and where. A `crp_baseline` whose source field reads only "EHR" has had its provenance silently destroyed. The data dictionary and the transformation log are where the lossy decisions get written down. Together with version control (Track 03) they make the OMOP mapping defensible to a reviewer who asks how the number got there.
            """
        ),
        kind="warn",
    )
    return


@app.cell
def _(mo):
    prov_quiz = mo.ui.radio(
        options=[
            "The entry does not state the unit of measurement.",
            "The entry does not define which draw was used as the baseline.",
            "The entry does not record the source field or LOINC code.",
            (
                "All three. The entry says only that the column contains a CRP "
                "baseline, which the reader could infer from the column name."
            ),
        ],
        label=(
            "A reviewer reads the manuscript and notes that the mean baseline CRP "
            "is 27.4 mg/L. They ask the corresponding author for the data dictionary. "
            "The dictionary entry for `crp_baseline` reads, in full: \"baseline CRP "
            "value.\" What is the load-bearing problem with this entry?"
        ),
    )
    prov_quiz
    return (prov_quiz,)


@app.cell
def _(mo, prov_quiz):
    if prov_quiz.value is None:
        _resp = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif prov_quiz.value.startswith("All three"):
        _resp = mo.callout(
            mo.md(
                "**Correct.** The data dictionary's job is to make the column "
                "self-describing. The entry as written is the column name with the "
                "word \"value\" added; it does not actually define anything. Three "
                "independent questions are all left open. The unit (mg/L and mg/dL "
                "differ by a factor of ten and are both in clinical use). The choice "
                "of draw (the four defensible candidates from the interactive above "
                "range from 18.7 to 42.1, a factor of more than two). The source "
                "mapping (which EHR lab code was treated as CRP, since institutions "
                "vary in whether they distinguish standard and high-sensitivity CRP "
                "and how they store below-detection-limit results). The published "
                "analysis depends on all three; the dictionary entry documents none "
                "of them."
            ),
            kind="success",
        )
    elif prov_quiz.value.startswith("The entry does not state the unit"):
        _resp = mo.callout(
            mo.md(
                "**The unit is one of the missing pieces, and it matters (mg/L "
                "and mg/dL differ by a factor of ten),** but it is one of three. "
                "The choice of which draw is the baseline is undocumented too, "
                "and the four defensible candidates from the interactive above "
                "range from 18.7 to 42.1 mg/L. The source field (which EHR lab "
                "code was treated as CRP, and whether high-sensitivity results "
                "were included) is missing as well. A complete dictionary entry "
                "would document all three."
            ),
            kind="warn",
        )
    elif prov_quiz.value.startswith("The entry does not define which draw"):
        _resp = mo.callout(
            mo.md(
                "**Which draw is used as baseline is one of the missing pieces, "
                "and the interactive above showed it can change the value by a "
                "factor of more than two,** but it is one of three. The unit "
                "(mg/L vs mg/dL) is not documented either, and the source mapping "
                "(which EHR lab code maps to this column) is also missing. A "
                "complete dictionary entry would document all three."
            ),
            kind="warn",
        )
    else:
        _resp = mo.callout(
            mo.md(
                "**The source-field mapping is one of the missing pieces, and it "
                "matters because the same conceptual lab can be stored under "
                "different codes or include different assays,** but it is one of "
                "three. The unit (mg/L vs mg/dL) is undocumented, and the choice "
                "of which draw is the baseline (the four candidates range from "
                "18.7 to 42.1 mg/L) is undocumented as well. A complete dictionary "
                "entry would document all three."
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

        Project organization (Track 02) gives a stranger a folder they can enter. Version control (Track 03) gives them the chain of decisions over time. Provenance (this track) gives them the column of numbers in human-readable form. The fourth piece, the one that closes the loop, is sharing: what goes out with the paper, what goes into a controlled-access repository, what stays behind because privacy or contract prevents release. Track 05 covers what to share, how to share it, and the reporting guidelines that force the right details into the open before publication.
        """
    )
    return


if __name__ == "__main__":
    app.run()
