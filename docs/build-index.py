#!/usr/bin/env python3
"""Build docs/index.json — the retrieval index an agent searches instead of the tree.

    python3 docs/build-index.py            # write docs/index.json
    python3 docs/build-index.py --check    # verify it is current; write nothing

Front-matter is the single source. This script never edits a Markdown file and
never invents a field: everything in the index came from a file that declared it,
except for the two derived cases below, which are derived precisely because a
hand-maintained second copy drifts (ADR-0001).

  * Chinese mirrors carry no front-matter. `docs/zh/<path>` mirrors `<path>` one
    to one, so its record is derived from the English source and marked
    `derived: true`. Editing the English file moves the mirror's record with it.
  * Agent Skills already have front-matter with an external consumer (the plugin
    system reads `name` and `description`). Those two fields are read as they
    stand; nothing is added to that schema.

One further exception, kept as a named set rather than a rule: a Markdown file that is
another tool's data is skipped outright — `NOT_A_DOCUMENT` in `repolib.py`, which is
also where the tree walk and the front-matter parser live, shared with `check.py`.

Exit codes: 0 ok · 1 a content file is missing front-matter, or carries a summary that is
visibly a fragment of something else · 2 --check found the index stale. Idempotent — two runs produce byte-identical output.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from repolib import front_matter, markdown_files  # noqa: E402

OUT = os.path.join(ROOT, "docs", "index.json")
# The one path allowed to have no front-matter: GitHub renders it above the prose
# and this file is the front door. Its record is stated here instead.
ROOT_README = {"kind": "index", "axis": "start-here", "themes": [], "platforms": [],
               "summary": "The front door: what this repo is, how to read it, and what is built."}

# A summary that is visibly a fragment of something else. These are shapes, not meanings:
# they catch a list or a leftover marker that ended up in the field, and they cannot catch
# a well-formed sentence lifted from the wrong paragraph — "Confirm in Cost Explorer the
# next day that nothing lingers." was a teardown note serving as a summary for months and
# no rule here would have objected. Eight documents once carried the language-switcher line
# and eight more carried a list item; this stops the mechanical half of that recurring.
# Ending in an ellipsis is deliberate house style (the toolbox summaries truncate their
# Inputs/Outputs opener) and is not a defect.
CAPTURED = [
    (re.compile(r"^\s*$"),            "is empty"),
    (re.compile(r"^\s*\d+\.\s"),      "starts as a list item"),
    (re.compile(r"[:\s]\d+\.\s*$"),   "ends on a list marker"),
    (re.compile(r"\s1\.\s.*\s2\.\s"), "is a numbered list flattened into one line"),
]


def captured(summary):
    """The reason this summary looks lifted rather than written, or None."""
    for pattern, why in CAPTURED:
        if pattern.search(summary):
            return why
    return None


def build():
    records, missing, lifted = {}, [], []

    for path in markdown_files():
        if path.startswith("docs/zh/"):
            continue                                   # derived below
        text = open(os.path.join(ROOT, path), encoding="utf-8").read()

        if path.startswith(".claude/skills/") and path.endswith("SKILL.md"):
            fm = front_matter(text)[0] or {}
            records[path] = {"kind": "agent-skill", "axis": "start-here",
                             "themes": [], "platforms": [],
                             "summary": fm.get("description", "").strip()}
            continue

        if path == "README.md":
            records[path] = dict(ROOT_README)
            continue

        fm, _ = front_matter(text)
        if fm is None:
            missing.append(path)
            continue
        records[path] = {"kind": fm.get("kind", ""), "axis": fm.get("axis", ""),
                         "themes": fm.get("themes", []), "platforms": fm.get("platforms", []),
                         "summary": fm.get("summary", "")}
        why = captured(records[path]["summary"])
        if why:
            lifted.append(f"{path}: summary {why}")
        if "marker" in fm:
            records[path]["marker"] = fm["marker"]
        # A walkthrough carries two canonical scripts and neither is a mirror of the
        # other (ADR-0010), so the viewer cannot reach for `mirrors:` to tell them
        # apart. It needs the language each one is written in, and its sibling.
        if "language" in fm:
            records[path]["language"] = fm["language"]
        if "counterpart" in fm:
            records[path]["counterpart"] = fm["counterpart"]

    for path in markdown_files():                      # derive the mirrors
        if not path.startswith("docs/zh/"):
            continue
        source = path[len("docs/zh/"):]
        base = records.get(source)
        if base is None:
            missing.append(f"{path} (no English source at {source})")
            continue
        rec = dict(base)
        rec["language"] = "zh"
        rec["mirrors"] = source
        rec["derived"] = True
        records[path] = rec

    return records, missing, lifted


def main():
    records, missing, lifted = build()
    if lifted:
        print(f"summaries that look lifted rather than written: {len(lifted)}", file=sys.stderr)
        for problem in lifted:
            print(f"  {problem}", file=sys.stderr)
        return 1
    if missing:
        print(f"missing front-matter: {len(missing)}", file=sys.stderr)
        for path in missing:
            print(f"  {path}", file=sys.stderr)
        return 1

    payload = {
        "schema": 1,
        "generated_by": "docs/build-index.py",
        "note": "Generated from front-matter. Edit the file, not this index.",
        "count": len(records),
        "files": {k: records[k] for k in sorted(records)},
    }
    text = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False) + "\n"

    if "--check" in sys.argv:
        current = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        if current != text:
            print("docs/index.json is stale — run docs/build-index.py", file=sys.stderr)
            return 2
        print(f"index current — {len(records)} files")
        return 0

    open(OUT, "w", encoding="utf-8").write(text)
    print(f"wrote {os.path.relpath(OUT, ROOT)} — {len(records)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
