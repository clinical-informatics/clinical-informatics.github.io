# Go deeper: OMOP Common Data Model

**If you want to understand OMOP better before moving on:**

- The [Book of OHDSI chapter on the Common Data Model](https://ohdsi.github.io/TheBookOfOhdsi/CommonDataModel.html) is the most accessible end-to-end explanation. It covers the design principles, the standardized vocabularies, and the rationale for the dual concept_id structure used throughout this track.
- The [OMOP CDM v5.4 specification](https://ohdsi.github.io/CommonDataModel/cdm54.html) is the canonical reference for every table, column, and required-vs-optional field. Use it when you need to confirm the exact definition of a column.

**If you want to see this applied clinically:**

- [Athena](https://athena.ohdsi.org/) is the OHDSI vocabulary browser. Look up the concept_ids from Reyes's record (`4138406`, `40766949`, `1503297`) to see the full concept metadata, the vocabulary the concept came from, and the relationships to other concepts.
- The [Book of OHDSI chapter on Defining Cohorts](https://ohdsi.github.io/TheBookOfOhdsi/Cohorts.html) shows how the OMOP schema enables phenotype definitions that run unchanged across institutions. The chapter ends with a phenotype the OHDSI consortium has validated against multiple data sources.

**If you want to go significantly further:**

- [HADES](https://ohdsi.github.io/Hades/) is the OHDSI R package ecosystem that runs analyses directly against OMOP databases. The `PatientLevelPrediction` and `CohortMethod` packages demonstrate the kinds of network studies the standardized schema makes possible.
- The [OHDSI Tutorials repository](https://www.ohdsi.org/educational-resources/tutorials/) hosts the materials from the OHDSI in-person workshops. The "OHDSI in 5 Days" series is the deepest free curriculum.
