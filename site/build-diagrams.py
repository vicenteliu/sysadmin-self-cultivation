#!/usr/bin/env python3
"""Derive every hero-diagram artifact from its one hand-authored light source.

    python3 site/build-diagrams.py                   # write the dark HTML and all the SVGs
    python3 site/build-diagrams.py --check           # verify; write nothing
    python3 site/build-diagrams.py --install-profile # put the brass skin where the plugin looks

A hero diagram is authored **once**, as `site/assets/diagrams/<slug>.html` in the light
skin. Everything else is derived:

    <slug>.html        hand-authored — the source, and the only file to edit
    <slug>.dark.html   derived — the same geometry with the dark half of the skin
    <slug>.light.svg   derived — standalone SVG, what Markdown embeds
    <slug>.dark.svg    derived

Writing the dark variant by hand was the obvious alternative and it is the wrong one:
two copies of four hundred lines of coordinates, differing only in ten hex values, is
exactly the hand-maintained second copy this repo refuses everywhere else — the same
reasoning that makes `docs/index.json` generated and the Chinese mirrors derived
(ADR-0001). Edit the light file; run this; commit what falls out.

The skin itself is `site/assets/diagrams/sysadmin-brass.profile.md`, committed here
because diagram-design resolves profiles out of the user's home directory: a clone
carries the `.diagram-design` marker but not the skin it names. `--install-profile`
copies it into place; `--check` verifies the token table below still derives exactly
what that profile declares, and says so when the installed copy has drifted from it.

`--check` also holds every number drawn into a figure to the retrieval index. A count in
a drawing is a fact that cannot re-derive itself on load, and the first one here went
stale the same afternoon it was drawn. And it estimates whether each label still fits
inside its box, because four figures shipped with text over an edge and every one of them
was found by eye, late.

Standard library only, and idempotent: two runs produce byte-identical output.

Exit codes: 0 ok · 1 a source is malformed · 2 --check found a derived file out of date.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIAGRAMS = os.path.join(ROOT, "site", "assets", "diagrams")
PROFILE = os.path.join(DIAGRAMS, "sysadmin-brass.profile.md")
MARKER = os.path.join(ROOT, ".diagram-design")
LIBRARY = os.path.expanduser("~/.diagram-design/profiles")

# Light → dark, applied in ONE pass. Sequential replacement would be wrong: paper
# becomes soot and ink becomes paper, so a second pass would recolour what the first
# just wrote.
SKIN = {
    "#faf8f4": "#1a1a17",   # paper        → soot
    "#f0ece4": "#25241f",   # paper-2
    "#ffffff": "#25241f",   # the white lift under a step node
    "#26262b": "#faf8f4",   # ink          → bone
    "#5d5a52": "#b8b2a6",   # muted
    "#8a8479": "#8f887c",   # soft
    "#c9c2b4": "rgba(201,194,180,0.25)",   # rule-solid
    "#a8763e": "#c99a5b",   # accent       → brass, lifted to read on soot
    "#4a6b8a": "#7fa3c4",   # link
    "rgba(38,38,43,":   "rgba(250,248,244,",   # ink washes and hairlines
    # The accent tint is deliberately a touch stronger on soot, so the full string is
    # mapped before the prefix rule (SKIN_RE is sorted longest-first).
    "rgba(168,118,62,0.08)": "rgba(201,154,91,0.10)",
    "rgba(168,118,62,": "rgba(201,154,91,",    # any other accent tint
    "rgba(93,90,82,":   "rgba(184,178,166,",   # muted washes
}
SKIN_RE = re.compile("|".join(re.escape(k) for k in
                     sorted(SKIN, key=len, reverse=True)), re.IGNORECASE)

SVG_RE = re.compile(r"<svg\b.*?</svg>", re.DOTALL)

# `| `paper` | Page background, default node fill | `#faf8f4` (bone) | `#1a1a17` (soot) |`
ROLE_ROW = re.compile(r"^\| `([a-z0-9-]+)` \| [^|]*\| `([^`]+)`[^|]*\| `([^`]+)`[^|]*\|\s*$")
SLUG_RE = re.compile(r"\Aprofile: ([a-z0-9][a-z0-9-]{0,63})\s*\Z")

# `<text … data-axis="platforms">60 DOCS</text>` — a number baked into a drawing, tagged
# with what it counts so it can be held to it.
BAKED_COUNT = re.compile(r'data-axis="([a-z-]+)"[^>]*>(\d+) DOCS')

# A box with a stroke is a node; a stroke-less rect is a label mask and is meant to be
# tight around its text. Only nodes are checked for text spilling out of them.
NODE_BOX = re.compile(r'<rect x="(-?\d+)" y="(-?\d+)" width="(\d+)" height="(\d+)"[^>]*stroke="(?!none)')
SVG_TEXT = re.compile(r'<text x="(-?\d+)" y="(-?\d+)"([^>]*)>([^<]*)</text>')
FONT_SIZE = re.compile(r'font-size="([\d.]+)"')
FONT_FAMILY = re.compile(r"font-family=\"'([^']+)'")
TRACKING = re.compile(r'letter-spacing="([\d.]+)em"')
BOX_PADDING = 8      # what the type reference asks be left inside a node
SLACK = 2            # the estimator's own noise, measured against the seven live figures

# Tokens the SKIN table maps that are not semantic roles: the white lift under a step
# node, and muted-at-10%. Declared so the role check can be strict about the rest.
NOT_ROLES = {"#ffffff", "rgba(93,90,82,"}
FONT_IMPORT = (
    "<style>@import url('https://fonts.googleapis.com/css2?"
    "family=Instrument+Serif:ital@0;1&amp;family=Geist:wght@400;500;600"
    "&amp;family=Geist+Mono:wght@400;500;600&amp;display=swap');</style>"
)


def profile_slug():
    """The slug the committed marker selects. One line, strict grammar, untrusted input."""
    try:
        match = SLUG_RE.match(open(MARKER, encoding="utf-8").read())
    except OSError:
        return None
    return match.group(1) if match else None


def profile_roles(text):
    """The `### Semantic roles` table as {role: (light, dark)}."""
    roles, inside = {}, False
    for line in text.split("\n"):
        if line.startswith("| Role | Purpose |"):
            inside = True
            continue
        if inside:
            if not line.startswith("|"):
                break
            row = ROLE_ROW.match(line)
            if row:
                roles[row.group(1)] = (row.group(2), row.group(3))
    return roles


def skin_problems():
    """Does the light-to-dark table still say what the style profile says?

    This is the skew the artifact check cannot see. Comparing a source with what was
    derived from it proves the deriver ran; it proves nothing about whether the deriver
    is using the right colours. Running each role's light value through the same
    substitution the documents get, and demanding the profile's dark value back, does.
    """
    try:
        text = open(PROFILE, encoding="utf-8").read()
    except OSError:
        return [f"{os.path.relpath(PROFILE, ROOT)} is missing — the skin has no source"]

    roles = profile_roles(text)
    if not roles:
        return [f"{os.path.relpath(PROFILE, ROOT)} has no `### Semantic roles` table"]

    problems = []
    for role, (light, dark) in sorted(roles.items()):
        got = SKIN_RE.sub(lambda m: SKIN[m.group(0).lower()], light)
        if got != dark:
            problems.append(f"role `{role}`: profile says {light} -> {dark}, "
                            f"the SKIN table derives {got}")

    covered = {k for k in SKIN if k not in NOT_ROLES}
    declared = {light for light, _ in roles.values()}
    for key in sorted(covered - declared):
        if not any(d.startswith(key) for d in declared):
            problems.append(f"SKIN maps {key}, which is neither a role nor declared in NOT_ROLES")
    return problems


def baked_count_problems():
    """Do the numbers drawn into a figure still match the repo they describe?

    A figure that states a count is stating a fact, and a fact drawn into an SVG cannot
    be re-derived on load the way the home page's can. This one went stale within a
    single afternoon: the axis map was drawn saying 19 documents under start-here, and
    the tenth Agent Skill — added two commits later — made it 20, so the site rendered
    the figure directly above a live count that disagreed with it.

    Deriving the artifacts proves the deriver ran. This proves the drawing is true.
    """
    index_path = os.path.join(ROOT, "docs", "index.json")
    try:
        files = json.load(open(index_path, encoding="utf-8"))["files"]
    except OSError:
        return ["docs/index.json is missing — run docs/build-index.py"]

    live = {}
    for path, record in files.items():
        if record.get("derived") or not path.endswith(".md"):
            continue
        live[record.get("axis", "")] = live.get(record.get("axis", ""), 0) + 1

    problems = []
    for slug in slugs():
        source = os.path.join(DIAGRAMS, f"{slug}.html")
        for axis, drawn in BAKED_COUNT.findall(open(source, encoding="utf-8").read()):
            if int(drawn) != live.get(axis, 0):
                problems.append(f"{slug}.html draws {drawn} documents for `{axis}`, "
                                f"the retrieval index has {live.get(axis, 0)}")
    return problems


def text_width(content, attrs):
    """Estimate a run's rendered width. Rough, and it does not need to be better.

    Advance widths differ per glyph and per face; what is being caught here is a label
    that overshoots its box by tens of pixels, not one that overshoots by one. Measured
    against the figures in this repo, per-character advance is about 0.60em for the mono
    face, 0.52em for the sans and 0.46em for the serif.
    """
    size = FONT_SIZE.search(attrs)
    size = float(size.group(1)) if size else 12.0
    family = FONT_FAMILY.search(attrs)
    family = family.group(1) if family else "Geist"
    advance = 0.60 if "Mono" in family else (0.46 if "Serif" in family else 0.52)
    tracking = TRACKING.search(attrs)
    return len(content) * size * (advance + (float(tracking.group(1)) if tracking else 0.0))


def overflow_problems():
    """Does any label run outside the box that is supposed to contain it?

    Four figures shipped with text over the edge of a node before anyone looked closely
    at a rendered SVG, and every one was found by eye, late. The arithmetic is simple
    enough to do at check time: estimate the run's width, find the smallest stroked box
    whose interior contains its baseline, and complain when the run leaves that interior.
    """
    problems = []
    for slug in slugs():
        source = os.path.join(DIAGRAMS, f"{slug}.html")
        text = open(source, encoding="utf-8").read()
        boxes = [tuple(int(v) for v in m.groups()) for m in NODE_BOX.finditer(text)]

        for match in SVG_TEXT.finditer(text):
            x, y, attrs, content = int(match.group(1)), int(match.group(2)), match.group(3), match.group(4)
            if not content.strip():
                continue
            width = text_width(content, attrs)
            if 'text-anchor="middle"' in attrs:
                left = x - width / 2
            elif 'text-anchor="end"' in attrs:
                left = x - width
            else:
                left = x

            box = None
            for bx, by, bw, bh in boxes:
                if by < y < by + bh and bx <= x <= bx + bw and (box is None or bw < box[2]):
                    box = (bx, by, bw, bh)
            if box is None:
                continue

            spill = max(box[0] + BOX_PADDING - left, left + width - (box[0] + box[2] - BOX_PADDING))
            if spill > SLACK:
                problems.append(f"{slug}.html: \"{content[:52]}\" runs {spill:.0f}px "
                                f"outside its {box[2]}px box")
    return problems


def installed_profile_state(slug):
    """Whether the machine-local profile library agrees with the committed copy."""
    if slug is None:
        return "the .diagram-design marker is missing or malformed"
    path = os.path.join(LIBRARY, f"{slug}.md")
    if not os.path.exists(path):
        return f"not installed — run site/build-diagrams.py --install-profile"
    committed = open(PROFILE, encoding="utf-8").read()
    if open(path, encoding="utf-8").read() != committed:
        return f"{path} differs from the committed copy"
    return None


def install_profile(force=False):
    """Put the committed profile where diagram-design resolves it from.

    diagram-design keeps profiles in the user's home directory by design, so a clone
    carries the marker but not the skin it names. The repo therefore holds the profile
    as an ordinary file, and this copies it into place.
    """
    slug = profile_slug()
    if slug is None:
        print("the .diagram-design marker is missing or malformed", file=sys.stderr)
        return 1
    body = open(PROFILE, encoding="utf-8").read()
    os.makedirs(LIBRARY, exist_ok=True)
    target = os.path.join(LIBRARY, f"{slug}.md")
    if os.path.exists(target) and not force:
        if open(target, encoding="utf-8").read() == body:
            print(f"{target} already matches the committed profile")
            return 0
        print(f"{target} exists and differs — pass --force to overwrite it", file=sys.stderr)
        return 1
    open(target, "w", encoding="utf-8").write(body)
    print(f"installed {slug} -> {target}")
    return 0


def slugs():
    return sorted(name[:-5] for name in os.listdir(DIAGRAMS)
                  if name.endswith(".html") and ".dark." not in name)


def to_dark(html, slug):
    """Swap the skin, and re-prefix the accessible-name ids for this variant.

    Two exported SVGs inlined in one page must not share `<title>` ids, or the second
    figure can be announced with the first one's name — hence `<slug>-dark-title`.
    """
    dark = SKIN_RE.sub(lambda m: SKIN[m.group(0).lower()], html)
    for role in ("title", "desc"):
        dark = dark.replace(f"{slug}-{role}", f"{slug}-dark-{role}")
    return dark


def to_svg(html, source_name):
    """Lift the diagram out of its editorial wrapper as a standalone, well-formed SVG."""
    match = SVG_RE.search(html)
    if not match:
        raise ValueError(f"{source_name}: no <svg> block")
    svg = match.group(0)
    if 'xmlns="http://www.w3.org/2000/svg"' not in svg:
        raise ValueError(f"{source_name}: <svg> has no xmlns")
    if "viewBox" not in svg:
        raise ValueError(f"{source_name}: <svg> has no viewBox")
    # Merge the font import into the existing <defs> rather than opening a second one.
    svg = svg.replace("<defs>", f"<defs>\n        {FONT_IMPORT}", 1)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + svg + "\n"


def build():
    wanted = {}
    for slug in slugs():
        source = os.path.join(DIAGRAMS, f"{slug}.html")
        light = open(source, encoding="utf-8").read()
        dark = to_dark(light, slug)
        wanted[os.path.join(DIAGRAMS, f"{slug}.dark.html")] = dark
        wanted[os.path.join(DIAGRAMS, f"{slug}.light.svg")] = to_svg(light, f"{slug}.html")
        wanted[os.path.join(DIAGRAMS, f"{slug}.dark.svg")] = to_svg(dark, f"{slug}.dark.html")
    return wanted


def main():
    if "--install-profile" in sys.argv:
        return install_profile(force="--force" in sys.argv)

    if not os.path.isdir(DIAGRAMS):
        print(f"no diagram directory at {DIAGRAMS}", file=sys.stderr)
        return 1
    try:
        wanted = build()
    except ValueError as err:
        print(err, file=sys.stderr)
        return 1

    if "--check" in sys.argv:
        problems = overflow_problems()
        if problems:
            print("a label does not fit the box it belongs to:", file=sys.stderr)
            for problem in problems:
                print(f"  {problem}", file=sys.stderr)
            return 2

        problems = baked_count_problems()
        if problems:
            print("a figure states a count the repo no longer has:", file=sys.stderr)
            for problem in problems:
                print(f"  {problem}", file=sys.stderr)
            return 2

        problems = skin_problems()
        if problems:
            print("the SKIN table no longer matches the style profile:", file=sys.stderr)
            for problem in problems:
                print(f"  {problem}", file=sys.stderr)
            return 2
        stale = [p for p, text in wanted.items()
                 if (open(p, encoding="utf-8").read() if os.path.exists(p) else "") != text]
        if stale:
            for path in sorted(stale):
                print(f"{os.path.relpath(path, ROOT)} is stale — run site/build-diagrams.py",
                      file=sys.stderr)
            return 2
        state = installed_profile_state(profile_slug())
        if state:
            print(f"note: the installed style profile is {state}", file=sys.stderr)
        print(f"diagrams current — {len(slugs())} sources, {len(wanted)} derived files, "
              f"skin matches the profile, drawn counts match the index, labels fit")
        return 0

    for path, text in sorted(wanted.items()):
        open(path, "w", encoding="utf-8").write(text)
    print(f"wrote {len(wanted)} derived files from {len(slugs())} sources")
    return 0


if __name__ == "__main__":
    sys.exit(main())
