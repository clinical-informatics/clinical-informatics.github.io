"""Track 01: Why privacy matters in health data.

"It's anonymized" is the most over-claimed sentence in clinical
informatics. This notebook walks the threat model, the three famous
re-identifications (Weld 1997, Netflix 2008, AOL 2006), and the
distinction between de-identification and anonymization. The interactive
piece is a k-anonymity simulator on a synthetic 5,000-patient registry:
pick which fields to include in a "de-identified" release, watch how
many patients become uniquely identifiable.
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

    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd

    rng = np.random.default_rng(20260517)
    return alt, mo, np, pd, rng


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 01: Why privacy matters in health data

        ## "It's anonymized" is the most over-claimed sentence in clinical informatics

        A clinician's intuition for privacy is shaped by the bedside: don't discuss the patient in the elevator, log out of the chart, close the curtain. The intuition is right. The mechanism is different at scale.

        When clinical data leaves the bedside (an extract for a researcher, a public-use file, a dataset for a vendor), the privacy question becomes "who can re-identify these rows?" Re-identification means taking a dataset stripped of obvious identifiers and recovering the link from rows back to specific individuals. It is concrete; it has happened; the literature is well-documented.

        Four ideas in this track:

        1. **The threat model.** Who would re-identify, why, and what would they gain.
        2. **The three famous re-identifications.** Each shows a different way "anonymized" data isn't.
        3. **De-identification vs anonymization.** Not the same thing. The distinction is load-bearing.
        4. **The quasi-identifier problem.** ZIP + sex + DOB is identifying 87% of the time. The defense isn't to drop them; the defense is to know the combinatorics.

        Then a synthetic registry of 5,000 patients with a k-anonymity slider.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1. The threat model

        Privacy is not a sentiment; it is a set of trade-offs against named threats. Three questions get you most of the way:

        | Question | What the answer looks like in documented re-identification cases |
        |---|---|
        | **Who is the attacker?** | A journalist looking for a public figure. A researcher demonstrating vulnerability. A government doing surveillance. An employer checking on staff. A commercial entity cross-referencing data-broker tables. The attacker has a side table you didn't know existed. |
        | **Why would they bother?** | Curiosity, demonstration, commercial linkage to a marketing profile, litigation, harm (outing, blackmail, denial of insurance). Most documented attacks were demonstrations by researchers; the rest cover the other categories. |
        | **What would re-identification let them do?** | Connect the dataset's medical content (diagnoses, prescriptions, dates) to a named person. That link is leverage: reputational, financial, legal. |

        The point of writing the threat model down: the right defense scales with the right threat. Locking down a public-use file the way you would lock down a research analyst's workstation is wasted effort. Treating a public release as "low-stakes because the names are gone" is a documented failure mode.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2. Three famous re-identifications

        Each one shows a different way "anonymized" data isn't. Read these once and keep them.

        ### Governor Weld's medical records (Sweeney, 1997)

        The Massachusetts Group Insurance Commission released "anonymized" hospital discharge records. Names and SSNs were removed. ZIP code, date of birth, and sex remained.

        Latanya Sweeney, then a graduate student, paid twenty dollars for the Cambridge voter registration list. The Governor of Massachusetts, William Weld, lived in Cambridge. His ZIP code, DOB, and sex appeared in both files. **She mailed his medical record to his office.**

        **The lesson.** The "obvious" identifiers were removed, the data was called anonymized, and a single match against a publicly purchasable side table re-identified a specific individual. ZIP + DOB + sex are **quasi-identifiers**: not identifying alone, near-unique in combination. Sweeney's 2000 paper later quantified this: **87% of the US population is uniquely identifiable by those three fields**.

        ### The Netflix Prize dataset (Narayanan and Shmatikov, 2008)

        In 2006, Netflix released 100 million movie ratings from 500,000 subscribers, with subscriber names replaced by random IDs. The dataset was the basis of a public competition. Two years later, Narayanan and Shmatikov at the University of Texas showed that with as few as **eight movie ratings** (some of which could be slightly wrong, dates off by up to two weeks), they could uniquely identify a Netflix subscriber **99% of the time**. They used the publicly available Internet Movie Database (IMDb) as the side table; some users had posted their reviews there.

        **The lesson.** **Sparse high-dimensional data is itself an identifier**, even when no traditional identifier is present. A patient's longitudinal trajectory (a sequence of diagnoses, procedures, lab values, prescriptions) plays the same role as a sequence of obscure movie ratings. Patients with rare conditions or unusual courses are systematically more identifiable than patients with common conditions.

        ### The AOL search query release (2006)

        AOL released 20 million search queries from 657,000 users, with usernames replaced by integer IDs. Journalists at the New York Times re-identified User 4417749 within days by reading her queries, which included her last initial, her hometown, and the names of people she had searched for. They visited her at home; she confirmed. AOL pulled the dataset four days after release; copies still circulate.

        **The lesson.** Even when the dataset is just text and contains no demographics, **the content people produce is identifying**. The clinical analog is free-text clinical notes (Track 10 of this curriculum), which routinely contain enough biographical detail to identify the subject independent of any structured field.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3. De-identification vs anonymization

        These two words are used interchangeably in conversation. They are different in law and different in technical guarantee. The distinction is the most important vocabulary fix in this track.

        | Property | De-identification (HIPAA Safe Harbor) | Anonymization (statistical) |
        |---|---|---|
        | **What it removes** | The 18 HIPAA-named identifiers (names, addresses, SSN, MRN, account numbers, full dates, ZIP > 3 digits, ages > 89, photos, biometrics, IP, URL, etc.) | Whatever is required for re-identification to be statistically infeasible |
        | **What it leaves** | Year of service, 3-digit ZIP, sex, race, ethnicity, diagnoses, procedures, the rest of the clinical content | Often: only summary statistics, or perturbed values, or differentially-private outputs |
        | **What it guarantees** | Legal permission to share under HIPAA, with a DUA | Re-identification is mathematically hard regardless of side tables |
        | **What it doesn't guarantee** | That the data is statistically un-re-identifiable | (no legal status by itself) |
        | **Real-world status** | Almost every "anonymized" clinical dataset in circulation is actually de-identified | Most clinical datasets are not anonymized in this sense |

        The takeaway: **de-identified is legally shareable; anonymized is statistically protected.** Many privacy-promising releases are the first thing called the second. This is sometimes fine (the residual re-identification risk is acceptable for the use case), but it is never fine *without naming it*. Saying "the dataset is anonymized" when you mean "the dataset meets HIPAA Safe Harbor" is the over-claim that gets institutions into the newspaper.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 4. The k-anonymity simulator

        A synthetic registry of 5,000 patients with realistic clinical and demographic structure. Pick the fields you'd include in a "de-identified" release. The notebook computes:

        - **k-anonymity**, the smallest group of patients sharing the same combination of selected fields. A k=1 patient is uniquely identifiable; a k=5 patient is one of five candidates; etc.
        - **The fraction of patients with k=1**, which is the share of the dataset that's uniquely identifiable on the selected fields alone.

        The interpretation is simple: the lower the k for any patient, the easier it is for an attacker with a side table to nail them.
        """
    )
    return


@app.cell
def _(np, pd, rng):
    n = 5000
    # Realistic age distribution skewed toward older adults
    ages = rng.normal(58, 15, size=n).clip(18, 95).astype(int)
    # Sex (assigned at birth)
    sex = rng.choice(["female", "male"], size=n, p=[0.62, 0.38])
    # Race/ethnicity
    race = rng.choice(
        ["White", "Black", "Asian", "Other", "Unknown"],
        size=n,
        p=[0.62, 0.16, 0.08, 0.10, 0.04],
    )
    # 3-digit ZIP code (Massachusetts-ish for flavor)
    zip3 = rng.choice(["021", "022", "023", "024", "025", "026", "027"], size=n)
    # Birth year derived from age
    birth_year = 2026 - ages
    # Birth month (uniform)
    birth_month = rng.integers(1, 13, size=n)
    # Encounter year of recent visit
    encounter_year = rng.choice([2023, 2024, 2025, 2026], size=n)
    # Diagnosis: a mix of common and rare conditions
    dx = rng.choice(
        [
            "Hypertension", "Diabetes type 2", "Hyperlipidemia",
            "Rheumatoid arthritis", "Lupus", "Castleman disease",
            "ANCA vasculitis", "Sarcoidosis", "Heart failure",
            "Asthma", "COPD", "CKD stage 3",
        ],
        size=n,
        p=[0.17, 0.16, 0.14, 0.06, 0.03, 0.005, 0.015, 0.02, 0.10, 0.10, 0.08, 0.12],
    )

    cohort = pd.DataFrame(
        {
            "patient_id": [f"P-{i:05d}" for i in range(n)],
            "age": ages,
            "sex": sex,
            "race": race,
            "zip3": zip3,
            "birth_year": birth_year,
            "birth_month": birth_month,
            "encounter_year": encounter_year,
            "diagnosis": dx,
        }
    )
    return (cohort,)


@app.cell
def _(mo):
    field_choices = mo.ui.multiselect(
        options=[
            "sex",
            "age (exact)",
            "race",
            "zip3 (first 3 digits of ZIP)",
            "birth_year",
            "birth_month",
            "encounter_year",
            "diagnosis (some rare; some common)",
        ],
        value=["sex", "zip3 (first 3 digits of ZIP)"],
        label="Pick which quasi-identifier fields to include in the released dataset",
    )
    field_choices
    return (field_choices,)

@app.cell
def _(alt, cohort, field_choices, mo, pd):
    field_map = {
        "sex": "sex",
        "age (exact)": "age",
        "race": "race",
        "zip3 (first 3 digits of ZIP)": "zip3",
        "birth_year": "birth_year",
        "birth_month": "birth_month",
        "encounter_year": "encounter_year",
        "diagnosis (some rare; some common)": "diagnosis",
    }
    cols = [field_map[v] for v in field_choices.value]

    if len(cols) == 0:
        results = mo.callout(
            mo.md("_Select at least one field above to compute k-anonymity._"),
            kind="neutral",
        )
    else:
        grouped = cohort.groupby(cols).size().reset_index(name="k")
        merged = cohort.merge(grouped, on=cols, how="left")
        k_per_patient = merged["k"].values

        pct_k1 = float((k_per_patient == 1).mean()) * 100
        pct_k_le_5 = float((k_per_patient <= 5).mean()) * 100
        pct_k_le_10 = float((k_per_patient <= 10).mean()) * 100
        median_k = int(pd.Series(k_per_patient).median())
        n_groups = len(grouped)

        bins = pd.cut(
            k_per_patient,
            bins=[0, 1, 2, 5, 10, 50, 100, 10_000],
            labels=[
                "k = 1 (unique)",
                "k = 2",
                "k = 3-5",
                "k = 6-10",
                "k = 11-50",
                "k = 51-100",
                "k > 100",
            ],
            include_lowest=True,
        )
        hist = (
            pd.Series(bins, name="k_bin").value_counts().reset_index()
        )
        hist.columns = ["k_bin", "count"]
        order = [
            "k = 1 (unique)", "k = 2", "k = 3-5", "k = 6-10",
            "k = 11-50", "k = 51-100", "k > 100",
        ]
        hist["k_bin"] = pd.Categorical(hist["k_bin"], categories=order, ordered=True)
        hist = hist.sort_values("k_bin")

        chart = (
            alt.Chart(hist)
            .mark_bar()
            .encode(
                x=alt.X("k_bin:N", title="Anonymity group size (k)", sort=order),
                y=alt.Y("count:Q", title="Patients in the released dataset"),
                color=alt.condition(
                    alt.datum.k_bin == "k = 1 (unique)",
                    alt.value("#D1495B"),
                    alt.value("#2E86AB"),
                ),
            )
            .properties(width=560, height=320, title="Distribution of anonymity-group sizes")
        )

        summary_md = mo.md(
            f"""
            **Fields released:** `{', '.join(cols)}` (across 5,000 synthetic patients).

            - **Uniquely identifiable patients (k=1):** {pct_k1:.1f}%
            - **Identifiable to 5 or fewer candidates (k≤5):** {pct_k_le_5:.1f}%
            - **Identifiable to 10 or fewer candidates (k≤10):** {pct_k_le_10:.1f}%
            - **Median anonymity group size (median k):** {median_k}
            - **Distinct quasi-identifier combinations in the release:** {n_groups:,}

            Red bar in the chart below is the fraction of the cohort that is **uniquely identifiable** on the selected fields alone, before any side table is brought to bear. Any side table the attacker has access to (voter rolls, social media, a data broker's table) can only narrow further.
            """
        )

        if pct_k1 > 50:
            verdict = mo.callout(
                mo.md(
                    "**Most of the cohort is uniquely identifiable.** This combination would not pass any reasonable privacy review. An attacker with a side table linking *any* of these fields to patient identity could re-identify most rows. Generalize (3-digit ZIP, year not month, decade not exact age), suppress the rare diagnoses, or aggregate before releasing."
                ),
                kind="warn",
            )
        elif pct_k1 > 5:
            verdict = mo.callout(
                mo.md(
                    "**A meaningful slice of the cohort is uniquely identifiable.** The release would likely require an Expert Determination (Track 02) plus a Data Use Agreement. Patients with rare diagnoses are the most exposed; consider suppressing those rows or aggregating the diagnosis column."
                ),
                kind="warn",
            )
        elif pct_k1 > 0:
            verdict = mo.callout(
                mo.md(
                    "**A small slice is uniquely identifiable.** Look at which rows have k=1 (usually the rare-diagnosis or extreme-age rows). Suppress those individually or apply local generalization. The remainder is reasonably protected against the threat model in Section 1."
                ),
                kind="info",
            )
        else:
            verdict = mo.callout(
                mo.md(
                    "**No row is uniquely identifiable on the released fields alone.** This is necessary but not sufficient for anonymization: an attacker with the right side table can still link, and k-anonymity does not protect against the l-diversity attack (homogeneous sensitive values within a group). Sufficient for a HIPAA-compliant Limited Data Set when paired with a DUA."
                ),
                kind="success",
            )

        results = mo.vstack([summary_md, chart, verdict])

    results
    return (results,)


@app.cell
def _(mo):
    mo.md(
        r"""
        **What to try.** Run these scenarios in the picker above:

        1. **Just sex.** k=1 should be 0% (with 5,000 patients and binary sex, every patient shares the field with ~half the cohort).
        2. **Sex + zip3.** Still safe; only seven 3-digit ZIPs, sex is binary, ~350 patients per cell.
        3. **Sex + zip3 + birth_year.** Now you're starting to slice the cohort into ~14 (ZIPs) × ~70 (years) × 2 = 2,000 cells across 5,000 patients. Some cells are tiny.
        4. **Sex + zip3 + birth_year + birth_month.** You've crossed into "most patients are uniquely identifiable" territory. This is roughly the Sweeney trio rebuilt.
        5. **Sex + zip3 + diagnosis.** Pay attention to the rare diagnoses (Castleman disease, ANCA vasculitis). A 28-year-old woman in ZIP 023 with Castleman is uniquely identifiable on three fields alone.

        The pattern that should land: **k-anonymity drops fast as you add fields**. The interaction is multiplicative, not additive. The defense is to generalize (year not month, decade not year, 3-digit not 5-digit ZIP) or to suppress (drop the rows whose quasi-identifiers are too unique).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 5. What this leaves you

        Four things in place:

        1. **A threat model.** Privacy is trade-offs against named attackers, not a vague feeling. Write the model down.
        2. **Three documented re-identification cases.** Each maps to a different attack type: quasi-identifier joining (Weld), sparse high-dimensional matching (Netflix), free-text content (AOL). Clinical data is exposed to all three.
        3. **A vocabulary fix.** De-identification (HIPAA Safe Harbor) is legal permission; anonymization is statistical guarantee. Most "anonymized" clinical data is actually de-identified. Knowing the difference is the most useful single skill in this track.
        4. **The quasi-identifier instinct.** ZIP + sex + DOB is identifying for 87% of US adults. Add encounter date and a diagnosis, and you've often crossed into uniqueness on a small cohort. The defense is generalization and suppression, applied on purpose, with a documented residual risk.

        Track 02 covers the legal floor: what HIPAA actually requires (and the corners it leaves uncovered). Track 03 then takes the ethical question of secondary use. Track 04 connects the privacy work to the algorithmic-fairness work (the two overlap more than they usually get credit for). Track 05 closes with governance: which humans should be in the room when these trade-offs get made.
        """
    )
    return


if __name__ == "__main__":
    app.run()
