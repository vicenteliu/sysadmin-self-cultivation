---
kind: lab
axis: cross-cutting
themes: [networking, cloud]
platforms: []
derived: true
mirrors: cross-cutting/labs/multi-cloud-cidr-overlap/README.md
summary: "一个单云管理员连起两朵云的那一天撞上的第一个具体拦路石：地址空间重叠时互联会被拒绝，而每一个控制台都在把你往同一个 10.0.0.0/16 上推。"
---
# Lab —— 重叠的 CIDR 让互联坏掉（而且不存在一个中央路由器）

> 🌐 **语言：** [English（默认）](../../../../../cross-cutting/labs/multi-cloud-cidr-overlap/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`cross-cutting/labs/multi-cloud-cidr-overlap/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

**目标：** 感觉到一个单云管理员在连起两朵云的那一天撞上的头号具体拦路石 —— 你**没法把地址空间
重叠的网络对等或者用 VPN 连起来**。这是一个硬性的机械事实，在 AWS、Azure（Cloud Adoption
Framework）和 GCP 的文档里都得到了确认：CIDR 重叠时，对等会被*拒绝*。而每一朵云的控制台都在把你
往 `10.0.0.0/16` 上推，所以两朵各自用了默认值的云 —— 或者一朵云和一片本地 —— **是接不起来的**。

```
each cloud owns a CIDR     (AWS 10.0/16, Azure 10.1/16, ...)
and keeps its OWN routes   (no central router; each side needs a route to the others)
deliver(src, dst_ip)       routes only if the destination is unambiguous AND src has a route
```

它演练什么 —— 五条教训：
1. **不重叠 + 两边都有路由 → 流量通。** 那条互联能用。
2. **CIDR 重叠 → 有歧义。** `10.0.0.5` 被*两朵*云同时拥有，所以那条互联判定不了它归谁 ——
   对等/VPN 被拒绝。
3. **一边缺一条路由 → 被丢弃。** 不存在中央路由器；每朵云给自己做路由，所以一条被忘掉的路由表
   条目会把流量黑洞掉。
4. **非对称路由 → 半开。** 有去程路由而没有回程路由，会让请求过去、而回复被丢掉。
5. **本地的 `10.0.0.0/8` 把那些云一口吞掉 → 那个混合重叠陷阱。** 一个宽泛的本地超网和每一朵云的
   `10.x` 段都重叠 —— 要横跨*所有这些*去规划不重叠的地址空间。

## 为什么在本地

不用云账号、不用 VPN 网关、不产生账单。这个演练是一份大约 150 行的跨云路由模型 —— CIDR 归属、
重叠所制造的那份歧义，以及逐云（而不是中央）的路由表 —— 好让你检视的是那份*逻辑*，不是三个控制台。
它在任何跑得了 Python 的地方都跑得起来，在 CI 里也是。

## 跑

```bash
python3 cidr_overlap_drill.py
```

## 你会看到什么

五个被叙述出来的步骤，每一个都带一个 `OK`/`XX`：一条干净的双向互联；一对重叠段被检测为有歧义；
一个因为缺路由而被丢掉的包；一次因为非对称路由而半开的连接；以及一个和某个云段撞上的本地超网。
最后给出一个 PASS 判定，`exit 0`。

## 验证（要紧的那部分）

exit `0` = 每一条教训都成立；它兼作一个 CI 检查。现在**故意把这个模型弄坏** —— 有两条彼此独立的
破坏路径：

```bash
python3 cidr_overlap_drill.py --sabotage ignore-overlap   # 假装重叠没关系 -> 步骤 2 和 5 路由错，exit 1
python3 cidr_overlap_drill.py --sabotage central-router   # 假设有一个什么路由都有的魔法路由器 -> 步骤 3 和 4 看不见那个缺口，exit 1
```

如果重叠的地址还能被"路由"，那那份歧义本来就不是真的；如果一个魔法中央路由器总是有路由，那逐云的
路由表本来就不承重。这些失败，正是这个模型确实要紧的证据。

## 重点

有两条单云反射在这里同时被纠正。第一，**"云会替我搞定寻址和路由"** —— 在一个 VPC/VNet *内部*
这是真的，*跨*云就是假的，而在跨云那边，你继承的是本地那门横跨每一朵云和本地的企业级 IP 地址管理
（IPAM）纪律。第二，**"我回头再把它们对等起来就行"** —— 段重叠的话你就不行，而给活着的子网重新
编址，是多云决定里唯一一个真正难以逆转的。先规划好不重叠的 CIDR。完整的接缝目录见
[多云 support 笔记](../../multi-cloud-support.md)，逐云的网络原语见
[`the-stack/02-network.md`](../../../the-stack/02-network.md)。

## 拆除

没有 —— 它就是一个自包含的脚本。把这个目录删掉就行。
