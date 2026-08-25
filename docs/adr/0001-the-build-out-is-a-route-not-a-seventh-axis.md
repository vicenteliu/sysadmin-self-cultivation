---
kind: adr
axis: meta
themes: []
platforms: []
summary: "This repo has six axes over one body of material, and the README says what they are for: \"enter from whichever matches your question.\" That works when you already know what to ask."
---
# The build-out is a route through the axes, not a seventh axis

This repo has six axes over one body of material, and the README says what they
are for: *"enter from whichever matches your question."* That works when you
already know what to ask. It fails the reader who does not — who has to stand up
IT for a new office and does not yet know that identity has to be settled before
the first laptop is enrolled.

`build-out/` answers that reader by walking one scenario end to end: a 100-person
office, single site plus a small branch, forced-hybrid (a few things must stay
local), with a customer-driven SOC 2 obligation.

## Decision

**The build-out carries sequence and dependency. It does not carry content.**

Each step names what it produces, what must be true before it starts, what
depends on it, and then **points into the existing axes** for the substance. A
step that finds itself explaining how SCIM works has failed — that explanation
already exists, and a second copy of it is a second thing to keep true.

## Considered options

- **A seventh axis.** Rejected. The six are *faces of the material* — by platform,
  by layer, by theme. A build-out is not another face; it is a **path across all
  six**. Filing it as a peer would tell the reader there is a seventh body of
  material to read, when in fact it teaches no new page.

- **A standalone tutorial, written out in full.** Rejected, and this is the one
  that would actually have been tempting: it reads better in isolation. But it
  duplicates roughly everything already written, and two hand-maintained copies
  of the same knowledge diverge from the first edit that lands on one side only.
  The failure is silent — the newer copy looks just as authoritative as the older.

## Consequences

- **A step is short by construction.** If a step is long, it is explaining
  something that belongs in an axis; move it and link.
- **Coverage becomes measurable.** Every step should be able to point at a
  runnable lab or a `toolbox/` tool. The steps that cannot are recorded in
  `build-out/GAPS.md` — and that list is a better roadmap than a roadmap, because
  it is derived from a real scenario rather than from a sense of what is missing.
  A gap is only a gap when the step *should* have a tool and the repo lacks one;
  material a 100-person office never touches is not a hole.
- **The honesty markers get harder to fudge here than anywhere else.** A
  greenfield narrative invites writing the parts you have not done in the same
  confident voice as the parts you have. Steps 0–2 (lease, uplink, riser and IDF)
  are largely outside hands-on experience and are written as *questions to ask
  before signing*, not as how to negotiate — a question list can be derived from
  first principles; negotiating cannot.
