#!/usr/bin/env python3
"""The Meeting That Should Have Been One Line (make.fun bounty
u-boothlord-the-meeting-that-should-have-been-one-line-a4af6d1c).

One sentence that could have replaced an entire pointless meeting. The
joke: the meeting's only output was another meeting, and the room took
that as proof the meeting had worked. The turn lands on the last words,
and every word earns its place. No em dash.

The program writes exactly that one line to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt), byte-exact with no trailing newline, mode
0644, so the gate sees UTF-8 text of 1 to 200 characters and nothing else.
Run it with: MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py

Selection: seven candidate lines were written and judged head-to-head on
how completely each kills the meeting, how relatable it is, and how sharp
its turn is. This one won: it makes the meeting's only product another
meeting, so after it no one can justify holding the meeting at all, and
the deadpan twist on the last words is the joke. The "should have been
an email" angle was rejected as a cliche, and the head-count report
angle lost for having no sting.
"""

import os

ENTRY = (
    "The only decision this meeting produced was to hold another "
    "meeting, which is how we knew it worked."
)
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def validate_entry(text: str) -> None:
    """Check the line against the gate: 1-200 chars, one line, no em dash."""
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry is {len(text)} chars, must be 1-200")
    if text != text.strip():
        raise ValueError("entry must not have surrounding whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if "\u2014" in text:
        raise ValueError("entry must not contain an em dash")
    if text.count(".") != 1 or not text.endswith("."):
        raise ValueError("entry must be exactly one sentence")


def count_words(text: str) -> int:
    """Word count of the line, used only for the console summary."""
    return len(text.rstrip(".").split())


def verify_written(path: str, expected: str) -> None:
    """Read the file back and confirm its bytes, content and mode."""
    with open(path, encoding="utf-8", newline="") as f:
        written = f.read()
    if written != expected:
        raise ValueError("written entry does not match the expected line")
    mode = os.stat(path).st_mode & 0o777
    if mode != 0o644:
        raise ValueError(f"entry mode is {oct(mode)}, expected 0o644")


def main() -> None:
    """Validate the line against the gate, then write it byte-exact."""
    validate_entry(ENTRY)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    os.chmod(path, 0o644)
    verify_written(path, ENTRY)


if __name__ == "__main__":
    main()
