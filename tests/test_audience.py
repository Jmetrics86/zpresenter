from zpresenter.audience import Severity, analyze_deck
from zpresenter.models import AudienceProfile, Deck, Slide


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
