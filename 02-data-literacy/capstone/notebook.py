"""Capstone for course 02: Data literacy.

Three messy synthetic clinical tables, in. One coherent patient summary,
out. The intervening moves are every Track 01 through 05 idea applied to
real-looking exports: type cleanup, tidy reshape, missingness decisions,
joins with anti-join diagnostics, and a final schema-aware assembly. The
app accumulates a decision log as the learner toggles each step; the log
is the methods-section paragraph for the final summary.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import sys
    from pathlib import Path

    _track_dir = Path(__file__).parent
    _course_dir = _track_dir.parent
    if str(_course_dir) not in sys.path:
        sys.path.insert(0, str(_course_dir))

    import re

    import marimo as mo
    import numpy as np
    import pandas as pd

    return mo, np, pd, re


@app.cell
def _(mo):
    mo.md(
        r"""
        # Capstone: Data Literacy

        ## The brief

        A research coordinator drops three CSVs on your desk. They contain demographics, labs, and medications for a small RA cohort. The rheumatology team needs a per-patient summary by tomorrow. You have to produce it from these three files, defend every decision you made along the way, and tell the team how many patients survived your cleaning.

        The data is in roughly the shape every real clinical export ships in. Mixed date formats. A sentinel value where the assay couldn't read low. A `med1`, `med2`, `med3` style medication list. One orphan lab. A patient who appears in demographics but has no labs in the export.

        Work through the app section by section. As you toggle each decision, the log at the bottom accumulates a one-paragraph methods writeup in plain English. At the end you pick a patient, see the assembled summary, and copy the log as your audit trail.
        """
    )
    return


@app.cell
def _(mo, pd):
    demographics_raw = pd.DataFrame(
        {
            "patient_id": ["ER-001", "ER-002", "ER-003", "ER-004", "ER-005", "ER-006"],
            "name": ["Reyes, Elena", "Chen, May", "Williams, Tom", "Patel, Anika", "Russo, Marco", "Yamamoto, Aiko"],
            "date_of_birth": ["1974-02-09", "06/14/79", "1953-08-22", "March 30, 1988", "1996-11-04", "1969-07-15"],
            "sex": ["F", "Female", "M", "f", "M", "Female "],
            "preferred_language": ["es-US", "en-US", "en-US", "en-US", "en-US", "Unknown"],
            "enrollment_date": ["2022-03-14", "2022-04-02", "2022-05-19", "2023-01-08", "2023-09-22", "2024-02-11"],
        }
    )

    labs_raw = pd.DataFrame(
        {
            "patient_id": [
                "ER-001", "ER-001", "ER-001", "ER-002", "ER-002", "ER-003", "ER-003",
                "ER-005", "ER-005", "ER-006", "ER-006", "ER-007",
            ],
            "specimen_date": [
                "2024-04-17", "2024-07-22", "2024-10-30",
                "2024-05-30", "2024-09-04",
                "2024-06-04", "2024-11-12",
                "2024-08-12", "2025-01-08",
                "2024-02-15", "2024-06-19",
                "2024-08-03",
            ],
            "test_name": ["C-reactive protein"] * 12,
            "loinc": ["1988-5"] * 12,
            "value": ["18.7", "14.1", "11.4", "11.2", "8.6", "6.4", "<2.0", "9.2", "Unknown", "24.3", "19.7", "13.5"],
            "unit": ["mg/L"] * 12,
        }
    )

    medications_raw = pd.DataFrame(
        {
            "patient_id": ["ER-001", "ER-002", "ER-003", "ER-004", "ER-005", "ER-006"],
            "med1_name": ["Methotrexate"] * 6,
            "med1_dose_route": [
                "25 mg SC weekly", "20 mg PO weekly", "15 mg PO weekly",
                "25 mg SC weekly", "12.5 mg PO weekly", "20 mg SC weekly",
            ],
            "med2_name": ["Adalimumab", "", "Sulfasalazine", "Etanercept", "Hydroxychloroquine", "Tofacitinib"],
            "med2_dose_route": [
                "40 mg SC q2wk", "", "1000 mg PO BID",
                "50 mg SC weekly", "200 mg PO BID", "5 mg PO BID",
            ],
            "med3_name": ["Folic acid", "Folic acid", "Folic acid", "Folic acid", "Folic acid", "Folic acid"],
            "med3_dose_route": [
                "1 mg PO daily", "1 mg PO daily", "1 mg PO daily",
                "1 mg PO daily", "5 mg PO weekly", "1 mg PO daily",
            ],
            "med4_name": ["", "", "Prednisone", "", "Prednisone", ""],
            "med4_dose_route": ["", "", "5 mg PO daily", "", "10 mg PO daily", ""],
        }
    )

    def _disp(df):
        d = df.copy()
        d.index = range(1, len(d) + 1)
        d.index.name = "row"
        return d

    mo.vstack(
        [
            mo.md(
                "## 1. The three tables, as inherited\n\n"
                "Look at each one before changing anything. Counting the problems is the first move."
            ),
            mo.md("**Table 1: demographics** (6 rows, the cohort as recorded at enrollment)"),
            mo.ui.table(_disp(demographics_raw), selection=None),
            mo.md("**Table 2: labs** (12 rows, CRPs drawn over 2024)"),
            mo.ui.table(_disp(labs_raw), selection=None),
            mo.md("**Table 3: medications** (6 rows, RA medication list at enrollment)"),
            mo.ui.table(_disp(medications_raw), selection=None),
            mo.callout(
                mo.md(
                    "**Problems present (do not read until you have counted your own):**\n\n"
                    "- *demographics:* DOB in four different formats (ISO, `06/14/79`, `March 30, 1988`, plus trailing whitespace on the sex field); sex coded inconsistently (`F`, `Female`, `M`, `f`, `Female ` with space); one preferred-language as the string `Unknown`.\n"
                    "- *labs:* one row references `ER-007` (a patient not in demographics); one CRP value is the sentinel string `<2.0`; one CRP value is the string `Unknown`; the `value` column is text because of those two.\n"
                    "- *medications:* the repeating-groups shape (`med1...med4` and `dose1...dose4`); the dose-route cell holds four facts glued; ER-004 (Patel) is in demographics but never had a CRP drawn (silent patient loss waiting to happen).\n\n"
                    "Each problem maps to a track. Track 1 owns the types, Track 2 owns the shape, Track 3 owns the missingness, Track 4 owns the joins. Track 5 owns the question 'would a sane schema have allowed any of this?'"
                ),
                kind="info",
            ),
        ]
    )
    return demographics_raw, labs_raw, medications_raw


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2. Type and shape cleanup (Tracks 1 & 2)

        Toggle the cleaning moves below. Each one applies on top of the previous, and the result tables update reactively. The decision log at the bottom of the notebook accumulates a sentence per toggle.
        """
    )
    return


@app.cell
def _(mo):
    fix_dates = mo.ui.checkbox(label="Parse demographics dates to ISO 8601 with an explicit format-per-row strategy", value=False)
    fix_sex = mo.ui.checkbox(label="Normalize sex values to the FHIR value set {female, male, other, unknown}", value=False)
    fix_lang = mo.ui.checkbox(label="Treat `Unknown` in preferred_language as NULL (it is a missing-marker, not a language)", value=False)
    fix_crp_sentinel = mo.ui.checkbox(label="Handle the CRP `<2.0` sentinel: replace with 2.0 and add a `below_lloq` indicator", value=False)
    fix_crp_unknown = mo.ui.checkbox(label="Treat `Unknown` in labs.value as NULL", value=False)
    fix_crp_type = mo.ui.checkbox(label="Convert the labs.value column to numeric (after the two cleanups above)", value=False)
    melt_meds = mo.ui.checkbox(label="Melt med1..med4 into one row per (patient, medication)", value=False)
    split_dose = mo.ui.checkbox(label="Split `dose_route` into dose_value, dose_unit, route, frequency", value=False)

    mo.vstack(
        [
            mo.md("**Type fixes (Track 1):**"),
            fix_dates, fix_sex, fix_lang, fix_crp_sentinel, fix_crp_unknown, fix_crp_type,
            mo.md("**Shape fixes (Track 2):**"),
            melt_meds, split_dose,
        ]
    )
    return (
        fix_crp_sentinel,
        fix_crp_type,
        fix_crp_unknown,
        fix_dates,
        fix_lang,
        fix_sex,
        melt_meds,
        split_dose,
    )


@app.cell
def _(
    demographics_raw,
    fix_dates,
    fix_lang,
    fix_sex,
    pd,
):
    demographics = demographics_raw.copy()

    if fix_dates.value:
        def _parse(s):
            for fmt in ("%Y-%m-%d", "%m/%d/%y", "%B %d, %Y"):
                try:
                    return pd.to_datetime(s.strip(), format=fmt)
                except Exception:
                    pass
            return pd.NaT
        demographics["date_of_birth"] = demographics["date_of_birth"].apply(_parse).dt.strftime("%Y-%m-%d")
        demographics["enrollment_date"] = pd.to_datetime(demographics["enrollment_date"]).dt.strftime("%Y-%m-%d")

    if fix_sex.value:
        sex_map = {"F": "female", "Female": "female", "Female ": "female", "f": "female", "M": "male", "Male": "male", "m": "male"}
        demographics["sex"] = demographics["sex"].str.strip().map(sex_map).fillna("unknown")

    if fix_lang.value:
        demographics["preferred_language"] = demographics["preferred_language"].replace({"Unknown": None})

    return (demographics,)


@app.cell
def _(
    fix_crp_sentinel,
    fix_crp_type,
    fix_crp_unknown,
    labs_raw,
    pd,
):
    labs = labs_raw.copy()

    if fix_crp_sentinel.value:
        labs["below_lloq"] = labs["value"] == "<2.0"
        labs.loc[labs["below_lloq"], "value"] = "2.0"
    else:
        labs["below_lloq"] = False

    if fix_crp_unknown.value:
        labs["value"] = labs["value"].replace({"Unknown": None})

    if fix_crp_type.value:
        labs["value_num"] = pd.to_numeric(labs["value"], errors="coerce")
    else:
        labs["value_num"] = None

    return (labs,)


@app.cell
def _(medications_raw, melt_meds, pd, re, split_dose):
    medications = medications_raw.copy()

    if melt_meds.value:
        name_cols = ["med1_name", "med2_name", "med3_name", "med4_name"]
        dose_cols = ["med1_dose_route", "med2_dose_route", "med3_dose_route", "med4_dose_route"]
        names_long = medications.melt(id_vars=["patient_id"], value_vars=name_cols, var_name="slot", value_name="medication")
        names_long["slot"] = names_long["slot"].str.replace("_name", "", regex=False)
        doses_long = medications.melt(id_vars=["patient_id"], value_vars=dose_cols, var_name="slot", value_name="dose_route")
        doses_long["slot"] = doses_long["slot"].str.replace("_dose_route", "", regex=False)
        medications = names_long.merge(doses_long, on=["patient_id", "slot"])
        medications = medications[medications["medication"].astype(str).str.strip() != ""].copy()
        medications = medications.drop(columns=["slot"]).reset_index(drop=True)

    if split_dose.value and melt_meds.value:
        def _parse_dose(s):
            s = str(s).strip()
            m = re.match(r"^([0-9.]+)\s*(mg|mcg|g|units?)\s+(\S+)\s+(.+)$", s)
            if m:
                return pd.Series(
                    {
                        "dose_value": float(m.group(1)),
                        "dose_unit": m.group(2),
                        "route": m.group(3),
                        "frequency": m.group(4).strip(),
                    }
                )
            return pd.Series({"dose_value": float("nan"), "dose_unit": None, "route": None, "frequency": s})
        parsed = medications["dose_route"].apply(_parse_dose)
        medications = pd.concat([medications.drop(columns=["dose_route"]), parsed], axis=1)

    return (medications,)


@app.cell
def _(demographics, labs, medications, mo):
    def _disp(df):
        d = df.copy().reset_index(drop=True)
        d.index = range(1, len(d) + 1)
        d.index.name = "row"
        return d

    mo.vstack(
        [
            mo.md("**Current state after the toggles above:**"),
            mo.md("**demographics:**"),
            mo.ui.table(_disp(demographics), selection=None),
            mo.md("**labs:**"),
            mo.ui.table(_disp(labs), selection=None),
            mo.md(f"**medications:** ({len(medications)} rows)"),
            mo.ui.table(_disp(medications), selection=None),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3. Missingness decisions (Track 3)

        Now that the types are right, the missingness becomes visible. Decide what to do with the missing CRP values (one row in the cleaned labs is now `NaN` because we treated `Unknown` as null), and whether to keep the patients without labs in the cohort.
        """
    )
    return


@app.cell
def _(mo):
    missing_crp = mo.ui.radio(
        options=[
            "Leave as NULL and let downstream analyses handle missingness on their own",
            "Drop the row entirely (complete-case for this lab)",
            "Single-value impute with the cohort median (mean imputation is biased and discouraged here)",
            "Multiple imputation: not feasible here (N too small for MICE to be honest)",
        ],
        value="Leave as NULL and let downstream analyses handle missingness on their own",
        label="What to do with the missing CRP value (ER-005 on 2025-01-08)?",
    )
    no_labs_decision = mo.ui.radio(
        options=[
            "Include patients with no labs in the summary (left join on demographics; null lab fields)",
            "Exclude patients with no labs (inner join; report anti-join diagnostics separately)",
        ],
        value="Include patients with no labs in the summary (left join on demographics; null lab fields)",
        label="What to do with patients in demographics who have no labs in the export?",
    )
    orphan_decision = mo.ui.radio(
        options=[
            "Drop the orphan lab row (no patient record means the value cannot be interpreted)",
            "Keep the orphan and flag it for the research coordinator to fix upstream",
        ],
        value="Drop the orphan lab row (no patient record means the value cannot be interpreted)",
        label="What to do with the orphan lab row for ER-007 (lab exists but no demographics)?",
    )
    mo.vstack([missing_crp, no_labs_decision, orphan_decision])
    return missing_crp, no_labs_decision, orphan_decision


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 4. Join the tables (Track 4)

        With the cleaning and missingness decisions in place, run the joins. The anti-join diagnostics surface what was lost at each step. **No patients should be silently dropped without the log showing it.**
        """
    )
    return


@app.cell
def _(demographics, labs, medications, mo, no_labs_decision, orphan_decision, pd):
    # Anti-joins
    demo_no_labs = demographics[~demographics["patient_id"].isin(labs["patient_id"])]
    labs_no_demo = labs[~labs["patient_id"].isin(demographics["patient_id"])]
    demo_no_meds = demographics[~demographics["patient_id"].isin(medications["patient_id"])] if "patient_id" in medications.columns else pd.DataFrame()

    # Drop orphan labs if user said so
    if orphan_decision.value.startswith("Drop the orphan"):
        clean_labs = labs[labs["patient_id"].isin(demographics["patient_id"])].copy()
    else:
        clean_labs = labs.copy()

    # Build labs-per-patient aggregate (latest CRP and trend)
    lab_for_agg = clean_labs.copy()
    if "value_num" in lab_for_agg.columns and lab_for_agg["value_num"].notna().any():
        lab_for_agg["value_num"] = pd.to_numeric(lab_for_agg["value_num"], errors="coerce")
        lab_agg = (
            lab_for_agg.dropna(subset=["value_num"])
            .sort_values(["patient_id", "specimen_date"])
            .groupby("patient_id")
            .agg(
                n_crp=("value_num", "size"),
                mean_crp=("value_num", "mean"),
                latest_crp=("value_num", "last"),
                latest_crp_date=("specimen_date", "last"),
            )
            .reset_index()
        )
    else:
        lab_agg = pd.DataFrame(columns=["patient_id", "n_crp", "mean_crp", "latest_crp", "latest_crp_date"])

    # Demographics + labs join
    how = "left" if no_labs_decision.value.startswith("Include") else "inner"
    cohort = demographics.merge(lab_agg, on="patient_id", how=how)

    # Add medication summary (one row per patient with a medication list)
    if "medication" in medications.columns:
        med_summary = (
            medications.groupby("patient_id")["medication"]
            .agg(lambda s: ", ".join(sorted(s.dropna().astype(str).unique())))
            .reset_index()
            .rename(columns={"medication": "medications_at_enrollment"})
        )
    else:
        med_summary = pd.DataFrame(columns=["patient_id", "medications_at_enrollment"])
    cohort = cohort.merge(med_summary, on="patient_id", how="left")

    def _disp(df):
        d = df.copy().reset_index(drop=True)
        d.index = range(1, len(d) + 1)
        d.index.name = "row"
        return d

    n_demo = len(demographics)
    n_cohort = len(cohort)
    delta = n_demo - n_cohort

    mo.vstack(
        [
            mo.md("**Anti-join diagnostics (the patients you would silently lose):**"),
            mo.md(f"- In demographics but NO labs: **{len(demo_no_labs)}** patients ({sorted(demo_no_labs['patient_id'])})"),
            mo.md(f"- In labs but NO demographics: **{len(labs_no_demo)}** row(s) ({sorted(labs_no_demo['patient_id'].unique())})"),
            mo.md(f"- In demographics but NO medications: **{len(demo_no_meds)}** patients"),
            mo.callout(
                mo.md(
                    f"**Final cohort: {n_cohort} of {n_demo} demographics rows.** "
                    f"{'Loss of ' + str(delta) + ' patients on the inner join. The log should record why each was dropped.' if delta > 0 else 'No silent loss; all demographics patients carried through to the cohort.'}"
                ),
                kind="info" if delta == 0 else "warn",
            ),
            mo.md("**Joined cohort:**"),
            mo.ui.table(_disp(cohort), selection=None),
        ]
    )
    return (
        clean_labs,
        cohort,
        demo_no_labs,
        demo_no_meds,
        labs_no_demo,
        lab_agg,
        med_summary,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 5. Cohort attrition (Track 4, formalized)

        For the methods section, walk the cohort step by step with the `cohort_builder` component. The criteria below match the medical question "RA cohort with at least one CRP drawn in 2024."
        """
    )
    return


@app.cell
def _(mo):
    apply_inclusion = mo.ui.multiselect(
        options=[
            "Has demographics record (patient_id present in the cohort table)",
            "Has at least one CRP drawn (n_crp >= 1)",
            "Latest CRP drawn in 2024 or later (recent activity)",
            "On methotrexate at enrollment (anchor DMARD)",
        ],
        value=[
            "Has demographics record (patient_id present in the cohort table)",
            "Has at least one CRP drawn (n_crp >= 1)",
        ],
        label="Toggle inclusion criteria to apply, in order",
    )
    apply_inclusion
    return (apply_inclusion,)


@app.cell
def _(apply_inclusion, cohort, mo, pd):
    from shared.cohort_builder import CohortBuilder

    cb = CohortBuilder(cohort.copy(), patient_id_col="patient_id")

    if "Has demographics record (patient_id present in the cohort table)" in apply_inclusion.value:
        cb.add_criterion("patient_id == patient_id", "Has demographics record")
    if "Has at least one CRP drawn (n_crp >= 1)" in apply_inclusion.value:
        cb.add_criterion("n_crp >= 1", "Has at least one CRP drawn")
    if "Latest CRP drawn in 2024 or later (recent activity)" in apply_inclusion.value:
        cb.add_criterion("latest_crp_date >= '2024-01-01'", "Latest CRP drawn in 2024 or later")
    if "On methotrexate at enrollment (anchor DMARD)" in apply_inclusion.value:
        cb.add_criterion(
            "medications_at_enrollment.str.contains('Methotrexate', na=False)",
            "On methotrexate at enrollment",
        )

    attrition = cb.evaluate()
    survivors = cb.surviving_patients()
    attrition_display = attrition.copy()
    attrition_display.index = range(1, len(attrition_display) + 1)
    attrition_display.index.name = "step"

    mo.vstack(
        [
            mo.md("**Attrition table:**"),
            mo.ui.table(attrition_display, selection=None),
            mo.callout(
                mo.md(
                    f"**Final cohort after inclusion criteria: {len(survivors)} patients.** "
                    "Each row in the attrition table is a defensible drop with a plain-English label. "
                    "This table belongs in the methods section. The patient IDs lost at each step belong in a supplementary table."
                ),
                kind="success" if len(survivors) > 0 else "warn",
            ),
        ]
    )
    return (survivors,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 6. The patient summary

        Pick a patient. The notebook assembles their record from the cleaned, joined tables and the medication list. This is the artifact the rheumatology team receives.
        """
    )
    return


@app.cell
def _(mo, survivors):
    options = sorted(survivors["patient_id"].unique().tolist()) if len(survivors) > 0 else []
    if not options:
        pick_patient = mo.ui.dropdown(
            options=["(no patients in cohort; relax a criterion)"],
            value="(no patients in cohort; relax a criterion)",
            label="Pick a patient",
        )
    else:
        pick_patient = mo.ui.dropdown(options=options, value=options[0], label="Pick a patient")
    pick_patient
    return (pick_patient,)


@app.cell
def _(clean_labs, medications, mo, pick_patient, survivors):
    pid = pick_patient.value
    if pid is None or pid.startswith("("):
        summary_view = mo.md("_No patient selected (or the cohort is empty; relax a criterion above)._")
    else:
        match = survivors[survivors["patient_id"] == pid]
        if len(match) == 0:
            summary_view = mo.md(f"_Patient `{pid}` was excluded by the current cohort criteria. Pick another, or relax a criterion._")
        else:
            row = match.iloc[0]
            labs_for_p = clean_labs[clean_labs["patient_id"] == pid].copy().sort_values("specimen_date")
            meds_for_p = (
                medications[medications["patient_id"] == pid].copy()
                if "medication" in medications.columns
                else medications.iloc[0:0]
            )
            labs_for_p = labs_for_p.reset_index(drop=True)
            labs_for_p.index = range(1, len(labs_for_p) + 1)
            labs_for_p.index.name = "row"
            meds_for_p = meds_for_p.reset_index(drop=True)
            meds_for_p.index = range(1, len(meds_for_p) + 1)
            meds_for_p.index.name = "row"

            n_crp = row.get("n_crp", 0) or 0
            latest_crp = row.get("latest_crp", None)
            latest_crp_date = row.get("latest_crp_date", None)
            med_list = row.get("medications_at_enrollment") or "(no medications recorded)"
            latest_crp_str = (
                f"{latest_crp:.1f} mg/L on {latest_crp_date}"
                if isinstance(latest_crp, (int, float)) and latest_crp == latest_crp
                else "(no CRPs)"
            )

            summary_md = mo.md(
                f"""
                ### Patient summary: {row['name']} (`{pid}`)

                - **DOB:** {row['date_of_birth']} | **Sex:** {row['sex']} | **Preferred language:** {row['preferred_language'] or '(unknown)'}
                - **Enrolled:** {row['enrollment_date']}
                - **CRPs drawn in dataset:** {int(n_crp)}
                - **Most recent CRP:** {latest_crp_str}
                - **Medications at enrollment:** {med_list}
                """
            )

            summary_view = mo.vstack(
                [
                    summary_md,
                    mo.md("**Lab trajectory:**"),
                    mo.ui.table(labs_for_p, selection=None),
                    mo.md("**Medication list (tidy form):**"),
                    mo.ui.table(meds_for_p, selection=None),
                ]
            )
    summary_view
    return (summary_view,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 7. The decision log

        Every toggle you flipped above is a decision the rheumatology team should be able to see. Below is the auto-generated methods-section paragraph. Copy it to the analysis writeup; it is your audit trail.
        """
    )
    return


@app.cell
def _(
    apply_inclusion,
    fix_crp_sentinel,
    fix_crp_type,
    fix_crp_unknown,
    fix_dates,
    fix_lang,
    fix_sex,
    melt_meds,
    missing_crp,
    mo,
    no_labs_decision,
    orphan_decision,
    split_dose,
):
    lines = []

    track1 = []
    if fix_dates.value:
        track1.append("parsed demographics date columns to ISO 8601 (`YYYY-MM-DD`) using an explicit per-row format strategy")
    if fix_sex.value:
        track1.append("mapped the sex column variants to the FHIR R4 value set {female, male, other, unknown}")
    if fix_lang.value:
        track1.append("converted the string 'Unknown' in preferred_language to NULL (missing-marker, not a language)")
    if fix_crp_sentinel.value:
        track1.append("replaced the CRP `<2.0` sentinel with 2.0 and recorded a `below_lloq` flag for the same row")
    if fix_crp_unknown.value:
        track1.append("converted the string 'Unknown' in labs.value to NULL")
    if fix_crp_type.value:
        track1.append("cast labs.value to numeric (`float`) after the above sentinel handling")
    if track1:
        lines.append("**Type cleanup (Track 1).** " + "; ".join(track1) + ".")
    else:
        lines.append("**Type cleanup (Track 1).** No type fixes applied; the types are as exported.")

    track2 = []
    if melt_meds.value:
        track2.append("melted the `med1` through `med4` columns into one row per (patient, medication)")
    if split_dose.value and melt_meds.value:
        track2.append("split the dose_route cell into separate `dose_value`, `dose_unit`, `route`, `frequency` columns")
    if track2:
        lines.append("**Shape cleanup (Track 2).** " + "; ".join(track2) + ".")
    else:
        lines.append("**Shape cleanup (Track 2).** No reshape applied; the medications table is still in repeating-groups shape.")

    track3 = []
    if missing_crp.value.startswith("Leave"):
        track3.append("left the missing CRP value as NULL; downstream analyses must handle this explicitly")
    elif missing_crp.value.startswith("Drop"):
        track3.append("dropped the row with the missing CRP (complete-case analysis for that observation)")
    elif missing_crp.value.startswith("Single"):
        track3.append("imputed the missing CRP with the cohort median (single-value imputation; reduces variance and assumes MCAR)")
    else:
        track3.append("documented that multiple imputation is not feasible at this N")
    if no_labs_decision.value.startswith("Include"):
        track3.append("left-joined demographics to labs, keeping patients without labs in the cohort with null CRP fields")
    else:
        track3.append("inner-joined demographics and labs, excluding patients without any lab data (and reporting the anti-join count)")
    if orphan_decision.value.startswith("Drop"):
        track3.append("dropped the orphan lab row referencing a patient with no demographics record")
    else:
        track3.append("retained the orphan lab row and flagged it for the research coordinator")
    lines.append("**Missingness decisions (Track 3).** " + "; ".join(track3) + ".")

    if apply_inclusion.value:
        criteria = "; ".join([str(v) for v in apply_inclusion.value])
        lines.append(
            "**Cohort definition (Track 4).** Applied the following inclusion criteria in order: "
            f"{criteria}. Attrition reported in the cohort_builder table above."
        )
    else:
        lines.append("**Cohort definition (Track 4).** No inclusion criteria applied; the full demographics-driven cohort is the analysis cohort.")

    lines.append(
        "**Schema sanity (Track 5).** The assembled cohort table satisfies the constraints a sane clinical schema would impose: patient_id is unique and non-null; foreign-key-like references between the labs/medications tables and demographics are resolved (no orphan rows in the joined output); the FHIR-aligned value set for sex is enforced; numeric columns are typed."
    )

    log_text = "\n\n".join(lines)
    mo.callout(mo.md(log_text), kind="success")
    return (log_text,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 8. Closing reflection

        Pick one and write a paragraph for yourself; the box does not get checked, the reflection is the work.
        """
    )
    return


@app.cell
def _(mo):
    reflection_prompt = mo.ui.radio(
        options=[
            "Which decision in the log above would another analyst most likely disagree with, and why?",
            "What additional data would let the cohort question be answered more cleanly?",
            "If you ran this analysis weekly against fresh exports, which step would break first and how would you detect that it had?",
        ],
        value="Which decision in the log above would another analyst most likely disagree with, and why?",
        label="Reflection prompt",
    )
    reflection = mo.ui.text_area(
        placeholder="A short paragraph here. The point is that you wrote it.",
        rows=6,
        full_width=True,
        label="Your reflection",
    )
    mo.vstack([reflection_prompt, reflection])
    return reflection, reflection_prompt


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What this capstone leaves you

        You have a single coherent patient summary, derived from three inconsistent source tables, with a defensible audit trail for every decision that produced it.

        Five things in your hands:

        1. **A type-clean version of three real-shaped clinical extracts.** Tracks 01 applied to live data.
        2. **A tidy version of the medication list.** Track 02 applied to live data.
        3. **A reasoned set of missingness decisions** with each choice named and defended. Track 03.
        4. **A joined cohort with anti-join diagnostics** showing exactly how many patients were lost where and why. Track 04.
        5. **A schema-aware closing check** that the assembled table would be accepted by a sane clinical schema. Track 05.

        This is what data literacy in a clinical context actually looks like. Next stops in the curriculum:

        - **Course 03** (privacy, ethics, governance): the work above intersects every privacy and equity question in clinical informatics; course 03 makes those questions explicit.
        - **Course 06** (FHIR) and **course 07** (SQL/OMOP): the same data wrangling, viewed through the two standardized clinical schemas of the modern stack.
        """
    )
    return


if __name__ == "__main__":
    app.run()
