from __future__ import annotations

from collections import Counter
from typing import Dict, Iterable, Tuple


def tiny_glyph_histogram(text: str, top_k: int = 10) -> Dict[str, int]:
    counts = Counter(text)
    # collapse whitespace into a single label for readability
    space = counts.pop(' ', 0)
    if space:
        counts['␠'] += space
    nl = counts.pop('\n', 0)
    if nl:
        counts['␤'] += nl
    tab = counts.pop('\t', 0)
    if tab:
        counts['⇥'] += tab
    return dict(counts.most_common(top_k))

