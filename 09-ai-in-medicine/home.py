"""Course 09: AI in medicine.

Marimo course menu. Six tracks plus a Socratic critical-appraisal capstone.
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

        ## Machine learning for clinicians who evaluate, not build.

        Six tracks plus a Socratic critical-appraisal capstone. The course deepens the discrimination and calibration vocabulary introduced in Course 04 Track 3, applies it to clinical model evaluation, and ends with a vendor-appraisal exercise.

        ### Tracks

        | # | Track | What it covers |
        |---|---|---|
        | 01 | **What a model actually does** | Inputs in, score out. Training, prediction, and a reactive readmission scoring demo. |
        | 02 | **Training, validation, overfitting** | Why a model that memorizes its training set is useless on new patients. Cross-validation. |
        | 03 | **Discrimination vs calibration** | The ROC explorer alongside the calibration plot. Two models, same AUC, different probabilities. |
        | 04 | **Reading an AI paper critically** | A five-dimension appraisal framework applied to a published paper. |
        | 05 | **Bias, fairness, and clinical risk** | Where bias enters. Subgroup performance. Fairness-metric trade-offs. Vendor checklist. |
        | 06 | **LLMs in clinical workflows** | Next-token prediction as the intuition. Hallucination, RAG, evaluation. |

        ### Capstone

        **Critical appraisal of a vendor "RA flare predictor".** Apply the Track 04 framework in a Socratic commit-then-reveal exercise.

        ---

        Each track folder has a `README.md` and a `notebook.py`. Open the notebook in Marimo to interact with the material.
        """
    )
    return


if __name__ == "__main__":
    app.run()
