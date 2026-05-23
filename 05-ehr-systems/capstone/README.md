# Capstone: course 05

**Audit a synthetic EHR extract for data quality issues using a structured checklist, then watch the cleanup decisions shrink and reshape the cohort.**

You play the data engineer on the rheumatology research team. The PI has asked for a cohort of seropositive RA patients on biologic therapy with at least one DAS28-CRP value documented, so the team can compute response trajectories. You pull the extract. It is a 600-row synthetic export from the institutional CDW, and it has every problem from Track 05 seeded into it: duplicate patients, inconsistent coding, missing structured DAS28, MRN drift, phantom encounters, plausibility failures. Your job is to walk the audit, document the findings, decide the cleanup rules, and see how the cohort that survives compares with the naive count.

The capstone has four parts:

1. **Audit checklist.** Walk the eight categorical problems on the extract and confirm whether each one is present. Each finding gets a remediation proposal.
2. **Cleanup rules.** Translate each remediation into a concrete filter or transformation expressed in pandas-query form.
3. **Cohort assembly.** Apply the cleanup rules in order using `shared.cohort_builder`, watch attrition at each step, and identify the single biggest drop.
4. **Hand-off memo.** The notebook assembles your committed answers into a one-page audit document the analytics team could act on.

**Prerequisite:** all five tracks of this course (especially Tracks 01, 03, and 05).

**Estimated time:** 75 minutes.

**How to start:** open `notebook.py` in Marimo. The extract is built into the notebook (no external file required).
