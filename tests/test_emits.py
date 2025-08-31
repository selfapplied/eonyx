from __future__ import annotations

import subprocess
import sys

from eonix.core import emit


def test_silence_allowed_default_threshold():
    # With conservative defaults, many prompts should prefer silence
    rcases = [
        "", "two seeds meet", "random text", "abcdefg", "mirror",
    ]
    silences = 0
    for p in rcases:
        out = emit(p)
        if out == "":
            silences += 1
        assert len(out) <= 3
    assert silences >= 2


def test_cli_exit_codes_and_short_output():
    # When silence, exit code 1; when emit, code 0 with short output
    exe = [sys.executable, "-m", "eonix.cli", "two seeds meet", "--theta", "0.0"]
    proc = subprocess.run(exe, capture_output=True, text=True)
    assert proc.returncode in (0, 1)
    assert len(proc.stdout) <= 3

    exe2 = [sys.executable, "-m", "eonix.cli", "noise noise noise", "--hush"]
    proc2 = subprocess.run(exe2, capture_output=True, text=True)
    assert proc2.returncode in (0, 1)
    assert len(proc2.stdout) <= 3

