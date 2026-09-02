---
kind: questions
axis: meta
themes: []
platforms: []
derived: true
mirrors: docs/questions/platforms.md
summary: "被问到这个仓库头上、关于云网络设计和自建虚拟化的问题 —— 两个都已答 —— 其中一个是作为一份三方笔记被关闭的，而不是被写出来的。"
---
# 问题 · 平台与虚拟化

> 🌐 **语言：** [English（默认）](../../../../docs/questions/platforms.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`docs/questions/platforms.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

> 索引、状态图例和那些范围之外的理由，住在上一级的 [`docs/questions.md`](../questions.md)。

| # | 问题 | 状态 | 在哪儿 |
|---|---|---|---|
| 1 | AWS、GCP 和 Oracle Cloud 各自怎么设计他们的网络服务？ | ✅ 逐平台 · 作为一份三方笔记**已关闭** | [`platforms/aws`](../../platforms/aws/architecture.md) · [`azure`](../../platforms/azure/architecture.md) · [`gcp`](../../../../platforms/gcp/architecture.md) · [`oci`](../../../../platforms/oci/architecture.md)，而 [`the-stack/02`](../../the-stack/02-network.md) 已经是这个仓库横跨七个平台对比某一层的那个地方。一份单独的三方笔记会在混合的立足点上把它重复一遍 —— 见[边界](../questions.md#边界) |
| 2 | 自建一片 VM 估算面：vCenter 和 Proxmox 之间实际差在哪，以及有哪些方案？ | ✅ | [`vcenter-and-proxmox.md`](../../../../platforms/vsphere/vcenter-and-proxmox.md) —— 每个控制面住在哪、它死掉时你失去什么，以及那条发现：一次 hypervisor 迁移是一个穿着 hypervisor 戏服的存储与客户机支持项目 |
