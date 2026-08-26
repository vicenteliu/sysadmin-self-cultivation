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

Standard library only, and idempotent: two runs produce byte-identical output.

Exit codes: 0 ok · 1 a source is malformed · 2 --check found a derived file out of date.
"""
import os, re, sys

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
              f"skin matches the profile")
        return 0

    for path, text in sorted(wanted.items()):
        open(path, "w", encoding="utf-8").write(text)
    print(f"wrote {len(wanted)} derived files from {len(slugs())} sources")
    return 0


if __name__ == "__main__":
    sys.exit(main())
