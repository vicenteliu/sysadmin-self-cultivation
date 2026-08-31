---
kind: adr
axis: meta
themes: []
platforms: []
summary: "The floor is a game scene, and a game engine is the obvious way to build one. Shipping that engine would undo the decision that the viewer installs nothing — so Godot stops at the export step, and the pixel art that comes out of it does not follow the reader's theme."
---
# Godot is a design tool, and the floor keeps one palette

The [floor](0011-the-floor-renders-the-reference-office-and-may-not-compute-it.md) is a 2D
game scene, and the obvious way to build a game scene is a game engine. Godot has a tile
editor, a scene tree and an HTML5 export; laying out a hundred-and-ten-port office by hand
in JavaScript coordinates is not obviously the better plan.

But [ADR-0006](0006-the-viewer-vendors-its-dependencies.md) already fought this fight for
the viewer and won it on a specific requirement: **the direct path is one command with
nothing installed**, and it works on a plane. Two of the four options it rejected were
rejected for being install steps wearing other names.

## Decision

**Godot never reaches the browser. It is a design-time tool whose output is data.**

The scene is laid out in Godot, and what leaves it is a JSON of tile placements, prop
positions and beat-addressable camera targets, plus sprite sheets. The runtime in `site/`
is hand-written Canvas2D and does not know Godot exists — the same shape as
`build-diagrams.py`, which turns an authored source into a committed artifact the viewer
consumes without a toolchain.

**The art is half drawn and half generated.** Scenery — floor, walls, furniture, racks —
is authored raster pixel art, because procedural drawing has a visible ceiling and the
point of borrowing this form is that it looks like a place rather than a diagram. The
**cast** is generated in code from a small set of parts, because sixty-five figures need
variation no one is going to draw sixty-five times. This is the division the form's
existing example already arrived at, and it is worth copying rather than rediscovering.

**The floor has one palette and does not follow the reader's theme.** Everything else the
viewer renders swaps on the theme toggle: mermaid re-renders, hero diagrams switch between
derived light and dark variants under a mechanical inversion rule stated in
`sysadmin-brass.profile.md`. That rule works because those artifacts are text. Raster
pixel art is not, and honouring the toggle would mean two hand-drawn sprite sheets plus a
`--check` to keep them in step. **A game scene has its own light.** The palette is drawn
from the brass skin so it belongs to this repo, and it is fixed.

**Everything that produces the floor is committed** — the Godot project, the sprite
sources, the export script, and its output — with a `--check` reporting when the output is
behind its source. ADR-0007 settled this for figures and even committed the style profile
itself, on the reasoning that a clone must be able to rebuild what it can see.

## Considered options

- **Ship Godot's HTML5/WASM export as the runtime.** Rejected on four counts, any one of
  which would have been enough. The engine blob is an order of magnitude past the 2.5 MB
  bundle ADR-0006 needed a whole decision record to justify, and that bundle bought
  full-text search — nothing here buys as much. Editing the floor would require the Godot
  editor, which is the install step ADR-0006 refused twice. `serve.py` is
  `http.server` and sends no cross-origin isolation headers, so the threaded export would
  need work on both server paths. And the scene source becomes `.tscn` and `.gd`, which
  cannot be reviewed in a diff — the exact inverse of ADR-0007's reason for preferring
  mermaid, that *the source and the picture are the same object*.

- **Hand-place everything, no Godot at all.** Rejected as false economy. Tile layout is
  what a tile editor is for, and the alternative is coordinates typed into a JSON file by
  someone who cannot see what they are typing.

- **Fully procedural art, including scenery.** The version this decision started as, and
  it survives in the cast. Rejected for the scenery because the ceiling is real and
  visible: generated furniture reads as a diagram of a room rather than a room, and the
  form was borrowed precisely for the difference.

- **Two sprite sheets, one per theme.** Rejected on cost against benefit. It doubles every
  art change, needs a guard nobody has written, and buys consistency with a toggle that a
  game scene has no reason to obey.

- **Do not commit the Godot project; keep only the export.** Rejected on ADR-0007's
  ground for refusing a hand-written dark variant: it makes the layout a one-way door.
  After the first export, the only way to move a wall would be to edit JSON by hand.

## Consequences

- **`site/README.md`'s theme row becomes wrong and must be amended.** It currently says the
  theme follows the system setting, that mermaid re-renders and hero diagrams swap
  variants. The floor is the first thing here that opts out, and the README should say so
  rather than let a reader find it.
- **The repo grows binary art.** Sprite sheets are not large next to the vendored bundle,
  but they are the first committed assets that cannot be diffed. Treat an art change as its
  own commit, the way ADR-0006 asks for the vendored pair.
- **Godot must be installed to change the layout, and that is acceptable** precisely
  because it is never needed to *read* or *run* anything. The zero-install promise is about
  the reader, and the reader is untouched.
- **The first episode did not use Godot at all, and this ADR is not wrong about that.**
  Forty-eight by thirty tiles, seven rooms and twelve desk pods were faster to type than
  to stand a toolchain up for, so `01-the-network.floor.json` was authored directly and
  `tools/floor/` holds no Godot project. What this decision fixes is the *boundary* —
  design-time yes, shipped never — and the boundary binds whether or not the tool has
  been reached for. [`tools/floor/README.md`](../../tools/floor/README.md) says plainly
  that it has not, because describing a plan as a fact is the failure this repo's
  markers exist to catch.
- **The scenery is authored as text and derived to raster, which is a smaller claim than
  this ADR first made.** `tiles.tiles` is drawn one character per pixel and
  `build-tiles.py` emits the PNG. The look is the hand-drawn one the decision wanted; the
  storage is diffable, which the decision had assumed it could not be. The line about
  "the first committed assets that cannot be diffed" turned out not to apply — the
  derived sheet is committed, but its source is text and reviewable.
- **The generated cast is the part most likely to disappoint.** If sixty-five figures built
  from parts read as repetitive, the fallback is a small number of drawn figures with
  recoloured variants — which changes the art pipeline and no decision above it.
