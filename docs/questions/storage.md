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
| 1 | How is an internal file-sharing and storage service designed? | ⏳ | [step 07](../../build-out/07-files-and-collaboration.md) holds one table cell — *file server to suite is SaaS-ification* — and no design. **The term splits first**: a self-hosted *file server* and a suite's *storage* are different questions |
| 2 | Should that service be self-hosted or bought? | ⏳ | the honest answer at a hundred people may be *neither, buy it* — and if so this is where that answer lives, not in a parameter table |
| 3 | How is a database designed when part of the data belongs to a network service you do not run? | ⏳ | [`cross-cutting/databases.md`](../../cross-cutting/databases.md) — mixed footing, and the boundary matters more than the design |
| 4 | Self-hosting one: how do synchronisation and backup actually work? | ⏳ | [`databases.md`](../../cross-cutting/databases.md) plus [step 09](../../build-out/09-backup-and-the-restore-drill.md), whose *backups must leave the platform they protect* is the load-bearing sentence |
