# 11 · Assets and tickets — the record that starts at device #1

> ⚒️ hands-on (ServiceNow, ~5 years; asset reconciliation and audit automation)
> **Before:** 03 identity · 04 devices. **After:** 13 the help desk · 14 compliance evidence · 15 JML

The number in the title is a lie about time and honest about dependency. This
step is *placed* eleventh because it needs identity and devices to exist — but it
has to **start at the first device**, not at the hundredth. An inventory
assembled afterwards is not an inventory; it is a reconstruction, and everyone
who has attempted one knows it never finishes.

## What this step produces

- A decision, written down, about **which system is authoritative for what**:
  purchasing owns *who paid for it and who it belongs to*; the endpoint management
  tool owns *what state it is in*. Neither owns both.
- A **unique key** for a device that does not change over its life.
- A reconciliation that runs on a schedule and produces a diff — the diff is the
  work product, not the inventory.
- A ticket queue with categories that map to something you would actually report on.
- A disposal path that ends in evidence, not in a cupboard.

## Questions to ask first

- **What is the unique key — serial, asset tag, or hostname?** Hostname is the
  intuitive answer and the wrong one: it changes on re-image, on re-assignment, and
  on a naming-convention change. Serial survives all three.
- **Who owns the record when a device moves between people?** If the answer is
  "we update it in the ticket", the record is already drifting.
- **When two sources disagree, which one wins?** Answer this now, in writing. It is
  a five-minute decision before there is data and a political one after.
- **What proves a disk was wiped at disposal?** If the answer is "we wiped it", you
  have no answer.
- **What ticket categories would you defend in a report?** Pick the few you would
  actually act on; a taxonomy with forty leaves gets filled in at random.

## 2015 → today

| | 2015 | today |
|---|---|---|
| Inventory source | a spreadsheet, typed by hand | the endpoint tool reports state continuously |
| Ownership source | purchase orders, in a drawer | procurement system, ideally with an API |
| The actual job | *collecting* the data | **reconciling** two sources that both claim to be right |
| Audit posture | assemble evidence when asked | evidence accrues continuously, or it does not exist |
| Failure mode | the sheet is stale | the sheet is *live and still wrong*, which is harder to notice |

**How much of that is AI: some, and it is worth being precise about which part.**
Continuous state reporting is SaaS-ification and agent tooling — it did not wait on
a model. What AI genuinely helps with is the diff: given two records that disagree,
proposing *why* (re-imaged and re-enrolled? sold and not retired? duplicate serial
from a warranty replacement?). That is hypothesis generation over messy data, which
is what the current generation is actually good at.

It should not close the ticket. The same 2026 survey that shows sysadmins adopting
AI for advisory work shows them refusing it authority — roughly half will let it
assess and schedule, while the share willing to let it decide or override policy
sits near a tenth. Asset reconciliation belongs on the advisory side of that line:
let it explain the discrepancy, let a person decide which record is true.

## Read deeper

- [`cross-cutting/itsm-and-assets.md`](../cross-cutting/itsm-and-assets.md) — the
  four things ITSM tracks, the inventory that keeps you honest, access governance
- [`cross-cutting/identity-iam.md`](../cross-cutting/identity-iam.md) — because a
  device record without an owner identity is half a record
- [`endpoint/`](../endpoint/) — where the state data comes from

## Do it

- [`toolbox/user-lifecycle/`](../toolbox/user-lifecycle/) — the identity half of the
  same reconciliation, runnable, dry-run by default
- [`toolbox/baseline-check/`](../toolbox/baseline-check/) and
  [`toolbox/patch-report/`](../toolbox/patch-report/) — two of the state sources this
  step has to reconcile against ownership

- [`cross-cutting/labs/asset-reconciliation/`](../cross-cutting/labs/asset-reconciliation/)
  — both systems report 97 devices, 97 devices exist, and three records are wrong.
  What the join key costs you, and why the residue it leaves is the work product.

## Getting it backwards

**Starting the inventory once it matters.** It begins to matter at the first audit,
the first insurance question, or the first departure where a laptop does not come
back — and all three arrive after the point where reconstruction is possible. The
cost of starting at device #1 is a column in a form. The cost of starting at #100
is a person for a month, and the result is still wrong.

**Letting the ticket system be the asset system.** It is right there and it has
fields. But a ticket is an event and an asset is a state, and a system optimised
for closing events will happily let the state rot — the queue looks healthy while
the record decays.

**Keying on hostname.** Discovered a year later, when the re-imaged machines appear
as new devices, the old records never retire, and the count is now higher than the
number of laptops that exist. Nothing about this is recoverable without touching
every device.
