---
name: author-module
description: Author a new module for The Sysadmin's Self-Cultivation repo (a platform doc, a cross-cutting note, an architecture/operations/automation companion, or a lab) that matches the established conventions — blockquote thesis, section skeleton, ✋/🧗 honesty markers, validated mermaid, cadence tables, cross-links. Use when adding/writing a new chapter, note, platform module, or companion doc to this repo, or when the user says "write a note on X", "add a module for X", "keep it consistent with the repo".
created: 2026-07-02
owner: Vicente Liu
---

# Skill: author-module

Write a new piece of this repo so it reads like the rest of it. The repo has ~50
files with a very consistent voice and structure; this skill encodes that so
additions stay coherent and honest.

## First: read the exemplars

Before writing, read the closest existing module and mirror it:
- **Platform module** → [`platforms/aws/README.md`](../../platforms/aws/README.md) +
  its `skills-map.md` / `ai-ramp.md` / `architecture.md` / `operations.md` /
  `automation.md`.
- **Cross-cutting note** → [`cross-cutting/identity-iam.md`](../../cross-cutting/identity-iam.md)
  or [`cross-cutting/databases.md`](../../cross-cutting/databases.md).
- **The-stack layer** → [`the-stack/01-physical.md`](../../the-stack/01-physical.md).
- Always re-read [`WHY.md`](../../WHY.md) for the honesty discipline.

## The house style (non-negotiable)

- **Open with a `> blockquote` thesis** — 1-3 confident, concrete sentences that say
  what this is and why it matters. Teacherly, a little wry. Complete sentences (no
  arrow-chains or fragments).
- **Voice:** explain the *concept* first (platform-agnostic), then rename per tool —
  the operating-model instinct. Say the technical terms in full.
- **Cross-link liberally** with relative paths — to `the-stack/0X`, other
  `cross-cutting/*`, `platforms/*`, `00-the-operating-model.md`, `WHY.md`, and
  sibling docs. Links are how the repo hangs together.

## The section skeleton

Adapt to the module type, but a cross-cutting note or platform companion is roughly:

1. Thesis blockquote.
2. **The one idea / one model** — the mental model, often with a mermaid diagram.
3. **The renames / seven-way teardown** — concept mapped per tool/platform.
4. A **comparison or cadence table** — the core artifact (platform ops docs get a
   `continuous/daily/weekly/monthly/quarterly/on-incident` cadence table).
5. **Choosing** — the real selection factors.
6. **Ops notes — what pages you** — the failure modes.
7. **The admin discipline** — checkable "what to be able to do".
8. **The AI-assisted ramp** — how AI helps + where it burns you (verify hardest).
9. **Honest boundaries** — ✋/🧗, always last-but-one.
10. **Lab** — a spec, or a link to a runnable one (prefer runnable).
11. **The [module] on one screen** — a closing `mindmap`.

## Honesty markers (apply the honesty-audit discipline inline)

Mark the topic **✋ hands-on depth** only where the author has real experience;
everything else is a **🧗 verified ramp**, mapped and doc-checked, never "years of
production". Transferable instincts are ✋ even on a 🧗 platform. The `## Honest
boundaries` section states this plainly.

## Mermaid rules (they MUST validate)

- Node labels with special chars go in `["..."]` quotes; avoid parens/commas/colons in
  unquoted labels; `<br/>` for line breaks inside quoted labels.
- Mindmap node text = plain words only (no parens or punctuation).
- **Validate every diagram before finishing:** extract each ```mermaid block to a
  scratch file and run `npx --yes @mermaid-js/mermaid-cli -i f.mmd -o f.svg` in the
  scratchpad; fix any that fail.

## Wire-in (don't leave it dangling)

After writing, update the indexes: [`CONTENTS.md`](../../CONTENTS.md), the relevant
folder `README.md` (`cross-cutting/README.md` or `platforms/README.md`),
[`ROADMAP.md`](../../ROADMAP.md), and the root [`README.md`](../../README.md) status if
it's a headline addition. Then it's discoverable, not orphaned.

## Guardrails

- Match length to the neighbors (~120-165 lines for a chapter); don't pad.
- Surgical edits to indexes — one row per new module, consistent wording.
- Commit with the repo's message style (`<area>: <what> — <why>`), and validate
  mermaid before committing.
