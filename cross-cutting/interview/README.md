# cross-cutting/interview/

> [`skills-maps/`](../skills-maps/README.md) answers *what can I do.* This answers
> *how do they check* — the same material, same sections, from the other side of
> the table.

A skill map is a list of capabilities you tick. An interview is somebody deciding
whether the tick is true. These files pair one to one: every section here has the
same name as a section there, so a question always leads back to the capability it
tests, and a capability always leads forward to how it gets probed.

## The maps

| File | Pairs with | Sections |
| --- | --- | --- |
| [`networking.md`](networking.md) | [`skills-maps/networking.md`](../skills-maps/networking.md) | 11 |
| [`identity.md`](identity.md) | [`skills-maps/identity.md`](../skills-maps/identity.md) | 10 |

## The entry format

Four parts, and **the fourth one changes shape depending on the section's marker.**

```
### "the question, as it actually gets asked"                     🔨 or 🧭
**Probes:** the judgement being tested — never the fact being recalled.
**Answer:** a work example (🔨) or the honest-ramp framing (🧭).
**Prove it:** a runnable lab or tool, where one exists.
```

**Under `🔨` the answer is a work example** — something that actually happened,
told anonymised. It is not a script to recite. It is **the evidence for the
marker**: a `🔨` with nothing behind it is an overclaim hiding one level below
where any audit reaches, which is the whole argument of
[ADR-0004](../../docs/adr/0004-interview-answers-are-evidence-for-a-marker.md).

**Under `🧭` the answer is the honest ramp** — what is mapped and verified, what
transfers, and where the boundary sits. There is no model answer to give here and
none is wanted. [`honesty-audit`](../../.claude/skills/honesty-audit/SKILL.md)
argues that a ramp stated plainly reads as judgement rather than as a gap, and
that framing is the answer. Saying *"I have not run this in production, here is
what I did verify and here is what transfers"* is a stronger response than a
fluent bluff, and it is the only one that survives the second question.

## Anonymisation is not optional here

A question plus what it probes is generic. **An answer is specific, and
specificity locates an employer.** Every work example on these pages follows the
discipline in ADR-0004:

- **Scale and shape, never place or party.** A regional vCenter estate, a hundred
  thousand nodes, a five-year ITSM tenure — these survive. Region names, company
  names and alignable dates do not.
- **No reconstructible timelines.** An incident is a sequence of decisions, not a
  date with a duration.
- **The test is compositional.** Any single detail can be harmless while the set
  is identifying. Ask not *"is this sensitive"* but *"does this narrow the field,
  given everything else already on the page."*

## What this is not

**Not a question bank to memorise.** A memorised answer fails on the follow-up,
which is the question that actually decides the interview. What is written here is
the *material* — the example and the framing — and recalling it under pressure is a
separate skill. [`interview-drill`](../../.claude/skills/interview-drill/SKILL.md)
is the loop for that: it asks, follows up, and checks whether the answer stayed on
the evidence or drifted into the fluent version.

**Not a substitute for the chapters.** Like a [build-out](../../build-out/) step,
an entry here that starts explaining how something works has failed — that
explanation already exists, and a second copy is a second thing to keep true.
