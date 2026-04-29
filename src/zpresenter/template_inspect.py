"""Inspect slide masters / layouts — supports branding templates and debugging."""

from __future__ import annotations

from dataclasses import dataclass

from pptx.presentation import Presentation


@dataclass(frozen=True)
class SlideLayoutRow:
    master_index: int
    layout_index: int
    name: str


def describe_slide_layouts(prs: Presentation) -> list[SlideLayoutRow]:
    """Return every slide layout across all masters (order: master idx, layout idx)."""
    rows: list[SlideLayoutRow] = []
    for mi, master in enumerate(prs.slide_masters):
        for li, layout in enumerate(master.slide_layouts):
            rows.append(SlideLayoutRow(master_index=mi, layout_index=li, name=layout.name))
    return rows
