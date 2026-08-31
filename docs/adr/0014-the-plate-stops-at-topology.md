---
kind: adr
axis: meta
themes: [networking]
platforms: []
summary: "The floor the walkthrough plays over was structurally wrong: rooms floating in the middle of the plate with no circulation, no core and doors opening into the desks. Fixing it means drawing a floor plan, and a floor plan is architecture — which this repo has already judged is not its depth."
---
# The plate stops at topology

The floor the walkthrough plays over was wrong in a way that had nothing to do with
pixels. Rooms floated in the middle of the plate, each drawing its own complete perimeter
so that two neighbours produced two walls; nothing connected the lift lobby to anything;
doors opened straight into the desks; there was no core, no corridor and no second way
out. It read as a diagram of some rooms rather than as a floor.

Fixing that means drawing a floor plan. And a floor plan is architecture — corridor
widths, egress distances, sanitary provision, how deep open plan may sit from a window —
which is exactly the ground [`build-out/GAPS.md`](../../build-out/GAPS.md) already judged
and refused:

> Commissioning a room from a shell is physical work with contractors. The rack-side
> habits are covered in `platforms/self-host/`; the building-side is 🧭 and stays so.

[`docs/questions.md`](../questions.md) narrowed the same request once before, keeping
MDF/IDF, riser and path-to-the-edge and cutting containment, tray, pull schedules and
construction sequencing. The things a correct floor plan needs are deeper than the things
that were cut.

## Decision

**The plate carries topology and stops there.** It is
[`walkthrough/reference-office.plate.json`](../../walkthrough/reference-office.plate.json):
the spaces, what each one is, what it is next to, and how you walk from any of them to any
other. *Who is beside what, and how you get there.*

**It does not carry, and must not acquire:** corridor widths, egress distances, travel
distance to an exit, sanitary provision, occupancy load, depth-from-window limits, or any
statement that the plan would pass anything. A floor drawn to look like it complies, that
nobody qualified has checked, is worse than one that visibly does not try.

**Circulation is explicit data, not the gaps between things.** A ring runs inside the
shell and every enclosed space opens onto it. That is the claim being made, so it is
written down and checked rather than left to be inferred from where the furniture is not.

**The topology is proved, not asserted.** A headless Godot project at
[`tools/floor/godot/`](../../tools/floor/) walks the plate: from the lift lobby, along
circulation only, reaching every space without crossing a desk cell. The plate stores the
result as a fingerprint of what was proved, so a plate edited afterwards reports that
nobody has re-proved it. Godot is design-time and check-time and never ships
([ADR-0013](0013-godot-is-a-design-tool-and-the-floor-keeps-one-palette.md)).

**The plate is shared; an episode is not.** Geometry and identity belong to the reference
office and every walkthrough draws the same floor. What an episode owns is its panels and
its beat cues — which is where the weight actually is: the first episode's props are five
times the size of the geometry, and they are all about networking.

## Considered options

- **Borrow a floor-plan dataset.** [CubiCasa5k](https://github.com/CubiCasa/CubiCasa5k),
  [HouseExpo](https://github.com/TeaganLi/HouseExpo),
  [MLStructFP](https://github.com/MLSTRUCT/MLStructFP) and ResPlan all publish structured
  plans, and one of them could have backed the layout. Rejected on a fact: **they are
  residential.** Houses and apartments, annotated for machine learning. Citing a corpus of
  flats as authority for an office floor would be a worse overclaim than drawing it by
  hand and saying so, because it would look sourced.

- **Draw the plan properly — circulation widths, egress, sanitary counts.** The version
  that would actually be right, and the one to reach for if this repo ever acquires an
  architect. Rejected because it would have this repo assert, in a picture, a competence
  its own honesty markers say it does not have. The failure would be silent: nobody reads
  a floor plan looking for the claim it is making.

- **Leave the plate as scenery and stop calling it a plan.** Tempting, and it is what the
  first version effectively was. Rejected because the walkthrough already argues from
  adjacency out loud — the store beside the IDF because that is the path a broken laptop
  takes, the tea point far from both because its job is noise. Those are topology claims.
  A stage that contradicts them is worse than no stage.

- **Infer circulation from empty space.** No corridor data; let the reader see the gaps.
  Rejected because it cannot be checked, and an unchecked claim about how a floor works is
  the class of thing this repo files under 🧭 rather than draws.

## Consequences

- **Godot becomes a build-time dependency for changing the layout, and for nothing else.**
  ADR-0013 already accepted that trade: the promise about installing nothing is a promise
  to the *reader*, and the reader still installs nothing. A clone without Godot skips the
  proof, still compares the fingerprint, and is told when a plate has moved since anyone
  last proved it.
- **A room can no longer be moved casually.** It has to still open onto circulation, and
  the proof will say if it does not. That is the intended cost.
- **`the-reference-office.md` gains three support spaces and a boundary sentence, not a
  plan.** The document stays parameters and derivations; the plate stays geometry. Neither
  grows into the other.
- **What the floor cannot answer, it should not imply.** *How wide is that corridor* and
  *where is the second exit* have no answer here, and the honest response is to say which
  question the plate was built to answer instead.
