"""Track 01: What bioinformatics is and how it relates to clinical informatics.

Bioinformatics is the application of computational methods to biological
data. The track defines the field, names the three-segment spectrum
(molecular bench / translational / clinical genomics) and the boundary
with clinical informatics, sketches the brief history (HGP, 1000
Genomes, ENCODE, All of Us, gnomAD), and walks Ms. Reyes's HLA-DRB1
shared-epitope test from the buccal swab her rheumatologist ordered to
the line in her chart the clinician reads.
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
        "00": "Foundations of clinical informatics",
        "02": "Data literacy",
        "05": "EHR systems",
        "06": "Learn FHIR",
        "09": "AI in medicine",
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
        # Track 01: What bioinformatics is

        ## A working definition

        Bioinformatics is the application of computational methods to biological data. The data is whatever a biological measurement produces (DNA sequence, RNA expression, protein interaction, microbial community composition); the methods are whatever it takes to turn that data into something a researcher or clinician can act on (alignment, variant calling, annotation, statistical testing, visualization, knowledge-base lookup).

        Most of the discipline organizes around three substantive areas the rest of this course addresses one at a time.

        - **Molecular bench bioinformatics.** Algorithms and pipelines that operate at the level of biological sequences themselves: aligning short reads to a reference genome, calling variants, assembling sequence from scratch, predicting protein structure. This is the algorithmic core of the field and is where most published bioinformatics methods sit.
        - **Translational bioinformatics.** Methods that connect molecular data to clinical phenotypes: cohort identification from genomic data, association studies between variants and disease, pharmacogenomic dose-prediction models. This is the bridge between the bench and the bedside.
        - **Clinical genomics.** The operational use of genomic information in clinical care: ordering a test, receiving a structured result, acting on it. This is where bioinformatics and clinical informatics meet. The clinician orders the test; the bioinformatics pipeline produces the variant call; the EHR shows the clinician a result line.

        The course is for clinical informaticists. The boundary the course sits on is the third area: how genomic information enters and lives in clinical systems. The first two are addressed at the concept level only.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A brief history

        Six dates anchor the modern field. The clinical informaticist working in this space will hear all six referenced in conversation; knowing what each one represents is the operational minimum.
        """
    )
    return


@app.cell
def _(pd):
    history_table = pd.DataFrame(
        [
            {
                "Date": "1990 to 2003",
                "Event": "Human Genome Project",
                "What it produced": "The first reference sequence of the human genome, completed in 2003 (with later refinements). The project cost approximately $3 billion and produced the reference sequence every clinical and research workflow today aligns against.",
            },
            {
                "Date": "2007",
                "Event": "First commercial direct-to-consumer genetic testing",
                "What it produced": "23andMe began offering ancestry and trait reports to consumers. The DTC industry has grown to tens of millions of US consumers and is the source of most clinician encounters with genomic information that the clinician did not order.",
            },
            {
                "Date": "2008 to 2015",
                "Event": "1000 Genomes Project",
                "What it produced": "A reference catalog of human genetic variation across 26 populations, with approximately 2,500 individuals sequenced. The 1000 Genomes call set is still cited in most variant-prioritization workflows as the population-frequency reference for common variants.",
            },
            {
                "Date": "2012",
                "Event": "ENCODE phase 2 release",
                "What it produced": "Functional annotation of approximately 80% of the human genome (regulatory regions, transcribed regions, transcription-factor binding sites). ENCODE is the reference for 'is this variant in a functional element' questions in clinical-genomics interpretation.",
            },
            {
                "Date": "2016",
                "Event": "gnomAD launched (originally ExAC, became gnomAD)",
                "What it produced": "A continuously updated population-frequency database now covering approximately 800,000 exomes and genomes. The reference for 'is this variant common in healthy populations.' Most clinical-variant-classification workflows consult gnomAD before any disease assertion.",
            },
            {
                "Date": "2018 to ongoing",
                "Event": "All of Us Research Program enrollment",
                "What it produced": "The US national population-cohort study, currently enrolling toward 1 million participants with broad consent for research use of EHR, biospecimen, survey, and wearable data. The largest US-based research-bioinformatics resource being built today.",
            },
        ]
    )
    history_table.index = range(1, len(history_table) + 1)
    history_table.index.name = "row"
    history_table
    return (history_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Two properties of the history are load-bearing for the rest of the course.

        First, the cost of sequencing has fallen by approximately five orders of magnitude in two decades. The HGP cost $3 billion for one genome in 2003; a clinical-grade exome today costs approximately $300 and a clinical-grade whole genome costs approximately $1,000. The cost trajectory is what made population-scale genomics (the All of Us, UK Biobank, gnomAD entries above) operationally possible.

        Second, the field has accumulated reference resources rather than just methods. A modern clinical-variant-classification workflow does not start from raw data; it consults gnomAD for population frequency, ClinVar for prior pathogenicity assertions, OMIM for disease association, the ACMG criteria for the classification rubric. The reference resources are the institutional memory of the field and are the standards a clinical-genomics workflow has to interoperate with.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The boundary with clinical informatics

        Where does bioinformatics stop and clinical informatics start? The cleanest single answer is at the moment the variant call leaves the laboratory information system. Before that moment, the data is in bioinformatics-pipeline territory (FASTQ to BAM to VCF, the file types Track 02 addresses). After that moment, the data is in clinical-informatics territory (the report is structured for the EHR, the clinician receives it at a workflow moment, the alert fires if a pharmacogenomic-actionable variant is present).

        A clinical informaticist working on a clinical-genomics initiative is responsible for the EHR-side of the boundary: the order entry, the result-display logic, the CDS alerts, the patient-facing materials. The bioinformatics core is responsible for the pipeline side: the alignment, the variant calling, the annotation, the QC. The two sides communicate through standards (the HL7 FHIR Genomics Reporting IG that Track 03 takes up) and through the standard handoff format (the structured genomic-report).

        Three operational consequences for the clinical informaticist follow.

        First, the clinical informaticist does not need to understand sequence alignment algorithms to be effective. What they need is to understand the inputs the bioinformatics pipeline takes, the outputs it produces, and the standards both ends speak. Most of this course operates at that interface.

        Second, the clinical informaticist needs to understand the standards on both sides. The FHIR Genomics IG is the standard the EHR speaks; the VCF format is the standard the bioinformatics pipeline produces. Track 02 covers the VCF side; Track 03 covers the FHIR side. The clinical informaticist who can read both is the one who can bridge the gap.

        Third, the clinical informaticist needs to understand the institutional infrastructure on the research side. Many clinical-genomics initiatives become research initiatives (cohort discovery, retrospective analysis, biobank enrollment); the same patient's data may move between clinical and research systems. Track 04 addresses the research-infrastructure side.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Worked example: Reyes's HLA-DRB1 test, buccal swab to chart line

        Ms. Reyes's HLA-DRB1 shared-epitope test is the worked example that anchors the rest of the course. The test was ordered by her rheumatologist at her diagnosis visit in 2022 because the shared epitope (a five-amino-acid motif on certain HLA-DRB1 alleles) is the strongest known genetic risk factor for seropositive rheumatoid arthritis. The result (HLA-DRB1*04:01 positive) was part of the genetic context for her seropositive-RA diagnosis.

        The path from buccal swab to chart line has eight stages. Each stage is a hand-off between a clinical, laboratory, or bioinformatics system; understanding the full path is the operational foundation for the rest of the course.
        """
    )
    return


@app.cell
def _(pd):
    pipeline_table = pd.DataFrame(
        [
            {
                "Stage": 1,
                "What happens": "Order placed",
                "Where": "Rheumatology clinic",
                "Systems involved": "EHR (order entry)",
                "Reyes-specific detail": "Dr. Bennett places an HLA-DRB1 typing order at the 2022-02-14 new-patient visit, with seropositive-RA workup as the clinical indication.",
            },
            {
                "Stage": 2,
                "What happens": "Specimen collected",
                "Where": "Phlebotomy or clinic",
                "Systems involved": "EHR (specimen tracking)",
                "Reyes-specific detail": "Buccal swab collected the same day. Specimen sent to the institutional genomics lab.",
            },
            {
                "Stage": 3,
                "What happens": "DNA extraction and PCR amplification",
                "Where": "Genomics laboratory",
                "Systems involved": "Laboratory information system (LIS)",
                "Reyes-specific detail": "DNA extracted from buccal cells; HLA-DRB1 region amplified by PCR with allele-specific primers.",
            },
            {
                "Stage": 4,
                "What happens": "Sequencing (or genotyping)",
                "Where": "Genomics laboratory",
                "Systems involved": "Sequencer (or genotyping array), instrument-control software",
                "Reyes-specific detail": "Sanger sequencing of the amplified HLA-DRB1 region. Produces raw chromatogram traces.",
            },
            {
                "Stage": 5,
                "What happens": "Allele calling",
                "Where": "Genomics laboratory bioinformatics pipeline",
                "Systems involved": "HLA-typing software (specialized tool that maps sequence to known HLA alleles)",
                "Reyes-specific detail": "Pipeline reports HLA-DRB1*04:01 / *13:01 (one allele inherited from each parent).",
            },
            {
                "Stage": 6,
                "What happens": "Report generation",
                "Where": "Genomics laboratory",
                "Systems involved": "LIS, report-generation software",
                "Reyes-specific detail": "PDF report generated with the alleles, the shared-epitope interpretation (positive, since *04:01 carries the QKRAA motif), and the clinical context.",
            },
            {
                "Stage": 7,
                "What happens": "Report delivered to EHR",
                "Where": "Lab-to-EHR interface",
                "Systems involved": "HL7 v2 ORU message (or modern FHIR DiagnosticReport)",
                "Reyes-specific detail": "PDF arrives as a media attachment on a generic 'HLA typing' result entry in the EHR. The structured fields contain only the test name and the order metadata; the actual result is in the PDF.",
            },
            {
                "Stage": 8,
                "What happens": "Clinician reads",
                "Where": "Rheumatology clinic",
                "Systems involved": "EHR (result viewer, PDF viewer)",
                "Reyes-specific detail": "Dr. Bennett opens the PDF at the follow-up visit and integrates the shared-epitope-positive result into the seropositive-erosive-RA assessment.",
            },
        ]
    )
    pipeline_table.index = range(1, len(pipeline_table) + 1)
    pipeline_table.index.name = "row"
    pipeline_table
    return (pipeline_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three observations about the eight-stage pipeline.

        First, the bioinformatics work is concentrated in stages 4 and 5. Sequencing produces raw chromatogram traces; the bioinformatics pipeline turns those traces into the allele call. Track 02 of this course addresses the data formats that flow through those stages for next-generation-sequencing-based tests; HLA typing by Sanger sequencing is the historical example that fits the same shape.

        Second, the clinical-informatics work is concentrated in stages 1, 2, 7, and 8. Order entry, specimen tracking, result delivery, and result display are EHR-side responsibilities. The clinical informaticist's leverage on the workflow is concentrated there.

        Third, stage 7 is the typical failure point. The structured fields of the EHR result entry capture only the metadata; the actual clinical content is in the PDF. A query against the structured fields cannot find HLA-DRB1*04:01-positive patients (it can find patients with HLA-typing-test-completed, but not the test result). Track 03 addresses the PDF-vs-structured-field gap and the standards (HL7 FHIR Genomics Reporting IG) that the field has agreed should close it.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "20",
        "00",
        "Data at rest and the file-type vocabulary",
        "Course 00 Track 3 introduced the data-at-rest vocabulary (files, file types, relational databases). The genomic file types Track 02 addresses (FASTQ, BAM, VCF, GFF, BED) are domain-specific instances of the same general framework Course 00 established. The clinical informaticist who has internalized Course 00 will find Track 02 straightforward.",
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "20",
        "05",
        "Laboratory information systems",
        "Course 05 introduced the EHR-and-LIS landscape. The genomics laboratory is a LIS the bioinformatics pipeline lives inside; the LIS-to-EHR interface (stage 7 above) is the canonical handoff Course 05 covered for any lab result.",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "20",
        "06",
        "FHIR Genomics Reporting as the structured-result standard",
        "Course 06 introduced FHIR. The HL7 FHIR Genomics Reporting Implementation Guide is the FHIR profile for genomic test results; it is the standards-based answer to the PDF-result problem stage 7 above produces. Track 03 takes up the IG in detail.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        Bioinformatics is the application of computational methods to biological data. The discipline organizes around three substantive areas (molecular bench bioinformatics, translational bioinformatics, clinical genomics); this course operates at the boundary between the third area and clinical informatics. The brief history (HGP 1990 to 2003, the cost-of-sequencing collapse, the accumulation of reference resources like gnomAD and ClinVar) shapes what the field can do today. Ms. Reyes's HLA-DRB1 shared-epitope test, walked across the eight-stage pipeline from buccal swab to chart line, is the worked example the rest of the course builds on.

        Track 02 takes up the genomic data structures and file types that flow through the pipeline stages a bioinformatics-pipeline-aware informaticist needs to recognize.
        """
    )
    return


if __name__ == "__main__":
    app.run()
