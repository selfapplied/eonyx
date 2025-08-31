from __future__ import annotations

import argparse
import subprocess
import sys
from .visual.rainbow import colorize_text


def run_eonyx(seed: str) -> str:
    cmd = [sys.executable, "eonyx.py", seed]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    out = proc.stdout
    if "--- Generated Text ---" in out:
        return out.split("--- Generated Text ---", 1)[1].strip()
    return out.strip()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Rainbow Bridge: colorize Eonyx output")
    p.add_argument("seed", help="seed text to pass to eonyx")
    p.add_argument("--gravity", type=float, default=1.0, help="thermal gravity scale")
    args = p.parse_args(argv)

    text = run_eonyx(args.seed)
    print(colorize_text(text, gravity=args.gravity))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

