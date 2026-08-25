---
kind: adr
axis: meta
themes: []
platforms: []
summary: "Every module in this repo marks what is hands-on depth and what is an honest ramp."
---
# The honesty markers are 🔨 and 🧭, not ✋ and 🧗

Every module in this repo marks what is **hands-on depth** and what is an
**honest ramp**. `WHY.md` argues that the distinction is the whole point, and
`README.md` puts it in the seventeenth line, before the table of contents. The
markers are therefore the most-read glyphs in the repository — they appear 591
times across 104 files, and one of them is the first thing a stranger sees.

They were `✋` and `🧗`, and both were chosen for what they mean rather than for
how they read.

## Decision

**Hands-on depth is `🔨`. A verified ramp is `🧭`.** The other markers — `✅`
done, `🚧` planned, `❌` overclaim, `⚠` warning, `🌐` language — are unchanged.

The markers carry meaning in two places at once: a reader scanning a dense table
sees a glyph, and a reader stopping on one reads a claim. `✋` and `🧗` were
built for the second reader and failed the first.

- **`✋` reads as *stop*.** Its intended sense was *hands-on* — the hand,
  literally. But the raised palm is a halt gesture in almost every context a
  reader has met it in, and the pun that rescues it only works in one language.
  A marker that carries the repo's central promise cannot depend on a pun.
- **Both were human figures**, so both took skin-tone modifiers, rendered
  differently on every platform, and collapsed toward each other in monochrome
  fallback.
- **Their silhouettes were the same shape.** Two vertical figures, side by side
  in rows like `✅ ✅ ✅ | 🧗 + Entra/identity ✋`, are distinguishable only by
  stopping to look — which is the one thing a scan-line marker must not require.

`🔨` and `🧭` are objects, not figures: no skin tone, no variation selector, and
a **solid diagonal against a circle** — legible as two different things at a
glance and at any size. The metaphors survive the change: a hammer is what the
thing was built with, and a compass is what you carry into terrain you have not
walked, which is this repo's definition of a ramp.

## Considered options

- **`🛠️` for hands-on depth.** Rejected on a **term collision**. This repo has a
  `toolbox/` axis and a `toolbox-picker` skill, and `🛠️` is the near-universal
  glyph for *tools* and *settings*; it would file "what I can do" and "what the
  repo ships" behind one symbol, and those are different claims. A single `🔨`
  reads as *this was hammered out* rather than *here is a kit* — a narrower
  margin than it sounds, and the honest name for it is a judgement call, not a
  clean win.

- **`⚒️` for hands-on depth.** Chosen first, shipped across 104 files, and
  corrected a day later. It is kept in this record because the reason it failed
  is the most transferable thing here — see **The correction**.

- **`⚓` for hands-on depth.** Rejected late, and it had been the recommendation
  until the word was checked rather than the character. The character was unused;
  the *word* was not. **Anchor is already this repo's verb for ramping** —
  `ai-workflow/how-i-use-ai-to-learn-and-operate.md` numbers it Rule 2, *"Anchor
  everything to what you already know"*, and all four `ai-ramp.md` notes repeat
  it. Pointing `⚓` at depth would have aimed a symbol at the opposite of what
  its word already meant, three lines away from where the word is defined.

- **Renaming the ramp rule to free `⚓`.** Rejected. The rule is good and it is
  numbered; moving a piece of the method to make room for a glyph inverts what
  serves what.

- **Keeping `✋`/`🧗` and explaining them in a legend.** Rejected, and this is
  the option the change exists to refuse. A marker that needs a note to avoid
  being misread has already failed at the only moment that matters — the glance
  it was put there to survive.

- **Changing the whole palette.** Rejected. `✅` alone appears 261 times and its
  meaning is not in question. Changing symbols that work, in the same pass as
  symbols that do not, would make the diff unreadable and the reason unrecoverable.

## The correction

The first version of this decision chose `⚒️` (U+2692, HAMMER AND PICK) and
appended U+FE0F — and this document said so in its own consequences: *anything
generating these markers must emit the selector*. The instruction was followed
exactly, in all 104 files, and it was not enough.

**A variation selector only *requests* emoji presentation. It does not create a
colour glyph.** U+2692 defaults to text presentation, so a font shipping no
colour glyph for it renders a small monochrome symbol — directly beside `🧭`
(U+1F9ED), a native emoji codepoint that is in colour everywhere. The result was
worse than either marker alone: an asymmetric pair in which one side read as
punctuation. On the README the change looked as though it had not happened, which
is how it was caught.

The rule this leaves behind is short enough to apply without re-deriving it:
**a codepoint that needs a selector to be an emoji is not a marker.** Choose from
the native-emoji range, where colour is not a font's decision to make.

`🔨` is U+1F528 — one codepoint, no selector, colour everywhere. The cost of
learning it the slow way was a second rewrite of 327 occurrences across 103
files, one day after the first.

## Consequences

- **The rewrite is 591 occurrences across 104 files, and it is one-way.**
  Reverting is a second rewrite of the same size, which is why the reasoning is
  recorded here rather than in a commit message. The correction above then cost
  a further 327 — evidence for that sentence rather than against it.
- **Markers render in colour without help.** Both `🔨` (U+1F528) and `🧭`
  (U+1F9ED) are native emoji codepoints, so nothing that generates them needs to
  know about variation selectors.
- **Markers live inside mermaid diagrams**, not only in prose and tables — in
  `the-stack/02-network.md`, `the-stack/03-compute-and-images.md`,
  `cross-cutting/kubernetes.md`, and the step template in `build-out/README.md`.
  A text substitution touches diagram source, so diagrams are re-validated after
  the change rather than assumed intact.
- **`honesty-audit` classifies claims by these markers**, so the skill is updated
  no later than the prose it classifies. A window in which the skill and the
  corpus disagree would produce confidently wrong audits.
- **The Chinese mirrors change with the canon.** `docs/zh/` states that English
  is the source of truth; markers that differ across the mirror would make that
  claim false in the one place it is easiest to check.
