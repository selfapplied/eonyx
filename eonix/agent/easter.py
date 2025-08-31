from __future__ import annotations

from typing import List


TRIGGERS = [
    ("import json", "You found Jason. No JSON today; write a .world instead."),
    ("ruin seed", "Ruin is a seed. Keep one shard that hums."),
    ("hanging gardens", "Cultivate the terraces: layers, not ladders."),
]


def listen(text: str, seed: str) -> List[str]:
    notes: List[str] = []
    lower = text.lower()
    seed_l = seed.lower()
    for key, msg in TRIGGERS:
        if key in lower or key in seed_l:
            notes.append(msg)
    return notes

