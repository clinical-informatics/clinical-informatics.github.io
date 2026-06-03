# Track 02: Project organization

A folder contains forty-one files. Three are named `analysis_final.csv`, `analysis_final_v2.csv`, and `analysis_FINAL_use_this_one.csv`. The figure in the submitted manuscript was made from one of them, and no one is now certain which. The raw data has been edited in place, so the original values are gone. This folder cannot be rerun, and it cannot be defended.

The track presents the small number of organizational decisions that make a data project rerunnable by a stranger or by its own author a year later. Four are load-bearing. **Raw data is read-only:** the source files are never edited in place, and every change is a script that writes a new file, so the path from raw to final is always reconstructable. **The folder structure separates inputs from code from outputs:** `data/raw`, `data/processed`, `code`, `results`, so a reader knows where to look and what is safe to delete. **File and variable names are consistent and machine-friendly:** no spaces, dates in ISO 8601, no `FINAL` arms race. **The README is written first:** the document that describes how the project is meant to work exists before the project does, which forces the structure to be explicit while changing it is still cheap. The notebook lets the reader reorganize a deliberately messy RA project folder and see which reproducibility questions each decision answers.

**Prerequisites:** Track 01 of this course.

**How to start:** open `notebook.py`. Marimo loads it in app mode.

**Companion reading:** `go-deeper.md` in this folder.

**What's next:** Track 03 (version control without coding).
