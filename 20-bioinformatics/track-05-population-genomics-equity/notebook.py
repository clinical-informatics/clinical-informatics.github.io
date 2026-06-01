"""Track 05: Population genomics, equity, and the future.

The largest population-genomics resources of the past decade (All of
Us, UK Biobank, MyCode, eMERGE) are reshaping what clinical genomics
can do. The track presents each consortium, introduces polygenic risk
scores at concept level, addresses the ancestry-vs-race distinction,
covers direct-to-consumer testing including Reyes's 23andMe result,
and closes with the equity discussion on European-ancestry over-
representation in genomic databases.
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
        "11": "Health economics data",
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
        # Track 05: Population genomics, equity, and the future

        ## The population-cohort era

        The past decade of population genomics has been organized around four large biobank cohorts (All of Us, UK Biobank, MyCode, eMERGE) that combine genomic data with deep phenotypic data at population scale. The cohorts have changed what clinical-genomics research can do: questions that previously required years of recruitment can now be answered against ready-to-query population resources.

        The track presents each cohort, introduces polygenic risk scores at the concept level, addresses the ancestry-vs-race distinction in genomics with explicit cross-reference to Course 03 fairness and Course 09 bias, walks the direct-to-consumer testing landscape including Ms. Reyes's pandemic-era 23andMe result, and closes with the equity discussion on the historical European-ancestry over-representation in genomic databases.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Four biobanks that reshaped the field
        """
    )
    return


@app.cell
def _(pd):
    biobank_table = pd.DataFrame(
        [
            {
                "Biobank": "All of Us Research Program",
                "Country": "United States",
                "Approximate size": "Enrolling toward 1 million participants; current enrollment approximately 800,000 (2026).",
                "Data layers": "EHR data, biospecimens (DNA, RNA), survey data, wearable data, physical-measurement data. Whole-genome sequencing on a growing subset.",
                "Operational use for clinical informatics": "The largest US-based research-bioinformatics resource. Researcher Workbench is the cloud-hosted secure-enclave access pathway; clinical informaticists working with All of Us data access it through the Workbench.",
            },
            {
                "Biobank": "UK Biobank",
                "Country": "United Kingdom",
                "Approximate size": "Approximately 500,000 participants; deeply phenotyped at baseline.",
                "Data layers": "EHR linkage, genotyping array data, whole-exome sequencing (complete), whole-genome sequencing (rolling), biomarker measurements, imaging.",
                "Operational use for clinical informatics": "The most-used population-cohort resource in published clinical-genomics research. UK Biobank publications are the standard reference for many disease-association studies. Access is via institutional application and standardized data-use agreement.",
            },
            {
                "Biobank": "MyCode (Geisinger)",
                "Country": "United States",
                "Approximate size": "Approximately 300,000 participants; integrated with Geisinger Health System EHR.",
                "Data layers": "Geisinger EHR data plus exome sequencing on a large subset.",
                "Operational use for clinical informatics": "The most-developed example of clinical-genomics integration into a US health system. Returns clinically actionable findings (ACMG 79) to participants and their clinicians as part of routine care. The reference model for institutional clinical-genomics-at-scale.",
            },
            {
                "Biobank": "eMERGE Network",
                "Country": "United States (multi-site)",
                "Approximate size": "Approximately 100,000 participants across multiple participating academic medical centers.",
                "Data layers": "EHR data from participating sites, genotyping array data, exome sequencing on subsets.",
                "Operational use for clinical informatics": "The NIH-funded consortium that connects EHR-based phenotyping with genomic data across multiple institutions. The eMERGE publications are the standard reference for EHR-phenotype-to-genotype association methodology.",
            },
        ]
    )
    biobank_table.index = range(1, len(biobank_table) + 1)
    biobank_table.index.name = "row"
    biobank_table
    return (biobank_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three operational properties of the population-cohort era are load-bearing for the clinical informaticist.

        First, the population biobanks are not replacing institutional research; they are extending the substrate. A clinical informaticist working on an RA-specific question at their own institution can validate findings against UK Biobank's RA participants, replicate against All of Us's RA participants, and look for related findings in eMERGE's RA cohort. The institutional and population resources are complementary.

        Second, the cohort-level resources operate under controlled-access models. UK Biobank requires an institutional application and a standardized Material Transfer Agreement; All of Us requires Researcher Workbench credentialing; MyCode is largely accessible only to Geisinger-affiliated researchers and approved external collaborators. The access pathway is part of the project's institutional infrastructure.

        Third, the cohorts have different consent models. All of Us uses broad consent with patient-portal return of results for actionable findings. UK Biobank uses a more research-oriented consent with no individual return of results. MyCode returns ACMG-79 actionable findings clinically through Geisinger. The consent model shapes what the clinical informaticist can do with the data and what the patient receives from participating.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Polygenic risk scores at concept level

        A polygenic risk score (PRS) is a single number that summarizes a person's genetic predisposition to a complex trait or disease. The number is computed by summing weighted contributions from many (thousands to millions) of common genetic variants. The weights come from large genome-wide association studies (GWAS) that identified each variant's individual association with the trait.

        Three properties of PRS are load-bearing for the clinical informaticist.

        - **PRS is a summary, not a diagnosis.** A high PRS for a complex disease (cardiovascular disease, type 2 diabetes, schizophrenia) means the person has a higher-than-average genetic predisposition; it does not mean the person will develop the disease, and a low PRS does not rule it out. The score's predictive value is statistical, not deterministic.
        - **PRS performance is ancestry-dependent.** PRS computed from a GWAS in one ancestry population performs less well when applied to a different ancestry population. The performance gap is the central equity concern in PRS clinical use. The Martin et al. 2019 Nature Genetics paper (go-deeper) documented the gap quantitatively.
        - **PRS clinical utility is an open question for most diseases.** A PRS for coronary artery disease may stratify a population usefully; whether it changes management for any individual patient is the open question. Several disease-specific PRS clinical-utility trials are in progress; the field expects clarity over the next several years.

        For the clinical informaticist, the operational implication is that PRS is a research-grade tool with limited current clinical use. A clinical-genomics workflow that integrates PRS should treat it as a research finding requiring clinical interpretation, not as a deterministic clinical input. Future integration into clinical CDS depends on the trials in progress.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Ancestry vs race in genomics

        Ancestry and race are different concepts. Ancestry refers to the genealogical origin of a person's chromosomal segments and is a biological property of the genome. Race is a social construct with biological, geographic, and political components that has been used in clinical algorithms for decades. The distinction matters operationally because the two concepts behave differently in genomic analysis.

        Three operational distinctions are load-bearing.

        First, ancestry in genomic analysis is typically inferred from the genome itself. A modern population-genomics pipeline performs ancestry inference by comparing the patient's genome to reference populations (1000 Genomes, gnomAD); the output is a vector of ancestry-component proportions (e.g., 45 percent European, 35 percent African, 20 percent Indigenous American). The output is a continuous quantity, not a discrete label.

        Second, race in clinical algorithms is typically self-reported and is recorded as a categorical EHR field. The race field captures something different from the genomic ancestry: a person's social identity, their reported background, and (in US clinical contexts) the way they are categorized in healthcare administrative systems.

        Third, replacing race with ancestry in clinical algorithms does not automatically resolve equity concerns. A clinical algorithm that uses self-reported race as a variable can be racist in operation; an algorithm that uses genetic ancestry instead can have its own equity problems (the ancestry inference is itself sensitive to which reference populations were used and how they were sampled). The clinical informaticist working in this space should treat both ancestry-based and race-based clinical algorithms as candidates for equity review, not as inherent fixes.

        Course 03 (privacy, ethics, governance) and Course 09 (AI in medicine, particularly Track 5 on bias) developed this material in detail. Course 12 Track 5 covered the specific clinical algorithms whose race-correction has been reconsidered in the past decade (eGFR, VBAC, ASCVD). This track is the genomic-specific application of those broader frameworks.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "20",
        "03",
        "Algorithmic fairness from Course 03",
        "Course 03 Track 4 introduced the algorithmic-fairness framework. The ancestry-vs-race distinction in this track is the genomic-specific instance of that framework; the operational rules (audit by subgroup, document the inference method, plan the monitoring) carry forward unchanged.",
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "20",
        "09",
        "Subgroup performance from Course 09",
        "Course 09 Track 5 introduced the four entry points for bias and the subgroup-performance vocabulary. The PRS ancestry-dependence above and the European-ancestry over-representation below are the genomic instances of those entry points: training-data bias and feature-engineering bias respectively. The same subgroup-stratified analysis vocabulary applies.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Direct-to-consumer testing

        The DTC genetic-testing industry has grown to tens of millions of US consumers since 23andMe's 2007 launch. The clinical-informatics consequence is that patients arrive at clinical encounters with DTC results and ask their clinicians to interpret them. A clinical informaticist working on patient-facing materials, clinician-education programs, or CDS rules has to know what DTC tests actually report and what they do not.

        Three operational properties of DTC genetic testing are load-bearing.
        """
    )
    return


@app.cell
def _(pd):
    dtc_table = pd.DataFrame(
        [
            {
                "What DTC actually reports": "Genotypes at a fixed set of array positions (typically 600,000 to 700,000 variants from a SNP genotyping array).",
                "What it does well": "Common-variant genotype calls at the array positions. Ancestry-component proportions from those genotypes. Common-variant trait associations (hair color, eye color, lactose intolerance).",
                "What it does not do well": "Rare-variant detection (requires sequencing, not arrays). Comprehensive coverage of any specific disease gene (the array contains the variants the manufacturer chose; rare disease-causing variants are usually absent). Clinical-grade certainty on any single result (the false-positive rate at any single position is non-negligible).",
            },
            {
                "What DTC actually reports": "FDA-cleared health reports for a small subset of conditions (since 23andMe's 2017 FDA clearance for 10 genetic-health-risk reports, expanded since).",
                "What it does well": "Reports the patient's status for the specific variants the FDA clearance covers (BRCA1 / BRCA2 three Ashkenazi-Jewish founder variants, MUTYH two variants, several others).",
                "What it does not do well": "Provides comprehensive BRCA1/BRCA2 testing (the three covered variants represent a small fraction of pathogenic BRCA1/BRCA2 variants in any population other than Ashkenazi-Jewish ancestry). A negative DTC BRCA1/BRCA2 result is not equivalent to clinical-grade negative testing.",
            },
            {
                "What DTC actually reports": "Ancestry-component breakdowns and shared-ancestry connection features (DNA Relatives, family-tree integration).",
                "What it does well": "Ancestry inference at the population-component level (continental and sub-continental breakdowns). Identification of shared DNA segments with other database participants.",
                "What it does not do well": "Definitive ancestry categorizations. The breakdown is a continuous statistical inference; consumers often interpret it as deterministic ('I am 25% Irish'). The shared-DNA-segment feature has produced family disruption and legal-implications-of-genealogy events.",
            },
        ]
    )
    dtc_table.index = range(1, len(dtc_table) + 1)
    dtc_table.index.name = "row"
    dtc_table
    return (dtc_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Reyes's 23andMe result

        Ms. Reyes did a 23andMe test during the pandemic out of curiosity. Her result has three substantive components.

        - **Ancestry.** The report says approximately 65 percent European (with sub-components: Iberian, French/German), 25 percent Indigenous American, 8 percent Sub-Saharan African, 2 percent unassigned. Her family's stated ancestry matches the European and Indigenous American components; the African component is small and consistent with population history but is a surprise to her.
        - **Health reports (FDA-cleared subset).** No detected variants in the FDA-covered BRCA1/BRCA2 panel; no detected variants in the FDA-covered MUTYH panel; no detected variants in the FDA-covered late-onset Alzheimer's APOE panel. Each report says, in fine print, that the panel covers a specific limited set of variants and that the negative result does not rule out other pathogenic variants in the same gene.
        - **Carrier status and traits.** Multiple common-variant trait reports (hair texture, photic sneeze reflex, asparagus metabolism). These are not clinically actionable.

        Three points the clinical informaticist should know about how a patient like Ms. Reyes would discuss this result with her clinician.

        First, Reyes might ask "does this affect my RA risk?" The answer is essentially no. 23andMe does not include an RA-specific genetic-risk report; HLA-DRB1 shared-epitope status (the strong RA risk factor, which she is positive for from her clinical test) is not in the standard 23andMe report. The shared epitope is technically detectable from her DNA, but 23andMe does not surface it.

        Second, Reyes might ask "is the BRCA report enough?" The clinically correct answer is no for a patient with a family history of breast or ovarian cancer; the three FDA-cleared variants cover only Ashkenazi-Jewish founder variants and miss most pathogenic BRCA variants in any other ancestry. The fine print says this; most patients do not read the fine print.

        Third, Reyes might ask "should I do anything based on this?" The clinically appropriate answer is to bring any clinically relevant results to her clinician for confirmation through a clinical-grade test before making a clinical decision. The DTC result is informational, not actionable on its own.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The European-ancestry over-representation

        The historical pattern of population-genomic research has been a European-ancestry over-representation. Estimates from the published literature consistently put European-ancestry participants at 70 to 85 percent of GWAS sample sizes and a similar fraction of large-biobank cohorts (UK Biobank is approximately 95 percent European-ancestry; All of Us was designed in part to address this gap and has roughly 50 percent under-represented-in-research participants). The Sirugo, Williams, Tishkoff 2019 Cell paper (linked in the go-deeper) documents the pattern quantitatively across a decade of GWAS.

        Three operational consequences for clinical informatics.

        First, polygenic risk scores derived from European-ancestry GWAS underperform when applied to non-European-ancestry patients. The Martin et al. 2019 paper documented effect-size reductions of 50 percent or more in some cases. A clinical-genomics workflow that deploys PRS-based CDS should expect ancestry-stratified performance and should monitor for it.

        Second, clinical-genomics interpretation for non-European-ancestry patients can be systematically less informative. A novel variant in a non-European-ancestry patient is more likely to be absent from gnomAD (which itself has European-ancestry over-representation but is more balanced than most cohorts); absence from gnomAD makes interpretation more uncertain because population-frequency context is missing.

        Third, the research-infrastructure response (All of Us's design for under-represented-in-research recruitment; UK Biobank's analog efforts; non-US efforts including the H3Africa consortium and Singapore's national initiative; gnomAD's continued expansion of non-European sequencing) is the structural answer. The clinical-genomics field is correcting this on a decadal timescale; the clinical informaticist working in this space should expect rapid changes in the data landscape over the next five to ten years.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What the next decade likely brings

        Three trajectories are reasonably clear from the published 2025 to 2026 state of the field.

        First, clinical-grade whole-genome sequencing will become the default for many indications currently served by gene panels. The cost has dropped to approximately $1,000 per clinical genome; the bioinformatics-pipeline maturity is high; the only remaining barriers are reimbursement and clinical-interpretation workflow. Expect WGS to displace panels in pediatric undiagnosed disease, pharmacogenomics, and complex hereditary cancer workups over the next several years.

        Second, polygenic risk scores will enter clinical use for a small set of high-leverage applications. Cardiovascular risk stratification is the most likely first widespread use; current trials should report clinical-utility evidence by the late 2020s. The integration architecture (PRS as a structured clinical-genomics result, returned through the FHIR Genomics IG, surfaced through CDS Hooks at relevant clinical moments) is the operational path.

        Third, the PDF-vs-structured-field gap will close at major institutions but remain at smaller ones. The HL7 FHIR Genomics IG is mature and is being implemented at flagship academic medical centers; clinical-laboratory vendors are gradually supporting structured reporting. Smaller institutions and community laboratories will lag the structural transition by several years.

        The clinical informaticist working in this space is therefore facing a field where the standards are mature, the infrastructure is increasingly clinical-grade, the equity questions are recognized, and the integration into clinical care is rolling out unevenly. The capstone exercise that follows takes up the design of a precision-medicine program against that backdrop.
        """
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "20",
        "11",
        "Cost-effectiveness of pharmacogenomic testing",
        "Course 11 introduced cost-effectiveness analysis. Pre-emptive pharmacogenomic testing is a canonical case for CEA: a one-time test produces results applied across multiple future prescriptions. The published CEAs (for warfarin-CYP2C9/VKORC1, clopidogrel-CYP2C19, others) report ICERs that depend strongly on the patient's expected number of relevant future prescriptions; the capstone takes this up explicitly.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        The past decade of population genomics organized around four large biobank cohorts (All of Us, UK Biobank, MyCode, eMERGE) that combine genomic data with deep phenotypic data at population scale. Polygenic risk scores summarize genetic predisposition through weighted sums over many common variants; their clinical utility remains an open question for most diseases and their performance is ancestry-dependent. Ancestry and race are different concepts; the ancestry-vs-race distinction matters operationally and connects to Course 03 and Course 09's fairness frameworks. Direct-to-consumer testing reports common-variant genotypes from a SNP array; clinically meaningful results (negative BRCA, suggested actions) require fine-print reading and clinical-grade confirmation. Ms. Reyes's 23andMe result illustrates the patient-clinician interpretation conversation. The European-ancestry over-representation in genomic databases is the central equity concern, and the field is correcting it on a decadal timescale.

        The course closes with the Socratic capstone: design a precision-medicine program (pharmacogenomic testing at the point of high-risk prescribing) that integrates everything every prior course in this curriculum has covered.
        """
    )
    return


if __name__ == "__main__":
    app.run()
