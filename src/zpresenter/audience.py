"""Audience-aware checks — density, pacing, and clarity hints."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel

from zpresenter.iconography import resolve_icon
from zpresenter.media import local_path_exists
from zpresenter.models import AudienceProfile, Deck, Slide


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


def _bullet_findings(
    slide_index: int,
    bullets: list[str],
    limits: dict[str, int],
    *,
    scope: str = "",
) -> list[Finding]:
    findings: list[Finding] = []
    if len(bullets) > limits["max_bullets"]:
        if scope:
            msg = f"{scope} has {len(bullets)} bullets (limit ~{limits['max_bullets']} per column)."
        else:
            msg = (
                f"Slide has {len(bullets)} bullets "
                f"(limit ~{limits['max_bullets']} for this audience)."
            )
        findings.append(
            Finding(
                severity=Severity.warn,
                slide_index=slide_index,
                message=msg,
                suggestion="Split into another slide or promote details to speaker notes.",
            )
        )
    for j, bullet in enumerate(bullets):
        if len(bullet) > limits["max_bullet_chars"]:
            prefix = f"{scope} bullet {j + 1}" if scope else f"Bullet {j + 1}"
            findings.append(
                Finding(
                    severity=Severity.info,
                    slide_index=slide_index,
                    message=f"{prefix} is long ({len(bullet)} chars).",
                    suggestion="Shorten or move nuance to speaker notes.",
                )
            )
        if not bullet.strip():
            findings.append(
                Finding(
                    severity=Severity.warn,
                    slide_index=slide_index,
                    message=f"{scope}: empty bullet" if scope else "Empty bullet detected.",
                    suggestion="Remove empty bullets.",
                )
            )
    return findings


def _warn_unknown_icon(slide_index: int, icon_id: str, label: str) -> Finding:
    return Finding(
        severity=Severity.warn,
        slide_index=slide_index,
        message=f'Unknown icon id "{icon_id}" ({label}).',
        suggestion="Run `zpresenter icons search` or `zpresenter icons list`.",
    )


def _icon_findings(slide: Slide, slide_index: int) -> list[Finding]:
    out: list[Finding] = []

    tid = slide.title_icon
    if tid and tid.strip() and resolve_icon(tid) is None:
        out.append(_warn_unknown_icon(slide_index, tid.strip(), "title_icon"))

    def parallel(ids: list[str | None] | None, label: str) -> None:
        if not ids:
            return
        for j, iid in enumerate(ids):
            if iid is None or not str(iid).strip():
                continue
            if resolve_icon(iid) is None:
                out.append(_warn_unknown_icon(slide_index, str(iid).strip(), f"{label}[{j}]"))

    parallel(slide.bullet_icons, "bullet_icons")
    parallel(slide.bullets_left_icons, "bullets_left_icons")
    parallel(slide.bullets_right_icons, "bullets_right_icons")
    return out


def _media_findings(slide: Slide, slide_index: int, deck_dir: Path | None) -> list[Finding]:
    if deck_dir is None:
        return []
    out: list[Finding] = []
    for j, img in enumerate(slide.images or []):
        src = img.src.strip()
        if src.startswith("http://") or src.startswith("https://"):
            continue
        if not local_path_exists(img.src, deck_dir):
            out.append(
                Finding(
                    severity=Severity.warn,
                    slide_index=slide_index,
                    message=f'Missing image file for images[{j}] ({img.src}).',
                    suggestion="Place the asset beside the deck JSON or pass paths relative to that file.",
                )
            )
    return out


def analyze_deck(deck: Deck, *, deck_path: Path | None = None) -> list[Finding]:
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

    deck_dir = deck_path.parent.resolve() if deck_path is not None else None

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
        findings.extend(_icon_findings(slide, i))
        findings.extend(_media_findings(slide, i, deck_dir))

        if slide.layout == "section":
            slides_since_section = 0
            pacing_alert_sent = False
            continue

        if i == 0 and slide.layout == "title":
            slides_since_section = 0
            pacing_alert_sent = False
            continue

        slides_since_section += 1

        if slide.layout in ("chart_bar", "chart_line"):
            cats = slide.chart_categories or []
            series_list = slide.chart_series or []
            if not cats or not series_list:
                findings.append(
                    Finding(
                        severity=Severity.error,
                        slide_index=i,
                        message="Chart slide missing categories or series.",
                        suggestion='Provide chart_categories and chart_series aligned by length.',
                    )
                )
            else:
                for si, ser in enumerate(series_list):
                    if len(ser.values) != len(cats):
                        findings.append(
                            Finding(
                                severity=Severity.error,
                                slide_index=i,
                                message=f"Series \"{ser.name}\" length does not match categories ({len(ser.values)} vs {len(cats)}).",
                                suggestion="Ensure each series.values matches chart_categories length.",
                            )
                        )

        if slide.layout == "two_column":
            left = slide.bullets_left or []
            right = slide.bullets_right or []
            if not left and not right:
                findings.append(
                    Finding(
                        severity=Severity.warn,
                        slide_index=i,
                        message="Two-column slide has no bullets_left or bullets_right.",
                        suggestion="Populate both columns or switch layout.",
                    )
                )
            findings.extend(_bullet_findings(i, left, limits, scope="Left column"))
            findings.extend(_bullet_findings(i, right, limits, scope="Right column"))

        if slide.layout == "title_content" and slide.bullets:
            findings.extend(_bullet_findings(i, slide.bullets, limits))

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
