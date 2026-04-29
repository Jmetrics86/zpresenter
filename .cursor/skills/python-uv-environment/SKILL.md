---
name: python-uv-environment
description: >-
  Uses Astral uv for all Python workflows in this repository and respects the
  locked project environment. Use when editing or running Python code, managing
  dependencies, creating virtual environments, running tests or scripts, or when
  the user mentions pip, venv, requirements.txt, or Python tooling for zpresenter.
---

# Python with uv (this project)

## Rules

1. **Use uv for Python** — Prefer `uv` over raw `pip`, `pip install`, `python -m venv` without uv, or ad hoc global interpreters when working in this repo.
2. **Respect the project environment** — Treat dependencies as defined by `pyproject.toml` and `uv.lock` (when present). Do not instruct mixing unmanaged global installs with this project’s env unless the user explicitly asks for an exception.

## Before changing deps or running Python

- Check **repository root** for `pyproject.toml`, `uv.lock`, and `.python-version`. Use them as the source of truth for Python version and packages.
- If `pyproject.toml` exists but there is no lockfile yet, use `uv lock` after dependency changes unless the user prefers otherwise.
- Run executables and scripts **through the project env**: `uv run <command>` (e.g. `uv run pytest`, `uv run python script.py`, `uv run ruff check`).

## Common operations

| Goal | Prefer |
|------|--------|
| Install deps from lock | `uv sync` |
| Add/remove a package | `uv add` / `uv remove` |
| Refresh lockfile after manual `pyproject` edits | `uv lock` |
| One-off command in project env | `uv run ...` |
| New project / first-time setup | `uv init` or `uv sync` as appropriate |

## Agent behavior

- When suggesting shell commands for this repo’s Python work, **default to uv** in examples.
- When a user pastes pip-style instructions, **translate** to the equivalent uv workflow for this project when it is safe and accurate.
- If `pyproject.toml` is missing and the user is bootstrapping Python here, prefer **`uv init`** (or documenting `uv sync` once a manifest exists) over hand-rolling `venv` + `pip`.

## Optional: progressive detail

If the repo later adds scripts or CI that duplicate commands, align documentation and skills with the same uv commands above for consistency.
