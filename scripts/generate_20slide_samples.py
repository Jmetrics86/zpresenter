#!/usr/bin/env python3
"""Generate 3 comprehensive 20-slide sample decks covering all layouts, images, and iconography.

Run from repo root:
    uv run python scripts/generate_20slide_samples.py
"""

from __future__ import annotations

import json
from pathlib import Path

from zpresenter.models import AudienceProfile, ChartSeries, Deck, DeckTheme, Slide, SlideImage

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "examples" / "samples"
SCHEMA_REF = "../../schemas/deck.schema.json"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _cs(name: str, values: tuple[float, ...]) -> ChartSeries:
    return ChartSeries(name=name, values=list(values))


def _img(seed: str, placement: str, caption: str | None = None) -> SlideImage:
    src = f"https://picsum.photos/seed/{seed}/1200/675"
    return SlideImage(src=src, placement=placement, caption=caption)


def _write(deck: Deck, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    payload = deck.model_dump(mode="json")
    payload["$schema"] = SCHEMA_REF
    path = OUT / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  Wrote {path.relative_to(ROOT)} ({len(deck.slides)} slides)")


# ---------------------------------------------------------------------------
# Deck 1 — Apex Ventures: Market Strategy 2026  (Executive / Finance)
# ---------------------------------------------------------------------------

def deck_apex_strategy() -> Deck:
    """20-slide executive strategy deck — full use of all layouts, icons, and images."""
    th = DeckTheme(primary_hex="1E3A5F", accent_hex="D97706", muted_hex="64748B")

    slides: list[Slide] = [
        # 1 title ─ opening, banner image
        Slide(
            layout="title",
            layout_intent="opening",
            title="Apex Ventures: Market Strategy 2026",
            subtitle="Capturing the $4.2 T digital infrastructure opportunity",
            title_icon="commerce.rocket",
            notes="30-min board session. Objective: approve H2 capital deployment.",
            images=[_img("boardroom", "banner_lower", "Apex HQ — Strategy Week 2026")],
        ),
        # 2 section ─ executive summary
        Slide(
            layout="section",
            layout_intent="chapter_break",
            title="Executive Summary",
            title_color_hex="1E3A5F",
            notes="Agenda: market, strategy, financials, ask.",
        ),
        # 3 title_content ─ why now
        Slide(
            layout="title_content",
            layout_intent="narrative",
            title="Why This Moment Matters",
            title_icon="meta.lightbulb",
            bullets=[
                "Composable infrastructure market crossing $180 B in 2026 — 3-year CAGR of 34%",
                "Enterprise AI workloads demanding elastic, multi-cloud fabric by default",
                "Three legacy incumbents under margin pressure — acquisition window open",
                "Regulatory clarity on data residency unlocking EU/APAC greenfield",
                "Apex's partner network at scale: 2,400 VARs primed for GTM acceleration",
            ],
            bullet_icons=[
                "data.trend_up",
                "tech.cloud",
                "commerce.money",
                "security.shield",
                "people.handshake",
            ],
            notes="Anchor on the CAGR stat — CFO will ask for primary source.",
        ),
        # 4 chart_bar ─ market size by segment
        Slide(
            layout="chart_bar",
            layout_intent="metrics_bar",
            title="TAM by Segment — $B",
            subtitle="Source: Gartner Infrastructure Services Forecast 2026",
            chart_categories=["Compute", "Storage", "Network", "Security", "AI Ops"],
            chart_series=[
                _cs("2024", (38.2, 24.1, 18.6, 29.4, 12.8)),
                _cs("2026E", (52.7, 31.4, 24.0, 44.1, 28.5)),
            ],
            notes="Security and AI Ops are the fastest growers — focus M&A lens here.",
            images=[_img("analytics", "accent_corner", "Gartner 2026")],
        ),
        # 5 two_column ─ competitive landscape
        Slide(
            layout="two_column",
            layout_intent="comparison",
            title="Competitive Positioning",
            title_icon="nav.target",
            bullets_left=[
                "Apex (us): Composable, API-first, open standards",
                "Sub-100ms provisioning SLA",
                "Zero-trust by default, SOC 2 Type II",
                "Unified control plane across 18 regions",
            ],
            bullets_left_icons=["status.success", "status.success", "security.shield", "tech.cloud"],
            bullets_right=[
                "Incumbent A: Monolithic, 6-week lead time",
                "Incumbent B: Proprietary stack, high lock-in",
                "Start-up C: Under-capitalised, single region",
                "Hyperscaler: High margin, poor mid-market fit",
            ],
            bullets_right_icons=["status.fail", "status.fail", "status.warning", "status.warning"],
            notes="Don't over-dwell. Move to financial slide within 4 min.",
        ),
        # 6 quote ─ customer proof
        Slide(
            layout="quote",
            layout_intent="pull_quote",
            quote="Apex cut our infrastructure lead time from 11 weeks to 4 days. It's the single biggest change to our engineering velocity this decade.",
            attribution="CTO, Fortune 500 Financial Services Client",
            notes="NPS 78. Reference call arranged for due-diligence team.",
            images=[_img("officebuild", "accent_corner")],
        ),
        # 7 section ─ strategic pillars
        Slide(
            layout="section",
            layout_intent="chapter_break",
            title="Strategic Pillars 2026",
            title_color_hex="1E3A5F",
        ),
        # 8 title_content ─ growth levers, image right
        Slide(
            layout="title_content",
            layout_intent="visual_emphasis",
            title="Three Growth Levers",
            title_icon="data.trend_up",
            bullets=[
                "Platform Expansion: AI Ops module GA in Q3 — 340 beta customers",
                "Geographic Reach: 4 new regions (Riyadh, Seoul, São Paulo, Warsaw)",
                "Partner Ecosystem: co-sell motions with 3 hyperscalers signed Q2",
                "M&A Optionality: 2 targets under NDA for security bolt-on",
            ],
            bullet_icons=["status.new", "nav.pin", "people.handshake", "commerce.money"],
            images=[_img("growth", "primary_right", "Q3 AI Ops launch dashboard")],
            notes="Partner co-sell alone adds $42 M to H2 pipeline.",
        ),
        # 9 chart_line ─ revenue trajectory
        Slide(
            layout="chart_line",
            layout_intent="metrics_trend",
            title="ARR Trajectory — $M",
            subtitle="Core platform + AI Ops + Partner channel",
            chart_categories=["Q1 24", "Q2 24", "Q3 24", "Q4 24", "Q1 25", "Q2 25"],
            chart_series=[
                _cs("Core ARR", (22.1, 26.8, 31.4, 37.0, 43.2, 51.6)),
                _cs("AI Ops ARR", (0.0, 0.0, 0.0, 1.4, 3.8, 7.2)),
                _cs("Partner ARR", (4.2, 5.1, 6.3, 8.0, 10.5, 14.1)),
            ],
            notes="Net retention 118% — expansion from existing base continues.",
        ),
        # 10 title_content ─ customer segments
        Slide(
            layout="title_content",
            layout_intent="narrative",
            title="Customer Segment Priorities",
            title_icon="people.team",
            bullets=[
                "Enterprise (>$1 B rev): ACV $280K avg — 72 logos, 94% retention",
                "Upper Mid-Market: ACV $64K — fastest growing cohort at 61% YoY",
                "Government / Public Sector: new practice, first 8 contracts H1 2025",
                "ISV / SaaS Partners: 120 embedded integrations — NRR 131%",
                "Geographic: EMEA now 22% of new ARR vs 9% in 2024",
            ],
            bullet_icons=[
                "people.team",
                "data.trend_up",
                "security.shield",
                "tech.api",
                "nav.arrow_right",
            ],
        ),
        # 11 two_column ─ enterprise vs smb
        Slide(
            layout="two_column",
            layout_intent="comparison",
            title="Enterprise vs. Mid-Market Playbook",
            bullets_left=[
                "18-month sales cycle, multi-buyer",
                "Custom SLAs and dedicated TAM",
                "Compliance-led: FedRAMP, ISO 27001",
                "Avg 3.4 product modules at signature",
            ],
            bullets_right=[
                "30-day trial to close typical path",
                "Self-serve onboarding + CSM pooled",
                "Standard SLA tier, SOC 2 Type II",
                "Land with compute, expand to AI Ops",
            ],
            notes="Don't conflate the two motions — separate pipeline reviews.",
        ),
        # 12 section ─ financial performance
        Slide(
            layout="section",
            layout_intent="chapter_break",
            title="Financial Performance",
            title_color_hex="1E3A5F",
        ),
        # 13 chart_bar ─ quarterly revenue
        Slide(
            layout="chart_bar",
            layout_intent="metrics_bar",
            title="Quarterly Revenue — $M",
            subtitle="GAAP revenue; Q2 25 preliminary",
            chart_categories=["Q3 24", "Q4 24", "Q1 25", "Q2 25E"],
            chart_series=[
                _cs("Platform", (14.2, 17.8, 21.3, 25.6)),
                _cs("Professional Services", (3.1, 3.8, 4.2, 4.9)),
            ],
        ),
        # 14 title_content ─ unit economics, image corner
        Slide(
            layout="title_content",
            layout_intent="narrative",
            title="Unit Economics Snapshot",
            title_icon="data.chart",
            bullets=[
                "Gross margin: 74% (platform 81%, services 28%)",
                "LTV/CAC: 6.8× enterprise, 4.1× mid-market",
                "Payback period: 14 months (enterprise), 9 months (SMB)",
                "Rule of 40 score: 62 — top decile for growth stage",
            ],
            bullet_icons=["commerce.money", "data.trend_up", "time.clock", "meta.spark"],
            images=[_img("finance", "accent_corner", "Q2 25 board pack data")],
            notes="Gross margin improvement driven by infra efficiency roadmap.",
        ),
        # 15 chart_line ─ nrr & gross margin
        Slide(
            layout="chart_line",
            layout_intent="metrics_trend",
            title="Retention & Efficiency Trends",
            subtitle="Net Revenue Retention (%) and Gross Margin (%)",
            chart_categories=["Q1 24", "Q2 24", "Q3 24", "Q4 24", "Q1 25", "Q2 25"],
            chart_series=[
                _cs("NRR %", (109.0, 112.0, 114.0, 116.0, 117.0, 118.0)),
                _cs("Gross Margin %", (68.0, 70.0, 71.5, 72.8, 73.4, 74.0)),
            ],
        ),
        # 16 section ─ risk & roadmap
        Slide(
            layout="section",
            layout_intent="chapter_break",
            title="Risk, Roadmap & Ask",
            title_color_hex="1E3A5F",
        ),
        # 17 title_content ─ risk register
        Slide(
            layout="title_content",
            layout_intent="narrative",
            title="Key Risk Factors & Mitigants",
            title_icon="status.warning",
            bullets=[
                "Macro: enterprise spend slowdown — mitigated by 14-mo backlog coverage",
                "Competition: hyperscaler price war — differentiated via AI Ops & compliance",
                "Talent: engineering attrition above benchmark — comp rebalancing approved",
                "Regulatory: EU AI Act compliance cost — budgeted €1.8M, on track",
            ],
            bullet_icons=[
                "status.warning",
                "security.shield",
                "people.person",
                "security.lock",
            ],
        ),
        # 18 two_column ─ H2 vs Q4 focus
        Slide(
            layout="two_column",
            layout_intent="comparison",
            title="H2 2025 Priorities",
            title_icon="time.calendar",
            bullets_left=[
                "Q3: AI Ops GA launch",
                "Q3: APAC region live",
                "Q3: 50 new enterprise logos",
                "Q3: SOC 2 renewal complete",
            ],
            bullets_left_icons=["status.new", "nav.pin", "people.team", "security.shield"],
            bullets_right=[
                "Q4: Series C close ($120M target)",
                "Q4: FedRAMP moderate achieved",
                "Q4: First ISV marketplace listing",
                "Q4: Annual board strategy day",
            ],
            bullets_right_icons=["commerce.money", "security.lock", "tech.api", "people.voice"],
            notes="Series C investor deck ready for board preview next slide.",
        ),
        # 19 title_content ─ the ask
        Slide(
            layout="title_content",
            layout_intent="visual_emphasis",
            title="Board Resolution Required",
            title_icon="nav.target",
            bullets=[
                "Approve $38M H2 operating budget — AI Ops launch, 3 new regions",
                "Authorise M&A mandate up to $80M for security segment bolt-on",
                "Ratify Series C timing: roadshow Q3, close target Nov 2025",
                "Appoint independent audit committee member (candidates in appendix)",
            ],
            bullet_icons=["status.info", "commerce.money", "data.trend_up", "people.person"],
            images=[_img("meeting", "primary_right", "Board decision session")],
        ),
        # 20 title_content ─ closing / next steps
        Slide(
            layout="title_content",
            layout_intent="narrative",
            title="Next Steps",
            title_icon="nav.arrow_right",
            bullets=[
                "CFO distributes Series C data room access — end of week",
                "Legal: NDA counterparty list for M&A targets — 5 business days",
                "CEO + CTO: Investor roadshow dry run — August 4",
                "Board: Written resolution by August 10 or reconvene August 12",
            ],
            bullet_icons=["people.person", "security.key", "people.voice", "time.calendar"],
            notes="All actions logged in board management platform. Thank you.",
        ),
    ]

    return Deck(
        title="Apex Ventures — Market Strategy 2026",
        subtitle="Confidential Board Presentation · July 2026",
        author="Apex Strategy Office",
        audience=AudienceProfile(technical_level="executive", attention_span="short"),
        theme=th,
        slides=slides,
    )


# ---------------------------------------------------------------------------
# Deck 2 — Meridian Engineering: Platform Architecture Review
# ---------------------------------------------------------------------------

def deck_meridian_platform() -> Deck:
    """20-slide technical platform review — engineering audience, deep metrics."""
    th = DeckTheme(primary_hex="0F172A", accent_hex="059669", muted_hex="6B7280")

    slides: list[Slide] = [
        # 1 title ─ cover
        Slide(
            layout="title",
            layout_intent="opening",
            title="Meridian Platform: Architecture Review Q3 2026",
            subtitle="Reliability · Scalability · Developer Experience · Cost Efficiency",
            title_icon="tech.cpu",
            notes="90-min eng-wide all-hands. Recording shared post-session.",
            images=[_img("datacenter", "banner_lower", "Meridian Primary Region — SJC1")],
        ),
        # 2 section ─ context
        Slide(
            layout="section",
            layout_intent="chapter_break",
            title="Context & Goals",
            title_color_hex="059669",
        ),
        # 3 title_content ─ why this review
        Slide(
            layout="title_content",
            layout_intent="narrative",
            title="Why This Architecture Review Now",
            title_icon="meta.question",
            bullets=[
                "Traffic 4.8× since last review — original capacity model no longer valid",
                "P99 latency SLO missed 6 consecutive weeks — root cause is DB read path",
                "12 separate teams now owning infra config — drift and toil accumulating",
                "Cloud bill 31% above forecast — optimisation opportunity estimated $2.8M/yr",
                "Incident rate: 4.2 SEV-2s per month in Q2 vs target of ≤ 1",
            ],
            bullet_icons=[
                "data.trend_up",
                "status.warning",
                "tech.branch",
                "commerce.money",
                "status.blocked",
            ],
        ),
        # 4 chart_bar ─ traffic growth
        Slide(
            layout="chart_bar",
            layout_intent="metrics_bar",
            title="Monthly Active Requests — Billion",
            subtitle="All services combined; Q2 2026 includes AI inference traffic",
            chart_categories=["Q3 24", "Q4 24", "Q1 25", "Q2 25", "Q3 25E"],
            chart_series=[
                _cs("API Gateway", (1.2, 1.6, 2.1, 2.8, 3.6)),
                _cs("CDN / Static", (0.8, 1.0, 1.3, 1.7, 2.2)),
                _cs("AI Inference", (0.0, 0.0, 0.2, 0.6, 1.4)),
            ],
            notes="AI inference is the fastest-growing workload class.",
        ),
        # 5 two_column ─ current vs target architecture
        Slide(
            layout="two_column",
            layout_intent="comparison",
            title="Current vs. Target Architecture",
            title_icon="ui.layout",
            bullets_left=[
                "Monolithic Postgres: 14TB, single writer",
                "Synchronous inter-service calls, no circuit breaker",
                "Manual Kubernetes YAML per team",
                "No central observability — 6 isolated stacks",
            ],
            bullets_left_icons=["status.fail", "status.fail", "status.warning", "status.warning"],
            bullets_right=[
                "Sharded Postgres + read replicas per domain",
                "Async event mesh (Kafka) with retry semantics",
                "Unified Helm chart factory, GitOps CI",
                "OpenTelemetry → Grafana Stack centralised",
            ],
            bullets_right_icons=["status.success", "tech.api", "tech.branch", "security.eye"],
        ),
        # 6 chart_line ─ p99 latency
        Slide(
            layout="chart_line",
            layout_intent="metrics_trend",
            title="API P99 Latency — ms",
            subtitle="SLO = 200ms; shading shows SLO breach weeks",
            chart_categories=["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8"],
            chart_series=[
                _cs("Checkout API", (178.0, 184.0, 201.0, 231.0, 248.0, 263.0, 244.0, 229.0)),
                _cs("Auth API", (92.0, 91.0, 94.0, 97.0, 102.0, 98.0, 95.0, 93.0)),
                _cs("SLO Target", (200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0)),
            ],
            notes="Checkout API breach started when DB connection pool saturated.",
        ),
        # 7 section ─ reliability
        Slide(
            layout="section",
            layout_intent="chapter_break",
            title="Reliability Engineering",
            title_color_hex="059669",
        ),
        # 8 title_content ─ incident analysis, image corner
        Slide(
            layout="title_content",
            layout_intent="narrative",
            title="Q2 Incident Deep-Dive",
            title_icon="tech.bug",
            bullets=[
                "SEV-1 (May 12): DB deadlock cascade — 47-min MTTR, $1.4M revenue impact",
                "SEV-2 (May 28): CDN misconfiguration — 112-min MTTR, 18% traffic black-holed",
                "SEV-2 (Jun 9): Auth service OOM loop — 68-min MTTR, 34K user logouts",
                "Common theme: missing runbooks and poor alert signal-to-noise",
            ],
            bullet_icons=["status.fail", "status.warning", "status.warning", "meta.lightbulb"],
            images=[_img("incident", "accent_corner", "Incident timeline Q2 2026")],
        ),
        # 9 two_column ─ SRE bets
        Slide(
            layout="two_column",
            layout_intent="comparison",
            title="SRE Investment Priorities H2",
            title_icon="tech.gear",
            bullets_left=[
                "Reliability (immediate)",
                "Circuit breaker on all downstream calls",
                "Automated DB failover ≤ 60 s",
                "On-call runbook coverage 100%",
                "SLO dashboard for all P0 services",
            ],
            bullets_left_icons=[None, "status.success", "time.clock", "research.document", "data.dashboard"],
            bullets_right=[
                "Efficiency (Q4)",
                "Spot instance migration for batch jobs",
                "Cache-aside layer for top 20 hot paths",
                "Unified cost attribution tagging",
                "FinOps weekly review cadence",
            ],
            bullets_right_icons=[None, "commerce.money", "data.filter", "data.table", "time.calendar"],
            notes="Circuit breaker work starts sprint 1 — no dependencies.",
        ),
        # 10 chart_bar ─ error budget consumption
        Slide(
            layout="chart_bar",
            layout_intent="metrics_bar",
            title="Error Budget Consumption by Service — %",
            subtitle="Q2 2026 | 30-day rolling | 99.9% SLO = 43.8 min downtime budget",
            chart_categories=["Checkout", "Auth", "Catalog", "Payments", "Notifications"],
            chart_series=[
                _cs("Budget Consumed", (218.0, 34.0, 12.0, 71.0, 8.0)),
                _cs("Budget Remaining", (0.0, 66.0, 88.0, 29.0, 92.0)),
            ],
            notes="Checkout is in overage — freeze all non-reliability feature work.",
        ),
        # 11 title_content ─ platform roadmap
        Slide(
            layout="title_content",
            layout_intent="narrative",
            title="Platform Team Roadmap",
            title_icon="time.calendar",
            bullets=[
                "July: Kafka event mesh MVP — Checkout and Auth services migrated",
                "August: Read replica sharding — DB load reduced by estimated 65%",
                "September: OpenTelemetry rollout complete — all P0 services instrumented",
                "October: GitOps factory shipped — team toil reduction 4 hr/eng/week",
                "November: Cost attribution v1 — per-service cloud cost visible to eng leads",
            ],
            bullet_icons=[
                "tech.api",
                "tech.cpu",
                "security.eye",
                "tech.branch",
                "commerce.money",
            ],
            images=[_img("roadmap", "primary_right", "Platform engineering roadmap board")],
        ),
        # 12 section ─ developer experience
        Slide(
            layout="section",
            layout_intent="chapter_break",
            title="Developer Experience (DX)",
            title_color_hex="059669",
        ),
        # 13 chart_line ─ deployment frequency
        Slide(
            layout="chart_line",
            layout_intent="metrics_trend",
            title="Deployment Frequency — Deploys per Week",
            subtitle="DORA metrics tracking; target ≥ 50 deploys/week by Q4",
            chart_categories=["Q1 24", "Q2 24", "Q3 24", "Q4 24", "Q1 25", "Q2 25"],
            chart_series=[
                _cs("Production deploys", (18.0, 21.0, 24.0, 28.0, 33.0, 37.0)),
                _cs("Staging deploys", (42.0, 48.0, 51.0, 56.0, 61.0, 68.0)),
            ],
        ),
        # 14 two_column ─ dx wins vs debt
        Slide(
            layout="two_column",
            layout_intent="comparison",
            title="Developer Experience: Wins vs. Outstanding Debt",
            bullets_left=[
                "Wins this quarter",
                "PR-to-merge p50: 6.2h → 3.8h",
                "Test suite: 8-min p99 → 4.1 min",
                "Monorepo migration: 80% complete",
            ],
            bullets_left_icons=[None, "status.success", "status.success", "status.success"],
            bullets_right=[
                "Remaining tech debt",
                "Local dev env: 40-min setup still too slow",
                "Flaky tests: 3.8% flake rate vs 1% target",
                "Docs coverage: 52% public APIs documented",
            ],
            bullets_right_icons=[None, "status.warning", "tech.bug", "research.document"],
        ),
        # 15 title_content ─ toolchain
        Slide(
            layout="title_content",
            layout_intent="narrative",
            title="Approved Toolchain 2026",
            title_icon="tech.gear",
            bullets=[
                "Orchestration: Kubernetes 1.31 + Crossplane for cloud resources",
                "CI/CD: GitHub Actions → ArgoCD (GitOps), branch deploy on PR",
                "Observability: OpenTelemetry SDK + Grafana Cloud (traces, metrics, logs)",
                "Service Mesh: Istio for mTLS, traffic shaping, and circuit breaking",
                "IaC: Terraform + Terragrunt, modules published to internal registry",
            ],
            bullet_icons=[
                "tech.cloud",
                "tech.branch",
                "security.eye",
                "security.lock",
                "tech.gear",
            ],
        ),
        # 16 section ─ security & compliance
        Slide(
            layout="section",
            layout_intent="chapter_break",
            title="Security & Compliance",
            title_color_hex="059669",
        ),
        # 17 title_content ─ security posture
        Slide(
            layout="title_content",
            layout_intent="narrative",
            title="Security Posture Report",
            title_icon="security.shield",
            bullets=[
                "SOC 2 Type II surveillance audit: PASSED — no exceptions (June 2026)",
                "SAST/DAST integrated in CI: 98% coverage on P0 repositories",
                "Secret scanning: 4 accidental credential leaks detected & rotated Q2",
                "Pen test Q1: 2 high findings closed; 0 critical findings",
                "Supply chain: SBOM generated for all container images from Q3",
            ],
            bullet_icons=[
                "status.success",
                "security.shield",
                "security.key",
                "status.warning",
                "research.document",
            ],
            images=[_img("security", "accent_corner", "SOC 2 audit report June 2026")],
        ),
        # 18 two_column ─ zero-trust roadmap
        Slide(
            layout="two_column",
            layout_intent="comparison",
            title="Zero-Trust Implementation Progress",
            title_icon="security.lock",
            bullets_left=[
                "Completed",
                "mTLS between all services (Istio)",
                "OIDC SSO for all internal tools",
                "Workload identity federation (GCP)",
            ],
            bullets_left_icons=[None, "status.success", "status.success", "status.success"],
            bullets_right=[
                "In progress / planned",
                "Device posture enforcement (Q3)",
                "Privileged Access Workstation rollout",
                "FIDO2 hardware key for Tier-1 ops",
            ],
            bullets_right_icons=[None, "time.clock", "time.clock", "time.calendar"],
        ),
        # 19 chart_bar ─ cloud cost by service
        Slide(
            layout="chart_bar",
            layout_intent="metrics_bar",
            title="Cloud Spend by Service — $K / Month",
            subtitle="Q2 2025 actuals; target 20% reduction by Q4",
            chart_categories=["Compute", "Storage", "Data Transfer", "Managed DB", "AI / ML"],
            chart_series=[
                _cs("Q2 2025 Actual", (142.0, 38.0, 27.0, 94.0, 61.0)),
                _cs("Q4 Target", (110.0, 34.0, 22.0, 78.0, 70.0)),
            ],
            notes="Managed DB most impactful — read replica migration saves ~$16K/mo.",
        ),
        # 20 title_content ─ closing asks
        Slide(
            layout="title_content",
            layout_intent="narrative",
            title="Platform Team: What We Need",
            title_icon="nav.target",
            bullets=[
                "Headcount: 2 senior SREs (approved in H2 plan) — start recruiting immediately",
                "Budget: $180K for observability tooling (Grafana Cloud Enterprise tier)",
                "Priority freeze: Checkout service — reliability-only sprints until SLO green",
                "Exec sponsor: VP Eng to attend weekly platform review for 8 weeks",
            ],
            bullet_icons=["people.team", "commerce.money", "status.blocked", "people.voice"],
            notes="Platform health = product velocity. Thank you — questions welcome.",
        ),
    ]

    return Deck(
        title="Meridian Engineering — Platform Architecture Review Q3 2026",
        subtitle="Engineering All-Hands Confidential · Internal Only",
        author="Meridian Platform Team",
        audience=AudienceProfile(technical_level="technical", attention_span="long"),
        theme=th,
        slides=slides,
    )


# ---------------------------------------------------------------------------
# Deck 3 — Nova Commerce: 2026 Product Launch
# ---------------------------------------------------------------------------

def deck_nova_launch() -> Deck:
    """20-slide product launch deck — marketing / GTM audience, visual & punchy."""
    th = DeckTheme(primary_hex="4F46E5", accent_hex="EC4899", muted_hex="6B7280")

    slides: list[Slide] = [
        # 1 title ─ cover, banner image
        Slide(
            layout="title",
            layout_intent="opening",
            title="Nova Commerce 3.0",
            subtitle="Intelligent commerce — built for the era of ambient buying",
            title_icon="status.new",
            notes="15-min lightning pitch for press briefing, then 10-min Q&A.",
            images=[_img("productlaunch", "banner_lower", "Nova 3.0 — shipping Q3 2026")],
        ),
        # 2 section ─ the problem
        Slide(
            layout="section",
            layout_intent="chapter_break",
            title="The Problem We Solve",
            title_color_hex="4F46E5",
        ),
        # 3 title_content ─ why ecommerce is broken
        Slide(
            layout="title_content",
            layout_intent="narrative",
            title="Today's Commerce Is Fragmented & Frictionless",
            title_icon="meta.question",
            bullets=[
                "Average checkout abandonment 72% — buyers lose intent mid-flow",
                "7 different platforms to run one storefront: ERP, PIM, OMS, WMS, CRM, CX, analytics",
                "Returns cost 2× fulfilment — wrong size, wrong expectation, wrong product",
                "Personalisation feels creepy, not helpful — conversion lift rarely exceeds 3%",
                "AI tools bolted on post-hoc — not native to the commerce stack",
            ],
            bullet_icons=[
                "data.trend_down",
                "tech.gear",
                "commerce.cart",
                "people.person",
                "tech.api",
            ],
        ),
        # 4 chart_bar ─ market pain points
        Slide(
            layout="chart_bar",
            layout_intent="metrics_bar",
            title="Top Merchant Pain Points — % Citing as Critical",
            subtitle="Nova Commerce Merchant Survey 2026 | n = 2,400",
            chart_categories=["Checkout UX", "Inventory Sync", "AI / Personalise", "Returns", "Cost"],
            chart_series=[
                _cs("Mid-Market Merchants", (68.0, 54.0, 71.0, 48.0, 62.0)),
                _cs("Enterprise Merchants", (52.0, 79.0, 65.0, 81.0, 44.0)),
            ],
        ),
        # 5 section ─ introducing nova 3.0
        Slide(
            layout="section",
            layout_intent="chapter_break",
            title="Introducing Nova Commerce 3.0",
            title_color_hex="4F46E5",
        ),
        # 6 two_column ─ before vs after
        Slide(
            layout="two_column",
            layout_intent="comparison",
            title="Commerce Before and After Nova 3.0",
            title_icon="meta.spark",
            bullets_left=[
                "Before Nova 3.0",
                "Static product pages, same for everyone",
                "Rule-based promotions, manually configured",
                "Returns processed 5–10 days",
                "Inventory oversell a weekly occurrence",
            ],
            bullets_left_icons=[None, "status.fail", "status.fail", "status.warning", "status.warning"],
            bullets_right=[
                "With Nova 3.0",
                "Ambient AI: page adapts to each session",
                "Intent signals → promotion in real time",
                "AI triage + label print in 90 seconds",
                "Unified inventory graph, real-time sync",
            ],
            bullets_right_icons=[None, "status.new", "meta.lightbulb", "status.success", "status.success"],
        ),
        # 7 title_content ─ core capabilities, image right
        Slide(
            layout="title_content",
            layout_intent="visual_emphasis",
            title="Five Core Capabilities",
            title_icon="ui.layout",
            bullets=[
                "Ambient Storefronts: AI-rendered pages, no template editing",
                "Unified Commerce Graph: one data model across all channels",
                "Intelligent Returns: vision AI classifies condition in seconds",
                "Real-Time Inventory: sub-second sync across 50+ fulfilment nodes",
                "Commerce Copilot: conversational merchandising for ops teams",
            ],
            bullet_icons=[
                "status.new",
                "tech.api",
                "meta.lightbulb",
                "data.dashboard",
                "people.voice",
            ],
            images=[_img("productui", "primary_right", "Nova 3.0 Ambient Storefront — live demo")],
        ),
        # 8 chart_line ─ conversion lift
        Slide(
            layout="chart_line",
            layout_intent="metrics_trend",
            title="Conversion Lift — Beta Merchant Results",
            subtitle="100-day rolling average; 42 beta merchants · Q1–Q2 2026",
            chart_categories=["Week 1", "Week 4", "Week 8", "Week 12", "Week 16"],
            chart_series=[
                _cs("Ambient Storefront uplift %", (0.0, 1.2, 2.8, 4.1, 5.7)),
                _cs("Checkout conversion uplift %", (0.0, 0.8, 1.9, 3.2, 4.4)),
                _cs("AOV uplift %", (0.0, 1.6, 2.4, 3.8, 5.1)),
            ],
            notes="5.7% Ambient uplift alone justifies Nova 3.0 at our price point.",
        ),
        # 9 quote ─ beta merchant
        Slide(
            layout="quote",
            layout_intent="pull_quote",
            quote="Nova's ambient storefront cut our A/B test cycle from 3 weeks to 2 hours. We shipped 48 personalisation experiments in Q1 that would have taken the full year before.",
            attribution="Head of Digital, Top-10 European Sports Retailer",
            images=[_img("retail", "accent_corner")],
        ),
        # 10 section ─ go to market
        Slide(
            layout="section",
            layout_intent="chapter_break",
            title="Go-to-Market Strategy",
            title_color_hex="4F46E5",
        ),
        # 11 title_content ─ pricing
        Slide(
            layout="title_content",
            layout_intent="narrative",
            title="Pricing & Packaging",
            title_icon="commerce.money",
            bullets=[
                "Growth ($499/mo): Ambient Storefronts + Unified Graph + 3 channels",
                "Scale ($1,499/mo): + Real-Time Inventory + Commerce Copilot + 10 channels",
                "Enterprise (custom): + Intelligent Returns + SLA + dedicated onboarding",
                "All plans: unlimited SKUs, no GMV fees, 30-day free trial",
            ],
            bullet_icons=[
                "status.success",
                "data.trend_up",
                "people.team",
                "status.new",
            ],
        ),
        # 12 two_column ─ channel strategy
        Slide(
            layout="two_column",
            layout_intent="comparison",
            title="Channel Strategy",
            title_icon="nav.target",
            bullets_left=[
                "Direct (ACV > $12K)",
                "Outbound AE team: 120 mid-market targets",
                "Inbound from content + community",
                "Annual deals with CSM coverage",
            ],
            bullets_left_icons=[None, "people.person", "meta.lightbulb", "people.team"],
            bullets_right=[
                "Partner & Marketplace",
                "Shopify Plus app: 600K merchant reach",
                "Salesforce AppExchange listing",
                "System integrator co-sell (Accenture, PwC)",
            ],
            bullets_right_icons=[None, "commerce.cart", "tech.api", "people.handshake"],
        ),
        # 13 chart_bar ─ pipeline build
        Slide(
            layout="chart_bar",
            layout_intent="metrics_bar",
            title="H2 2026 Pipeline Build — $M ARR",
            subtitle="Weighted pipeline by channel and deal stage",
            chart_categories=["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            chart_series=[
                _cs("Direct AE", (1.8, 2.4, 3.1, 3.8, 4.6, 5.5)),
                _cs("Partner Co-sell", (0.4, 0.7, 1.1, 1.6, 2.3, 3.1)),
                _cs("Self-serve Upgrade", (0.2, 0.4, 0.6, 0.9, 1.3, 1.8)),
            ],
        ),
        # 14 title_content ─ launch partners
        Slide(
            layout="title_content",
            layout_intent="visual_emphasis",
            title="Launch Day Ecosystem Partners",
            title_icon="people.handshake",
            bullets=[
                "Payment: Stripe + Adyen dual-support, 180 local payment methods",
                "Logistics: ShipBob, Fulfil.io, Amazon Multi-Channel natively integrated",
                "Tax: Avalara real-time tax calculation in checkout flow",
                "Data: Snowflake data sharing app for merchant analytics",
                "AI: OpenAI GPT-4o powers Commerce Copilot under the hood",
            ],
            bullet_icons=[
                "commerce.card",
                "commerce.cart",
                "security.shield",
                "data.dashboard",
                "meta.lightbulb",
            ],
            images=[_img("partners", "accent_corner", "Day-1 integration partners")],
        ),
        # 15 chart_line ─ MRR forecast
        Slide(
            layout="chart_line",
            layout_intent="metrics_trend",
            title="MRR Growth Forecast — $M",
            subtitle="Conservative · Base · Optimistic scenarios",
            chart_categories=["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            chart_series=[
                _cs("Conservative", (0.5, 1.0, 1.8, 2.8, 4.0, 5.4)),
                _cs("Base Case", (0.7, 1.5, 2.6, 4.1, 5.9, 8.0)),
                _cs("Optimistic", (1.0, 2.2, 4.0, 6.5, 9.4, 12.8)),
            ],
            notes="Base case assumes 14 enterprise logos and 280 self-serve converts by EOY.",
        ),
        # 16 section ─ product roadmap
        Slide(
            layout="section",
            layout_intent="chapter_break",
            title="What's Coming Next",
            title_color_hex="4F46E5",
        ),
        # 17 two_column ─ Q4 vs 2027 roadmap
        Slide(
            layout="two_column",
            layout_intent="comparison",
            title="Roadmap: Q4 2026 vs H1 2027",
            title_icon="time.calendar",
            bullets_left=[
                "Q4 2026",
                "Mobile Ambient: PWA + native iOS / Android",
                "Social Commerce: TikTok Shop, Reels checkout",
                "B2B Portal: net-terms, quote-to-order",
                "Headless GraphQL API v3 GA",
            ],
            bullets_left_icons=[None, "ui.mobile", "people.voice", "people.team", "tech.api"],
            bullets_right=[
                "H1 2027",
                "Voice Commerce: Alexa + Google Home",
                "AR Try-On: WebXR product visualisation",
                "Autonomous Merchandising: AI-managed catalogue",
                "International: JP, BR, IN localisation",
            ],
            bullets_right_icons=[None, "meta.lightbulb", "ui.accessibility", "status.new", "nav.pin"],
        ),
        # 18 title_content ─ design system
        Slide(
            layout="title_content",
            layout_intent="visual_emphasis",
            title="Nova Design System 3.0",
            title_icon="ui.palette",
            bullets=[
                "140 accessible components — WCAG 2.2 AA by default",
                "Motion library: 60 micro-interactions, GPU-accelerated",
                "Figma ↔ Code sync: tokens published via Style Dictionary",
                "Dark mode, RTL, and 12-column grid out of the box",
                "Open source under MIT — community contributions welcome",
            ],
            bullet_icons=[
                "ui.accessibility",
                "status.new",
                "ui.palette",
                "ui.layout",
                "tech.branch",
            ],
            images=[_img("designsystem", "primary_right", "Nova Design System component library")],
        ),
        # 19 title_content ─ proof points
        Slide(
            layout="title_content",
            layout_intent="narrative",
            title="Early Proof Points",
            title_icon="data.chart",
            bullets=[
                "42 beta merchants across EU, US, AU — median 4.7% conversion lift",
                "8,600 hours of merchant testing = 3 years of feedback in one cycle",
                "NPS 74 on beta — vs industry benchmark 38 for commerce platforms",
                "0 critical bugs shipped to production in 6-month beta window",
                "99.99% uptime across all beta merchants — zero SLA breaches",
            ],
            bullet_icons=[
                "people.team",
                "time.clock",
                "status.success",
                "status.success",
                "security.shield",
            ],
        ),
        # 20 title_content ─ call to action
        Slide(
            layout="title_content",
            layout_intent="visual_emphasis",
            title="Start Your Nova 3.0 Journey",
            title_icon="commerce.rocket",
            bullets=[
                "Free trial: nova.io/trial — no credit card, 30 days, full feature access",
                "Press briefing: request a one-on-one with our CPO this week",
                "Partner enquiries: partnerships@nova.io — fast-track review available",
                "Open source community: github.com/nova-commerce/nova — star us ⭐",
            ],
            bullet_icons=[
                "status.success",
                "people.voice",
                "people.handshake",
                "tech.branch",
            ],
            images=[_img("calltoaction", "banner_lower", "Nova 3.0 — shipping Q3 2026")],
        ),
    ]

    return Deck(
        title="Nova Commerce 3.0 — Product Launch 2026",
        subtitle="Press Briefing Deck · Embargo Until 00:01 PST July 22 2026",
        author="Nova Commerce Product Team",
        audience=AudienceProfile(technical_level="general", attention_span="medium"),
        theme=th,
        slides=slides,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    decks = [
        (deck_apex_strategy,  "sample-apex-strategy-2026"),
        (deck_meridian_platform, "sample-meridian-platform-2026"),
        (deck_nova_launch, "sample-nova-launch-2026"),
    ]

    for fn, name in decks:
        print(f"\nBuilding {name}…")
        deck = fn()
        _write(deck, name)

    print("\nDone. Validate with:")
    for _, name in decks:
        print(f"  uv run zpresenter check examples/samples/{name}.json")


if __name__ == "__main__":
    main()
