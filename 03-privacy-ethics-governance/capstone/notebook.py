"""Capstone for course 03: Privacy, ethics, and governance.

Five-dimension Socratic review of a real-shaped proposal: develop an AI
sepsis predictor on multi-site EHR data, partner with a vendor, deploy
back to clinical workflow, and eventually license out. The learner writes
each section, commits, and the reveal opens. At the end, the committee
memo is assembled from the learner's own writing.
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

    import marimo as mo
    import pandas as pd

    return mo, pd


@app.cell
def _(mo):
    mo.md(
        r"""
        # Capstone: Privacy, Ethics, and Governance

        ## The proposal on the docket

        **Title:** Project Helios. An AI-based early-sepsis prediction tool for inpatient deployment.

        **Sponsor:** A regional integrated health system in the northeastern United States. The system comprises the **Helios Academic Medical Center** (Boston, 720 beds, urban, research-intensive, predominantly insured patient mix) and three **community hospital partners**: Helios South (Worcester, 280 beds, mixed urban/suburban, ~35% Medicaid), Helios West (Springfield, 220 beds, urban, ~50% Medicaid, predominantly Hispanic catchment), and Helios North (rural Vermont border, 90 beds, predominantly white catchment).

        **What they want to build.** A real-time deterioration-prediction model for early sepsis on the inpatient wards, integrated with the EHR's rapid-response workflow. Adult inpatients only. Five years of historical EHR data (~280,000 unique patients) to train; prospective validation; deployment across all four sites.

        **The vendor.** A national AI company specializing in clinical decision support. The proposal includes a Business Associate Agreement under which the vendor receives identifiable PHI to develop the model, and a Master Services Agreement covering the eventual deployment. The vendor's standard contract includes a clause permitting the vendor to use "learnings derived from customer data" to improve its products sold to other health systems.

        **The eventual goal.** Beyond deployment within the Helios system, the institution plans to license the model out to other health systems for revenue, with Helios receiving a share of the licensing fees.

        **Regulatory landscape.** Patients are primarily Massachusetts residents but the Helios catchment includes patients from Vermont, New Hampshire, Connecticut, and Rhode Island. Approximately 4% of patients are international (mostly EU residents seeking specialty care at the AMC).

        **What's been done so far.** Draft IRB protocol (waiver of consent requested for the retrospective training data). Privacy-office sign-off pending. Vendor security questionnaire returned. No subgroup-stratified performance analysis has been pre-specified.

        You are the clinical informatics representative on the governance committee. The committee meets next Wednesday. **Your job is to produce a written review across five dimensions.** Each section is Socratic: commit your written analysis first, then the reveal opens. The committee memo at the end is assembled from your writing.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Step 1 of 5: Privacy threat model

        Apply Track 01. Who would re-identify this dataset? Why? What would they gain? Which quasi-identifiers are load-bearing? What's the residual re-identification risk after Safe Harbor de-identification?

        Write at least a paragraph. The reveal opens at 100 characters.
        """
    )
    return


@app.cell
def _(mo):
    from shared.socratic import commit_text, go_deeper, reflection, reveal, scenario

    step1_widget, step1_ready = commit_text(
        "Your privacy threat model for Project Helios",
        min_chars=100,
    )
    step1_widget
    return commit_text, go_deeper, reflection, reveal, scenario, step1_ready, step1_widget


@app.cell
def _(mo, reveal, step1_ready, step1_widget):
    mo.stop(
        not step1_ready(),
        mo.callout(
            mo.md("_Write at least a short paragraph above. The reveal opens after you do._"),
            kind="neutral",
        ),
    )

    ideal_1 = (
        "**Threat model for Project Helios.** Three relevant attacker categories: "
        "(1) **journalists and public figures**: a public figure admitted at Helios AMC for sepsis would be of interest, "
        "and the multi-site dataset preserves dates of admission which combined with public reporting (obituary, news article, sports injury) is identifying; "
        "(2) **commercial linkers**: insurance and data brokers cross-referencing Helios records against marketing profiles, made easier by the four-site geographic spread that allows narrowing to a specific community; "
        "(3) **employers and adversaries**: an HR department or estranged family member testing whether a specific person was hospitalized.\n\n"
        "**Quasi-identifiers that matter most.** Date of admission (clinical-timeline + obituary matching). 5-digit ZIP (especially for the Vermont border site where most ZIPs are very small populations; the 20,000-person Safe Harbor floor may not protect them). Rare diagnoses combined with site (a 28-year-old with Castleman disease admitted to Helios North is uniquely identifiable on three fields). The longitudinal structure across years adds the Netflix-Prize attack surface: a sequence of encounters at this site/date/diagnosis combination is itself an identifier.\n\n"
        "**Residual risk after Safe Harbor.** Modest for the AMC patients (large urban population). Substantial for the rural site (small ZIPs, small subgroups). Highest for the rare-disease tail at any site. Critically, the model **training set** uses identifiable PHI under a BAA; the de-identification question is only relevant for downstream releases (publications, benchmark datasets). The committee needs to know which downstream releases are planned and what each one's threat model is."
    )

    reveal(step1_widget.value, ideal_1, learner_label="Your threat model")
    return (ideal_1,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Step 2 of 5: Legal pathway

        Apply Track 02. Which HIPAA pathway is appropriate for each phase of the project? What state laws layer on top? Does GDPR apply, and how? What needs to be in the Data Use Agreement and the Business Associate Agreement?

        Write a paragraph or two.
        """
    )
    return


@app.cell
def _(commit_text, mo):
    step2_widget, step2_ready = commit_text(
        "Your legal-pathway analysis",
        min_chars=120,
    )
    step2_widget
    return step2_ready, step2_widget


@app.cell
def _(mo, reveal, step2_ready, step2_widget):
    mo.stop(
        not step2_ready(),
        mo.callout(
            mo.md("_Write your analysis above. The reveal opens at 120 characters._"),
            kind="neutral",
        ),
    )

    ideal_2 = (
        "**Three phases, three pathways.**\n\n"
        "**(a) Retrospective training data.** PHI in motion to the vendor under a BAA. Not a de-identification path; this is HIPAA TPO healthcare-operations or research-with-IRB-waived-authorization, depending on framing. The IRB protocol with the waiver of authorization (cited in the proposal) is the right path for the research dimension. The BAA must cover the security, use-limitation, and termination terms. **Critically**, the vendor's standard 'learnings derived from customer data' clause needs scrutiny: as currently drafted, it permits the vendor to apply derivatives of Helios patients' data to other customers' models. This may be HIPAA-permitted but is the Project Nightingale archetype.\n\n"
        "**(b) Prospective validation.** Same framework: IRB-approved protocol with PHI use governed by the BAA. If consent is required (depending on the prospective intervention component), individual consent or expedited IRB waiver. The prospective deployment fundamentally changes the framing: it is operational deployment, not pure research, and the IRB's authority may be limited.\n\n"
        "**(c) External licensing.** A separate analysis. If the model is licensed to other health systems and applied to *their* patients, those patients' data flows are governed by the receiving institution's BAAs, not Helios's. But the model itself has been *trained* on Helios PHI, and the question 'does deploying a Helios-trained model elsewhere constitute a disclosure of derivatives of Helios patients' data?' is unresolved in the literature. The committee should ask the privacy office to weigh in explicitly.\n\n"
        "**State law layers.** Massachusetts has a baseline health-data privacy law plus the strict standards built into 201 CMR 17. Vermont, NH, CT, and RI each layer additional consumer-health-data protections; the most restrictive state's framework typically governs for patients from that state. **GDPR applies** to the EU patients (4% of cohort): a separate consent or legal basis is required, and individual rights (access, deletion, portability) extend further than HIPAA permits. Don't conflate the EU patients' framework with the rest.\n\n"
        "**DUA and BAA must-haves.** Vendor data-use limitation (the 'learnings' clause restructured). Subgroup performance reporting cadence (Track 04 question). Model update notification with revalidation requirement. Termination and data deletion. Audit rights. Subcontractor flow-down."
    )

    reveal(step2_widget.value, ideal_2, learner_label="Your legal-pathway analysis")
    return (ideal_2,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Step 3 of 5: Ethical analysis

        Apply Track 03's five-dimensional framework: consent-expectation fit, public vs commercial benefit, equity, transparency, reversibility. Locate Project Helios on each one. Where are the highest-risk dimensions, and what would lower the risk?
        """
    )
    return


@app.cell
def _(commit_text, mo):
    step3_widget, step3_ready = commit_text(
        "Your ethical analysis across the five dimensions",
        min_chars=150,
    )
    step3_widget
    return step3_ready, step3_widget


@app.cell
def _(mo, reveal, step3_ready, step3_widget):
    mo.stop(
        not step3_ready(),
        mo.callout(
            mo.md("_Write your five-dimension analysis above. The reveal opens at 150 characters._"),
            kind="neutral",
        ),
    )

    ideal_3 = (
        "**Five dimensions, applied.**\n\n"
        "**1. Consent-expectation fit: LOW.** Patients admitted to Helios for inpatient care would reasonably expect their data to be used for internal QI and for academic research. The vendor-partnership and especially the external-licensing dimensions exceed what a reasonable patient would have envisioned. The IRB waiver of authorization is the legal cover, but the expectation gap is real. This is the Project Nightingale + Henrietta Lacks combination: data leaving the institution for commercial development that the patients did not envision.\n\n"
        "**2. Public vs commercial benefit: MIXED, trending commercial.** Internal deployment serves Helios patients (public/clinical benefit). The external licensing is commercial (Helios + vendor revenue, with downstream patients at other health systems as eventual beneficiaries through deployed tools). The honest framing names both. The 'learnings clause' in the vendor contract tilts the balance further toward commercial.\n\n"
        "**3. Equity: SUBSTANTIAL CONCERNS.** This is the most serious dimension. The AMC catchment is predominantly insured; Helios West is 50% Medicaid and predominantly Hispanic; Helios North is rural and predominantly white; Helios South is mixed. A model trained on the combined data will inherit the spending and care-pattern differences across these populations (Obermeyer label-bias risk). If deployed across the four sites without subgroup-stratified validation, it may systematically underperform on Medicaid patients or on the Hispanic catchment. External licensing extends this concern to *any* institution that deploys the model, including safety-net hospitals whose patient mix may differ further from any of the four training sites.\n\n"
        "**4. Transparency: INADEQUATE as proposed.** Patients have not been individually informed (waiver of authorization). Institutional disclosure is at the level of the Notice of Privacy Practices. There is no plan for patient-level or community-level disclosure of the vendor partnership or the external-licensing strategy. The Project Nightingale failure mode is live here.\n\n"
        "**5. Reversibility: VERY LOW.** Once the model is trained on five years of PHI, the model retains derived insights even if the training data is later destroyed. Once licensed externally, the model is in the hands of other institutions and cannot be recalled. Individual patients cannot withdraw their contribution.\n\n"
        "**What lowers the risk.** Reframe the 'learnings' clause to prohibit vendor cross-use without explicit Helios approval. Add explicit patient-facing transparency (a public listing of vendor partnerships; population-level notice through the patient portal). Build a Patient Advisory Council voice into the governance decision. Carve out external licensing as a separate decision requiring its own governance review rather than being baked into the initial vendor agreement."
    )

    reveal(step3_widget.value, ideal_3, learner_label="Your ethical analysis")
    return (ideal_3,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Step 4 of 5: Equity review

        Apply Track 04. Where in the pipeline does bias enter for this project? What needs to be measured before deployment, and what needs to be monitored after? What's the appropriate fairness criterion given the use case, and why?
        """
    )
    return


@app.cell
def _(commit_text, mo):
    step4_widget, step4_ready = commit_text(
        "Your equity review",
        min_chars=150,
    )
    step4_widget
    return step4_ready, step4_widget


@app.cell
def _(mo, reveal, step4_ready, step4_widget):
    mo.stop(
        not step4_ready(),
        mo.callout(
            mo.md("_Write your equity review above. The reveal opens at 150 characters._"),
            kind="neutral",
        ),
    )

    ideal_4 = (
        "**Five entry points for bias in Project Helios.**\n\n"
        "**1. Training data.** The four sites have very different demographics. If the training data is dominated by AMC patients (likely, given the 720-bed center is the largest by volume), the model is at risk of underperforming at Helios West (50% Medicaid, predominantly Hispanic) and Helios North (rural). Validation must be stratified *by site*, not just on the pooled data. Pooled AUC will hide site-specific failures.\n\n"
        "**2. Labels.** What outcome is the model predicting? The proposal says 'early sepsis,' but the operational label is likely 'sepsis billing code applied during the encounter' or 'ICU transfer with a sepsis bundle activation.' Both labels have the Obermeyer structure: they reflect the care patterns of the site, not pure biological deterioration. Medicaid patients may be transferred to the ICU at different rates than commercially-insured patients for similar severity. The label inherits that disparity. The honest committee question: 'what proxy is the label, and is the proxy biased by site or by insurance?'\n\n"
        "**3. Features.** Standard inpatient features (vitals, labs, medications, demographics) include several that correlate with race, insurance, and site. Even without 'race' as a feature, ZIP code, primary language, and primary care provider all encode race indirectly. Most concerning: any feature that itself reflects different care patterns (e.g., 'frequency of vital signs check') may encode the institution's differential attention to patients.\n\n"
        "**4. Deployment context.** Trained on multi-site data, deployed at four sites with different patient populations, eventually deployed at *other* institutions through licensing. Each new deployment is a new population the model wasn't validated on. The licensing strategy especially: a Helios-trained model deployed at a 100% Medicaid safety-net hospital may perform very differently than the validation suggested.\n\n"
        "**5. Feedback loops.** Once deployed, the model's alerts trigger interventions. Patients who would have deteriorated without intervention now don't. On retraining, the predictive signal weakens in the populations where the alerts were acted on. If the alerts are *differentially acted on* by site (more responsive teams at the AMC, less so at the rural site), the feedback loop concentrates predictive accuracy at the AMC and degrades it elsewhere.\n\n"
        "**What needs to be measured pre-deployment.** Sensitivity, specificity, PPV, calibration *stratified by*: site, race, ethnicity, primary language, insurance class, and age band. Pooled metrics are insufficient. Any subgroup where performance is meaningfully worse needs an explicit decision: deploy anyway with monitoring, fix the model, or exclude that subgroup.\n\n"
        "**What needs to be monitored post-deployment.** Same stratified metrics, on a regular cadence (monthly is reasonable; quarterly is the minimum). Alert rate and alert outcome by subgroup. Drift detection (the model's performance over time). Critically, a documented trigger for what *halts deployment*: if subgroup performance drops below a threshold, what happens? Who decides?\n\n"
        "**Appropriate fairness criterion.** For an early-warning alert intended to *catch deteriorating patients*, the primary fairness criterion is **equal opportunity** (equal sensitivity across groups). Missing deteriorating patients is the dominant harm; equalizing the miss rate across subgroups should be the operational target. Predictive parity (equal PPV) is the wrong primary target here because it would allow the model to have lower sensitivity on a subgroup as long as the PPV is preserved. The committee should name this choice explicitly and document the trade-off (per Kleinberg, you cannot simultaneously equalize FPR and PPV when base rates differ)."
    )

    reveal(step4_widget.value, ideal_4, learner_label="Your equity review")
    return (ideal_4,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Step 5 of 5: Governance routing

        Apply Track 05. Which governance bodies must approve Project Helios? Which decision rights are likely to fall through the gaps? Which "novelty" dimensions need an explicit cross-functional working group, and what's the agenda for that group's first meeting?
        """
    )
    return


@app.cell
def _(commit_text, mo):
    step5_widget, step5_ready = commit_text(
        "Your governance routing",
        min_chars=150,
    )
    step5_widget
    return step5_ready, step5_widget


@app.cell
def _(mo, reveal, step5_ready, step5_widget):
    mo.stop(
        not step5_ready(),
        mo.callout(
            mo.md("_Write your governance routing above. The reveal opens at 150 characters._"),
            kind="neutral",
        ),
    )

    ideal_5 = (
        "**Bodies that must approve, with the question each owns.**\n\n"
        "- **IRB.** The research dimension of the retrospective training set and the prospective validation. Waiver of authorization criteria. Plans for vulnerable populations (Medicaid, non-English-speaking, rural).\n"
        "- **Privacy office.** HIPAA pathway selection for each phase. State-law harmonization (MA, VT, NH, CT, RI). GDPR applicability for the EU patients. Audit trail requirements.\n"
        "- **Compliance.** Anti-kickback and Stark implications of the licensing arrangement. Whether the vendor payment structure creates regulatory exposure.\n"
        "- **Data governance committee.** Who at Helios can access the cross-site data; whether the data extract leaves the institution; what stewardship the source-system stewards retain.\n"
        "- **AI/ML governance committee.** Pre-deployment subgroup performance reporting. Post-deployment monitoring plan. Trigger criteria for halting deployment. Subgroup performance reporting cadence written into the vendor contract.\n"
        "- **Vendor management + legal.** The full contract review. The 'learnings clause' carve-out. Termination and offboarding. Liability and indemnification. Audit rights.\n"
        "- **Clinical informatics steering (CMIO).** EHR integration. Alert workflow design. Alert fatigue prevention. Communication-to-end-users plan.\n"
        "- **Security / CISO.** Data flows to the vendor, encryption, logging, monitoring. Vendor security posture. Breach response.\n\n"
        "**Likely decision-right gaps.**\n\n"
        "- **Equity review.** As currently constituted, the AI/ML governance committee at most institutions is weak on stratified-performance enforcement. **Explicitly name who runs the subgroup analyses, on what cadence, with what triggers for action.** Without this, the equity work is performed in good faith and then has no ongoing owner.\n"
        "- **Patient/community disclosure.** No standing committee owns 'should patients be told about this vendor partnership and external-licensing strategy?' This is the Project Nightingale gap. Propose an explicit transparency decision: institutional public statement, individual patient notice through the portal, or both.\n"
        "- **External licensing.** The proposal bundles internal deployment and external licensing into one approval. **Recommend separating them.** Approve internal deployment with subgroup monitoring; defer external licensing pending evidence of subgroup performance at the four Helios sites. The licensing decision involves different ethical considerations and should have its own review.\n"
        "- **Novelty review.** Project Helios is new-in-kind for this institution in at least three ways: first multi-site AI deployment, first vendor partnership at this scale, first external licensing of a Helios-trained model. **Propose a cross-functional working group** with a written charter and a sunset date, co-chaired by the CMIO and an external bioethicist, with a Patient Advisory Council voting member, charged with the questions the standing committees won't own.\n\n"
        "**Agenda for the working group's first meeting.**\n"
        "1. Restructure the vendor 'learnings' clause; document the change.\n"
        "2. Pre-specify subgroup performance reporting cadence (monthly), thresholds, and halting criteria; write into BAA + MSA.\n"
        "3. Patient-facing transparency: scope (institutional statement, individual notice, ongoing reporting), drafting timeline, who approves.\n"
        "4. Separate the external-licensing decision from the internal-deployment decision; defer external licensing pending 18 months of post-deployment subgroup monitoring.\n"
        "5. Recruit a Patient Advisory Council member with voting rights; orient them; brief them on the materials.\n"
        "6. Schedule the standing committees' reviews in parallel, not serially; identify decision-rights gaps before the standing reviews start."
    )

    reveal(step5_widget.value, ideal_5, learner_label="Your governance routing")
    return (ideal_5,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Synthesis: assemble the committee memo

        Below is the committee memo, auto-assembled from your written answers. Read it as a draft of what you would actually circulate to the governance committee. Edit it in the box at the bottom into the final version you would send.
        """
    )
    return


@app.cell
def _(mo, step1_widget, step2_widget, step3_widget, step4_widget, step5_widget):
    memo = (
        "## Committee memo: Project Helios review\n\n"
        "**Reviewer:** Clinical informatics representative (you).\n\n"
        "**Project:** AI-based early-sepsis prediction tool, multi-site EHR data, vendor partnership, eventual external licensing.\n\n"
        "**Summary recommendation:** *Approve with conditions* on internal deployment; *defer* external licensing pending evidence; require structural changes to the vendor contract and an explicit patient-transparency commitment.\n\n"
        "---\n\n"
        "### 1. Privacy threat model\n\n"
        f"{step1_widget.value or '_[your Step 1 writing]_'}\n\n"
        "### 2. Legal pathway\n\n"
        f"{step2_widget.value or '_[your Step 2 writing]_'}\n\n"
        "### 3. Ethical analysis (five-dimensional framework)\n\n"
        f"{step3_widget.value or '_[your Step 3 writing]_'}\n\n"
        "### 4. Equity review\n\n"
        f"{step4_widget.value or '_[your Step 4 writing]_'}\n\n"
        "### 5. Governance routing\n\n"
        f"{step5_widget.value or '_[your Step 5 writing]_'}\n\n"
        "---\n\n"
        "### Recommendation in detail\n\n"
        "- **Approve internal deployment** at the four Helios sites, *conditional on*:\n"
        "  - Pre-specified subgroup performance reporting (site, race, ethnicity, primary language, insurance class) before any clinical deployment.\n"
        "  - Restructured vendor contract: the 'learnings clause' carved out; subgroup performance reporting cadence and halting thresholds written in.\n"
        "  - Patient-facing transparency commitment: institutional public statement of the vendor partnership and the analytics use of clinical data, plus the option for individual notice through the portal.\n"
        "  - Post-deployment monitoring plan with monthly stratified-metric reporting and a documented halting trigger.\n\n"
        "- **Defer external licensing** as a separate decision requiring its own governance review after at least 18 months of post-deployment subgroup monitoring at the four Helios sites.\n\n"
        "- **Convene a cross-functional novelty working group** co-chaired by the CMIO and an external bioethicist, with Patient Advisory Council voting representation, charted with the cross-cutting questions the standing committees do not own.\n\n"
        "---\n\n"
        "*Ready to send to the committee. Edit in the box below if you want to revise the recommendation language.*"
    )

    memo_view = mo.md(memo)
    memo_view
    return (memo,)


@app.cell
def _(memo, mo):
    final_memo = mo.ui.text_area(
        label="Final memo (edit as needed)",
        value=memo,
        rows=24,
        full_width=True,
    )
    final_memo
    return (final_memo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Reflection

        What in this review most surprised you, or most challenged your prior intuition about how clinical AI projects should be governed? There is no answer key. The reflection is the work.
        """
    )
    return


@app.cell
def _(reflection):
    _reflection_widget, reflection_layout = reflection(
        "Your reflection on the Project Helios review.",
    )
    reflection_layout
    return (reflection_layout,)


@app.cell
def _(go_deeper, mo):
    closing = mo.vstack(
        [
            mo.md(
                r"""
                ---

                ## What this leaves you

                The five-track framework of this course is now in your hands, applied to a concrete proposal:

                1. **Threat model** for privacy (Track 01).
                2. **Legal pathway** under HIPAA and adjacent layers (Track 02).
                3. **Ethical analysis** across the five dimensions (Track 03).
                4. **Equity review** across the five entry points of bias (Track 04).
                5. **Governance routing** with explicit attention to decision-right gaps (Track 05).

                The committee memo above is the artifact this course was preparing you to produce. The course's job is done with you when you can write that memo for a project on your own institution's docket.

                The cross-references continue. Course 04 (clinical epidemiology) gives you the language of bias and validity that the equity review depends on. Course 06 (FHIR) and course 07 (SQL/OMOP) give you the data infrastructure the privacy threat model rides on. Course 09 (AI in medicine) goes deeper on the fairness mechanics that Track 04 sketched. Course 12 (clinical decision support) walks the deployment-context work that Track 05 set up. Course 14 (interoperability policy) closes the loop on the federal-policy frame that HIPAA fits inside.
                """
            ),
            go_deeper(
                "If you write this memo for a real project on your institution's docket, you have done the work this course was designed to prepare you for. The framework is the contribution; the writing is the proof you can apply it."
            ),
        ]
    )
    closing
    return (closing,)


if __name__ == "__main__":
    app.run()
