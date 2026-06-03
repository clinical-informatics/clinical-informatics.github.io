"""Capstone for course 13: Research reproducibility.

The reader audits a synthetic published RA cohort study with poor
reproducibility practices and assembles a documentation plan that would
make the analysis reproducible. Five Socratic commit-then-reveal steps,
one per track. The final cells assemble the reader's answers into a
downloadable Markdown documentation plan.

WASM-safe: no shared imports, no data files, no relative paths.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    MIN_CHARS = 40

    IDEALS = {
        "step1": (
            "The paper's primary claim is a mean difference (27.4 to 18.1 mg/L). "
            "For that claim to be assessable, baseline and follow-up have to be "
            "defined. Neither is. Track 04's interactive showed that four "
            "defensible \"baseline\" choices yield values from 18.7 to 42.1 "
            "mg/L, more than a factor of two. Combined with unstated follow-up "
            "timing and unstated exclusion criteria, the analyst had many "
            "decision points available, any of which could move the reported "
            "difference across the p < 0.05 line. Track 01 named this the "
            "garden of forking paths.\n\n"
            "What is not in the paper: a pre-registered protocol that "
            "constrained which definitions were primary. Without it, a reader "
            "cannot tell which analytic choices were specified in advance and "
            "which were made after the data were inspected. That is the gap "
            "pre-registration exists to close.\n\n"
            "On the three R's:\n\n"
            "- **Reproducible.** Not currently. Neither data nor code is "
            "shared, and the cleaning step happened in Excel without a "
            "history.\n"
            "- **Replicable.** Untestable. The underspecified definitions "
            "have to resolve consistently in a fresh cohort, and the paper "
            "does not say what they resolve to.\n"
            "- **Robust.** Untested. The paper reports no sensitivity "
            "analyses across the defensible alternatives.\n\n"
            "**Structural fix.** Pre-register the analysis plan with a "
            "primary definition of baseline and follow-up before any analytic "
            "decision is made; report sensitivity analyses across the "
            "defensible alternatives in the manuscript."
        ),
        "step2": (
            "Three Track 02 failures are visible from the clues in the "
            "paper.\n\n"
            "**Manuscript filename is `manuscript_FINAL_revised_v3_clean.docx`.** "
            "Versioning in filenames is the canonical anti-pattern; the project "
            "has no Git history, only a folder of files with `FINAL` arms-race "
            "naming.\n\n"
            "**\"Data were cleaned in Excel.\"** Excel cleaning edits the file "
            "in place by default. The original lab export with its original "
            "values is likely no longer recoverable, which violates the read-"
            "only-raw rule and means the analysis cannot be rerun from raw if a "
            "question arises about a specific value.\n\n"
            "**No folder structure, no README.** The project does not separate "
            "inputs from code from outputs. Nothing tells a stranger where the "
            "analysis is, what the raw data is, or in what order the cleaning "
            "ran.\n\n"
            "**Structural fix.** Adopt the four-decisions checklist for the "
            "rewrite. Read-only raw data (keep the original export untouched; "
            "do all cleaning in scripts that write new files). A folder "
            "structure separating `data/`, `code/`, `results/`, `docs/`. "
            "Machine-friendly filenames with ISO 8601 dates and no `FINAL` "
            "versioning. A README written before the rewrite begins, "
            "describing how to rerun the project from raw."
        ),
        "step3": (
            "The three filename revisions (`v3`, `revised`, `clean`) are "
            "evidence the team has been versioning by copy-rename, which is "
            "the failure mode version control solves. The project has no "
            "version control at all.\n\n"
            "Putting the project under Git would record cleaning decisions as "
            "separate commits with written rationales, let the team compare "
            "any two versions of any file, and give the manuscript a citable "
            "Git tag at submission tied to a specific commit hash.\n\n"
            "**Roll-out steps.**\n\n"
            "- Initialize a Git repository in the project folder.\n"
            "- Make an initial commit of the raw lab export. From that "
            "commit forward, raw is read-only.\n"
            "- Reconstruct the cleaning steps as scripts and commit them one "
            "at a time, each with a message explaining what the step does and "
            "why.\n"
            "- Push to a private GitHub repository for the team; make it "
            "public at publication, with a Zenodo DOI tagged at the submission "
            "commit.\n"
            "- Going forward, every change to the writeup, the data, the "
            "code, or the figures is a commit. The `FINAL` filename arms race "
            "disappears.\n\n"
            "The roll-out does not require teaching every author to use Git "
            "from the command line. Most authors interact with the project "
            "through GitHub's web interface (issues, pull requests, edits in "
            "the browser), which is sufficient for the writeup track."
        ),
        "step4": (
            "The data dictionary is the load-bearing missing artifact. The "
            "manuscript reports a mean baseline CRP of 27.4 mg/L, but the "
            "dataset's `crp_baseline` column has no definition attached. Six "
            "entries are missing.\n\n"
            "- **Definition of baseline.** Which draw, on what indexing rule? "
            "Track 04's interactive showed the four defensible candidates "
            "ranging from 18.7 to 42.1 mg/L; the choice has to be named.\n"
            "- **Unit.** mg/L and mg/dL differ by a factor of ten; both are "
            "in clinical use.\n"
            "- **Assay.** Standard CRP and high-sensitivity CRP have "
            "different LOINC codes and different distributions; one or the "
            "other has to be specified.\n"
            "- **Source field.** Which EHR lab code was treated as CRP, and "
            "how cases of multiple codes for the same conceptual lab were "
            "resolved.\n"
            "- **Below-detection handling.** Values reported as `<0.5 mg/L` "
            "have to be either kept as a censored category, recoded to a "
            "midpoint, or dropped; the choice affects the mean.\n"
            "- **Missingness handling.** Patients with no qualifying CRP "
            "draw have to be excluded explicitly, and the exclusion count "
            "reported.\n\n"
            "The `crp_followup` column needs the analogous definition, "
            "including how the time point was chosen and how multiple "
            "follow-up draws were aggregated.\n\n"
            "The transformation log is the second missing artifact. The "
            "\"cleaning in Excel\" note has to be replaced by a sequence of "
            "named scripts, each with a one-line description of what it does, "
            "in the order they run. The OMOP capstone of Course 07 called for "
            "exactly this discipline: every mapping decision, every "
            "value-recoding, every cleanup gets written down because no "
            "standard is lossless.\n\n"
            "**Structural fix.** Produce a data dictionary (one row per "
            "column with all six fields above for CRP and analogous fields "
            "for the other columns), a transformation log (one entry per "
            "script in run order), and a lineage note at the top of the "
            "dataset pointing to the source EHR query and the date the query "
            "ran."
        ),
        "step5": (
            "Three problems in the paper's sharing setup, all fixable.\n\n"
            "**Data availability statement.** \"Available on request from the "
            "corresponding author\" is the standard non-statement. It does not "
            "commit to a tier or a repository, it is not enforceable, and "
            "editorial studies have shown that authors respond to such "
            "requests at low rates and often with substantial delays. Most "
            "journals now reject this language.\n\n"
            "The fix: rewrite as a tiered statement using the Track 05 ladder. "
            "Aggregate cohort statistics, ICD-10 frequencies, and the analysis "
            "code go in a public-tier repository (Zenodo, with a DOI) so they "
            "are citable and accessible without contact. The de-identified "
            "per-patient longitudinal CRP and DAS28 data go in a "
            "controlled-access repository (dbGaP or institutional equivalent) "
            "under a DUA that prohibits re-identification. Direct identifiers "
            "(name, MRN, full dates, exact geography) are withheld entirely; "
            "the shared dataset uses synthetic IDs and relative time.\n\n"
            "**Code availability statement.** Missing entirely. The fix: "
            "publish the cleaning, cohort-building, and analysis code in a "
            "public GitHub repository, archive a specific commit with Zenodo "
            "to get a DOI, and include the computational environment (a "
            "lockfile and a Dockerfile) so the analysis can be rerun against "
            "the controlled-access data.\n\n"
            "**Reporting guideline.** Unnamed. This is an observational "
            "cohort study, so the matched EQUATOR guideline is **STROBE**. "
            "The fix: complete the STROBE checklist (22 items plus "
            "design-specific sub-items), submit it as a supplement, and "
            "ensure the methods section reports against each item. Items the "
            "current methods paragraph fails to cover include eligibility "
            "criteria, exposure definition, confounders considered, "
            "statistical methods detail, and limitations.\n\n"
            "A preprint posted to medRxiv at submission gives a time-stamped "
            "citable record before peer review completes, which is now "
            "standard practice and increasingly valued by funders."
        ),
    }

    return IDEALS, MIN_CHARS, mo


@app.cell
def _(mo):
    mo.md(
        r"""
        # Capstone: Audit a published analysis and produce a documentation plan

        You are asked to audit a published RA cohort study and produce a documentation plan that would make the analysis reproducible. The paper is real-shaped: a community rheumatology practice has submitted a single-center observational paper to a journal. The journal has accepted it conditionally and asked for a data availability statement, a reporting-guideline confirmation, and code availability. The authors have asked for an outside read before they respond.

        The capstone has five steps, one per track of this course. At each step you commit a substantive answer in a text area and then see how a reproducibility-oriented reviewer would think through the same question. The final cell assembles your five answers (plus a short reflection) into a single Markdown documentation plan that a project lead could act on.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            ### The paper to audit

            **Title.** Real-world response to adalimumab in seropositive rheumatoid arthritis: a single-center cohort study.

            **Setting.** A community rheumatology practice. About 1,200 RA patients followed since 2018.

            **Methods (verbatim from the paper).** "We analyzed retrospective EHR data on 1,247 patients with seropositive RA who had been on adalimumab. CRP was measured at baseline and at follow-up. The primary outcome was reduction in CRP at follow-up. Data were cleaned in Excel and imported into R. Analysis used standard descriptive statistics."

            **Results (key claim).** Mean baseline CRP 27.4 mg/L; mean follow-up CRP 18.1 mg/L (p < 0.001). Conclusion of favorable response to adalimumab.

            **Data availability statement.** "Data are available on request from the corresponding author."

            **Code availability statement.** Not mentioned.

            **Reporting guideline.** Not mentioned.

            **Supplementary materials.** One Excel file with a tab labeled "patients" containing the analysis dataset. No data dictionary.

            **The manuscript file on disk.** `manuscript_FINAL_revised_v3_clean.docx`
            """
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    step1_input = mo.ui.text_area(
        label=(
            "Identify the forking-paths risks created by undefined baseline and "
            "follow-up, the absence of pre-registration, and what is or is not "
            "reproducible, replicable, and robust about the analysis as written."
        ),
        placeholder=(
            "Note specifically what the unstated baseline-CRP and follow-up-CRP "
            "definitions expose, the role pre-registration would have played, "
            "and the standing of the analysis on the three R's from Track 01."
        ),
        rows=8,
        full_width=True,
    )
    mo.vstack(
        [
            mo.md(
                "## Step 1: What does Track 01 say about this analysis?\n\n"
                "From a reproducibility-vs-replicability-vs-robustness standpoint, "
                "what concerns does the analytical setup raise? Are forking-paths "
                "risks present? Is there evidence of pre-registration?"
            ),
            step1_input,
        ]
    )
    return (step1_input,)


@app.cell
def _(IDEALS, MIN_CHARS, mo, step1_input):
    if not step1_input.value or len(step1_input.value) < MIN_CHARS:
        _resp = mo.callout(
            mo.md(
                f"_Write at least {MIN_CHARS} characters to commit your answer "
                "and see how we'd think through this._"
            ),
            kind="neutral",
        )
    else:
        _resp = mo.vstack(
            [
                mo.callout(
                    mo.md(f"**Your answer**\n\n{step1_input.value}"),
                    kind="info",
                ),
                mo.callout(
                    mo.md(
                        f"**How we'd think through this**\n\n{IDEALS['step1']}"
                    ),
                    kind="success",
                ),
            ]
        )
    _resp
    return


@app.cell
def _(mo):
    step2_input = mo.ui.text_area(
        label=(
            "Name the Track 02 four-decisions failures the manuscript filename "
            "and the \"Excel cleaning\" note expose, and the structural fixes "
            "the rewrite needs."
        ),
        placeholder=(
            "Cite the specific clues in the paper that point to each failure: "
            "the manuscript filename, the Excel cleaning note, the absence of "
            "any folder structure or README mention."
        ),
        rows=8,
        full_width=True,
    )
    mo.vstack(
        [
            mo.md(
                "## Step 2: What does Track 02 say about this project?\n\n"
                "What organizational decisions did the team skip? The "
                "manuscript filename and the \"Excel cleaning\" note give clues."
            ),
            step2_input,
        ]
    )
    return (step2_input,)


@app.cell
def _(IDEALS, MIN_CHARS, mo, step2_input):
    if not step2_input.value or len(step2_input.value) < MIN_CHARS:
        _resp = mo.callout(
            mo.md(
                f"_Write at least {MIN_CHARS} characters to commit your answer "
                "and see how we'd think through this._"
            ),
            kind="neutral",
        )
    else:
        _resp = mo.vstack(
            [
                mo.callout(
                    mo.md(f"**Your answer**\n\n{step2_input.value}"),
                    kind="info",
                ),
                mo.callout(
                    mo.md(
                        f"**How we'd think through this**\n\n{IDEALS['step2']}"
                    ),
                    kind="success",
                ),
            ]
        )
    _resp
    return


@app.cell
def _(mo):
    step3_input = mo.ui.text_area(
        label=(
            "Specify how the project would shift to version control: initial "
            "commit of raw data, commit-per-step for cleaning, repository "
            "hosting, tagging the submission version."
        ),
        placeholder=(
            "What would the Git roll-out look like in practice? How would the "
            "non-technical co-authors participate?"
        ),
        rows=8,
        full_width=True,
    )
    mo.vstack(
        [
            mo.md(
                "## Step 3: What does Track 03 say about this project?\n\n"
                "What is missing for version control? What would have to change "
                "for the project to support reproducible collaboration?"
            ),
            step3_input,
        ]
    )
    return (step3_input,)


@app.cell
def _(IDEALS, MIN_CHARS, mo, step3_input):
    if not step3_input.value or len(step3_input.value) < MIN_CHARS:
        _resp = mo.callout(
            mo.md(
                f"_Write at least {MIN_CHARS} characters to commit your answer "
                "and see how we'd think through this._"
            ),
            kind="neutral",
        )
    else:
        _resp = mo.vstack(
            [
                mo.callout(
                    mo.md(f"**Your answer**\n\n{step3_input.value}"),
                    kind="info",
                ),
                mo.callout(
                    mo.md(
                        f"**How we'd think through this**\n\n{IDEALS['step3']}"
                    ),
                    kind="success",
                ),
            ]
        )
    _resp
    return


@app.cell
def _(mo):
    step4_input = mo.ui.text_area(
        label=(
            "List the data-dictionary entries the analysis needs (baseline-CRP "
            "definition, unit, assay, source-field, below-detection handling, "
            "missingness) and the transformation-log entries the cleaning "
            "steps require."
        ),
        placeholder=(
            "Anchor each entry to a specific question the paper currently "
            "leaves unanswerable; cite the OMOP \"no standard is lossless\" "
            "cross-reference where it applies."
        ),
        rows=8,
        full_width=True,
    )
    mo.vstack(
        [
            mo.md(
                "## Step 4: What does Track 04 say about this analysis?\n\n"
                "What does the paper's (missing) data dictionary need to "
                "specify before the analysis is defensible? Use the "
                "baseline-CRP problem from the track as the anchor."
            ),
            step4_input,
        ]
    )
    return (step4_input,)


@app.cell
def _(IDEALS, MIN_CHARS, mo, step4_input):
    if not step4_input.value or len(step4_input.value) < MIN_CHARS:
        _resp = mo.callout(
            mo.md(
                f"_Write at least {MIN_CHARS} characters to commit your answer "
                "and see how we'd think through this._"
            ),
            kind="neutral",
        )
    else:
        _resp = mo.vstack(
            [
                mo.callout(
                    mo.md(f"**Your answer**\n\n{step4_input.value}"),
                    kind="info",
                ),
                mo.callout(
                    mo.md(
                        f"**How we'd think through this**\n\n{IDEALS['step4']}"
                    ),
                    kind="success",
                ),
            ]
        )
    _resp
    return


@app.cell
def _(mo):
    step5_input = mo.ui.text_area(
        label=(
            "Rewrite the data availability statement in tiered form; name the "
            "code repository requirement and DOI mechanism; identify the "
            "matched EQUATOR guideline and what its checklist requires."
        ),
        placeholder=(
            "Take each of the three sharing components separately (data, "
            "code, reporting guideline). Specify the tier, the repository or "
            "checklist, and the artifact each produces."
        ),
        rows=8,
        full_width=True,
    )
    mo.vstack(
        [
            mo.md(
                "## Step 5: What does Track 05 say about this paper?\n\n"
                "What is wrong with the paper's data availability statement "
                "and its omission of code availability and a reporting "
                "guideline? What concrete fixes would the journal expect?"
            ),
            step5_input,
        ]
    )
    return (step5_input,)


@app.cell
def _(IDEALS, MIN_CHARS, mo, step5_input):
    if not step5_input.value or len(step5_input.value) < MIN_CHARS:
        _resp = mo.callout(
            mo.md(
                f"_Write at least {MIN_CHARS} characters to commit your answer "
                "and see how we'd think through this._"
            ),
            kind="neutral",
        )
    else:
        _resp = mo.vstack(
            [
                mo.callout(
                    mo.md(f"**Your answer**\n\n{step5_input.value}"),
                    kind="info",
                ),
                mo.callout(
                    mo.md(
                        f"**How we'd think through this**\n\n{IDEALS['step5']}"
                    ),
                    kind="success",
                ),
            ]
        )
    _resp
    return


@app.cell
def _(mo):
    reflection_input = mo.ui.text_area(
        label=(
            "Which of the five failures was most expensive to surface? If you "
            "had been brought in as a consultant six months before submission, "
            "where would you have spent your time first? Write a short paragraph."
        ),
        placeholder=(
            "This reflection is for you. It is included at the end of the "
            "assembled plan but no ideal answer is revealed; the writing "
            "itself is the point."
        ),
        rows=4,
        full_width=True,
    )
    mo.vstack(
        [
            mo.md(
                "## Reflection\n\n"
                "Step back. Of the five failures above, which would you prioritize?"
            ),
            reflection_input,
        ]
    )
    return (reflection_input,)


@app.cell
def _(
    mo,
    reflection_input,
    step1_input,
    step2_input,
    step3_input,
    step4_input,
    step5_input,
):
    brief = f"""# Documentation plan: adalimumab RA cohort study

_A reproducibility plan for the conditionally-accepted manuscript. Produced from the Course 13 capstone audit. Five sections, one per track of the course, plus an author reflection._

## 1. Status assessment (Track 01)

{step1_input.value or '_(not yet committed)_'}

## 2. Project reorganization (Track 02)

{step2_input.value or '_(not yet committed)_'}

## 3. Version control rollout (Track 03)

{step3_input.value or '_(not yet committed)_'}

## 4. Provenance documentation (Track 04)

{step4_input.value or '_(not yet committed)_'}

## 5. Sharing and publication (Track 05)

{step5_input.value or '_(not yet committed)_'}

## Author reflection

{reflection_input.value or '_(not yet committed)_'}

---

_Generated from the Course 13 capstone notebook. This plan is the starting deliverable for the team revising the manuscript. It does not replace the actual project work; it specifies what that work is and what artifacts it produces._
"""
    mo.md(
        "## The assembled documentation plan\n\n"
        "The Markdown below assembles your five answers and the reflection "
        "into a single document. The download button at the end exports it as "
        "a `.md` file the project lead can read."
    )
    return (brief,)


@app.cell
def _(brief, mo):
    mo.md(brief)
    return


@app.cell
def _(brief, mo):
    download = mo.download(
        data=brief.encode("utf-8"),
        filename="reproducibility-documentation-plan.md",
        label="Download the documentation plan as Markdown",
    )
    download
    return (download,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## How to use this plan

        The documentation plan is a starting deliverable, not a finished one. Three things follow.

        First, the structural changes (Tracks 02 and 03) are the cheapest to do first because they unblock everything else. Putting the project under Git, separating raw from processed from results, and writing the README are a one-day effort that pays back across the rewrite.

        Second, the data dictionary and the transformation log (Track 04) are the load-bearing artifacts for the manuscript itself. The mean-baseline-27.4 number cannot be defended without them, and the conditional acceptance depends on defending it.

        Third, the sharing decisions (Track 05) close the publication loop: the tiered data availability statement, the code repository with a DOI, the STROBE checklist, and the medRxiv preprint together form the public-facing artifact set the journal expects.

        The reader who has built this plan can sit across the table from the manuscript authors and tell them what is missing and how to fix it. That is the practice this course exists to teach.
        """
    )
    return


if __name__ == "__main__":
    app.run()
