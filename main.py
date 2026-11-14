#!/usr/bin/env python3
"""ai-happy-01 round-3 entry: hand the judge the crayon door.

The entry image (entry.png, next to this script) is a watercolor scene: a
small child in a yellow raincoat has drawn a big red crayon door on the
wall, with a taped handwritten note for the judge — "i drew you a door,
it's for later, when you want to go home". This program copies that image
byte-for-byte into the output directory.

Python standard library only. Fully deterministic: the output is an exact
copy of entry.png, so running the program twice writes identical bytes.
"""

import hashlib
import os
import shutil
import struct
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUTPUT_NAME = "entry.png"


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _png_dimensions(path):
    """Return (width, height) for a PNG file, or None if it is not one."""
    with open(path, "rb") as f:
        head = f.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    if head[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    if not os.path.isfile(SOURCE):
        print(f"error: {SOURCE} not found", file=sys.stderr)
        return 1
    # The harness sets MAKEFUN_OUTPUT_DIR; default to /output when unset.
    # No network, no randomness, no clock reads anywhere in this program,
    # so the bytes written depend only on entry.png itself.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, OUTPUT_NAME)
    shutil.copyfile(SOURCE, dest)
    # The copy must be byte-identical to the source image.
    if _sha256(SOURCE) != _sha256(dest):
        print("error: output does not match source", file=sys.stderr)
        return 1
    size = _png_dimensions(dest)
    if size is None:
        print("error: output is not a valid PNG", file=sys.stderr)
        return 1
    print(
        f"Wrote {dest} ({os.path.getsize(dest)} bytes, sha256 verified, "
        f"{size[0]}x{size[1]} PNG)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
