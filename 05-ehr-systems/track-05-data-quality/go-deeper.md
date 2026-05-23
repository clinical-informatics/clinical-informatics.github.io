# Go deeper: real-world data quality problems

## If you want to understand this better before moving on

**Weiskopf NG, Weng C. "Methods and dimensions of electronic health record data quality assessment: enabling reuse for clinical research." *Journal of the American Medical Informatics Association*, 2013.** [https://pubmed.ncbi.nlm.nih.gov/22733976/](https://pubmed.ncbi.nlm.nih.gov/22733976/)

The framework this track is built on. Free via PubMed. The paper reviews the published literature on EHR data quality assessment and lands on the five dimensions (completeness, correctness, concordance, plausibility, currency) the track uses. Worth reading once for the vocabulary; worth reading a second time when you are about to write a data-quality plan for an actual project.

## If you want to see this applied clinically

**Kahn MG, Callahan TJ, Barnard J, et al. "A harmonized data quality assessment terminology and framework for the secondary use of electronic health record data." *eGEMs (Generating Evidence and Methods to improve patient outcomes)*, 2016.** [https://pubmed.ncbi.nlm.nih.gov/27713905/](https://pubmed.ncbi.nlm.nih.gov/27713905/)

The Kahn framework is the most-used operational extension of Weiskopf-Weng. The paper proposes three categories (Conformance, Completeness, Plausibility) with multiple subcategories each, and ties them to the actual checks that the OHDSI Achilles tool implements. If you are going to run a data quality assessment on a real extract, this paper plus Weiskopf-Weng is the two-paper reading list. Free via PubMed.

## If you want to go significantly further

**The OHDSI Achilles characterization tool, with documentation.** [https://ohdsi.github.io/Achilles/](https://ohdsi.github.io/Achilles/)

Achilles is the operational data-quality tool the OHDSI community uses to characterize any OMOP-CDM database. It runs hundreds of pre-defined data-quality checks against a CDM-mapped dataset and produces an HTML report. The documentation is the cleanest worked example of the Kahn framework above turned into actual code. Free, open source, and runnable against a sample OMOP dataset to see what the output looks like. The right tutorial for any informaticist who is about to be responsible for an institutional data-quality pipeline.
