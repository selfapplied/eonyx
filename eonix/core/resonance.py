from __future__ import annotations

import zlib
from typing import Callable


def _compress_length(data: bytes, level: int = 6, compressor: Callable[..., bytes] | None = None) -> int:
    if compressor is not None:
        return len(compressor(data))
    return len(zlib.compress(data, level))


def score_fragment(context: str, fragment: str, lam: float = 1.0, silence_bias: float = 0.0) -> float:
    """Resonance score = compression gain delta - lam * L1 - silence_bias.

    - compression gain: len(zlib(context)) - len(zlib(context+fragment))
    - L1 penalty: lam * |fragment|
    - silence bias: constant bias to prefer not emitting
    """
    context_bytes = context.encode("utf-8", errors="ignore")
    frag_bytes = fragment.encode("utf-8", errors="ignore")
    base = _compress_length(context_bytes)
    with_frag = _compress_length(context_bytes + frag_bytes)
    compression_delta = float(base - with_frag)
    l1_penalty = lam * float(len(fragment))
    return compression_delta - l1_penalty - silence_bias

