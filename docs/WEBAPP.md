# zpresenter Web UI

Card-based presentation editor with live preview and PPTX export — like Gamma, backed by the same `Deck` JSON schema.

## Architecture

```
Browser (React + Tailwind + Recharts)
       ↕  /api/*
FastAPI (Python) — wraps zpresenter core models/builder
       ↓  POST /api/decks/export-pptx
python-pptx  →  .pptx download
```

The JSON Deck format is unchanged. You can author in JSON, preview as rich cards in the browser, then export to PowerPoint at any time.

## Setup

### 1 — Python web extras

```bash
uv add fastapi 'uvicorn[standard]'
# or via the optional group:
uv sync --extra web
```

### 2 — Build the React frontend

```bash
cd webapp
npm install
npm run build      # outputs webapp/dist/
```

### 3 — Start

```bash
uv run zpresenter serve
# Opens http://127.0.0.1:8000 automatically
```

## Development mode (hot reload)

Run both servers in separate terminals:

```bash
# Terminal 1 — Python API with auto-reload
uv run zpresenter serve --reload

# Terminal 2 — Vite dev server (React + hot module replacement)
cd webapp && npm run dev
# → http://localhost:5173  (proxies /api to :8000)
```

## UI overview

| Area | Function |
|------|----------|
| **Top bar** | Deck title · Present (fullscreen) · Export PPTX |
| **Left sidebar → Load** | Paste Deck JSON · **AI deck generation** (outline → streaming JSON) · pick an example · validation findings |
| **Left sidebar → Slides** | Thumbnail strip — click to jump to any slide |
| **Main canvas** | Current slide card (16:9, shadow, theme-colored) |
| **Speaker notes** | Shown below card (hidden in present mode) |

### Keyboard shortcuts

| Key | Action |
|-----|--------|
| `←` / `↑` | Previous slide |
| `→` / `↓` | Next slide |
| `F` | Enter present mode (fullscreen) |
| `Esc` | Exit present mode |

## Card layouts

Each Deck layout renders as a styled card:

| layout | Card style |
|--------|-----------|
| `title` | Accent top band · large centered title · subtitle · footer rule |
| `section` | Centered chapter title · accent stub · hairline |
| `title_content` | Title with accent underline · bullet list with icons |
| `two_column` | Title · two equal columns with divider |
| `quote` | Accent left bar · large italic quote · right-aligned attribution |
| `chart_bar` / `chart_line` | Recharts bar or line chart with full series + legend |

## API reference

All endpoints accept/return JSON. The Python FastAPI interactive docs are at `/api/docs`.

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/health` | Liveness check |
| `GET` | `/api/schema` | JSON Schema for Deck |
| `GET` | `/api/icons` | Full icon catalog |
| `GET` | `/api/examples` | List built-in example filenames |
| `GET` | `/api/examples/{path}` | Return raw example JSON |
| `POST` | `/api/decks/validate` | Validate + materialize layouts → findings |
| `POST` | `/api/decks/export-pptx` | Return `.pptx` file download |
| `POST` | `/api/decks/generate` | **SSE** — stream full Deck JSON from a topic brief (`brief`, `slide_count`, optional `technical_level` / `attention_span`, `provider`, `model`, `api_key`). Same event shape as slide improve (`delta` / `done` / `error`). |
| `POST` | `/api/slides/improve` | **SSE** — stream improved slide JSON for one slide |
| `GET` | `/api/models` | Providers, default models, env var names, server key status |

## Production deployment

After `npm run build`, `webapp/dist/` is served as static files by FastAPI at `/`.
No separate web server needed — `zpresenter serve` handles everything.

### Docker image

From the repository root:

```bash
docker compose build
docker compose up
```

Browse to http://localhost:8000 . The Dockerfile installs optional Anthropic, OpenAI, and Gemini SDKs so slide improvement and deck generation both work inside the container. Pass API keys via `.env` (uncomment `env_file` in `docker-compose.yml`) or `docker run -e …`.
