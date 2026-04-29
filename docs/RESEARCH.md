# Landscape research — programmatic & declarative presentations

This note summarizes **current alternatives** (2025–2026) to **zpresenter’s approach**: structured content (JSON) plus audience-aware checks plus native `.pptx` assembly via **python-pptx**. It is opinionated toward automation, pipelines, and developer workflows—not exhaustive rating of slide design apps.

Sources include official docs and PyPI listings retrieved during web research (March–April 2026 timeframe).

---

## 1. Native Python `.pptx` libraries

| Solution | Model | Strengths | Limits vs zpresenter |
|----------|--------|-----------|----------------------|
| **[python-pptx](https://python-pptx.readthedocs.io/)** | Imperative API over OOXML | Industrial-grade, widely used; placeholders, charts, notes; **editable** native slides | No deck-level schema or audience semantics—you bring structure |
| **[Aspose.Slides FOSS for Python](https://products.aspose.org/slides/python/)** | Presentation API | MIT; pure Python; mirrors PowerPoint concepts | Different API surface; ecosystem smaller than python-pptx |
| **[EasyPPTX](https://pypi.org/project/EasyPPTX/)** (PyPI) | Wrapper on python-pptx | Percent/grid layouts, TOML templates, dark themes, **explicitly marketed for AI-assisted authoring** | Higher abstraction; different contract than JSON Deck |

**Takeaway:** zpresenter intentionally stays close to **python-pptx** so slides remain editable PowerPoint artifacts while opinionated metadata lives in JSON.

---

## 2. Outline / structured data → slides (minimal or no AI)

| Solution | Input | Output | Notes |
|----------|-------|--------|------|
| **[slide-generator](https://pypi.org/project/slide-generator/)** (PyPI) | Structured outline dict | `.pptx` via HTML → Playwright images | Rich layouts (charts, images); heavy runtime (Chromium); slides often image-based |
| **EasyPPTX** | Python API / TOML | `.pptx` | Strong templating story |

**Takeaway:** zpresenter prioritizes **native placeholders** (selectable text) over rasterized/HTML-first pipelines unless we later opt into hybrid rendering.

---

## 3. Markdown-first slide ecosystems

| Solution | Stack | Strengths | Typical `.pptx` tradeoff |
|----------|-------|-----------|---------------------------|
| **[Slidev](https://sli.dev/guide/exporting)** | Vite + Markdown (+ Vue) | Live coding, themes, presenter mode; exports PDF/PPTX/PNG | Official docs note **PPTX export uses slide images** — text often not selectable |
| **[Marp](https://github.com/marp-team/marp-vscode)** | Markdown → Marpit | Excellent authoring in VS Code; exports PDF/PPTX | Editable PPTX is **experimental** and relies on browser + LibreOffice path; GitHub discussions highlight **semantic text-box fidelity limits** |
| **[Fusuma](https://github.com/hiroppy/fusuma)** | Markdown/MDX | Zero-config, themes, GH Pages flows | Web-first |
| **[Mostage](https://mo.js.org/)** | Markdown | Plugins, themes, multiple exports | Feature matrix historically lagged speaker modes vs Slidev |

**Takeaway:** Markdown stacks excel at **authoring velocity** and developer ergonomics; **semantic PowerPoint** remains a distinct niche—where JSON + python-pptx fits.

---

## 4. AI / SaaS presentation generators

| Solution | Delivery | Strengths | Fit for repo-local pipelines |
|----------|-----------|-------------|------------------------------|
| **[SlideSpeak API](https://slidespeak.co/slidespeak-api/)** | REST | Native `.pptx`, templates, outlines ([docs](https://docs.slidespeak.co/basics/api-references/generate-presentation/)) | Requires API keys, quotas; great for product integration—not embedded library |
| **[SlideForge](https://slideforge.dev)** | REST / MCP | Native `.pptx`; deterministic **spec** renders and template fills; MCP integration for agents ([docs](https://slideforge.dev/docs)) | SaaS / usage pricing |
| **[SlideDeck AI](https://pypi.org/project/slidedeckai/)** | Python + LLMs + python-pptx | Multi-provider LLMs; generates structured JSON then pptx | Heavy deps; AI-centric—not “rules-first” |

**Takeaway:** zpresenter can remain **offline-first** and **deterministic** (audience checks, schema); AI integration could be a future optional layer feeding the same JSON contract.

---

## 5. Positioning summary

| Dimension | Slidev / Marp | SaaS AI decks | **zpresenter** |
|-----------|-----------------|---------------|----------------|
| Primary artifact | Markdown / Web | Prompt / upload | **JSON Deck + checks** |
| `.pptx` semantics | Often image/pdf pipelines | Native pptx varies | **Placeholder-first native pptx** |
| Audience governance | DIY | Prompt tuning | **`AudienceProfile` + findings** |

---

## 6. Features adopted from landscape analysis

To reduce friction familiar from **python-pptx** forums (multiple slide masters, opaque layout names), zpresenter ships **`zpresenter list-layouts`**: enumerate slide masters and layout names from the built-in blank theme **or** from a corporate `.pptx` template—supporting branding workflows described across templating-centric tools without adopting heavier wrappers.

See **`README.md`** CLI table for usage.

---

## 7. Future backlog (not committed)

- Optional `--template` on **build** to start from a branded `.pptx` master (EasyPPTX-style reference decks).
- Markdown → Deck converter for authoring parity with Marp-class tools.
- Optional SlideSpeak-style outline ingestion behind explicit API keys.

---

## References (URLs)

- python-pptx documentation: https://python-pptx.readthedocs.io/
- EasyPPTX (PyPI): https://pypi.org/project/EasyPPTX/
- Slidev exporting: https://sli.dev/guide/exporting
- Marp for VS Code: https://github.com/marp-team/marp-vscode
- SlideSpeak API overview: https://slidespeak.co/slidespeak-api/
- SlideSpeak generate presentation API: https://docs.slidespeak.co/basics/api-references/generate-presentation/
- SlideDeck AI (PyPI): https://pypi.org/project/slidedeckai/
- Aspose.Slides FOSS: https://products.aspose.org/slides/python/
- slide-generator (PyPI): https://pypi.org/project/slide-generator/
- Fusuma: https://github.com/hiroppy/fusuma
- Mostage: https://mo.js.org/
- SlideForge: https://slideforge.dev/
