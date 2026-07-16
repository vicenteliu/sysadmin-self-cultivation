#!/usr/bin/env bash
# patch-report — pending-updates inventory with reboot-required flags.
# Read-only: queries the package manager's metadata, changes nothing. Refreshing
# the metadata itself (apt update / dnf makecache) is deliberately NOT done here —
# report on what the box already knows; refreshing is your (scheduled) job.
#
# Usage: patch-report.sh [--quiet]   (--quiet: counts + verdict only)
# Exit codes: 0 = nothing pending · 1 = updates pending and/or reboot required
#             2 = unsupported platform
set -u

QUIET=0
[ "${1:-}" = "--quiet" ] && QUIET=1

pending=0
reboot_needed=0

if command -v apt-get >/dev/null 2>&1; then
  MGR="apt"
  LIST=$(apt list --upgradable 2>/dev/null | tail -n +2)
  [ -n "$LIST" ] && pending=$(printf '%s\n' "$LIST" | grep -c '^')
  echo "manager: apt · pending upgrades: $pending"
  if [ "$QUIET" -eq 0 ] && [ "$pending" -gt 0 ]; then
    printf '%s\n' "$LIST" | sed 's/^/  /'
  fi
  if [ -f /var/run/reboot-required ]; then
    reboot_needed=1
    echo "REBOOT REQUIRED"
    [ "$QUIET" -eq 0 ] && [ -f /var/run/reboot-required.pkgs ] && \
      sort -u /var/run/reboot-required.pkgs | sed 's/^/  because: /'
  fi

elif command -v dnf >/dev/null 2>&1 || command -v yum >/dev/null 2>&1; then
  MGR=$(command -v dnf >/dev/null 2>&1 && echo dnf || echo yum)
  # check-update exits 100 when updates exist, 0 when none, 1 on error.
  OUT=$("$MGR" -q check-update 2>/dev/null)
  RC=$?
  if [ "$RC" -eq 100 ]; then
    LIST=$(printf '%s\n' "$OUT" | awk 'NF>=3 && $1 !~ /^(Obsoleting|Last)/ { print $1, $2 }')
    pending=$(printf '%s\n' "$LIST" | grep -c '^')
    echo "manager: $MGR · pending upgrades: $pending"
    [ "$QUIET" -eq 0 ] && printf '%s\n' "$LIST" | sed 's/^/  /'
    SEC=$("$MGR" -q updateinfo list security 2>/dev/null | grep -vc '^Last' || true)
    [ "${SEC:-0}" -gt 0 ] && echo "security advisories: $SEC"
  elif [ "$RC" -eq 0 ]; then
    echo "manager: $MGR · pending upgrades: 0"
  else
    echo "error: $MGR check-update failed (rc=$RC)" >&2; exit 2
  fi
  if command -v needs-restarting >/dev/null 2>&1; then
    if ! needs-restarting -r >/dev/null 2>&1; then
      reboot_needed=1
      echo "REBOOT REQUIRED (needs-restarting)"
    fi
  fi

else
  echo "error: no supported package manager found (apt/dnf/yum)" >&2
  exit 2
fi

if [ "$pending" -eq 0 ] && [ "$reboot_needed" -eq 0 ]; then
  echo "OK: fully patched, no reboot pending"
  exit 0
fi
exit 1
