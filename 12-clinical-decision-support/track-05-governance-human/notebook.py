"""Track 05: Governance and the human side.

A CDS deployment that is technically correct can still fail for
governance reasons: the wrong committee approved it, the clinicians were
not consulted in design, the equity audit was not done, or the
regulatory category was misread. The track presents the governance
vocabulary, addresses equity in CDS with the race-correction
reconsideration of the past decade, surveys the FDA SaMD and ONC
regulatory landscape, and closes with the vendor-evaluation checklist.
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
        "09": "AI in medicine",
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
        # Track 05: Governance and the human side

        ## What governance is for

        A CDS deployment that is technically correct can fail for governance reasons. The wrong committee approved a tool whose risk warranted a different review process. The clinicians who use the alert were not consulted in design and find it disruptive. The equity audit was not performed and the deployed alert under-flags a clinically important subgroup. The regulatory category was misread and the institution is operating an FDA-regulated tool without clearance.

        CDS governance is the institutional infrastructure that addresses these failure modes upstream. The track defines the vocabulary (who decides what gets built, who decides what gets retired, who is responsible when an alert goes wrong), addresses equity in CDS with the race-correction reconsideration of the past decade as the central case, surveys the regulatory landscape (FDA SaMD, IMDRF risk classification, ONC certification), and closes with the vendor-evaluation checklist a clinical informaticist uses when an institution is considering a new CDS tool.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The governance vocabulary

        Five roles cover most CDS governance structures in US academic medical centers and large community systems. The names vary by institution; the functions are stable.
        """
    )
    return


@app.cell
def _(pd):
    governance_table = pd.DataFrame(
        [
            {
                "Role": "CDS governance committee",
                "What it does": "Approves new CDS interventions before deployment. Reviews evaluation data on existing interventions periodically. Retires interventions that are not meeting their stated benefit.",
                "Who is on it": "CMIO, CNIO, departmental clinical leaders, pharmacy lead, clinical informatics analysts, patient-safety representative, legal counsel.",
                "Meeting frequency": "Monthly is typical at academic medical centers; quarterly at smaller institutions.",
            },
            {
                "Role": "Clinical content owner",
                "What it does": "The clinician (typically a department-level physician or APP) responsible for the clinical correctness of a specific intervention. Reviews the alert's logic, signs off on the recommended action, owns periodic re-evaluation.",
                "Who is on it": "Named individual per intervention. Often a department-level subject-matter expert.",
                "Meeting frequency": "Reviews triggered by alert volume, override rate, or annual cycle.",
            },
            {
                "Role": "Implementation analyst / builder",
                "What it does": "Translates the clinical specification into the CDS rule (in the EHR rules engine or as a CDS Hooks service). Manages the deployment, the rollback path, the monitoring instrumentation.",
                "Who is on it": "Clinical informatics analyst or EHR vendor-certified builder.",
                "Meeting frequency": "Active during build and deployment; on-call during early post-go-live.",
            },
            {
                "Role": "Evaluation lead",
                "What it does": "Designs and runs the evaluation (the ITS or stepped-wedge from Track 04). Produces the post-go-live report the governance committee reviews.",
                "Who is on it": "Clinical informatics analyst with epidemiology or biostatistics background, or a partnered research group.",
                "Meeting frequency": "Active during the evaluation period (typically 6 to 12 months post-go-live).",
            },
            {
                "Role": "Patient-safety and quality oversight",
                "What it does": "Receives reports of CDS-related safety events. Coordinates root-cause analysis when an alert is implicated in a near-miss or an adverse event. Maintains the institutional CDS safety registry.",
                "Who is on it": "Patient-safety officer, risk-management lead, often a clinical informaticist with safety training.",
                "Meeting frequency": "Event-driven plus periodic registry review.",
            },
        ]
    )
    governance_table.index = range(1, len(governance_table) + 1)
    governance_table.index.name = "row"
    governance_table
    return (governance_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three operational properties of the governance structure are load-bearing.

        First, the named clinical content owner per intervention is the single most important governance practice. An intervention without a named owner has no one whose job includes keeping it correct. Unowned interventions accumulate stale logic, drift away from current guidelines, and are the source of most post-deployment CDS failures.

        Second, the retirement path is as important as the deployment path. A CDS portfolio that only grows accumulates noise; the governance committee's authority to retire interventions is what keeps the portfolio at a manageable size. The retirement criteria (override rate above a threshold for sustained periods, no measurable benefit at planned evaluation, supplanted by a better intervention) should be written down in advance.

        Third, the patient-safety reporting line is non-negotiable. A CDS alert that fires on the wrong patient, recommends the wrong dose, or suppresses a safety alarm is a patient-safety event the same way a medication error is a patient-safety event. The institutional safety-reporting infrastructure should treat CDS-related events as part of its scope.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Equity in CDS: the race-correction reconsideration

        The past decade of clinical-medicine literature has reconsidered the use of race as an input variable in clinical algorithms. The reconsideration applies directly to CDS: many deployed alerts use clinical scores that historically embedded race as an input, and the question of whether to keep, modify, or replace those scores is now a governance question every institution faces.

        Three published cases are load-bearing.
        """
    )
    return


@app.cell
def _(pd):
    race_correction_table = pd.DataFrame(
        [
            {
                "Algorithm": "eGFR (estimated glomerular filtration rate)",
                "What was the race correction": "The CKD-EPI 2009 equation multiplied the eGFR by 1.159 for Black patients, producing a higher reported eGFR than the same equation would for a non-Black patient with the same serum creatinine.",
                "Why it mattered clinically": "Higher reported eGFR meant Black patients were less likely to be flagged for nephrology referral, transplant evaluation, or dose adjustments. The differential systematically delayed care.",
                "Resolution": "The CKD-EPI 2021 equation removed the race coefficient. NKF and ASN jointly recommended adoption of the race-free equation in 2021. Most US institutions have transitioned.",
            },
            {
                "Algorithm": "VBAC (vaginal birth after cesarean) calculator",
                "What was the race correction": "The MFMU VBAC calculator (Grobman et al. 2007) included Black and Hispanic race as factors that reduced the predicted probability of successful VBAC.",
                "Why it mattered clinically": "Lower predicted success probability led clinicians and patients toward repeat cesarean and away from trial of labor, with downstream effects on subsequent pregnancies, complications, and patient autonomy.",
                "Resolution": "The MFMU group republished the calculator without race in 2021. The race-free version is the current recommended tool.",
            },
            {
                "Algorithm": "ASCVD (atherosclerotic cardiovascular disease) Pooled Cohort Equations",
                "What was the race correction": "The 2013 ACC/AHA Pooled Cohort Equations used Black race as a categorical input to the risk equation, with separate model coefficients for Black and non-Black patients.",
                "Why it mattered clinically": "The same patient with the same clinical features had a different risk estimate depending on the recorded race. The race coefficient had been derived from cohorts whose representativeness for current US populations is contested.",
                "Resolution": "The 2023 AHA PREVENT equations removed race. Adoption is ongoing.",
            },
        ]
    )
    race_correction_table.index = range(1, len(race_correction_table) + 1)
    race_correction_table.index.name = "row"
    race_correction_table
    return (race_correction_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three operational consequences for the institutional CDS governance.

        First, the institution should inventory every CDS intervention that depends on a clinical score that includes race as an input. The inventory is the prerequisite for any updating effort.

        Second, the institution should replace deprecated race-correction-dependent scores with their race-free successors when those exist (eGFR, VBAC, ASCVD as above). The replacement is operationally non-trivial because the EHR rule, the CDS service, the reporting workbench, and the embedded patient-facing materials all reference the score.

        Third, the institution should monitor subgroup performance after replacement. A race-free score is not automatically a race-fair score; the new score may produce its own subgroup disparities that the inventory and monitoring infrastructure has to be ready to catch.

        The Vyas, Eisenstein, and Jones 2020 NEJM paper "Hidden in Plain Sight: Reconsidering the Use of Race Correction in Clinical Algorithms" is the load-bearing single reference for this conversation. The track go-deeper links it.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "12",
        "09",
        "Bias entry points and subgroup performance",
        "Course 09 Track 5 introduced the four entry points for bias and the subgroup-performance vocabulary. A CDS alert is a model in the wild; the governance committee's equity review is the operational application of the Course 09 subgroup analysis at the institutional level.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The regulatory landscape

        Three regulatory frameworks shape what an institution can and cannot deploy as CDS.
        """
    )
    return


@app.cell
def _(pd):
    regulatory_table = pd.DataFrame(
        [
            {
                "Regulatory framework": "FDA Software as a Medical Device (SaMD)",
                "What it governs": "Software that meets the FDA's definition of a medical device. Includes some clinical-decision-support tools, especially those that drive autonomous actions or that the clinician cannot independently verify.",
                "What it requires": "Pre-market clearance (510(k)) or approval (PMA) before deployment, depending on the risk category. Post-market surveillance and adverse-event reporting.",
                "Implications for the institution": "An institution deploying FDA-regulated CDS must verify the clearance status of the tool and follow the manufacturer's instructions for use. Modifying a cleared tool in ways that change the intended use can trigger a new clearance requirement.",
            },
            {
                "Regulatory framework": "21st Century Cures Act CDS exemptions (FDA)",
                "What it governs": "The four-prong exemption in the Cures Act says CDS that displays clinical information and recommendations to a clinician who can independently review the basis is not a medical device and therefore not FDA-regulated. The Cures-Act exemption applies to most traditional CDS.",
                "What it requires": "The four criteria must all be met: not intended to acquire/process medical-device data; analyzes clinical information; provides recommendations to a clinician; the clinician can independently review the basis.",
                "Implications for the institution": "An institution operating a CDS that fails any of the four criteria (often because the clinician cannot review the basis, common with opaque AI models) loses the exemption and is operating an FDA-regulated device.",
            },
            {
                "Regulatory framework": "ONC HTI-1 / predictive-decision-support intervention requirements",
                "What it governs": "The 2024 ONC HTI-1 rule and its predictive-decision-support-intervention (PDSI) requirements apply to AI-based CDS in ONC-certified EHRs. Sets transparency, intervention-risk-management, and ongoing-monitoring requirements.",
                "What it requires": "Certified EHRs that ship with predictive-decision-support interventions must expose 31 metadata attributes (training data source, intended use, performance, etc) and must support institutional intervention-risk-management practices.",
                "Implications for the institution": "An institution deploying AI-based CDS through a certified EHR inherits the certification's PDSI requirements. The institution should know which deployed interventions are PDSIs and should follow the associated intervention-risk-management process.",
            },
        ]
    )
    regulatory_table.index = range(1, len(regulatory_table) + 1)
    regulatory_table.index.name = "row"
    regulatory_table
    return (regulatory_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Two operational rules for the regulatory question.

        First, the regulatory category of a deployed CDS is a determination the institution has to make explicitly. An undocumented assumption that an intervention is "just CDS, not a device" is a compliance risk. The CDS governance committee should record the regulatory category as part of the approval record for every intervention.

        Second, the AI-based CDS category is the regulatory frontier. The FDA, the FTC, the ONC, and state-level regulators have all issued AI-CDS guidance in 2023 to 2025 that is still being interpreted. An institution deploying AI-based CDS should follow regulatory developments closely and build compliance flexibility into the deployment architecture.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The vendor-evaluation checklist

        Six questions, asked of a vendor before adoption of a new CDS tool, surface most CDS-related governance and equity problems at the procurement stage rather than after deployment.

        - **Intended use.** What is the precise clinical question the tool answers, in what setting, for what patient population? An imprecise intended-use statement is a sign that the vendor has not done the design work themselves and is asking the institution to figure out what the tool is for.
        - **Training and validation.** Where did the training data come from, when was it collected, what was the validation approach, what is the performance on a cohort similar to the institution's patient population? The Course 09 Track 4 five-dimension appraisal framework applies directly.
        - **Subgroup performance.** AUC and calibration reported separately by race, sex, age, payer mix. The Course 09 Track 5 vocabulary applies. A vendor that cannot produce this is selling a tool that has not been honestly evaluated for equity.
        - **Regulatory status.** FDA SaMD cleared, exempt, or unclear. ONC PDSI categorization if delivered through a certified EHR. The vendor should be able to answer this in writing.
        - **Modifiability.** Can the institution change the threshold, the cohort, the action? A tool that the institution cannot tune to its own context is not adoptable beyond pilot.
        - **Post-deployment monitoring.** What is the vendor's plan for monitoring performance after deployment? What is the institution responsible for? What is the vendor responsible for? The contract should answer this; if it does not, the deployment is undefined post-go-live.

        A vendor that cannot answer most of these questions is selling a product that is not ready for clinical deployment.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "12",
        "03",
        "Privacy, ethics, governance from Course 03",
        "Course 03 introduced the governance and ethics framework at the curriculum level. The CDS governance committee, the equity audit, and the regulatory landscape this track addresses are the operational application of that framework at the CDS-deployment level.",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "12",
        "16",
        "CDS governance as a leadership question",
        "Course 16 (Leadership and Professional Practice) takes up institutional governance as a leadership skill. The CDS governance committee is one of the standing committees a CMIO or clinical informatics director chairs; the leadership skills Course 16 covers (stakeholder management, change management, ROI conversations) apply directly.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        CDS governance is the institutional infrastructure that addresses the governance, equity, and regulatory failure modes upstream. Five roles cover most governance structures (governance committee, clinical content owner, implementation analyst, evaluation lead, patient-safety oversight); the clinical-content-owner role is the highest-leverage single practice. Equity in CDS is a current and active conversation, with the race-correction reconsideration (eGFR, VBAC calculator, ASCVD) as the canonical case. Three regulatory frameworks (FDA SaMD, the Cures-Act CDS exemption, ONC HTI-1 PDSI) shape what an institution can deploy and how. The vendor-evaluation checklist surfaces most CDS-procurement problems before they become deployment problems.

        Course 12 closes here. The capstone takes up the seven-step CDS design exercise that integrates everything every prior course has covered into a single end-to-end CDS-design brief.
        """
    )
    return


if __name__ == "__main__":
    app.run()
