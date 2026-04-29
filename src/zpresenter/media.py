"""Resolve deck image paths and remote URLs for embedding in `.pptx`."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen


def _is_url(src: str) -> bool:
    s = src.strip()
    return s.startswith("http://") or s.startswith("https://")


def resolve_local_path(src: str, base_dir: Path | None) -> Path:
    """Resolve a non-URL src to an absolute filesystem path."""
    s = src.strip()
    p = Path(s)
    if p.is_absolute():
        return p
    if base_dir is not None:
        return (base_dir / p).resolve()
    return (Path.cwd() / p).resolve()


def fetch_url_bytes(src: str, *, timeout_s: float = 30.0) -> BytesIO:
    """GET an image URL; returns a seekable buffer for python-pptx."""
    req = Request(
        src.strip(),
        headers={"User-Agent": "zpresenter/deck-builder"},
    )
    with urlopen(req, timeout=timeout_s) as resp:  # noqa: S310 — intentional user-supplied deck URL
        data = resp.read()
    return BytesIO(data)


def load_image_for_picture(src: str, base_dir: Path | None) -> str | BytesIO:
    """
    Return a path string or in-memory buffer suitable for `shapes.add_picture`.
    Raises FileNotFoundError, URLError, or OSError on failure.
    """
    if _is_url(src):
        try:
            return fetch_url_bytes(src)
        except URLError as e:
            raise OSError(f"Could not fetch image URL: {src!r}") from e
    path = resolve_local_path(src, base_dir)
    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")
    return str(path)


def local_path_exists(src: str, base_dir: Path | None) -> bool:
    """False for URLs (not checked). True if resolved file exists."""
    if _is_url(src):
        return True
    return resolve_local_path(src, base_dir).is_file()
