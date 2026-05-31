"""Course 11: Health economics data.

Marimo course menu. Six tracks plus a building capstone built around the
biologic-vs-csDMARD decision in RA.
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

        Six tracks plus a building capstone. The course covers how claims data is structured, the cost and utilization vocabulary, decision analysis with reactive probability sliders, cost-effectiveness analysis, decision curve analysis as the unifying threshold framework, and how to read outcomes data critically.

        ### Tracks

        | # | Track | What it covers |
        |---|---|---|
        | 01 | **How claims data is structured** | What a claim records. The 7 claim rows for Reyes's 2024-01-08 visit. |
        | 02 | **Cost and utilization measures** | Total cost of care, PMPM, allowed vs paid. Reyes's 2024 utilization. |
        | 03 | **Decision analysis** | Decision trees with reactive probability sliders. One-way sensitivity. |
        | 04 | **Cost-effectiveness** | QALYs, ICERs, willingness-to-pay thresholds, the CE plane. |
        | 05 | **Decision curve analysis** | Net benefit. Treat-all / treat-none / use-the-model. |
        | 06 | **Reading outcomes data critically** | VBC vocabulary, confounders in HE research, CHEERS. |

        ### Capstone

        **Decision tree for the RA treatment choice with one-way sensitivity analysis.** Inputs are response probabilities and outcome utilities; output is expected value per arm plus a sensitivity sweep showing where the preferred strategy flips.

        ---

        Each track folder has a `README.md` and a `notebook.py`. Open the notebook in Marimo to interact with the material.
        """
    )
    return


if __name__ == "__main__":
    app.run()
