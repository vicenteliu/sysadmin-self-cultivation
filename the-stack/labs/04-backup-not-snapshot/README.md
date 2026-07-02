# Lab 04 — Backup is not snapshot (prove it in your own hands)

**Goal:** make the central lesson of [chapter 04](../../04-storage.md) tangible —
**replication and snapshots faithfully copy destruction; only an independent,
point-in-time backup recovers you, and only up to its RPO.** You'll run a drill
that seeds a database, replicates it, backs it up once, writes more data, then
`DROP`s the table — and watch exactly what survives.

**You'll practice:** the difference between replication and backup, restoring for
real (not just "a backup exists"), and measuring **RTO** (how long recovery took)
and **RPO** (how much data the backup couldn't give back) — the two numbers every
backup conversation is actually about.

## Why this lab is pure-local

No cloud, no credentials, no cost, no external packages — just Python 3.8+ and its
built-in `sqlite3`. Three directories stand in for three **failure domains**:

| Directory | Simulates | In the real world |
| --- | --- | --- |
| `primary/` | the live database | your block volume (chapter 04) |
| `replica/` | a continuously-synced copy | RAID / a sync replica / a same-volume snapshot |
| `vault/` | independent point-in-time copies | the off-site, separate-account backup 3-2-1 is about |

Directories are an honest stand-in for *separation*, not for media or geography —
the point is the **independence** of the vault from the primary's fate, which is
the property that does the saving.

## Run it

```bash
python3 backup_drill.py
```

That's it — no install. Exit code `0` means every assertion about the lesson held,
so it doubles as a CI check. Useful flags:

```bash
python3 backup_drill.py --seed-rows 5000 --post-backup-rows 500  # bigger RPO gap
python3 backup_drill.py --keep                                   # leave the workspace to poke at
```

## What you'll see

The drill narrates eight steps and ends on three checked lessons:

```
=== 6. Assess the damage — what actually survived? ===
  ✓ primary is destroyed (table gone) — as expected
  ✓ replica is ALSO destroyed — replication is not backup (LESSON 1)
  ✓ the vault backup is untouched — independence is what saved it (LESSON 2)
...
=== 8. Count the RPO — what the backup could not give back ===
  rows LOST (RPO)  : 250   ← everything written after the last backup
  ✓ RPO cost exactly the 250 post-backup rows — RPO is real (LESSON 3)
```

## Verify (don't take the script's word for it)

Run with `--keep` and inspect the four failure domains yourself:

```bash
python3 backup_drill.py --keep
# the primary and the replica both lost the table:
sqlite3 drill-workspace/primary/app.db  "SELECT count(*) FROM widgets;"   # error: no such table
sqlite3 drill-workspace/replica/app.db  "SELECT count(*) FROM widgets;"   # error: no such table
# only the vault backup still has the data:
sqlite3 drill-workspace/vault/backup-0001.db "SELECT count(*) FROM widgets;"   # a real number
```

(If you don't have the `sqlite3` CLI, the same queries work from Python — the
script uses only the stdlib.) Seeing the identical "no such table" on **both**
primary and replica, while the vault answers with a row count, is the whole lesson
in three commands.

## The point

- **Replication ≠ backup.** The replica mirrored the `DROP` instantly and
  faithfully — exactly what a sync replica or a same-volume snapshot does with a
  `DROP TABLE`, `rm -rf`, or ransomware. It survives *hardware* failure, not
  *logical* destruction.
- **Independence is the property that saves you.** The vault copy recovered the
  data only because the disaster couldn't reach it.
- **RPO and RTO are numbers, not adjectives.** This drill hands you both: a
  measured restore time, and an exact count of the rows written after the last
  backup that no restore could return. "How much can we lose, and how long to get
  back?" now has a concrete answer you produced.
- **A backup you haven't restored is a hope.** You just restored one.

## Teardown

Nothing persistent is created — the workspace is deleted automatically unless you
pass `--keep`. To remove a kept workspace:

```bash
rm -rf drill-workspace
```
