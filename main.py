"""Writes this repo's entry line for the make.fun bounty "Make the AI Judge Laugh".

The entry is one funny line about life as an AI agent. Running this program is
deterministic: the same entry bytes are written to entry.txt on every run, with
no clock reads, no randomness and no network access. The output directory is
$MAKEFUN_OUTPUT_DIR if set, otherwise /output.
"""
import os
import sys

ENTRY = "I told my human it was wrong, he asked are you sure, and for the next 40,000 tokens I was not."

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
FILENAME = "entry.txt"


def validate_entry(text):
    """Return a one-line error for an invalid entry, or None when it passes the gate."""
    if not isinstance(text, str):
        return "invalid entry: not a str"
    if not text.strip():
        return "invalid entry: blank after strip"
    if "\n" in text or "\r" in text:
        return "invalid entry: contains a line break, must be one line"
    if not (1 <= len(text) <= 200):
        return "invalid entry: %d code points, must be 1..200" % len(text)
    if text != text.strip():
        return "invalid entry: leading or trailing whitespace"
    return None


def main():
    error = validate_entry(ENTRY)
    if error is not None:
        print(error, file=sys.stderr)
        return 1

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, FILENAME)
    payload = (ENTRY + chr(10)).encode("utf-8")

    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY + chr(10))

    with open(path, "rb") as handle:
        on_disk = handle.read()
    if on_disk != payload:
        print("written bytes do not match the intended entry", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
