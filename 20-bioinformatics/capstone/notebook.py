"""Capstone for course 20: Design a precision medicine program.

A six-step Socratic exercise that closes the curriculum. The reader is
the clinical informaticist on the design team for a health system that
is launching a precision-medicine program (pharmacogenomic testing at
the point of prescribing for a defined high-risk-medication list). Each
step is a commit-then-reveal that ties to specific prior courses.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    # Socratic helpers inlined per the WASM rule against shared.X imports.
    def commit_text(prompt, min_chars=40):
        widget = mo.ui.text_area(
            label=prompt,
            rows=6,
            full_width=True,
            placeholder="Take a few sentences. The reveal will not unlock until you do.",
        )

        def ready():
            value = widget.value or ""
            return len(value.strip()) >= min_chars

        return widget, ready

    def reveal(learner_value, ideal_answer, learner_label="Your answer"):
        learner_display = learner_value if learner_value else "_(no answer yet)_"
        return mo.hstack(
            [
                mo.callout(
                    mo.vstack(
                        [
                            mo.md(f"**{learner_label}**"),
                            mo.md(str(learner_display)),
                        ]
                    ),
                    kind="neutral",
                ),
                mo.callout(
                    mo.vstack(
                        [
                            mo.md("**How we would think through this**"),
                            mo.md(ideal_answer),
                        ]
                    ),
                    kind="success",
                ),
            ],
            widths="equal",
        )

    def reflection(prompt, placeholder=""):
        widget = mo.ui.text_area(
            label=prompt,
            rows=5,
            full_width=True,
            placeholder=placeholder or "Take a few sentences. No reveal here. The reflection is the work.",
        )
        layout = mo.vstack(
            [
                widget,
                mo.callout(
                    mo.md("_There is no answer key for this one. The point is to make your reasoning explicit to yourself._"),
                    kind="neutral",
                ),
            ]
        )
        return widget, layout

    return commit_text, mo, reflection, reveal


@app.cell
def _(mo):
    mo.md(
        r"""
        # Capstone: Design a precision medicine program

        ## The scenario

        Your health system (a mid-sized academic medical center with five affiliated community hospitals and a large outpatient network) is launching a precision-medicine program. The first phase is pre-emptive pharmacogenomic testing for a defined list of high-risk drug-gene pairs: TPMT before azathioprine, CYP2C19 before clopidogrel, HLA-B*5701 before abacavir, HLA-B*5801 before allopurinol (in East Asian ancestry patients), CYP2D6 for codeine and other CYP2D6-substrate analgesics. The program would offer testing at primary-care registration for opt-in patients; results would be stored as structured data in the EHR and surfaced through CDS Hooks alerts at relevant order-entry moments.

        You are the clinical informaticist on the design team. The six steps below walk the six dimensions every real precision-medicine-program design has to address. Commit an answer to each before the reveal unlocks.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Step 1: Infrastructure (Course 00 + Course 05)

        What institutional and federal infrastructure does the program require? Name the systems on the institutional side (EHR, LIS, CDW, secure enclave, genomics core) and the federal-side resources the program will consult (NCBI, ClinVar, CPIC).
        """
    )
    return


@app.cell
def _(commit_text):
    step1_widget, step1_ready = commit_text("Name the infrastructure pieces on each side and how they connect.")
    step1_widget
    return step1_ready, step1_widget


@app.cell
def _(mo, reveal, step1_ready, step1_widget):
    mo.stop(not step1_ready(), mo.md("_Write a few sentences above to unlock the reveal._"))
    reveal(
        step1_widget.value,
        """
        **Institutional infrastructure required.**

        - **EHR with structured genomic-result storage.** The Genomic Implication / Variant Observations from the HL7 FHIR Genomics IG should land as structured fields, not as PDFs. Course 03 Track 03 covered the PDF-vs-structured-field gap; the program's success depends on closing it for the pharmacogenomic results.
        - **LIS at the institutional genomics lab.** Performs the actual testing. May be in-house or contracted (Course 05). The LIS-to-EHR interface is the canonical handoff.
        - **CDS Hooks service.** Listens at the order-select hook for the covered medications, checks the patient's structured pharmacogenomic result, returns a card if the result requires action. The CDS Hooks pattern is from Course 12 Track 03.
        - **CDW for monitoring.** Captures the alert volume, the override rate, the action-taken rate per drug-gene pair. The CDW is the substrate for the post-deployment evaluation Course 12 Track 04 covered.

        **Federal-layer resources consulted.**

        - **CPIC guidelines.** The clinical evidence base for each drug-gene pair. The guidelines specify the actionable phenotypes and the recommended actions.
        - **ClinVar.** Consulted for the variant-classification side (which CYP2C19 alleles are loss-of-function, which are normal).
        - **PharmGKB.** Companion resource to CPIC; consulted for the underlying evidence and the allele definitions.

        The program's architecture is the standards-based delivery layer (CDS Hooks) running over the institutional structured-genomic-result storage (HL7 Genomics IG), consulting the federal evidence base (CPIC). The clinical informaticist's job is to operationalize this stack inside the institution's existing infrastructure.
        """,
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Step 2: Standards (Track 02 + Course 06)

        Which standards apply to the program's data flow? Name the standard that governs the variant representation, the standard that governs the structured genomic report in the EHR, and the standard the CDS rule itself is written in.
        """
    )
    return


@app.cell
def _(commit_text):
    step2_widget, step2_ready = commit_text("Name the standards and where each applies.")
    step2_widget
    return step2_ready, step2_widget


@app.cell
def _(mo, reveal, step2_ready, step2_widget):
    mo.stop(not step2_ready(), mo.md("_Write a few sentences above to unlock the reveal._"))
    reveal(
        step2_widget.value,
        """
        Four standards govern the data flow.

        - **GA4GH Variation Representation Specification (VRS)** governs how the variant itself is represented at the data level. The VRS canonical identifier is the clean key for variant interoperability across institutions.
        - **HL7 FHIR Genomics Reporting Implementation Guide** governs the structured genomic report in the EHR. The Variant Observation profile is the FHIR shape the pharmacogenomic result is stored under; the DiagnosticReport profile is the report header.
        - **CPIC standardized phenotype terms** govern the actionable phenotype representation. Each drug-gene pair has a defined set of phenotypes (e.g., for CYP2C19: poor metabolizer, intermediate metabolizer, normal metabolizer, rapid metabolizer, ultra-rapid metabolizer). The phenotype, not the raw allele, is what the CDS rule operates on.
        - **CDS Hooks** governs the delivery-layer protocol. The order-select hook fires when the medication is selected; the CDS service receives the order and the patient's pharmacogenomic phenotype; the response is a Card per CDS Hooks specification.

        Beneath these four sit the foundational standards: FHIR R4 (the resource layer the Genomics IG profiles), LOINC (the codes for the Observation types), RxNorm (the codes for the medications). The combination is the standards stack the program depends on. A program that does not commit to this stack will be re-implementing it institution by institution.
        """,
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Step 3: Returns to patients (Track 03)

        How does the patient receive the result? Consider three sub-questions: when in the testing workflow does the patient learn the test was performed, how is the result delivered to them, and what happens when the result later changes a prescribing decision.
        """
    )
    return


@app.cell
def _(commit_text):
    step3_widget, step3_ready = commit_text("How do results flow back to the patient?")
    step3_widget
    return step3_ready, step3_widget


@app.cell
def _(mo, reveal, step3_ready, step3_widget):
    mo.stop(not step3_ready(), mo.md("_Write a few sentences above to unlock the reveal._"))
    reveal(
        step3_widget.value,
        """
        Three sub-questions and their published-pattern answers.

        **When does the patient learn the test was performed?** At the point of consent. The opt-in conversation at primary-care registration documents what the test covers (the drug-gene pairs in scope, the actionable phenotypes), what will be done with the result (stored in the EHR, queried at relevant prescribing moments), and what will not be done with the result (no incidental-findings reporting, no ancestry estimation, no future-condition predictions beyond the scope of pharmacogenomic CDS). The published consent should be at approximately a 6th-to-8th-grade reading level; PEN-13 or similar instruments can verify.

        **How is the result delivered?** Two layers. (1) A patient-portal message at the time of result, with an attached one-page plain-language summary explaining what was tested, what the result means, and what to do with the result. (2) The structured result lands in the EHR and is queryable by any clinician with patient-record access; future clinicians do not need to wait for the patient to disclose the result.

        **What happens when the result later changes a prescribing decision?** The CDS Hooks card that fires at order-select is also the moment the patient is informed of the decision. The clinician explaining a dose change or an alternative drug now has a documented genomic basis for the conversation. The CDS card's source attribution provides the published evidence the clinician can share with the patient.

        Two additional design choices the program has to make explicitly. First, whether to support patient access to the underlying raw data (the VCF). Most institutions decline; the operational reason is that the raw data is much larger than the actionable result and requires bioinformatics interpretation. Second, whether to support patient transfer of the result to other institutions. The FHIR Bulk Data Access and the FHIR Genomics IG together support this; the institution should commit to the patient-mediated transfer pathway as a default.
        """,
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Step 4: Research-clinical coexistence (Track 04)

        The clinical program will generate substantial data. Some of that data will be valuable for research. How does the program design support legitimate research use without compromising the clinical program's primary purpose?
        """
    )
    return


@app.cell
def _(commit_text):
    step4_widget, step4_ready = commit_text("How do the clinical and research data streams coexist?")
    step4_widget
    return step4_ready, step4_widget


@app.cell
def _(mo, reveal, step4_ready, step4_widget):
    mo.stop(not step4_ready(), mo.md("_Write a few sentences above to unlock the reveal._"))
    reveal(
        step4_widget.value,
        """
        Three operational decisions shape research-clinical coexistence.

        **Tiered consent at enrollment.** The pharmacogenomic-testing consent should distinguish the clinical use (always opt-in) from the research use (separately opt-in). A patient who agrees to pharmacogenomic testing for their own care should not be presumed to agree to their data being used in research; the research consent is a separate decision. The published consent frameworks at MyCode (Geisinger), the All of Us program, and the eMERGE consortium each handle this in slightly different ways; the program should pick one and commit to it.

        **Honest-broker mediation between the streams.** The clinical data sits in the EHR (Reyes's name, MRN, structured pharmacogenomic results, encounters). The research data sits in the institutional research enclave with a research-specific identifier. The honest-broker service mediates the linkage between the two; researchers see the research identifier and (if their study allows) selected clinical phenotype features pulled through the broker, but do not see the patient's name or MRN. The pattern is the canonical institutional design Course 03 introduced abstractly and Track 04 of this course addressed concretely.

        **Aggregation thresholds for de-identified results.** Some research questions (population-level pharmacogenomic prevalence; allele-frequency reporting) can be answered from de-identified aggregated data without individual-patient linkage. The program should set an aggregation threshold (typically k >= 11 small-cell suppression per HHS de-identification guidance) and provide a public-facing aggregated data resource for questions answerable at the aggregate level.

        The principle behind all three decisions is that the clinical program owns the data primarily; research access is a secondary use governed by consent, by the honest-broker pattern, and by aggregation discipline. A program that does not separate the two streams cleanly risks both inappropriate research use and erosion of the clinical-program participants' trust.
        """,
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Step 5: Governance (Course 03 + Course 12)

        What governance is required at the institutional level? Name the committees and the documented processes the program has to have in place before it can deploy.
        """
    )
    return


@app.cell
def _(commit_text):
    step5_widget, step5_ready = commit_text("Name the governance bodies and the processes.")
    step5_widget
    return step5_ready, step5_widget


@app.cell
def _(mo, reveal, step5_ready, step5_widget):
    mo.stop(not step5_ready(), mo.md("_Write a few sentences above to unlock the reveal._"))
    reveal(
        step5_widget.value,
        """
        Five governance bodies and their processes apply.

        **CDS governance committee** (introduced in Course 12 Track 05) approves the specific CDS Hooks alerts that will be deployed for each drug-gene pair. Reviews the alert logic, the threshold, the suggested action, the override-rate target. Approves the retirement criteria for any alert whose override rate exceeds the threshold for sustained periods.

        **Pharmacy & Therapeutics committee** approves the drug-gene pairs in scope and the recommended actions. P&T is the clinical-content authority; their sign-off is what makes the CDS recommendations clinically defensible.

        **Institutional Review Board** is involved if any research use of the data is in scope. For the clinical program alone (no research use), the IRB may not need to formally approve, but most institutions will require an IRB-of-record review of the consent process and the data-handling plan. For the research-consent-and-honest-broker pieces of step 4, IRB approval is required.

        **Genomic Medicine Governance Committee** (sometimes called Personalized Medicine Steering Committee, Precision Medicine Governance) is the body specifically responsible for the precision-medicine program. Meets periodically to review the program's metrics, decide on expansion to new drug-gene pairs, and address novel-finding incidental questions.

        **Equity oversight** (introduced in Course 12 Track 05 and reinforced by Track 05 of this course) is the named institutional process for ongoing review of the program's subgroup performance and equity implications. The named clinical content owner for the program reports subgroup metrics on a defined schedule (typically quarterly or biannually). The reporting frequency should be specified in the program's governance plan.

        The five together are the governance scaffolding. A program that does not have all five in place is operating without one or more required institutional protections.
        """,
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Step 6: Equity (Track 05)

        Name the equity concerns the program has to address before deployment, and the monitoring plan that will catch new equity concerns post-deployment.
        """
    )
    return


@app.cell
def _(commit_text):
    step6_widget, step6_ready = commit_text("What are the equity concerns and how do you monitor them?")
    step6_widget
    return step6_ready, step6_widget


@app.cell
def _(mo, reveal, step6_ready, step6_widget):
    mo.stop(not step6_ready(), mo.md("_Write a few sentences above to unlock the reveal._"))
    reveal(
        step6_widget.value,
        """
        Three equity concerns are load-bearing.

        **Ancestry-dependent allele frequencies and interpretation.** The drug-gene pairs in scope have different actionable-phenotype prevalences across ancestries. HLA-B*5801 is much more common in East Asian patients; CYP2C19 loss-of-function is common across multiple ancestries but at different frequencies; CYP2D6 has dozens of clinically relevant alleles with strongly ancestry-stratified frequencies. The program's CPIC-derived phenotype calling must be ancestry-aware and the structured result must include the ancestry-relevant context.

        **Enrollment equity.** Pre-emptive pharmacogenomic testing is offered at primary-care registration. Patients who do not have a primary-care relationship at the institution (uninsured, underinsured, transient populations) systematically miss enrollment. The program should explicitly include outreach mechanisms to non-primary-care patients (the ED, the safety-net clinic affiliations, the federally qualified health centers in the institution's network) so the testing is not de facto restricted to the patients with the strongest healthcare access.

        **CDS alert equity.** A CDS rule that fires at order-select can have different population-level effects depending on the prevalence of the actionable phenotype and the prevalence of the relevant prescription in different ancestry groups. The program's post-deployment monitoring should include subgroup-stratified alert-fire-rate and action-taken-rate; persistent gaps across subgroups should trigger a review.

        **Monitoring plan structure.** Three monitored quantities per drug-gene pair, reported quarterly:

        - **Subgroup-stratified phenotype prevalence in the tested population**: detects under-testing of subgroups whose published phenotype prevalence is being missed.
        - **Subgroup-stratified alert-fire rate**: detects whether the CDS alert is firing at the expected rate across subgroups.
        - **Subgroup-stratified action-taken rate** (the fraction of alerts where the clinician accepted the suggested action): detects whether clinicians are acting on the alert equally across subgroups.

        Persistent gaps in any of the three trigger an equity review at the Genomic Medicine Governance Committee. The program retires any alert that the equity review cannot resolve.
        """,
    )
    return


@app.cell
def _(mo, reflection):
    refl_widget, refl_layout = reflection(
        "Reflection: which of the six dimensions feels most uncertain to you for a real institution to commit to? What would resolve the uncertainty?",
        placeholder="Think about your institution (or a real one you know) and what would actually be hard to commit to.",
    )
    refl_layout
    _ = refl_widget
    return refl_layout, refl_widget


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            ### Go deeper

            The CPIC Clinical Pharmacogenetics Implementation Consortium guidelines (track 03 go-deeper) are the clinical-evidence foundation for the program. The HL7 FHIR Genomics Reporting Implementation Guide (track 03 go-deeper) is the standards-based representation. The MyCode publications (Geisinger, references in the track 05 go-deeper) are the longest-running real-world example of pre-emptive pharmacogenomic testing at scale. The All of Us program documentation (track 05 go-deeper) provides the patient-consent and return-of-results reference patterns. Each is linked from the corresponding track's go-deeper.
            """
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The curriculum closes here

        This is the last capstone in the curriculum.

        Across 21 courses (00 through 20, with the gap-fill courses 16 through 20 added in the later phases), the curriculum has built up a clinical informaticist's working vocabulary from first principles. The reader who has worked through all of it can sit in a CDS governance committee meeting, in a precision-medicine-program design meeting, in a vendor-evaluation review, in a research-data-use-committee meeting, and in a leadership conversation about an EHR-and-bioinformatics integration as a credible clinical informaticist.

        The journey from Course 00's data-information-knowledge-wisdom orientation through Course 12's seven-step CDS-design grand-finale through this six-step precision-medicine-program capstone is the curriculum's complete arc. The reader who finished is the audience the curriculum was built for.

        Welcome to the field.
        """
    )
    return


if __name__ == "__main__":
    app.run()
