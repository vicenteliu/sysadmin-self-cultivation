---
kind: adr
axis: meta
themes: []
platforms: []
summary: "the-reference-office.md sits at the root, is cited by forty-six files and is the premise of both routes, and the table of six axes has never had a row for it. It is not a seventh axis and it is not being moved: it is the repo's one fixture — a named scenario the routes and labs reason against — and that shape now has a word."
---
# The reference office is a fixture, not an axis

> 🌐 **Languages:** English (default) · [中文](../zh/docs/adr/0016-the-reference-office-is-a-fixture-not-an-axis.md)

[`the-reference-office.md`](../../the-reference-office.md) is the largest document in the
tree. It sits at the root beside the front door, forty-six files cite it, and both routes —
[`build-out/`](../../build-out/) and [`walkthrough/`](../../walkthrough/README.md) — take it
as their premise. [ADR-0002](0002-the-reference-office-is-parameters-not-a-bill-of-materials.md)
rules on what it may contain and [ADR-0015](0015-the-reference-office-consumes-services-and-operates-none.md)
on what it may not, and neither says what it *is* in the structure. The table of six axes
in [`CONTENTS.md`](../../CONTENTS.md) has no row for it, and the map on the front door does
not draw it.

The repo's own test for an axis is the one [ADR-0001](0001-the-build-out-is-a-route-not-a-seventh-axis.md)
wrote and [ADR-0005](0005-the-site-is-a-view-not-a-seventh-axis.md) applied a second time:
*something that teaches no new page is not an axis.* The reference office fails that test
in the other direction. It holds pages nothing else holds — the occupancy curve, the
desk count, the wireless derivation, six parameter domains and a demand ledger — so the
test admits it, and everything about its position in the tree says *seventh axis* except
the one table that would have to say so. That is the shape
[ADR-0008](0008-a-count-is-not-a-bound.md) warned about: a structure nobody has named is
a structure nobody is checking.

It is the wrong shape for an axis all the same. An axis is a **way of reading** one body
of material — by platform, by layer, by theme. The reference office is not a way of
reading anything. It is a **piece of the material** that two routes and four labs reason
*against*, and a reader does not enter the repo through it any more than they enter a
textbook through its worked example.

## Decision

**The reference office is the repo's one fixture.** A fixture is a named, parameterised
scenario that routes and labs reason against and that belongs to no axis — which is why
it lives at the root, beside the things that also belong to every axis and to none. It is
not an axis, not a route and not a view; it is the third kind, and there is exactly one.

**[`CONTENTS.md`](../../CONTENTS.md) lists it as such**, in the same table that lists the
six axes and the two routes, so the structure has a row for every shape it contains.

**A second fixture is a second file with its own name.** [ADR-0015](0015-the-reference-office-consumes-services-and-operates-none.md)
already said this for a product side — *a separate named scenario, its own file, its own
parameters* — and this record makes it the rule for the kind rather than for that one
case. A fixture that arrives as a section of another fixture has arrived unannounced.

**The word is reserved.** *Fixture* here never means a test fixture, a light fitting or
the furniture on the floor; the glossary carries the entry.

## Considered options

- **Promote it to a seventh axis.** It would give the file a row and a place on the map
  at no cost but the drawing. Rejected because it is false: an axis row in `CONTENTS.md`
  reads *enter here when you want to…*, and nobody enters the material through a
  parameter table. Calling it an axis would also put it beside `platforms/` as a peer, and
  the two are not peers — one is a way to read the other.

- **Move it under `build-out/`.** ADR-0002 ruled that *content that exists to serve a
  recording belongs with the recording*, and the build-out is the route that leans on it
  hardest. Rejected because it serves two routes, not one, and forty-six files besides;
  the move would be paid in every one of those links plus a Chinese mirror, and no reader
  would find the file more easily for it. A rule about coupling does not become a rule
  about directories.

- **Leave it unnamed.** The status quo, and the cheapest. Rejected on ADR-0008's lesson:
  it was already a seventh axis in every respect but the table, and the next reader to
  notice would have had no record saying that was deliberate. It was not deliberate; it
  was unexamined, which is the thing a decision record exists to end.

## Consequences

- **`CONTENTS.md` gains one row and one word.** The table that lists six axes and two
  routes now also lists one fixture, and the front-door map is not redrawn for it — a map
  of the ways in does not need to show the thing they are ways in *to*.
- **The glossary's reference-office entry says where it sits**, not only what it is, and
  the *Axis* entry names it among the things that are not axes.
- **Nothing in `check.py` enforces this.** A fixture is a file, not a directory, and the
  rule is editorial: it is honoured by the row in `CONTENTS.md` and would be broken by a
  second scenario appearing inside this one. That is the same kind of rule ADR-0015 left
  in prose, and for the same reason — there is nothing mechanical to count.
- **Every lab that says *a hundred-person office* is still not citing this file**, and
  the glossary's rule still stands: where a lab's number and the fixture's derivation are
  both live, the derivation wins. Naming the fixture did not change the rule; it gave the
  rule a subject.
