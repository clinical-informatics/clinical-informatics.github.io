# Glossary: 07 Data wrangling and engineering

Terms introduced or extensively used in this course. Curriculum-wide terms are defined in the [start-here glossary](../start-here/GLOSSARY.md).

## Standards

- **Code standard.** An agreement that one clinical fact carries one stable identifier across every system that conforms. LOINC, SNOMED CT, ICD-10-CM, CPT, RxNorm, and NDC are the standards present in a US clinical warehouse.
- **LOINC.** Logical Observation Identifiers Names and Codes. The standard for lab tests and clinical observations. Maintained by the Regenstrief Institute.
- **SNOMED CT.** Systematized Nomenclature of Medicine, Clinical Terms. The standard for clinical findings, problems, procedures, and anatomy.
- **ICD-10-CM.** International Classification of Diseases, 10th revision, Clinical Modification. The US standard for billing diagnoses. Distinct from ICD-10 (international) and ICD-10-PCS (US inpatient procedures).
- **CPT.** Current Procedural Terminology. The US standard for procedures and professional services. Published by the AMA.
- **RxNorm.** The US standard for medications at the ingredient and product level. Maintained by the National Library of Medicine.
- **NDC.** National Drug Code. The FDA standard for dispensed drug packages.
- **Value set.** A curated, authored list of codes from one or more vocabularies that defines a clinical concept for a specific purpose (for example, the codes that count as "rheumatoid arthritis" for a registry).
- **Crosswalk.** A mapping between codes in different vocabularies that represent the same clinical fact.

## OMOP

- **OMOP CDM.** Observational Medical Outcomes Partnership Common Data Model. A fixed schema for clinical data: the same tables and columns at every conforming institution, with values drawn from a shared vocabulary.
- **concept_id.** An integer identifier from the OMOP vocabulary that uniquely identifies a clinical fact. Every clinical row in every OMOP clinical table carries one or more concept_id columns.
- **Standard concept.** The OMOP vocabulary's canonical representation of a clinical entity. Marked with `standard_concept = 'S'` in the concept table. For conditions, the standard concept is typically SNOMED-aligned; for labs, LOINC-aligned; for drugs, RxNorm-aligned.
- **Source concept.** The OMOP representation of the original code from the source EHR. Stored in `<thing>_source_concept_id`. Distinct from the standard concept; both are kept on every row.
- **Source value.** The original string from the source EHR, preserved verbatim. Stored in `<thing>_source_value`. Used for audit and for any query that needs the original encoding.
- **person, visit_occurrence, condition_occurrence, drug_exposure, measurement, observation.** The six core clinical tables of OMOP CDM v5.4.
- **concept_ancestor.** A pre-computed transitive closure of the SNOMED is-a hierarchy, exposed as a relational table in OMOP. Supports ancestor and descendant queries in SQL.
- **Athena.** OHDSI's web-based vocabulary browser. The standard tool for resolving a concept_id to its full metadata.

## Analytic layers

- **Extraction layer.** The SQL query that produces the analytic cohort from the warehouse. Runs on the warehouse engine and returns a flat tabular result.
- **Post-extraction layer.** The DataFrame library (pandas, DuckDB, polars, dplyr) used for tidying, per-patient summaries, and analysis after the cohort has been extracted.
- **DuckDB.** An in-process SQL engine that reads CSV, Parquet, and Arrow files without loading them entirely into RAM. The natural choice when the cohort exceeds memory and the operations are SQL-shaped.
- **polars.** A Python and Rust DataFrame library with lazy evaluation and parallel execution. The natural choice when pandas is too slow on a recurring pipeline.
- **dplyr.** The verb-based DataFrame library for R. The natural choice when downstream work is in R.
- **Window function.** A SQL construct that computes a value per row using a window of related rows defined by `PARTITION BY` and `ORDER BY`. Used in this course for last-value-per-patient queries.
- **Common Table Expression (CTE).** A named subquery defined with `WITH` and reused in the main query. Used to separate the logic of a multi-step query into readable pieces.

## Graph databases

- **Node.** An entity in a graph database. Carries a label (its type) and properties (key-value attributes).
- **Edge.** A relationship between two nodes. Directed and typed; carries its own properties.
- **Property.** A key-value pair attached to a node or an edge.
- **Traversal.** Walking from one node to another along the graph's edges. Variable-length traversal walks the same edge type some unspecified number of times.
- **Cypher.** The query language most widely used for graph databases. Pattern-matching syntax with parentheses for nodes, square brackets for edges, arrows for direction.
- **Neo4j, Memgraph, Amazon Neptune, ArangoDB.** Production graph databases. Each fits a different operational context.

## Cohort definition

- **Cohort.** The set of patients who meet a defined inclusion criterion. Defined by a query against the warehouse.
- **Phenotype.** A computable definition of a clinical condition for the purpose of cohort identification. Includes the value sets used and the rules that combine them.
- **Person-time.** The denominator for incidence rates. Sum of follow-up time across all patients in the cohort. Calculated in OMOP from `drug_exposure` or `observation_period` dates.
