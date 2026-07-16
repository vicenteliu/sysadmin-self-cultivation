#!/usr/bin/env python3
"""user-lifecycle — CSV-driven batch user create/disable on Linux.

DRY-RUN BY DEFAULT: prints the exact commands it would run and exits. Nothing
touches the system until you pass --apply (which requires root).

CSV columns (header required):
    action,username,comment,groups
    create,jdoe,Jane Doe,developers|sudo      # groups |-separated, optional
    disable,olduser,,

Semantics:
