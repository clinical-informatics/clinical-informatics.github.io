# Go deeper: how EHRs structure data internally

Three resources, vetted and free at time of writing.

## If you want to understand this better before moving on

**The Book of OHDSI, Chapter 4: The Common Data Model.** [https://ohdsi.github.io/TheBookOfOhdsi/CommonDataModel.html](https://ohdsi.github.io/TheBookOfOhdsi/CommonDataModel.html)

Chapter 4 of The Book of OHDSI walks the OMOP common data model table by table: `person`, `visit_occurrence`, `condition_occurrence`, `drug_exposure`, `measurement`, `observation`. We get to OMOP in course 07. The reason this chapter is the right early read after Track 01 is that the OMOP authors explicitly chose their schema in opposition to the operational EHR's schema, and the writing makes every trade-off visible. Reading the operational schema first (Track 01) and then the OMOP schema makes the design choices on both sides legible in a way neither does alone.

## If you want to see this applied clinically

**Hripcsak G, et al. "Observational Health Data Sciences and Informatics (OHDSI): Opportunities for Observational Researchers." *Studies in Health Technology and Informatics*, 2015.** [https://pubmed.ncbi.nlm.nih.gov/26262116/](https://pubmed.ncbi.nlm.nih.gov/26262116/)

The OHDSI consortium paper, free via PubMed. Short, pragmatic, and useful for one reason in particular: it makes the operational-versus-analytical distinction concrete on a federated network of hundreds of millions of patients. The paper says, explicitly, what most clinicians have suspected for years, that the same clinical question asked of two hospitals' EHRs will return two incompatible answers without a common data model in between.

## If you want to go significantly further

**Designing Data-Intensive Applications, by Martin Kleppmann (O'Reilly, 2017).** The first three chapters in particular: data models, storage and retrieval, and encoding. Free preview chapters are available on the publisher site, and many institutions provide full access through O'Reilly Online Learning. Not clinical; covers the underlying database concepts (B-trees and LSM-trees, transactions and isolation, replication and partitioning) at a depth that most clinical informatics writing assumes you already have. If you ever want to read a vendor's storage architecture diagram with confidence, this book is the most efficient route there.
