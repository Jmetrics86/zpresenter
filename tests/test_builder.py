from io import BytesIO

from pptx import Presentation

from zpresenter.builder import build_presentation, presentation_to_bytes
from zpresenter.models import Deck, Slide


def test_build_roundtrip_slide_count() -> None:
    deck = Deck(
        title="Deck title",
        subtitle="Sub",
        slides=[
            Slide(layout="title", title="Hello", subtitle="World"),
            Slide(layout="title_content", title="Agenda", bullets=["One", "Two"]),
        ],
    )
    raw = presentation_to_bytes(build_presentation(deck))
    prs = Presentation(BytesIO(raw))
    assert len(prs.slides) == 2
    assert prs.core_properties.title == "Deck title"
