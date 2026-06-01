# Go deeper: Genomic data structures and file types

**If you want to understand the file formats better before moving on:**

- [The samtools / htslib documentation](https://www.htslib.org/) is the canonical reference for SAM, BAM, CRAM, VCF, and BCF formats. The format specifications are linked from the same page; reading the SAM specification end-to-end is the standard rite of passage for anyone working with sequencing data at the file level.
- [The UCSC Genome Browser's "File formats" page](https://genome.ucsc.edu/FAQ/FAQformat.html) covers BED, GFF, GTF, WIG, and the other annotation formats with worked examples. The UCSC page is the most accessible single reference for the annotation side of the genomic-data ecosystem.

**If you want to see this applied clinically:**

- [The GATK Best Practices documentation (Broad Institute)](https://gatk.broadinstitute.org/hc/en-us/sections/360007226651-Best-Practices-Workflows) is the canonical reference workflow for going from raw sequencing reads (FASTQ) to clinically usable variant calls (VCF). Reading the Best Practices workflow end-to-end is the fastest way to see how the file formats fit together in the production pipeline.

**If you want to go significantly further:**

- [The IGV (Integrative Genomics Viewer) at the Broad Institute](https://software.broadinstitute.org/software/igv/) is the standard interactive viewer for BAM, VCF, BED, and the other formats. Loading a representative BAM file and a matching VCF in IGV and walking the alignment around a variant call is the standard hands-on exercise for understanding what each format actually contains at the byte level.
