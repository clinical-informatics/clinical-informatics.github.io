"""Track 01: Knowing your audience.

No visible code. The notebook presents the four audiences in clinical
informatics (technical, clinical, executive, patient), runs the reader
through a same-finding-four-renderings exercise on a synthetic sepsis-CDS
evaluation finding, and closes with a misalignment quiz.

WASM-safe: no shared imports, no data files, no relative paths.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    AUDIENCE_RENDERINGS = {
        "Technical (engineers, data scientists, analysts)": (
            "**Cohort:** 12,400 adult inpatients admitted to medicine, surgery, "
            "or critical-care services between 2024-09 and 2025-11. "
            "**Outcome:** 30-day in-hospital mortality after admission. "
            "**Pre-intervention crude rate:** 5.71% (95% CI 5.32% to 6.10%). "
            "**Post-intervention crude rate:** 4.51% (4.20% to 4.82%). "
            "**Absolute reduction:** 1.20 percentage points. "
            "**Multivariable adjustment** for age, sex, Charlson comorbidity "
            "index, and prior 30-day admission yields adjusted RR 0.79 "
            "(95% CI 0.65 to 0.96), p = 0.024. Alert fires on average twice "
            "per shift per service; override rate 60.3% (within the "
            "pre-specified 50% to 70% acceptable range). FHIR endpoints used: "
            "Observation (LOINC vital signs and CBC panel), Condition "
            "(active), MedicationStatement. Average latency 1.4 seconds from "
            "data update to alert."
        ),
        "Clinical (clinicians, nurses, pharmacists)": (
            "Across 12,400 admissions over 14 months, the new sepsis alert was "
            "associated with about 1.2 fewer deaths per 100 admissions in the "
            "first 30 days. That is roughly 150 lives over the period. The "
            "alert fires on average twice per shift per service; clinicians "
            "override about 60% of the time, which is in the range the rollout "
            "planned for. The alert uses vital signs, CBC trends, and active "
            "conditions to identify patients at elevated risk for sepsis in the "
            "next 6 to 12 hours; the response is a chart-open notification "
            "suggesting bedside re-evaluation. There is no automated action, no "
            "order placement, no documentation requirement. The alert exists to "
            "surface the question, not to answer it."
        ),
        "Executive (CMIO, CMO, CIO, CFO)": (
            "The sepsis alert reduced 30-day mortality from 5.7% to 4.5% across "
            "12,400 admissions over 14 months. About 150 lives saved over the "
            "period. Capital cost $480K; annual operating $120K. Implied cost "
            "per life saved at 14 months is well under $4K, far below any "
            "reasonable willingness-to-pay threshold. The override rate (60%) "
            "is within the planned range; clinician satisfaction with the "
            "alert was 4.2 out of 5 on the rollout survey. "
            "**Recommendation: continue operation; budget $120K annual "
            "operating for FY26.**"
        ),
        "Patient (patients, family members, patient and family advisory council)": (
            "We added a system to the hospital that watches for early signs of "
            "a serious infection called sepsis and alerts the care team to "
            "check the patient. Since we turned it on in September 2024, fewer "
            "patients have died from sepsis at our hospital. The alert "
            "sometimes prompts a doctor or nurse to recheck a patient, but it "
            "does not change what care looks like for you or your family. The "
            "system uses the same lab values and vital signs the care team "
            "already collects; it does not add tests, slow down care, or make "
            "decisions on its own. The doctor or nurse still decides what to "
            "do, and a patient or family member can always ask why a particular "
            "check is being done."
        ),
    }

    MISALIGNMENT_OPTIONS = {
        "Spotted: technical detail in a patient-facing message.": "patient",
        "Spotted: a dollar figure in a clinician-facing message about clinical workflow.": "clinical",
        "Spotted: clinical-workflow detail in an executive-facing one-pager.": "executive",
        "Spotted: marketing prose in a technical specification.": "technical",
    }

    return AUDIENCE_RENDERINGS, MISALIGNMENT_OPTIONS, mo


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 01: Knowing your audience

        A clinical informaticist has just spent three weeks finalizing the rollout plan for a sepsis CDS intervention. Within the next week she has to brief four very different groups: the IT team that will build the integration, the medical-and-nursing services that will see the alerts, the C-suite signing off on the budget, and (via a patient-and-family advisory council) patients who will be subject to the alert in care. The default mistake is to compose one set of slides and deliver them four times. The right move is to compose four versions of the same facts, each shaped for what its audience can act on.

        This track names the four audiences, the questions each will bring to a briefing, and the practice of identifying the audience before composing the message.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Four audiences in clinical informatics

        Four audience types appear in nearly every clinical-informatics briefing. Each has its own questions and its own threshold for what counts as a sufficient answer.

        | Audience | Who they are | What they need | What they do not need |
        |---|---|---|---|
        | **Technical** | Engineers, data scientists, analysts. | Precision, complete specifications, testability, failure modes. | Clinical context already understood; marketing framing. |
        | **Clinical** | Clinicians, nurses, pharmacists. | Workflow fit, alert behavior at the bedside, the override mechanism, the harm-reduction case. | Technical infrastructure detail; most financial detail. |
        | **Executive** | CMIO, CMO, CIO, CFO. | The KPI move, the dollar number, the risk, the time horizon, the ask. | Technical detail; clinical jargon; everything beyond the one page. |
        | **Patient** | Patients, family members, the patient-and-family advisory council. | The experience, the consent context, the safety implications, the recourse pathway. | Regulatory acronyms; technical detail; most financial detail. |

        The default communication failure is **altitude mismatch**: speaking at the technical altitude to an executive audience (the executive disengages), or at the executive altitude to a technical audience (the technical reader does not have enough to act). The fix is to choose the altitude before choosing the content.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Same finding, four renderings

        The interactive below presents one substantive finding from a synthetic CDS evaluation and renders it for each of the four audiences. The data are the same in every rendering; the framing, the altitude, the vocabulary, and the level of detail differ.

        ### The shared finding

        > A 14-month rollout of a sepsis decision-support intervention across 12,400 adult inpatient admissions reduced 30-day in-hospital mortality from 5.71% to 4.51% (adjusted RR 0.79, 95% CI 0.65 to 0.96), with an override rate of 60.3% and implementation cost of $480K capital plus $120K annual operating.

        Pick an audience below to see the rendering shaped for that audience.
        """
    )
    return


@app.cell
def _(AUDIENCE_RENDERINGS, mo):
    audience_pick = mo.ui.dropdown(
        options=list(AUDIENCE_RENDERINGS.keys()),
        value=list(AUDIENCE_RENDERINGS.keys())[0],
        label="Audience",
    )
    audience_pick
    return (audience_pick,)


@app.cell
def _(AUDIENCE_RENDERINGS, audience_pick, mo):
    _rendering = AUDIENCE_RENDERINGS[audience_pick.value]
    _body = (
        f"### Rendering for: {audience_pick.value}\n\n"
        f"{_rendering}"
    )
    mo.callout(mo.md(_body), kind="neutral")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What changed across the renderings

        The four renderings share the same finding (the mortality reduction, the cohort size, the override rate, the cost). They differ on three load-bearing dimensions.

        - **Altitude.** The technical rendering is at low altitude (FHIR endpoints, latency, adjustment variables). The executive rendering is at high altitude (KPI move, dollar number, recommendation). The clinical and patient renderings sit in the middle, anchored to the workflow and the lived experience respectively.
        - **Vocabulary.** The technical rendering uses regulated technical terms (RR, 95% CI, LOINC). The clinical rendering uses clinical language and the framing of bedside use. The executive rendering uses financial and KPI vocabulary. The patient rendering uses everyday language with the clinical content explained in line.
        - **The ask.** Each rendering implies a different action. The technical rendering supports the question "is this implementable;" the clinical rendering supports "is this safe and usable;" the executive rendering supports "should this be funded;" the patient rendering supports "is this trustworthy."

        A failed communication usually fails on all three at once: the altitude is wrong, which means the vocabulary is wrong, which means the implied ask is wrong, which means the audience cannot act on what they just read.
        """
    )
    return


@app.cell
def _(MISALIGNMENT_OPTIONS, mo):
    quiz = mo.ui.radio(
        options=list(MISALIGNMENT_OPTIONS.keys()),
        label=(
            "You are reviewing a colleague's draft briefing materials for the "
            "sepsis CDS rollout. One paragraph reads: \"The Charlson-adjusted "
            "30-day mortality dropped from 5.71% to 4.51% (RR 0.79, 95% CI "
            "0.65 to 0.96). Twelve children's units in the hospital used the "
            "alert most heavily. Your loved one's care team may sometimes "
            "receive an additional check when they review the chart.\" Which "
            "audience-mismatch problem is the paragraph displaying?"
        ),
    )
    quiz
    return (quiz,)


@app.cell
def _(mo, quiz):
    if quiz.value is None:
        _resp = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif quiz.value.startswith("Spotted: technical detail in a patient-facing"):
        _resp = mo.callout(
            mo.md(
                "**Correct.** The paragraph opens with a Charlson-adjusted "
                "relative risk and a 95% confidence interval (technical "
                "altitude, technical vocabulary), in a sentence that ends with "
                "addressing the reader's \"loved one's care team\" (patient "
                "altitude, patient vocabulary). A patient audience cannot use "
                "the relative-risk framing; a clinical-language framing of the "
                "same finding (\"about 1.2 fewer deaths per 100 admissions in "
                "the first 30 days\") matches the altitude of the rest of the "
                "paragraph. The mistake is altitude collision within a single "
                "paragraph."
            ),
            kind="success",
        )
    else:
        _resp = mo.callout(
            mo.md(
                "**Reread the paragraph.** The Charlson-adjusted relative-risk "
                "framing is technical-altitude content, and the \"your loved "
                "one's care team\" framing is patient-altitude content. The "
                "paragraph mixes the two in adjacent sentences. The "
                "characteristic failure is technical detail in a patient-facing "
                "message: a patient reader cannot use the RR framing, and the "
                "presence of technical jargon early in the paragraph signals to "
                "the patient reader that the document is not really for them."
            ),
            kind="warn",
        )
    _resp
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Where this goes next

        Audience analysis is the prerequisite move. Once the audience is named, the next decisions are sentence-level: which words, which sentence structures, which framing of uncertainty, which omitted detail. Track 02 covers the craft of writing the same finding in language a non-statistician executive or non-statistician clinician can use without surrendering the precision the underlying analysis requires.
        """
    )
    return


if __name__ == "__main__":
    app.run()
