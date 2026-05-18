"""Course 14: Interoperability policy.

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
        # 14: Interoperability policy

        ## The policy context that makes the technical courses meaningful.

        This course is currently scaffolded. The track folders exist with short READMEs describing what each one will cover; the interactive notebooks will be filled in as the curriculum builds out. Check `tasks.md` in the curriculum root for progress.

        ### Tracks

        | # | Track | What it will cover |
        |---|---|---|
        | 01 | **Why policy exists** | Information blocking: what it is, why it persisted, who benefited from it. |
        | 02 | **21st Century Cures Act** | What it requires. Information blocking rules. What changed in practice. |
        | 03 | **ONC and CMS interoperability rules** | Certification, mandated standards, why FHIR adoption accelerated when it did. |
        | 04 | **The international landscape** | GDPR. NHS Digital. What other countries are doing differently and why. |
        | 05 | **Where the gaps still are** | What policy hasn't solved. The patient matching problem. What's coming next. |

        ### Capstone

        **Apply applicable policy to a health-system scenario (records access, dataset access, vendor restriction) (Socratic).**

        ---

        Each track folder has a `README.md` you can read now. The `notebook.py` files render a placeholder until the track is built.
        """
    )
    return


if __name__ == "__main__":
    app.run()
