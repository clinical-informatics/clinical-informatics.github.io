"""Capstone for course 05: EHR systems.

A building capstone. The learner audits a 600-row synthetic EHR extract
for data quality issues, proposes remediation, and uses the shared
cohort builder to watch the cleanup decisions shrink and reshape the
final RA-biologic-DAS28 cohort.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd

    rng = np.random.default_rng(20260518)
    return mo, np, pd, rng


@app.cell
def _(mo, pd):
    # CohortBuilder inlined from shared/cohort_builder.py so the WASM export
    # is self-contained. Pyodide cannot import sibling modules from the source
    # tree, so the live-site export needs the class defined in the notebook
    # itself. Mirrors the public API of start-here/shared/cohort_builder.py.

    from dataclasses import dataclass, field

    @dataclass
    class Criterion:
        expression: str
        plain_english: str
        survivors: int = 0
        lost: int = 0

    @dataclass
    class CohortBuilder:
        df: pd.DataFrame
        patient_id_col: str = "patient_id"
        criteria: list = field(default_factory=list)

        def add_criterion(self, expression, plain_english):
            self.criteria.append(
                Criterion(expression=expression, plain_english=plain_english)
            )
            return self

        def reset(self):
            self.criteria.clear()
            return self

        def evaluate(self):
            current = self.df.copy()
            starting = len(current)
            rows = [
                {
                    "step": 0,
                    "criterion": "Starting cohort",
                    "patients_remaining": starting,
                    "patients_lost_this_step": 0,
                }
            ]
            previous = starting
            for i, crit in enumerate(self.criteria, start=1):
                try:
                    current = current.query(crit.expression)
                except Exception as exc:
                    rows.append(
                        {
                            "step": i,
                            "criterion": f"{crit.plain_english} (error: {exc})",
                            "patients_remaining": previous,
                            "patients_lost_this_step": 0,
                        }
                    )
                    continue
                remaining = len(current)
                lost = previous - remaining
                crit.survivors = remaining
                crit.lost = lost
                rows.append(
                    {
                        "step": i,
                        "criterion": crit.plain_english,
                        "patients_remaining": remaining,
                        "patients_lost_this_step": lost,
                    }
                )
                previous = remaining
            return pd.DataFrame(rows)

        def surviving_patients(self):
            current = self.df.copy()
            for crit in self.criteria:
                try:
                    current = current.query(crit.expression)
                except Exception:
                    continue
            return current

        def render(self):
            table = self.evaluate()
            starting = int(table.iloc[0]["patients_remaining"])
            ending = int(table.iloc[-1]["patients_remaining"])
            biggest_drop = (
                table.iloc[1:]
                .sort_values("patients_lost_this_step", ascending=False)
                .head(1)
                if len(table) > 1
                else None
            )
            if biggest_drop is not None and len(biggest_drop) > 0:
                drop_label = biggest_drop.iloc[0]["criterion"]
                drop_n = int(biggest_drop.iloc[0]["patients_lost_this_step"])
                summary = (
                    f"You started with **{starting}** patients and ended with **{ending}**. "
                    f"The single biggest drop happened at the step **{drop_label}**, "
                    f"which removed **{drop_n}** patients."
                )
            else:
                summary = (
                    f"You started with **{starting}** patients and ended with **{ending}**."
                )
            return mo.vstack(
                [
                    mo.md("### Your cohort, step by step"),
                    mo.ui.table(table, selection=None),
                    mo.callout(mo.md(summary), kind="info"),
                ]
            )

    return (CohortBuilder,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # Capstone: course 05. Audit, clean, assemble.

        ## The PI's request

        You are the data engineer embedded in a rheumatology research team. The PI runs into your office:

        > We're putting together a paper on early-response trajectories to TNF-alpha inhibitors in seropositive RA. I want a cohort of all patients in our system with a confirmed seropositive RA diagnosis, currently on a TNFi (adalimumab, etanercept, infliximab, golimumab, certolizumab), with at least one DAS28-CRP value documented since their biologic start date. The faster the better.

        You write the SQL against the institutional CDW (Track 03) and pull a 600-row patient-level extract. Before you hand it to the PI, you remember Track 05: the extract has all the data-quality problems the CDW inherits from the operational EHR (Track 01) and the messaging layer (Track 02). You decide to audit it first.

        This capstone has four parts:

        1. **The extract.** Generated below. 600 patients, all the realistic data-quality problems seeded.
        2. **Audit.** Walk eight categorical issues and confirm whether each one is present in this extract.
        3. **Cleanup.** Translate each finding into a concrete filter. Apply the filters in order with the shared cohort builder.
        4. **Hand-off memo.** A one-page document the analytics team could act on.
        """
    )
    return


@app.cell
def _(np, pd, rng):
    # Build the 600-row patient-level extract with seeded data-quality issues.
    n_patients = 600

    patient_id = [f"P-{i:05d}" for i in range(1, n_patients + 1)]
    age = rng.normal(58, 13, n_patients).clip(20, 90).round(0).astype(int)
    sex = rng.choice(["F", "M"], size=n_patients, p=[0.72, 0.28])

    # Diagnosis distribution. 65% have RA (M05.79 or M05.9), 35% are on the
    # extract for unrelated reasons (the SQL pulled them in because of the join logic).
    has_ra = rng.random(n_patients) < 0.65
    # Some RA rows use the deprecated/imprecise M05.9 code instead of M05.79.
    ra_code = np.where(
        has_ra,
        rng.choice(["M05.79", "M05.9"], size=n_patients, p=[0.75, 0.25]),
        rng.choice(["I10", "E11.9", "M79.7", "K21.9", "F32.9"], size=n_patients),
    )

    # Seropositive flag: anti-CCP or RF positive (true seropositive RA).
    # Only meaningful when has_ra is True.
    seropositive = np.where(has_ra & (rng.random(n_patients) < 0.78), True, False)

    # On a TNFi: among RA patients, 55% on TNFi. Among non-RA, ~3% (off-label or other indications).
    on_tnfi_now = np.where(
        has_ra,
        rng.random(n_patients) < 0.55,
        rng.random(n_patients) < 0.03,
    )

    # Currency failure: 15% of "active TNFi" rows are actually stopped.
    # We'll record the truth in a separate column the audit reveals.
    tnfi_currency = np.where(
        on_tnfi_now,
        rng.choice(["active", "stopped"], size=n_patients, p=[0.85, 0.15]),
        "none",
    )

    # DAS28 structured: 60% of TNFi patients have a structured DAS28 value.
    # The other 40% have it only in notes (or not at all).
    das28_structured = np.where(
        on_tnfi_now & (rng.random(n_patients) < 0.60),
        rng.uniform(1.8, 6.4, n_patients).round(1),
        np.nan,
    )

    # CRP value. 8% are implausible (>1000 mg/L), simulating typo / unit errors.
    crp_base = rng.gamma(2.0, 8.0, n_patients).clip(0.1, 200.0).round(1)
    crp_implausible = rng.random(n_patients) < 0.08
    crp_value = np.where(crp_implausible, rng.uniform(1500, 9000, n_patients).round(0), crp_base)

    # Duplicate MRNs: 30 patients have a second row with a slightly different name.
    # We mark these rows so the audit can confirm dedup logic.
    has_duplicate_mrn_partner = np.zeros(n_patients, dtype=bool)
    dup_index_pairs = rng.choice(n_patients, size=30, replace=False)
    has_duplicate_mrn_partner[dup_index_pairs] = True

    # MRN drift: 20 patients have an old MRN value that should be linked to a current MRN.
    mrn_drift_old = np.full(n_patients, "", dtype=object)
    drift_indices = rng.choice(np.arange(n_patients)[~has_duplicate_mrn_partner], size=20, replace=False)
    for idx in drift_indices:
        mrn_drift_old[idx] = f"OLD-{patient_id[idx]}"

    # Phantom encounter: 12 patients have a canceled-encounter flag they should be filtered against.
    phantom_encounter = np.zeros(n_patients, dtype=bool)
    phantom_indices = rng.choice(n_patients, size=12, replace=False)
    phantom_encounter[phantom_indices] = True

    extract = pd.DataFrame({
        "patient_id": patient_id,
        "mrn": [f"ER-{p[2:]}" for p in patient_id],
        "mrn_old": mrn_drift_old,
        "age": age,
        "sex": sex,
        "primary_dx_code": ra_code,
        "seropositive": seropositive,
        "on_tnfi_active_flag": on_tnfi_now,
        "tnfi_status_truth": tnfi_currency,
        "das28_structured": das28_structured,
        "crp_value_mgL": crp_value,
        "duplicate_mrn_partner": has_duplicate_mrn_partner,
        "phantom_encounter": phantom_encounter,
    })
    extract.index = range(1, len(extract) + 1)
    extract.index.name = "row"

    return (extract,)


@app.cell
def _(extract, mo):
    mo.vstack([
        mo.md(
            f"""
            ## Step 1: the extract

            **{len(extract):,} patients**, one row per patient. The columns:

            - **`patient_id`, `mrn`** are the chart-side identifiers. `mrn_old` is populated when the patient has a merge history.
            - **`age`, `sex`** are demographics.
            - **`primary_dx_code`** is the primary diagnosis code from the index visit (M05.79 = seropositive erosive RA; M05.9 = unspecified RA; the others are non-RA).
            - **`seropositive`** is the lab-confirmed serology flag.
            - **`on_tnfi_active_flag`** is what the EHR's medication-active flag says.
            - **`tnfi_status_truth`** is what the truth is (some "active" rows are actually stopped; this column is here so you can see the currency failure).
            - **`das28_structured`** is the most-recent structured DAS28-CRP value. NaN when there is none in the structured field.
            - **`crp_value_mgL`** is the most-recent CRP. Some values are implausible.
            - **`duplicate_mrn_partner`** is True when this row has a partner row representing the same patient under a different MRN.
            - **`phantom_encounter`** is True when this patient's index visit was actually canceled.

            First eight rows so you have the shape in your head:
            """
        ),
        mo.as_html(extract.head(8)),
    ])
    return


@app.cell
def _(extract, mo, pd):
    audit_summary = {
        "Duplicate MRNs": int(extract["duplicate_mrn_partner"].sum()),
        "MRN drift (merge history)": int((extract["mrn_old"] != "").sum()),
        "Inconsistent RA coding (M05.9)": int(((extract["primary_dx_code"] == "M05.9")).sum()),
        "Missing structured DAS28": int(extract["das28_structured"].isna().sum()),
        "Implausible CRP (>1000 mg/L)": int((extract["crp_value_mgL"] > 1000).sum()),
        "Phantom encounters": int(extract["phantom_encounter"].sum()),
        "Currency failure (stopped TNFi flagged active)":
            int(((extract["on_tnfi_active_flag"]) & (extract["tnfi_status_truth"] == "stopped")).sum()),
        "Non-RA rows in extract": int(((extract["primary_dx_code"] != "M05.79") & (extract["primary_dx_code"] != "M05.9")).sum()),
    }
    audit_summary_df = pd.DataFrame(
        list(audit_summary.items()),
        columns=["Finding", "Rows affected"],
    )
    audit_df = mo.as_html(audit_summary_df)
    return audit_df, audit_summary


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Step 2: the audit checklist

        Eight categorical data-quality problems from Track 05 are seeded in this extract. Before you do any cleanup, walk the checklist and confirm whether each one is present. The multiselect below collects your findings.
        """
    )
    return


@app.cell
def _(mo):
    audit_picks = mo.ui.multiselect(
        options=[
            "Duplicate MRNs",
            "MRN drift (merge history)",
            "Inconsistent RA coding (M05.9)",
            "Missing structured DAS28",
            "Implausible CRP (>1000 mg/L)",
            "Phantom encounters",
            "Currency failure (stopped TNFi flagged active)",
            "Non-RA rows in extract",
            "Sharp/van der Heijde scores in note-only form",
        ],
        label=(
            "**Which of these data-quality problems are present in this extract? Pick all that apply.** "
            "(There are eight present and one decoy that this extract does not surface.)"
        ),
    )
    audit_picks
    return (audit_picks,)


@app.cell
def _(audit_df, audit_picks, audit_summary, mo):
    mo.stop(
        not audit_picks.value or len(audit_picks.value) == 0,
        mo.md("_Make at least one selection above to see the reveal._"),
    )

    expected = {
        "Duplicate MRNs",
        "MRN drift (merge history)",
        "Inconsistent RA coding (M05.9)",
        "Missing structured DAS28",
        "Implausible CRP (>1000 mg/L)",
        "Phantom encounters",
        "Currency failure (stopped TNFi flagged active)",
        "Non-RA rows in extract",
    }
    decoy = "Sharp/van der Heijde scores in note-only form"

    picked = set(audit_picks.value)
    missed = sorted(expected - picked)
    false_positives = sorted(picked - expected)

    if decoy in picked:
        decoy_note = (
            "**You picked the decoy.** Sharp/van der Heijde scores in note-only form are a real Track 04 / Track 05 problem, "
            "but this particular patient-level extract does not surface them. (The PDF reports would live in the document store, "
            "not in this row-per-patient table.) Worth knowing it is real; not worth flagging here."
        )
    else:
        decoy_note = "**You correctly skipped the decoy.** Sharp/van der Heijde notes are a real problem, but not visible at this extract level."

    miss_note = (
        f"You missed: {', '.join(missed)}. Worth a second pass." if missed else "You caught all eight present findings."
    )
    fp_note = (
        f"You picked items that are not actually present: {', '.join(false_positives)}." if false_positives else ""
    )

    audit_reveal = mo.vstack([
        mo.callout(
            mo.md(
                "**Audit reveal: how many rows each finding actually affects.** "
                "Compare against your picks above."
            ),
            kind="info",
        ),
        audit_df,
        mo.md(f"**Score:** {miss_note} {fp_note}"),
        mo.callout(mo.md(decoy_note), kind="neutral"),
    ])
    audit_reveal
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Step 3: cleanup rules and cohort assembly

        For each finding, you decide whether to filter the row out, transform it, or keep it. The seven cleanup decisions below are the ones the PI's cohort question forces you to make. Toggle them on and off and watch the cohort attrition.

        Order matters in attrition tables: the *step at which a patient drops* depends on which criterion catches them first. The order below is the conservative one (dedup and reconciliation first, plausibility second, clinical criteria last) so that each subsequent step does not waste work on rows that should already be gone.
        """
    )
    return


@app.cell
def _(mo):
    candidate_criteria = [
        ("Drop duplicate MRN partners (keep the canonical row)",
         "duplicate_mrn_partner == False"),
        ("Drop phantom (canceled) encounters",
         "phantom_encounter == False"),
        ("Drop implausible CRP values (>1000 mg/L)",
         "crp_value_mgL <= 1000"),
        ("Filter to seropositive RA diagnosis codes (M05.79 or M05.9)",
         "primary_dx_code in ['M05.79', 'M05.9']"),
        ("Require seropositive serology",
         "seropositive == True"),
        ("Reconcile TNFi currency (drop rows where the truth says stopped)",
         "tnfi_status_truth == 'active'"),
        ("Require at least one structured DAS28-CRP value",
         "das28_structured == das28_structured"),
    ]
    cohort_selector = mo.ui.multiselect(
        options=[c[0] for c in candidate_criteria],
        label="Toggle cleanup and inclusion criteria on and off",
    )
    return candidate_criteria, cohort_selector


@app.cell
def _(cohort_selector):
    cohort_selector
    return


@app.cell
def _(CohortBuilder, candidate_criteria, cohort_selector, extract, mo):
    chosen = cohort_selector.value or []
    expr_by_label = {label: expr for label, expr in candidate_criteria}

    cb = CohortBuilder(extract, patient_id_col="patient_id")
    for label in chosen:
        cb.add_criterion(expr_by_label[label], label)

    if not chosen:
        cohort_view = mo.callout(
            mo.md(
                "Toggle one or more criteria above to start building the cohort. "
                "Each toggle adds a step to the attrition table and recomputes the survivor count."
            ),
            kind="neutral",
        )
    else:
        cohort_view = cb.render()
    cohort_view
    return (cb,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### What the attrition shows

        Once you have all seven criteria turned on, three things should be visible:

        1. **The starting cohort is 600 patients.** Almost none of those are the patient the PI actually wants.
        2. **The biggest single drop is the RA-diagnosis filter.** Roughly a third of the extract is not RA at all. That is normal: the CDW pulled patients into the extract for join-related reasons that have nothing to do with the clinical question.
        3. **The DAS28 step is the second-biggest drop.** Forty percent of TNFi patients have no structured DAS28 value. The PI gets a much smaller cohort than expected. Whether to NLP the notes (course 10) to recover the rest is a real decision; it is a *more* complete cohort at the cost of analytical reliability.

        Each cleanup step you turned on is a decision with consequences. Document them.
        """
    )
    return


@app.cell
def _(cb, mo):
    final_summary = mo.md(
        f"""
        ### Final cohort summary

        After applying every cleanup step turned on above, you end with **{len(cb.surviving_patients()):,} patients**.

        That number is *not* the answer to "how many patients in our system have seropositive RA on a TNFi with a recent DAS28." It is the answer to "how many patients survived this specific cleanup pipeline." The two numbers are different. Course 13 of this curriculum is about documenting which is which so the analytical user can choose.
        """
    )
    final_summary
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Step 4: hand-off memo

        Write the one-paragraph summary the rheumatology research team will read. Two sentences on what the audit found. Two sentences on what cleanup you applied. One sentence on what the final cohort represents (and what it does not).
        """
    )
    return


@app.cell
def _(mo):
    memo_text = mo.ui.text_area(
        label="Hand-off memo (write the paragraph above the document the team will read):",
        rows=8,
        full_width=True,
        placeholder=(
            "Audit findings: ... \n"
            "Cleanup applied: ... \n"
            "What this cohort represents: ..."
        ),
    )
    memo_text
    return (memo_text,)


@app.cell
def _(cb, cohort_selector, memo_text, mo):
    chosen_steps = cohort_selector.value or []
    final_n = len(cb.surviving_patients())
    memo_value = (memo_text.value or "").strip()
    has_memo = len(memo_value) >= 50

    if not has_memo:
        body = "_Write at least a couple of sentences above to assemble the memo._"
    else:
        bullets = "\n".join(f"- {step}" for step in chosen_steps) or "- _(no cleanup applied)_"
        body = f"""
**TO:** Rheumatology research team
**RE:** Cohort extract for seropositive RA on TNFi with documented DAS28

**Findings and decisions:**

{memo_value}

**Cleanup steps applied (in order):**

{bullets}

**Final cohort:** {final_n:,} patients meeting the cleanup criteria above.

**Caveats:**

- This number reflects the cleanup pipeline applied here; it is not a definitive count of RA-TNFi-DAS28 patients in the system.
- Patients dropped at the DAS28 step may have DAS28 documented in clinical notes; NLP recovery would expand the cohort at the cost of analytical reliability.
- The TNFi-currency reconciliation depends on the truth column being trustworthy; in a real extract, currency would have to be validated against medication-administration records.

**Audit-trail metadata:**

- Extract size: 600 patients (synthetic).
- Cleanup steps: {len(chosen_steps)} of 7 available.
"""
    mo.callout(mo.md(body), kind="info" if has_memo else "neutral")
    return


@app.cell
def _(mo):
    reflection = mo.ui.text_area(
        label=(
            "**Reflection.** This capstone asked you to do the unglamorous middle layer of clinical informatics: "
            "audit, clean, document. Write a paragraph about which decision in the pipeline you were least sure of, "
            "and what additional information would have made you more confident."
        ),
        rows=5,
        full_width=True,
        placeholder="No reveal on this one. The reflection is the work.",
    )
    mo.vstack([
        reflection,
        mo.callout(
            mo.md(
                "_The right answer to this reflection is usually about the DAS28 step. Whether to drop the 40% of "
                "TNFi patients without structured DAS28, or to NLP-recover them, is a real research-design decision "
                "with no automatic answer._"
            ),
            kind="neutral",
        ),
    ])
    return


if __name__ == "__main__":
    app.run()
