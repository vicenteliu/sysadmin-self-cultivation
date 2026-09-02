---
kind: questions
axis: meta
themes: []
platforms: []
derived: true
mirrors: docs/questions/storage.md
summary: "被问到这个仓库头上、关于公司数据住在哪的问题 —— 一个内部文件服务，以及一个有一部分属于别人的数据库。"
---
# 问题 · 存储与数据

> 🌐 **语言：** [English（默认）](../../../../docs/questions/storage.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`docs/questions/storage.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

> 索引、状态图例和那些范围之外的理由，住在上一级的 [`docs/questions.md`](../questions.md)。

| # | 问题 | 状态 | 在哪儿 |
|---|---|---|---|
| 1 | 一个内部文件分享与存储服务是怎么设计的？ | ✅ | 这个词先要拆开 —— [`CONTEXT.md`](../../CONTEXT.md) 现在把一台**文件服务器**和**套件存储**分开了，因为它们坏的方式不一样。一旦文件进了一套套件，那个设计问题就不再是目录上的权限，而是*谁能看见这个* —— 那是[步骤 07](../../build-out/07-files-and-collaboration.md) 和 [`permission-sprawl`](../../../../cross-cutting/labs/permission-sprawl/) |
| 2 | 那个服务该自建还是该买？ | ✅ | **在这个规模上，买。** 一台文件服务器在[Where things run](../../the-reference-office.md#本地--什么不能离开)那三个测试上一个都过不了 —— 它不作用于这栋楼、上行断掉时这层楼上没有任何东西需要它，而且它不是你故意弄坏的那样东西。那次拒绝被记录在那儿，而不是被留着重新辩论 |
| 3 | 当一部分数据属于一个你并不运营的网络服务时，一个数据库是怎么设计的？ | ✅ | [`databases.md`](../../cross-cutting/databases.md#当一半的数据属于别人的时候) —— 权威是逐**字段**决定的，不是逐系统；一份拷贝携带它的年龄；而同步方向是一个你刻意做出的单向决定 |
| 4 | 自建一个：同步和备份实际是怎么工作的？ | ✅ | [`databases.md`](../../cross-cutting/databases.md#当一半的数据属于别人的时候) —— 那个恢复目标不是一个数字。敲进去的行不可替代；同步来的行需要一个能从冷启动开始的同步，而那正是没人去测的那部分 |
