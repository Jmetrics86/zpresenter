"""Structured deck models — single source of truth for layouts and content."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

TechnicalLevel = Literal["executive", "general", "technical"]
AttentionSpan = Literal["short", "medium", "long"]
SlideLayoutKind = Literal["title", "title_content", "section", "quote"]


class AudienceProfile(BaseModel):
    """Hints for validation and density — tune messaging for the room."""

    technical_level: TechnicalLevel = "general"
    attention_span: AttentionSpan = "medium"


class Slide(BaseModel):
    """One slide with layout-specific optional fields."""

    layout: SlideLayoutKind
    title: str | None = None
    subtitle: str | None = None
    bullets: list[str] | None = None
    quote: str | None = None
    attribution: str | None = None
    notes: str | None = None


class Deck(BaseModel):
    """Full presentation."""

    title: str = Field(min_length=1)
    subtitle: str | None = None
    author: str | None = None
    audience: AudienceProfile = Field(default_factory=AudienceProfile)
    slides: list[Slide] = Field(default_factory=list)


def parse_deck_json(data: str | bytes) -> Deck:
    return Deck.model_validate_json(data)


def deck_json_schema() -> dict[str, Any]:
    """JSON Schema for deck documents (serialization shape). Keep `schemas/` in sync when models change."""
    return Deck.model_json_schema(mode="serialization")
