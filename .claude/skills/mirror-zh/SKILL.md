---
name: mirror-zh
description: Mirror an English canonical doc from The Sysadmin's Self-Cultivation repo into a Chinese translation under docs/zh/, following the repo's translation convention — same path mirrored, technical terms kept in English, a bidirectional 🌐 language switcher, cross-links pointing back to the English source, and index/pointer updates. Use when the user says "做个中文镜像", "mirror this to Chinese", "translate this to zh", "put it in docs/zh", or wants a Chinese version of an existing note.
created: 2026-07-08
owner: Vicente Liu
---

# Skill: mirror-zh

Turn an English canonical doc into a faithful Chinese mirror that lands consistent
with the rest of `docs/zh/`. The rule the repo already set (see
[`docs/README.md`](../../../docs/README.md)): **English is authoritative; each language
folder mirrors the English tree; translations may lag.** This skill makes producing
one mechanical and correct — the fiddly parts are the relative-link depth and the
bidirectional switcher, so they're spelled out below.

## First: read the exemplars

- The register/voice → [`docs/zh/README.md`](../../../docs/zh/README.md) (opinionated,
  technical Chinese; terms kept in English).
- A full chapter mirror → [`docs/zh/cross-cutting/m365-support.md`](../../../docs/zh/cross-cutting/m365-support.md)
  and [`docs/zh/platforms/aws/support.md`](../../../docs/zh/platforms/aws/support.md).
  Read one before writing.

## The workflow

1. **Mirror the path.** English `<path>` → `docs/zh/<path>`, exactly. E.g.
   `cross-cutting/m365-support.md` → `docs/zh/cross-cutting/m365-support.md`;
   `platforms/aws/support.md` → `docs/zh/platforms/aws/support.md`.

2. **Translate in full — not a summary.** Every section, table, and mermaid diagram.
   The content must match the English; only the language changes.

3. **Keep technical terms in English.** Service/product names, error codes, CLI and
   cmdlets, and load-bearing jargon stay English inside Chinese prose — e.g. Exchange
   Online, Entra, Conditional Access, break-glass, Message Trace, `AccessDenied`,
   `ThrottlingException`, IAM, security group, NACL, SCP, `Connect-ExchangeOnline`.
   Translate the *prose*, keep the *terms*. Preserve 🔨/🧭 markers and bold emphasis.

4. **Mermaid: translate node text to plain Chinese words** (mindmap nodes take no
   parentheses/punctuation — same rule as [`author-module`](../author-module/SKILL.md)).
   Validate every diagram before finishing.

5. **Top matter — the switcher + authority note.** Directly under the H1, add:
   ```
   > 🌐 **语言：** [English（默认）](<rel-to-english-source>) · **中文**
   >
   > ⚠️ 本项目**默认语言为英文**，`<english/path>` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。
   ```
   Then a `---`, then the translated thesis blockquote.

6. **Cross-links: first check whether the target is itself mirrored, then pick a branch.**

   **Target has a zh mirror** (`docs/zh/<target>` exists — whole subtrees are mirrored
   now, all of `toolbox/` among them): link to the mirror. Inside `docs/zh/` the tree
   has the same shape as English, so the link is **byte-identical to the English one**.
   Add nothing; there is nothing to climb.

   **Target has no mirror**: link BACK to the English canonical — climb to repo root,
   then append the English path. One `../` per directory segment between the mirror and
   the root, and `docs/zh/` is already two of them:

   | Mirror lives at | Segments | Climb to root |
   | --- | --- | --- |
   | `docs/zh/README.md` | 2 | `../../` |
   | `docs/zh/cross-cutting/X.md` | 3 | `../../../` |
   | `docs/zh/platforms/aws/X.md` | 4 | `../../../../` |
   | `docs/zh/toolbox/ansible/roles/patch/X.md` | 6 | `../../../../../../` |

   Count the segments or measure the climb — don't read it off the table:
   `python3 -c "import os;print(os.path.relpath('.','docs/zh/a/b/c'))"`. The table
   can't hold every depth, and the depths it omits are where this has actually broken.

   > **How it broke once (2026-08-24, 13 dead links).** Both branches were off by
   > exactly one `../`, in *opposite* directions: targets that were mirrored got a
   > `../` added, pushing the link out of `docs/zh/`; targets that weren't got one too
   > few, landing in `docs/` instead of the repo root. One constant, two symptoms —
   > which is why "the depth is off" is not a specific enough diagnosis to act on.

7. **Make it bidirectional — add the switcher to the English source.** The repo
   convention is that a doc carries a `🌐` switcher **only once its mirror exists**.
   Add to the English doc, right under its H1:
   ```
   > 🌐 **Languages:** English (default) · [中文](<rel-to-mirror>)
   ```
   From the English `<path>`, climb to root then into `docs/zh/<path>`:

   | English doc | Link to its mirror |
   | --- | --- |
   | `cross-cutting/X.md` | `../docs/zh/cross-cutting/X.md` |
   | `platforms/aws/X.md` | `../../docs/zh/platforms/aws/X.md` |

8. **Make it discoverable — add a pointer from [`docs/zh/README.md`](../../../docs/zh/README.md)**
   to the new mirror (a short `[标题（中文镜像）](rel/path)` link near where the English
   doc is referenced), matching how the existing mirrors are surfaced there.

## Verify (don't skip)

- **Every relative link resolves** — run the checker; don't spot-check by hand:

  ```
  python3 .claude/skills/mirror-zh/check_links.py
  ```

  It resolves every relative link in the repo, prints how many it checked, lists each
  dead one together with where that target actually sits on disk, and exits 1 if any
  are dead. Read the count, not just the verdict: `0 dead` out of 4 links and `0 dead`
  out of 1403 are different results. A hand check of the file you just edited also
  can't see the links you broke in the file you edited an hour ago.
- **Mermaid validates** (see step 4).
- **The mirror is complete** — same sections as the English source, nothing dropped.

## Wire-in & commit

- If the repo tracks a translation count or a "started" note, keep it accurate.
- Commit with `docs(zh): mirror <path> into Chinese` — the same message style
  [`author-module`](../author-module/SKILL.md) uses.

## Guardrails

- **Full mirror, not a summary** — a lagging translation is fine (docs/README says
  so); a *partial* one that silently drops sections is not.
- **Terms in English, prose in Chinese** — don't "translate" `AccessDenied` or
  `security group`.
- **Link to the zh mirror where one exists, to the English canonical where it doesn't** —
  never to a zh sibling that isn't there. Check which case you're in (step 6).
- Run the link check before calling it done — dead relative links are the failure
  mode this skill exists to prevent.
