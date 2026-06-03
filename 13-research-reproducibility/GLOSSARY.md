# Glossary: 13 Research reproducibility

A few terms this course reuses are defined in the [curriculum-wide glossary](../start-here/GLOSSARY.md): OMOP CDM, de-identification, HIPAA, claims data. The reproducibility vocabulary specific to this course appears below.

**Reproducibility.** The property that an independent analyst, given the same data and the same analysis code, obtains the same result. Reproducibility is about the computational pipeline, not about whether the scientific finding is true. An analysis can be fully reproducible and still wrong (the code faithfully reproduces a biased estimate). The opposite case is more common: the finding may be true, but no one can rerun the analysis because the data, the code, or the steps between them were never documented.

**Replicability.** The property that a new study, with new data collected under the same protocol, reaches the same conclusion. Replicability is about the science. It is distinct from reproducibility: reproducibility asks "can I rerun your analysis on your data," replicability asks "if I run your study again from scratch, do I find the same thing." A result can be reproducible (your code runs) but not replicable (a fresh cohort does not show the effect).

**Robustness.** The property that the conclusion survives reasonable changes to the analytic choices: a different model specification, a different handling of missing data, a different outcome cutoff. A finding that holds only under one specific combination of analytic choices is fragile, and the fragility is usually invisible in the published paper.

**Replication crisis.** The documented finding, across psychology, biomedicine, and clinical research, that a large fraction of published results fail to replicate when the study is repeated. The Open Science Collaboration's 2015 psychology replication project and the Begley and Ellis 2012 finding that 47 of 53 landmark preclinical cancer studies could not be reproduced are the canonical references. The crisis is what motivates the practices this course teaches.

**Researcher degrees of freedom.** The many analytic choices an analyst makes that are individually defensible but collectively let the analyst (consciously or not) steer toward a desired result: which covariates to adjust for, which outcome window to use, which patients to exclude, which test to run. The phrase comes from Simmons, Nelson, and Simonsohn 2011.

**p-hacking.** Trying analytic variations until a result crosses the p < 0.05 threshold, then reporting only the variation that worked. p-hacking exploits researcher degrees of freedom. It does not require dishonesty; it can happen one defensible decision at a time.

**HARKing.** Hypothesizing After the Results are Known: presenting a hypothesis that was actually formed after seeing the data as though it had been specified in advance. HARKing converts an exploratory finding into a confirmatory-looking one, which inflates the apparent strength of the evidence.

**Pre-registration.** Recording the study hypothesis, the primary outcome, and the analysis plan in a time-stamped public record before the data are analyzed. Pre-registration is the structural defense against p-hacking and HARKing: the analysis plan exists before the results, so the two cannot be retrofitted to each other. ClinicalTrials.gov registration is the regulatory form of this for trials.

**Provenance.** The recorded origin and processing history of a dataset: where each value came from, what was done to it, by whom, and when. Provenance is the answer to "how did this number get here." Data with good provenance can be traced from a published table back to a source record; data without it cannot be defended when questioned.

**Data lineage.** The step-by-step record of how a dataset was transformed from raw source to analysis-ready form. Lineage is the operational form of provenance: each transformation (a filter, a join, a recode, a unit conversion) is a documented step, so the path from raw to final is reconstructable.

**Audit trail.** A chronological record of the actions taken on data or in a system, sufficient to reconstruct what happened. In the reproducibility context, the audit trail is the union of version-control history, a data-processing log, and the provenance documentation.

**Version control.** A system that records every change to a set of files over time, so any prior state can be recovered and any two states can be compared. Version control replaces the `analysis_final_v2_REALfinal.csv` naming pattern with a single file whose entire history is recorded alongside it. Git is the dominant version-control system.

**Git.** The dominant version-control system. Git records snapshots of a project's files as a history of commits, lets the analyst recover any prior snapshot, and lets two people merge changes made independently. Git is a tool the analyst runs; it is distinct from GitHub, which is a website that hosts Git projects.

**GitHub.** A website that hosts Git repositories and adds collaboration features on top: issues for tracking work and bugs, pull requests for proposing and reviewing changes, and access control for who can see or edit a project. GitLab and Bitbucket are comparable alternatives. A learner can use GitHub's issues and pull requests without writing any code.

**Repository (repo).** The unit Git tracks: a project folder plus the complete history of every change ever made to the files inside it. Cloning a repository copies both the current files and the full history.

**Commit.** A single recorded snapshot in a version-control history, with a message describing what changed and why. A good commit message states the reason for the change, not only the mechanical edit. The commit is the atomic unit of provenance for code.

**Pull request (PR).** A proposed set of changes submitted for review before being merged into the main version of a project. The pull request is where collaborators discuss, critique, and approve a change. For a non-developer, the pull request is the review-and-discussion surface, not a coding step.

**Issue.** A tracked item of work, a question, or a defect, recorded on GitHub (or a comparable tracker) and discussed in a comment thread. Issues are the to-do list and the conversation record of a project; they are usable by non-developers as a project-management tool.

**README.** The plain-text (usually Markdown) file at the top of a project that explains what the project is, how it is organized, how to rerun it, and where the data came from. The README is the first file a stranger opens, and on GitHub it renders automatically on the project's front page.

**README-driven development.** Writing the README, which describes how the project is meant to work, before building the project. The practice forces the structure and the intended workflow to be made explicit at the start, when changing them is cheap, rather than reverse-engineered at the end.

**Data dictionary (codebook).** A document that defines every variable in a dataset: its name, its meaning, its units, its allowed values, and how missingness is represented. A dataset without a data dictionary is uninterpretable to anyone who did not build it, and often to its builder a year later.

**Computational environment.** The specific software versions, packages, and settings under which an analysis was run. The same code can produce different results under different package versions, so reproducibility requires recording the environment (a dependency list, a lock file, or a container) alongside the code.

**FAIR principles.** A framework for research-data stewardship: data should be Findable, Accessible, Interoperable, and Reusable. FAIR describes properties of well-managed data and its metadata; it is the guidance most funders and journals now point to for data-management plans. FAIR is about good stewardship and does not by itself mean the data are open.

**Persistent identifier.** A durable, resolvable reference to a digital object that does not break when the object is moved. The DOI (Digital Object Identifier) is the common form for papers, preprints, and datasets. Citing a dataset by DOI, rather than by a lab-server URL that will eventually 404, is the practice that keeps a citation resolvable.

**Data availability statement.** A required section of a published paper that states whether the underlying data are available, where, and under what access conditions. The statement makes the sharing decision explicit and reviewable rather than leaving it implicit.

**Preprint.** A complete manuscript posted to a public server (medRxiv, bioRxiv, arXiv) before, or in parallel with, peer review. Preprints make findings available immediately and establish a time-stamped, citable record; they have not been peer reviewed, which is the property a reader must keep in mind.

**EQUATOR Network.** The organization (Enhancing the QUAlity And Transparency Of health Research) that maintains the library of reporting guidelines for health research. EQUATOR is where an author goes to find the guideline that applies to a given study design.

**Reporting guideline.** A checklist of the items a given study type must report for the work to be assessable and reproducible. The design-specific guidelines are the operational ones: CONSORT for randomized trials, STROBE for observational studies, TRIPOD for prediction models, PRISMA for systematic reviews, STARD for diagnostic-accuracy studies. A reporting guideline specifies what to report, not how to do the study.
