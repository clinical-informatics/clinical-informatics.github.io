"""Track 04: LLMs and clinical text.

Clinical NLP today has two strands: classical pipelines (Track 02) and
large language models (Course 09 Track 6). The track maps when each
strand wins, addresses clinical-domain fine-tuning, demonstrates schema-
driven extraction by writing the schema into the prompt, and surveys the
clinical-NLP benchmark landscape.
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
        "07": "Data wrangling and engineering",
        "09": "AI in medicine",
        "12": "Clinical decision support",
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
        # Track 04: LLMs and clinical text

        ## Two strands of clinical NLP

        Clinical NLP in 2025 to 2026 has two complementary strands. The classical pipeline addressed in Track 02 (tokenization, NER, relation extraction, negation handling) is still the standard for high-throughput structured extraction with documented performance and reproducible behavior. The large-language-model strand introduced in Course 09 Track 6 is the standard for flexible drafting, open-ended summarization, and schema-driven extraction tasks where the schema can change without retraining.

        The two strands solve different problems and live alongside one another in production systems. The track maps when each strand wins, addresses clinical-domain fine-tuning (the bridge between general-domain LLMs and clinical text), demonstrates schema-driven extraction with the schema in the prompt, and surveys the clinical-NLP benchmark landscape.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## When to use which

        The decision table below summarizes the operational comparison. Both columns are useful; neither replaces the other.
        """
    )
    return


@app.cell
def _(pd):
    decision_table = pd.DataFrame(
        [
            {
                "Dimension": "Task with a fixed schema (extract medications + doses + frequencies)",
                "Classical pipeline": "Strong. Tuned dictionaries, regex, and templates produce predictable, auditable output at high throughput.",
                "LLM": "Workable. Prompt-with-schema extraction works but is slower and more expensive per document.",
            },
            {
                "Dimension": "Task with a flexible schema (extract whatever clinical facts seem relevant for this question)",
                "Classical pipeline": "Weak. Each new schema requires new rules or retraining.",
                "LLM": "Strong. The schema is in the prompt; changing the schema changes the prompt and nothing else.",
            },
            {
                "Dimension": "Open-ended summarization",
                "Classical pipeline": "Weak. Classical summarization (extractive sentence selection) produces stilted output.",
                "LLM": "Strong. Fluent paraphrastic summarization is the canonical LLM strength.",
            },
            {
                "Dimension": "Drafting (clinical correspondence, patient-message reply, note skeleton)",
                "Classical pipeline": "Not applicable.",
                "LLM": "Strong. Drafting with clinician edit is the deployed pattern.",
            },
            {
                "Dimension": "Negation and uncertainty handling",
                "Classical pipeline": "Strong. NegEx and ConText handle the common patterns reliably.",
                "LLM": "Mixed. LLMs handle common patterns but produce inconsistent output on unusual ones; prompt design matters.",
            },
            {
                "Dimension": "Throughput (millions of documents per day)",
                "Classical pipeline": "Strong. Modest hardware processes hundreds of documents per second.",
                "LLM": "Weak. API rate limits, inference latency, and per-token cost cap the throughput.",
            },
            {
                "Dimension": "Auditable per-decision behavior (a regulator asks why this extraction was made)",
                "Classical pipeline": "Strong. The matching rule is documented; the decision can be reproduced by inspection.",
                "LLM": "Weak. The model's reasoning is not directly inspectable; documenting the prompt and the temperature is the closest analog.",
            },
            {
                "Dimension": "Behavior on novel input (a note written in a way the system has not seen)",
                "Classical pipeline": "Weak. Coverage gaps are silent; the system extracts nothing rather than extracting wrong things.",
                "LLM": "Mixed. The model produces an output for any input, but the output may be a hallucination on inputs unlike the training distribution.",
            },
        ]
    )
    decision_table.index = range(1, len(decision_table) + 1)
    decision_table.index.name = "row"
    decision_table
    return (decision_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three operational rules follow from the table.

        First, deployed systems that need predictable behavior at scale use a classical pipeline. The cTAKES + NegEx + UMLS-CUI architecture is still what production research-data warehouses and CDS systems run on. The behavior is documented, the throughput is high, and the regulator-facing answer to "why did the system extract X" is the rule itself.

        Second, deployed systems that need flexibility use an LLM. The clinical-summarization and patient-message-draft and chart-summarization-on-open patterns from Course 09 Track 6 are all LLM-based. The shared property is that the output is reviewed by a clinician before it becomes an action.

        Third, the strongest production architectures combine both. A classical pipeline performs the structured extraction; an LLM performs the open-ended summarization that the classical pipeline can not produce. The two outputs feed different downstream consumers.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Clinical-domain fine-tuning

        General-domain language models (BERT, RoBERTa, GPT-3.5 and later) were trained on web text. Clinical text differs from web text in vocabulary (clinical abbreviations, drug names, anatomical terms), in structure (the SOAP-note shape, the lab-and-imaging conventions), and in pragmatics (the negation patterns, the assertion styles, the hedge vocabulary). A general-domain model applied to clinical text performs noticeably worse than the same architecture fine-tuned on clinical text.

        The published clinical-domain fine-tuned models cluster into three groups.

        - **Biomedical-corpus-trained encoders.** BioBERT (Lee et al. 2020), trained on PubMed abstracts and PMC full-text; SciBERT (Beltagy et al. 2019), trained on a broader scientific corpus. These do well on biomedical-literature tasks (NER on disease names, relation extraction in published abstracts).
        - **Clinical-note-trained encoders.** ClinicalBERT (Alsentzer et al. 2019), trained on MIMIC discharge summaries; BlueBERT (Peng et al. 2019), trained on PubMed plus MIMIC. These do best on clinical-note tasks (entity extraction from EHR notes, prediction tasks built on note features).
        - **Clinically-fine-tuned generative models.** Med-PaLM and Med-PaLM 2 (Google), MEDITRON-70B (EPFL/Yale), BioGPT (Microsoft). These are decoder models with clinical instruction tuning; they target the question-answering, summarization, and free-text generation tasks that LLMs are used for clinically.

        The pattern across the three groups: the more the training corpus resembles the deployment corpus, the better the fine-tuned model performs. Clinical-note tasks are best handled by clinical-note-trained models; biomedical-literature tasks by biomedical-literature-trained models. Domain mismatch on either axis costs measurable performance.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Schema-driven extraction with the schema in the prompt

        The most common LLM-based clinical NLP pattern in production today is schema-driven extraction. The prompt describes the structured output the model should produce. The model returns JSON conforming to the schema. A downstream consumer validates the JSON and treats the conforming output as a structured extraction.

        The pattern looks like this.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Example prompt template

        ```
        You will be given a clinical note. Extract every medication change
        described in the note and return a JSON object with this schema:

        {
          "medication_changes": [
            {
              "medication_name": string,
              "change_type": "start" | "stop" | "increase" | "decrease",
              "new_dose": string | null,
              "frequency": string | null,
              "reason": string | null
            }
          ]
        }

        Return only the JSON. If no medication changes are described,
        return {"medication_changes": []}.

        Clinical note:
        ---
        {NOTE_TEXT}
        ---
        ```

        ### Representative output on Ms. Reyes's 2022-03-07 follow-up note

        ```json
        {
          "medication_changes": [
            {
              "medication_name": "methotrexate",
              "change_type": "start",
              "new_dose": "10 mg",
              "frequency": "weekly",
              "reason": "Seropositive erosive rheumatoid arthritis meeting 2010 ACR/EULAR criteria"
            },
            {
              "medication_name": "folic acid",
              "change_type": "start",
              "new_dose": "1 mg",
              "frequency": "daily",
              "reason": "Standard concurrent therapy with methotrexate"
            }
          ]
        }
        ```
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Three operational notes on the pattern.

        First, the schema is the contract. A downstream consumer can pin the schema in a JSON Schema document and validate every output against it; non-conforming outputs are rejected or sent back to the model with a correction prompt. The schema makes the integration tractable.

        Second, the reason field carries information no classical pipeline can produce. The model has reconstructed why the medication was started by reading the surrounding assessment paragraph. The reconstruction is approximate and has to be verified, but it is the kind of cross-sentence reasoning that the classical pipeline cannot do at all.

        Third, the model's behavior on the same note can vary across calls (the model is stochastic at non-zero temperature). For schema-driven extraction the temperature is typically set to zero or very low; for drafting tasks a higher temperature is sometimes preferred. Documenting the temperature is part of documenting the system.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## When schema-driven LLM extraction is and is not appropriate

        Three guardrails apply to schema-driven LLM extraction in clinical settings.

        - **Clinician review for any output that drives an action.** A medication-change extraction that feeds a CDS alert needs clinician sign-off on each output, just like a draft note needs clinician edit before chart-entry. The LLM's role is to draft the structured output; the clinician's role is to verify and act on it.
        - **Audit logging of the prompt, the input, and the output.** A regulator asking why a particular extraction was made should see the exact prompt template, the exact input note, the model version, the temperature, and the raw output. The audit log is the post-hoc reproducibility mechanism.
        - **Validation against a held-out gold-standard set.** The model's performance on the schema is reported on a labeled corpus before deployment and re-evaluated periodically. Track 05 takes up the evaluation mechanics; the operational rule is that a clinical LLM extraction in production has continuous evaluation, not one-time evaluation at adoption.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The clinical-NLP benchmark landscape

        Four benchmark families dominate the clinical NLP evaluation literature.
        """
    )
    return


@app.cell
def _(pd):
    benchmark_table = pd.DataFrame(
        [
            {
                "Benchmark family": "n2c2 / i2b2 shared tasks",
                "What it covers": "Clinical NLP tasks released as community challenges (NER on de-identified clinical notes, medication extraction, temporal relations, adverse-drug-event extraction, family-history extraction).",
                "Why it matters": "The historical reference benchmarks for clinical NER and relation extraction. Most published clinical NLP systems report n2c2 scores.",
                "Hosted at": "n2c2.dbmi.hms.harvard.edu (Harvard DBMI).",
            },
            {
                "Benchmark family": "MedQA / MedMCQA / PubMedQA",
                "What it covers": "Medical question-answering benchmarks built from USMLE-style items (MedQA), Indian medical entrance exams (MedMCQA), and PubMed-derived yes/no/maybe questions (PubMedQA).",
                "Why it matters": "The standard reference for LLM clinical-knowledge evaluation. Med-PaLM and competitor papers all report scores against these.",
                "Hosted at": "Hugging Face datasets; the original benchmark publications link to the raw files.",
            },
            {
                "Benchmark family": "MedNLI",
                "What it covers": "Natural-language inference on clinical sentence pairs. Given a premise from a clinical note and a hypothesis, classify the relationship as entailment, contradiction, or neutral.",
                "Why it matters": "Tests whether a model has acquired clinical reasoning beyond surface pattern matching. Used as a fine-tuning evaluation target for clinical encoders.",
                "Hosted at": "PhysioNet (requires credentialed access because the source notes are from MIMIC).",
            },
            {
                "Benchmark family": "BLUE / BLURB",
                "What it covers": "Biomedical Language Understanding Evaluation: a multi-task suite covering sentence classification, NER, relation extraction, and similarity tasks across biomedical text. BLURB is the Microsoft-led successor.",
                "Why it matters": "The standard multi-task evaluation for biomedical encoders. Reporting on BLUE/BLURB is the convention for new clinical fine-tuned models.",
                "Hosted at": "microsoft.github.io/BLURB.",
            },
        ]
    )
    benchmark_table.index = range(1, len(benchmark_table) + 1)
    benchmark_table.index.name = "row"
    benchmark_table
    return (benchmark_table,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Three observations about clinical-NLP benchmarks.

        First, the benchmarks are not the same as production performance. A model that achieves 0.90 F1 on n2c2 may achieve 0.65 F1 on a particular institution's notes because the note-writing conventions differ. The benchmark score is a necessary but not sufficient indicator of fitness for a given deployment.

        Second, the benchmark gold standards have known limitations. Inter-annotator agreement on clinical NER tasks is typically 0.80 to 0.90 F1; a model that achieves 0.85 F1 against the gold may be performing at human level for that task. Reporting model performance as a fraction of inter-annotator agreement is the more honest framing.

        Third, MedQA-style benchmarks have known training-data leakage issues. The benchmark items are public and have likely been seen in some form by any LLM trained on a large internet corpus. Reported MedQA scores for closed-weight LLMs should be interpreted as upper bounds on the model's true held-out performance.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "10",
        "09",
        "LLM appraisal vocabulary from Course 09",
        "Course 09 Track 6 introduced LLMs as next-token predictors with hallucination as a property of the mechanism. Track 4 of Course 09 introduced the five-dimension appraisal framework. Both apply directly here: a vendor selling an LLM-based clinical NLP product is appraised on the same five dimensions (training population, outcome definition, validation approach, calibration, subgroup performance) plus the LLM-specific evaluation challenges (no clean held-out set, prompt sensitivity, API drift).",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "10",
        "12",
        "LLM-based clinical NLP as a CDS layer",
        "Course 12 takes up CDS. An LLM-based extraction layer that feeds a CDS rule is governed by the same five-rights framework as any other CDS source: right information, right person, right format, right channel, right time. The LLM's role is to produce the structured input the CDS rule operates on, not to make the clinical decision.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        Clinical NLP today has two complementary strands. The classical pipeline (Track 02) is the standard for high-throughput, auditable, schema-fixed extraction; LLMs are the standard for flexible drafting, open-ended summarization, and schema-driven extraction tasks. Clinical-domain fine-tuning bridges the gap between general-domain LLMs and clinical text; the canonical fine-tuned models are BioBERT, ClinicalBERT, BlueBERT, and Med-PaLM. Schema-driven extraction with the schema in the prompt is the most common production LLM-NLP pattern; the schema is the integration contract, the temperature should be low, and the audit log of prompt-input-output is the regulatory and reproducibility mechanism. Four benchmark families (n2c2, MedQA-style QA, MedNLI, BLUE/BLURB) cover most clinical-NLP evaluation; the benchmark score is necessary but not sufficient for production deployment.

        Track 05 takes up the evaluation mechanics: precision, recall, F1, the strict-vs-lenient matching distinction, inter-annotator agreement, and the cost-asymmetry argument that clinical NLP usually prioritizes recall.
        """
    )
    return


if __name__ == "__main__":
    app.run()
