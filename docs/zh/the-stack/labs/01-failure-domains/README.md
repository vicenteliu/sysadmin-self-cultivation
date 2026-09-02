---
kind: lab
axis: the-stack
themes: []
platforms: []
derived: true
mirrors: the-stack/labs/01-failure-domains/README.md
summary: "不用云、不用凭据、不花钱、不装外部包 —— 只要 Python 3.8+。"
---
# Lab 01 —— 故障域（把副本摆好，让丢掉一个机柜也活得下来）

> 🌐 **语言：** [English（默认）](../../../../../the-stack/labs/01-failure-domains/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`the-stack/labs/01-failure-domains/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

**目标：** 把[第 01 章](../../01-physical.md)那个中心教训变得摸得着 —— **一个故障域就是一份共享
依赖的爆炸半径，而"高可用"的意思是把副本摆好，让任何单个域的故障都不会把它们一起带走。**
你会跑一个演练：它把一片机队建模成若干机柜，用两种方式放置一个服务，干掉一个机柜，然后看哪种放置
活了下来。

**你会练到：** 用故障域来思考（机柜 = TOR 交换机 + PDU = 爆炸半径）、朴素放置和反亲和放置之间的
差别，以及那次让它变得可迁移的改名 —— *一个机柜是一个 fault domain 是一个 availability zone 是
一条放置约束。*

## 这个 lab 为什么是纯本地的

不用云、不用凭据、不花钱、不装外部包 —— 只要 Python 3.8+。机柜和主机是在内存里建模的；"干掉一个
机柜"就是把它移除。重点不在这个模拟 —— 而在那份**放置判断**，而不管那个机柜是你设计的、还是那个
AZ 是云递给你的，这份判断都一模一样。

## 跑它

```bash
python3 failure_domains.py
```

exit code `0` 表示每一条断言都成立，所以它兼作一个 CI 检查。你会看到：

```
=== 2. Place a 2-replica service TWO ways ===
  naive placement      : a1 (rack-a), a2 (rack-a)
  anti-affinity        : a1 (rack-a), b1 (rack-b)
...
=== 4. Assess — which service survived? ===
  ✓ naive service is DOWN — both replicas were in rack-a (LESSON 1)
  ✓ anti-affinity service is UP on ['b1'] — one replica survived (LESSON 2)
=== 5. Scale the lesson — 3 replicas across 3 racks tolerate one rack loss ===
  ✓ lost rack-b, 2 of 3 replicas still serving — N+1 across domains (LESSON 3)
```

## 重点

- **同处一地的副本共享同一个命运。** 一个机柜里的两份拷贝就是一份拷贝 —— 那个两个朴素副本都落在
  rack-a 里的"高可用"服务，是一个明晃晃藏在那儿的单点故障。
- **跨故障域的反亲和，才是 HA 的*意思*。** 强迫那些副本落到不同机柜里，就是"熬得过丢掉一个机柜"
  和"熬不过"之间的全部差别。
- **N 个副本铺在 N 个域上，就容得下一个域的故障** —— N+1 那个想法，被变具体了。
- **放置永远是你的活。** 云给你 fault domain；它不会拦着你把两个副本都放进同一个里。这个演练就是
  那个错误，被抓在代码里，而不是被抓在故障当中。

这是[第 01 章那份 lab 规格](../../01-physical.md)的可跑形态，也是
[self-host](../../../platforms/self-host/) 那个平台徒手设计、而每一朵云的 AZ/fault-domain 模型都
要求你去用的那同一门纪律。

## 拆除

没有创建任何持久化的东西 —— 这个演练在内存里跑完就退出。没有要清理的。
