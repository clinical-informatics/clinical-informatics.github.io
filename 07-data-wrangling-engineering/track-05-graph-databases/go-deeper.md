# Go deeper: Graph databases

**If you want to learn Cypher and the graph model before moving on:**

- The [Neo4j Cypher manual](https://neo4j.com/docs/cypher-manual/current/) is the canonical reference for the language. The introduction and pattern-matching chapters cover the syntax demonstrated in this track at the level needed to write production queries.
- The [Graph Databases book by Robinson, Webber, and Eifrem](https://neo4j.com/graph-databases-book/) is the standard introduction to the data model itself. It is published by O'Reilly and is freely available in digital form from Neo4j.

**If you want to see graphs applied to clinical data:**

- The [SNOMED CT browser](https://browser.ihtsdotools.org/) lets you traverse the SNOMED is-a hierarchy interactively. Start at "Rheumatoid arthritis" and follow the parents and children to see the traversal example from this track on the real ontology.
- [PrimeKG](https://www.nature.com/articles/s41597-023-01960-3) is a precision-medicine knowledge graph published in Scientific Data in 2023 that integrates 20 biomedical resources (drugs, diseases, phenotypes, genes, pathways) into a single graph. It is a worked example of the graph model at the scale and shape clinical informatics is moving toward.

**If you want to go significantly further:**

- The [Awesome Knowledge Graphs in Healthcare list](https://github.com/Accenture/AmpliGraph) and similar curated lists collect the major clinical knowledge graph projects and the software used to build them. The list is a useful starting point for surveying the field.
- For the relational alternative on OMOP, the [OMOP `concept_ancestor` table](https://ohdsi.github.io/CommonDataModel/cdm54.html#CONCEPT_ANCESTOR) is the pre-computed transitive closure of SNOMED's is-a hierarchy. It supports ancestor and descendant queries directly in SQL without a graph database, at the cost of storing the closure rather than the edges.
