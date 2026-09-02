---
kind: skill-map
axis: platforms
themes: [cloud]
platforms: [openstack]
derived: true
mirrors: platforms/openstack/skills-map.md
summary: "当你做得到它、并且解释得出那些故障模式时，才勾上一个框。"
---
# OpenStack —— 管理员技能图

> 🌐 **语言：** [English（默认）](../../../../platforms/openstack/skills-map.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/openstack/skills-map.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

一份可勾选的能力清单。分层：

- **Core** —— 没有这个你管理不了 OpenStack。
- **Working** —— 一个扎实的中/高级管理员应有的。
- **Depth** —— 把一个强管理员区分出来的；常常是面试里的分水岭。

**当你做得到它、并且解释得出那些故障模式**时才勾上一个框。逐面对应
[`aws/skills-map.md`](../aws/skills-map.md)。一句诚实的说明：在这个平台上，这些框是那个
**ramp 目标**，不是一份生产深度的声称 —— 见这个模块的[诚实边界](README.md)。

## 身份与访问 —— Keystone
- [ ] **Core** —— 解释 project（租户）、user、role 和 token；也就是别的每一个服务都依赖的那条
  认证流。
- [ ] **Working** —— 范围限定到一个 project 的 role 分配；给自动化用的服务账号。
- [ ] **Depth** —— 联合 / 外部身份；在 Keystone 日志里读一次被拒绝的请求。

## 计算 —— Nova
- [ ] **Core** —— 拉起并管理一个实例；理解 **flavor**（那张尺寸菜单）和来自 Glance 的镜像。
- [ ] **Core** —— 知道 Nova 底下跑的是 **KVM** —— 那个你可能已经在运维的 hypervisor。
- [ ] **Working** —— 逐 project 的配额；用 host aggregate 和 availability zone 做放置。
- [ ] **Depth** —— 热迁移；那个调度器；用 **Ironic** 交付裸金属实例。

## 网络 —— Neutron
- [ ] **Core** —— 一个租户网络（VXLAN overlay）、一个路由器，和一个够得到某个实例的 floating IP。
- [ ] **Core** —— security group（有状态的）—— 并且追查*为什么一个实例上不了网*。
- [ ] **Working** —— provider network；多个租户网络与网络间路由。
- [ ] **Depth** —— 调试 Neutron（运维者最常点名的那个会坏的组件）；在一个 overlay 上跑
  [那架调试阶梯](../../the-stack/02-network.md)。

## 存储 —— Cinder / Swift / Glance（常常是 Ceph）
- [ ] **Core** —— 挂上一个 **Cinder** 块卷；存一个 **Glance** 镜像并从它启动。
- [ ] **Working** —— **Swift** 对象存储；快照；理解在很多部署里 Ceph 坐在这三者之下。
- [ ] **Depth** —— 运维 **Ceph**（健康度、再平衡、placement group）—— 它本身就是一个平台；
  外加 [`the-stack/04`](../../the-stack/04-storage.md) 那门备份纪律。

## 发放与那个控制平面
- [ ] **Core** —— 从 **`openstack` CLI** 驱动它；用 cloud-init 管首次启动。
- [ ] **Working** —— 用 **Heat** stack（或者 Terraform）做声明式发放。
- [ ] **Depth** —— **那个控制平面故障模式**：一个卡死的队列/数据库让 API 停摆，而那些在跑的 VM
  活下来 —— 在它教会你之前就知道它。

## 可观测性与安全
- [ ] **Core** —— 遥测（Ceilometer/Gnocchi）或者所有人都会加上的那套 Prometheus 栈；一条会通知
  到人的告警。
- [ ] **Working** —— 用 Barbican 管密钥；security group 卫生。
- [ ] **Depth** —— 监控那个控制平面本身（它的故障就是你的故障）；跨 project 做容量规划。

## 那个"你到底能不能运维它"的测试

这里那条诚实的及格线和公有云不一样：如果你能把 **DevStack** 立起来、创建一个
project/flavor/网络、拉起一个 cloud-init 实例，并且*解释得出那些控制平面故障模式*，你就能对运维
OpenStack 做推理了 —— 那就是那个 ramp 目标。生产能力（在负载下、在凌晨三点调试 Neutron 和 Ceph）
是只有跑过它才会有的那部分，而这张图把这一点说出来了。
