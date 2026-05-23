# Track 04: Imaging informatics (PACS, DICOM, RIS, structured reporting)

Ms. Reyes had bilateral hand and wrist radiographs at her first rheumatology visit in February 2022. By 2024 she had a series of three: the baseline, one at six months, one at eighteen months. The radiology report on each one walks the Sharp/van der Heijde erosion and joint-space-narrowing components. The 2022 study and the 2024 study sit on different storage tiers. The orders flowed from the EHR through one system. The result PDFs came back through a different one. Inside the radiologist's reading room, a fourth system displays the images.

This track is about how that subsystem works. DICOM as the standard. PACS as the storage and viewer. RIS as the orders-and-reporting layer. The DICOMweb services that connect everything. Structured reporting (DICOM SR) versus the PDF report that most hospitals still ship. The bridge between PACS and the EHR.

The track puts a DICOM tag dump in front of you, walks the four-system architecture as a diagram, and surfaces the structural reason the radiology report on Ms. Reyes's chart is a PDF instead of a row in a structured-results table.

**Estimated time:** 75 minutes.

**Prerequisites:** Tracks 01 through 03 of this course (especially Track 01's storage-tiering section and Track 03's analytical-system framing).

**How to start:** open `notebook.py` in Marimo. The notebook shows a synthetic DICOM tag dump for Reyes's 2024 hand-series instance, walks the four-system architecture interactively, and contrasts a structured-report and a PDF-report rendering of the same Sharp/van der Heijde score.

**Companion reading:** `04.1-imaging.md` in this folder is the reference essay.

**What's next:** Track 05 (real-world data quality), which picks up the structured-versus-PDF gap that this track surfaces.
