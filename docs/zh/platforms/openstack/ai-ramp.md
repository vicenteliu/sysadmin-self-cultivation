---
kind: companion
axis: platforms
themes: [cloud]
platforms: [openstack]
marker: "mixed"
derived: true
mirrors: platforms/openstack/ai-ramp.md
summary: "怎么在 OpenStack 上快速走到「有能力做推理」—— 以及一句关于 AI 在哪儿停下的诚实交代。"
---
# OpenStack —— AI 辅助的 ramp

> 🌐 **语言：** [English（默认）](../../../../platforms/openstack/ai-ramp.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/openstack/ai-ramp.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

> 怎么在 OpenStack 上快速走到*有能力做推理* —— 以及一句关于 AI 在哪儿停下的诚实交代。OpenStack
> 是 ramp 方法的一个干净演示，**同时**也是它极限的一个干净演示：那些概念几分钟就迁移过来了，但
> 这个平台真正的难处是运维性的，而那部分你得靠跑它去挣。

[`WHY.md`](../../WHY.md) 的那个前提：一个有经验的管理员加上 AI，可以在几天内对一个从没跑过的平台
做推理。OpenStack 奖赏这一点 —— 它那些面干净地映射到一份"虚拟化 + Linux"背景已经懂的东西上
（KVM、VLAN/overlay、Ceph 式的存储、IAM）。但它同时也标出了整个仓库要对之诚实的那条边界：
**AI 能教你那套架构；它给不了你凌晨三点那次 Neutron 事故。**

## 那个循环（OpenStack 口味）

1. **锚到你已经懂的东西上。** *"我跑 KVM 和 Proxmox，我懂 VLAN 和 overlay、Ceph 式的存储，还有
   IAM。把 Nova、Neutron、Cinder 和 Keystone 映射到那上面 —— 什么是一样的、什么只是改了名、什么
   是真正新的？"* 因为那个 hypervisor（KVM）已经是你的了，这次映射落得很快。
2. **拿到那个 80/20。** *"在所有 OpenStack 项目里，一个运维者每天真正碰的是哪几个，哪些是可选
   的？"*（Keystone/Nova/Neutron/Cinder/Glance 是核心；那条长尾可以等。）
3. **生成那个产物。** *"用 `openstack` CLI 创建一个 project、一个 flavor、一个带路由器的租户网络，
   然后拉起一个 cloud-init 实例的那些命令。"* 第一稿几秒钟就有。
4. **对着文档验证** —— 服务名、CLI 参数和 API microversion 在各个 release 之间会漂；假定那份草稿
   有 90% 是对的，然后去猎那 10%。
5. **在 DevStack 里跑它。** 一台 VM 里的单节点一体化 OpenStack，就是这个平台上那个用完即弃的账号
   —— 现实是那个评审者，而在这里它是免费的。
6. **让 AI 反过来评审它** —— *"这套网络/配额设计里的安全或容量风险在哪儿？"*

## AI 在哪儿挣得了它的饭钱

- **那次概念翻译** —— Nova↔EC2、Neutron↔VPC、Cinder↔EBS、Keystone↔IAM、Glance↔AMI ——
  AI 在一次提问里就把整套组件映射到你（或者读者）已经懂的那些云上。
- **起草 CLI/Heat** —— 那些 `openstack` 命令和 Heat 模板，作为一份你要去验证的初稿。
- **解读报错** —— 把一次失败的 `server create` 或者一段 Neutron 的 trace 贴进去：*"这指向什么？"*

## AI 会烧到你的地方（验得最狠）

- 它会**把各个 OpenStack release 混起来** —— CLI 参数、API microversion 和项目名都会变；AI 会很
  自信地把不同年代掺在一起。
- 它会**发明不存在的 `openstack` 子命令和 Heat 资源类型**。
- 它**低估那个控制平面** —— AI 会帮你*用* OpenStack，而对*跑*它那份运维负担保持沉默（那个队列、
  那个数据库、Ceph 健康度），而那才是真正难的部分。

## 那条诚实的极限

这是这个仓库的诚实政策最看得见的那个平台。AI 把你 ramp 到*能对* OpenStack *做推理* —— 那套架构、
那条组件流、那个 CLI —— 而且是真的快。它**不会**把你 ramp 到生产能力，因为 OpenStack 真正的那项
技能是在负载下运维一个控制平面，而那是挣来的，不是提问出来的。那句真话
（[`README.md`](README.md)）：一份扎实的架构把握加上一条可验证的 ramp，底下那个 hypervisor
（KVM）是真实的 🔨 地面，而 OpenStack 那个控制平面是诚实的 🧭 —— 正是这个仓库存在着要守住的那个
区别。
