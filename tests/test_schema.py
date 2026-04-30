from zpresenter.models import Deck, deck_json_schema


def test_deck_json_schema_roundtrip_documentation() -> None:
    schema = deck_json_schema()
    assert "$defs" in schema
    props = schema["properties"]
    assert "title" in props and "slides" in props


def test_sample_matches_exported_schema_structure() -> None:
    """Ensure schema generation stays aligned with Deck parsing."""
    schema = deck_json_schema()
    layout_prop = schema["$defs"]["Slide"]["properties"]["layout"]
    if "enum" in layout_prop:
        slide_enum = layout_prop["enum"]
    else:
        slide_enum = next(v["enum"] for v in layout_prop["anyOf"] if v.get("enum"))
    assert set(slide_enum) == {
        "title",
        "title_content",
        "section",
        "quote",
        "chart_bar",
        "chart_line",
        "two_column",
    }
    intent_prop = schema["$defs"]["Slide"]["properties"]["layout_intent"]
    intent_enum = next(v["enum"] for v in intent_prop["anyOf"] if v.get("enum"))
    assert set(intent_enum) == {
        "opening",
        "chapter_break",
        "narrative",
        "comparison",
        "metrics_bar",
        "metrics_trend",
        "pull_quote",
        "visual_emphasis",
    }
    deck = Deck.model_validate_json(
        '{"title": "T", "slides": [{"layout": "title", "title": "Hello"}]}'
    )
    assert deck.slides[0].layout == "title"


def test_intent_only_slide_materializes_layout() -> None:
    deck = Deck.model_validate_json(
        '{"title": "T", "slides": [{"layout_intent": "opening", "title": "Hi"}]}'
    )
    assert deck.slides[0].layout == "title"
