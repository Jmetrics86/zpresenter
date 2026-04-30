"""FastAPI server — card-based presentation UI with PPTX export."""

from __future__ import annotations

import io
import json
import os
from pathlib import Path
from typing import Any, Literal

# Load .env from the repo root automatically so developers can store API keys
# there without setting shell environment variables manually.
try:
    from dotenv import load_dotenv  # type: ignore[import-untyped]

    _env_file = Path(__file__).resolve().parents[2] / ".env"
    if _env_file.is_file():
        load_dotenv(dotenv_path=_env_file, override=False)
except ImportError:
    pass  # python-dotenv not installed — env vars must be set in the shell

from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, ValidationError

from zpresenter.audience import analyze_deck, summarize_findings
from zpresenter.builder import build_presentation, presentation_to_bytes
from zpresenter.iconography import describe_icon, list_icon_ids
from zpresenter.models import Deck, deck_json_schema

app = FastAPI(title="zpresenter", version="0.2.0", docs_url="/api/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_REPO_ROOT = Path(__file__).resolve().parents[2]
_EXAMPLES_DIR = _REPO_ROOT / "examples"
_UI_DIST = _REPO_ROOT / "webapp" / "dist"


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/schema")
def api_schema() -> dict[str, Any]:
    return deck_json_schema()


@app.get("/api/icons")
def api_icons() -> list[dict[str, Any]]:
    return [{"id": iid, **meta} for iid in list_icon_ids() if (meta := describe_icon(iid))]


@app.get("/api/examples")
def api_examples() -> list[str]:
    out: list[str] = []
    if not _EXAMPLES_DIR.exists():
        return out
    for p in sorted(_EXAMPLES_DIR.glob("*.json")):
        out.append(p.name)
    samples = _EXAMPLES_DIR / "samples"
    if samples.exists():
        for p in sorted(samples.glob("*.json")):
            out.append(f"samples/{p.name}")
    return out


@app.get("/api/examples/{path:path}")
def api_load_example(path: str) -> dict[str, Any]:
    target = (_EXAMPLES_DIR / path).resolve()
    examples_root = _EXAMPLES_DIR.resolve()
    if not target.is_file() or examples_root not in target.parents and target.parent != examples_root:
        raise HTTPException(404, "Example not found")
    return json.loads(target.read_text(encoding="utf-8"))


@app.post("/api/decks/validate")
def api_validate(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    try:
        deck = Deck.model_validate(body)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc
    findings = analyze_deck(deck)
    err, warn, info = summarize_findings(findings)
    return {
        "deck": deck.model_dump(mode="json"),
        "findings": [f.model_dump() for f in findings],
        "summary": {"errors": err, "warnings": warn, "info": info},
    }


@app.post("/api/decks/export-pptx")
def api_export_pptx(body: dict[str, Any] = Body(...)) -> StreamingResponse:
    try:
        deck = Deck.model_validate(body)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc
    prs_bytes = presentation_to_bytes(build_presentation(deck))
    safe = "".join(c if c.isalnum() or c in " _-" else "_" for c in deck.title)[:48].strip()
    filename = f"{safe or 'deck'}.pptx"
    return StreamingResponse(
        io.BytesIO(prs_bytes),
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ---------------------------------------------------------------------------
# AI slide improvement — streaming SSE endpoint
# ---------------------------------------------------------------------------

class ImproveRequest(BaseModel):
    deck: dict[str, Any]
    slide_index: int
    instructions: str = ""
    provider: Literal["anthropic", "openai", "gemini"] = "anthropic"
    model: str = ""
    api_key: str = ""


@app.post("/api/slides/improve")
async def api_improve_slide(body: ImproveRequest) -> StreamingResponse:
    """Stream LLM-improved slide JSON as Server-Sent Events.

    Events
    ------
    ``{"type": "delta", "text": "..."}``   — incremental token
    ``{"type": "done", "buffer": "..."}``  — complete accumulated text
    ``{"type": "error", "message": "..."}`` — error; stream ends
    """
    from zpresenter.ai_improve import resolve_api_key, stream_improvement  # noqa: PLC0415

    try:
        deck = Deck.model_validate(body.deck)
    except ValidationError as exc:
        raise HTTPException(422, detail=exc.errors()) from exc

    if not (0 <= body.slide_index < len(deck.slides)):
        raise HTTPException(
            400,
            f"slide_index {body.slide_index} out of range 0–{len(deck.slides) - 1}.",
        )

    slide = deck.slides[body.slide_index]
    api_key = resolve_api_key(body.provider, body.api_key)
    if not api_key:
        from zpresenter.ai_improve import _PROVIDER_ENV  # noqa: PLC0415
        env_name = _PROVIDER_ENV.get(body.provider, "API_KEY")
        raise HTTPException(
            400,
            f"No API key for provider '{body.provider}'. "
            f"Pass api_key in the request body or set the {env_name} environment variable.",
        )

    async def sse_stream():
        buf = ""
        try:
            async for chunk in stream_improvement(
                slide=slide,
                deck=deck,
                instructions=body.instructions,
                provider=body.provider,
                model=body.model,
                api_key=api_key,
            ):
                buf += chunk
                yield f"data: {json.dumps({'type': 'delta', 'text': chunk})}\n\n"
        except Exception as exc:  # noqa: BLE001
            yield f"data: {json.dumps({'type': 'error', 'message': str(exc)})}\n\n"
            return
        yield f"data: {json.dumps({'type': 'done', 'buffer': buf})}\n\n"

    return StreamingResponse(
        sse_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


class GenerateDeckRequest(BaseModel):
    brief: str = Field(..., min_length=12)
    slide_count: int = Field(default=12, ge=3, le=35)
    technical_level: Literal["executive", "general", "technical"] | None = None
    attention_span: Literal["short", "medium", "long"] | None = None
    provider: Literal["anthropic", "openai", "gemini"] = "anthropic"
    model: str = ""
    api_key: str = ""


@app.post("/api/decks/generate")
async def api_generate_deck(body: GenerateDeckRequest) -> StreamingResponse:
    """Stream LLM-generated Deck JSON as Server-Sent Events (same framing as slide improve)."""
    from zpresenter.ai_generate import stream_deck_generation  # noqa: PLC0415
    from zpresenter.ai_improve import resolve_api_key  # noqa: PLC0415

    api_key = resolve_api_key(body.provider, body.api_key)
    if not api_key:
        from zpresenter.ai_improve import _PROVIDER_ENV  # noqa: PLC0415

        env_name = _PROVIDER_ENV.get(body.provider, "API_KEY")
        raise HTTPException(
            400,
            f"No API key for provider '{body.provider}'. "
            f"Pass api_key in the request body or set the {env_name} environment variable.",
        )

    async def sse_stream():
        buf = ""
        try:
            async for chunk in stream_deck_generation(
                brief=body.brief,
                slide_count=body.slide_count,
                provider=body.provider,
                model=body.model,
                api_key=api_key,
                technical_level=body.technical_level,
                attention_span=body.attention_span,
            ):
                buf += chunk
                yield f"data: {json.dumps({'type': 'delta', 'text': chunk})}\n\n"
        except Exception as exc:  # noqa: BLE001
            yield f"data: {json.dumps({'type': 'error', 'message': str(exc)})}\n\n"
            return
        yield f"data: {json.dumps({'type': 'done', 'buffer': buf})}\n\n"

    return StreamingResponse(
        sse_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/api/models")
def api_models() -> dict[str, Any]:
    """Return available providers/models and which have API keys configured."""
    from zpresenter.ai_improve import _PROVIDER_ENV  # noqa: PLC0415

    providers = {
        "anthropic": {
            "label": "Anthropic",
            "models": ["claude-sonnet-4-5", "claude-opus-4-7"],
            "env_var": _PROVIDER_ENV["anthropic"],
            "configured": bool(os.getenv(_PROVIDER_ENV["anthropic"])),
        },
        "openai": {
            "label": "OpenAI",
            "models": ["gpt-4o", "gpt-4o-mini", "o1-mini"],
            "env_var": _PROVIDER_ENV["openai"],
            "configured": bool(os.getenv(_PROVIDER_ENV["openai"])),
        },
        "gemini": {
            "label": "Google Gemini",
            "models": ["gemini-2.0-flash", "gemini-1.5-pro"],
            "env_var": _PROVIDER_ENV["gemini"],
            "configured": bool(os.getenv(_PROVIDER_ENV["gemini"])),
        },
    }
    return {"providers": providers}


# ---------------------------------------------------------------------------
# Serve built React UI in production (after `npm run build` in webapp/).
# ---------------------------------------------------------------------------
if _UI_DIST.exists():
    app.mount("/", StaticFiles(directory=str(_UI_DIST), html=True), name="ui")
