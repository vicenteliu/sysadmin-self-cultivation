---
kind: note
axis: cross-cutting
themes: [networking, identity]
platforms: [self-host]
marker: "🔨"
summary: "What actually happens between clicking connect and reaching the thing — five decisions somebody owns, an address that shows up in every log afterwards, and the reason split tunnelling breaks on DNS rather than on routing."
---
# How a remote user lands on the office network

> 🌐 **Languages:** English (default) · [中文](../docs/zh/cross-cutting/vpn-and-remote-access.md)

> [`build-out/10`](../build-out/10-remote-access.md) decides **what still requires
> network-level access**, and the answer for a SaaS-first office is a short list.
> [`remote-access-four-causes`](labs/remote-access-four-causes/) drills **why the same
> error message has four causes**. Neither says what happens in between, which is what
> was asked.
> Recorded in [`docs/questions/networking.md`](../docs/questions/networking.md).

**The altitude here is deliberate and narrow.** This note does not describe how a
tunnel is negotiated, how a key exchange completes or what a packet header looks like.
That is mechanism, and mechanism is [out of altitude everywhere in this
repo](../CONTEXT.md). What follows is the sequence of **decisions somebody made and
owns** between a person clicking connect and reaching a thing — five of them, each with
a consequence that outlives the session.

## The sentence to correct first

**A VPN does not put you "on the network".** It gives you **an address on a segment**,
and hands your machine **a set of routes** saying which destinations to send there.
That is the whole of it, and almost every remote-access design problem is one of those
two things being decided badly or not at all.

Everything below follows from taking that literally.

## Decision 1 — what proves you may have an address at all

Before anything is routed, something decides this person is allowed. In a current
estate that is the directory, and the tunnel is a client of it exactly as
[802.1X on a port is](site-network-design.md) — same question, different doorway.

**The decision that matters is what else is required besides the person.** A credential
proves who; it does not prove *what they are sitting at*. Device posture as a
condition — is this machine enrolled, encrypted, patched — is the difference between
remote access and *an account plus any laptop in the world*.

**And this is where the circular dependency lives.** The tunnel needs the directory.
If the failure you are recovering from is the directory, the tunnel is not a way in —
it is a second thing that is down. [`build-out/10`](../build-out/10-remote-access.md)
asks for a break-glass route *that does not depend on the thing being fixed*, and that
sentence is the whole reason this note flags it: it is the same shape as
[a recovery key stored behind the identity it exists to bypass](../endpoint/encryption-and-keys.md)
and as [the conditional-access lockout drill](labs/m365-conditional-access-lockout/).
Three different systems, one failure.

## Decision 2 — which segment the address comes from

This is the decision most estates skip, and skipping it quietly undoes the
segmentation work.

The office floor has [about four segments and a reason for each](site-network-design.md).
A remote user has to arrive in one of them. **The default nearly everywhere is to put
them in staff**, because that is where the people are — and the result is that the
tunnel becomes a route around the segmentation rather than an entrance through it.

**The version worth defending:** remote arrives in its own segment, with the same
question asked of it as any other — *what am I willing to block between this and the
rest, and will I actually block it?* Usually the honest answer narrows the reachable
set to the short list [`build-out/10`](../build-out/10-remote-access.md) already asked
for, which is a handful of things that could not leave the building.

**The consequence nobody plans for:** that address appears in every log downstream. If
remote users draw from a range that is indistinguishable from a desk, then six months
later *was this person in the office* is a question the estate cannot answer — and it
is asked during exactly the investigations where it matters. **Reserve the range and
make it obvious**; the address plan is the cheapest audit control in the building and
it costs one paragraph at design time.

## Decision 3 — which destinations go down the tunnel

Full tunnel sends everything. Split tunnel sends only what matches a route you install.

| | Full | Split |
|---|---|---|
| **What you get** | One path, one set of egress controls, one place to log | The internal short list arrives; everything else goes direct |
| **What it costs** | Every video call and every large download crosses your uplink twice | The controls that lived at the office egress no longer see most traffic |
| **What decides it** | Whether you are enforcing anything at egress that is not enforced elsewhere | Whether your uplink and your concentrator can carry the whole staff's internet |

**For a SaaS-first office the honest default is split**, because the traffic you would
be hauling home is a TLS session to somebody else's data centre that your egress
controls cannot inspect anyway, and the uplink is
[the one thing this office cannot lose](../the-reference-office.md#on-premises--what-cannot-leave).

**The trap is that split tunnelling does not break on routing.** Routes are easy to get
right and easy to verify. It breaks on the next decision.

## Decision 4 — which resolver answers, and for what

**DNS is where remote access actually fails**, and it fails in both directions.

- **Internal name, external resolver.** The route for the internal subnet is installed
  correctly, and the name never resolves to an address inside it, so nothing is ever
  sent down the tunnel. The user reports *the VPN is connected but nothing works*,
  which is true and is not about the VPN.
- **External name, internal resolver.** A public service whose name also exists in the
  internal zone resolves to an internal address that is only reachable through the
  tunnel. Now the service works at the desk and fails at home, or the reverse, and the
  symptom migrates with the user.

**So the decision is: which names does the tunnel claim, and which resolver serves
them.** Write that down as a list of suffixes, not as a resolver address, because the
list is the design and the address is an implementation detail that will change.

This is the same discipline the [debug ladder](site-network-design.md) applies
everywhere else in this repo: **resolve the name before you blame the path.**

## Decision 5 — what the far end can reach, and for how long

The tunnel deposits a packet on a segment. What happens next is ordinary firewalling,
and the thing worth stating is the one people forget: **a session that authenticated
three weeks ago is still authenticated.**

Re-authentication interval, idle timeout, and what happens to a live tunnel when the
person is disabled in the directory are three separate settings, and in most estates
only the first has been considered. [The reference office turns over about forty times
a year](../the-reference-office.md#why-these-numbers); a leaver whose tunnel survives
their last day is not a hypothetical there, it is a scheduling question.

## What replaced it, and what it did not replace

The category moved. Where a concentrator once terminated everyone, an identity-aware
proxy now puts individual applications behind the directory, and the user reaches them
without any network membership at all. That is a genuinely better answer **for anything
that speaks HTTP**.

**What it does not replace** is the short list from
[`build-out/10`](../build-out/10-remote-access.md): a switch's management interface, a
console, the appliance that only speaks its own protocol. Those still want network-level
access, which is why the honest current design is usually **both** — a proxy for the
applications and a small, narrow tunnel for the handful of things that could not leave
the building.

**And the failure modes did not move.** The
[four-causes drill](labs/remote-access-four-causes/) works identically against either:
one message, four causes, and elimination resolving all four where habit resolves two.

## Honest boundaries

🔨 **Hands-on.** VPN operations across offices and data centres, certificate and TLS
fundamentals, and the authentication failure paths — the material
[`build-out/10`](../build-out/10-remote-access.md) is marked 🔨 for. The DNS section
above is the one that comes most directly from being paged about it.

🧭 **Identity-aware proxy deployments at scale** — the model is clear and the trade
against a tunnel is stated above, but this author has operated tunnels and mapped the
proxy generation rather than run one for a fleet.

**Not claimed:** cryptographic review of any tunnel protocol, carrier-side transport, or
throughput engineering for a concentrator at scale.

## Read deeper

- [`build-out/10`](../build-out/10-remote-access.md) — what still requires network-level
  access, which is the decision this note assumes has been made
- [`labs/remote-access-four-causes/`](labs/remote-access-four-causes/) — one error
  message, four causes, and why elimination beats habit
- [`site-network-design.md`](site-network-design.md) — the segments a remote user has to
  arrive in one of
- [`network-evolution.md`](network-evolution.md) — why the perimeter became a boundary
  around a session rather than around a place
- [`labs/m365-conditional-access-lockout/`](labs/m365-conditional-access-lockout/) — the
  circular dependency in Decision 1, drilled
