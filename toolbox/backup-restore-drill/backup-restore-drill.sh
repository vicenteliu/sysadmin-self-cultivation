#!/usr/bin/env bash
# backup-restore-drill — prove a backup by restoring it.
# A backup you haven't restored isn't a backup (the-stack lab 04's law).
#
# Restores a tar archive into a throwaway temp dir, reports what came out, and
# (optionally) compares the restore against the source directory it claims to
# back up. Read-only towards your system: writes only under mktemp, cleans up.
#
# Usage:
#   backup-restore-drill.sh <archive.tar[.gz|.bz2|.xz]> [--against <source-dir>]
#
# Exit codes: 0 = restore ok (and matches source if --against)
#             1 = extraction failed or restore differs from source
#             2 = usage error
set -u

usage() { echo "usage: $0 <archive.tar[.gz|.bz2|.xz]> [--against <source-dir>]" >&2; exit 2; }

[ $# -ge 1 ] || usage
ARCHIVE=$1; shift
SOURCE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --against) [ $# -ge 2 ] || usage; SOURCE=$2; shift 2 ;;
    *) usage ;;
  esac
done

[ -f "$ARCHIVE" ] || { echo "error: no such archive: $ARCHIVE" >&2; exit 2; }
if [ -n "$SOURCE" ] && [ ! -d "$SOURCE" ]; then
  echo "error: no such source dir: $SOURCE" >&2; exit 2
fi

TMP=$(mktemp -d "${TMPDIR:-/tmp}/restore-drill.XXXXXX") || exit 2
trap 'rm -rf "$TMP"' EXIT

echo "drill: restoring $(basename "$ARCHIVE") -> $TMP"
if ! tar -xf "$ARCHIVE" -C "$TMP" 2>"$TMP/.tar-err"; then
  echo "FAIL: extraction error:" >&2
  sed 's/^/  /' "$TMP/.tar-err" >&2
  exit 1
fi
rm -f "$TMP/.tar-err"

FILES=$(find "$TMP" -type f | wc -l | tr -d ' ')
SIZE=$(du -sh "$TMP" 2>/dev/null | cut -f1)
echo "restored: $FILES files, $SIZE"
if [ "$FILES" -eq 0 ]; then
  echo "FAIL: archive restored to zero files — that is not a backup" >&2
  exit 1
fi

if [ -z "$SOURCE" ]; then
  echo "OK: archive extracts cleanly ($FILES files). For full proof, re-run with --against <source-dir>."
  exit 0
fi

# The archive may contain the source dir as a top-level entry — compare against
# the matching root inside the restore if so.
BASE=$(basename "$SOURCE")
CMP_ROOT="$TMP"
[ -d "$TMP/$BASE" ] && CMP_ROOT="$TMP/$BASE"

if DIFF_OUT=$(diff -r "$CMP_ROOT" "$SOURCE" 2>&1); then
  echo "OK: restore matches source exactly ($FILES files) — this backup is proven"
  exit 0
else
  COUNT=$(printf '%s\n' "$DIFF_OUT" | grep -c '^')
  echo "FAIL: restore differs from source ($COUNT difference line(s)); first 10:" >&2
  printf '%s\n' "$DIFF_OUT" | head -10 | sed 's/^/  /' >&2
  exit 1
fi
