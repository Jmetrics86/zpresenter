"""CLI — build `.pptx` from JSON decks and run audience checks."""

from __future__ import annotations

import json
from pathlib import Path

import typer
from pptx import Presentation
from rich.console import Console
from rich.table import Table

from zpresenter.audience import Severity, analyze_deck, summarize_findings
from zpresenter.builder import build_presentation, save_presentation
from zpresenter.models import Deck, deck_json_schema, parse_deck_json
from zpresenter.template_inspect import describe_slide_layouts

app = typer.Typer(
    no_args_is_help=True,
    help="Build audience-aware presentations from structured decks.",
)
console = Console()


def _load_deck(deck_path: Path) -> Deck:
    """Parse deck JSON from disk."""
    return parse_deck_json(deck_path.read_text(encoding="utf-8"))


@app.command("check")
def check_command(
    deck_path: Path = typer.Argument(..., exists=True, readable=True, help="Path to deck JSON"),
) -> None:
    """Analyze a deck JSON for clarity and pacing issues."""
    deck = _load_deck(deck_path)
    findings = analyze_deck(deck)
    err, warn, info = summarize_findings(findings)
    console.print(f"[bold]{deck.title}[/bold] - findings: error={err}, warn={warn}, info={info}\n")

    if not findings:
        console.print("[green]No issues reported.[/green]")
        raise typer.Exit(0)

    table = Table(show_header=True)
    table.add_column("Sev", style="bold")
    table.add_column("#")
    table.add_column("Message")
    table.add_column("Suggestion")

    sev_style = {
        Severity.error: "red",
        Severity.warn: "yellow",
        Severity.info: "cyan",
    }

    for f in findings:
        idx = "" if f.slide_index is None else str(f.slide_index + 1)
        style = sev_style[f.severity]
        table.add_row(f"[{style}]{f.severity.value}[/{style}]", idx, f.message, f.suggestion or "")

    console.print(table)

    if err > 0:
        raise typer.Exit(code=2)
    raise typer.Exit(code=1 if warn > 0 else 0)


@app.command("build")
def build_command(
    deck_path: Path = typer.Argument(..., exists=True, readable=True, help="Path to deck JSON"),
    out_path: Path = typer.Argument(..., help="Output path for `.pptx`"),
    skip_check: bool = typer.Option(
        False, "--skip-check", help="Do not fail when audience checks report errors."
    ),
) -> None:
    """Render deck JSON to a PowerPoint file."""
    deck = _load_deck(deck_path)

    findings = analyze_deck(deck)
    err, warn, _info = summarize_findings(findings)
    if err > 0 and not skip_check:
        console.print(
            f"[red]Audience checks reported {err} error(s).[/red] Run `zpresenter check {deck_path}` or pass `--skip-check`."
        )
        raise typer.Exit(code=2)
    if warn > 0:
        console.print(f"[yellow]Warning:[/yellow] {warn} audience warning(s); continuing.")

    prs = build_presentation(deck)
    save_presentation(prs, out_path)
    console.print(f"[green]Wrote[/green] {out_path.resolve()}")


@app.command("schema")
def schema_command(
    out: Path | None = typer.Option(
        None,
        "--out",
        "-o",
        help="Write JSON Schema to this path instead of printing to stdout.",
    ),
) -> None:
    """Emit JSON Schema for the Deck document (for editors and CI validation)."""
    schema = deck_json_schema()
    text = json.dumps(schema, indent=2, ensure_ascii=False) + "\n"
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        console.print(f"[green]Wrote[/green] {out.resolve()}")
        raise typer.Exit(0)
    typer.echo(text, nl=False)


@app.command("validate-json")
def validate_json(deck_path: Path = typer.Argument(..., exists=True, readable=True)) -> None:
    """Verify deck JSON parses; prints normalized summary."""
    deck = _load_deck(deck_path)
    console.print(json.dumps(deck.model_dump(mode="json"), indent=2))


@app.command("list-layouts")
def list_layouts_command(
    template: Path | None = typer.Argument(
        None,
        help="Optional .pptx file whose masters/layouts to list (omit for built-in blank theme).",
    ),
) -> None:
    """List slide masters and layout names — inspect branding templates or debug layout keywords."""
    if template is not None:
        if not template.is_file():
            console.print(f"[red]Not found:[/red] {template}")
            raise typer.Exit(1)
        prs = Presentation(str(template))
        label = str(template.resolve())
    else:
        prs = Presentation()
        label = "(python-pptx default blank theme)"

    rows = describe_slide_layouts(prs)
    console.print(f"[bold]Layouts[/bold] - {label}\n")
    table = Table(show_header=True)
    table.add_column("Master", style="bold")
    table.add_column("Idx")
    table.add_column("Layout name")
    for r in rows:
        table.add_row(str(r.master_index), str(r.layout_index), r.name)
    console.print(table)
    master_ct = len(prs.slide_masters)
    console.print(f"\n[dim]{len(rows)} layout(s) across {master_ct} master(s)[/dim]")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
