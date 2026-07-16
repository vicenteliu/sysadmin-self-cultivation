# cidr-check

> **Inputs:** CIDR ranges (args or `--file plan.txt`) · **Outputs:** overlap report on
> stdout · **Risk:** read-only, touches nothing · **Root:** not needed

Detect overlapping CIDR ranges before they become a peering conflict, a VPN
routing surprise, or an unmergeable multi-cloud network. Feed it every subnet in
the plan; it reports every pair that overlaps and flags full containment.
IPv4 and IPv6 both work; comparisons stay within the same family.

Grown from the multi-cloud lab: the classic failure is two teams (or two clouds)
independently picking `10.0.0.0/16`.

## Usage

```bash
./cidr-check.py 10.0.0.0/16 10.0.1.0/24 192.168.0.0/24
./cidr-check.py --file plan.txt      # lines: CIDR [label] · # comments ok
```

```
OVERLAP: 10.0.0.0/16 (aws-prod) <-> 10.0.1.0/24 (gcp-dev) — first contains second
1 overlap(s) across 3 ranges
```

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | no overlaps |
| 1 | overlaps found |
| 2 | usage error or unparsable CIDR |

## Tested on

Python 3.9+ stdlib only. Verified: macOS 26 (Python 3.14), Ubuntu 24.04 container
(Python 3.12). Lab-verified, not production-hardened.
