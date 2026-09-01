---
kind: skill-map
axis: cross-cutting
themes: [identity]
platforms: [aws]
marker: "mixed"
summary: "Every platform folder carries a skill map: one platform, cut across every theme."
---
# cross-cutting/skills-maps/

> 🌐 **Languages:** English (default) · [中文](../../docs/zh/cross-cutting/skills-maps/README.md)

> Every platform folder carries a [skill map](../../platforms/aws/skills-map.md):
> **one platform, cut across every theme.** This folder is the transpose —
> **one theme, cut across every platform.** Same checkbox format, same question
> ("can you *do* it?"), rotated ninety degrees.

The rotation is the point. A platform map answers *"what do I still not know about
AWS?"* A theme map answers a question the platform maps structurally cannot:
**"how much of what I know about networking travels, and how much of it was
really just AWS?"**

## The maps

| Map | Covers | Markers |
| --- | --- | --- |
| [`networking.md`](networking.md) | Addressing, routing, L2/overlay, DNS, DHCP, filtering rules, load balancing, TLS, remote access, flow analysis, inter-cloud | 🔨 ×9 · 🧭 ×2 |
| [`identity.md`](identity.md) | Directory, AuthN/AuthZ, federation & SSO, running an IdP, SCIM/JML, RBAC, conditional access, privileged access, access review, workload identity | 🔨 ×8 · 🧭 ×2 |

More themes follow the same demand order as [`../../ROADMAP.md`](../../ROADMAP.md).
These two came first because they are the two densest clusters in the demand
signal, and because between them they carry most of what the other themes assume.

## The tiers mean something different here

A platform map anchors its tiers **inside** the platform — *"Core: you cannot
administer AWS without this."* A theme map has no such anchor, so it uses a
different one: **how far the skill travels.**

| Tier | Anchor |
| --- | --- |
| **Core** | True on all seven platforms. The concept survives every rename; only the noun changes. |
| **Working** | True on most. Real differences exist and you have to know which platform you're on. |
| **Depth** | Platform-specific, or where the platforms genuinely disagree. This is where the transferable model stops and the reading starts. |

Read a filled-in map top-to-bottom and it tells you two things at once: what to
learn next, and **how much of it you get to keep** when the platform changes.
Unchecked Core boxes are the expensive ones — a gap there is a gap everywhere.

Check a box when you can *do* it and *explain the failure modes* — not when
you've read about it. Same rule as the platform maps.

## Markers sit on sections, not on the folder

Platform maps carry **no** 🔨/🧭 markers inside them; the honesty marker lives on
the platform as a whole. That works there and fails here, because a theme map
almost always mixes: network *design* is 🔨 in the same file where network
*monitoring* is 🧭. A single marker on the file would have to read "mixed", which
is the vagueness [`WHY.md`](../../WHY.md) exists to refuse.

So in this folder the marker sits on the **section** — the finest grain at which
the claim is still true, and no finer. Individual checkboxes stay unmarked: a
hundred glyphs down a page stops being a signal and starts being wallpaper.

**The platform maps are unchanged.** The precedent is broken only on this axis.

## Where a skill lives when two themes want it

**A skill belongs to the theme of what it acts on, not the theme of how it acts.**

Network monitoring is the case that forces the rule. It is monitoring, so an
observability map will eventually want it; it is also unreadable without knowing
what a route table and a five-tuple are. Filed under observability it would be
diluted to "networks need monitoring too" inside a three-pillars frame. So it is
filed here, permanently — and a future `observability.md` covers the host and
application layers and links across rather than absorbing it.

The same rule sends certificate lifecycle here (it acts on the transport) rather
than to a future security map, and sends conditional access to
[`identity.md`](identity.md) (it acts on a sign-in) rather than to endpoint.

## Not a seventh axis

[ADR-0001](../../docs/adr/0001-the-build-out-is-a-route-not-a-seventh-axis.md)
settled the pattern when `build-out/` raised it: the repo's axes are *faces of the
material*, and something that teaches no new page is not a new face. These maps
teach no new page. Every box points into an axis for the substance, exactly as a
build-out step does — which is why they live inside `cross-cutting/` and not
beside it.

The consequence is the same one ADR-0001 named: **a box that needs a paragraph to
explain it is a box in the wrong place.** Move the explanation to the axis and
link to it.

## Prove it

A section ends with a `**Prove it:**` line when the repo has something runnable
for it — a [lab](../labs/) or a [`toolbox/`](../../toolbox/) tool. Sections
without one end without one; that is information, not an oversight.

Unlike [`build-out/GAPS.md`](../../build-out/GAPS.md), **missing runnable evidence
here is not recorded as a gap.** That list is derived from one concrete scenario
and stays narrow on purpose; a wish-list from a different axis would quietly
change what it means.
