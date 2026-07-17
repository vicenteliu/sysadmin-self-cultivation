#!/usr/bin/env python3
"""Snapshot hygiene across hypervisors — a snapshot you forgot is a time bomb.

Reads one or more inventory documents (vsphere-inventory and/or pve-inventory —
same schema, so one audit covers both sides of a migration) and flags every
snapshot that violates the hygiene thresholds: too old, chained too deep, or
too many per VM. Assessment only; deleting/consolidating stays a human call.
See README.md for the thresholds and their rationale.
"""

import argparse
import datetime
import json
import sys


def parse_created(value):
    """ISO timestamp (with or without offset/microseconds) → aware datetime, or None."""
    if not value:
        return None
    try:
        dt = datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=datetime.timezone.utc)
    except ValueError:
        return None


def audit_vm(vm, now, max_age_days, max_depth, max_count):
    """One VM → [(level, message), ...] where level is 'warn' or 'info'."""
    findings = []
    detail = vm.get("snapshot_detail")
    if detail is None:
        if vm.get("snapshots"):
            findings.append(("info", f"{vm['snapshots']} snapshot(s) but no detail — "
                             "re-collect with a current inventory tool to audit them"))
        return findings

    for snap in detail:
        created = parse_created(snap.get("created"))
        if created is None:
            findings.append(("info", f"'{snap.get('name')}': creation time unknown — "
                             "age can't be judged"))
            continue
        age = (now - created).total_seconds() / 86400
        if age > max_age_days:
            findings.append(("warn", f"'{snap.get('name')}' is {age:.1f} days old "
                             f"(threshold {max_age_days:g})"))
    depth = max((s.get("depth") or 1 for s in detail), default=0)
    if depth > max_depth:
        findings.append(("warn", f"snapshot chain is {depth} deep "
                         f"(threshold {max_depth})"))
    if len(detail) > max_count:
        findings.append(("warn", f"{len(detail)} snapshots on one VM "
                         f"(threshold {max_count})"))
    return findings


def main():
    ap = argparse.ArgumentParser(
        description="Flag stale, deep, or crowded snapshots across inventories.")
    ap.add_argument("inventories", nargs="*", metavar="FILE",
                    help="inventory JSON file(s); stdin when none given")
    ap.add_argument("--max-age-days", type=float, default=3,
                    help="oldest acceptable snapshot (default 3 — VMware's own "
                         "72-hour guidance)")
    ap.add_argument("--max-depth", type=int, default=2,
                    help="deepest acceptable chain (default 2)")
    ap.add_argument("--max-count", type=int, default=3,
                    help="most snapshots per VM (default 3)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    docs = []
    try:
        if args.inventories:
            for path in args.inventories:
                with open(path) as f:
                    docs.append(json.load(f))
        else:
            docs.append(json.load(sys.stdin))
    except (OSError, json.JSONDecodeError) as e:
        print(f"error: cannot read inventory: {e}", file=sys.stderr)
        sys.exit(2)

    now = datetime.datetime.now(datetime.timezone.utc)
    results, warns, snap_total, vm_total = [], 0, 0, 0
    for doc in docs:
        vms = doc.get("vms")
        if not isinstance(vms, list):
            print("error: no 'vms' array — not an inventory document", file=sys.stderr)
            sys.exit(2)
        source = doc.get("source") or {}
        label = f"{source.get('kind', '?')}:{source.get('endpoint', '?')}"
        for vm in vms:
            vm_total += 1
            snap_total += vm.get("snapshots") or 0
            findings = audit_vm(vm, now, args.max_age_days, args.max_depth,
                                args.max_count)
            if findings:
                warns += sum(1 for lvl, _ in findings if lvl == "warn")
                results.append({"source": label, "vm": vm.get("name"),
                                "findings": [{"level": l, "detail": d}
                                             for l, d in findings]})

    if args.json:
        print(json.dumps({"vms_checked": vm_total, "snapshots": snap_total,
                          "warnings": warns, "flagged": results}, indent=2))
    else:
        for r in results:
            print(f"{r['vm']}  ({r['source']})")
            for f in r["findings"]:
                print(f"  {f['level'].upper():<5} {f['detail']}")
        print(f"\n{vm_total} VM(s), {snap_total} snapshot(s): "
              + (f"{warns} hygiene warning(s)" if warns else "clean"))

    sys.exit(1 if warns else 0)


if __name__ == "__main__":
    main()
