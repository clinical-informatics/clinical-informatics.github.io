"""Track 02: Genomic data structures and file types.

Five file types account for most of the genomic-data pipeline a clinical
informaticist will encounter. The track walks each in the order it
appears in the sequencer-to-report pipeline, shows a representative
snippet, and closes with an interactive format-identifier exercise.
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
        "07": "Data wrangling and engineering",
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
        # Track 02: Genomic data structures and file types

        ## The sequencer-to-report pipeline

        A modern next-generation-sequencing-based test follows the same shape regardless of the clinical question. The sequencer produces raw reads in FASTQ format. The reads are aligned to a reference genome, producing a BAM file. The aligned reads are scanned for differences from the reference, producing a VCF file of variant calls. The variants are annotated with their genomic context (gene, exon, regulatory region) from a GFF or GTF annotation file, and with the target regions of the test from a BED file. The annotated variants are filtered and interpreted, and a clinical report is generated.

        Five file types cover almost all of that pipeline. A clinical informaticist who can recognize each format from a short snippet and name what it contains can read most clinical-genomics-pipeline documentation, work with the bioinformatics core on a clinical-genomics integration, and audit a vendor's clinical-genomics workflow. The track walks each one in pipeline order.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## FASTQ: raw sequencing reads

        FASTQ is the format the sequencer produces. Each read appears as four lines: a header (line starts with `@`), the sequence itself, a separator (line starts with `+`), and a per-base quality string. The quality string encodes a per-position confidence in the called base; the position-by-position match between the sequence and the quality string is exact.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Representative snippet

        ```
        @SRR8615624.1 NS500644:155:HM2GVAFXY:1:11101:5879:1031 length=76
        NTCCAGTGAAAGCAGGAACATGAGAATCCACCTACCGGAAATAGATAGGAAAACTGGACCATGAACAACTGCAGTAA
        +
        #AAAAFAFFFAFAFFFFFAFAAFFFFAFFFFAFFFFFFFFAFFFFFFFFFFFFAFFFFFFFFFFFFFFAFAAFAFF
        ```

        Read this top-to-bottom.

        - **Line 1 (`@SRR8615624.1 ...`)**: the read identifier. SRR8615624 is the run accession from the NCBI Sequence Read Archive; `.1` is the first read in the run. The rest of the line is the instrument metadata (NextSeq 500 sequencer, flow cell ID, position).
        - **Line 2 (`NTCCAGT...`)**: the 76-base sequence the sequencer called. The `N` at position 1 means the sequencer could not call a base at that position; the rest are A, C, G, T calls.
        - **Line 3 (`+`)**: the separator. Sometimes carries the identifier again; usually empty.
        - **Line 4 (`#AAAAFAF...`)**: the per-base quality string, one character per base. The characters encode Phred quality scores (a measure of base-calling confidence). The leading `#` (low quality) matches the leading `N` base call.

        FASTQ is large. A clinical exome produces approximately 5 to 20 GB of FASTQ data per sample. The format is the universal handoff from any sequencer to any downstream pipeline.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## BAM: reads aligned to a reference genome

        BAM (Binary Alignment Map) is the binary, indexed form of SAM (Sequence Alignment Map). A BAM file contains the same reads as the input FASTQ, but each read carries its alignment to a reference genome: which chromosome, which position, how the read matches (mismatches, insertions, deletions), and the quality of the alignment.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Representative snippet (SAM text representation; BAM is the binary form)

        ```
        @HD VN:1.6 SO:coordinate
        @SQ SN:chr6 LN:170805979
        @PG ID:bwa PN:bwa VN:0.7.17 CL:bwa mem -t 8 hg38.fa sample_R1.fq sample_R2.fq

        SRR8615624.1  99  chr6  32551887  60  76M  =  32552063  252  TCCAGTGAAAGCAGGAACATG...  AAAAFAFFFAFAFFFFFAFAA...  NM:i:0  MD:Z:76
        ```

        The first three lines are header lines (`@HD` file metadata, `@SQ` reference sequence, `@PG` program-history annotation showing the read was aligned by BWA-MEM 0.7.17).

        The data line is one read. The 11 tab-separated columns are: read ID, alignment flag (99 = paired, properly aligned, mate on reverse strand), chromosome (chr6), position (32,551,887 on chr6, which is in the HLA region), mapping quality (60 = high confidence), CIGAR string (`76M` = 76 bases match the reference), mate-chromosome (`=` = same chromosome), mate-position, template length, the read sequence, the quality string. Optional tag columns at the end carry additional annotations (NM:i:0 = zero mismatches against the reference; MD:Z:76 = 76 matching positions).

        BAM is the intermediate file most downstream tools consume. The clinical-genomics IGV viewer (Integrative Genomics Viewer) opens BAM files and renders the read pile-up around any genomic position; the visual is what a bioinformatician uses to manually inspect a variant call.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## VCF: variant calls

        VCF (Variant Call Format) is the output of the variant-calling stage of the pipeline. Each row is one variant: a position in the genome where the patient's sample differs from the reference.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Representative snippet

        ```
        ##fileformat=VCFv4.2
        ##reference=hg38
        ##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">
        ##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">
        ##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
        ##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">
        #CHROM  POS       ID         REF  ALT  QUAL  FILTER  INFO              FORMAT  SAMPLE1
        chr6    32584259  rs660895   A    G    1500  PASS    DP=145;AF=0.503   GT:DP   0/1:145
        chr6    32584322  rs17887074 C    T    1820  PASS    DP=160;AF=1.000   GT:DP   1/1:160
        chr1    169519049 rs1799963  G    A    1200  PASS    DP=89;AF=0.494    GT:DP   0/1:89
        ```

        The `##` lines are metadata: the file format version, the reference build, the meaning of each INFO and FORMAT field. The `#CHROM` line is the column header. Each subsequent row is one variant.

        Reading the first variant row: chromosome 6, position 32,584,259, dbSNP identifier rs660895, reference allele A, alternate allele G, quality score 1500, FILTER status PASS, INFO column has total depth 145 and alternate allele frequency 0.503, and the sample-specific FORMAT-column-pair says the genotype is 0/1 (heterozygous) at read depth 145.

        Two operational properties of VCF are load-bearing.

        - **One row per variant, one column per sample.** A multi-sample VCF (joint variant calling across a cohort) has one column per sample after the FORMAT column. A family quartet has columns for proband, mother, father, sibling; each row shows the genotype of each family member at that variant.
        - **The INFO column is extensible.** Annotation tools add INFO fields for population frequency from gnomAD, predicted impact from snpEff or VEP, clinical significance from ClinVar. A heavily annotated clinical VCF can have 50 or more INFO fields per variant.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## GFF / GTF: genomic annotations

        GFF (General Feature Format) and GTF (Gene Transfer Format, a tighter GFF subset) are tab-delimited annotation formats. Each row describes one feature in the genome: a gene, an exon, a regulatory element, a transcription-factor binding site, anything with a defined start and end position.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Representative GTF snippet (Ensembl-style)

        ```
        chr6 ensembl_havana gene       32584000 32595000 . + . gene_id "ENSG00000196126"; gene_name "HLA-DRB1"; gene_biotype "protein_coding";
        chr6 ensembl_havana transcript 32584000 32595000 . + . gene_id "ENSG00000196126"; transcript_id "ENST00000360004"; gene_name "HLA-DRB1";
        chr6 ensembl_havana exon       32584000 32584252 . + . gene_id "ENSG00000196126"; transcript_id "ENST00000360004"; exon_number "1";
        chr6 ensembl_havana exon       32585520 32585788 . + . gene_id "ENSG00000196126"; transcript_id "ENST00000360004"; exon_number "2";
        ```

        Each row has nine fields: chromosome, source, feature type, start, end, score, strand, frame, and the attributes column.

        The attributes column carries the gene-and-transcript identifiers. Reading the first row: this is a protein-coding gene named HLA-DRB1 on chromosome 6 from position 32,584,000 to 32,595,000 on the forward strand, with Ensembl gene identifier ENSG00000196126. The subsequent rows are the transcript and the exons that make up this gene.

        GFF and GTF are used to translate a variant's genomic position into its biological context. A variant at chr6:32584259 is inside the HLA-DRB1 gene; the same variant is in the first exon (positions 32584000 to 32584252). The annotation tool consults the GFF/GTF to make this translation.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## BED: genomic regions

        BED (Browser Extensible Data) is the simplest of the five formats. Each row is one region in the genome: chromosome, start, end, and (optionally) a name and a score.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Representative snippet

        ```
        chr6  32584000  32595000  HLA-DRB1_capture
        chr6  29942000  29945000  HLA-A_capture
        chr1  169519000 169519200 F5_factor5
        chr11 26354000  26365000  TPMT_exon3
        ```

        Four columns: chromosome, start (0-based), end (1-based), name. Each row describes one region the test targets.

        BED is most often used to define the regions a clinical sequencing test covers (the "capture kit" for an exome, the "panel" for a targeted gene panel). A clinical-laboratory's BED file is the operational definition of what the test can and cannot detect; a variant in a gene that is not in the BED file will not be sequenced and therefore cannot be called. The BED file is the cleanest single artifact for understanding a clinical-genomics test's scope.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The pipeline summary

        The five formats fit together in a fixed pipeline order. The table below names each format, what it contains, and at which pipeline stage it appears.
        """
    )
    return


@app.cell
def _(pd):
    pipeline_summary = pd.DataFrame(
        [
            {"Format": "FASTQ", "Stage": "1. Raw sequencer output", "What it contains": "Reads with per-base quality scores. No alignment, no biological context.", "Approximate size per clinical exome": "5 to 20 GB"},
            {"Format": "BAM", "Stage": "2. Aligned reads", "What it contains": "Reads with their alignment to a reference genome.", "Approximate size per clinical exome": "10 to 30 GB"},
            {"Format": "VCF", "Stage": "3. Variant calls", "What it contains": "Positions where the sample differs from the reference, with quality and population annotations.", "Approximate size per clinical exome": "10 to 50 MB (annotated)"},
            {"Format": "GFF / GTF", "Stage": "Reference annotation (used at variant-annotation step)", "What it contains": "Gene, transcript, and exon coordinates against the reference.", "Approximate size per clinical exome": "1.5 GB (full Ensembl human annotation)"},
            {"Format": "BED", "Stage": "Test region definition (used at multiple stages)", "What it contains": "Genomic regions a test targets.", "Approximate size per clinical exome": "Less than 1 MB"},
        ]
    )
    pipeline_summary.index = range(1, len(pipeline_summary) + 1)
    pipeline_summary.index.name = "row"
    pipeline_summary
    return (pipeline_summary,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Interactive: format identifier

        Five snippets below. For each, pick the format you think it is. The reveal at the end compares against the correct answer.
        """
    )
    return


@app.cell
def _():
    snippets = [
        ("Snippet A", "```\n@SRR1234567.5 length=100\nACTGGATCAGTAATCGAGCTATCCAGCT\n+\nFFAFAFFAFFAFFAFFFAFFFFFAFAFF\n```"),
        ("Snippet B", "```\nchr17  41197695  41197800  BRCA1_exon10\nchr17  41209068  41209152  BRCA1_exon11\n```"),
        ("Snippet C", "```\nchr11 ensembl gene 26352000 26367000 . + . gene_id 'ENSG00000137364'; gene_name 'TPMT';\n```"),
        ("Snippet D", "```\n#CHROM POS ID REF ALT QUAL FILTER INFO\nchr11 26365000 rs1142345 C T 1820 PASS DP=120;AF=0.502\n```"),
        ("Snippet E", "```\n@HD VN:1.6 SO:coordinate\nSRR1234567.5 99 chr17 41197900 60 100M = 41198021 121 ACTGGATCAGT... FFAFAFFAFFAF...\n```"),
    ]
    return (snippets,)


@app.cell
def _(mo):
    snippet_a_pick = mo.ui.radio(options=["FASTQ", "BAM/SAM", "VCF", "GFF/GTF", "BED"], label="Snippet A")
    snippet_b_pick = mo.ui.radio(options=["FASTQ", "BAM/SAM", "VCF", "GFF/GTF", "BED"], label="Snippet B")
    snippet_c_pick = mo.ui.radio(options=["FASTQ", "BAM/SAM", "VCF", "GFF/GTF", "BED"], label="Snippet C")
    snippet_d_pick = mo.ui.radio(options=["FASTQ", "BAM/SAM", "VCF", "GFF/GTF", "BED"], label="Snippet D")
    snippet_e_pick = mo.ui.radio(options=["FASTQ", "BAM/SAM", "VCF", "GFF/GTF", "BED"], label="Snippet E")
    return snippet_a_pick, snippet_b_pick, snippet_c_pick, snippet_d_pick, snippet_e_pick


@app.cell
def _(mo, snippets):
    mo.md(f"### {snippets[0][0]}\n\n{snippets[0][1]}")
    return


@app.cell
def _(snippet_a_pick):
    snippet_a_pick
    return


@app.cell
def _(mo, snippets):
    mo.md(f"### {snippets[1][0]}\n\n{snippets[1][1]}")
    return


@app.cell
def _(snippet_b_pick):
    snippet_b_pick
    return


@app.cell
def _(mo, snippets):
    mo.md(f"### {snippets[2][0]}\n\n{snippets[2][1]}")
    return


@app.cell
def _(snippet_c_pick):
    snippet_c_pick
    return


@app.cell
def _(mo, snippets):
    mo.md(f"### {snippets[3][0]}\n\n{snippets[3][1]}")
    return


@app.cell
def _(snippet_d_pick):
    snippet_d_pick
    return


@app.cell
def _(mo, snippets):
    mo.md(f"### {snippets[4][0]}\n\n{snippets[4][1]}")
    return


@app.cell
def _(snippet_e_pick):
    snippet_e_pick
    return


@app.cell
def _(
    mo,
    snippet_a_pick,
    snippet_b_pick,
    snippet_c_pick,
    snippet_d_pick,
    snippet_e_pick,
):
    answers = {
        "Snippet A": "FASTQ",
        "Snippet B": "BED",
        "Snippet C": "GFF/GTF",
        "Snippet D": "VCF",
        "Snippet E": "BAM/SAM",
    }
    picks = {
        "Snippet A": snippet_a_pick.value,
        "Snippet B": snippet_b_pick.value,
        "Snippet C": snippet_c_pick.value,
        "Snippet D": snippet_d_pick.value,
        "Snippet E": snippet_e_pick.value,
    }
    n_picked = sum(1 for v in picks.values() if v is not None)
    if n_picked == 0:
        verdict = mo.md("_Pick an answer for each snippet to see the reveal._")
    else:
        rows = []
        n_correct = 0
        for k, v in picks.items():
            correct = answers[k]
            mark = "(no answer)" if v is None else ("CORRECT" if v == correct else f"picked {v}, correct is {correct}")
            if v == correct:
                n_correct += 1
            rows.append(f"- **{k}**: {mark}")
        verdict = mo.callout(
            mo.md(f"**Score: {n_correct} of {n_picked} picked correctly.**\n\n" + "\n".join(rows)),
            kind="success" if n_correct == n_picked and n_picked == 5 else ("info" if n_correct >= 3 else "warn"),
        )
    verdict
    return answers, n_correct, n_picked, picks, rows, verdict


@app.cell
def _(xref):
    xref.callback(
        "20",
        "00",
        "File types in general",
        "Course 00 Track 3 introduced the general framework for files and file types. The five genomic formats in this track are domain-specific instances of the same general categories Course 00 covered (text-with-structure for FASTQ / VCF / GFF / BED, binary for BAM).",
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "20",
        "02",
        "Data types and tidy data",
        "Course 02 Track 2 introduced tidy-data conventions (one fact per row). VCF is a tidy data structure (one variant per row, one annotation column per attribute); GFF is similar. A clinical informaticist working with VCF data in pandas can read it as a TSV and apply Course 07 pandas idioms directly.",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "20",
        "07",
        "Working with VCFs in pandas / SQL",
        "Course 07 covered pandas, SQL, and DuckDB. A VCF can be read into pandas as a tab-delimited file (after skipping the header lines starting with ##). DuckDB and pyranges are common tools for handling the GFF/GTF/BED annotation joins at scale.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        Five file types account for almost all of the genomic-data pipeline a clinical informaticist will encounter. FASTQ is the raw sequencer output (reads with quality scores); BAM is the aligned reads (with per-read genomic positions); VCF is the variant calls (one row per variant, INFO column extensible with annotations); GFF / GTF is the reference annotation (gene, transcript, exon coordinates); BED is the test-region definition (one row per region). The five fit into a fixed pipeline order. The interactive identifier above gave the reader practice recognizing each format from a short snippet.

        Track 03 takes up the clinical-genomics-in-the-EHR side: how the variant call that comes out of the pipeline is reported back to the EHR, and the PDF-vs-structured-field gap that defines the operational state of most US clinical-genomics deployments today.
        """
    )
    return


if __name__ == "__main__":
    app.run()
