"""Track 02: Project organization for reproducibility.

No visible code. The notebook presents the four organizational decisions
that make a data project rerunnable, lets the reader configure each decision
on a deliberately messy synthetic RA project folder, and shows which
reproducibility questions the chosen configuration answers and which it
leaves open.

WASM-safe: no shared imports, no data files, no relative paths.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    def evaluate_organization(folder, naming, raw, readme):
        answered = []
        unanswered = []

        if folder == "Separated by purpose (data, code, results, docs)":
            answered.append(
                "Where the figure-producing code lives, because `code/` is a "
                "named place separate from data and results."
            )
        elif folder == "Sorted by file type":
            answered.append(
                "Where each file type lives, but not which script produced which figure."
            )
            unanswered.append(
                "Which script produced the figure, because file-type grouping does not "
                "separate inputs, transformations, and outputs."
            )
        else:
            unanswered.append(
                "Where the code lives at all, because data, code, and outputs share the "
                "top level."
            )

        if raw == "Raw data read-only; every transformation in a script that writes a new file":
            answered.append(
                "How to rebuild every processed file from raw, because each transformation "
                "is a script and the raw input still exists."
            )
        elif raw == "Raw data preserved; cleaned copy saved alongside":
            answered.append(
                "That the raw values are still on disk."
            )
            unanswered.append(
                "Exactly how the cleaned version was produced, because no script preserves "
                "the steps that went from raw to processed."
            )
        else:
            unanswered.append(
                "How to recover the original raw values, because the raw file was "
                "overwritten when it was cleaned in place."
            )

        if naming == "Machine-friendly throughout (no spaces, ISO 8601 dates, no FINAL versioning)":
            answered.append(
                "Which version of any file is current, because the sort order is the "
                "history and there is no `FINAL` ambiguity."
            )
        elif naming == "A convention with frequent exceptions":
            unanswered.append(
                "Whether `analysis_final.csv` or `analysis_FINAL_use_this_one.csv` is the "
                "manuscript file, because the convention was not held to."
            )
        else:
            unanswered.append(
                "Which of the three `analysis_final*.csv` files made the manuscript "
                "figure, because the names do not disambiguate them."
            )

        if readme == "README written first, kept current":
            answered.append(
                "Where to start, what the folder structure means, and how to rerun, from "
                "a single document that was written before the project was."
            )
        elif readme == "README written at submission, never updated":
            unanswered.append(
                "Whether the README still describes the project, because it was written "
                "once at submission and the project has moved since."
            )
        else:
            unanswered.append(
                "Where to start at all, because no document describes how the parts "
                "fit together."
            )

        return answered, unanswered

    return evaluate_organization, mo


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 02: Project organization

        A folder contains forty files. The figure in the submitted manuscript was made from one of three CSVs that all begin with `analysis_final`, and no one is now certain which. The raw lab export has been edited in place during cleaning, so the original values are no longer recoverable. There is no document that says how the parts of the project fit together. This folder cannot be rerun, and it cannot be defended.

        Project organization is the structural defense against this state. Four decisions, made early and held to, produce a project that a stranger or its own author can pick up a year later and rerun. None of the four is technically demanding. All four are usually skipped, because their value becomes visible only when the work depends on them, by which time they are expensive to retrofit.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What is in the folder

        ```
        ra-cohort-study/
        ├── analysis_final.csv
        ├── analysis_final_v2.csv
        ├── analysis_FINAL_use_this_one.csv
        ├── clean data.csv
        ├── clean_data_jan2024.csv
        ├── copy of analysis_final.csv
        ├── crp_plot.png
        ├── das28_baseline.csv
        ├── das28_baseline_OLD.csv
        ├── das28_followup.csv
        ├── final figure.png
        ├── helper.R
        ├── labs_master.csv
        ├── labs_master_edited.csv
        ├── manuscript_draft.docx
        ├── manuscript_FINAL.docx
        ├── manuscript_FINAL_revised.docx
        ├── manuscript_FINAL_revised_v2_clean.docx
        ├── my_script.R
        ├── new_helper.R
        ├── notes.txt
        ├── notes_for_paper.txt
        ├── notes_for_paper_v2.txt
        ├── output1.csv
        ├── Patients.xlsx
        ├── patients (1).xlsx
        ├── PATIENTS_FINAL.xlsx
        ├── plot1.png
        ├── plot1_v2.png
        ├── plot.R
        ├── plot_final.png
        ├── README.txt           (empty)
        ├── results.docx
        ├── Results FINAL.docx
        ├── revision response.docx
        ├── script.py
        ├── script2.py
        ├── TODO.txt
        ├── .DS_Store
        └── ~$nalysis.xlsx
        ```

        Four problems are present at once. The raw lab export was overwritten when it was cleaned, so the original values are gone. Several revisions of the cleaning code were made and only the last one is on disk. Three CSVs named `analysis_final*` are byte-for-byte different and the manuscript Methods section does not say which one was used. No README explains how the parts fit together. None of these is the result of laziness. They are the default state of a project that did not commit to any structural decisions up front.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Four decisions are load-bearing

        Four organizational decisions, made early and held to, prevent the four problems above. Each one answers a specific reproducibility question; together they are the structural minimum that allows a project to be rerun.

        1. **Raw data is read-only.** The source files (the EHR export, the lab CSV, the patient list) are never edited in place. Every cleaning or transformation step is a script that reads the raw file and writes a new file. The path from raw to final is reconstructable because the raw is still there.

        2. **The folder structure separates inputs from code from outputs.** A `data/` directory holds the inputs. A `code/` directory holds the scripts. A `results/` directory holds the figures and tables the scripts produce. A reader knows where to look. Anything under `results/` is safe to delete because the code rebuilds it.

        3. **File and variable names are consistent and machine-friendly.** No spaces. Dates in ISO 8601 (`2024-01-08`, which sorts chronologically as a string). No `FINAL` or `FINAL_v2` versioning, because the versioning system is version control (Track 03). Names are predictable, so a search succeeds and a list sorts.

        4. **The README is written first.** The document that describes how the project is meant to work exists before the project does. It states the folder layout, the data sources, the order in which code is run, and the output. Writing it before the code is written forces the structural decisions to be made deliberately, while they are still cheap to change.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            **Structure is the visible part. The invariants that hold it together are the load-bearing part.** A pristine-looking `data/raw/` directory whose files have been silently edited in place is worse than a messy folder where the original CSV is still there. The pristine version looks reproducible without being so. The four decisions below are policies as much as layouts. A team that adopts the folder structure but not the read-only rule for raw data has the appearance of reproducibility without the substance.
            """
        ),
        kind="warn",
    )
    return


@app.cell
def _(mo):
    folder = mo.ui.dropdown(
        options=[
            "Flat (everything at the top level)",
            "Sorted by file type",
            "Separated by purpose (data, code, results, docs)",
        ],
        value="Flat (everything at the top level)",
        label="Folder structure",
    )
    naming = mo.ui.dropdown(
        options=[
            "Whatever I felt like at the time",
            "A convention with frequent exceptions",
            "Machine-friendly throughout (no spaces, ISO 8601 dates, no FINAL versioning)",
        ],
        value="Whatever I felt like at the time",
        label="File and variable naming",
    )
    raw = mo.ui.dropdown(
        options=[
            "Raw data edited in place when it needs fixing",
            "Raw data preserved; cleaned copy saved alongside",
            "Raw data read-only; every transformation in a script that writes a new file",
        ],
        value="Raw data edited in place when it needs fixing",
        label="Raw data policy",
    )
    readme = mo.ui.dropdown(
        options=[
            "No README",
            "README written at submission, never updated",
            "README written first, kept current",
        ],
        value="No README",
        label="README policy",
    )
    mo.vstack(
        [
            mo.md(
                "**Choose the four decisions.** Each option is a real practice. "
                "The panel below reports what the configuration answers and what it leaves open."
            ),
            folder,
            naming,
            raw,
            readme,
        ]
    )
    return folder, naming, raw, readme


@app.cell
def _(evaluate_organization, folder, mo, naming, raw, readme):
    _ans, _unans = evaluate_organization(
        folder.value, naming.value, raw.value, readme.value
    )
    _ans_md = (
        "\n".join(f"- ✓ {a}" for a in _ans)
        if _ans
        else "_(nothing answered)_"
    )
    _unans_md = (
        "\n".join(f"- ✗ {u}" for u in _unans)
        if _unans
        else "_(nothing left open)_"
    )
    _kind = "success" if not _unans else "warn"
    _body = (
        "### Result of this configuration\n\n"
        "**Answered:**\n\n"
        f"{_ans_md}\n\n"
        "**Still open:**\n\n"
        f"{_unans_md}"
    )
    mo.callout(mo.md(_body), kind=_kind)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What good looks like

        The four decisions, taken together, produce a folder a reader can enter cold.

        ```
        ra-cohort-2024/
        ├── README.md                  (written before the project; describes structure and how to rerun)
        ├── data/
        │   ├── raw/                   (write-once, read-only; never edited in place)
        │   │   ├── 2024-01-08_labs.csv
        │   │   └── 2024-01-08_patients.csv
        │   └── processed/             (output of code/; can be deleted and rebuilt)
        │       └── analysis-cohort.csv
        ├── code/
        │   ├── 01-clean-labs.py
        │   ├── 02-build-cohort.py
        │   └── 03-make-figures.py
        ├── results/
        │   ├── figures/
        │   │   └── crp-trajectory.png
        │   └── tables/
        │       └── baseline-characteristics.csv
        └── docs/
            └── analysis-plan.md
        ```

        Three properties hold once this layout is in place. The provenance chain is reconstructable, because every file under `processed/` and `results/` came from a script under `code/` operating on a file under `raw/`. Deletion is safe, because every file under `processed/` and `results/` is rebuildable. Onboarding is bounded, because a stranger reads one document, `README.md`, to know where to start.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## README-driven development

        The phrase "README-driven" inverts the ordinary writing order. The README is normally the last thing written, when the project is essentially done and someone realizes a stranger could not find their way in. By then the structure is fixed, the names are inconsistent, and the document records the project's accidents rather than its plan.

        Written first, the README is a contract. It states what the folders will contain, what the data is, what is run in what order, and what the output is. Writing it is the first action on the project, before any code is written and before any data is loaded. Three effects follow:

        - The structural decisions are made deliberately, while they are still cheap to change.
        - The folder names and file conventions exist before any file does, so they are consistent from the start.
        - A project that does not match the README is visibly wrong, which forces either the project to change or the README to be updated, and does not let drift accumulate silently.

        The analogy in clinical research is the protocol of a trial. The methods section is written after the trial and reports what happened. The protocol is written before the trial and constrains what is allowed to happen. README-driven development treats the data project the same way a protocol treats the trial.
        """
    )
    return


@app.cell
def _(mo):
    org_quiz = mo.ui.radio(
        options=[
            "The manuscript files do not use ISO 8601 dates.",
            "The raw lab export was edited in place; the cleaning script overwrote it.",
            "The figure is at the top level, not in a `results/` folder.",
            "There is no README explaining the project.",
        ],
        label=(
            "You inherit the folder above. For the manuscript revision you need to "
            "recreate `crp_plot.png` exactly. Which structural problem, if uncorrected, "
            "makes recreating the figure literally impossible, regardless of how well "
            "organized everything else is?"
        ),
    )
    org_quiz
    return (org_quiz,)


@app.cell
def _(mo, org_quiz):
    if org_quiz.value is None:
        _resp = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif org_quiz.value.startswith("The raw lab export"):
        _resp = mo.callout(
            mo.md(
                "**Correct.** The other three are problems of legibility and navigation: "
                "they make the project hard to read, but every file is still on disk and a "
                "determined reader could find their way. The read-only-raw failure is "
                "categorically different. Once the original values are overwritten, no folder "
                "structure, naming convention, or document recovers them. Raw-data-is-read-only "
                "is the first of the four decisions because the other three become "
                "unenforceable once it has been violated."
            ),
            kind="success",
        )
    elif org_quiz.value.startswith("The manuscript files"):
        _resp = mo.callout(
            mo.md(
                "**Inconsistent file naming is a real problem,** but it makes the project "
                "hard to navigate, not impossible to reproduce. The manuscript CSVs are still "
                "on disk and can be inspected. The raw-data-overwrite scenario, by contrast, "
                "destroys the underlying values. The distinction between hard and impossible "
                "is the point of the question."
            ),
            kind="warn",
        )
    elif org_quiz.value.startswith("The figure is at the top level"):
        _resp = mo.callout(
            mo.md(
                "**A flat structure makes a project hard to read,** but every file is still "
                "present. The figure can be regenerated from raw if the raw is intact. The "
                "read-only-raw failure removes the underlying values, and folder layout "
                "cannot recover them."
            ),
            kind="warn",
        )
    else:
        _resp = mo.callout(
            mo.md(
                "**The missing README makes the project hard to enter,** but the data and "
                "code are still there. With enough effort a determined reader could "
                "reconstruct the project from the files. They cannot reconstruct the raw "
                "values once those have been overwritten in place. The other three problems "
                "are about legibility; the read-only-raw failure is about impossibility."
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

        The four decisions above are static. They describe how a project looks at a moment in time. The next track adds the time dimension: a version-control system records every change to every file, so the project itself becomes a sequence of revisions rather than a single snapshot. Read-only raw data and machine-friendly naming are necessary; they are not sufficient. A project that follows the four decisions but has no history loses the chain of decisions that produced its files, and that is the next failure to address.
        """
    )
    return


if __name__ == "__main__":
    app.run()
