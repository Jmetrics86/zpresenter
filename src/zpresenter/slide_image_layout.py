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
# All rectangles are bounded by the standard 10.0 × 7.5 inch slide.
_BASE: dict[tuple[SlideLayoutKind, ImagePlacement], tuple[float, float, float, float]] = {
    # Title / section — logo corner or full-width lower strip
    ("title",   "accent_corner"): (7.42, 4.28, 2.38, 1.78),   # right=9.80  bottom=6.06
    ("title",   "banner_lower"):  (0.48, 6.28, 9.12, 1.22),   # right=9.60  bottom=7.50
    ("section", "accent_corner"): (7.42, 4.15, 2.38, 1.78),   # right=9.80  bottom=5.93
    ("section", "banner_lower"):  (0.48, 6.28, 9.12, 1.22),   # right=9.60  bottom=7.50
    # Title + body — split right, full-width below, corner, or strip
    ("title_content", "primary_right"):  (5.28, 1.38, 4.58, 5.08),  # right=9.86  bottom=6.46
    ("title_content", "primary_below"):  (0.50, 5.42, 9.08, 2.08),  # right=9.58  bottom=7.50
    ("title_content", "accent_corner"):  (7.58, 4.92, 2.18, 1.48),  # right=9.76  bottom=6.40
    ("title_content", "banner_lower"):   (0.48, 6.32, 9.12, 1.18),  # right=9.60  bottom=7.50
    # Quote
    ("quote", "primary_below"): (0.52, 4.72, 9.05, 2.35),  # right=9.57  bottom=7.07
    ("quote", "accent_corner"): (7.08, 3.72, 2.55, 2.05),  # right=9.63  bottom=5.77
    ("quote", "banner_lower"):  (0.48, 6.32, 9.12, 1.18),  # right=9.60  bottom=7.50
    # Charts — accent corner pulled in to stay within 10" width
    ("chart_bar",  "accent_corner"):  (7.98, 1.48, 1.82, 1.32),  # right=9.80  bottom=2.80
    ("chart_bar",  "banner_lower"):   (0.52, 6.28, 9.08, 1.22),  # right=9.60  bottom=7.50
    ("chart_bar",  "primary_below"):  (0.52, 5.72, 9.08, 1.78),  # right=9.60  bottom=7.50
    ("chart_line", "accent_corner"):  (7.98, 1.48, 1.82, 1.32),  # right=9.80  bottom=2.80
    ("chart_line", "banner_lower"):   (0.52, 6.28, 9.08, 1.22),  # right=9.60  bottom=7.50
    ("chart_line", "primary_below"):  (0.52, 5.72, 9.08, 1.78),  # right=9.60  bottom=7.50
    # Two column — accent corner and span corrected to fit within bounds
    ("two_column", "two_column_span_below"): (0.50, 5.90, 9.12, 1.60),  # right=9.62  bottom=7.50
    ("two_column", "accent_corner"):         (7.88, 1.32, 1.82, 1.42),  # right=9.70  bottom=2.74
    ("two_column", "banner_lower"):          (0.48, 6.28, 9.12, 1.22),  # right=9.60  bottom=7.50
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
