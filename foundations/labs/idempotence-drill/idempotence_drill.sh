#!/usr/bin/env bash
# idempotence_drill.sh — prove, in your own hands, the central lesson of the
# foundations chapter: an idempotent script (safe to run twice) is infrastructure;
# a fragile one is a liability. And `set -euo pipefail` is the line between a tool
# and a footgun.
#
# No dependencies beyond bash + coreutils. It builds a throwaway workspace, runs a
# FRAGILE setup script twice (watch it double its work and sail past a failure),
# then an IDEMPOTENT + strict version twice (watch it converge and refuse to run
# with a broken variable), and checks the difference.
#
# Exit code 0 means every assertion about the lesson held. Run it in CI.

set -euo pipefail  # this script practices what it preaches

WORKDIR="$(mktemp -d)"
KEEP=0
[[ "${1:-}" == "--keep" ]] && KEEP=1

cleanup() {
  if [[ "$KEEP" == "1" ]]; then
    echo -e "\n(workspace kept at $WORKDIR)"
  else
    rm -rf "$WORKDIR"
  fi
}
trap cleanup EXIT

fail=0
check() { # check <condition-exit-code> <ok-msg> <fail-msg>
  if [[ "$1" == "0" ]]; then echo "  ✓ $2"; else echo "  ✗ $3"; fail=$((fail+1)); fi
}

echo "workspace: $WORKDIR"

# ---------------------------------------------------------------------------
echo -e "\n=== 1. The FRAGILE script — no safety, not idempotent ==="
# It appends a config line unconditionally and 'mkdir's without -p. Run it twice
# and it doubles the line and would crash on the second mkdir — except it has no
# 'set -e', so it sails right past its own failure and keeps going.
cat > "$WORKDIR/fragile.sh" <<'EOF'
#!/usr/bin/env bash
# no set -euo pipefail — errors are ignored
target="$WORKDIR_INNER/app"
mkdir "$target"                                  # fails on 2nd run (already exists)
echo "server=prod" >> "$target/app.conf"         # appends EVERY run — not idempotent
echo "  fragile: wrote a config line"
EOF
chmod +x "$WORKDIR/fragile.sh"

WORKDIR_INNER="$WORKDIR/fragile-run" ; mkdir -p "$WORKDIR_INNER"
# run it twice, capturing whether it "succeeded" (exit 0) both times despite the error
export WORKDIR_INNER
bash "$WORKDIR/fragile.sh"  >/dev/null 2>&1 ; r1=$?
bash "$WORKDIR/fragile.sh"  >/dev/null 2>&1 ; r2=$?
conf="$WORKDIR_INNER/app/app.conf"
lines=$(grep -c "server=prod" "$conf" 2>/dev/null || echo 0)
echo "  ran it twice; 'server=prod' now appears $lines time(s) in app.conf"
check "$([[ "$lines" == "2" ]] && echo 0 || echo 1)" \
  "the fragile script DOUBLED its config line on the 2nd run — not idempotent (LESSON 1)" \
  "expected the fragile line to be duplicated, got $lines"
check "$([[ "$r2" == "0" ]] && echo 0 || echo 1)" \
  "it reported SUCCESS (exit 0) on the 2nd run despite mkdir failing — no set -e hides the error (LESSON 2)" \
  "expected the fragile script to mask its failure with exit 0"

# ---------------------------------------------------------------------------
echo -e "\n=== 2. The SAFE script — set -euo pipefail + idempotent ==="
# Same job, done right: strict mode, a required-arg guard, mkdir -p, and a
# check-then-append so the line is present exactly once no matter how often it runs.
cat > "$WORKDIR/safe.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail                                # exit on error, unset var, failed pipe
target="${1:?usage: safe.sh <dir>}"             # refuse to run with an empty target
mkdir -p "$target"                               # idempotent: fine if it exists
grep -qxF "server=prod" "$target/app.conf" 2>/dev/null \
  || echo "server=prod" >> "$target/app.conf"    # append ONLY if absent
echo "  safe: converged app.conf"
EOF
chmod +x "$WORKDIR/safe.sh"

safe_target="$WORKDIR/safe-run/app"
bash "$WORKDIR/safe.sh" "$safe_target" >/dev/null 2>&1
bash "$WORKDIR/safe.sh" "$safe_target" >/dev/null 2>&1   # run twice
bash "$WORKDIR/safe.sh" "$safe_target" >/dev/null 2>&1   # and a third time
safe_conf="$safe_target/app.conf"
safe_lines=$(grep -c "server=prod" "$safe_conf" 2>/dev/null || echo 0)
echo "  ran it three times; 'server=prod' appears $safe_lines time(s) — converged"
check "$([[ "$safe_lines" == "1" ]] && echo 0 || echo 1)" \
  "the safe script is IDEMPOTENT — the line is present exactly once after 3 runs (LESSON 3)" \
  "expected exactly 1 config line after repeated runs, got $safe_lines"

# and prove the guard: running it with NO argument must fail loudly, not do damage
if bash "$WORKDIR/safe.sh" >/dev/null 2>&1; then guard=1; else guard=0; fi
check "$guard" \
  "with no argument it FAILS FAST (the \${1:?} guard) instead of acting on an empty path (LESSON 4)" \
  "expected the safe script to refuse to run without an argument"

# ---------------------------------------------------------------------------
echo -e "\n===================================================================="
if [[ "$fail" != "0" ]]; then
  echo "DRILL FAILED — $fail assertion(s) did not hold."
  exit 1
fi
cat <<'EOF'
DRILL PASSED — the lessons held:
  1. The fragile script DOUBLED its work on re-run — not idempotent.
  2. Without set -e it masked its own failure with a success exit code.
  3. The safe script converged: run it 1x or 100x, the state is the same.
  4. set -euo pipefail + a required-arg guard fail fast instead of doing damage.

A script you can run twice safely is infrastructure. One that breaks or doubles
on the second run is a liability you have to babysit. This is the discipline every
IaC tool (Ansible, Terraform) is built on — you just felt it in raw bash.
EOF
exit 0
