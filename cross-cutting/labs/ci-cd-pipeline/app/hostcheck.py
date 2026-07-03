#!/usr/bin/env python3
"""
hostcheck — a tiny, sysadmin-flavored unit worth testing in a pipeline:
validate and normalize a hostname the way you'd sanitize input before it reaches
DNS or an inventory file. Pure stdlib, no dependencies — so CI needs nothing but
Python.

Rules (a practical subset of RFC 1123):
  - 1..253 chars total; labels 1..63 chars, separated by dots
  - labels contain only [a-z0-9-], not starting or ending with '-'
  - input is trimmed and lowercased (normalization) before validation
"""

import re

_LABEL = re.compile(r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$")


def normalize(hostname: str) -> str:
    """Trim surrounding whitespace and lowercase — the normalization step that
    turns '  Web01.PROD  ' into 'web01.prod' before validation."""
    return hostname.strip().lower()


def is_valid(hostname: str) -> bool:
    """True if `hostname` is a valid hostname after normalization."""
    host = normalize(hostname)
    if not host or len(host) > 253:
        return False
    labels = host.split(".")
    return all(_LABEL.match(label) for label in labels)


def main(argv=None):
    import sys
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("usage: hostcheck.py <hostname> [...]", file=sys.stderr)
        return 2
    bad = 0
    for raw in args:
        ok = is_valid(raw)
        print(f"{'ok ' if ok else 'BAD'}  {raw!r} -> {normalize(raw)!r}")
        bad += 0 if ok else 1
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
