---
kind: skill-map
axis: platforms
themes: [cloud]
platforms: [azure]
derived: true
mirrors: platforms/azure/skills-map.md
summary: "和 AWS 同样的分层：Core（没它管不了）、Working（扎实的中/高级）、Depth（那个分水岭）。"
---
# Azure —— 管理技能图

> 🌐 **语言：** [English（默认）](../../../../platforms/azure/skills-map.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/azure/skills-map.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

和 [AWS](../aws/skills-map.md) 同样的分层：**Core**（没它管不了）、**Working**（扎实的中/高级）、
**Depth**（那个分水岭）。**当你能从代码把它*做*出来、并且*解释*得出它的故障模式时**，才勾上一个框。

> 如果你先做了 AWS 那张图，就把每一行读作*"Azure 的对应物是什么，以及那个怪癖是什么？"* ——
> 这里面大部分是直接迁移过来的。

## 基本功 —— 那个层级（Azure 特有）

- [ ] **Core** —— 解释 tenant → management group → subscription → resource group → resource，
  以及每一条边界是**用来干什么**的。
- [ ] **Core** —— 创建/删除一个 resource group，并把它理解成一条生命周期边界（删掉那个 RG =
  删掉它的内容）。
- [ ] **Working** —— 在 RG/subscription 之间搬资源；搞清楚什么搬不了。

## 身份与访问 —— 两套系统，不是一套

- [ ] **Core** —— **Entra ID 对 Azure RBAC**：目录身份对资源权限。搞清楚哪个是哪个。
- [ ] **Core** —— 在正确的**范围**上分配一个 RBAC 角色（management group / subscription / RG /
  resource）；那些内置角色（Reader/Contributor/Owner），以及什么时候**不该**用 Owner。
- [ ] **Core** —— 给自动化用的 service principal / 应用注册。
- [ ] **Working** —— **Managed Identity**（system 分配对 user 分配），好让工作负载不携带任何密钥
  —— 那个 Azure 版的 "instance profile"。
- [ ] **Working** —— 用 Entra 组做访问；一个最小权限的自定义 RBAC 角色。
- [ ] **Depth** —— Conditional Access、**PIM**（即时特权访问），以及在 Activity Log 里读一次被拒绝
  的动作。

## 网络（VNet）

- [ ] **Core** —— 设计一个 VNet：地址空间加 subnet。
- [ ] **Core** —— 挂在 subnet/网卡上的 **NSG**（有状态）；追查*一台 VM 为什么出不去*。
- [ ] **Core** —— 没有公网 IP，而通过 **Azure Bastion** 够到那台 VM（那个"不开 SSH/RDP"的模式）。
- [ ] **Working** —— Load Balancer 对 Application Gateway；Azure DNS zone。
- [ ] **Working** —— **Private Endpoint** / service endpoint（让存储/SQL 不上公网）。
- [ ] **Depth** —— VNet peering、UDR 加 Azure Firewall / NVA、混合（VPN Gateway / ExpressRoute）。

## 计算

- [ ] **Core** —— 从 CLI 或 IaC 部署/停止/删除一台 VM；挂上一个 managed identity。
- [ ] **Core** —— 没有公网 IP；通过 Bastion 或者经 Entra 的 `az ssh` 连过去。
- [ ] **Working** —— VM Scale Set 加 Load Balancer；自定义镜像（Compute Gallery）。
- [ ] **Depth** —— AKS 基本功；Azure Functions（serverless）；用 Spot VM 省成本。

## 存储与数据

- [ ] **Core** —— 一个**关掉了公开访问**并开着加密的 Storage Account；Blob 容器。
- [ ] **Core** —— 通过 RBAC（优先）对上账号密钥对上 SAS 来访问 —— 以及为什么密钥是一份负债。
- [ ] **Working** —— 私有配置下的 Azure SQL；备份（Recovery Services Vault）。
- [ ] **Depth** —— 生命周期管理加存储层（成本）；异地冗余选项。

## 发放与配置 —— 从代码建

- [ ] **Core** —— 用版本控制里的 **Bicep** 或 **Terraform** 把一套栈立起来。
- [ ] **Core** —— 干净地删掉它（删 RG / `terraform destroy`），不留任何孤儿。
- [ ] **Working** —— apply 之前先 `what-if` / `plan`；module；远端 state（Terraform）或者
  deployment stack。
- [ ] **Working** —— 用 **Azure Policy** 去强制/拒绝（例如"不许有公网 IP"、"必须加密"）。
- [ ] **Depth** —— landing zone / management group 设计；策略即代码；给基础设施做 CI/CD。

## 可观测性

- [ ] **Core** —— 一个 Azure Monitor 指标加一条真的会把人叫醒的告警。
- [ ] **Core** —— 把日志送进 **Log Analytics**；写一条基本的 **KQL** 查询。
- [ ] **Core** —— **Activity Log**：回答"谁创建/删除了这个？"
- [ ] **Working** —— 仪表盘；用 diagnostic setting 把日志集中路由；App Insights。
- [ ] **Depth** —— 跨 subscription 的集中日志；SLO 思维；workbook 仪表盘。

## 安全与合规 —— 安全、可证明、负担得起

- [ ] **Core** —— 用 **Key Vault** 放密钥/密钥材料/证书；通过 managed identity 访问（代码里不放
  密钥）。
- [ ] **Core** —— 一个 **Budget** 加成本告警，好让一台被遗忘的 VM/NAT/Bastion 不会让你意外。
- [ ] **Working** —— **Defender for Cloud** 的 secure score 加建议；Azure Policy 护栏。
- [ ] **Working** —— 通过 management group 做多 subscription 分离（生产/开发的爆炸半径）。
- [ ] **Depth** —— landing zone 护栏；一把泄露密钥/秘密的事故响应；成本异常告警。

## 那个"你能不能运维它"的测试

在所有面上、从代码把那些 Core 框做出来，加上调得动那些常见故障 = 你能诚实地说你能在一个可用的
水平上管理 Azure。具体到这个平台，**那个身份分野（Entra 对 RBAC）** 和 **resource group 层级**
是从 AWS 过来的人最容易被绊倒的两样东西 —— 把那两个钉死，其余的就跟上来了。
