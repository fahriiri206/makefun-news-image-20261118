#!/usr/bin/env python3
"""Copy the committed entry image to the competition output path."""

import hashlib
import os
import struct
import sys
import zlib

MAX_SIDE = 1024
MAX_BYTES = 1024 * 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_crc(chunk_type, chunk_data):
    return zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF


def check_dimensions(data):
    if len(data) < 24 or data[12:16] != b"IHDR":
        fail("missing IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width == 0 or height == 0:
        fail("IHDR declares an empty image")
    if width > MAX_SIDE or height > MAX_SIDE:
        fail(f"image is {width}x{height}, over the {MAX_SIDE}x{MAX_SIDE} limit")
    return width, height


def walk_chunks(data):
    if not data.startswith(PNG_SIGNATURE):
        fail("bad PNG signature")
    pos = len(PNG_SIGNATURE)
    seen_ihdr = False
    seen_iend = False
    while pos < len(data):
        if seen_iend:
            fail("data after IEND")
        if pos + 8 > len(data):
            fail("truncated chunk header")
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        chunk_type = data[pos + 4:pos + 8]
        end = pos + 8 + length + 4
        if end > len(data):
            fail(f"truncated {chunk_type!r} chunk")
        chunk_data = data[pos + 8:pos + 8 + length]
        stored = struct.unpack(">I", data[pos + 8 + length:end])[0]
        if png_crc(chunk_type, chunk_data) != stored:
            fail(f"bad CRC in {chunk_type!r} chunk")
        if not seen_ihdr:
            if chunk_type != b"IHDR":
                fail("IHDR is not the first chunk")
            seen_ihdr = True
        if chunk_type == b"IEND":
            seen_iend = True
        pos = end
    if not seen_ihdr:
        fail("missing IHDR chunk")
    if not seen_iend:
        fail("missing IEND chunk")


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def find_image():
    here = os.path.dirname(os.path.realpath(__file__))
    candidate = os.path.join(here, "entry.png")
    if os.path.isfile(candidate):
        return candidate
    fallback = "/bot/entry.png"
    if os.path.isfile(fallback):
        return fallback
    fail("entry.png not found beside main.py or at /bot/entry.png")


def main():
    source = find_image()
    try:
        with open(source, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        fail(f"cannot read {source}: {exc}")

    if not data.startswith(PNG_SIGNATURE):
        fail("bad PNG signature")
    if len(data) > MAX_BYTES:
        fail(f"image is {len(data)} bytes, over the {MAX_BYTES}-byte limit")
    walk_chunks(data)
    check_dimensions(data)

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    target = os.path.join(output_dir, "entry.png")
    try:
        with open(target, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    except OSError as exc:
        fail(f"cannot write {target}: {exc}")

    digest = hashlib.sha256(data).hexdigest()
    print(f"{target} {len(data)} bytes sha256={digest}")


if __name__ == "__main__":
    main()
