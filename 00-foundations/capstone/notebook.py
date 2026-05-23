"""Capstone for course 00: foundations of clinical informatics.

Socratic walkthrough of a single scenario (a community hospital wanting
to share readmission predictions with its accountable care organization)
that exercises every track in the course at once. Four committed answers
across DIKW, the computer-science and network plumbing, the stakeholders,
and governance, with reveals on each.

This is an orientation capstone, not a technical-depth capstone. The
goal is to verify the learner can see the whole system at once.
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
    # Socratic helpers inlined from shared/socratic.py so the WASM export is
    # self-contained. Pyodide cannot import sibling modules from the source
    # tree, so the live-site export needs the helpers defined in the notebook
    # itself. Mirrors the API of start-here/shared/socratic.py.

    def commit_text(prompt, *, min_chars=40):
        widget = mo.ui.text_area(
            label=prompt,
            rows=6,
            full_width=True,
            placeholder="Take a few sentences. The reveal won't unlock until you do.",
        )

        def _ready():
            value = widget.value or ""
            return len(value.strip()) >= min_chars

        return widget, _ready

    def reveal(learner_value, ideal_answer, *, learner_label="Your answer"):
        learner_display = learner_value if learner_value else "_(no answer yet)_"
        return mo.hstack(
            [
                mo.callout(
                    mo.vstack(
                        [
                            mo.md(f"**{learner_label}**"),
                            mo.md(str(learner_display)),
                        ]
                    ),
                    kind="neutral",
                ),
                mo.callout(
                    mo.vstack(
                        [
                            mo.md("**How we'd think through this**"),
                            mo.md(ideal_answer),
                        ]
                    ),
                    kind="success",
                ),
            ],
            widths="equal",
        )

    def reflection(prompt, placeholder=""):
        widget = mo.ui.text_area(
            label=prompt,
            rows=5,
            full_width=True,
            placeholder=placeholder
            or "Take a few sentences. No reveal here. The reflection is the work.",
        )
        layout = mo.vstack(
            [
                widget,
                mo.callout(
                    mo.md(
                        "_There's no answer key for this one. The point isn't to be right. "
                        "It's to make your reasoning explicit to yourself._"
                    ),
                    kind="neutral",
                ),
            ]
        )
        return widget, layout

    def go_deeper(body):
        return mo.callout(
            mo.vstack(
                [
                    mo.md("### Go deeper"),
                    mo.md(body),
                ]
            ),
            kind="info",
        )

    return commit_text, go_deeper, reflection, reveal


@app.cell
def _(mo):
    mo.md(
        r"""
        # Capstone: foundations of clinical informatics

        ## The scenario on the table.

        **Walden Community Hospital** is a 180-bed community hospital in a midsized U.S. metro. It is the only hospital in its county that runs a true full-service inpatient operation; the next nearest is forty minutes away. Walden's outpatient footprint is six primary-care clinics, a small multispecialty group, and a rheumatology clinic where Ms. Reyes is a patient.

        Walden joined a Medicare Shared Savings Program **Accountable Care Organization** (ACO) two years ago. The ACO is a partnership with four other regional hospitals and roughly 240 affiliated physician practices. Under the shared-savings contract, the ACO is measured on (among other things) thirty-day readmission rates for its attributed Medicare beneficiaries. Money flows back to Walden and the other ACO partners if the ACO beats its benchmarks. Money flows the other way if it does not.

        Walden's data-science team has built a thirty-day readmission prediction model that runs nightly against the inpatients on the medicine service. The model output (a probability score from 0 to 1) appears in the EHR the next morning. The discharge planning team uses the score, alongside their clinical judgment, to prioritize transitional-care outreach: which patients get a same-week home visit, which get a phone call from the pharmacy team, which get the standard discharge instructions.

        The model is working reasonably well at Walden. The ACO's executive committee has asked Walden to **share the predictions** for the ACO's attributed Medicare beneficiaries with the rest of the ACO, so that the affiliated practices can do their own transitional-care outreach when one of their patients is discharged from a Walden bed.

        It sounds simple. It is not simple. **You are the clinical informatics representative on the small working group the ACO has stood up to figure out how to do this.** Your job is to walk the working group through the problem the way Course 0 has taught you to see it: every layer at once.

        The capstone has four committed answers. Each one is short on purpose. Write a paragraph or two, commit, and the reveal opens. Making your reasoning explicit before you see how someone else would reason through it is the exercise.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Step 1 of 4: What data, information, knowledge, wisdom are in play here?

        Apply Track 02. The thing being shared is *a readmission probability score*. Walk it through the DIKW layers. What is the data layer? What context turns it into information? What knowledge does the receiving practice need to act on it? What does wisdom look like for the affiliated PCP receiving the score on Monday morning?

        Write at least a short paragraph. The reveal opens at 120 characters.
        """
    )
    return


@app.cell
def _(commit_text):
    step1_widget, step1_ready = commit_text(
        "DIKW analysis of the shared readmission score.",
        min_chars=120,
    )
    step1_widget
    return step1_ready, step1_widget


@app.cell
def _(mo, reveal, step1_ready, step1_widget):
    mo.stop(
        not step1_ready(),
        mo.callout(
            mo.md("_Write at least a short paragraph above. The reveal opens once you do._"),
            kind="neutral",
        ),
    )

    ideal_1 = (
        "**Data.** The raw signal is a probability between 0 and 1 (say, *0.34*) attached to a "
        "patient identifier, a discharge timestamp, the model's version, and the input features "
        "that produced the score. Without that metadata the number is not even data, it is a "
        "digit. The data layer also has to carry which model was used and when, because the "
        "model will be retrained and the same patient can have different scores on different "
        "days under different model versions.\n\n"
        "**Information.** The probability becomes information when it carries the context that "
        "makes it actionable: the model's operating threshold (above 0.30 is *high-risk* in "
        "Walden's local calibration), the patient's baseline risk distribution relative to "
        "Walden's general medicine population, the components that drove this particular score "
        "(prior admissions, lab abnormalities, length of stay, social-history flags), and a "
        "calibration statement (*this score is well-calibrated in patients similar to Walden's "
        "medicine population*).\n\n"
        "**Knowledge.** The receiving practice needs the knowledge of what to do with a "
        "high-risk score. That knowledge lives in the practice's own care-transitions "
        "protocol: who calls the patient, on what day, with what script, with what escalation "
        "criteria. The score does not contain the knowledge of what to do; the practice has to "
        "have that already or the score is noise.\n\n"
        "**Wisdom.** The PCP who opens the score on Monday morning is the wisdom layer. Wisdom "
        "asks: does this score match what I know about this patient and her family; was the "
        "admission for a problem I have specifically been working on with her; is there a "
        "social or behavioral factor the model could not see that I know about; is now the right "
        "moment to escalate, to reach out personally, or to trust that the standard protocol is "
        "enough. The score that arrives without anyone exercising the wisdom layer downstream is "
        "the score that gets ignored. That is the failure mode the working group has to design "
        "against."
    )
    reveal(step1_widget.value, ideal_1, learner_label="Your DIKW analysis")
    return (ideal_1,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Step 2 of 4: What computer-science and network plumbing does the data have to travel through?

        Apply Tracks 03 and 04. The score is computed nightly at Walden against inpatients. The receiving system is an affiliated practice's EHR, which is a different EHR than Walden's. What shape does the data need to be in? What systems does it live in along the way? What network boundaries does it have to cross? Where are the realistic failure points in the plumbing?

        Write at least a short paragraph. The reveal opens at 120 characters.
        """
    )
    return


@app.cell
def _(commit_text, mo):
    step2_widget, step2_ready = commit_text(
        "Computer-science and network plumbing analysis.",
        min_chars=120,
    )
    step2_widget
    return step2_ready, step2_widget


@app.cell
def _(mo, reveal, step2_ready, step2_widget):
    mo.stop(
        not step2_ready(),
        mo.callout(
            mo.md("_Write at least a short paragraph above. The reveal opens once you do._"),
            kind="neutral",
        ),
    )

    ideal_2 = (
        "**Data at rest.** The score is most naturally a small structured object: patient "
        "identifier, score, model version, generated-at timestamp, threshold context, and a "
        "few feature-contribution flags. That shape fits JSON cleanly (a FHIR `RiskAssessment` "
        "resource is the standards-shaped version) and could also travel as CSV if the receivers "
        "expect a nightly flat-file feed. The score lives in three places: Walden's CDW where it "
        "is computed, an outbound staging area at Walden, and the receiving system inside each "
        "ACO partner.\n\n"
        "**Data in motion.** The score has to cross at least three network boundaries. Inside "
        "Walden, the LAN moves the score from the CDW to the outbound staging area. The "
        "Walden firewall has to permit outbound traffic from staging to the ACO's data hub (or "
        "directly to each partner). The partner's firewall has to permit inbound traffic from "
        "Walden (or the ACO hub) into its EHR or its own data warehouse. Each partner runs a "
        "different EHR, so the receiving format may not be uniform across partners; one partner "
        "may want a FHIR RiskAssessment, another a CSV feed, another a direct write into an EHR "
        "flowsheet through a vendor-specific integration. The hub-and-spoke architecture (ACO "
        "data hub in the middle) usually wins over point-to-point integrations because it "
        "centralizes the format translation and the security review.\n\n"
        "**Realistic failure points.** The nightly job at Walden fails silently and nobody at "
        "the practice notices for a week. The patient identifier the receiving practice uses "
        "(its MRN) differs from the identifier Walden uses, so the score arrives but cannot be "
        "matched to the patient's chart. The model's threshold context is dropped on the wire "
        "and the receiving practice treats 0.34 as an absolute number rather than a "
        "percentile in Walden's distribution. The receiving EHR's UI surfaces the score in a "
        "place nobody on the care team actually looks. The integration breaks every time either "
        "Walden or the partner upgrades their EHR, and nobody owns the operational handoff."
    )
    reveal(step2_widget.value, ideal_2, learner_label="Your plumbing analysis")
    return (ideal_2,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Step 3 of 4: Which stakeholders across the actor groups need to agree?

        Apply Track 05. List the actors whose agreement is required for this to work end-to-end. The goal is not to enumerate every possible actor; it is to identify whose agreement is *load-bearing* and where the timing of the project will live.

        Write at least a short paragraph. The reveal opens at 120 characters.
        """
    )
    return


@app.cell
def _(commit_text, mo):
    step3_widget, step3_ready = commit_text(
        "Stakeholders who have to agree.",
        min_chars=120,
    )
    step3_widget
    return step3_ready, step3_widget


@app.cell
def _(mo, reveal, step3_ready, step3_widget):
    mo.stop(
        not step3_ready(),
        mo.callout(
            mo.md("_Write at least a short paragraph above. The reveal opens once you do._"),
            kind="neutral",
        ),
    )

    ideal_3 = (
        "**Providers.** Walden's clinical leadership (CMIO, CMO, the medicine service chief), "
        "the discharge planning team that already uses the score, and the affiliated practices "
        "in the ACO whose PCPs will receive the score. Each receiving practice's medical "
        "director has to agree both to receive the data and to redesign their own "
        "care-transitions workflow around it.\n\n"
        "**Payers.** CMS, through the Medicare Shared Savings Program rules that govern the "
        "ACO and define what counts as ACO-attributed beneficiary data. The shared-savings "
        "contract itself implicitly authorizes the data-sharing for care-coordination purposes; "
        "explicit affirmation from the ACO's payer-relations team is usually still required.\n\n"
        "**EHR vendors.** Walden's EHR vendor (for the outbound feed mechanism), and each "
        "partner's EHR vendor (for the inbound ingestion). If the partners run two or three "
        "different EHRs, the working group is also negotiating with two or three different "
        "vendors. This is where calendar weeks tend to live.\n\n"
        "**Regulators.** ONC indirectly, through the certification rules that determine what "
        "FHIR or other API surfaces each EHR is required to expose. OCR through HIPAA: the data "
        "sharing has to be authorized under treatment-payment-operations or under a more "
        "specific BAA arrangement, depending on the structure. Most ACOs sit comfortably inside "
        "treatment-and-operations; some specific uses (research-flavored uses, marketing-flavored "
        "uses) would require additional authorization.\n\n"
        "**Standards bodies.** Not as a stakeholder you negotiate with directly, but as the "
        "source of the shape the data should travel in: FHIR's RiskAssessment resource (HL7) "
        "for the format, LOINC and SNOMED for any clinical context that travels alongside the "
        "score, the local MRN-to-MRN matching strategy (or a Patient matching standard like "
        "the CommonWell or Carequality work) for identity resolution.\n\n"
        "**Public health and research infrastructure** are not load-bearing for this scenario. "
        "If the readmission program later wanted to publish its outcomes or contribute to a "
        "research network, both groups would re-enter the picture.\n\n"
        "**Where timing will live.** The slowest agreement is almost always the legal and "
        "vendor work, not the technical work. The technical feed is two to four weeks once "
        "everyone is aligned. The BAA negotiations, the vendor integration scoping, and the "
        "per-partner ingestion design are the parts that take the calendar quarters."
    )
    reveal(step3_widget.value, ideal_3, learner_label="Your stakeholder analysis")
    return (ideal_3,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Step 4 of 4: What governance must be in place?

        Forward-reference to Course 03, which does this work in depth. For Course 0 the question is orientation: what governance structures need to be standing up before the score starts flowing? Think about who is responsible for ongoing oversight, who reviews the model's performance over time, who handles the situation when the model is wrong about a specific patient and there is a bad outcome, and what equity considerations need to be on the table.

        Write at least a short paragraph. The reveal opens at 120 characters.
        """
    )
    return


@app.cell
def _(commit_text, mo):
    step4_widget, step4_ready = commit_text(
        "Governance requirements.",
        min_chars=120,
    )
    step4_widget
    return step4_ready, step4_widget


@app.cell
def _(mo, reveal, step4_ready, step4_widget):
    mo.stop(
        not step4_ready(),
        mo.callout(
            mo.md("_Write at least a short paragraph above. The reveal opens once you do._"),
            kind="neutral",
        ),
    )

    ideal_4 = (
        "**Ongoing model oversight.** The model is not a one-time deliverable; it is a "
        "clinical-facing system that will drift as Walden's patient population, coding patterns, "
        "and care-delivery models change. A governance body (Walden's clinical AI committee or "
        "its equivalent) has to own ongoing monitoring: discrimination, calibration, override "
        "rates, and the actual downstream outcome (did readmissions go down). The ACO needs a "
        "parallel oversight role for the cross-system use.\n\n"
        "**Performance review cadence.** A specified review cadence (often quarterly) with "
        "pre-specified thresholds for when the model has to be retrained, recalibrated, or "
        "paused. The first six months after deployment need closer monitoring than the steady "
        "state.\n\n"
        "**Subgroup performance.** The model has to be evaluated separately in the populations "
        "whose readmissions matter most: by age, by race and ethnicity, by primary payer, by "
        "the social-history variables that often carry the equity signal. A model that "
        "discriminates well overall but poorly in one subpopulation can quietly redirect "
        "care-transitions resources away from the patients who need them most. Track 05 of "
        "Course 03 (algorithmic fairness) is the deep treatment.\n\n"
        "**Error and adverse-event response.** When the model is wrong about a specific patient "
        "and there is a bad outcome (a missed readmission, an overuse of resources on a "
        "low-risk patient), there has to be a defined pathway for review. Not a blame pathway, "
        "a learning pathway. Who owns it. Where the patient's PCP fits in. How findings feed "
        "back into the next retraining cycle.\n\n"
        "**Data use and retention.** The score has a lifecycle (Track 02). Beyond the operational "
        "window, what happens to the scores? Are they retained for outcomes evaluation? For how "
        "long? Under what authorization? The retention question is downstream of the same kinds "
        "of decisions Course 03 takes seriously.\n\n"
        "**Patient transparency.** What, if anything, gets told to the patient about the score? "
        "Different health systems have arrived at different answers; the working group should "
        "decide deliberately rather than defaulting to invisibility. This is the autonomy "
        "commitment from Track 06 in concrete form."
    )
    reveal(step4_widget.value, ideal_4, learner_label="Your governance plan")
    return (ideal_4,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## Reflection.

        One last prompt, with no reveal. The writing is the work.
        """
    )
    return


@app.cell
def _(reflection):
    reflection_widget, reflection_layout = reflection(
        "Look back at your four answers above. Which of the four felt easiest to write, and "
        "which felt hardest? Was the hardest one hard because the vocabulary was new, because "
        "the problem was genuinely ambiguous, or because the answer depends on facts about your "
        "own setting that the scenario did not supply? The honest answer is useful as you move "
        "into the rest of the curriculum.",
    )
    reflection_layout
    return reflection_layout, reflection_widget


@app.cell
def _(go_deeper):
    go_deeper(
        "Two short reads if this scenario lit something up.\n\n"
        "- **For the technical side**, the **HL7 FHIR `RiskAssessment` resource specification** "
        "(hl7.org/fhir/R4/riskassessment.html) is the standards-shaped version of the thing this "
        "scenario was shipping around. Reading the resource definition gives you the FHIR-native "
        "language for *what fields would carry a readmission probability across the wire*. "
        "Course 06 of the curriculum is where this kind of reading becomes routine.\n\n"
        "- **For the governance side**, the **AMIA position paper on AI for health (2023)** "
        "(jamia.oxfordjournals.org has the open-access version) names the governance commitments "
        "the field has converged on for this kind of system. It is short, readable, and a "
        "useful map of where the ongoing arguments are. Course 03 returns to this material "
        "seriously; Course 09 picks it up again for AI specifically."
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ## You finished Course 0.

        This was orientation. The work was naming what you already knew implicitly: that clinical informatics is its own field with its own history; that data is not data alone but lives in layers and stages; that the systems clinical work runs on have a shape you can describe; that the people who built and maintain those systems have titles and roles you can name; and that the org chart of U.S. healthcare is knowable.

        The rest of the curriculum builds on this. The same Ms. Reyes you met in Track 01 will appear in every course. The same DIKW vocabulary will be used to talk about predictions, about CDS alerts, about NLP extractions. The same lifecycle will be walked through for FHIR resources, for OMOP records, for claims. The same actor groups will be the ones whose agreement everything else depends on.

        **What's next.** Most learning paths in `start-here/learning-paths.md` route from here into `01-computational-thinking`. Open it from the file tree on the left, or run `marimo run 01-computational-thinking/home.py` to launch its menu.
        """
    )
    return


if __name__ == "__main__":
    app.run()
