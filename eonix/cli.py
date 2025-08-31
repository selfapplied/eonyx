from __future__ import annotations

import argparse
import sys

from .core import emit


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Eonix listener/emitter CLI")
    p.add_argument("prompt", nargs="?", default="", help="input prompt text")
    p.add_argument("--theta", type=float, default=0.5, help="emit threshold")
    p.add_argument("--lam", type=float, default=1.0, help="L1 penalty weight")
    p.add_argument("--hush", action="store_true", help="only emit if very high resonance")
    p.add_argument("--mirror", action="store_true", help="penalize non-mirror-symmetric candidates")
    args = p.parse_args(argv)

    frag = emit(args.prompt, theta=args.theta, lam=args.lam, hush=args.hush, mirror=args.mirror)
    if frag:
        print(frag, end="")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

