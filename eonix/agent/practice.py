from __future__ import annotations

import os
import sys
import time
import subprocess
from typing import Dict

from eonix.stats.hist import tiny_glyph_histogram
from eonix.zipc.reflect import reflect_text
from eonix.worlds import detect_world
from .easter import listen as listen_easter


def _run(seed: str) -> str:
    proc = subprocess.run([sys.executable, 'eonyx.py', seed], capture_output=True, text=True)
    out = proc.stdout
    return out.split('--- Generated Text ---', 1)[1].strip() if '--- Generated Text ---' in out else out.strip()


def _write_reflection(dirpath: str, seed: str, world: str, text: str, hist: Dict[str, int]) -> None:
    path = os.path.join(dirpath, 'Reflection.md')
    mirror = reflect_text(text)
    with open(path, 'w', encoding='utf-8') as f:
        f.write("# Listening Reflection\n\n")
        f.write(f"- world: {world}\n")
        f.write(f"- seed: {seed}\n\n")
        f.write("## Text\n\n")
        f.write("```\n")
        f.write(text)
        f.write("\n```\n\n")
        f.write("## Mirror\n\n")
        f.write("```\n")
        f.write(mirror)
        f.write("\n```\n\n")
        f.write("## Tiny Glyph Histogram\n\n")
        f.write(", ".join([f"{k}:{v}" for k, v in hist.items()]))
        # Surprises
        notes = listen_easter(text, seed)
        if notes:
            f.write("\n\n## Surprises\n\n")
            for n in notes:
                f.write(f"- {n}\n")
        f.write("\n\n## Notes\n\n- What stood out?\n- Where is the silence?\n- What tiny edit is invited (if any)?\n")


def main(argv=None) -> int:
    seed = (argv or ['two seeds meet'])[0]
    world = detect_world().name
    text = _run(seed)
    hist = tiny_glyph_histogram(text)

    ts = time.strftime('%Y%m%d-%H%M%S')
    dirpath = os.path.join('runs', f'practice-{world}-{ts}')
    os.makedirs(dirpath, exist_ok=True)
    with open(os.path.join(dirpath, 'text.txt'), 'w', encoding='utf-8') as f:
        f.write(text)
    _write_reflection(dirpath, seed, world, text, hist)
    print(dirpath)
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))

