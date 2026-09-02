#!/usr/bin/env python3
"""
image_pinning_drill.py — prove, in your own hands, why two machines "built from the
same image" are routinely not the same machine, and why the bug only ever reproduces
on the newer one.

Chapter 03's pipeline is baked → fried: what goes INTO the image, and what cloud-init
personalises at first boot. This drill is about the seam between them, and about the
one word that quietly voids the whole guarantee — **latest**.

    baked   in the image. Changing it costs a rebuild and a redeploy of the fleet.
    fried   applied at first boot. Changing it costs one reboot.
    pinned  the image reference resolves to the same artifact tomorrow.

An unpinned reference is not a name, it is a query, and it is answered at build time.
Two machines launched six weeks apart from `linux-lts/latest` are two different
machines, the fleet's inventory says they are identical, and nothing in it is lying.

No cloud, no credentials, no dependencies. Pure Python stdlib. Exit code 0 means
every assertion about the lesson held. Run it in CI.

    python3 image_pinning_drill.py
    python3 image_pinning_drill.py --sabotage latest-is-stable
    python3 image_pinning_drill.py --sabotage baked-is-free
"""

import argparse
import sys

SABOTAGE = None


def log(msg=""):
    print(msg, flush=True)


def step(n, title):
    log(f"\n=== {n}. {title} ===")


# --------------------------------------------------------------------------
# The catalogue: one image family, republished over time. This is what "latest"
# is a query against.
# --------------------------------------------------------------------------

CATALOGUE = [
    # (published_day, image_id, baked contents)
    (0,   "linux-lts-2401", {"kernel": "6.1.70", "agent": "1.4.2", "openssl": "3.0.11"}),
    (14,  "linux-lts-2402", {"kernel": "6.1.72", "agent": "1.4.2", "openssl": "3.0.13"}),
    (41,  "linux-lts-2403", {"kernel": "6.1.75", "agent": "1.5.0", "openssl": "3.0.13"}),
]


def resolve(reference, day):
    """What an image reference resolves to on a given day."""
    if reference == "latest":
        if SABOTAGE == "latest-is-stable":
            # The sabotage: pretend a moving reference is a name. This is the model
            # in the operator's head, implemented, so the drill can show it.
            return CATALOGUE[0]
        eligible = [c for c in CATALOGUE if c[0] <= day]
        return eligible[-1]
    for c in CATALOGUE:
        if c[1] == reference:
            return c
    raise KeyError(reference)


class Machine:
    def __init__(self, name, reference, day, user_data):
        self.name = name
        self.reference = reference
        self.built_on = day
        published, self.image_id, baked = resolve(reference, day)
        self.baked = dict(baked)
        # cloud-init fries the per-machine configuration at first boot
        self.fried = dict(user_data)

    def config(self):
        merged = dict(self.baked)
        merged.update(self.fried)
        return merged

    def row(self):
        """What the fleet inventory records. Note what is NOT in it."""
        return {"name": self.name, "image": self.reference, "role": self.fried["role"]}


USER_DATA = {"role": "app", "log_level": "info", "ntp": "time.office.internal"}


def cost_to_change(field, machine, fleet_size):
    """What it costs to change one value, given where it lives."""
    if field in machine.fried and SABOTAGE != "baked-is-free":
        return "one reboot", 1
    return f"rebuild the image + redeploy {fleet_size} machines", fleet_size


def run():
    failures = []

    def check(cond, ok, bad):
        if cond:
            log(f"  ✓ {ok}")
        else:
            log(f"  ✗ {bad}")
            failures.append(bad)

    log(__doc__.strip().split("\n\n")[0])

    # ---------------------------------------------------------------- 1
    step(1, "Two machines, one written procedure, six weeks apart")
    a = Machine("app-01", "latest", 3, USER_DATA)
    b = Machine("app-02", "latest", 44, USER_DATA)
    log(f"  app-01 built day {a.built_on:>2} from 'latest' -> {a.image_id}")
    log(f"  app-02 built day {b.built_on:>2} from 'latest' -> {b.image_id}")
    log(f"  inventory says: {a.row()}")
    log(f"                  {b.row()}")
    check(a.row()["image"] == b.row()["image"] and a.image_id != b.image_id,
          "the inventory records them as identical and they are not — the row has no "
          "column for what 'latest' resolved to (LESSON 1)",
          "the two machines resolved to the same image")

    # ---------------------------------------------------------------- 2
    step(2, "Where they actually differ, and which half of the pipeline it is in")
    diff = {k: (a.config()[k], b.config()[k])
            for k in a.config() if a.config()[k] != b.config()[k]}
    for k, (l, r) in sorted(diff.items()):
        log(f"    {k:<9} app-01={l:<9} app-02={r}")
    fried_diff = [k for k in diff if k in a.fried]
    check(diff and not fried_diff,
          f"{len(diff)} differences, all of them BAKED — the fried half is byte-identical "
          "because cloud-init ran the same user-data on both (LESSON 2)",
          "the divergence was in the fried half, which the same user-data should have "
          "made identical")
    log("  This is the useful half of the finding: the personalisation you wrote is")
    log("  doing exactly what you asked. The drift is underneath it.")

    # ---------------------------------------------------------------- 3
    step(3, "The bug that only reproduces on the newer machine")
    log("  A ticket: 'the app crashes on app-02, works fine on app-01.'")
    log("  Both are 'app' role, both from 'latest', both same user-data.")
    log(f"  agent: app-01={a.config()['agent']}  app-02={b.config()['agent']}")
    log("  Nothing in the change record changed. Nobody deployed anything.")
    check(a.config()["agent"] != b.config()["agent"],
          "the difference is an agent version nobody chose, on a day nobody picked "
          "— the change is real and has no change record (LESSON 3)",
          "the two machines carry the same agent version")
    log("  A rebuild of app-01 'to reproduce it' resolves latest again and makes")
    log("  app-01 into app-02. The evidence destroys itself on contact.")

    # ---------------------------------------------------------------- 4
    step(4, "Pin the reference and the fleet becomes reproducible")
    c = Machine("app-03", "linux-lts-2402", 3, USER_DATA)
    d = Machine("app-04", "linux-lts-2402", 44, USER_DATA)
    log(f"  app-03 built day {c.built_on:>2} from 'linux-lts-2402' -> {c.image_id}")
    log(f"  app-04 built day {d.built_on:>2} from 'linux-lts-2402' -> {d.image_id}")
    check(c.config() == d.config(),
          "same pinned reference, forty-one days apart, byte-identical config — "
          "reproducible is a property of the REFERENCE, not of the pipeline (LESSON 4)",
          "two machines from a pinned reference diverged")
    log("  Pinning does not stop you upgrading. It makes the upgrade a commit.")

    # ---------------------------------------------------------------- 5
    step(5, "What the seam costs you, in the unit that decides where a value lives")
    fleet = 40
    for field in ("log_level", "openssl"):
        how, blast = cost_to_change(field, a, fleet)
        where = "fried" if field in a.fried else "baked"
        log(f"  change {field:<10} ({where:<5}) -> {how}")
    _, fried_blast = cost_to_change("log_level", a, fleet)
    _, baked_blast = cost_to_change("openssl", a, fleet)
    check(fried_blast == 1 and baked_blast == fleet,
          f"the same edit costs 1 machine or {fleet}, decided entirely by which side "
          "of the seam the value was put on (LESSON 5)",
          "baked and fried changes cost the same, so the seam is not load-bearing")
    log("  Which is the rule: bake what is slow and shared, fry what is per-machine")
    log("  or likely to change. A value on the wrong side is not a bug until the day")
    log("  you need to change it, and then it is a project.")

    # ---------------------------------------------------------------- verdict
    log("\n" + "=" * 70)
    if failures:
        log(f"DRILL FAILED — {len(failures)} assertion(s) did not hold:")
        for f in failures:
            log(f"  - {f}")
        return 1
    log("DRILL PASSED — the lessons held:")
    log("  1. 'latest' is a query answered at build time, not a name.")
    log("  2. Identical user-data makes the fried half identical; the baked half drifts.")
    log("  3. The resulting bug has no change record and destroys its own evidence.")
    log("  4. A pinned reference is what makes a fleet reproducible.")
    log("  5. Baked-vs-fried decides whether an edit costs one reboot or a fleet.")
    log("")
    log("The inventory was never wrong. It has no column for the question, which is")
    log("the same shape as every other finding in this repo: the control that is")
    log("missing is not a better console, it is recording what the reference resolved")
    log("to at the moment it was resolved.")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sabotage", choices=["latest-is-stable", "baked-is-free"],
                    help="break the model on purpose; the drill must then fail")
    args = ap.parse_args()
    global SABOTAGE
    SABOTAGE = args.sabotage
    if SABOTAGE:
        log(f"*** SABOTAGE: {SABOTAGE} — assertions are expected to fail ***")
    sys.exit(run())


if __name__ == "__main__":
    main()
