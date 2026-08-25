---
kind: adr
axis: meta
themes: []
platforms: []
summary: "ADR-0002 made five decisions about the-reference-office.md."
---
# Interview answers are evidence for a marker, not a script to recite

[ADR-0002](0002-the-reference-office-is-parameters-not-a-bill-of-materials.md) made
five decisions about `the-reference-office.md`. Four of them stand. The fifth said:

> **Interview material is questions plus what each one probes, never finished answers.**

`the-reference-office.md` still carries the ⏳ stub that restates it, with the
reasoning attached: *public material teaches you how to think; a finished answer does
the work for you, and the two do not belong in the same file.*

That reasoning is sound about one reader and silent about the other.

## Decision

**Interview material carries the answer, and the answer's shape is decided by the
honesty marker on its section.** `🔨` sections carry a real, anonymised example from
work actually done. `🧭` sections carry the honest-ramp framing — what transfers, and
where the gap is. ADR-0002's other four decisions are untouched.

The argument that reverses the fifth is that this repo has always had two readers, and
the rule was written for only one of them.

For a stranger, ADR-0002 is right: hand them a polished response and you have replaced
the thinking you were trying to teach. But **591 honesty markers make a claim that
somebody has to be able to defend**, and the repo's own `honesty-audit` skill states
the test in as many words — *"if an interviewer said 'walk me through a time you did
this, in detail,' would it hold?"* A `🔨` with nothing behind it is not a modest
claim. It is the overclaim this repo was built to make impossible, hidden one level
down where no audit reaches.

So an answer under a `🔨` is not a script. **It is the evidence for the marker**, and
writing it is how the marker gets checked rather than asserted.

Under a `🧭` the objection never applied at all. There is no model answer to give,
because the honest response *is* the content: this is mapped and verified, not run;
here is what transfers; here is the boundary. `honesty-audit` already argues that a
ramp stated plainly is a selling point rather than a weakness. Writing that down is
teaching, which is the thing ADR-0002 was protecting.

## The exchange

Reversing the rule buys a risk that the old rule was incidentally holding off, and
the reversal is only honest if the risk is paid for rather than ignored.

**A question plus what it probes is generic. An answer is specific, and specificity
locates an employer.** A finished account of an incident carries scale, sequence,
tooling and timing — and those compose. The repo already sat closer to that line than
it looked: `AMS-region vCenter administrator` appeared seven times, and combined with
a dated certification and a fleet size it narrows the field considerably.

So the decision comes with a discipline, and it applies to the existing material as
much as the new:

- **Scale and shape, never place or party.** A regional vCenter estate, a hundred
  thousand nodes, a five-year ITSM tenure — all of these survive. Region names,
  company names and alignable dates do not.
- **No reconstructible timelines.** An incident is told as a sequence of decisions,
  not as a date with a duration.
- **The test is compositional.** Any single detail can be harmless and the set still
  identifying. The question to ask is never "is this detail sensitive" but "does this
  detail, added to the others already on the page, narrow the field."

`AMS` is retired to `regional vCenter administrator` in the same change. Dropping the
region costs nothing that mattered; keeping the word *regional* keeps the part that
did, which is that the estate was a whole region and not a lab cluster.

## Considered options

- **Keep ADR-0002 whole; put answers in a private, gitignored layer.** Rejected, and
  it was the recommendation until the second reader was counted. It works, but it
  severs the answer from the marker it is evidence for. The value of an example is
  that it sits under the claim it defends; in another file it becomes a document
  nobody opens, and the `🔨` above it goes back to being an assertion.

- **A separate private repository.** Rejected for the same reason, harder. The 591
  markers are the mounting points; nothing mounts across a repository boundary.

- **Rewrite ADR-0002 to remove the clause.** Rejected on
  [ADR-0003](0003-the-honesty-markers-are-a-hammer-and-a-compass.md)'s precedent,
  which kept a wrong decision in the record rather than editing over it. An ADR
  corpus whose documents were never wrong is not a record of thinking; it is a record
  of the current opinion wearing a date.

## Consequences

- **ADR-0002's fifth decision is superseded and the other four are not.** The
  reference office still separates sections by shelf life, still quarantines model
  names, still takes the could-someone-buy-from-this test, and still grows only when
  the scenario needs a parameter.
- **The `⏳` stub in `the-reference-office.md` now has a different contract.** When it
  is written it holds questions, what each probes, *and* the answer — under the same
  marker discipline as everything else.
- **`🧭` sections acquire an obligation they did not have.** Previously a ramp could
  be declared and left. Now it has to be articulable: what transfers, and where the
  boundary is. That is harder than writing a `🔨` example and more useful.
- **Anonymisation is now a repo-wide standard, not a per-file judgement call**, and it
  applies retroactively. The compositional test above is the one that matters; the
  others are shorthand for it.
