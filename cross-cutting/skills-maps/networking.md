---
kind: skill-map
axis: cross-cutting
themes: [networking]
platforms: []
marker: "mixed"
summary: "One theme, cut across every platform. The substance lives in the-stack/02-network.md — this is the checkable version of it."
---
# Networking — Theme Skill Map

> One theme, cut across every platform. The substance lives in
> [`the-stack/02-network.md`](../../the-stack/02-network.md) — this is the
> checkable version of it. Conventions, tier anchors and the marker rule are in
> [`README.md`](README.md).

Tiers anchor on **how far the skill travels**: **Core** is true on all seven
platforms, **Working** is true on most and you must know which one you're on,
**Depth** is where the platforms genuinely disagree. Check a box when you can
*do* it and *explain the failure modes*.

## Addressing & subnetting 🔨

- [ ] **Core** — Split a prefix by hand — subnet count, usable hosts, broadcast — without a calculator.
- [ ] **Core** — Write an **IP plan that survives five years**: non-overlapping RFC1918 across every site and cloud, room to grow, written down *before* the first subnet exists.
- [ ] **Core** — Explain what a /31 is for on a point-to-point link, and why /24-everywhere is a decision with a cost.
- [ ] **Working** — Size a cloud subnet knowing the platform reserves addresses inside it, and that the number differs per cloud.
- [ ] **Working** — Dual-stack IPv6: address scopes, why NAT largely disappears, and what that changes about egress.
- [ ] **Depth** — Two estates arrive with overlapping `10.0.0.0/16`. Enumerate the options — renumber, NAT the overlap, proxy — and price each. There is no cheap one.

**Prove it:** [`toolbox/cidr-check`](../../toolbox/cidr-check/) · [`labs/multi-cloud-cidr-overlap`](../labs/multi-cloud-cidr-overlap/)

## Routing & the path a packet takes 🔨

- [ ] **Core** — Read a route table and predict where a packet goes. Longest-prefix match, not table order.
- [ ] **Core** — Trace *"this host can't reach the internet"* in a fixed order — link, address, route, filter, DNS — without skipping to a guess.
- [ ] **Core** — Default route, on-link, next-hop, blackhole: say what each does to a packet.
- [ ] **Working** — Source NAT vs destination NAT, and why an outbound-only design still needs a device somebody pays for.
- [ ] **Working** — Recognise **asymmetric routing** from the symptom: the SYN arrives, the reply leaves by another path, the stateful firewall drops it, and both sides' logs look innocent.
- [ ] **Depth** — BGP as it actually appears in hybrid: what gets advertised, what gets propagated to a cloud gateway, and how a route you did not intend to export gets out.

## L2, VLANs & the underlay/overlay split 🔨

- [ ] **Core** — Say which of the two planes you are configuring on the platform in front of you. Most cloud confusion is this question, unasked.
- [ ] **Core** — VLAN, trunk, access port, native VLAN — and the native-VLAN mismatch that silently merges two segments.
- [ ] **Working** — Encapsulation (VXLAN/Geneve) and the MTU it costs — then find the 50-ish bytes on the wire.
- [ ] **Working** — Same concept, three vocabularies: vSphere port groups, Proxmox bridges, OpenStack Neutron networks.
- [ ] **Depth** — Distributed firewalling in an overlay: enforcement at the vNIC instead of at a chokepoint, and what that does to your rule count.

## DNS 🔨

- [ ] **Core** — Walk the resolution chain out loud: stub → resolver → root → TLD → authoritative, and say which step cached the answer you are looking at.
- [ ] **Core** — The operationally load-bearing record types: A/AAAA, CNAME, MX, TXT, SRV, PTR, NS, SOA.
- [ ] **Core** — Read a `dig` answer: which server replied, was it authoritative, what was the TTL, and is this the answer the *application* gets.
- [ ] **Working** — Split-horizon **on purpose**, and TTL as a change-management instrument — lower it before the change, not during the outage.
- [ ] **Working** — Private zones per cloud plus conditional forwarding to on-prem, in both directions.
- [ ] **Depth** — The TXT-record family that carries mail authentication, and why publishing all three still proves nothing on its own.

**Prove it:** [`labs/mail-authentication-alignment`](../labs/mail-authentication-alignment/)

## DHCP & host onboarding 🔨

- [ ] **Core** — DORA, lease, reservation, scope — and diagnose scope exhaustion from the symptom rather than the alert.
- [ ] **Core** — The options that carry weight: gateway, DNS, NTP, and the boot options PXE depends on.
- [ ] **Working** — Relay/helper across subnets: why the broadcast crosses a router only because something forwarded it.
- [ ] **Working** — What replaces DHCP in each cloud, and where the metadata service takes over the job.
- [ ] **Depth** — The PXE/iPXE chain end to end on bare metal, including the handoff that fails silently when two DHCP servers answer.

## Filtering — designing the rules 🔨

- [ ] **Core** — Stateful vs stateless, and which layer each platform gives you which — then say which one a return packet needs.
- [ ] **Core** — **Default-deny as a posture**: a rule set that starts closed and opens by exception, not one that starts open and closes by incident.
- [ ] **Core** — Read a rule set and answer *"does this flow pass?"* on paper, before touching the estate.
- [ ] **Working** — Rule **order** and shadowed rules: first match wins, so a broad rule at the top silently disables everything beneath it — and nothing reports this.
- [ ] **Working** — **Egress** filtering — the half most estates skip, and the half that matters once something is already inside.
- [ ] **Working** — Security groups vs NACLs vs an appliance policy: three enforcement models with three different blast radii.
- [ ] **Depth** — Review a grown rule set: find the unused rules, the any-any rules, and the rules whose object stopped existing two migrations ago.

## Load balancing 🔨

- [ ] **Core** — L4 vs L7: what each can see, and therefore what each can route on.
- [ ] **Core** — Health checks — what "healthy" is actually testing, and the failure mode where every target is marked down at once.
- [ ] **Working** — Session affinity, connection draining, idle timeouts — the three settings behind most "it works but users get logged out" tickets.
- [ ] **Working** — TLS termination vs passthrough vs re-encryption, and where the certificate lives in each.
- [ ] **Depth** — Read an access log to attribute a latency spike to the balancer, a target, or the client.

## TLS & certificate lifecycle 🔨

- [ ] **Core** — What a certificate actually asserts — and what it does not.
- [ ] **Core** — Chain of trust: leaf, intermediate, root. Diagnose the missing-intermediate bug that works in one client and fails in another.
- [ ] **Core** — Read a certificate: SAN list, expiry, issuer — and check the SAN, not the CN.
- [ ] **Working** — ACME automation, and the reload that must follow renewal or the new certificate never gets served.
- [ ] **Working** — An internal CA and getting its root trusted across the fleet.
- [ ] **Depth** — mTLS; and pinning, which converts a routine expiry into an outage with no configuration change to blame.

## Remote access & VPN 🔨

- [ ] **Core** — Site-to-site vs client VPN: what each terminates, and where.
- [ ] **Core** — Split vs full tunnel — and the DNS consequence, which is the part that actually breaks.
- [ ] **Core** — Debug *"the VPN won't connect"* **by elimination**: several causes produce one identical symptom, so a check earns its place by what it rules out, not by what it reports.
- [ ] **Working** — IPsec phases (or WireGuard's much smaller surface) and MTU/MSS clamping.
- [ ] **Working** — Name the **identity dependency**: what happens to every remote path the moment the directory is unreachable.
- [ ] **Depth** — A break-glass path that does not depend on the directory — and the reason most designs discover they lack one during the incident.

**Prove it:** [`labs/remote-access-four-causes`](../labs/remote-access-four-causes/)

## Network monitoring & flow analysis 🧭

- [ ] **Core** — Read a flow-log record — five-tuple, bytes, action — and say what it **cannot** tell you. It records that a packet was permitted, not that the application worked.
- [ ] **Core** — The four questions monitoring has to answer: is it reachable, is it fast enough, is it lossy, and since when.
- [ ] **Working** — Latency, loss and jitter as SLIs, measured somewhere that makes the number mean something.
- [ ] **Working** — Capture packets when the flow log is not enough — and filter at capture time, before the disk fills.
- [ ] **Working** — Path-MTU failure by signature: small requests fine, large ones hang, nothing logs an error.
- [ ] **Depth** — Flow-log formats differ per platform; normalise before aggregating or the total is fiction.

## Hybrid & inter-cloud connectivity 🧭

- [ ] **Core** — Why overlapping CIDRs make an interconnect impossible, and why **no central router exists** to arbitrate.
- [ ] **Working** — Tunnel over the internet vs a dedicated circuit: cost, latency and SLA, and which of the three actually drove the decision.
- [ ] **Working** — Hub-and-spoke vs full mesh, and the O(n²) that ends the mesh at about the fifth network.
- [ ] **Working** — DNS across the boundary is **two** configurations, not one — resolution in both directions, failing independently.
- [ ] **Depth** — Egress accounting across a boundary: name where the gigabytes crossed a billing line, before the invoice does.

**Prove it:** [`labs/multi-cloud-cidr-overlap`](../labs/multi-cloud-cidr-overlap/)

## The "can you actually operate it" test

Every **Core** box checked means the network layer transfers: hand you an
unfamiliar platform and you are translating vocabulary, not relearning the
subject. **Working** boxes are where the platforms stop agreeing and you have to
know which one you are standing on. **Depth** boxes are the ones that get reached
for at 3am, and the ones an interviewer uses to find the floor.

Four of the eleven sections point at something runnable. The other seven do not,
and that is worth seeing rather than filling: there is no drill here for rule-set
design, load balancing, or certificate lifecycle, and those are three places
where reading is least sufficient.
