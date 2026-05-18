"""Course 03: Privacy, ethics, and governance.

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
        # 03: Privacy, ethics, and governance

        ## What protects patients, what the rules actually require, and what they don't.

        This course is currently scaffolded. The track folders exist with short READMEs describing what each one will cover; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for progress.

        ### Tracks

        | # | Track | What it will cover |
        |---|---|---|
        | 01 | **Why privacy matters in health data** | Re-identification, famous breaches of 'anonymized' data, the difference between de-identification and anonymization. |
        | 02 | **HIPAA and beyond** | HIPAA as a floor, not a ceiling. Safe Harbor vs Expert Determination. Data use agreements and the IRB. |
        | 03 | **Secondary use of clinical data** | Data collected for care, repurposed for research. The ethical, legal, and operational tensions. |
        | 04 | **Algorithmic fairness and equity** | Where bias enters: training data, labels, features, deployment context. What to ask of any model. |
        | 05 | **Governance structures** | Who decides what gets built and deployed. Data governance committees, vendor contracts, the clinician's role. |

        ### Capstone

        **Privacy, governance, and equity analysis of a proposed research project using EHR data (Socratic).**

        ---

        Each track folder has a `README.md` you can read now. The `notebook.py` files render a placeholder until the track is built.
        """
    )
    return


if __name__ == "__main__":
    app.run()
