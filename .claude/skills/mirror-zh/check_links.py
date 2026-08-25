#!/usr/bin/env python3
"""Resolve every relative Markdown link in the repo and report the dead ones.

Dead relative links are the failure mode the mirror-zh skill exists to prevent,
and the depth math is where it goes wrong. Don't eyeball it — run this.

    python3 .claude/skills/mirror-zh/check_links.py

Exit code is 1 when anything is dead, so it works as a gate. It always prints
how many links it actually resolved: "0 dead" out of 4 links checked is not the
same result as "0 dead" out of 1403, and only the count tells them apart.
"""
import os
import re
import sys
from glob import glob

LINK = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
EXTERNAL = ('http://', 'https://', 'mailto:', '#', '<')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

# Skipped on purpose, and said out loud rather than left to a glob quirk: .claude/
# holds the skills, and their prose carries placeholder targets like `](rel/path)`
# that are meant to be filled in, not resolved. Everything published is in scope.
SKIP_DIRS = ('.git', '.claude')


def markdown_files():
    for here, dirs, names in os.walk('.'):
        dirs[:] = [d for d in sorted(dirs)
                   if os.path.relpath(os.path.join(here, d), '.') not in SKIP_DIRS]
        for name in sorted(names):
            if name.endswith('.md'):
                yield os.path.relpath(os.path.join(here, name), '.')


def main():
    os.chdir(ROOT)
    dead, checked, files = [], 0, 0
    for path in markdown_files():
        files += 1
        here = os.path.dirname(path)
        with open(path, encoding='utf-8', errors='replace') as fh:
            for lineno, line in enumerate(fh, 1):
                for match in LINK.finditer(line):
                    target = match.group(1).strip().split('#')[0].strip()
                    if not target or target.startswith(EXTERNAL):
                        continue
                    checked += 1
                    resolved = os.path.normpath(os.path.join(here, target))
                    if not os.path.exists(resolved):
                        dead.append((path, lineno, target, resolved))

    print(f'{files} markdown files · {checked} relative links resolved · {len(dead)} dead'
          f'   (skipped: {", ".join(SKIP_DIRS)})')
    for path, lineno, target, resolved in dead:
        print(f'\n{path}:{lineno}')
        print(f'    link      {target}')
        print(f'    resolves  {resolved}   (missing)')
        # Where the target actually lives, so the fix is measured and not computed.
        name = os.path.basename(resolved.rstrip('/'))
        found = [c for c in glob(f'**/{name}', recursive=True) if not c.startswith('.git/')]
        for cand in found[:6]:
            rel = os.path.relpath(cand, os.path.dirname(path))
            if os.path.isdir(cand):
                rel += '/'
            print(f'    on disk   {rel}')
        if not found:
            print('    on disk   (nothing by that name — the target may be gone)')
    return 1 if dead else 0


if __name__ == '__main__':
    sys.exit(main())
