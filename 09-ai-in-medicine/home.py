"""Course 09: AI in medicine.

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
        # 09: AI in medicine

        ## Machine learning for clinicians who evaluate, not build. Explicitly deepens Track 04 (epi).

        This course is currently scaffolded. The track folders exist with short READMEs describing what each one will cover; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for progress.

        ### Tracks

        | # | Track | What it will cover |
        |---|---|---|
        | 01 | **What a model actually does** | Intuition before math. A model as a function. What training and prediction mean. |
        | 02 | **Training, validation, overfitting** | Why you can't test on what you trained on. Overfitting shown visually. |
        | 03 | **Discrimination vs calibration** | ROC, threshold slider, 2x2, and calibration plot side by side. Why a well-discriminating model can still be useless. |
        | 04 | **Reading an AI paper critically** | What to look for: training population, outcome, validation approach, calibration, subgroup performance. |
        | 05 | **Bias, fairness, and clinical risk** | Where bias enters. Disparate subgroup performance. What to ask a vendor. |
        | 06 | **LLMs in clinical workflows** | What LLMs are without math. Where they help, where they're dangerous, hallucination explained clearly. |

        ### Capstone

        **Critical appraisal of a published clinical AI model across each appraisal dimension (Socratic).**

        ---

        Each track folder has a `README.md` you can read now. The `notebook.py` files render a placeholder until the track is built.
        """
    )
    return


if __name__ == "__main__":
    app.run()
