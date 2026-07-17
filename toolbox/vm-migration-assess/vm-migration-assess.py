#!/usr/bin/env python3
"""Score every VM in a vsphere-inventory document for VMware→Proxmox migration.

Reads the JSON that vsphere-inventory emits (file or stdin), applies a fixed,
readable rule set, and reports a verdict per VM — EASY / MODERATE / HARD —
with the specific findings behind it. Assessment only: it never touches
either environment. See README.md for the full rule table.
"""

import argparse
import json
import sys

INFO, MINOR, MODERATE, HARD = 0, 1, 2, 3
LEVELS = {INFO: "info", MINOR: "minor", MODERATE: "moderate", HARD: "hard"}
VERDICTS = {INFO: "EASY", MINOR: "EASY", MODERATE: "MODERATE", HARD: "HARD"}

OLD_WINDOWS = ("windows 2000", "windows nt", "windows xp", "windows server 2003")


def assess_vm(vm):
    """One VM → (verdict, [(severity, message), ...])."""
    findings = []
    guest = (vm.get("guest_os") or "").lower()
    disks = vm.get("disks") or []
    nics = vm.get("nics") or []

    for d in disks:
        if d.get("backing") == "rdm":
            findings.append((HARD, f"{d.get('label', 'disk')}: raw device mapping — "
                             "no direct Proxmox equivalent, replan that storage"))
    if any(o in guest for o in OLD_WINDOWS):
        findings.append((HARD, "end-of-life Windows guest — virtio drivers "
                         "unavailable; migrate as-is only with IDE/e1000 legacy config"))

    if vm.get("snapshots"):
        findings.append((MODERATE, f"{vm['snapshots']} snapshot(s) — consolidate "
                         "before export; snapshot chains do not convert"))
    if "windows" in guest and not any(o in guest for o in OLD_WINDOWS):
        findings.append((MODERATE, "Windows guest — install virtio drivers before "
                         "cutover (disk + NIC model change)"))

    if vm.get("firmware") == "efi":
        findings.append((MINOR, "EFI firmware — recreate as OVMF VM and check "
                         "Secure Boot expectations"))
    nic_models = {n.get("model") for n in nics}
    if "windows" not in guest and nic_models - {"virtio"}:
        findings.append((MINOR, f"NIC model(s) {', '.join(sorted(nic_models - {'virtio'}))} "
                         "→ virtio on Proxmox; Linux carries the driver in-kernel"))
    total_gb = sum(d.get("capacity_gb") or 0 for d in disks)
    if total_gb > 2048:
        findings.append((MINOR, f"{round(total_gb / 1024, 1)} TiB of disk — plan the "
                         "transfer window and bandwidth"))
    hw = vm.get("hw_version") or ""
    if hw.startswith("vmx-") and hw[4:].isdigit() and int(hw[4:]) < 10:
        findings.append((MINOR, f"virtual hardware {hw} is ancient — verify guest "
                         "assumptions before conversion"))

    if vm.get("power") == "on":
        findings.append((INFO, "powered on — schedule a downtime window (offline "
                         "conversion) or plan a re-sync cutover"))
    if any(d.get("thin") is False for d in disks):
        findings.append((INFO, "thick-provisioned disk(s) export at full size"))

    worst = max((sev for sev, _ in findings), default=INFO)
    return VERDICTS[worst], findings


def main():
    ap = argparse.ArgumentParser(
        description="Assess VMware→Proxmox migration difficulty per VM.")
    ap.add_argument("--in", dest="infile", metavar="FILE",
                    help="vsphere-inventory JSON (default: stdin)")
    ap.add_argument("--json", action="store_true",
                    help="machine-readable output instead of the report")
    args = ap.parse_args()

    try:
        with (open(args.infile) if args.infile else sys.stdin) as f:
            inv = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"error: cannot read inventory: {e}", file=sys.stderr)
        sys.exit(2)
    vms = inv.get("vms")
    if not isinstance(vms, list):
        print("error: no 'vms' array — is this a vsphere-inventory document?",
              file=sys.stderr)
        sys.exit(2)
    kind = (inv.get("source") or {}).get("kind")
    if kind and kind != "vsphere":
        print(f"note: source kind is '{kind}', rules assume a vSphere source",
              file=sys.stderr)

    results = []
    for vm in vms:
        verdict, findings = assess_vm(vm)
        results.append({"name": vm.get("name"), "verdict": verdict,
                        "findings": [{"severity": LEVELS[s], "detail": m}
                                     for s, m in findings]})

    counts = {"EASY": 0, "MODERATE": 0, "HARD": 0}
    for r in results:
        counts[r["verdict"]] += 1

    if args.json:
        print(json.dumps({"source": inv.get("source"), "counts": counts,
                          "vms": results}, indent=2))
    else:
        order = {"HARD": 0, "MODERATE": 1, "EASY": 2}
        for r in sorted(results, key=lambda r: (order[r["verdict"]], r["name"] or "")):
            print(f"{r['verdict']:<9} {r['name']}")
            for f in r["findings"]:
                print(f"          - [{f['severity']}] {f['detail']}")
        print(f"\n{len(results)} VM(s): {counts['EASY']} easy, "
              f"{counts['MODERATE']} moderate, {counts['HARD']} hard")

    sys.exit(1 if counts["HARD"] else 0)


if __name__ == "__main__":
    main()
