"""Course 07: Data wrangling and engineering.

Marimo course menu. The course is currently scaffolded; track content will
be filled in as the curriculum builds out. The menu below lists the tracks
and a one-sentence description of what each one will cover.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # 07: Data wrangling and engineering

        ## SQL, pandas, OMOP, graph databases. The data engineering layer.

        This course is currently scaffolded. The track folders exist with short READMEs describing what each one will cover; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for progress.

        ### Tracks

        | # | Track | What it will cover |
        |---|---|---|
        | 01 | **SQL from first principles** | Clinical questions first, SQL second. Aggregations, grouping, and window functions via clinical use cases. |
        | 02 | **pandas for clinical data** | DataFrames as clinical tables. Filtering, grouping, merging through clinical scenarios. Dates as a special focus. |
        | 03 | **Standards: why they exist** | Portability vs interoperability defined and distinguished. The same fact stored six ways across six EHRs. |
        | 04 | **OMOP CDM** | Why OMOP exists. Core tables, concept IDs, the vocabulary layer. Mapped from Ms. Reyes's EHR. |
        | 05 | **Graph databases** | Conceptual fluency only. When a problem is graph-shaped. Ms. Reyes's medication history as a knowledge graph. |

        ### Capstone

        **Build an OMOP-structured dataset for a synthetic RA cohort from messy source data; run three clinical queries.**

        ---

        Each track folder has a `README.md` you can read now. The `notebook.py` files render a placeholder until the track is built.
        """
    )
    return


if __name__ == "__main__":
    app.run()
