# Track 01: Why privacy matters in health data

"Anonymized" is a claim, not a property. This track covers what the claim actually means, when it holds, and why it often does not. The mechanics are concrete. Latanya Sweeney's 2000 paper found that ZIP code, sex, and date of birth uniquely identify roughly 87% of the United States population. Add a hospital admission date and the number gets worse. Add a rare disease and worse still.

The goal is a legible threat model. When you make a privacy decision (release this dataset, share that table, redact this field) you should know what the decision buys you and what it costs.

Four ideas:

1. **The threat model.** Who would re-identify a dataset, why would they bother, and what would they gain. An account of the actual attacker, not a hypothetical one.
2. **Three famous re-identifications.** Governor Weld's medical records (Sweeney, 1997). The Netflix Prize dataset (Narayanan and Shmatikov, 2008). The AOL search query release (2006). Each shows a different way "anonymized" data isn't.
3. **De-identification versus anonymization.** Not the same thing. De-identification means the obvious identifiers were removed. Anonymization means re-identification is statistically infeasible. Most clinical data is the first. Almost none is the second.
4. **The quasi-identifier problem.** Quasi-identifiers are columns that look harmless individually and become identifying in combination. ZIP + sex + DOB is the classic. Encounter date + diagnosis + hospital is the clinical version. The defense is not to remove these columns; the defense is to understand the combinatorics.

The interactive piece is a synthetic registry of 5,000 patients. The learner picks which fields to include in a "de-identified" release, then sees how many patients become uniquely identifiable. The bar moves with each field selected, and the threshold for k-anonymous (no row identifiable to fewer than k patients) shows up as a horizontal line.


**Prerequisites:** None. This is the first track of the first course that touches patient data, so the assumed background is clinical literacy, not informatics experience.

**Companion reading:** `01.1-why-privacy.md` in this folder.

**What's next:** Track 02 on HIPAA. Track 01 builds the threat model. Track 02 walks the specific legal floor the United States has set for it.
