"""Icon catalog helpers."""

from zpresenter.iconography import resolve_icon, search_icons


def test_resolve_known_id() -> None:
    assert resolve_icon("status.success") == "\u2713"


def test_resolve_unknown_returns_none() -> None:
    assert resolve_icon("not.in.catalog") is None
    assert resolve_icon(None) is None
    assert resolve_icon("") is None


def test_search_finds_tags() -> None:
    ids = search_icons("kpi")
    assert "data.chart" in ids
