# Glossary: 20 Bioinformatics for clinical informaticists

Most terms used in this course are defined in the [curriculum-wide glossary](../start-here/GLOSSARY.md): FHIR (R4), HIPAA, OMOP CDM. Bioinformatics-specific terms appear below.

**ACMG 79.** The American College of Medical Genetics and Genomics list of 79 genes (current revision; the list has grown over time from the original 56) for which a pathogenic or likely-pathogenic variant identified incidentally during clinical exome or genome sequencing should be reported back to the patient. The list defines the "actionable secondary findings" category in clinical genomic reporting.

**BAM (Binary Alignment Map).** The binary, indexed version of the SAM (Sequence Alignment Map) format. A BAM file contains short DNA-sequence reads aligned to a reference genome, with their alignment positions, quality scores, and per-base information. The intermediate file between raw sequencing output (FASTQ) and variant calls (VCF).

**BED (Browser Extensible Data).** A tab-delimited format for genomic regions. Each row is one region with a chromosome, start, end, and optional name and score columns. Used to define target regions for sequencing (an exome capture kit's BED file lists every region the kit targets) and to annotate genomic features (a BED file of gene exons, of regulatory elements).

**BLAST (Basic Local Alignment Search Tool).** The canonical sequence-similarity search tool at NCBI. Given a query sequence, BLAST returns the most similar sequences in a chosen database (nucleotide or protein) with statistical significance scores. The historical entry point for sequence comparison.

**ClinVar.** The NCBI-maintained free public archive of human variants with their clinical significance assertions (pathogenic, likely pathogenic, uncertain significance, likely benign, benign). The reference resource for "is this specific variant known to cause disease."

**dbGaP (database of Genotypes and Phenotypes).** The NCBI-maintained controlled-access repository for studies that combine genotype and phenotype data on human subjects. Access requires institutional approval through the Data Access Request process. The standard archive for NIH-funded human-subjects genomic research.

**dbSNP (database of Single Nucleotide Polymorphisms).** The NCBI-maintained free public archive of human variation. Each variant has a stable identifier (rs number). The reference resource for "does this variant have a stable name and what is known about its population frequency."

**DTC (direct-to-consumer) genetic testing.** Genetic testing ordered by the consumer rather than by a clinician, with results returned directly to the consumer. 23andMe and AncestryDNA are the dominant US providers. The clinical informatics consequence is that patients bring DTC results to clinical encounters and ask their clinicians to interpret them.

**FASTQ.** A text format for raw sequencing reads. Each read appears as four lines: an `@`-prefixed identifier, the sequence itself, a `+`-prefixed separator, and a per-base quality string. The output of a sequencer before any alignment or analysis.

**GA4GH (Global Alliance for Genomics and Health).** An international standards organization that has published the canonical specifications for genomic-data representation (the GA4GH Variation Representation Specification), genomic-data discovery (Beacon), and genomic-data exchange (htsget, the GA4GH passport for federated access). The standards body the genomic-informatics community references for interoperability.

**GFF / GTF.** Tab-delimited formats for genomic annotations (genes, exons, regulatory features). GFF (General Feature Format) is the older standard; GTF (Gene Transfer Format) is a tighter, more constrained GFF subset. The reference file types for "what is at this position in the genome."

**gnomAD.** The Genome Aggregation Database. A large, freely browsable collection of population-level variant frequencies aggregated from approximately 800,000 exomes and genomes. The reference resource for "how common is this variant in healthy populations."

**HL7 Genomics Reporting IG.** The HL7 FHIR Implementation Guide for representing genomic test results as structured FHIR resources (Observation profiles for variants, DiagnosticReport profiles for the lab report). The standards-based answer to the PDF-genomic-report problem.

**HLA-DRB1.** A human leukocyte antigen class II gene. Particular alleles in the HLA-DRB1 04 family (specifically *04:01 and *04:04) carry a "shared epitope" sequence motif strongly associated with seropositive rheumatoid arthritis. Ms. Reyes is HLA-DRB1*04:01 positive; this is part of her seropositive-RA workup.

**OMIM (Online Mendelian Inheritance in Man).** A comprehensive, continuously updated catalog of human genes and Mendelian disorders. Maintained at Johns Hopkins. The standard reference for inherited-disease gene curation.

**PGx (pharmacogenomics).** The use of genomic information to guide drug selection or dosing. Canonical examples include TPMT screening before azathioprine (to avoid life-threatening myelosuppression in poor metabolizers), CYP2C19 before clopidogrel (to avoid loss of efficacy in poor metabolizers), and HLA-B*5701 before abacavir (to avoid severe hypersensitivity reaction in carriers).

**Polygenic risk score (PRS).** A single number computed by summing weighted contributions from many (thousands to millions) of common genetic variants, intended to summarize a person's genetic predisposition to a complex trait or disease. The clinical-utility question for PRS remains open across most diseases.

**Reference genome.** The standardized human genome sequence (currently GRCh38 / hg38, with GRCh37 / hg19 still in widespread use) that sequencing reads are aligned against. All clinical variant calls are reported as differences from the reference.

**Shared epitope.** A five-amino-acid sequence motif (QKRAA or QRRAA) in the third hypervariable region of the HLA-DRB1 beta chain, present in several DRB1 alleles (most notably *04:01 and *04:04). The shared epitope is the strongest known genetic risk factor for seropositive rheumatoid arthritis.

**VCF (Variant Call Format).** A tab-delimited text format for genomic variants. Each row is one variant with chromosome, position, reference allele, alternate allele, quality, filter status, and additional annotations. The standard interchange format between variant-calling pipelines and downstream analysis tools.

**Whole-exome sequencing (WES).** Sequencing limited to the protein-coding regions of the genome (approximately 1.5% of the total genome). The clinical default for hereditary-disease workup when the suspected disorder is broad enough that gene-panel testing is insufficient.

**Whole-genome sequencing (WGS).** Sequencing of the entire genome, including non-coding regions. More comprehensive than WES but more expensive and produces more variants of uncertain significance. The default for research and increasingly used clinically for specific indications.
