---
kind: glossary
axis: start-here
themes: []
platforms: []
summary: "A glossary for this repo — the words that mean something specific here, and the words they get confused with."
---
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
invokes to *apply* this repo's method. Ten exist. A unit of automation, never a
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
unrelated), manifest, search index (that is the **search corpus**, below)

**Search corpus**:
The generated `site/corpus.json` — the full text of every document, flattened for the
site's search box and fetched only when someone searches. Built by
`site/build-corpus.py`, which also emits `site/titles.json` because the retrieval index
records a summary but never a title. **Deliberately not called an index**: that word is
already spoken for three times over, and this is a fourth thing — the prose itself,
not a record about it.
_Avoid_: search index, full-text index, catalog

**Hero diagram**:
One of the four branded figures under `site/assets/diagrams/` that open an axis — the
axis map, the stack, the ramp, the route. Authored once as a light HTML file; the dark
HTML and both SVGs are **derived** by `site/build-diagrams.py` and never hand-edited.
Distinct from the in-document **mermaid** diagrams, which are the default:
[ADR-0007](docs/adr/0007-a-figures-medium-is-decided-by-what-renders-it.md) decides
which medium a figure belongs in, and both are subject to the rule above them — a
figure must carry what the prose does not.
_Avoid_: illustration, graphic, branded diagram, figure (that is either of the two)

### The walkthrough

**Walkthrough**:
A narrated pass through [`the-reference-office.md`](the-reference-office.md), written to
be **spoken by a text-to-speech engine and heard** — never read. One file per episode
lives in [`walkthrough/`](walkthrough/), in two languages side by side. It is a **route**,
not an axis: it teaches no page this repo does not already hold, and decides only the
**order and the register**
([ADR-0009](docs/adr/0009-the-walkthrough-ships-its-script-not-its-audio.md)). Its
sequence is its own — it is not `build-out/`'s sixteen steps with a voice on top, and the
numbers do not correspond.
_Avoid_: episode (that is the published audio, below), script, narration, tour, podcast.
Four places used *walkthrough* for a guided lab sequence before this term existed and
were reworded when it did; **the word is reserved** — a step-by-step lab is a *guided
run*, and a **lab** is the self-verifying kind.

**Beat**:
The unit a walkthrough is made of: **one paragraph, one TTS call, one audio segment, one
floor state.** Delimited by an HTML comment carrying a **stable id** —
`<!-- beat: coverage-not-capacity -->` — which GitHub, the viewer and the speech engine
all ignore, so the visible file stays nothing but the words that get spoken. The id is
never an ordinal, because inserting a paragraph must not silently shift every scene cue
after it by one. Alignment is by beat and never by timestamp
([ADR-0012](docs/adr/0012-alignment-is-by-beat-not-by-timestamp.md)).
_Avoid_: paragraph, segment, cue, chapter, timestamp

**Episode**:
**One published audio recording**, on a podcast host, outside this repo. A walkthrough is
material; an episode is a channel. The two words are kept apart because
[ADR-0002](docs/adr/0002-the-reference-office-is-parameters-not-a-bill-of-materials.md)
already ruled on the coupling — *content that exists to serve a recording belongs with the
recording* — which is why the directory is named for the route and not for the feed.
_Avoid_: using "episode" for the Markdown file (that is a walkthrough)

**The plate**:
What this floor *is* — the spaces, what each one is, what it is next to, and how you walk
from any of them to any other. It lives in
[`walkthrough/reference-office.plate.json`](walkthrough/README.md), it is shared by every
episode, and it **stops at topology**: no corridor widths, no egress distances, no
sanitary counts, no claim that the plan would pass anything
([ADR-0014](docs/adr/0014-the-plate-stops-at-topology.md)). Its circulation is written
down rather than inferred from where the furniture is not, and a headless Godot project
proves the whole of it is reachable from the lift lobby without crossing a desk.
Deliberately not called *the plan* — that is the **address plan**, one entry down — and
not *the office*, which is [the reference office](the-reference-office.md), the parameters
it is built from.
_Avoid_: the plan, the office, the map, the layout, the blueprint

**The floor**:
What the plate *looks like when it is drawn* — the interactive 2D scene in the viewer that
a walkthrough plays over, with pan, zoom, clickable props and a cast. **The plate is the
floor's subject; the floor is the plate's rendering**, which is why moving a wall is a
plate edit and recolouring one is not. It is a **view**: it renders facts that already
exist in Markdown and computes none
([ADR-0011](docs/adr/0011-the-floor-renders-the-reference-office-and-may-not-compute-it.md)).
Distinct from a **hero diagram**, which is static and derived from an HTML source. Named
*floor* rather than *site* on purpose: that word already means both the viewer at
[`site/`](site/README.md) and one physical place in
[`site-network-design.md`](cross-cutting/site-network-design.md), and a third sense would
have been one too many.
_Avoid_: the map, the scene, the simulation, the site, the office (that is the reference
office), the plate (that is what it draws)

**Prop**:
A clickable object on the floor — an access point, a switch, a room, an IDF, a segment.
Its id and its bindings to Markdown anchors live in the walkthrough's `*.floor.json`,
beside the script rather than under `site/`, because a fact the viewer holds alone is a
fact lost the moment the viewer is deleted. A prop's panel shows **the judgement and the
criteria** and never a configuration: this repo holds no device configurations, and it
does not grow one to fill a panel.
_Avoid_: object, entity, hotspot, marker

**Cast**:
The figures on the floor, which **are the wireless load and not decoration** — the
reference office's occupancy curve made visible, at the device count that drives the
access-point derivation. The cast may be *rendered* from numbers the repo states and may
never be used to *compute* numbers it does not.
_Avoid_: characters, sprites, agents, avatars, NPCs

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

**Vendor name**:
A product or manufacturer named in the text, and **which of two jobs it is doing
decides whether it belongs.** As a **signature** it is allowed and already in use —
naming what you will *see* in an environment (`the-stack/02`'s *LB signature* row
lists HAProxy / keepalived / F5 so a reader can recognise a self-hosted estate), or
quoting the market (`ROADMAP.md` cites *"firewalls (Palo Alto/Fortinet)"* because
that is what the postings say). As a **recommendation** it is forbidden outside a
dated `Reference build`, per
[ADR-0002](docs/adr/0002-the-reference-office-is-parameters-not-a-bill-of-materials.md).
The test: *does this name help someone recognise where they are, or is it telling
them what to buy?* The first transfers and the second expires.
_Avoid_: model name (that is narrower — ADR-0002 forbids those in Selection rules
specifically), brand, product

**Protocol name**:
The same two jobs as a **vendor name** above, and the same test. As a **signature** it is
allowed — naming what a reader will *see* and have to recognise: 802.1X and RADIUS on the
ports, LLDP on the switch, a DHCP relay in the path. As **mechanism** it is out of
altitude everywhere in this repo: how the handshake completes, how a frame finds a switch
port, how a lease is renewed. The test: *does naming it tell someone where they are, or
does explaining it tell them what the wire is doing?* The first is a signature; the second
is a different ability, and only the first one is here.
_Avoid_: protocol (unqualified, when the mechanism is meant), standard, RFC

**Altitude**:
How high above the mechanism a piece of work sits. Two uses, related and distinct.
**Tooling altitude** — which layer you drive an API from (CLI, SDK, IaC), where
reaching for the wrong one is the recurring mistake the `automation.md` companions
name. **Content altitude** — where a document stops on purpose, which is an editorial
rule rather than a description: [`the-stack/02`](the-stack/02-network.md) stops at
decisions somebody must make and own, and deliberately excludes protocol mechanics,
because *being able to run a network and being able to say what the wire is doing are
different abilities.* A section that drifts below its stated altitude is a defect even
when every sentence in it is true.
_Avoid_: level, depth (that is the 🔨 claim), layer (that is `the-stack/`)

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
transposed view of them; [`site/`](site/README.md) is a **view** — it renders
the material and adds none of it, which is the same test applied a second time
([ADR-0005](docs/adr/0005-the-site-is-a-view-not-a-seventh-axis.md)).
_Avoid_: section, category, track
