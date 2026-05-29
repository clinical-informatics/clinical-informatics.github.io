# Go deeper: De-identification

**If you want to understand the HIPAA framework better before moving on:**

- [HHS guidance on the De-identification of Protected Health Information](https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html) is the canonical reference for the Safe Harbor method and the Expert Determination method. The page enumerates the 18 identifier categories and explains the recipient-population requirement that conditions the safe-harbor "no actual knowledge" clause.
- [NIST Special Publication 800-188, "Trustworthy Foundations of De-Identification"](https://csrc.nist.gov/pubs/sp/800/188/final) is the technical companion. It covers the residual-risk question, the quasi-identifier problem, k-anonymity, and the operational measures that go beyond Safe Harbor.

**If you want to see this applied clinically:**

- [Stubbs and Uzuner, "Annotating longitudinal clinical narratives for de-identification: The 2014 i2b2/UTHealth corpus" (Journal of Biomedical Informatics 2015)](https://www.sciencedirect.com/science/article/pii/S1532046415001148) documents the construction of the most widely used clinical de-identification benchmark. The paper is the gold-standard reference for understanding what high-quality de-id annotation looks like and what the inter-annotator disagreements indicate about the task's difficulty.
- The [DEID software from Massachusetts General Hospital](https://www.physionet.org/content/deid/1.1/) is a published de-identification toolkit available with documentation at PhysioNet. It demonstrates a rule-based system with documented performance and is a useful comparison point for evaluating any newer system against.

**If you want to go significantly further:**

- [Norgeot et al., "Protected Health Information filter (Philter): accurately and securely de-identifying free-text clinical notes" (NPJ Digital Medicine 2020)](https://www.nature.com/articles/s41746-020-0258-y) is the published reference for a modern hybrid (rule plus ML) de-identification system. The paper documents both the algorithmic design and the residual-risk analysis a real institution would conduct before sharing notes externally.
