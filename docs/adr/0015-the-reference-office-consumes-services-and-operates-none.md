---
kind: adr
axis: meta
themes: []
platforms: []
summary: "The reference office was asked to grow parameters for a cloud footprint and an online service, and nobody had ever said whether this office operates anything. It does not: it is a hundred-person company's IT department, and the material that would back a product side is the material this repo teaches generally rather than lives in."
---
# The reference office consumes services and operates none

[`the-reference-office.md`](../../the-reference-office.md) was asked to grow three new
parameter domains: a self-hosted VM host, a cloud footprint, and an online service. Two of
those turn on a question the file has never answered and never noticed it was not
answering — **does this office run anything for anybody outside it?**

The question is not idle, because this repo already holds the material a product side
would need. [`cross-cutting/ci-cd.md`](../../cross-cutting/ci-cd.md),
[`kubernetes.md`](../../cross-cutting/kubernetes.md),
[`databases.md`](../../cross-cutting/databases.md) and
[`web-and-tls.md`](../../cross-cutting/web-and-tls.md) are all written and all useful. A
reader who meets the reference office after reading those four will reasonably ask why the
office never touches any of them.

The answer was sitting in the build-out the whole time, unstated. Its sixteen steps are
uplink, building, identity, devices, network, tenant and mail, files, endpoint security,
backup, remote access, assets, rooms, help desk, compliance and joiner-mover-leaver.
**Not one of them ships anything to a customer.** And two steps have already decided which
way the workloads went:

> | What the room holds | servers, storage, tape, UPS | switches, an access controller, a print device, a little lab gear |
>
> **How much of that is AI: none.** The change here is that workloads left the building —
> SaaS-ification and hosting, not models.
> — [`build-out/02`](../../build-out/02-the-building.md)

> | Where the image lives | on-site, on your infrastructure | a config profile and an app list; the "image" is mostly the OS vendor's |
> — [`build-out/04`](../../build-out/04-devices-and-images.md)

## Decision

**The reference office is a hundred-person company's IT department. It consumes services
and operates none.** There is no product, no customer traffic, no public endpoint it is
accountable for. When the office appears in a sentence, the thing being run is being run
*for the hundred people in the building*.

**What its parameters may hold:** what it buys and how many seats of it, where identity
lives, what the endpoints are and how they are replaced, what reaches the help desk, what
data exists and what losing it costs, and what runs on premises **because it cannot
leave**. Consumption, and the estate that consumes.

**What they may not hold:** a service's traffic, its release cadence, its error budget,
its customers, its on-call rota, or any number that only exists because somebody outside
the building depends on it.

**A product side, if it is ever wanted, is a separate named scenario** — its own file, its
own parameters, its own honesty markers — and not a section of this one. It is not
forbidden. It is a different fiction, and it does not get to arrive unannounced inside
this one.

**The cloud half of `Where things run` inherits this line.** Every entry in it answers a
single question: *why is this not in the IDF?* A cloud parameter that cannot answer that
is describing somebody else's estate.

## Considered options

- **Let the office operate a product.** The material exists, and it would make the four
  cross-cutting notes concrete for the first time. Rejected on two counts. It changes what
  this repo is *about* — from an IT department supporting a hundred staff to a company
  running a service — and it would do it in a parameter table, with no decision record
  anywhere. And the four notes it would draw on are all marked `mixed`, while the office's
  existing derivations are 🔨; the one place where this repo's hands-on ground is concrete
  would become the place where it is thinnest.

- **Say nothing and decide it per parameter.** The status quo, and it is what was already
  happening: three domains were proposed for this office before anyone asked whether the
  office operates anything. Rejected on [ADR-0008](0008-a-count-is-not-a-bound.md)'s
  lesson, which is exactly this shape — a boundary that lives only in prose gets crossed
  without anyone noticing, because nothing is checking it.

- **Keep one file and split it into an office half and a product half.** Rejected because
  the repo is already carrying the cost of two unnamed hundred-person offices: three labs
  say *a hundred-person office* and invent their own numbers, and none of them cites
  `the-reference-office.md`. Adding a second fiction *inside* the file that is supposed to
  settle that is the wrong direction.

- **Put the product side in `platforms/`.** Rejected because those directories teach a
  platform across seven surfaces; they are not scenarios, and a scenario dropped into one
  would be read as a claim about that platform.

## Consequences

- **The cloud and on-premises halves of `Where things run` are defined against each
  other**, which is why they are one ⏳ section and not two. Each line on one side exists
  because of a reason the other side could not satisfy.
- **`ci-cd.md`, `kubernetes.md`, `databases.md` and `web-and-tls.md` gain no office
  anchor, and that is not a gap.** They teach at their own altitude. A reader looking for
  where the reference office uses them will find this record instead.
- **A future product scenario starts here.** Whoever writes it inherits a decision that
  already says what it must not do: arrive as a section of the office.
- **The `Where things run` section stays ⏳ until something asks.** Nothing in the repo has
  yet been forced to invent this office's cloud numbers — the four labs that anchor to *a
  hundred-person office* are the help desk, asset reconciliation, permission sprawl and
  mail authentication, and not one of them is about cloud. The section carries its entry
  condition and no content, the way `Reference build` has since it was written.
