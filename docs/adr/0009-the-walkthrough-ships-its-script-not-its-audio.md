---
kind: adr
axis: meta
themes: []
platforms: []
summary: "The repo is adding a narrated walkthrough of the reference office — the first material here meant to be heard rather than read, and the first with a distribution channel outside the repository. The audio for it will not be in the tree, which needs a reason on the record."
---
# The walkthrough ships its script, not its audio

[`walkthrough/`](../../walkthrough/README.md) is a narrated pass through
[the reference office](../../the-reference-office.md): a hundred-person floor, told in
order, in a register the rest of this repo deliberately does not use. It is the first
material here written to be **spoken by a machine and heard by a person**, and the first
with a distribution channel outside the repository — a podcast feed.

Two questions arrived with it, and neither answered itself. Is a story a new axis? And
where does the audio live?

## Decision

**The walkthrough is a route, and the repository ships the script only.**

**A route, not an axis.** Same test as [ADR-0001](0001-the-build-out-is-a-route-not-a-seventh-axis.md)
and [ADR-0005](0005-the-site-is-a-view-not-a-seventh-axis.md): *does it teach a new page?*
It does not. Every fact in the first walkthrough already sits in
`the-reference-office.md`, `cross-cutting/site-network-design.md` or
`build-out/05-network.md`. What it adds is an **order** and a **register**. Its sequence
is nonetheless its own — that first walkthrough spans three files across two axes plus the
root — so it is not `build-out/`'s sixteen steps with a voice on top, and the numbering
does not correspond.

**The script is a first-class document; the audio is not in the tree.** A
`walkthrough/*.md` is Markdown with front-matter like everything else here: GitHub renders
it, `docs/index.json` records it, the search corpus holds it, a `--check` can catch it
going stale. The audio is generated — by a reader with their own TTS credentials, or by
the author for publication — and no recording is committed.

**The file contains only the words that get spoken.** No tables, no inline links, no *as
the table above shows*, no parenthetical asides; numbers written the way they are said.
Cross-references live in the front-matter's `sources:`. This is
[ADR-0007](0007-a-figures-medium-is-decided-by-what-renders-it.md)'s argument reused —
*the source and the artifact are the same object, so they cannot disagree*. `cat` the file
and you have the TTS input, with no extraction step in between to drift.

**A published walkthrough freezes.** Its front-matter carries `published:` and a
fingerprint of each `sources:` file as it stood that day. After that the script is not
edited: an error becomes an **erratum** recorded in the document — *the audio says X; X is
wrong* — because a recording on a podcast host cannot be amended and a silent fix would
leave it lying to every listener. A checker reports when a source has moved underneath a
published walkthrough, which is the only reliable signal that an episode needs
re-recording.

## Considered options

- **Read the existing prose aloud.** The tidiest answer: no new words, no new file kind,
  ADR-0005 untouched. Rejected on what it sounds like. This repo's prose is deliberately
  terse, declarative and table-heavy — an editorial choice worth keeping — and a speech
  engine reading it produces a lecture, which is the one thing the walkthrough exists not
  to be. The register is the deliverable, and register does not survive being read out of
  a document written for the eye.

- **A seventh axis.** Rejected on ADR-0001's test, which it fails plainly: the first
  walkthrough teaches no fact the repo did not already hold. Filing it as an axis would
  also have obliged it to be complete across the material, and it is explicitly not — it
  grows one episode at a time, demand-first, the way `toolbox/` does.

- **A separate repository, or a desktop application.** Genuinely tempting, because the
  floor is a game scene and a game engine would be at home. Rejected because the material
  would **fork**, and the fork would be the copy people actually watch — the same failure
  ADR-0001 and ADR-0005 have each already rejected once. A satellite gets no front-matter,
  no place in the retrieval index, no mirror, and nothing to catch it going stale.

- **Commit the audio.** Rejected on two counts. Binary artifacts of that size would dwarf
  even the vendored bundle [ADR-0006](0006-the-viewer-vendors-its-dependencies.md) had to
  justify, and they would be **wrong for most readers anyway**: a listener's own TTS voice,
  language and speaking rate differ from the author's, so a committed recording serves one
  person and bloats the tree for everyone else.

## Consequences

- **Three artifacts must each stand alone, because three audiences each lack one thing.**
  A GitHub reader has no picture and no sound. A viewer user may have no sound. A podcast
  listener has **no screen** — which is the constraint that decides the most, and the one
  easiest to forget while looking at a screen. The script must read complete, the floor
  must browse complete, the audio must hear complete.
- **The honesty markers have to be spoken.** A 🔨/🧭 badge drawn on the floor does not
  exist on the podcast channel, so the walkthrough's narrator says the boundary out loud
  and in character when the footing changes. In the first episode it changes once, from
  the 🔨 segmentation and addressing material to the 🧭 wireless arithmetic that
  `the-reference-office.md` already flags as drawn from vendor engineering guidance rather
  than from having lived with a deployment.
- **`site/README.md` and `ROADMAP.md` acquire a new thing to describe**, and `CONTENTS.md`
  a new route. The walkthrough is not in the axis list and does not get a card, for the
  reason ADR-0005 gave when it kept `build-out/` off one.
- **The erratum discipline will look strange the first time it is used.** Leaving a known
  error in a document with a note beside it reads as sloppiness until you remember the
  recording cannot be changed. It is the same reasoning `docs/questions.md` uses when it
  refuses to delete an answered line.
