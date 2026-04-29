"""Pydantic deck / slide validation."""

import pytest
from pydantic import ValidationError

from zpresenter.models import Slide, SlideImage


def test_title_slide_image_placement_must_match_layout() -> None:
    with pytest.raises(ValidationError):
        Slide(
            layout="title",
            title="x",
            images=[SlideImage(src="a.png", placement="primary_right")],
        )


def test_bullet_icons_length_must_match_bullets() -> None:
    with pytest.raises(ValidationError):
        Slide(
            layout="title_content",
            title="T",
            bullets=["a", "b"],
            bullet_icons=["data.chart"],
        )


def test_bullets_left_icons_length_must_match() -> None:
    with pytest.raises(ValidationError):
        Slide(
            layout="two_column",
            title="T",
            bullets_left=["x"],
            bullets_right=["y"],
            bullets_left_icons=[None, None],
        )
