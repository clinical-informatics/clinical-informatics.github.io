"""Track 02: HL7 v2, CDA, and what we inherited.

A historical walk through the messaging standards that hospitals run on
right now: HL7 v2 (1987 and still dominant), CDA (2005), and the path
that led to FHIR. Built around real-shaped synthetic messages for
Ms. Reyes.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import types

    import marimo as mo
    import pandas as pd

    # Cross-reference helpers inlined from shared/cross_reference.py so the
    # WASM export is self-contained. Exposed as the `xref` namespace so the
    # call sites read the same as before.
    _COURSE_TITLES = {
        "00": "Foundations of clinical informatics",
        "01": "Computational thinking",
        "02": "Data literacy",
        "03": "Privacy, ethics, and governance",
        "04": "Clinical epidemiology",
        "05": "EHR systems",
        "06": "Learn FHIR",
        "07": "Data wrangling and engineering",
        "08": "Clinical visualization",
        "09": "AI in medicine",
        "10": "NLP and clinical text",
        "11": "Health economics data",
        "12": "Clinical decision support",
        "13": "Research reproducibility",
        "14": "Interoperability policy",
        "15": "Data storytelling",
    }

    def _course_label(course_id):
        title = _COURSE_TITLES.get(course_id.split("-")[0])
        if title is None:
            return course_id
        return f"course {course_id.split('-')[0]}: {title}"

    def _xref_callback(from_course, to_course, topic, body):
        src = _course_label(to_course)
        return mo.callout(
            mo.vstack([mo.md(f"**Remember {topic} from {src}?**"), mo.md(body)]),
            kind="info",
        )

    def _xref_forward(from_course, to_course, topic, body):
        dst = _course_label(to_course)
        return mo.callout(
            mo.vstack([mo.md(f"**Forward to {dst}: {topic}**"), mo.md(body)]),
            kind="neutral",
        )

    xref = types.SimpleNamespace(callback=_xref_callback, forward=_xref_forward)

    return mo, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 02: HL7 v2, CDA, and what we inherited

        ## Why the lab system in the basement still talks 1987

        Right now, while you read this, a stream of messages is flowing across the network in your hospital. The lab sends a result to the EHR. The EHR sends a registration to the billing system. The radiology system sends an order acknowledgment to the EHR. The pharmacy system sends a verification back to the lab. None of these messages are FHIR. Almost all of them are HL7 v2 pipe-and-caret messages, in a format that was standardized in 1987 and that has not had a breaking-change major release since.

        That fact tends to surprise people who have only seen the FHIR side. FHIR is real, it is growing fast, and external interfaces to the EHR (patient apps, payer connections, public-health reporting) increasingly run on it. But inside the hospital, between the systems that have been talking to each other for two decades, the protocol is still v2. Forty years of accumulated investment is hard to rip out, and v2 mostly works for what it does.

        This track is the historical arc. We read a real HL7 v2 ADT message. We read a real HL7 v2 ORU result message. We read a CDA fragment. We trace how each format solved a problem and created a new one, and we end at the door of course 06 (Learn FHIR).

        The messages all describe Ms. Reyes's 2024-01-08 rheumatology visit.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A very short history

        | Year | Standard | What it was for | What it could not do |
        |---|---|---|---|
        | 1987 | HL7 v2.1 | Encoded clinical events as pipe-delimited messages for system-to-system transport inside a hospital | Carry rich documents. Cross-vendor consistency. Strict validation. |
        | 1996 | HL7 v2.3 | The version most hospitals settled on. Reasonably mature. | Same. Also, optionality everywhere. |
        | 2003 | HL7 v3 (RIM-based) | An attempt at a fully-typed object model for clinical information | Adoption. Too complex; mostly abandoned outside Europe and government settings. |
        | 2005 | CDA Release 2 | Structured *documents* (CCD, C-CDA), built on the HL7 v3 RIM, XML-based | Practical machine-readability. Most CDA documents in the wild are rendered for humans, not consumed programmatically. |
        | 2014 | FHIR DSTU 1 | RESTful resource-based exchange built on web standards (HTTP, JSON, OAuth) | Replace the installed base. Not yet, anyway. |
        | 2017 | US Core IG | A profile of FHIR R3/R4 that US vendors agreed to support | (Track 04 of course 06 covers this) |
        | 2020 | ONC Cures Act final rule | Required US-certified EHRs to expose FHIR R4 APIs | Force the internal hospital messaging stack to follow suit. |

        The lesson in that table is not that HL7 v2 was bad. The lesson is that **each standard was the correct answer to the problem in front of the field at the time**. v2 solved 1987's problem (let me get a result from the lab into the EHR without writing custom code for each integration). CDA solved 2005's problem (let me share a discharge summary with the next provider in a way they can render and store). FHIR is solving 2014's problem (let me build apps and APIs on top of clinical data using standard web tools). They coexist now. The hospital you work at probably uses all three at once.

        Let's read them.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## HL7 v2: ADT^A04 (patient registration)

        The most common message type in any hospital is ADT: admit, discharge, transfer. Every time a patient is registered, their status changes, their bed moves, their demographics get updated, an ADT message is fired. The EHR sends ADT to the lab so the lab knows who the new patient is. The EHR sends ADT to the radiology system. The EHR sends ADT to the billing system. ADT is the heartbeat of the hospital.

        Below is an ADT^A04 (register a new outpatient encounter) for Ms. Reyes's 2024-01-08 visit. This is what the message looks like on the wire.
        """
    )
    return


@app.cell
def _(mo):
    adt_message = (
        "MSH|^~\\&|REGADT|MCM|ADTUPD|MCM|20240108080000||ADT^A04|9821001|P|2.5|||AL|NE|||EN\r"
        "EVN|A04|20240108080000\r"
        "PID|||ER-001^^^MCM^MR~Z9847562^^^MCM^PI||Reyes^Elena^Maria^^^^L||19740209|F||W^White^HL70005|"
        "742 Elm Street^^Springfield^MA^01103^USA^H||(555)0142|||M^Married^HL70002|||"
        "999-00-1234|||H^Hispanic or Latino^HL70189\r"
        "PV1||O|RHEUM^^^MCM||||DOC0044556^Bennett^Maya^^^MD|||REH|||||||||V|9912001|||||||||||||||||||MCM|||||20240108083000\r"
        "DG1|1||M05.79^Seropositive erosive rheumatoid arthritis^I10|||F\r"
        "GT1|1||Reyes^Elena^Maria||742 Elm Street^^Springfield^MA^01103|(555)0142||19740209|F|P|SE\r"
        "IN1|1|BCBS001^Blue Cross Blue Shield of MA^MCM|BCBSMA|Blue Cross Blue Shield of Massachusetts|"
        "1 Boston Place^^Boston^MA^02108||||||||||||Reyes^Elena^Maria|SE|19740209|||||||||||||||||||PPO123456789\r"
    )

    mo.vstack([
        mo.md("**Raw ADT^A04 message (one wire transmission, eight segments):**"),
        mo.md(f"```\n{adt_message.replace(chr(13), chr(10))}```"),
    ])
    return (adt_message,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Stare at that long enough and the shape becomes legible. Eight lines. Each line is a **segment**. The first three letters of each segment name the kind of segment. The bars (`|`) split the segment into **fields**. Within a field, the carets (`^`) split it into **components**. Within a component, ampersands (`&`) split it into subcomponents. The whole thing is a tree, and the punctuation tells you which level of the tree you are at.

        Here is the segment breakdown:

        | Segment | What it carries |
        |---|---|
        | `MSH` | Message header: the sending and receiving systems, the timestamp, the message type (`ADT^A04`), the version (`2.5`), the message control id |
        | `EVN` | Event type and event timestamp |
        | `PID` | Patient identification: MRN, name, DOB, sex, address, phone, marital status, SSN, race, ethnicity |
        | `PV1` | Patient visit: visit number, patient class (O = outpatient), assigned location (`RHEUM`), attending provider |
        | `DG1` | Diagnosis: ICD-10 M05.79 (seropositive erosive RA), final status |
        | `GT1` | Guarantor: who is financially responsible |
        | `IN1` | Insurance: payer information, policy id |

        The vocabulary inside the message points at HL7-controlled tables (HL70005 for race, HL70002 for marital status, HL70189 for ethnicity) and at standard coding systems (`I10` for ICD-10).

        Two structural details to absorb before we look at the lab message:

        1. **Most fields are optional.** A `PID` segment has 39 defined fields. The example above populates roughly a dozen of them. Two different hospitals' ADT^A04 messages will populate different fields. That is the source of most cross-vendor integration pain.
        2. **The standard reserves "Z-segments" for site-specific extensions.** If a hospital needs to send a field that the standard does not define, it adds a `Z` segment like `ZPV` or `ZDG`. Z-segments are valid v2; they are also non-portable by design. Every hospital that builds a Z-segment has effectively created a private dialect.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## HL7 v2: ORU^R01 (a CRP result)

        ORU (observation result unsolicited) is the message type used to ship lab and observation results. Here is the ORU^R01 that the lab analyzer would fire when Ms. Reyes's 2024-01-08 CRP comes back.
        """
    )
    return


@app.cell
def _(mo):
    oru_message = (
        "MSH|^~\\&|LAB|MCM|EHRADT|MCM|20240108091500||ORU^R01|MSG20240108-77|P|2.5\r"
        "PID|||ER-001^^^MCM^MR||Reyes^Elena^Maria||19740209|F\r"
        "OBR|1||LAB-400001|1988-5^C reactive protein^LN|||20240108090000|||||||20240108090000||"
        "DOC0044556^Bennett^Maya|||||LAB-400001|||F\r"
        "OBX|1|NM|1988-5^C reactive protein^LN||36.2|mg/L^^UCUM|0-5|H|||F|||20240108091500\r"
        "OBR|2||LAB-400002|4537-7^Erythrocyte sedimentation rate^LN|||20240108090000|||||||20240108090000||"
        "DOC0044556^Bennett^Maya|||||LAB-400002|||F\r"
        "OBX|2|NM|4537-7^Erythrocyte sedimentation rate^LN||51|mm/h^^UCUM|0-20|H|||F|||20240108091500\r"
        "OBR|3||LAB-400003|32218-7^Cyclic citrullinated peptide IgG Ab^LN|||20240108090000|||||||20240108090000||"
        "DOC0044556^Bennett^Maya|||||LAB-400003|||F\r"
        "OBX|3|NM|32218-7^Cyclic citrullinated peptide IgG Ab^LN||154|U/mL^^UCUM|<20|H|||F|||20240108091500\r"
    )

    mo.vstack([
        mo.md("**Raw ORU^R01 (three result components from a single lab order set):**"),
        mo.md(f"```\n{oru_message.replace(chr(13), chr(10))}```"),
    ])
    return (oru_message,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Same shape as the ADT message. The interesting segments are `OBR` and `OBX`.

        - **`OBR`** describes the *order*: which test was ordered, when it was collected, when it was reported, who ordered it. One OBR per lab test.
        - **`OBX`** carries the *result value*: the result type (`NM` for numeric), the LOINC code, the actual value, the units, the reference range, the abnormal flag (`H` for high), the result status (`F` for final).

        Look at the OBX for CRP: `1988-5^C reactive protein^LN`. That `LN` at the end is the HL7 code for LOINC, the international vocabulary for laboratory observations. So the lab is saying: "the value of LOINC 1988-5 (which is C-reactive protein) is 36.2, in UCUM units of mg/L, the normal range is 0 to 5, and this is flagged as High."

        That is real interoperability. The receiving EHR can parse this, look up LOINC 1988-5 in its own concept tables, and store the result in a row of its `LAB_RESULT` table (Track 01) without any custom mapping. **When v2 works, it works well.**
        """
    )
    return


@app.cell
def _(mo):
    msg_quiz = mo.ui.radio(
        options=[
            "OBR-2 (Order control ID): always populated identically across vendors.",
            "OBX-3 (Observation identifier): some vendors use a local code instead of LOINC, or omit the coding-system suffix.",
            "OBX-2 (Value type): the only place a vendor can change the data type.",
            "MSH-9 (Message type): vendors cannot change the type identifier.",
        ],
        label=(
            "**The promise of LOINC-coded OBX rows is full interoperability. The reality is that many ORU messages "
            "in production fail to interoperate cleanly. Which field is the most common single point of failure?**"
        ),
    )
    msg_quiz
    return (msg_quiz,)


@app.cell
def _(mo, msg_quiz):
    mo.stop(msg_quiz.value is None, mo.md("_Choose an answer._"))
    msg_correct = msg_quiz.value.startswith("OBX-3 ")

    if msg_correct:
        msg_quiz_feedback = (
            "Right. OBX-3 is the observation identifier (a CWE field that should hold the standard code, the display name, "
            "and the coding system). In practice, lab systems with older interfaces or local quirks often send a *local* "
            "code (the lab's internal test code like `CRP-HOSP`) without a LOINC equivalent, or send LOINC without "
            "the coding-system suffix, or send the wrong LOINC for what they actually measured. The EHR receiving the "
            "message has to maintain a local mapping table to figure out what each lab actually means. The mapping "
            "table is *the* unglamorous data-quality artifact at every health system that handles ORU messages."
        )
    else:
        msg_quiz_feedback = (
            "Not quite. The single most common failure point is OBX-3 (observation identifier): "
            "many ORU messages in production carry a local lab code instead of LOINC, omit the coding-system suffix, "
            "or carry the wrong LOINC for what was actually measured. Every health system that ingests ORU traffic "
            "maintains a manual mapping table to translate local codes into standard ones. That mapping table is "
            "where v2 interoperability quietly leaks."
        )
    mo.callout(mo.md(msg_quiz_feedback), kind="success" if msg_correct else "warn")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What v2 cannot do

        Three structural limits on HL7 v2 are worth naming explicitly:

        1. **It is message-shaped, not document-shaped.** v2 ships a result, an order, a registration. It does not ship a discharge summary or a problem-oriented chart note in any complete form. Vendors have built v2 message types that approximate documents (the MDM message for clinical documents), but they are not the natural fit.
        2. **Optionality is structural.** Roughly every field in the spec is optional in some context. Two valid ADT^A04 messages from two valid sending systems can look completely different. Validation is loose. Most v2 traffic is validated by the receiving system at runtime, not by a contract at design time.
        3. **Custom Z-segments fork the standard.** The standard sanctions site-specific extensions. Every hospital that uses them has a private dialect that other hospitals cannot parse without local knowledge.

        Those three limits are why CDA was attempted.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## CDA: structured documents

        CDA (Clinical Document Architecture) is the HL7 v3 attempt at a document-shaped exchange format. A CDA document is a single XML file that combines:

        - **A header** with metadata: who, what, when, why, signed by whom.
        - **A human-readable body**: a narrative section that any web browser can render. This is the part the receiving clinician sees.
        - **Optional structured entries** inside each section: the same facts as the narrative, but encoded with standard codes so a machine can pick them out.

        The big use case is the **Continuity of Care Document (CCD)**: a clinical summary that travels with a patient from one provider to the next. Meaningful Use Stage 2 (2014) required that certified EHRs be able to generate and consume CCDs, which is the reason CDA became ubiquitous in US hospitals.

        Below is a (heavily trimmed) CDA fragment carrying Ms. Reyes's problem list from 2024-01-08.
        """
    )
    return


@app.cell
def _(mo):
    cda_fragment = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <typeId root="2.16.840.1.113883.1.3" extension="POCD_HD000040"/>
  <templateId root="2.16.840.1.113883.10.20.22.1.2"/>
  <code code="34133-9" displayName="Summarization of Episode Note"
        codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC"/>
  <title>Continuity of Care Document - Ms. Elena Reyes</title>
  <effectiveTime value="20240108083000-0500"/>
  <recordTarget>
    <patientRole>
      <id extension="ER-001" root="2.16.840.1.113883.19.5"/>
      <patient>
        <name use="L">
          <given>Elena</given>
          <given qualifier="MID">Maria</given>
          <family>Reyes</family>
        </name>
        <administrativeGenderCode code="F" codeSystem="2.16.840.1.113883.5.1"/>
        <birthTime value="19740209"/>
      </patient>
    </patientRole>
  </recordTarget>
  <component>
    <structuredBody>
      <component>
        <section>
          <templateId root="2.16.840.1.113883.10.20.22.2.5.1"/>
          <code code="11450-4" displayName="Problem List"
                codeSystem="2.16.840.1.113883.6.1"/>
          <title>Problems</title>
          <text>
            <table>
              <thead><tr><th>Problem</th><th>Onset</th><th>Status</th></tr></thead>
              <tbody>
                <tr><td>Seropositive erosive rheumatoid arthritis</td>
                    <td>2022-03-07</td><td>Active</td></tr>
                <tr><td>Anemia of chronic disease</td>
                    <td>2022-02-14</td><td>Active</td></tr>
              </tbody>
            </table>
          </text>
          <entry typeCode="DRIV">
            <act classCode="ACT" moodCode="EVN">
              <templateId root="2.16.840.1.113883.10.20.22.4.3"/>
              <code code="CONC" codeSystem="2.16.840.1.113883.5.6"/>
              <statusCode code="active"/>
              <effectiveTime><low value="20220307"/></effectiveTime>
              <entryRelationship typeCode="SUBJ">
                <observation classCode="OBS" moodCode="EVN">
                  <templateId root="2.16.840.1.113883.10.20.22.4.4"/>
                  <code code="55607006" displayName="Problem"
                        codeSystem="2.16.840.1.113883.6.96"
                        codeSystemName="SNOMED CT"/>
                  <statusCode code="completed"/>
                  <value xsi:type="CD" code="M05.79"
                         displayName="Seropositive erosive rheumatoid arthritis"
                         codeSystem="2.16.840.1.113883.6.90"
                         codeSystemName="ICD-10-CM"/>
                </observation>
              </entryRelationship>
            </act>
          </entry>
        </section>
      </component>
    </structuredBody>
  </component>
</ClinicalDocument>"""

    mo.vstack([
        mo.md("**CDA fragment (Continuity of Care Document, Problem List section, trimmed):**"),
        mo.md(f"```xml\n{cda_fragment}\n```"),
    ])
    return (cda_fragment,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three observations about CDA that the fragment makes legible:

        1. **Two parallel renderings of the same fact.** The `<text>` section has a human-readable HTML table of the problem list. The `<entry>` section has the same fact encoded with ICD-10 and SNOMED CT codes for a machine to pick up. The narrative and the structured entry are supposed to mean the same thing. **In practice they often do not match**, and the standard does not enforce that they should. That mismatch is one of CDA's quiet failures.
        2. **Everything is keyed to template ids.** The CCD template tree (the OID `2.16.840.1.113883.10.20.22...`) is how the standard says "this is a Problem List section, this is a Problem Concern entry." A receiving system that does not know the template tree cannot pick the structured entries out reliably.
        3. **The data is buried under namespaces and codes.** To read the patient's diagnosis you have to find the `<observation>` inside the `<entryRelationship>` inside the `<act>` inside the `<entry>` inside the `<section>` inside the `<structuredBody>` inside the `<component>`. CDA is dense.

        CDA's strengths are real. It is a *document*, which is the right shape for the discharge-summary use case. It carries both human and machine renderings, which matches how documents actually get used. It has been written into law (Meaningful Use Stage 2) as the inter-EHR document format, so it is ubiquitous.

        CDA's weaknesses are also real, and they are why FHIR happened. The XML is heavy. The template trees are dense. Building software against CDA requires learning the v3 RIM, which most developers never want to do. And the optional-structured-entry pattern means that *practical* machine readability is low: most CDA documents in production are rendered for humans and never parsed.
        """
    )
    return


@app.cell
def _(xref):
    xref.forward(
        from_course="05",
        to_course="06",
        topic="Where FHIR picks up",
        body=(
            "FHIR (Fast Healthcare Interoperability Resources) is the standard that picked up where HL7 v2 and CDA left off. "
            "Course 06 (Learn FHIR) walks the format end to end: Track 0 covers the web-architecture history that made FHIR possible, "
            "Tracks 1 to 5 cover resources, server interaction, modeling, implementation guides, and SMART on FHIR. "
            "The short version for now: FHIR is REST-and-JSON over HTTP, which is the same web architecture every app and "
            "browser is already built on. That is the bet, and it has mostly paid off for external APIs. The internal "
            "hospital messaging stack is still mostly v2 and will be for years."
        ),
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Where this leaves you

        Most of the messaging inside the hospital still moves on a format from 1987. CDA is the document standard the field landed on for inter-EHR summaries, and FHIR is the standard new external work is being built against. The three coexist; they were each the correct answer at the time they were specified, and replacement is slow because the installed base is large.

        Track 03 is about what happens when this messaging traffic gets poured into a system designed for analytics rather than for the chart.
        """
    )
    return


if __name__ == "__main__":
    app.run()
