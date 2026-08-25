# The honesty markers are ⚒️ and 🧭, not ✋ and 🧗

Every module in this repo marks what is **hands-on depth** and what is an
**honest ramp**. `WHY.md` argues that the distinction is the whole point, and
`README.md` puts it in the seventeenth line, before the table of contents. The
markers are therefore the most-read glyphs in the repository — they appear 591
times across 104 files, and one of them is the first thing a stranger sees.

They were `✋` and `🧗`, and both were chosen for what they mean rather than for
how they read.

## Decision

**Hands-on depth is `⚒️`. A verified ramp is `🧭`.** The other markers — `✅`
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

`⚒️` and `🧭` are objects, not figures: no skin tone, stable rendering, and an
**X-cross against a circle** — legible as two different things at a glance and
at any size. The metaphors survive the change: a pick is what you dig depth
with, and a compass is what you carry into terrain you have not walked, which is
this repo's definition of a ramp.

## Considered options

- **`🛠️` for hands-on depth.** Rejected on a **term collision**. This repo has a
  `toolbox/` axis and a `toolbox-picker` skill; a crossed-tools glyph would put
  "what I can do" and "what the repo ships" behind the same symbol, and those
  are different claims. `⚒️` reads as *dig* rather than *toolkit* and keeps them
  apart — though it is the nearest miss, and the residual likeness is the price.

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

## Consequences

- **The rewrite is 591 occurrences across 104 files, and it is one-way.**
  Reverting is a second rewrite of the same size, which is why the reasoning is
  recorded here rather than in a commit message.
- **`⚒️` must carry U+FE0F.** U+2692 defaults to *text* presentation and renders
  as a monochrome glyph without the variation selector. `🧭` (U+1F9ED) needs
  none. Anything generating these markers must emit `⚒️`, not `⚒`.
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
