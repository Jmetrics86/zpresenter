"""Placement geometry (inches) for slide images — slots map to fixed regions per layout."""

from __future__ import annotations

from zpresenter.models import ImagePlacement, SlideLayoutKind


def _stack_vertical(
    left: float,
    top: float,
    width: float,
    height: float,
    n: int,
    *,
    gap: float = 0.08,
) -> list[tuple[float, float, float, float]]:
    if n <= 0:
        return []
    if n == 1:
        return [(left, top, width, height)]
    each_h = (height - gap * (n - 1)) / n
    return [(left, top + i * (each_h + gap), width, each_h) for i in range(n)]


# (left_in, top_in, width_in, height_in) base box for the first image in a stack.
_BASE: dict[tuple[SlideLayoutKind, ImagePlacement], tuple[float, float, float, float]] = {
    # Title / section — logo or strip
    ("title", "accent_corner"): (7.42, 4.28, 2.38, 1.78),
    ("title", "banner_lower"): (0.48, 6.42, 9.12, 1.22),
    ("section", "accent_corner"): (7.42, 4.15, 2.38, 1.78),
    ("section", "banner_lower"): (0.48, 6.42, 9.12, 1.22),
    # Title + body — split, below, overlay, strip
    ("title_content", "primary_right"): (5.28, 1.38, 4.58, 5.08),
    ("title_content", "primary_below"): (0.5, 5.52, 9.08, 2.08),
    ("title_content", "accent_corner"): (7.58, 4.92, 2.18, 1.48),
    ("title_content", "banner_lower"): (0.48, 6.52, 9.12, 1.18),
    # Quote
    ("quote", "primary_below"): (0.52, 4.72, 9.05, 2.35),
    ("quote", "accent_corner"): (7.08, 3.72, 2.55, 2.05),
    ("quote", "banner_lower"): (0.48, 6.52, 9.12, 1.18),
    # Charts
    ("chart_bar", "accent_corner"): (8.32, 1.48, 1.82, 1.32),
    ("chart_bar", "banner_lower"): (0.52, 6.35, 9.08, 1.38),
    ("chart_bar", "primary_below"): (0.52, 6.05, 9.08, 1.75),
    ("chart_line", "accent_corner"): (8.32, 1.48, 1.82, 1.32),
    ("chart_line", "banner_lower"): (0.52, 6.35, 9.08, 1.38),
    ("chart_line", "primary_below"): (0.52, 6.05, 9.08, 1.75),
    # Two column
    ("two_column", "two_column_span_below"): (0.5, 6.02, 9.12, 1.58),
    ("two_column", "accent_corner"): (8.12, 1.32, 1.92, 1.42),
    ("two_column", "banner_lower"): (0.48, 6.62, 9.12, 1.12),
}


def rects_for_images(
    layout: SlideLayoutKind,
    placement: ImagePlacement,
    count: int,
) -> list[tuple[float, float, float, float]]:
    """Return inch rectangles for `count` stacked images in the same placement."""
    key = (layout, placement)
    base = _BASE.get(key)
    if base is None or count < 1:
        return []
    le, ti, wi, he = base
    return _stack_vertical(le, ti, wi, he, count)
