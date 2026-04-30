"""LLM-powered deck generation from a topic brief (streaming JSON).

Uses the same providers as ``ai_improve``; output must validate as ``Deck``.
"""

from __future__ import annotations

import re
from collections.abc import AsyncIterator

from zpresenter.ai_improve import stream_llm_completion

_DECK_SCHEMA_HINT = """\
OUTPUT FORMAT — ONE JSON OBJECT ONLY (no markdown fences, no prose).
Keys must match zpresenter Deck serialization:

ROOT (required)
  title       string (deck title)
  subtitle    optional string
  author      optional string
  audience    optional {{ technical_level, attention_span }}
              technical_level: "executive" | "general" | "technical"
              attention_span: "short" | "medium" | "long"
  theme       optional {{ primary_hex, accent_hex, muted_hex }} — RRGGBB without #
  slides      array of slide objects (length MUST equal TARGET_SLIDE_COUNT)

SLIDE
  Prefer omitting "layout" and using "layout_intent" where helpful:
    opening, chapter_break, narrative, comparison, metrics_bar, metrics_trend,
    pull_quote, visual_emphasis
  Or set explicit layout: title | title_content | section | quote |
    chart_bar | chart_line | two_column

  Fields by layout:
    title / section / title_content: title, optional subtitle, bullets for title_content
    quote: quote, optional attribution (headline slot shows quote)
    chart_*: title, chart_categories[], chart_series[] with aligned lengths
    two_column: title, bullets_left[], bullets_right[]
  Optional on slides: notes, title_color_hex (RRGGBB), title_icon (catalog id),
    bullet_icons parallel to bullets, bullets_left_icons / bullets_right_icons,
    images[] with src (relative path like examples/assets/foo.png OR https URL),
    placement allowed for that layout.

RULES
1. Produce exactly TARGET_SLIDE_COUNT slides with varied intents/layouts (mix narrative,
   sections, one chart bar or line where data fits the brief, comparison/two_column if apt).
2. Keep bullets concise for presentation (avoid paragraphs).
3. Use plausible demo chart numbers when metrics support the narrative.
4. Omit images entirely unless you use real-looking placeholder paths under examples/assets/.
5. Start your reply with {{ and end with }} — nothing else.
"""


def build_generation_prompt(
    *,
    brief: str,
    slide_count: int,
    technical_level: str | None,
    attention_span: str | None,
) -> str:
    audience_bits = []
    if technical_level:
        audience_bits.append(f'technical_level should be "{technical_level}".')
    if attention_span:
        audience_bits.append(f'attention_span should be "{attention_span}".')
    audience_line = " ".join(audience_bits) if audience_bits else "Infer sensible audience from the brief."

    return f"""{_DECK_SCHEMA_HINT}

TARGET_SLIDE_COUNT: {slide_count}

AUDIENCE HINTS: {audience_line}

TOPIC / OUTLINE / SOURCE NOTES:
{brief.strip()}

Generate the Deck JSON now:"""


def extract_json_for_deck(raw: str) -> str:
    """Strip markdown fences or outer prose; return the JSON object substring."""
    text = raw.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if fence:
        text = fence.group(1).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        return text[start : end + 1].strip()
    return text


async def stream_deck_generation(
    *,
    brief: str,
    slide_count: int,
    provider: str,
    model: str,
    api_key: str,
    technical_level: str | None,
    attention_span: str | None,
    max_tokens: int = 8192,
) -> AsyncIterator[str]:
    prompt = build_generation_prompt(
        brief=brief,
        slide_count=slide_count,
        technical_level=technical_level,
        attention_span=attention_span,
    )
    async for chunk in stream_llm_completion(
        prompt=prompt,
        provider=provider,
        model=model,
        api_key=api_key,
        max_tokens=max_tokens,
    ):
        yield chunk
