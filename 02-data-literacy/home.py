"""Course 02: Data literacy.

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
        # 02: Data literacy

        ## Rows, columns, joins, missingness. Thinking in tables.

        This course is currently scaffolded. The track folders exist with short READMEs describing what each one will cover; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for progress.

        ### Tracks

        | # | Track | What it will cover |
        |---|---|---|
        | 01 | **Data types and why they matter** | Numbers vs text, dates (the special nightmare), categories and codes; CRP stored as text and the average that breaks. |
        | 02 | **Tidy data** | One fact per cell. What untidy data looks like in clinical practice and what reshaping the medication table actually does. |
        | 03 | **Null values and missingness** | MCAR, MAR, MNAR in plain English. What happens when you ignore each one, watched on a slider. |
        | 04 | **Joins: the central skill** | Inner, left, right, anti-join, applied to two clinical tables. The 'silent patient loss' problem made visible. |
        | 05 | **What a database actually is** | Why a database is not a spreadsheet. Schema, constraints, and the forward reference to FHIR and OMOP. |

        ### Capstone

        **Clean, join, and summarize three messy synthetic clinical tables using the cohort builder.**

        ---

        Each track folder has a `README.md` you can read now. The `notebook.py` files render a placeholder until the track is built.
        """
    )
    return


if __name__ == "__main__":
    app.run()
