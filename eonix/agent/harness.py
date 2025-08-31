from __future__ import annotations

import difflib
import json
import os
import subprocess
import sys
from typing import Dict, Tuple

from eonix.stats.hist import tiny_glyph_histogram


def run_generation(seed: str) -> str:
    proc = subprocess.run([sys.executable, 'eonyx.py', seed], capture_output=True, text=True)
    out = proc.stdout
    return out.split('--- Generated Text ---', 1)[1].strip() if '--- Generated Text ---' in out else out.strip()


def compression_score(before: str, after: str) -> float:
    # crude proxy: shorter output is better; normalized by before len
    if not before:
        return 0.0
    return max(0.0, (len(before) - len(after)) / max(1, len(before)))


def symmetry_score(s: str) -> float:
    # character-level palindrome fraction
    return sum(1 for a, b in zip(s, reversed(s)) if a == b) / max(1, len(s))


def resonance(before: str, after: str) -> Dict[str, float]:
    return {
        'compression': compression_score(before, after),
        'symmetry': symmetry_score(after),
    }


def evaluate_change(seed: str, edit_desc: str) -> Dict[str, object]:
    text0 = run_generation(seed)
    hist0 = tiny_glyph_histogram(text0)
    # edit is assumed to be applied outside; we just run again
    text1 = run_generation(seed)
    hist1 = tiny_glyph_histogram(text1)
    res = resonance(text0, text1)
    diff = ''.join(difflib.unified_diff(text0.splitlines(True), text1.splitlines(True), fromfile='before', tofile='after'))
    return {
        'seed': seed,
        'edit': edit_desc,
        'before': {'text': text0, 'hist': hist0},
        'after': {'text': text1, 'hist': hist1},
        'resonance': res,
        'diff': diff,
    }


def main(argv=None) -> int:
    seed = argv[0] if argv else 'two seeds meet'
    result = evaluate_change(seed, edit_desc='(no-op)')
    os.makedirs('runs', exist_ok=True)
    path = os.path.join('runs', 'harness.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print('resonance:', result['resonance'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))

