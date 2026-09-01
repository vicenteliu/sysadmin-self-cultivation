---
kind: questions
axis: meta
themes: [networking]
platforms: []
summary: "Questions asked of this repo about networking — five answered, eight open, each open one with a named destination."
---
# Questions · Networking

> The index, the status legend and the out-of-scope reasoning live one level up in
> [`docs/questions.md`](../questions.md).

| # | Question | Status | Where |
|---|---|---|---|
| 1 | What does a current office network look like, architecturally? | ✅ | [`site-network-design.md`](../../cross-cutting/site-network-design.md) |
| 2 | How has office network architecture changed over fifteen years? | ⏳ | the evolution note |
| 3 | How have the network protocols changed over that span? | ⏳ | the evolution note |
| 4 | Firewalls: Palo Alto now — what came before, and what changed? | ⏳ | the evolution note, **as a signature, not a recommendation** — see [Boundaries](../questions.md#boundaries) |
| 5 | What does an F5-class device actually do? | ⏳ | the evolution note; partly answered by the *LB signature* row in [`the-stack/02`](../../the-stack/02-network.md) |
| 6 | How are access points deployed, and by what rule? | ✅ | [`Selection rules`](../../the-reference-office.md#selection-rules) — 🧭 |
| 7 | How have wireless and its protocols changed? | ⏳ | the evolution note |
| 8 | How does a large office's network differ from a small one's? | ✅ | [`site-network-design.md`](../../cross-cutting/site-network-design.md#when-the-size-changes-the-design) |
| 9 | How does a VPN actually land a user on the office network? | ⏳ | a VPN note of its own |
| 10 | What are the basic troubleshooting commands? | ⏳ | a debug-ladder companion — **per rung, not a reference** — see [Boundaries](../questions.md#boundaries) |
| 11 | How do IPv4 and IPv6 coexist now, and how is it configured? | ✅ | [`the-stack/02`](../../the-stack/02-network.md) |
| 12 | What changed about speed? It cannot still be gigabit everywhere. | ✅ current · ⏳ history | [`site-network-design.md`](../../cross-cutting/site-network-design.md) + [`Selection rules`](../../the-reference-office.md#selection-rules); the fifteen-year arc belongs to the evolution note |
| 13 | How is the low-voltage network actually wired? Show a topology. | ⏳ | the **floor**'s near register — MDF/IDF, riser, path to the edge — in [`walkthrough/`](../../walkthrough/README.md); still **not the construction side**, see [Boundaries](../questions.md#boundaries) |

**Five answered, eight open.** The eight are not a wish-list: each has a named
destination, which is what separates this from a list of things that would be nice.
