#!/usr/bin/env bash
# linux-triage — one-shot health/triage report: the first move of every incident.
# Read-only: gathers CPU / memory / disk / network / failed services / recent log
# errors and prints one report. Runs unprivileged; a couple of sections say more
# when root.
#
# Usage: linux-triage.sh
# Exit codes: 0 = no red flags · 1 = red flags found (failed units, disk ≥90%,
#             load > 2x cores) · 2 = unsupported platform
set -u

[ "$(uname -s)" = "Linux" ] || { echo "error: Linux only" >&2; exit 2; }

FLAGS=0
hr() { printf '\n== %s ==\n' "$1"; }
flag() { printf 'FLAG: %s\n' "$1"; FLAGS=$((FLAGS + 1)); }

hr "host"
printf 'host: %s · kernel: %s\n' "$(hostname)" "$(uname -r)"
printf 'uptime:%s\n' "$(uptime | sed 's/.*up/ up/')"
CORES=$(nproc 2>/dev/null || echo 1)
LOAD1=$(cut -d' ' -f1 /proc/loadavg)
printf 'load1: %s on %s core(s)\n' "$LOAD1" "$CORES"
awk -v l="$LOAD1" -v c="$CORES" 'BEGIN { exit !(l > 2*c) }' && flag "load1 $LOAD1 > 2x cores ($CORES)"

hr "cpu — top 5"
ps aux --sort=-%cpu 2>/dev/null | awk 'NR==1 || NR<=6 { printf "%-10s %5s %5s  %s\n", $1, $3, $4, $11 }'

hr "memory"
free -h
ps aux --sort=-%mem 2>/dev/null | awk 'NR>1 && NR<=6 { printf "%-10s %5s%%  %s\n", $1, $4, $11 }'

hr "disk"
df -h -x tmpfs -x devtmpfs -x overlay 2>/dev/null | tail -n +2 | while read -r fs size used avail pct mnt; do
  printf '%-24s %5s/%-5s %4s  %s\n' "$fs" "$used" "$size" "$pct" "$mnt"
done
# red-flag pass (subshell above can't raise FLAGS)
while read -r pct mnt; do
  flag "disk ${pct} on ${mnt}"
done < <(df -x tmpfs -x devtmpfs -x overlay --output=pcent,target 2>/dev/null \
         | tail -n +2 | awk '$1+0 >= 90 { print $1, $2 }')
# inodes
while read -r ipct mnt; do
  flag "inodes ${ipct} on ${mnt}"
done < <(df -x tmpfs -x devtmpfs -x overlay --output=ipcent,target 2>/dev/null \
         | tail -n +2 | awk '$1+0 >= 90 { print $1, $2 }')

hr "network"
if command -v ip >/dev/null; then ip -brief addr | sed 's/^/  /'; fi
if command -v ss >/dev/null; then
  printf 'listening (tcp): %s · established: %s\n' \
    "$(ss -ltnH 2>/dev/null | wc -l)" "$(ss -tnH state established 2>/dev/null | wc -l)"
fi

hr "services"
if command -v systemctl >/dev/null; then
  FAILED=$(systemctl --failed --no-legend --plain 2>/dev/null | awk '{print $1}')
  if [ -n "$FAILED" ]; then
    printf '%s\n' "$FAILED" | sed 's/^/  failed: /'
    N=$(printf '%s\n' "$FAILED" | grep -c '^')
    flag "$N failed systemd unit(s)"
  else
    echo "  no failed units"
  fi
else
  echo "  (no systemd)"
fi

hr "recent log errors (last 20)"
if command -v journalctl >/dev/null; then
  journalctl -p err -n 20 --no-pager -q 2>/dev/null | sed 's/^/  /' || echo "  (journal not readable — run as root for more)"
else
  for f in /var/log/syslog /var/log/messages; do
    [ -r "$f" ] && { grep -iE 'error|fail' "$f" | tail -20 | sed 's/^/  /'; break; }
  done
fi

hr "verdict"
if [ "$FLAGS" -eq 0 ]; then
  echo "no red flags"
  exit 0
else
  echo "$FLAGS red flag(s) above — start there"
  exit 1
fi
