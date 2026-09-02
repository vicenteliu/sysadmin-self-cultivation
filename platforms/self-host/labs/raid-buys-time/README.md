---
kind: lab
axis: platforms
themes: [virtualization]
platforms: [self-host]
marker: "🔨"
summary: "RAID buys you the time to swap, and the rebuild is when you spend it: a mirror replicates an rm, a 20 TB disk is a 37-hour bet, at fleet scale the second failure inside that window is an annual event, on today's sizes RAID 5's second failure is a read error, and RAID 6 bounds it by a thousand."
---
# Lab — RAID buys you time, and the rebuild is when you spend it

> 🌐 **Languages:** English (default) · [中文](../../../../docs/zh/platforms/self-host/labs/raid-buys-time/README.md)

> **Inputs:** none — the vendor numbers sit at the top of the file · **Outputs:** rebuild
> windows, arrays lost per year, and the odds of a read error mid-rebuild · **Risk:** none
> — no disks, no `mdadm`, no root · **Root:** not needed

**Goal:** put arithmetic under one bullet of the [operations note](../../operations.md):
disk failures are constant at fleet scale, spares are consumables with a stocked shelf and
a swap procedure, *RAID buys you the time to swap; a second failure during a rebuild is
the nightmare RAID levels exist to bound.* Every clause in that sentence is a number, and
this drill computes each one from the disk vendors' own spec sheets — an annual failure
rate, a rebuild throughput, an unrecoverable-read-error rate.

**You'll practise:** reading a RAID level as a promise about the next few hours rather
than about the data, sizing the window by disk size *and* swap lead time, and choosing
between RAID 5 and RAID 6 with the read-error arithmetic in front of you instead of the
capacity arithmetic.

## Why this lab is pure-local

The [arc's third run](../README.md) builds a real `md0`, fails a member with `mdadm`, reads
the canary, deletes it and reads again — do that; the canary gone on both disks is the
older truth from [`the-stack/04`](../../../../the-stack/04-storage.md), felt. But the
bullet in the operations note is about *fleet* scale and the *window*, and no laptop has
ten thousand arrays or a year. Here the mirror is two dictionaries, the rebuild is a
division, and the window is a probability. No disks, no root, no `pip install`. Python
stdlib, and CI runs it.

## Run it

```bash
python3 platforms/self-host/labs/raid-buys-time/raid_drill.py
```

Exit code `0` means every assertion about the lesson held.

## What you'll see

1. **A mirror survives a dead disk and replicates an `rm`.** Fail a member: the canary
   reads. Delete it on a healthy mirror: zero copies left, because RAID's whole job is
   that a write reaches every member — and an `rm` is a write.

2. **The window scales with the disk.** 2 TB at 150 MB/s rebuilds in 3.7 hours; 20 TB
   in **37**. A ten-times bigger disk is a ten-times longer bet on the survivors.

3. **Fleet scale makes it an annual event.** Ten thousand six-disk arrays at 2% AFR is
   1,200 rebuilds a year. With a hot spare, **0.51** arrays a year lose data to a second
   failure inside the window; with a stocked shelf, 0.56; with disks on order, **1.49**.
   The swap lead time is the larger half of the window.

4. **On today's sizes, RAID 5's second failure is a read error.** A 20 TB rebuild reads
   a hundred terabytes off the survivors. At the consumer spec of one unrecoverable
   error per 10¹⁴ bits, the chance of hitting one is **100%**; at the enterprise 10¹⁵, a
   coin flip. Even 2 TB disks are 55% at the consumer rate.

5. **RAID 6 bounds it by a thousand.** Same fleet, same lead time: 1.49 arrays a year
   on RAID 5, 0.0015 on RAID 6. That ratio is what the level is for.

## Verify (don't take the script's word for it)

```bash
python3 raid_drill.py --break-it raid-is-backup      # exit 1
python3 raid_drill.py --break-it rebuild-is-instant  # exit 1
```

`raid-is-backup` makes an `rm` touch only the member you were looking at — the *other
copy still has it* instinct — and two assertions break, both in step one.
`rebuild-is-instant` makes a swap cost nothing: the window is the lead time alone, the
rebuild reads no bits, and eight assertions break, because every number in steps two to
five was the rebuild.

Then argue with the inputs. The numbers sit at the top of the file:

```bash
python3 -c '
import raid_drill as r
for tb in (4, 8, 12, 20):
    print(tb, "TB  RAID 5 URE at 1e-15:", f"{r.p_ure_during_rebuild(tb, r.URE_ENTERPRISE):.0%}",
          " arrays/yr, shelf:", f"{r.fleet_events_per_year(tb, \"stocked shelf\", 5):.2f}")
'
```

Halve `AFR` and the annual rate halves; double `REBUILD_MB_S` and the window halves; but
nothing you set makes a hundred terabytes read clean at 10⁻¹⁴, which is the finding.

## The point

- **RAID is a promise about the next few hours.** Not about the data — an `rm` reaches
  every member — and not forever: it holds until the array is whole again, and that is
  the window.
- **The window is disk size plus swap lead time.** The rebuild you cannot shorten much;
  the lead time you can, and the [operations note](../../operations.md)'s *spares as
  consumables* is that number, on a shelf.
- **At fleet scale improbable is annual.** One array's 0.1% is a fleet's 1.5 a year. The
  discipline exists because the arithmetic does.
- **Choose the level by the read-error arithmetic.** On 20 TB disks a RAID 5 rebuild
  is a rebuild that expects to fail; RAID 6 is the level that survives the survivor's
  bad sector. The capacity arithmetic never says so.

## Teardown

None. The drill holds everything in memory and writes nothing.
