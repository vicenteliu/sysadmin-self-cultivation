# backup-restore-drill

> **Inputs:** a tar archive; optionally the source dir it backs up · **Outputs:**
> restore report on stdout · **Risk:** read-only towards your system — writes only
> to a temp dir it deletes on exit · **Root:** not needed

Prove a backup by restoring it. Extracts the archive into a throwaway temp
directory, counts what came out, and — with `--against` — compares the restore
byte-for-byte against the source. A backup that has never been restored is a hope,
not a backup ([the-stack lab 04](../../the-stack/labs/04-backup-not-snapshot/)).

## Usage

```bash
./backup-restore-drill.sh nightly-etc.tar.gz                       # does it extract at all?
./backup-restore-drill.sh nightly-etc.tar.gz --against /etc        # does it match reality?
```

```
drill: restoring nightly-etc.tar.gz -> /tmp/restore-drill.x1Yz
restored: 312 files, 3.4M
OK: restore matches source exactly (312 files) — this backup is proven
```

Run it right after the backup job for the strongest guarantee; run it against an
older archive to learn how much drift a real restore would carry.

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | restore ok (and matches source when `--against` given) |
| 1 | extraction failed, empty restore, or restore differs from source |
| 2 | usage error |

## Tested on

macOS 26 (bsdtar) and Ubuntu 24.04 container (GNU tar): clean-match, tampered-file,
and corrupt-archive cases. Lab-verified, not production-hardened.
