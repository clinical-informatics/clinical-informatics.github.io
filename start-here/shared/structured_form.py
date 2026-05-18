"""Structured form component for clinical-informatics.

For building Marimo capstones that look like real clinical tools. The
learner fills out a guided form. A live preview shows what's being
built. When they're done, they can download a PDF or Markdown summary.

Used by the CDS capstone (course 12), the storytelling capstones
(course 15), and several intermediate exercises.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass
class FormField:
    name: str
    label: str
    kind: str  # "text", "textarea", "radio", "multiselect", "number"
    options: tuple[str, ...] = ()
    placeholder: str = ""
    help_text: str = ""


@dataclass
class StructuredForm:
    title: str
    intro: str = ""
    fields: list[FormField] = field(default_factory=list)

    def add(self, **kwargs) -> "StructuredForm":
        self.fields.append(FormField(**kwargs))
        return self

    def render(self):
        """Build the interactive form. Returns (widget_dict, render_fn)."""
        import marimo as mo

        widgets: dict[str, object] = {}
        ui_blocks = [mo.md(f"## {self.title}")]
        if self.intro:
            ui_blocks.append(mo.md(self.intro))

        for f in self.fields:
            if f.kind == "text":
                w = mo.ui.text(label=f.label, placeholder=f.placeholder, full_width=True)
            elif f.kind == "textarea":
                w = mo.ui.text_area(
                    label=f.label, placeholder=f.placeholder, rows=4, full_width=True
                )
            elif f.kind == "radio":
                w = mo.ui.radio(options=list(f.options), label=f.label)
            elif f.kind == "multiselect":
                w = mo.ui.multiselect(options=list(f.options), label=f.label)
            elif f.kind == "number":
                w = mo.ui.number(label=f.label)
            else:
                raise ValueError(f"Unknown field kind: {f.kind}")

            widgets[f.name] = w
            block = mo.vstack(
                [
                    w,
                    mo.md(f"_{f.help_text}_") if f.help_text else mo.md(""),
                ]
            )
            ui_blocks.append(block)

        def preview():
            values = {name: w.value for name, w in widgets.items()}
            return values, _markdown_summary(self.title, self.fields, values)

        return widgets, ui_blocks, preview


def _markdown_summary(title: str, fields: Iterable[FormField], values: dict[str, object]) -> str:
    lines = [f"# {title}", ""]
    for f in fields:
        val = values.get(f.name)
        if val is None or (isinstance(val, (list, tuple)) and len(val) == 0):
            display = "_(not answered)_"
        elif isinstance(val, (list, tuple)):
            display = ", ".join(str(v) for v in val)
        else:
            display = str(val)
        lines.append(f"## {f.label}")
        lines.append("")
        lines.append(display)
        lines.append("")
    return "\n".join(lines)


def download_button(markdown: str, *, filename: str = "summary.md"):
    """Return a Marimo download button that emits the markdown as a file."""
    import marimo as mo

    return mo.download(
        data=markdown.encode("utf-8"),
        filename=filename,
        label=f"Download {filename}",
    )
