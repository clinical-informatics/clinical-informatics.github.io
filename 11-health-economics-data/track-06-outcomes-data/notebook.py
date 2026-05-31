"""Track 06: Reading outcomes data critically.

Value-based care vocabulary at the level a clinical informaticist needs at
the contracting table. The three common confounders that affect almost
every published health-economics outcomes study (treatment selection,
immortal time bias, channeling). The CHEERS reporting checklist as the
operational appraisal framework for cost-effectiveness papers.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import types

    import marimo as mo
    import pandas as pd

    _COURSE_TITLES = {
        "03": "Privacy, ethics, and governance",
        "04": "Clinical epidemiology",
        "13": "Research reproducibility",
        "16": "Leadership and professional practice",
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

    return mo, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 06: Reading outcomes data critically

        ## What this track is for

        Value-based care, accountable-care organizations, bundled payments, and quality-payment programs all rest on outcomes measurement against a payer-defined denominator. The track defines the value-based-care vocabulary at the level a clinical informaticist needs at the contracting table, addresses the three confounders that affect almost every published health-economics outcomes study, and closes with the CHEERS reporting checklist as the operational appraisal framework for any cost-effectiveness paper a clinician is asked to consider.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The value-based-care vocabulary

        Five payment-model categories cover most of the value-based-care landscape in 2025 to 2026 US practice. The Health Care Payment Learning and Action Network (HCP-LAN) framework places each one on a four-step continuum from fee-for-service to fully population-based payment.
        """
    )
    return


@app.cell
def _(pd):
    vbc_table = pd.DataFrame(
        [
            {
                "Payment model": "Fee-for-service (FFS)",
                "HCP-LAN category": "Category 1",
                "How payment works": "Provider is paid per service rendered, with no link to outcomes or quality.",
                "Informatics implication": "No additional measurement infrastructure required beyond claims. The historical default.",
            },
            {
                "Payment model": "Pay-for-performance (P4P)",
                "HCP-LAN category": "Category 2 (FFS with quality)",
                "How payment works": "Fee-for-service is the base; a percentage bonus or penalty is applied based on quality-measure performance.",
                "Informatics implication": "Quality measures (HEDIS, MIPS, eCQM) must be computed reliably from EHR or claims; the measurement infrastructure is the institutional dependency.",
            },
            {
                "Payment model": "Bundled payment",
                "HCP-LAN category": "Category 3 (APMs built on FFS)",
                "How payment works": "A single payment covers all services for an episode of care (a hip replacement, a cardiac event), regardless of how many services were rendered. The provider keeps the savings if costs come in under the bundle.",
                "Informatics implication": "Episode definition is the technical center. Episodes must be constructed reliably from the claims data; the analytics decide whether the institution gains or loses on the bundle.",
            },
            {
                "Payment model": "Accountable Care Organization (ACO)",
                "HCP-LAN category": "Category 3 or 4",
                "How payment works": "Provider group is held responsible for the total cost of care and the quality of care for a defined patient population (attributed members). Shared savings or losses against a benchmark.",
                "Informatics implication": "Population denominator (the attribution algorithm) and risk-stratified quality measurement must be operationalized. The Medicare Shared Savings Program and ACO REACH are the canonical examples.",
            },
            {
                "Payment model": "Population-based / capitation",
                "HCP-LAN category": "Category 4",
                "How payment works": "Provider is paid a fixed amount per member per month to cover all care for the attributed population, with quality and outcome adjustments.",
                "Informatics implication": "The strongest informatics dependency. Risk adjustment, quality measurement, total-cost-of-care reporting, and population health management all become operational requirements. Capitation in Medicare Advantage is the canonical example.",
            },
        ]
    )
    vbc_table.index = range(1, len(vbc_table) + 1)
    vbc_table.index.name = "row"
    vbc_table
    return (vbc_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Two operational consequences for the clinical informaticist.

        First, every step up the HCP-LAN ladder requires more measurement infrastructure. Moving from FFS to P4P adds quality-measure computation; moving from P4P to ACO adds population denominator construction; moving from ACO to capitation adds risk adjustment. The institutional decision to enter or expand a VBC contract is a decision to invest in the corresponding infrastructure.

        Second, the measurement infrastructure has to be correct on the contract's denominator definition, not just on the institution's preferred definition. The CMS ACO attribution algorithm, the bundled-payment episode construction logic, and the eCQM specifications are payer-defined; the institution's analytics have to reproduce the payer's calculation, not an idealized version of it. Discrepancies between the institution's internal numbers and the payer's settlement statement are the most common operational pain point in VBC contracts.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Three confounders that affect almost every health-economics outcomes study

        Observational outcomes research in claims and EHR data is subject to three confounders that randomized trials handle by design. Each one has a clinical example and a standard published methodological response.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Treatment selection bias

        The choice of treatment is correlated with the outcome of interest through factors the analyst has not measured. A naive comparison of outcomes by treatment then reflects the unmeasured factors as well as the treatment effect.

        **Clinical example.** A study comparing one-year mortality between adalimumab-treated and methotrexate-only-treated RA patients in a claims database finds that adalimumab patients have lower mortality. The naive interpretation is that adalimumab is protective. The more likely interpretation is that the rheumatologist chose adalimumab for the healthier subset of MTX-inadequate-responder patients (those with no contraindications, no active malignancy, no advanced age, no advanced comorbidity) and prescribed MTX-only for the sicker subset. The mortality difference reflects the selection, not the drug.

        **Published response.** Propensity-score matching, instrumental-variable analysis, target-trial emulation, or new-user / active-comparator designs. The published methods literature has a 30-year tradition of addressing this confounder; the toolset is mature and the appraisal expectation is that the paper used at least one of these methods.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Immortal time bias

        The time before a patient becomes eligible for the exposure of interest is misclassified as exposed time. The exposed group's outcomes are inflated because patients who experienced the outcome before becoming exposed cannot enter the exposed group.

        **Clinical example.** A study of biologic-treated RA patients counts the months between RA diagnosis and biologic initiation as "biologic-exposed" time. Patients who died of any cause in those months are then counted as biologic-exposed deaths, but they were not actually exposed; or, if the study correctly classifies them as unexposed, the exposed group still requires patients to have survived long enough to start the biologic, which inflates the exposed group's apparent survival.

        **Published response.** Time-varying exposure analysis (the patient is unexposed before initiation and exposed after), or the active-comparator design (compare biologic initiators to csDMARD initiators starting at the moment of initiation rather than at the moment of diagnosis). Suissa's 2008 paper on immortal time bias in pharmacoepidemiology is the most-cited reference.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Channeling

        Physicians channel certain patients toward certain drugs in non-random ways. The newly approved drug goes to the patients who failed older drugs; the older drugs are used by patients who tolerated them; the most-discussed drug is used by patients whose physicians follow the literature. Channeling is a special case of selection bias driven by physician prescribing patterns.

        **Clinical example.** When tofacitinib was approved for RA in 2012, the first wave of prescriptions went to patients who had failed multiple biologics. A naive 2014 comparison of one-year outcomes for tofacitinib vs adalimumab found tofacitinib had worse outcomes; the more accurate interpretation was that tofacitinib was prescribed to patients with refractory disease (channeling), not that tofacitinib was a worse drug. Comparisons made several years later, after channeling had stabilized, gave a different picture.

        **Published response.** Active-comparator new-user designs that restrict the comparison to patients initiating either drug for the same indication at the same point in their disease course. Stratification by prior treatment history. Sensitivity analysis on the channeling-relevant subgroups.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The CHEERS reporting checklist

        The Consolidated Health Economic Evaluation Reporting Standards (CHEERS) is the published reporting checklist for cost-effectiveness analyses. The 28-item checklist is the operational appraisal framework for any CE paper.

        Below is the high-yield-first ordering an informaticist can use at the manuscript or vendor-pitch level. A CE paper that handles every item below well is one that can credibly inform a coverage decision; a paper that omits any of them is not ready to act on yet.
        """
    )
    return


@app.cell
def _(pd):
    cheers_short = pd.DataFrame(
        [
            {"Order": 1, "CHEERS item": "Perspective", "What to check": "Whose costs and benefits are counted (health-care system, payer, societal)? The perspective shapes which costs are included and is the single biggest determinant of the ICER."},
            {"Order": 2, "CHEERS item": "Time horizon", "What to check": "Over what period are costs and effects accumulated? A one-year horizon for a chronic-disease intervention systematically undercounts both. A lifetime horizon is the published-methods standard."},
            {"Order": 3, "CHEERS item": "Discount rate", "What to check": "What annual rate is applied to discount future costs and effects (US 3%, UK 3.5%)? An undiscounted analysis of a long-horizon decision is a methods error."},
            {"Order": 4, "CHEERS item": "Source of effectiveness data", "What to check": "Meta-analysis of RCTs is strongest; single RCT is acceptable; observational data is weaker (and inherits the three confounders above); expert opinion is the weakest. The strength of the effectiveness evidence bounds the credibility of the ICER."},
            {"Order": 5, "CHEERS item": "Sensitivity analyses", "What to check": "Did the paper present one-way, two-way, and probabilistic sensitivity analyses? An analysis without sensitivity analyses cannot establish whether the headline ICER is robust to its inputs."},
            {"Order": 6, "CHEERS item": "Model assumptions", "What to check": "What model structure was used (decision tree, Markov, micro-simulation)? Are the structural assumptions documented and defensible? An undocumented structure is uninterpretable."},
            {"Order": 7, "CHEERS item": "Subgroup analyses", "What to check": "Was the ICER reported separately for clinically relevant subgroups (race, sex, age, severity)? An overall ICER that masks dramatic subgroup variation can lead to coverage decisions that are inappropriate for the subgroups most affected."},
            {"Order": 8, "CHEERS item": "Conflicts of interest", "What to check": "Industry funding for CE analyses is associated with conclusions more favorable to the sponsor's product. Funding source and conflicts are required disclosures and are part of the appraisal."},
        ]
    )
    cheers_short.index = range(1, len(cheers_short) + 1)
    cheers_short.index.name = "row"
    cheers_short
    return (cheers_short,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Two reading rules.

        First, every CHEERS item is independently load-bearing. A CE analysis with a defensible perspective, time horizon, and effectiveness source can still be misleading if the sensitivity analyses were omitted or if subgroup performance was not reported. The 28 items together are the appraisal; weakness on any one item is a meaningful gap.

        Second, the CHEERS checklist is necessary but not sufficient for adoption. A paper that meets every CHEERS item can still describe an intervention that does not fit the local institution's case-mix, payer mix, or workflow. The CHEERS check filters the papers worth reading further; the local-fit check determines which of those should change practice.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Reading observational outcomes data: STROBE and RECORD-PE

        Two additional reporting checklists cover the broader observational-outcomes-research landscape that CHEERS does not.

        - **STROBE (Strengthening the Reporting of Observational Studies in Epidemiology).** The general observational-research reporting standard. Items cover the cohort definition, the exposure and outcome operationalization, the confounding-adjustment approach, and the sensitivity analyses. Any observational outcomes paper should report against STROBE.
        - **RECORD-PE (REporting of studies Conducted using Observational Routinely-collected health Data - PharmacoEpidemiology extension).** Specific to studies of medication effects in routinely-collected data (claims, EHR). Adds items on the data-source description, the operational definitions used, and the time-varying exposure handling. Any pharmacoepidemiologic study using claims or EHR data should report against RECORD-PE in addition to STROBE.

        The two reporting standards are the operational form of the three-confounder vocabulary above. A study that addresses STROBE and RECORD-PE in full will, by construction, have addressed treatment selection bias (RECORD-PE item on confounding adjustment), immortal time bias (the time-varying-exposure item), and channeling (the active-comparator-design item).
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "11",
        "04",
        "Selection bias and confounding from Course 04",
        "Course 04 Track 2 introduced selection bias and confounding. The three confounders in this track (treatment selection, immortal time, channeling) are operational forms of the same concept that recur in any observational outcomes research using claims or EHR data.",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "11",
        "16",
        "VBC contracting from the leadership view",
        "Course 16 (Leadership and Professional Practice) takes up the contract-negotiation side of VBC. The vocabulary in this track is the analytic backbone of the CMO / CMIO conversations about whether to enter a particular VBC contract and how to invest in the measurement infrastructure the contract requires.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        Value-based care has five payment-model categories on the HCP-LAN four-step ladder, from fee-for-service through population-based capitation. Each step up the ladder requires more measurement infrastructure, and the infrastructure must be correct on the payer's denominator definition, not on the institution's preferred definition. Three confounders (treatment selection, immortal time, channeling) affect almost every health-economics observational outcomes study; each has a standard published methodological response. The CHEERS checklist is the appraisal framework for any cost-effectiveness paper; STROBE and RECORD-PE cover the broader observational-research landscape.

        Course 11 closes here. The capstone takes up the building exercise of constructing a decision tree for the RA treatment choice and running a one-way sensitivity analysis end-to-end.
        """
    )
    return


if __name__ == "__main__":
    app.run()
