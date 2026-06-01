# Glossary: 12 Clinical decision support

Most terms used in this course are defined in the [curriculum-wide glossary](../start-here/GLOSSARY.md): CDS Hooks, Clinical Quality Language (CQL), decision curve analysis (DCA), discrimination, FHIR (R4), SMART on FHIR, value set. CDS-specific terms appear below.

**Alert fatigue.** The state in which a CDS alert fires so often, or so often wrongly, that clinicians stop reading the alerts. The standard published override rate for inpatient drug-interaction alerts is around 90 to 97 percent. Alert fatigue is the default outcome of a poorly designed CDS deployment; the remedy is upstream (alert design, thresholding, workflow placement), not downstream (clinician training).

**Card (CDS Hooks).** The JSON object a CDS service returns to the EHR in response to a hook invocation. A card carries a summary, a detail explanation, source attribution, and zero or more suggested actions the clinician can accept or reject inline.

**CDS service.** An external service that an EHR calls at a workflow moment (a hook) and that returns recommendation cards to display. CDS services live outside the EHR, communicate over HTTPS with FHIR-formatted payloads, and are the standards-based replacement for vendor-built-in alerts.

**Five rights of CDS.** Right information, right person, right format, right channel, right time. The published framework for designing a CDS intervention that does not produce alert fatigue. Failing any of the five is usually enough to make the alert ignored.

**Hard stop.** A CDS alert that prevents the clinician from completing an action without an override. Hard stops are reserved for situations where the harm of proceeding without acknowledgment is high (drug-drug interactions with severe consequences, dose ceilings for narrow-therapeutic-index drugs). Overusing hard stops produces a different kind of alert fatigue: workflow paralysis.

**Hook.** A defined workflow moment at which an EHR may call out to one or more CDS services. The CDS Hooks specification names a small set of standardized hooks (patient-view, order-select, order-sign, encounter-start, appointment-book, and others); the EHR vendor implements the hook trigger, and the institution registers the CDS services it wants invoked at each hook.

**Order-select hook.** A CDS Hooks moment that fires when the clinician selects a medication or order before signing it. The hook receives the candidate order as part of the request payload, so the CDS service can return a card warning about a drug-drug interaction, dose adjustment, or alternative therapy.

**Order-sign hook.** A CDS Hooks moment that fires when the clinician is about to sign an order. The hook is the last chance to intervene before the order becomes operational; cards returned at order-sign often carry suggested-action changes that the clinician can accept inline.

**Override rate.** The fraction of CDS alerts the clinician dismisses without acting on the recommendation. The standard headline metric in CDS evaluation literature. An override rate above approximately 90 percent is the operational definition of alert fatigue.

**Patient-view hook.** A CDS Hooks moment that fires when the clinician opens a patient's chart. The hook is the right one for alerts about chronic disease management, gaps in care, or risk-stratification flags. Cards returned at patient-view are typically informational rather than action-required.

**SaMD (Software as a Medical Device).** Software intended to perform one or more medical functions independent of a physical medical device. The FDA regulates SaMD when the intended use places it in one of the defined risk categories; clinical decision support that meets the IMDRF criteria for SaMD requires FDA clearance. The boundary between regulated SaMD and non-regulated clinical-decision software is the subject of evolving guidance.

**Suggested action.** A specific change to a clinical order that a CDS service offers as part of a card. The EHR renders the suggested action as an accept/reject control; if the clinician accepts, the EHR applies the change without requiring the clinician to navigate elsewhere. Suggested actions are the highest-leverage way to convert a CDS recommendation into a clinical change without adding workflow steps.
