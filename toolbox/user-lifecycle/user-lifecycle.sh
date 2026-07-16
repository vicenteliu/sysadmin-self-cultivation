#!/usr/bin/env bash
# user-lifecycle — CSV-driven batch user create / disable on Linux.
# Identity is the densest cluster in real JDs; joiner/mover/leaver at scale is a
# CSV, not fifty hand-typed useradd lines.
#
# SAFE BY DEFAULT: prints the plan and does nothing. Add --apply to execute.
# Applying needs root. Never sets passwords on the command line; created accounts
# are locked (no password) — hand them an SSH key or a `passwd` reset out of band.
#
# CSV: one row per user, `#` comments and blank lines ignored. Columns:
#   username,action[,groups]
#   action = create | disable
#   groups = optional  '|'-separated supplementary groups (create only)
#
#   alice,create,sudo|docker
#   bob,disable
#
# Usage:
#   user-lifecycle.sh users.csv            # dry-run (default) — prints the plan
#   sudo user-lifecycle.sh users.csv --apply
# Exit codes: 0 = ok (planned or applied) · 1 = one or more actions failed
#             2 = usage / bad CSV / not root when applying
set -u

APPLY=0
CSV=""
for a in "$@"; do
  case "$a" in
    --apply) APPLY=1 ;;
    -*) echo "unknown option: $a" >&2; exit 2 ;;
    *) CSV=$a ;;
  esac
done
[ -n "$CSV" ] && [ -f "$CSV" ] || { echo "usage: $0 <users.csv> [--apply]" >&2; exit 2; }

if [ "$APPLY" -eq 1 ] && [ "$(id -u)" -ne 0 ]; then
  echo "error: --apply needs root" >&2; exit 2
fi
[ "$APPLY" -eq 1 ] || echo "== DRY RUN (no changes) — add --apply as root to execute =="

fails=0
lineno=0
while IFS= read -r line || [ -n "$line" ]; do
  lineno=$((lineno+1))
  case "$line" in ''|\#*) continue ;; esac
  IFS=, read -r user action groups <<EOF
$line
EOF
  user=$(printf '%s' "$user" | tr -d '[:space:]')
  action=$(printf '%s' "$action" | tr -d '[:space:]')
  [ -n "$user" ] && [ -n "$action" ] || { echo "line $lineno: bad row: $line" >&2; fails=$((fails+1)); continue; }

  exists=no; id "$user" >/dev/null 2>&1 && exists=yes

  case "$action" in
    create)
      if [ "$exists" = yes ]; then
        echo "skip   $user: already exists"
        continue
      fi
      cmd="useradd -m -s /bin/bash"
      [ -n "${groups:-}" ] && cmd="$cmd -G $(printf '%s' "$groups" | tr '|' ',')"
      cmd="$cmd $user"
      if [ "$APPLY" -eq 1 ]; then
        if $cmd && passwd -l "$user" >/dev/null 2>&1; then
          echo "create $user: created (locked; supply key/reset out of band)"
        else
          echo "create $user: FAILED" >&2; fails=$((fails+1))
        fi
      else
        echo "create $user: would run: $cmd  (then lock password)"
      fi
      ;;
    disable)
      if [ "$exists" = no ]; then
        echo "skip   $user: does not exist"
        continue
      fi
      if [ "$APPLY" -eq 1 ]; then
        # disable = lock + expire + kill sessions. Do NOT delete: leavers'
        # files and audit trail must survive (userdel is a separate decision).
        if usermod -L -e 1 "$user" >/dev/null 2>&1; then
          pkill -KILL -u "$user" 2>/dev/null || true
          echo "disable $user: locked + expired + sessions killed (not deleted)"
        else
          echo "disable $user: FAILED" >&2; fails=$((fails+1))
        fi
      else
        echo "disable $user: would lock + expire + kill sessions (not delete)"
      fi
      ;;
    *)
      echo "line $lineno: unknown action '$action' for $user" >&2; fails=$((fails+1))
      ;;
  esac
done < "$CSV"

if [ "$fails" -gt 0 ]; then echo "--- $fails failure(s)" >&2; exit 1; fi
echo "--- ok"
exit 0
