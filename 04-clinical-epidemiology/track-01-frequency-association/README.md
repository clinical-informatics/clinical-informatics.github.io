# Track 01: Measures of frequency and association

Five measures appear in nearly every clinical paper: prevalence, incidence, RR, OR, and HR. This track defines each one on a synthetic 2,000-patient RA cohort and shows how restricting the cohort changes the numbers.

Confusing these measures is one of the most common errors in the clinical literature. Treating an odds ratio as if it were a risk ratio inflates effects. Treating a relative risk as if it were an absolute risk overstates clinical impact. Treating cumulative incidence as a rate when follow-up is unequal hides selection.

The cohort is split evenly: half on csDMARDs alone, half on a TNFi, with three years of follow-up. Each measure is defined inline, computed on the full cohort, and then recomputed as you restrict by age, sex, sero status, or disease duration. Watching the numbers shift is how the intuition builds.

**Prerequisite:** None within this course. The 01-computational-thinking and 02-data-literacy courses are useful background but not required.


**How to start:** `marimo run track-01-frequency-association/notebook.py`, or click the run button from the course home page.

## What you will leave with

- A sentence for each of prevalence, cumulative incidence, incidence rate, RR, OR, and HR that explains *when to use it* and *what its denominator means*.
- An intuition for when OR and RR diverge (common outcomes) and what the rare-disease approximation actually buys you.
- An intuition for why HR is the right summary when follow-up is unequal.
- A feel for how restricting a cohort (age, sex, sero status, disease duration) moves the measures in different directions, and which measures are most fragile when the sample shrinks.

## What's next

Track 02 covers bias. You will take a simple cohort analysis, add a confounder, and watch the effect estimate flip sign. The goal is a working sense of how the number you see can be the wrong number.
