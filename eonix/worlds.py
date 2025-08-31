from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class World:
    name: str
    mask: Dict[str, float]  # glyph→weight
    gravity: float
    prelude: str = ""


def _parse_world_file(path: str) -> Optional[World]:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = [ln.rstrip('\n') for ln in f]
    except Exception:
        return None

    name: Optional[str] = None
    gravity = 0.0
    mask: Dict[str, float] = {}
    prelude = ""

    def _decode_glyph(tok: str) -> str:
        table = {"␠": " ", "␤": "\n", "⇥": "\t"}
        return table.get(tok, tok)

    for raw in lines:
        s = raw.strip()
        if not s or s.startswith('#'):
            continue
        parts = s.split()
        key = parts[0].lower()
        if key == 'name:' and len(parts) >= 2:
            name = s.split(':', 1)[1].strip()
            continue
        if key == 'name' and len(parts) >= 2:
            name = ' '.join(parts[1:])
            continue
        if key == 'gravity' and len(parts) >= 2:
            try:
                gravity = float(parts[1])
            except Exception:
                pass
            continue
        if key == 'mask' and len(parts) >= 3:
            glyph = _decode_glyph(parts[1])
            try:
                weight = float(parts[2])
                mask[glyph] = weight
            except Exception:
                pass
            continue
        if key == 'prelude:' and len(parts) >= 2:
            prelude = s.split(':', 1)[1].lstrip()
            continue
        # First bare line becomes the name if not set
        if name is None:
            name = s

    if name is None:
        return None
    return World(name=name, mask=mask, gravity=gravity, prelude=prelude)


def detect_world(cwd: str | None = None) -> World:
    cwd = cwd or os.getcwd()
    base = os.path.basename(cwd).lower()
    # Plaintext world files are preferred over heuristics
    for fname in ('.world', 'WORLD'):
        path = os.path.join(cwd, fname)
        w = _parse_world_file(path)
        if w is not None:
            return w
    # Simple heuristics; extend as needed
    if any(k in base for k in ("code", "src", "lib")):
        return World(name="forge", mask={"{": 1.2, "}": 1.2, "_": 1.1}, gravity=0.2)
    if any(k in base for k in ("docs", "notes", "story")):
        return World(name="scribe", mask={" ": 0.9, ".": 1.1, ",": 1.1}, gravity=0.6)
    if any(k in base for k in ("data", "genome", "zip")):
        return World(name="archive", mask={"0": 1.2, "1": 1.2, "·": 1.1}, gravity=-0.3)
    return World(name="default", mask={}, gravity=0.0)

