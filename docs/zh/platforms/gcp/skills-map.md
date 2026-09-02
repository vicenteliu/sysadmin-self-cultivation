---
kind: skill-map
axis: platforms
themes: [cloud]
platforms: [gcp]
derived: true
mirrors: platforms/gcp/skills-map.md
summary: "当你能从代码把它做出来、并且解释得出它的故障模式时，才勾上一个框 —— 不是在你读过它的时候。"
---
# GCP —— 管理技能图

> 🌐 **语言：** [English（默认）](../../../../platforms/gcp/skills-map.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/gcp/skills-map.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

一份可勾选的能力清单。分层：

- **Core** —— 没有这个你管理不了 GCP。
- **Working** —— 对一个扎实的中/高级管理员的预期。
- **Depth** —— 把一个强管理员区分出来的东西；常常是面试的分水岭。

**当你能从代码把它*做*出来、并且*解释*得出它的故障模式时**，才勾上一个框 —— 不是在你读过它的时候。
这张图逐面对应 [`aws/skills-map.md`](../aws/skills-map.md)，好让两张能并排读；而
**GCP 特有的那些差量被内联点了出来**。

## 身份与访问（Cloud IAM）—— 那扇正门

- [ ] **Core** —— 解释那个资源层级（org → folder → project → resource），以及 IAM 的
  **role 怎么在每一级绑定到 member 上**（继承向下流）。
- [ ] **Core** —— 在能干活的最窄范围上授予一个**预定义角色**；知道 primitive 角色
  （owner/editor/viewer）对真实用途来说太宽了。
- [ ] **Core** —— 创建一个 **service account** 并把它当作工作负载身份用 —— 机器上没有密钥文件
  （那条"机器上不放密钥"的规则）。
- [ ] **Working** —— 写一个恰好带着某件任务所需权限的**自定义角色**；在审计日志里读一次被拒绝的
  请求。
- [ ] **Depth** —— Workload Identity Federation（完全不用 service account 密钥）；把 Org Policy
  约束当作预防性护栏。

## 网络（**全局** VPC）—— 那个结构上的异类

- [ ] **Core** —— 设计一个 VPC 并内化它是**全局的**这件事；在它下面创建**区域级 subnet**。
- [ ] **Core** —— 瞄准网络 tag 或 service account（而不只是 IP 段）的**防火墙规则** ——
  那个 GCP 特有的模型。
- [ ] **Core** —— 用 Cloud NAT 做私有出网；追查*一台实例为什么上不了网*。
- [ ] **Working** —— Cloud Load Balancing（全局 anycast）和它的后端模型；Cloud DNS 的公有对私有
  zone。
- [ ] **Depth** —— 在一个全局 VPC 上做多区域（这里"只是路由"，对上 AWS 的 peering）；
  Private Google Access / Private Service Connect；经 Cloud Interconnect 的混合连通。

## 计算 —— 代码跑的地方

- [ ] **Core** —— 用 `gcloud` 创建/停止/删除一台 Compute Engine 实例；合理地挑一个机型 ——
  **或者拨一个自定义机型**（GCP 那个精确尺寸选项）。
- [ ] **Core** —— 给一台实例挂上一个 **service account**；用 startup-script 做引导。
- [ ] **Working** —— instance template → 带自动扩缩的 **Managed Instance Group** 加一个负载均衡器
  加健康检查。
- [ ] **Working** —— 构建/维护一个自定义**镜像**（那条云镜像流水线，
  [`the-stack/03`](../../the-stack/03-compute-and-images.md)）。
- [ ] **Depth** —— 用 GKE 跑容器；用 **Cloud Run** 跑 serverless 容器；用 preemptible/Spot 省成本；
  理解热迁移。

## 存储与数据 —— 状态住的地方

- [ ] **Core** —— 一个带正确访问控制的 Cloud Storage 桶（统一的桶级访问，不是公开的）；存储类别。
- [ ] **Core** —— Persistent Disk：**zonal 对 regional**（regional PD 跨两个 zone 同步复制 ——
  一个比锁在 AZ 里的 block 更干净的 HA 原语）。
- [ ] **Working** —— 私有网络里的 Cloud SQL；备份、HA 配置、故障切换。
- [ ] **Working** —— Cloud Storage 生命周期规则加类别迁移（成本）。
- [ ] **Depth** —— 用 Filestore 做共享文件；Spanner 基本功；跨区域复制以及它的出网成本。

## 发放与配置 —— 从代码建，不从点击建

- [ ] **Core** —— 用版本控制里的 **Terraform** 把一套栈立起来；干净地销毁它（不留孤儿的、
  还在计费的资源）。
- [ ] **Core** —— 用 **project**（那个账号/爆炸半径单位）来组织工作；理解那个组织层级。
- [ ] **Working** —— 远端 state 加锁；可复用的 module。
- [ ] **Working** —— `gcloud` 脚本；实例 startup script / OS Config。
- [ ] **Depth** —— 给基础设施做 CI/CD；把 Org Policy 当作策略即代码护栏；漂移检测。

## 可观测性 —— 它健康吗，以及谁做了什么

- [ ] **Core** —— 一条真的会把人叫醒的 Cloud Monitoring 告警策略。
- [ ] **Core** —— 在 Cloud Logging 里查日志；从审计日志回答"谁创建/删除了这个？"
- [ ] **Working** —— 仪表盘；基于日志的指标；**那套内建的 SLO 工具**（一个 GCP 的优势 ——
  SLO 是原生的）。
- [ ] **Depth** —— 分布式 tracing（Cloud Trace）；跨 project 的集中日志。

## 安全与合规 —— 安全、可证明、负担得起

- [ ] **Core** —— 在真实资源之前**先设一条预算告警**；默认开启的加密；统一的桶级访问。
- [ ] **Core** —— Secret Manager（代码里不放密钥）；用 Cloud KMS 管密钥材料。
- [ ] **Working** —— Security Command Center 基本功；Org Policy 约束；用分开的 project 做
  生产/开发的爆炸半径。
- [ ] **Depth** —— landing zone / 组织层级的护栏设计；一把泄露的 service account 密钥的事故响应；
  成本异常检测。

## 那个"你到底能不能运维它"的测试

如果你能从代码在全部七片面上把那些 **Core** 框做出来，并且调得动那些常见故障，你就能诚实地说你能
在一个可用的水平上管理 GCP。因为那些面和 AWS 映射得这么干净，一个在一朵云上扎实的管理员，应该能
很快在 GCP 上达到那条线 —— 那条 ramp 是真的，而注意力要花在那四个结构性异类上（全局 VPC、project、
自定义机型、service account IAM）。
