"""Capstone: Design a clinical decision rule.

A Socratic walkthrough using every move from Tracks 01 through 05. You
define an outcome, list inputs, write the rule, find three edge cases,
name the data dependencies, and identify who the rule is likely to fail
for. Each step gates its sample answer behind your written commit. The
notebook assembles your committed answers into a one-page design
document at the end.

Scenario: design a CDR to flag hospitalized patients who would benefit
from a palliative care consultation but don't currently have one.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import sys
    from pathlib import Path

    # The shared/ symlink lives at the course root (one level up from capstone/).
    _course_root = Path(__file__).parent.parent
    if str(_course_root) not in sys.path:
        sys.path.insert(0, str(_course_root))

    import marimo as mo
    from shared.socratic import commit_text, reveal
    return commit_text, mo, reveal


@app.cell
def _(mo):
    mo.md(
        r"""
        # Capstone: Design a clinical decision rule

        ## The scenario.

        You're on the steering committee for your hospital's inpatient palliative care expansion. The PC team can take more consultations than they currently receive. The unmet need is real, and the under-referral is not random: it disproportionately falls on patients with non-cancer terminal illness, patients whose clinicians use interpreters, and patients from communities where PC has been historically under-offered.

        The committee wants a clinical decision rule that flags inpatients who would benefit from a PC consult but don't have one. They've asked you to come back next week with a one-page design document. This notebook is that document.

        You will define the outcome, list candidate inputs, write the rule in plain English, find three edge cases your rule will get wrong, name the data the rule depends on, and identify who the rule is likely to fail for. Each step asks you to commit a written answer; the sample answer unlocks alongside yours only after you write something. There is no single correct answer here. The Socratic point is that the work of designing a CDR is the writing.

        At the end the notebook assembles your six committed answers into a one-page document you can copy out as your draft.
        """
    )
    return


@app.cell
def _(commit_text):
    outcome_widget, outcome_ready = commit_text(
        "**Step 1.** Define the outcome the rule is trying to predict, operationally enough that a data scientist could implement it. Avoid the phrase \"would benefit\"; replace it with concrete criteria you could verify from the chart.",
        min_chars=80,
    )
    outcome_widget
    return outcome_ready, outcome_widget


@app.cell
def _(mo, outcome_ready, outcome_widget, reveal):
    mo.stop(
        not outcome_ready(),
        mo.md("_Write at least a few sentences above. The sample answer unlocks when you commit._"),
    )
    sample_outcome = (
        "Adult inpatient on a medicine or surgical service with at least one of the following: "
        "(a) **advanced cancer**, defined as metastatic disease or locally advanced disease without curative-intent treatment; "
        "(b) **advanced organ failure**, defined as NYHA class III-IV heart failure, GOLD stage III-IV COPD, CKD stage V, or cirrhosis with documented decompensation, with at least one prior admission in the past six months; "
        "(c) **moderate-to-severe dementia**, defined as FAST stage 6a or higher with new dependence on basic ADLs; "
        "AND who has not received a documented palliative care consultation during the current admission. "
        "The clinically relevant outcome over which the rule will be evaluated is whether a PC consult, placed within 48 hours of identification, results in at least one of: a documented goals-of-care conversation, an introduction of palliative-intent symptom management, or a hospice referral, before discharge."
    )
    reveal(outcome_widget.value, sample_outcome, learner_label="Your outcome definition")
    return (sample_outcome,)


@app.cell
def _(commit_text):
    inputs_widget, inputs_ready = commit_text(
        "**Step 2.** List the inputs your rule would use to detect the outcome above. For each input, name the chart source and one limitation you would document up front. Aim for at least five inputs.",
        min_chars=120,
    )
    inputs_widget
    return inputs_ready, inputs_widget


@app.cell
def _(inputs_ready, inputs_widget, mo, reveal):
    mo.stop(
        not inputs_ready(),
        mo.md("_Write at least a paragraph above. The sample list unlocks when you commit._"),
    )
    sample_inputs = (
        "- **Active diagnoses (problem list and visit-level ICD-10).** For advanced cancer (C-codes with associated metastatic codes), advanced organ failure (I50.2x, J44.x, K72.x, K74.6x, N18.5/N18.6), and dementia stage (G30.x, F02.8x). Caveat: ICD-10 coding lags clinical reality, especially for newly-diagnosed disease.\n\n"
        "- **Encounter history within the past six months.** Admission count, ED visit count, ICU stays. Source: the EHR encounter table. Caveat: outside admissions are often invisible unless the hospital sits on an interoperability network.\n\n"
        "- **Functional status.** Most recent documented Katz or Barthel index, or a structured 'new dependence on ADLs' flag from nursing assessment. Caveat: documentation rates vary by unit and provider.\n\n"
        "- **Medications.** Long-acting opioids prescribed for cancer-related or end-stage organ-failure pain; antineoplastic medications by class. Source: the MAR and outpatient med list. Caveat: outpatient med reconciliation lags admission by hours to days.\n\n"
        "- **Existing palliative-care contact.** Any prior PC consult during this admission OR an outpatient PC clinic visit within the prior six months OR an active hospice enrollment flag. Source: the orders system and the encounter table. This is a *negation* input: if it's present, the rule does not fire.\n\n"
        "- **Goals-of-care documentation.** Presence of a goals-of-care note within the prior six months. Source: structured fields if your EHR has them, otherwise NLP extraction from notes. Caveat: structured-field uptake is uneven.\n\n"
        "- **The surprise question** ('would you be surprised if this patient died in the next twelve months?'), if your hospital captures it. Source: nursing or attending-of-record documentation. Caveat: variable capture; where present, the predictive validity is reasonable."
    )
    reveal(inputs_widget.value, sample_inputs, learner_label="Your input list")
    return (sample_inputs,)


@app.cell
def _(commit_text):
    rule_widget, rule_ready = commit_text(
        "**Step 3.** Write the rule in plain English. One paragraph. Make it specific enough that two different data scientists implementing it would produce the same alert on the same chart. Decide explicitly: does the rule fire passively (appears on a dashboard) or actively (paged to the primary team)? What action does it imply?",
        min_chars=120,
    )
    rule_widget
    return rule_ready, rule_widget


@app.cell
def _(mo, reveal, rule_ready, rule_widget):
    mo.stop(
        not rule_ready(),
        mo.md("_Commit your rule above. The sample unlocks when you do._"),
    )
    sample_rule = (
        "Once daily at 06:00, identify adult inpatients on a medicine or surgical service who meet at least one of "
        "(a) advanced cancer with metastatic or locally advanced disease without curative-intent treatment, "
        "(b) advanced organ failure with at least one prior admission in the past six months, or "
        "(c) moderate-to-severe dementia with new ADL dependence, "
        "AND who have not had a palliative care consultation placed during the current admission, "
        "AND who do not have an active hospice enrollment or an outpatient PC clinic visit within the prior six months. "
        "The rule appears as a soft notification in the primary team's daily census dashboard, not as an interruptive alert. "
        "The notification text reads: \"PC consult criterion met. Consider consult, or document reason for deferral.\" "
        "The action it implies is a structured decision (consult / defer with reason / not applicable), captured in a field used for monitoring uptake and equity. The rule does not page anyone."
    )
    reveal(rule_widget.value, sample_rule, learner_label="Your rule")
    return (sample_rule,)


@app.cell
def _(commit_text):
    edges_widget, edges_ready = commit_text(
        "**Step 4.** Find three edge cases your rule will get wrong. For each: write a short clinical sketch of the patient, state whether the rule will incorrectly fire or incorrectly miss, and name which of Track 02's five sources (phenotypic mimics, suppressed signals, off-cohort, off-window, missing data) is responsible.",
        min_chars=200,
    )
    edges_widget
    return edges_ready, edges_widget


@app.cell
def _(edges_ready, edges_widget, mo, reveal):
    mo.stop(
        not edges_ready(),
        mo.md("_Write at least three short cases above. The sample edge cases unlock when you commit._"),
    )
    sample_edges = (
        "**Edge case 1 (false positive).** "
        "Mr. T, 72, with stage IV colon cancer on second-line FOLFIRI, ECOG 1, asymptomatic, admitted for a port-flush complication. "
        "He already has a documented goals-of-care note from his outpatient oncologist within the past two months. "
        "The rule fires because the active-diagnosis input matches and no inpatient PC consult is on file. "
        "A PC consult here would duplicate work the outpatient team has already done. "
        "**Source:** *missing data*. The rule can't see the outpatient goals-of-care documentation because the structured field is not captured uniformly across the integrated network.\n\n"
        "**Edge case 2 (false negative).** "
        "Ms. K, 55, newly diagnosed three weeks ago with bulbar-onset ALS, admitted for aspiration pneumonia. "
        "Her ICD-10 problem list has 'aspiration pneumonia' and 'dysphagia' but not yet 'amyotrophic lateral sclerosis' as a structured diagnosis. "
        "The rule does not fire: ALS is not in the advanced-organ-failure vocabulary, and the diagnosis hasn't been coded structurally yet. "
        "A PC consult here is essential. "
        "**Source:** *suppressed signal*. The structured representation of her diagnosis lags clinical reality by weeks.\n\n"
        "**Edge case 3 (false negative).** "
        "Mr. R, 68, with metastatic prostate cancer on androgen deprivation, last admitted eight months ago for an unrelated GI bleed. "
        "This admission is for an NSTEMI. "
        "The rule's six-month look-back for prior admissions does not include his last hospitalization, "
        "and the cancer diagnosis alone (without the recurrent-admission criterion in the organ-failure pathway) does not trigger. "
        "He nonetheless has a serious illness and a PC consult would help with longitudinal goals-of-care planning. "
        "**Source:** *off-window data*. The prior admission is real but outside the rule's window."
    )
    reveal(edges_widget.value, sample_edges, learner_label="Your edge cases")
    return (sample_edges,)


@app.cell
def _(commit_text):
    data_widget, data_ready = commit_text(
        "**Step 5.** Name the data the rule depends on, and the failure mode of each source. For every input from Step 2 (and any new ones), say: what system it comes from, what its latency is, and what happens to the rule when that source breaks or drifts.",
        min_chars=150,
    )
    data_widget
    return data_ready, data_widget


@app.cell
def _(data_ready, data_widget, mo, reveal):
    mo.stop(
        not data_ready(),
        mo.md("_Commit your data inventory above. The sample answer unlocks when you do._"),
    )
    sample_data = (
        "- **Problem list and visit-level ICD-10.** Source: EHR. Latency: real-time, but coded reality lags clinical reality by days to weeks for new or recently-changed diagnoses. Failure mode: a recently-recognized advanced cancer or new ALS diagnosis won't trigger until the chart is coded. Mitigation: a manual-override entry point on the rule, plus an NLP-derived problem-list supplement where available.\n\n"
        "- **Encounter history (admissions, ED visits, ICU stays).** Source: EHR encounter table. Latency: near-real-time within the institution. Failure mode: outside admissions invisible without HIE; an interoperability disruption silently shrinks the look-back. Mitigation: monitor HIE feed status and flag patients whose history might be incomplete.\n\n"
        "- **Functional status documentation.** Source: nursing assessment fields. Latency: typically captured within 24 hours of admission. Failure mode: variable documentation rates by unit; the field may be empty entirely on some services. Mitigation: structural improvement (require the field at admission) or treat absence-of-documentation as informative rather than as silence.\n\n"
        "- **Medication administration record and outpatient med list.** Source: EHR pharmacy module. Latency: real-time for inpatient MAR, lagging for outpatient med rec. Failure mode: a discharge from a system the EHR doesn't read means new chronic opioids look like new prescriptions. Mitigation: rely on this input only as supportive.\n\n"
        "- **Existing PC consult, hospice flag, outpatient PC visit.** Source: orders system and outpatient encounter table. Latency: real-time inpatient, near-real-time hospital-affiliated outpatient. Failure mode: hospice enrollment from an agency the hospital doesn't share data with is invisible; the rule will fire on patients who are already enrolled in hospice elsewhere. Mitigation: require a manual review step before any consult is placed, with a free-text field for 'patient already has hospice care: source.'\n\n"
        "- **Goals-of-care documentation.** Source: structured fields where present, NLP extraction otherwise. Latency: real-time for structured, NLP-dependent for free text. Failure mode: uneven structured-field uptake means the rule misses recent goals-of-care work for some patients. Mitigation: NLP-based extraction with manual review for high-stakes alerts; quarterly audit of false positives caused by missed-prior-goals-of-care."
    )
    reveal(data_widget.value, sample_data, learner_label="Your data inventory")
    return (sample_data,)


@app.cell
def _(commit_text):
    failures_widget, failures_ready = commit_text(
        "**Step 6.** Identify the patient subgroups for whom your rule is likely to fail. For each subgroup, name the specific input or design choice that creates the failure, and propose a monitoring approach you would commit to in writing as part of deployment.",
        min_chars=200,
    )
    failures_widget
    return failures_ready, failures_widget


@app.cell
def _(failures_ready, failures_widget, mo, reveal):
    mo.stop(
        not failures_ready(),
        mo.md("_Commit your who-it-fails-for analysis above. The sample answer unlocks when you do._"),
    )
    sample_failures = (
        "- **Patients with non-cancer terminal illness (ALS, late-stage MS, advanced HIV with multiple opportunistic infections).** The rule's vocabulary covers cancer, organ failure, and dementia. The literature already documents systemic PC under-referral for non-cancer terminal disease. Monitor: subgroup analysis of alert rate among patients with these diagnoses versus matched cancer patients, quarterly.\n\n"
        "- **Patients whose serious illness is recent enough that ICD coding hasn't caught up.** The diagnosis inputs lag clinical reality, especially for first-admission patients newly diagnosed with rapidly progressive disease. Monitor: track time-from-clinical-diagnosis-to-structured-diagnosis as an independent quality metric.\n\n"
        "- **Patients whose clinicians use interpreters.** Goals-of-care documentation and the surprise question are documented less reliably in encounters with interpreter use. The rule may fire less often, or rely on weaker inputs, for these patients. Monitor: subgroup alert rate and PC consult uptake stratified by interpreter use, monthly.\n\n"
        "- **Patients from racial or socioeconomic groups historically under-referred for PC.** If a future version of the rule is trained on past consult orders as a positive label, it will learn the existing pattern of who gets consulted and encode that pattern. Monitor: monthly equity audit of alert rate, consult acceptance rate, and goals-of-care conversation completion by race, ethnicity, primary language, and insurance class. Commit to a written stopping rule: if alert rate differs by more than a pre-specified margin across subgroups without clinical justification, the rule comes off until adjudicated.\n\n"
        "- **Patients on services that document functional status less consistently.** The dementia-plus-ADL-dependence pathway depends on a field captured unevenly across units. Monitor: per-unit documentation rates of relevant fields and per-unit alert rates."
    )
    reveal(failures_widget.value, sample_failures, learner_label="Your subgroup analysis")
    return (sample_failures,)


@app.cell
def _(mo):
    final_reflection = mo.ui.text_area(
        label="**Final reflection.** What does your rule deliberately *not* do? What kinds of patients is it not for, what kinds of clinical decisions is it not trying to support, and what would you tell the primary teams in the rollout email about what to ignore? (No reveal. The writing is the work.)",
        placeholder="A paragraph like this is often what separates a deployable rule from one that quietly accretes scope over the first year.",
        rows=6,
        full_width=True,
    )
    mo.vstack(
        [
            final_reflection,
            mo.callout(
                mo.md("_No answer key for this one. It goes into your design document as written._"),
                kind="neutral",
            ),
        ]
    )
    return (final_reflection,)


@app.cell
def _(
    data_widget,
    edges_widget,
    failures_widget,
    final_reflection,
    inputs_widget,
    mo,
    outcome_widget,
    rule_widget,
):
    sections = [
        ("1. Outcome", outcome_widget.value or "_(not yet written)_"),
        ("2. Inputs", inputs_widget.value or "_(not yet written)_"),
        ("3. The rule, in plain English", rule_widget.value or "_(not yet written)_"),
        ("4. Known edge cases", edges_widget.value or "_(not yet written)_"),
        ("5. Data dependencies and failure modes", data_widget.value or "_(not yet written)_"),
        ("6. Subgroups the rule is likely to fail for, and monitoring commitments", failures_widget.value or "_(not yet written)_"),
        ("7. What the rule deliberately does not do", final_reflection.value or "_(not yet written)_"),
    ]
    body = "\n\n".join(f"### {title}\n\n{content}" for title, content in sections)
    document = mo.callout(
        mo.md(
            "## Your design document\n\n"
            "Below are your six committed answers plus your reflection, assembled as a one-page CDR design document. "
            "Copy it out of the browser (Ctrl/Cmd + P → save as PDF, or select and copy) and you have your draft for next week's CDS committee.\n\n"
            "---\n\n"
            + body
        ),
        kind="info",
    )
    document
    return body, document, sections


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What you did in this capstone.

        You took the five moves of computational thinking and applied them in sequence to a real-feeling CDS design problem:

        - **Decomposition** (Track 01) when you named the rule's parts: cohort, signals, thresholds, time window, data source, trigger moment, action.
        - **Patterns and edge cases** (Track 02) when you generated three patients your rule would get wrong on purpose, against the five named sources.
        - **Abstraction** (Track 03) when you decided which inputs to keep, which to drop, and where to draw the line between "in the rule" and "not in the rule."
        - **Algorithmic reading** (Track 04) when you wrote the rule plainly enough that two implementers would produce the same alert.
        - **The trust framework** (Track 05) when you named what the rule depends on, where it will fail, and who it will fail for, with a written monitoring commitment for each subgroup.

        That document is what fluency in computational thinking looks like when it's applied to your own work. You can take it into a real CDS conversation tomorrow.

        ## What comes after this course.

        The five tracks plus this capstone gave you the *vocabulary* of computational thinking. The rest of the curriculum applies that vocabulary to the informatics tools you'll meet next: data literacy (course 02), the privacy and equity context that frames any CDS work (course 03), clinical epidemiology and the 2x2 table (course 04), how the EHR actually stores and moves data (course 05), FHIR (course 06), the data engineering layer (course 07), visualization (course 08), AI in medicine where the trust framework comes back hard (course 09), NLP for the data that lives in notes (course 10), health economics and decision curve analysis (course 11), clinical decision support as the curriculum's own capstone course (course 12), and the things that make any of it last (courses 13 through 15).

        Pick whichever one is closest to the next real problem in front of you and start there.
        """
    )
    return


if __name__ == "__main__":
    app.run()
