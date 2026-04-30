"""Heuristic layout hints — semantic intent compatibility and content-shaped suggestions."""

from __future__ import annotations

from dataclasses import dataclass, field

from zpresenter.models import Deck, LayoutIntent, Slide, SlideLayoutKind

_INTENT_ALLOWED: dict[LayoutIntent, frozenset[SlideLayoutKind]] = {
    "opening": frozenset({"title"}),
    "chapter_break": frozenset({"section"}),
    "narrative": frozenset({"title_content"}),
    "comparison": frozenset({"two_column"}),
    "metrics_bar": frozenset({"chart_bar"}),
    "metrics_trend": frozenset({"chart_line"}),
    "pull_quote": frozenset({"quote"}),
    "visual_emphasis": frozenset({"title_content", "two_column"}),
}

# Default concrete layout when intent is set but content does not imply a shape.
_INTENT_PRIMARY: dict[LayoutIntent, SlideLayoutKind] = {
    "opening": "title",
    "chapter_break": "section",
    "narrative": "title_content",
    "comparison": "two_column",
    "metrics_bar": "chart_bar",
    "metrics_trend": "chart_line",
    "pull_quote": "quote",
    "visual_emphasis": "title_content",
}


def layouts_for_intent(intent: LayoutIntent) -> frozenset[SlideLayoutKind]:
    return _INTENT_ALLOWED[intent]


def intent_primary_layout(intent: LayoutIntent) -> SlideLayoutKind:
    """Canonical layout when authoring intent-only slides with minimal fields."""
    return _INTENT_PRIMARY[intent]


def intent_matches_layout(intent: LayoutIntent | None, layout: SlideLayoutKind) -> bool:
    if intent is None:
        return True
    return layout in _INTENT_ALLOWED[intent]


def infer_layout_from_content(slide: Slide, slide_index: int) -> SlideLayoutKind | None:
    """Best-effort layout implied by populated fields (not necessarily ideal UX)."""
    if slide.chart_categories and slide.chart_series:
        intent = slide.layout_intent
        if intent == "metrics_trend":
            return "chart_line"
        if intent == "metrics_bar":
            return "chart_bar"
        # Prefer line when subtitle hints trajectory (weak heuristic).
        sub = (slide.subtitle or "").lower()
        if any(k in sub for k in ("trend", "cohort", "trajectory", "over time")):
            return "chart_line"
        return "chart_bar"

    if slide.quote and slide.quote.strip():
        return "quote"

    left = slide.bullets_left or []
    right = slide.bullets_right or []
    if left and right:
        return "two_column"

    if slide.bullets:
        return "title_content"

    if slide.title and slide_index == 0:
        return "title"

    if slide.title and slide_index > 0:
        return "section"

    return None


def resolve_slide_layout_or_raise(slide: Slide, slide_index: int) -> SlideLayoutKind:
    """Resolve ``layout=None`` slides using ``layout_intent`` + content heuristics."""
    intent = slide.layout_intent
    inferred = infer_layout_from_content(slide, slide_index)

    if intent is not None:
        allowed = layouts_for_intent(intent)
        if inferred is not None:
            if inferred in allowed:
                return inferred
            raise ValueError(
                f"slides[{slide_index}]: layout_intent {intent!r} allows {sorted(allowed)} "
                f"but content implies {inferred!r}. Set `layout` explicitly, adjust fields, "
                "or change layout_intent."
            )
        return intent_primary_layout(intent)

    if inferred is not None:
        return inferred
    if slide.layout is None:
        raise ValueError(
            f"slides[{slide_index}]: cannot infer layout — set `layout` or `layout_intent`, "
            "or add recognizable content (bullets, quote, chart series, two columns, …)."
        )
    return slide.layout


@dataclass
class LayoutSuggestion:
    slide_index: int
    current: SlideLayoutKind
    inferred: SlideLayoutKind | None
    aligned_with_content: bool
    intent_ok: bool
    layout_intent: LayoutIntent | None
    reasons: list[str] = field(default_factory=list)


def suggest_slide(slide: Slide, slide_index: int) -> LayoutSuggestion:
    """Requires concrete ``layout`` (normal ``Deck`` JSON parse path materializes omitted layouts)."""
    if slide.layout is None:
        raise ValueError(
            "suggest_slide expects slides with concrete layout — parse JSON via Deck.model_validate."
        )
    reasons: list[str] = []
    inferred = infer_layout_from_content(slide, slide_index)
    intent = slide.layout_intent

    aligned = inferred is None or inferred == slide.layout
    if inferred is not None and inferred != slide.layout:
        reasons.append(f"Inferred `{inferred}` from fields; slide uses `{slide.layout}`.")

    intent_ok = intent_matches_layout(intent, slide.layout)
    if intent and not intent_ok:
        allowed = ", ".join(sorted(layouts_for_intent(intent)))
        reasons.append(f'layout_intent "{intent}" expects one of: {allowed}.')

    # Opening slide convention
    if slide_index == 0 and slide.layout != "title":
        reasons.append('Slide 0 is usually layout "title" for audiences expecting a cover.')

    return LayoutSuggestion(
        slide_index=slide_index,
        current=slide.layout,
        inferred=inferred,
        aligned_with_content=aligned,
        intent_ok=intent_ok,
        layout_intent=intent,
        reasons=reasons,
    )


def suggest_deck(deck: Deck) -> list[LayoutSuggestion]:
    return [suggest_slide(s, i) for i, s in enumerate(deck.slides)]
