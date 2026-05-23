# Glossary: 05 EHR systems

Plain-English definitions for the terms course 05 introduces. The curriculum-wide glossary in the [start-here repo](https://github.com/clinical-informatics/start-here/blob/main/GLOSSARY.md) covers terms shared across multiple courses.

---

**ADT message.** An HL7 v2 message family (admit, discharge, transfer) used inside hospitals to broadcast patient-registration events. The most common message type by volume in any health system. The lab knows a patient is in the hospital because the EHR sent the lab an ADT message.

**Block storage.** A storage architecture where the storage volume looks to the operating system like a raw disk, allowing small in-place updates at any byte offset. The right primitive for database files. Contrast with object storage.

**C-CDA.** Consolidated Clinical Document Architecture. The implementation guide that constrains CDA documents into a small set of US-standard templates (continuity of care document, discharge summary, progress note, and others). Required by Meaningful Use Stage 2.

**CDA.** Clinical Document Architecture. An HL7 v3 XML-based standard for clinical documents. Combines a human-readable narrative section with optional structured-entry sections. The format US EHRs use to ship a continuity of care document from one provider to the next.

**CDW.** Clinical data warehouse. An analytical system designed to live next to the operational EHR. Built around a star schema, optimized for scans and aggregations rather than for the chart.

**Clarity.** Epic's nightly relational extract of its operational data store (Chronicles). The starting point for most Epic-shop analytical pipelines.

**Conformed dimension.** In star-schema design, a dimension table that is the single source of truth used by every fact table. A conformed `dim_patient` means the same patient row joins consistently to every clinical-event fact.

**DICOM.** Digital Imaging and Communications in Medicine. The standard for clinical imaging exchange. Defines a file format (image plus metadata tags), an information model (Patient -> Study -> Series -> Instance), and network protocols (DIMSE and DICOMweb).

**DICOMweb.** The modern web-based service family for DICOM. Three operations: QIDO-RS (search), WADO-RS (retrieve), STOW-RS (store). The imaging-side equivalent of FHIR REST.

**DIMSE.** DICOM Message Service Element. The legacy DICOM network protocol from the early 1990s. Used between imaging modalities and PACS systems for image transfer (C-STORE) and query (C-FIND, C-MOVE).

**DICOM SR.** DICOM Structured Reporting. A DICOM object type that carries clinical findings as structured, coded tree of templated nodes rather than as a PDF narrative. Standardized for BI-RADS, Lung-RADS, PI-RADS, and other RADS-family specialties; less common outside them.

**EAV.** Entity-attribute-value. A storage pattern where instead of one column per attribute, attributes are stored as rows in a tall table (one row per measurement, with columns for the patient, the measurement name, and the value). Used in every EHR for flowsheets. Trades query convenience for schema flexibility.

**ELT.** Extract, Load, Transform. The newer ordering of the data-pipeline operations, where raw data is loaded into the warehouse first and transformed in place using warehouse compute. Contrast with ETL.

**ETL.** Extract, Transform, Load. The classic ordering of data-pipeline operations: transform data on an intermediate server before loading the transformed result into the warehouse. Contrast with ELT.

**Fact table.** In a star schema, the central table holding the measurable clinical events (one row per lab result, encounter, medication administration, claim). Carries numeric measures and foreign keys to the dimensions.

**Flowsheet.** The EHR's high-frequency-measurement capture surface. Vitals, intake and output, ventilator settings, ICU monitoring, joint counts, pain scales. Always stored as EAV under the hood.

**HL7 v2.** Health Level Seven version 2. The pipe-and-caret message-based standard for inter-system clinical messaging, in continuous use since 1987. Most traffic inside a hospital today still moves over HL7 v2.

**Index.** A separate data structure (commonly a B-tree) that lets the database find rows by a particular column without scanning the whole table. Operational EHRs are aggressively indexed for chart access patterns, sparsely indexed for population queries.

**Interface engine.** The hub-and-spoke routing system (Rhapsody, Mirth Connect, Cloverleaf, Intersystems HealthShare) that handles inter-system clinical messaging. The post office of the hospital's clinical network.

**Lakehouse.** A storage architecture that uses cheap object storage as the physical layer (like a data lake) with a transactional table layer on top (Delta, Iceberg, Hudi) that adds ACID transactions and schema enforcement (like a warehouse). The converging pattern as of the mid-2020s.

**Modality Worklist.** A DICOM service the RIS provides to each imaging modality. When a patient arrives, the radiographer queries the worklist on the device, picks the matching order, and the device pre-populates Patient Name, MRN, and Accession Number on the DICOM header automatically.

**Object storage.** A storage architecture where the unit is an entire object (a file). Write once, read whole, never patch a byte in the middle. Addressed by long string keys. Scales to petabytes cheaply. Amazon S3 is the canonical example.

**OLAP.** Online analytical processing. The workload of the clinical data warehouse: scan-heavy queries, aggregations across many rows, joins across many tables, multi-second response acceptable.

**OLTP.** Online transaction processing. The workload of the operational EHR: many small, fast, in-place reads and writes, sub-second response, lookups by primary key. The chart is OLTP.

**ORM message.** An HL7 v2 message family for orders. The EHR sends an ORM to the radiology system or the lab when a study or a test is ordered.

**ORU message.** An HL7 v2 message family for observation results. The lab sends an ORU to the EHR when results land.

**PACS.** Picture Archiving and Communication System. The imaging-side database. Stores DICOM instances, indexes them by patient and study identifier, handles tiering across hot, warm, and cold storage, and serves images to viewers.

**RIS.** Radiology Information System. The workflow layer between the EHR and the imaging hardware. Manages orders, scheduling, Modality Worklists, dictation, and the final report flow back to the EHR.

**RPO.** Recovery point objective. The maximum amount of data the hospital is willing to lose if a disaster strikes. An RPO of 5 minutes means transaction logs ship to the disaster-recovery site every 5 minutes.

**RTO.** Recovery time objective. The maximum amount of time the hospital is willing to be without the EHR after a disaster. An RTO of 30 minutes means the cutover plan must bring an alternate environment up in 30 minutes.

**Schema on read.** The data-lake property of imposing schema at query time. Raw files (CSV, JSON, Parquet, FHIR bundles, DICOM blobs) live in storage as-is; the query engine parses them when read. Contrast with schema on write.

**Schema on write.** The data-warehouse property of enforcing schema at load time. Every row that lands in the warehouse has been conformed to a pre-defined table structure. Cleaner to query, more rigid to evolve.

**SCD.** Slowly changing dimension. A dimensional-modeling pattern for handling attributes that change over time. SCD Type 2, the most common, keeps the historical row and adds a new row when an attribute changes, with `valid_from` and `valid_to` columns letting fact rows join back to the dimension state that was true at the time of the event.

**SOP class.** In DICOM, the Service-Object Pair class identifier that tells a receiving system what kind of object a file is. `1.2.840.10008.5.1.4.1.1.1.1` is the SOP Class for Digital X-Ray Image, for example.

**Star schema.** The dominant logical design for clinical data warehouses. One fact table per clinical domain (lab results, encounters, drug exposures), surrounded by dimension tables (patient, provider, date, location). Named for the resulting entity-relationship diagram.

**Study Instance UID.** In DICOM, the persistent identifier for an imaging study. Long string (like `1.2.840.113619.2.55.3.604688334.123.1722777200.1`), globally unique, stable forever. The handle systems use to refer to a study.

**Value set.** A curated list of codes from one or more code systems that all express the same concept. The query strategy that handles inconsistent coding: filter on the value set, not on a single code.

**VNA.** Vendor-neutral archive. An institutional long-term imaging store, often cloud-based, that holds DICOM data from every department's PACS in one repository. Handles cross-vendor compatibility and cross-departmental access.

**Weiskopf-Weng framework.** The five-dimension model of EHR data quality (completeness, correctness, concordance, plausibility, currency) from Weiskopf and Weng's 2013 JAMIA review. The standard reference for clinical data-quality assessment.

**Z-segment.** An HL7 v2 segment that begins with the letter Z and is reserved by the standard for site-specific extensions. Valid v2 but non-portable: a Z-segment is a private dialect that other systems cannot parse without local knowledge.
