# The reference office is parameters, and the model names are quarantined

Every build-out step says *a hundred people* without ever saying how big the place is, so
a decision-teaching repo had nothing concrete to decide against. `the-reference-office.md`
fixes that at the root level, next to `00-the-operating-model.md`, because it is a premise
of the whole repo rather than the product of any one step.

It carries model names and cost shape, which this repo has never done before. That is the
part worth explaining.

## What was actually decided

**Sections are separated by shelf life, not by topic.** Derivations, criteria, model
names and cost age at wildly different speeds. Mixed together, the fastest-rotting part
takes the rest down with it. Kept apart, the dated table can be replaced whole in two
years without touching a line of the prose that explains why the numbers are what they
are.

**Model names are allowed, in one quarantined table, dated.** They earn their place
because the repo is a tutorial and worked examples teach; they are quarantined because
they are the only part of this material with a two-year half-life, and the only part that
can make a teaching repo read like a buying guide.

**The reference build has a mechanical entry test — could someone buy from this?** Model,
port count, access point count all pass. How a protocol behaves does not. Without that
test the file drifts downward into mechanism over time, one reasonable-looking sentence at
a time, and the repo quietly stops being what it says it is.

**It grows when the scenario needs a parameter, never when a video needs one.** The test
is whether the scenario would still want the line if nothing were ever filmed. Content
that exists to serve a recording belongs with the recording.

**Interview material is questions plus what each one probes, never finished answers.**

> ⚠️ **Superseded by [ADR-0004](0004-interview-answers-are-evidence-for-a-marker.md).**
> Only this fifth decision; the other four on this page stand. Answers are now written,
> with their shape set by the section's honesty marker and their detail bounded by an
> anonymisation discipline. The reasoning that replaced this one is that the rule was
> written for a stranger reading the repo, and silent about the author, who has 591
> markers to defend.

## Two things deliberately not done

**The building-side boundary in `build-out/GAPS.md` stands, untouched.** It reads that
commissioning a room from a shell is physical work with contractors, and that the
building-side stays a stretch. That boundary is about *doing the work*. This file is about
*the parameters of the scenario*, which is a different thing, so the reference office
lives at the root and not inside step 02. **Nothing was superseded, and nothing needed to
be.**

**Nothing already in the repo was rewritten into it.** Failure modes already live in the
`Getting it backwards` section of all sixteen steps, runnable tooling already lives in
`toolbox/`, and working with AI already lives in `ai-workflow/`. The reference office
points at all three and duplicates none of them. Two parallel copies of the same material
drift, and the drift is silent.

## The version one that was deliberately thin

Only parameters and derivations are written. Selection rules, the reference build, cost
shape and interview material are stubs with entry conditions on them.

Equipment selection depends on the parameters and not the other way round — you cannot
size access points before you know the floor. Writing the network gear first because a
network episode happened to be in production would have been exactly the coupling the
growth rule above exists to prevent.
