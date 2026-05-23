"""Cross-reference callouts for clinical-informatics.

Cross-references make the stacking arcs of the curriculum visible. Use them
whenever you revisit a concept introduced in an earlier course. The
learner sees a small inline panel saying "remember X from course N? Here's
what happens when we extend it…"

The arcs that matter most:

- **2x2 table → ROC curve → discrimination vs calibration → decision curve analysis**
- **Portability vs interoperability → OMOP → FHIR → CDS Hooks**
- **Computational thinking → CQL logic**
- **Structured vs unstructured data → NLP**
- **Privacy principles, revisited in every course that touches patient data**
"""

from __future__ import annotations


COURSE_TITLES = {
    "00": "Foundations of clinical informatics",
    "01": "Computational thinking",
    "02": "Data literacy",
    "03": "Privacy, ethics, and governance",
    "04": "Clinical epidemiology",
    "05": "EHR systems",
    "06": "Learn FHIR",
    "07": "Data wrangling and engineering",
    "08": "Clinical visualization",
    "09": "AI in medicine",
    "10": "NLP and clinical text",
    "11": "Health economics data",
    "12": "Clinical decision support",
    "13": "Research reproducibility",
    "14": "Interoperability policy",
    "15": "Data storytelling",
    "16": "Leadership and professional practice",
    "17": "Workflow, safety, and human factors",
    "18": "Population and public health",
    "19": "Patient data and digital health",
    "20": "Bioinformatics",
}


def _course_label(course_id: str) -> str:
    title = COURSE_TITLES.get(course_id.split("-")[0], None)
    if title is None:
        return course_id
    return f"course {course_id.split('-')[0]}: {title}"


def callback(
    from_course: str,
    to_course: str,
    topic: str,
    body: str,
):
    """Render a cross-reference callback.

    Parameters
    ----------
    from_course:
        The course where the reader currently is (e.g. ``"09"``).
    to_course:
        The course where the concept was first introduced (e.g. ``"04"``).
    topic:
        The short name of the concept being recalled.
    body:
        A paragraph that recalls the prior treatment and motivates the
        deeper treatment that follows in the current course.
    """
    import marimo as mo

    src = _course_label(to_course)
    header = f"**Remember {topic} from {src}?**"
    return mo.callout(
        mo.vstack([mo.md(header), mo.md(body)]),
        kind="info",
    )


def forward(from_course: str, to_course: str, topic: str, body: str):
    """Render a forward reference to a later course."""
    import marimo as mo

    dst = _course_label(to_course)
    header = f"**Forward to {dst}: {topic}**"
    return mo.callout(
        mo.vstack([mo.md(header), mo.md(body)]),
        kind="neutral",
    )
