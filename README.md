# zpresenter

Build **audience-aware** slide decks from structured **JSON**, validate pacing and density rules, and emit PowerPoint (`.pptx`) via [python-pptx](https://github.com/scanny/python-pptx).

## How it works

1. **Input** — A single **`Deck`** JSON file: metadata (`title`, `subtitle`, `author`, optional **`theme`** and **`audience`**), plus **`slides[]`**. Each slide has a **`layout`** (explicit or **resolved** from **`layout_intent`** + body fields — Gamma-style minimal decks can omit **`layout`**; see **`examples/gamma-minimal.deck.json`**). Populate only the fields that slide type uses (bullets, charts, images, icons, notes, etc.).
2. **Validation** — **`zpresenter check`** loads the deck with [Pydantic](https://docs.pydantic.dev/), runs layout rules (e.g. chart series lengths), optional **audience** heuristics (bullet count, pacing, missing assets), and icon/image warnings. Fix issues in JSON and re-run.
3. **Rendering** — **`zpresenter build`** resolves **paths relative to the deck JSON file’s directory** (and optional **`https`** image URLs), applies typography and chrome from **`src/zpresenter/slide_design.py`** (fonts, margins, accent bars, dividers), maps logical layouts to PowerPoint placeholders, and writes a `.pptx`.
4. **Deterministic output** — Given the same JSON and asset files, **`zpresenter build`** is repeatable and stays offline (aside from optional **`https`** images). Optional **web UI** endpoints can stream LLM suggestions when you choose; they never change how **`build`** runs.

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
| **Use `slides[0]` as `layout: "title"` or `layout_intent: "opening"`** | Cover slides match executive expectations and pacing hints; **`opening`** resolves to **`title`** when **`layout`** is omitted. |
| **Put detail in `notes`** | Body bullets stay short; nuance, timing, and backup stats belong in **`notes`** (speaker-only). Dense paragraphs on-slide fight the layout engine and readability. |
| **Break cadence with `section`** | Insert **`layout": "section"`** chapter slides every ~8–16 content slides ( **`check`** suggests when stretches get long). One strong title per section slide. |
| **Charts: align lengths** | **`chart_categories`** length must equal each **`chart_series[].values`** length. Prefer clear category labels (quarters, phases, weeks). |
| **Two-column: balance columns** | Fill **`bullets_left`** and **`bullets_right`** with comparable depth so the vertical divider and pacing feel intentional. |
| **Theme colors** | Set **`deck.theme`** (`primary_hex`, `accent_hex`, **`muted_hex`**) as **`RRGGBB`** without `#`. **`muted_hex`** improves subtitles and secondary lines; omitting it still yields sane defaults. |
| **Icons** | Use catalog IDs (`data.chart`, `security.lock`, …). Run **`zpresenter icons search …`** / **`icons list`**. Unknown IDs warn on **`check`**. Parallel **`bullet_icons`** must match **`bullets`** length when both exist. |
| **Images** | Put files beside the deck (e.g. **`examples/assets/`** for **`examples/sample.deck.json`**). Use **`placement`** appropriate to **`layout`** (see schema). Optional **`context`** documents intent for your team (not rendered). Run **`check`** with a real deck path so missing files are caught. |
| **Iterate with `check` before `build`** | Resolve **errors** (red); treat **warnings** as policy (build can proceed with **`--skip-check`** only when you accept the risk). |

**Using Cursor or other AI:** paste schema-backed JSON or samples into chat and ask for edits; paste **`check`** output when fixing issues. The repo does not embed API keys — authoring assistance uses your editor/tools; **`build`** stays offline aside from optional **`https`** image fetches.

Optional **`layout_intent`** on each slide documents semantic goal for tooling and **`check`**; when **`layout`** is omitted, intent plus populated fields **determine** the resolved **`layout`** before **`build`**.

## Deck JSON reference

### Deck-level

| Field | Role |
|-------|------|
| **`title`**, **`subtitle`**, **`author`** | Deck identity; **`title`** appears in PowerPoint properties. |
| **`theme`** | Optional **`primary_hex`**, **`accent_hex`**, **`muted_hex`** (`RRGGBB`) — accents for section headlines, accent bars, subtitles/captions. |
| **`audience`** | **`technical_level`**, **`attention_span`** — drives **`check`** heuristics. |
| **`slides`** | Ordered array of slide objects. |

### Slide layouts

Each slide needs a concrete **`layout`** after parsing — either **set explicitly** or **resolved** from **`layout_intent`** (see **`layout_solver.resolve_slide_layout_or_raise`**). If **`layout_intent`** disagrees with what your bullets/chart/columns imply, validation fails until you align intent, fields, or **`layout`**.

| `layout` | Typical content |
|----------|------------------|
| **`title`** | Opening — **`title`**, optional **`subtitle`**. |
| **`section`** | Chapter marker — **`title`** only (often with **`title_color_hex`**). |
| **`title_content`** | **`title`** + **`bullets[]`**. |
| **`quote`** | **`quote`** (+ optional **`attribution`**); headline slot shows quote text. |
| **`chart_bar`** / **`chart_line`** | **`title`**, optional **`subtitle`**, **`chart_categories`**, **`chart_series[]`**. |
| **`two_column`** | **`title`**, **`bullets_left`**, **`bullets_right`**. |

Optional on many slides: **`layout_intent`** (semantic **`layout`** driver when **`layout`** omitted — see Gamma-style **`examples/gamma-minimal.deck.json`**), **`notes`**, **`title_color_hex`**, **`title_icon`**, **`bullet_icons`** (parallel to **`bullets`**), **`bullets_left_icons`** / **`bullets_right_icons`**, **`images[]`**.

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
| `zpresenter suggest-layout <deck.json>` | Heuristic layout suggestions from content + optional **`layout_intent`** (`--json` for machine-readable output). |
| `zpresenter build <deck.json> <out.pptx>` | Render `.pptx`; fails on audience **errors** unless `--skip-check`. Optional **`--template`** / **`-t`** branded `.pptx` for masters/theme. |
| `zpresenter validate-json <deck.json>` | Parse deck and print normalized JSON. |
| `zpresenter schema` | Print JSON Schema for `Deck` (stdout). |
| `zpresenter schema --out schemas/deck.schema.json` | Write schema file (after model changes). |
| `zpresenter list-layouts` | List slide masters / layout names from the built-in blank theme. |
| `zpresenter list-layouts template.pptx` | Inspect masters and layouts from an existing `.pptx` (e.g. branded template). |
| `zpresenter icons list` | Show semantic icon IDs (optional `--category` / `-c`). |
| `zpresenter icons search <term>` | Search icons by id, category, or tag substring. |
| `zpresenter icons show <id>` | Print one catalog entry (e.g. `data.chart`). |
| `zpresenter serve` | Start FastAPI + built React UI (default http://127.0.0.1:8000). Use **`--reload`** for API hot reload; pair with **`npm run dev`** in `webapp/` for Vite HMR (see **`docs/WEBAPP.md`**). |

## Examples

### Minimal / reference

| File | Notes |
|------|--------|
| `examples/gamma-minimal.deck.json` | **Intent-first** — `layout` omitted; `layout_intent` + fields resolve before `build`. Simplest way to author. |
| `examples/sample.deck.json` | Minimal demo — icons + raster `images` under `examples/assets/`. |

### 20-slide showcase decks (all layouts · images · iconography)

Run `uv run python scripts/generate_20slide_samples.py` to regenerate.

| File | Theme | Audience |
|------|-------|----------|
| `examples/samples/sample-apex-strategy-2026.json` | Navy / amber — executive market strategy | executive / short |
| `examples/samples/sample-meridian-platform-2026.json` | Charcoal / emerald — engineering platform review | technical / long |
| `examples/samples/sample-nova-launch-2026.json` | Indigo / pink — product launch GTM | general / medium |

### Original showcase decks (~28–30 slides)

Run `uv run python scripts/generate_sample_decks.py` to regenerate.

| File | Notes |
|------|--------|
| `examples/samples/sample-product-launch-orbit.json` | SaaS/GTM narrative: charts, two-column, blues/greens |
| `examples/samples/sample-clinical-clear302.json` | Clinical/evidence: efficacy/safety charts, dense splits |
| `examples/samples/sample-design-system-nova.json` | Design-system audit: accessibility + governance + palette charts |

### Compact examples

| File | Notes |
|------|--------|
| `examples/dummy-board-strategy.json` | Executive / short attention |
| `examples/dummy-platform-architecture.json` | Technical / long attention |
| `examples/dummy-team-workshop.json` | General / medium |

## Web UI (card-based, Gamma-style)

zpresenter ships a browser UI with live card previews and PPTX export — no `.pptx` file needed to author.

```bash
uv sync                                    # FastAPI + uvicorn are already project deps
cd webapp && npm install && npm run build && cd ..
uv run zpresenter serve                   # opens browser → http://127.0.0.1:8000
```

Optional LLM SDKs (only if you use AI improver / AI deck generation): `uv add anthropic`, `uv add openai`, or `uv add google-generativeai` — same as **`AI slide improvement`** below.

| Area | What it does |
|------|----------------|
| **Load** tab | Paste Deck JSON · pick an example · **AI deck generation** (outline → streamed JSON → Apply) · **Load Deck** · validation findings |
| **Slides** tab | Thumbnail strip — jump to any slide |
| **Main canvas** | Current slide as a 16:9 card (title, section, bullets, two-column, chart, quote) |
| **Overview** | Press **O** for a Slidev-style grid; pick a slide or **Esc** to close |
| **Present mode** | **F** or the Present button — fullscreen; **Esc** exits |
| **AI Improve** | **I** toggles per-slide streaming edits (needs API key — see below) |
| **Export PPTX** | Downloads `.pptx` from the same validated JSON |

Dev mode: `uv run zpresenter serve --reload` in one terminal, `cd webapp && npm run dev` in another → http://localhost:5173 (proxies `/api` to port 8000).

See **`docs/WEBAPP.md`** for the full setup guide and API reference.

### Docker (optional)

```bash
docker compose build
docker compose up
```

Open http://localhost:8000 . The image includes the production React build and all three optional AI SDKs. Configure API keys via a `.env` file next to `docker-compose.yml` and uncomment the `env_file` block in `docker-compose.yml`, or pass `-e ANTHROPIC_API_KEY=…` (etc.) when running the container.

## AI features (slide improvement & deck generation)

The web UI can call Anthropic (Claude), OpenAI (GPT-4o / o1), or Google Gemini when you provide keys: **AI Improve** (**`I`**) refines one slide at a time; **AI deck generation** on the **Load** tab builds a full Deck from an outline (see below). Neither affects **`zpresenter build`** unless you paste or export the resulting JSON.

### Preferred method: `.env` file (server-side, most secure)

Create a `.env` file **in the project root** (same folder as `pyproject.toml`). Add only the key for the provider you use:

```bash
# .env  — never commit this file
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIza...
```

> **`.env` is already listed in `.gitignore`** — it will not be committed accidentally.

Start the server normally:

```bash
uv run zpresenter serve
```

The server reads `.env` automatically (via python-dotenv, bundled with uvicorn). A green dot appears next to the provider name in the AI panel confirming the key is active — no key entry needed in the browser.

### Alternative: environment variable in your shell

Set the key in the terminal before starting the server. The key exists only for the lifetime of that shell session:

```bash
# macOS / Linux
export ANTHROPIC_API_KEY="sk-ant-..."
uv run zpresenter serve

# Windows PowerShell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
uv run zpresenter serve
```

### Browser-only fallback (key never sent to disk)

If you cannot or prefer not to configure the server, enter your API key directly in the AI panel in the browser. It is stored only in that browser's `localStorage`, never written to any file on disk, and sent to the server only inside the encrypted HTTPS/localhost POST request body for that session.

Click **save** in the panel after entering the key — it persists across page refreshes in that browser.

### Which provider should I install?

Install only the SDK for the provider whose key you have:

```bash
uv add anthropic             # Claude Sonnet / Opus
uv add openai                # GPT-4o / o1
uv add google-generativeai   # Gemini Flash / Pro
```

### AI deck generation (full outline → JSON)

On the web UI **Load** tab, expand **AI deck generation**: paste a topic or outline, set slide count (3–35), optional audience hints, then **Generate**. When streaming finishes, **Apply deck** runs the same validation as **Load Deck**. The API endpoint is `POST /api/decks/generate` (SSE — same event framing as slide improvement).

### Security checklist

| ✅ Do | ❌ Don't |
|-------|---------|
| Use a `.env` file in the project root | Hard-code the key in any `.json`, `.py`, or `.ts` source file |
| Add `.env` to `.gitignore` (already done) | Commit `.env` or any file containing a bare key |
| Use a **restricted** key scoped to this project | Reuse your personal "master" API key |
| Rotate the key if you suspect leakage | Share the key over Slack, email, or chat |
| Prefer `ANTHROPIC_API_KEY` in `.env` over browser storage for shared machines | Leave the browser localStorage key active on a shared or public computer |

## Development

```bash
uv run pytest
uv run ruff check src tests
```

| Doc | Contents |
|-----|----------|
| `docs/WEBAPP.md` | Web UI setup, dev mode, API reference |
| `docs/PRESENTATION_EVOLUTION.md` | Architecture roadmap — PPTX wall, intent-first authoring, Gamma-lite phases |
| `docs/RESEARCH.md` | Comparable tools (Markdown stacks, SaaS APIs, libraries) and positioning |
| `docs/AUDIT.md` | Document inventory, findings, and remediation history |
