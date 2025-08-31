from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict


@dataclass
class World:
    name: str
    mask: Dict[str, float]  # glyph→weight
    gravity: float


def detect_world(cwd: str | None = None) -> World:
    cwd = cwd or os.getcwd()
    base = os.path.basename(cwd).lower()
    # Simple heuristics; extend as needed
    if any(k in base for k in ("code", "src", "lib")):
        return World(name="forge", mask={"{": 1.2, "}": 1.2, "_": 1.1}, gravity=0.2)
    if any(k in base for k in ("docs", "notes", "story")):
        return World(name="scribe", mask={" ": 0.9, ".": 1.1, ",": 1.1}, gravity=0.6)
    if any(k in base for k in ("data", "genome", "zip")):
        return World(name="archive", mask={"0": 1.2, "1": 1.2, "·": 1.1}, gravity=-0.3)
    return World(name="default", mask={}, gravity=0.0)

