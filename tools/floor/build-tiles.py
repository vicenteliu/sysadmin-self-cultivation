#!/usr/bin/env python3
"""Derive the floor's sprite sheet from the hand-drawn tile source.

    python3 tools/floor/build-tiles.py            # write the sheet and its index
    python3 tools/floor/build-tiles.py --check    # exit non-zero when they are behind

    tools/floor/tiles.tiles          authored, one character per pixel  ← the source
    site/assets/floor/tiles.png      derived, a horizontal strip
    site/assets/floor/tiles.json     derived, name to column index

Why a PNG at all, when the source is text a browser could read? Because the runtime
draws this sheet a few thousand times a frame, and rasterising it once at build time
costs nothing while doing it per load costs something on every load. The source stays
text so that a tile change is a reviewable diff — which is the same reason
site/build-diagrams.py keeps its figures authored as HTML.

Standard library only: zlib and struct are all a PNG needs.
"""

import json, os, re, struct, sys, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SOURCE = os.path.join(HERE, "tiles.tiles")
OUT_DIR = os.path.join(ROOT, "site", "assets", "floor")
PNG = os.path.join(OUT_DIR, "tiles.png")
INDEX = os.path.join(OUT_DIR, "tiles.json")
SIZE = 16


def parse(text):
    """palette block, then one 16-by-16 block per tile. Deliberately rigid: a row that
    is not exactly 16 characters is a drawing mistake, and padding it would hide one."""
    palette, tiles, problems = {".": None}, {}, []
    mode, name, rows = None, None, []
    for n, raw in enumerate(text.split("\n"), 1):
        line = raw.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.strip() == "end":
            if mode == "tile":
                if len(rows) != SIZE:
                    problems.append(f"tile `{name}` has {len(rows)} rows, expected {SIZE}")
                tiles[name] = rows
            mode, name, rows = None, None, []
            continue
        if line.startswith("palette"):
            mode = "palette"
            continue
        if line.startswith("tile "):
            mode, name, rows = "tile", line.split(None, 1)[1].strip(), []
            continue
        if mode == "palette":
            key, _, value = line.partition(" ")
            value = value.strip()
            if value == "none":
                palette[key] = None
            elif re.fullmatch(r"#[0-9a-fA-F]{6}", value):
                palette[key] = tuple(int(value[i:i + 2], 16) for i in (1, 3, 5))
            else:
                problems.append(f"line {n}: `{value}` is not a colour")
        elif mode == "tile":
            if len(line) != SIZE:
                problems.append(f"tile `{name}` row {len(rows) + 1} is {len(line)} characters, expected {SIZE}")
            rows.append(line)

    for tile_name, tile_rows in tiles.items():
        for y, row in enumerate(tile_rows):
            for x, ch in enumerate(row):
                if ch not in palette:
                    problems.append(f"tile `{tile_name}` at {x},{y} uses `{ch}`, which the palette does not define")
    return palette, tiles, problems


def encode_png(width, height, pixels):
    """A minimal RGBA PNG. `pixels` is a flat list of (r, g, b, a) rows."""
    raw = b"".join(b"\x00" + b"".join(struct.pack("BBBB", *px) for px in row) for row in pixels)

    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9))
            + chunk(b"IEND", b""))


def build():
    palette, tiles, problems = parse(open(SOURCE, encoding="utf-8").read())
    if problems:
        return None, None, problems
    names = list(tiles)
    width, height = SIZE * len(names), SIZE
    rows = []
    for y in range(height):
        row = []
        for name in names:
            for x in range(SIZE):
                colour = palette[tiles[name][y][x]]
                row.append((0, 0, 0, 0) if colour is None else (*colour, 255))
        rows.append(row)
    index = {"tile": SIZE, "order": names, "columns": {n: i for i, n in enumerate(names)}}
    return encode_png(width, height, rows), index, []


def main():
    check = "--check" in sys.argv[1:]
    png, index, problems = build()
    if problems:
        print(f"{len(problems)} problem{'s' if len(problems) != 1 else ''} in tools/floor/tiles.tiles:",
              file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        return 1

    want = {PNG: png, INDEX: (json.dumps(index, indent=2) + "\n").encode()}
    if check:
        stale = []
        for path, data in want.items():
            rel = os.path.relpath(path, ROOT)
            if not os.path.exists(path):
                stale.append(f"{rel} is missing")
            elif open(path, "rb").read() != data:
                stale.append(f"{rel} is behind tools/floor/tiles.tiles")
        if stale:
            for s in stale:
                print(s, file=sys.stderr)
            print("run tools/floor/build-tiles.py", file=sys.stderr)
            return 1
        print(f"tiles current — {len(index['order'])} tiles, {SIZE}px, derived from tiles.tiles")
        return 0

    os.makedirs(OUT_DIR, exist_ok=True)
    for path, data in want.items():
        open(path, "wb").write(data)
    print(f"wrote {os.path.relpath(PNG, ROOT)} — {len(index['order'])} tiles "
          f"({len(png)} bytes) and its index")
    return 0


if __name__ == "__main__":
    sys.exit(main())
