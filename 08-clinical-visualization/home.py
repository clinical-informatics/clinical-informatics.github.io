"""Course 08: Clinical visualization.

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
        # 08: Clinical visualization

        ## Charts that communicate. Charts that mislead.

        This course is currently scaffolded. The track folders exist with short READMEs describing what each one will cover; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for progress.

        ### Tracks

        | # | Track | What it will cover |
        |---|---|---|
        | 01 | **Choosing the right chart type** | Data type → chart type as a decision. Common mismatches and why they mislead. |
        | 02 | **Longitudinal and time-series data** | Disease activity over time. How to show change, how to show uncertainty in a trend. |
        | 03 | **Visualizing uncertainty** | Error bars, confidence intervals, prediction intervals. Same data, different uncertainty display, different impression. |
        | 04 | **Common misleading patterns** | Truncated axes, cherry-picked windows, inappropriate chart types, dual axes, with real clinical examples. |

        ### Capstone

        **Disease activity dashboard for Ms. Reyes's RA cohort: DAS28 over time, lab trends, medication history.**

        ---

        Each track folder has a `README.md` you can read now. The `notebook.py` files render a placeholder until the track is built.
        """
    )
    return


if __name__ == "__main__":
    app.run()
