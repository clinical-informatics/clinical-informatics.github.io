## Go deeper

**For a published example of an equity-flagged feature included by default without justification:**
- Vyas DA, Eisenstein LG, Jones DS. *Hidden in Plain Sight: Reconsidering the Use of Race Correction in Clinical Algorithms.* NEJM 2020; 383(9): 874-882. The piece that put race correction in eGFR and other clinical algorithms on the national agenda. A worked example of category 2 ("equity-flagged features") and a working illustration of why "we included it because the AUC went up" is not sufficient justification. [pubmed.ncbi.nlm.nih.gov/32853499](https://pubmed.ncbi.nlm.nih.gov/32853499/)

**For the canonical case of a model in production whose feature choices encoded bias at scale:**
- Obermeyer Z, Powers B, Vogeli C, Mullainathan S. *Dissecting Racial Bias in an Algorithm Used to Manage the Health of Populations.* Science 2019; 366(6464): 447-453. A widely-deployed risk-stratification tool used healthcare costs as a proxy for clinical need and systematically under-prioritized Black patients with the same disease burden. A study in what a feature actually means versus what its designers thought it meant. [pubmed.ncbi.nlm.nih.gov/31649194](https://pubmed.ncbi.nlm.nih.gov/31649194/)

**To go significantly further:**
- Rudin C. *Stop Explaining Black Box Machine Learning Models for High-Stakes Decisions and Use Interpretable Models Instead.* Nature Machine Intelligence 2019; 1: 206-215. The argument that, in high-stakes settings (medicine, criminal justice, hiring), parsimony is not a tax on accuracy but a precondition for deployment. Rudin's working position: for most clinical problems, an interpretable model in the four- to twelve-feature range performs comparably to a black-box model with two orders of magnitude more inputs, and the gap between them is mostly accounting noise. Closely related to the LACE-vs-200-feature comparison the notebook touches. [nature.com/articles/s42256-019-0048-x](https://www.nature.com/articles/s42256-019-0048-x)
