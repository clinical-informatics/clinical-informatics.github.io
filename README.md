# Clinical Informatics Open Curriculum

The source repository for the **Clinical Informatics Open Curriculum**, a free and open curriculum of twenty-one interactive courses in clinical informatics for clinicians, trainees, and clinical researchers.

The site lives at **[https://clinical-informatics.github.io/](https://clinical-informatics.github.io/)**. Every course runs in the browser. Nothing to install.

Designed, written, and edited by **Mario David Felix, MD MHS**.

## What this repository contains

- The full content of every course (one directory per course, plus `start-here/` for the home and shared components).
- The static-site build pipeline that converts the course directories into the MkDocs site at the URL above.
- Synthetic data for **Ms. Elena Reyes**, the running rheumatoid arthritis case used in every course.
- The GitHub Actions workflow that builds and deploys the site on every push to `main`.

## Repository layout

```
clinical-informatics.github.io/
├── README.md                        ← this file
├── mkdocs.yml                       ← site config
├── build_site.py                    ← generates docs/ from the course directories
├── pyproject.toml                   ← Python dependencies
├── .github/workflows/deploy.yml     ← CI: build + deploy on push to main
├── start-here/                      ← home page, learning paths, glossary, shared components, Ms. Reyes data
├── 00-foundations/                  ← course 00
├── 01-computational-thinking/       ← course 01
├── ...
└── 20-bioinformatics/               ← course 20
```

Each course directory contains a `README.md` (the course intro), a `track-XX-*` directory per track (each with its own intro plus a Marimo notebook), a `capstone/` directory, and a `go-deeper.md` per track listing the curated free resources for that topic.

## Building the site locally

```bash
pip install -e '.[site]'
python build_site.py            # generates docs/, exports notebooks to WASM
mkdocs serve                    # preview at http://127.0.0.1:8000/
```

For faster iteration during prose work:

```bash
python build_site.py --quick           # skip marimo exports (docs only, ~10 seconds)
python build_site.py --limit 3         # only build the first 3 courses
```

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum. Pull requests are not accepted. To report an error or suggest content, email [fmario619@gmail.com](mailto:fmario619@gmail.com).
