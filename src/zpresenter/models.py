"""Structured deck models — single source of truth for layouts and content."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

TechnicalLevel = Literal["executive", "general", "technical"]
AttentionSpan = Literal["short", "medium", "long"]
SlideLayoutKind = Literal[
    "title",
    "title_content",
    "section",
    "quote",
    "chart_bar",
    "chart_line",
    "two_column",
]

ImagePlacement = Literal[
    "primary_right",
    "primary_below",
    "accent_corner",
    "banner_lower",
    "two_column_span_below",
]


ALLOWED_IMAGE_PLACEMENTS: dict[SlideLayoutKind, frozenset[ImagePlacement]] = {
    "title": frozenset({"accent_corner", "banner_lower"}),
    "section": frozenset({"accent_corner", "banner_lower"}),
    "title_content": frozenset(
        {"primary_right", "primary_below", "accent_corner", "banner_lower"}
    ),
    "quote": frozenset({"primary_below", "accent_corner", "banner_lower"}),
    "chart_bar": frozenset({"accent_corner", "banner_lower", "primary_below"}),
    "chart_line": frozenset({"accent_corner", "banner_lower", "primary_below"}),
    "two_column": frozenset({"accent_corner", "banner_lower", "two_column_span_below"}),
}


class DeckTheme(BaseModel):
    """Optional hex accents — applied to section titles and slides that opt in."""

    primary_hex: str | None = Field(None, description="RRGGBB section title accent")
    accent_hex: str | None = Field(None, description="RRGGBB secondary accent")
    muted_hex: str | None = Field(
        None,
        description="RRGGBB for subtitles, captions, and secondary lines (defaults to slate if omitted).",
    )


class AudienceProfile(BaseModel):
    """Hints for validation and density — tune messaging for the room."""

    technical_level: TechnicalLevel = "general"
    attention_span: AttentionSpan = "medium"


class ChartSeries(BaseModel):
    """One named series aligned by index with chart_categories."""

    name: str = Field(min_length=1)
    values: list[float] = Field(min_length=1)


class SlideImage(BaseModel):
    """Raster image referenced by path (relative to deck JSON dir), absolute path, or https URL."""

    src: str = Field(min_length=1)
    placement: ImagePlacement = "primary_right"
    caption: str | None = None
    context: str | None = Field(
        None,
        description="Optional semantic hint for authoring or tooling (not shown on-slide).",
    )


class Slide(BaseModel):
    """One slide with layout-specific optional fields."""

    layout: SlideLayoutKind
    title: str | None = None
    subtitle: str | None = None
    bullets: list[str] | None = None
    bullets_left: list[str] | None = None
    bullets_right: list[str] | None = None
    quote: str | None = None
    attribution: str | None = None
    chart_categories: list[str] | None = None
    chart_series: list[ChartSeries] | None = None
    notes: str | None = None
    title_color_hex: str | None = Field(None, description="Optional RRGGBB for slide headline")
    title_icon: str | None = Field(
        None,
        description="Catalog icon id prepended to titles where supported (see zpresenter icons list).",
    )
    bullet_icons: list[str | None] | None = Field(
        None,
        description="Parallel to bullets — catalog icon id or null per bullet.",
    )
    bullets_left_icons: list[str | None] | None = None
    bullets_right_icons: list[str | None] | None = None
    images: list[SlideImage] | None = Field(
        None,
        description="Embedded images — placement selects on-slide slot for this layout.",
    )

    @model_validator(mode="after")
    def _align_icon_lists(self) -> Slide:
        if self.bullets is not None and self.bullet_icons is not None:
            if len(self.bullet_icons) != len(self.bullets):
                raise ValueError("bullet_icons must match bullets length when both are set.")
        if self.bullets_left is not None and self.bullets_left_icons is not None:
            if len(self.bullets_left_icons) != len(self.bullets_left):
                raise ValueError("bullets_left_icons must match bullets_left length.")
        if self.bullets_right is not None and self.bullets_right_icons is not None:
            if len(self.bullets_right_icons) != len(self.bullets_right):
                raise ValueError("bullets_right_icons must match bullets_right length.")
        return self

    @model_validator(mode="after")
    def _validate_slide_images(self) -> Slide:
        imgs = self.images or []
        allowed = ALLOWED_IMAGE_PLACEMENTS[self.layout]
        for img in imgs:
            if img.placement not in allowed:
                ok = ", ".join(sorted(allowed))
                raise ValueError(
                    f'Image placement "{img.placement}" is not valid for layout "{self.layout}". '
                    f"Allowed: {ok}"
                )
        if self.layout == "title_content":
            ps = {img.placement for img in imgs}
            if "primary_right" in ps and "primary_below" in ps:
                raise ValueError(
                    'title_content slides cannot combine "primary_right" and "primary_below" images.'
                )
        return self


class Deck(BaseModel):
    """Full presentation."""

    title: str = Field(min_length=1)
    subtitle: str | None = None
    author: str | None = None
    audience: AudienceProfile = Field(default_factory=AudienceProfile)
    theme: DeckTheme | None = None
    slides: list[Slide] = Field(default_factory=list)


def parse_deck_json(data: str | bytes) -> Deck:
    return Deck.model_validate_json(data)


def deck_json_schema() -> dict[str, Any]:
    """JSON Schema for deck documents (serialization shape). Keep `schemas/` in sync when models change."""
    return Deck.model_json_schema(mode="serialization")
