from pptx import Presentation
from typer.testing import CliRunner

from zpresenter.cli import app
from zpresenter.template_inspect import SlideLayoutRow, describe_slide_layouts


def test_describe_blank_theme_layouts() -> None:
    rows = describe_slide_layouts(Presentation())
    assert len(rows) >= 1
    assert all(isinstance(r, SlideLayoutRow) for r in rows)
    assert rows[0].name


def test_list_layouts_cli_smoke() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["list-layouts"])
    assert result.exit_code == 0
    combined = (result.stdout or "") + (result.stderr or "")
    assert "layout" in combined.lower()
