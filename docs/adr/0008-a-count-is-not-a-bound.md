---
kind: adr
axis: meta
themes: []
platforms: []
summary: "ADR-0007 bounded hero diagrams at four and said a fifth would need an argument. Three more were added without that argument ever being made, and nobody noticed — because a bound written as a count cannot tell you it has been crossed."
---
# A count is not a bound

[ADR-0007](0007-a-figures-medium-is-decided-by-what-renders-it.md) decided that
mermaid is the default and a branded hero diagram is the bounded exception. That
decision stands. Two of its sentences do not:

> **A hero diagram is the exception, and it is bounded.** Four exist…
>
> **A fifth hero needs an argument, not an occasion.** The bound is what keeps the
> exception from becoming the rule.

There are seven. `site-network`, `vsphere-500vm` and `esxi-host-network` were added in
three separate commits, and **the argument the fifth was supposed to need was never made
for any of them.** Each was reasoned about carefully against the rule above it — does
this figure carry what the prose does not — and not once against the bound, which was
sitting in a decision record the whole time.

Nothing caught it. `build-diagrams.py --check` counts sources and artifacts and would
happily report seven of one and twenty-one of the other, because a script cannot know
that seven is more than a sentence in an ADR said it should be.

## Decision

**The bound is a criterion, not a count.** Reach for a hero diagram when **the layout
itself carries meaning** — a focal element, a deliberate hierarchy, a spatial
relationship that an automatic layout engine would destroy. Reach for mermaid when only
the topology matters, which is most of the time.

That test admits all seven and explains why, which the count never did:

| Figure | What the layout carries |
| --- | --- |
| `repo-map` | Containment — six views *inside* one body, the route spanning the same width |
| `stack-layers` | Order, and one focal layer among seven equals |
| `seven-surfaces` | A tall middle column flanked by the method that uses it |
| `build-out-route` | Proportion — phases spaced by how many steps each holds |
| `site-network` | A boundary — which segment the firewall is the gateway for |
| `vsphere-500vm` | Four tiers, each a different kind of thing |
| `esxi-host-network` | A binding — one `vmk` pinned to one uplink, which a list cannot show |

It also still refuses things. A folder index, a three-node chain, a table redrawn as
boxes: none of those have a layout that means anything, and mermaid or prose takes them.

## Considered options

- **Keep the count and raise it to seven.** Rejected for the reason this ADR exists: the
  number would be wrong again at the next figure, and the check that cannot see a count
  in an ADR still cannot see it. A bound nobody can enforce is decoration.

- **Keep the count and remove the three figures.** Rejected on the evidence. Each was
  argued for individually and each argument holds; it is the bound that was wrong, not
  the drawings. Deleting good work to preserve a sentence is the wrong repair.

- **Enforce the count in `--check`.** Rejected as the wrong shape of enforcement — it
  would fail on the day someone adds a figure that deserves to exist, which is a check
  that trains people to bypass it. The same reasoning removed four over-eager rules from
  the summary gate in `docs/build-index.py`.

## Consequences

- **This class of failure has no automated guard, and this ADR does not invent one.** A
  rule that lives only in prose is enforced only by someone re-reading the prose. What
  *is* now guarded is narrower and mechanical: `build-diagrams.py --check` grew a text
  overflow check, because four figures shipped with text outside its box before anyone
  looked closely.
- **A figure must be checked against the prose it will sit in, and against the figures
  near it.** Both failures happened here: one figure drew a `/16` while the table it was
  about to sit above had always specified a `/22`, and another asserted "a second failure
  domain" that nothing on it demonstrated. Neither is visible to any `--check` in this
  repo, and both are now written into
  [`diagram-module`](../../.claude/skills/diagram-module/SKILL.md) as steps rather than
  as hopes.
- **The honest record is that a decision record was violated three times before anyone
  read it back.** Writing the rule down was not enough. That is worth knowing about every
  other rule in `docs/adr/` too.
