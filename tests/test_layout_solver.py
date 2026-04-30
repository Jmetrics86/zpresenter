"""Tests for semantic layout hints and content-shaped inference."""

from zpresenter.layout_solver import (
    infer_layout_from_content,
    intent_matches_layout,
    resolve_slide_layout_or_raise,
    suggest_deck,
    suggest_slide,
)
from zpresenter.models import ChartSeries, Deck, Slide


def test_intent_matches_layout_when_none() -> None:
    assert intent_matches_layout(None, "title_content") is True


def test_intent_requires_specific_layout() -> None:
    assert intent_matches_layout("comparison", "two_column") is True
    assert intent_matches_layout("comparison", "title_content") is False


def test_infer_chart_bar_from_series() -> None:
    slide = Slide(
        layout="title_content",
        title="Wrong layout",
        chart_categories=["Q1", "Q2"],
        chart_series=[ChartSeries(name="Rev", values=[1.0, 2.0])],
    )
    assert infer_layout_from_content(slide, 1) == "chart_bar"


def test_infer_chart_line_from_subtitle_hint() -> None:
    slide = Slide(
        layout="title_content",
        title="Trend",
        subtitle="Trajectory over time",
        chart_categories=["Q1", "Q2"],
        chart_series=[ChartSeries(name="Rev", values=[1.0, 2.0])],
    )
    assert infer_layout_from_content(slide, 1) == "chart_line"


def test_infer_two_column_when_both_columns_populated() -> None:
    slide = Slide(
        layout="title_content",
        title="x",
        bullets_left=["a"],
        bullets_right=["b"],
    )
    assert infer_layout_from_content(slide, 1) == "two_column"


def test_infer_chart_bar_when_metrics_bar_intent() -> None:
    slide = Slide(
        layout="title_content",
        layout_intent="metrics_bar",
        title="x",
        chart_categories=["A"],
        chart_series=[ChartSeries(name="n", values=[1.0])],
    )
    assert infer_layout_from_content(slide, 1) == "chart_bar"


def test_infer_chart_line_when_metrics_trend_intent() -> None:
    slide = Slide(
        layout="title_content",
        layout_intent="metrics_trend",
        title="x",
        chart_categories=["A"],
        chart_series=[ChartSeries(name="n", values=[1.0])],
    )
    assert infer_layout_from_content(slide, 1) == "chart_line"


def test_resolve_slide_prefers_compatible_inference_under_intent() -> None:
    s = Slide(
        layout=None,
        layout_intent="comparison",
        title="t",
        bullets_left=["a"],
        bullets_right=["b"],
    )
    assert resolve_slide_layout_or_raise(s, 2) == "two_column"


def test_resolve_slide_for_chapter_break_and_title_only() -> None:
    s = Slide(layout=None, layout_intent="chapter_break", title="Chapter")
    assert resolve_slide_layout_or_raise(s, 3) == "section"


def test_suggest_slide_flags_intent_mismatch() -> None:
    slide = Slide(layout="title_content", title="Hi", layout_intent="opening")
    r = suggest_slide(slide, 1)
    assert r.intent_ok is False
    assert any("expects one of" in x for x in r.reasons)


def test_suggest_deck_runs() -> None:
    deck = Deck(title="T", slides=[Slide(layout="title", title="Cover")])
    rows = suggest_deck(deck)
    assert len(rows) == 1
    assert rows[0].aligned_with_content is True
