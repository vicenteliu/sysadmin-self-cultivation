---
kind: questions
axis: meta
themes: []
platforms: []
summary: "Questions asked of this repo about where company data lives — an internal file service, and a database that is partly somebody else's."
---
# Questions · Storage and data

> The index, the status legend and the out-of-scope reasoning live one level up in
> [`docs/questions.md`](../questions.md).

| # | Question | Status | Where |
|---|---|---|---|
| 1 | How is an internal file-sharing and storage service designed? | ✅ | The term splits first — [`CONTEXT.md`](../../CONTEXT.md) now separates a **file server** from **suite storage**, because they fail differently. Once the files are in a suite the design question is no longer permissions on directories but *who can see this*, which is [step 07](../../build-out/07-files-and-collaboration.md) and [`permission-sprawl`](../../cross-cutting/labs/permission-sprawl/) |
| 2 | Should that service be self-hosted or bought? | ✅ | **Bought, at this size.** A file server passes none of the three tests in [Where things run](../../the-reference-office.md#on-premises--what-cannot-leave) — it does not act on the building, nothing on this floor needs it when the uplink is down, and it is not the thing you break on purpose. The refusal is recorded there rather than left to be re-litigated |
| 3 | How is a database designed when part of the data belongs to a network service you do not run? | ✅ | [`databases.md`](../../cross-cutting/databases.md#when-half-the-data-belongs-to-somebody-else) — authority is decided per **field**, not per system; a copy carries its age; and sync direction is a one-way decision you make on purpose |
| 4 | Self-hosting one: how do synchronisation and backup actually work? | ✅ | [`databases.md`](../../cross-cutting/databases.md#when-half-the-data-belongs-to-somebody-else) — the recovery objective is not one number. Typed rows are irreplaceable; synchronised rows need a sync that can start from cold, which is the part nobody tests |
