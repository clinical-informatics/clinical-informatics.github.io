"""Course 11: Health economics data.

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
        # 11: Health economics data

        ## Claims, costs, decisions, and value.

        This course is currently scaffolded. The track folders exist with short READMEs describing what each one will cover; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for progress.

        ### Tracks

        | # | Track | What it will cover |
        |---|---|---|
        | 01 | **How claims data is structured** | What a claim actually records. What it can and can't tell you. |
        | 02 | **Cost and utilization measures** | Total cost of care, PMPM, utilization rates, applied to Ms. Reyes. |
        | 03 | **Decision analysis** | Decision trees with probability sliders. Sensitivity analysis (one-way, tornado). Biologic vs conventional DMARD. |
        | 04 | **Cost-effectiveness** | QALYs, ICERs, willingness-to-pay thresholds in plain English. The CE plane. |
        | 05 | **Decision curve analysis** | Net benefit in plain English. DCA as the unifying framework. Cross-reference to CDS course. |
        | 06 | **Reading outcomes data critically** | Value-based care. Common confounders in health economics research. |

        ### Capstone

        **Decision tree + one-way sensitivity analysis for an RA treatment choice; interpret strategy stability.**

        ---

        Each track folder has a `README.md` you can read now. The `notebook.py` files render a placeholder until the track is built.
        """
    )
    return


if __name__ == "__main__":
    app.run()
