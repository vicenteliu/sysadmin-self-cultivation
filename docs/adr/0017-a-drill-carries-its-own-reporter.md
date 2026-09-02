---
kind: adr
axis: meta
themes: []
platforms: []
summary: "Twenty-three drills carry the same fifteen-line reporter, copied by hand, and two dialects of it have already drifted apart. The obvious fix is a shared module. The decision is the opposite: a drill imports nothing from this repo, the reporter is a vendored block with one canonical copy, and check.py asserts every copy is byte-identical."
---
# A drill carries its own reporter

> 🌐 **Languages:** English (default) · [中文](../zh/docs/adr/0017-a-drill-carries-its-own-reporter.md)

Every drill in this repo ends the same way: a `log()`, a `step()`, a `check()` that prints
✓ or ✗ and accumulates failures, and a verdict that exits `0` only if every lesson held.
[`runnable-lab`](../../.claude/skills/runnable-lab/SKILL.md) prescribes that pattern, and
twenty-three files follow it — by carrying the same fifteen lines, pasted in by hand,
one copy each.

Left alone, copies drift, and these have. Nine drills define `check()` at module scope
with a `FAILURES` list; the rest define it as a closure inside `main()`. One family prints
`✓` and `✗` under a `=== 3. title ===` banner; the other prints `OK` and `XX` under
`[3] title`. Nothing is wrong with either, and nothing decided between them — they are two
authors' habits, and a third author would reasonably produce a third.

The obvious fix is a shared module: one `labkit.py`, imported by every drill, edited in
one place. This record exists because that fix is refused.

## Decision

**A drill imports nothing from this repo.** [`CONTEXT.md`](../../CONTEXT.md) defines a
lab as *pure-local, zero-dependency, self-verifying*, and the dependency it means is not
only `pip install`. A drill is read on a GitHub page, copied into a terminal, and run;
the first thing it may not do is fail with `ModuleNotFoundError: labkit`, because a lab
whose first lesson is *you needed the rest of the repo* has taught the wrong thing about
this repo.

**The reporter is a vendored block.** One canonical text — `log`, `step`, `check`, and
the verdict — is copied verbatim into every drill. It is the reporter only: the fixture
data, the model, the lessons and the `--break-it` mechanism stay the drill's own, because
those are what a drill *is* and the reporter is only how it speaks.

**[`check.py`](../../check.py) owns the canonical copy and asserts every drill matches
it, byte for byte.** A copy that diverges is a failing check, not a stylistic choice.
That turns twenty-three pasted copies from a liability into a verified convention — the
thing `check.py` already tries to do by hand for its own `slug()`, whose docstring says
*byte for byte with* another file and has no way to know whether that is still true.

**The block is `✓` / `✗` under `=== n. title ===`.** The skill prescribed that before this
record did; the other dialect converges on it, one edit per drill.

**A drill written in shell carries the same contract in shell**, and is checked against
a shell block or named as exempt in `check.py --list`. What it may not be is skipped in
silence — the failure this repo keeps rediscovering.

## Considered options

- **A shared `labkit.py`, found via `sys.path`.** One edit, no drift, the textbook answer.
  Rejected for the reason above: it changes what a drill is. Every drill would gain a
  line that only works inside this checkout, and the glossary's definition would have to
  grow an exception it cannot explain to a reader who copied one file.

- **Leave the copies as they are, unchecked.** The status quo, and it is what produced
  two dialects in under three months. Rejected on the same lesson as
  [ADR-0008](0008-a-count-is-not-a-bound.md): a convention that lives only in prose and
  habit is a convention nobody is checking, and twenty-three copies with no guard are
  twenty-three places to drift.

- **Generate drills from a template.** The reporter would be the template's and the
  lessons the author's. Rejected because it inverts which half matters: a drill is prose
  with assertions, and the prose is the part a template would own least well. A generator
  also becomes a second thing to run, which the check-and-build chain does not need.

- **Check the copies loosely — a fingerprint, or *contains a `check()` function*.**
  Rejected because a loose check admits the drift it was meant to end. Byte-identical is
  the only assertion that means *this is the block*, and it costs nothing more to make.

## Consequences

- **`check.py` gains a constant and a check.** The block lives in `check.py` as text,
  `--list` can print it, and the drills group compares every `*_drill.py` against it. The
  [`runnable-lab`](../../.claude/skills/runnable-lab/SKILL.md) skill points at that
  constant rather than carrying a second copy of it.
- **Every drill is edited once** to converge on the block — a mechanical change, one
  file at a time, with the clean run and the `--break-it` run both still exiting as they
  did before.
- **Editing the block is a twenty-four-file change, by design.** That cost is the point:
  a reporter that changes rarely and everywhere at once is a convention, and one that
  changes in one place is a dependency. Anyone who finds the cost too high has found the
  argument for `labkit.py`, and should reopen this record rather than route around it.
- **The bash drill is not exempt from the contract**, only from the Python block. Its
  `check()` prints the same marks and counts the same failures; `check.py` says so in
  its listing rather than leaving the reader to wonder why one lab is missing.
- **A drill stays copyable.** That was the invariant all along; this record is what
  makes it a decision rather than a habit.
