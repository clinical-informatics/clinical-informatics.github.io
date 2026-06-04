"""Course 14: Interoperability policy.

Marimo course menu. Five tracks plus a Socratic policy-analysis capstone.
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

        Five tracks plus a Socratic capstone. The course covers why information blocking had to be named and prohibited in federal law, what the 21st Century Cures Act required and what its exceptions mean in practice, how the ONC and CMS rules turned the Cures Act into technical mandates (explaining why FHIR adoption accelerated when it did), how GDPR and the European Health Data Space differ from the U.S. framework, and where the gaps still are.

        ### Tracks

        | # | Track | What it covers |
        |---|---|---|
        | 01 | **Why policy exists** | Information blocking as the structural problem. HITECH and Meaningful Use as the precondition. Who benefited and how. |
        | 02 | **21st Century Cures Act** | What the 2016 law required. The information-blocking exceptions (eight in the original 2020 Final Rule, ten after HTI-1). What changed in practice. |
        | 03 | **ONC and CMS interoperability rules** | Cures Act Final Rule, HTI-1, HTI-2, CMS Patient Access and Payer-to-Payer. Why FHIR adoption accelerated. |
        | 04 | **The international landscape** | GDPR versus HIPAA. NHS Digital. The European Health Data Space. |
        | 05 | **Where the gaps still are** | Patient matching. USCDI evolution. TEFCA. AI transparency under HTI-1. |

        ### Capstone

        **Apply the policy framework to three health-system scenarios (records access, dataset access, vendor restriction) and produce a written analysis (Socratic).**

        ---

        Each track folder has a `README.md` and a `notebook.py`. Open the notebook in Marimo to interact with the material.
        """
    )
    return


if __name__ == "__main__":
    app.run()
