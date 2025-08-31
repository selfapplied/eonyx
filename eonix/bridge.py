from __future__ import annotations

import argparse
import subprocess
import sys
from .visual.rainbow import colorize_text
from .stats.hist import tiny_glyph_histogram
from .worlds import detect_world


def run_eonyx(seed: str) -> str:
    cmd = [sys.executable, "eonyx.py", seed]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    out = proc.stdout
    if "--- Generated Text ---" in out:
        return out.split("--- Generated Text ---", 1)[1].strip()
    return out.strip()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Rainbow Bridge: colorize Eonyx output and stats")
    p.add_argument("seed", help="seed text to pass to eonyx")
    p.add_argument("--gravity", type=float, default=1.0, help="thermal gravity scale")
    args = p.parse_args(argv)

    world = detect_world()
    text = run_eonyx(args.seed)
    # Apply world gravity offset
    g = args.gravity + world.gravity
    colored = colorize_text(text, gravity=g)
    print(colored)

    # Print tiny glyph histogram
    hist = tiny_glyph_histogram(text)
    print("\n-- world:", world.name)
    print("-- glyphs:", " ".join(f"{k}:{v}" for k, v in hist.items()))

    # Save run artifact
    try:
        import time, os, json
        os.makedirs("runs", exist_ok=True)
        ts = time.strftime("%Y%m%d-%H%M%S")
        fn = os.path.join("runs", f"run-{world.name}-{ts}.json")
        with open(fn, "w", encoding="utf-8") as f:
            json.dump({"world": world.name, "seed": args.seed, "hist": hist, "text": text}, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

