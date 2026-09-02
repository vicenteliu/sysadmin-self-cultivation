---
kind: tool
axis: meta
themes: []
platforms: []
summary: "Inputs: hand-drawn ASCII tiles · Outputs: the floor's sprite sheet and its index under site/assets/floor/ · Risk: writes two generated files, nothing else · Root: not needed"
---
# tools/floor — the floor's design-time side

> 🌐 **Languages:** English (default) · [中文](../../docs/zh/tools/floor/README.md)

> **Inputs:** [`tiles.tiles`](tiles.tiles), one character per pixel · **Outputs:**
> `site/assets/floor/tiles.png` and `tiles.json` · **Risk:** writes two generated files
> and nothing else · **Root:** not needed

Everything here runs **before** the browser and never reaches it. The floor's runtime is
[`site/js/floor.js`](../../site/js/floor.js), hand-written Canvas2D with no framework and
no build step, exactly like the rest of the viewer
([ADR-0006](../../docs/adr/0006-the-viewer-vendors-its-dependencies.md)).

```bash
python3 tools/floor/build-tiles.py            # write the sheet and its index
python3 tools/floor/build-tiles.py --check    # exit non-zero when they are behind
```

## The tile source

`tiles.tiles` is a palette followed by one sixteen-by-sixteen block per tile, drawn one
character per pixel. It is the source; the PNG is derived and must never be hand-edited.

The builder is deliberately rigid. A row that is not exactly sixteen characters, or a
character the palette does not define, is a **drawing mistake** and it fails rather than
padding — which it earned on its first run, catching a seventeen-character row that would
otherwise have shifted a tile by a pixel and been noticed by nobody.

Text in, raster out, on purpose. A tile change stays a reviewable diff, and the runtime
still gets a sheet it can blit a few thousand times a frame without rasterising anything
per load. That is the same trade
[ADR-0007](../../docs/adr/0007-a-figures-medium-is-decided-by-what-renders-it.md) made for
the hero figures.

**One palette, and it does not follow the reader's theme.** A game scene has its own
light, and honouring the theme toggle would mean two hand-drawn sheets plus a guard
nobody has written
([ADR-0013](../../docs/adr/0013-godot-is-a-design-tool-and-the-floor-keeps-one-palette.md)).

Three rules decide what goes in it, and the first version of this sheet broke all three:

- **Ramps are hue-shifted, never just darkened.** Wood goes red into shadow and yellow
  into light; the monitor shell goes blue into shadow. A ramp built by dropping the
  brightness of one hue reads as plastic.
- **Value is tiered by layer, and the floor is the darkest large area.** Carpet sits
  lowest, furniture in the middle, the cast highest in local contrast, so a person reads
  against a desk and a desk reads against the carpet. The first sheet had a mid-light
  carpet, near-white walls and wood brighter than either — everything fought and the
  walls won.
- **Tiles are designed edge-first.** A wall is a band inside the cell, not the cell.
  Filling the cell made a partition read four tiles thick where two rooms met, because
  each room drew its own perimeter; the band lets two rooms share one visible wall.

**The projection is 45 degrees — front plus a little top-down, not isometric.** You see
the front of a monitor and the front of a drawer. Anything drawn pure top-down (the first
chair was) sits at odds with everything around it.

## What is drawn from the sheet, and what is not

| From `tiles.tiles` | Drawn in code |
| --- | --- |
| Carpet, walls, windows, doors, desks, chairs, meeting tables, booths, racks, plants, printers, cabinets, the lobby's furniture | Which cell each of them lands in |
| | The **cast**, generated from a small set of parts, because sixty-five figures need variation nobody is going to draw sixty-five times |
| | Access points, segment swatches, coverage gradients, the legends |

**A pod is a bench.** Two desk rows butted together with people on the outside, facing
each other across a spine of monitors — which is what an open-plan floor is. The first
version alternated a row of desks with a row of people, which is not a layout any office
has. It is why there are two desk tiles and two chair tiles: the far side of the bench
shows the backs of its monitors, and a chair's back is on the side the sitter is not
facing.

Every sprite call has a flat fallback. If the sheet fails to load, the floor still draws
and the argument still stands — a missing decoration should not take the material down
with it.

## Godot proves the floor; it does not draw it

[ADR-0013](../../docs/adr/0013-godot-is-a-design-tool-and-the-floor-keeps-one-palette.md)
settles that Godot is design-time and **never** ships to the browser. That still holds.
What changed is what it is *for*.

```bash
python3 tools/floor/prove-topology.py            # walk the floor, report
python3 tools/floor/prove-topology.py --stamp    # walk it, then record the verdict
python3 tools/floor/prove-topology.py --check    # for CI: is the plate still proved?
```

The plate is hand-authored JSON and stays that way. Generating a layout in headless
GDScript is only writing the same coordinates in a language that reviews worse — the exact
objection ADR-0013 raised against `.tscn`. What Godot does instead is the thing that
cannot be asserted:

**It walks the floor.** [`godot/prove_topology.gd`](godot/prove_topology.gd) floods from
the lift lobby along circulation only and reports any room or space it cannot reach, and
any desk cell it would have to cross. On its first run it failed, and it was right to:
the lobby's door opened at x=5 while the corridor ring began at x=8, and the large room's
door opened at x=40 while the ring ended at x=37. **Two doors opening onto nothing, in a
plan that looked fine.** Neither would have survived the proof and neither was going to be
caught by eye.

`--stamp` records the date, the verdict and a fingerprint of the plate's *geometry* — the
rectangles, the doors, the circulation, the pods, and nothing else, so renaming a room does
not invalidate a proof while moving a wall does. `--check` compares that fingerprint, which
is why **a clone without Godot is not stuck**: it skips the walk, still catches a plate
that has moved since anyone proved it, and exits 0. The promise that a reader installs
nothing is a promise to the reader; a contributor moving a wall installs Godot.

**What it does not check, deliberately:** corridor widths, egress distances, travel
distance to an exit, sanitary provision. Those are architecture, and
[ADR-0014](../../docs/adr/0014-the-plate-stops-at-topology.md) is where the line is
argued.
