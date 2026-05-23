# Track 03: How computers represent and store data

When the EHR is slow on Tuesday morning, the right person to ask depends on whether the bottleneck is the database, the network, or the application. When a research request takes nine weeks, the reason usually lives in a difference between two storage systems that were designed for different jobs. When a vendor says their tool can ingest *any format*, they mean four of them. This track gives you the vocabulary for those conversations.

The track moves through five short pieces.

1. **Bits and bytes.** The substrate underneath everything else. The most common source of quietly wrong clinical analyses (number-as-number versus number-as-text) named here, deepened in Course 02.
2. **Four data structures at concept level.** Tables (most clinical data), trees (problem lists, SNOMED CT, ICD-10), graphs (drug-interaction networks, knowledge graphs), key-value (FHIR Bundle indexing, session caches). Each shape matched to the kind of clinical data it holds.
3. **Four file types most clinical data lives in.** TXT, CSV, JSON, XML. One-screen example of each. The honest comparison: JSON won most new work, XML still appears anywhere CDA is in use, CSV is forever, TXT is for things humans read.
4. **File vs database, and relational concept.** What a database gives you that a folder of files does not (constraints, concurrency, query optimization), and what *relational* means.
5. **OLTP vs OLAP from the health-system standpoint.** The EHR is transactional; the CDW is analytical. Two databases because two jobs cannot share one. The single most useful piece of vocabulary the track teaches.

The track closes with a pick-the-right-format exercise across four clinical scenarios (a discharge summary, a single in-flight lab result, a complete FHIR Bundle, and a year of claims) and names the pattern under the answers: the format choice is usually about the pipe between the two systems, not about the content itself.

**Prerequisites:** Track 02 (the lifecycle frames why data-at-rest matters in the first place).

**How to start:** open `notebook.py` from the file tree on the left.

**What's next:** Track 04 (how computers move data).
