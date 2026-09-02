---
kind: note
axis: the-stack
themes: [networking]
platforms: [aws, azure, gcp, oci]
marker: "mixed"
summary: "Chapter 01 ended on a promise: the real lock-in lives up here."
---
# 02 — The Network Layer

> 🌐 **Languages:** English (default) · [中文](../docs/zh/the-stack/02-network.md)

> Chapter 01 ended on a promise: the real lock-in lives up here. The network layer
> is where the seven platforms differ most, where the money quietly leaks, and
> where "it's always DNS" was coined by someone who had already checked DNS twice.

The physical layer gave us buildings full of hardware in failure domains. This
layer's job is to let all of it talk — safely, quickly, and (on the clouds) *as if*
the sharing weren't happening. Networking is also where a self-hosting background
pays off most on the way up the stack: every cloud construct below is a renamed
thing you've already crimped a cable for.

## What this layer does (everywhere, always)

- **Address** — give every workload a place: IP plans, subnets, DNS names.
- **Connect** — move packets between workloads, buildings, sites, and the internet:
  switching, routing, peering, tunnels.
- **Isolate** — keep tenants, tiers, and teams apart: VLANs, VRFs, virtual
  networks, segmentation.
- **Filter** — decide which packets are allowed: firewalls, security groups, ACLs.
- **Distribute** — spread load and survive failures: load balancers, anycast, DNS.
- **Observe** — see what actually happened: flow logs, packet captures, counters.

> **Where this chapter stops, on purpose.** Every verb above is stated at the
> altitude of a decision somebody has to make and then own. Underneath it sits a
> layer this repository does not cover anywhere — how a host actually resolves a
> neighbour on the wire, what an ARP cache holds and when an entry goes stale,
> what answers a name when there is no DNS server to ask, how a frame finds its
> way from one switch port to another.
>
> That absence is a boundary rather than an oversight, and it is the same
> reasoning as the Boundaries table in [`build-out/GAPS.md`](../build-out/GAPS.md).
> This material stays useful exactly as long as it stays narrow, and the narrow
> thing it does is decisions and their consequences. Protocol mechanics are a
> different altitude with a different reader, and carrying both would cost both.
>
> It is worth naming rather than leaving for someone to discover. **Being able to
> run a network and being able to say what the wire is doing are different
> abilities, and this repository only trains the first one.**

## Two concepts before the seven

### Underlay vs. overlay

Everything on this layer makes sense once you split it into two planes:

```mermaid
flowchart TB
  subgraph OV["Overlay — virtual networks, the ones YOU configure"]
    v1["VPC / VNet / VCN / tenant network / VLAN"]
    v2["subnets · route tables · security groups"]
  end
  subgraph UL["Underlay — the physical fabric moving the actual packets"]
    p1["Clos / leaf-spine fabric · TOR switches · routers"]
    p2["encapsulation carries overlay traffic across it (VXLAN and friends)"]
  end
  OV -->|"encapsulated onto"| UL
```

- **Self-host:** you build *both* planes. The overlay might just be VLANs on the
  underlay — or EVPN-VXLAN if the shop is modern.
- **The clouds:** the provider owns the underlay entirely; you live in the overlay
  and configure it through an API. That's what "software-defined networking" means
  operationally: **your network is now rows in a provider database**, materialized
  by their fabric.
- **OpenStack / NSX:** you run the SDN machinery yourself — the overlay is yours
  *and* the underlay is yours, which is both the appeal and the bill.

### Dual-stack, because the migration never happened

IPv6 has been arriving for twenty-five years, and the operationally important fact
about it is **not** how the addresses are written. It is that **the migration people
kept predicting did not occur, and dual-stack stopped being a transition state.** It
is the destination. Estates that planned a cutover are still waiting; estates that
planned to run both have been running both for a decade.

Three things follow, and they are the parts that show up in tickets:

- **You now have two paths to every destination and they fail independently.** A name
  with both an `A` and an `AAAA` record hands the client a choice, and clients prefer
  IPv6. If the v6 path is broken while the v4 path is fine, the symptom is *"the site
  is slow"* or *"it works for some people"* — the client tries v6, waits, and falls
  back. Happy Eyeballs hides this from users and from you, which is exactly why it
  takes so long to find. **`AAAA` is published, therefore `AAAA` must work** is the
  discipline; publishing it optimistically is the common self-inflicted outage.
- **There is no NAT to hide behind, and that is a filtering change, not an addressing
  one.** Every host having a globally routable address means the firewall is doing
  work that IPv4's address shortage was doing accidentally. An estate that opened v6
  without writing v6 rules has a second, unfiltered internet path — and its v4 rule
  set looks complete.
- **Address assignment is a different model, not a different notation.** SLAAC, DHCPv6
  and the interaction of the two are where the operational surprises live, alongside
  privacy addresses that change what your logs mean. *Which of your systems records
  the address it saw, and can you still map it to a person tomorrow?*

The clouds diverge more here than they do on almost any other dimension in the table
below — dual-stack is not uniformly available, and where it is, the mechanism differs.
Check per platform rather than carrying an assumption across.

## Seven ways to build it

**Self-hosted 🔨** — VLANs for segmentation, a firewall pair at the edge,
DNS/DHCP you run yourself (BIND and friends), HAProxy/keepalived or an appliance
for load balancing, site-to-site VPN or leased lines between locations. The
failure modes are physical (a looped cable can still ruin a floor) and the limits
are honest: what the boxes can do, you can do.

**vSphere 🔨** — standard and distributed vSwitches bridge VMs onto the physical
VLANs; the network team's world and the VM team's world meet at a port group.
**NSX 🧭** adds a full overlay (segments, distributed firewall, virtual routers) on
top — vSphere shops adopt it exactly when VLAN sprawl and east-west filtering
outgrow the physical network.

**OpenStack 🧭** — Neutron provides tenant networks (typically VXLAN overlays),
routers, floating IPs, and security groups. Powerful and honest about its plumbing
— which means you *will* meet the plumbing: Neutron is consistently the component
operators name first when asked what pages them.

**AWS 🧭** — the **VPC**: a regional network you carve into **AZ-scoped subnets**.
Route tables per subnet, an Internet Gateway for north-south, NAT Gateways for
private egress, **security groups (stateful, instance-attached)** plus **NACLs
(stateless, subnet-level)**. The mental model is a classic three-tier DC diagram —
deliberately so.

**Azure 🧭** — the **VNet**: regional, with subnets that span zones. **NSGs**
attach at subnet *or* NIC; **User-Defined Routes** override system routing;
Private Endpoints thread SaaS into your address space. Azure networking loves
explicitness — more knobs than AWS at the same layer, which cuts both ways.

**GCP 🧭** — the structural outlier: the **VPC is global**, subnets are
**regional**, and firewall rules live at the VPC level targeting tags or service
accounts. One network can span the planet with no peering between regions —
elegant, and a genuinely different topology to plan for:

```mermaid
flowchart LR
  subgraph AWS["AWS — network is regional"]
    subgraph vpc1["VPC us-east-1"]
      s1["subnet in AZ-a"]
      s2["subnet in AZ-b"]
    end
    subgraph vpc2["VPC eu-west-1"]
      s3["subnet in AZ-a"]
    end
    vpc1 <-->|"peering / TGW — your job"| vpc2
  end
  subgraph GCP["GCP — network is global"]
    subgraph vpcg["one VPC"]
      g1["subnet us-east1"]
      g2["subnet europe-west1"]
      g1 <-->|"just routes"| g2
    end
  end
```

**OCI 🧭** — the **VCN**: regional, with (preferably) regional subnets; **security
lists** at the subnet *and* **NSGs** per resource — two overlapping filtering
mechanisms, pick a lane and standardize. Interconnect and egress pricing are
deliberately aggressive; OCI courts exactly the workloads the egress meter hurts.

## The comparison table

| Dimension | Self-host 🔨 | vSphere (+NSX) | OpenStack 🧭 | AWS 🧭 | Azure 🧭 | GCP 🧭 | OCI 🧭 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Virtual network** | VLANs / EVPN-VXLAN | port groups / NSX segments | Neutron tenant nets | VPC (regional) | VNet (regional) | **VPC (global)** | VCN (regional) |
| **Subnet scope** | per-VLAN, your design | per port group | per tenant net | **per AZ** | spans zones | **regional** | regional (pref.) |
| **Stateful filter** | firewall / iptables | NSX DFW | security groups | security groups | NSGs | firewall rules (VPC-level) | NSGs |
| **Second filter layer** | ACLs on switches | — | — | NACLs (stateless) | ASGs group NSGs | hierarchical policies | security lists (subnet) |
| **North-south** | edge firewall pair | edge / NSX gateway | Neutron router + floating IP | IGW / NAT GW | LB / NAT GW | Cloud NAT / global LB | IGW / NAT GW |
| **Cross-site** | VPN / leased line | same + NSX federation | VPN-as-a-service | Direct Connect | ExpressRoute | Interconnect | FastConnect |
| **LB signature** | HAProxy / keepalived / F5 | NSX LB | Octavia | ALB / NLB | Azure LB / App GW / Front Door | **global anycast LB** | LB / NLB |
| **IPv6** | dual-stack, yours to plan | dual-stack on port groups | dual-stack per tenant net | dual-stack VPC, egress-only IGW | dual-stack VNet | dual-stack, external/internal | dual-stack VCN |
| **DNS** | BIND you run 🔨 | — (yours) | Designate | Route 53 | Azure DNS / private zones | Cloud DNS | OCI DNS |

## Choosing — and the egress meter

Most layer-2/3 capability differences between the four clouds are marginal. The
selection-grade differences are these:

- **Topology model.** GCP's global VPC vs. everyone else's regional networks
  changes multi-region design fundamentally — what needs peering and transit
  elsewhere is "just routes" there.
- **The egress meter — the actual lock-in.** Traffic *in* is free; traffic *out*
  is billed; on AWS, traffic **between AZs** is billed too, and NAT Gateways add a
  per-GB processing tax on top. Data gravity isn't a metaphor — it's a per-gigabyte
  exit fee on ever leaving:

```mermaid
flowchart LR
  inet["Internet"] -->|"ingress — free"| vpc["Your cloud network"]
  vpc -->|"egress — billed per GB"| inet
  vpc -->|"inter-AZ — billed (AWS)"| vpc
  vpc -->|"NAT gateway — per-GB processing tax"| inet
  vpc -->|"to another cloud or your DC — egress, billed"| dc["Your data center"]
  dc -->|"your cost model: ports + transit, flat-ish"| dc
```

  Self-host inverts the model: you pay for **ports and transit capacity**, roughly
  flat, however much you move. This single difference decides more hybrid
  architectures than any feature list — and it's OCI's chosen battleground
  (aggressively cheaper egress) and the reason repatriation stories are almost
  always bandwidth-heavy workloads.
- **Compliance topology.** Private connectivity to SaaS (private endpoints),
  forced tunneling through inspection, on-prem interconnect — if your traffic must
  be inspected or must never touch the internet, verify the pattern exists *before*
  choosing.
- **Team, again.** NSX and OpenStack Neutron are SDN systems you operate. Cloud
  VPCs are SDN systems you *consume*. The skills gap between those is real.

## Ops notes — what pages you

- **It's always DNS** — stale records, split-horizon confusion, a TTL somebody set
  to a day, a resolver that answers differently inside and outside the VPC. Check
  DNS *first*, then check it again after you've blamed something else.
- **When it isn't DNS, it's MTU** — overlays steal bytes (VXLAN takes ~50), clouds
  ship non-obvious defaults, and path-MTU discovery dies quietly behind security
  groups that drop ICMP. Symptoms: small requests work, big transfers hang.
- **Stateful vs. stateless bites in one direction** — security groups auto-allow
  return traffic; NACLs and switch ACLs don't. "Request arrives, response
  vanishes" means an ephemeral-port return path someone forgot.
- **Asymmetric routing** — two paths out, one firewall in the middle, conntrack
  drops the half-connection it never saw. Classic in dual-NIC and multi-route-table
  setups on every platform including self-host.
- **Conntrack / connection-table exhaustion** — NAT gateways, LBs, and Linux boxes
  all keep state; all of it has a ceiling; all ceilings are found in production.
- **VPN tunnels flap; BGP sessions don't lie** — monitor the routing session, not
  the ping.

The methodical version — the debug ladder worth internalizing until it's reflex:

```mermaid
flowchart TD
  q["Can't reach it"] --> dns{"Does the name resolve — and to what you think?"}
  dns -->|no| fixdns["DNS: record · TTL · split-horizon · resolver"]
  dns -->|yes| route{"Is there a route — both directions?"}
  route -->|no| fixroute["route tables · peering · gateway · asymmetry"]
  route -->|yes| fw{"Do the filters allow it — both layers, both directions?"}
  fw -->|no| fixfw["SG / NSG / NACL / firewall — remember stateless return paths"]
  fw -->|yes| mtu{"Do small packets work but big ones hang?"}
  mtu -->|yes| fixmtu["MTU / PMTUD — overlay overhead, ICMP blocked"]
  mtu -->|no| deeper["flow logs · packet capture — now you get to look"]
```

## The admin discipline (what to be able to do)

Six things, and the rest is detail: stand up a **three-tier network from code**
on any platform handed to you; explain **stateful vs. stateless** filtering and
show where each platform hides the stateless layer; run the **debug ladder**
above without skipping rungs, and read a **flow log** to prove which rung it was;
write an **IP plan that survives five years** before the first subnet exists —
merging two overlapping `10.0.0.0/16`s later is a project with a name; configure
**split-horizon DNS** deliberately rather than accidentally; and read an **egress
bill** well enough to say where the gigabytes crossed a billing boundary.

The checkable version of all of it — 63 boxes across eleven sections, tiered by
how far each skill travels rather than by platform — is
[`cross-cutting/skills-maps/networking.md`](../cross-cutting/skills-maps/networking.md).

## The AI-assisted ramp (network flavor)

- **Translate from what you own:** *"I know VLANs, BIND, iptables, and enterprise
  firewalls. Map that onto AWS VPC constructs — and be explicit about which layer
  is stateful and which is stateless."*
- **Design review, not design:** have AI draft the three-tier Terraform, then walk
  every rule asking "why is this open?" AI defaults to permissive quick-start
  patterns (0.0.0.0/0 has no business in a security group it wrote for you).
- **Where AI burns you (verify hardest):** it **invents rule syntax and quota
  numbers**; it states **MTU defaults and egress prices from its training years**
  (both change — look up current values, always); it forgets **GCP's global VPC**
  and gives you regional-model advice there; it blurs **security list vs. NSG on
  OCI** and **NSG vs. ASG on Azure**. Anything that filters traffic or costs money
  gets checked against the provider's current docs.

## Honest boundaries

The 🔨 here is the classic enterprise stack: years of hands-on DNS/DHCP/BIND,
VLANs, firewalls, VPNs, and TCP/IP debugging across offices and data centers, with
a CCNP-level routing-and-switching foundation and vSphere networking operated for
real. The 🧭 is two things, and the second was previously left unsaid rather than
claimed. The first is the modern SDN layer: each cloud's VPC specifics, NSX, and
EVPN-VXLAN fabrics are ramped via exactly the method above — solid conceptual
mapping, verified against current docs, no claimed years of daily BGP peering or
NSX production ops. The second is **wireless**: density planning, channel and
power strategy, RF survey practice and access-point selection are mapped and
verified, not designed on a floor and lived with afterwards. It is named here
because the 🔨 list above is deep enough that a reader would otherwise reasonably
fold wireless into it, and the silence would be doing work the evidence does not
support. The design method is written out in
[`cross-cutting/site-network-design.md`](../cross-cutting/site-network-design.md),
marked 🧭 in the same place. The debug ladder, though, is platform-independent and
scar-tissue-tested: it was learned on hardware, and it works identically on
overlays someone else runs.

## Lab (✅ runnable — [`labs/02-first-match-and-longest-prefix/`](labs/02-first-match-and-longest-prefix/))

**Two files, two lookup disciplines, and nothing on the page says which** — zero
network, zero credentials, Python stdlib only, so CI can run it:

```bash
python3 the-stack/labs/02-first-match-and-longest-prefix/lookup_order_drill.py
```

A routing table resolves by **longest prefix** and does not care about order; a
firewall ruleset resolves by **first match** and cares about nothing else. Both are an
ordered list of prefixes on a screen. The drill shuffles each one twenty times — every
routing verdict is identical, eleven of twenty ruleset shuffles change one — then walks
the two mirror errors that follow: promoting a route line to "prioritise" it changes
nothing and reads as a ruled-out theory, and one broad allow at the top silently makes
three rules below it inert, including a deliberate quarantine deny that still shows in
every screenshot and review. Two sabotage flags implement each mistaken model so you
can watch what it would have predicted.

## Guided run (spec)

**This is a [guided run](../CONTEXT.md), not a lab.** It needs a real environment, so nothing here can assert that you did it and CI cannot run it. That is the whole of the distinction and it is not a demotion — a guided run reaches real latency, real error messages and real bills, which no model does.

**Same network, three ways.** One three-tier design (public LB / private app /
isolated data + NAT egress), built three times:

1. **Terraform on AWS**, then **Terraform on GCP** — same topology, and write down
   every place the global-VPC model changed your code.
2. **DevStack (OpenStack)** locally — build the same tenant network with Neutron
   and meet the plumbing the clouds hide.
3. **The drill:** break each one four ways (kill a route, block a return path,
   poison DNS, clamp MTU) and fix it using only the debug ladder — no guessing.

## Where each platform keeps this layer

This chapter compares; the platform folders operate. For any one of the seven, the
structure is in its `architecture.md` and the day-2 work in its `operations.md`:
[AWS](../platforms/aws/architecture.md) · [Azure](../platforms/azure/architecture.md) · [GCP](../platforms/gcp/architecture.md) · [OCI](../platforms/oci/architecture.md) · [vSphere](../platforms/vsphere/architecture.md) · [OpenStack](../platforms/openstack/architecture.md) · [self-host](../platforms/self-host/architecture.md) — and the same seven under [`platforms/`](../platforms/) for the operations
and automation companions.

## The chapter on one screen

```mermaid
mindmap
  root((Network layer))
    Two planes
      underlay - the fabric
      overlay - what you configure
    Seven ways
      Self-host 🔨 both planes yours
      vSphere 🔨 port groups meet VLANs
      NSX 🧭 SDN you operate
      OpenStack 🧭 Neutron pages you
      AWS 🧭 regional VPC, AZ subnets
      Azure 🧭 explicit knobs everywhere
      GCP 🧭 global VPC outlier
      OCI 🧭 two filter layers, cheap egress
    The money
      ingress free
      egress billed
      inter-AZ billed
      NAT taxed
      self-host pays for ports
    Debug ladder
      DNS first
      then routes
      then filters both directions
      then MTU
      then flow logs
```
