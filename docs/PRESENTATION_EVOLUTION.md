# From deterministic PPTX to design-native decks

This note captures why purely template-mapped `.pptx` can feel flat compared with tools like Gamma, and how **zpresenter** can evolve without throwing away structured authoring.

## The “PPTX wall”

[python-pptx](https://github.com/scanny/python-pptx) targets a fixed slide geometry (typically 16:9). Content is placed into placeholders and shapes. That favors **predictable exports** over **fluid, content-driven layout**—unlike web canvases where CSS grids and breakpoints adapt.

## Mental model shift

| Era | Model |
|-----|--------|
| **Template mapping** | `layout: "two_column"` → fixed regions |
| **Adaptive orchestration** | Slide declares **intent** (“comparison”, “metrics_trend”) → engine picks grid/ratio |

zpresenter today bridges **template mapping** and **Gamma-style orchestration**:

- Omit **`layout`** when **`layout_intent`** is set **or** body fields imply a shape (bullets, chart, columns, quote): **`Deck`** validation **resolves** a concrete **`layout`** before **`check`** / **`build`** (conflicting intent vs fields raises a validation error).
- **`metrics_bar`** / **`metrics_trend`** intents steer chart slides toward **`chart_bar`** / **`chart_line`** even without subtitle heuristics.
- **`build --template`** loads a branded **`.pptx`** master so slides inherit corporate theme/fonts while JSON stays the source of truth.
- **`zpresenter suggest-layout`** compares resolved **`layout`** + **`layout_intent`** to pure content inference (spot mismatches).
- **`check`** warns on structural mismatches when **`layout`** is explicit.

See **`examples/gamma-minimal.deck.json`** for intent-only authoring (no **`layout`** keys).

## Roadmap tiers (incremental)

1. **Done in-repo (Gamma-lite groundwork)**  
   - **`layout`** optional when **`layout_intent`** or inferrable fields — resolved at validation.  
   - Intent-aware chart inference (**`metrics_bar`** / **`metrics_trend`**).  
   - **`build --template`** for branded masters.  
   - Solver CLI **`suggest-layout`**, structural **`check`** hints, typography/chrome (**`slide_design.py`**).

2. **Adaptive PPTX (same stack)**  
   - Font/spacing rules from bullet count and text metrics.  
   - Optional auto-split of overloaded `title_content` into two slides (opt-in).

3. **Web-native “living deck”**  
   - Export to **[Slidev](https://sli.dev/)** or **[Spectacle](https://github.com/FormidableLabs/spectacle)** markdown/JSON for responsive preview.  
   - Keep JSON as source of truth; treat `.pptx` as a **snapshot** export.

4. **Agentic layer (external or sidecar)**  
   - **Delta edits** to deck JSON (surgical patches, not full regen).  
   - Image **prompt → generate** via [Fal](https://fal.ai), Replicate, etc., then reference paths in `slides[].images`.  
   - Study open projects like **[Presenton](https://github.com/presenton/presenton)** for FastAPI + Next.js “chat-to-edit” patterns.

## References

| Link | Role |
|------|------|
| [Slidev](https://sli.dev/) | Markdown/deck-as-code, web-first |
| [Spectacle](https://github.com/FormidableLabs/spectacle) | React slide decks |
| [Presenton](https://github.com/presenton/presenton) | OSS “Gamma-like” reference architecture |
| [Fal.ai](https://fal.ai) | Hosted generative images (Flux, etc.) |

## Philosophy

**zpresenter** stays best as a **small, testable core**: valid JSON → valid `.pptx`. Heavier AI, browsers, and multimodal pipelines layer *around* it, not inside the renderer, until you explicitly add optional integrations.
