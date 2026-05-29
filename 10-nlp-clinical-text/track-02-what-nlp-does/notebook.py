"""Track 02: What NLP actually does.

The classical NLP pipeline has four standard stages: tokenization, named
entity recognition, relation extraction, and negation/uncertainty
detection. The track walks each stage on a sentence from one of Ms.
Reyes's notes, then runs an inline regex + dictionary NER pipeline
across her full 8-note corpus so the end-to-end output is visible.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import re
    import sys
    import types
    from pathlib import Path

    import marimo as mo
    import pandas as pd

    _COURSE_TITLES = {
        "02": "Data literacy",
        "04": "Clinical epidemiology",
        "07": "Data wrangling and engineering",
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

    _WASM_DATA_BASE = "/10-nlp-clinical-text/track-02-what-nlp-does/app"

    def load_cached_text(filename):
        if "pyodide" in sys.modules:
            from pyodide.http import open_url
            url = f"{_WASM_DATA_BASE}/cache/{filename}"
            return open_url(url).read()
        return (Path(__file__).parent / "cache" / filename).read_text()

    return load_cached_text, mo, pd, re, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 02: What NLP actually does

        ## The four-stage classical pipeline

        A clinical NLP system is built as a sequence of stages, each transforming the text closer to a structured output. The four stages of the classical pipeline are tokenization (splitting the text into units), named entity recognition (identifying which units refer to which clinical concepts), relation extraction (connecting entities that belong together), and negation and uncertainty detection (deciding whether a mentioned concept is affirmed, denied, or hedged).

        The track presents each stage on a sentence from one of Ms. Reyes's notes, then runs an inline regex plus dictionary NER pipeline across her full 8-note corpus so the end-to-end output is visible.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The working sentence

        The track uses the following sentence from Ms. Reyes's 2022-03-07 follow-up note:

        > Initiate methotrexate 10 mg PO weekly, with folic acid 1 mg daily.

        Each stage of the pipeline is shown on this sentence first, then on the full corpus.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Stage 1: tokenization

        Tokenization splits the sentence into the units the rest of the pipeline operates on. The general-domain tokenizer would split on whitespace and punctuation; the clinical tokenizer has to be smarter about medication names, dose expressions, and unit abbreviations.

        The sentence above produces the following tokens under a clinical-aware tokenizer.
        """
    )
    return


@app.cell
def _(pd):
    working_sentence = "Initiate methotrexate 10 mg PO weekly, with folic acid 1 mg daily."
    tokens = ["Initiate", "methotrexate", "10", "mg", "PO", "weekly", ",", "with", "folic acid", "1", "mg", "daily", "."]
    tokens_df = pd.DataFrame({"index": range(len(tokens)), "token": tokens})
    tokens_df.index = range(1, len(tokens_df) + 1)
    tokens_df
    return tokens, tokens_df, working_sentence


@app.cell
def _(mo):
    mo.md(
        r"""
        Two clinical-tokenization decisions are visible in the output.

        First, "folic acid" is kept as a single two-word token. A general-domain tokenizer would split it into "folic" and "acid". The clinical tokenizer recognizes the multi-word drug name and keeps the unit intact.

        Second, "10" and "mg" are separate tokens. A pure regex tokenizer would split them this way by default; a clinical tokenizer could alternatively keep "10 mg" as a single dose-token, depending on whether the downstream stage expects to see the dose value and the unit as separate entities or as a combined one. The choice is a design decision.

        General-domain mistakes a clinical tokenizer must avoid include splitting "DM-2" into three tokens, splitting "1.5 mg/kg/dose" awkwardly, and splitting "anti-CCP" into "anti", "-", "CCP". A clinical tokenizer is conservative and handles these as single tokens where appropriate.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Stage 2: named entity recognition

        Named entity recognition (NER) labels each token (or token span) with the entity type it refers to. The clinical NER targets vary by toolkit, but the standard set covers medications, doses, routes, frequencies, lab tests, conditions, anatomical sites, and observations.

        On the working sentence, a clinical NER pipeline produces the following entity spans.
        """
    )
    return


@app.cell
def _(pd):
    sentence_ner = pd.DataFrame(
        [
            {"span": "Initiate", "entity_type": "ACTION_VERB"},
            {"span": "methotrexate", "entity_type": "MEDICATION"},
            {"span": "10 mg", "entity_type": "DOSE"},
            {"span": "PO", "entity_type": "ROUTE"},
            {"span": "weekly", "entity_type": "FREQUENCY"},
            {"span": "folic acid", "entity_type": "MEDICATION"},
            {"span": "1 mg", "entity_type": "DOSE"},
            {"span": "daily", "entity_type": "FREQUENCY"},
        ]
    )
    sentence_ner.index = range(1, len(sentence_ner) + 1)
    sentence_ner
    return (sentence_ner,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Each labeled span is a potential extraction target. A downstream consumer can ask "what medications were started in this note" and receive the two MEDICATION spans (methotrexate, folic acid) as the answer.

        Clinical NER systems are built in one of three ways. Rule-based systems use regular expressions and a dictionary of canonical clinical terms (the inline pipeline in this notebook is a small example). Statistical systems train a sequence-labeling model on annotated text (the standard architecture is BiLSTM-CRF in the pre-transformer era and BERT-token-classification in the modern era). Hybrid systems combine the two. Each approach produces the same shape of output (a list of typed spans); the differences are in performance, transparency, and resource requirements.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Stage 3: relation extraction

        Named entities are the units; relations are the edges. Relation extraction asks which entities in a sentence belong together. The working sentence has two medication-dose-route-frequency clusters, and relation extraction pairs them correctly.
        """
    )
    return


@app.cell
def _(pd):
    sentence_relations = pd.DataFrame(
        [
            {"medication": "methotrexate", "dose": "10 mg", "route": "PO", "frequency": "weekly"},
            {"medication": "folic acid", "dose": "1 mg", "route": "(unspecified)", "frequency": "daily"},
        ]
    )
    sentence_relations.index = range(1, len(sentence_relations) + 1)
    sentence_relations
    return (sentence_relations,)


@app.cell
def _(mo):
    mo.md(
        r"""
        The output is a structured row per medication, populated from the NER spans. Relation extraction is the step that turns a list of entities into clinically usable rows. A pipeline that stopped at NER would produce eight typed spans; the row representation above is what a downstream consumer can act on.

        Two relation-extraction patterns appear most often. Within-sentence pairing uses proximity and clinical templates ("medication followed by dose followed by route followed by frequency" is the canonical order in US clinical text). Cross-sentence pairing requires more sophisticated machinery (coreference resolution, document-level reasoning) and is the part of the pipeline that LLM-based extractors do noticeably better than classical pipelines.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Stage 4: negation and uncertainty detection

        Identifying that a sentence mentions a clinical concept is necessary; deciding whether the sentence affirms, denies, or hedges that concept is also necessary. "Fever" appears in "fever 38.5C" (affirmed), "no fever" (denied), and "possible fever, recheck temp" (uncertain). A pipeline that ignores the surrounding context will mis-classify the last two as positive fever findings.

        The standard published algorithm is NegEx (Chapman et al. 2001), extended to uncertainty by the ConText algorithm (Harkema et al. 2009). The pattern is the same: a small library of trigger phrases (`no`, `denies`, `negative for`, `rules out` for negation; `possible`, `rule out`, `concerning for`, `appears to be` for uncertainty), each with a defined scope (typically a few tokens forward or backward), and each label propagated to the entities within the scope.

        The working sentence ("Initiate methotrexate 10 mg PO weekly, with folic acid 1 mg daily.") has no negation or uncertainty triggers. The two medication entities are affirmed. A sentence in Reyes's first note ("She denies psoriasis, IBD, recent rash, sicca symptoms, or Raynaud phenomenon.") demonstrates the negation case directly: five condition entities, all of them within the scope of the trigger "denies" and therefore labeled negated.
        """
    )
    return


@app.cell
def _(pd):
    negation_example = pd.DataFrame(
        [
            {"sentence_fragment": "She denies psoriasis,", "entity": "psoriasis", "trigger": "denies", "negated": True},
            {"sentence_fragment": "IBD,", "entity": "IBD", "trigger": "denies", "negated": True},
            {"sentence_fragment": "recent rash,", "entity": "rash", "trigger": "denies", "negated": True},
            {"sentence_fragment": "sicca symptoms,", "entity": "sicca symptoms", "trigger": "denies", "negated": True},
            {"sentence_fragment": "or Raynaud phenomenon.", "entity": "Raynaud phenomenon", "trigger": "denies", "negated": True},
        ]
    )
    negation_example.index = range(1, len(negation_example) + 1)
    negation_example
    return (negation_example,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Note that the NER step happens before the negation step. The NER step finds the five condition entities; the negation step then asks whether the surrounding sentence affirms or denies each. A pipeline that runs NER alone produces five spurious "positive" findings on this sentence; the negation step is what makes the output clinically usable.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## End-to-end: an inline NER pipeline on the Reyes corpus

        The pipeline below is a small rule-based NER system, written inline. It scans every sentence in Ms. Reyes's 8 notes and emits a span per match across three entity categories: medications (matched against a dictionary), labs (matched against a dictionary of common rheumatology labs), and conditions (matched against a small condition list). The pipeline does not do dose extraction or negation handling; both are doable in a few more rules but make the demonstration noisier. The point is to see the end-to-end pipeline produce structured output from narrative text.
        """
    )
    return


@app.cell
def _(load_cached_text):
    notes_text = load_cached_text("notes.txt")
    return (notes_text,)


@app.cell
def _(re):
    MEDICATION_DICT = [
        "methotrexate", "MTX", "folic acid", "naproxen", "ibuprofen",
        "adalimumab", "Humira", "prednisone", "hydroxychloroquine",
        "etanercept", "Enbrel", "infliximab",
    ]
    LAB_DICT = [
        "CRP", "ESR", "anti-CCP", "RF", "rheumatoid factor",
        "ANA", "anti-nuclear antibody", "uric acid", "TSH",
        "hemoglobin", "Hgb", "WBC", "platelet", "plt",
        "ALT", "creatinine", "Cr",
        "QuantiFERON", "Hep B", "Hep C", "hepatitis B", "hepatitis C",
    ]
    CONDITION_DICT = [
        "rheumatoid arthritis", "RA", "psoriasis", "IBD",
        "Raynaud", "lupus", "ankylosing spondylitis",
        "osteoarthritis", "gout", "psoriatic arthritis",
        "viral arthropathy", "anemia", "hypertension",
    ]

    def find_matches(text, dictionary, label):
        matches = []
        for term in dictionary:
            pattern = re.compile(r"\b" + re.escape(term) + r"\b", re.IGNORECASE)
            for m in pattern.finditer(text):
                matches.append({"start": m.start(), "end": m.end(), "surface": m.group(0), "entity_type": label, "canonical": term})
        return matches

    return CONDITION_DICT, LAB_DICT, MEDICATION_DICT, find_matches


@app.cell
def _(CONDITION_DICT, LAB_DICT, MEDICATION_DICT, find_matches, notes_text, pd):
    all_matches = []
    all_matches.extend(find_matches(notes_text, MEDICATION_DICT, "MEDICATION"))
    all_matches.extend(find_matches(notes_text, LAB_DICT, "LAB"))
    all_matches.extend(find_matches(notes_text, CONDITION_DICT, "CONDITION"))

    matches_df = pd.DataFrame(all_matches).sort_values("start").reset_index(drop=True)
    n_med = int((matches_df["entity_type"] == "MEDICATION").sum())
    n_lab = int((matches_df["entity_type"] == "LAB").sum())
    n_cond = int((matches_df["entity_type"] == "CONDITION").sum())
    return all_matches, matches_df, n_cond, n_lab, n_med


@app.cell
def _(mo, n_cond, n_lab, n_med):
    mo.md(
        f"""
        Pipeline output: across the 8 notes (about 9,000 characters of narrative text), the pipeline extracted **{n_med}** medication mentions, **{n_lab}** lab mentions, and **{n_cond}** condition mentions.
        """
    )
    return


@app.cell
def _(matches_df):
    matches_df.head(20)
    return


@app.cell
def _(matches_df, pd):
    counts_by_canonical = (
        matches_df.groupby(["entity_type", "canonical"])
        .size()
        .reset_index(name="mentions")
        .sort_values(["entity_type", "mentions"], ascending=[True, False])
        .reset_index(drop=True)
    )
    counts_by_canonical.index = range(1, len(counts_by_canonical) + 1)
    _ = pd
    counts_by_canonical
    return (counts_by_canonical,)


@app.cell
def _(mo):
    mo.md(
        r"""
        The aggregated counts above show what an end-to-end NER pipeline yields from the narrative side: a structured table of "Reyes's notes mention methotrexate 6 times, anti-CCP 4 times, RA 5 times." A downstream consumer (a research pipeline, a CDS rule, a quality measure) can query the table directly.

        Two important caveats. First, this pipeline has no negation handling, so the "she denies psoriasis" mention is counted as a positive psoriasis finding. Second, the pipeline is dictionary-based, so any medication, lab, or condition not in the dictionary is missed entirely. Both limitations are real and are why production clinical NLP systems use statistical or hybrid approaches that generalize beyond the dictionary and that ship with negation/uncertainty handling.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The clinical NLP toolset

        Five tools cover most of the open-source clinical NLP landscape. None of them runs in the WASM browser environment this notebook is served from, so the inline pipeline above stands in for them at the demonstration level; in a real institution one of the following would be the foundation.

        - **Apache cTAKES.** The canonical Java-based clinical NLP pipeline. Comprehensive coverage of the four-stage pipeline, UMLS integration, negation and assertion modules. Used widely in academic clinical NLP research.
        - **MetaMap.** The NLM-published tool that maps clinical text to UMLS Concept Unique Identifiers (CUIs). The standard reference for concept-level extraction with normalization to a controlled vocabulary.
        - **scispaCy.** A Python-native, spaCy-based biomedical NLP toolkit from the Allen Institute. Smaller and faster than cTAKES; covers tokenization, NER (for a fixed set of UMLS-derived entity types), and UMLS concept linking.
        - **MedSpaCy.** A spaCy-based clinical NLP toolkit with negation, assertion, and section detection components built specifically for clinical text. Complementary to scispaCy.
        - **CLAMP.** A configurable clinical NLP pipeline from UTHealth; commercial use requires a license, academic use is free.

        Two LLM-based options are increasingly common as a complement or replacement: a prompt-engineered call to an enterprise LLM (covered in Track 4), or a fine-tuned biomedical BERT model run locally (BioBERT, ClinicalBERT, BlueBERT).
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "10",
        "07",
        "The vocabulary side of NER",
        "Course 07 Track 1 introduced the code-standard vocabularies (LOINC, SNOMED CT, ICD-10-CM, RxNorm). Clinical NER systems typically normalize their entity spans to one of these vocabularies (RxNorm for medications, LOINC for labs, SNOMED CT for conditions). The normalization step is what turns 'methotrexate' the surface string into RxNorm 6851 the persistent identifier.",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "10",
        "04",
        "Negation and uncertainty are easy to demo, hard to do well",
        "Track 5 of this course takes up evaluation. Negation and uncertainty are typically reported as separate F1 scores from the underlying entity extraction; a pipeline that achieves 0.90 F1 on entity extraction can have 0.70 F1 on negation status because the surrounding-sentence reasoning is more error-prone than the entity-span identification itself.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        A classical clinical NLP pipeline has four stages: tokenization splits the text into operating units, NER labels spans with their entity types, relation extraction connects entities that belong together, and negation/uncertainty detection decides whether each entity is affirmed, denied, or hedged. The four stages produce a structured table from narrative input. An inline regex+dictionary pipeline applied to Ms. Reyes's 8 notes extracted dozens of medication, lab, and condition mentions; the same pipeline architecture in production form is what Apache cTAKES, MetaMap, scispaCy, and the other clinical NLP toolkits implement.

        Track 03 takes up de-identification: the upstream step that has to happen before any clinical note can be processed by an NLP pipeline outside the originating institution.
        """
    )
    return


if __name__ == "__main__":
    app.run()
