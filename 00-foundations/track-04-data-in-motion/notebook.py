"""Track 04: How computers move data ("data in motion").

Plain English orientation. No code visible. Client-server through the
restaurant analogy. The hospital LAN, the VPN, the firewall, the public
internet. HTTP/REST/APIs at concept level (forward-ref to course 06).
On-prem vs cloud. Security boundaries that matter clinically (HIPAA and
HITRUST landscape, forward-ref to course 03). Closes with a click-through
of where a single lab result sits at each stage from analyzer to LIS to
EHR to claims to CDW to researcher, naming the network boundary at every
step.
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
        # Track 04: How computers move data

        ## Track 03 left us holding the data.

        The previous track named what clinical data looks like when it is at rest: bits arranged into tables, trees, graphs, and key-value structures; packaged into TXT, CSV, JSON, or XML files; held in databases that are either transactional (the EHR) or analytical (the data warehouse).

        That is not the end of the story. Almost none of that data is useful where it sits. The lab analyzer is in the basement; the rheumatologist is on the third floor. The EHR is on a server in the building; the patient is on her phone at home. The clinical data warehouse is inside the health system's firewall; the research collaborator who wants to query it is at a university in another state.

        Between rest and use is the network. This track names what the network looks like for clinical systems, and where the boundaries that matter to the field actually sit.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## Client and server.")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The single most useful piece of vocabulary in this track is **client-server**. Almost every clinical system you interact with is one of two roles in this pattern, and almost every conversation about network architecture is implicitly about which is which.

        The restaurant analogy is the one the field uses, and it is good enough that the rest of the curriculum will reuse it.

        - You sit down at a table. You are the **client**. You have a question (*what is for lunch?*) but no way to answer it yourself. You hand the question to a server.
        - The **server** takes your request, walks back to the kitchen (the database), gets what you need, and brings it back to your table.
        - The **menu** is the agreed-upon set of things you are allowed to ask for. You cannot order something not on the menu; the server has no way to bring it.
        - The **conversation** between you and the server has a small set of rules (you order, the server confirms, the food arrives, you pay). Both of you know the rules. Neither of you spells them out every time.

        That pattern, in slightly different costumes, is what browsers, EHR clients, mobile apps, and API calls are all doing. Substitute the names:

        - The **client** is the rheumatologist's laptop running the EHR client software, or her phone running the EHR mobile app, or the patient's phone running MyChart.
        - The **server** is the EHR's application server inside the health system data center, talking to the database behind it.
        - The **menu** is the API: the agreed-upon set of requests the client is allowed to make.
        - The **conversation rules** are protocols like HTTP, which both client and server know without having to negotiate them every time.

        Every other piece of vocabulary in this track is decoration on top of client-server.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## Where the wires are.")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Inside a hospital, the wires (and the wireless they extend through) are organized into a small number of zones. Each zone has its own rules about what is allowed in, what is allowed out, and who can see what crosses the boundary.

        Pick a zone to read the working definition and what crosses it.
        """
    )
    return


@app.cell
def _(mo):
    zone_picker = mo.ui.radio(
        options=[
            "The hospital LAN (the wires inside the building).",
            "The firewall (the boundary between the hospital and the rest of the world).",
            "The VPN (the way the work-from-home rheumatologist gets back inside).",
            "The public internet (everything else).",
        ],
        label="Pick a zone.",
        value="The hospital LAN (the wires inside the building).",
    )
    zone_picker
    return (zone_picker,)


@app.cell
def _(mo, zone_picker):
    if zone_picker.value is None:
        zone_view = mo.md("")
    elif zone_picker.value.startswith("The hospital LAN"):
        zone_view = mo.callout(
            mo.md(
                "**The hospital LAN.** *LAN* stands for **Local Area Network**: the wired and "
                "wireless network inside the hospital's physical building. The lab analyzer in "
                "the basement, the EHR server in the data center, the rheumatologist's "
                "workstation on the third floor, and the WoW (workstation on wheels) the nurse is "
                "rolling between rooms all sit on the same LAN. They can reach each other quickly "
                "and without going through any boundary checks beyond what the hospital's own "
                "network team has set up. The LAN is where most clinical data traffic happens, "
                "and it is where the EHR feels fast. When the EHR is slow at 9 a.m., the question "
                "*is it the LAN, the database, or the application* is the first decomposition."
            ),
            kind="info",
        )
    elif zone_picker.value.startswith("The firewall"):
        zone_view = mo.callout(
            mo.md(
                "**The firewall.** A piece of equipment (sometimes physical, sometimes software, "
                "in modern deployments often both) that sits at the boundary between the hospital "
                "LAN and the rest of the world. The firewall enforces what traffic is allowed in "
                "and what is allowed out, by source, by destination, by port, and by protocol. "
                "*Open a firewall rule* is a sentence that means *get the network team to permit "
                "this specific kind of traffic across this boundary*. Most clinical integrations "
                "with outside systems begin with a firewall request. The firewall is also why a "
                "vendor's *we only need to talk to your EHR* turns into a six-month project: "
                "each direction of traffic, each port, and each IP range needs explicit permission, "
                "documentation, and review."
            ),
            kind="info",
        )
    elif zone_picker.value.startswith("The VPN"):
        zone_view = mo.callout(
            mo.md(
                "**The VPN.** A **Virtual Private Network**. When the rheumatologist works from "
                "home, her laptop is on her home Wi-Fi and the EHR application server is inside "
                "the hospital firewall. The VPN is the encrypted tunnel that makes her laptop "
                "*look like* it is on the hospital LAN even though it is physically not. From "
                "the EHR's point of view, her workstation is inside the building; from her home's "
                "point of view, her network traffic is leaving through an encrypted pipe to the "
                "hospital and coming back the same way. VPNs are how most remote clinical work "
                "happens. They are also where some of the most consequential security incidents "
                "of the past few years began, because a stolen VPN credential lets an attacker "
                "look like they are inside the LAN."
            ),
            kind="info",
        )
    else:
        zone_view = mo.callout(
            mo.md(
                "**The public internet.** Everything outside the hospital firewall and outside "
                "any VPN. The patient's phone on her home Wi-Fi. The research collaborator's "
                "laptop in an academic library. The vendor's cloud-hosted application server in "
                "an AWS region two states away. The public internet is where most of the data "
                "moves once it leaves the hospital, and it is where every assumption the LAN "
                "lets you make stops being true. Traffic on the public internet has to be "
                "encrypted in transit (the *S* in HTTPS); identities have to be verified at every "
                "endpoint; logs have to capture who touched what. Most modern interoperability "
                "(FHIR APIs, patient portals, third-party app integrations) lives on the public "
                "internet by design."
            ),
            kind="info",
        )
    zone_view
    return (zone_view,)


@app.cell
def _(mo):
    mo.md("## HTTP, REST, and APIs.")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The rules clients and servers use to talk to each other on the modern internet are mostly **HTTP** (HyperText Transfer Protocol). HTTP is the protocol the browser uses to load every web page you have ever opened. The same protocol, with the same vocabulary (`GET`, `POST`, `PUT`, `DELETE`), is what clinical APIs use.

        - `GET` is *give me this*. The browser sends `GET https://mychart.example.org/labs/123` to retrieve a lab result. The EHR's FHIR endpoint receives `GET https://ehr.example.org/Patient/ER-001/Observation?code=1988-5` to retrieve Ms. Reyes's CRPs.
        - `POST` is *here is something new*. A new lab result arrives at the EHR via `POST`. A new portal message from the patient arrives at the EHR via `POST`.
        - `PUT` is *replace what was there with this*. An update to a medication order is a `PUT`.
        - `DELETE` is *take this away*. A cancellation is a `DELETE`.

        **REST** (Representational State Transfer) is the design pattern that says *organize your API so that everything is a noun (a patient, an observation, a medication) at a stable URL, and use HTTP verbs to act on those nouns*. REST is not a standard; it is a convention. Almost every modern clinical API, including FHIR, follows it.

        An **API** (Application Programming Interface) is *the menu*. It is the documented list of nouns the server understands and the verbs it accepts on each. The FHIR API for an EHR is a published document that says *here are the resources you can ask for, here are the search parameters you can use, here is what you will get back*. Course 06 of the curriculum (`learn-fhir`) is the deep dive on what one of these APIs looks like in practice; for Course 0 it is enough to hold that an API is a contract written down.

        Why this matters clinically: when somebody says *the EHR has an API*, they are saying *there is a documented menu of things a third-party tool is allowed to ask for, and the EHR commits to answering those requests in a particular shape*. When somebody says *the EHR doesn't have an API*, they are saying *the only way to get data out is a custom integration project*. The difference is the difference between a two-week and a two-year timeline.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## On-prem vs cloud.")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The other big architecture question every clinical informatics conversation eventually touches is *where does the server actually live*.

        **On-prem** means the server is physically in the hospital's data center. Hospital staff maintain it. The hospital owns the hardware. Most large EHR deployments (Epic and Oracle Health classically) ran on-prem for the first decade after HITECH. The advantages are control (you know where every byte lives), latency (the clinical network is right there, traffic does not need to leave the building), and a regulatory story that is easier to make. The disadvantages are cost (you pay for the hardware and the staff to run it), scale (when you need more capacity you buy and rack more servers), and the fact that *every hospital is running its own copy of everything*.

        **Cloud** means the server is in a data center run by a third party (AWS, Azure, Google Cloud, or a vendor's private cloud built on top of one of those). The hospital does not own the hardware. The vendor or the cloud provider maintains it. The advantages are flexibility (capacity scales when needed), cost (no hardware to buy, no data center to operate), and updates (the vendor pushes new versions without a hospital install). The disadvantages are that the data physically leaves the building, the regulatory story has to be made carefully (HIPAA Business Associate Agreements, HITRUST certification, vendor SOC 2 reports), and an outage at the cloud provider is an outage for the hospital.

        Modern EHRs are increasingly **hosted**, which is a particular flavor of cloud where the vendor runs your specific instance of the EHR in their cloud and the hospital still treats it as *theirs*. Most new EHR deployments in the past five years have been hosted; most existing on-prem deployments are migrating in that direction.

        Patient-facing apps, third-party clinical tools, registries, research platforms: almost all of these are cloud-native by default. On-prem is the older default; cloud is where most new work happens.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## The security boundaries that matter clinically.")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The U.S. legal and operational landscape around clinical data security rests on a handful of acronyms that show up in every project plan. Course 03 (privacy, ethics, governance) is where the field does this work seriously. For orientation, here is the shape.

        - **HIPAA.** The Health Insurance Portability and Accountability Act of 1996. The federal law that defines what counts as **Protected Health Information** (PHI), who is allowed to handle it (**covered entities** like hospitals and clinicians, and **business associates** that work for them), and what the **Privacy Rule** and **Security Rule** require of each. HIPAA is the floor every clinical project sits on. Almost every conversation about whether a particular data move is allowed begins with *does the receiver have a Business Associate Agreement, and what does it permit*.
        - **HITECH.** The 2009 law from Track 01 has a less-discussed second half: it strengthened HIPAA enforcement, expanded breach notification requirements, and extended liability to business associates directly. The reason vendors take HIPAA seriously is partly HITECH.
        - **HITRUST.** A private certification framework (run by the HITRUST Alliance) that takes HIPAA, NIST, ISO 27001, and a handful of other standards and bundles them into an auditable certification. Most cloud vendors selling into healthcare get HITRUST-certified because hospitals will not sign with them otherwise.
        - **SOC 2.** A more general security audit framework run by the AICPA. SOC 2 Type II reports show that a vendor's security controls have actually been operating effectively over a period of time, not only that they exist on paper. Required of most cloud-hosted clinical vendors.

        The pattern: every boundary clinical data crosses (LAN to firewall, firewall to internet, internet to vendor cloud, vendor cloud to research collaborator) has to be matched with a contract and a control that name what is allowed and how it is verified. The technical pieces (firewalls, encryption, identity systems) are necessary; the contractual pieces (BAAs, HITRUST, SOC 2) are how the legal world checks that the technical pieces are in place.

        Course 03 takes this seriously. For Course 0 the orientation is enough: the U.S. clinical data world is one of the most heavily regulated parts of the broader information economy, and the regulation is what shapes how the wires are run.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Walk the lab result.

        Take one CRP value (Ms. Reyes's 36.2 mg/L from 2024-01-08) and walk it through every system it touches and every boundary it crosses. Each stop names the system, the network zone, and the boundary the data crossed to get there.
        """
    )
    return


@app.cell
def _(mo):
    walk_picker = mo.ui.radio(
        options=[
            "Stop 1: Lab analyzer.",
            "Stop 2: Laboratory Information System (LIS).",
            "Stop 3: EHR (transactional database).",
            "Stop 4: Clinical data warehouse (CDW).",
            "Stop 5: Claims system at the insurer.",
            "Stop 6: Patient's phone (MyChart).",
            "Stop 7: Research collaborator's analytic environment.",
        ],
        label="Pick a stop.",
        value="Stop 1: Lab analyzer.",
    )
    walk_picker
    return (walk_picker,)


@app.cell
def _(mo, walk_picker):
    if walk_picker.value is None:
        walk_view = mo.md("")
    elif walk_picker.value.startswith("Stop 1"):
        walk_view = mo.callout(
            mo.md(
                "**Lab analyzer.** Physical machine in the basement chemistry lab. **Zone: "
                "hospital LAN.** The analyzer emits the result on the LAN as an HL7 v2 "
                "message (older) or a FHIR Observation (newer), addressed to the LIS. **Boundary "
                "crossed: none yet.** This traffic never leaves the building. The reason hospitals "
                "tolerate the cost of running labs on-prem is partly that having the analyzers on "
                "the same LAN as the LIS makes this leg of the journey effectively instantaneous "
                "and easy to control."
            ),
            kind="info",
        )
    elif walk_picker.value.startswith("Stop 2"):
        walk_view = mo.callout(
            mo.md(
                "**Laboratory Information System.** The LIS receives the analyzer message, "
                "applies any reflex testing rules, validates the result, attaches the canonical "
                "patient identifier, and stamps it into the lab database. **Zone: hospital LAN.** "
                "The LIS then emits the validated result to the EHR. **Boundary crossed: none, "
                "still on the LAN.** Two systems, one LAN, no firewall, no encryption in transit "
                "required beyond the LAN's own controls."
            ),
            kind="info",
        )
    elif walk_picker.value.startswith("Stop 3"):
        walk_view = mo.callout(
            mo.md(
                "**EHR (transactional database).** The EHR receives the lab result, files it in "
                "the patient's chart, fires any clinical decision support rules tied to lab "
                "results, refreshes the rheumatologist's *inbox* if she follows this patient, "
                "and refreshes the patient's *lab releases pending* queue for MyChart. **Zone: "
                "hospital LAN (if on-prem) or vendor cloud (if hosted).** If hosted, the result "
                "has already crossed the hospital's firewall through a permanent encrypted "
                "channel between the hospital and the vendor's cloud. Either way, the result is "
                "now in the OLTP database the rheumatologist will read at 9:14 a.m. tomorrow."
            ),
            kind="info",
        )
    elif walk_picker.value.startswith("Stop 4"):
        walk_view = mo.callout(
            mo.md(
                "**Clinical data warehouse.** Overnight, a scheduled batch job pulls the day's "
                "new lab results out of the EHR and into the CDW, restructured for analytic "
                "queries (OLTP to OLAP, the distinction from Track 03). **Zone: hospital LAN.** "
                "**Boundary crossed: typically none, both systems are inside the hospital.** "
                "Research queries hit the CDW, not the EHR, so the rheumatologist's workflow at "
                "9 a.m. tomorrow is not slowed by a researcher's overnight aggregation."
            ),
            kind="info",
        )
    elif walk_picker.value.startswith("Stop 5"):
        walk_view = mo.callout(
            mo.md(
                "**Claims system at the insurer.** When Ms. Reyes's rheumatology visit is "
                "submitted as a claim, the lab result is attached as supporting documentation "
                "(through the X12 837 claim format, with the lab attachment in CDA or PDF). "
                "**Zone: public internet (encrypted), then the insurer's network.** **Boundaries "
                "crossed: hospital firewall outbound; insurer firewall inbound.** The contract "
                "between the hospital and the insurer (and HIPAA's treatment-payment-operations "
                "carve-out) is what authorizes the cross-boundary move. The insurer's database is "
                "an entirely separate OLTP system that the hospital cannot see into."
            ),
            kind="info",
        )
    elif walk_picker.value.startswith("Stop 6"):
        walk_view = mo.callout(
            mo.md(
                "**Patient's phone.** Ms. Reyes opens MyChart on her phone the evening before "
                "her visit. The MyChart app makes an authenticated `GET` to the EHR's "
                "patient-facing API (often a FHIR endpoint), receives the lab result as JSON, "
                "and renders it on her screen. **Zone: public internet from her phone to the "
                "vendor cloud (or to the hospital data center), encrypted end-to-end with TLS.** "
                "**Boundary crossed: hospital firewall (or vendor cloud edge), inbound from "
                "outside.** Her authentication token is what lets the EHR confirm she is asking "
                "about her own labs and not somebody else's."
            ),
            kind="info",
        )
    else:
        walk_view = mo.callout(
            mo.md(
                "**Research collaborator's analytic environment.** A researcher at another "
                "institution, working under a data use agreement and an IRB-approved protocol, "
                "queries an aggregated cohort that includes Ms. Reyes's CRP. The data leaves the "
                "hospital's CDW, gets de-identified or limited-data-set transformed, and lands "
                "in a research enclave at the collaborator's institution. **Zone: public "
                "internet, encrypted; into a controlled research enclave on the other end.** "
                "**Boundaries crossed: CDW to de-identification pipeline; hospital firewall "
                "outbound under a DUA; collaborator's firewall inbound; into the research "
                "enclave.** Three layers of contract authorize this move: the DUA, the IRB "
                "protocol, and (depending on the data) the patient's research authorization."
            ),
            kind="info",
        )
    walk_view
    return (walk_view,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What you noticed walking the result.

        The same CRP value of 36.2 mg/L visits seven systems. Each system has a different job. Each move across a boundary is authorized by a different combination of technical control (firewall rule, encryption, identity token) and contractual control (BAA, DUA, IRB protocol).

        Two observations from the walk:

        - **The interesting boundaries are not the ones inside the building.** Stops 1 through 4 are all on the LAN; nothing dramatic happens between them. The boundaries that matter clinically (and the ones that take time and contracts to open) are the ones that leave the building: out to the insurer, out to the patient, out to the research collaborator.
        - **The data carries less context every time it crosses a boundary.** The analyzer knows everything about its own quality-control history. The LIS keeps most of that. The EHR keeps the value and the LOINC. The claims system gets the value and a CPT code. The patient gets the value rendered as a number with a flag. The researcher gets the value stripped of identifiers and standardized into a common data model. Each boundary is also a context-stripping event, and the field's interoperability work is largely about how much context can be preserved across the boundaries that need preserving.

        Course 03 (privacy and governance) is where the contracts get serious. Course 06 (FHIR) is where the API contracts get specific. Course 14 (interoperability policy) is where the policy that shapes the boundaries gets named. For Course 0 the takeaway is to be able to see the boundaries when somebody is talking about *moving the data* and to ask the right next question.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## One more.")
    return


@app.cell
def _(mo):
    boundary_quiz = mo.ui.radio(
        options=[
            "The LAN inside the building.",
            "The hospital firewall (outbound).",
            "The cloud vendor's edge.",
            "The patient's phone on her home Wi-Fi.",
            "The Business Associate Agreement with the vendor.",
        ],
        label=(
            "A health system is replacing an on-prem patient portal with a new cloud-hosted "
            "patient portal from a third-party vendor. After the cutover, when Ms. Reyes opens "
            "the portal on her phone, the portal app authenticates against the vendor's cloud, "
            "which makes a call to the hospital's FHIR endpoint to retrieve her labs. The portal "
            "vendor is HITRUST-certified and has a signed BAA with the health system. Which "
            "single piece of the new setup did *not* exist before this cutover and is the "
            "biggest new thing the security team has to think about?"
        ),
    )
    boundary_quiz
    return (boundary_quiz,)


@app.cell
def _(boundary_quiz, mo):
    if boundary_quiz.value is None:
        boundary_resp = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif boundary_quiz.value.startswith("The cloud vendor's edge"):
        boundary_resp = mo.callout(
            mo.md(
                "**Yes.** The LAN was already there. The hospital firewall was already there. "
                "The patient's phone was already there (she was using the old portal before the "
                "cutover). The BAA is a contract, and the security team is comfortable with how "
                "to do those. What is *new* is the vendor's cloud edge: a system the hospital "
                "does not own, that now holds the patient's authentication, that now makes calls "
                "into the hospital's FHIR endpoint on the patient's behalf. The new boundary the "
                "security team has to think about is the trust placed in the vendor's cloud as "
                "an intermediary between the patient and the hospital's data. HITRUST and the "
                "BAA are how the trust is verified; what is *new* is the trust itself."
            ),
            kind="success",
        )
    elif boundary_quiz.value.startswith("The LAN") or boundary_quiz.value.startswith("The hospital firewall"):
        boundary_resp = mo.callout(
            mo.md(
                "**Already existed before this cutover.** The LAN and the hospital firewall were "
                "already in place. What is new is the vendor cloud that the firewall now has to "
                "let into the FHIR endpoint."
            ),
            kind="warn",
        )
    elif boundary_quiz.value.startswith("The patient's phone"):
        boundary_resp = mo.callout(
            mo.md(
                "**Already existed before this cutover.** Ms. Reyes had a phone and a portal "
                "before. The new thing is what sits between her phone and the hospital data: a "
                "vendor cloud that did not exist in the old architecture."
            ),
            kind="warn",
        )
    else:
        boundary_resp = mo.callout(
            mo.md(
                "**A new contract, yes, but not the biggest *new* thing.** The BAA formalizes "
                "what the vendor is allowed to do. What is structurally new is the vendor's cloud "
                "itself sitting between the patient and the hospital data, and the BAA is how the "
                "field manages the trust in that cloud."
            ),
            kind="warn",
        )
    boundary_resp
    return (boundary_resp,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What you did in this track.

        - Named **client-server** through the restaurant analogy and saw that every clinical system you interact with is implicitly one role or the other.
        - Walked the four network zones (LAN, firewall, VPN, public internet) and what each one allows and constrains.
        - Named **HTTP, REST, and APIs** at concept level: HTTP is the protocol, REST is the convention, an API is the menu.
        - Distinguished **on-prem** from **cloud** and noted that most new clinical work is cloud or vendor-hosted.
        - Sketched the U.S. clinical security landscape (HIPAA, HITECH, HITRUST, SOC 2) and saw that every boundary clinical data crosses is matched with a contract and a technical control.
        - Walked Ms. Reyes's CRP through seven systems and noticed where the consequential boundaries actually are.

        ## What's next.

        **Track 05: The American health system and its parts.** The boundaries from this track are between systems run by different actors. The next track names the actors: who provides care, who pays for it, who builds the EHRs, who regulates the field, who runs public health, and which standards bodies hold the vocabularies together. By the end of Track 05 the picture of *who has to agree* for the kind of integration above to happen will be in place.
        """
    )
    return


if __name__ == "__main__":
    app.run()
