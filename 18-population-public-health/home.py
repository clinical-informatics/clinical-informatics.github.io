"""Course 18: population health and public health informatics.

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
        # 18: Population health and public health informatics

        ## From individual patient care to population view. Reyes is one of 1,247 RA patients in her health system's registry. Risk stratification, value-based care, SDOH, public health surveillance (NEDSS, ESSENCE).

        This course is currently scaffolded. The track folders exist with short READMEs describing what each one will cover; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for progress.

        ### Tracks

        | # | Track | What it will cover |
        |---|---|---|
        | 01 | **From individual care to population view** | Kindig and Stoddart 2003. Population vs public health. The denominator question. Reyes as one row vs Reyes in the registry. |
        | 02 | **Registries and the population data model** | Disease registries, quality registries (NCDR, NSQIP). Registry-vs-EHR distinction. Reyes's RA registry membership. |
        | 03 | **Risk stratification** | HCC, LACE, HOSPITAL. AI-based stratification. Interactive: comorbidity slider showing Reyes's score shift. |
        | 04 | **Value-based care and delivery models** | ACOs (MSSP, REACH), PCMH, BPCI bundles, pay-for-performance. Reyes's ACO attribution. |
        | 05 | **Social determinants of health** | Five-domain framework, PRAPARE, Gravity, SDOH-CC IG. The Reyes food-insecurity capture problem. |
        | 06 | **Public health informatics** | Notifiable disease reporting (NEDSS), syndromic surveillance (ESSENCE), IIS, NHSN. Reyes's COVID and flu cases walked through. |

        ### Capstone

        **Design a diabetes population health management program: cohort, risk stratification, VBC alignment, SDOH integration, public health reporting, equity (Socratic).**

        ---

        Each track folder has a `README.md` you can read now. The `notebook.py` files render a placeholder until the track is built.
        """
    )
    return


if __name__ == "__main__":
    app.run()
