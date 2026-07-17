#!/usr/bin/env python3
"""Assemble a per-shop subset of the toolbox into a standalone pack.

Selection comes from catalog.json (concern + platform tags); the pack keeps the
repo's layout so every relative link and documented command works unchanged.
Skills are included only when everything they reference made it into the pack —
no dangling references. Writes nowhere except --out. See README.md.
"""

import argparse
import datetime
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent  # <repo>/toolbox/generate → <repo>

# Docs that enumerate a whole set travel only when that whole set is selected.
CHARTER = "toolbox/README.md"          # lists every tool → needs all tools + roles
ANSIBLE_README = "toolbox/ansible/README.md"  # lists every role → needs all roles

REPO_URL = "https://github.com/vicenteliu/sysadmin-self-cultivation"


def die(msg, code):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def load_catalog():
    path = HERE / "catalog.json"
    if not path.is_file():
        die(f"catalog not found: {path}", 2)
    with open(path) as f:
        return json.load(f)


def matches(item, concerns, platform):
    if not set(item["concerns"]) & concerns:
        return False
    return platform is None or platform in item["platforms"]


def pick_skills(catalog, tools, roles):
    """Skills whose required tools/roles/skills are all in the pack (fixpoint)."""
    included, skipped = {}, {}
    changed = True
    while changed:
        changed = False
        for name, skill in catalog["skills"].items():
            if name in included:
                continue
            req = skill["requires"]
            missing = [t for t in req["tools"] if t not in tools]
            missing += [r for r in req["roles"] if r not in roles]
            missing += [s for s in req["skills"] if s not in included]
            if missing:
                skipped[name] = missing
            else:
                included[name] = skill
                skipped.pop(name, None)
                changed = True
    return included, skipped


def copy_into(rel, out):
    src, dst = ROOT / rel, out / rel
    if not src.exists():
        die(f"repo is missing {rel} — run from a full checkout", 2)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dst, dirs_exist_ok=True)  # --force re-runs overwrite
    else:
        shutil.copy2(src, dst)


def write_manifest(out, argv_line, concerns, tools, roles, skills, skipped):
    lines = [
        "# Toolbox pack",
        "",
        f"Generated {datetime.date.today()} from [sysadmin-self-cultivation]({REPO_URL})",
        f"by `toolbox/generate` — selection: {', '.join(sorted(concerns))}.",
        "Regenerate with:",
        "",
        "```bash",
        argv_line,
        "```",
        "",
        "## Contents",
        "",
        "| Item | Kind | What it does |",
        "| --- | --- | --- |",
    ]
    for name, t in sorted(tools.items()):
        lines.append(f"| [`{name}`](toolbox/{name}/) | script | {t['summary']} |")
    for name, r in sorted(roles.items()):
        lines.append(
            f"| [`{name}`](toolbox/ansible/roles/{name}/) | Ansible role | {r['summary']} |")
    for name, s in sorted(skills.items()):
        lines.append(
            f"| [`{name}`](.claude/skills/{name}/SKILL.md) | Agent Skill | {s['summary']} |")
    if skipped:
        lines += ["", "Skills left out (they reference tools this pack doesn't carry):"]
        for name, missing in sorted(skipped.items()):
            lines.append(f"- `{name}` — needs {', '.join(missing)}")
    lines += ["", "## Using the pack", ""]
    if tools:
        first = sorted(tools)[0]
        lines.append(f"Run scripts from the pack root, e.g. "
                     f"`./toolbox/{first}/{tools[first]['entry']}` — each tool's own "
                     f"README states inputs, risk level, and exit codes.")
    if roles:
        lines.append(
            "Ansible: `cd toolbox/ansible && ansible-playbook -i inventory.ini "
            "playbooks/<play>.yml --check --diff` first, then without `--check`.")
    if skills:
        lines.append(
            "Skills: run your agent (e.g. Claude Code) from the pack root and the "
            "skills under `.claude/skills/` drive these tools by sentence.")
    lines += [
        "",
        "## The rules that travel with it",
        "",
        "- **Safe by default** — read-only or dry-run unless you pass the explicit",
        "  apply/destructive flag; nothing here changes state casually.",
        "- **Honest scope** — every README keeps its `Tested on:` line. Lab-verified",
        "  is not production-hardened; treat these as working material, not product.",
        "- **Quiet success, loud failure** — exit 0 terse when fine, non-zero with an",
        "  actionable message when not; both humans and agents branch on that.",
        "",
    ]
    (out / "README.md").write_text("\n".join(lines))


def cmd_list(catalog):
    print("concerns:")
    for name, desc in catalog["concerns"].items():
        print(f"  {name:<12} {desc}")
    print("profiles:")
    for name, p in catalog["profiles"].items():
        print(f"  {name:<20} {p['description']} ({', '.join(p['concerns'])})")
    print("items:")
    for kind in ("tools", "roles"):
        for name, item in catalog[kind].items():
            tags = ",".join(item["concerns"])
            plats = ",".join(item["platforms"])
            print(f"  {name:<22} {kind[:-1]:<5} {tags:<20} [{plats}]")
    for name, s in catalog["skills"].items():
        req = s["requires"]
        needs = ", ".join(req["tools"] + req["roles"] + req["skills"])
        print(f"  {name:<22} skill requires: {needs}")


def main():
    ap = argparse.ArgumentParser(
        description="Assemble a per-shop subset of the toolbox.")
    ap.add_argument("--list", action="store_true",
                    help="show concerns, profiles, and catalog, then exit")
    ap.add_argument("--pick", metavar="CONCERNS",
                    help="comma-separated concerns (see --list)")
    ap.add_argument("--profile", metavar="NAME", help="a named selection (see --list)")
    ap.add_argument("--platform", choices=["linux", "macos"],
                    help="additionally keep only items tested on this platform")
    ap.add_argument("--out", metavar="DIR", help="directory to write the pack into")
    ap.add_argument("--force", action="store_true",
                    help="write into an existing non-empty --out")
    args = ap.parse_args()

    catalog = load_catalog()
    if args.list:
        cmd_list(catalog)
        return

    if bool(args.pick) == bool(args.profile):
        die("pick exactly one of --pick or --profile (or use --list)", 2)
    if not args.out:
        die("--out DIR is required", 2)

    if args.profile:
        profile = catalog["profiles"].get(args.profile)
        if not profile:
            die(f"unknown profile '{args.profile}' — profiles: "
                f"{', '.join(catalog['profiles'])}", 1)
        concerns = set(profile["concerns"])
    else:
        concerns = {c.strip() for c in args.pick.split(",") if c.strip()}
        unknown = concerns - set(catalog["concerns"])
        if unknown:
            die(f"unknown concern(s) {', '.join(sorted(unknown))} — concerns: "
                f"{', '.join(catalog['concerns'])}", 1)

    tools = {n: t for n, t in catalog["tools"].items()
             if matches(t, concerns, args.platform)}
    roles = {n: r for n, r in catalog["roles"].items()
             if matches(r, concerns, args.platform)}
    if not tools and not roles:
        die("selection matches nothing — try --list", 1)
    skills, skipped = pick_skills(catalog, tools, roles)

    out = Path(args.out).expanduser()
    if out.exists() and any(out.iterdir()) and not args.force:
        die(f"{out} exists and is not empty (use --force to write anyway)", 2)
    out.mkdir(parents=True, exist_ok=True)

    for t in tools.values():
        copy_into(t["path"], out)
    if roles:
        for rel in catalog["ansible_common"]:
            copy_into(rel, out)
        for r in roles.values():
            copy_into(r["path"], out)
            copy_into(r["playbook"], out)
        if set(roles) == set(catalog["roles"]):
            copy_into(ANSIBLE_README, out)
    for s in skills.values():
        copy_into(s["path"], out)
    if set(tools) == set(catalog["tools"]) and set(roles) == set(catalog["roles"]):
        copy_into(CHARTER, out)

    argv_line = ("toolbox/generate/generate.py "  # runs from a repo checkout
                 + " ".join(sys.argv[1:]))
    write_manifest(out, argv_line, concerns, tools, roles, skills, skipped)

    print(f"pack written: {out} — {len(tools)} tool(s), {len(roles)} role(s), "
          f"{len(skills)} skill(s)")
    for name, missing in sorted(skipped.items()):
        print(f"  skill '{name}' left out (needs {', '.join(missing)})")


if __name__ == "__main__":
    main()
