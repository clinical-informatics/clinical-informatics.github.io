"""Course 13: Research reproducibility.

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
        # 13: Research reproducibility

        ## Unglamorous but the thing most people wish someone had taught them early.

        This course is currently scaffolded. The track folders exist with short READMEs describing what each one will cover; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for progress.

        ### Tracks

        | # | Track | What it will cover |
        |---|---|---|
        | 01 | **Why reproducibility matters** | The replication crisis in clinical research. What 'reproducible' actually means. |
        | 02 | **Project organization** | How to structure a data project. File naming, folder structure, README-driven development. |
        | 03 | **Version control without coding** | What Git does in plain English. GitHub for non-developers; issues and PRs as collaboration tools. |
        | 04 | **Data provenance and documentation** | Where did this dataset come from? What was done to it? No standard is lossless. |
        | 05 | **Sharing and publication** | Data sharing requirements. What to share, what not to. Preprints. EQUATOR. |

        ### Capstone

        **Identify reproducibility gaps in a synthetic published analysis and produce a documentation plan (Socratic).**

        ---

        Each track folder has a `README.md` you can read now. The `notebook.py` files render a placeholder until the track is built.
        """
    )
    return


if __name__ == "__main__":
    app.run()
