---
name: zpresenter-authoring
description: >-
  Authors structured decks for zpresenter — layouts (including charts and two-column),
  audience-aware density, speaker notes, deck theme hex accents, and JSON conventions.
  Use when creating or editing presentations in this repo, slide content,
  layouts (title, section, title_content, quote, chart_bar, chart_line, two_column),
  catalog icons (title_icon, bullet_icons), slide images (placement slots, paths),
  audience tuning, or running zpresenter CLI.
---

# ZPresenter authoring

## Deck contract

- Decks are **JSON** consumed by `zpresenter build` / `zpresenter check` (see `examples/sample.deck.json`).
- **JSON Schema** for validation and IntelliSense: `schemas/deck.schema.json` — regenerate with `uv run zpresenter schema --out schemas/deck.schema.json` after editing `Deck` / `Slide` / `AudienceProfile` in `src/zpresenter/models.py`.
- Example files include `"$schema"` pointing at `schemas/deck.schema.json` (paths differ: `examples/*.json` use `../schemas/…`; `examples/samples/*.json` use `../../schemas/…`).
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
| `chart_bar` / `chart_line` | `title`, optional `subtitle`, `chart_categories`, `chart_series[]` |
| `two_column` | `title`, `bullets_left`, `bullets_right` |

Optional **`deck.theme`** (`primary_hex`, `accent_hex`, **`muted_hex`**) and **`slide.title_color_hex`** (`RRGGBB`) tune accents and headline color.

## Visual layout

- **`src/zpresenter/slide_design.py`** defines the Calibri type scale, charcoal body copy, accent bars + hairlines under headlines, centered section bands, vertical divider between two-column bullets, footer hairline on opening titles, and quote attribution styling — applied automatically at **`build`**.

## Iconography

- Semantic catalog IDs (e.g. `data.chart`, `security.lock`) live in **`src/zpresenter/iconography/`**; builders prepend the resolved glyph to titles and bullets.
- Slide fields: **`title_icon`**; **`bullet_icons`** (same length as **`bullets`** when set); **`bullets_left_icons`** / **`bullets_right_icons`** (same lengths as the corresponding columns when set).
- CLI: **`zpresenter icons list`**, **`zpresenter icons search <term>`**, **`zpresenter icons show <id>`**. Unknown IDs surface as warnings from **`zpresenter check`**.

## Slide images

- **`slides[].images[]`**: **`src`** (path relative to the deck JSON file, or absolute / **https**), **`placement`** (layout-specific slot — see **`ALLOWED_IMAGE_PLACEMENTS`** in **`src/zpresenter/models.py`** and geometry in **`src/zpresenter/slide_image_layout.py`**), optional **`caption`** (small label under the raster), optional **`context`** (semantic tag for authors; not rendered).
- Put shared assets next to the deck (e.g. **`examples/assets/`** for **`examples/sample.deck.json`**). **`zpresenter check`** warns when a local file is missing if the check is run with a real deck path.

Rich showcases: **`examples/samples/*.json`** — regenerate via **`uv run python scripts/generate_sample_decks.py`**.

## Commands

Use uv: `uv run zpresenter check examples/sample.deck.json`, `uv run zpresenter build examples/sample.deck.json out/demo.pptx`.

Human-readable onboarding and CLI overview: **`README.md`**. Document inventory and audit trail: **`docs/AUDIT.md`**. Competitive landscape write-up: **`docs/RESEARCH.md`**.

Use **`zpresenter list-layouts`** or **`zpresenter list-layouts path/to/template.pptx`** to inspect slide master layout names (helps match branded themes).

After editing Python or deps: `uv sync`, then `uv run pytest`, `uv run ruff check src tests`.
