#!/usr/bin/env python3
"""Read-only Proxmox VE inventory — the destination side of a migration.

Emits the same JSON schema as vsphere-inventory so the two sides of a
VMware→Proxmox move can be compared field by field. Two modes:

  live      run ON a PVE node — shells out to read-only `pvesh get` calls
  --from D  run anywhere — read the same pvesh output captured to files
            (capture commands are in README.md)

Python 3.9+ stdlib only. Never writes to the cluster. See README.md.
"""

import argparse
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import NoReturn

DISK_KEY = re.compile(r"^(scsi|virtio|sata|ide)\d+$")
NET_KEY = re.compile(r"^net\d+$")
SIZE = re.compile(r"size=(\d+(?:\.\d+)?)([KMGT])")
UNIT_GB = {"K": 1 / 1048576, "M": 1 / 1024, "G": 1.0, "T": 1024.0}

OSTYPE = {
    "l24": "Linux 2.4 kernel", "l26": "Linux (2.6+ kernel)",
    "win11": "Microsoft Windows 11/2022/2025", "win10": "Microsoft Windows 10/2016/2019",
    "win8": "Microsoft Windows 8/2012", "win7": "Microsoft Windows 7/2008r2",
    "w2k8": "Microsoft Windows Server 2008", "w2k3": "Microsoft Windows Server 2003",
    "w2k": "Microsoft Windows 2000", "wxp": "Microsoft Windows XP",
    "wvista": "Microsoft Windows Vista", "solaris": "Solaris", "other": "other",
}


def die(msg, code) -> NoReturn:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def pvesh_live(path):
    try:
        out = subprocess.run(
            ["pvesh", "get", path, "--output-format", "json"],
            capture_output=True, text=True, timeout=60)
    except FileNotFoundError:
        die("pvesh not found — run on a PVE node, or use --from DIR "
            "with captured output", 1)
    if out.returncode != 0:
        die(f"pvesh get {path} failed: {out.stderr.strip()}", 1)
    return json.loads(out.stdout)


class Source:
    """pvesh results, live or from a capture directory."""

    def __init__(self, capture_dir):
        self.dir = Path(capture_dir) if capture_dir else None

    def get(self, path, filename, optional=False):
        if self.dir is None:
            return pvesh_live(path)
        f = self.dir / filename
        if not f.is_file():
            if optional:
                return None
            die(f"capture is missing {filename} (for pvesh get {path}) — "
                "see README for the capture commands", 1)
        return json.loads(f.read_text())


def parse_disks(config):
    disks = []
    for key in sorted(k for k in config if DISK_KEY.match(k)):
        line = str(config[key])
        if "media=cdrom" in line:
            continue
        m = SIZE.search(line)
        volume = line.split(",")[0]
        if volume.startswith("/dev/"):
            backing = "passthrough"
        elif ".qcow2" in volume:
            backing = "qcow2"
        elif ".vmdk" in volume:
            backing = "vmdk"
        else:
            backing = "raw"
        disks.append({
            "label": key,
            "capacity_gb": round(float(m.group(1)) * UNIT_GB[m.group(2)], 1) if m else None,
            "thin": None,  # thin-ness lives in the storage layer, not the config line
            "backing": backing,
        })
    return disks


def parse_nics(config):
    nics = []
    for key in sorted(k for k in config if NET_KEY.match(k)):
        parts = dict(p.split("=", 1) for p in str(config[key]).split(",") if "=" in p)
        model, mac = next(((k, v) for k, v in parts.items()
                           if k in ("virtio", "e1000", "e1000e", "rtl8139", "vmxnet3")),
                          (None, None))
        nics.append({"model": model, "network": parts.get("bridge"), "mac": mac})
    return nics


def collect(src):
    resources = src.get("/cluster/resources", "resources.json")
    version = src.get("/version", "version.json", optional=True)
    product = f"pve-manager/{version['version']}" if version else "Proxmox VE"

    vms, bridges = [], set()
    for r in resources:
        if r.get("type") != "qemu":
            continue
        node, vmid = r["node"], r["vmid"]
        config = src.get(f"/nodes/{node}/qemu/{vmid}/config", f"config-{vmid}.json")
        snaps = src.get(f"/nodes/{node}/qemu/{vmid}/snapshot",
                        f"snapshot-{vmid}.json", optional=True) or []
        nics = parse_nics(config)
        bridges |= {n["network"] for n in nics if n["network"]}
        vms.append({
            "name": config.get("name") or r.get("name") or str(vmid),
            "power": "on" if r.get("status") == "running" else "off",
            "vcpus": int(config.get("cores", 1)) * int(config.get("sockets", 1)),
            "memory_mb": int(config.get("memory", 0)) or None,
            "guest_os": OSTYPE.get(config.get("ostype"), config.get("ostype")),
            "firmware": "efi" if str(config.get("bios", "")).startswith("ovmf") else "bios",
            "hw_version": config.get("machine"),  # qemu machine type, e.g. q35
            "disks": parse_disks(config),
            "nics": nics,
            "snapshots": sum(1 for s in snaps if s.get("name") != "current"),
        })

    hosts = [{
        "name": r["node"],
        "cpu_cores": r.get("maxcpu"),
        "memory_mb": round(r["maxmem"] / 1048576) if r.get("maxmem") else None,
        "product": product,
    } for r in resources if r.get("type") == "node"]

    datastores = [{
        "name": r["storage"],
        "capacity_gb": round(r["maxdisk"] / 1073741824, 1) if r.get("maxdisk") else None,
        "free_gb": round((r["maxdisk"] - r.get("disk", 0)) / 1073741824, 1)
            if r.get("maxdisk") else None,
        "type": r.get("plugintype"),
    } for r in resources if r.get("type") == "storage"]

    return {
        "source": {"kind": "pve", "endpoint": hosts[0]["name"] if hosts else None,
                   "product": product,
                   "collected_at": datetime.datetime.now(datetime.timezone.utc)
                       .strftime("%Y-%m-%dT%H:%M:%SZ")},
        "vms": vms, "hosts": hosts, "datastores": datastores,
        # PVE has no cluster-wide network list in /cluster/resources; these are
        # the bridges the VM configs actually reference.
        "networks": [{"name": b} for b in sorted(bridges)],
    }


def main():
    ap = argparse.ArgumentParser(
        description="Read-only Proxmox VE inventory (same schema as vsphere-inventory).")
    ap.add_argument("--from", dest="capture", metavar="DIR",
                    help="read captured pvesh output from DIR instead of running pvesh")
    ap.add_argument("--out", metavar="FILE", help="write JSON here instead of stdout")
    args = ap.parse_args()

    inv = collect(Source(args.capture))
    doc = json.dumps(inv, indent=2)
    if args.out:
        with open(args.out, "w") as f:
            f.write(doc + "\n")
    else:
        print(doc)
    print(f"inventory: {len(inv['vms'])} VM(s), {len(inv['hosts'])} node(s), "
          f"{len(inv['datastores'])} storage(s)", file=sys.stderr)


if __name__ == "__main__":
    main()
