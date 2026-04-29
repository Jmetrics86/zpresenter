"""Map logical layouts to python-pptx slide layouts with ordered fallbacks."""

from __future__ import annotations

from pptx.presentation import Presentation
from pptx.slide import SlideLayout as PptxSlideLayout

from zpresenter.models import SlideLayoutKind


def _iter_slide_layouts(prs: Presentation):
    """All layouts across all slide masters (not only `prs.slide_layouts`, which is master 0)."""
    for master in prs.slide_masters:
        yield from master.slide_layouts


def layout_for(kind: SlideLayoutKind, prs: Presentation) -> PptxSlideLayout:
    """Resolve theme layouts by name; tries several keyword sets per logical layout."""
    order: dict[SlideLayoutKind, list[tuple[str, ...]]] = {
        "title": [("title", "slide"), ("title",)],
        "title_content": [("title", "content"), ("content",)],
        "section": [("section", "header"), ("section",)],
        "quote": [("quote",), ("comparison",), ("title", "content")],
    }
    for keys in order[kind]:
        for layout in _iter_slide_layouts(prs):
            name = layout.name.lower()
            if all(k in name for k in keys):
                return layout
    return prs.slide_layouts[0]
