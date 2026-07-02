#!/usr/bin/env python3
"""
backup_drill.py — prove, in your own hands, the central lesson of chapter 04:
replication and snapshots faithfully copy destruction; only an independent,
point-in-time backup recovers you — and only up to its RPO.

No cloud, no credentials, no external dependencies. Pure Python stdlib + SQLite.
Three "failure domains" are simulated by three separate directories:

    primary/   the live database        (your block volume)
    replica/   a continuously-synced copy (replication — NOT a backup)
    vault/     independent point-in-time copies (the 3-2-1 off-site backup)

The drill: seed data, replicate it, take one real backup, write MORE data,
then DROP the table. We then show the replica is just as dead as the primary,
restore from the vault, measure RTO, and count exactly what the RPO cost us.

Exit code 0 means every assertion about the lesson held. Run it in CI.
"""

import argparse
import shutil
import sqlite3
import sys
import time
from pathlib import Path


CANARY = ("canary", "if this row survives, the restore worked")


def log(msg=""):
    print(msg, flush=True)


def step(n, title):
    log(f"\n=== {n}. {title} ===")


def connect(path):
    return sqlite3.connect(str(path))


def row_count(db_path):
    """Return the widget row count, or None if the table doesn't exist."""
    con = connect(db_path)
    try:
        cur = con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='widgets'"
        )
        if cur.fetchone() is None:
            return None
        return con.execute("SELECT COUNT(*) FROM widgets").fetchone()[0]
    finally:
        con.close()


def canary_present(db_path):
    con = connect(db_path)
    try:
        if row_count(db_path) is None:
            return False
        row = con.execute(
            "SELECT note FROM widgets WHERE key=?", (CANARY[0],)
        ).fetchone()
        return row is not None and row[0] == CANARY[1]
    finally:
        con.close()


def replicate(primary, replica):
    """Simulate synchronous replication: the replica mirrors the primary byte
    for byte, including whatever just happened to the primary — good or bad."""
    shutil.copy2(primary, replica)


def seed(primary, seed_rows):
    con = connect(primary)
    try:
        con.execute("CREATE TABLE widgets (key TEXT PRIMARY KEY, note TEXT)")
        con.execute("INSERT INTO widgets VALUES (?, ?)", CANARY)
        con.executemany(
            "INSERT INTO widgets VALUES (?, ?)",
            [(f"seed-{i:04d}", f"seed row {i}") for i in range(seed_rows)],
        )
        con.commit()
    finally:
        con.close()


def append_rows(primary, prefix, n):
    con = connect(primary)
    try:
        con.executemany(
            "INSERT INTO widgets VALUES (?, ?)",
            [(f"{prefix}-{i:04d}", f"{prefix} row {i}") for i in range(n)],
        )
        con.commit()
    finally:
        con.close()


def drop_the_table(primary):
    """The disaster: an operator, an app bug, or ransomware destroys the data.
    A hardware-failure control (RAID/snapshot/replication) does not save you
    from this — the destruction is a legitimate, committed write."""
    con = connect(primary)
    try:
        con.execute("DROP TABLE widgets")
        con.commit()
    finally:
        con.close()


def run(workspace: Path, seed_rows: int, post_backup_rows: int) -> int:
    primary = workspace / "primary" / "app.db"
    replica = workspace / "replica" / "app.db"
    vault = workspace / "vault"
    recovered = workspace / "recovered" / "app.db"
    for p in (primary, replica, recovered):
        p.parent.mkdir(parents=True, exist_ok=True)
    vault.mkdir(parents=True, exist_ok=True)

    failures = []

    def check(cond, ok_msg, fail_msg):
        if cond:
            log(f"  ✓ {ok_msg}")
        else:
            log(f"  ✗ {fail_msg}")
            failures.append(fail_msg)

    step(1, "Provision the primary database and seed known data")
    seed(primary, seed_rows)
    total_at_seed = row_count(primary)
    log(f"  primary/app.db created with {total_at_seed} rows (incl. the canary)")
    check(canary_present(primary), "canary row is present in the primary",
          "canary missing from primary right after seeding")

    step(2, "Turn on 'replication' — the replica mirrors the primary")
    replicate(primary, replica)
    log(f"  replica/app.db now mirrors the primary ({row_count(replica)} rows)")
    log("  NOTE: this is what RAID / a sync replica / a same-volume snapshot buys"
        " you — a faithful copy, destruction included.")

    step(3, "Take ONE real backup to the vault (independent, point-in-time)")
    # A cloud-agnostic point-in-time copy. In the real world this lands in a
    # separate account/project/region — here, a separate directory stands in for
    # that separate failure domain. This is the copy 3-2-1 is about.
    backup_name = "backup-0001.db"  # fixed name keeps the run deterministic
    backup_path = vault / backup_name
    con = connect(primary)
    try:
        # sqlite's online backup API = a consistent point-in-time snapshot,
        # the honest analog of a database-aware backup (not a file copy of a
        # live, mid-write database).
        dest = sqlite3.connect(str(backup_path))
        con.backup(dest)
        dest.close()
    finally:
        con.close()
    rows_in_backup = row_count(backup_path)
    backup_wall = time.time()
    log(f"  vault/{backup_name} written with {rows_in_backup} rows")
    check(canary_present(backup_path), "canary is in the backup",
          "canary missing from the backup")

    step(4, "Business continues — write MORE data AFTER the backup")
    append_rows(primary, "postbackup", post_backup_rows)
    replicate(primary, replica)  # replication keeps mirroring
    total_at_disaster = row_count(primary)
    log(f"  primary now has {total_at_disaster} rows"
        f" ({post_backup_rows} written since the backup)")
    log("  these post-backup rows exist ONLY on primary+replica, NOT in the vault"
        " — that gap is your RPO exposure, live.")

    step(5, "DISASTER — the table is dropped (bug / fat-finger / ransomware)")
    time.sleep(0.05)  # let a little wall-clock pass so RPO-time is measurable
    disaster_wall = time.time()
    drop_the_table(primary)
    replicate(primary, replica)  # replication faithfully propagates the DROP
    log("  DROP TABLE widgets — committed on primary, then replicated.")

    step(6, "Assess the damage — what actually survived?")
    primary_rows = row_count(primary)
    replica_rows = row_count(replica)
    check(primary_rows is None, "primary is destroyed (table gone) — as expected",
          "primary somehow still has the table")
    check(replica_rows is None,
          "replica is ALSO destroyed — replication is not backup (LESSON 1)",
          "replica unexpectedly survived — the simulation is wrong")
    check(rows_in_backup is not None and canary_present(backup_path),
          "the vault backup is untouched — independence is what saved it (LESSON 2)",
          "the vault backup was affected — it was not independent")

    step(7, "Recover for real from the vault — and measure RTO")
    t0 = time.perf_counter()
    if recovered.exists():
        recovered.unlink()
    shutil.copy2(backup_path, recovered)
    # prove it opens and is queryable, not just that a file appeared
    recovered_rows = row_count(recovered)
    rto = time.perf_counter() - t0
    check(canary_present(recovered), "canary recovered — the restore is real",
          "canary NOT in the recovered database — restore failed")
    log(f"  restored {recovered_rows} rows in {rto*1000:.1f} ms (this is your RTO)")

    step(8, "Count the RPO — what the backup could not give back")
    rows_lost = (total_at_disaster or 0) - (recovered_rows or 0)
    rpo_seconds = disaster_wall - backup_wall
    log(f"  rows at disaster : {total_at_disaster}")
    log(f"  rows recovered   : {recovered_rows}")
    log(f"  rows LOST (RPO)  : {rows_lost}   "
        f"← everything written in the {rpo_seconds:.2f}s after the last backup")
    check(rows_lost == post_backup_rows,
          f"RPO cost exactly the {post_backup_rows} post-backup rows — RPO is real (LESSON 3)",
          "RPO accounting does not add up")

    log("\n" + "=" * 68)
    if failures:
        log(f"DRILL FAILED — {len(failures)} assertion(s) did not hold:")
        for f in failures:
            log(f"  - {f}")
        return 1
    log("DRILL PASSED — the three lessons held:")
    log("  1. Replication faithfully copied the destruction (replica died too).")
    log("  2. Only the independent, point-in-time backup recovered the data.")
    log(f"  3. RPO was real: {rows_lost} rows written after the backup were gone.")
    log("")
    log("The one number that matters and this drill made concrete:")
    log("  a backup you have not restored is a hope. You just restored one.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workspace", default="./drill-workspace",
                    help="where to build the three failure domains (default: ./drill-workspace)")
    ap.add_argument("--seed-rows", type=int, default=1000,
                    help="rows written before the backup (default: 1000)")
    ap.add_argument("--post-backup-rows", type=int, default=250,
                    help="rows written after the backup = your RPO exposure (default: 250)")
    ap.add_argument("--keep", action="store_true",
                    help="keep the workspace afterward for inspection")
    args = ap.parse_args()

    workspace = Path(args.workspace).resolve()
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True)

    log(f"workspace: {workspace}")
    try:
        rc = run(workspace, args.seed_rows, args.post_backup_rows)
    finally:
        if args.keep:
            log(f"\n(workspace kept at {workspace} — inspect primary/ replica/ vault/ recovered/)")
        else:
            shutil.rmtree(workspace, ignore_errors=True)
    sys.exit(rc)


if __name__ == "__main__":
    main()
