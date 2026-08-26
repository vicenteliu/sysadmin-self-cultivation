---
name: diagram-module
description: Draw a figure for The Sysadmin's Self-Cultivation repo and keep it in sync — decide whether a diagram is warranted at all, pick mermaid (in the Markdown, rendered by GitHub) or a diagram-design hero (HTML source, SVG artifact), author it in the repo's brass skin, validate it, and run the consistency check over the generated site data. Use when the user says "add a diagram", "draw this", "配张图", "画个图", "make a diagram for X", "the diagrams are out of date", or asks whether a doc needs a figure.
created: 2026-08-25
owner: Vicente Liu
---

# Skill: diagram-module

Figures for this repo, and the discipline that keeps them honest. This skill does not
write documents — that is [`author-module`](../author-module/SKILL.md). It decides
whether a figure is warranted, which medium it belongs in, and it owns the derived
artifacts once one exists.

## First: read the exemplars

- A hero, and its derived pair → [`site/assets/diagrams/stack-layers.html`](../../../site/assets/diagrams/stack-layers.html)
  (the only file to edit) and the files `site/build-diagrams.py` derives from it.
- Two in-document mermaid figures that earn their place →
  [`.claude/skills/README.md`](../README.md) (which skill hands off to which) and
  [`cross-cutting/README.md`](../../../cross-cutting/README.md) (where the support notes
  converge).
- The prose those figures sit next to — read one before drawing.

## Rule 1 — the figure must carry what the prose does not

**A diagram that restates a paragraph or a table is a defect, not a bonus.** It costs a
reader's attention, it costs a maintainer's diff, and it says nothing. A figure earns
its place only by carrying something the words around it do not: an **order**, a
**dependency**, a **boundary**, a **proportion**, or a **convergence**.

Apply it out loud before drawing. The honest answer is often no:

| Situation | Verdict |
| --- | --- |
| The doc already has the seven surfaces as a table | ✗ — the figure would be the table |
| Sixteen steps, and how long each phase really is | ✓ — proportion is not in the list |
| Four support notes, one of which synthesises the others | ✓ — convergence is not in the table |
| Three boxes in a line | ✗ — that is a sentence; write the sentence |
| A folder index listing what is in the folder | ✗ — that is what the index is |

This rule outranks any instruction to "add diagrams". If a pass over ten files finds
that two of them warrant a figure, the answer is two figures and a note saying why the
other eight did not.

## Rule 2 — the medium follows what renders it

**If GitHub can render it, it must be mermaid.** GitHub renders a fenced `mermaid`
block natively, the source stays diffable, and the repo is already full of them.

Reach for a **hero diagram** — `diagram-design` output, HTML source, SVG artifact —
when **the layout itself carries meaning**: a focal element, a deliberate hierarchy, a
spatial relationship an automatic layout engine would destroy. Reach for mermaid when
only the topology matters, which is most of the time.

That test replaces a count. This skill used to say "there are four; a fifth needs an
argument" — and three more were added without that argument ever being made, because a
number cannot announce that it has been crossed
([ADR-0008](../../../docs/adr/0008-a-count-is-not-a-bound.md)). Do not write a count
here again.

| | mermaid | hero diagram |
| --- | --- | --- |
| Lives in | the Markdown, inline | `site/assets/diagrams/` |
| GitHub renders it | yes, natively | yes, via the exported SVG |
| Diffable | yes — it is text | the HTML source is; the SVG is generated |
| Themed | at runtime, by the viewer | two exported variants, light and dark |
| Cost to change | edit the fence | edit the source, re-run the deriver |

## Before you draw: read what it will sit next to

Two failures here were not about drawing at all. Both are cheap to prevent and invisible
to every `--check` in this repo.

**Read the prose the figure will sit in, and check the figure against it.** A site-network
figure was drawn with a `/16` site range and was about to be placed above a table that had
always specified *"one `/22` out of a documented site range"*. The figure was redrawn to
the `/22`; the note was not edited. A figure that argues with the paragraph beside it is
worse than no figure, because the reader believes the picture.

**Read the figures already near it, and check for a claim you cannot show.** A 500-VM
figure carried the label *"a second failure domain"* on an iSCSI path — true only if each
`vmk` is pinned to one uplink, and nothing on that drawing said whether it was. The fix
was a second figure showing the binding. When two figures share facts, list the shared
facts and compare them one by one; nine were compared for that pair.

## Mermaid: the layout traps, learned the hard way

These are not style preferences. Each one produced a broken figure in this repo:

- **A back-edge inverts a `TB` flowchart.** `check -.-> ramp` closing a loop pushed the
  last rank to the top and read bottom-up. If the cycle is not the point, cut the
  back-edge and say it in prose.
- **`direction LR` inside a subgraph is ignored when the subgraph has no internal
  edges.** The nodes stack vertically anyway. Forcing it with invisible `~~~` links
  makes the layout worse, not better.
- **A disconnected subgraph beside a connected tree lays out sparsely** — dagre ranks
  them separately and leaves a hole. Two components means two figures, or one figure
  and a sentence.
- **A subgraph title longer than about 28 characters wraps and lands on the first node
  inside it.** The site compensates (`subGraphTitleMargin` in `site/js/render.js`), but
  GitHub does not. Keep subgraph titles short.
- Quote any label with punctuation: `node["like this"]`, `<br/>` for line breaks.
  Mindmap node text is plain words only — no parens, no punctuation.

**Validate before finishing.** Extract each block to the scratchpad and run
`npx --yes @mermaid-js/mermaid-cli -i f.mmd -o f.svg`. A diagram that fails to parse is
worse than no diagram: the site renders the failure in place, and GitHub renders a
blank.

## Hero diagrams: author once, derive the rest

The skin is pinned by [`.diagram-design`](../../../.diagram-design) at the repo root
(`profile: sysadmin-brass` — bone paper, iron ink, brass accent, with system font
fallbacks because an exported SVG loads no webfont). Do not re-run the style gate.

1. Author **one** file: `site/assets/diagrams/<slug>.html`, light skin, from the
   `diagram-design` template. That file is the source; nothing else is.
2. Run `python3 site/build-diagrams.py`. It derives `<slug>.dark.html`,
   `<slug>.light.svg` and `<slug>.dark.svg`, re-prefixing the `<title>`/`<desc>` ids for
   the dark variant. **Never hand-edit a derived file** — the next run overwrites it.
3. Embed it so both GitHub and the site pick the right variant:

   ```html
   <picture>
     <source media="(prefers-color-scheme: dark)" srcset="../site/assets/diagrams/<slug>.dark.svg">
     <img alt="<a real description, not the title>" src="../site/assets/diagrams/<slug>.light.svg">
   </picture>
   ```

4. Caption it. A hero without a line saying what to take from it is decoration.

The skin is committed at `site/assets/diagrams/sysadmin-brass.profile.md` because
`diagram-design` resolves profiles from `~/.diagram-design/profiles/`, which a clone does
not carry. On a machine that has never built a diagram here:

```bash
python3 site/build-diagrams.py --install-profile
```

If the skin changes, change the token table in `site/build-diagrams.py` to match — and
you will be told if you forget, because `--check` derives every role's light value and
demands the profile's dark value back.

## The consistency check (run it before you finish)

```bash
python3 site/build-diagrams.py --check    # every artifact matches its source · the token
                                          # table matches the style profile · every number
                                          # drawn matches the index · every label fits its box
python3 docs/build-index.py --check       # front-matter still matches the retrieval index
python3 site/build-corpus.py --check      # titles and search corpus still match the prose
```

Deliberately no counts above. A count in a document is a fact that goes stale silently,
which this file has now demonstrated twice — once claiming the repo had 67 mermaid
diagrams when 67 was a count of *files*, and once claiming four artifacts from four
sources long after there were more of both.

**What no check covers**: whether the figure agrees with the prose beside it, whether it
agrees with the figure above it, and whether it should exist at all. Those are the two
sections at the top of this skill, and they are read by a person or not at all.

Non-zero from any of them means a generated file is behind its source. Re-run the
script without `--check`, then commit source and artifact together. Two of these are
not this skill's to own, but a figure changes a document, and a changed document
staling the corpus is the failure this check exists to catch.

## Wire-in

A new hero is referenced from the axis index it opens, and it may also belong on the
site's home page ([`site/js/render.js`](../../../site/js/render.js), `renderHome`). A new
mermaid needs nothing but its fence. Either way, re-run the two builders above so the
site ships a corpus that matches what a reader now sees.

## Guardrails

- **Never draw to fill a quota.** Rule 1 is the whole skill; the rest is mechanics.
- Accent is editorial, not a signalling system: one or two focal elements per hero,
  never five.
- A hero diagram is a *view* of the material, not a new page of it — the site is too
  ([ADR-0005](../../../docs/adr/0005-the-site-is-a-view-not-a-seventh-axis.md)). If a
  figure is teaching something the repo does not say anywhere in prose, the missing
  thing is prose, and the job belongs to [`author-module`](../author-module/SKILL.md).
- Commit with the repo's message style (`<area>: <what> — <why>`), and never commit a
  source without its derived artifacts.
