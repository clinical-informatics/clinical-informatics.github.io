# Go deeper: imaging informatics

## If you want to understand this better before moving on

**DICOM Standard, official online edition (free).** [https://www.dicomstandard.org/current](https://www.dicomstandard.org/current)

The DICOM standard is released by the DICOM Standards Committee and made fully available online for free. Twenty-one parts; you will not read it cover to cover. The parts to dip into:

- Part 3 (Information Object Definitions): the canonical reference for which tags belong to which SOP class.
- Part 5 (Data Structures and Encoding): what a `.dcm` file actually is, byte by byte.
- Part 7 (Message Exchange): the DIMSE protocol family. Helpful if you need to debug a C-STORE failure.
- Part 18 (Web Services): the DICOMweb services (QIDO-RS, WADO-RS, STOW-RS).

When somebody is reading a tag dump and arguing about what `(0028, 1052)` means, the standard is the answer.

## If you want to see this applied clinically

**van der Heijde D. "How to read radiographs according to the Sharp/van der Heijde method." *Journal of Rheumatology*, 2000.** [https://pubmed.ncbi.nlm.nih.gov/10685822/](https://pubmed.ncbi.nlm.nih.gov/10685822/)

The scoring method this track has been using as the Reyes example, written by the method's namesake. Free via PubMed. The reason this paper belongs in this go-deeper rather than in course 04's is that the scoring system is a worked example of the kind of clinical knowledge that DICOM Structured Reporting *could* encode and almost always does not. Reading it makes the structured-versus-PDF gap concrete: this is what the radiologist is computing, and this is what the PDF report is failing to surface.

## If you want to go significantly further

**Pianykh OS. *Digital Imaging and Communications in Medicine (DICOM): A Practical Introduction and Survival Guide.* Springer, 2012 (2nd ed.).**

A real textbook on DICOM. Not free in full, but most academic medical center libraries have it. The 2nd edition is dated in some specifics (DICOMweb was still emerging) but the underlying material on DIMSE protocols, conformance statements, and PACS architecture is still the best single-volume treatment in print. Worth borrowing if you are responsible for any non-trivial imaging integration work.

If you want an entirely-free alternative, the dcm4che documentation ([https://dcm4che.atlassian.net/wiki/spaces/dcm4che/overview](https://dcm4che.atlassian.net/wiki/spaces/dcm4che/overview)) covers the same DIMSE and DICOMweb material as the textbook with the bonus that it ships running code you can deploy and inspect.
