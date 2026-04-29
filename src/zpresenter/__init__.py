"""Audience-aware presentation builder."""

from zpresenter.models import AudienceProfile, ChartSeries, Deck, DeckTheme, Slide, parse_deck_json

__all__ = [
    "AudienceProfile",
    "ChartSeries",
    "Deck",
    "DeckTheme",
    "Slide",
    "__version__",
    "parse_deck_json",
]
__version__ = "0.1.0"
