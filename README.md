# zpresenter

Build **audience-aware** slide decks from structured **JSON**, validate pacing and density rules, and emit PowerPoint (`.pptx`) via [python-pptx](https://github.com/scanny/python-pptx).

## Requirements

- [uv](https://docs.astral.sh/uv/)
- Python **3.12+** (see `.python-version`)

## Quick start

```bash
uv sync
uv run zpresenter check examples/sample.deck.json
uv run zpresenter build examples/sample.deck.json out/sample.pptx
```

## CLI

| Command | Purpose |
|---------|---------|
| `zpresenter check <deck.json>` | Run audience / pacing checks (exit non-zero on warnings/errors depending on severity). |
| `zpresenter build <deck.json> <out.pptx>` | Render `.pptx`; fails on audience **errors** unless `--skip-check`. |
| `zpresenter validate-json <deck.json>` | Parse deck and print normalized JSON. |
| `zpresenter schema` | Print JSON Schema for `Deck` (stdout). |
| `zpresenter schema --out schemas/deck.schema.json` | Write schema file (after model changes). |
| `zpresenter list-layouts` | List slide masters / layout names from the built-in blank theme. |
| `zpresenter list-layouts template.pptx` | Inspect masters and layouts from an existing `.pptx` (e.g. branded template). |

## Deck format

- Logical layouts: `title`, `section`, `title_content`, `quote`.
- Optional `audience`: `technical_level` (`executive` \| `general` \| `technical`), `attention_span` (`short` \| `medium` \| `long`).
- Prefer **`notes`** for speaker-only detail.

Committed schema for editors and tooling: **`schemas/deck.schema.json`**. Example decks reference it via `"$schema": "../schemas/deck.schema.json"`.

## Examples

| File | Notes |
|------|--------|
| `examples/sample.deck.json` | Minimal demo |
| `examples/dummy-board-strategy.json` | Executive / short attention |
| `examples/dummy-platform-architecture.json` | Technical / long attention |
| `examples/dummy-team-workshop.json` | General / medium |

## Development

```bash
uv run pytest
uv run ruff check src tests
```

See **`docs/AUDIT.md`** for a document inventory, findings, and remediation history.

See **`docs/RESEARCH.md`** for comparable tools (Markdown stacks, SaaS APIs, libraries) and positioning notes.
