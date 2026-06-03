"""Track 05: Sharing and publication.

No visible code. The notebook covers the three sharing questions a published
clinical analysis must answer: what to share at what access tier, where the
code goes, and which reporting guideline applies. Two interactives: a
share / controlled / withhold classifier for a representative set of RA
cohort data elements, and a reporting-guideline picker that maps study
designs to the matched EQUATOR guideline.

WASM-safe: no shared imports, no data files, no relative paths.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    DATA_ELEMENTS = {
        "Patient's full name": {
            "disposition": "Withhold",
            "rationale": (
                "A direct identifier. Removed under HIPAA Safe Harbor (item 1). "
                "Carries no analytic value the synthetic study ID does not carry. "
                "Replaced in the shared dataset by a synthetic study ID."
            ),
        },
        "Medical record number (MRN)": {
            "disposition": "Withhold",
            "rationale": (
                "A direct identifier. Removed under HIPAA Safe Harbor (item 6). "
                "Like the name, replaced by a synthetic study ID in the shared "
                "dataset."
            ),
        },
        "Full date of CRP draw": {
            "disposition": "Withhold",
            "rationale": (
                "Safe Harbor removes all date elements except the year. The "
                "shareable form is either year only or, for a longitudinal "
                "analysis, the time elapsed from a study-defined index date (in "
                "days or weeks). Relative time preserves the trajectory without "
                "exposing the date."
            ),
        },
        "Age in years (capped at 90+)": {
            "disposition": "Share publicly",
            "rationale": (
                "Safe Harbor allows age in years up to 89; ages 90 and above are "
                "aggregated into a single 90+ bin. With that cap applied, age is "
                "shareable publicly and is essential for clinical analysis."
            ),
        },
        "5-digit ZIP code": {
            "disposition": "Withhold",
            "rationale": (
                "Safe Harbor allows only the 3-digit ZIP prefix, and only if the "
                "covered population exceeds 20,000. The 5-digit form is too "
                "narrow. The shareable alternative is ZIP3 with the small-"
                "population check applied, or a coarser geography (state or "
                "census region)."
            ),
        },
        "Free-text rheumatology clinical note": {
            "disposition": "Controlled access",
            "rationale": (
                "Even after a de-identification pipeline (Course 10), free-text "
                "notes carry residual re-identification risk: a misspelled name, "
                "an indirect reference to a colleague, a quoted patient phrase. "
                "Sharing via a DUA-protected controlled-access repository (dbGaP "
                "or the equivalent) is the standard call. Public sharing is "
                "rarely defensible without expert-determination de-identification."
            ),
        },
        "ICD-10 diagnosis code (e.g. M05.79)": {
            "disposition": "Share publicly",
            "rationale": (
                "Diagnosis codes are not identifiers. They are essential for "
                "characterizing the cohort and reproducing the inclusion "
                "criteria. Share at the per-patient level alongside the "
                "synthetic study ID."
            ),
        },
        "Per-patient CRP and DAS28 series (synthetic IDs, relative time)": {
            "disposition": "Controlled access",
            "rationale": (
                "After Safe Harbor scrubbing, synthetic IDs, and relative time, "
                "the per-patient longitudinal series is still potentially "
                "re-identifiable through combinations of disease, trajectory, "
                "age, and clinic. Sharing under a DUA through a controlled-"
                "access repository is the standard call for individual-level "
                "clinical research data; the public-tier alternatives are the "
                "aggregate statistics."
            ),
        },
    }

    STUDY_DESIGNS = {
        "Randomized controlled trial": {
            "guideline": "CONSORT",
            "fullname": "Consolidated Standards of Reporting Trials",
            "covers": (
                "Trial design, randomization, allocation concealment, blinding, "
                "primary and secondary outcomes, harms, registration. A 25-item "
                "checklist plus a participant flow diagram (enrolled, "
                "randomized, received intervention, lost to follow-up, "
                "analyzed)."
            ),
        },
        "Observational cohort, case-control, or cross-sectional study": {
            "guideline": "STROBE",
            "fullname": (
                "Strengthening the Reporting of Observational Studies in "
                "Epidemiology"
            ),
            "covers": (
                "Setting, eligibility, exposure, outcome, confounders, "
                "statistical methods, descriptive data, results, limitations. A "
                "22-item checklist with design-specific sub-items for cohort, "
                "case-control, and cross-sectional studies."
            ),
        },
        "Prediction model (development or validation)": {
            "guideline": "TRIPOD",
            "fullname": (
                "Transparent Reporting of a multivariable prediction model for "
                "Individual Prognosis Or Diagnosis"
            ),
            "covers": (
                "Source of data, predictors, outcome, sample size, missing "
                "data, statistical analysis, model performance (discrimination "
                "and calibration, with cross-reference to Course 09), and "
                "presentation of the final model. TRIPOD+AI (2024) extends the "
                "guideline to machine-learning prediction models."
            ),
        },
        "Systematic review or meta-analysis": {
            "guideline": "PRISMA",
            "fullname": (
                "Preferred Reporting Items for Systematic reviews and "
                "Meta-Analyses"
            ),
            "covers": (
                "Eligibility criteria, information sources, search strategy, "
                "study selection, data extraction, risk-of-bias assessment, "
                "synthesis methods, results, limitations. A 27-item checklist "
                "plus the PRISMA flow diagram (records identified, screened, "
                "assessed, included)."
            ),
        },
        "Diagnostic accuracy study": {
            "guideline": "STARD",
            "fullname": "STAndards for Reporting Diagnostic accuracy studies",
            "covers": (
                "Study design, participants, the index test, the reference "
                "standard, analysis, and results including a 2x2 of test-"
                "positive against the reference standard. The 2x2 ties back to "
                "Course 04. A 30-item checklist plus a flow diagram."
            ),
        },
        "Case report or case series": {
            "guideline": "CARE",
            "fullname": "CAse REport",
            "covers": (
                "Patient information, clinical findings, timeline, diagnostic "
                "assessment, therapeutic intervention, follow-up, and outcomes. "
                "A 13-item checklist intended for the single-patient or small-"
                "series report."
            ),
        },
    }

    return DATA_ELEMENTS, STUDY_DESIGNS, mo


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 05: Sharing and publication

        A journal accepts the RA cohort paper on the condition that the authors complete a data availability statement and confirm the analysis follows the applicable reporting guideline. Three questions follow that the authors had not planned for. What of the data can be shared, given that it derives from identifiable patient records? Where does the analysis code go, and in a form someone can actually run? Which reporting guideline applies to an observational cohort study, and does the manuscript contain every item it requires?

        The track presents the structural answers to all three. Each answer is a small set of decisions, and each decision attaches to a standard tooling layer (the data availability statement, the code repository, the reporting checklist) the field has built to make sharing routine.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Three questions a published paper answers

        The three questions are independent. Each has its own answer, its own artifact, and its own tooling.

        | Question | Answer | Where it lives in the paper |
        |---|---|---|
        | **What of the data can be shared?** | Some elements share publicly, some only under controlled access, some are withheld entirely. | The data availability statement, a single paragraph at the end of the methods or in a dedicated section. |
        | **Where does the code go?** | A public repository with a persistent identifier (a DOI), in a form that re-runs against the shared data. The computational environment is part of the code. | The code availability statement, usually a sentence with a URL and a DOI. |
        | **Which reporting guideline applies?** | The one matched to the study design. The journal expects the design-specific checklist completed and submitted with the manuscript. | The methods section reports against the checklist; the completed checklist itself goes as a supplement. |

        The rest of this track addresses each question.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Question 1: what can be shared

        The defensible answer is graduated. Four tiers of sharing match the kind of information being shared.

        1. **Public** (no access control). Aggregate statistics, ICD-10 frequencies, the cohort's mean DAS28, the analysis code. No individual is reconstructable from public-tier shares.

        2. **Controlled access** (data use agreement required; controlled-access repository, dbGaP for U.S. NIH-funded data). De-identified individual-level data that retains analytic value but carries residual re-identification risk if combined with other sources. A DUA binds the requester to specific uses, prohibits re-identification, and is enforceable.

        3. **Restricted access** (institutional review and direct collaboration). Data that cannot be exported even under a DUA, but that an outside collaborator can analyze inside the originating institution's secure enclave. Federated analysis and analytics-in-place sit here.

        4. **Withhold**. Direct identifiers (name, MRN, full date of birth, full address) and elements that cannot be de-identified to a defensible standard. Replaced in the shared dataset by synthetic IDs and aggregated bins.

        The HIPAA Safe Harbor method from Course 03 sets the floor: eighteen identifier categories must be removed for data to be considered de-identified. Many datasets need expert-determination de-identification in addition, because the Safe Harbor stripped data still carries re-identification risk through combinations of quasi-identifiers. The four-tier ladder above is the operational form of those privacy principles for a publication context.
        """
    )
    return


@app.cell
def _(DATA_ELEMENTS, mo):
    element_pick = mo.ui.dropdown(
        options=list(DATA_ELEMENTS.keys()),
        value=list(DATA_ELEMENTS.keys())[0],
        label="Data element",
    )
    disposition_pick = mo.ui.radio(
        options=["Share publicly", "Controlled access", "Withhold"],
        label="Where does this element go?",
    )
    mo.vstack(
        [
            mo.md(
                "**Pick an element from the dataset, then pick the right place "
                "on the sharing ladder.** The reactive panel below confirms the "
                "right call and gives the rationale."
            ),
            element_pick,
            disposition_pick,
        ]
    )
    return disposition_pick, element_pick


@app.cell
def _(DATA_ELEMENTS, disposition_pick, element_pick, mo):
    _info = DATA_ELEMENTS[element_pick.value]
    _correct = _info["disposition"]
    _chosen = disposition_pick.value
    if _chosen is None:
        _resp = mo.callout(mo.md("_Pick a disposition._"), kind="neutral")
    elif _chosen == _correct:
        _resp = mo.callout(
            mo.md(f"**Correct.** {_info['rationale']}"),
            kind="success",
        )
    else:
        _resp = mo.callout(
            mo.md(
                f"**The right call is _{_correct}_.** {_info['rationale']}"
            ),
            kind="warn",
        )
    _resp
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Question 2: where does the code go

        A result is not reproducible if the data is available but the code that produced the numbers is not. Code-sharing has three components, and journals increasingly require all three.

        1. **A public repository.** Typically GitHub (or GitLab, or Zenodo for a versioned archive). The repository must be public, not private, by the time the paper is published. The README documents how to rerun.

        2. **A persistent identifier.** A GitHub URL alone is not citable: the repository can be deleted or renamed. A persistent identifier (a DOI, usually issued by Zenodo or Figshare against a specific Git tag) is permanent and citable in the manuscript text. Linking the Git tag to the DOI freezes a specific version of the code as the version-of-record for the paper.

        3. **The computational environment.** A bare script is not enough. The Python version, the package versions, the operating system, and (often) the system libraries are part of what produced the numbers. A lockfile (`pyproject.toml` plus `uv.lock`, or `requirements.txt` with pinned versions) records the package state. A container definition (a `Dockerfile`) records the operating-system layer. Together they let a reader rebuild the environment that produced the analysis.

        Code-sharing pairs naturally with version control (Track 03). The Git tag that the DOI points to is the exact commit that produced the published figures, with the full history of how that state was reached.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Question 3: which reporting guideline applies

        A reporting guideline is a checklist that names every item a published study of a given design must include for the work to be assessable. The guidelines are written by working groups of the relevant field, hosted on the **EQUATOR Network** (the searchable library of reporting guidelines for health research), and required or recommended by most journals. The guideline matched to a study design is not a stylistic preference; it is the floor below which the work cannot be peer-reviewed or replicated.

        The match is design-specific. The interactive below maps the common study designs in clinical research to their matched guidelines.
        """
    )
    return


@app.cell
def _(STUDY_DESIGNS, mo):
    design_pick = mo.ui.dropdown(
        options=list(STUDY_DESIGNS.keys()),
        value="Observational cohort, case-control, or cross-sectional study",
        label="Study design",
    )
    mo.vstack(
        [
            mo.md(
                "**Pick the study design.** The reactive panel below names the "
                "matched reporting guideline and what it requires."
            ),
            design_pick,
        ]
    )
    return (design_pick,)


@app.cell
def _(STUDY_DESIGNS, design_pick, mo):
    _info = STUDY_DESIGNS[design_pick.value]
    _body = (
        f"### {_info['guideline']}\n\n"
        f"_{_info['fullname']}_\n\n"
        f"{_info['covers']}"
    )
    mo.callout(mo.md(_body), kind="neutral")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Preprints and persistent identifiers

        Two pieces of infrastructure separate from journals close the publication loop.

        **Preprints** make a finding available immediately, with a time-stamped citable record, before peer review completes. **medRxiv** (clinical and health sciences) and **bioRxiv** (life sciences) are the dominant servers; both are operated by Cold Spring Harbor Laboratory and screened to exclude content that is not scientific research. A preprint is not peer-reviewed and the server says so on every page, but it is citable, indexed by Google Scholar and Europe PMC, and increasingly accepted as a form of priority claim.

        **Persistent identifiers** (DOIs) keep a citation resolvable after the lab server is decommissioned. A DOI is assigned by a registry (Crossref for journal articles, DataCite for datasets and code, the preprint servers for their own preprints), and the registry's job is to keep the DOI pointing at the right URL even if the URL changes. The DOI is what appears in a paper's reference list, not the underlying URL.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The data availability statement: an example

        Together, the three sharing decisions become a paragraph. The structure most journals expect is a tiered description of what is shared and how, with named repositories or contact mechanisms for each tier.

        ```
        Data availability statement

        Aggregate cohort characteristics, ICD-10 code frequencies, and summary
        statistics are publicly available at [repository URL] with DOI [DOI].
        Per-patient longitudinal CRP, DAS28, and biologic-exposure data (with
        synthetic patient identifiers, relative time, and HIPAA Safe Harbor
        de-identification applied) are available under controlled access
        through [controlled-access repository]. Direct identifiers (name,
        medical record number, full dates, exact geography) are not shared at
        any tier. Investigators wishing to access controlled-tier data should
        contact [contact] with a brief description of the proposed analysis.

        Code availability statement

        All analysis code is publicly available under an open-source license
        at [URL], with persistent identifier [DOI]. The repository includes
        a lockfile and container definition sufficient to reproduce the
        published figures from the controlled-access data.
        ```

        The statement does not have to be long. It does have to name every tier, identify the repository or contact mechanism for each, and describe what was withheld and why.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Where this goes next

        Tracks 02 through 04 produced a project that is rerunnable internally. Track 05 is the public-facing layer: the data is at the right tier, the code is in the right repository with a DOI, and the manuscript is reporting against the right checklist. The capstone now audits a synthetic published analysis that did none of this and produces the documentation plan that would fix it.
        """
    )
    return


if __name__ == "__main__":
    app.run()
