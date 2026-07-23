#!/usr/bin/env python3
"""
count.py — Suno style-field character-count gate for LYRIC FORGE.

The Suno style field has a hard limit of 998 characters. This script counts the
characters in a style field and reports PASS/FAIL against that limit, plus whether
the count sits inside the recommended 986-998 target band.

Usage:
    python count.py "your style field text here"
    python count.py --file path/to/style-field.txt
    echo "style field text" | python count.py        # reads from stdin

Exit codes:
    0  PASS — count <= 998
    1  FAIL — count > 998 (over the hard limit)
    2  usage / input error
"""

import argparse
import sys

HARD_LIMIT = 998        # absolute maximum allowed by Suno
TARGET_LOW = 986        # recommended lower bound of the target band
TARGET_HIGH = 998       # recommended upper bound of the target band


def read_input(args):
    """Resolve the style-field text from --file, a positional arg, or stdin."""
    if args.file:
        with open(args.file, "r", encoding="utf-8") as handle:
            return handle.read()
    if args.text:
        return args.text
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return None


def evaluate(text):
    """Return (count, status, message) for the given style field text."""
    # Strip a single trailing newline that editors/stdin commonly append so it
    # does not falsely inflate the count. Internal whitespace is preserved
    # because Suno counts every visible character in the field.
    if text.endswith("\n"):
        text = text[:-1]
    count = len(text)

    if count > HARD_LIMIT:
        return count, "FAIL", f"OVER LIMIT by {count - HARD_LIMIT} chars (max {HARD_LIMIT})"
    if TARGET_LOW <= count <= TARGET_HIGH:
        return count, "PASS", f"in target band ({TARGET_LOW}-{TARGET_HIGH})"
    if count < TARGET_LOW:
        return count, "PASS", f"under target band — {TARGET_LOW - count} chars of headroom to {TARGET_LOW}"
    return count, "PASS", f"within hard limit ({HARD_LIMIT})"


def main():
    parser = argparse.ArgumentParser(
        description="Count characters in a Suno style field and gate against the 998-char limit."
    )
    parser.add_argument("text", nargs="?", help="Style field text passed inline.")
    parser.add_argument("--file", help="Read the style field from a UTF-8 text file.")
    args = parser.parse_args()

    text = read_input(args)
    if text is None:
        parser.print_usage(sys.stderr)
        print("error: provide style field text inline, via --file, or on stdin", file=sys.stderr)
        sys.exit(2)

    count, status, message = evaluate(text)
    print(f"{status}: {count} chars — {message}")
    sys.exit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
