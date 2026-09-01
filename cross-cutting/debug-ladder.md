---
kind: note
axis: cross-cutting
themes: [networking]
platforms: [self-host]
marker: "🔨"
summary: "One command per rung of the network debug ladder, chosen for what it eliminates rather than what it reports — and the two answers that carry more information than everything else on this page."
---
# The debug ladder, one rung at a time

> [`the-stack/02`](../the-stack/02-network.md) draws the ladder: does the name resolve,
> is there a route, do the filters allow it, do big packets hang, and only then may you
> look. This note gives **each rung the command that verifies it** — and, more
> importantly, says **what a passing answer lets you stop considering.**
> Recorded in [`docs/questions/networking.md`](../docs/questions/networking.md).

**Why this is not a command reference, deliberately.** A reference is organised by tool
and answers *what does this command do*. This is organised by **question**, and every
entry has to earn its place the way every check in this repo does —
[a check earns its place by what it eliminates, not by what it
reports](labs/remote-access-four-causes/). A command that eliminates nothing is not a
rung, however famous it is.

The ladder is the invariant. **The commands are a dialect**, and they change per
operating system and per platform; that is why the per-rung tables below are short and
why none of them is exhaustive.

## Rung 0 — what exactly is "it"?

Before the first rung, the single most common way to waste an hour: **climbing the
ladder against the wrong target.** The user says *the site is down*; the site has four
names, two of which are aliases, and one resolves differently inside the building.

Establish three things and write them down where the ticket can see them: **the exact
name or address**, **from which machine**, and **what "works" would look like.** If you
cannot state the third one, you are not debugging, you are sympathising.

## Rung 1 — does the name resolve, and to what you think?

**The question.** Not *is DNS up*. Whether **this name**, from **this machine**,
resolves to the address you believe it does.

| Where | The command | What it answers |
|---|---|---|
| Linux / macOS | `dig +short NAME` and then `dig +short NAME @RESOLVER` | What the system answers, then what a **named** resolver answers |
| Windows | `Resolve-DnsName NAME` and `Resolve-DnsName NAME -Server RESOLVER` | The same two questions |
| Anywhere | `getent hosts NAME` on Linux | What the **resolver library** returns, which is not always what `dig` returns |

**What a pass eliminates:** the whole of DNS, *for the tool you just ran*.

**And that caveat is the trap.** `dig` talks to the resolver in your configuration.
An application may use a different one — a container's, a VPN client's, a runtime's own
stub, a browser's encrypted resolver. **A passing `dig` and a failing application is a
DNS answer, not a DNS pass**, and it is the single most common false summit on this
ladder. The [remote-access note](vpn-and-remote-access.md) is the same failure seen
from the tunnel's side.

**Run the two-resolver form by reflex.** One query says what you get; two say *whether
the resolver is the variable*, which is the actual question, and it costs one extra
line.

## Rung 2 — is there a route, and does the return path exist?

**The question.** Whether packets have a way there **and back**. You can normally only
see the first half, which is why asymmetry survives so long.

| Where | The command | What it answers |
|---|---|---|
| Linux | `ip route get ADDRESS` | The exact route **this packet** will take, source address included — not the whole table |
| macOS | `route -n get ADDRESS` | The same |
| Windows | `Find-NetRoute -RemoteIPAddress ADDRESS` | The same |
| Cloud | the platform's *route table* for the subnet, and the peering's own | The half a guest OS cannot see |

**Why `ip route get` and not `ip route show`:** the table tells you what exists; `get`
tells you **what will be chosen**, which is the question, and it applies the same
longest-prefix logic that is about to surprise you.

**What a pass eliminates:** your side's routing. **It does not eliminate the return
path**, and it never can from here. When everything on this rung looks right and the
connection still hangs, asymmetry is the first thing to suspect and the last thing
anybody checks.

## Rung 3 — do the filters allow it, both layers, both directions?

**The question.** Whether something is dropping it — and this rung carries **the single
highest-information answer in network debugging.**

| Where | The command | What it answers |
|---|---|---|
| Anywhere | `nc -vz HOST PORT` | Refused, timed out, or open — the distinction below |
| Linux / macOS | `curl -sS --max-time 5 -o /dev/null -w '%{http_code}\n' URL` | The same distinction plus whether the service answered |
| Windows | `Test-NetConnection HOST -Port PORT` | The same |
| Cloud | the security group **and** the stateless layer under it | The layer people forget until a return packet is dropped |

**The two answers, and why the difference is worth more than the rest of this page:**

- **Refused** means your packet **arrived** and something on the other side actively
  said no. Routing works. Filtering to that host works. The problem is at the far end —
  a service not listening, or bound to the wrong interface. **You have eliminated three
  rungs with one word.**
- **Timed out** means **you know nothing.** It is what a dropped packet, a black-holing
  filter, a wrong route and a dead host all look like. A timeout is the ladder telling
  you to keep climbing, not an answer.

**Stateless layers are where the return path dies.** A stateful filter that allowed the
outbound remembers the flow; a stateless one has to be told about the reply
independently, and the failure looks exactly like a routing problem from the client.

**What a pass eliminates:** filtering **in the direction you tested**. Same asymmetry
caveat as rung 2, and the same reason it survives.

## Rung 4 — do small packets work and big ones hang?

**The question.** Whether the path can carry a full-sized packet. The signature is
unmistakable once you have seen it: **the handshake completes, the transfer stalls.**
Logging in works and downloading does not. It is the rung people skip and then spend a
day below.

| Where | The command | What it answers |
|---|---|---|
| Linux | `ping -M do -s 1472 HOST`, then bisect the size | The largest packet that crosses **without fragmentation** |
| macOS | `ping -D -s 1472 HOST` | The same |
| Windows | `ping -f -l 1472 HOST` | The same |

**Why the number is 1472 and not 1500:** the flag sets the payload, and the headers
are on top. **Do not memorise it — bisect.** What you want is the boundary, and the
boundary is what tells you which encapsulation is in the path.

**What a pass eliminates:** MTU, and with it the whole class of *works until it has to
move data*. **What a failure tells you is more specific than a fix**: the size where it
breaks names the overhead, and the overhead names the tunnel — which is why this rung
appears again in [`service-mesh.md`](service-mesh.md) and in
[`kubernetes.md`](kubernetes.md) with the same shape and more rungs.

## Rung 5 — now you may look

Only now. Four rungs of elimination have earned it, and the reason for the order is
economic rather than moral: **a capture is the most information and the most expensive
to read.** Opening it first means reading everything to find nothing.

| Where | The command | What it answers |
|---|---|---|
| Linux / macOS | `tcpdump -ni IFACE host HOST and port PORT` | Whether the packet left, and what came back |
| Cloud | flow logs for the interface, filtered to the same five-tuple | The same question where you cannot attach |

**The discipline that makes this rung short:** you arrived with a hypothesis, because
four rungs eliminated the alternatives. Capture to **confirm or kill that hypothesis**,
then stop. A capture opened without one is a hobby.

## Why the order is the order

Each rung is **cheaper than the one below it** and **eliminates more**. That is the
whole design, and it is why skipping is expensive rather than merely untidy: skip to
the capture and you are reading packets without knowing which packets matter, and every
one of them looks plausible.

It is also why *ping* does not have a rung of its own. `ping` answers *did something
reply to an ICMP echo*, and a failure is consistent with a route problem, a filter, a
dead host, and a policy that simply drops ICMP. **It eliminates nothing**, which is not
an argument against running it — it is an argument against believing it.

## Honest boundaries

🔨 **Hands-on.** This is core operational ground: routing and switching at CCNP level,
years of DNS and DHCP ownership, firewalls and VPNs across offices and data centres,
and the failure paths in [`build-out/10`](../build-out/10-remote-access.md). The
refused-versus-timeout section and the MTU signature are both scar tissue rather than
reading.

**Deliberately not here:** every flag each of these tools accepts, the equivalents on
platforms not listed, and packet-level protocol analysis. That is the reference this
note was
[narrowed away from](../docs/questions.md#boundaries), and the narrowing is the point —
a per-rung command serves the ladder, a reference replaces it with recall.

## Read deeper

- [`the-stack/02`](../the-stack/02-network.md) — the ladder itself, and the admin
  discipline it belongs to
- [`labs/remote-access-four-causes/`](labs/remote-access-four-causes/) — the ladder
  drilled: one message, four causes, elimination resolving all four where habit
  resolves two
- [`vpn-and-remote-access.md`](vpn-and-remote-access.md) — rung 1's false summit, from
  the tunnel's side
- [`foundations/`](../foundations/) — the debugging reflex this is one instance of
- [`site-network-design.md`](site-network-design.md) — the design the ladder is climbed
  against
