"""Build PowerPoint decks from pydantic models."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import PP_PLACEHOLDER
from pptx.util import Pt

from zpresenter.layouts_pptx import layout_for
from zpresenter.models import Deck, Slide


def _set_notes(slide, text: str | None) -> None:
    if not text:
        return
    notes_frame = slide.notes_slide.notes_text_frame
    notes_frame.text = text


def _fill_title_placeholder(slide, title: str | None) -> None:
    if slide.shapes.title is not None and title is not None:
        slide.shapes.title.text = title


def _subtitle_placeholder(slide):
    for shape in slide.placeholders:
        if shape.placeholder_format.type == PP_PLACEHOLDER.SUBTITLE:
            return shape
    return None


def _body_placeholder(slide):
    for shape in slide.placeholders:
        t = shape.placeholder_format.type
        if t in (PP_PLACEHOLDER.BODY, PP_PLACEHOLDER.OBJECT):
            return shape
    return None


def _apply_slide(prs: Presentation, slide: Slide) -> None:
    layout = layout_for(slide.layout, prs)
    s = prs.slides.add_slide(layout)

    if slide.layout == "title":
        _fill_title_placeholder(s, slide.title or "")
        sub = _subtitle_placeholder(s)
        if sub is not None and slide.subtitle:
            sub.text = slide.subtitle
        _set_notes(s, slide.notes)
        return

    if slide.layout == "section":
        _fill_title_placeholder(s, slide.title or "")
        _set_notes(s, slide.notes)
        return

    if slide.layout == "quote":
        _fill_title_placeholder(s, slide.quote or slide.title or "")
        sub = _subtitle_placeholder(s)
        if sub is not None and slide.attribution:
            sub.text = slide.attribution
        _set_notes(s, slide.notes)
        return

    # title_content
    _fill_title_placeholder(s, slide.title or "")
    body = _body_placeholder(s)
    if body is not None and slide.bullets:
        tf = body.text_frame
        tf.clear()
        for i, bullet in enumerate(slide.bullets):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = bullet
            p.level = 0
            p.font.size = Pt(18)
    _set_notes(s, slide.notes)


def build_presentation(deck: Deck) -> Presentation:
    prs = Presentation()
    props = prs.core_properties
    props.title = deck.title
    props.subject = deck.subtitle or ""
    if deck.author:
        props.author = deck.author

    for slide in deck.slides:
        _apply_slide(prs, slide)

    return prs


def save_presentation(prs: Presentation, path: Path | str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(path))


def presentation_to_bytes(prs: Presentation) -> bytes:
    buf = BytesIO()
    prs.save(buf)
    return buf.getvalue()
