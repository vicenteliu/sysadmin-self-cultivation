"""repolib.py — what every builder and guard in this repo was carrying its own copy of.

Nothing here is a check and nothing here generates anything: it is the handful of
facts about *this tree* that four scripts had each written down for themselves —
which directories to skip, which Markdown file is another tool's data, how GitHub
slugs a heading, how front-matter is shaped — and had let drift. Two SKIP_DIRS
disagreed about `.serena/`; the same excluded path had two names; `slug()` existed
twice with a docstring promising they were byte-identical and nothing checking it.

Imported by check.py and by the builders and guards it runs. Never by a drill: a
drill imports nothing from this repo (ADR-0017). Standard library only.
"""

import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

# Directories no walk enters. `.serena/` is a tool's local state, gitignored; `vendor/`
# is the viewer's pinned JavaScript (ADR-0006); the rest are the usual.
SKIP_DIRS = frozenset({".git", ".serena", "node_modules", "vendor", "__pycache__",
                       ".venv", "site-packages"})

# Markdown that is another tool's data rather than a document, listed by path rather
# than matched by rule because an exclusion nobody can see is how a check goes quiet.
# The diagram-design style profile has to stay byte-identical to the copy
# `site/build-diagrams.py --install-profile` writes into ~/.diagram-design/profiles/,
# so it cannot carry front-matter, and its links point at that tool's documentation.
NOT_A_DOCUMENT = frozenset({"site/assets/diagrams/sysadmin-brass.profile.md"})

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.M)
# Two different jobs that once shared one name (FENCE_RE) in two files: a whole fenced
# block, to blank or strip; and a single fence line, to toggle state while walking.
FENCED_BLOCK_RE = re.compile(r"```.*?```", re.S)
FENCE_LINE_RE = re.compile(r"^```", re.M)
# A link inside backticks is a specimen of a link, not one.
CODE_SPAN_RE = re.compile(r"`[^`\n]*`")
# [text](target) — target may carry an #anchor; images and absolute URLs are skipped.
LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(\s*(?!https?:|mailto:|#!)([^)\s]*?)(#[^)\s]*)?\s*\)")
# A walkthrough beat marker: `<!-- beat: stable-id -->` (ADR-0012).
BEAT_RE = re.compile(r"^<!--\s*beat:\s*([a-z0-9][a-z0-9-]*)\s*-->\s*$", re.M)

_LIST_RE = re.compile(r"^\[(.*)\]$")


def slug(text):
    """GitHub's heading slug: drop anything that is not alphanumeric, a space, a hyphen
    or an underscore; lowercase; spaces to hyphens. Emoji and dashes vanish and leave
    their surrounding spaces behind, which is why real anchors carry doubled and
    trailing hyphens — reproducing that is the whole point of deriving it."""
    return "".join(c.lower() for c in text if c.isalnum() or c in "-_ ").replace(" ", "-")


def front_matter(text):
    """(fields, body) for the minimal YAML this repo writes: scalars, quoted strings
    and flat inline lists. Nested structures are deliberately unsupported everywhere.
    Returns (None, text) when there is no front-matter."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    out = {}
    for line in text[4:end].split("\n"):
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, _, raw = line.partition(":")
        raw = raw.strip()
        m = _LIST_RE.match(raw)
        if m:
            out[key.strip()] = [v.strip() for v in m.group(1).split(",") if v.strip()]
        elif len(raw) >= 2 and raw[0] == raw[-1] == '"':
            out[key.strip()] = raw[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        else:
            out[key.strip()] = raw
    return out, text[end + 5:]


def markdown_files():
    """Every document in the tree as a sorted, slash-separated path relative to ROOT —
    SKIP_DIRS not entered, NOT_A_DOCUMENT left out."""
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(base, name), ROOT).replace(os.sep, "/")
            if rel not in NOT_A_DOCUMENT:
                yield rel


_TEXT = {}


def read(rel):
    """The text of one file under ROOT, read once per process. check.py's groups each
    used to open every document again; the tree is small, but eight readers of the same
    four hundred files is a habit, not a design."""
    if rel not in _TEXT:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
            _TEXT[rel] = fh.read()
    return _TEXT[rel]
