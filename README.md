# Clinical Informatics Open Curriculum

**An open-source course in clinical informatics, written for clinicians, trainees, and researchers who want a way into the field that doesn't feel like climbing a wall.**

Written by **Mario David Felix, MD MHS**.

The curriculum lives at **[https://clinical-informatics.github.io/](https://clinical-informatics.github.io/)**. Twenty-one interactive courses that run entirely in your browser. Nothing to install, no account required.

## Repo structure

This repo holds both the curriculum content (one directory per course) and the static site that publishes it.

```
clinical-informatics.github.io/
├── README.md                        ← you are here
├── mkdocs.yml                       ← site config
├── build_site.py                    ← generates docs/ from the course directories
├── pyproject.toml                   ← Python dependencies
├── .github/workflows/deploy.yml     ← CI: build + deploy on push to main
├── start-here/                      ← orientation, shared components, Ms. Reyes data
├── 00-foundations/                  ← course 00
├── 01-computational-thinking/       ← course 01
├── ...
└── 20-bioinformatics/               ← course 20
```

## Building the site locally

```bash
pip install -e '.[site]'
python build_site.py            # generates docs/, exports notebooks to WASM
mkdocs serve                    # preview at http://127.0.0.1:8000/
```

For faster iteration during development:

```bash
python build_site.py --quick           # skip marimo exports (docs only, ~10 seconds)
python build_site.py --limit 3         # only build first 3 courses
```

## License

- **Course content:** Creative Commons BY 4.0.
- **Code:** MIT.

Single-author curriculum; pull requests are not being accepted. If you spot an error or want to suggest something, open an issue.
