---
kind: questions
axis: meta
themes: []
platforms: []
derived: true
mirrors: docs/questions/observability.md
summary: "被问到这个仓库头上、关于监控的问题 —— 它怎么设计、主流方案是什么，以及监控一切到底可不可能。"
---
# 问题 · 可观测性

> 🌐 **语言：** [English（默认）](../../../../docs/questions/observability.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`docs/questions/observability.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

> 索引、状态图例和那些范围之外的理由，住在上一级的 [`docs/questions.md`](../questions.md)。

| # | 问题 | 状态 | 在哪儿 |
|---|---|---|---|
| 1 | 一套监控系统是怎么设计的？ | ✅ | [`the-stack/06`](../../the-stack/06-observability.md) —— 三根支柱、SLI/SLO，以及原生与中立那个选择 |
| 2 | 今天的主流方案有哪些？ | ✅ | [`the-stack/06`](../../the-stack/06-observability.md#七种做法--原生栈与自带栈) —— 七种做法和一张对比表，**当作签名**：你在一片估算面里会看到什么，不是该买什么 |
| 3 | 有没有可能监控**一切**？ | ✅ | [`the-stack/06`](../../the-stack/06-observability.md#你能监控一切吗) —— **不能**，而那四堵墙都不是预算。有用的那个动作是把目标换掉：*知道你没在监控什么*是可核查的，而*监控一切*不是 |
