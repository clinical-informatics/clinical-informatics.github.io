"""Track 03: Version control without coding.

No visible code. The notebook presents Git in plain English, distinguishes
Git from GitHub, and displays a small synthetic project's commit history
and a pull request as readable artifacts. No commands run; the reader
inspects commits via dropdown and reviews a pull request that violates
a project convention.

WASM-safe: no shared imports, no data files, no relative paths.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    COMMITS = [
        {
            "hash": "c5a3b1f",
            "author": "M. Felix <m.felix@example.org>",
            "date": "2024-01-18 14:30",
            "subject": "Add baseline characteristics table",
            "body": (
                "Added code/04-baseline-table.py producing "
                "results/tables/baseline-characteristics.csv. Reports n, age (mean, SD), "
                "sex, seropositivity, time since RA diagnosis, baseline DAS28."
            ),
            "files": [
                "+ code/04-baseline-table.py",
                "+ results/tables/baseline-characteristics.csv",
            ],
            "diff_file": None,
            "diff": None,
        },
        {
            "hash": "4d09c87",
            "author": "M. Felix <m.felix@example.org>",
            "date": "2024-01-16 09:23",
            "subject": "Switch CRP trajectory to median (skewed distribution)",
            "body": (
                "The CRP distribution is right-skewed: 92% of values fall between 0 and "
                "60 mg/L, with a long tail to ~200 mg/L during flares. Mean is pulled by "
                "the tail and overstates the central tendency. Switched to median + IQR. "
                "Reviewed with J. Park."
            ),
            "files": [
                "~ code/03-make-figures.py",
                "~ results/figures/crp-trajectory.png",
            ],
            "diff_file": "code/03-make-figures.py",
            "diff": (
                "- ax.plot(df['week'], df.groupby('week')['crp'].mean(), label='Mean CRP')\n"
                "+ ax.plot(df['week'], df.groupby('week')['crp'].median(), label='Median CRP')\n"
                "+ ax.fill_between(\n"
                "+     df['week'],\n"
                "+     df.groupby('week')['crp'].quantile(0.25),\n"
                "+     df.groupby('week')['crp'].quantile(0.75),\n"
                "+     alpha=0.2,\n"
                "+     label='IQR (25-75th percentile)',\n"
                "+ )"
            ),
        },
        {
            "hash": "18b9e22",
            "author": "M. Felix <m.felix@example.org>",
            "date": "2024-01-15 11:48",
            "subject": "Initial CRP trajectory figure",
            "body": (
                "Added code/03-make-figures.py. Produces "
                "results/figures/crp-trajectory.png showing mean CRP over time across "
                "the cohort. Will revisit the mean vs median question after looking at "
                "the distribution shape."
            ),
            "files": [
                "+ code/03-make-figures.py",
                "+ results/figures/crp-trajectory.png",
            ],
            "diff_file": None,
            "diff": None,
        },
        {
            "hash": "33ae771",
            "author": "M. Felix <m.felix@example.org>",
            "date": "2024-01-11 10:05",
            "subject": "Build baseline cohort (n=1247 RA patients)",
            "body": (
                "Added code/02-build-cohort.py. Joins cleaned labs to the patient table "
                "and applies cohort criteria (anti-CCP positive or ICD-10 M05/M06, at "
                "least one CRP in the index window, age 18 or older). Cohort size: 1247."
            ),
            "files": [
                "+ code/02-build-cohort.py",
                "+ data/processed/cohort.csv",
            ],
            "diff_file": None,
            "diff": None,
        },
        {
            "hash": "92cf015",
            "author": "M. Felix <m.felix@example.org>",
            "date": "2024-01-09 16:40",
            "subject": "Clean labs: dedupe, parse dates, drop invalid CRPs",
            "body": (
                "Added code/01-clean-labs.py. Removes 4 duplicate rows. Parses the date "
                "column from string to date type. Drops 2 rows with CRP recorded as "
                "negative (entry errors). Writes data/processed/labs-clean.csv. Raw file "
                "unchanged."
            ),
            "files": [
                "+ code/01-clean-labs.py",
                "+ data/processed/labs-clean.csv",
            ],
            "diff_file": None,
            "diff": None,
        },
        {
            "hash": "e7b8d4a",
            "author": "M. Felix <m.felix@example.org>",
            "date": "2024-01-08 14:22",
            "subject": "Add raw lab export (2024-01-08 pull)",
            "body": (
                "Ingested labs CSV from the IRB-approved data pull on 2024-01-08. File "
                "placed under data/raw/. Read-only from this point forward."
            ),
            "files": ["+ data/raw/2024-01-08_labs.csv"],
            "diff_file": None,
            "diff": None,
        },
        {
            "hash": "a1f23c0",
            "author": "M. Felix <m.felix@example.org>",
            "date": "2024-01-05 09:14",
            "subject": "Initialize project: README, folder skeleton",
            "body": (
                "Created README.md describing the analysis plan, the folder layout, and "
                "the order in which code is run. Created data/, code/, results/, docs/ "
                "directories. Raw data not yet ingested."
            ),
            "files": [
                "+ README.md",
                "+ data/",
                "+ code/",
                "+ results/",
                "+ docs/",
            ],
            "diff_file": None,
            "diff": None,
        },
    ]

    PR_DATA = {
        "number": 14,
        "title": "Add ESR trajectory alongside CRP",
        "author": "J. Park",
        "branch": "add-esr-trajectory",
        "base": "main",
        "description": (
            "ESR is the slower-moving complement to CRP and the rheumatology audience "
            "expects both side by side. Adding it as a second y-axis on the trajectory "
            "figure (commit 18b9e22). No changes to the cohort or the data."
        ),
        "files_changed": "code/03-make-figures.py (+8 -1)",
        "diff": (
            "  ax.plot(df['week'], df.groupby('week')['crp'].median(), label='Median CRP')\n"
            "+ ax2 = ax.twinx()\n"
            "+ ax2.plot(\n"
            "+     df['week'],\n"
            "+     df.groupby('week')['esr'].mean(),\n"
            "+     color='steelblue', linestyle='--', label='Mean ESR',\n"
            "+ )\n"
            "+ ax2.set_ylabel('ESR (mm/hr)')"
        ),
        "review_comment_author": "M. Felix",
        "review_comment_date": "2024-01-19",
        "review_comment_body": (
            "Per commit 4d09c87 we switched the CRP trajectory to median because of "
            "right skew. ESR has the same distributional shape. Recommend using median "
            "+ IQR for consistency with the existing convention."
        ),
    }

    return COMMITS, PR_DATA, mo


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 03: Version control without coding

        The `analysis_FINAL_use_this_one.csv` problem from Track 02 has a structural solution. A tool records every version of every file in a project automatically, keeps them all, and lets anyone recover any prior state or compare any two states. The tool is **version control**. The dominant version-control system is **Git**.

        The reproducibility case for version control is direct. The complete history of the project is a sequence of recorded snapshots, each one tied to a written reason. The version that produced any figure or table can always be located. The decision behind any change is on the record. Two versions can always be compared. Multiple people can work on the same project at the same time and the history merges cleanly. No commands run in this track. The notebook displays a small project's commit history and a pull request as readable artifacts. The reader inspects commits via a dropdown and reviews a pull request that violates a project convention.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What Git does, in one paragraph

        Git records the state of a project at the moments you tell it to record (a **commit**). Each commit captures the exact contents of every file at that moment, together with a written message explaining the change. The history of the project is a chronological sequence of commits, none of which is ever overwritten. Recovering any prior state is a matter of asking for the commit. Comparing any two states is a matter of asking for the difference between two commits. Multiple collaborators work on the project in parallel by creating **branches** (separate lines of history), and their work is merged back into the main project through a review-and-merge step. None of this requires manual version management; the system does it.
        """
    )
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            **Git is the version-control system. GitHub is a website that hosts Git projects and adds collaboration features on top of them.** Conflating the two is the most common point of confusion. Git is software that runs on any computer and works without an internet connection. GitHub is one of several services (GitLab and Bitbucket are similar) that host Git histories online and add issues, pull requests, code review, and access control. A project can use Git without GitHub. The reverse is not possible.
            """
        ),
        kind="warn",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Three concepts to know

        Three units of work cover essentially all of the collaboration a clinical data project does on GitHub. The first is a Git concept; the second and third are GitHub concepts built on top of Git.

        | Concept | What it is | What it answers |
        |---|---|---|
        | **Commit** | A recorded snapshot of the project at a moment in time, with a written message explaining the change. | What changed, when, by whom, and why. |
        | **Issue** | A tracked unit of work or discussion attached to the project. Has a title, a description, a thread of comments, and a status (open / closed). | What we are working on, what we have decided, what we have not yet decided. |
        | **Pull request (PR)** | A proposed change to the project: a set of commits on a branch, alongside a description and a review thread, awaiting approval to merge. | Should this change land, and on whose say-so. |

        A clinician collaborating on a data project uses all three without writing code. Issues serve as a project-management tool: an issue records an unresolved question about the analysis plan, a decision the team needs to make, or a defect in the data. A pull request is a review surface: the proposed change is visible, the diff is visible, anyone can comment, and the merge is gated on review. The collaboration patterns are independent of the language a project is written in; a Markdown-and-CSV analysis uses them the same way a Python codebase does.
        """
    )
    return


@app.cell
def _(COMMITS, mo):
    _lines = [
        f"{c['hash']}  {c['date'][:10]}  {c['subject']}" for c in COMMITS
    ]
    _hist = "\n".join(_lines)
    _body = (
        "## A project's history is its sequence of commits\n\n"
        "Below is the commit history of a small synthetic RA cohort analysis, in the "
        "standard short form. Newest commit first. Each line is one recorded snapshot "
        "of the project, tied to the reason for the change. Picking any of them brings "
        "up the full record below.\n\n"
        f"```\n{_hist}\n```\n"
    )
    mo.md(_body)
    return


@app.cell
def _(COMMITS, mo):
    commit_pick = mo.ui.dropdown(
        options=[c["subject"] for c in COMMITS],
        value=COMMITS[1]["subject"],
        label="Commit to inspect",
    )
    mo.vstack(
        [
            mo.md(
                "**Pick a commit to see its full record.** The default is the "
                "median-vs-mean fix, which has the most informative diff."
            ),
            commit_pick,
        ]
    )
    return (commit_pick,)


@app.cell
def _(COMMITS, commit_pick, mo):
    _c = next(c for c in COMMITS if c["subject"] == commit_pick.value)
    _files_lines = "\n".join(f"  {f}" for f in _c["files"])
    _hdr = (
        f"commit {_c['hash']}\n"
        f"Author: {_c['author']}\n"
        f"Date:   {_c['date']}\n\n"
        f"    {_c['subject']}\n\n"
        f"    {_c['body']}\n\n"
        f"Files changed ({len(_c['files'])}):\n"
        f"{_files_lines}"
    )
    _body = f"```\n{_hdr}\n```\n"
    if _c["diff"]:
        _body += (
            f"\n**Diff for `{_c['diff_file']}`:**\n\n"
            f"```diff\n{_c['diff']}\n```\n"
        )
    else:
        _body += (
            "\n_No diff displayed for this commit. New files are added in their "
            "entirety; the file list above records the additions._\n"
        )
    mo.md(_body)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A pull request is a review surface for a proposed change

        The history above is the project's main line. Proposed changes do not merge into it directly. A collaborator makes a **branch** (a parallel line of history) and commits their proposed change there. They then open a **pull request** asking that their branch be merged into the main line. The pull request displays the proposed change as a diff, alongside a description from the author and a thread where reviewers comment. The change does not merge until a reviewer approves.

        Below is an open pull request on the same project. The author proposes adding an ESR trajectory alongside the CRP trajectory established in commit `18b9e22`. One inline review comment has been posted. The reader has been asked to give a second review.
        """
    )
    return


@app.cell
def _(PR_DATA, mo):
    _body = (
        f"### Pull request #{PR_DATA['number']}: {PR_DATA['title']}\n\n"
        f"**Author:** {PR_DATA['author']}  \n"
        f"**Status:** Open  \n"
        f"**Branch:** `{PR_DATA['branch']}` into `{PR_DATA['base']}`\n\n"
        "**Description**\n\n"
        f"{PR_DATA['description']}\n\n"
        "**Files changed**\n\n"
        f"`{PR_DATA['files_changed']}`\n\n"
        f"```diff\n{PR_DATA['diff']}\n```\n\n"
        "**Review comments (1)**\n\n"
        f"_{PR_DATA['review_comment_author']} commented on "
        f"{PR_DATA['review_comment_date']}:_\n\n"
        f"> {PR_DATA['review_comment_body']}\n\n"
        "_(no reply yet from the author)_"
    )
    mo.callout(mo.md(_body), kind="neutral")
    return


@app.cell
def _(mo):
    pr_action = mo.ui.radio(
        options=[
            "Approve",
            "Request changes",
            "Comment",
        ],
        label=(
            "You are the assigned second reviewer. The author has not yet "
            "responded to the inline comment. Which review action is the right "
            "one to take right now?"
        ),
    )
    pr_action
    return (pr_action,)


@app.cell
def _(mo, pr_action):
    if pr_action.value is None:
        _resp = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif pr_action.value == "Request changes":
        _resp = mo.callout(
            mo.md(
                "**Correct.** A reviewer requests changes when something must change "
                "before the work can merge: the proposed change violates an established "
                "project convention without addressing the inconsistency, the math is "
                "wrong, the description and the code disagree, a needed test is missing. "
                "The first of those applies here. The project's convention, set in commit "
                "`4d09c87` with a written rationale (right-skewed distribution), is "
                "median plus IQR for laboratory trajectories. The PR uses mean for ESR, "
                "which has the same distributional shape, and the inline comment raising "
                "the inconsistency has not been answered. Merging now would commit a "
                "quietly inconsistent figure to the project history. Requesting changes "
                "is what version control is for: the disagreement is captured, recorded, "
                "and resolved before the change is in the history, not after."
            ),
            kind="success",
        )
    elif pr_action.value == "Approve":
        _resp = mo.callout(
            mo.md(
                "**Approve is the unconditional \"merge this\" verdict.** It is the "
                "right call when the change is correct, complete, and consistent with "
                "the rest of the project. Here the PR uses mean for ESR while the "
                "established convention from commit `4d09c87` is median plus IQR for "
                "right-skewed lab trajectories. The inline comment surfacing this is "
                "unanswered. Approving now records the inconsistency in the project "
                "history, which is the failure mode the review step is meant to prevent."
            ),
            kind="warn",
        )
    else:
        _resp = mo.callout(
            mo.md(
                "**Comment records a thought without a verdict.** It is the right tool "
                "for a non-blocking suggestion (\"consider a two-panel layout next "
                "time\"). The question here is not a suggestion. The PR violates a "
                "convention the project committed deliberately, the inline review "
                "comment has surfaced this, and the author has not responded. Leaving "
                "a Comment-only review leaves the disagreement unresolved at the moment "
                "the review is meant to resolve it. Request changes is the action that "
                "holds the merge until the convention question is answered."
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

        Version control records what changed in the code and the writeups, when, and why. It does not record where the data came from or what was done to it inside any particular script. A clean Git history still leaves the question "this column means what, in what units, and how was it derived?" unanswered. The next track covers data provenance: the documentation, dictionaries, and transformation logs that answer the question Git cannot answer. The reflection from Course 07's OMOP capstone applies directly here: every concept mapping is a provenance decision, and no standard is lossless.
        """
    )
    return


if __name__ == "__main__":
    app.run()
