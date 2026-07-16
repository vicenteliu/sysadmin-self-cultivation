#!/usr/bin/env python3
"""cidr-check — detect overlapping CIDR ranges across network plans.

Read-only: parses CIDRs, reports pairwise overlaps, touches nothing.

Usage:
    cidr-check.py 10.0.0.0/16 10.0.1.0/24 192.168.0.0/24
    cidr-check.py --file plan.txt        # one entry per line: CIDR [label...]
                                          # blank lines and #-comments ignored

Exit codes: 0 = no overlaps · 1 = overlaps found · 2 = usage or parse error
"""
import argparse
import ipaddress
import sys
from itertools import combinations


def parse_entries(pairs):
    """pairs: iterable of (cidr_string, label). Returns [(network, label)];
    exits 2 on the first unparsable entry — a plan with typos isn't a plan."""
    entries = []
    for cidr, label in pairs:
        try:
            net = ipaddress.ip_network(cidr, strict=False)
        except ValueError as e:
            print(f"error: cannot parse {cidr!r}: {e}", file=sys.stderr)
            sys.exit(2)
        entries.append((net, label))
    return entries


def read_file(path):
    pairs = []
    try:
        with open(path, encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split(None, 1)
                pairs.append((parts[0], parts[1] if len(parts) > 1 else ""))
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(2)
    return pairs


def main():
    ap = argparse.ArgumentParser(description="Detect overlapping CIDR ranges.")
    ap.add_argument("cidrs", nargs="*", help="CIDR ranges (e.g. 10.0.0.0/16)")
    ap.add_argument("--file", "-f", help="file with one 'CIDR [label]' per line")
    args = ap.parse_args()

    pairs = [(c, "") for c in args.cidrs]
    if args.file:
        pairs += read_file(args.file)
    if len(pairs) < 2:
        ap.print_usage(sys.stderr)
        print("error: need at least two CIDRs to compare", file=sys.stderr)
        sys.exit(2)

    entries = parse_entries(pairs)
    overlaps = []
    for (a, la), (b, lb) in combinations(entries, 2):
        if a.version == b.version and a.overlaps(b):
            overlaps.append((a, la, b, lb))

    if not overlaps:
        print(f"OK: {len(entries)} ranges, no overlaps")
        return 0
    for a, la, b, lb in overlaps:
        na = f"{a}" + (f" ({la})" if la else "")
        nb = f"{b}" + (f" ({lb})" if lb else "")
        contain = ""
        if a.supernet_of(b):
            contain = " — first contains second"
        elif b.supernet_of(a):
            contain = " — second contains first"
        print(f"OVERLAP: {na} <-> {nb}{contain}")
    print(f"{len(overlaps)} overlap(s) across {len(entries)} ranges")
    return 1


if __name__ == "__main__":
    sys.exit(main())
