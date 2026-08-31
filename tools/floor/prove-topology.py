#!/usr/bin/env python3
"""Prove the plate's one claim, and record what was proved.

    python3 tools/floor/prove-topology.py            # run the proof, report
    python3 tools/floor/prove-topology.py --stamp    # run it, then record the verdict
    python3 tools/floor/prove-topology.py --check    # for CI: is the plate still proved?

The claim, and the only one the plate makes: **from the lift lobby, along circulation
only, every room and space is reachable without crossing a desk cell.** Nothing about
corridor widths, egress distances or sanitary provision — see
docs/adr/0014-the-plate-stops-at-topology.md for why those are absent on purpose.

The proof itself runs in headless Godot, because a flood fill written here would tell me
only that the floor is walkable the way I imagined it. Godot is design-time and
check-time and never ships (ADR-0013).

**A clone without Godot is not stuck.** `--check` still compares the fingerprint of the
plate's geometry against the one recorded when it was last proved, so an edited plate is
reported as unproved rather than silently trusted. That is the whole point of a `--check`
in this repo: staleness gets caught, not discovered.
"""

import hashlib, json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PLATE = os.path.join(ROOT, "walkthrough", "reference-office.plate.json")
PROJECT = os.path.join(HERE, "godot")
SCRIPT = "prove_topology.gd"
GODOT_CANDIDATES = ["/Applications/Godot.app/Contents/MacOS/Godot"]


def geometry(plate):
    """Everything the proof depends on, and nothing that it does not. A label change
    must not invalidate a verdict; a moved wall must."""
    keep = {}
    for group in ("rooms", "spaces", "booths"):
        keep[group] = sorted(
            [[o["id"], o["rect"], o["door"]["side"], o["door"]["at"]] for o in plate[group]])
    keep["circulation"] = sorted([[c["id"], c["rect"]] for c in plate["circulation"]])
    keep["desks"] = sorted([[p["at"], p["seats"]] for p in plate["desks"]["pods"]])
    keep["grid"] = [plate["grid"]["w"], plate["grid"]["h"]]
    keep["entry"] = plate["entry"]
    return keep


def fingerprint(plate):
    blob = json.dumps(geometry(plate), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


def godot_binary():
    found = shutil.which("godot") or os.environ.get("GODOT_BIN")
    if found and os.path.exists(found):
        return found
    return next((c for c in GODOT_CANDIDATES if os.path.exists(c)), None)


def harness():
    return shutil.which("cli-anything-godot") or os.path.expanduser(
        "~/.local/bin/cli-anything-godot")


def prove():
    """Returns (verdict dict, None) or (None, reason it could not run)."""
    binary = godot_binary()
    if not binary:
        return None, "Godot not found — install Godot 4 or set GODOT_BIN"
    runner = harness()
    if not os.path.exists(runner):
        return None, "cli-anything-godot not found — cli-hub install godot"
    env = {**os.environ, "PLATE": PLATE, "GODOT_BIN": binary}
    out = subprocess.run([runner, "--json", "-p", PROJECT, "script", "run", SCRIPT],
                         capture_output=True, text=True, env=env, timeout=180)
    try:
        wrapped = json.loads(out.stdout)
        line = next(l for l in wrapped["stdout"].splitlines() if l.startswith("{"))
        return json.loads(line), None
    except Exception:
        return None, f"the proof did not return a verdict: {out.stdout[-300:] or out.stderr[-300:]}"


def main():
    args = sys.argv[1:]
    plate = json.load(open(PLATE, encoding="utf-8"))
    current = fingerprint(plate)
    recorded = (plate.get("topology") or {}).get("fingerprint")
    verified = (plate.get("topology") or {}).get("verified")

    if "--check" in args:
        if recorded is None:
            print("the plate has never been proved — run tools/floor/prove-topology.py --stamp",
                  file=sys.stderr)
            return 1
        if recorded != current:
            print(f"the plate has changed since it was proved on {verified} "
                  f"({recorded} → {current}) — nobody has walked it since",
                  file=sys.stderr)
            return 1
        print(f"topology proved {verified} — plate unchanged since ({current})")
        return 0

    verdict, why = prove()
    if verdict is None:
        print(why, file=sys.stderr)
        return 2
    print(json.dumps(verdict, indent=2, ensure_ascii=False))
    if not verdict["ok"]:
        print(f"\nthe floor does not hold together: {len(verdict['unreachable'])} of "
              f"{verdict['spaces_checked']} spaces cannot be reached from the "
              f"{verdict['entry']} along circulation", file=sys.stderr)
        return 1

    if "--stamp" in args:
        import datetime
        plate["topology"]["verified"] = datetime.date.today().isoformat()
        plate["topology"]["fingerprint"] = current
        plate["topology"]["reached"] = verdict["cells_reached"]
        plate["topology"]["spaces"] = verdict["spaces_checked"]
        open(PLATE, "w", encoding="utf-8").write(
            json.dumps(plate, ensure_ascii=False, indent=2) + "\n")
        print(f"\nstamped: {verdict['spaces_checked']} spaces, "
              f"{verdict['cells_reached']} cells, fingerprint {current}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
