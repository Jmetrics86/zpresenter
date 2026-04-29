"""Semantic icon registry — IDs map to display characters (symbols/emoji) plus searchable tags."""

from __future__ import annotations

from typing import TypedDict

# IDs use dot namespaces: category.name — stable for JSON decks and search.


class IconEntry(TypedDict):
    char: str
    category: str
    tags: list[str]


# Context buckets: pick icons that match narrative (security, metrics, people, …)
CATALOG: dict[str, IconEntry] = {
    # Status & feedback
    "status.success": {"char": "\u2713", "category": "status", "tags": ["ok", "done", "yes", "pass", "complete"]},
    "status.fail": {"char": "\u2717", "category": "status", "tags": ["no", "error", "reject"]},
    "status.warning": {"char": "\u26a0", "category": "status", "tags": ["alert", "caution", "risk"]},
    "status.info": {"char": "\u2139", "category": "status", "tags": ["note", "help", "about"]},
    "status.blocked": {"char": "\u26d4", "category": "status", "tags": ["stop", "blocked", "freeze"]},
    "status.new": {"char": "\u2728", "category": "status", "tags": ["sparkle", "launch", "feature"]},
    # Data & analytics
    "data.chart": {"char": "\U0001f4ca", "category": "data", "tags": ["bar", "metrics", "analytics", "kpi"]},
    "data.trend_up": {"char": "\U0001f4c8", "category": "data", "tags": ["growth", "up", "improve"]},
    "data.trend_down": {"char": "\U0001f4c9", "category": "data", "tags": ["decline", "down"]},
    "data.line": {"char": "\U0001f4c9", "category": "data", "tags": ["line", "series"]},
    "data.table": {"char": "\u25a6", "category": "data", "tags": ["grid", "tabular"]},
    "data.filter": {"char": "\U0001f50d", "category": "data", "tags": ["search", "segment"]},
    "data.dashboard": {"char": "\U0001f4ca", "category": "data", "tags": ["dashboard", "cockpit"]},
    # People & org
    "people.team": {"char": "\U0001f465", "category": "people", "tags": ["team", "group", "users"]},
    "people.person": {"char": "\U0001f464", "category": "people", "tags": ["user", "person", "role"]},
    "people.handshake": {"char": "\U0001f91d", "category": "people", "tags": ["partner", "deal", "gs"]},
    "people.voice": {"char": "\U0001f3a4", "category": "people", "tags": ["speaker", "present", "talk"]},
    # Security & compliance
    "security.lock": {"char": "\U0001f512", "category": "security", "tags": ["privacy", "encrypt", "sso"]},
    "security.key": {"char": "\U0001f511", "category": "security", "tags": ["access", "credentials"]},
    "security.shield": {"char": "\U0001f6e1", "category": "security", "tags": ["defense", "soc2", "audit"]},
    "security.eye": {"char": "\U0001f441", "category": "security", "tags": ["visibility", "monitoring"]},
    # Commerce & GTM
    "commerce.cart": {"char": "\U0001f6d2", "category": "commerce", "tags": ["checkout", "store", "sku"]},
    "commerce.money": {"char": "\U0001f4b0", "category": "commerce", "tags": ["revenue", "pricing", "arr"]},
    "commerce.card": {"char": "\U0001f4b3", "category": "commerce", "tags": ["payment", "psp"]},
    "commerce.rocket": {"char": "\U0001f680", "category": "commerce", "tags": ["launch", "gtm", "growth"]},
    # Product & tech
    "tech.gear": {"char": "\u2699", "category": "tech", "tags": ["settings", "config", "ops"]},
    "tech.cpu": {"char": "\U0001f4bb", "category": "tech", "tags": ["compute", "server", "infra"]},
    "tech.cloud": {"char": "\u2601", "category": "tech", "tags": ["cloud", "saas", "hosted"]},
    "tech.api": {"char": "\U0001f517", "category": "tech", "tags": ["link", "integration", "graphql"]},
    "tech.bug": {"char": "\U0001fab2", "category": "tech", "tags": ["bug", "defect", "qa"]},
    "tech.branch": {"char": "\U0001f500", "category": "tech", "tags": ["git", "release", "pipeline"]},
    # UI & design
    "ui.palette": {"char": "\U0001f3a8", "category": "ui", "tags": ["design", "brand", "color", "tokens"]},
    "ui.layout": {"char": "\u25eb", "category": "ui", "tags": ["layout", "grid", "columns"]},
    "ui.mobile": {"char": "\U0001f4f1", "category": "ui", "tags": ["phone", "ios", "android"]},
    "ui.accessibility": {"char": "\u267f", "category": "ui", "tags": ["a11y", "wcag", "inclusive"]},
    # Navigation & structure
    "nav.arrow_right": {"char": "\u2192", "category": "nav", "tags": ["next", "flow", "sequence"]},
    "nav.target": {"char": "\U0001f3af", "category": "nav", "tags": ["goal", "north star", "okr"]},
    "nav.pin": {"char": "\U0001f4cd", "category": "nav", "tags": ["milestone", "checkpoint"]},
    # Research & clinical
    "research.lab": {"char": "\U0001f52c", "category": "research", "tags": ["science", "trial", "lab"]},
    "research.pill": {"char": "\U0001f48a", "category": "research", "tags": ["dose", "drug", "therapy"]},
    "research.heart": {"char": "\u2764", "category": "research", "tags": ["patient", "care", "outcome"]},
    "research.document": {"char": "\U0001f4c4", "category": "research", "tags": ["protocol", "csr", "reg"]},
    # Time & planning
    "time.clock": {"char": "\U0001f553", "category": "time", "tags": ["schedule", "deadline", "quarter"]},
    "time.calendar": {"char": "\U0001f4c5", "category": "time", "tags": ["roadmap", "calendar", "week"]},
    # Meta
    "meta.lightbulb": {"char": "\U0001f4a1", "category": "meta", "tags": ["idea", "insight", "tip"]},
    "meta.question": {"char": "\u2753", "category": "meta", "tags": ["ask", "faq", "unknown"]},
    "meta.spark": {"char": "\u2726", "category": "meta", "tags": ["highlight", "callout"]},
}


def resolve_icon(icon_id: str | None) -> str | None:
    """Return the rendered character for a catalog id, or None if unknown / empty."""
    if not icon_id or not icon_id.strip():
        return None
    entry = CATALOG.get(icon_id.strip())
    return entry["char"] if entry else None


def list_icon_ids(*, category: str | None = None) -> list[str]:
    if category is None:
        return sorted(CATALOG.keys())
    c = category.lower().strip()
    return sorted(k for k, v in CATALOG.items() if v["category"].lower() == c)


def categories() -> list[str]:
    return sorted({v["category"] for v in CATALOG.values()})


def search_icons(query: str) -> list[str]:
    """Return icon ids whose id, category, or tags match query (substring, case-insensitive)."""
    q = query.lower().strip()
    if not q:
        return list_icon_ids()
    out: list[str] = []
    for icon_id, meta in CATALOG.items():
        if q in icon_id.lower():
            out.append(icon_id)
            continue
        if q in meta["category"].lower():
            out.append(icon_id)
            continue
        if any(q in t for t in meta["tags"]):
            out.append(icon_id)
    return sorted(set(out))


def describe_icon(icon_id: str) -> IconEntry | None:
    return CATALOG.get(icon_id)
