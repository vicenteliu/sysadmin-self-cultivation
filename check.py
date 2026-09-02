#!/usr/bin/env python3
"""
check.py — every check this repo has, from one place.

    python3 check.py              # run everything, report, exit non-zero on failure
    python3 check.py --list       # what would run, and nothing else
    python3 check.py --only links # run one group: builders, links, counts, walkthrough, labs, viewer

Until this existed the checks were real and the *list* of them was not: five
builders with `--check` modes, a walkthrough checker, a viewer smoke test and
eleven self-verifying labs, named across four READMEs and remembered by hand. A
check nobody can enumerate is a check that silently stops being run, which is the
same failure ADR-0008 records about a bound written as a count.

Two groups here guard the prose. **Nothing in this repo checked its own internal links**,
and nothing checked the numbers the prose states about itself — see the counts section
below for what that cost.
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
        text = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        text = FENCE_RE.sub("", text)
        text = CODE_RE.sub("", text)
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
    """Beats per walkthrough, read the way build-walkthrough.py reads them: a beat is
    a `<!-- beat: id -->` marker in the English script."""
    out = {}
    for path in _glob("walkthrough/[0-9]*-*.en.md"):
        text = open(path, encoding="utf-8").read()
        out[os.path.basename(path)] = len(re.findall(r"<!--\s*beat:", text))
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


def counted_things():
    """(name, what disk says, [patterns that find the claim in prose]).

    A pattern must anchor to the noun. `二十个` alone appears in a spoken script
    about people; `二十个可跑` is a claim about this repo."""
    beats = walkthrough_beats()
    rows = question_rows()
    return [
        ("walkthroughs", {len(_glob("walkthrough/[0-9]*-*.en.md"))},
         [NUM_EN + r"\s+walkthroughs\b", r"(?:共|目前|已有)\s*" + NUM + r"\s*篇走读"]),
        ("walkthrough beats", set(beats.values()) | {sum(beats.values())},
         [NUM_EN + r"\s+beats\b", NUM + r"\s*拍[，。 ,\n]"]),
        ("runnable labs", {len(find_labs())},
         [NUM_EN + r"[ -]runnable, self-verifying", NUM + r"\s*个可跑、自验证"]),
        ("agent skills", {len(_glob(".claude/skills/*/SKILL.md"))},
         [NUM_EN + r"\s+Agent Skills\b", r"自?带\s*" + NUM + r"\s*个\s*\[?`?\.claude/skills"]),
        # `15 of 16 steps point at a lab` states coverage, not inventory — only the
        # denominator is a claim about how many steps there are.
        ("build-out steps", {len(_glob("build-out/[0-9]*.md"))},
         [r"\bof\s+" + NUM_EN + r"\s+steps\b", r"\*\*" + NUM + r"\s*步全部"]),
        ("questions asked", {len(rows)},
         [NUM_EN + r"\s+questions across\b", r"域" + NUM + r"问"]),
        ("Chinese mirrors", {len(_glob("docs/zh/**/*.md"))},
         [r"docs/zh/`?\s*目前\s*" + NUM + r"\s*篇"]),
    ]


def check_counts():
    problems = check_questions_ledger()
    compiled = [(name, truth, [re.compile(p) for p in pats])
                for name, truth, pats in counted_things()]
    for rel in markdown_files():
        text = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        # Blank the fences instead of removing them, or every line number after the
        # first code block is a lie.
        blanked = FENCE_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
        for name, truth, rxs in compiled:
            for rx in rxs:
                for m in rx.finditer(blanked):
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
                    help="one of: builders, links, counts, walkthrough, viewer, labs")
    args = ap.parse_args()

    wanted = ["builders", "links", "counts", "walkthrough", "viewer", "labs"]
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
                for name, truth, _ in counted_things():
                    print(f"  {name:<28} disk says "
                          f"{' or '.join(str(v) for v in sorted(truth))}")
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
                n = len(counted_things())
                print(f"  ✓ stated counts                {n} kinds agree with disk"
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
