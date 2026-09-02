---
kind: questions
axis: meta
themes: [networking]
platforms: []
derived: true
mirrors: docs/questions/networking.md
summary: "被问到这个仓库头上、关于网络的问题 —— 十三个全部已答，其中三个是先被收窄之后才答的。"
---
# 问题 · 网络

> 🌐 **语言：** [English（默认）](../../../../docs/questions/networking.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`docs/questions/networking.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

> 索引、状态图例和那些范围之外的理由，住在上一级的 [`docs/questions.md`](../questions.md)。

| # | 问题 | 状态 | 在哪儿 |
|---|---|---|---|
| 1 | 一个当代办公网在架构上长什么样？ | ✅ | [`site-network-design.md`](../../cross-cutting/site-network-design.md) |
| 2 | 办公网架构在十五年里怎么变的？ | ✅ | [`network-evolution.md`](../../cross-cutting/network-evolution.md) —— 一个动作解释了其中大部分：网络不再是通往你工作的路，而变成了通往互联网的路 |
| 3 | 那段时间里网络协议怎么变的？ | ✅ | [`network-evolution.md`](../../cross-cutting/network-evolution.md) —— 而那个诚实的答案是：协议变的比它们所承载的东西更少；443 上的 TLS 承载一切，才是那次挪动了防火墙那根轴的变化 |
| 4 | 防火墙：现在是 Palo Alto —— 在它之前是什么，以及变了什么？ | ✅ | [`network-evolution.md`](../../cross-cutting/network-evolution.md#防火墙变的是那根轴不是吞吐) —— **当作签名**：那根轴从端口挪到了应用与用户身份，因为 443 上的 TLS 让一条端口规则变成了一条关于互联网的规则。它所取代的通常是那台同时终结 WAN 链路的路由器 |
| 5 | 一台 F5 级别的设备到底干什么？ | ✅ | [`network-evolution.md`](../../cross-cutting/network-evolution.md#负载均衡器以及你为什么遇见得更少了) —— 终结 TLS、分摊负载，并**持有那些无处可去的应用逻辑**，而那才是让它变得承重的部分。外加 [`the-stack/02`](../../the-stack/02-network.md) 里那一行 *LB 签名* |
| 6 | 接入点是怎么部署的，按什么规则？ | ✅ | [`Selection rules`](../../the-reference-office.md#selection-rules) —— 🧭 |
| 7 | 无线和它的协议怎么变的？ | ✅ 🧭 | [`network-evolution.md`](../../cross-cutting/network-evolution.md#无线-) —— 每平方米的容量升上去了，每个射频的客户端数几乎没动。在那里被标成 🧭，与 [`site-network-design.md`](../../cross-cutting/site-network-design.md#诚实边界) 保持一致 |
| 8 | 一间大办公室的网络和一间小的差在哪？ | ✅ | [`site-network-design.md`](../../cross-cutting/site-network-design.md#什么时候规模会改变设计) |
| 9 | 一条 VPN 到底是怎么把一个用户落到办公网上的？ | ✅ | [`vpn-and-remote-access.md`](../../cross-cutting/vpn-and-remote-access.md) —— **被收窄到那些决定，不是那套机制**：一条 VPN 不会把你放到网络上，它给你一个网段上的地址和一组路由。五个决定，而会坏的那个是 DNS 而不是路由 |
| 10 | 基本的排障命令有哪些？ | ✅ | [`debug-ladder.md`](../../cross-cutting/debug-ladder.md) —— **逐级，不是一份参考**，正如那次收窄所要求的。每一条命令都按"一次通过让你可以停止考虑什么"来评判，而这一页上信息量最高的回答是*拒绝*对上*超时* |
| 11 | IPv4 和 IPv6 现在怎么共存，以及怎么配置？ | ✅ | [`the-stack/02`](../../the-stack/02-network.md) |
| 12 | 速度变了什么？总不能到现在还处处千兆吧。 | ✅ | 当前状态在 [`site-network-design.md`](../../cross-cutting/site-network-design.md) 里；历史在 [`network-evolution.md`](../../cross-cutting/network-evolution.md#速度它并没有在人们以为的地方增长) 里 —— 钱**往上、往侧面**挪了，挪进上行链路和那些射频，而桌面是唯一那个从来不需要它的层 |
| 13 | 那套低压网络实际是怎么布的？给我看一份拓扑。 | ✅ | **楼面**的近处那一档把它画了出来，而[走读 01](../../../../walkthrough/01-the-network.zh.md) 把它讲了出来 —— 带三台接入交换机的 IDF、plate 核心筒里的竖井，以及从接入端口到上联的*那条没人数的路径*。仍然**不包括施工那一侧**，它在[边界](../questions.md#边界)里保持被剪掉 |

**十三个被问到，十三个已答，零个未决。** 那是一个状态，不是一个终点 —— 而值得保留的那个形状是：
其中三个是先被收窄之后才被回答的，而那次剪裁被记录在[边界](../questions.md#边界)里，
而不是被留着重新发现一遍。
