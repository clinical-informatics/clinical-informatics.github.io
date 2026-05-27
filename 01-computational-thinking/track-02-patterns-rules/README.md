# Track 02: Patterns, rules, and edge cases

> You finished Track 01 with a working sepsis rule and a drop in alert volume. The post-op cohort is excluded, the infection-context requirement is on, and the inbox is quiet. Two months later, on rounds, a nurse pulls you aside: "It is still missing the older folks who go septic without ever mounting a tachycardic response, and yesterday it fired on a post-ictal patient with a lactate of four." The rule is still wrong, differently wrong, and you did not do anything wrong.

A clinical decision rule is a pattern. It works because most patients in its target population share a recognizable phenotype, and a single specification covers all of them at once. It fails on the patients who do not share that phenotype. Those failures are edge cases. A mature rule is not one with zero edge cases. It is one whose edge cases have been catalogued, named, and accepted.

This track teaches the deliberate generation of edge cases. You will take the rule from Track 01 and stack candidate changes on top of it one at a time. Each change catches a class of patients you were missing and misses a class of patients you were catching. The trade is the lesson. You finish with a working rule and a written catalogue of the patients it gets wrong, which is what a fielded rule looks like in a hospital that is paying attention.


**Prerequisite:** Track 01. The notebook continues where that one ended, on the same medicine cohort, with the same six-part decomposition.

**How to start:** open `notebook.py` from the file tree on the left. Marimo loads it in app mode.

**Companion reading:** [`02.1-patterns-edge-cases.md`](02.1-patterns-edge-cases.md) is a reference essay on the same material. Read it first, after, or not at all.

**What's next:** Track 03 introduces the inverse move. When a rule has been hardened with stacked conditions, the next step is often not another condition but a deletion. That move is abstraction.
