---
kind: questions
axis: meta
themes: [networking]
platforms: []
summary: "Questions asked of this repo about networking — eleven answered, two open, each open one with a named destination."
---
# Questions · Networking

> The index, the status legend and the out-of-scope reasoning live one level up in
> [`docs/questions.md`](../questions.md).

| # | Question | Status | Where |
|---|---|---|---|
| 1 | What does a current office network look like, architecturally? | ✅ | [`site-network-design.md`](../../cross-cutting/site-network-design.md) |
| 2 | How has office network architecture changed over fifteen years? | ✅ | [`network-evolution.md`](../../cross-cutting/network-evolution.md) — one move explains most of it: the network stopped being the path to your work and became the path to the internet |
| 3 | How have the network protocols changed over that span? | ✅ | [`network-evolution.md`](../../cross-cutting/network-evolution.md) — and the honest answer is that the protocols changed less than what they carry; TLS on 443 for everything is the change that moved the firewall's axis |
| 4 | Firewalls: Palo Alto now — what came before, and what changed? | ✅ | [`network-evolution.md`](../../cross-cutting/network-evolution.md#the-firewall-the-axis-changed-not-the-throughput) — **as a signature**: the axis moved from port to application and user identity, because TLS on 443 made a port rule a rule about the internet. What it replaced was usually the router that also terminated the WAN link |
| 5 | What does an F5-class device actually do? | ✅ | [`network-evolution.md`](../../cross-cutting/network-evolution.md#the-load-balancer-and-why-you-meet-fewer-of-them) — terminates TLS, spreads load, and **holds the application logic that has nowhere else to live**, which is the part that makes it load-bearing. Plus the *LB signature* row in [`the-stack/02`](../../the-stack/02-network.md) |
| 6 | How are access points deployed, and by what rule? | ✅ | [`Selection rules`](../../the-reference-office.md#selection-rules) — 🧭 |
| 7 | How have wireless and its protocols changed? | ✅ 🧭 | [`network-evolution.md`](../../cross-cutting/network-evolution.md#wireless-) — capacity per square metre rose, clients-per-radio barely moved. Marked 🧭 there, consistently with [`site-network-design.md`](../../cross-cutting/site-network-design.md#honest-boundaries) |
| 8 | How does a large office's network differ from a small one's? | ✅ | [`site-network-design.md`](../../cross-cutting/site-network-design.md#when-the-size-changes-the-design) |
| 9 | How does a VPN actually land a user on the office network? | ✅ | [`vpn-and-remote-access.md`](../../cross-cutting/vpn-and-remote-access.md) — **narrowed to the decisions, not the mechanism**: a VPN does not put you on the network, it gives you an address on a segment and a set of routes. Five decisions, and the one that breaks is DNS rather than routing |
| 10 | What are the basic troubleshooting commands? | ⏳ | a debug-ladder companion — **per rung, not a reference** — see [Boundaries](../questions.md#boundaries) |
| 11 | How do IPv4 and IPv6 coexist now, and how is it configured? | ✅ | [`the-stack/02`](../../the-stack/02-network.md) |
| 12 | What changed about speed? It cannot still be gigabit everywhere. | ✅ | current in [`site-network-design.md`](../../cross-cutting/site-network-design.md); history in [`network-evolution.md`](../../cross-cutting/network-evolution.md#speed-which-did-not-increase-where-people-expect) — the money moved **up and sideways**, into the uplink and the radios, and the desk is the one tier that never needed it |
| 13 | How is the low-voltage network actually wired? Show a topology. | ⏳ | the **floor**'s near register — MDF/IDF, riser, path to the edge — in [`walkthrough/`](../../walkthrough/README.md); still **not the construction side**, see [Boundaries](../questions.md#boundaries) |

**Five answered, eight open.** The eight are not a wish-list: each has a named
destination, which is what separates this from a list of things that would be nice.
