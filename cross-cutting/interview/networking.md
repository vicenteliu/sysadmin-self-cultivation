---
kind: interview
axis: cross-cutting
themes: [networking]
platforms: []
marker: "mixed"
summary: "Pairs with skills-maps/networking.md, section for section."
---
# Networking — Interview Map

> Pairs with [`skills-maps/networking.md`](../skills-maps/networking.md), section for
> section. Format, marker rules and the anonymisation discipline are in
> [`README.md`](README.md).

`⏳` marks an answer whose specific incident is not written down yet. The question and
what it probes are settled; the example is the part only the person can supply, and a
placeholder is more honest than a plausible one.

## Addressing & subnetting 🔨

### "How would you plan addressing for a company that will grow into a second site and a cloud?"
**Probes:** whether you treat an IP plan as a *document written before the first
subnet* or as something that accretes. The tell is whether you mention overlap at all.
**Answer:** Start from the merge you are trying to avoid. Non-overlapping RFC1918
carved per site and per cloud, sized for growth rather than for today, written down
before anything is provisioned — because the alternative is discovered later, when two
estates need to talk and both are `10.0.0.0/16`. At that point the options are
renumber, NAT the overlap, or proxy, and all three are projects with names.
**Prove it:** [`toolbox/cidr-check`](../../toolbox/cidr-check/) ·
[`labs/multi-cloud-cidr-overlap`](../labs/multi-cloud-cidr-overlap/)

### "Two companies merge and both use 10.0.0.0/16. What now?"
**Probes:** whether you know there is no cheap answer, and can price three bad ones
rather than reaching for the first.
**Answer:** ⏳ *Needs the specific.* The shape is: renumber one side (cleanest,
slowest, touches every host), NAT the overlap (fast, and now every troubleshooting
session has two truths about an address), or proxy at the application layer (narrow,
only works for a small set of flows). The decision is driven by which side has fewer
hosts and more change tolerance, not by which is technically nicer.

## Routing & the path a packet takes 🔨

### "A host can't reach the internet. Walk me through it."
**Probes:** whether you have a fixed order or you guess. Interviewers are listening
for a ladder, and for whether you say what each rung *eliminates*.
**Answer:** In order, and without skipping: link, address, route, filter, DNS. Each
rung earns its place by what it rules out, not by what it reports — checking that DNS
resolves tells you nothing if the default route is missing, so the order is the
answer. The common resolution is a route table with no default, or a NAT device that
exists in the diagram and not in the subnet's route table.
**Prove it:** [`labs/remote-access-four-causes`](../labs/remote-access-four-causes/)

### "Traffic gets there but the reply never comes back. What's your first guess?"
**Probes:** asymmetric routing, and whether you know why it is invisible in logs.
**Answer:** Asymmetric path meeting a stateful firewall. The SYN arrives by one path,
the reply leaves by another, the firewall on the return path never saw the handshake
open and drops it — and both sides' logs look innocent, because neither logged an
error. The find is in the route tables, not the firewall logs.

## L2, VLANs & the underlay/overlay split 🔨

### "What's the difference between the underlay and the overlay, and which one are you configuring?"
**Probes:** whether you can locate yourself on an unfamiliar platform. Most cloud
networking confusion is this question, unasked.
**Answer:** The underlay is the physical fabric that moves packets; the overlay is the
logical network you define on top. On a cloud you almost only touch the overlay. On
vSphere you touch both — port groups and VLANs meet at the uplink, and getting that
seam wrong is how a native-VLAN mismatch silently merges two segments that were
supposed to be separate.
**Prove it:** the seven-way comparison in
[`the-stack/02`](../../the-stack/02-network.md)

### "Tell me about a time an MTU problem bit you."
**Probes:** whether you recognise the signature rather than the setting — small
requests fine, large ones hang, nothing logs an error.
**Answer:** ⏳ *Needs the specific.* The shape is encapsulation overhead: a VXLAN or
Geneve header takes ~50 bytes off the payload, the path stops passing full-size
frames, and because the failure is silent it presents as an application timeout rather
than as a network fault. It gets found by testing with a fixed packet size, not by
reading a config.

## DNS 🔨

### "Split-horizon DNS — when would you use it, and what goes wrong?"
**Probes:** whether you have run it deliberately or inherited it accidentally.
**Answer:** Deliberately, when the same name must resolve differently inside and
outside — internal hosts to private addresses, external to the public front door. What
goes wrong is that it becomes accidental: a conditional forwarder added for one
migration, never removed, and now a name resolves differently depending on which
resolver a client happened to pick. The failure is intermittent by construction, which
is why it survives so long.

### "How do you use TTL during a change?"
**Probes:** whether DNS is a change-management instrument to you or a lookup table.
**Answer:** Lower it *before* the change, not during the outage — a 24-hour TTL
discovered at cutover is a 24-hour rollback. Drop it a day ahead, make the change,
watch, then raise it back. The mistake is treating TTL as a performance setting rather
than as the width of your rollback window.
**Prove it:** [`labs/mail-authentication-alignment`](../labs/mail-authentication-alignment/)

## DHCP & host onboarding 🔨

### "PXE boot is failing intermittently for new machines. Where do you look?"
**Probes:** whether you know the boot chain has more than one server in it.
**Answer:** ⏳ *Needs the specific.* The shape is two DHCP servers answering the same
broadcast domain — one carrying boot options and one not — so which one wins is a
race, and the symptom is *intermittent*, which sends people looking at the client. The
other common cause is a relay/helper missing on the VLAN, in which case it fails
consistently rather than intermittently, and that distinction is the diagnostic.

## Filtering — designing the rules 🔨

### "How do you approach designing a rule set from scratch?"
**Probes:** default-deny as a posture, and whether you think about egress at all.
**Answer:** Start closed and open by exception, and write the egress rules in the same
sitting as the ingress ones — the outbound half is the half most estates skip, and it
is the half that matters once something is already inside. Group by what the rule
serves rather than by protocol, so a decommissioned service takes its rules with it.

### "You've inherited a firewall with 400 rules. How do you clean it up?"
**Probes:** whether you know rule order can hide the problem, and whether you'd touch
production without evidence.
**Answer:** ⏳ *Needs the specific.* The shape: first find the shadowed rules — first
match wins, so a broad rule near the top silently disables everything beneath it, and
nothing reports this. Then the any-any rules, then rules whose object stopped existing
two migrations ago. Nothing gets deleted on inspection alone; it gets disabled with
logging first, because a rule set nobody understands is one nobody can safely reason
about from the text.

## Load balancing 🔨

### "Every backend just got marked unhealthy. What happened?"
**Probes:** whether you know what the health check is actually testing.
**Answer:** Usually the check is testing something shared rather than something
per-target — a dependency behind all of them, or an endpoint that returns 200 only
when a downstream is up. A health check that can fail for every target simultaneously
is not measuring target health; it is measuring the thing they have in common. The
second candidate is a check whose timeout is shorter than the target's worst-case
response under load, which turns a slowdown into an outage.

### "Where does the certificate live — at the balancer or the backend?"
**Probes:** termination vs passthrough vs re-encryption, and whether you can say what
each costs.
**Answer:** Terminate at the balancer and it can route on content, and the traffic
behind it is plaintext on your own network. Passthrough and the backend owns the
certificate and the balancer is blind to everything above L4. Re-encrypt and you get
both, and two certificate lifecycles to keep alive instead of one. The right answer
depends on whether anything needs to inspect the request, which is a design question
before it is a TLS question.

## TLS & certificate lifecycle 🔨

### "It works in curl but the Java client fails. Why?"
**Probes:** chain of trust, specifically the missing intermediate.
**Answer:** The server is serving the leaf without the intermediate. `curl` succeeds
because the local trust store happens to have the intermediate cached; a client with a
stricter or emptier store does not, and the chain cannot be built. The fix is on the
server — serve the full chain — and the reason it looks like a client bug is that the
first client tested was the forgiving one.

### "You automated renewal and it still expired. How?"
**Probes:** whether you know renewal and reload are two steps.
**Answer:** The certificate renewed on disk and the process never reloaded, so it went
on serving the cached one until it expired. Automation that stops at "the file is new"
is automation that has done half the job. The check that catches it is testing the
served certificate over the network, not the one on the filesystem.

## Remote access & VPN 🔨

### "'The VPN won't connect.' What do you do?"
**Probes:** elimination vs habit. Several distinct causes produce a byte-identical
symptom, so the ordering of your checks is the whole answer.
**Answer:** Treat it as four candidates producing one symptom — client-side config,
the tunnel itself, the identity provider being unreachable, and a filter on the path —
and pick checks by what each *eliminates* rather than what it reports. The trap is
that "can I reach the IdP?" returns the same answer whether the IdP is down or the
tunnel that would carry you to it is down.
**Prove it:** [`labs/remote-access-four-causes`](../labs/remote-access-four-causes/)

### "What happens to remote access when the directory is unreachable?"
**Probes:** whether you have looked for the circular dependency before it fired.
**Answer:** Every path that authenticates against it stops, including — usually — the
break-glass path somebody designed for exactly this and then pointed at the same
directory. Naming that dependency in advance is the work; discovering it during the
incident is the common case.
**Prove it:** [`build-out/10`](../../build-out/10-remote-access.md)

## Network monitoring & flow analysis 🧭

### "How would you build flow-log monitoring across three clouds?"
**Probes:** whether you know the formats differ, and that aggregating before
normalising produces a confident wrong number.
**Answer:** This is a ramp, not production experience — I have mapped the three
formats and verified the differences against vendor docs, and I have not operated a
cross-cloud aggregation at scale. What I would carry in is the discipline rather than
the tooling: normalise before aggregating or the total is fiction, and be explicit
that a flow log records *a packet was permitted*, not *the application worked*. The
part I would want help sizing is retention cost, which is where these projects
actually get killed.

### "What can't a flow log tell you?"
**Probes:** whether you treat it as evidence of success. This one is answerable from
first principles and is a good place to be precise rather than vague.
**Answer:** It records that packets matched a rule and were permitted or dropped. It
cannot tell you the application worked, that the response was correct, or that the
handshake completed above L4 — a permitted SYN with no session behind it looks
identical to a healthy connection in most formats.

## Hybrid & inter-cloud connectivity 🧭

### "Design connectivity between on-prem and two clouds."
**Probes:** whether you start from addressing or from products, and whether you know
there is no central router to arbitrate.
**Answer:** A ramp — I have mapped this across four clouds and built the CIDR-overlap
drill for it, and I have not run a production multi-cloud interconnect. Starting
point is addressing, because overlap makes the rest impossible and nothing in any
cloud resolves it for you. Then hub-and-spoke rather than mesh, since full mesh ends
at about the fifth network on O(n²). DNS across the boundary is two configurations
failing independently, not one. Where I would defer is circuit procurement and the
real-world SLA negotiation, which is not something reading gives you.
**Prove it:** [`labs/multi-cloud-cidr-overlap`](../labs/multi-cloud-cidr-overlap/)

### "What drives the choice between a VPN tunnel and a dedicated circuit?"
**Probes:** whether you can name the real driver rather than reciting three
attributes.
**Answer:** Cost, latency and SLA are the stated attributes; the actual driver is
usually which one procurement can deliver in the window you have. A tunnel is
available this afternoon and a circuit is a quarter, so the honest design question is
what the tunnel is carrying until the circuit lands, and whether anything on it will
be hard to move afterwards.

## Using this file

Every `⏳` is a question you can answer and have not written down. That gap is the
point of the format: an unwritten example is indistinguishable from an absent one at
the moment it is asked for.
