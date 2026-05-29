# Track 02: What NLP actually does

The classical NLP pipeline has four standard stages: tokenization (splitting text into the units the rest of the pipeline operates on), named entity recognition (identifying which spans of text refer to which kinds of clinical entity), relation extraction (pairing entities that belong together, like a medication with its dose), and negation/uncertainty detection (distinguishing affirmed mentions from denied or hedged ones). The track walks each stage on a sentence from one of Ms. Reyes's notes, and an inline regex + dictionary NER demo extracts medications, labs, and conditions across her full note corpus so the output of the pipeline is visible end to end.

**Prerequisites:** Track 01 of this course.

**How to start:** open `notebook.py`.

**Companion reading:** `go-deeper.md` in this folder.

**What's next:** Track 03 (De-identification).
