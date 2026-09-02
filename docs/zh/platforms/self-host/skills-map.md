---
kind: skill-map
axis: platforms
themes: [virtualization]
platforms: [self-host]
derived: true
mirrors: platforms/self-host/skills-map.md
summary: "当你做得到它、并且解释得出那些故障模式时，才勾上一个框。"
---
# 自托管 / 裸金属 —— 管理员技能图

> 🌐 **语言：** [English（默认）](../../../../platforms/self-host/skills-map.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/self-host/skills-map.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

一份可勾选的能力清单。分层：

- **Core** —— 没有这个你跑不了裸金属。
- **Working** —— 一个扎实的中/高级管理员应有的。
- **Depth** —— 把一个强管理员区分出来的；常常是面试里的分水岭。

**当你做得到它、并且解释得出那些故障模式**时才勾上一个框。逐面对应
[`aws/skills-map.md`](../aws/skills-map.md)。一句诚实的说明：在这个平台上，这些框大多是*从生产里
勾上的* —— 见这个模块的[诚实边界](README.md)。

## 身份与访问 —— 目录是你在跑
- [ ] **Core** —— Linux 的用户/组/sudo、SSH key 管理、PAM 基础。
- [ ] **Core** —— 跑一个目录（AD 或者 **OpenLDAP**）；把认证集中起来，而不是逐机器建账号。
- [ ] **Working** —— 由那个目录支撑的 SSO；最小权限的 sudo 策略。
- [ ] **Depth** —— 证书/PKI 基础；bastion + 跳板机的访问模式。

## 计算 —— 那个物理盒子
- [ ] **Core** —— 上架、接线、把一台服务器启动起来；在没有操作系统的时候用
  **BMC/IPMI/iLO/iDRAC** 够到它。
- [ ] **Core** —— 在你自己的硬件上用 **KVM** 或 **Proxmox** 跑 VM。
- [ ] **Working** —— 固件/BIOS 管理；硬件健康度监控。
- [ ] **Depth** —— GPU 直通；NUMA/CPU pinning；那个硬件多样性问题（一个镜像，很多型号）。

## 网络 —— 两个平面都是你的
- [ ] **Core** —— VLAN、交换机配置、一台防火墙；由你运维的 **DNS（BIND）**和 **DHCP**。
- [ ] **Core** —— 追查*为什么一台主机上不了网* —— [那架调试阶梯](../../the-stack/02-network.md)，
  跑在你自己拥有的硬件上。
- [ ] **Working** —— NTP、子网间路由、VPN/站点到站点。
- [ ] **Depth** —— EVPN/VXLAN overlay；非对称路由与 MTU 的调试。

## 存储 —— 用金属做的
- [ ] **Core** —— RAID 级别和那个重建窗口；本地盘 + 一个 NAS/NFS 共享。
- [ ] **Core** —— 监控可用空间；一块满掉的盘就是一次故障
  （[`the-stack/04`](../../the-stack/04-storage.md)）。
- [ ] **Working** —— SAN/iSCSI 的呈现、多路径；快照。
- [ ] **Depth** —— 用 Ceph/MinIO 做对象存储；**RAID 不是备份** —— 一次测过的 3-2-1 恢复。

## 发放 —— 那条流水线
- [ ] **Core** —— **PXE 启动** + 一个黄金镜像 + **cloud-init** 首次启动，全程不用手。
- [ ] **Core** —— 规模上纳管全盘加密，并带密钥托管。
- [ ] **Working** —— 用 **Ansible** 管配置；按硬件世代做镜像版本管理。
- [ ] **Depth** —— Terraform/MAAS 式的裸金属发放；重装镜像优先于原地打补丁。

## 可观测性与安全
- [ ] **Core** —— Prometheus/Grafana 或等价物；从被监控之物*之外*去监控。
- [ ] **Core** —— 打补丁纪律；把 CIS/加固基线烤进镜像里。
- [ ] **Working** —— 集中日志（ELK/Loki）；IPMI/硬件告警。
- [ ] **Depth** —— 物理访问控制；气隙/受控环境下的运维。

## 那个"你到底能不能运维它"的测试

如果你能不用手地把一片机队 PXE 装机、能带外够到一台死机、能跑那些核心服务
（DNS/DHCP/LDAP/NTP）、能设计故障域，并且能让存储活得过硬盘的死亡 —— 你就能在规模上跑裸金属了。
这是这个仓库里唯一一张技能图，"你做过这个吗？"的诚实答案是*做过，而且是在机队规模上* ——
而它就是那些云的技能图被*对照着*来读的那份底子。
