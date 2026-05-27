"""Track 06: The informatics field: roles, ethics, and where the literature lives.

Plain English orientation. No code visible. Role distinctions (CMIO,
CNIO, CRIO, clinical informaticist, data scientist, health IT). The AMIA
pathway and 10x10. Clinical Informatics board certification (the ABPM /
ABMS subspecialty). The ethical premise of the field (forward-ref to
course 03). Where the field publishes (JAMIA, JAMIA Open, Applied
Clinical Informatics, the AMIA Annual Symposium proceedings, BMC
Medical Informatics and Decision Making). Closes with a role-matcher
exercise and a "where would I publish this" sorter.
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
        # Track 06: Roles, ethics, and where the literature lives

        ## Why this track closes the course.

        Track 05 named the actor groups. This track zooms inside them. Almost every actor in the U.S. health system employs clinical informaticists; the title varies by setting; the day-to-day work varies more. The first half of this track is a working taxonomy of titles and what each role actually does. The second half is two pieces of professional infrastructure: the **AMIA pathway** for getting into the field, and the **places the field publishes** so you know where to read once you are looking.

        Ethics gets a paragraph here and a whole course later. Course 03 (privacy, ethics, governance) is where the field treats ethics as serious work rather than orientation. For Course 0 the goal is to name that it exists, sketch the premise, and hand off.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## The titles.")
    return


@app.cell
def _(mo):
    role_picker = mo.ui.radio(
        options=[
            "CMIO: Chief Medical Information Officer.",
            "CNIO: Chief Nursing Information Officer.",
            "CRIO: Chief Research Information Officer.",
            "Clinical informaticist (no executive prefix).",
            "Clinical data scientist.",
            "Health IT (the broader information technology staff).",
        ],
        label="Pick a role.",
        value="CMIO: Chief Medical Information Officer.",
    )
    role_picker
    return (role_picker,)


@app.cell
def _(mo, role_picker):
    if role_picker.value is None:
        role_view = mo.md("")
    elif role_picker.value.startswith("CMIO"):
        role_view = mo.callout(
            mo.md(
                "**CMIO.** The senior physician executive responsible for the clinical use of "
                "information systems in a health system. Almost always an MD (sometimes a DO) "
                "who continues to practice some amount of clinical medicine alongside the "
                "administrative role. Reports vary: some CMIOs report to the CMO (chief medical "
                "officer), some to the CIO (chief information officer), some directly to the "
                "CEO. The reporting line shapes the job. Typical scope: chairing the clinical "
                "advisory committees that govern EHR configuration, owning the relationship "
                "with the EHR vendor's clinical content team, signing off on clinical decision "
                "support deployments, leading the response when clinicians push back on a "
                "workflow, and increasingly owning the governance of AI tools embedded in the "
                "EHR. The CMIO is the clinical voice in the room where systems decisions get "
                "made and the systems voice in the room where clinical decisions get made."
            ),
            kind="info",
        )
    elif role_picker.value.startswith("CNIO"):
        role_view = mo.callout(
            mo.md(
                "**CNIO.** The senior nursing informatics executive. RN with a graduate degree "
                "(often an MSN or DNP with an informatics concentration). Owns the nursing side "
                "of the same questions the CMIO owns on the physician side: how documentation "
                "flows, how the medication administration record is structured, how scoring "
                "tools (Braden, falls risk) live in the EHR, how barcode scanning at the "
                "bedside is set up, how nursing handoffs are supported. Nursing is the largest "
                "single clinical workforce in most health systems; the CNIO role exists because "
                "informatics decisions land on nurses constantly and need a senior nursing "
                "voice in the design conversations."
            ),
            kind="info",
        )
    elif role_picker.value.startswith("CRIO"):
        role_view = mo.callout(
            mo.md(
                "**CRIO.** Chief Research Information Officer. A newer title, more common in "
                "academic medical centers than in community health systems. Owns the research "
                "use of the clinical data the institution generates: the clinical data "
                "warehouse, the OMOP or PCORnet mappings, the research enclaves, the honest "
                "broker arrangements, REDCap and similar study-data platforms, and the "
                "governance that authorizes research access to clinical data. Often holds a "
                "joint appointment in an academic department. Where this role does not exist, "
                "its work usually sits with a CTSA research informatics core or under the CMIO."
            ),
            kind="info",
        )
    elif role_picker.value.startswith("Clinical informaticist"):
        role_view = mo.callout(
            mo.md(
                "**Clinical informaticist.** The non-executive title for clinicians who do "
                "informatics work full or part time. May be a physician, a nurse, a pharmacist, "
                "a respiratory therapist, a laboratorian. Often holds a portion of clinical "
                "FTE alongside the informatics work. Typical day: sits on the clinical advisory "
                "committees the CMIO chairs, owns specific projects (a new order set, a CDS "
                "rule, a workflow redesign for one service line), serves as the translator "
                "between vendor analysts and clinical leaders, and is often the first reviewer "
                "on the design of any clinical-facing change to the EHR. The pipeline into "
                "this role is increasingly through formal informatics training (a master's, a "
                "fellowship, or the AMIA 10x10) rather than the *learned on the job* path that "
                "produced most of the current senior generation."
            ),
            kind="info",
        )
    elif role_picker.value.startswith("Clinical data scientist"):
        role_view = mo.callout(
            mo.md(
                "**Clinical data scientist.** A growing title that overlaps with clinical "
                "informatics without being identical to it. Tends to come from a quantitative "
                "background (statistics, epidemiology, computer science, machine learning) "
                "rather than from clinical training. Typical work: building and evaluating "
                "predictive models, running cohort studies on the clinical data warehouse, "
                "developing the analytic infrastructure that registries and value-based-care "
                "programs depend on, increasingly building and monitoring AI tools that ship "
                "inside the EHR. The most effective clinical data scientists pair tightly with "
                "clinical informaticists so that the models they build land in the clinical "
                "workflow appropriately rather than as orphaned dashboards. Courses 09 (AI in "
                "medicine) and 04 (clinical epidemiology) are where this role's substantive "
                "work lives in the curriculum."
            ),
            kind="info",
        )
    else:
        role_view = mo.callout(
            mo.md(
                "**Health IT.** The broader information technology staff: the engineers who "
                "keep the EHR running, the database administrators who maintain the underlying "
                "systems, the network engineers who run the LAN and the firewall, the "
                "integration analysts who write the interface engine rules, the help desk that "
                "answers when the printer in the OR breaks. Health IT and clinical informatics "
                "are different jobs that share substantial real estate. The line, roughly: "
                "health IT keeps the systems running; clinical informatics shapes how the "
                "systems work for clinical care. The CIO owns health IT; the CMIO owns clinical "
                "informatics; the two are peers in the C-suite (or near it) and have to "
                "cooperate constantly. When that cooperation breaks down, every project the "
                "health system runs slows down."
            ),
            kind="info",
        )
    role_view
    return (role_view,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The training pathways.

        Clinical informatics has a relatively young set of formal training pathways. The most established are clustered around the **American Medical Informatics Association (AMIA)** and around the **Clinical Informatics subspecialty** of the American Board of Preventive Medicine.

        - **The AMIA 10x10 program.** A widely-taken online introductory program (one semester, roughly the length of a graduate course) developed by AMIA in partnership with universities. Built for clinicians and others entering the field who do not have formal informatics training. The *10x10* name is a reference to AMIA's original goal of training 10,000 clinicians in 10 years; the program kept the name after the original goal was met.\n
        - **AMIA Clinical Informatics Board Review Course (CIBRC).** A more targeted offering for those preparing for the board exam.\n
        - **Master's degrees and PhDs in clinical or biomedical informatics.** Offered by many U.S. universities (Stanford, Columbia, Pitt, Vanderbilt, OHSU, Utah, Indiana, Houston, and many others). Two-year master's programs are the most common formal path; PhDs are typical for research careers.\n
        - **ACGME-accredited Clinical Informatics fellowships.** Two-year post-residency fellowships at major academic medical centers. The fellowship is the standard path for physicians who want to combine board certification with strong research training.\n
        - **The Clinical Informatics subspecialty board exam.** Since 2013, Clinical Informatics has been an ABMS-recognized subspecialty, administered by the American Board of Preventive Medicine (ABPM). Physicians who hold an ABMS primary specialty (any of them: medicine, surgery, pediatrics, family medicine, pathology, radiology, anything) are eligible to sit for the Clinical Informatics board exam after meeting the practice or fellowship pathway requirements. Passing the exam confers board certification in Clinical Informatics. As of 2024 there are several thousand U.S. physicians board-certified in the subspecialty.

        Nursing has its own parallel pathways through the American Nurses Credentialing Center (ANCC) certification in Informatics Nursing and through master's-level Nursing Informatics programs. Pharmacy, dentistry, and other clinical professions have their own newer credentials in informatics-adjacent areas.

        The pattern: the field has matured from *learned on the job* (which is how most current senior leaders got here) to *formally trained* (which is how most new entrants are getting here). Both pathways still exist; the formal pathway is becoming the default.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## The ethical premise.")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Course 03 (privacy, ethics, and governance) treats this seriously. For Course 0, the orienting paragraph is this.

        Clinical informatics handles data that was collected in the most asymmetric setting in modern life: a patient in a moment of vulnerability, often without the ability to refuse, often without understanding the downstream uses of what is being collected. Every other ethical commitment the field makes is downstream of taking that asymmetry seriously.

        The practical commitments that follow are familiar from the rest of medicine.

        - **Confidentiality.** The data is the patient's, not the institution's. The institution holds it in trust.
        - **Beneficence and non-maleficence.** Systems and tools should advance the patient's interest and avoid foreseeable harm. A CDS alert with a 97% override rate is not a neutral tool; it actively interferes with the next clinical decision the user has to make and trains the user to dismiss future alerts.
        - **Justice.** Systems work differently for different populations. A model trained on a single health system's patient population is not automatically valid in a different one. A workflow that assumes a smartphone excludes patients without one. The field has an obligation to look at *whose* care its tools improve and *whose* they do not.
        - **Autonomy.** Patients have a right to know what is being done with their data and (under HIPAA and the Cures Act) to access it. Patient-facing portals, the right of access, the Cures Act's prohibition on information blocking are the practical implementations.

        The list above is short and shallow on purpose. The real work is in Course 03, in Course 09 (where algorithmic fairness gets taken seriously), in Course 12 (where the design of CDS gets evaluated for unintended consequences), and in Course 14 (where policy meets practice). The point for now is that ethics is not bolted on to the field; it is the substrate.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## Where the field publishes.")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Knowing where the literature lives is most of what makes finding answers possible. Five places carry the bulk of the field's published work.

        - **JAMIA** (*Journal of the American Medical Informatics Association*). The flagship peer-reviewed journal of the field. Subscription-based; AMIA members get access through membership. Mix of research articles, brief communications, perspectives, and case reports. The journal of record for most substantive clinical informatics research.\n
        - **JAMIA Open.** The open-access companion journal. Same editorial bar, accessible to anyone without a subscription. Has become the default for work the authors want widely cited.\n
        - **Applied Clinical Informatics (ACI).** Peer-reviewed journal focused on the applied side of the field: implementation reports, evaluation studies, workflow studies, case studies. The journal where most *we built and deployed X and here is what we learned* papers appear.\n
        - **AMIA Annual Symposium proceedings.** AMIA's annual research conference (held each November) publishes a substantial proceedings volume. Many of the field's senior practitioners present here; the proceedings are freely available through PubMed Central. For a snapshot of where the field is at this year, the most recent symposium's proceedings are usually the right starting point.\n
        - **BMC Medical Informatics and Decision Making.** Open-access, broader scope than the AMIA-affiliated journals; publishes substantial work on CDS, decision-making research, and informatics methods.

        Adjacent venues you will encounter regularly: **Journal of Biomedical Informatics** (JBI) for methods-heavy work, **Health Affairs** for policy-flavored work, **JAMA Health Forum** for health-system-level analyses, **NEJM Catalyst** for delivery-system innovation, and the **CDC's Morbidity and Mortality Weekly Report (MMWR)** for public health informatics work. Specialty journals (JAMA Cardiology, Lancet Oncology, and so on) publish informatics work tied to their clinical area.

        Conferences worth knowing about: **AMIA Annual Symposium** (November), **AMIA Informatics Summit** (March), the **HL7 FHIR DevDays**, the **OHDSI Symposium** (for OMOP-centric research), and **HIMSS** (the big industry conference, less academic but where most vendor activity surfaces).
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
        ### Where would this paper land?

        Four hypothetical clinical informatics submissions. For each one, pick the publication venue that would be the most natural first home. There is sometimes more than one defensible answer; the explanation will tell you the trade-off.
        """
    )
    return


@app.cell
def _(mo):
    venue_options = [
        "JAMIA",
        "JAMIA Open",
        "Applied Clinical Informatics",
        "AMIA Annual Symposium proceedings",
        "BMC Medical Informatics and Decision Making",
    ]
    sub_a = mo.ui.radio(
        options=venue_options,
        label=(
            "A. A 2,800-patient study at a single academic medical center that built a new "
            "machine learning model to predict sepsis using EHR data, with extensive external "
            "validation at three other health systems, sophisticated subgroup analysis, and a "
            "novel methodological contribution to calibration assessment. The authors want "
            "this to be cited as the definitive treatment of the approach."
        ),
    )
    sub_a
    return sub_a, venue_options


@app.cell
def _(mo, sub_a):
    if sub_a.value is None:
        a_resp = mo.md("")
    elif sub_a.value == "JAMIA":
        a_resp = mo.callout(
            mo.md(
                "**Yes.** A methodologically substantial, externally validated, multi-site model "
                "with novel methods is exactly what JAMIA exists to publish. The journal's prestige "
                "and citation footprint match the authors' goal of having this read as definitive."
            ),
            kind="success",
        )
    elif sub_a.value == "JAMIA Open":
        a_resp = mo.callout(
            mo.md(
                "**Defensible if open access matters more than journal prestige.** The same "
                "editorial bar, accessible to anyone. The trade-off is citation reach: JAMIA still "
                "carries more weight in promotion and tenure conversations than JAMIA Open does, "
                "though the gap is closing. Authors who want maximum citation by other researchers "
                "often choose JAMIA; authors who want maximum reach (clinicians, policymakers, "
                "international audiences) often choose JAMIA Open."
            ),
            kind="success",
        )
    else:
        a_resp = mo.callout(
            mo.md(
                "**Possible but not the natural first home.** Applied Clinical Informatics is "
                "more implementation-focused than methodology-focused. BMC MIDM and the AMIA "
                "Symposium proceedings would both accept it but at less prestige than JAMIA. For "
                "a paper meant to be cited as definitive, JAMIA (or JAMIA Open for the open-access "
                "version) is the strongest first choice."
            ),
            kind="warn",
        )
    a_resp
    return (a_resp,)


@app.cell
def _(mo, venue_options):
    sub_b = mo.ui.radio(
        options=venue_options,
        label=(
            "B. A community hospital's case report describing how they implemented a new alert "
            "for venous thromboembolism prophylaxis on inpatients, including the workflow design, "
            "the rollout plan, the clinician engagement strategy, and 18-month outcomes. Pre- and "
            "post-implementation prophylaxis rates are reported with appropriate caveats about "
            "the design."
        ),
    )
    sub_b
    return (sub_b,)


@app.cell
def _(mo, sub_b):
    if sub_b.value is None:
        b_resp = mo.md("")
    elif sub_b.value == "Applied Clinical Informatics":
        b_resp = mo.callout(
            mo.md(
                "**Yes.** Implementation reports with deployment detail and pre/post outcomes are "
                "exactly what ACI exists for. The journal is designed for the *we built it and "
                "here is what happened* paper, where the value is in the operational detail and "
                "the realistic caveats rather than a novel methodological contribution."
            ),
            kind="success",
        )
    elif sub_b.value == "AMIA Annual Symposium proceedings":
        b_resp = mo.callout(
            mo.md(
                "**Possible.** The Symposium proceedings publish many similar implementation case "
                "reports, often as short papers. The trade-off vs. ACI: Symposium papers are "
                "shorter and tied to the conference timeline; ACI papers are full-length and have "
                "more space for the workflow detail that other implementers will want."
            ),
            kind="success",
        )
    elif sub_b.value == "JAMIA" or sub_b.value == "JAMIA Open":
        b_resp = mo.callout(
            mo.md(
                "**Possible but a stretch for this paper's design.** JAMIA can take implementation "
                "papers but tends to want more methodological novelty or external generalizability. "
                "A single-site implementation report with pre/post outcomes is a better fit for ACI."
            ),
            kind="warn",
        )
    else:
        b_resp = mo.callout(
            mo.md(
                "**Possible but not the strongest fit.** BMC MIDM accepts implementation work; ACI "
                "is the journal designed specifically for it. ACI is the better-fitting first home."
            ),
            kind="warn",
        )
    b_resp
    return (b_resp,)


@app.cell
def _(mo, venue_options):
    sub_c = mo.ui.radio(
        options=venue_options,
        label=(
            "C. A short methods note proposing a new way of evaluating the calibration of "
            "clinical prediction models in subgroups defined by race and ethnicity, with a worked "
            "example on a publicly available dataset. The authors want the method adopted "
            "quickly by other groups working on algorithmic fairness."
        ),
    )
    sub_c
    return (sub_c,)


@app.cell
def _(mo, sub_c):
    if sub_c.value is None:
        c_resp = mo.md("")
    elif sub_c.value == "JAMIA Open":
        c_resp = mo.callout(
            mo.md(
                "**Yes, for the *adopted quickly* goal.** JAMIA Open's open access means other "
                "groups working on algorithmic fairness will encounter the method without a "
                "paywall. A short methods note is a good fit; the journal publishes them. The "
                "trade-off vs. JAMIA proper: JAMIA Open lowers the access barrier at the cost of "
                "some prestige."
            ),
            kind="success",
        )
    elif sub_c.value == "JAMIA":
        c_resp = mo.callout(
            mo.md(
                "**Defensible.** A short methods note in JAMIA carries more prestige. The "
                "trade-off: it sits behind a paywall, which works against the authors' goal of "
                "rapid uptake by groups they have not pre-emailed."
            ),
            kind="success",
        )
    elif sub_c.value == "BMC Medical Informatics and Decision Making":
        c_resp = mo.callout(
            mo.md(
                "**Reasonable.** BMC MIDM is open access and publishes methods work. Lower "
                "citation footprint than JAMIA Open in clinical informatics specifically, but "
                "broader visibility in adjacent fields."
            ),
            kind="success",
        )
    else:
        c_resp = mo.callout(
            mo.md(
                "**Possible but not the natural first home.** The Symposium proceedings work for "
                "a method introduction tied to the conference cycle; ACI is more "
                "implementation-flavored. For a fairness methods note the authors want broadly "
                "cited, JAMIA Open (or JAMIA proper if access is less of a concern) is the "
                "strongest first choice."
            ),
            kind="warn",
        )
    c_resp
    return (c_resp,)


@app.cell
def _(mo, venue_options):
    sub_d = mo.ui.radio(
        options=venue_options,
        label=(
            "D. A team is presenting their first description of a new open-source tool for "
            "extracting structured findings from radiology reports. They want feedback from the "
            "community before submitting a full-length paper, and they want the work cited in "
            "subsequent submissions."
        ),
    )
    sub_d
    return (sub_d,)


@app.cell
def _(mo, sub_d):
    if sub_d.value is None:
        d_resp = mo.md("")
    elif sub_d.value == "AMIA Annual Symposium proceedings":
        d_resp = mo.callout(
            mo.md(
                "**Yes.** The Symposium is the field's annual gathering and where new tools and "
                "approaches get their first community exposure. A short paper in the proceedings "
                "(plus an oral or poster presentation) gives the team feedback from the right "
                "audience, a citable artifact, and the conversational hallway feedback they need "
                "to refine the full-length paper. Most new tools in the field surface here first."
            ),
            kind="success",
        )
    elif sub_d.value == "JAMIA Open":
        d_resp = mo.callout(
            mo.md(
                "**Defensible if the team prefers a peer-reviewed first home.** JAMIA Open's "
                "*Application Notes* category exists for exactly this. The trade-off vs. the "
                "Symposium: peer review takes longer and the team loses the conversational "
                "feedback the conference setting provides."
            ),
            kind="success",
        )
    elif sub_d.value == "Applied Clinical Informatics":
        d_resp = mo.callout(
            mo.md(
                "**Possible if the tool's deployment story is the headline.** ACI publishes tool "
                "descriptions when they come with implementation detail and outcomes. For a "
                "*first description seeking community feedback*, the Symposium is a more natural "
                "fit than ACI."
            ),
            kind="warn",
        )
    else:
        d_resp = mo.callout(
            mo.md(
                "**Possible but not the natural first home.** JAMIA proper is a longer review "
                "cycle than a *first description* warrants; BMC MIDM works but lacks the "
                "field-specific audience of the AMIA Symposium. The Symposium proceedings are "
                "where most new tools in clinical informatics get their first audience."
            ),
            kind="warn",
        )
    d_resp
    return (d_resp,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What you did in this track.

        - Named the working titles in the field (CMIO, CNIO, CRIO, clinical informaticist, clinical data scientist, health IT) and what each one actually does day to day.
        - Covered the training pathways (AMIA 10x10, master's and PhD programs, ACGME-accredited fellowships, the Clinical Informatics board certification, the parallel nursing and other allied pathways) and noted the field moving from *learned on the job* toward *formally trained*.
        - Heard the orienting paragraph on the field's ethics and saw where the deep treatment lives later in the curriculum (Course 03).
        - Located the five core publication venues (JAMIA, JAMIA Open, ACI, AMIA Annual Symposium proceedings, BMC MIDM) and the adjacent venues you will encounter.
        - Picked the natural first home for four very different hypothetical papers and noticed the trade-offs that drive each choice.

        ## What's next.

        **The capstone.** Six tracks of vocabulary, history, lifecycle, plumbing, actors, and roles do not become useful until you can carry them into a problem at once. The capstone is a Socratic walkthrough of a single scenario (a community hospital wanting to share readmission predictions with its accountable care organization) where every track in this course is in play. It is short on purpose. The work is recognizing what you already know.
        """
    )
    return


if __name__ == "__main__":
    app.run()
