# Go deeper: HL7 v2, CDA, and what we inherited

## If you want to understand this better before moving on

**Caristix HL7-Definition reference (free, online).** [https://hl7-definition.caristix.com/v2/HL7v2.5](https://hl7-definition.caristix.com/v2/HL7v2.5)

The official HL7 v2 spec is paywalled. Caristix maintains a free, browsable, accurate copy of the v2.5 specification, with full coverage of segments, fields, components, and the HL7 lookup tables that fields point at. When you have a real ORU in front of you and you need to know what OBX-11 means, this is the reference you want open. Includes search, message-type lookup, and field-level annotation. The most useful free HL7 v2 resource on the web.

## If you want to see this applied clinically

**D'Amore JD, Mandel JC, Kreda DA, et al. "Are Meaningful Use Stage 2 certified EHRs ready for interoperability? Findings from the SMART C-CDA Collaborative." *Journal of the American Medical Informatics Association*, 2014.** [https://pubmed.ncbi.nlm.nih.gov/24988894/](https://pubmed.ncbi.nlm.nih.gov/24988894/)

The Boston Children's Hospital SMART team collected real Meaningful Use Stage 2 C-CDA documents from 21 certified EHRs and audited them. The paper is short, blunt, and makes the practical-interoperability-versus-conformance gap concrete. Every document was certified; not one was clean enough to consume programmatically without local cleanup. If you ever doubted that the optionality story above was real, this paper resolves the doubt. Free via PubMed.

## If you want to go significantly further

**Mandl KD, Mandel JC, Murphy SN, Bernstam EV, Ramoni RL, Kreda DA, McCoy JM, Adida B, Kohane IS. "The SMART Platform: early experience enabling substitutable applications for electronic health records." *Journal of the American Medical Informatics Association*, 2012.** [https://pubmed.ncbi.nlm.nih.gov/22357556/](https://pubmed.ncbi.nlm.nih.gov/22357556/)

The original SMART paper. SMART (Substitutable Medical Applications, Reusable Technologies) is the architectural argument that led to FHIR. The paper predates the FHIR-DSTU release by two years and reads as a strongly-argued case for what the field needed to do next. The point of including it here, in the v2/CDA track, is that the design choices in FHIR (course 06) are reactions to specific painful experiences with v2 and CDA, and this paper documents those experiences from inside the team that pushed the next standard. Free via PubMed.
