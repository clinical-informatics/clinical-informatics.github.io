"""Track 02: Cost and utilization measures.

Five terms cover most of the cost-and-utilization vocabulary: total cost
of care, per-member-per-month (PMPM), utilization rate, allowed amount,
patient-responsibility amount. The track defines each one against Ms.
Reyes's actual 2024 claims, computes her per-month utilization summary,
and addresses the three-way dollar split that appears on every claim line.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import sys
    import types
    from pathlib import Path

    import altair as alt
    import marimo as mo
    import pandas as pd

    _COURSE_TITLES = {
        "04": "Clinical epidemiology",
        "16": "Leadership and professional practice",
        "18": "Population and public health",
    }

    def _course_label(course_id):
        title = _COURSE_TITLES.get(course_id.split("-")[0])
        return f"Course {course_id}: {title}" if title else f"Course {course_id}"

    def _xref_callback(from_course, to_course, topic, body):
        return mo.callout(
            mo.md(f"**Callback to {_course_label(to_course)}.** {topic}\n\n{body}"),
            kind="neutral",
        )

    def _xref_forward(from_course, to_course, topic, body):
        return mo.callout(
            mo.md(f"**Forward to {_course_label(to_course)}.** {topic}\n\n{body}"),
            kind="neutral",
        )

    xref = types.SimpleNamespace(callback=_xref_callback, forward=_xref_forward)

    _WASM_DATA_BASE = "/11-health-economics-data/track-02-cost-utilization/app"

    def load_cached_csv(filename):
        if "pyodide" in sys.modules:
            from pyodide.http import open_url
            url = f"{_WASM_DATA_BASE}/cache/{filename}"
            return pd.read_csv(open_url(url))
        return pd.read_csv(Path(__file__).parent / "cache" / filename)

    return alt, load_cached_csv, mo, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 02: Cost and utilization measures

        ## The five-term vocabulary

        Five terms cover most of the cost-and-utilization vocabulary an informaticist needs to read a payer report, populate a value-based-care dashboard, or analyze the operational impact of a clinical change.
        """
    )
    return


@app.cell
def _(pd):
    vocab_table = pd.DataFrame(
        [
            {
                "Term": "Total cost of care",
                "Definition": "The sum of all allowed amounts (across all professional and institutional claims) attributed to a defined population over a defined time period.",
                "Operational form": "Sum `allowed_amount` over a patient cohort and date range. Reported per patient, per month, per attributed population, or per condition group.",
            },
            {
                "Term": "PMPM (per member per month)",
                "Definition": "Total cost of care divided by total member-months. The standardized cost-per-person-per-month unit.",
                "Operational form": "PMPM = (sum of allowed) / (sum of member-months). One member contributing 12 months of coverage in a year contributes 12 member-months. The denominator handles partial enrollment correctly.",
            },
            {
                "Term": "Utilization rate",
                "Definition": "The count of services of a given type per patient per period. Commonly expressed as visits per thousand member-months or admissions per thousand member-years.",
                "Operational form": "Count claims of a given category (E/M, ED, inpatient) per cohort, scale to 1,000 member-units. Comparable across populations of different sizes.",
            },
            {
                "Term": "Allowed amount",
                "Definition": "What the payer's contract with the provider permits as payment for the service. The reimbursement ceiling.",
                "Operational form": "On every claim line as `allowed_amount`. Equal to the sum of paid amount and patient responsibility.",
            },
            {
                "Term": "Patient-responsibility amount",
                "Definition": "What the patient owes for the service, as copay, coinsurance, or deductible.",
                "Operational form": "On every claim line as `patient_responsibility`. Reflects the plan design and the patient's accumulated deductible status at the time of service.",
            },
        ]
    )
    vocab_table.index = range(1, len(vocab_table) + 1)
    vocab_table.index.name = "row"
    vocab_table
    return (vocab_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Two properties of the vocabulary are load-bearing for the rest of the course.

        First, PMPM is the standardized comparison unit. Comparing total cost of care across populations of different sizes or different observation windows requires the per-member-per-month normalization. A payer report quoting "average member spent $4,200" without specifying the time window is essentially uninterpretable; the same number as $350 PMPM is precisely defined.

        Second, allowed amount (not billed amount) is the relevant economic quantity. The billed amount is what the provider asked for and is set by the provider's chargemaster; the allowed amount is what the payer's contract with the provider sets and is the actual reimbursement. Most analyses use the allowed amount; an analysis using the billed amount is either describing the chargemaster (legitimate but unusual) or making a mistake.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Ms. Reyes's 2024 claims in summary

        Ms. Reyes's actual claims data covers calendar year 2024, with all claims at place-of-service 11 (office) from her rheumatology practice plus a handful of lab and imaging claims. The table below loads her full claims.csv and reports the totals; the chart below shows monthly allowed amount.
        """
    )
    return


@app.cell
def _(load_cached_csv, pd):
    claims = load_cached_csv("claims.csv")
    claims["service_date"] = pd.to_datetime(claims["service_date"])
    claims["month"] = claims["service_date"].dt.to_period("M").astype(str)

    n_claims = len(claims)
    n_visits = claims["service_date"].nunique()
    total_allowed = float(claims["allowed_amount"].sum())
    total_paid = float(claims["paid_amount"].sum())
    total_pt = float(claims["patient_responsibility"].sum())

    summary_rows = pd.DataFrame(
        [
            {"Quantity": "Claim lines", "Value": f"{n_claims}"},
            {"Quantity": "Distinct service dates (visits)", "Value": f"{n_visits}"},
            {"Quantity": "Total allowed amount (2024)", "Value": f"${total_allowed:,.2f}"},
            {"Quantity": "Total paid amount (2024)", "Value": f"${total_paid:,.2f}"},
            {"Quantity": "Total patient responsibility (2024)", "Value": f"${total_pt:,.2f}"},
        ]
    )
    summary_rows.index = range(1, len(summary_rows) + 1)
    return claims, n_claims, n_visits, summary_rows, total_allowed, total_paid, total_pt


@app.cell
def _(summary_rows):
    summary_rows
    return


@app.cell
def _(alt, claims, pd):
    monthly = (
        claims.groupby("month", as_index=False)[["allowed_amount", "paid_amount", "patient_responsibility"]]
        .sum()
        .sort_values("month")
    )
    monthly["month_str"] = monthly["month"].astype(str)

    monthly_long = monthly.melt(
        id_vars="month_str",
        value_vars=["paid_amount", "patient_responsibility"],
        var_name="payer",
        value_name="dollars",
    )
    monthly_long["payer"] = monthly_long["payer"].map({
        "paid_amount": "Paid by payer",
        "patient_responsibility": "Patient responsibility",
    })

    monthly_chart = (
        alt.Chart(monthly_long)
        .mark_bar()
        .encode(
            x=alt.X("month_str:N", title="Service month", sort=None),
            y=alt.Y("dollars:Q", title="Allowed amount (USD)"),
            color=alt.Color("payer:N", title=""),
            tooltip=["month_str:N", "payer:N", "dollars:Q"],
        )
        .properties(width=560, height=260, title="Reyes 2024 allowed amount per month, stacked by payer / patient")
    )
    monthly_chart
    return monthly, monthly_chart, monthly_long


@app.cell
def _(mo):
    mo.md(
        r"""
        ### The three-amount split

        The chart above stacks the paid-amount bar and the patient-responsibility bar to recover the allowed amount per month. For Reyes, the patient-responsibility share is small (her plan's office-visit copay plus occasional lab cost-share); the bulk of the allowed amount is paid by her commercial insurer. This is the typical pattern for a patient on a commercial PPO with a moderate deductible. The same chart for a patient with a high-deductible plan would show patient-responsibility dominating until the deductible is met, then payer-paid taking over.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Per-claim averages and utilization rates

        Two derived measures aggregate the line-level claims into per-visit and per-period summaries. Both are reported on most payer dashboards.
        """
    )
    return


@app.cell
def _(claims, pd):
    per_visit = (
        claims.groupby("service_date", as_index=False)
        .agg(
            n_lines=("claim_id", "count"),
            allowed=("allowed_amount", "sum"),
            paid=("paid_amount", "sum"),
            patient=("patient_responsibility", "sum"),
        )
        .sort_values("service_date")
    )
    per_visit["allowed"] = per_visit["allowed"].round(2)
    per_visit["paid"] = per_visit["paid"].round(2)
    per_visit["patient"] = per_visit["patient"].round(2)
    per_visit.index = range(1, len(per_visit) + 1)
    avg_per_visit = float(per_visit["allowed"].mean())
    _ = pd
    return avg_per_visit, per_visit


@app.cell
def _(per_visit):
    per_visit
    return


@app.cell
def _(avg_per_visit, claims, mo, n_visits):
    member_months = 12
    pmpm = float(claims["allowed_amount"].sum() / member_months)
    visits_per_1000_mm = round(n_visits / member_months * 1000)
    mo.md(
        f"""
        **Derived measures for Reyes (calendar year 2024, 12 member-months):**

        - **Visits:** {n_visits}
        - **Average allowed amount per visit:** ${avg_per_visit:.2f}
        - **PMPM (allowed):** ${pmpm:.2f}
        - **Visits per 1,000 member-months:** {visits_per_1000_mm}

        Interpretation. A PMPM of ${pmpm:.0f} for a single patient is high relative to a general adult population (typical commercial-PPO PMPM for a working-age adult is around $400 to $700). Reyes's elevated PMPM reflects the rheumatology specialty visits, the frequent serological monitoring, and (in the second half of 2024) the adalimumab specialty-pharmacy cost. A real PMPM analysis on a population would compute the same number across thousands of members.
        """
    )
    return member_months, pmpm, visits_per_1000_mm


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Interactive: filter by month or by service category

        The widget below filters Reyes's claims by month. The reactive summary updates as the filter changes. The default (All months) shows the full year.
        """
    )
    return


@app.cell
def _(claims, mo):
    month_options = ["All months"] + sorted(claims["month"].unique().tolist())
    month_filter = mo.ui.dropdown(options=month_options, value="All months", label="Filter to month")
    month_filter
    return month_filter, month_options


@app.cell
def _(claims, month_filter, pd):
    if month_filter.value == "All months":
        filtered = claims.copy()
    else:
        filtered = claims[claims["month"] == month_filter.value].copy()
    if len(filtered) == 0:
        filtered_summary = pd.DataFrame([{"Quantity": "No claims", "Value": "0"}])
    else:
        filtered_summary = pd.DataFrame(
            [
                {"Quantity": "Claim lines", "Value": f"{len(filtered)}"},
                {"Quantity": "Distinct service dates", "Value": f"{filtered['service_date'].nunique()}"},
                {"Quantity": "Allowed amount", "Value": f"${filtered['allowed_amount'].sum():,.2f}"},
                {"Quantity": "Paid by payer", "Value": f"${filtered['paid_amount'].sum():,.2f}"},
                {"Quantity": "Patient responsibility", "Value": f"${filtered['patient_responsibility'].sum():,.2f}"},
            ]
        )
    filtered_summary.index = range(1, len(filtered_summary) + 1)
    return filtered, filtered_summary


@app.cell
def _(filtered_summary):
    filtered_summary
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A note on commercial vs Medicare reimbursement

        Two reimbursement-rate facts shape every utilization-and-cost analysis in the US.

        - **Medicare pays on a published fee schedule.** The Medicare Physician Fee Schedule (MPFS) publishes a fee for every CPT code, every year, every locality. For office E/M, lab, and most outpatient services, Medicare's rate is below most commercial rates.
        - **Commercial payers negotiate above the Medicare rate.** The standard contracting practice is to set commercial rates as a multiple of Medicare. Commercial payers often pay 110% to 200% of the Medicare rate for the same service.

        The consequence for analyses across mixed populations: aggregating allowed amounts across a Medicare-and-commercial cohort over-weights the commercial patients in the cost total because their per-service dollars are higher. The remedy is to compute the cost separately by payer type or to standardize against a reference rate before aggregating.
        """
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "11",
        "16",
        "PMPM as a leadership metric",
        "Course 16 (Leadership and Professional Practice) takes up PMPM as one of the KPIs an informaticist owns at the institutional level. The PMPM dashboard for an attributed ACO population is the operational form of this track's vocabulary at the level a CMO or CMIO would see weekly.",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "11",
        "18",
        "Utilization measurement on the population view",
        "Course 18 (Population and Public Health Informatics) takes up the population-level utilization view. Visits per 1,000 member-months and admissions per 1,000 member-years are the standard population denominators; the per-patient version this track introduces is the building block.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        Five terms cover most of the cost-and-utilization vocabulary: total cost of care, PMPM, utilization rate, allowed amount, and patient-responsibility amount. PMPM is the standardized cross-population comparison unit; allowed amount (not billed amount) is the relevant economic quantity; the three-amount split (allowed = paid + patient-responsibility) holds on every claim line. Reyes's 2024 claims summarize to a high single-patient PMPM driven by specialty visits, serological monitoring, and the adalimumab specialty-pharmacy cost. Commercial vs Medicare reimbursement differs materially and has to be handled explicitly in any cross-payer analysis.

        Track 03 takes up decision analysis: how to combine these cost inputs with clinical outcome probabilities to make an expected-value comparison of two treatment strategies.
        """
    )
    return


if __name__ == "__main__":
    app.run()
