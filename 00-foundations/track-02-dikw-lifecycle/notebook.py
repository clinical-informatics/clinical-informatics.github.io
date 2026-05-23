"""Track 02: DIKW and the lifecycle of clinical data.

Plain English orientation. No code visible. The DIKW pyramid walked layer
by layer using Ms. Reyes's CRP, with Frické's 2009 critique cited honestly.
Then the lifecycle of clinical data (capture, store, use, share, retire)
walked through with the same CRP as a worked example.
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
        # Track 02: DIKW and the lifecycle of clinical data

        ## The number on the screen.

        Open Ms. Reyes's chart from this morning. Scroll to the lab tab. The first row reads:

        > C-reactive protein, 2024-01-08, 36.2 mg/L (reference 0 to 5, H)

        That is **a number on a screen**. By itself, it is not yet anything else. It is not a diagnosis. It is not a recommendation. It is not even, strictly, a fact about Ms. Reyes; it is a fact about a tube of her blood that a laboratory analyzer ran on the morning of the eighth.

        What turns that number into a clinical decision later in the visit is a series of steps that informatics has a name for. This track puts a vocabulary around those steps. The first half names the layers (data, information, knowledge, wisdom). The second half walks the same CRP through the lifecycle (capture, store, use, share, retire) and notices that the layering happens at every stage, not once.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## DIKW.")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **DIKW** stands for **data**, **information**, **knowledge**, **wisdom**. The acronym is older than clinical informatics; the field borrowed it from the broader information sciences in the 1980s and has been arguing with it ever since. It is the most widely taught hierarchy in the field and the easiest to misuse, so we will define each layer carefully and then look at what the framework gets wrong.

        Read each layer with the same CRP in mind.
        """
    )
    return


@app.cell
def _(mo):
    layer_picker = mo.ui.radio(
        options=[
            "Data: the raw signal.",
            "Information: the signal interpreted in context.",
            "Knowledge: the patterns the field has learned about signals like this one.",
            "Wisdom: knowing whether and how to act in this patient at this moment.",
        ],
        label="Pick a layer. Each one is a paragraph that walks Ms. Reyes's CRP through it.",
        value="Data: the raw signal.",
    )
    layer_picker
    return (layer_picker,)


@app.cell
def _(layer_picker, mo):
    if layer_picker.value is None:
        layer_view = mo.md("")
    elif layer_picker.value.startswith("Data"):
        layer_view = mo.callout(
            mo.md(
                "**Data.** The raw signal. For Ms. Reyes today the data is the value **36.2** "
                "with the unit **mg/L** attached to a specimen collected on **2024-01-08** and "
                "labeled with LOINC code **1988-5** (C-reactive protein, mass concentration in "
                "serum or plasma). At this layer the value has no clinical meaning yet. It is a "
                "measurement, faithfully recorded, with the metadata that tells you what was "
                "measured, when, and in what units. Without the metadata the number is not even "
                "data; it is a digit floating in nothing. Data is what gets logged. Whether it "
                "is useful is a different question for a different layer."
            ),
            kind="info",
        )
    elif layer_picker.value.startswith("Information"):
        layer_view = mo.callout(
            mo.md(
                "**Information.** The data interpreted in context. The value 36.2 mg/L is above "
                "the reference range (0 to 5 mg/L), which the lab system tags with an **H** flag. "
                "That flag turns the raw value into a statement: **Ms. Reyes has an elevated CRP**. "
                "Information layers the signal with what makes it noteworthy. Context that does "
                "this work here includes the reference range, the fact that the patient is "
                "Ms. Reyes specifically (not an anonymous tube), the prior values plotted on the "
                "same axis, and the unit-of-measure normalization that keeps mg/L from being "
                "compared against a value reported in mg/dL by accident. The CRP becomes "
                "information when it is *about* her, *compared to* something, and *flagged* in a "
                "way that draws attention."
            ),
            kind="info",
        )
    elif layer_picker.value.startswith("Knowledge"):
        layer_view = mo.callout(
            mo.md(
                "**Knowledge.** The patterns the field has learned about signals like this one. "
                "Knowledge here looks like: *elevated CRP in a patient with seropositive RA on a "
                "biologic, in the context of new joint symptoms and morning stiffness, raises the "
                "probability of inadequate disease control and warrants re-evaluation of "
                "treatment.* That sentence is not a fact about Ms. Reyes specifically; it is a "
                "rule the field has assembled from cohort studies, clinical trials, the EULAR and "
                "ACR treatment recommendations, and the accumulated experience of rheumatologists "
                "who have been wrong many times. Knowledge lives in guidelines, in textbooks, in "
                "the embedded rules of a clinical decision support tool, and in the trained "
                "rheumatologist's head. It is what lets information be acted on responsibly."
            ),
            kind="info",
        )
    else:
        layer_view = mo.callout(
            mo.md(
                "**Wisdom.** Knowing whether and how to act on the knowledge in *this* patient at "
                "*this* moment. The knowledge above says *re-evaluate*. Wisdom asks the next "
                "questions. Is the CRP elevation accompanied by other evidence of active disease, "
                "or is it discordant with a clean joint exam (in which case the next move may be "
                "to look for an occult infection or a competing inflammatory process)? Is the "
                "patient adherent to the methotrexate; has she had a recent dose increase her body "
                "has not caught up with yet? Is she three weeks past a viral illness that would "
                "leave a residually elevated CRP? Is now the right moment to escalate, or to "
                "watch for a month? Wisdom is the layer the field has the most trouble formalizing, "
                "because it is the layer where the patient stops being a row in a table and starts "
                "being a person."
            ),
            kind="info",
        )
    layer_view
    return (layer_view,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What the pyramid gets wrong.

        The DIKW hierarchy is usually drawn as a triangle with data at the bottom and wisdom at the top, with the implication that each layer is built cleanly out of the one below it. The most widely-cited critique of that picture is Martin Frické's 2009 paper, *The knowledge pyramid: a critique of the DIKW hierarchy*, published in the *Journal of Information Science*.

        Frické's argument, distilled: the layers do not have the sharp boundaries the picture suggests, and the *direction of flow* is not bottom-up the way the pyramid implies.

        - **Knowledge shapes what counts as data.** The lab analyzer reports CRP because the field already decided CRP is worth measuring. The reference range is built into the result. The choice of LOINC code is a choice the field made long before any individual specimen. Data is not raw; it arrives already filtered by the knowledge that asked for it.
        - **Information is sometimes more than data plus context, sometimes less.** The H flag is information about the value, but the H flag also strips away the subtlety of where in the elevated range the value sits. Two different rheumatologists looking at the same CRP of 36.2 may pull different information from it depending on the trend behind it.
        - **Wisdom is not more knowledge of the same kind.** A rheumatologist with twenty years of experience has not memorized twice as many guidelines as one with ten. The difference is taste about which guideline applies, taste built from being wrong in front of patients enough times to develop pattern recognition.

        The practical view: treat DIKW as a useful vocabulary for naming what is happening at each layer, but do not treat the layers as a fixed sequence. Most of the work of clinical informatics is helping the layers talk to each other, in both directions.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The lifecycle of clinical data.

        DIKW names *what* the data is at any moment. The lifecycle names *where* the data is in its journey through the systems that handle it. The lifecycle for a single clinical value has five stages.

        1. **Capture.** The value gets recorded.
        2. **Store.** The value is kept somewhere a system can retrieve.
        3. **Use.** The value is read in service of a decision.
        4. **Share.** The value moves outside the system that captured it.
        5. **Retire.** The value reaches the end of its operational life.

        Each stage has its own failure modes. Below, walk Ms. Reyes's CRP from 2024-01-08 through every stage. Click each stage to read what happens to that specific value at that step, and what can go wrong.
        """
    )
    return


@app.cell
def _(mo):
    stage_picker = mo.ui.radio(
        options=[
            "1. Capture.",
            "2. Store.",
            "3. Use.",
            "4. Share.",
            "5. Retire.",
        ],
        label="Pick a lifecycle stage. Same CRP, walked through each one.",
        value="1. Capture.",
    )
    stage_picker
    return (stage_picker,)


@app.cell
def _(mo, stage_picker):
    if stage_picker.value is None:
        stage_view = mo.md("")
    elif stage_picker.value.startswith("1."):
        stage_view = mo.callout(
            mo.md(
                "**Capture.** A phlebotomist drew a serum tube at 7:42 a.m. on 2024-01-08. The "
                "tube was barcoded and routed to the chemistry analyzer. The analyzer ran "
                "high-sensitivity CRP and emitted **36.2 mg/L** along with the LOINC code 1988-5, "
                "the specimen collection time, the patient identifier, the ordering provider, and "
                "the analyzer's own quality-control flags. The Laboratory Information System "
                "received that result and stamped it into Ms. Reyes's record.\n\n"
                "**What can go wrong here.** Mislabeled specimen (the tube belonged to the patient "
                "in the next bay). Wrong unit pulled from the analyzer (mg/dL instead of mg/L, "
                "which silently makes the value look ten times higher). LOINC mapping incorrect "
                "(routine CRP mapped to high-sensitivity CRP or vice versa, two different LOINCs "
                "with similar names). Specimen sat for two hours on a warm cart and the assay drifted. "
                "Capture is the layer with the most room for the most boring errors, and the most "
                "consequential ones, because every later layer trusts what capture handed it."
            ),
            kind="info",
        )
    elif stage_picker.value.startswith("2."):
        stage_view = mo.callout(
            mo.md(
                "**Store.** The value lives in at least three places at once. The **Laboratory "
                "Information System** keeps the canonical lab record, including the raw analyzer "
                "trace if the lab keeps those. The **EHR** caches a copy in its own database, "
                "indexed by patient and date, optimized for the rheumatologist who will read it in "
                "two weeks. The **clinical data warehouse** receives a copy overnight, restructured "
                "for analytic queries instead of transactional reads. (The distinction between "
                "transactional and analytical storage is the OLTP-vs-OLAP question; Course 00 "
                "Track 3 of this course names it formally.)\n\n"
                "**What can go wrong here.** The three copies drift out of sync (the LIS corrects "
                "the value at noon; the EHR cache still shows the original). The CDW load fails "
                "overnight and the value is missing from research queries for three days. The "
                "value is stored with a timezone the downstream system does not know to convert, "
                "so the collection time shifts by a day at year-end. Backups exist for the LIS but "
                "not for the EHR cache, so a partial outage restores some copies and not others."
            ),
            kind="info",
        )
    elif stage_picker.value.startswith("3."):
        stage_view = mo.callout(
            mo.md(
                "**Use.** The rheumatologist opens the chart at 9:14 a.m. on the morning of the "
                "follow-up. The CRP appears in the lab trend graph alongside the prior values "
                "(11.6 mg/L in November, 22.5 in February of the year before). It feeds the "
                "DAS28 score the rheumatologist enters at the bottom of the note. It is checked "
                "by a CDS rule that compares the result to a threshold for biologic dose "
                "adjustment. It is also displayed on Ms. Reyes's MyChart, where she sees it the "
                "evening before the visit and writes a portal message asking what it means.\n\n"
                "**What can go wrong here.** The trend graph defaults to a six-month window and "
                "hides the 2022 baseline, making the trajectory look more alarming or more "
                "reassuring than it is. The DAS28 calculator pulls the wrong CRP (a result from "
                "an inpatient stay six months ago is more recent in the lab table than the "
                "outpatient draw). The CDS rule fires inappropriately because Ms. Reyes is three "
                "weeks past a viral URI. MyChart renders the value without context and Ms. Reyes "
                "spends the night convinced her disease is out of control."
            ),
            kind="info",
        )
    elif stage_picker.value.startswith("4."):
        stage_view = mo.callout(
            mo.md(
                "**Share.** The value moves outside the system that captured it. The insurer "
                "receives it inside an attached lab report supporting the rheumatology visit "
                "claim. The patient downloads it through the **Blue Button** style export on her "
                "MyChart account. A research network the health system contributes to receives "
                "it inside the nightly OMOP-mapped extract that feeds the network's federated "
                "analyses. A specialist at a different health system receives it in a Continuity "
                "of Care Document attached to a referral.\n\n"
                "**What can go wrong here.** The value's LOINC code is dropped in transit and the "
                "receiving system only gets a local lab name it does not recognize. The patient "
                "downloads a copy in 2025 and a researcher in 2028 cannot tell if the value was "
                "collected in 2024 or copied forward from an earlier visit. The specialist's "
                "EHR cannot ingest the CDA cleanly and the value lands in a PDF attachment nobody "
                "opens. The research network's privacy review takes nine months while the question "
                "the research was trying to answer goes stale. Sharing is where the field's "
                "interoperability work earns its name; Courses 06 (FHIR) and 14 (interoperability "
                "policy) carry the thread."
            ),
            kind="info",
        )
    else:
        stage_view = mo.callout(
            mo.md(
                "**Retire.** A clinical value almost never gets deleted in the way the word "
                "*retire* suggests. The EHR retains lab data for the patient's lifetime plus the "
                "state's record-retention window (often six to ten years past last contact for "
                "adults, longer for minors). The CDW keeps it as long as the institution finds "
                "it useful. A research dataset built from it may be preserved indefinitely under "
                "the data-sharing terms of whatever grant funded it. Even the analyzer's raw "
                "trace may be archived to cold storage rather than discarded.\n\n"
                "**What can go wrong here.** The retention rule conflicts with a deletion request "
                "from a patient who has moved health systems. A research extract from 2014 is "
                "still circulating after the consent it relied on has expired. A backup tape from "
                "2009 is found in a closet and nobody is sure whether it counts as in-scope for "
                "the new privacy review. Retirement is the stage the field thinks about least and "
                "the one regulators are paying the most attention to right now. Course 03 (privacy, "
                "ethics, governance) lives in this stage."
            ),
            kind="info",
        )
    stage_view
    return (stage_view,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The lifecycle and DIKW together.

        The two frameworks layer. At every stage of the lifecycle, the value can be examined at every layer of DIKW.

        - At **capture**, the data is being created. The information is whether the H flag fires. The knowledge is the reference range the flag is calibrated against. The wisdom is the laboratory medicine specialist who set the reference range for the assay in the first place.
        - At **use**, the data is the same number. The information is the trend graph the rheumatologist sees. The knowledge is the EULAR treatment recommendation she has in mind. The wisdom is her decision about Ms. Reyes specifically.
        - At **share**, the data needs to keep its metadata; the information needs to keep its context; the knowledge needs to keep its provenance; the wisdom is whatever the receiving clinician brings to bear once the value arrives.

        Most failures in clinical informatics are a failure at one specific intersection: a stage of the lifecycle where one layer of DIKW gets stripped away. The lab value arrives at the research dataset with no reference range. The MyChart export shows the value without the trend. The DAS28 calculator gets the right value at the wrong time.

        Naming the intersection is what lets the field fix it.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## One more.")
    return


@app.cell
def _(mo):
    intersection_quiz = mo.ui.radio(
        options=[
            "Capture is broken (the value itself is wrong).",
            "Store is broken (the value is wrong in the EHR cache).",
            "Use is broken (a DIKW layer is being stripped at the moment of reading).",
            "Share is broken (the value is being mis-transmitted to MyChart).",
            "Retire is broken (an old value is being shown that should have been hidden).",
        ],
        label=(
            "Ms. Reyes opens MyChart the night before her visit and sees the CRP of 36.2 mg/L "
            "displayed in red with an H flag. There is no reference range. There is no trend "
            "line. There is no comment from her rheumatologist. She spends the night convinced "
            "her disease is flaring and writes a portal message at 11 p.m. asking whether she "
            "should go to the emergency room. The value the lab measured was correct. The value "
            "in the EHR is correct. The value in MyChart is correct. Where in the lifecycle is "
            "the failure?"
        ),
    )
    intersection_quiz
    return (intersection_quiz,)


@app.cell
def _(intersection_quiz, mo):
    if intersection_quiz.value is None:
        intersection_response = mo.callout(mo.md("_Pick one._"), kind="neutral")
    elif intersection_quiz.value.startswith("Use"):
        intersection_response = mo.callout(
            mo.md(
                "**Yes.** The data is fine. The store is fine. The share moved it correctly to "
                "MyChart. The failure is at the *use* stage: MyChart received the value but "
                "stripped the information layer (the reference range), the knowledge layer "
                "(what this value means in the context of her treated RA), and any path to the "
                "wisdom layer (the rheumatologist who could have annotated this value before she "
                "saw it). The value she is reading is correct, but as displayed it is data masquerading "
                "as information. Fixing this is a clinical informatics problem: it is about what "
                "the patient sees at the moment of use, not about what the lab measured. The fix "
                "lives at the user-experience layer of MyChart, in the policies about which results "
                "release immediately and which are held for clinician annotation, and in the "
                "workflows that get clinician context to the patient before the patient is alone "
                "with the value at 11 p.m."
            ),
            kind="success",
        )
    elif intersection_quiz.value.startswith("Share"):
        intersection_response = mo.callout(
            mo.md(
                "**Close, but the question says the value in MyChart is correct.** Sharing is "
                "what moved the value into MyChart; that move worked. The failure is what happens "
                "when MyChart renders the value for Ms. Reyes. That is a use-stage problem, not "
                "a share-stage problem."
            ),
            kind="warn",
        )
    elif intersection_quiz.value.startswith("Capture") or intersection_quiz.value.startswith("Store"):
        intersection_response = mo.callout(
            mo.md(
                "**Not in this scenario.** The question is clear that the lab value is correct "
                "and the EHR copy is correct. So whatever is going wrong is happening after the "
                "value has been captured and stored faithfully. That points downstream."
            ),
            kind="warn",
        )
    else:
        intersection_response = mo.callout(
            mo.md(
                "**Not in this scenario.** Retire is about how long a value persists. The value "
                "here is recent and properly current. The failure is at the moment Ms. Reyes "
                "reads it on her phone, which is a use-stage problem."
            ),
            kind="warn",
        )
    intersection_response
    return (intersection_response,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What you did in this track.

        - Walked Ms. Reyes's CRP through the four layers of DIKW (data, information, knowledge, wisdom) and saw what each layer adds.
        - Read Frické's critique honestly: the layers blur, the direction of flow is not strictly bottom-up, and the field treats DIKW as vocabulary, not gospel.
        - Walked the same value through the lifecycle (capture, store, use, share, retire) and named the failure modes at each stage.
        - Located one common clinical failure (the patient alone with a context-stripped value at 11 p.m.) at a specific intersection of stage and layer.

        ## What's next.

        **Track 03: How computers represent and store data.** The lifecycle's capture and store stages depend on machines actually keeping the value. The next track names what that looks like underneath: bits, the data structures the field uses, the four file types most clinical data lives in (TXT, CSV, JSON, XML), and the distinction every health system runs into between the transactional database that supports clinical work (OLTP) and the analytic database that supports research (OLAP).
        """
    )
    return


if __name__ == "__main__":
    app.run()
