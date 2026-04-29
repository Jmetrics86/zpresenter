---
name: zpresenter-authoring
description: >-
  Authors structured decks for zpresenter — layouts, audience-aware density,
  speaker notes, and JSON deck conventions. Use when creating or editing
  presentations in this repo, slide content, layouts (title, section,
  title_content, quote), audience tuning, or running zpresenter CLI.
---

# ZPresenter authoring

## Deck contract

- Decks are **JSON** consumed by `zpresenter build` / `zpresenter check` (see `examples/sample.deck.json`).
- **JSON Schema** for validation and IntelliSense: `schemas/deck.schema.json` — regenerate with `uv run zpresenter schema --out schemas/deck.schema.json` after editing `Deck` / `Slide` / `AudienceProfile` in `src/zpresenter/models.py`.
- Example files include `"$schema": "../schemas/deck.schema.json"` so VS Code can validate against the workspace mapping in `.vscode/settings.json`.
- **`slides[0]`** should use `"layout": "title"` unless there is a deliberate reason not to.
- **`audience`** drives validation: `technical_level` (`executive` | `general` | `technical`) and `attention_span` (`short` | `medium` | `long`).
- Prefer **speaker notes** (`notes`) for detail; keep on-slide text sparse.

## Layouts

| `layout` | Use |
|----------|-----|
| `title` | Opening — `title`, optional `subtitle` |
| `section` | Chapter markers — single `title` |
| `title_content` | `title` + `bullets[]` |
| `quote` | `quote` text + optional `attribution` |

## Commands

Use uv: `uv run zpresenter check examples/sample.deck.json`, `uv run zpresenter build examples/sample.deck.json out/demo.pptx`.

Human-readable onboarding and CLI overview: **`README.md`**. Document inventory and audit trail: **`docs/AUDIT.md`**. Competitive landscape write-up: **`docs/RESEARCH.md`**.

Use **`zpresenter list-layouts`** or **`zpresenter list-layouts path/to/template.pptx`** to inspect slide master layout names (helps match branded themes).

After editing Python or deps: `uv sync`, then `uv run pytest`, `uv run ruff check src tests`.
