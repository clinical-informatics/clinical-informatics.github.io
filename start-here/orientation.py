"""Orientation notebook for clinical-informatics.

Run this once before you start any course. It takes about ten minutes.

What this notebook does:

- Introduces the curriculum's tone and philosophy
- Walks you through Ms. Reyes's data files
- Shows you the cross-reference callouts you'll see throughout
- Demonstrates a quiz so you know what to expect
- Tells you where to go next
"""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    from pathlib import Path
    return Path, mo, pd


@app.cell
def __(mo):
    mo.md(
        r"""
        # Orientation: how to use this curriculum

        Welcome. The next ten minutes will save you a lot of time later. We'll:

        1. Show you what the curriculum looks like in practice
        2. Introduce **Ms. Elena Reyes**, the patient who appears in every course
        3. Demonstrate the **cross-reference callouts** that link concepts across courses
        4. Walk through one quiz, so you know what to expect

        Take your time. There's nothing to install. Nothing to memorize. Just read and click.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 1. The philosophy in one sentence

        > **Every term gets defined in plain English, before it gets used technically.**

        That's it. That's the whole rulebook.

        If a notebook ever uses a word you don't recognize, **that's a bug in the notebook, not a failing on your part.** Open an issue. Tell us. We'll fix it.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 2. Meet Ms. Elena Reyes

        Every course in this curriculum follows the same patient.

        **Ms. Elena Reyes** is 52 years old. She lives in Springfield, Massachusetts. She works as an accountant. She was diagnosed with seropositive rheumatoid arthritis in March 2022 and has been treated since by Dr. Maya Bennett at Bay Rheumatology Associates.

        Her data has been **assembled in every format you'll meet in this curriculum**:

        - As a FHIR R4 bundle (course 06)
        - As an Epic-style EHR export (course 05)
        - As a Cerner-style EHR export, the same facts in a very different shape (course 05)
        - As insurance claims, two years of them (course 11)
        - As longitudinal lab values (every course)
        - As clinical notes a rheumatologist might actually write (course 10)
        - As tables in the OMOP common data model (course 07)

        Let's look at one of those right now.
        """
    )
    return


@app.cell
def __(Path):
    DATA_DIR = Path(__file__).parent / "patients" / "elena-reyes"
    LABS_FILE = DATA_DIR / "labs.csv"
    return DATA_DIR, LABS_FILE


@app.cell
def __(LABS_FILE, mo, pd):
    if LABS_FILE.exists():
        labs = pd.read_csv(LABS_FILE)
        labs_view = labs[["specimen_date", "test_name", "value", "unit", "interpretation"]]
        block = mo.vstack(
            [
                mo.md(
                    "Here are Ms. Reyes's first thirty lab values. CRP and ESR are the "
                    "inflammation markers that tell us how active her disease is."
                ),
                mo.ui.table(labs_view.head(30), selection=None),
            ]
        )
    else:
        block = mo.md(
            "_(The labs file isn't where this notebook expects it. "
            "That's unusual. Please open an issue.)_"
        )
    block
    return block, labs, labs_view


@app.cell
def __(mo):
    mo.md(
        r"""
        Notice a few things about the data above:

        - Every value has a **unit** (mg/L, mm/h, U/mL). Lab values are nothing without their units. This will come up again in the data literacy course.
        - There's an **interpretation flag** (H for high, L for low, N for normal). That's the EHR's way of saying "we know this is outside the reference range." How that flag gets set is more interesting than you might think. We'll come back to it in course 05.
        - The CRP (C-reactive protein) values aren't just numbers. They tell a clinical story. Watch how her CRP comes down in early 2024. That's when adalimumab was added.

        **This kind of "the data tells a story" thinking is what informatics is about.**
        """
    )
    return


@app.cell
def __(mo):
    mo.md("## 3. Cross-reference callouts")
    return


@app.cell
def __(mo):
    # Inline example of the cross-reference component for demonstration
    callout = mo.callout(
        mo.vstack(
            [
                mo.md("**Remember the 2x2 table from course 04, clinical epidemiology?**"),
                mo.md(
                    "Here's what happens when you stop treating it as a discrete table "
                    "of test results and start treating it as the *output* of a continuous "
                    "model score. The ROC curve is what you get when you sweep the threshold "
                    "across all possible values."
                ),
            ]
        ),
        kind="info",
    )
    mo.vstack(
        [
            mo.md(
                "Cross-reference callouts appear throughout the curriculum. They look like the "
                "blue box below. Whenever you see one, it's a signal that this idea was first "
                "introduced earlier. You can always click back if you want to refresh."
            ),
            callout,
            mo.md(
                "The curriculum is built around several **stacking arcs**. Concepts that get "
                "introduced in one course and deepened across many others. The 2x2 table arc, "
                "for example, runs from epidemiology (04) into AI (09) into health economics (11) "
                "into decision support (12). You'll see it five times. By the fifth time, "
                "you'll own it."
            ),
        ]
    )
    return (callout,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 4. What a quiz looks like

        Quizzes appear at **genuine decision points**: moments where committing to an answer is the only way to engage with the next idea.

        Here's one to try.
        """
    )
    return


@app.cell
def __(mo):
    quiz_widget = mo.ui.radio(
        options=[
            "Ms. Reyes's anti-CCP test became positive after she started methotrexate",
            "Ms. Reyes's anti-CCP test was already positive at her initial visit, well before she started any treatment",
            "Ms. Reyes's anti-CCP test was negative throughout her course",
            "The data isn't sufficient to say",
        ],
        label=(
            "Look at the lab table above. Which of these statements about "
            "Ms. Reyes's anti-CCP antibody is true?"
        ),
    )
    quiz_widget
    return (quiz_widget,)


@app.cell
def __(mo, quiz_widget):
    if quiz_widget.value is None:
        feedback = mo.callout(mo.md("_Pick an answer to see feedback._"), kind="neutral")
    elif quiz_widget.value == (
        "Ms. Reyes's anti-CCP test was already positive at her initial visit, "
        "well before she started any treatment"
    ):
        feedback = mo.callout(
            mo.md(
                "**Correct.** Anti-CCP was 178 U/mL on 2022-02-14, which was her first visit. "
                "The reference range tops out at 20. Anti-CCP is an autoantibody. "
                "It's typically present *before* the clinical disease declares itself "
                "fully, which is one reason it's such a useful test."
            ),
            kind="success",
        )
    else:
        feedback = mo.callout(
            mo.md(
                "**Not quite.** Scroll back up to the lab table. Look for the row dated "
                "**2022-02-14** with `Anti-cyclic citrullinated peptide antibody`. "
                "Its value was 178 U/mL. That's at her **first** visit, before she ever "
                "took methotrexate. That date matters: it tells you the disease process "
                "was already in motion before any treatment touched her."
            ),
            kind="warn",
        )
    feedback
    return (feedback,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 5. What's next

        You're ready to start. Go back to the home menu and pick a course. If you don't know where to begin, the README in this repo has learning paths organized by role: clinician, trainee, researcher, IT, just curious.

        A few promises about every course in this curriculum:

        1. **No term goes unintroduced.** If a notebook uses a word, it defined it first or it linked to the glossary.
        2. **No formula appears before its intuition.** You'll see the picture before you see the math.
        3. **No course pretends a hard thing is easy.** When something is genuinely tricky, we say so out loud.
        4. **Ms. Reyes is always there.** The same patient, the same data, viewed from every angle the field offers.

        See you in the courses.
        """
    )
    return


if __name__ == "__main__":
    app.run()
