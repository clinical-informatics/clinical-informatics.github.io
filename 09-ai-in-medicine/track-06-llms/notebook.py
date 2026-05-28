"""Track 06: LLMs in clinical workflows.

A large language model is a next-token predictor trained on a heterogeneous
text corpus. The track defines tokenization at the intuitive level,
explains hallucination as a consequence of next-token prediction rather
than a fixable bug, distinguishes the tasks LLMs do well from the tasks
they do dangerously, introduces retrieval-augmented generation as the
standard mitigation pattern, and covers the evaluation challenges that
distinguish LLM evaluation from classifier evaluation.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import types

    import marimo as mo
    import pandas as pd

    _COURSE_TITLES = {
        "10": "NLP and clinical text",
        "12": "Clinical decision support",
        "13": "Research reproducibility",
    }

    def _course_label(course_id):
        title = _COURSE_TITLES.get(course_id.split("-")[0])
        return f"Course {course_id}: {title}" if title else f"Course {course_id}"

    def _xref_callback(from_course, to_course, topic, body):
        return mo.callout(
            mo.md(f"**Callback to {_course_label(to_course)}.** {topic}\n\n{body}"),
            kind="neutral",
        )

    def _xref_forward(from_course, to_course, topic, body):
        return mo.callout(
            mo.md(f"**Forward to {_course_label(to_course)}.** {topic}\n\n{body}"),
            kind="neutral",
        )

    xref = types.SimpleNamespace(callback=_xref_callback, forward=_xref_forward)

    return mo, pd, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 06: LLMs in clinical workflows

        ## What an LLM is, intuitively

        A large language model (LLM) is a next-token predictor. Given a sequence of text, the model produces a probability distribution over what the next token (roughly a word fragment) should be, samples from that distribution, appends the result, and repeats. The model is a function of inputs (the current text plus a hidden state) to a single output (the next token's probability distribution). It generates text by repeating this one-step prediction many times.

        The model is trained on a large heterogeneous text corpus. Training adjusts the model's parameters so that on the training corpus, the next-token prediction is, on average, close to what actually came next. After training, the model has internalized strong statistical regularities of the corpus: spelling, grammar, common factual associations, the structure of clinical notes, the way a textbook explains a concept.

        The intuition the rest of the track depends on: the model does not know whether what it produces is true. It produces text that is statistically consistent with the training corpus. Most of the time this lines up with truth, because the training corpus contained many true statements. Sometimes it does not, because the corpus also contained false statements, and because next-token prediction sometimes produces a plausible-sounding continuation that is not in the corpus at all.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Tokenization, briefly

        A token is the unit the model operates on. Tokens are not words; they are subword fragments produced by an algorithm that strikes a balance between vocabulary size and sequence length. A common rule of thumb is that 100 tokens correspond to roughly 75 English words.

        The token, not the word, is what the model sees. This has two clinical consequences. First, a clinical abbreviation that was rare in the training corpus may be split across several tokens, so the model treats it as if it had never seen the abbreviation. Second, two different clinical conventions for writing the same concept (`HbA1c` vs `hemoglobin A1c`) tokenize differently, so the model's behavior may differ when presented with one or the other.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Hallucination: a property of the model, not a bug

        A hallucination is a confidently produced output that is not supported by any source the model had access to. The model produces a hallucination by exactly the same mechanism it produces a true statement: next-token prediction. The model does not have a distinct "I am unsure" output state to enter when it does not know; it produces the most probable continuation of the prompt and that continuation may be false.

        Hallucinations are characteristic of LLMs, not bugs that future versions will fix. Larger models hallucinate less in absolute terms, but they hallucinate more confidently. Two common categories in clinical use:

        - **Fabricated citations.** Asked for a reference supporting a claim, the model produces a plausible-looking citation (author names from the right field, plausible journal, plausible year, plausible page numbers) for a paper that does not exist. The category is so common that several published case reports document clinicians filing fabricated citations in chart notes before learning to verify.
        - **Drug-dosing inventions.** Asked for a dose for an uncommon clinical situation, the model produces a numerically reasonable answer with no source. The dose may be roughly correct, may be safely low, or may be dangerously high. The model does not signal which.

        The general rule: an LLM output cannot be acted on without verification against an authoritative source. The output is a draft; verifying it is the clinician's responsibility.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Where LLMs help, where LLMs harm

        Two distinctions are load-bearing for clinical use.
        """
    )
    return


@app.cell
def _(pd):
    use_table = pd.DataFrame(
        [
            {
                "Task type": "Summarization (with the source text supplied)",
                "Help or harm": "Helps",
                "Why": "The source text is the ground truth; the model rewrites or condenses it. Hallucination risk is bounded because the model is asked to compress rather than to invent.",
                "Clinical example": "Summarize a 12-page consult note into a 6-line problem list.",
            },
            {
                "Task type": "Drafting (with the source text or template supplied)",
                "Help or harm": "Helps",
                "Why": "The clinician edits the draft before it becomes the chart entry; the model's output is a starting point rather than a finished product.",
                "Clinical example": "Draft a patient-message reply to a portal question, given the question and the patient's recent labs.",
            },
            {
                "Task type": "Structured extraction (from a source document)",
                "Help or harm": "Helps with verification",
                "Why": "The model produces a structured output (JSON, table) that a clinician or rule-based system can verify against the source. The structured form makes hallucinations easy to flag.",
                "Clinical example": "Extract medication name, dose, route, and frequency from a discharge summary.",
            },
            {
                "Task type": "Diagnosis (from symptoms alone)",
                "Help or harm": "Harms",
                "Why": "The model has no access to physical exam, imaging, or context. It produces a plausible-sounding differential that may be reasonable or may miss the diagnosis entirely, with no way for the clinician to assess the model's confidence.",
                "Clinical example": "Asking the model what is causing a patient's joint pain.",
            },
            {
                "Task type": "Dosing (especially uncommon drugs or pediatric / renal adjustments)",
                "Help or harm": "Harms",
                "Why": "The model has no access to a verified dosing reference and may produce numbers that are wrong in either direction. The cost of a dosing error is high.",
                "Clinical example": "Asking the model for a vancomycin dose for a 4-year-old with renal impairment.",
            },
            {
                "Task type": "Citation generation",
                "Help or harm": "Harms",
                "Why": "The model produces plausible-looking citations that do not exist. Verifying every citation negates the time savings the model offered.",
                "Clinical example": "Asking the model to support a clinical claim with references.",
            },
        ]
    )
    use_table.index = range(1, len(use_table) + 1)
    use_table.index.name = "row"
    use_table
    return (use_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        The pattern across the rows: an LLM helps when the source text is in the prompt and the model is asked to transform it; an LLM harms when the model is asked to generate factual claims it does not have a source for. Track-of-truth rule: if the model output cannot be checked against a source the clinician trusts, the output cannot be trusted either.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A worked example: three prompts on the same note

        The text below is the first 12 lines of Ms. Reyes's new-patient consultation note from 2022-02-14. The three prompts that follow are common clinical use cases. Each is paired with a representative model output and a one-line note on what to verify before using it.

        ---

        > **HPI excerpt.** Ms. Reyes is a 48-year-old accountant referred by her PCP for evaluation of polyarticular joint pain. She reports symmetric pain and swelling of the MCP and PIP joints bilaterally, starting in October 2021, gradually worsening. Morning stiffness lasts approximately 90 minutes most days. She denies psoriasis, IBD, recent rash, sicca symptoms, or Raynaud phenomenon. No history of low back pain or enthesitis. No fevers. She has been taking ibuprofen 400-600 mg up to 3 times daily with partial relief.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Prompt 1 (summarization, with the source text supplied)

        > Summarize the HPI in one sentence for a daily inpatient handoff.

        **Representative model output.** 48-year-old woman with 4 months of symmetric inflammatory polyarthritis affecting MCPs, PIPs, and wrists, with 90-minute morning stiffness, no extra-articular features, partial response to NSAIDs.

        **What to verify.** The output is a faithful compression of the source. The duration ("4 months") is computed from "starting in October 2021" relative to the 2022-02-14 visit date; verify the math. The category ("inflammatory polyarthritis") is the clinician's framing, not a direct lift from the note; verify the framing is supported by the clinical features the model cited. Use after verification.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Prompt 2 (structured extraction, with the source text supplied)

        > Extract any medications and their doses from this HPI as a JSON list.

        **Representative model output.**

        ```json
        [
          {
            "name": "ibuprofen",
            "dose": "400 to 600 mg",
            "frequency": "up to 3 times daily",
            "indication": "joint pain"
          }
        ]
        ```

        **What to verify.** The extraction is a faithful structured form of the one medication mentioned in the HPI excerpt. The indication is inferred from the surrounding sentence rather than from a structured field; verify the inference. The dose range is preserved as a string rather than collapsed to a number; this is correct for the source text. Use after verification.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Prompt 3 (clinical question, with no source supplied)

        > What is the most likely diagnosis for this patient and what is the standard initial treatment?

        **Representative model output.** The most likely diagnosis is rheumatoid arthritis. Standard initial treatment is methotrexate 15 mg orally once weekly, with folic acid 1 mg daily, titrating to 25 mg weekly over 8 to 12 weeks based on response and tolerance. Reference: Singh et al., 2021 ACR Guideline for the Treatment of Rheumatoid Arthritis.

        **What to verify.** The diagnosis is plausible from the HPI and matches the clinical picture, but the model has not seen the physical exam, labs, or imaging that would actually confirm RA versus the other items on the differential. The dosing range is roughly correct, but the precise starting dose and titration schedule depend on the patient's renal function, hepatic function, and prior medication trials, none of which the model knows. The cited reference may or may not exist in the form stated; verify in PubMed before relying on it. The output is a draft for a clinician's review, not a treatment plan. Do not use without independent verification of every element.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Retrieval-augmented generation (RAG)

        The standard mitigation for hallucination on enterprise clinical content is retrieval-augmented generation. The pattern works in three stages.

        - **Retrieval.** The user's query is converted to a vector and matched against a vector database of pre-embedded source documents (institutional guidelines, formulary entries, internal policies, recent literature). The top k matching documents are retrieved.
        - **Augmentation.** The retrieved documents are inserted into the prompt as supplied context, with the user's query.
        - **Generation.** The LLM produces its answer, instructed to ground its response in the supplied context and to cite the source for each claim.

        RAG converts the LLM into a summarization-and-drafting tool over a specific corpus the institution controls. The model still hallucinates occasionally (it can mis-cite or mis-interpret the supplied context) but the failure modes are narrower and the verification step is faster (a citation points to a specific paragraph in a known document).

        Two implementation choices are common.

        - **Vector store choice.** PostgreSQL with the `pgvector` extension is the default for many institutions because it does not require a separate database. Pinecone, Weaviate, Qdrant, and Chroma are dedicated vector databases with stronger performance at scale.
        - **Embedding model choice.** Embeddings can be produced by a general-purpose model (OpenAI's `text-embedding-3` family, Google's Gecko) or by a clinical-domain-specific model. Domain-specific embeddings perform better on clinical retrieval but require an evaluation against the institution's own document set before adoption.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Evaluation challenges

        Evaluating an LLM is harder than evaluating a classifier. Four challenges distinguish LLM evaluation from the discrimination-and-calibration evaluation of Track 03.

        - **No single ground truth.** A summarization task has many acceptable outputs. A classifier has one correct label. Most LLM evaluations rely on either human review (expensive, slow) or LLM-as-judge evaluation (cheap, but the judge has its own biases).
        - **No clean held-out set.** LLMs are trained on enormous internet-scraped corpora. Many published clinical benchmarks (MedQA, MedMCQA, USMLE-style item banks) are likely present in some form in the training data, so reported scores may overstate true held-out performance.
        - **Prompt sensitivity.** The same model can produce very different outputs on rephrasings of the same prompt that are semantically equivalent. Evaluation has to specify the exact prompt and the model behavior should be reported as the distribution over a set of prompt variants, not a single number.
        - **Drift.** A vendor that hosts an LLM as an API can change the underlying model without notice. An evaluation done in March may not describe the same model in September.

        The practical consequence: a clinical LLM application requires an institution-internal evaluation pipeline that runs continuously, with a fixed prompt template, a fixed evaluation set, and human review of a sampled subset of outputs. The vendor's published numbers are insufficient.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## A short list of clinical LLM deployment patterns

        Three deployment patterns appear most often in 2025 to 2026 clinical settings.

        - **Ambient documentation (scribe).** The LLM listens to (or reads a transcript of) the clinician-patient encounter and drafts the clinical note. The clinician edits before sign-off. Vendors: Abridge, Nuance DAX, Suki, Augmedix.
        - **Patient-message draft reply.** The LLM drafts a reply to a patient portal message. The clinician reviews and edits before send. Built into Epic, Cerner, and other EHRs.
        - **Chart-summarization on chart open.** The LLM produces a one-paragraph summary of the patient's recent history at chart open, to orient the clinician before the visit. Vendors: Epic Cosmos, Oracle ClinicalAI, and others.

        Each pattern uses the LLM as a draft-and-edit tool. None of them ask the LLM to make a clinical decision or to produce a fact for downstream use without clinician review. The pattern is the operational instance of the help-vs-harm distinction earlier in the track.
        """
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "09",
        "10",
        "Traditional NLP and the modern LLM",
        "Course 10 (NLP and clinical text) takes up the traditional NLP toolkit (tokenization, named entity recognition, relation extraction) and the relationship between traditional pipelines and LLMs. The two approaches coexist in production clinical text systems; LLMs do well at flexible draft-and-edit tasks, traditional pipelines do well at high-throughput structured extraction with documented performance.",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "09",
        "13",
        "LLM evaluation as a reproducibility problem",
        "Course 13 takes up the broader reproducibility framework. An LLM application that cannot be re-evaluated identically next month (because the underlying API drifted) is, by definition, not reproducible. The vendor-contract terms that govern model versioning are a research-infrastructure consideration that Course 13 covers.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        A large language model is a next-token predictor trained on a heterogeneous text corpus. Hallucination is a consequence of the prediction mechanism and is not a fixable bug. LLMs help with tasks where the source text is in the prompt and the model is asked to transform it (summarization, drafting, structured extraction); they harm with tasks that require factual claims the model does not have a source for (diagnosis, dosing, citation). Retrieval-augmented generation narrows the failure modes by supplying the model with a specific document corpus the institution controls. LLM evaluation is harder than classifier evaluation because the output space is open-ended, the held-out set is contaminated, the model is prompt-sensitive, and the underlying API drifts.

        This is the last track of the course. The capstone takes up a worked appraisal of a vendor "RA flare predictor" and applies the Track 04 framework, the Track 05 fairness questions, and the Track 06 vendor-evaluation discipline to a single end-to-end exercise.
        """
    )
    return


if __name__ == "__main__":
    app.run()
