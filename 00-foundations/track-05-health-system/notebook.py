"""Track 05: The American health system and its parts.

Plain English orientation. No code visible. The org chart of US healthcare
in one track: providers, payers, EHR vendors, regulators, research
infrastructure, public health, standards bodies. Where informatics sits
within each. Closes with a multi-stakeholder mapper for a single
interoperability scenario (Ms. Reyes seeing an out-of-network specialist).
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 05: The American health system and its parts

        ## Who has to agree.

        Tracks 03 and 04 walked Ms. Reyes's CRP through systems and across boundaries. Each boundary was authorized by a contract or a regulation or a standard. None of those exist by themselves; each one is the work of a specific organization with a specific role in the U.S. health system.

        This track is the **org chart**. The reason it sits in Course 0 is that almost every interesting informatics conversation eventually depends on knowing who the actors are. *We need ONC to certify this*, *the BAA with the vendor is the blocker*, *CMS will pay for it under the new rule*, *the IRB owns the research authorization*, *LOINC won't have a code for that for two cycles*: each of those sentences references a specific actor doing a specific job. Knowing the actors is most of what makes the sentences legible.

        Seven sets of actors do most of the work. Pick one at a time.
        """
    )
    return


@app.cell
def _(mo):
    actor_picker = mo.ui.radio(
        options=[
            "Providers (where care actually happens).",
            "Payers (who pays for the care).",
            "EHR vendors (who builds the systems care runs on).",
            "Regulators (who sets the federal rules).",
            "Research infrastructure (who funds and supports research with clinical data).",
            "Public health (who watches the population-level signal).",
            "Standards bodies (who maintains the vocabularies and the protocols).",
        ],
        label="Pick an actor group.",
        value="Providers (where care actually happens).",
    )
    actor_picker
    return (actor_picker,)


@app.cell
def _(actor_picker, mo):
    if actor_picker.value is None:
        actor_view = mo.md("")
    elif actor_picker.value.startswith("Providers"):
        actor_view = mo.callout(
            mo.md(
                "**Providers.** The places and people who deliver care.\n\n"
                "- **Hospitals** divide into a few archetypes. **Academic medical centers** "
                "(AMCs) such as Johns Hopkins, Massachusetts General, UCSF, are large, "
                "teaching-affiliated, and usually the most research-active. **Community "
                "hospitals** are the majority of U.S. hospitals by count: smaller, locally "
                "anchored, often part of a regional system. **Critical-access hospitals** are "
                "small rural hospitals (25 or fewer beds, designated by CMS) that get a special "
                "Medicare payment structure to stay open in underserved geographies. **Safety-net "
                "hospitals** carry a disproportionate share of Medicaid and uninsured patients "
                "and have their own payment realities.\n"
                "- **Clinics and physician practices.** Independent practices, hospital-owned "
                "practices, multi-specialty groups, single-specialty groups. Ms. Reyes's "
                "rheumatology clinic is a hospital-owned outpatient practice.\n"
                "- **Federally Qualified Health Centers (FQHCs).** Community health centers that "
                "receive HRSA funding to serve underserved populations regardless of ability to "
                "pay. They are required to use a sliding-fee scale and to be governed by a "
                "patient-majority board. There are roughly 1,400 FQHC organizations operating "
                "more than 14,000 sites in the U.S.\n"
                "- **Allied health and ancillary providers.** Pharmacies, home health, "
                "rehabilitation, hospice, durable medical equipment, dialysis. Each one has its "
                "own EHR, its own data, its own integration story.\n\n"
                "**Where informatics lives within providers.** Most large provider organizations "
                "have a **CMIO** (Chief Medical Information Officer) and increasingly a **CNIO** "
                "(Chief Nursing Information Officer) and a **CRIO** (Chief Research Information "
                "Officer). Beneath them sit clinical informaticists, analysts, and the larger "
                "IT organization. Small practices share informatics work across the practice "
                "manager and the EHR vendor's support."
            ),
            kind="info",
        )
    elif actor_picker.value.startswith("Payers"):
        actor_view = mo.callout(
            mo.md(
                "**Payers.** The organizations that pay providers for care delivered. The U.S. "
                "is unusual in having a public-private mix rather than a single national payer.\n\n"
                "- **Commercial insurers.** UnitedHealthcare, Anthem (Elevance Health), Aetna "
                "(CVS Health), Humana, Cigna, and the regional Blue Cross Blue Shield plans. "
                "Cover most working-age adults and their dependents through employer-sponsored "
                "plans or the Affordable Care Act marketplaces.\n"
                "- **Medicare.** The federal program for adults 65 and over, for people with "
                "long-term disabilities, and for people with end-stage renal disease. "
                "Administered by CMS. Has four parts (A for hospital, B for outpatient, C for "
                "Medicare Advantage which is privately-administered Medicare, D for "
                "prescription drugs). Medicare's coverage and reimbursement decisions tend to "
                "set the pattern that commercial insurers follow.\n"
                "- **Medicaid.** Joint federal-state program for low-income individuals and "
                "families. Eligibility rules and managed-care arrangements vary substantially "
                "by state. Many Medicaid programs contract with **Medicaid Managed Care "
                "Organizations** (MCOs) to actually administer benefits.\n"
                "- **TRICARE.** Health coverage for active-duty military, retirees, and their "
                "dependents.\n"
                "- **VA.** The Veterans Health Administration operates its own integrated "
                "delivery system (the VA hospitals and clinics) and is also a payer in the "
                "sense that veterans receive care funded through it.\n"
                "- **IHS.** The Indian Health Service provides care to members of federally "
                "recognized American Indian and Alaska Native tribes.\n\n"
                "**Where informatics lives within payers.** Payer informatics is its own large "
                "world: claims analytics, prior authorization, value-based care contracts, risk "
                "adjustment, quality measurement, fraud detection. Course 11 (health economics "
                "data) is where this work shows up in the curriculum."
            ),
            kind="info",
        )
    elif actor_picker.value.startswith("EHR vendors"):
        actor_view = mo.callout(
            mo.md(
                "**EHR vendors.** The companies that build and sell the electronic systems care "
                "runs on. Knowing the names matters because the choice of vendor shapes almost "
                "every downstream informatics decision in a health system.\n\n"
                "- **Epic.** The largest vendor in the large-hospital and academic-medical-center "
                "market by far. Privately held, based in Verona, Wisconsin. Most of the major "
                "U.S. AMCs run Epic. Owns the patient portal MyChart, which is the dominant "
                "patient-facing experience in U.S. healthcare.\n"
                "- **Oracle Health** (formerly Cerner, acquired by Oracle in 2022). The "
                "second-largest in large hospitals. Used by many community health systems, the "
                "VA's modernization, and a substantial international presence.\n"
                "- **MEDITECH.** Strong in community hospitals, especially smaller and rural "
                "systems.\n"
                "- **Athenahealth.** Cloud-native, strong in physician practices and smaller "
                "ambulatory groups. Owned by Bain Capital and Hellman & Friedman.\n"
                "- **eClinicalWorks**, **NextGen**, **Allscripts** (now Veradigm) and others "
                "compete in the ambulatory and smaller-hospital market.\n"
                "- **Specialty-specific EHRs.** Ophthalmology (Modernizing Medicine), "
                "behavioral health (Netsmart), oncology (Flatiron), dialysis (Acumen). Often "
                "interoperated alongside a main EHR rather than replacing it.\n\n"
                "**Where informatics lives within vendors.** Vendor clinical informatics teams "
                "build the content (order sets, CDS rules, clinical applications), partner with "
                "health systems on configuration, and increasingly run the data science teams "
                "that build the AI features now shipping inside the EHR. A great deal of "
                "informatics work happens inside the vendor world rather than inside the health "
                "system that buys from it."
            ),
            kind="info",
        )
    elif actor_picker.value.startswith("Regulators"):
        actor_view = mo.callout(
            mo.md(
                "**Regulators.** Federal agencies that set the rules under which the rest of the "
                "system operates.\n\n"
                "- **CMS.** The Centers for Medicare and Medicaid Services. Inside HHS. Sets "
                "coverage and payment rules for Medicare and Medicaid, runs the Quality Payment "
                "Program (MIPS), runs the Promoting Interoperability program (the descendant of "
                "Meaningful Use), and increasingly sets interoperability requirements for "
                "Medicare Advantage plans and qualified health plans on the ACA marketplaces.\n"
                "- **ONC.** The Office of the National Coordinator for Health Information "
                "Technology. Also inside HHS. Runs the EHR certification program (an EHR is not "
                "*certified* unless it meets ONC's technical standards), defines the standards "
                "for interoperability (USCDI, the FHIR APIs in the Cures Act rule), and "
                "investigates information blocking complaints. ONC is the technical-standards "
                "regulator; CMS uses ONC's standards to shape payment.\n"
                "- **FDA.** Regulates medical devices. The relevant subset for clinical "
                "informatics is **Software as a Medical Device** (SaMD): the question of when a "
                "piece of clinical software (a CDS tool, an AI model, a digital therapeutic) "
                "rises to the level of a regulated device. The line is blurry and moving; "
                "Course 12 (CDS) returns to it.\n"
                "- **HHS** generally. The Department of Health and Human Services is the umbrella "
                "agency that contains CMS, ONC, FDA, NIH, AHRQ, CDC, HRSA, IHS, and the rest of "
                "the federal health apparatus.\n"
                "- **OCR.** The Office for Civil Rights inside HHS. Enforces HIPAA. Investigates "
                "breach reports and imposes penalties when applicable.\n\n"
                "**Where informatics lives within regulators.** Federal informatics is its own "
                "career path: writing the standards, running certification, investigating "
                "complaints, evaluating regulatory submissions. ONC in particular employs a "
                "substantial population of clinical informaticists."
            ),
            kind="info",
        )
    elif actor_picker.value.startswith("Research infrastructure"):
        actor_view = mo.callout(
            mo.md(
                "**Research infrastructure.** The federally-funded and federally-coordinated "
                "ecosystem that supports research using clinical data.\n\n"
                "- **NIH.** The National Institutes of Health. The dominant funder of biomedical "
                "research in the U.S. and globally. Twenty-seven institutes and centers, "
                "including the NLM (which stewards PubMed, the UMLS, and the broader medical "
                "vocabulary infrastructure).\n"
                "- **AHRQ.** The Agency for Healthcare Research and Quality. Smaller than NIH "
                "and focused on health-services research: quality, safety, access, "
                "cost-effectiveness, the workings of the delivery system itself.\n"
                "- **CTSAs.** Clinical and Translational Science Awards. NIH-funded hubs (about "
                "sixty across the U.S.) at major academic medical centers that provide research "
                "infrastructure (research informatics, biostatistics, regulatory support) for "
                "the institution's clinical research enterprise.\n"
                "- **Registries.** Disease-specific data collections (cancer, diabetes, "
                "rheumatology, cardiovascular). Some are run by professional societies, some by "
                "the government, some by industry consortia. The NCDR (American College of "
                "Cardiology), NSQIP (American College of Surgeons), and CESR (Childhood Cancer "
                "Survivor Study) are examples.\n"
                "- **Research networks.** **PCORnet** (Patient-Centered Outcomes Research "
                "Network) and the FDA's **Sentinel System** are large, federated networks of "
                "health systems that pool harmonized clinical data for research at scale.\n\n"
                "**Where informatics lives within research infrastructure.** Research "
                "informatics is its own subspecialty: data mapping and harmonization, "
                "honest-broker arrangements, privacy and de-identification at scale, the OMOP "
                "common data model (Course 07 Track 4), the i2b2 platform, REDCap for study "
                "data capture. Many CTSA hubs run a research informatics core that supports "
                "everyone else in the institution."
            ),
            kind="info",
        )
    elif actor_picker.value.startswith("Public health"):
        actor_view = mo.callout(
            mo.md(
                "**Public health.** The actors who watch population-level signals and respond "
                "to outbreaks and ongoing health threats.\n\n"
                "- **CDC.** The Centers for Disease Control and Prevention. Federal agency "
                "inside HHS. Runs nationwide disease surveillance, immunization programs, "
                "outbreak response, and a long list of data systems including NEDSS (notifiable "
                "disease reporting), ESSENCE (syndromic surveillance), NHSN (healthcare-associated "
                "infections), and the public-use death certificate data.\n"
                "- **State Departments of Public Health.** Each state runs its own public health "
                "apparatus: disease reporting, immunization registries (IIS), vital records, "
                "laboratory services. State DPHs are usually the first recipient of reportable "
                "disease cases from providers; they aggregate and forward to CDC.\n"
                "- **Local health departments.** County or city level. Run school health, "
                "community outreach, environmental health inspections, and the on-the-ground "
                "response to local outbreaks.\n\n"
                "**Where informatics lives within public health.** Public health informatics is "
                "its own discipline with its own training programs and its own standards "
                "(HL7 v2 messages dominate reporting flows because state systems still expect "
                "them, even as the rest of the field moves to FHIR). Course 18 of the curriculum "
                "(population and public health) is the deep dive. The 2020 COVID response made "
                "it visible how much of U.S. public health data infrastructure was built in the "
                "1990s and never refreshed."
            ),
            kind="info",
        )
    else:
        actor_view = mo.callout(
            mo.md(
                "**Standards bodies.** The organizations that maintain the vocabularies and the "
                "protocols that let the rest of the system interoperate at all.\n\n"
                "- **HL7.** Health Level Seven International. The standards organization that "
                "develops and maintains the family of HL7 standards: HL7 v2 (the pipe-delimited "
                "message format still in use everywhere), CDA (the XML clinical document "
                "format), and FHIR (the modern JSON-over-REST standard that Course 06 takes "
                "apart in detail).\n"
                "- **IHE.** Integrating the Healthcare Enterprise. Develops **profiles**: "
                "tightly specified applications of HL7 and other standards for particular "
                "clinical use cases (sharing a radiology study, exchanging a continuity-of-care "
                "summary, querying a national health information exchange). Profiles are what "
                "make *we both speak FHIR* into *we can actually integrate*.\n"
                "- **LOINC.** Logical Observation Identifiers Names and Codes. The vocabulary "
                "for lab tests and clinical measurements. Ms. Reyes's CRP carries LOINC code "
                "1988-5; that code means the same thing in every health system that uses LOINC. "
                "Maintained by the Regenstrief Institute.\n"
                "- **SNOMED CT.** The clinical terminology. Diagnoses, findings, procedures, "
                "anatomy, all in a structured tree. Used worldwide. Maintained by SNOMED "
                "International.\n"
                "- **RxNorm.** The vocabulary for medications. Maintained by the NLM. Every "
                "prescribable drug has an RxNorm identifier that crosses brand and generic names "
                "and ties to NDC codes.\n"
                "- **ICD-10-CM and ICD-10-PCS.** The diagnosis and inpatient procedure coding "
                "systems used for billing. Maintained by the National Center for Health "
                "Statistics (NCHS) and CMS for the U.S. clinical modification.\n"
                "- **NCPDP.** The National Council for Prescription Drug Programs. Develops the "
                "standards for electronic prescribing and pharmacy claims (SCRIPT, Telecom).\n"
                "- **X12.** The standards organization behind the EDI transaction sets that "
                "carry claims (837), eligibility (270/271), and remittance advice (835) between "
                "providers and payers.\n\n"
                "**Where informatics lives within standards bodies.** Most standards work is "
                "done by working groups of volunteers from across the field (vendors, "
                "providers, regulators, payers, consultants). The work is slow, consensus-driven, "
                "and absolutely load-bearing for everything else. Many career clinical "
                "informaticists participate in HL7 or IHE working groups alongside their day jobs."
            ),
            kind="info",
        )
    actor_view
    return (actor_view,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Who has to agree, in one picture.

        The pattern across the seven groups: every clinical informatics decision touches more than one of them. The CRP value Track 04 traced depended on a provider (the rheumatology practice), a payer (her insurer), a vendor (the EHR), regulators (HIPAA, ONC's API rule), standards bodies (LOINC, FHIR, X12 if it became a claim), and research infrastructure (if it ever joined a research extract). Public health did not feature in this particular case; if Ms. Reyes had been diagnosed with a reportable disease, it would have.

        The reason this matters operationally is timing. Decisions inside a single actor (the provider, the vendor) move on a project timeline. Decisions that require multiple actors to agree (a contract, a standard, a regulation) move on the actors' shared timeline, which is the slower of the two. Most large clinical informatics initiatives are slow because they wait on shared timelines, not because the technical work is hard.

        The remainder of the curriculum lives inside these actors. **Course 03** (privacy, ethics, governance) sits with the regulators and the contracts that hold them. **Course 05** (EHR systems) sits with the vendors and the providers that buy from them. **Course 06** (FHIR) and **Course 14** (interoperability policy) sit with the standards bodies and ONC. **Course 11** (health economics) sits with the payers. **Course 18** (population and public health) sits with the public health actors. Holding the org chart in mind is what makes the rest of the curriculum land.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## One more.")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Who has to agree for this scenario.

        Ms. Reyes's hand pain has worsened. Her rheumatologist refers her to an out-of-state hand surgeon for a one-time consult. The hand surgeon's practice uses a different EHR vendor than the rheumatology clinic. Ms. Reyes's commercial insurance is one of the big national plans. The surgeon's office wants to see her recent labs, her medication list, her imaging, and her rheumatology notes before the visit.

        For this single referral to work end-to-end (clinically, legally, and technically), which sets of actors have to be in agreement, even implicitly? Pick all that apply.
        """
    )
    return


@app.cell
def _(mo):
    stakeholder_selector = mo.ui.multiselect(
        options=[
            "Providers (the rheumatology clinic and the hand surgeon's practice).",
            "Payers (Ms. Reyes's commercial insurer).",
            "EHR vendors (the rheumatology EHR vendor and the surgeon's EHR vendor).",
            "Regulators (CMS, ONC, OCR).",
            "Standards bodies (HL7 for FHIR, LOINC for labs, RxNorm for meds, SNOMED for findings).",
            "Research infrastructure (NIH, AHRQ, PCORnet).",
            "Public health (CDC, state DPH).",
        ],
        label="Pick all that apply.",
    )
    stakeholder_selector
    return (stakeholder_selector,)


@app.cell
def _(mo, stakeholder_selector):
    chosen_stakeholders = set(stakeholder_selector.value or [])
    needed = {
        "Providers (the rheumatology clinic and the hand surgeon's practice).",
        "Payers (Ms. Reyes's commercial insurer).",
        "EHR vendors (the rheumatology EHR vendor and the surgeon's EHR vendor).",
        "Regulators (CMS, ONC, OCR).",
        "Standards bodies (HL7 for FHIR, LOINC for labs, RxNorm for meds, SNOMED for findings).",
    }
    if not chosen_stakeholders:
        stakeholder_response = mo.callout(
            mo.md("_Pick at least one. You can change your mind after seeing the answer._"),
            kind="neutral",
        )
    elif chosen_stakeholders == needed:
        stakeholder_response = mo.callout(
            mo.md(
                "**Five of the seven.** Providers (both sides), payers (the insurer has to "
                "authorize the out-of-network consult and route the claim), vendors (the two "
                "EHRs need to exchange data, which is a vendor capability question), regulators "
                "(ONC's certification rules are why both EHRs support FHIR APIs in the first "
                "place; OCR's HIPAA rules govern the data exchange; CMS rules shape the payer's "
                "side), and standards bodies (FHIR/LOINC/RxNorm/SNOMED are what let the "
                "vocabularies survive the trip between two different EHRs). Research "
                "infrastructure and public health are not load-bearing for a single referral; "
                "they would be if Ms. Reyes joined a research cohort or had a reportable "
                "condition. The pattern is the point: even a *single referral* involves five "
                "of the seven actor groups, and the timing of the visit depends on the slowest "
                "of the agreements among them."
            ),
            kind="success",
        )
    else:
        stakeholder_response = mo.callout(
            mo.md(
                "**Close.** The five that are load-bearing for this referral are providers, "
                "payers, EHR vendors, regulators, and standards bodies. Research infrastructure "
                "and public health are not needed for a one-time referral; they would be if "
                "Ms. Reyes joined a research cohort or had a reportable disease. The takeaway: "
                "even one referral pulls in five of the seven actor groups, and the timing of "
                "the visit depends on the slowest of the agreements among them."
            ),
            kind="warn",
        )
    stakeholder_response
    return chosen_stakeholders, needed, stakeholder_response


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What you did in this track.

        - Named the seven actor groups in the U.S. health system: providers, payers, EHR vendors, regulators, research infrastructure, public health, standards bodies.
        - Noted what kinds of decisions each one owns, and named the most important players inside each.
        - Saw that informatics work lives inside every one of these actors, and that career informaticists often move between them.
        - Mapped a single referral scenario to the five actor groups whose agreement it depends on, and noticed why the visit's timing is the slowest of the shared agreements.

        ## What's next.

        **Track 06: Roles, ethics, and where the literature lives.** The actor groups above employ clinical informaticists with distinct titles (CMIO, CNIO, CRIO, analyst, data scientist, health IT) doing distinct work. Track 06 names those roles, describes the AMIA pathway and the Clinical Informatics board certification, gestures at the ethics that animate the field (which Course 03 takes seriously), and points at the journals and conferences where the field's literature actually lives.
        """
    )
    return


if __name__ == "__main__":
    app.run()
