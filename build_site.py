"""Build the clinical-informatics site.

This script:
1. Generates MkDocs source pages (docs/) from the course directories.
2. Runs `marimo export html-wasm` for each notebook.
3. Deduplicates the per-notebook assets/ directories into a single shared
   /_marimo/assets/ directory at the site root, and rewrites relative paths
   in each notebook's index.html to point at the shared location.
4. Writes a .pages file for each course so the awesome-pages plugin orders
   tracks correctly.

Run with:
    python build_site.py                # full build, all notebooks
    python build_site.py --quick        # skip marimo exports (docs only, for fast iteration)
    python build_site.py --limit 3      # only export notebooks from the first 3 courses

After build, run `mkdocs serve` to preview locally at http://127.0.0.1:8000/.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
SHARED_ASSETS_DIR_NAME = "_marimo_assets"  # served at /_marimo_assets/ in the site
NOTEBOOK_APP_DIR_NAME = "app"  # per-track WASM export lives at docs/<course>/<track>/app/
SHARED_ASSETS_PATH = DOCS / SHARED_ASSETS_DIR_NAME

# The course directories, in canonical curriculum order.
COURSES = [
    "00-foundations",
    "01-computational-thinking",
    "02-data-literacy",
    "03-privacy-ethics-governance",
    "04-clinical-epidemiology",
    "05-ehr-systems",
    "06-learn-fhir",
    "07-data-wrangling-engineering",
    "08-clinical-visualization",
    "09-ai-in-medicine",
    "10-nlp-clinical-text",
    "11-health-economics-data",
    "12-clinical-decision-support",
    "13-research-reproducibility",
    "14-interoperability-policy",
    "15-data-storytelling",
    "16-leadership-practice",
    "17-workflow-safety-human-factors",
    "18-population-public-health",
    "19-patient-data-digital-health",
    "20-bioinformatics",
]

COURSE_TITLES = {
    "00-foundations": "00: Foundations of clinical informatics",
    "01-computational-thinking": "01: Computational thinking",
    "02-data-literacy": "02: Data literacy",
    "03-privacy-ethics-governance": "03: Privacy, ethics, and governance",
    "04-clinical-epidemiology": "04: Clinical epidemiology",
    "05-ehr-systems": "05: EHR systems",
    "06-learn-fhir": "06: Learn FHIR",
    "07-data-wrangling-engineering": "07: Data wrangling and engineering",
    "08-clinical-visualization": "08: Clinical visualization",
    "09-ai-in-medicine": "09: AI in medicine",
    "10-nlp-clinical-text": "10: NLP and clinical text",
    "11-health-economics-data": "11: Health economics data",
    "12-clinical-decision-support": "12: Clinical decision support",
    "13-research-reproducibility": "13: Research reproducibility",
    "14-interoperability-policy": "14: Interoperability policy",
    "15-data-storytelling": "15: Data storytelling",
    "16-leadership-practice": "16: Leadership and professional practice",
    "17-workflow-safety-human-factors": "17: Workflow, patient safety, and human factors",
    "18-population-public-health": "18: Population and public health informatics",
    "19-patient-data-digital-health": "19: Patient-generated data, telemedicine, digital health",
    "20-bioinformatics": "20: Bioinformatics for clinical informaticists",
}


def reset_docs(preserve_notebooks: bool = False) -> None:
    """Wipe generated docs/ markdown pages. If preserve_notebooks is True, leave
    notebook/ subdirectories and the shared _marimo_assets/ alone (useful for
    iterating on prose pages without re-running expensive marimo exports).
    """
    if DOCS.exists():
        for entry in DOCS.iterdir():
            # Keep hand-written: index.md, glossary.md, learning-paths.md, orientation.md
            if entry.name in {"index.md", "glossary.md", "learning-paths.md", "orientation.md"}:
                continue
            if preserve_notebooks and entry.name == SHARED_ASSETS_DIR_NAME:
                continue
            if entry.is_dir():
                if preserve_notebooks:
                    # Walk the course dir, delete .md files and .pages, keep notebook/ subdirs
                    for sub in entry.rglob("*"):
                        if sub.is_file() and (sub.suffix == ".md" or sub.name == ".pages"):
                            sub.unlink()
                else:
                    shutil.rmtree(entry)
            else:
                entry.unlink()
    DOCS.mkdir(parents=True, exist_ok=True)


def strip_site_cruft(text: str, depth: int = 0) -> str:
    """Strip Codespaces / repo / file-tree language that doesn't make sense on the website.

    Source READMEs were written for the GitHub-repo + Codespaces delivery model.
    On the standalone site, references to "this repo", "Codespaces", "open notebook.py
    from the file tree", etc. are noise.

    `depth` is the directory depth of the page being processed relative to the
    docs root (home=0, course intro=1, track or capstone intro=2). GitHub URLs
    are rewritten to source-relative `.md` links using this depth so
    `mkdocs build --strict` accepts them.
    """
    prefix = "../" * depth
    # Codespaces badge: original markdown is a wrapped link
    # [![Open in GitHub Codespaces](badge-url)](codespaces.new/...). Strip the whole wrapping link.
    text = re.sub(r"\[!\[Open in GitHub Codespaces\][^)]*\)\]\([^)]*\)\n?", "", text)
    # Defensive: any leftover ![Open in GitHub Codespaces] images on their own
    text = re.sub(r"!\[Open in GitHub Codespaces\][^\n]*\n?", "", text)
    # GitHub repo URLs for org courses become source-relative .md links so the
    # mkdocs link checker resolves them (otherwise --strict treats the warning
    # as an error).
    text = re.sub(
        r"https?://github\.com/clinical-informatics/(\d{2}-[a-z-]+)/?",
        rf"{prefix}\1/index.md",
        text,
    )
    # The start-here repo: rewrite to the site home, source-relative
    text = re.sub(
        r"https?://github\.com/clinical-informatics/start-here/?",
        f"{prefix}index.md" if depth > 0 else "index.md",
        text,
    )
    # "This course is part of the [clinical-informatics-open] curriculum..." boilerplate (per-course READMEs)
    text = re.sub(
        r"\nThis course is part of the \[[^\]]+\]\([^)]+\) curriculum\..*?Check `tasks\.md` in the curriculum root for current progress\.\n",
        "\n",
        text,
        flags=re.DOTALL,
    )
    # Per-track "This track is scaffolded only..." sentence
    text = re.sub(
        r"\nThis track is \*\*scaffolded only\*\*\. The notebook is a placeholder[^\n]*\n",
        "\n",
        text,
    )
    # "How to start" lines for track READMEs ("open notebook.py from the file tree on the left...")
    text = re.sub(
        r"\n\*\*How to start[^*]*?\*\*[^\n]*\n",
        "\n",
        text,
    )
    # "Companion reading (once written):" placeholder line
    text = re.sub(
        r"\n\*\*Companion reading \(once written\):\*\*[^\n]*\n",
        "\n",
        text,
    )
    # "Companion reading:" line that names the essay file by name (repo language)
    text = re.sub(
        r"\n\*\*Companion reading:\*\*[^\n]*\n",
        "\n",
        text,
    )
    # "## Prerequisites" H2 section in per-course READMEs (mentions start-here
    # repo, course-as-folder language; the curriculum's prerequisite story
    # already lives on the home page learning paths)
    text = re.sub(
        r"\n## Prerequisites\n.*?(?=\n## |\Z)",
        "",
        text,
        flags=re.DOTALL,
    )
    # Lingering "start-here repo" inline mentions (rare after the H2 strip but
    # defensive against future authoring drift)
    text = re.sub(
        r"\[start-here repo\]\([^)]*\)",
        "the curriculum home page",
        text,
    )
    # "How to start" H2 section in per-course READMEs (full section, until next H2 or end)
    text = re.sub(
        r"\n## How to start\n.*?(?=\n## |\Z)",
        "",
        text,
        flags=re.DOTALL,
    )
    # "What you'll find in this repo" H2 section in per-course READMEs
    text = re.sub(
        r"\n## What you'll find in this repo\n.*?(?=\n## |\Z)",
        "",
        text,
        flags=re.DOTALL,
    )
    # "Who this is for" H2 section (start-here README): kept implicit by the curriculum design
    text = re.sub(
        r"\n## Who this is for\n.*?(?=\n## |\Z)",
        "",
        text,
        flags=re.DOTALL,
    )
    # "The philosophy" H2 section (start-here README): voice is in the prose, no need to spell it out
    text = re.sub(
        r"\n## The philosophy\n.*?(?=\n## |\Z)",
        "",
        text,
        flags=re.DOTALL,
    )
    # License sections in per-course READMEs (the global footer covers this)
    text = re.sub(
        r"\n## License\n.*?(?=\n## |\Z)",
        "",
        text,
        flags=re.DOTALL,
    )
    text = re.sub(
        r"\n## License and use\n.*?(?=\n## |\Z)",
        "",
        text,
        flags=re.DOTALL,
    )
    # The "You're in the start-here repo" intro paragraph (replaced by build status + how to use admonitions)
    text = re.sub(
        r"\nYou're in the start-here repo\.[^\n]*\n",
        "",
        text,
    )
    # Stray "[" left from any other markdown-link-wrapped badge we missed (defensive)
    # Pattern: a line that is just "[" or starts with "[\n"
    text = re.sub(r"\n\[\n", "\n", text)
    # Footer reference like "[learning-paths.md](learning-paths.md)" pointing to a flat file
    text = re.sub(
        r"A more detailed path guide lives in \[learning-paths\.md\]\(learning-paths\.md\)\.",
        "A more detailed path guide lives on the [learning paths](learning-paths.md) page.",
        text,
    )
    # Final cleanup: trailing whitespace, repeated blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Strip trailing `---` divider left behind when a stripped section was the
    # last thing on the page (e.g. Prerequisites or What you'll find in this repo)
    text = re.sub(r"\n---\s*\n?\Z", "\n", text)
    return text


def link_course_map(body: str, track_slugs: list[str], has_capstone: bool) -> str:
    """Rewrite the course-map table in a course README so each track row's
    title cell links to the corresponding track's intro page (and the capstone
    row links to capstone/index.md, when present).

    Matches table rows of the form
        | 01 | Decomposing a clinical problem | ...the rest of the row... |
    where the first cell is a two-digit number. Links the second cell to
    `<slug>/index.md` using the track folder ordering (row 01 -> first track
    folder, row 02 -> second, ...). The capstone row (second cell exactly
    `**Capstone**`) links to `capstone/index.md`.
    """
    slug_iter = iter(track_slugs)

    def rewrite_track_row(match: re.Match) -> str:
        try:
            slug = next(slug_iter)
        except StopIteration:
            return match.group(0)
        pre, title, post = match.group(1), match.group(2).strip(), match.group(3)
        if title.startswith("["):
            return match.group(0)
        return f"{pre}[{title}]({slug}/index.md){post}"

    body = re.sub(
        r"(\|\s*\d{2}\s*\|\s*)([^|\n]+?)(\s*\|)",
        rewrite_track_row,
        body,
    )
    if has_capstone:
        body = re.sub(
            r"(\|\s*\.\.\.\s*\|\s*)(\*\*Capstone\*\*)(\s*\|)",
            r"\1[\2](capstone/index.md)\3",
            body,
        )
    return body


HOW_TO_USE_HOME = """!!! tip "How to use this curriculum"

    Every track has two pages, **read the intro first, then do the notebook**.

    The intro page sets up the question the track is built around and walks through the clinical reasoning. The notebook page is where you build intuition: interactive sliders, reactive tables, quizzes you commit to before seeing the answer. The combination is the point. Either alone is half the experience.

    **A note on text-input cells.** Some notebook cells ask you to type a written answer. Marimo reacts as you type, but very short inputs sometimes do not trigger the downstream result. If a result does not appear, click below the cell to commit your answer, or add more text until it does.
"""

HOW_TO_USE_COURSE = """!!! tip "How to use this course"

    Each track has two pages, an intro and an interactive notebook. **Read the intro first, then do the notebook.** The intro gives you the framing and the vocabulary; the notebook is where you build the intuition through interactive work.

    **A note on text-input cells.** Some notebook cells ask you to type a written answer. Marimo reacts as you type, but very short inputs sometimes do not trigger the downstream result. If a result does not appear, click below the cell to commit your answer, or add more text until it does.
"""


def read_track_reading(track_dir: Path) -> str:
    """Return the reading content for a track: README + 0X.X-*.md essay (NOT go-deeper).

    Strips intra-track relative .md links and Codespaces / repo cruft. Companion
    essays have their H1 and "reference companion to the notebook" tagline
    stripped so the rendered page flows directly from the README into the first
    real section of the essay.
    """
    parts: list[str] = []
    readme = track_dir / "README.md"
    if readme.exists():
        parts.append(readme.read_text())
    # Concept doc lives next to README, named like "01.1-decomposition.md"
    for essay in sorted(track_dir.glob("0*.md")):
        if essay.name == "go-deeper.md":
            continue
        essay_text = essay.read_text()
        # Strip the essay's H1 (redundant with the track title)
        essay_text = re.sub(r"\A#\s+[^\n]*\n+", "", essay_text)
        # Strip the "reference companion to the notebook" tagline that
        # introduces every essay (variants: "Read it first, after, or skip it",
        # "Read it first, after, or not at all", with optional trailing prose)
        essay_text = re.sub(
            r"\AA reference companion to the notebook\.[^\n]*\n+",
            "",
            essay_text,
        )
        # Drop a leading `---` divider if the tagline strip exposed one
        essay_text = re.sub(r"\A---\s*\n+", "", essay_text)
        parts.append("\n\n---\n\n")
        parts.append(essay_text)
    merged = "\n".join(parts) if parts else "_Track content coming soon._\n"
    merged = re.sub(r"\[([^\]]+)\]\((?!https?://|/)[^)]*\.md\)", r"\1", merged)
    merged = strip_site_cruft(merged, depth=2)
    return merged


def read_go_deeper(track_dir: Path) -> str:
    """Return the go-deeper content for a track, or empty string if none."""
    go_deeper = track_dir / "go-deeper.md"
    if not go_deeper.exists():
        return ""
    text = go_deeper.read_text()
    text = re.sub(r"\[([^\]]+)\]\((?!https?://|/)[^)]*\.md\)", r"\1", text)
    return strip_site_cruft(text, depth=2)


# Notebook link inserted at the bottom of each track intro, before go-deeper.
NOTEBOOK_HANDOFF = (
    "\n\n---\n\n"
    "## Now the notebook\n\n"
    "You have the framing. Open the **[Notebook](notebook.md)** for this track to do the interactive work. "
    "The notebook builds the intuition the intro can only describe.\n"
)


def export_notebook(notebook_path: Path, output_dir: Path) -> bool:
    """Run `marimo export html-wasm` for a single notebook. Returns True on success."""
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "marimo", "export", "html-wasm",
        str(notebook_path),
        "-o", str(output_dir),
        "--mode", "run",
        "--no-show-code",
        "--force",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  FAILED: {notebook_path}")
        print(f"    stderr: {result.stderr[:500]}")
        return False
    return True


def dedupe_assets(notebook_dirs: list[Path]) -> None:
    """Move the first notebook's assets/ to a shared location, delete other copies, rewrite paths.

    Marimo's WASM export produces an assets/ subdir with content-hashed filenames that are
    identical across notebooks. We dedupe by keeping one copy at the site root and rewriting
    every notebook's index.html to point at it via root-relative paths.
    """
    if not notebook_dirs:
        return

    # Find the first directory with an assets/ subdir
    source_assets: Path | None = None
    extras_to_copy = ["android-chrome-192x192.png", "android-chrome-512x512.png",
                      "apple-touch-icon.png", "favicon-16x16.png", "favicon-32x32.png",
                      "favicon.ico", "logo.png", "manifest.json", "site.webmanifest"]

    for nb_dir in notebook_dirs:
        assets = nb_dir / "assets"
        if assets.exists():
            source_assets = assets
            break

    if source_assets is None:
        print("  no assets directories found; nothing to dedupe")
        return

    # Move the source assets to the shared location
    if SHARED_ASSETS_PATH.exists():
        shutil.rmtree(SHARED_ASSETS_PATH)
    shutil.copytree(source_assets, SHARED_ASSETS_PATH)
    # Also copy the favicon/manifest extras from this notebook to the shared dir
    for extra in extras_to_copy:
        src = source_assets.parent / extra
        if src.exists():
            shutil.copy(src, SHARED_ASSETS_PATH / extra)

    print(f"  shared assets at: {SHARED_ASSETS_PATH.relative_to(ROOT)}")

    # Now rewrite every notebook's index.html and delete its local assets/ + extras
    shared_url = f"/{SHARED_ASSETS_DIR_NAME}"
    n_rewritten = 0
    for nb_dir in notebook_dirs:
        index = nb_dir / "index.html"
        if not index.exists():
            continue
        html = index.read_text()
        # Rewrite ./assets/ → /_marimo_assets/  (root-relative; works under any path)
        html = html.replace('"./assets/', f'"{shared_url}/')
        html = html.replace("'./assets/", f"'{shared_url}/")
        # Rewrite favicon, manifest, extras references
        for extra in extras_to_copy:
            html = html.replace(f'"./{extra}"', f'"{shared_url}/{extra}"')
            html = html.replace(f"'./{extra}'", f"'{shared_url}/{extra}'")
        index.write_text(html)

        # Delete the local assets/ to dedupe
        local_assets = nb_dir / "assets"
        if local_assets.exists():
            shutil.rmtree(local_assets)
        # Delete the local favicon/manifest extras (now at shared location)
        for extra in extras_to_copy:
            stray = nb_dir / extra
            if stray.exists():
                stray.unlink()
        # Delete the stray CLAUDE.md if marimo copied it
        stray_claude = nb_dir / "CLAUDE.md"
        if stray_claude.exists():
            stray_claude.unlink()
        n_rewritten += 1

    print(f"  rewrote {n_rewritten} notebook index.html files to use shared assets")


def slugify(name: str) -> str:
    """Convert a directory name like 'track-01-decomposing' to a slug."""
    return name.replace(" ", "-").lower()


def build_course(course_id: str, skip_export: bool = False) -> list[Path]:
    """Generate docs/<course_id>/ pages and export the course's notebooks.

    Returns the list of notebook output directories (for asset deduplication later).
    """
    course_dir = ROOT / course_id
    if not course_dir.is_dir():
        print(f"  SKIP {course_id} (directory not found)")
        return []

    course_docs = DOCS / course_id
    course_docs.mkdir(parents=True, exist_ok=True)

    notebook_dirs: list[Path] = []

    # Discover track folders and capstone presence early so the course-intro
    # course-map table can be rewritten with links to each track page.
    track_dirs_sorted = sorted(
        [d for d in course_dir.iterdir() if d.is_dir() and d.name.startswith("track-")]
    )
    track_slugs = [slugify(d.name) for d in track_dirs_sorted]
    has_capstone = (course_dir / "capstone").is_dir()

    # Course index page from the course README
    course_readme = course_dir / "README.md"
    if course_readme.exists():
        title = COURSE_TITLES.get(course_id, course_id)
        body = course_readme.read_text()
        # Strip the leading H1 if it's just the course number repeated
        body = re.sub(r"^# .+\n", "", body, count=1)
        body = strip_site_cruft(body, depth=1)
        # Wire course-map table rows to the per-track intros
        body = link_course_map(body, track_slugs, has_capstone)
        # Inject the how-to-use admonition after the pitch + byline (i.e., before the first H2)
        body = re.sub(
            r"(\n)(## )",
            r"\1" + HOW_TO_USE_COURSE + r"\n\2",
            body,
            count=1,
        )
        (course_docs / "index.md").write_text(f"# {title}\n\n{body}\n")

    # Helper to emit the full-viewport notebook page
    def notebook_page_md(label: str) -> str:
        return (
            "---\n"
            "hide:\n"
            "  - toc\n"
            f"title: {label}\n"
            "---\n\n"
            f"# {label}\n\n"
            '<iframe src="../app/" '
            'style="width: 100%; height: calc(100vh - 220px); min-height: 600px; '
            'border: 1px solid var(--md-default-fg-color--lightest); border-radius: 8px;" '
            'loading="lazy"></iframe>\n\n'
            "_The notebook runs entirely in your browser. First load takes 10 to 30 seconds while Python boots._\n\n"
            "_If a text-input cell does not show its result after you start typing, click below the cell to commit your answer, or add more text. Marimo reacts as you type, but very short inputs sometimes do not trigger the downstream cell._\n"
        )

    # Track pages: each track becomes a directory with index.md (intro) + notebook.md (interactive)
    track_titles: list[tuple[str, str]] = []
    for track_dir in track_dirs_sorted:
        slug = slugify(track_dir.name)
        track_doc_dir = course_docs / slug
        track_doc_dir.mkdir(parents=True, exist_ok=True)
        reading = read_track_reading(track_dir)
        go_deeper = read_go_deeper(track_dir)

        # Export the notebook and emit notebook.md if successful
        notebook_py = track_dir / "notebook.py"
        has_notebook = False
        out_dir = track_doc_dir / "app"
        if notebook_py.exists() and not skip_export:
            if export_notebook(notebook_py, out_dir):
                notebook_dirs.append(out_dir)
                has_notebook = True
        elif notebook_py.exists() and skip_export and out_dir.exists():
            notebook_dirs.append(out_dir)
            has_notebook = True

        # Compose the intro page: reading + notebook hand-off + go-deeper
        intro_parts = [reading]
        if has_notebook:
            intro_parts.append(NOTEBOOK_HANDOFF)
        if go_deeper:
            intro_parts.append("\n\n---\n\n" + go_deeper)
        (track_doc_dir / "index.md").write_text("".join(intro_parts))

        if has_notebook:
            (track_doc_dir / "notebook.md").write_text(notebook_page_md("Notebook"))

        track_pages = ["  - Introduction: index.md"]
        if has_notebook:
            track_pages.append("  - Notebook: notebook.md")
        track_pages_yaml = "nav:\n" + "\n".join(track_pages) + "\n"
        (track_doc_dir / ".pages").write_text(track_pages_yaml)

        m = re.search(r"^#\s+(.+)$", reading, re.MULTILINE)
        track_titles.append((slug, m.group(1) if m else track_dir.name))

    # Capstone: same two-page split
    capstone_dir = course_dir / "capstone"
    capstone_title: str | None = None
    if capstone_dir.is_dir():
        cap_doc_dir = course_docs / "capstone"
        cap_doc_dir.mkdir(parents=True, exist_ok=True)
        cap_readme = capstone_dir / "README.md"
        reading = cap_readme.read_text() if cap_readme.exists() else "_Capstone content coming soon._\n"
        reading = strip_site_cruft(reading, depth=2)
        m = re.search(r"^#\s+(.+)$", reading, re.MULTILINE)
        capstone_title = m.group(1) if m else "Capstone"

        notebook_py = capstone_dir / "notebook.py"
        has_notebook = False
        out_dir = cap_doc_dir / "app"
        if notebook_py.exists() and not skip_export:
            if export_notebook(notebook_py, out_dir):
                notebook_dirs.append(out_dir)
                has_notebook = True
        elif notebook_py.exists() and skip_export and out_dir.exists():
            notebook_dirs.append(out_dir)
            has_notebook = True

        cap_parts = [reading]
        if has_notebook:
            cap_parts.append(NOTEBOOK_HANDOFF)
        (cap_doc_dir / "index.md").write_text("".join(cap_parts))

        if has_notebook:
            (cap_doc_dir / "notebook.md").write_text(notebook_page_md("Notebook"))

        cap_pages = ["  - Introduction: index.md"]
        if has_notebook:
            cap_pages.append("  - Notebook: notebook.md")
        cap_pages_yaml = "nav:\n" + "\n".join(cap_pages) + "\n"
        (cap_doc_dir / ".pages").write_text(cap_pages_yaml)

    # awesome-pages .pages file to enforce ordering within the course.
    # Index gets an explicit "Introduction" label so the sidebar shows it as a
    # sibling of the track sections (parallels each track's Introduction/Notebook
    # split). Tracks and capstone keep their directory names so awesome-pages
    # picks up the H1 from each subfolder's index.md.
    pages_lines = ["nav:", "  - Introduction: index.md"]
    for slug, _ in track_titles:
        pages_lines.append(f"  - {slug}")
    if capstone_title:
        pages_lines.append("  - capstone")
    (course_docs / ".pages").write_text("\n".join(pages_lines) + "\n")

    print(f"  built {course_id}: {len(track_dirs_sorted)} tracks + {'capstone' if capstone_title else 'no capstone'}")
    return notebook_dirs


def classify_course(course_id: str) -> tuple[str, int, int, bool]:
    """Inspect a course directory and return (status, built_tracks, total_tracks, capstone_built).

    A notebook is considered 'built' if it does NOT contain the literal string
    'scaffolded only' (which is in every scaffold placeholder).

    status is one of: 'built' (all tracks + capstone built),
                      'partial' (some tracks built),
                      'scaffolded' (no tracks built).
    """
    course_dir = ROOT / course_id
    if not course_dir.is_dir():
        return ("scaffolded", 0, 0, False)
    tracks = sorted([d for d in course_dir.iterdir() if d.is_dir() and d.name.startswith("track-")])
    total = len(tracks)
    built = 0
    for t in tracks:
        nb = t / "notebook.py"
        if not nb.exists():
            continue
        text = nb.read_text()
        if "scaffolded only" not in text and "scaffold)" not in text:
            built += 1
    cap = course_dir / "capstone" / "notebook.py"
    capstone_built = False
    if cap.exists():
        text = cap.read_text()
        capstone_built = "scaffolded only" not in text and "scaffold)" not in text
    if built == total and (total > 0) and capstone_built:
        status = "built"
    elif built > 0 or capstone_built:
        status = "partial"
    else:
        status = "scaffolded"
    return (status, built, total, capstone_built)


def build_status_admonition() -> str:
    """Generate a markdown admonition summarizing what's built across all 21 courses."""
    by_status: dict[str, list[str]] = {"built": [], "partial": [], "scaffolded": []}
    detail: list[str] = []
    for cid in COURSES:
        status, b, t, cap = classify_course(cid)
        title = COURSE_TITLES.get(cid, cid)
        by_status[status].append(title)
        if status == "partial":
            cap_str = ", capstone built" if cap else ""
            detail.append(f"  - **{title}**: {b}/{t} tracks built{cap_str}")

    lines = ['!!! note "Current build status"']
    lines.append("")
    def pluralize(n: int, singular: str, plural: str) -> str:
        return f"**{n} {singular if n == 1 else plural}**"
    n_built = len(by_status['built'])
    n_partial = len(by_status['partial'])
    n_scaff = len(by_status['scaffolded'])
    lines.append(
        f"    The curriculum is being actively written. {pluralize(n_built, 'course', 'courses')} "
        f"of 21 {'is' if n_built == 1 else 'are'} fully built (interactive notebooks ready). "
        f"{pluralize(n_partial, 'course', 'courses')} {'is' if n_partial == 1 else 'are'} partially built, "
        f"and {pluralize(n_scaff, 'is scaffolded', 'are scaffolded')} with the structure in place but content still to come. "
        "Tracks whose content has not been written yet show a placeholder notebook in the interactive area at the bottom of their page; "
        "the reading content above it is also a placeholder until written."
    )
    lines.append("")
    if by_status["built"]:
        lines.append("    **Fully built:**")
        lines.append("")
        for t in by_status["built"]:
            lines.append(f"    - {t}")
        lines.append("")
    if by_status["partial"]:
        lines.append("    **Partially built:**")
        lines.append("")
        for line in detail:
            lines.append(f"  {line}")
        lines.append("")
    if by_status["scaffolded"]:
        lines.append("    **Scaffolded (content coming):**")
        lines.append("")
        for t in by_status["scaffolded"]:
            lines.append(f"    - {t}")
        lines.append("")
    return "\n".join(lines) + "\n"


def write_top_level_pages() -> None:
    """Copy start-here landing content into docs/ if not already present."""
    start_here = ROOT / "start-here"

    # docs/index.md from start-here/README.md, with build-status + how-to-use admonitions injected
    sh_readme = start_here / "README.md"
    if sh_readme.exists():
        text = sh_readme.read_text()
        text = strip_site_cruft(text)
        # Inject build status + how-to-use admonitions right after the byline.
        # The byline currently reads "Designed, written, and edited by ..." on
        # the home page; the per-course READMEs still use "Written by ...".
        # Match either form so the home page and the course-intro pipeline
        # share a single rewrite.
        injection = "\n" + build_status_admonition() + "\n" + HOW_TO_USE_HOME + "\n"
        text = re.sub(
            r"((?:Designed, written, and edited|Written) by \*\*Mario David Felix, MD MHS\*\*\.\n)",
            r"\1" + injection,
            text,
            count=1,
        )
        (DOCS / "index.md").write_text(text)

    # docs/learning-paths.md (rewrite GitHub URLs to internal site links)
    sh_paths = start_here / "learning-paths.md"
    if sh_paths.exists():
        text = strip_site_cruft(sh_paths.read_text())
        (DOCS / "learning-paths.md").write_text(text)

    # docs/glossary.md
    sh_glossary = start_here / "GLOSSARY.md"
    if sh_glossary.exists():
        (DOCS / "glossary.md").write_text(sh_glossary.read_text())

    print("  wrote top-level pages: index.md (with build-status admonition), learning-paths.md, glossary.md")


def write_top_level_pages_yaml(course_ids: list[str]) -> None:
    """Write a top-level .pages file grouping courses into the seven categories.

    The categories mirror those in start-here/home.py so a learner sees the
    same conceptual scaffolding in the sidebar as in the welcome notebook.
    """
    # Each category lists the course IDs that belong to it, in curriculum order.
    categories: list[tuple[str, list[str]]] = [
        ("Foundational courses", [
            "00-foundations",
            "01-computational-thinking",
            "02-data-literacy",
            "03-privacy-ethics-governance",
            "04-clinical-epidemiology",
        ]),
        ("Technical core", [
            "05-ehr-systems",
            "06-learn-fhir",
            "07-data-wrangling-engineering",
            "08-clinical-visualization",
        ]),
        ("Applied courses", [
            "09-ai-in-medicine",
            "10-nlp-clinical-text",
            "11-health-economics-data",
            "12-clinical-decision-support",
        ]),
        ("Wider field", [
            "13-research-reproducibility",
            "14-interoperability-policy",
            "15-data-storytelling",
        ]),
        ("Working informaticist's toolkit", [
            "16-leadership-practice",
            "17-workflow-safety-human-factors",
        ]),
        ("Modern practice frontiers", [
            "18-population-public-health",
            "19-patient-data-digital-health",
            "20-bioinformatics",
        ]),
    ]

    course_set = set(course_ids)
    nav_lines = [
        "nav:",
        "  - Home: index.md",
        "  - Learning paths: learning-paths.md",
        "  - Glossary: glossary.md",
    ]
    for category_title, members in categories:
        # Only include categories with at least one built course
        built = [c for c in members if c in course_set]
        if not built:
            continue
        nav_lines.append(f"  - {category_title}:")
        for cid in built:
            title = COURSE_TITLES.get(cid, cid)
            # Keep the "NN: " number prefix so the course number is visible at
            # a glance (e.g. "01: Computational thinking" rather than just
            # "Computational thinking").
            nav_lines.append(f"    - '{title}': {cid}")
    (DOCS / ".pages").write_text("\n".join(nav_lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="Skip marimo exports (docs only)")
    parser.add_argument("--limit", type=int, default=None, help="Only build the first N courses")
    args = parser.parse_args()

    print("=== Resetting docs/ ===")
    reset_docs(preserve_notebooks=args.quick)

    print("=== Writing top-level pages ===")
    write_top_level_pages()

    courses = COURSES[: args.limit] if args.limit else COURSES
    print(f"=== Building {len(courses)} courses ===")

    all_notebook_dirs: list[Path] = []
    for course_id in courses:
        nb_dirs = build_course(course_id, skip_export=args.quick)
        all_notebook_dirs.extend(nb_dirs)

    if not args.quick:
        print("=== Deduplicating notebook assets ===")
        dedupe_assets(all_notebook_dirs)

    print("=== Writing top-level nav ===")
    write_top_level_pages_yaml(courses)

    print(f"\nDone. {len(all_notebook_dirs)} notebooks exported.")
    print("Run `mkdocs serve` to preview at http://127.0.0.1:8000/")


if __name__ == "__main__":
    main()
