"""Course 15: Data storytelling.

Marimo course menu. Five tracks plus a building capstone for the
CMO-pitch + clinical-staff-summary artifacts.
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

        Five tracks plus a building capstone. The course covers how to make the analyses, evaluation reports, vendor assessments, and CDS designs from the rest of the curriculum usable to the audiences who have to act on them: technical teams, clinicians, executives, and patients.

        ### Tracks

        | # | Track | What it covers |
        |---|---|---|
        | 01 | **Knowing your audience** | Four audience types in clinical informatics. What each needs, what each does not need, and how to identify the audience before composing the message. |
        | 02 | **Writing about data clearly** | Plain English for quantitative findings. Explaining uncertainty without burying the finding. Phrases that obscure rather than communicate. |
        | 03 | **Building a narrative** | The three-part structure (finding, implication, recommendation) that turns data into a recommendation an audience can act on. |
        | 04 | **Presenting visuals to non-technical audiences** | How to walk a non-technical audience through a chart. What to annotate. What to leave out. Cross-reference to Course 08. |
        | 05 | **Communicating with AI teams and vendors** | The questions a clinician should ask. The clinician as the domain expert in the room. |

        ### Capstone

        **Take the CDS design brief from Course 12 and produce two communication artifacts: a 2-minute verbal pitch for a CMO and a one-page visual summary for clinical staff (building).**

        ---

        Each track folder has a `README.md` and a `notebook.py`. Open the notebook in Marimo to interact with the material.
        """
    )
    return


if __name__ == "__main__":
    app.run()
