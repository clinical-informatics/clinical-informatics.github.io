"""Course 10: NLP and clinical text.

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
        # 10: NLP and clinical text

        ## The data that lives in notes, not fields. Most clinically meaningful information lives here.

        This course is currently scaffolded. The track folders exist with short READMEs describing what each one will cover; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for progress.

        ### Tracks

        | # | Track | What it will cover |
        |---|---|---|
        | 01 | **Structured vs unstructured data** | What lives in notes that doesn't live in fields. Why that matters for research and CDS. |
        | 02 | **What NLP actually does** | Tokenization, named entity recognition, relation extraction, each with one of Ms. Reyes's notes. |
        | 03 | **De-identification** | Why it's hard. Common approaches. What residual risk looks like. |
        | 04 | **LLMs and clinical text** | How LLMs relate to traditional NLP. Practical use cases and failure modes. |
        | 05 | **Evaluating NLP tools** | Precision, recall, F1 in plain English. Same idea as sensitivity/specificity, different vocabulary. |

        ### Capstone

        **Run a pre-built NLP pipeline on Ms. Reyes's notes; compare to structured EHR fields.**

        ---

        Each track folder has a `README.md` you can read now. The `notebook.py` files render a placeholder until the track is built.
        """
    )
    return


if __name__ == "__main__":
    app.run()
