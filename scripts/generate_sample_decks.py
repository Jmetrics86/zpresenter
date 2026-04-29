#!/usr/bin/env python3
"""Generate large showcase decks under examples/samples/. Run from repo root: uv run python scripts/generate_sample_decks.py"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from zpresenter.models import AudienceProfile, ChartSeries, Deck, DeckTheme, Slide

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "examples" / "samples"
SCHEMA_REF = "../../schemas/deck.schema.json"


def generation_stamp() -> str:
    """Wall-clock stamp embedded in deck titles when samples are generated."""
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def _write(deck: Deck, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    payload = deck.model_dump(mode="json")
    payload["$schema"] = SCHEMA_REF
    path = OUT / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)} ({len(deck.slides)} slides)")


def _cs(name: str, values: tuple[float, ...]) -> ChartSeries:
    return ChartSeries(name=name, values=list(values))


def deck_product_launch(stamp: str) -> Deck:
    """B2B SaaS / GTM narrative with charts and split views."""
    th = DeckTheme(primary_hex="1D4ED8", accent_hex="059669")
    slides: list[Slide] = [
        Slide(
            layout="title",
            title=f"Orbit Commerce Cloud · {stamp}",
            subtitle="FY26 product narrative · enterprise GTM · design system beta",
            notes="Establish North Star; 18 min to Part II demos.",
        ),
        Slide(
            layout="section",
            title="Executive framing",
            notes="Pause for CFO alignment question.",
            title_color_hex="1D4ED8",
        ),
        Slide(
            layout="title_content",
            title="Why now",
            bullets=[
                "Composable storefront APIs overtaking monolithic suites (EU mid-market surge)",
                "Checkout latency tied directly to conversion — infra budgets unlocking",
                "Partners asking for reference architectures they can stamp repeatedly",
                "Board mandate: predictable gross margin expansion without hiring spike",
            ],
            notes="Anchor all bullets with EU datapoints only if speaking to EU buyers.",
        ),
        Slide(
            layout="two_column",
            title="Buyer vs champion tensions",
            bullets_left=[
                "CIO: sovereignty + SSO everywhere",
                "CFO: COGS visibility per SKU lane",
                "CISO: blast-radius budgets per tenant shard",
                "RevOps: Salesforce hygiene before rollout",
            ],
            bullets_right=[
                "VP Eng: typed SDK + staged rollouts",
                "VP Product: experimentation guardrails",
                "Design: tokens parity across white-label tenants",
                "Support: searchable incident timelines",
            ],
            notes="Pairwise role-play breakout optional.",
        ),
        Slide(
            layout="section",
            title="Market motion",
            title_color_hex="1D4ED8",
        ),
        Slide(
            layout="chart_bar",
            title="Pipeline creation ($M)",
            subtitle="Rolling 4 quarters · blended segments",
            chart_categories=["Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25"],
            chart_series=[
                _cs("Enterprise", (4.2, 5.1, 6.0, 7.4)),
                _cs("Mid-market", (2.8, 3.2, 3.9, 4.6)),
                _cs("Starter", (1.1, 1.4, 1.7, 2.0)),
            ],
            notes="Animate bars left-to-right; call out enterprise acceleration.",
        ),
        Slide(
            layout="chart_line",
            title="Net retention cohort curve",
            subtitle="Trailing twelve months · logo cohort FY23",
            chart_categories=["M3", "M6", "M9", "M12", "M15", "M18"],
            chart_series=[
                _cs("NRR %", (108.0, 115.0, 121.0, 127.0, 129.0, 131.0)),
                _cs("Expansion ARR indexed", (100.0, 118.0, 132.0, 148.0, 154.0, 159.0)),
            ],
            notes="Emphasize stabilization post Month 12.",
        ),
        Slide(
            layout="title_content",
            title="Segment wedges",
            bullets=[
                "Retail grocery chains adopting endless aisle orchestration (+42% YoY logos)",
                "Industrial distributors syncing ERP ATP signals nightly",
                "Marketplaces consolidating payouts through layered PSP adapters",
                "Healthcare GPO pilots held on compliance review (timeline: H2)",
            ],
        ),
        Slide(
            layout="section",
            title="Solution architecture",
            title_color_hex="1D4ED8",
        ),
        Slide(
            layout="two_column",
            title="Control plane vs data plane",
            bullets_left=[
                "Routing: global policy engine + circuit breakers",
                "Tenancy: shard maps + blast isolation budgets",
                "Release: progressive exposure + synthetic probes",
                "Secrets: KMS envelopes per region pair",
            ],
            bullets_right=[
                "Checkout hot path microservices only",
                "Fulfillment adapters behind bulkheads",
                "Observability: RED metrics per bounded context",
                "Replay journals for settlement discrepancies",
            ],
        ),
        Slide(
            layout="title_content",
            title="Differentiators",
            bullets=[
                "Native GraphQL federation + declarative storefront schemas",
                "Edge SSR cache keyed by personalization cohort hash",
                "Built-in experimentation hooks without checkout regressions",
                "SOC2 Type II + PCI DSS SAQ-D roadmap packaged",
            ],
        ),
        Slide(
            layout="chart_bar",
            title="Latency reduction program",
            subtitle="p95 checkout · milliseconds",
            chart_categories=["Baseline", "Wave A", "Wave B", "Wave C"],
            chart_series=[
                _cs("Mobile web", (980.0, 720.0, 540.0, 410.0)),
                _cs("Desktop", (620.0, 480.0, 390.0, 310.0)),
            ],
        ),
        Slide(
            layout="quote",
            quote="Latency is the silent churn lever nobody invoices.",
            attribution="Field CTO diary",
            notes="Pause beat — room calibration.",
        ),
        Slide(
            layout="section",
            title="Go-to-market plays",
            title_color_hex="1D4ED8",
        ),
        Slide(
            layout="two_column",
            title="FY26 campaigns",
            bullets_left=[
                "Northstar lighthouse rev share + exec briefing cadence",
                "Embedded Solutions Engineer pods per strategic logo",
                "Partner certifications refreshed quarterly",
                "Regional exec dinners paired with architecture studios",
            ],
            bullets_right=[
                "Hands-on sandbox clusters auto-teardown nightly",
                "ROI simulator worksheet packaged with AE toolkit",
                "Self-serve SKU ladder simplified (Starter anchor skew)",
                "Community hack weekends co-hosted with GSIs",
            ],
        ),
        Slide(
            layout="title_content",
            title="Pricing snapshot",
            bullets=[
                "Platform fee stepping down after $50M GMV processed annually",
                "Burst overage pooled across child stores (franchise friendly)",
                "Premium support: named TAM + Slack bridge with SRE rotator",
                "Optional white-glove migrations priced as fixed phases (scoping worksheet v3)",
            ],
        ),
        Slide(
            layout="chart_line",
            title="Win rate vs technical eval depth",
            subtitle="Opportunities closed-won FY25 · %",
            chart_categories=["1 workshop", "2 workshops", "POC", "POC + perf", "POC + security"],
            chart_series=[_cs("Win rate", (22.0, 31.0, 44.0, 58.0, 67.0))],
        ),
        Slide(
            layout="section",
            title="Execution risks",
            title_color_hex="1D4ED8",
        ),
        Slide(
            layout="title_content",
            title="What could break the plan",
            bullets=[
                "PSP routing changes in EU regulatory pilots (watch EBA drafts weekly)",
                "Long-running ERP cutover weekends colliding with Black Friday freeze",
                "GPU-adjacent personalization features inflating edge COGS if unbounded",
                "Channel conflict if marketplace partnerships outpace direct coverage maps",
            ],
        ),
        Slide(
            layout="two_column",
            title="Mitigations",
            bullets_left=[
                "Exec war-room cadence during freeze windows",
                "Playbooks for PSP rollback + shadow traffic mode",
                "COGS guardrails on personalization compute burst",
            ],
            bullets_right=[
                "Territory pairing rules refreshed each quarter",
                "Customer advisory board gate for roadmap commitments",
                "Partner scorecards published internally monthly",
            ],
        ),
        Slide(
            layout="section",
            title="Customer proof & expansion",
            title_color_hex="1D4ED8",
        ),
        Slide(
            layout="title_content",
            title="Logo highlights FY25",
            bullets=[
                "Three global grocers live on unified catalog + endless aisle orchestration",
                "Two industrial distributors exposing ATP APIs to storefront experiments",
                "One marketplace migrated PSP routing without weekend downtime",
                "Healthcare GPO sandbox awaiting IRB clearance for PHI-light feeds",
            ],
        ),
        Slide(
            layout="two_column",
            title="Land → expand motions",
            bullets_left=[
                "Land: sandbox parity checklist + SSO bake-off scripts",
                "Land: ROI worksheet tied to SKU throughput assumptions",
                "Land: exec sponsor alignment memo template",
            ],
            bullets_right=[
                "Expand: experimentation tier unlock post-NRR checkpoint",
                "Expand: franchise analytics tenant rollup dashboards",
                "Expand: GSIs embedding Solutions Engineer pods quarterly",
            ],
        ),
        Slide(
            layout="chart_bar",
            title="Expansion ARR · $M cum.",
            subtitle="Within Year 1 of first production traffic",
            chart_categories=["T1", "T2", "T3", "T4"],
            chart_series=[
                _cs("Retail", (0.9, 2.1, 3.8, 5.6)),
                _cs("Industrial", (0.7, 1.6, 2.9, 4.2)),
                _cs("Marketplaces", (1.2, 2.4, 3.7, 5.1)),
            ],
        ),
        Slide(
            layout="title_content",
            title="Professional services overlay",
            bullets=[
                "Migration factory templates reduced median cutover window from 14 → 9 weekends",
                "Executive training simulator packaged as SCORM + embedded analytics hooks",
                "Partner certification tracks refreshed after SDK major version bump",
                "Paid architecture studios capped at six concurrent global engagements",
            ],
        ),
        Slide(
            layout="chart_line",
            title="Support ticket severity mix",
            subtitle="% of tickets · rolling 90d",
            chart_categories=["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            chart_series=[
                _cs("Sev1", (4.1, 3.8, 3.2, 2.9, 2.6, 2.4)),
                _cs("Sev2", (18.0, 17.2, 16.5, 15.9, 15.2, 14.8)),
            ],
        ),
        Slide(
            layout="two_column",
            title="Product analytics instrumentation",
            bullets_left=[
                "Checkout funnel spans unified trace IDs across edge + origin",
                "Feature flags audited nightly against experimentation registry",
                "Synthetic probes cover top 40 merchant SKU bundles",
            ],
            bullets_right=[
                "Replay snapshots scrubbed before leaving tenant boundary",
                "Dashboards embedded in Salesforce opportunity stages",
                "On-call paging thresholds tuned per merchant tier",
            ],
        ),
        Slide(
            layout="quote",
            quote="Ship the narrative with the numbers tied to bones, not slogans.",
            attribution="Closing guidance",
        ),
        Slide(
            layout="title_content",
            title="Next steps",
            bullets=[
                "Book three lighthouse design critiques (pick from shortlist)",
                "Confirm legal redlines on data processing addendum by EOM",
                "Align QBR storyline with freshly locked financial model v4.2",
            ],
            notes="Assign DRI per bullet before leaving room.",
        ),
    ]
    return Deck(
        title=f"Orbit Commerce Cloud · FY26 · {stamp}",
        subtitle="Showcase narrative",
        author="ZPresenter samples",
        audience=AudienceProfile(technical_level="technical", attention_span="long"),
        theme=th,
        slides=slides,
    )


def deck_clinical_evidence(stamp: str) -> Deck:
    """Evidence / outcomes review with dense two-column scrutiny."""
    th = DeckTheme(primary_hex="0F766E", accent_hex="D97706")
    cat_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    slides: list[Slide] = [
        Slide(
            layout="title",
            title=f"CLEAR-302 outcomes programme · {stamp}",
            subtitle="Phase III interim · efficacy · safety · operational readiness",
            notes="Audience: sponsor steering committee — stick to slide timings.",
        ),
        Slide(layout="section", title="Trial posture", title_color_hex="0F766E"),
        Slide(
            layout="title_content",
            title="Study synopsis",
            bullets=[
                "Randomized, double-blind, placebo-controlled multicenter trial (n=1,842)",
                "Primary endpoint: sustained responder rate at Week 24 (central reads)",
                "Key secondary: biomarker suppression score delta vs baseline",
                "Safety surveillance intensity escalated after interim DSMB charter revision",
            ],
        ),
        Slide(
            layout="two_column",
            title="Population ingress criteria",
            bullets_left=[
                "Adults 18–75 with diagnostic Grade II–III severity",
                "Washout windows enforced per protocol Amendment 4",
                "Stable background meds documented ≥90 days prior",
                "HbA1c corridor eligibility unchanged vs CLEAR-215",
            ],
            bullets_right=[
                "Exclude active malignancy within 24 months",
                "Exclude transplant recipients",
                "Exclude concurrent investigational agents",
                "Exclude QT prolongation beyond protocol thresholds",
            ],
        ),
        Slide(
            layout="chart_bar",
            title="Enrollment velocity · subjects / month",
            subtitle="Sites activated vs screened",
            chart_categories=cat_months,
            chart_series=[
                _cs("Activated sites", (12.0, 18.0, 24.0, 31.0, 36.0, 41.0)),
                _cs("Screened subjects", (44.0, 71.0, 103.0, 138.0, 164.0, 188.0)),
            ],
        ),
        Slide(layout="section", title="Efficacy signals", title_color_hex="0F766E"),
        Slide(
            layout="chart_line",
            title="Responder trajectory · central reads",
            subtitle="ITT population · % achieving threshold",
            chart_categories=["Week 4", "Week 8", "Week 12", "Week 16", "Week 20", "Week 24"],
            chart_series=[
                _cs("Arm A", (18.0, 31.0, 42.0, 48.0, 53.0, 57.0)),
                _cs("Arm B", (11.0, 19.0, 26.0, 31.0, 34.0, 36.0)),
            ],
        ),
        Slide(
            layout="title_content",
            title="Biomarker narrative",
            bullets=[
                "Median hs-CRP reduction −38% vs −12% placebo (exploratory hierarchy preserved)",
                "Protein signature panel trending toward pre-specified composite",
                "Subgroup forest: consistency across geography except APAC enrollment lag",
            ],
        ),
        Slide(
            layout="two_column",
            title="Sensitivity analyses",
            bullets_left=[
                "Per-protocol set: directional alignment with ITT",
                "Missing at random sensitivity: tipping point tables updated",
                "Multiple imputation scenario C: marginal effect attenuation ≤1.2 pp",
            ],
            bullets_right=[
                "COVID-era site pause stratum: attenuation noted (pre-registered)",
                "Stratification by baseline severity bucket: HR still favorable",
                "Interim look alpha spend within O'Brien-Fleming boundaries",
            ],
        ),
        Slide(layout="section", title="Safety", title_color_hex="0F766E"),
        Slide(
            layout="chart_bar",
            title="TEAE incidence · % of subjects",
            subtitle="Treatment emergent · relatedness adjudicated",
            chart_categories=["GI", "Renal", "Hepatic", "Cardio", "Neuro"],
            chart_series=[
                _cs("Arm A", (12.4, 3.1, 2.2, 4.0, 1.5)),
                _cs("Placebo", (10.9, 2.8, 1.9, 3.6, 1.7)),
            ],
        ),
        Slide(
            layout="title_content",
            title="Adjudicated SAE narrative",
            bullets=[
                "Two SAE clusters reviewed by blinded neurology council (resolved per protocol)",
                "No imbalance in QTcF beyond prespecified surveillance grid",
                "Hepatic signal flat vs internal historical control deck",
            ],
        ),
        Slide(layout="section", title="Exploratory pharmacokinetics", title_color_hex="0F766E"),
        Slide(
            layout="chart_line",
            title="Serum trough concentrations",
            subtitle="μg/mL · sparse sampling windows",
            chart_categories=["Week 2", "Week 4", "Week 8", "Week 12", "Week 16"],
            chart_series=[
                _cs("Arm A median", (42.0, 51.0, 58.0, 61.0, 63.0)),
                _cs("Arm B median", (39.0, 46.0, 52.0, 54.0, 55.0)),
            ],
        ),
        Slide(
            layout="two_column",
            title="PK/PD translation",
            bullets_left=[
                "Exposure-response models stable across weight quartiles",
                "Food effect analysis negligible vs prespecified MCID band",
                "Renally impaired cohort bridging simulation approved",
            ],
            bullets_right=[
                "Pediatric bridging deferred until adult DBL locked",
                "DDI grid green except strong CYP3A4 inhibitors (boxed)",
                "Impurity specs tightened post-lot retrospective review",
            ],
        ),
        Slide(
            layout="chart_bar",
            title="Immunogenicity titre · ADA % positive",
            subtitle="Central lab · cumulative",
            chart_categories=["Baseline", "Week 8", "Week 16", "Week 24"],
            chart_series=[
                _cs("Treatment emergent ADA", (3.2, 5.1, 6.8, 7.9)),
                _cs("Neutralizing subset", (0.8, 1.4, 2.1, 2.6)),
            ],
        ),
        Slide(
            layout="title_content",
            title="Subgroup interplay (exploratory)",
            bullets=[
                "Age ≥65 shows attenuated responder delta — hypothesis generating only",
                "Baseline biomarker tertiles preserve directional HR across regions",
                "Prior biologic exposure stratum requires Phase IV commitment language",
            ],
        ),
        Slide(
            layout="two_column",
            title="Label negotiation hooks",
            bullets_left=[
                "Responder definition anchored on Week 24 threshold copy",
                "Biomarker language contingent on SPA biomarker cohort lock",
                "Pediatric carve-out referencing deferred PIP milestones",
            ],
            bullets_right=[
                "Safety tables harmonized across CSR + IB appendices",
                "SMPC-ready narratives drafted for EU linguists",
                "JP-HA briefing deck rehearsed with local medical affairs partner",
            ],
        ),
        Slide(
            layout="chart_line",
            title="Site activation trajectory",
            subtitle="Countries live · cumulative",
            chart_categories=["M1", "M2", "M3", "M4", "M5", "M6"],
            chart_series=[_cs("Countries", (6.0, 11.0, 17.0, 22.0, 26.0, 29.0))],
        ),
        Slide(
            layout="quote",
            quote="Every beautiful chart still defers to the safety table's footnotes.",
            attribution="Medical monitor standup",
        ),
        Slide(layout="section", title="Operational readiness", title_color_hex="0F766E"),
        Slide(
            layout="two_column",
            title="Site quality levers",
            bullets_left=[
                "Remote SDV spot checks + risk-based triggers",
                "Central lab kit traceability dashboards",
                "Temperature excursion playbooks refreshed",
            ],
            bullets_right=[
                "ePRO adherence nudges via localized SMS tone tests",
                "Recruitment diversity scorecard in monthly ops review",
                "Unblinded pharmacovigilance bridge during weekend on-call rotations",
            ],
        ),
        Slide(
            layout="chart_line",
            title="Query resolution turnaround",
            subtitle="Median days · target line 5d",
            chart_categories=cat_months,
            chart_series=[_cs("Median days to close", (6.2, 5.8, 5.1, 4.9, 4.6, 4.4))],
        ),
        Slide(
            layout="title_content",
            title="Regulatory correspondence",
            bullets=[
                "Type II meeting packet drafting ahead of SPA renewal checkpoint",
                "Label negotiation contingent on biomarker supplemental cohort alignment",
                "Europe pediatric investigative plan threaded separately (PIP milestones)",
            ],
        ),
        Slide(
            layout="section",
            title="Investment thesis recap",
            title_color_hex="0F766E",
        ),
        Slide(
            layout="two_column",
            title="Board asks vs sponsor commitments",
            bullets_left=[
                "Approve incremental DSMB observer budget line",
                "Unlock Phase IIIb exploratory dermatology cohort budget envelope",
                "Fast-track pharmacometrics hiring req (#LM-441)",
            ],
            bullets_right=[
                "Deliver interim CSR skeleton within 45 days post DBL draft",
                "Publish responder algorithm pseudocode openly post-readout",
                "Freeze ancillary endpoints lab definitions prior to Week 36 snapshot",
            ],
        ),
        Slide(
            layout="title_content",
            title="Timeline checkpoints",
            bullets=[
                "Week 28: interim biomarker composite lock",
                "Week 36: DSMB memorandum expected read-through",
                "Week 44: CSR narrative sprint + disclosure scrub parallel track",
            ],
        ),
        Slide(
            layout="quote",
            quote="Evidence wins rooms when humility sits beside significance.",
            attribution="Steering committee charter",
        ),
    ]
    return Deck(
        title=f"CLEAR-302 outcomes programme · {stamp}",
        subtitle="Clinical showcase deck",
        author="ZPresenter samples",
        audience=AudienceProfile(technical_level="executive", attention_span="short"),
        theme=th,
        slides=slides,
    )


def deck_design_system(stamp: str) -> Deck:
    """Design-system audit / UX governance storyline."""
    th = DeckTheme(primary_hex="6D28D9", accent_hex="DB2777")
    slides: list[Slide] = [
        Slide(
            layout="title",
            title=f"Nova Design System · {stamp}",
            subtitle="FY26 maturity audit · accessibility · governance flywheel",
            notes="Designer-heavy audience — emphasize tokens + measurement loops.",
        ),
        Slide(layout="section", title="North Star metrics", title_color_hex="6D28D9"),
        Slide(
            layout="title_content",
            title="Why measure systems not screens",
            bullets=[
                "Fragmented UI libraries inflate QA drag faster than headcount curves",
                "Accessibility debt compounds silently until procurement audits bite",
                "Brand elasticity constrained when semantic layers drift from tokens",
                "Storybook adoption plateau signals governance fatigue — not tooling gaps",
            ],
        ),
        Slide(
            layout="two_column",
            title="Signals vs noise",
            bullets_left=[
                "Token drift sprint burndowns trending upward again",
                "Design bug age in Jira creeping past 45d median",
                "Figma library publish cadence slowing (weekly → biweekly)",
                "Color-contrast regressions clustered in marketing microsites",
            ],
            bullets_right=[
                "Engineering handoff rework hours per feature stable",
                "Component reuse index up 6pts across mobile surfaces",
                "Lighthouse accessibility score p90 above 92 for core app",
                "Brand NPS unaffected (no customer perception signal yet)",
            ],
        ),
        Slide(
            layout="chart_bar",
            title="Design-debt backlog age",
            subtitle="Median days open · by swimlane",
            chart_categories=["Foundations", "Patterns", "Content", "Brand", "Research"],
            chart_series=[
                _cs("Q1 snapshot", (38.0, 44.0, 52.0, 61.0, 28.0)),
                _cs("Current", (29.0, 35.0, 40.0, 48.0, 22.0)),
            ],
        ),
        Slide(
            layout="section",
            title="Accessibility program",
            title_color_hex="6D28D9",
        ),
        Slide(
            layout="chart_line",
            title="WCAG violation burn-down",
            subtitle="Critical + serious · backlog count",
            chart_categories=["W1", "W2", "W3", "W4", "W5", "W6"],
            chart_series=[
                _cs("Web", (118.0, 96.0, 74.0, 59.0, 48.0, 41.0)),
                _cs("Mobile", (86.0, 72.0, 61.0, 54.0, 47.0, 43.0)),
            ],
        ),
        Slide(
            layout="title_content",
            title="Program pillars",
            bullets=[
                "Shift-left linting inside Figma tokens + code export pipeline",
                "Paired audits with CX research for real device matrix coverage",
                "Escalation path when marketing pages bypass CMS components",
                "Quarterly storytelling for executive design council (not just dashboards)",
            ],
        ),
        Slide(
            layout="two_column",
            title="Governance model",
            bullets_left=[
                "RFC lightweight template embedded in Slack workflow",
                "Design council quorum rotation quarterly",
                "Breaking-change calendar synced with mobile release trains",
                "Deprecation banners wired via CMS metadata hooks",
            ],
            bullets_right=[
                "Contribution ladder refreshed with mentorship pairing",
                "Office hours staffed rotating Design Tech leads",
                "Dogfood sandbox pinned to staging CDN snapshots nightly",
                "Budget carve-out for tooling parity laptop fleet renewal",
            ],
        ),
        Slide(
            layout="quote",
            quote="Consistency is kindness scaled.",
            attribution="Nova DS principles",
        ),
        Slide(layout="section", title="Brand palette hygiene", title_color_hex="6D28D9"),
        Slide(
            layout="chart_bar",
            title="Off-brand hex usage incidents",
            subtitle="Weekly violations detected · automated crawl",
            chart_categories=["Marketing", "Docs", "Blog", "Support", "Community"],
            chart_series=[_cs("Violations", (22.0, 11.0, 18.0, 9.0, 31.0))],
        ),
        Slide(
            layout="title_content",
            title="Palette drift hotspots",
            bullets=[
                "Partner microsites importing deprecated emerald accent (#34D399)",
                "Documentation screenshots stale vs prod chrome tint drift",
                "Community hackathon repos skipping lint pipeline entirely",
            ],
        ),
        Slide(
            layout="two_column",
            title="Remediation playbook",
            bullets_left=[
                "Sweep scripts tagging rogue hex codes nightly",
                "Story-wide lint blocking merges when severity critical",
                "Designer pairing slots Thursdays for retrofit backlog",
            ],
            bullets_right=[
                "Marketing CMS clamp enforcing palette subsets only",
                "Screenshot harness regenerated via CI nightly crawl",
                "Office-hours backlog grooming alternating EU/US friendly slots",
            ],
        ),
        Slide(layout="section", title="Partner ecosystem fit", title_color_hex="6D28D9"),
        Slide(
            layout="title_content",
            title="Systems integrator alignment",
            bullets=[
                "GSIs standardized on Nova tokens package v17 — divergence tracked weekly",
                "Reference storefront repos pinned to semver minors only during freeze windows",
                "Partner-built widgets audited via automated DOM snapshot regression packs",
                "Sandbox tenancy quotas negotiated before FY26 renewal packets ship",
            ],
        ),
        Slide(
            layout="two_column",
            title="Training & certification ladder",
            bullets_left=[
                "Foundational tier: tokens + semantic HTML checkpoints",
                "Advanced tier: motion choreography + accessibility pairing labs",
                "Architect tier: cross-brand customization governance simulations",
            ],
            bullets_right=[
                "Exam integrity monitored via randomized Storybook mutation suites",
                "Certificates expire annually unless refresher quizzes ≥85%",
                "Partner badges surfaced publicly through verified CDN issuer profiles",
            ],
        ),
        Slide(
            layout="chart_bar",
            title="Partner build throughput",
            subtitle="Story points merged · normalized · quarterly",
            chart_categories=["Q1", "Q2", "Q3", "Q4"],
            chart_series=[
                _cs("Tier-1 SI", (880.0, 920.0, 970.0, 1040.0)),
                _cs("Emerging SI", (410.0, 460.0, 510.0, 560.0)),
            ],
        ),
        Slide(
            layout="section",
            title="Roadmap choreography",
            title_color_hex="6D28D9",
        ),
        Slide(
            layout="chart_line",
            title="Adoption ladder · composite score",
            subtitle="Weighted components · rolling",
            chart_categories=["T0", "T1", "T2", "T3", "T4", "T5"],
            chart_series=[_cs("Score", (41.0, 48.0, 54.0, 61.0, 67.0, 73.0))],
        ),
        Slide(
            layout="title_content",
            title="Quarterly bets",
            bullets=[
                "Motion primitives tier-1 parity across React Native surfaces",
                "Data viz palette harmonization with Finance dashboards",
                "Localized type scale experiments in DE + JP pilot tenants",
                "Experimental dark mode token set behind feature gate (opt-in cohorts)",
            ],
        ),
        Slide(
            layout="two_column",
            title="Risks & dependencies",
            bullets_left=[
                "Headcount freeze on contractor design technologists",
                "Figma enterprise contract renegotiation window",
                "Cross-platform font licensing renewal in Q3",
            ],
            bullets_right=[
                "Dependent on mobile monorepo upgrade train #M-19",
                "Brand team campaign lock-in may override token freeze window",
                "Accessibility counsel review SLAs lengthening to 9d median",
            ],
        ),
        Slide(layout="section", title="Motion & content ops", title_color_hex="6D28D9"),
        Slide(
            layout="title_content",
            title="Interaction choreography backlog",
            bullets=[
                "Micro-interaction backlog prioritized via CX friction replay clips",
                "Latency-sensitive easing curves capped per WCAG motion preference hooks",
                "Locale-aware durations enforced via regression snapshots per locale pack",
                "Reduced-motion parity QA gates wired into CI smoke suites nightly",
            ],
        ),
        Slide(
            layout="two_column",
            title="Content design throughput",
            bullets_left=[
                "Copy decks routed through centralized terminology glossary",
                "AI-assisted drafts flagged until human editorial stamp applied",
                "Localization budgets gated behind glossary completeness scores",
            ],
            bullets_right=[
                "Markdown ingestion lint catches inaccessible emoji clusters",
                "Release calendar synced with CMS embargo slots across locales",
                "Voice tone audits sampled quarterly via stratified ticket pulls",
            ],
        ),
        Slide(
            layout="chart_bar",
            title="Localization defect backlog",
            subtitle="Median age · days · by severity tier",
            chart_categories=["SEV3", "SEV2", "SEV1"],
            chart_series=[
                _cs("Desktop app", (21.0, 14.0, 9.0)),
                _cs("Mobile app", (27.0, 18.0, 11.0)),
                _cs("Marketing web", (33.0, 22.0, 14.0)),
            ],
        ),
        Slide(
            layout="chart_line",
            title="Design QA throughput",
            subtitle="Stories merged · weekly · normalized",
            chart_categories=["Wk40", "Wk41", "Wk42", "Wk43", "Wk44", "Wk45"],
            chart_series=[
                _cs("Merged stories", (118.0, 126.0, 129.0, 134.0, 139.0, 143.0)),
                _cs("Rework loops", (22.0, 21.0, 19.0, 18.0, 17.0, 16.0)),
            ],
        ),
        Slide(
            layout="two_column",
            title="Experimentation ethics guardrails",
            bullets_left=[
                "Exposure budgets capped per cohort shard hash",
                "Explicit consent banners mirrored across SDK surfaces",
                "Kill-switch rehearsals staged quarterly with incident command roles",
            ],
            bullets_right=[
                "Psychologically sensitive cohorts excluded by policy registry",
                "Dark-pattern scanners fed screenshot hashes nightly",
                "Executive dashboards scrub PIIs before UX council reviews",
            ],
        ),
        Slide(
            layout="quote",
            quote="Governance without empathy ships bureaucracy.",
            attribution="Nova guild retro notes",
        ),
        Slide(
            layout="title_content",
            title="Closing commitments",
            bullets=[
                "Publish maturity scorecard externally by end of quarter (transparency pledge)",
                "Anchor next executive readout on customer-reported friction deltas, not vanity ADP",
                "Fund dedicated a11y pairing budget line (Finance pre-approval secured)",
            ],
        ),
    ]
    return Deck(
        title=f"Nova Design System · audit · {stamp}",
        subtitle="Design ops showcase",
        author="ZPresenter samples",
        audience=AudienceProfile(technical_level="general", attention_span="medium"),
        theme=th,
        slides=slides,
    )


def patch_example_quarterly_review(stamp: str) -> None:
    """Keep examples/sample.deck.json in sync with a generation stamp on deck + opening title."""
    path = ROOT / "examples" / "sample.deck.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    label = "Quarterly Review"
    data["title"] = f"{label} · {stamp}"
    for sl in data.get("slides", []):
        if sl.get("layout") == "title":
            sl["title"] = f"{label} · {stamp}"
            break
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)} (stamped title)")


def main() -> None:
    stamp = generation_stamp()
    _write(deck_product_launch(stamp), "sample-product-launch-orbit")
    _write(deck_clinical_evidence(stamp), "sample-clinical-clear302")
    _write(deck_design_system(stamp), "sample-design-system-nova")
    patch_example_quarterly_review(stamp)


if __name__ == "__main__":
    main()
