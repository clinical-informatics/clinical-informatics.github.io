# Track 01: Decomposing a clinical problem

> Your hospital's sepsis alert fires forty times a day. Clinicians have stopped looking at it. You have stopped looking at it. The alert is doing exactly what it was told to do. So why is it useless?

The first move of computational thinking is decomposition: restate a problem as a set of smaller named parts you can examine one at a time. You already do this in clinical reasoning. The work here is naming the move and applying it deliberately to a misbehaving sepsis alert.

After the notebook, you can name the working parts of any clinical decision rule: cohort, signals, thresholds, time window, data source, and trigger moment. Most of the work of fixing a rule is identifying which of these six is the problem.


**How to start:** open `notebook.py` in this folder from the file tree on the left. Marimo loads it in app mode. There is no code to read. Every interaction is a slider, a checkbox, or a short prompt.

**Companion reading:** [`01.1-decomposition.md`](01.1-decomposition.md) is a short reference essay on the same material. Read it first, after, or not at all. It is not a prerequisite.

**What's next:** Track 02 takes the rule you finish this notebook with and adds conditions one at a time. Each new condition tightens the rule and creates a new edge case. Together, the two tracks cover the two halves of the same skill: taking a rule apart, and assembling one while knowing what it will and will not catch.
