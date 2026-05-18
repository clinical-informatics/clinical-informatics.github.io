"""Course 04: Clinical epidemiology.

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
        # 04: Clinical epidemiology

        ## A thinking course. The one that makes terms click that you've been nodding along to for years.

        This course is currently scaffolded. The track folders exist with short READMEs describing what each one will cover; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for progress.

        ### Tracks

        | # | Track | What it will cover |
        |---|---|---|
        | 01 | **Measures of frequency and association** | Incidence, prevalence, RR, OR, HR, each with a clinical example from Ms. Reyes's cohort. |
        | 02 | **Bias** | Selection, information, confounding, with real clinical examples and a confounder you can add to an analysis on a slider. |
        | 03 | **Diagnostic test performance** | The 2x2 table as the core intuition exercise. Sliders for sensitivity, specificity, prevalence; watch PPV collapse. |
        | 04 | **Basic statistical tests** | Match the test to the data type. P-values and CIs done right. Common misinterpretations. |
        | 05 | **Study designs** | Which design could answer the question, at what cost. Causation vs association. |

        ### Capstone

        **Identify the three biggest threats to validity in a naive analysis of a synthetic RA dataset (Socratic).**

        ---

        Each track folder has a `README.md` you can read now. The `notebook.py` files render a placeholder until the track is built.
        """
    )
    return


if __name__ == "__main__":
    app.run()
