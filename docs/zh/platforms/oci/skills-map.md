---
kind: skill-map
axis: platforms
themes: [cloud]
platforms: [oci]
derived: true
mirrors: platforms/oci/skills-map.md
summary: "当你能从代码把它做出来、并且解释得出它的故障模式时，才勾上一个框。"
---
# OCI —— 管理技能图

> 🌐 **语言：** [English（默认）](../../../../platforms/oci/skills-map.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/oci/skills-map.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

一份可勾选的能力清单。分层：

- **Core** —— 没有这个你管理不了 OCI。
- **Working** —— 对一个扎实的中/高级管理员的预期。
- **Depth** —— 把一个强管理员区分出来的东西；常常是面试的分水岭。

**当你能从代码把它*做*出来、并且*解释*得出它的故障模式时**，才勾上一个框。逐面对应
[`aws/skills-map.md`](../aws/skills-map.md)；而 **OCI 特有的那些差量被内联点了出来**。
诚实提示：这些是那条 **ramp 的目标** —— 见这个模块的[诚实边界](README.md)。

## 身份与访问 —— IAM 加 compartment
- [ ] **Core** —— 设计一个 **compartment** 层级（那个爆炸半径/隔离单位）并写出**策略语句**
  （`Allow group X to manage Y in compartment Z`）。
- [ ] **Core** —— 用 **instance principal** 让一台 VM 不用密钥就能认证。
- [ ] **Working** —— dynamic group；受限的最小权限策略。
- [ ] **Depth** —— 与一个外部 IdP 联合；在审计日志里读一次被拒绝的请求。

## 网络 —— VCN
- [ ] **Core** —— 设计一个 **VCN**（区域级）、subnet、一个 Internet/NAT 网关；追查*一台实例为什么
  上不了网*。
- [ ] **Core** —— **在 security list 或 NSG 之间挑一个并标准化** —— 别把两个缠在一起
  （那个 OCI 特有的过滤陷阱）。
- [ ] **Working** —— route table、service gateway（让流量不上互联网）。
- [ ] **Depth** —— FastConnect / 混合；多 VCN peering。

## 计算 —— shape
- [ ] **Core** —— 启动一台实例；用**弹性 shape**（拨 OCPU 加内存），并记住一个 **OCPU 是一个完整
  核**，不是一个超线程。
- [ ] **Core** —— 挂上一个 service account / instance principal；用 cloud-init 做引导。
- [ ] **Working** —— instance pool 加自动扩缩；自定义镜像。
- [ ] **Depth** —— **裸金属 shape**（OCI 那些一等的金属），用于按核授权或性能；用 preemptible
  省成本。

## 存储与数据
- [ ] **Core** —— 挂载 Block Volume；带正确访问控制的 Object Storage。
- [ ] **Working** —— File Storage（NFS）；把 **Archive 层**当成一个取回便宜的备份目标
  （OCI 那个出网优势）。
- [ ] **Depth** —— 跨区域复制以及它（很低的）出网成本；Autonomous Database 基本功。

## 发放与配置
- [ ] **Core** —— 用 **Terraform**（或者 OCI 那个托管的 Terraform，**Resource Manager**）把一套栈
  立起来；干净地销毁它。
- [ ] **Working** —— `oci` CLI / SDK；远端 state。
- [ ] **Depth** —— 给基础设施做 CI/CD；把 Security Zones 当作策略即代码护栏。

## 可观测性与安全
- [ ] **Core** —— 一条会通知人的 Monitoring 告警；查 Logging；**先设一条预算告警**。
- [ ] **Working** —— **Cloud Guard**（姿态加威胁）；用 Vault 放密钥。
- [ ] **Depth** —— **Security Zones**（预防性护栏）；APM tracing；成本异常检测。

## 那个"你到底能不能运维它"的测试

如果你能从代码把那些 **Core** 框做出来 —— 一个 compartment 加一条 policy、一个 VCN、一台带
instance principal 的实例、存储，以及一条预算告警 —— 你就能在一个可用的水平上管理 OCI。因为那些面
和 AWS 映射得这么干净，一个在另一朵云上扎实的管理员很快就能到那条线；注意力要花在那四个刻意的差别
上（compartment、OCPU 对 vCPU、security list 对 NSG、那门策略语言）。
