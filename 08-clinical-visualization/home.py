"""Course 08: Clinical visualization.

Marimo course menu. Lists the four tracks plus the disease-activity dashboard
capstone and a one-sentence description of what each one covers.
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

        Four tracks and one capstone. Each track pairs a written introduction with an interactive Marimo notebook. Ms. Reyes's four-year lab and disease-activity trajectory carries every example.

        ### Tracks

        | # | Track | What it covers |
        |---|---|---|
        | 01 | **Choosing the right chart type** | Data type to chart type as a decision. Six clinical scenarios with the right chart for each and three mismatches that mislead. |
        | 02 | **Longitudinal and time-series data** | Reyes's CRP and ESR over four years. Reference-range bands, medication annotations, smoothing decisions. |
        | 03 | **Visualizing uncertainty** | Standard error, confidence interval, and prediction interval as three claims about the same data. |
        | 04 | **Common misleading patterns** | Truncated axes, cherry-picked windows, dual axes, time series as bars, aggregation that hides spikes. |

        ### Capstone

        **Disease-activity dashboard for Ms. Reyes's RA cohort.** Patient selector, date-range selector, lab multi-select, DAS28 toggle, medication-timeline toggle. The dashboard assembles reactively from the controls.

        ---

        Each track folder has a `README.md` and a `notebook.py`. Open the notebook in Marimo to interact with the material.
        """
    )
    return


if __name__ == "__main__":
    app.run()
