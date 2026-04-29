"""Map logical layouts to python-pptx slide layouts with ordered fallbacks."""

from __future__ import annotations

from pptx.presentation import Presentation
from pptx.slide import SlideLayout as PptxSlideLayout

from zpresenter.models import SlideLayoutKind

_blankish = [("blank",), ("title", "only"), ("title",)]
_chart_layouts = _blankish
_dual_layouts = [("comparison",), ("two", "content"), ("blank",)]

_LAYOUT_ORDER: dict[SlideLayoutKind, list[tuple[str, ...]]] = {
    "title": [("title", "slide"), ("title",)],
    "title_content": [("title", "content"), ("content",)],
    "section": [("section", "header"), ("section",)],
    "quote": [("quote",), ("comparison",), ("title", "content")],
    "chart_bar": list(_chart_layouts),
    "chart_line": list(_chart_layouts),
    "two_column": list(_dual_layouts),
}


def _iter_slide_layouts(prs: Presentation):
    """All layouts across all slide masters (not only `prs.slide_layouts`, which is master 0)."""
    for master in prs.slide_masters:
        yield from master.slide_layouts


def layout_for(kind: SlideLayoutKind, prs: Presentation) -> PptxSlideLayout:
    """Resolve theme layouts by name; tries several keyword sets per logical layout."""
    order = _LAYOUT_ORDER[kind]
    for keys in order:
        for layout in _iter_slide_layouts(prs):
            name = layout.name.lower()
            if all(k in name for k in keys):
                return layout
    return prs.slide_layouts[0]
