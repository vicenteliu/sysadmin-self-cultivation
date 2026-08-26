---
kind: tool
axis: meta
themes: []
platforms: []
summary: "Inputs: the Markdown already in this repo · Outputs: a browsable, searchable view of it at http://127.0.0.1:8000 · Risk: read-only, localhost-only, and it can only reach files the retrieval index already lists · Root: not needed"
---
# site — the documentation browser

> **Inputs:** the Markdown already in this repo · **Outputs:** a browsable, searchable
> view of it at `http://127.0.0.1:8000` · **Risk:** read-only, binds to localhost, and
> can only reach files [`docs/index.json`](../docs/index.json) already lists ·
> **Root:** not needed

> 🌐 **Languages:** English (default) · [中文](../docs/zh/site/README.md)

Two hundred thousand words is past the size where scrolling a folder works. This is the
same material with navigation, full-text search, a language switcher and rendered
diagrams — and **nothing else**. Every word it shows is a file GitHub also renders; it
is a view, never a place where a fact first appears
([ADR-0005](../docs/adr/0005-the-site-is-a-view-not-a-seventh-axis.md)).

## Run it

Two ways, same files, same URL contract.

```bash
python3 site/serve.py                              # http://127.0.0.1:8000
python3 site/serve.py --port 9000                  # if 8000 is taken

docker compose -f site/docker-compose.yml up       # http://127.0.0.1:8099
```

**Nothing is installed either way.** The direct path is Python standard library only;
`marked` and `mermaid` are committed under `site/vendor/`, so the viewer works offline,
on a plane, and in an air-gapped environment. That is why there is a 2.5 MB bundle in
the tree — the reasoning, and the four options it beat, are in
[ADR-0006](../docs/adr/0006-the-viewer-vendors-its-dependencies.md).

To hand the whole thing to someone with no clone, bake a self-contained image:

```bash
python3 docs/build-index.py && python3 site/build-corpus.py   # freeze current content
docker build -f site/Dockerfile -t sysadmin-docs .            # context is the repo root
docker run --rm -p 8099:8080 sysadmin-docs
```

## What it does

| | |
| --- | --- |
| **Search** | Full text over every document, English and Chinese. `/` focuses the box. |
| **Facets** | The sidebar regroups by axis, platform, theme or kind — the same front-matter the retrieval index is built from. |
| **Languages** | 🌐 swaps a document for its Chinese mirror and the interface with it. A document with no mirror says so instead of silently falling back. |
| **Theme** | Follows the system setting; the toggle overrides it. Mermaid re-renders and hero diagrams swap variants with it. |
| **The route** | `build-out/`'s sixteen steps as a linear track — deliberately not an axis card. |

## What is generated

Three files are derived and committed. Each has a `--check` mode that exits non-zero
when it is behind its source, so staleness is caught rather than discovered.

```bash
python3 docs/build-index.py --check     # docs/index.json  ← every file's front-matter
python3 site/build-corpus.py --check    # titles.json + corpus.json ← the prose
python3 site/build-diagrams.py --check  # 12 diagram artifacts ← 4 HTML sources,
                                        # and the token table ← the style profile
```

The diagram check covers one more thing than staleness. `diagram-design` resolves style
profiles out of `~/.diagram-design/profiles/`, which a clone does not carry, so the skin
is committed here as `assets/diagrams/sysadmin-brass.profile.md`. On a machine that has
never built a diagram in this repo:

```bash
python3 site/build-diagrams.py --install-profile
```

`corpus.json` is the **search corpus** — 1.2 MB of full text, fetched only when someone
searches. It is not an index: [`CONTENTS.md`](../CONTENTS.md) is the human table of
contents, a folder `README.md` is that folder's index, and `docs/index.json` is the
retrieval index. See [`CONTEXT.md`](../CONTEXT.md).

## The URL contract

```
/                             the viewer
/doc/<repo-relative>.md       one document
/doc/docs/index.json          the retrieval index the navigation is built from
```

`serve.py` enforces it with an **allowlist** built from the retrieval index: a path the
index does not list is a 404, so `.git/`, `.serena/` and every non-Markdown file in the
tree stay unreachable even though the repo root is one directory up. `nginx.conf`
implements the same contract by file extension plus a dotfile refusal — looser, because
nginx has no index to consult at request time, and still enough to refuse everything
that matters. A repo that ships a hardening baseline should not ship a viewer that
serves its own `.git` to localhost.

## Layout

```
site/
├── serve.py            the direct path — standard library, allowlisted, localhost
├── build-corpus.py     titles.json + corpus.json
├── build-diagrams.py   the dark HTML and both SVGs, derived from each light source
├── index.html  style.css  strings.json
├── js/                 router · nav · search · render · i18n  (native ES modules)
├── assets/diagrams/    4 hand-authored hero sources + 12 derived files
├── vendor/             marked + mermaid, committed on purpose
├── nginx.conf  docker-compose.yml  Dockerfile
└── titles.json  corpus.json        generated — do not edit
```

## Adding to it

New documents need nothing: write the Markdown with front-matter, run the two builders,
reload. New figures belong to
[`diagram-module`](../.claude/skills/diagram-module/SKILL.md). The one piece of
deployment knowledge the viewer holds is the GitHub URL at the top of
[`js/render.js`](js/render.js), used only for files the allowlist does not serve.

**It is not a server.** It binds to `127.0.0.1`, has no authentication, and serving it
to a network is not a supported mode. To publish, push the static files — the viewer is
plain HTML, CSS and JS, and works from any static host without change.
