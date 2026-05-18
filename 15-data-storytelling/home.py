"""Course 15: Data storytelling.

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
        # 15: Data storytelling

        ## The course that makes everything else useful beyond your own work.

        This course is currently scaffolded. The track folders exist with short READMEs describing what each one will cover; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for progress.

        ### Tracks

        | # | Track | What it will cover |
        |---|---|---|
        | 01 | **Knowing your audience** | Technical vs clinical vs executive vs patient. How to find out which one you're talking to. |
        | 02 | **Writing about data clearly** | Plain English for quantitative findings. Explaining uncertainty without losing the audience. |
        | 03 | **Building a narrative** | Data alone doesn't persuade. Finding → implication → recommendation. |
        | 04 | **Presenting visuals to non-technical audiences** | How to walk someone through a chart who has never seen one before. |
        | 05 | **Communicating with AI teams and vendors** | How to specify what you need, how to ask the right questions, how to evaluate what you're shown. |

        ### Capstone

        **Take the CDS design brief from course 12 and produce a 2-minute pitch + one-page visual summary.**

        ---

        Each track folder has a `README.md` you can read now. The `notebook.py` files render a placeholder until the track is built.
        """
    )
    return


if __name__ == "__main__":
    app.run()
