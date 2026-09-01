#!/usr/bin/env python3
"""Check a walkthrough against its floor, its sources, and its own format.

    python3 walkthrough/build-walkthrough.py            # report, exit 0 unless broken
    python3 walkthrough/build-walkthrough.py --check    # same, for CI
    python3 walkthrough/build-walkthrough.py --freeze 01-the-network
                                                        # stamp published: + source fingerprints

Nothing here is generated. A walkthrough has no derived artifact — the script IS the
TTS input (ADR-0009) — so this script only ever reports. What it guards:

  beats      the two language scripts carry the same beat ids in the same order, the
             floor cues only real beats, and the first beat carries a full state
  anchors    every prop anchor is a real heading in a real file, checked by rebuilding
             GitHub's slug from the heading text rather than trusting the fragment
  speakable  the spoken text holds no tables, links, code spans, emphasis or asides —
             things a speech engine either reads aloud as noise or silently drops
  frozen     once `published:` is set, the `sources:` fingerprints must still match;
             a mismatch means the recording is now describing a document that moved,
             which is the only reliable signal that an episode needs re-recording

Standard library only, like everything else that runs in this repo.
"""

import hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

BEAT_RE = re.compile(r"^<!--\s*beat:\s*([a-z0-9][a-z0-9-]*)\s*-->\s*$", re.M)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.M)
FENCE_RE = re.compile(r"^```", re.M)

# The spoken text is read by a machine and heard by a person. Each of these is either
# read out as noise or dropped silently, and both failures are invisible on the page.
UNSPEAKABLE = [
    (re.compile(r"^\s*\|"),        "a table row"),
    (re.compile(r"\]\("),          "an inline link"),
    (re.compile(r"`"),             "a code span"),
    (re.compile(r"\*\*"),          "bold emphasis"),
    (re.compile(r"^\s*[-*+]\s"),   "a list item"),
    (re.compile(r"[（(][^)）]{6,}[)）]"), "a parenthetical aside"),
    (re.compile(r"[~<>]"),          "a character a speech engine will not say"),
]


def slug(text):
    """GitHub's heading slug: drop anything that is not a word character, a space or a
    hyphen, lowercase, then spaces to hyphens. Emoji and dashes vanish and leave their
    surrounding spaces behind, which is why real anchors carry doubled and trailing
    hyphens — reproducing that is the whole point of deriving it instead of guessing."""
    out = []
    for ch in text:
        if ch.isalnum() or ch in "-_ ":
            out.append(ch.lower())
    return "".join(out).replace(" ", "-")


def front_matter(text):
    """The same minimal YAML docs/build-index.py accepts: scalars, quoted strings and
    inline lists. Nested structures are deliberately not supported anywhere in this repo."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    fm = {}
    for line in text[4:end].split("\n"):
        if not line.strip() or ":" not in line:
            continue
        key, _, raw = line.partition(":")
        raw = raw.strip()
        if raw.startswith("[") and raw.endswith("]"):
            fm[key.strip()] = [v.strip() for v in raw[1:-1].split(",") if v.strip()]
        elif len(raw) >= 2 and raw[0] == raw[-1] == '"':
            fm[key.strip()] = raw[1:-1]
        else:
            fm[key.strip()] = raw
    return fm, text[end + 5:]


def fingerprint(path):
    with open(os.path.join(ROOT, path), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:16]


def spoken_lines(body):
    """Every line that a speech engine would receive: not the title, not a beat marker,
    not a fenced block."""
    out, fenced = [], False
    for n, line in enumerate(body.split("\n"), 1):
        if FENCE_RE.match(line):
            fenced = not fenced
            continue
        if fenced or not line.strip():
            continue
        if line.startswith("#") or BEAT_RE.match(line + "\n"):
            continue
        out.append((n, line))
    return out


def check_script(path, problems):
    """Beat ids in order, plus the format rules. Returns (front_matter, [beat ids])."""
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    text = open(path, encoding="utf-8").read()
    fm, body = front_matter(text)
    if fm is None:
        problems.append(f"{rel}: no front matter")
        return {}, []

    beats = BEAT_RE.findall(body)
    if not beats:
        problems.append(f"{rel}: no beats — a walkthrough is made of beats")
    seen = set()
    for beat in beats:
        if beat in seen:
            problems.append(f"{rel}: beat `{beat}` appears twice — ids are names, and names are unique")
        seen.add(beat)
    if re.fullmatch(r"beat-\d+", " ".join(beats).split(" ")[0] if beats else "x"):
        problems.append(f"{rel}: beat ids look like ordinals — an inserted paragraph would shift every cue")

    for n, line in spoken_lines(body):
        for pattern, why in UNSPEAKABLE:
            if pattern.search(line):
                problems.append(f"{rel}:{n}: spoken text contains {why}")
                break

    for src in fm.get("sources", []):
        if not os.path.exists(os.path.join(ROOT, src)):
            problems.append(f"{rel}: sources names `{src}`, which does not exist")

    published = (fm.get("published") or "").strip()
    if published:
        stamped = fm.get("fingerprints", [])
        stamped = dict(p.split("=", 1) for p in stamped if "=" in p)
        for src in fm.get("sources", []):
            if not os.path.exists(os.path.join(ROOT, src)):
                continue
            now, was = fingerprint(src), stamped.get(src)
            if was is None:
                problems.append(f"{rel}: published {published} but `{src}` was never fingerprinted")
            elif now != was:
                problems.append(
                    f"{rel}: `{src}` has moved since this was published on {published} "
                    f"({was} → {now}) — the recording now describes a document that changed")
    return fm, beats


def check_floor(floor_path, scripts, problems):
    rel = os.path.relpath(floor_path, ROOT).replace(os.sep, "/")
    floor = json.load(open(floor_path, encoding="utf-8"))

    # Geometry lives in the plate, shared by every walkthrough; the walkthrough carries
    # and cues. Reaching for a missing plate must fail loudly — the first version of
    # this split passed in silence because an absent `stage` read as an empty one.
    plate_name = floor.get("plate")
    if not plate_name:
        problems.append(f"{rel}: names no plate — a walkthrough draws a floor it does not own")
        return floor, []
    plate_path = os.path.join(HERE, plate_name)
    if not os.path.exists(plate_path):
        problems.append(f"{rel}: names plate `{plate_name}`, which does not exist")
        return floor, []
    stage = json.load(open(plate_path, encoding="utf-8"))
    prel = os.path.relpath(plate_path, ROOT).replace(os.sep, "/")

    topo = stage.get("topology") or {}
    if not topo.get("fingerprint"):
        problems.append(f"{prel}: has never been proved — run tools/floor/prove-topology.py --stamp")

    for group in ("rooms", "spaces", "booths"):
        for o in stage.get(group, []):
            d = o.get("door")
            if not d or d.get("side") not in ("n", "s", "e", "w"):
                problems.append(f"{prel}: `{o['id']}` has no door — a sealed room is not a room")

    ordered = None
    for script_rel, beats in scripts.items():
        if ordered is None:
            ordered = (script_rel, beats)
        elif beats != ordered[1]:
            only_a = [b for b in ordered[1] if b not in beats]
            only_b = [b for b in beats if b not in ordered[1]]
            if only_a or only_b:
                problems.append(
                    f"{script_rel} and {ordered[0]} do not carry the same beats — "
                    f"only in {ordered[0]}: {only_a[:4]}; only in {script_rel}: {only_b[:4]}")
            else:
                problems.append(f"{script_rel} and {ordered[0]} carry the same beats in a different order")
    all_beats = ordered[1] if ordered else []

    for beat in floor.get("beats", {}):
        if beat not in all_beats:
            problems.append(f"{rel}: cues beat `{beat}`, which no script contains")
    if all_beats and all_beats[0] not in floor.get("beats", {}):
        problems.append(f"{rel}: the first beat `{all_beats[0]}` has no state — "
                        f"later beats may inherit, the first cannot")
    first = floor.get("beats", {}).get(all_beats[0] if all_beats else "", {})
    for field in ("zoom", "cast", "focus", "highlight"):
        if field not in first:
            problems.append(f"{rel}: the first beat's state is missing `{field}`")

    prop_ids = {p["id"] for p in floor.get("props", [])}
    known = prop_ids | {r["id"] for r in stage.get("rooms", [])} \
                     | {b["id"] for b in stage.get("booths", [])} \
                     | {s["id"] for s in stage.get("spaces", [])} \
                     | {s["id"] for s in stage.get("segments", [])}
    for beat, state in floor.get("beats", {}).items():
        for target in (state.get("highlight") or []):
            if target not in known:
                problems.append(f"{rel}: beat `{beat}` highlights `{target}`, which is not on the stage")
        focus = state.get("focus")
        if focus and focus not in known:
            problems.append(f"{rel}: beat `{beat}` focuses `{focus}`, which is not on the stage")

    # A `plan` prop marks an idea, not a place — addressing, authentication, a decision.
    # Walkthroughs one and two both put theirs on open floor, and that is not decoration:
    # a marker for an idea drawn inside a meeting room reads as a claim about that room.
    # Walkthrough three landed one on top of `room-medium-2` and the pantry at once, and
    # nothing here noticed, because ids and anchors were checked and placement was not.
    boxes = [(o["id"], o["rect"]) for group in ("rooms", "spaces", "booths")
             for o in stage.get(group, [])]
    for prop in floor.get("props", []):
        if prop.get("kind") != "plan":
            continue
        x, y = prop.get("at", (None, None))
        if x is None:
            continue
        inside = [pid for pid, (rx, ry, rw, rh) in boxes
                  if rx <= x < rx + rw and ry <= y < ry + rh]
        if inside:
            problems.append(f"{rel}: plan prop `{prop['id']}` sits inside "
                            f"{', '.join(f'`{i}`' for i in inside)} — a plan marks an idea "
                            f"and belongs on open floor, or it reads as a claim about the room")

    declared = stage.get("desks", {}).get("total")
    counted = sum(p.get("seats", 0) for p in stage.get("desks", {}).get("pods", []))
    if declared is None:
        problems.append(f"{prel}: states no desk total — the count is a fact and has to be stated")
    elif declared != counted:
        problems.append(f"{prel}: desks declare {declared} but the pods hold {counted} — "
                        f"a number on screen must be the number in the document")

    headings = {}
    for prop in floor.get("props", []):
        for anchor in prop.get("anchors", []):
            path = anchor["path"]
            full = os.path.join(ROOT, path)
            if not os.path.exists(full):
                problems.append(f"{rel}: prop `{prop['id']}` points at `{path}`, which does not exist")
                continue
            if path not in headings:
                text = open(full, encoding="utf-8").read()
                headings[path] = {slug(h) for _, h in HEADING_RE.findall(text)}
            if anchor["frag"] not in headings[path]:
                near = [h for h in headings[path] if anchor["frag"][:12] in h]
                hint = f" — did you mean `{near[0]}`?" if near else ""
                problems.append(f"{rel}: prop `{prop['id']}` anchors `{path}#{anchor['frag']}`, "
                                f"which is not a heading there{hint}")

    for prop in floor.get("props", []):
        if prop.get("sameAs"):
            if prop["sameAs"] not in prop_ids:
                problems.append(f"{rel}: prop `{prop['id']}` is sameAs `{prop['sameAs']}`, which does not exist")
            continue
        for field in ("why", "criteria", "anchors"):
            if not prop.get(field):
                problems.append(f"{rel}: prop `{prop['id']}` has no `{field}` — "
                                f"a panel shows the judgement and the criteria, or it shows nothing")
    return floor, all_beats


def walkthroughs():
    for name in sorted(os.listdir(HERE)):
        if name.endswith(".floor.json"):
            yield name[: -len(".floor.json")]


def freeze(slug_name):
    """Stamp published: and the source fingerprints. After this the script is not edited;
    an error becomes an erratum, because the recording cannot be amended."""
    import datetime
    changed = []
    for lang in ("zh", "en"):
        path = os.path.join(HERE, f"{slug_name}.{lang}.md")
        if not os.path.exists(path):
            continue
        text = open(path, encoding="utf-8").read()
        fm, _ = front_matter(text)
        today = datetime.date.today().isoformat()
        prints = " ".join(f"{s}={fingerprint(s)}" for s in fm.get("sources", []))
        text = re.sub(r"^published:.*$", f"published: {today}", text, count=1, flags=re.M)
        if "fingerprints:" in text:
            text = re.sub(r"^fingerprints:.*$", f"fingerprints: [{prints.replace(' ', ', ')}]",
                          text, count=1, flags=re.M)
        else:
            text = text.replace(f"published: {today}",
                                f"published: {today}\nfingerprints: [{prints.replace(' ', ', ')}]", 1)
        open(path, "w", encoding="utf-8").write(text)
        changed.append(os.path.basename(path))
    print(f"froze {slug_name}: {', '.join(changed)}")
    print("the scripts are now published — edits become errata, not corrections")


def main():
    args = sys.argv[1:]
    if "--freeze" in args:
        freeze(args[args.index("--freeze") + 1])
        return 0

    problems, counted = [], 0
    for slug_name in walkthroughs():
        scripts = {}
        for lang in ("zh", "en"):
            path = os.path.join(HERE, f"{slug_name}.{lang}.md")
            if not os.path.exists(path):
                problems.append(f"walkthrough/{slug_name}: no `{lang}` script — "
                                f"a walkthrough carries two, and neither is a translation")
                continue
            fm, beats = check_script(path, problems)
            scripts[f"{slug_name}.{lang}.md"] = beats
        floor_path = os.path.join(HERE, f"{slug_name}.floor.json")
        if scripts:
            floor, all_beats = check_floor(floor_path, scripts, problems)
            counted += 1
            cued = len(floor.get("beats", {}))
            print(f"walkthrough/{slug_name} — {len(all_beats)} beats, {cued} cued, "
                  f"{len(floor.get('props', []))} props, {len(scripts)} scripts, "
                  f"plate {floor.get('plate', '—')}")

    if problems:
        print(f"\n{len(problems)} problem{'s' if len(problems) != 1 else ''}:", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        return 1
    print(f"{counted} walkthrough{'s' if counted != 1 else ''} — beats, anchors and format all hold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
