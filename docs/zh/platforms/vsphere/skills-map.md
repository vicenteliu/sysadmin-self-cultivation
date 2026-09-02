---
kind: skill-map
axis: platforms
themes: [virtualization]
platforms: [vsphere]
derived: true
mirrors: platforms/vsphere/skills-map.md
summary: "当你能把它做出来、并且解释得出它的故障模式时，才勾上一个框 —— 不是在你读过它的时候。"
---
# vSphere —— 管理技能图

> 🌐 **语言：** [English（默认）](../../../../platforms/vsphere/skills-map.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/vsphere/skills-map.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

一份可勾选的能力清单。分层：

- **Core** —— 没有这个你管理不了 vSphere。
- **Working** —— 对一个扎实的中/高级管理员的预期。
- **Depth** —— 把一个强管理员区分出来的东西；常常是面试的分水岭。

**当你能把它*做*出来、并且*解释*得出它的故障模式时**，才勾上一个框 —— 不是在你读过它的时候。
逐面对应 [`aws/skills-map.md`](../aws/skills-map.md)，好让两张能并排读。

## 身份与访问 —— vCenter 权限
- [ ] **Core** —— 解释角色、权限和对象；经由 **AD 组**授予访问权，不是逐用户。
- [ ] **Core** —— 把 vCenter SSO 与 Active Directory / LDAP 集成。
- [ ] **Working** —— 为一件具体任务设计一个最小权限角色（例如一个备份服务账号），而不是把
  Administrator 发出去。
- [ ] **Depth** —— lockdown 模式、ESXi 主机加固，以及在 vCenter 事件里读一次权限拒绝。

## 计算 —— 主机、集群、VM
- [ ] **Core** —— 把 ESXi 主机加进 vCenter；建一个集群；创建/管理 VM。
- [ ] **Core** —— 打开 **DRS**（负载均衡）和 **HA**（主机故障时重启）；解释每一样覆盖什么、
  以及不覆盖什么。
- [ ] **Working** —— 资源池、预留/上限/份额；给副本布置用的反亲和性规则。
- [ ] **Depth** —— vMotion 的前提以及*一次迁移为什么失败*；Fault Tolerance；从性能数据做
  rightsizing。

## 网络 —— vSwitch 及其之上
- [ ] **Core** —— 标准 vSwitch、port group、VLAN 打标；把一台 VM 接到正确的网络上。
- [ ] **Working** —— 跨主机的**分布式 vSwitch**（DVS）；上联、teaming、故障切换。
- [ ] **Depth** —— NSX 分段加分布式防火墙；排查东西向连通性
  （在一个 overlay 上爬那架[调试梯子](../../the-stack/02-network.md)）。

## 存储 —— datastore
- [ ] **Core** —— VMFS 和 NFS datastore；发放一个 VMDK；监控剩余空间（一个**满掉的 datastore**
  是一次集体故障 —— [`the-stack/04`](../../the-stack/04-storage.md)）。
- [ ] **Working** —— **vSAN**（把超融合的本地盘变成一个 datastore）；storage vMotion。
- [ ] **Depth** —— 多路径、SAN/iSCSI 的呈现、VM/vSAN 加密加密钥保管。

## 发放与配置 —— 从镜像建
- [ ] **Core** —— 黄金 VM → **模板** → 带定制规范的克隆。
- [ ] **Working** —— 跨站点的内容库；给 Linux 首次开机用的 cloud-init。
- [ ] **Working** —— 用 **PowerCLI** 做可重复的运维自动化。
- [ ] **Depth** —— 对着 vSphere 的 Terraform；由生命周期管理的主机镜像。

## 生命周期与可观测性
- [ ] **Core** —— 主机**维护模式**加疏散；vCenter/ESXi 的升级路径。
- [ ] **Core** —— 真的会通知人的 vCenter 告警；读性能图表看争用（CPU ready、内存 ballooning、
  datastore 延迟）。
- [ ] **Depth** —— 用 vROps / Aria Operations 看容量与健康；不停机地滚一遍机队。

## 那个"你到底能不能运维它"的测试

如果你能把那些 **Core** 框做出来 —— 一个 DRS/HA 集群、vMotion、你会去监控的 datastore、基于模板的
发放，以及一次干净的升级 —— 你就能在一个可用的水平上跑一片生产 vSphere 估算面。**Working** 和
**Depth** 是那些让一个大集群在负载之下保持健康的东西，也是面试官会去探的东西。这张图是这个仓库里
那张**大部分是真的在生产里做过**的图。
