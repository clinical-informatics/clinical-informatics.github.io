# Glossary: 00 Foundations of clinical informatics

Plain-English definitions of the terms this course introduces, or that it treats in a particular way. The curriculum-wide glossary lives in the [start-here repo](https://github.com/clinical-informatics/start-here/blob/main/GLOSSARY.md). If a term shows up in your reading and isn't here, check there.

If you can't find it in either place, open an issue. The glossary is a living artifact.

---

**ACO (Accountable Care Organization).** A group of doctors, hospitals, and other providers who come together voluntarily to coordinate care for a defined population of patients (often Medicare beneficiaries). The ACO shares in savings if it beats spending and quality benchmarks, and bears risk if it does not. The capstone scenario is built around an ACO.

**AMC (Academic Medical Center).** A large, university-affiliated hospital with a strong teaching and research mission. Most U.S. AMCs run Epic. Track 05.

**AMIA (American Medical Informatics Association).** The professional society for clinical and biomedical informatics in the U.S. Owns the major academic journals in the field (JAMIA, JAMIA Open) and runs the field's annual research symposium. Track 06.

**API (Application Programming Interface).** The documented menu of requests a system will accept. The FHIR API for an EHR is a written specification of which clinical resources you can ask for, how to ask, and what you will get back. Track 04.

**BAA (Business Associate Agreement).** A contract under HIPAA that allows a *business associate* (a vendor, a third-party tool, a cloud provider) to handle Protected Health Information on behalf of a *covered entity* (a hospital, a clinician). Most cloud-based clinical work begins with a BAA. Tracks 04 and 05.

**Bit.** A single piece of information that can be in one of two states (0 or 1). Eight bits make a byte. The substrate every other concept in Track 03 sits on.

**CDA (Clinical Document Architecture).** The HL7 XML standard for clinical documents (discharge summaries, continuity-of-care summaries, lab reports). HITECH-era exchanges were built on CDA. Track 03.

**CDS (Clinical Decision Support).** Software that helps clinicians decide things in the workflow. Alerts, reminders, order sets, embedded calculators, predictive scores. Course 12 is the deep dive.

**CDW (Clinical Data Warehouse).** The OLAP database alongside the EHR, restructured for analytic queries. Track 03.

**Client-server.** The architectural pattern in which one program (the *client*) makes requests and another (the *server*) answers them. Almost every clinical system you interact with is one role or the other. Track 04.

**CMS (Centers for Medicare and Medicaid Services).** Federal agency inside HHS that runs Medicare and Medicaid and sets payment and quality rules that shape most of U.S. healthcare. Track 05.

**CMIO (Chief Medical Information Officer).** The senior physician executive responsible for clinical use of information systems in a health system. Track 06.

**CNIO (Chief Nursing Information Officer).** The senior nursing informatics executive. Track 06.

**Cohort.** The set of patients a rule, a query, or a study is about. A poorly defined cohort is the most common single source of clinical decision support failure (Track 01 of `01-computational-thinking`).

**CRIO (Chief Research Information Officer).** The senior executive responsible for the research use of clinical data. Track 06.

**CSV (Comma-Separated Values).** The lingua franca file format for tabular data. Strengths: simple, universally supported. Weaknesses: no nesting, no built-in type information. Track 03.

**Data.** The raw signal. A measurement faithfully recorded with the metadata that tells you what was measured, when, and in what units. The bottom layer of DIKW. Track 02.

**DIKW.** Data, information, knowledge, wisdom. The hierarchy the field borrowed from the broader information sciences for naming what is happening at each layer when a clinical signal is interpreted. Track 02 walks each layer, with Frické's 2009 critique cited honestly.

**EHR (Electronic Health Record).** The clinical system clinicians use to document care, place orders, and read results. Almost every U.S. hospital has one; HITECH 2009 is the reason. Track 01.

**EULAR.** European Alliance of Associations for Rheumatology. Publishes the rheumatology treatment recommendations the rheumatologist in Ms. Reyes's chart would reference. Track 02.

**FHIR (Fast Healthcare Interoperability Resources).** The HL7 modern interoperability standard that uses HTTP REST and JSON. The dominant API style for new clinical work. Course 06 is the deep dive.

**Firewall.** The boundary equipment that controls what traffic is allowed into and out of a network. Most clinical integrations begin with a firewall request. Track 04.

**Frické 2009.** Martin Frické's critique of the DIKW hierarchy, published in the *Journal of Information Science*. The most-cited critique of the *clean bottom-up pyramid* picture. Track 02.

**HHS (Department of Health and Human Services).** The federal umbrella agency that contains CMS, ONC, FDA, NIH, AHRQ, CDC, HRSA, IHS, and OCR. Track 05.

**HIPAA (Health Insurance Portability and Accountability Act).** The 1996 federal law that defines Protected Health Information and the privacy and security obligations of covered entities and business associates. The floor every clinical data project sits on. Track 04. Course 03 is the deep dive.

**HITECH.** The Health Information Technology for Economic and Clinical Health Act of 2009. The federal law that subsidized EHR adoption and produced Meaningful Use. Track 01.

**HITRUST.** A private certification framework that bundles HIPAA, NIST, ISO 27001, and other standards into an auditable certification commonly required of cloud vendors selling into healthcare. Track 04.

**HL7 (Health Level Seven International).** The standards organization that develops and maintains the family of HL7 standards: HL7 v2, CDA, and FHIR. Track 05.

**HTTP (HyperText Transfer Protocol).** The protocol the browser uses to load web pages and that modern clinical APIs use to exchange data. Vocabulary: GET, POST, PUT, DELETE. Track 04.

**Information.** The DIKW layer where raw data carries enough context (reference range, patient identity, flag) to be noteworthy. Track 02.

**JSON (JavaScript Object Notation).** The nested key-value file format that dominates modern web and clinical APIs. FHIR's primary serialization. Track 03.

**Knowledge.** The DIKW layer where the field's accumulated patterns and rules apply to a piece of information. Lives in guidelines, textbooks, embedded rules, and trained clinicians. Track 02.

**LAN (Local Area Network).** The wired and wireless network inside a single building. The zone most clinical data traffic happens on. Track 04.

**LOINC.** Logical Observation Identifiers Names and Codes. The standard vocabulary for lab tests and clinical measurements. Maintained by the Regenstrief Institute. Ms. Reyes's CRP carries LOINC code 1988-5. Tracks 02 and 05.

**Meaningful Use.** The HITECH-era CMS program that paid hospitals and clinicians for using certified EHRs in defined ways. Now part of the Promoting Interoperability program. Track 01.

**OCR (Office for Civil Rights).** The office inside HHS that enforces HIPAA. Track 05.

**OLAP (Online Analytical Processing).** The kind of database designed for large analytic queries, optimized for aggregation across many records. The CDW is OLAP. Track 03.

**OLTP (Online Transaction Processing).** The kind of database designed for clinical operations, optimized for many small writes and reads. The EHR is OLTP. Track 03.

**ONC (Office of the National Coordinator for Health Information Technology).** The HHS office that runs the EHR certification program and defines the technical standards for interoperability. Track 05.

**On-prem.** Server lives in the hospital's own data center. The traditional default for large EHRs. Track 04.

**PCORnet.** Patient-Centered Outcomes Research Network. A federated network of health systems that pools harmonized clinical data for research. Track 05.

**POMR (Problem-Oriented Medical Record).** Lawrence Weed's 1960s structure for the medical record: numbered problem list at the front, SOAP notes anchored to a problem. The reason every chart has a problem list. Track 01.

**REST (Representational State Transfer).** The architectural convention behind modern web APIs: nouns at stable URLs, HTTP verbs to act on them. FHIR follows REST. Track 04.

**RxNorm.** The standard vocabulary for medications. Maintained by the NLM. Tracks 02 and 05.

**Sentinel System.** The FDA's federated post-market drug-safety surveillance network. Track 05.

**SNOMED CT.** The standard clinical terminology for diagnoses, findings, procedures, and anatomy. Maintained by SNOMED International. Tracks 02 and 05.

**SOC 2.** A security audit framework run by the AICPA. Required of most cloud-hosted clinical vendors. Track 04.

**SQL (Structured Query Language).** The dominant query language for relational databases. The default for asking questions of clinical data warehouses. Track 03. Course 07 Track 1 is the working-level treatment.

**TXT.** Plain text. The file format for free-text narrative (clinical notes, README files, log output). No machine-readable structure. Track 03.

**VPN (Virtual Private Network).** The encrypted tunnel that makes a remote computer look like it is on the hospital LAN. How most remote clinical work happens. Track 04.

**Wisdom.** The DIKW layer where knowledge is applied to a specific patient at a specific moment. The layer the field has the most trouble formalizing. Track 02.

**XML (eXtensible Markup Language).** The nested tagged file format that older HL7 standards (CDA, HL7 v3) are built on. Still common anywhere CDA is in use. Track 03.
