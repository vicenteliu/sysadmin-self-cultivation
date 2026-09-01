---
kind: note
axis: start-here
themes: []
platforms: []
derived: true
mirrors: 00-the-operating-model.md
summary: "每个平台底下那副可迁移的骨架。"
---
# Operating Model（运维模型）

> 🌐 **语言：** [English（默认）](../../00-the-operating-model.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`00-the-operating-model.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

> 每个平台底下那副可迁移的骨架。学会这一次；剩下的都是语法。

大多数"学会 AWS / Azure / GCP"的材料，是把一百个服务砸给你，然后指望能粘住几个。这是
反的。在品牌名底下，一个管理员来来回回做的永远是同样的那几件事。把它们点出名字，一个
新平台就不再是一堵行话砌的墙，而变成一道填空题。

## 三个动作

一个 admin 为了**驱动**一个平台所做的一切，都归约成：

1. **注册一个受限范围的身份。** 一个 principal（user、service account、role、app
   registration），带着仍然够干活的**最小**权限。
2. **拿到凭据并完成认证。** 一个 access key、一个 token、一次短期 session、一张证书。
   这就是你的脚本和工具随身带的东西。
3. **通过 API 驱动平台 —— 并把它写成代码。** console 是用来**看**的；API/CLI/SDK 是
   用来**做**的；infrastructure-as-code 是用来让它可重复、可评审、可丢弃的。

这三件事你要是能干净利落地做出来，你就能运维任何东西。剩下的是知道**有哪些**资源存在，
以及**故障模式**是什么。

## 每个平台都有的七个面

拿任何一个云/平台过一遍这七个面，你就测绘了 admin 这份工作大约 90% 的内容：

| 面 | 它回答的问题 | 迁移过去叫什么 |
| --- | --- | --- |
| **Identity & access** | 谁能做什么，以及他怎么证明自己是谁？ | IAM / RBAC、role、policy、least-privilege、生命周期 |
| **Compute** | 代码在哪里跑？ | VM、容器、serverless、autoscaling |
| **Networking** | 东西之间怎么安全地互相够到？ | 虚拟网络、subnet、路由、防火墙、DNS、负载均衡 |
| **Storage & data** | 状态住在哪？ | object / block / file 存储、托管数据库、备份 |
| **Provisioning & config** | 这一切怎么被创建出来并保持一致？ | infrastructure-as-code、配置管理、镜像 |
| **Observability** | 它健康吗，我怎么知道？ | metric、log、trace、告警、仪表盘 |
| **Security & compliance** | 它安全吗，我能证明吗？ | 加密、secret、加固、审计、guardrail、把成本当成一种控制 |

这个仓库里每一个平台模块都按这七个面组织。一旦你把它们内化，学第二个平台就变成了
*"好，他们管 VNet 叫什么，坑在哪？"* —— 这个问题 AI 几秒钟就答了。

## 什么真的会迁移（以及什么不会）

**干净地迁移** —— 上面那些概念。least-privilege 就是 least-privilege，不管它是一条
AWS IAM policy 还是一次 Azure role assignment。subnet 就是 subnet。幂等、可评审的
基础设施在每个平台上都是目标。

**不会迁移** —— **名字**、**默认值**、**怪癖**和**故障模式**。而这一层恰恰是错误和
故障的来源，也恰恰是"我读过营销页"会把你烧到的地方。它同时也是 AI 最擅长压缩的一层
—— **前提是**你去验证（见 [`ai-workflow/`](ai-workflow/)）。

## 让它落地的那份纪律

一个没有上手的心智模型只是冷知识。对每个平台，及格线是：

- 我能创建一个**受限范围的身份**，并用它给一个脚本完成认证。
- 我能从**代码**（不是点击）起一套小而真实的栈。
- 我能像搭起来一样干净地**拆掉它**。
- 我能讲清楚我搭的这套东西在**安全和成本**上的含义。
- 我知道**最常坏的那三四样东西**，以及我会怎么调试它们。

那就叫"称职"。每个平台目录下的 lab 存在的意义，就是逼你真的去做一遍 —— 因为读一篇讲
subnet 的文章和配一个 subnet 是两种不同的技能，而只有其中一种会出现在面试或者一次故障
里。
