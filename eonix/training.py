from __future__ import annotations

import argparse
import os
import sys
import subprocess
from typing import List, Tuple


def _read_train_file(path: str) -> List[Tuple[str, str]]:
    pairs: List[Tuple[str, str]] = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for raw in f:
                s = raw.strip('\n')
                if not s or s.lstrip().startswith('#'):
                    continue
                if '=>' in s:
                    seed, expect = [t.strip() for t in s.split('=>', 1)]
                else:
                    seed, expect = s, ''
                pairs.append((seed, expect))
    except Exception:
        pass
    return pairs


def _score_match(generated: str, expected: str) -> float:
    if not expected:
        return 0.0
    # Simple overlap score
    g = set(generated.strip())
    e = set(expected.strip())
    if not e:
        return 0.0
    return len(g & e) / max(1, len(e))


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Eonix training: plaintext spec runner")
    p.add_argument('train_file', help="TRAIN file with lines: 'seed => expected' or just 'seed'")
    p.add_argument('--out', default='runs/train.log', help="output log file")
    args = p.parse_args(argv)

    pairs = _read_train_file(args.train_file)
    if not pairs:
        print("No training pairs found.")
        return 1

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    scores = []
    with open(args.out, 'w', encoding='utf-8') as log:
        for seed, expect in pairs:
            proc = subprocess.run([sys.executable, 'eonyx.py', seed], capture_output=True, text=True)
            out = proc.stdout
            text = out.split('--- Generated Text ---', 1)[1].strip() if '--- Generated Text ---' in out else out.strip()
            s = _score_match(text, expect)
            scores.append(s)
            log.write(f"SEED:\t{seed}\nEXPECT:\t{expect}\nTEXT:\t{text}\nSCORE:\t{s:.3f}\n---\n")

    avg = sum(scores) / len(scores)
    print(f"trained on {len(scores)} pairs, avg score {avg:.3f}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))

