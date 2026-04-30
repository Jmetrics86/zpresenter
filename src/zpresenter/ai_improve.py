"""LLM-powered slide content improvement with streaming.

Supported providers
-------------------
* anthropic  — Claude Sonnet / Opus  (pip: anthropic)
* openai     — GPT-4o / o1 series    (pip: openai)
* gemini     — Gemini Flash / Pro     (pip: google-generativeai)

Each SDK is imported lazily so only the one the user calls needs to be installed.

API keys
--------
Resolved in priority order:
  1. ``api_key`` argument passed to ``stream_improvement()``
  2. Environment variable: ANTHROPIC_API_KEY / OPENAI_API_KEY / GOOGLE_API_KEY
"""

from __future__ import annotations

import json
from collections.abc import AsyncIterator

from zpresenter.models import Deck, Slide

# ---------------------------------------------------------------------------
# Prompt engineering
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """\
You are a presentation content expert. Improve the slide's text content \
according to the task below.

STRICT RULES
1. Return ONLY a single raw JSON object — no markdown fences, no explanation, \
no surrounding text.
2. Never change: layout, layout_intent, chart_categories, chart_series, images.
3. Preserve every null field as null; do not invent new fields.
4. Use identical JSON keys to the input — only improve string VALUES.
5. Your output MUST start with {{ and end with }}.

--- DECK CONTEXT ---
Title   : {deck_title}
Audience: {technical_level}, {attention_span} attention

--- CURRENT SLIDE ---
{slide_json}

--- TASK ---
{instructions}

Improved slide JSON:"""


def _build_prompt(slide: Slide, deck: Deck, instructions: str) -> str:
    return _SYSTEM_PROMPT.format(
        deck_title=deck.title,
        technical_level=deck.audience.technical_level,
        attention_span=deck.audience.attention_span,
        slide_json=json.dumps(slide.model_dump(mode="json"), indent=2),
        instructions=instructions.strip() or "Improve clarity, conciseness, and impact.",
    )


# ---------------------------------------------------------------------------
# Provider streams (lazy SDK imports)
# ---------------------------------------------------------------------------

async def _stream_anthropic(
    prompt: str,
    model: str,
    api_key: str,
    *,
    max_tokens: int,
) -> AsyncIterator[str]:
    import anthropic  # noqa: PLC0415

    client = anthropic.AsyncAnthropic(api_key=api_key)
    async with client.messages.stream(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        async for text in stream.text_stream:
            yield text


async def _stream_openai(
    prompt: str,
    model: str,
    api_key: str,
    *,
    max_tokens: int,
) -> AsyncIterator[str]:
    from openai import AsyncOpenAI  # noqa: PLC0415

    client = AsyncOpenAI(api_key=api_key)
    stream = await client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    async for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


async def _stream_gemini(
    prompt: str,
    model: str,
    api_key: str,
    *,
    max_tokens: int,
) -> AsyncIterator[str]:
    import google.generativeai as genai  # noqa: PLC0415

    genai.configure(api_key=api_key)
    gmodel = genai.GenerativeModel(
        model,
        generation_config={"max_output_tokens": max_tokens},
    )
    response = await gmodel.generate_content_async(prompt, stream=True)
    async for chunk in response:
        if chunk.text:
            yield chunk.text


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

_PROVIDER_STREAMS = {
    "anthropic": _stream_anthropic,
    "openai": _stream_openai,
    "gemini": _stream_gemini,
}

_PROVIDER_ENV = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "gemini": "GOOGLE_API_KEY",
}

_DEFAULT_MODELS = {
    "anthropic": "claude-sonnet-4-5",
    "openai": "gpt-4o",
    "gemini": "gemini-2.0-flash",
}


def resolve_api_key(provider: str, explicit_key: str) -> str:
    """Return ``explicit_key`` or fall back to the provider's env variable."""
    import os  # noqa: PLC0415

    if explicit_key:
        return explicit_key
    env = _PROVIDER_ENV.get(provider, "")
    return os.getenv(env, "") if env else ""


async def stream_llm_completion(
    *,
    prompt: str,
    provider: str,
    model: str,
    api_key: str,
    max_tokens: int = 2048,
) -> AsyncIterator[str]:
    """Yield token chunks from the chosen LLM (shared by slide improve and deck generation)."""
    fn = _PROVIDER_STREAMS.get(provider)
    if fn is None:
        valid = ", ".join(_PROVIDER_STREAMS)
        raise ValueError(f"Unknown provider {provider!r}. Use: {valid}.")

    resolved_model = model or _DEFAULT_MODELS.get(provider, "")
    async for chunk in fn(prompt, resolved_model, api_key, max_tokens=max_tokens):
        yield chunk


async def stream_improvement(
    *,
    slide: Slide,
    deck: Deck,
    instructions: str,
    provider: str,
    model: str,
    api_key: str,
) -> AsyncIterator[str]:
    """Yield token chunks from the chosen LLM for an improved slide JSON."""
    prompt = _build_prompt(slide, deck, instructions)
    async for chunk in stream_llm_completion(
        prompt=prompt,
        provider=provider,
        model=model,
        api_key=api_key,
        max_tokens=2048,
    ):
        yield chunk
