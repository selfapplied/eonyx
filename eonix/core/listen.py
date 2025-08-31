from __future__ import annotations

from typing import List


def glyph_bank() -> List[str]:
    """Returns the minimal glyph bank.

    Design: extremely small and conservative to bias toward silence.
    """
    letters = list("abcdefghijklmnopqrstuvwxyz")
    digits = list("0123456789")
    punct = list(".,-:;!?")
    symbols = ["·", "◆", "◇", "✶"]
    # Keep order stable; prefer letters first
    return letters + digits + punct + symbols


def silence_prior() -> float:
    """Base prior favoring silence. Larger => stronger silence preference.

    Used as an offset against resonance scores.
    """
    return 0.5

