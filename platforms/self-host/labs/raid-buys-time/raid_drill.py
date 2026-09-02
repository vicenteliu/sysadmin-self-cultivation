#!/usr/bin/env python3
"""
raid_drill.py — RAID buys you the time to swap, and the rebuild is when you spend it.

The [operations note](../../operations.md) says it in one bullet: disk failures are
constant at fleet scale, spares are consumables with a stocked shelf and a swap
procedure, "RAID buys you the time to swap; a second failure *during* a rebuild is the
nightmare RAID levels exist to bound." The arc's third run adds the older truth from
[`the-stack/04`](../../../../the-stack/04-storage.md): an `rm` is replicated to every
member, so RAID is not backup.

This drill is the arithmetic under that bullet. The numbers are the disk vendors' own —
an annual failure rate, a rebuild throughput, an unrecoverable-read-error rate — and
they sit at the top of the file to be argued with.

Five things it measures rather than asserts:
  1. a mirror survives a dead disk and replicates an `rm` — RAID is not backup
  2. the rebuild window scales with the disk, so a bigger disk is a longer bet
  3. at fleet scale, the second failure inside the window is an annual event, and
     the swap lead time — the shelf — moves the number more than the RAID level does
  4. on today's disk sizes, RAID 5's second failure is not a second disk: it is a read
     error on a survivor, and it is likely
  5. RAID 6 bounds it — by a thousand, not by a little

    python3 raid_drill.py
    python3 raid_drill.py --break-it raid-is-backup      # exit 1
    python3 raid_drill.py --break-it rebuild-is-instant  # exit 1

--break-it runs the model the way the instinct assumes: the other copy still has the
file, or a swap is a swap and the rebuild costs nothing. Neither is how an array works.

No disks, no mdadm, no root. Pure stdlib and deterministic. Exit code 0 means every
assertion about the lesson held.
"""

import argparse
import math
import sys

BREAK = None   # --break-it sets one of the modes above; the model consults it

# --- the numbers, to be argued with ------------------------------------------------
AFR = 0.02                # annual failure rate per disk — the vendors say 1–2%
REBUILD_MB_S = 150        # sustained rebuild throughput per disk
ARRAY_DISKS = 6           # one array
FLEET_ARRAYS = 10_000     # the estate the note is written from
URE_CONSUMER = 1e-14      # unrecoverable read errors per bit read — the spec sheet
URE_ENTERPRISE = 1e-15
SWAP_LEAD_HOURS = {"hot spare": 0, "stocked shelf": 4, "procurement": 72}
HOURS_PER_YEAR = 8760


# --- the reporter — vendored, byte for byte, in every drill (ADR-0017) ------------
# check.py holds the canonical copy and fails a drill whose copy differs. Change it
# there and then everywhere; a drill imports nothing from this repo.

FAILURES = []


def log(msg=""):
    print(msg, flush=True)


def step(n, title):
    log(f"\n=== {n}. {title} ===")


def check(cond, ok_msg, fail_msg):
    if cond:
        log(f"  ✓ {ok_msg}")
    else:
        log(f"  ✗ {fail_msg}")
        FAILURES.append(fail_msg)
    return cond


def verdict(held, broken=False):
    """What main() returns: 1 with every failure listed, or 0 with the lessons that
    held — one line each, in the drill's own words."""
    log("\n" + "=" * 70)
    if FAILURES:
        log(f"FAILED — {len(FAILURES)} assertion(s) did not hold:")
        for f in FAILURES:
            log(f"  ✗ {f}")
        if broken:
            log("\nThat is the point of --break-it. Re-run without it.")
        return 1
    log("PASSED — the lessons held:")
    for line in held:
        log(line)
    return 0

# --- end of the reporter ------------------------------------------------------------



# --- the model: one mirror you can break, and the arithmetic of the rebuild -------

class Mirror:
    """Two members holding the same blocks. RAID's whole job is that a write goes to
    every member — which is exactly why an `rm` does too."""

    def __init__(self, members=2):
        self.members = [dict() for _ in range(members)]
        self.failed = set()

    def write(self, name, data):
        for i, m in enumerate(self.members):
            if i not in self.failed:
                m[name] = data

    def fail_disk(self, i):
        self.failed.add(i)

    def rm(self, name):
        # The break: the instinct that the other copy is a backup — an rm on the
        # array only touches the member you happened to be looking at.
        targets = [0] if BREAK == "raid-is-backup" else range(len(self.members))
        for i in targets:
            if i not in self.failed:
                self.members[i].pop(name, None)

    def read(self, name):
        for i, m in enumerate(self.members):
            if i not in self.failed and name in m:
                return m[name]
        return None

    def copies(self, name):
        return sum(1 for i, m in enumerate(self.members) if i not in self.failed and name in m)


def rebuild_hours(disk_tb):
    # The break: a swap is a swap; the rebuild costs nothing.
    if BREAK == "rebuild-is-instant":
        return 0.0
    return disk_tb * 1e6 / REBUILD_MB_S / 3600


def window_hours(disk_tb, lead):
    return SWAP_LEAD_HOURS[lead] + rebuild_hours(disk_tb)


def p_failures_in_window(hours, disks):
    """Probability that at least one of `disks` fails inside `hours`, at AFR."""
    return 1 - (1 - AFR * hours / HOURS_PER_YEAR) ** disks


def rebuilds_per_year():
    return FLEET_ARRAYS * ARRAY_DISKS * AFR


def fleet_events_per_year(disk_tb, lead, level):
    """Expected arrays per year that lose data: a first failure starts a rebuild,
    and RAID 5 dies at one more failure inside the window, RAID 6 at two."""
    hours = window_hours(disk_tb, lead)
    p_second = p_failures_in_window(hours, ARRAY_DISKS - 1)
    if level == 5:
        return rebuilds_per_year() * p_second
    p_third = p_failures_in_window(hours, ARRAY_DISKS - 2)
    return rebuilds_per_year() * p_second * p_third


def p_ure_during_rebuild(disk_tb, ure_rate):
    """A RAID 5 rebuild reads every surviving disk end to end. The chance of at least
    one unrecoverable read error over that many bits — and one is enough."""
    if BREAK == "rebuild-is-instant":
        return 0.0
    bits = (ARRAY_DISKS - 1) * disk_tb * 1e12 * 8
    return 1 - math.exp(-bits * ure_rate)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--break-it", choices=["raid-is-backup", "rebuild-is-instant"],
                    help="run the model the way the instinct assumes; the drill must then fail")
    args = ap.parse_args()
    global BREAK
    BREAK = args.break_it

    log((__doc__ or "").strip().split("\n\n")[0])
    if BREAK:
        log(f"\n  !! --break-it {BREAK} !!")

    step(1, "A mirror survives a dead disk, and replicates an rm")
    m = Mirror()
    m.write("canary", "the data")
    m.fail_disk(0)
    log(f"  disk 0 fails: canary readable = {m.read('canary') is not None}  (RAID's job)")
    check(m.read("canary") == "the data",
          "a dead disk costs nothing — the surviving member has every block",
          "the mirror lost data on a single disk failure")
    m = Mirror()
    m.write("canary", "the data")
    m.rm("canary")
    log(f"  rm canary on a healthy mirror: copies left = {m.copies('canary')} of 2")
    check(m.copies("canary") == 0,
          "the rm reached every member — RAID replicated the deletion, so RAID is not backup (LESSON 1)",
          "a copy of the canary survived the rm on one member, which is not how an array writes")

    step(2, "The rebuild window scales with the disk")
    small, big = rebuild_hours(2), rebuild_hours(20)
    log(f"  2 TB at {REBUILD_MB_S} MB/s rebuilds in {small:.1f} h; 20 TB in {big:.1f} h")
    check(big > 9 * small,
          f"a ten-times bigger disk is a ten-times longer window — {big:.0f} hours of betting on the survivors (LESSON 2)",
          "the rebuild window did not grow with the disk")

    step(3, "Fleet scale: the second failure inside the window is an annual event")
    log(f"  {FLEET_ARRAYS:,} arrays × {ARRAY_DISKS} disks × {AFR:.0%} AFR = {rebuilds_per_year():,.0f} rebuilds a year")
    rates = {lead: fleet_events_per_year(20, lead, 5) for lead in SWAP_LEAD_HOURS}
    for lead, hours in SWAP_LEAD_HOURS.items():
        log(f"  RAID 5, 20 TB, {lead:<14} window {window_hours(20, lead):6.1f} h → "
            f"{rates[lead]:.2f} arrays lost per year")
    check(rates["procurement"] >= 1,
          f"with disks on order, {rates['procurement']:.1f} arrays a year lose data — the nightmare is scheduled, not hypothetical (LESSON 3)",
          f"even with a procurement lead the fleet loses {rates['procurement']:.2f} arrays a year — the window is not doing anything")
    check(rates["stocked shelf"] < rates["procurement"] / 2,
          f"a stocked shelf cuts it to {rates['stocked shelf']:.2f} — the swap lead time is the larger half of the window",
          "the shelf did not shorten the window: swap lead time is not in the model")

    step(4, "On today's disks, RAID 5's second failure is a read error, and it is likely")
    for tb in (2, 20):
        pc, pe = p_ure_during_rebuild(tb, URE_CONSUMER), p_ure_during_rebuild(tb, URE_ENTERPRISE)
        log(f"  RAID 5 rebuild, {tb:>2} TB disks: P(a URE on a survivor) = "
            f"{pc:.0%} at 1e-14, {pe:.0%} at 1e-15")
    check(p_ure_during_rebuild(20, URE_CONSUMER) > 0.9,
          "a 20 TB RAID 5 rebuild on spec-sheet disks almost certainly hits an unrecoverable read — the second failure is not a second disk (LESSON 4)",
          "the rebuild read a hundred terabytes without a likely read error, which the spec sheet does not support")
    check(p_ure_during_rebuild(20, URE_ENTERPRISE) > 0.5,
          "…and enterprise disks make it a coin flip, not a certainty — better, not safe",
          "enterprise disks made the rebuild read-error-free, which is a tenfold rate applied to a hundred terabytes")

    step(5, "RAID 6 bounds it — by a thousand")
    r5, r6 = fleet_events_per_year(20, "procurement", 5), fleet_events_per_year(20, "procurement", 6)
    log(f"  same fleet, same lead time: RAID 5 loses {r5:.2f} arrays a year, RAID 6 loses {r6:.4f}")
    log(f"  ratio ≈ {r5 / r6 if r6 else float('inf'):,.0f}×")
    check(r6 * 100 < r5,
          "a second parity turns an annual event into a once-in-centuries one — that is what the level is bounding (LESSON 5)",
          "RAID 6 did not bound the double failure — the level is not modelled")

    return verdict([
        "  1. A dead disk costs nothing; an rm reaches every member. RAID is not backup.",
        "  2. The rebuild window scales with the disk — a 20 TB disk is a 37-hour bet.",
        "  3. At fleet scale the second failure inside the window is an annual event,",
        "     and the swap lead time is the larger half of the window.",
        "  4. On today's sizes RAID 5's second failure is a read error on a survivor.",
        "  5. RAID 6 bounds it by three orders of magnitude. That is what a level is for.",
        "",
        "The instinct this drill retired:",
        "  'it is on RAID' — RAID is a promise about the next few hours, and the shelf",
        "  is what decides how many hours. Treat spares as consumables, or the array",
        "  will treat them as the difference between a rebuild and a restore.",
    ], broken=bool(BREAK))


if __name__ == "__main__":
    sys.exit(main())
