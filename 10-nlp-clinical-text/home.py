"""Course 10: NLP and clinical text.

Marimo course menu. Five tracks plus a building capstone on Reyes's notes.
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
        # 10: NLP and clinical text

        ## The data that lives in notes, not fields.

        Five tracks plus a building capstone. The majority of clinically meaningful information lives in narrative notes rather than structured fields. The course addresses what NLP pipelines extract from those notes, how the notes are de-identified for research use, where LLMs fit in the modern NLP landscape, and how to evaluate any NLP tool before adoption.

        ### Tracks

        | # | Track | What it covers |
        |---|---|---|
        | 01 | **Structured vs unstructured data** | What lives in notes that does not live in fields, on one of Ms. Reyes's encounters. |
        | 02 | **What NLP actually does** | Tokenization, NER, relation extraction, negation, each illustrated on her notes. |
        | 03 | **De-identification** | The HIPAA Safe Harbor 18 identifiers. Three approaches. A before-and-after on a Reyes note. |
        | 04 | **LLMs and clinical text** | Where LLMs fit alongside classical pipelines. Clinical-domain fine-tuning. Schema-driven extraction. |
        | 05 | **Evaluating NLP tools** | Precision, recall, F1, mapped to PPV and sensitivity. Strict vs lenient matching. The cost asymmetry. |

        ### Capstone

        **Build a structured representation of Ms. Reyes's record from her 8 clinical notes and contrast with the structured EHR fields.** Quantify what was lost when only the structured fields were queried.

        ---

        Each track folder has a `README.md` and a `notebook.py`. Open the notebook in Marimo to interact with the material.
        """
    )
    return


if __name__ == "__main__":
    app.run()
