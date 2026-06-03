"""Course 13: Research reproducibility.

Marimo course menu. Five tracks plus a Socratic reproducibility-audit capstone.
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
        # 13: Research reproducibility

        ## Unglamorous, and the thing most people wish someone had taught them early.

        Five tracks plus a Socratic capstone. The course covers why reproducibility is a clinical-research problem, how to organize a data project so it can be rerun, what version control does without requiring any code, how to document a dataset's provenance and the loss every transformation introduces, and what sharing and publication require.

        ### Tracks

        | # | Track | What it covers |
        |---|---|---|
        | 01 | **Why reproducibility matters** | The replication crisis. The reproducible / replicable / robust distinction. Why an analysis can be wrong with every number correct. |
        | 02 | **Project organization** | Structuring a data project so it can be rerun. File naming, folder structure, raw-data-is-sacred, README-driven development. |
        | 03 | **Version control without coding** | What Git does in plain English. GitHub for non-developers; issues and pull requests as collaboration tools. |
        | 04 | **Data provenance and documentation** | Where a dataset came from, what was done to it, and documenting the loss. Cross-reference to Course 07: no mapping is lossless. |
        | 05 | **Sharing and publication** | What to share and what to withhold. Code sharing, preprints, persistent identifiers, the EQUATOR reporting guidelines. |

        ### Capstone

        **Audit a synthetic published RA analysis for reproducibility gaps and produce a documentation plan that would make it reproducible (Socratic).**

        ---

        Each track folder has a `README.md` and a `notebook.py`. Open the notebook in Marimo to interact with the material.
        """
    )
    return


if __name__ == "__main__":
    app.run()
