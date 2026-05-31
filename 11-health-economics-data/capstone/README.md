# Capstone: Decision tree for the RA treatment choice, with one-way sensitivity

The reader assembles a decision tree for the biologic-vs-csDMARD choice in a patient like Ms. Reyes. The inputs are reactive: the probability of a clinically meaningful response on each treatment, the probability of an adverse event on each, the utility of full response vs partial vs serious adverse event, and the time horizon. The outputs are the expected value per arm and a sensitivity-sweep chart that shows the value of each arm as a function of one chosen input, with the cross-over point (the value of the input at which the preferred strategy flips) marked explicitly.

The capstone is a building exercise; by the end the reader has produced the kind of decision-analytic artifact that a pharmacy and therapeutics committee would actually use in a formulary decision.

**Prerequisites:** all six tracks in this course.

**How to start:** open `notebook.py`. Marimo loads it in app mode.
