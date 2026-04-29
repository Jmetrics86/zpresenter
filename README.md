# zpresenter

Build **audience-aware** slide decks from structured **JSON**, validate pacing and density rules, and emit PowerPoint (`.pptx`) via [python-pptx](https://github.com/scanny/python-pptx).

## How it works

1. **Input** — A single **`Deck`** JSON file: metadata (`title`, `subtitle`, `author`, optional **`theme`** and **`audience`**), plus an ordered **`slides[]`** array. Each slide picks a **`layout`** and only the fields that layout understands (bullets, charts, images, icons, notes, etc.).
2. **Validation** — **`zpresenter check`** loads the deck with [Pydantic](https://docs.pydantic.dev/), runs layout rules (e.g. chart series lengths), optional **audience** heuristics (bullet count, pacing, missing assets), and icon/image warnings. Fix issues in JSON and re-run.
3. **Rendering** — **`zpresenter build`** resolves **paths relative to the deck JSON file’s directory** (and optional **`https`** image URLs), applies typography and chrome from **`src/zpresenter/slide_design.py`** (fonts, margins, accent bars, dividers), maps logical layouts to PowerPoint placeholders, and writes a `.pptx`.
4. **Deterministic output** — Given the same JSON and asset files, builds are repeatable. LLMs or humans only affect *what you put in the JSON*; the tool does not call cloud AI during `build`.

## Requirements

- [uv](https://docs.astral.sh/uv/)
- Python **3.12+** (see `.python-version`)

## Quick start

```bash
uv sync
uv run zpresenter check examples/sample.deck.json
uv run zpresenter build examples/sample.deck.json out/sample.pptx
```

Use **`schemas/deck.schema.json`** in your editor (`"$schema"` in example files) for completions and validation.

## Authoring workflow (best results)

These habits line up with how **`audience`** and the renderer behave:

| Practice | Why |
|----------|-----|
| **Start from a sample** | Copy **`examples/sample.deck.json`** or a file under **`examples/samples/`**, keep `"$schema"` pointing at the schema, then rename and trim. |
| **Set `audience` honestly** | **`technical_level`** (`executive` / `general` / `technical`) and **`attention_span`** (`short` / `medium` / `long`) tune **`check`** limits (bullet counts, section pacing hints). Mis-set audience ⇒ noisy or misleading warnings. |
| **Use `slides[0]` as `layout: "title"`** unless you intend otherwise — opening narrative matches executive expectations and avoids pacing warnings. |
| **Put detail in `notes`** | Body bullets stay short; nuance, timing, and backup stats belong in **`notes`** (speaker-only). Dense paragraphs on-slide fight the layout engine and readability. |
| **Break cadence with `section`** | Insert **`layout": "section"`** chapter slides every ~8–16 content slides ( **`check`** suggests when stretches get long). One strong title per section slide. |
| **Charts: align lengths** | **`chart_categories`** length must equal each **`chart_series[].values`** length. Prefer clear category labels (quarters, phases, weeks). |
| **Two-column: balance columns** | Fill **`bullets_left`** and **`bullets_right`** with comparable depth so the vertical divider and pacing feel intentional. |
| **Theme colors** | Set **`deck.theme`** (`primary_hex`, `accent_hex`, **`muted_hex`**) as **`RRGGBB`** without `#`. **`muted_hex`** improves subtitles and secondary lines; omitting it still yields sane defaults. |
| **Icons** | Use catalog IDs (`data.chart`, `security.lock`, …). Run **`zpresenter icons search …`** / **`icons list`**. Unknown IDs warn on **`check`**. Parallel **`bullet_icons`** must match **`bullets`** length when both exist. |
| **Images** | Put files beside the deck (e.g. **`examples/assets/`** for **`examples/sample.deck.json`**). Use **`placement`** appropriate to **`layout`** (see schema). Optional **`context`** documents intent for your team (not rendered). Run **`check`** with a real deck path so missing files are caught. |
| **Iterate with `check` before `build`** | Resolve **errors** (red); treat **warnings** as policy (build can proceed with **`--skip-check`** only when you accept the risk). |

**Using Cursor or other AI:** paste schema-backed JSON or samples into chat and ask for edits; paste **`check`** output when fixing issues. The repo does not embed API keys — authoring assistance uses your editor/tools; **`build`** stays offline aside from optional **`https`** image fetches.

## Deck JSON reference

### Deck-level

| Field | Role |
|-------|------|
| **`title`**, **`subtitle`**, **`author`** | Deck identity; **`title`** appears in PowerPoint properties. |
| **`theme`** | Optional **`primary_hex`**, **`accent_hex`**, **`muted_hex`** (`RRGGBB`) — accents for section headlines, accent bars, subtitles/captions. |
| **`audience`** | **`technical_level`**, **`attention_span`** — drives **`check`** heuristics. |
| **`slides`** | Ordered array of slide objects. |

### Slide layouts

| `layout` | Typical content |
|----------|------------------|
| **`title`** | Opening — **`title`**, optional **`subtitle`**. |
| **`section`** | Chapter marker — **`title`** only (often with **`title_color_hex`**). |
| **`title_content`** | **`title`** + **`bullets[]`**. |
| **`quote`** | **`quote`** (+ optional **`attribution`**); headline slot shows quote text. |
| **`chart_bar`** / **`chart_line`** | **`title`**, optional **`subtitle`**, **`chart_categories`**, **`chart_series[]`**. |
| **`two_column`** | **`title`**, **`bullets_left`**, **`bullets_right`**. |

Optional on many slides: **`notes`**, **`title_color_hex`**, **`title_icon`**, **`bullet_icons`** (parallel to **`bullets`**), **`bullets_left_icons`** / **`bullets_right_icons`**, **`images[]`**.

### Icons & images

- **Icons** — **`title_icon`** and parallel **`bullet_icons`** use semantic IDs from **`zpresenter icons`**. Prepends a glyph before visible text where supported.
- **Images** — Each **`images[]`** entry: **`src`** (path relative to the deck JSON directory, absolute path, or **`https`** URL), **`placement`** (must be allowed for that **`layout`** — see **`schemas/deck.schema.json`** / **`ALLOWED_IMAGE_PLACEMENTS`** in **`src/zpresenter/models.py`**), optional **`caption`**, optional **`context`** (authoring-only).

### Visual system

Rendering applies a consistent **Calibri** scale, charcoal body text, accent bars and hairlines under headlines on content/chart/two-column slides, section bands, a **two-column vertical divider**, and an optional footer rule on opening titles — see **`src/zpresenter/slide_design.py`**.

### Schema & regeneration

- **Schema:** **`schemas/deck.schema.json`** — regenerate after model changes with **`uv run zpresenter schema --out schemas/deck.schema.json`**.
- **Large showcases:** **`uv run python scripts/generate_sample_decks.py`** writes **`examples/samples/*.json`** and stamps **`deck.title`** and the opening title slide with **`YYYY-MM-DD HH:MM`**; it also refreshes **`examples/sample.deck.json`** the same way.

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
| `zpresenter icons list` | Show semantic icon IDs (optional `--category` / `-c`). |
| `zpresenter icons search <term>` | Search icons by id, category, or tag substring. |
| `zpresenter icons show <id>` | Print one catalog entry (e.g. `data.chart`). |

## Examples

| File | Notes |
|------|--------|
| `examples/sample.deck.json` | Minimal demo — icons + raster **`images`** under **`examples/assets/`** |
| `examples/samples/sample-product-launch-orbit.json` | Long SaaS/GTM narrative (~29 slides): charts, two-column, theme blues/greens |
| `examples/samples/sample-clinical-clear302.json` | Clinical/evidence storyline (~28 slides): efficacy/safety charts, dense splits |
| `examples/samples/sample-design-system-nova.json` | Design-system audit (~30 slides): accessibility + governance + palette charts |
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
