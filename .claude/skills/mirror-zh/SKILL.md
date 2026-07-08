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
   Translate the *prose*, keep the *terms*. Preserve ✋/🧗 markers and bold emphasis.

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

6. **Cross-links point BACK to the English canonical** (the zh versions usually don't
   exist). Compute the climb to repo root, then append the English path.
   **Depth cheat-sheet** (this is where mistakes happen):

   | Mirror lives at | Climb to root | Example link to `cross-cutting/x.md` |
   | --- | --- | --- |
   | `docs/zh/cross-cutting/X.md` | `../../../` | `../../../cross-cutting/x.md` |
   | `docs/zh/platforms/aws/X.md` | `../../../../` | `../../../../cross-cutting/x.md` |
   | `docs/zh/README.md` | `../../` | `../../cross-cutting/x.md` |

   Rule: one `../` per directory segment between the mirror and repo root.

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

- **Every relative link resolves** — from each edited file's directory, confirm the
  target exists (`[ -e <path> ]`). The depth math is the #1 source of dead links.
- **Mermaid validates** (see step 4).
- **The mirror is complete** — same sections as the English source, nothing dropped.

## Wire-in & commit

- If the repo tracks a translation count or a "started" note, keep it accurate.
- Commit with `docs(zh): mirror <path> into Chinese` and **no `Co-Authored-By`
  trailer** — this is a public portfolio repo; match its clean, unsigned history
  ([`author-module`](../author-module/SKILL.md) has the same commit rule).

## Guardrails

- **Full mirror, not a summary** — a lagging translation is fine (docs/README says
  so); a *partial* one that silently drops sections is not.
- **Terms in English, prose in Chinese** — don't "translate" `AccessDenied` or
  `security group`.
- **Links go to the English canonical**, never to a zh sibling that doesn't exist.
- Run the link check before calling it done — dead relative links are the failure
  mode this skill exists to prevent.
