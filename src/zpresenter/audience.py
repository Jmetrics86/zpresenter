"""Audience-aware checks — density, pacing, and clarity hints."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel

from zpresenter.models import AudienceProfile, Deck


class Severity(StrEnum):
    error = "error"
    warn = "warn"
    info = "info"


class Finding(BaseModel):
    severity: Severity
    slide_index: int | None = None
    message: str
    suggestion: str | None = None


def _limits(profile: AudienceProfile) -> dict[str, int]:
    span = profile.attention_span
    tech = profile.technical_level
    base = {"max_bullets": 7, "max_bullet_chars": 120, "max_title_chars": 72, "section_every": 12}
    if span == "short":
        base.update({"max_bullets": 5, "max_bullet_chars": 90, "section_every": 8})
    elif span == "long":
        base.update({"max_bullets": 9, "max_bullet_chars": 140, "section_every": 16})
    if tech == "executive":
        base["max_bullets"] = min(base["max_bullets"], 5)
        base["max_bullet_chars"] = min(base["max_bullet_chars"], 100)
    return base


def analyze_deck(deck: Deck) -> list[Finding]:
    findings: list[Finding] = []
    limits = _limits(deck.audience)

    if not deck.slides:
        findings.append(
            Finding(
                severity=Severity.error,
                slide_index=None,
                message="Deck has no slides.",
                suggestion="Add at least one slide.",
            )
        )
        return findings

    if deck.slides[0].layout != "title":
        findings.append(
            Finding(
                severity=Severity.warn,
                slide_index=0,
                message="Opening slide is not a title slide.",
                suggestion='Start with layout "title" so the deck announces topic and context.',
            )
        )

    slides_since_section = 0
    pacing_alert_sent = False

    for i, slide in enumerate(deck.slides):
        if slide.layout == "section":
            slides_since_section = 0
            pacing_alert_sent = False
            continue

        if i == 0 and slide.layout == "title":
            slides_since_section = 0
            pacing_alert_sent = False
            continue

        slides_since_section += 1

        if slide.layout == "title_content" and slide.bullets:
            if len(slide.bullets) > limits["max_bullets"]:
                findings.append(
                    Finding(
                        severity=Severity.warn,
                        slide_index=i,
                        message=f"Slide has {len(slide.bullets)} bullets (limit ~{limits['max_bullets']} for this audience).",
                        suggestion="Split into another slide or promote details to speaker notes.",
                    )
                )
            for j, bullet in enumerate(slide.bullets):
                if len(bullet) > limits["max_bullet_chars"]:
                    findings.append(
                        Finding(
                            severity=Severity.info,
                            slide_index=i,
                            message=f"Bullet {j + 1} is long ({len(bullet)} chars).",
                            suggestion="Shorten or move nuance to speaker notes.",
                        )
                    )
                if not bullet.strip():
                    findings.append(
                        Finding(
                            severity=Severity.warn,
                            slide_index=i,
                            message="Empty bullet detected.",
                            suggestion="Remove empty bullets.",
                        )
                    )

        if slide.title and len(slide.title) > limits["max_title_chars"]:
            findings.append(
                Finding(
                    severity=Severity.info,
                    slide_index=i,
                    message="Title may be visually crowded when projected.",
                    suggestion="Shorten headline; move detail to subtitle or notes.",
                )
            )

        if slides_since_section > limits["section_every"] and not pacing_alert_sent:
            pacing_alert_sent = True
            findings.append(
                Finding(
                    severity=Severity.info,
                    slide_index=i,
                    message=f"No section slide for ~{slides_since_section} slides.",
                    suggestion='Consider inserting layout "section" to reset attention.',
                )
            )

    return findings


def summarize_findings(findings: list[Finding]) -> tuple[int, int, int]:
    """Counts errors, warns, infos."""
    err = sum(1 for f in findings if f.severity == Severity.error)
    warn = sum(1 for f in findings if f.severity == Severity.warn)
    info = sum(1 for f in findings if f.severity == Severity.info)
    return err, warn, info
