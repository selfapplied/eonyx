from __future__ import annotations

from typing import Iterable

# Simple thermal mapping using ANSI 256-color escapes


def _temp_of_char(ch: str) -> float:
    # Heuristic: letters ~ neutral, punctuation cool, digits warming
    if ch.isalpha():
        return 0.0
    if ch.isdigit():
        return 0.2
    if ch in ",.;:!?":
        return -0.2
    if ch in "◆◇✶":
        return 0.6
    return 0.0


def _ansi_256_from_temp(t: float) -> int:
    # Map -1..+1 to blue..red rail
    t = max(-1.0, min(1.0, t))
    cold = 21   # blue
    warm = 196  # red
    mid = 244   # gray
    if t > 0.1:
        return int(warm - (1.0 - t) * (warm - mid))
    if t < -0.1:
        return int(cold + (t + 1.0) * (mid - cold))
    return mid


def colorize_text(text: str, gravity: float = 1.0) -> str:
    out = []
    for ch in text:
        temp = _temp_of_char(ch) * gravity
        code = _ansi_256_from_temp(temp)
        out.append(f"\033[38;5;{code}m{ch}\033[0m")
    return "".join(out)

