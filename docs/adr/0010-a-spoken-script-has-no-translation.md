---
kind: adr
axis: meta
themes: []
platforms: []
summary: "English is this repo's source of truth and docs/zh/ is a mirror that may lag. A walkthrough script breaks that model, because the thing a translation destroys is the thing a spoken script is made of."
---
# A spoken script has no translation

> 🌐 **Languages:** English (default) · [中文](../zh/docs/adr/0010-a-spoken-script-has-no-translation.md)

This repo has one rule about language and it has held for every document so far: **English
is the source of truth, `docs/zh/` is a mirror, and where they disagree the English
wins.** `docs/build-index.py` implements it — everything under `docs/zh/` is skipped on
the first pass and re-attached as `derived: true` with a `mirrors:` pointer — and
`site/js/nav.js` reads that relationship to prefer the mirror when the interface is in
Chinese.

A [walkthrough](0009-the-walkthrough-ships-its-script-not-its-audio.md) does not fit it.
A mirror is a translation, and translation preserves facts while destroying cadence —
which is exactly backwards for a document whose entire value is how it sounds when spoken.
A Chinese script rendered from English breathes in English, and an English script rendered
from Chinese breathes in Chinese. Both are correct and both are unlistenable.

## Decision

**Two scripts per episode, neither derived from the other, both bound to one set of
sources.**

`walkthrough/01-….en.md` and `walkthrough/01-….zh.md` sit side by side in the route's own
directory. Each is canonical **for its own cadence**. Neither carries `derived: true`;
neither points at the other with `mirrors:`.

**"English wins" is narrowed to what it was always actually about — the facts.** Both
scripts declare the same `sources:`, and those sources are English Markdown. A
disagreement between the two scripts is not settled by preferring one script; it is
settled by reading the source both of them are accountable to. That is a smaller claim
than the old rule made, and a truer one.

**The Chinese script does not live under `docs/zh/`.** Position is a claim about
relationship, and that directory says *translation* — both to `build-index.py`, which
would stamp the file `derived`, and to a person reading the tree. Putting a canonical
document there and then writing an exception to un-say it is worse than not saying it.

## Considered options

- **Follow the existing rule: English canonical, Chinese mirrored.** Rejected on the
  product. The author narrates in Chinese and the podcast starts in Chinese, so the
  mirrored script is the one that gets recorded — meaning the recorded artifact would be a
  translation of a document written to be spoken in a language nobody was going to speak
  it in.

- **Invert the rule for this kind only: Chinese canonical, English mirrored.** Rejected
  because it does not fix anything, it only moves the damage to the other language. The
  English episode would then be a translation of Chinese cadence, and this repo's default
  audience reads English.

- **Put the Chinese script under `docs/zh/walkthrough/` and add an exception to
  `build-index.py`.** Rejected. It means editing a generator that currently guards 191
  records, so that a special case can cancel out a signal the directory itself was sending.
  The cheaper fix is to not send the signal.

- **One script, one language, no second version.** Rejected as a decision disguised as a
  simplification. The repo already carries a Chinese mirror because the audience is real;
  dropping it for the one format meant to be *heard* — the most accessible format here —
  would be the wrong place to economise.

## Consequences

- **`docs/index.json` gains a pair of full records where it used to gain a record and a
  mirror.** Both scripts count as documents. The mirror-coverage badge does not move, and
  should not: nothing has been mirrored.
- **The two scripts will diverge, and that is allowed.** Same beats, same sources, same
  order, different jokes and different sentence lengths. What is *not* allowed is a fact in
  one that is absent from the other's `sources:`, which is the thing the shared source list
  exists to make checkable.
- **The viewer needed a new affordance, and shipped without it first.** Everything in the
  navigation had been either canonical-English or a `derived` Chinese mirror, and both
  scripts are canonical — so on the first build an English reader got a Chinese title in
  the sidebar and, on the English script, a meta bar reading *no Chinese mirror yet*,
  which was simply false. The fix is three small pieces: `docs/build-index.py` records a
  document's own `language:` and its `counterpart:` when the front matter declares them,
  the navigation lists the script written in the language on screen — the same hiding it
  already does for the 26 mirrors, applied to a sibling instead of a derivative — and the
  meta bar offers `🌐 中文` / `🌐 English`, labelled in the language you are going to and
  never called a mirror.
- **The prediction was in this ADR and it still shipped broken.** The paragraph this one
  replaces said the viewer would need a different affordance. Writing that down did not
  build it, and nothing mechanical could have caught it: no `--check` in this repo knows
  what a sidebar looks like to a reader. That is the same admission
  [ADR-0008](0008-a-count-is-not-a-bound.md) had to make about a bound living only in
  prose.
- **This is a narrowing of the language rule, not a repeal.** Every other document in this
  repo is unaffected: English is still the source of truth, `docs/zh/` is still a mirror,
  and the badge still says how far behind it is. What changed is that the rule now says
  which of its two jobs it was doing.
