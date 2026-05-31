# Glossary: 11 Health economics data

Most terms used in this course are defined in the [curriculum-wide glossary](../start-here/GLOSSARY.md): claims data, decision curve analysis (DCA), encounter, OMOP CDM. Health-economics-specific terms are defined below.

**Allowed amount.** The amount a payer has agreed to pay for a service under its contract with the provider. The allowed amount is the sum of the paid amount (what the payer paid) and the patient-responsibility amount (what the patient owes as copay, coinsurance, or deductible). The billed amount on the claim is usually higher than the allowed amount; the difference is contractual write-off.

**Channeling bias.** A selection bias specific to comparative effectiveness research in claims data. Patients are not randomly assigned to medications; physicians "channel" certain patients toward certain drugs (the sickest patients get the newer biologic, the healthier patients get methotrexate alone). Naive comparisons of outcomes by drug then reflect the channeling, not the drug.

**Cost-effectiveness plane.** A two-axis chart with incremental cost on the y-axis and incremental effectiveness on the x-axis, divided into four quadrants. The southeast quadrant (more effective, less costly) is a dominant strategy. The northwest quadrant (less effective, more costly) is dominated. The northeast and southwest quadrants involve a trade-off the willingness-to-pay threshold resolves.

**ICER (incremental cost-effectiveness ratio).** The ratio of the difference in cost between two strategies to the difference in effectiveness. ICER = (cost_B - cost_A) / (effectiveness_B - effectiveness_A). The ICER is compared to the willingness-to-pay threshold to decide whether strategy B is cost-effective relative to strategy A.

**Immortal time bias.** A bias that occurs when the time before a patient becomes eligible for the exposure of interest is misclassified as exposed time. A study of biologic-treated patients that counts the months before the biologic was started as biologic-exposed time inflates the survival of the biologic group, because patients who died before becoming exposed cannot enter the exposed group.

**PMPM (per member per month).** A normalized cost measure. Total cost across a population divided by total member-months. PMPM is the standard unit of comparison for health-plan cost across populations of different sizes and observation windows.

**QALY (quality-adjusted life-year).** A unit of effectiveness that combines length of life and quality of life. One year of life at perfect health is 1.0 QALY; one year at a health state with utility 0.7 is 0.7 QALY. The same year at utility 0.0 (death) is 0 QALY. QALYs make it possible to compare interventions that affect length of life, quality of life, or both.

**Treatment selection bias.** A bias in comparative effectiveness research that arises because the choice of treatment is correlated with the outcome of interest through factors the analyst has not measured. Patients who chose treatment A may differ from patients who chose treatment B in ways that themselves predict outcome. The same idea Course 04 Track 2 introduced as confounding by indication.

**Utility (in cost-effectiveness).** A number between 0 (death) and 1 (perfect health) representing the desirability of a health state. Utilities are estimated by standardized instruments (EQ-5D, SF-6D) administered to patients, and are the weights that convert life-years to QALYs.

**Value-based care (VBC).** A delivery and payment model in which clinicians and institutions are paid for outcomes achieved rather than for the volume of services delivered. ACOs, bundled payments, and quality-payment programs are the operational forms. VBC depends on outcomes measurement, which is most of why this course matters.

**Willingness-to-pay threshold.** The amount per QALY a payer (or society) is willing to pay for an intervention. In the United States, the commonly cited thresholds are $50,000 to $150,000 per QALY; the UK NICE threshold is approximately 20,000 to 30,000 pounds per QALY. An intervention with ICER below the threshold is cost-effective at that threshold.
