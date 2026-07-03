---
name: platform-ramp
description: Ramp onto any platform (a cloud, a hypervisor, an MDM, a service) fast and honestly, using this repo's operating model — map the seven surfaces, produce a checkable skill map, give the AI-assisted method, and label every claim ✋ hands-on vs 🧗 ramp. Use when the user says "help me ramp onto X", "get me competent on X", "map X onto what I know", "I've never touched X", or hands you a new platform to learn.
created: 2026-07-02
owner: Vicente Liu
---

# Skill: platform-ramp

Turn "I've never touched this platform" into "I can operate it at a working level,
and I know exactly where I'm bluffing" — the core method of
[The Sysadmin's Self-Cultivation](../../README.md), made invokable for any platform.

## The premise

An experienced admin plus AI can be operating a never-touched platform in days —
because the concepts transfer and AI supplies the platform-specific syntax. What AI
*can't* supply is the judgment to catch it when it's wrong. So this skill is two
disciplines held together: **AI for speed, judgment for truth**, with an honesty
ledger so you never claim depth you don't have.

Read [`00-the-operating-model.md`](../../00-the-operating-model.md) and
[`WHY.md`](../../WHY.md) once; this skill applies them.

## The three moves (every platform is these)

1. **Register a scoped identity** — least privilege, narrowest scope.
2. **Get a credential** — short-lived; no key on the box.
3. **Drive by API and codify it** — CLI/SDK for doing, IaC for repeatable.

## The workflow

### 1 — Map the seven surfaces (the translation, not a tutorial)

Prompt the model as a *translator from what the user already knows*:
> "I know [Linux / VLANs / IAM concepts / vSphere / …]. Map platform **X** onto the
> seven surfaces below — what's the same, what's renamed, and what's genuinely
> different? Just the delta."

The seven surfaces: **identity & access · compute · networking · storage & data ·
provisioning & config · observability · security & compliance.** Produce a one-line
"X's word for it" per surface (see the [AWS worked example](../../platforms/aws/README.md)
for the shape).

### 2 — Hunt the structural outliers

Most of a platform is a rename; the danger is the 2-4 places it *isn't*. Ask:
> "Where does X genuinely differ from [AWS/what I know], and where would my instinct
> give me the wrong answer?"

(E.g. GCP's global VPC, OCI's OCPU-vs-vCPU, Azure's two permission planes.) These get
the attention; the rest is lookup.

### 3 — Produce the checkable skill map

Not a feature list — a competency map in **Core / Working / Depth** tiers across the
seven surfaces, where each box means *"I can do it from code and explain the failure
modes."* Mirror [`platforms/aws/skills-map.md`](../../platforms/aws/skills-map.md).

### 4 — Generate an artifact, then verify hard

Draft the least-privilege policy, the network, the CLI command. **Then verify every
service name, parameter, and permission against current docs**, and run it in a
throwaway/free-tier with a budget alarm. AI's failure mode is confident wrongness —
assume the draft is 90% right and hunt the 10%.

### 5 — Write the honesty ledger (the non-negotiable step)

Label the user's *actual* standing on this platform:
- **✋ hands-on depth** — only where they've operated it for real; can be probed in an
  interview.
- **🧗 verified ramp** — mapped and doc-checked, not run in production; say so plainly.
- Transferable *instincts* (least privilege, failure domains, idempotence,
  incident method) are ✋ even on a new platform; the platform-*specific* surface is 🧗.

Never write "years of production X" for a 🧗 platform. The claim is always
*"a transferable model plus a fast, verifiable ramp."*

## Output

A short ramp brief: the seven-surface map, the 2-4 outliers, a Core-tier skill
checklist, one verified artifact to try, and the ✋/🧗 ledger. Offer to expand any
surface or generate a runnable lab (see the `runnable-lab` skill).

## Guardrails

- Verify hardest exactly where AI hallucinates: identity policy strings, service
  names, quotas/prices, and anything security-critical.
- The judgment is the user's; AI removes the rote lookup, not the accountability.
- If the user has real hands-on depth on the platform, say so and *invert* the ramp —
  AI drafts, their expertise verifies (see the [vSphere ai-ramp](../../platforms/vsphere/ai-ramp.md)).
