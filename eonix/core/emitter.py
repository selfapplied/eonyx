from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from .listen import glyph_bank, silence_prior
from .resonance import score_fragment
from ..zipc.reflect import reflect_text


@dataclass
class EmitResult:
    fragment: str
    score: float
    considered: int
    threshold: float


def _candidate_fragments(glyphs: List[str]) -> List[str]:
    # Singles, then short repeats of top symbols will be tried in selection phase
    return glyphs


def emit_with_meta(
    prompt: str,
    theta: float = 0.5,
    lam: float = 1.0,
    hush: bool = False,
    mirror: bool = False,
    glyphs: Optional[List[str]] = None,
) -> EmitResult:
    """Emit the most resonant fragment or silence.

    - Prefers silence unless best score >= theta (or higher if hush).
    - Mirror flag penalizes fragments that are not reflection-consistent.
    """
    glyphs = glyphs or glyph_bank()
    prior = silence_prior()
    base_threshold = max(theta, 0.0)
    threshold = base_threshold * (2.0 if hush else 1.0)

    best_frag = ""
    best_score = float("-inf")
    considered = 0

    # Evaluate single glyphs first
    for g in _candidate_fragments(glyphs):
        s = score_fragment(prompt, g, lam=lam, silence_bias=prior)
        if mirror:
            r = reflect_text(g)
            if r != g:
                s -= 1.0  # penalize asymmetry
        considered += 1
        if s > best_score:
            best_score, best_frag = s, g

    # Consider short repeats of the current best glyph
    if best_frag:
        for k in (2, 3):
            frag = best_frag * k
            s = score_fragment(prompt, frag, lam=lam, silence_bias=prior)
            if mirror:
                r = reflect_text(frag)
                if r != frag:
                    s -= 1.0
            considered += 1
            if s > best_score:
                best_score, best_frag = s, frag

    # Early stop: prefer silence by default
    if best_score < threshold:
        return EmitResult(fragment="", score=best_score, considered=considered, threshold=threshold)

    return EmitResult(fragment=best_frag, score=best_score, considered=considered, threshold=threshold)


def emit(
    prompt: str,
    theta: float = 0.5,
    lam: float = 1.0,
    hush: bool = False,
    mirror: bool = False,
    glyphs: Optional[List[str]] = None,
) -> str:
    return emit_with_meta(prompt, theta=theta, lam=lam, hush=hush, mirror=mirror, glyphs=glyphs).fragment

