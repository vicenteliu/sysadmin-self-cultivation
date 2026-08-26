#!/usr/bin/env python3
"""Build the site's two generated data files from the Markdown the retrieval index already lists.

    python3 site/build-corpus.py            # write site/titles.json and site/corpus.json
    python3 site/build-corpus.py --check    # verify both are current; write nothing

Two files, because they are fetched at different times. `titles.json` is small and
loads with the first paint — the navigation needs a human title for every path, and
`docs/index.json` records a summary but never a title. `corpus.json` carries the full
text of all 190-odd documents and is fetched only when someone actually searches.

This is a **search corpus**, not an index. The word "index" is spoken for three times
over in this repo (`CONTENTS.md`, a directory `README.md`, and `docs/index.json` — the
retrieval index); "catalog" is `toolbox/generate/catalog.json`. See `CONTEXT.md`.

`docs/index.json` is the single source for *which* files exist and what facets they
carry; this script never walks the tree itself, so a file that is missing front-matter
fails in `docs/build-index.py` — one gate, not two. Run that script first.

Standard library only, and idempotent: two runs produce byte-identical output.

Exit codes: 0 ok · 1 the retrieval index is missing or stale-looking · 2 --check found
a generated file out of date.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "docs", "index.json")
OUT_TITLES = os.path.join(ROOT, "site", "titles.json")
OUT_CORPUS = os.path.join(ROOT, "site", "corpus.json")

FRONT_MATTER = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
MERMAID = re.compile(r"^```mermaid\n.*?^```\n", re.DOTALL | re.MULTILINE)
H1 = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
HEADING = re.compile(r"^#{2,4}\s+(.+?)\s*$", re.MULTILINE)
INLINE = re.compile(r"[`*]|^>\\s*|<[^>]+>", re.MULTILINE)   # not `_`: role names carry it
LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")


def title_of(text, path):
    """The document's own H1, or a readable fallback built from its filename."""
    m = H1.search(text)
    if m:
        return INLINE.sub("", LINK.sub(r"\1", m.group(1))).strip()
    stem = os.path.basename(path)[:-3]
    if stem in ("README", "index"):
        parent = os.path.basename(os.path.dirname(path)) or "root"
        return parent.replace("-", " ").title()
    return re.sub(r"^\d+[-.]", "", stem).replace("-", " ").title()


SYNTAX = re.compile(r"^#{1,6}\s+|^\s*[-*+]\s+\[[ xX]\]\s*|^\s*[-*+]\s+|^\s*\|[-:| ]+\|\s*$",
                    re.MULTILINE)


def plain(text):
    """Markdown reduced to searchable words.

    Mermaid goes: it is syntax, not prose. So do heading marks, list bullets, task
    boxes, and table rules — a snippet built from a table otherwise reads as pipes.
    Titles are cleaned separately and keep more, because `baseline_hardening` is a name.
    """
    text = MERMAID.sub("", text)
    text = LINK.sub(r"\1", text)
    text = SYNTAX.sub("", text)
    text = INLINE.sub(" ", text)
    text = text.replace("|", " · ")
    return re.sub(r"\s+", " ", text).strip()


def build():
    if not os.path.exists(INDEX):
        print("docs/index.json is missing — run docs/build-index.py first", file=sys.stderr)
        return None, None, 1
    index = json.load(open(INDEX, encoding="utf-8"))

    titles, docs, missing = {}, {}, []
    for path in sorted(index["files"]):
        if not path.endswith(".md"):
            continue
        full = os.path.join(ROOT, path)
        if not os.path.exists(full):
            missing.append(path)
            continue
        raw = open(full, encoding="utf-8").read()
        body = FRONT_MATTER.sub("", raw)
        titles[path] = title_of(body, path)
        docs[path] = {
            "t": titles[path],
            "h": [INLINE.sub("", LINK.sub(r"\1", h)).strip() for h in HEADING.findall(body)],
            "b": plain(body),
        }

    # A mirror legitimately shares its source's title (the toolbox keeps tool names in
    # English). Only two *canonical* documents sharing one title is a collision, and the
    # navigation has to tell them apart: `README.md` and `CONTEXT.md` both open "# The
    # Sysadmin's Self-Cultivation".
    seen = {}
    for path in sorted(titles):
        if index["files"].get(path, {}).get("derived"):
            continue
        seen.setdefault(titles[path], []).append(path)
    for title, paths in seen.items():
        if len(paths) < 2:
            continue
        for path in paths:
            kind = index["files"].get(path, {}).get("kind", "")
            if kind:
                titles[path] = docs[path]["t"] = f"{title} ({kind})"

    if missing:
        print(f"retrieval index lists {len(missing)} file(s) that do not exist:", file=sys.stderr)
        for path in missing:
            print(f"  {path}", file=sys.stderr)
        print("run docs/build-index.py", file=sys.stderr)
        return None, None, 1

    head = {"schema": 1, "generated_by": "site/build-corpus.py",
            "note": "Generated from the Markdown. Edit the file, not this."}
    titles_doc = dict(head, count=len(titles), titles=titles)
    corpus_doc = dict(head, count=len(docs), docs=docs)
    return titles_doc, corpus_doc, 0


def render(payload):
    return json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False) + "\n"


def main():
    titles_doc, corpus_doc, code = build()
    if code:
        return code
    wanted = [(OUT_TITLES, render(titles_doc)), (OUT_CORPUS, render(corpus_doc))]

    if "--check" in sys.argv:
        stale = [p for p, text in wanted
                 if (open(p, encoding="utf-8").read() if os.path.exists(p) else "") != text]
        if stale:
            for path in stale:
                print(f"{os.path.relpath(path, ROOT)} is stale — run site/build-corpus.py",
                      file=sys.stderr)
            return 2
        print(f"corpus current — {titles_doc['count']} documents")
        return 0

    for path, text in wanted:
        open(path, "w", encoding="utf-8").write(text)
        print(f"wrote {os.path.relpath(path, ROOT)} — {len(text) // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
