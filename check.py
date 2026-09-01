#!/usr/bin/env python3
"""
check.py — every check this repo has, from one place.

    python3 check.py              # run everything, report, exit non-zero on failure
    python3 check.py --list       # what would run, and nothing else
    python3 check.py --only links # run one group: builders, links, walkthrough, labs, viewer

Until this existed the checks were real and the *list* of them was not: five
builders with `--check` modes, a walkthrough checker, a viewer smoke test and
eleven self-verifying labs, named across four READMEs and remembered by hand. A
check nobody can enumerate is a check that silently stops being run, which is the
same failure ADR-0008 records about a bound written as a count.

One group here is new. **Nothing in this repo checked its own internal links.**
Every other check guards a generated artifact against its source; this one guards
the prose against itself, which is where a repo of cross-references actually rots
— a heading gets reworded, forty anchors go stale, and each one is invisible until
somebody clicks it.

Standard library only. No network. Safe to run anywhere, including CI.
"""

import argparse
import os
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))

SKIP_DIRS = {".git", "node_modules", "vendor", "__pycache__", ".venv", "site-packages"}

# Files whose links point outside this repo because the file is a COPY of something
# upstream. Excluded by path, listed here rather than silently skipped, because an
# exclusion nobody can see is how a check goes quiet.
NOT_OUR_PROSE = {
    # A diagram-design style profile, committed so a clone can build diagrams without
    # ~/.diagram-design/profiles/. Its links point at that tool's own documentation.
    "site/assets/diagrams/sysadmin-brass.profile.md",
}

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.M)
FENCE_RE = re.compile(r"```.*?```", re.S)
# A link inside backticks is a specimen of a link, not one — `[title](rel/path)` in
# prose describing what to write. Stripped for the same reason fences are.
CODE_RE = re.compile(r"`[^`\n]*`")
# [text](target) — target may carry an #anchor; skip images and absolute URLs
LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(\s*(?!https?:|mailto:|#!)([^)\s]*?)(#[^)\s]*)?\s*\)")


# --- the groups ---------------------------------------------------------------

BUILDERS = [
    ("retrieval index", ["docs/build-index.py", "--check"]),
    ("search corpus", ["site/build-corpus.py", "--check"]),
    ("hero diagrams", ["site/build-diagrams.py", "--check"]),
    ("floor tiles", ["tools/floor/build-tiles.py", "--check"]),
    ("plate topology", ["tools/floor/prove-topology.py", "--check"]),
]

WALKTHROUGH = [("walkthroughs", ["walkthrough/build-walkthrough.py"])]

VIEWER = [("viewer URL contract", ["site/serve-smoke.py"])]


def scan_labs():
    """Walk every directory under a labs/ and split it two ways.

    CONTEXT.md defines a **lab** as pure-local, zero-dependency and self-verifying,
    where exit code 0 means the lesson held — and those carry a `*_drill.py`. A
    directory under labs/ holding something else is a runnable exercise against a
    real account, which this checker must not try to run and must not hide either.
    Returns (self_verifying, needs_an_account)."""
    drills, others = [], []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        if os.path.basename(os.path.dirname(base)) != "labs":
            continue
        py = sorted(f for f in files if f.endswith(".py") and not f.startswith("_"))
        if not py:
            continue
        rel_dir = os.path.relpath(base, ROOT)
        drill = next((f for f in py if f.endswith("_drill.py")), None)
        if drill:
            drills.append((f"lab · {os.path.basename(base)}",
                           [os.path.join(rel_dir, drill)]))
        else:
            others.append((os.path.basename(base), os.path.join(rel_dir, py[0])))
    return sorted(drills), sorted(others)


def find_labs():
    return scan_labs()[0]


# --- the link and anchor check ------------------------------------------------

def slug(text):
    """GitHub's heading slug, byte for byte with walkthrough/build-walkthrough.py:
    drop anything that is not alphanumeric, space, hyphen or underscore; lowercase;
    spaces to hyphens. Emoji and dashes vanish and leave their spaces behind, which
    is why real anchors carry doubled hyphens."""
    return "".join(c.lower() for c in text if c.isalnum() or c in "-_ ").replace(" ", "-")


def markdown_files():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(base, f), ROOT)
            if rel not in NOT_OUR_PROSE:
                yield rel


def check_links(verbose=False):
    """Resolve every relative link in every Markdown file, and every anchor into a
    Markdown file. Returns a list of problems."""
    problems = []
    headings = {}
    checked = 0

    def anchors_of(rel):
        if rel not in headings:
            path = os.path.join(ROOT, rel)
            try:
                text = open(path, encoding="utf-8").read()
            except (OSError, UnicodeDecodeError):
                headings[rel] = set()
                return headings[rel]
            headings[rel] = {slug(h) for _, h in HEADING_RE.findall(text)}
        return headings[rel]

    for rel in markdown_files():
        text = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        text = FENCE_RE.sub("", text)          # a link inside a fence is an example
        text = CODE_RE.sub("", text)           # and so is one inside backticks
        here = os.path.dirname(rel)
        for m in LINK_RE.finditer(text):
            target, frag = m.group(1), (m.group(2) or "")[1:]
            checked += 1
            if not target:                      # same-file anchor
                dest = rel
            else:
                dest = os.path.normpath(os.path.join(here, target))
                if not os.path.exists(os.path.join(ROOT, dest)):
                    problems.append(f"{rel}: link to `{target}` — no such file")
                    continue
            if frag and dest.endswith(".md"):
                have = anchors_of(dest)
                if frag not in have:
                    near = sorted(h for h in have if frag[:12] and frag[:12] in h)
                    hint = f" — did you mean `{near[0]}`?" if near else ""
                    problems.append(f"{rel}: `{target}#{frag}` is not a heading there{hint}")
    if verbose:
        print(f"    {checked} links across {len(list(markdown_files()))} files")
    return problems, checked


# --- the runner ---------------------------------------------------------------

def run(argv):
    """Run one checker. Returns (ok, seconds, tail-of-output-if-failed)."""
    t0 = time.time()
    proc = subprocess.run([sys.executable] + argv, cwd=ROOT,
                          capture_output=True, text=True)
    dt = time.time() - t0
    if proc.returncode == 0:
        return True, dt, ""
    tail = (proc.stdout + proc.stderr).strip().splitlines()
    return False, dt, "\n".join("      " + ln for ln in tail[-12:])


GROUPS = {
    "builders": lambda: BUILDERS,
    "walkthrough": lambda: WALKTHROUGH,
    "viewer": lambda: VIEWER,
    "labs": find_labs,
}


def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0] if __doc__ else "")
    ap.add_argument("--list", action="store_true", help="print what would run and stop")
    ap.add_argument("--only", metavar="GROUP",
                    help="one of: builders, links, walkthrough, viewer, labs")
    args = ap.parse_args()

    wanted = ["builders", "links", "walkthrough", "viewer", "labs"]
    if args.only:
        if args.only not in wanted:
            print(f"unknown group {args.only!r} — choose from {', '.join(wanted)}",
                  file=sys.stderr)
            return 2
        wanted = [args.only]

    if args.list:
        for g in wanted:
            print(f"{g}:")
            if g == "links":
                print("  every relative link and Markdown anchor in the tree")
                continue
            for name, argv in GROUPS[g]():
                print(f"  {name:<28} {' '.join(argv)}")
        return 0

    failed, ran = [], 0
    for g in wanted:
        print(f"\n{g}")
        if g == "links":
            t0 = time.time()
            problems, n = check_links()
            ran += 1
            if problems:
                failed.append("links")
                print(f"  ✗ links                        {len(problems)} broken of {n}"
                      f"   ({time.time() - t0:.1f}s)")
                for p in problems[:20]:
                    print(f"      {p}")
                if len(problems) > 20:
                    print(f"      … and {len(problems) - 20} more")
            else:
                print(f"  ✓ links                        {n} resolve"
                      f"   ({time.time() - t0:.1f}s)")
            continue
        if g == "labs":
            _, needs_account = scan_labs()
            for nm, path in needs_account:
                print(f"  – {nm:<28} not run — needs a real account, so it is an")
                print(f"      exercise rather than a lab as CONTEXT.md defines one: {path}")
        for name, argv in GROUPS[g]():
            ok, dt, tail = run(argv)
            ran += 1
            print(f"  {'✓' if ok else '✗'} {name:<28} {'ok' if ok else 'FAILED'}"
                  f"   ({dt:.1f}s)")
            if not ok:
                failed.append(name)
                print(tail)

    print("\n" + "=" * 62)
    if failed:
        print(f"{len(failed)} of {ran} checks failed: {', '.join(failed)}")
        return 1
    print(f"all {ran} checks pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
