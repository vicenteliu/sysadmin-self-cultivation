---
kind: route-step
axis: build-out
themes: [networking]
platforms: []
marker: "🔨"
summary: "🔨 hands-on — switching, DNS/DHCP, the boot path, and the fault-isolation habits Before: 01 uplink · 02 the building · 03 identity · 04 devices."
---
# 05 · Network — VLANs, wireless, guest, printing, door access

> 🔨 hands-on — switching, DNS/DHCP, the boot path, and the fault-isolation habits
> **Before:** 01 uplink · 02 the building · 03 identity · 04 devices. **After:** 07 files · 10 remote access · 12 meeting rooms

This is where the forced-hybrid constraint from the scenario becomes concrete.
Almost everything left the building — but **door access, badge printing and the lab
gear did not**, and those are exactly the things that need a stable local network
with sane segmentation. An office network today exists mostly to carry people to
the internet safely, and to keep a small number of stubborn devices alive.

## What this step produces

- A segmentation plan with a **reason per segment**, not a segment per device type.
- An address plan that will not collide with the VPN, the branch, or a cloud VPC —
  checked, not assumed.
- Wireless designed for **density**, not coverage; a 100-person floor is a capacity
  problem, and one AP per large room is a 2015 answer.
- A guest network that is genuinely isolated and can be shown to be.
- DNS and DHCP with an owner, and a documented answer to "what resolves what".

## Questions to ask first

- **What actually needs to be on a separate segment, and why?** The honest list for
  this office is short: staff, guest, and the things that cannot be trusted or
  patched (door controller, print, lab). Segmenting further because it feels tidy
  produces rules nobody can explain in a year.
- **What address space, and does it collide with anything you will ever tunnel to?**
  Overlapping RFC1918 ranges are the classic self-inflicted wound: it works until
  the day a VPN or a cloud peering is added, and then it cannot be fixed without
  renumbering a live office.
- **How many people in the largest room, all on video at once?** That is the wireless
  sizing question. Coverage maps answer a question nobody has.
- **Does authentication to the network use the directory?** If yes, this depends on
  03 and gives you a real access story. If no, you have a shared key that will be on
  someone's phone forever.
- **Is guest isolation provable?** Not "configured" — demonstrable, because a customer
  asking about SOC 2 will ask this specific thing.
- **What is the door controller's failure mode?** Some fail locked. Ask before you
  find out.

## 2015 → today

| | 2015 | today |
|---|---|---|
| What the LAN carries | file servers, print, apps, and the internet | the internet — plus a short list of things that cannot leave |
| Wireless | coverage; wired was the serious path | **the primary access layer**, sized for density |
| Segmentation driver | departments and servers | trust level: staff / guest / unpatchable |
| Network authentication | a key, or nothing | tied to the directory, which is why this depends on 03 |
| Where the failure hurts | one service | everyone, immediately — the LAN is now the on-ramp |

**How much of that is AI: none for design; some for diagnosis.** Segmentation and
addressing are engineering decisions with no model in the loop. Vendor "AI-driven"
wireless optimisation is real but is mostly the same RF heuristics with a new
label — be specific about what it is doing before crediting it.

The honest AI use here is the same as everywhere else in this series: given
symptoms, propose causes. That is worth having on a bad day, and it is not the
same as letting it change a VLAN.

## Read deeper

- [`the-stack/02-network.md`](../the-stack/02-network.md) — the network layer across
  seven platforms
- [`cross-cutting/identity-iam.md`](../cross-cutting/identity-iam.md) — because
  network authentication is an identity decision wearing a networking hat
- [`the-stack/07-security.md`](../the-stack/07-security.md) — segmentation as one
  layer of defence-in-depth, not as the whole of it

## Do it

- [`toolbox/cidr-check/`](../toolbox/cidr-check/) — check the address plan for
  overlaps **before** it is deployed. This is the cheapest tool in the repo relative
  to what it prevents.
- [`cross-cutting/labs/multi-cloud-cidr-overlap/`](../cross-cutting/labs/multi-cloud-cidr-overlap/)
  — the same mistake at a larger scale, made tangible.

## Getting it backwards

**Picking addresses that feel free.** `192.168.1.0/24` works perfectly until the
day it has to be reached from somewhere that also chose it. Renumbering a live
office is a weekend nobody enjoys and a week of stragglers.

**Designing wireless for coverage.** The survey looks good, the office is fine in
week one with forty people in it, and it collapses when the all-hands puts eighty
in one room on video.

**Flat, because segmentation can be added later.** It cannot, cheaply — by the time
it matters, everything is addressed and everything assumes reachability. The
unpatchable device that was going to be isolated "soon" is sitting on the staff
network with a default password and a web interface.
