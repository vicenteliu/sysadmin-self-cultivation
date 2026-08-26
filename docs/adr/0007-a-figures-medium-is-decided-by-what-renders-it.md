---
kind: adr
axis: meta
themes: []
platforms: []
summary: "The repo had 67 mermaid diagrams and one way of making them. Adding branded hero figures introduced a second way, and two ways of doing one thing is how a convention rots — so the boundary between them is written down here rather than left to taste."
---
# A figure's medium is decided by what renders it

The repo had 67 mermaid diagrams and one way of making them. Adding branded hero
figures introduced a second way, and two ways of doing one thing is how a convention
rots — so the boundary between them is written down here rather than left to taste.

## Decision

**If GitHub can render it, it is mermaid.** A fenced `mermaid` block renders on
GitHub, renders in the viewer, and diffs as text — the source and the picture are the
same object, so they cannot disagree.

**A hero diagram is the exception, and it is bounded.** Four exist: the axis map, the
stack, the ramp, and the route. Each opens an axis. Each is authored once as a light
HTML file and everything else is derived by
[`site/build-diagrams.py`](../../site/build-diagrams.py) — the dark HTML, and both
SVGs. Markdown embeds the SVGs through `<picture>`, so GitHub and the viewer each get
the variant that matches the reader's theme.

And above both, the rule that decides whether to draw at all: **a figure must carry
what the prose does not** — an order, a dependency, a boundary, a proportion, a
convergence. A figure that restates a paragraph or a table is a defect. A pass over
seventeen folder indexes produced two new mermaid diagrams and four hero embeds, and
the eleven files left alone were left alone on purpose.

## Considered options

- **Everything in mermaid.** The tidiest answer, and the one that keeps a single
  medium. Rejected for a narrow case: a figure that opens an axis is doing editorial
  work — hierarchy, an accent, a deliberate one focal element — and mermaid's automatic
  layout will not hold those decisions. Twice, while laying out the skills figure, dagre
  moved a lane and inverted a rank and made the caption a lie.

- **Everything from `diagram-design`.** Rejected outright. Sixty-seven diagrams become
  an HTML source and two SVGs for every one of the hundred-odd fenced blocks; a
  one-word label fix becomes a build; and GitHub loses the plain-text diff that makes a
  diagram reviewable in a pull request.

- **Hero HTML only, linked rather than embedded.** Simpler — no export step, no second
  artifact to keep in step. Rejected because GitHub will not render an HTML file, so
  every reader on GitHub would get a link instead of a picture, in exactly the four
  places where the picture is the point.

- **Hand-write the dark variant beside the light one.** Rejected on the same ground
  ADR-0001 rejected a second copy of the build-out: four hundred lines of coordinates
  duplicated for ten hex values, drifting from the first edit that lands on one side.
  It is derived instead, and `--check` says when the derivation is behind.

## Consequences

- **Four sources, twelve derived files.** Never hand-edit a derived one; the next run
  overwrites it. `python3 site/build-diagrams.py --check` is the guard, and
  [`diagram-module`](../../.claude/skills/diagram-module/SKILL.md) is the skill that
  owns running it.
- **The skin is committed, and checked against the deriver.** `diagram-design` resolves
  style profiles out of the user's home directory, so a clone would carry the
  `.diagram-design` marker but not the skin it names — the repo therefore holds the
  profile itself at `site/assets/diagrams/sysadmin-brass.profile.md`, and
  `--install-profile` puts it where the plugin looks. This closed a hole the first
  version of this ADR recorded as unclosable: `--check` now runs every semantic role's
  light value through the same substitution the documents get and demands the profile's
  dark value back. It found two real skews the moment it existed — the accent tint was
  deriving at the wrong opacity in three live artifacts, and `rule-solid` was deriving
  an opaque approximation of a translucent hairline.
- **A fifth hero needs an argument, not an occasion.** The bound is what keeps the
  exception from becoming the rule.
- **Mermaid's layout is a constraint on content.** Keep subgraph titles under about 28
  characters, avoid back-edges in a `TB` flow, and do not put a disconnected component
  beside a connected one. The traps and their symptoms are recorded in
  [`diagram-module`](../../.claude/skills/diagram-module/SKILL.md) so the next author
  does not rediscover them.
