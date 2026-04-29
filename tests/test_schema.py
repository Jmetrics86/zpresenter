from zpresenter.models import Deck, deck_json_schema


def test_deck_json_schema_roundtrip_documentation() -> None:
    schema = deck_json_schema()
    assert "$defs" in schema
    props = schema["properties"]
    assert "title" in props and "slides" in props


def test_sample_matches_exported_schema_structure() -> None:
    """Ensure schema generation stays aligned with Deck parsing."""
    schema = deck_json_schema()
    slide_enum = schema["$defs"]["Slide"]["properties"]["layout"].get("enum")
    assert slide_enum == ["title", "title_content", "section", "quote"]
    deck = Deck.model_validate_json(
        '{"title": "T", "slides": [{"layout": "title", "title": "Hello"}]}'
    )
    assert deck.slides[0].layout == "title"
