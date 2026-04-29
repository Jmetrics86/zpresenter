from pathlib import Path

from zpresenter.audience import Severity, analyze_deck
from zpresenter.models import AudienceProfile, Deck, Slide, SlideImage


def test_empty_deck_errors() -> None:
    finding = analyze_deck(Deck(title="X", slides=[]))[0]
    assert finding.severity == Severity.error


def test_first_slide_title_warning() -> None:
    deck = Deck(
        title="T",
        slides=[
            Slide(layout="section", title="Mid"),
            Slide(layout="title", title="Late"),
        ],
    )
    warns = [f for f in analyze_deck(deck) if f.severity == Severity.warn]
    assert any("Opening slide is not a title slide" in f.message for f in warns)


def test_missing_slide_image_warns_when_deck_path_known(tmp_path: Path) -> None:
    deck_file = tmp_path / "deck.json"
    deck = Deck(
        title="T",
        slides=[
            Slide(
                layout="title",
                title="Hi",
                images=[SlideImage(src="missing.png", placement="accent_corner")],
            ),
        ],
    )
    warns = [
        f for f in analyze_deck(deck, deck_path=deck_file) if "Missing image file" in f.message
    ]
    assert warns


def test_unknown_icon_title_warns() -> None:
    deck = Deck(
        title="T",
        slides=[
            Slide(layout="title", title="Hello", title_icon="not.a.real.id"),
        ],
    )
    warns = [f for f in analyze_deck(deck) if "Unknown icon" in f.message]
    assert warns


def test_executive_bullet_limit() -> None:
    deck = Deck(
        title="T",
        audience=AudienceProfile(technical_level="executive", attention_span="medium"),
        slides=[
            Slide(layout="title", title="T"),
            Slide(layout="title_content", title="Busy", bullets=[str(i) for i in range(8)]),
        ],
    )
    warns = [f for f in analyze_deck(deck) if "bullets" in f.message.lower()]
    assert warns
