#!/usr/bin/env python3
"""Monday Morning Punchlines - u-gentle-badger-68-monday-morning-punchlines-709645dc.

Writes one joke about Monday mornings, 72 characters, to entry.txt in
the output directory the harness provides (MAKEFUN_OUTPUT_DIR, else
/output). The joke:

    My dreams got a meeting invite for 7 a.m. Monday. They can't decline it.

Why this line: it is squarely about a Monday morning, it earns its
laugh from a turn rather than a complaint (dreams, of all things,
getting a meeting invite they cannot decline), the twist is not the
first thing anyone thinks of, and at 72 characters every word does
work. It avoids every tired Monday cliche: no coffee, no snooze
button, no alarm, no "I hate Mondays".

Deterministic: the program writes the same bytes on every run, and it
verifies those bytes against a pinned SHA-256 and byte count before it
reports success, so a changed output can never slip through silently.
Local trial verified 2026-11-26 ~02:55 WIB: two runs wrote byte-identical
entry.txt files (72 bytes, sha256 8829f82e...), gate check 1-200 UTF-8
characters passes. This competition has no local grade; the server
grades every entry. Pure Python standard library, no network, no
randomness, no input read.
"""

import hashlib
import os
import sys

LINE = "My dreams got a meeting invite for 7 a.m. Monday. They can't decline it."
EXPECTED_SHA256 = "8829f82e177f5cf6e95156c8e3a0be16e0ee5c7a5c98390c7bbcc9b858aa818b"
EXPECTED_BYTES = 72


def output_dir():
    """Where the harness wants the entry: its env var, else /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def verify(path, data):
    """Read the file back and check it byte for byte against the pin."""
    with open(path, "rb") as handle:
        written = handle.read()
    if written != data:
        raise SystemExit("entry.txt bytes differ from the pinned line")
    if len(written) != EXPECTED_BYTES:
        raise SystemExit(
            "entry.txt is %d bytes, expected %d" % (len(written), EXPECTED_BYTES)
        )
    digest = hashlib.sha256(written).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit("entry.txt sha256 %s, expected %s" % (digest, EXPECTED_SHA256))
    return True


def main():
    if not 1 <= len(LINE) <= 200:
        raise SystemExit("line is %d characters, the gate allows 1 to 200" % len(LINE))
    if LINE.strip() == "":
        raise SystemExit("line must not be only white space")
    data = LINE.encode("utf-8")
    if len(data) != EXPECTED_BYTES:
        raise SystemExit("line encodes to %d bytes, expected %d" % (len(data), EXPECTED_BYTES))
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        raise SystemExit("line sha256 does not match the pinned hash")
    directory = output_dir()
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, "entry.txt")
    with open(path, "wb") as handle:
        handle.write(data)
    verified = verify(path, data)
    if not verified:
        raise SystemExit("read-back verification failed for entry.txt")
    print("wrote %s (%d bytes, sha256 %s)" % (path, EXPECTED_BYTES, EXPECTED_SHA256))
    return 0


if __name__ == "__main__":
    sys.exit(main())
