"""Tests for AI deck generation helpers."""

from __future__ import annotations

from fastapi.testclient import TestClient

from zpresenter.ai_generate import build_generation_prompt, extract_json_for_deck
from zpresenter.models import Deck
from zpresenter.server import app


def test_extract_json_fence() -> None:
    raw = '```json\n{"title": "T", "slides": [{"layout": "title", "title": "X"}]}\n```'
    s = extract_json_for_deck(raw)
    d = Deck.model_validate_json(s)
    assert d.title == "T"
    assert len(d.slides) == 1


def test_extract_braces_with_prose() -> None:
    raw = 'Ok here:\n{"title": "U", "slides": [{"layout": "title", "title": "Y"}]} thanks'
    s = extract_json_for_deck(raw)
    d = Deck.model_validate_json(s)
    assert d.title == "U"


def test_build_generation_prompt_slide_count() -> None:
    p = build_generation_prompt(
        brief="hello world " * 5,
        slide_count=7,
        technical_level=None,
        attention_span=None,
    )
    assert "TARGET_SLIDE_COUNT: 7" in p


def test_build_generation_prompt_audience_hints() -> None:
    p = build_generation_prompt(
        brief="x" * 20,
        slide_count=5,
        technical_level="executive",
        attention_span="short",
    )
    assert 'technical_level should be "executive"' in p
    assert 'attention_span should be "short"' in p


def test_api_generate_requires_api_key() -> None:
    client = TestClient(app)
    r = client.post(
        "/api/decks/generate",
        json={"brief": "a" * 15, "slide_count": 5, "provider": "anthropic"},
    )
    assert r.status_code == 400
    assert "API key" in r.json()["detail"]
