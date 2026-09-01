---
kind: note
axis: cross-cutting
themes: [networking]
platforms: [self-host]
marker: "mixed"
summary: "Fifteen years of office network change, and the single move that explains most of it — the network stopped being the path to your work and became the path to the internet. What that did to the firewall, the load balancer, the desk port and the radios."
---
# What changed in the office network, and what did not

> Six questions arrived asking this in different shapes — how the architecture
> changed, how the protocols changed, what a firewall was before it was an
> application firewall, what an F5-class box actually does, how wireless changed, and
> why it is not simply gigabit everywhere. They have one answer underneath them, so
> they get one note.
> Recorded in [`docs/questions/networking.md`](../docs/questions/networking.md).

**Every product name here is a signature and never a recommendation.** The test this
repo applies ([`CONTEXT.md`](../CONTEXT.md)): *does naming it help you recognise where
you are, or is it telling you what to buy?* The first transfers. The second expires in
about two years, which is roughly how long ago the last confident buying opinion in
this field stopped being right.

## One move explains most of it

In 2010 the office network was **the path to your work.** The file server was down the
hall. Mail was in a rack you could touch. The line-of-business application ran on a box
somebody in the building was responsible for. A person's productive day depended on
packets that never left the premises, and the design followed: fat LAN, fast local
switching, a modest pipe to the outside because the outside was where you read the news.

Today the office network is **the path to the internet.** Nothing you actually work on
is inside the building — the tenant, the suite, the code host, the ticket system are
all somebody else's. [`build-out/02`](../build-out/02-the-building.md) states the
consequence flatly: *workloads left the building.*

That single sentence produces almost every difference below. Read the rest of this note
as its consequences rather than as a list of changes.

## The architecture

| | Then | Now |
|---|---|---|
| **What the LAN carries** | Traffic to servers in the building | Traffic to the edge of the building and out |
| **Where the value concentrates** | The core switch and the server VLANs | The uplink, and the identity that gates it |
| **The perimeter** | A boundary around a place | A boundary around a **session** — the place stopped being defensible when the work left it |
| **What a segment means** | Often a department or a floor | A trust level, and there are about four of them ([`site-network-design.md`](site-network-design.md#segmentation--a-reason-per-segment-)) |
| **Where the redundancy is** | Two of everything in the rack | Two ways out of the building; one of most things inside it |
| **What breaks the office** | The server room | The uplink, and the identity provider that is not in the building either |

**The load did not shrink, it relocated.** It went up — to the uplink — and sideways,
to wireless. The desk stayed where it was, which is the whole of the next section.

## Speed, which did not increase where people expect

The honest answer to *it cannot still be gigabit everywhere* is: **at the desk, yes it
can, and that is the correct design rather than a budget failure.**

| Tier | Then | Now | Why |
|---|---|---|---|
| **Desk port** | 100M, then 1G | **still 1G** | Nothing at a desk here is starved. The work is a TLS session to somebody else's data centre, and the bottleneck is never the copper |
| **AP-facing port** | 100M was fine | **multi-gig** | A current-generation radio can exceed a gigabit, and a 1G drop makes the access point the bottleneck it was bought to remove |
| **Access-to-core uplink** | 1G, sometimes bonded | **10G** | It aggregates everything the floor does, and everything the floor does now leaves |
| **The uplink to the world** | Single-digit megabits, and a second line was exotic | **Hundreds of megabits to gigabits, with a diverse second path** | This is where the work went, so this is where the money went |

**So the speed story is a shape, not a number.** The money moved *up and sideways* —
into the uplink and into the radios — and the desk is the one tier that did not need it
and still does not. Specifying the desk up is the most common way to spend a network
budget in the wrong ceiling, and it looks like diligence.

## The firewall: the axis changed, not the throughput

**What came before** an application-aware firewall was a device that made decisions on
**port and protocol**. You wrote rules about TCP 25 and TCP 443 and UDP 53, and those
numbers meant something, because an application and a port had a stable relationship.

**What broke that** was not an attack. It was **TLS on 443 for everything.** Once the
suite, the code host, the ticket system, the file storage, the video call and the
attacker's exfiltration all look like an outbound HTTPS session, a rule about port 443
is a rule about *the internet*, which is not a rule.

**So the axis moved from port to identity — twice.**

- **Application identity.** The device now decides what an application *is* by looking
  at the session rather than at the port number. That is the change that renamed the
  category; everything else marketed alongside it is a feature.
- **User identity.** A rule that says *finance may reach the payroll service* is worth
  writing; a rule that says *10.20.4.0/24 may reach 203.0.113.7* is a rule about
  furniture. This is why
  [`site-network-design.md`](site-network-design.md) treats network authentication as an
  identity decision and not a networking one, and why 802.1X sits where it does in
  [`build-out/05`](../build-out/05-network.md).

**As a signature:** a Palo-Alto-class box in an estate tells you somebody bought
application and user visibility, usually after an audit asked a question that port
rules could not answer. What it *replaced* was typically a stateful firewall from a
router vendor, often the same box that terminated the WAN link — and that consolidation
is the more interesting half of the history, because it is why the firewall is now a
separate device with a separate lifecycle and a separate renewal.

**What did not change:** the rule set still grows monotonically, nobody removes rules,
and the shadowed rule that has been dead for three years is still the one that makes
the next change dangerous. New axis, same failure mode.

## The load balancer, and why you meet fewer of them

**What an F5-class device actually does**, stripped of the product:

1. **Terminates TLS**, so certificates live in one place with one renewal instead of on
   every backend.
2. **Spreads load** across backends and stops sending traffic to the ones that fail a
   health check — the part everybody names, and the least interesting.
3. **Holds the logic that has nowhere else to live.** Header rewrites, path routing,
   redirects, the rule somebody added during an incident in 2017. This is the real
   answer and the reason these devices become load-bearing: **they accumulate
   application behaviour that is not in any application's repository.**

**Why you meet fewer of them in an office**: because the applications left. A hundred-
person office has no service to balance —
[ADR-0015](../docs/adr/0015-the-reference-office-consumes-services-and-operates-none.md)
says so for the reference office explicitly. Where you still meet one is in front of an
estate that kept something, or one layer down inside a cloud, rented by the hour and
called something else.

**As a signature:** finding an F5-class appliance tells you there is, or recently was,
an application estate somebody owns. Finding HAProxy and keepalived instead tells you a
team that runs Linux built the same thing themselves — the *LB signature* row in
[`the-stack/02`](../the-stack/02-network.md) lists those side by side across seven
platforms for exactly this recognition.

## Wireless 🧭

**Footing first**, because this section's is different from the rest of the note.
Wireless design is the 🧭 in [`site-network-design.md`](site-network-design.md#honest-boundaries)
and it stays 🧭 here: the generational history below is drawn from published
engineering guidance and checked for internal consistency, not from having planned and
then lived with a floor's RF.

**What genuinely changed across the generations:** capacity per square metre. More
spatial streams, wider channels, and scheduling that lets an access point talk to
several clients in one transmission rather than queueing them. That is a real and large
improvement and it is about **density**, not about any one client going faster.

**What barely moved:** the number of clients one radio serves well. Planning still lands
near **twenty-five active clients per radio** — an airtime-fairness limit rather than a
spec-sheet one, which is why the figure has survived several generations of marketing
that implied otherwise. [The reference office's derivation](../the-reference-office.md#wireless--count-it-twice-and-take-the-larger)
uses it and says where it comes from.

**What changed operationally, and matters more than the PHY rate:** the client's
experience is now dominated by **band and access-point steering and by how a handoff is
handled**, not by peak throughput. A floor with excellent radios and bad placement is a
floor with bad wifi, and no generation has fixed that.

**And one thing reversed.** Cabling every desk generously used to be the expensive,
obviously-correct call. It still happens — [`build-out/02`](../build-out/02-the-building.md)
says the runs still go to every desk — but the *load* moved to wireless and to
power-over-ethernet for the radios, so the cabling budget's centre of gravity moved from
desk density to **watts at the ceiling**.

## What did not change at all

Worth as much as the list above, because it is where the next outage comes from.

- **DNS and DHCP are still what actually breaks.** Every generation of this stack has
  produced an outage that looked like everything being down and was one of these two.
- **A broadcast domain still has a size**, and somebody still finds out empirically.
- **Copper is still about a hundred metres.** Physics did not get a release note.
- **The thing you cannot see is still the thing that pages you** — which is why the
  debug ladder is a ladder and gets climbed in order.
- **Nobody removes a firewall rule.** See above.

## Honest boundaries

🔨 **Lived, on the wired side.** Segmentation, addressing, DNS and DHCP ownership,
802.1X to a directory, guest isolation, VLANs, firewalls and VPNs across offices and
data centres — CCNP-level routing and switching, and years of the operational half. The
architecture, speed and firewall sections above are that ground.

🧭 **Wireless**, as marked in its own section and consistently with
[`site-network-design.md`](site-network-design.md#honest-boundaries).

🧭 **Market history is not the same as vendor history.** This note says what a class of
device did and what it replaced. It does not say which vendor won which quarter, or
what a current licence costs, because both date faster than anything else here and
neither transfers.

**Not claimed:** carrier-side evolution, service-provider routing at scale, or anything
about the economics of the transitions above.

## Read deeper

- [`site-network-design.md`](site-network-design.md) — the current state, designed
  rather than narrated
- [`the-stack/02`](../the-stack/02-network.md) — the same layer compared across seven
  platforms, including the LB and DNS signature rows
- [`the reference office`](../the-reference-office.md#selection-rules) — where the speed
  tiers above become numbers for one floor
- [`build-out/02`](../build-out/02-the-building.md) — *workloads left the building*, the
  sentence this whole note is a consequence of
- [`docs/questions/networking.md`](../docs/questions/networking.md) — the six questions
  this answers, and the two it does not
