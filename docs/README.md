# docs/ — Documentation & translations

The project's **default language is English**; the canonical docs live at the repo
root and under `platforms/`, `cross-cutting/`, and `ai-workflow/`.

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
