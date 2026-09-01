---
kind: adr
axis: meta
themes: []
platforms: []
summary: "There is a 2.5 MB minified JavaScript bundle committed to this repository. It is larger than every Markdown file here put together, and it is the single most surprising thing in the tree, so it needs a reason on the record."
---
# The viewer vendors its dependencies instead of adopting a site generator

> 🌐 **Languages:** English (default) · [中文](../zh/docs/adr/0006-the-viewer-vendors-its-dependencies.md)

There is a 2.5 MB minified JavaScript bundle committed to this repository
([`site/vendor/mermaid.min.js`](../../site/vendor/)). It is larger than every Markdown
file here put together, and it is the single most surprising thing in the tree, so it
needs a reason on the record.

The requirement it comes from: the site must start **two ways** — directly, and in a
container — and the direct path must be *one command with nothing installed*.

## Decision

**The viewer is hand-built, has no build step for content, and carries its two runtime
libraries in the tree.** `python3 site/serve.py` is the whole direct path: no `pip
install`, no `npm install`, no network. `docker compose up` serves the same files
through nginx. Markdown renders in the browser; the only generated artifacts are a
titles map and a search corpus, both produced by a standard-library Python script.

## Considered options

- **MkDocs Material.** The strongest alternative, and the one to reach for if this
  decision is ever revisited: Python-native, which matches a repo that is already
  Markdown plus Python plus shell, with search, navigation, i18n and dark mode for
  free, and an official container image. Rejected on one structural mismatch and one
  consequence. The mismatch: the canonical documents live at the repo root and across
  six sibling directories, and MkDocs wants a single `docs_dir` — which means a staging
  copy on every run, so "direct launch" acquires a build step. The consequence: the
  home page would become a theme's idea of a home page, and the axis map, the route
  view and the mirror-coverage badge would each be a fight with a template.

- **VitePress or Docusaurus.** More capable than either option here. Rejected because
  `node_modules` in a repo whose every other runnable artifact is standard-library
  Python or POSIX shell is a bigger foreign body than one committed bundle — and it
  fails the same zero-install test, harder.

- **Load the libraries from a CDN.** The obvious way to avoid the 2.5 MB. Rejected:
  it trades a large repo for a viewer that does not work on a plane, in an air-gapped
  environment, or after the CDN moves a URL. This repo's labs are pure-local and
  zero-dependency on purpose; a viewer that phones out to render a diagram would be the
  one thing here that does not hold on its own.

- **Fetch the libraries on first run.** The compromise, and the one that looks best
  until it is written down: `site/vendor/fetch.sh`, `vendor/` in `.gitignore`. Rejected
  because it *is* an install step, only one wearing a different name, and it fails on
  exactly the machine where the offline viewer would have been worth most.

## Consequences

- **The working tree grows from about 2 MB to about 5.8 MB** — 2.5 MB of vendored
  JavaScript and 1.3 MB of search corpus against 2 MB of actual writing. Two generated
  files are now larger than everything a human typed, which is worth knowing and is not
  worth fixing. The vendored pair should change roughly never; pin the versions and treat
  an upgrade as its own commit.
- **There is more hand-written code to own** — a router, a facet navigator, a search
  scorer, a Markdown post-processor. About 900 lines across five ES modules, with no
  bundler, because native modules load fine from a static server.
- **Search is a generated file, and generated files go stale.** `site/build-corpus.py
  --check` exits non-zero when it has, mirroring `docs/build-index.py`'s contract
  exactly, so the same habit covers both.
- **The direct path and the container path are two implementations of one URL
  contract**, and they can drift. `serve.py` enforces it with an allowlist read from
  the retrieval index; `nginx.conf` enforces it by file extension and a dotfile refusal.
  The Python one is deliberately the stricter of the two, and both refuse `.git`.
