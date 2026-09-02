#!/usr/bin/env python3
"""
check.py — every check this repo has, from one place.

    python3 check.py              # run everything, report, exit non-zero on failure
    python3 check.py --list       # what would run, and nothing else
    python3 check.py --only links # run one group: builders, links, counts, walkthrough, viewer, toolbox, labs

Until this existed the checks were real and the *list* of them was not: five
builders with `--check` modes, a walkthrough checker, a viewer smoke test and
eleven self-verifying labs, named across four READMEs and remembered by hand. A
check nobody can enumerate is a check that silently stops being run, which is the
same failure ADR-0008 records about a bound written as a count.

Two groups here guard the prose. **Nothing in this repo checked its own internal links**,
and nothing checked the numbers the prose states about itself — see the counts section
below for what that cost. The kinds of number it checks, and the phrasings that carry
them, are data: `docs/counts.json`. A front page states only those kinds, and a new
kind is added there first — a number no kind anchors is a number nothing checks, which
is how four went stale on the front door while this check stayed green.
Every other check guards a generated artifact against its source; this one guards
the prose against itself, which is where a repo of cross-references actually rots
— a heading gets reworded, forty anchors go stale, and each one is invisible until
somebody clicks it.

A third group guards the toolbox, which nothing guarded at all until a tracked file
that did not parse sat in it for weeks — twelve lines of an abandoned rewrite, copied
into every generated pack. Two checks close that: every script in the tree at least
parses, and the one document the four hypervisor tools share is defined once, in
`toolbox/inventory.schema.json`, and validated from the captures that ship with
`pve-inventory`.

The facts about the tree that every builder and guard needs — which directories to
skip, how a heading slugs, how front-matter is shaped — live in `repolib.py`, which is
where four scripts' private copies of them were merged.

Standard library only. No network. Safe to run anywhere, including CI.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time

from repolib import (ROOT, SKIP_DIRS, HEADING_RE, FENCED_BLOCK_RE, CODE_SPAN_RE, LINK_RE,
                     BEAT_RE, slug, front_matter, markdown_files, read)


# --- the groups ---------------------------------------------------------------

BUILDERS = [
    ("retrieval index", ["docs/build-index.py", "--check"]),
    ("search corpus", ["site/build-corpus.py", "--check"]),
    ("hero diagrams", ["site/build-diagrams.py", "--check"]),
    ("floor tiles", ["tools/floor/build-tiles.py", "--check"]),
    ("plate topology", ["tools/floor/prove-topology.py", "--check"]),
]

WALKTHROUGH = [("walkthroughs", ["walkthrough/guard-walkthrough.py"])]

VIEWER = [("viewer URL contract", ["site/serve-smoke.py"])]


# --- the toolbox check --------------------------------------------------------

INVENTORY_SCHEMA = "toolbox/inventory.schema.json"

# The one inventory producer that needs no host: pve-inventory reads pvesh output
# captured to files, and ships a capture. Its document is validated against the
# schema, then handed to both consumers, which must read it and answer in JSON.
# `{inventory}` is replaced with the path of the produced document.
INVENTORY_PRODUCER = ("pve-inventory from fixtures",
                      ["toolbox/pve-inventory/pve-inventory.py",
                       "--from", "toolbox/pve-inventory/fixtures"])
INVENTORY_CONSUMERS = [
    ("vm-migration-assess", ["toolbox/vm-migration-assess/vm-migration-assess.py",
                             "--in", "{inventory}", "--json"]),
    ("snapshot-audit", ["toolbox/snapshot-audit/snapshot-audit.py", "{inventory}", "--json"]),
]
# Named here so the listing says it rather than the reader wondering why one of the
# four tools is missing: vsphere-inventory talks SOAP to a live vCenter and has no
# capture mode, so nothing can run it on a push.
INVENTORY_NOT_RUN = ("vsphere-inventory",
                     "not validated — no capture mode, so nothing can run it without a vCenter")


def script_files():
    """Every .py and every .sh in the tree, outside SKIP_DIRS."""
    py, sh = [], []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            rel = os.path.relpath(os.path.join(base, f), ROOT)
            if f.endswith(".py"):
                py.append(rel)
            elif f.endswith(".sh"):
                sh.append(rel)
    return sorted(py), sorted(sh)


def check_scripts_parse():
    """Every .py compiles and every .sh passes `bash -n`. Returns (problems, n).

    Compiling is not running: this catches the file that cannot be a program at all,
    which is the only kind of breakage that survives with no test and no caller."""
    py, sh = script_files()
    problems = []
    for rel in py:
        try:
            compile(open(os.path.join(ROOT, rel), encoding="utf-8").read(), rel, "exec")
        except SyntaxError as e:
            problems.append(f"{rel}:{e.lineno}: {e.msg}")
    for rel in sh:
        proc = subprocess.run(["bash", "-n", rel], cwd=ROOT, capture_output=True, text=True)
        if proc.returncode != 0:
            why = proc.stderr.strip().splitlines()
            problems.append(f"{rel}: {why[-1] if why else 'bash -n failed'}")
    return problems, len(py) + len(sh)


def _is_type(value, name):
    return {
        "null": value is None,
        "boolean": isinstance(value, bool),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "string": isinstance(value, str),
        "array": isinstance(value, list),
        "object": isinstance(value, dict),
    }[name]


def validate(instance, schema, root, path="$"):
    """The subset of JSON Schema the inventory schema uses — type, enum, required,
    properties, additionalProperties, items, and $ref into $defs. Returns problems,
    each naming the path that broke. Not a general validator and not meant to be."""
    if "$ref" in schema:
        node = root
        for part in schema["$ref"].lstrip("#/").split("/"):
            node = node[part]
        return validate(instance, node, root, path)
    problems = []
    types = schema.get("type")
    if types is not None:
        types = [types] if isinstance(types, str) else types
        if not any(_is_type(instance, t) for t in types):
            return [f"{path}: expected {' or '.join(types)}, got {type(instance).__name__}"]
    if "enum" in schema and instance not in schema["enum"]:
        problems.append(f"{path}: {instance!r} is not one of {schema['enum']}")
    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                problems.append(f"{path}: missing required key {key!r}")
        props = schema.get("properties", {})
        for key, val in instance.items():
            if key in props:
                problems.extend(validate(val, props[key], root, f"{path}.{key}"))
            elif schema.get("additionalProperties") is False:
                problems.append(f"{path}: unexpected key {key!r}")
    if isinstance(instance, list) and "items" in schema:
        for i, val in enumerate(instance):
            problems.extend(validate(val, schema["items"], root, f"{path}[{i}]"))
    return problems


def check_inventory_schema():
    """Produce the fixture inventory, validate it, hand it to both consumers.

    A consumer may exit 0 (clean) or 1 (findings) — those are answers. Exit 2 is the
    toolbox's own word for *could not run*, and anything but JSON on stdout under
    `--json` is a broken promise to the agent that asked for it."""
    with open(os.path.join(ROOT, INVENTORY_SCHEMA), encoding="utf-8") as f:
        schema = json.load(f)
    label, argv = INVENTORY_PRODUCER
    proc = subprocess.run([sys.executable] + argv, cwd=ROOT, capture_output=True, text=True)
    if proc.returncode != 0:
        why = (proc.stderr or proc.stdout).strip().splitlines()
        return [f"{label}: exit {proc.returncode} — {why[-1] if why else 'no output'}"]
    try:
        doc = json.loads(proc.stdout)
    except ValueError as e:
        return [f"{label}: stdout is not JSON ({e})"]
    problems = [f"{label}: {p}" for p in validate(doc, schema, schema)]
    if problems:
        return problems
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "inventory.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write(proc.stdout)
        for name, argv in INVENTORY_CONSUMERS:
            argv = [a.replace("{inventory}", path) for a in argv]
            cp = subprocess.run([sys.executable] + argv, cwd=ROOT,
                                capture_output=True, text=True)
            if cp.returncode not in (0, 1):
                why = (cp.stderr or cp.stdout).strip().splitlines()
                problems.append(f"{name}: exit {cp.returncode} on the fixture inventory — "
                                f"{why[-1] if why else 'no output'}")
                continue
            try:
                json.loads(cp.stdout)
            except ValueError as e:
                problems.append(f"{name}: --json output is not JSON ({e})")
    return problems


def scan_labs():
    """Walk every directory under a labs/ and split it two ways.

    CONTEXT.md defines a **lab** as pure-local, zero-dependency and self-verifying,
    where exit code 0 means the lesson held. A directory under labs/ holding something
    else is a runnable exercise, which this checker must not try to run and must not
    hide either. Returns (self_verifying, not_run) where each not_run entry carries
    the reason it is not run.

    Classified by dependency, not by filename. `*_drill.py` is the naming convention
    and most labs follow it, but the-stack/labs/01-failure-domains/ does not, and for
    a while this function reported that pure-stdlib drill as needing a real account —
    a false sentence printed on every run, about the one file in the repo whose whole
    subject is that a check should be believed."""
    drills, others = [], []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        if os.path.basename(os.path.dirname(base)) != "labs":
            continue
        py = sorted(f for f in files if f.endswith(".py") and not f.startswith("_"))
        if not py:
            continue
        rel_dir = os.path.relpath(base, ROOT)
        name = os.path.basename(base)
        drill = next((f for f in py if f.endswith("_drill.py")), None)
        if "requirements.txt" in files:
            # It declares a dependency, so it is not zero-dependency, so it is not a
            # lab as CONTEXT.md defines one — whatever the script is called.
            others.append((name, os.path.join(rel_dir, drill or py[0]),
                           "declares dependencies (requirements.txt), so it is an "
                           "exercise rather than a lab as CONTEXT.md defines one"))
        elif drill or len(py) == 1:
            drills.append((f"lab · {name}", [os.path.join(rel_dir, drill or py[0])]))
        else:
            others.append((name, os.path.join(rel_dir, py[0]),
                           "several scripts and no *_drill.py, so there is no entry "
                           "point to run — name one `*_drill.py`"))
    return sorted(drills), sorted(others)


def find_labs():
    return scan_labs()[0]


# --- the drill reporter -------------------------------------------------------
#
# ADR-0017: a drill imports nothing from this repo, so its reporter — log, step,
# check, verdict — is pasted into every drill, and this is the copy the others are
# held to. Change it here, then in every drill; a copy that differs fails below.

DRILL_BLOCK = r'''# --- the reporter — vendored, byte for byte, in every drill (ADR-0017) ------------
# check.py holds the canonical copy and fails a drill whose copy differs. Change it
# there and then everywhere; a drill imports nothing from this repo.

FAILURES = []


def log(msg=""):
    print(msg, flush=True)


def step(n, title):
    log(f"\n=== {n}. {title} ===")


def check(cond, ok_msg, fail_msg):
    if cond:
        log(f"  ✓ {ok_msg}")
    else:
        log(f"  ✗ {fail_msg}")
        FAILURES.append(fail_msg)
    return cond


def verdict(held, broken=False):
    """What main() returns: 1 with every failure listed, or 0 with the lessons that
    held — one line each, in the drill's own words."""
    log("\n" + "=" * 70)
    if FAILURES:
        log(f"FAILED — {len(FAILURES)} assertion(s) did not hold:")
        for f in FAILURES:
            log(f"  ✗ {f}")
        if broken:
            log("\nThat is the point of --break-it. Re-run without it.")
        return 1
    log("PASSED — the lessons held:")
    for line in held:
        log(line)
    return 0

# --- end of the reporter ------------------------------------------------------------
'''

# Drills written in shell carry the same contract in shell. Named here so the listing
# says so, rather than leaving one lab looking unchecked.
SHELL_DRILLS = {
    "foundations/labs/idempotence-drill/idempotence_drill.sh":
        "carries the reporter contract in shell; the Python block does not apply",
}


def check_drill_block():
    """Every drill check.py runs carries DRILL_BLOCK byte for byte."""
    problems = []
    for _, argv in find_labs():
        if DRILL_BLOCK not in read(argv[0]):
            problems.append(f"{argv[0]}: does not carry the reporter block byte for byte — "
                            f"copy it from check.py (`python3 check.py --list --only labs` "
                            f"prints it)")
    return problems


# --- the link and anchor check ------------------------------------------------

def check_links(verbose=False):
    """Resolve every relative link in every Markdown file, and every anchor into a
    Markdown file. Returns a list of problems."""
    problems = []
    headings = {}
    checked = 0

    def anchors_of(rel):
        if rel not in headings:
            try:
                text = read(rel)
            except (OSError, UnicodeDecodeError):
                headings[rel] = set()
                return headings[rel]
            headings[rel] = {slug(h) for _, h in HEADING_RE.findall(text)}
        return headings[rel]

    for rel in markdown_files():
        text = FENCED_BLOCK_RE.sub("", read(rel))   # a link inside a fence is an example
        text = CODE_SPAN_RE.sub("", text)           # and so is one inside backticks
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
    problems += check_mirror_links()
    if verbose:
        print(f"    {checked} links across {len(list(markdown_files()))} files")
    return problems, checked


def check_mirror_links():
    """A mirror must link to a mirror where one exists.

    docs/README.md's convention is that each language folder mirrors the English tree,
    so a link inside docs/zh/ that reaches back to the English canonical is correct only
    while that target has no mirror. The moment it gets one the link is stale, and
    nothing notices: it still resolves, and it still lands on a real document — in the
    wrong language, silently ending the reader's Chinese path.

    This is the failure the mirror batches actually create. Writing a batch means
    pointing at the English canonical for everything the next batch will mirror, and
    the next batch has no way to know which links to come back for."""
    problems = []
    for rel in markdown_files():
        if not rel.startswith("docs/zh/"):
            continue
        here = os.path.dirname(rel)
        text = FENCED_BLOCK_RE.sub("", read(rel))
        text = CODE_SPAN_RE.sub("", text)
        for line in text.splitlines():
            # The 🌐 switcher points at the English canonical on purpose — that is the
            # one link on the page whose whole job is to leave the mirror.
            if line.lstrip().startswith("> 🌐"):
                continue
            for m in LINK_RE.finditer(line):
                target = m.group(1)
                if not target:
                    continue
                dest = os.path.normpath(os.path.join(here, target))
                if dest.startswith("docs/zh/"):
                    continue
                mirror = os.path.join("docs", "zh", dest)
                if os.path.exists(os.path.join(ROOT, mirror)):
                    problems.append(
                        f"{rel}: links to `{target}` in the English tree, but "
                        f"`{mirror}` exists — a mirror links to a mirror")
    return problems


# --- the counts check ---------------------------------------------------------
#
# ADR-0008 records that a count is not a bound, and ADR-0007's was crossed three
# times before anybody noticed. This is the other half of that lesson: a count
# written into prose is a claim, and prose is the one artifact in this repo that no
# builder regenerates. Walkthrough 02 shipped and seven index documents went on
# saying "walkthrough 01" as though it were the only one; `docs/questions.md` said
# 30 answered while CONTENTS.md still said 12. Both were found by reading, which is
# the method that fails silently.
#
# So: compute each number from disk, then find every place the prose states it.
# A stated count that disagrees with disk fails. A count nobody states cannot go
# stale — it can only go missing — which is why the fix that accompanies this check
# makes each index document *state* how many walkthroughs there are.
#
# The patterns lived here as code until the front door was found stating four numbers
# in phrasings none of them anchored — "covers 27 pages", "17 notes", "two runnable
# labs", "most carry --break-it" — and the check stayed green for weeks. They are now
# `docs/counts.json`, where `--list` prints them and a new kind is added first.
#
# The stricter rule was tried and rejected: *a document that links one walkthrough
# must link them all*. It catches the omission directly and needs no stated number,
# but it fires on four documents that are right — ADR-0013 cites walkthrough 01
# because that is the one it was written about and an ADR is never edited,
# `docs/questions/networking.md` answers a network question with the network
# walkthrough, and `site/README.md` uses one URL as a shell example. A check with
# four standing exceptions is a check people learn to skip.

# Numbers in this repo's voice are usually words. Anchoring every pattern to its
# noun is what keeps `三十个` in a spoken script from being read as inventory.
WORD_NUMBERS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen "
    "fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}
WORD_NUMBERS.update({w: i + 21 for i, w in enumerate(
    "twenty-one twenty-two twenty-three twenty-four twenty-five twenty-six "
    "twenty-seven twenty-eight twenty-nine thirty".split())})
WORD_NUMBERS.update({w: i for i, w in enumerate(
    "零 一 二 三 四 五 六 七 八 九 十 十一 十二 十三 十四 十五 十六 十七 十八 十九 二十".split())})
WORD_NUMBERS.update({w: i + 21 for i, w in enumerate(
    "二十一 二十二 二十三 二十四 二十五 二十六 二十七 二十八 二十九 三十".split())})
WORD_NUMBERS["两"] = 2
# Capitalised because prose starts sentences — and spelling them out here is cheaper
# than re.I, which costs about 40% of this check's runtime on a fifty-way alternation.
WORD_NUMBERS.update({w.capitalize(): n for w, n in list(WORD_NUMBERS.items())})

NUM = "(" + "|".join([r"\d+"] + sorted(WORD_NUMBERS, key=len, reverse=True)) + ")"
# `one` matches inside `none`, and `none open` is how a domain file says zero.
# English patterns need a left boundary; the Chinese ones must not have one, because
# the CJK character before a Chinese numeral is itself a word character.
NUM_EN = r"(?<![A-Za-z-])" + NUM


def as_int(token):
    return int(token) if token.isdigit() else WORD_NUMBERS[token]


def _glob(pattern):
    import glob
    return sorted(glob.glob(os.path.join(ROOT, pattern), recursive=True))


def walkthrough_beats():
    """Beats per walkthrough, read the way guard-walkthrough.py reads them: a beat is
    a `<!-- beat: id -->` marker in the English script."""
    out = {}
    for path in _glob("walkthrough/[0-9]*-*.en.md"):
        rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
        out[os.path.basename(path)] = len(BEAT_RE.findall(read(rel)))
    return out


def question_rows():
    """Every question in every domain file, as (domain, status). The domain files are
    the record; docs/questions.md's table is a claim about them."""
    rows = []
    for path in _glob("docs/questions/*.md"):
        domain = os.path.splitext(os.path.basename(path))[0]
        for line in open(path, encoding="utf-8"):
            # The status cell may carry more than the marker — `✅ 🧭`, or `✅ per
            # platform · **closed**`. What decides the row is what it starts with.
            m = re.match(r"\|\s*\d+\s*\|.*?\|\s*(✅|⏳)", line)
            if m:
                rows.append((domain, m.group(1)))
    return rows


def check_questions_ledger():
    """docs/questions.md carries a per-domain table of asked/answered/open. Compare
    every cell of it — and its total row — against the domain files themselves."""
    problems = []
    rows = question_rows()
    if not rows:
        return ["docs/questions/: no question rows found — has the table format changed?"]
    truth = {}
    for domain, status in rows:
        a, ok, op = truth.get(domain, (0, 0, 0))
        truth[domain] = (a + 1, ok + (status == "✅"), op + (status == "⏳"))

    index = os.path.join(ROOT, "docs/questions.md")
    text = open(index, encoding="utf-8").read()
    seen = set()
    for m in re.finditer(r"\|\s*\[[^\]]+\]\(questions/([a-z-]+)\.md\)\s*\|"
                         r"\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", text):
        domain, said = m.group(1), tuple(int(g) for g in m.group(2, 3, 4))
        seen.add(domain)
        if domain not in truth:
            problems.append(f"docs/questions.md: a row for `{domain}` but no "
                            f"docs/questions/{domain}.md")
        elif said != truth[domain]:
            problems.append(f"docs/questions.md: {domain} says "
                            f"{said[0]}/{said[1]}/{said[2]} (asked/answered/open), "
                            f"the file holds {truth[domain][0]}/{truth[domain][1]}/"
                            f"{truth[domain][2]}")
    for domain in sorted(set(truth) - seen):
        problems.append(f"docs/questions.md: docs/questions/{domain}.md exists and the "
                        f"table has no row for it")

    # A domain file may also state its own tally in prose, and prose is not a table
    # row — docs/questions/networking.md read "Five answered, eight open" for two
    # batches after all thirteen were answered, and the per-domain table above agreed
    # with the files the whole time. The ledger was right and the sentence beside it
    # was not, which is the narrowest possible version of ADR-0008's subject.
    for path in _glob("docs/questions/*.md"):
        domain = os.path.splitext(os.path.basename(path))[0]
        if domain not in truth:
            continue
        asked, answered, still_open = truth[domain]
        prose = open(path, encoding="utf-8").read()
        for m in re.finditer(NUM_EN + r"\s+answered", prose):
            said = as_int(m.group(1))
            if said != answered:
                problems.append(f"docs/questions/{domain}.md: prose says {said} "
                                f"answered, the table holds {answered}")
        for m in re.finditer(NUM_EN + r"\s+open\b", prose):
            said = as_int(m.group(1))
            if said != still_open:
                problems.append(f"docs/questions/{domain}.md: prose says {said} "
                                f"open, the table holds {still_open}")

    totals = tuple(sum(v[i] for v in truth.values()) for i in range(3))
    m = re.search(r"\|\s*\|\s*\*\*(\d+)\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|"
                  r"\s*\*\*(\d+)\*\*\s*\|", text)
    if not m:
        problems.append("docs/questions.md: no total row — the table cannot be checked "
                        "against itself")
    else:
        said = tuple(int(g) for g in m.group(1, 2, 3))
        if said != totals:
            problems.append(f"docs/questions.md: the total row says "
                            f"{said[0]}/{said[1]}/{said[2]}, the domain files hold "
                            f"{totals[0]}/{totals[1]}/{totals[2]}")
    return problems


def diagram_counts():
    """In-document mermaid diagrams, counted the way the prose claims them: the
    English tree (`.claude/skills/` included — a skill's diagram is in a document),
    and that plus the Chinese mirrors."""
    en = zh = 0
    for rel in markdown_files():
        n = len(re.findall(r"^```mermaid", read(rel), re.M))
        if rel.startswith("docs/zh/"):
            zh += n
        else:
            en += n
    return en, en + zh


def indexed_files():
    """What docs/build-index.py indexes: files carrying front matter, and the record
    count the index actually holds. They differ — mirrors are derived — so a claim
    about one is not a claim about the other."""
    with_fm = sum(1 for rel in markdown_files() if front_matter(read(rel))[0] is not None)
    try:
        recs = json.load(open(os.path.join(ROOT, "docs/index.json"), encoding="utf-8"))
        n = len(recs if isinstance(recs, list) else recs.get("records", recs.get("files", [])))
    except Exception:
        n = with_fm
    return with_fm, n


COUNTS = "docs/counts.json"
# chars before a number token in which a pattern's prefix may sit. Every pattern is a
# few words around {NUM}; the bound is asserted when the table loads.
WINDOW = 80
TOKEN_RE = re.compile(NUM)


def truths():
    """What disk says for each kind in docs/counts.json — a set, because some claims
    are legitimately either of two numbers (with and without the mirrors)."""
    beats = walkthrough_beats()
    labs = find_labs()
    return {
        "walkthroughs": {len(_glob("walkthrough/[0-9]*-*.en.md"))},
        "walkthrough beats": set(beats.values()) | {sum(beats.values())},
        "runnable labs": {len(labs)},
        "the-stack labs": {sum(1 for _, argv in labs if argv[0].startswith("the-stack/labs/"))},
        # The flag, not the string: every drill's reporter block mentions --break-it.
        "drills with a break path": {sum(1 for _, argv in labs
                                         if 'add_argument("--break-it"' in read(argv[0]))},
        "cross-cutting notes": {sum(1 for p in _glob("cross-cutting/*.md")
                                    if not p.endswith("/README.md"))},
        "decision records": {len(_glob("docs/adr/[0-9]*.md"))},
        "agent skills": {len(_glob(".claude/skills/*/SKILL.md"))},
        "build-out steps": {len(_glob("build-out/[0-9]*.md"))},
        "questions asked": {len(question_rows())},
        "Chinese mirrors": {len(_glob("docs/zh/**/*.md"))},
        "in-document diagrams": set(diagram_counts()),
        "indexed files": set(indexed_files()),
    }


class Claim:
    """One phrasing that states a count: the pattern as written, and the same pattern
    split at its {NUM} into the prefix that must end where a number token starts and
    the suffix that must begin where it ends. The split is what makes the scan cheap —
    see check_counts."""

    def __init__(self, src):
        self.src = src
        self.full = re.compile(src.replace("{NUM_EN}", NUM_EN).replace("{NUM}", NUM))
        marker = "{NUM_EN}" if "{NUM_EN}" in src else "{NUM}"
        pre, post = src.split(marker, 1)
        if marker == "{NUM_EN}":
            pre += r"(?<![A-Za-z-])"
        self.prefix = re.compile("(?:" + pre + r")\Z")
        self.suffix = re.compile(post)


def count_kinds():
    """[(name, truth, [Claim], [examples])] from docs/counts.json, or raises with the
    reason the table cannot be trusted. The table and the truths must name the same
    kinds, every pattern must carry exactly one {NUM}, and every example must match."""
    with open(os.path.join(ROOT, COUNTS), encoding="utf-8") as fh:
        table = json.load(fh)["kinds"]
    disk = truths()
    names = [k["name"] for k in table]
    if set(names) != set(disk) or len(names) != len(set(names)):
        raise ValueError(f"{COUNTS} names {sorted(names)} but check.py can measure "
                         f"{sorted(disk)} — the two lists must agree")
    out = []
    for kind in table:
        claims = []
        for src in kind["patterns"]:
            if src.count("{NUM") != 1:
                raise ValueError(f"{COUNTS}: {kind['name']!r} pattern {src!r} must carry "
                                 f"exactly one {{NUM}} or {{NUM_EN}}")
            if len(src.replace("{NUM_EN}", "").replace("{NUM}", "")) > WINDOW // 2:
                raise ValueError(f"{COUNTS}: {kind['name']!r} pattern {src!r} is longer than "
                                 f"the search window allows")
            claims.append(Claim(src))
        for example in kind.get("examples", []):
            m = next((m for c in claims for m in [c.full.search(example)] if m), None)
            if m is None:
                raise ValueError(f"{COUNTS}: {kind['name']!r} example {example!r} matches "
                                 f"none of its patterns")
            as_int(m.group(1))
        out.append((kind["name"], disk[kind["name"]], claims, kind.get("examples", [])))
    return out


def check_counts():
    problems = check_questions_ledger()
    try:
        kinds = count_kinds()
    except ValueError as e:
        return problems + [str(e)]
    # Every pattern is prefix + number + suffix, so a match can only sit on a number
    # token. Find the tokens once per file, test every suffix at each token's end with
    # one combined regex (most tokens are dates and table cells and fail it at once),
    # and only then test the prefix and confirm with the whole pattern. Thirty patterns
    # opening with a fifty-way alternation were each scanning the whole corpus before,
    # and that was the entire runtime of this check.
    claims = [(name, truth, c) for name, truth, cs, _ in kinds for c in cs]
    any_suffix = re.compile("|".join(f"(?:{c.suffix.pattern})" for _, _, c in claims))
    for rel in markdown_files():
        # Blank the fences instead of removing them, or every line number after the
        # first code block is a lie.
        blanked = FENCED_BLOCK_RE.sub(lambda m: "\n" * m.group(0).count("\n"), read(rel))
        for tok in TOKEN_RE.finditer(blanked):
            s, e = tok.span()
            if not any_suffix.match(blanked, e):
                continue
            for name, truth, c in claims:
                if not c.suffix.match(blanked, e):
                    continue
                pre = c.prefix.search(blanked, max(0, s - WINDOW), s)
                if pre is None:
                    continue
                m = c.full.match(blanked, pre.start())
                if m is None:
                    continue
                said = as_int(m.group(1))
                if said in truth:
                    continue
                want = " or ".join(str(v) for v in sorted(truth))
                line = blanked[:m.start()].count("\n") + 1
                problems.append(
                    f"{rel}:{line}: says {name} = {said}, disk says {want}"
                    f"   — “{m.group(0).strip()}”")
    return sorted(problems)


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


def report(name, problems, ok_text, t0, failed):
    """One line per in-process check, the same shape the subprocess ones print."""
    dt = time.time() - t0
    if problems:
        failed.append(name)
        print(f"  ✗ {name:<28} {len(problems)} problem(s)   ({dt:.1f}s)")
        for p in problems[:20]:
            print(f"      {p}")
        if len(problems) > 20:
            print(f"      … and {len(problems) - 20} more")
    else:
        print(f"  ✓ {name:<28} {ok_text}   ({dt:.1f}s)")


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
                    help="one of: builders, links, counts, walkthrough, viewer, toolbox, labs")
    args = ap.parse_args()

    wanted = ["builders", "links", "counts", "walkthrough", "viewer", "toolbox", "labs"]
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
            if g == "counts":
                print("  the questions ledger, against the domain files")
                print(f"  the kinds in {COUNTS}, each with the phrasings that state it:")
                for name, truth, _, examples in count_kinds():
                    print(f"  {name:<28} disk says "
                          f"{' or '.join(str(v) for v in sorted(truth))}"
                          f"   — {' · '.join(f'“{e}”' for e in examples)}")
                continue
            if g == "toolbox":
                py, sh = script_files()
                print(f"  {'scripts parse':<28} every .py compiles, every .sh passes bash -n "
                      f"({len(py)} + {len(sh)} files)")
                label, argv = INVENTORY_PRODUCER
                print(f"  {'inventory schema':<28} {' '.join(argv)} → {INVENTORY_SCHEMA} → "
                      + ", ".join(n for n, _ in INVENTORY_CONSUMERS))
                print(f"  – {INVENTORY_NOT_RUN[0]:<28} {INVENTORY_NOT_RUN[1]}")
                continue
            for name, argv in GROUPS[g]():
                print(f"  {name:<28} {' '.join(argv)}")
            if g == "labs":
                print(f"  {'reporter block':<28} every drill above carries it byte for byte")
                for rel, why in SHELL_DRILLS.items():
                    print(f"  – {os.path.basename(rel):<26} {why}")
                if args.only == "labs":
                    print("\n  the block, as check.py holds it:\n")
                    for line in DRILL_BLOCK.rstrip("\n").split("\n"):
                        print(f"    {line}" if line else "")
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
        if g == "counts":
            t0 = time.time()
            problems = check_counts()
            ran += 1
            if problems:
                failed.append("counts")
                print(f"  ✗ stated counts                {len(problems)} disagree with disk"
                      f"   ({time.time() - t0:.1f}s)")
                for p in problems[:20]:
                    print(f"      {p}")
                if len(problems) > 20:
                    print(f"      … and {len(problems) - 20} more")
            else:
                n = len(count_kinds())
                print(f"  ✓ stated counts                {n} kinds agree with disk"
                      f"   ({time.time() - t0:.1f}s)")
            continue
        if g == "toolbox":
            t0 = time.time()
            problems, n = check_scripts_parse()
            ran += 1
            report("scripts parse", problems, f"{n} files parse", t0, failed)
            t0 = time.time()
            problems = check_inventory_schema()
            ran += 1
            report("inventory schema", problems,
                   "fixture document validates, both consumers read it", t0, failed)
            print(f"  – {INVENTORY_NOT_RUN[0]:<28} {INVENTORY_NOT_RUN[1]}")
            continue
        if g == "labs":
            t0 = time.time()
            problems = check_drill_block()
            ran += 1
            report("reporter block", problems,
                   f"{len(find_labs())} drills carry it byte for byte", t0, failed)
            for rel, why in SHELL_DRILLS.items():
                print(f"  – {os.path.basename(rel):<28} {why}")
            _, not_run = scan_labs()
            for nm, path, why in not_run:
                print(f"  – {nm:<28} not run — {why}")
                print(f"      {path}")
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
