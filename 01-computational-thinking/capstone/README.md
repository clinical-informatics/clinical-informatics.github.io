# Capstone: Design a clinical decision rule

A Socratic walkthrough that uses every move from the five tracks. You design a clinical decision rule end to end on a real-feeling scenario: identifying hospitalized patients who would benefit from a palliative care consultation but do not currently have one.

The notebook walks six steps:

1. **Define the outcome** operationally enough that a data scientist could implement it.
2. **List the inputs** the rule would use, with chart sources and limitations.
3. **Write the rule in plain English** specifically enough that two implementers would produce the same alert.
4. **Find three edge cases** your rule will get wrong, and name which of Track 02's five sources is responsible for each.
5. **Describe the data dependencies and failure modes** for each input.
6. **Identify who the rule is likely to fail for**, and commit to a written monitoring approach for each subgroup.

Each step requires a written answer. The sample answer unlocks only after you have written something of your own. At the end, the notebook assembles your committed answers into a one-page design document. That document is the artifact you can copy out and bring to a real CDS committee.


**Prerequisite:** Tracks 01 through 05. The capstone reuses every framework from those tracks and assumes the vocabulary.

**How to start:** open `notebook.py` from the file tree on the left. Marimo loads it in app mode.

**Output:** a one-page CDR design document written by you, with each section gated by an explicit commitment to think before reading the sample.
