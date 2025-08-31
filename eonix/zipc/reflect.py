from __future__ import annotations

from typing import Dict


_mirror_pairs: Dict[str, str] = {
    "(": ")",
    ")": "(",
    "[": "]",
    "]": "[",
    "{": "}",
    "}": "{",
    "<": ">",
    ">": "<",
    "◆": "◆",
    "◇": "◇",
    "·": "·",
}


def reflect_text(s: str) -> str:
    """Simple mirror mapping for symmetry checks.

    Reverses the string and swaps with mirror pairs where available.
    """
    mapped = [
        _mirror_pairs.get(ch, ch)
        for ch in reversed(s)
    ]
    return "".join(mapped)

