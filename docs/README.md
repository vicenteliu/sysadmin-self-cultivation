---
kind: index
axis: meta
themes: []
platforms: []
summary: "The project's default language is English; the canonical docs live at the repo root and under platforms/, cross-cutting/, and ai-workflow/."
---
# docs/ — Documentation & translations

> 🌐 **Languages:** English (default) · [中文](zh/docs/README.md)

The project's **default language is English**; the canonical docs live at the repo
root and under `platforms/`, `cross-cutting/`, and `ai-workflow/`.

It also holds the repo's own metadata: the [decision records](adr/), the
[open questions](questions.md) — what the repo has been asked and cannot yet answer,
including the ones deliberately out of scope and why — and the
**retrieval index** — [`index.json`](index.json), generated from every file's
front-matter by [`build-index.py`](build-index.py) so an agent can search the repo
without walking it. The index is generated, never edited: change the file, then run
the script. `--check` exits non-zero when it has gone stale.

The same generated-not-edited contract covers the two files the browser at
[`site/`](../site/README.md) reads — its titles map and its **search corpus** — and the
twelve artifacts derived from the four hero-diagram sources. Each builder takes
`--check`.

This directory holds **translations** (multi-language support). Each language gets a
subfolder that mirrors the English tree as translations are contributed.

```
docs/
└── zh/                 # Chinese
    └── README.md       # translated overview; more docs added over time
```

**Translations may lag the English source.** When they disagree, the English root
docs are authoritative. To contribute a translation, mirror the English file's path
under the language folder (e.g. `platforms/aws/README.md` → `docs/zh/platforms/aws/README.md`).
