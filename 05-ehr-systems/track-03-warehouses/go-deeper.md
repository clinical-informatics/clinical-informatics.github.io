# Go deeper: clinical data warehouses

## If you want to understand this better before moving on

**Kimball Group, "Dimensional Modeling Techniques" reference (free, online).** [https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/)

The Kimball Group's free reference page collects the canonical techniques of dimensional modeling: star schemas, slowly changing dimensions, conformed dimensions, fact-table grains. Not clinical; it is the original BI literature that the entire clinical data warehouse field borrowed its vocabulary from. Reading the Kimball technique cards once gives you the language to talk with any data engineer in the building, in or out of healthcare.

## If you want to see this applied clinically

**Murphy SN, Weber G, Mendis M, et al. "Serving the enterprise and beyond with informatics for integrating biology and the bedside (i2b2)." *Journal of the American Medical Informatics Association*, 2010.** [https://pubmed.ncbi.nlm.nih.gov/20190053/](https://pubmed.ncbi.nlm.nih.gov/20190053/)

The original i2b2 paper. i2b2 is the star-schema-based clinical data mart that most CTSA-funded academic medical centers built their first analytical platform on, starting in the late 2000s. The paper is short and pragmatic. It walks the exact decisions you are working through above: which fact table per clinical domain, which dimensions, how to handle vocabulary, how to expose the result for cohort discovery without coding. The paper is more useful than its abstract suggests because it documents the design rationale for choices that became conventions of the field. Free via PubMed.

## If you want to go significantly further

**Hripcsak G, Duke JD, Shah NH, et al. "Observational Health Data Sciences and Informatics (OHDSI): Opportunities for Observational Researchers." *Studies in Health Technology and Informatics*, 2015.** [https://pubmed.ncbi.nlm.nih.gov/26262116/](https://pubmed.ncbi.nlm.nih.gov/26262116/)

Yes, this is the same paper recommended in Track 01's go-deeper. The reason it lands again here is that OMOP is the most consequential standardized clinical CDM, and OHDSI is the community that built and runs it. The paper makes the federation case explicitly: 250 million patients across dozens of institutions, queryable with the same code, because everyone mapped to the same schema. After reading the Kimball reference and the i2b2 paper, the OHDSI paper completes the arc from "custom CDW per hospital" to "shared CDM across hospitals." Course 07 of this curriculum is where you put SQL on OMOP, but it helps to have read this first.
