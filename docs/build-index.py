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
another tool's data is skipped outright — see `NOT_A_DOCUMENT`.

Exit codes: 0 ok · 1 a content file is missing front-matter, or carries a summary that is
visibly a fragment of something else · 2 --check found the index stale. Idempotent — two runs produce byte-identical output.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "index.json")
SKIP_DIRS = (".git", ".serena", "__pycache__", "node_modules")
# The one path allowed to have no front-matter: GitHub renders it above the prose
# and this file is the front door. Its record is stated here instead.
ROOT_README = {"kind": "index", "axis": "start-here", "themes": [], "platforms": [],
               "summary": "The front door: what this repo is, how to read it, and what is built."}

# Markdown that is another tool's data rather than a document. The diagram-design style
# profile has to stay byte-identical to the copy `site/build-diagrams.py --install-profile`
# writes into `~/.diagram-design/profiles/`, so front-matter cannot be added to it, and it
# is no more a document than `toolbox/generate/catalog.json` is.
NOT_A_DOCUMENT = {"site/assets/diagrams/sysadmin-brass.profile.md"}

LIST_RE = re.compile(r"^\[(.*)\]$")

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


def parse_front_matter(text):
    """Minimal YAML for the shape this repo writes: scalars, quoted strings, flat lists."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    out = {}
    for line in text[4:end].split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, raw = line.partition(":")
        raw = raw.strip()
        m = LIST_RE.match(raw)
        if m:
            out[key.strip()] = [v.strip() for v in m.group(1).split(",") if v.strip()]
        elif len(raw) >= 2 and raw[0] == raw[-1] == '"':
            out[key.strip()] = raw[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        else:
            out[key.strip()] = raw
    return out


def walk_markdown():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            if name.endswith(".md"):
                yield os.path.relpath(os.path.join(dirpath, name), ROOT).replace(os.sep, "/")


def captured(summary):
    """The reason this summary looks lifted rather than written, or None."""
    for pattern, why in CAPTURED:
        if pattern.search(summary):
            return why
    return None


def build():
    records, missing, lifted = {}, [], []

    for path in walk_markdown():
        if path.startswith("docs/zh/"):
            continue                                   # derived below
        text = open(path, encoding="utf-8").read()

        if path.startswith(".claude/skills/") and path.endswith("SKILL.md"):
            fm = parse_front_matter(text) or {}
            records[path] = {"kind": "agent-skill", "axis": "start-here",
                             "themes": [], "platforms": [],
                             "summary": fm.get("description", "").strip()}
            continue

        if path in NOT_A_DOCUMENT:
            continue

        if path == "README.md":
            records[path] = dict(ROOT_README)
            continue

        fm = parse_front_matter(text)
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

    for path in walk_markdown():                       # derive the mirrors
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
