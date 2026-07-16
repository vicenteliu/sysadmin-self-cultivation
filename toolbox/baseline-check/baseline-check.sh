#!/usr/bin/env bash
# baseline-check — read-only audit of a small hardening-baseline subset.
# Checks a deliberately small set of high-signal items (a CIS-flavored sample,
# not a CIS scanner). Reports PASS/FAIL/INFO/SKIP per check; changes nothing.
# Remediation belongs to config management (the toolbox's Ansible wave), not here.
#
# Usage: baseline-check.sh
# Exit codes: 0 = no FAILs · 1 = one or more FAILs · 2 = unsupported platform
set -u

[ "$(uname -s)" = "Linux" ] || { echo "error: Linux only" >&2; exit 2; }

PASS=0; FAIL=0
ok()   { printf 'PASS  %s\n' "$1"; PASS=$((PASS+1)); }
bad()  { printf 'FAIL  %s\n' "$1"; FAIL=$((FAIL+1)); }
info() { printf 'INFO  %s\n' "$1"; }
skip() { printf 'SKIP  %s\n' "$1"; }

# sshd effective config. Prefer `sshd -T` (resolves defaults + Match blocks) but
# it needs root AND valid host keys; when it yields nothing (missing keys, parse
# error, non-root) fall back to parsing the config file rather than silently
# reporting "unset".
sshd_val() {
  key=$1 val=""
  if [ "$(id -u)" -eq 0 ] && command -v sshd >/dev/null 2>&1; then
    val=$(sshd -T 2>/dev/null | awk -v k="$key" '$1==k { print $2; exit }')
  fi
  if [ -z "$val" ] && [ -r /etc/ssh/sshd_config ]; then
    val=$(awk -v k="$key" 'tolower($1)==k { print tolower($2); exit }' /etc/ssh/sshd_config)
  fi
  printf '%s' "$val"
}

# 1-2. SSH posture
if [ -r /etc/ssh/sshd_config ] || command -v sshd >/dev/null 2>&1; then
  V=$(sshd_val permitrootlogin)
  case "${V:-unset}" in
    no|prohibit-password) ok "ssh: PermitRootLogin = ${V}" ;;
    unset) info "ssh: PermitRootLogin not set (distro default applies — verify it)" ;;
    *) bad "ssh: PermitRootLogin = ${V} (want no / prohibit-password)" ;;
  esac
  V=$(sshd_val passwordauthentication)
  case "${V:-unset}" in
    no) ok "ssh: PasswordAuthentication = no" ;;
    unset) info "ssh: PasswordAuthentication not set (distro default is usually yes)" ;;
    *) bad "ssh: PasswordAuthentication = ${V} (want no — keys only)" ;;
  esac
else
  skip "ssh: no sshd on this host"
fi

# 3. firewall active
if command -v ufw >/dev/null 2>&1 && ufw status 2>/dev/null | grep -q "^Status: active"; then
  ok "firewall: ufw active"
elif command -v firewall-cmd >/dev/null 2>&1 && firewall-cmd --state >/dev/null 2>&1; then
  ok "firewall: firewalld running"
elif command -v nft >/dev/null 2>&1 && [ "$(id -u)" -eq 0 ] && [ -n "$(nft list ruleset 2>/dev/null)" ]; then
  ok "firewall: nftables ruleset present"
else
  bad "firewall: no active firewall detected (ufw/firewalld/nftables)"
fi

# 4. only root has UID 0
DUP=$(awk -F: '$3==0 && $1!="root" { print $1 }' /etc/passwd)
if [ -n "$DUP" ]; then bad "accounts: extra UID-0 user(s): $(echo "$DUP" | tr '\n' ' ')"; else ok "accounts: root is the only UID 0"; fi

# 5. empty password fields (needs shadow access)
if [ -r /etc/shadow ]; then
  EMPTY=$(awk -F: '$2=="" { print $1 }' /etc/shadow)
  if [ -n "$EMPTY" ]; then bad "accounts: empty password field: $(echo "$EMPTY" | tr '\n' ' ')"; else ok "accounts: no empty password fields"; fi
else
  skip "accounts: /etc/shadow not readable (run as root)"
fi

# 6. world-writable files under /etc (2 levels)
WW=$(find /etc -maxdepth 2 -xdev -type f -perm -0002 2>/dev/null | head -5)
if [ -n "$WW" ]; then bad "perms: world-writable under /etc: $(echo "$WW" | tr '\n' ' ')"; else ok "perms: no world-writable files under /etc (depth 2)"; fi

# 7. default umask
UMASK=$(awk '$1=="UMASK" { print $2 }' /etc/login.defs 2>/dev/null)
case "${UMASK:-unset}" in
  022|027|077) ok "umask: login.defs UMASK = $UMASK" ;;
  unset) info "umask: not set in /etc/login.defs" ;;
  *) bad "umask: login.defs UMASK = $UMASK (want 022/027/077)" ;;
esac

# 8. IP forwarding off unless this is meant to route
IPF=$(sysctl -n net.ipv4.ip_forward 2>/dev/null || cat /proc/sys/net/ipv4/ip_forward 2>/dev/null)
if [ "${IPF:-0}" = "0" ]; then ok "sysctl: ip_forward = 0"; else info "sysctl: ip_forward = 1 (fine for a router/container host, review otherwise)"; fi

# 9. persistent journal
if [ -d /var/log/journal ]; then ok "logs: journald persistent storage"; else info "logs: journal is volatile (mkdir /var/log/journal to persist)"; fi

# 10. unattended patching present (informational either way)
if dpkg -l unattended-upgrades >/dev/null 2>&1 || systemctl is-enabled dnf-automatic.timer >/dev/null 2>&1; then
  info "patching: automatic updates mechanism present"
else
  info "patching: no automatic updates mechanism detected"
fi

printf -- '---\n%d pass, %d fail\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
