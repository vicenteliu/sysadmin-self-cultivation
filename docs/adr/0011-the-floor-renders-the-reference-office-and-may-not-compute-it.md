---
kind: adr
axis: meta
themes: [networking]
platforms: []
summary: "The viewer is gaining an interactive 2D office — pan, zoom, clickable props, a cast of people who are the wireless load. It is the most capable thing this repo has ever rendered, which makes it the most likely to start deciding things, so the line it may not cross is drawn here."
---
# The floor renders the reference office and may not compute it

The viewer is gaining a **floor**: an interactive 2D scene of
[the reference office](../../the-reference-office.md), with pan and zoom, clickable props,
and a cast of figures at desks. A [walkthrough](0009-the-walkthrough-ships-its-script-not-its-audio.md)
plays over it.

[ADR-0005](0005-the-site-is-a-view-not-a-seventh-axis.md) settled that the site renders
the material and adds none of it, and gave the test: *if deleting `site/` would cost the
repo a fact, the boundary has been crossed.* A Markdown renderer cannot cross that line
by accident. A simulation can cross it in a single afternoon, because a scene that knows
where six access points are is one small function away from telling you where sixteen
would go.

## Decision

**The floor is a view. It renders facts the Markdown already states and computes none.**

**The cast is the load, not decoration.** `the-reference-office.md` states the occupancy
curve — around sixty-five on a Tuesday, low fifties on Monday, high thirties on Friday —
and derives roughly a hundred and forty-five associated devices from it, which is the
input to the access-point count. The figures on the floor *are* that number, so the
argument that a hundred-person office behaves like a sixty-five-person office is watchable
rather than asserted. **This is rendering: every quantity on screen is read from a
document, never calculated by the scene.** Set the headcount to four hundred and have the
floor emit an access-point count, and the viewer has just become the place a fact first
appeared.

**Zoom is semantic, in three registers, because the material has three.** Far is
occupancy, coverage and the four segments (🔨). Middle is placement — the large room
earning a dedicated radio, room systems on copper, booths counted separately (**🧭**, and
the register the narrator changes footing in). Near is the path: three access switches,
about a hundred and ten active ports, the PoE budget near five hundred watts, and the
three speed tiers drawn as three different cables (🔨). *Uplink and stacking are where the
sizing mistake lives* is a claim about what you see when you look closer, which is what
semantic zoom is for.

**A prop's panel shows the judgement and the criteria, never a configuration.** Clicking
an access point gives why it is there, how the count was reached — three by client count,
one by throughput, four by the coverage floor, five or six after placement, and coverage
is what binds — what it demands of the switch, and the anchors, which carry their 🔨/🧭
markers in the headings they link to. It does not give an SSID-to-VLAN binding or an
802.1X stanza. This repo holds no device configurations, `the-reference-office.md`'s
`Reference build` is still ⏳ with a stated entry condition, and a panel is not a reason to
trip it. **If configurations are wanted, they get written into that section first — dated,
replaceable whole, past ADR-0002's "could someone buy from this?" test — and the panel
then links to them.**

**Prop identity and anchor bindings live with the route, not with the viewer.** They sit
in `walkthrough/<episode>.floor.json`, beside the script. *There are six access points and
one of them belongs to the large room* is a fact; a fact held only under `site/` fails
ADR-0005's deletion test.

**Browsing is the default mode; narration is a layer on top.** A reader with no TTS
configured opens a floor they can explore, not a player waiting for audio. Clicking during
playback pauses the narration, because two streams of information at once cancel rather
than combine.

## Considered options

- **A decorative cast.** Figures at desks for atmosphere, carrying nothing. Rejected: it
  is a screensaver over a document, and it would leave the repo's most counter-intuitive
  finding — *size for Tuesday, not for the payroll* — exactly as invisible as it is now.
  The whole reason to build a floor is that this claim is about bodies in a room.

- **A parameterised simulator.** Sliders for headcount, floor area and device ratio, with
  the derivations wired up live. The most useful-sounding option and the one to refuse
  hardest: it would be genuinely good, and it would put the repo's arithmetic in JavaScript
  under `site/` where no reviewer, no mirror and no `--check` would ever see it. If those
  derivations should be executable, they belong in [`toolbox/`](../../toolbox/README.md)
  as a tool with a `Tested on:` line, not in a viewer.

- **Configuration snippets in the prop panels.** Rejected, and it is the rejection with a
  real cost — clicking an access point yields prose and links rather than something to
  copy, and that is part of what "boring" meant in the first place. Taken anyway, because a
  configuration has a shorter half-life than a model number and would quietly relocate this
  repo's stated altitude into an unreviewed JSON file. The route through
  `the-reference-office.md` stays open.

- **Prop bindings as viewer assets under `site/assets/`.** Simpler to build and wrong on
  ADR-0005's test. Deleting `site/` would take the office's inventory with it.

## Consequences

- **`the-reference-office.md` is now load-bearing for something rendered.** Its numbers
  appear on a screen, so a change to them changes a picture. That is the intended coupling
  and it runs one way only: the document decides, the floor follows.
- **The floor cannot answer "what about my office?", and will be asked.** The honest answer
  is the one the document already gives — *the derivations are the transferable part* — and
  the floor should point at them rather than grow a settings panel.
- **A `--check` guards what it can.** Every prop id in a `.floor.json` must resolve to an
  existing anchor in a `sources:` file, and every beat id it references must exist in the
  script. Neither check can tell whether a number on screen is the number in the document;
  that stays a human reading, the same admission
  [ADR-0008](0008-a-count-is-not-a-bound.md) had to make.
- **Three audiences, three complete artifacts.** The script reads complete on GitHub, the
  floor browses complete in silence, the audio hears complete with no screen. Any feature
  that only works when all three are present is a feature that fails most readers.
