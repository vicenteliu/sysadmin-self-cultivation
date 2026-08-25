# The Sysadmin's Self-Cultivation

A glossary for this repo — the words that mean something specific here, and the
words they get confused with. Nothing else belongs in this file: status lives in
[`ROADMAP.md`](ROADMAP.md), structure in [`CONTENTS.md`](CONTENTS.md), decisions
in [`docs/adr/`](docs/adr/).

## Language

### The three things called "skills"

The word is overloaded three ways here, and conflating them has already cost one
round of rework. They are unrelated.

**Skill map**:
A checkable competency list — `- [ ]` boxes tiered **Core / Working / Depth**,
where checking a box means you can *do* the thing and *explain its failure
modes*. Two orientations exist: [`platforms/*/skills-map.md`](platforms/aws/skills-map.md)
(one platform across every theme) and [`cross-cutting/skills-maps/*.md`](cross-cutting/skills-maps/README.md)
(one theme across every platform).
_Avoid_: skill list, competency matrix, checklist

**Agent Skill**:
A `SKILL.md` workflow in [`.claude/skills/`](.claude/skills/) that an AI agent
invokes to *apply* this repo's method. Eight exist. A unit of automation, never a
unit of knowledge.
_Avoid_: skill (unqualified), tool, command

**Demand cluster**:
One row of the job-market frequency table in [`ROADMAP.md`](ROADMAP.md) — how
often a group of technologies appears in real postings. It sets build order and
nothing else.
_Avoid_: skill area, topic, category

### The honesty markers

**🔨 (hands-on depth)**:
A claim that the author has operated this for real, in production, with
consequences. Survives a deep follow-up question.
_Avoid_: expert, proficient, strong, ✋ and ⚒️ (both retired — see [ADR-0003](docs/adr/0003-the-honesty-markers-are-a-hammer-and-a-compass.md), including why the second one lasted a day)

**🧭 (verified ramp)**:
A claim that the material is mapped, doc-checked and often lab-verified, but not
run in production. Honest about the gap rather than hiding it.
_Avoid_: familiar with, exposure, working knowledge, 🧗 (retired — see ADR-0003)

**Overclaim (❌)**:
Any 🔨 verb attached to 🧭 experience. The failure mode the markers exist to
prevent; [`honesty-audit`](.claude/skills/honesty-audit/SKILL.md) is what detects it.

### Interview material

**Interview question**:
A question an interviewer actually asks, paired with **what it probes** — the
judgement being tested, not the fact being recalled. Lives in
[`cross-cutting/interview/`](cross-cutting/interview/README.md), grouped by the same
sections as the matching [skill map](cross-cutting/skills-maps/README.md). A skill-map
box says *what you can do*; an interview question says *how they check*.
_Avoid_: quiz question, flashcard, prep question

**Answer**:
What follows a question, and **its shape is decided by the section's marker** — a
🔨 section answers with a [work example](#), a 🧭 section answers with the honest-ramp
framing. It is evidence for the marker, never a script to recite. Note the reversal:
[ADR-0002](docs/adr/0002-the-reference-office-is-parameters-not-a-bill-of-materials.md)
used *finished answer* for the thing not to write;
[ADR-0004](docs/adr/0004-interview-answers-are-evidence-for-a-marker.md) reversed it.
_Avoid_: model answer, sample answer, script, canned response

**Work example**:
Something that actually happened at work, told anonymised — scale and shape, never
place or party, and no reconstructible timeline. It attaches to a 🔨 section and is
what makes that marker checkable rather than asserted. **Not a lab** (synthetic
and runnable — see below), and **not the reference office** (a fiction the repo reasons against).
_Avoid_: war story, anecdote, case study, experience

### Retrieval

**Retrieval index**:
The generated `docs/index.json` — one machine-readable record per file, built from
front-matter by `docs/build-index.py`, for an agent to search without opening
anything. **"Index" is three things here and only this one is the retrieval index:**
[`CONTENTS.md`](CONTENTS.md) is the human table of contents, a directory `README.md`
is a local index for its folder, and this is neither.
_Avoid_: catalog (that is `toolbox/generate/catalog.json`, hand-maintained and
unrelated), manifest, search index

### Tiers, in a skill map

**Core / Working / Depth**:
Tiers with **two different anchors depending on the map's orientation.** In a
platform map they anchor *inside* the platform ("Core: you cannot administer AWS
without this"). In a theme map they anchor on **how far the skill travels** —
Core is true on all seven platforms, Working on most, Depth is where the
platforms genuinely disagree.
_Avoid_: beginner/intermediate/advanced, junior/senior

### Terms that collide elsewhere

**IdP**:
**Identity Provider** — Entra ID, Okta, Keycloak, ADFS. Always this, never
Internal Developer Platform; that concept does not appear in this repo.
_Avoid_: IDP (uppercase D), identity platform

**Anchor**:
A **ramping** verb, not a depth claim: tying an unfamiliar platform to what you
already know. Numbered Rule 2 of [`ai-workflow/`](ai-workflow/how-i-use-ai-to-learn-and-operate.md).
It belongs to 🧭, which is why ⚓ was rejected as a depth marker.
_Avoid_: using "anchor" to mean established expertise

**Gap**:
Something [`build-out/GAPS.md`](build-out/GAPS.md) records: a step in the
100-person-office scenario that *should* point at a runnable lab or a
[`toolbox/`](toolbox/) tool and cannot. **Derived from that scenario only.**
Missing material anywhere else in the repo is not a gap and does not go in that
file.
_Avoid_: todo, backlog item, missing piece

**Lab**:
A pure-local, zero-dependency, self-verifying drill where exit code `0` means the
lessons held. Most carry a `--break-it` flag that swaps in the *standard*
procedure and shows it failing.
_Avoid_: tutorial, exercise, demo

**Axis**:
One of the repo's six faces over one body of material — by platform, by layer, by
theme, and so on. Something that teaches no new page is **not** an axis, however
useful ([ADR-0001](docs/adr/0001-the-build-out-is-a-route-not-a-seventh-axis.md)).
`build-out/` is a route across the axes; `cross-cutting/skills-maps/` is a
transposed view of them.
_Avoid_: section, category, track
