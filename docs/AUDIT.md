# Document & artifact audit — zpresenter

Audited repository-crafted artifacts (excluding `.venv`, lock tooling caches, and vendored deps). A remediation pass applied **README**, JSON Schema export, VS Code wiring, and `$schema` tags in examples in the same session as this audit.

## Inventory

| Artifact | Role | Assessment |
|----------|------|------------|
| `README.md` | Human onboarding | Added — uv workflow, CLI table, schema pointers. |
| `docs/AUDIT.md` | Audit trail | Added — this file. |
| `docs/RESEARCH.md` | Competitive landscape | Added — Markdown stacks, SaaS APIs, Python libs; positioning notes. |
| `schemas/deck.schema.json` | Deck JSON Schema | Added — regenerate via `zpresenter schema --out`. |
| `.vscode/settings.json` | IDE validation | Added — binds `examples/**/*.json` to deck schema. |
| `pyproject.toml` | Package metadata, deps, pytest/ruff, entrypoint | Complete; dev deps grouped correctly. |
| `uv.lock` | Reproducible installs | Present — primary env truth with uv. |
| `.python-version` | Interpreter pin | Present — aligns with `requires-python`. |
| `.gitignore` | VCS hygiene | Covers `.venv`, build dirs, `out/` builds. |
| `examples/sample.deck.json` | Canonical deck sample | Valid; includes `$schema` + schema binding. |
| `examples/dummy-*.json` | Scenario demos | Valid; include `$schema`. |
| `.cursor/skills/python-uv-environment/SKILL.md` | Agent: uv workflow | Solid; references lockfile — keep synced if tooling changes. |
| `.cursor/skills/zpresenter-authoring/SKILL.md` | Agent: deck authoring | Solid; benefited from explicit schema + docs pointers. |
| `src/zpresenter/*.py` | Runtime | README documents CLI and deck contract; models remain primary truth. |
| `tests/*.py` | Regression tests | Present — schema coverage added in remediation. |

## Findings

### Critical

1. **No root README** — New contributors had no single entrypoint for uv sync, CLI commands, deck contract, or validation workflow.
2. **No machine-readable deck contract for editors** — JSON decks validated only at CLI parse time; IDEs could not validate deck JSON against a stable schema without digging into Pydantic source.

### High

3. **Schema drift risk** — Without an exported schema tied to `Deck`, examples and Cursor skills could drift from actual models (`models.py`).
4. **Examples lacked `$schema`** — Optional but improves diagnostics in VS Code when paired with workspace schema mapping.

### Medium

5. **No persistent audit trail** — Prioritized improvements lived only in chat history; this file fixes that.
6. **CI / GitHub Actions absent** — Automated `pytest` + `ruff` on push not wired (backlog).

### Low

7. **`validate-json` overlaps partially with `check`** — Acceptable; different purposes (pure parse vs audience rules).

## Prioritized improvements (executed)

| Priority | Item | Action taken |
|----------|------|----------------|
| P0 | Onboarding | Added root **README.md** with uv workflow, CLI table, examples index. |
| P0 | Deck validation ergonomics | Added **`zpresenter schema`** and committed **`schemas/deck.schema.json`** generated from `Deck`. |
| P1 | Editor integration | Added **`.vscode/settings.json`** mapping `examples/**/*.json` to the deck schema. |
| P1 | Examples | Prepended **`$schema`** to example JSON files pointing at `../schemas/deck.schema.json`. |
| P2 | Skills | Updated **zpresenter-authoring** skill with schema + README pointers. |
| P2 | Tests | **`tests/test_schema.py`** ensures exported schema stays wired to `Deck`. |

## Backlog (not implemented here)

- Add CI workflow (`uv sync`, `pytest`, `ruff check`).
- Optional pre-commit hook regenerating schema when `models.py` changes.
- Markdown → deck importer (large feature).

## Regenerating the schema

After changing `Deck`, `Slide`, or `AudienceProfile` in `models.py`:

```bash
uv run zpresenter schema --out schemas/deck.schema.json
```

Commit the updated JSON alongside Python changes.
