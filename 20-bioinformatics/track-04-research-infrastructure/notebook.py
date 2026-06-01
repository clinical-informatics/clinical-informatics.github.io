"""Track 04: Research bioinformatics infrastructure.

A clinical informaticist working at any academic medical center will
encounter the research bioinformatics infrastructure when a clinical-
genomics project becomes a research project (or vice versa). The track
presents the institutional layer, the federal layer, and the major
public datasets. Ms. Reyes's hypothetical RA-biobank enrollment walks
through the infrastructure.
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
        "03": "Privacy, ethics, and governance",
        "05": "EHR systems",
        "13": "Research reproducibility",
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
        # Track 04: Research bioinformatics infrastructure

        ## The two-layer picture

        Research bioinformatics infrastructure has two layers. The institutional layer is the academic medical center's local infrastructure: the genomics core that runs the sequencer, the computational biology core that runs the analysis pipelines, the biostatistics core that runs the analyses, the HPC cluster that provides the compute, the secure enclave that holds the controlled-access human-subjects data. The federal layer is the NIH-supported infrastructure: the NCBI databases that hold the public reference resources, the dbGaP archive that holds controlled-access human-subjects data, the public datasets that serve as benchmarks and reference cohorts.

        A clinical informaticist working on any clinical-genomics initiative will encounter both layers. The institutional layer is the operational infrastructure the project runs on; the federal layer is the reference data the project consults and (sometimes) the archive the project's results will be deposited in. The track addresses each layer in turn and closes with Ms. Reyes's hypothetical RA-biobank enrollment as the worked end-to-end example.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The institutional layer

        Most academic medical centers organize their research-bioinformatics infrastructure into a small set of named cores. The exact names vary by institution; the functions are stable.
        """
    )
    return


@app.cell
def _(pd):
    cores_table = pd.DataFrame(
        [
            {
                "Core": "Genomics core (sometimes 'sequencing core' or 'genomics shared resource')",
                "What it does": "Operates the sequencing instruments. Receives specimens, performs library preparation, runs the sequencer, produces FASTQ files.",
                "Charge-back model": "Per-sample fee that covers reagents, instrument time, technician labor. Typical academic exome rates are $300 to $600 per sample at 2024 to 2026 prices.",
                "Equivalent in industry": "Contract research organization (CRO) sequencing service.",
            },
            {
                "Core": "Computational biology core (sometimes 'bioinformatics core')",
                "What it does": "Runs the analysis pipelines from FASTQ to interpreted variant calls. Performs alignment, variant calling, annotation, QC. May also support custom downstream analyses for specific projects.",
                "Charge-back model": "Hourly bioinformatician rate plus compute. Typical academic rates are $80 to $200 per hour.",
                "Equivalent in industry": "Internal bioinformatics team or contracted analysis service.",
            },
            {
                "Core": "Biostatistics core",
                "What it does": "Runs the statistical analyses. Performs association testing, multiple-testing correction, power calculations, study-design consultation.",
                "Charge-back model": "Hourly biostatistician rate. Typical academic rates are $100 to $250 per hour.",
                "Equivalent in industry": "Internal biostatistics team or contracted analysis service.",
            },
            {
                "Core": "HPC cluster (high-performance computing)",
                "What it does": "Provides the compute on which the bioinformatics pipelines run. A typical academic HPC has thousands of CPU cores and petabytes of storage; specialized nodes provide GPU compute for deep-learning pipelines.",
                "Charge-back model": "CPU-hour and storage-month rates. Many institutions provide a free baseline allocation and charge above the threshold.",
                "Equivalent in industry": "Cloud compute (AWS, GCP, Azure).",
            },
            {
                "Core": "Secure enclave (sometimes 'protected data environment')",
                "What it does": "Provides a compute-and-storage environment with the security controls required for controlled-access human-subjects data (dbGaP, All of Us research workbench, institutional biobank).",
                "Charge-back model": "Often grant-funded as institutional infrastructure rather than per-project charge-back. Project access usually requires IRB review plus a Data Use Agreement.",
                "Equivalent in industry": "FedRAMP-compliant cloud environment for protected data.",
            },
        ]
    )
    cores_table.index = range(1, len(cores_table) + 1)
    cores_table.index.name = "row"
    cores_table
    return (cores_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three operational properties of the institutional layer are load-bearing.

        First, the cores operate as shared institutional infrastructure with cost recovery. A research project pays the cores for the services it consumes (sequencing, analysis, compute, storage); the cores use the revenue to maintain the instruments and the staff. The cost-recovery model is what makes shared cores institutionally sustainable.

        Second, the project's bioinformatics work usually happens at the intersection of the cores rather than inside any one core. A typical clinical-genomics research project consumes sequencing from the genomics core, runs the variant-calling pipeline on the computational-biology core, performs the statistical analysis through the biostatistics core, and stores the controlled-access data in the secure enclave. The project's research-bioinformatics PI coordinates across the cores.

        Third, the cores are often the institutional access point for federal resources. The genomics core may submit raw data to the NCBI Sequence Read Archive (SRA) on behalf of the project; the computational-biology core may submit variant calls to ClinVar. The federal-layer interaction is mediated by the institutional cores.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The federal layer: NIH databases and programs

        The federal layer is the NIH-supported infrastructure that holds the reference resources every clinical-genomics workflow consults. Most of it is hosted at the National Center for Biotechnology Information (NCBI) at the National Library of Medicine.
        """
    )
    return


@app.cell
def _(pd):
    federal_table = pd.DataFrame(
        [
            {
                "Resource": "GenBank",
                "Holds": "Annotated nucleotide sequence records. The historical reference archive for any DNA or RNA sequence submitted by a research group.",
                "Access": "Free and public.",
                "When a clinical informaticist would encounter it": "Rarely directly. GenBank underlies many of the reference resources clinical-genomics workflows depend on (gene models, transcript catalogs).",
            },
            {
                "Resource": "dbSNP",
                "Holds": "Single-nucleotide variants and short insertions/deletions with stable rs identifiers and population-frequency data.",
                "Access": "Free and public.",
                "When a clinical informaticist would encounter it": "Routinely. Every clinical VCF references rs identifiers from dbSNP; downstream annotation tools consult dbSNP for population frequencies.",
            },
            {
                "Resource": "ClinVar",
                "Holds": "Variants with their clinical significance assertions (pathogenic, likely pathogenic, uncertain significance, likely benign, benign).",
                "Access": "Free and public.",
                "When a clinical informaticist would encounter it": "Routinely. The standard reference for 'is this specific variant known to cause disease.' The clinical-variant-classification workflow at most US labs consults ClinVar before issuing a pathogenicity assertion.",
            },
            {
                "Resource": "OMIM (Online Mendelian Inheritance in Man)",
                "Holds": "A continuously updated catalog of human genes and Mendelian disorders. Each gene has an OMIM number; each disorder has an OMIM number.",
                "Access": "Free (with registration for bulk download). Maintained at Johns Hopkins.",
                "When a clinical informaticist would encounter it": "Routinely on hereditary-disease workups. The standard reference for 'what disorders is this gene associated with.'",
            },
            {
                "Resource": "dbGaP (database of Genotypes and Phenotypes)",
                "Holds": "Controlled-access archive for studies that combine genotype and phenotype data on human subjects.",
                "Access": "Controlled. Requires institutional review through the NIH Data Access Request process; access granted to specific researchers for specific approved purposes.",
                "When a clinical informaticist would encounter it": "When the project involves secondary analysis of an externally-deposited human-subjects genomic dataset. The dbGaP DAR process is part of the project setup.",
            },
            {
                "Resource": "Sequence Read Archive (SRA)",
                "Holds": "Raw and aligned sequencing data submitted by research groups. The world's largest public sequencing archive.",
                "Access": "Free for the public datasets; controlled for the human-subjects datasets (mirrored from dbGaP).",
                "When a clinical informaticist would encounter it": "When a research project uses an externally-deposited reference dataset (a control cohort, a published case series).",
            },
        ]
    )
    federal_table.index = range(1, len(federal_table) + 1)
    federal_table.index.name = "row"
    federal_table
    return (federal_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three operational properties of the federal layer.

        First, the resources are continuously updated. ClinVar receives thousands of new variant submissions per month; dbSNP is updated on an ongoing basis; OMIM revises gene-disease entries as new evidence accumulates. A clinical-genomics workflow that consults these resources is consulting a moving target; the version of the reference resource used in any analysis should be documented as part of the analysis-reproducibility chain (Course 13).

        Second, the controlled-access resources have a documented approval pathway. The dbGaP Data Access Request process is the canonical example: a research group writes a project description, an institutional review, and a data-management plan; the NIH Data Access Committee reviews and grants access for a defined time period with documented requirements. The approval pathway is the institutional infrastructure that makes controlled-access genomic research operationally tractable.

        Third, the public datasets serve as the benchmarks for the field. gnomAD (below) is the reference for variant population frequencies; the 1000 Genomes Project is the reference for ancestry-stratified frequencies; the GTEx project is the reference for tissue-specific gene expression. A clinical-genomics workflow that does not consult these benchmarks is operating without the field's accumulated reference base.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The major public datasets

        Four datasets dominate the public-reference landscape clinical-genomics workflows consult. Each is freely browsable; access is unrestricted.
        """
    )
    return


@app.cell
def _(pd):
    public_datasets_table = pd.DataFrame(
        [
            {
                "Dataset": "gnomAD (Genome Aggregation Database)",
                "What it contains": "Population-level variant frequencies aggregated from approximately 800,000 exomes and genomes across multiple ancestries (current version, gnomAD v4).",
                "Operational use": "The reference for 'how common is this variant in healthy populations.' A variant with high gnomAD frequency is unlikely to be a Mendelian-disease cause; a variant absent from gnomAD warrants closer scrutiny.",
            },
            {
                "Dataset": "TCGA (The Cancer Genome Atlas)",
                "What it contains": "Genomic, transcriptomic, methylation, and proteomic data on approximately 33 cancer types from approximately 11,000 patients. Hosted at the NCI Genomic Data Commons.",
                "Operational use": "The reference for cancer-genomics research. Validation cohort for cancer-mutation prevalence; substrate for predictive-biomarker discovery.",
            },
            {
                "Dataset": "GTEx (Genotype-Tissue Expression project)",
                "What it contains": "Gene-expression data from approximately 17,000 samples across 54 tissues from approximately 1,000 donors, linked to genotype data.",
                "Operational use": "The reference for tissue-specific gene expression. Used to assess whether a variant in a particular gene is biologically plausible for a particular tissue-specific disease.",
            },
            {
                "Dataset": "ENCODE (Encyclopedia of DNA Elements)",
                "What it contains": "Functional annotation of the human genome: regulatory regions, transcription-factor binding sites, chromatin state, RNA expression. Approximately 80 percent of the human genome has at least one ENCODE annotation.",
                "Operational use": "The reference for 'what does this region of the genome do.' Used to assess whether a non-coding variant is in a functional element.",
            },
        ]
    )
    public_datasets_table.index = range(1, len(public_datasets_table) + 1)
    public_datasets_table.index.name = "row"
    public_datasets_table
    return (public_datasets_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## CTSA: the institutional translational-science infrastructure

        The Clinical and Translational Science Awards (CTSA) program is the NIH-funded national network that supports translational science at academic medical centers. The program funds approximately 60 CTSA hubs across the US; each hub provides shared infrastructure (biostatistics, bioinformatics, regulatory support, community engagement) to its parent institution and to affiliated regional sites.

        Three operational consequences for the clinical informaticist.

        First, the CTSA-funded infrastructure is the institutional layer at most US academic medical centers. The biostatistics core, the bioinformatics core, the regulatory-support team, and the institutional REDCap deployment are often CTSA-funded.

        Second, the CTSA hubs operate as a network. A clinical informaticist with access to one CTSA hub's infrastructure can often access affiliated hubs' resources through the cross-hub collaboration mechanism. The network effect is what makes multi-site clinical-genomics studies tractable.

        Third, the CTSA program publishes a portfolio of shared tools and best practices. The CTSA bioinformatics-shared-resource page is the right starting point for a clinical informaticist who wants to understand what infrastructure is available at a CTSA-supported institution.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Worked end-to-end: Ms. Reyes's RA-biobank enrollment

        Ms. Reyes is approached at a routine rheumatology follow-up about participating in a research RA biobank. The biobank is run by the institutional rheumatology department in partnership with the CTSA-funded biospecimen core and the computational biology core. The eight-stage path her data takes if she enrolls walks through the full infrastructure.
        """
    )
    return


@app.cell
def _(pd):
    biobank_pipeline_table = pd.DataFrame(
        [
            {
                "Stage": 1,
                "What happens": "Consent and enrollment",
                "Infrastructure involved": "REDCap consent form (CTSA-supported), IRB-approved consent document",
                "Reyes-specific detail": "Reyes reviews the consent, opts in to broad use (Tier 2: institutional research) and opts out of recontact for return-of-results.",
            },
            {
                "Stage": 2,
                "What happens": "Specimen collection",
                "Infrastructure involved": "Biospecimen core (CTSA-supported)",
                "Reyes-specific detail": "Blood draw at the routine visit; DNA extracted and aliquoted into the biobank freezer.",
            },
            {
                "Stage": 3,
                "What happens": "Sequencing",
                "Infrastructure involved": "Institutional genomics core",
                "Reyes-specific detail": "Whole-exome sequencing at approximately 100x coverage; FASTQ files produced and transferred to the institutional HPC.",
            },
            {
                "Stage": 4,
                "What happens": "Analysis pipeline",
                "Infrastructure involved": "Computational biology core, HPC cluster, secure enclave",
                "Reyes-specific detail": "FASTQ to BAM to VCF pipeline; variants annotated against gnomAD (federal layer), ClinVar (federal layer), and ENCODE (federal layer); results stored in the secure enclave with the institutional biobank identifier (not Reyes's MRN).",
            },
            {
                "Stage": 5,
                "What happens": "EHR linkage",
                "Infrastructure involved": "Honest-broker service, institutional CDW",
                "Reyes-specific detail": "Reyes's biobank ID is linked to her CDW record through the honest-broker service; the genomic data and the clinical phenotype data are now joined for research analysis without exposing Reyes's identity outside the secure enclave.",
            },
            {
                "Stage": 6,
                "What happens": "Research analysis",
                "Infrastructure involved": "Biostatistics core, secure enclave",
                "Reyes-specific detail": "A research project on HLA-DRB1 variation in RA pulls Reyes's record (anonymized; appears as biobank-ID-78451) along with the other 4,200 RA participants in the biobank. The analysis identifies a candidate non-HLA variant.",
            },
            {
                "Stage": 7,
                "What happens": "Data deposition (controlled-access)",
                "Infrastructure involved": "dbGaP (federal layer)",
                "Reyes-specific detail": "The biobank deposits the aggregated, de-identified study data in dbGaP. Future researchers seeking access submit a Data Access Request and receive controlled access after NIH review.",
            },
            {
                "Stage": 8,
                "What happens": "Publication and result return (limited)",
                "Infrastructure involved": "Journal publication, ClinVar deposition",
                "Reyes-specific detail": "The research group publishes the finding. Variants of clinical significance are deposited in ClinVar (federal layer) under the institution's submitter ID. Reyes does not receive individual results (per her recontact opt-out).",
            },
        ]
    )
    biobank_pipeline_table.index = range(1, len(biobank_pipeline_table) + 1)
    biobank_pipeline_table.index.name = "row"
    biobank_pipeline_table
    return (biobank_pipeline_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three observations about the worked biobank pipeline.

        First, every stage involves both institutional and federal infrastructure. The genomics core (institutional) submits raw data to the SRA (federal). The variant-calling pipeline (institutional) consults gnomAD (federal) for population frequencies. The published variants (institutional research) are deposited in ClinVar (federal). The two layers are interleaved at every stage.

        Second, the honest-broker service and the secure enclave together are the privacy-protection infrastructure. The honest-broker mediates the linkage between Reyes's clinical identity and the biobank identifier; the secure enclave is where the linked data physically resides. Course 03 (privacy, ethics, governance) is the framework that defines what these systems do; this track is the operational instance.

        Third, Reyes's consent decisions shape the pipeline. Her broad-use consent enabled the institutional research; her recontact opt-out shaped how the institution handles individual results. The consent decisions are not abstract; they propagate through eight stages of operational systems.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "20",
        "00",
        "The US research infrastructure from Course 00",
        "Course 00 Track 5 introduced the US research-infrastructure landscape at the curriculum level (NIH, AHRQ, CTSAs, registries). This track is the genomic-research-specific instance of that infrastructure. The CTSA hubs, the NCBI databases, and the institutional cores are operational manifestations of the same general framework Course 00 covered.",
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "20",
        "03",
        "Privacy and the honest-broker pattern",
        "Course 03 introduced the privacy-and-governance framework. The honest-broker service and the secure enclave together are the operational instances of that framework in the research-genomics setting. The consent decisions Reyes made in stage 1 (broad use, recontact opt-out) are the consent operationalizations the course covered abstractly.",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "20",
        "13",
        "Documenting the reference-resource versions used",
        "Course 13 (Research reproducibility) takes up the documentation discipline. A bioinformatics analysis that consulted gnomAD v4.1 and ClinVar 2026-04 is not the same as one that consulted gnomAD v3.1 and ClinVar 2024-01; the version pins are part of the reproducibility documentation Course 13 will cover.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        Research bioinformatics infrastructure has two layers: the institutional (cores, HPC, secure enclave) and the federal (NCBI databases, dbGaP, CTSA program). The clinical informaticist working on any clinical-genomics initiative encounters both layers, often simultaneously. Four major public datasets (gnomAD, TCGA, GTEx, ENCODE) serve as the reference resources every clinical-genomics analysis consults. Ms. Reyes's hypothetical biobank enrollment walked through eight stages that interleave institutional and federal infrastructure, with her consent decisions shaping the pipeline at every stage.

        Track 05 takes up the population-genomics and equity dimensions: the large biobanks (All of Us, UK Biobank, MyCode, eMERGE), polygenic risk scores at concept level, ancestry-vs-race in genomics, and direct-to-consumer testing.
        """
    )
    return


if __name__ == "__main__":
    app.run()
