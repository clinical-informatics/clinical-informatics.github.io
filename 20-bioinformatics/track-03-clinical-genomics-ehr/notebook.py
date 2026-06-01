"""Track 03: Clinical genomics in the EHR.

The clinical-genomics loop has four parts: order, lab processing,
report, display. The track presents the standards that govern each
(HL7 Genomics Reporting IG, GA4GH variant representation, ACMG 79-
gene list), the canonical pharmacogenomic examples (TPMT, CYP2C19,
HLA-B*5701), and the PDF-vs-structured-field gap on Reyes's
HLA-DRB1*04:01 result.
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
        "06": "Learn FHIR",
        "07": "Data wrangling and engineering",
        "10": "NLP and clinical text",
        "12": "Clinical decision support",
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
        # Track 03: Clinical genomics in the EHR

        ## The clinical-genomics loop

        Clinical genomics in the EHR has four parts. The clinician places the test order. The laboratory processes the specimen and runs the bioinformatics pipeline that Track 02 covered. The lab returns a structured report to the EHR. The clinician reads the report at a workflow moment.

        The four parts together are the loop the rest of this course addresses. The first and fourth parts (order, display) are clinical-informatics territory. The second part (lab processing) is bioinformatics territory. The third part (report delivery) is the handoff between the two and is where most of the standards-development work happens. This track addresses the third and fourth parts (report, display).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The standards: HL7 FHIR Genomics Reporting IG

        The HL7 FHIR Genomics Reporting Implementation Guide is the standards-based answer to "how should a clinical lab return a structured genomic test result to an EHR." The IG specifies the FHIR resources, the profiles those resources should conform to, and the relationships between them.

        Three resource types are load-bearing.

        - **DiagnosticReport (the report header).** Identifies the test that was performed, the requesting clinician, the date, the laboratory, the overall conclusion. One DiagnosticReport per test.
        - **Observation (the individual finding).** One Observation per individual variant, per allele call, per quantitative measurement. The Genomics IG defines specific Observation profiles (Genomic Implication, Variant, Diagnostic Implication) that constrain Observation to carry the genomic-specific fields.
        - **MolecularSequence (the raw or interpreted sequence).** Less commonly used in clinical reporting; primarily used when the sequence data itself is part of the report (rare in clinical practice; common in research).

        The IG also defines the Genomics Operation `$find-subject-variants` for querying a FHIR genomic store for a specific variant or gene across all patients, and the `$find-population-statistics` operation for cohort-level queries. The operations are the standards-based answer to "how does a CDS service or a research query find all patients with a variant of interest."
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### A representative Variant Observation (HL7 Genomics IG profile)

        ```json
        {
          "resourceType": "Observation",
          "meta": {
            "profile": ["http://hl7.org/fhir/uv/genomics-reporting/StructureDefinition/variant"]
          },
          "status": "final",
          "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "laboratory"}]}],
          "code": {"coding": [{"system": "http://loinc.org", "code": "69548-6", "display": "Genetic variant assessment"}]},
          "subject": {"reference": "Patient/ER-001"},
          "valueCodeableConcept": {"coding": [{"system": "http://loinc.org", "code": "LA9633-4", "display": "Present"}]},
          "component": [
            {
              "code": {"coding": [{"system": "http://loinc.org", "code": "48018-6", "display": "Gene studied"}]},
              "valueCodeableConcept": {"coding": [{"system": "http://www.genenames.org/geneId", "code": "HGNC:4948", "display": "HLA-DRB1"}]}
            },
            {
              "code": {"coding": [{"system": "http://loinc.org", "code": "48005-3", "display": "Amino acid change (pHGVS)"}]},
              "valueCodeableConcept": {"coding": [{"system": "http://varnomen.hgvs.org", "code": "p.QKRAA", "display": "HLA-DRB1*04:01 shared epitope"}]}
            }
          ]
        }
        ```

        Reading top-to-bottom: a final-status, laboratory-category Observation conforming to the Genomics IG Variant profile, on patient ER-001 (Ms. Reyes), with a finding of "present." The component array carries the structured details: the gene studied is HLA-DRB1 (with the HGNC gene identifier), and the amino-acid change is the QKRAA motif (the shared epitope).

        This is the structured representation Ms. Reyes's HLA-DRB1*04:01 result should have. In most US institutions today it does not. The actual EHR record is a PDF attached to a generic "HLA typing" result entry, with the structured fields containing only the test name and the order metadata. The gap between the structured representation above and the PDF reality is what this track keeps coming back to.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The standards: GA4GH variant representation

        Underneath the FHIR Genomics IG sits the GA4GH (Global Alliance for Genomics and Health) Variation Representation Specification (VRS). VRS specifies how a genomic variant is represented unambiguously at the data level: which reference genome, which position, which reference allele, which alternate allele, with what coordinate system.

        Three properties of VRS are load-bearing for clinical-genomics interoperability.

        - **Sequence identifiers are content-addressable.** A reference sequence is identified by a hash of its content (SHA-512 truncated to a defined length), not by an arbitrary name. Two laboratories reporting against the same reference will produce identical sequence identifiers; differences in the sequence identifier are a guaranteed signal of a real reference difference.
        - **Variants have a canonical identifier.** Each unique variant has a single canonical VRS identifier (a hash of the variant's normalized representation). Two laboratories reporting the same variant will produce the same VRS identifier. The identifier is the clean key for variant interoperability.
        - **Standards stack.** FHIR Genomics IG uses VRS as its variant-representation layer. ClinVar uses VRS. The HGVS variant-naming standard (which most clinical reports use for human-readable variant names) is being aligned with VRS. The convergence is recent and ongoing; the clinical informaticist working in this space should expect the standards to keep moving over the next several years.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The ACMG 79-gene incidental findings list

        Clinical exome or whole-genome sequencing for a specific indication will often incidentally identify variants in genes unrelated to the indication. Some of those variants are clinically actionable (a BRCA1 pathogenic variant identified during exome sequencing for a developmental disorder). The American College of Medical Genetics and Genomics maintains a list of genes for which a pathogenic or likely-pathogenic variant identified incidentally should be reported back to the patient.

        The list has grown from 56 genes in the 2013 first edition (ACMG SF 1.0) through several revisions to the current 79-gene version (ACMG SF 3.2, with periodic updates). The genes cover three substantive categories: hereditary cancer predisposition (BRCA1, BRCA2, TP53, MLH1, others), cardiovascular conditions (KCNQ1, KCNH2, MYH7, others), and metabolic conditions (LDLR for familial hypercholesterolemia, others).

        Three operational properties of the ACMG 79 are load-bearing for clinical informatics.

        First, the list defines a quasi-floor for clinical exome reporting. A laboratory that does not report ACMG-79 incidental findings is deviating from the published consensus; a clinical informaticist evaluating a vendor laboratory should expect the laboratory to follow the list and should ask about deviations.

        Second, the list creates downstream CDS opportunities. A patient whose chart documents an ACMG-79 incidental finding is a patient for whom additional surveillance, additional family-counseling, or specific medication-avoidance recommendations apply. The HL7 Genomics IG's structured representation is what makes those CDS rules possible at scale.

        Third, the list is conditional on patient consent. The 2021 ACMG update introduced a formal patient-opt-out mechanism; the institution's consent process should give patients the choice to receive or decline incidental findings before the test is ordered. The consent decision propagates downstream and is part of what the EHR should track structurally.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Pharmacogenomics: the canonical clinical-actionable cases

        Pharmacogenomics is the use of genomic information to guide drug selection or dosing. A handful of drug-gene pairs have strong enough evidence and high enough actionability that pre-prescription testing or look-up is recommended by the CPIC (Clinical Pharmacogenetics Implementation Consortium) and is embedded in production CDS at many institutions.
        """
    )
    return


@app.cell
def _(pd):
    pgx_table = pd.DataFrame(
        [
            {
                "Drug-gene pair": "Azathioprine + TPMT",
                "The clinical question": "Does the patient have reduced TPMT activity that would cause life-threatening myelosuppression at standard azathioprine dose?",
                "What the test reveals": "TPMT allele typing or enzyme-activity assay. Approximately 0.3 percent of patients are TPMT-deficient (homozygous variant); approximately 10 percent are intermediate metabolizers (heterozygous).",
                "Action on a positive result": "Avoid azathioprine entirely in TPMT-deficient patients; reduce dose by 30 to 70 percent in intermediate metabolizers.",
            },
            {
                "Drug-gene pair": "Clopidogrel + CYP2C19",
                "The clinical question": "Does the patient have reduced CYP2C19 activity that prevents bioactivation of clopidogrel and reduces its antiplatelet effect?",
                "What the test reveals": "CYP2C19 allele typing. Approximately 30 percent of patients carry a loss-of-function allele (*2 or *3); approximately 2 percent are poor metabolizers.",
                "Action on a positive result": "Use prasugrel or ticagrelor instead of clopidogrel in poor metabolizers (and consider in intermediate metabolizers) after acute coronary syndrome.",
            },
            {
                "Drug-gene pair": "Abacavir + HLA-B*5701",
                "The clinical question": "Does the patient carry HLA-B*5701, which causes a life-threatening hypersensitivity reaction to abacavir?",
                "What the test reveals": "HLA-B typing. Approximately 5 to 8 percent of patients of European or African ancestry carry HLA-B*5701; lower in East Asian ancestry.",
                "Action on a positive result": "Avoid abacavir entirely in HLA-B*5701-positive patients. Testing is mandatory before abacavir initiation per FDA labeling.",
            },
            {
                "Drug-gene pair": "Allopurinol + HLA-B*5801",
                "The clinical question": "Does the patient carry HLA-B*5801, which is strongly associated with allopurinol-induced Stevens-Johnson syndrome and toxic epidermal necrolysis?",
                "What the test reveals": "HLA-B typing. Approximately 10 to 20 percent prevalence in East Asian populations; lower in European-ancestry populations.",
                "Action on a positive result": "Testing recommended before allopurinol initiation in East Asian ancestry patients; alternative urate-lowering therapy if positive.",
            },
            {
                "Drug-gene pair": "Codeine + CYP2D6",
                "The clinical question": "Does the patient have an extreme CYP2D6 metabolizer phenotype (ultra-rapid producing toxic morphine levels, or poor producing no analgesia)?",
                "What the test reveals": "CYP2D6 allele typing. Approximately 1 to 2 percent ultra-rapid; approximately 5 to 10 percent poor metabolizers (variable by ancestry).",
                "Action on a positive result": "Avoid codeine entirely in ultra-rapid metabolizers (especially in children and breastfeeding mothers); use alternative analgesia in poor metabolizers.",
            },
        ]
    )
    pgx_table.index = range(1, len(pgx_table) + 1)
    pgx_table.index.name = "row"
    pgx_table
    return (pgx_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three operational consequences of the pharmacogenomic landscape for the clinical informaticist.

        First, the operational pattern for all five drug-gene pairs is the same: a CDS Hooks order-select alert that fires when the drug is being prescribed, checks the structured pharmacogenomic result in the patient's record, and returns a card with the dose-adjustment recommendation or the alternative-drug suggestion. The pattern is the canonical use case for the CDS Hooks architecture Course 12 Track 3 covered.

        Second, the structured pharmacogenomic result has to be queryable. A PDF result attached to the order does not support the order-select CDS alert. The Genomics IG structured representation does. The CDS pattern depends on the institution closing the PDF-vs-structured-field gap on the pharmacogenomic side.

        Third, the patient-level result is durable. Ms. Reyes's TPMT phenotype does not change over her lifetime; testing once and storing the structured result is sufficient. The same is true for the HLA alleles (HLA-B*5701, HLA-DRB1 shared epitope) and the CYP2D6 / CYP2C19 phenotypes. Pre-emptive pharmacogenomic testing (test once at primary-care registration, store the result, query it on every relevant prescription) is the operational pattern most published pharmacogenomic-CDS deployments use.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The PDF-vs-structured-field gap: Reyes's HLA-DRB1 result

        Ms. Reyes's HLA-DRB1 shared-epitope test result lives in her chart as a PDF report attached to a generic "HLA typing" lab result entry. The structured fields of that result entry contain the test name, the order date, the result date, and the laboratory of origin. They do not contain the alleles (HLA-DRB1*04:01, HLA-DRB1*13:01), the shared-epitope-present-or-absent finding, or the QKRAA-motif amino-acid sequence.

        This is the operational state of clinical genomics at most US institutions in 2025 to 2026. The pattern has three downstream consequences.
        """
    )
    return


@app.cell
def _(pd):
    gap_table = pd.DataFrame(
        [
            {
                "Consequence": "Research queries cannot find the patients with the variant",
                "What that means": "A query for 'find all patients with HLA-DRB1*04:01' returns no rows from the structured EHR. The patients exist; the data is in PDFs that a SQL query cannot read.",
                "Remedy": "An NLP pipeline (Course 10) extracting allele calls from the PDFs is one path. A retrofit data-entry effort to populate the structured fields is another. The FHIR Genomics IG implementation for new test results going forward is the structural answer.",
            },
            {
                "Consequence": "CDS rules cannot fire on the variant",
                "What that means": "A CDS Hooks order-select rule for a drug that depends on HLA-DRB1 status cannot read the patient's HLA result from a PDF. The rule has no input; the rule does not fire.",
                "Remedy": "Same as above. The structured representation is the prerequisite for any CDS rule that depends on the genomic finding.",
            },
            {
                "Consequence": "The patient cannot easily share the result",
                "What that means": "A patient who moves to a different health system or sees a non-affiliated specialist cannot easily transmit the HLA-DRB1 result. The PDF is in the originating EHR; portability requires the patient or a clinician to find and re-upload the PDF.",
                "Remedy": "FHIR Bulk Data Access and the FHIR Genomics IG together support patient-mediated transmission of structured genomic results. The combination is the long-term answer.",
            },
        ]
    )
    gap_table.index = range(1, len(gap_table) + 1)
    gap_table.index.name = "row"
    gap_table
    return (gap_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three operational rules for the clinical informaticist working on closing the PDF gap.

        First, new test results going forward are the leverage point. Retrofitting historical PDFs is expensive and slow; requiring new genomic-test results to be reported through the FHIR Genomics IG (or a comparable structured channel) closes the gap for everything that arrives after the cut-over date.

        Second, the institutional contract with the genomics laboratory is where the requirement is set. The laboratory has to support structured reporting; the institution has to require it in the procurement and the testing-services contract. A laboratory that reports only PDFs is selling an artifact that does not fit the modern clinical-genomics workflow.

        Third, the standards are now mature enough to require. The HL7 FHIR Genomics IG, the GA4GH VRS, and the related operations have been published, ballot-approved, and implemented by several reference institutions. A laboratory that claims structured reporting is not technically feasible is not current with the standards landscape.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "20",
        "06",
        "FHIR resources as the report structure",
        "Course 06 introduced the FHIR data model. The HL7 FHIR Genomics Reporting IG is a profile collection that constrains FHIR's Observation, DiagnosticReport, and MolecularSequence resources for genomic test results. A clinical informaticist who is fluent in FHIR can read the Genomics IG resources directly; the genomics-specific structure adds component-array conventions for the gene and variant fields.",
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "20",
        "10",
        "NLP for extracting variants from PDF reports",
        "Course 10 introduced clinical NLP. The PDF-to-structured-field gap above is the canonical NLP application in clinical genomics today: a pipeline that parses genomic PDF reports and extracts the alleles, the variants, and the interpretation into structured fields. Several published pipelines exist; the pattern is the same one Course 10 covered for clinical notes generally.",
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "20",
        "12",
        "Pharmacogenomic CDS as a CDS Hooks application",
        "Course 12 Track 3 introduced CDS Hooks. The pharmacogenomic CDS pattern (order-select hook, check structured pharmacogenomic result, return a dose-adjustment or alternative-drug card) is the canonical CDS Hooks application in clinical genomics. The CPIC guidelines provide the evidence base; the CDS Hooks architecture provides the delivery layer.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        The clinical-genomics-in-the-EHR loop has four parts (order, lab processing, report, display). The HL7 FHIR Genomics Reporting IG is the standards-based answer for the report-and-display side; it builds on the GA4GH Variation Representation Specification for the variant-data layer. The ACMG 79-gene list defines the floor for clinical exome incidental-findings reporting. Five canonical pharmacogenomic drug-gene pairs (azathioprine-TPMT, clopidogrel-CYP2C19, abacavir-HLA-B*5701, allopurinol-HLA-B*5801, codeine-CYP2D6) define the operational core of clinical-pharmacogenomic CDS. The PDF-vs-structured-field gap, with Ms. Reyes's HLA-DRB1 result as the worked example, is the gap most US institutions still need to close before clinical-genomics CDS at scale is operationally possible.

        Track 04 takes up the research-side bioinformatics infrastructure: the cores, the HPC, the secure enclaves, the public databases, and the research-clinical interface a clinical informaticist will encounter when a clinical-genomics initiative becomes (or always was) a research initiative.
        """
    )
    return


if __name__ == "__main__":
    app.run()
