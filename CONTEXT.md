---
kind: glossary
axis: start-here
themes: []
platforms: []
summary: "A glossary for this repo — the words that mean something specific here, and the words they get confused with."
---
# The Sysadmin's Self-Cultivation

> 🌐 **Languages:** English (default) · [中文](docs/zh/CONTEXT.md)

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

### The reference office

**The reference office**:
The **proper name** of one fiction: the hundred-person, one-floor, hybrid office written
down in [`the-reference-office.md`](the-reference-office.md), whose scenario choices are
set and whose everything else is derived from a stated rule. It is what
[`build-out/`](build-out/) means when a step says *a hundred people*, and it is
**parameters, never a bill of materials**
([ADR-0002](docs/adr/0002-the-reference-office-is-parameters-not-a-bill-of-materials.md)).
It **consumes services and operates none** — no product, no customer traffic, no public
endpoint it is accountable for
([ADR-0015](docs/adr/0015-the-reference-office-consumes-services-and-operates-none.md)).

**"A hundred-person office" is not this term.** It is a generic phrase, and several labs
use it for their own scenario with their own numbers — 97 devices, seven ticket
categories, two document estates — none of which cites this file. That is allowed; what
is not allowed is letting the two blur, because a repo with two unnamed hundred-person
offices cannot tell you which one a number came from. **The proper name is the one with a
file behind it.** Where a lab's number and this file's derivation are both live, the
derivation wins and the lab is corrected, since a number that survives a rule is a
parameter and a number that does not is a coincidence.

Distinct from **the plate** (the topology it is drawn as) and **the floor** (the drawing),
both below.
_Avoid_: the office (unqualified, when the plate is meant), the scenario, the example
office, our office

### The walkthrough

**Walkthrough**:
A narrated pass through [`the-reference-office.md`](the-reference-office.md), written to
be **spoken by a text-to-speech engine and heard** — never read. One file per walkthrough
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

_Erratum_: seven decision records predate this entry and use *episode* for the file —
[0002](docs/adr/0002-the-reference-office-is-parameters-not-a-bill-of-materials.md) and
[0009](docs/adr/0009-the-walkthrough-ships-its-script-not-its-audio.md) through
[0014](docs/adr/0014-the-plate-stops-at-topology.md), in `<episode>.floor.json`, *the
first episode*, *two scripts per episode* and *what an episode owns*. Where those same
records say *the published episode*, the word is the one defined here.
**The records are not edited.** That is the precedent
[ADR-0008](docs/adr/0008-a-count-is-not-a-bound.md) set when it left ADR-0007's
sentences standing and wrote the correction beside them, and it is the same rule a
frozen walkthrough follows: an error becomes an erratum, because a silent fix leaves
the record lying about what it said.

**The plate**:
What this floor *is* — the spaces, what each one is, what it is next to, and how you walk
from any of them to any other. It lives in
[`walkthrough/reference-office.plate.json`](walkthrough/README.md), it is shared by every
walkthrough, and it **stops at topology**: no corridor widths, no egress distances, no
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

**Fleet**:
Ambiguous in this repo and therefore **never load-bearing on its own**. It appears in two
senses already: *servers or VMs under configuration management*
([`iac-and-config.md`](cross-cutting/iac-and-config.md),
[`ci-cd.md`](cross-cutting/ci-cd.md), [`web-and-tls.md`](cross-cutting/web-and-tls.md),
[`kubernetes.md`](cross-cutting/kubernetes.md)) and *the managed endpoint population*
([`ROADMAP.md`](ROADMAP.md)'s "macOS/Windows fleet",
[`platforms/self-host/`](platforms/self-host/)'s "PXE and image pipelines at fleet
scale"). Both are established and neither is being renamed. **Qualify it or use the
specific word** — *endpoints*, *the estate*, *hosts under Ansible* — and in particular the
reference office's endpoint parameters are titled *Endpoints and spares*, not *the fleet*,
so that a third sense is never coined.
_Avoid_: fleet unqualified where the reader cannot tell laptops from servers

**Deployment**:
**Two unrelated jobs in this repo, and neither gets the bare word.** In
[`ci-cd.md`](cross-cutting/ci-cd.md) and everything downstream of it, deploying means
**shipping code to an environment**. In [`endpoint/`](endpoint/README.md) and
[`build-out/04`](build-out/04-devices-and-images.md) the same English word means
**putting a machine into a person's hands**. Both usages are established and neither is
being renamed, so the device side says **provisioning** — or **imaging** for the build
half specifically — and the code side keeps *deployment*. A sentence that needs the bare
word is a sentence in the wrong chapter.
_Avoid_: deployment for devices; rollout for either, since it hides which one is meant

**File server** / **suite storage**:
Two answers to *where do the files live*, and [`build-out/07`](build-out/07-files-and-collaboration.md)
already calls the move between them SaaS-ification. A **file server** is storage this
office runs: a box, a filesystem, permissions on directories, and a backup that is now
your problem. **Suite storage** is the drive inside a productivity tenant, where the
sharing model — not the filesystem — decides who can read what, which is why
[`permission-sprawl`](cross-cutting/labs/permission-sprawl/) is a lab about links rather
than about ACLs. The distinction is load-bearing because the two fail differently: a file
server loses data, and suite storage loses track of who can see it.
_Avoid_: network drive, shared drive, cloud drive, 网盘 — each of them names one of the
two while sounding like it names both

**Inventory** / **asset register**:
**An inventory is what you discovered. An asset register is what you wrote down.** The
first comes from something that looks — a scan, an agent, a management console. The
second is a record with an owner, a cost centre and a lifecycle state. They are never
equal, and **the gap between them is not an error to be eliminated**: it is the estate's
actual condition, and measuring it is the whole of
[`asset-reconciliation`](cross-cutting/labs/asset-reconciliation/), where two systems both
report ninety-seven devices and three records are still wrong. A tool that reconciles them
to zero has hidden the finding, not fixed it.
_Avoid_: CMDB (that is one implementation of the register), asset list, inventory system
when the register is meant

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
procedure and shows it failing. **The mechanical test is whether CI can run it**,
which is why [`check.py`](check.py) discovers labs by their `*_drill.py` and runs
every one of them on every push.
_Avoid_: tutorial, exercise, demo

**Guided run**:
The other kind, and it needed its own word because the repo has both. A **step-by-step
exercise against a real environment** — a cloud sandbox, a local cluster, a developer
tenant — where the learning is in doing it and **nothing can assert that you did**.
Coined in the Walkthrough entry above to keep *walkthrough* free; defined here because
eleven of them were sitting in the tree labelled *planned lab*, which promised an
artifact that was never going to arrive.

**A guided run is not a lesser lab.** It reaches things a model cannot: real latency,
real error messages, real bills, and the muscle memory of a console. What it cannot do
is fail in CI, which is the whole of the distinction. Where a spec asks for a sandbox
account, a `kind` cluster or a `pip install`, it is describing this.
_Avoid_: lab (that is the self-verifying kind), tutorial, workshop

**Axis**:
One of the repo's six faces over one body of material — by platform, by layer, by
theme, and so on. Something that teaches no new page is **not** an axis, however
useful ([ADR-0001](docs/adr/0001-the-build-out-is-a-route-not-a-seventh-axis.md)).
`build-out/` is a route across the axes; `cross-cutting/skills-maps/` is a
transposed view of them; [`site/`](site/README.md) is a **view** — it renders
the material and adds none of it, which is the same test applied a second time
([ADR-0005](docs/adr/0005-the-site-is-a-view-not-a-seventh-axis.md)).
_Avoid_: section, category, track
