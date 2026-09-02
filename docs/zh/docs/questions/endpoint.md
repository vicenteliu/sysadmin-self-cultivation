---
kind: questions
axis: meta
themes: [endpoint]
platforms: []
derived: true
mirrors: docs/questions/endpoint.md
summary: "被问到这个仓库头上、关于终端估算面的问题 —— 横跨三个操作系统的发放、一个 MDM 到底管什么，以及一把磁盘恢复密钥放在哪。"
---
# 问题 · 终端

> 🌐 **语言：** [English（默认）](../../../../docs/questions/endpoint.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`docs/questions/endpoint.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

> 索引、状态图例和那些范围之外的理由，住在上一级的 [`docs/questions.md`](../questions.md)。

| # | 问题 | 状态 | 在哪儿 |
|---|---|---|---|
| 1 | 当一套发放平台必须同时覆盖 Windows、macOS **和** Linux 时，它是怎么设计的？ | ✅ | [`endpoint/provisioning.md`](../../endpoint/provisioning.md) —— 那两个时代、这三套系统真正共享的东西，以及作为约束的硬件多样性 |
| 2 | 一个 MDM 到底管什么，而各片估算面在实践中差在哪？ | ✅ | [`endpoint/management.md`](../../endpoint/management.md) —— 那个租来的管理面，以及一片 Apple 估算面的形状，**当作签名来读，不是当作推荐** |
| 3 | 全盘加密的恢复密钥存在哪，谁被允许取出一把？ | ✅ | [`endpoint/encryption-and-keys.md`](../../endpoint/encryption-and-keys.md) —— 托管把它所移除的风险集中起来，而那些密钥活得比那些机器长 |
| 4 | 在你把一条策略跑到三千台机器上之前，它的爆炸半径是多少？ | ✅ | [`labs/policy-blast-radius/`](../../endpoint/labs/policy-blast-radius) —— 而那个答案是：它不是一个数字，它是一个关于时间的函数。控制台那个计数是稳定的，而它没法告诉你它已经过期了 |
