---
kind: route-step
axis: build-out
themes: [storage-backup]
platforms: []
marker: "🔨"
summary: "🔨 hands-on — backup targets, RAID rebuild windows, snapshot hygiene, restore practice Before: 06 tenant · 07 files."
---
# 09 · Backup — and the restore drill

> 🔨 hands-on — backup targets, RAID rebuild windows, snapshot hygiene, restore practice
> **Before:** 06 tenant · 07 files. **After:** 14 compliance evidence

The title is the argument. **A backup that has never been restored is a belief, not
a control**, and the industry's most expensive lesson is that the two feel identical
right up to the moment they do not.

Its position after 06 and 07 is not ceremonial: you cannot decide what to protect
until you know where state actually lives, and in a SaaS-first office that answer is
surprising — it is spread across a tenant, a suite, a code host, and two or three
line-of-business SaaS products nobody listed.

## What this step produces

- An inventory of **where state actually lives**, including the SaaS products whose
  data you have never thought of as yours to protect.
- A recovery objective per category — how much time you can lose, how long you can
  be down — decided by the business and written down.
- Backups that leave the platform they protect. Retention inside a suite is not
  backup; a mistake or a compromise that reaches the tenant reaches its recycle bin.
- 🔴 **A restore, performed, on a date, by a person, with the result recorded.** This
  is the deliverable. Everything above it is setup.

## Questions to ask first

- **List every place company state lives.** The tenant and the file suite are obvious.
  The code host, the ticket system, the design tool, the CRM, the payroll platform
  are not — and several of them have a shared-responsibility model that puts your
  data squarely on your side of the line.
- **How much work can this company afford to lose?** An hour, a day, a week? The
  answer differs per system, and asking it is a business conversation, not an IT one.
- **Does the backup leave the blast radius?** A copy inside the same account, under
  the same credentials, protects against deletion and nothing else.
- **Who can delete the backups, and is that a different person from who can delete
  the data?**
- **When was the last successful restore, and who did it?** If the answer is a date
  with no name attached, it was a job status, not a restore.
- **What does the SOC 2 customer need to see?** Usually: a policy, an objective, and
  evidence the drill happened. All three are cheap if planned, expensive if
  retrofitted.

## 2015 → today

| | 2015 | today |
|---|---|---|
| What you protected | servers and a file share you owned end to end | data inside services you do not run |
| The mechanism | agents, tapes, a window overnight | APIs, and a third-party tool that holds credentials to your suite |
| The illusion | "the RAID is fine" | "it's in the cloud" |
| What is actually yours | everything | **your data — the vendor's shared-responsibility page says so, and almost nobody reads it** |
| The failure that still bites | untested restore | untested restore |

**How much of that is AI: none.** This step has not changed because of AI in any way
worth reporting, and reaching for one here would be the clearest sign the AI column
had become decoration.

The unglamorous truth is that the last row of that table has not moved in a decade:
the failure mode is still that nobody tried it.

## Read deeper

- [`the-stack/04-storage.md`](../the-stack/04-storage.md) — block, file, object, and
  backup as a storage-layer concern
- [`cross-cutting/databases.md`](../cross-cutting/databases.md) — backup and PITR
  where the data is a database rather than a file
- [`cross-cutting/saas-admin.md`](../cross-cutting/saas-admin.md) — the
  shared-responsibility boundary in a SaaS estate

## Do it

- [`the-stack/labs/04-backup-not-snapshot/`](../the-stack/labs/04-backup-not-snapshot/)
  — runnable, and the single most useful thing in this step: replication is not
  backup, demonstrated rather than asserted
- [`toolbox/backup-restore-drill/`](../toolbox/backup-restore-drill/) — the drill,
  made repeatable, which is how it survives contact with a calendar
- [`toolbox/snapshot-audit/`](../toolbox/snapshot-audit/) — snapshot hygiene across
  hypervisors, for the local things that did not leave the building

## Getting it backwards

**Treating the suite's recycle bin as backup.** It is retention, it is bounded, and
it lives inside the account you are protecting against. The scenario it fails is the
one you actually fear: an account compromise or a mistaken admin action that reaches
everything at once.

**Never restoring.** The jobs are green for two years. Then a restore is needed and
the archive is incomplete, or the credentials expired eight months ago, or the
restore takes four days and the recovery objective said four hours. Every one of
these is discoverable in an afternoon, in advance, at zero cost.

**Forgetting the SaaS products nobody listed.** The design tool with every source
file. The code host with every repository. Both have export APIs. Neither is backed
up by anyone unless somebody decided to.

**Backups reachable with the same credentials as production.** Convenient, and it
means one compromised admin session ends both.
