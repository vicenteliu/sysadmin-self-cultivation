---
kind: adr
axis: meta
themes: []
platforms: []
derived: true
mirrors: docs/adr/0007-a-figures-medium-is-decided-by-what-renders-it.md
summary: "这个仓库有 67 张 mermaid 图和一种做图的方式。加上带品牌的 hero 图引入了第二种，而一件事有两种做法正是一条约定腐烂的方式 —— 所以它们之间那条边界被写在这里，而不是留给品味。"
---
# 一张图的介质由渲染它的东西来决定

> 🌐 **语言：** [English（默认）](../../../../docs/adr/0007-a-figures-medium-is-decided-by-what-renders-it.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`docs/adr/0007-a-figures-medium-is-decided-by-what-renders-it.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

这个仓库有 67 张 mermaid 图和一种做图的方式。加上带品牌的 hero 图引入了第二种，而一件事有两种
做法正是一条约定腐烂的方式 —— 所以它们之间那条边界被写在这里，而不是留给品味。

## 决定

**如果 GitHub 渲染得了它，它就是 mermaid。** 一个围起来的 `mermaid` 块在 GitHub 上渲染、在
viewer 里渲染，并且按文本做 diff —— 源码和那张图是同一个对象，所以它们不可能互相不一致。

> ⚠️ **下面那个界限被 [ADR-0008](0008-a-count-is-not-a-bound.md) 取代。**
> 一共有七张，那个计数从来就不可执行，而它现在是一条判据。

**hero 图是那个例外，而它是有界的。** 存在四张：轴图、栈图、ramp 图和路线图。每一张开启一条轴。
每一张被作为一个轻量 HTML 文件创作一次，其余的一切都由
[`site/build-diagrams.py`](../../site/README.md) 派生 —— 暗色 HTML，以及两个 SVG。Markdown 通过
`<picture>` 嵌入那些 SVG，所以 GitHub 和 viewer 各自拿到匹配读者主题的那个变体。

而凌驾于两者之上的，是那条决定要不要画的规则：**一张图必须携带散文没有携带的东西** —— 一个顺序、
一份依赖、一条边界、一个比例、一次收敛。一张把一个段落或一张表重述一遍的图是一个缺陷。一次扫过
十七个目录索引的检查产出了两张新的 mermaid 图和四处 hero 嵌入，而被放过的那十一个文件是被刻意
放过的。

## 考虑过的选项

- **全部用 mermaid。** 最整齐的答案，也是那个保住单一介质的答案。因为一个很窄的情况而被否决：
  一张开启一条轴的图在做编辑工作 —— 层次、一个强调色、一个刻意的焦点元素 —— 而 mermaid 的自动布局
  守不住那些决定。在排那张技能图的时候，dagre 有两次挪动了一个泳道、颠倒了一个层级，并让那句
  说明变成了假话。

- **全部用 `diagram-design`。** 直接否决。六十七张图会变成一百来个围起来的块中每一个都要一份 HTML
  源码加两个 SVG；一次一个单词的标签修正变成一次构建；而 GitHub 会失去那份让一张图在 pull request
  里可评审的纯文本 diff。

- **只做 hero HTML，用链接而不是嵌入。** 更简单 —— 没有导出步骤，没有第二个要保持同步的产物。
  被否决，是因为 GitHub 不渲染一个 HTML 文件，所以每一位 GitHub 上的读者都会拿到一个链接而不是一张
  图 —— 而且恰好是在那四个"图才是重点"的地方。

- **在浅色版旁边手写暗色版。** 因为 ADR-0001 否决 build-out 第二份拷贝时的同一个理由被否决：
  四百行坐标为了十个十六进制值被复制一遍，从第一次只落在一边的编辑起就开始漂移。它改成被派生
  出来，而 `--check` 会说出那次派生什么时候落后了。

## 后果

- **四个源，十二个派生文件。** 绝不要手工编辑一个派生文件；下一次运行会覆盖它。
  `python3 site/build-diagrams.py --check` 是那个守卫，而
  [`diagram-module`](../../../../.claude/skills/diagram-module/SKILL.md) 是拥有"去跑它"这件事的
  那个 skill。
- **那套皮肤被提交了，并且对着那个派生器被核对。** `diagram-design` 从用户家目录里解析样式
  profile，所以一份克隆会带着那个 `.diagram-design` 标记、却不带它所点名的那套皮肤 —— 因此这个
  仓库自己持有那份 profile，放在 `site/assets/diagrams/sysadmin-brass.profile.md`，而
  `--install-profile` 把它放到插件去找的地方。这补上了这份 ADR 第一版记录为补不上的一个洞：
  `--check` 现在把每一个语义角色的浅色值，走一遍文档所走的同一次替换，并要求拿回那份 profile 的
  暗色值。它一存在就找到了两处真实的偏斜 —— 那个强调色在三个活的产物里以错误的不透明度派生，
  而 `rule-solid` 派生出了一条半透明细线的不透明近似。
- ~~**第五张 hero 需要一个论证，不是一个时机。**~~ 被
  [ADR-0008](0008-a-count-is-not-a-bound.md) 取代 —— 那个论证一次都没被做出，一共三次，因为一个
  计数没法宣布自己已经被越过了。
- **Mermaid 的布局是一条对内容的约束。** 把 subgraph 标题控制在大约 28 个字符以内、在一个 `TB`
  流里避免回边，并且不要把一个不连通的组件放在一个连通的旁边。那些陷阱和它们的症状被记录在
  [`diagram-module`](../../../../.claude/skills/diagram-module/SKILL.md) 里，好让下一位作者不用
  重新发现它们。
