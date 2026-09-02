---
kind: lab
axis: platforms
themes: [virtualization]
platforms: [openstack]
marker: "🧭"
derived: true
mirrors: platforms/openstack/labs/the-cloud-is-down-the-vms-are-up/README.md
summary: "那个 OpenStack 的标志性事故，做成一个你可以卡住的模型：一条塞满的消息队列让 API 停掉，而九台实例照样应答；只看租户的面板一直是绿的；而租户需要第一次变更时，故障才变成他们的。"
---
# Lab —— 云挂了，VM 还活着

> 🌐 **语言：** [English（默认）](../../../../../../platforms/openstack/labs/the-cloud-is-down-the-vms-are-up/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/openstack/labs/the-cloud-is-down-the-vms-are-up/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

> **输入：** 无 · **输出：** 在一次事故里，API、一次 ping 和两种健康检查各自说了什么 · **风险：** 无
> —— 不用 DevStack、不用云、不用凭据 · **root：** 不需要

**目标：** 把[运维篇](../../operations.md)那个标志性事故变成你已经经历过的东西。*一条塞满的消息
队列或者一个卡住的数据库让 API 停掉，而每一台已经在跑的 VM 照样嗡嗡地转着，一根毫毛都没动。* 那篇
说要在它教训你之前把这件事内化，并且要监控控制面本身，而不只是租户。这个 drill 把队列卡住，向 API
和实例问同一个问题，然后做那句警告真正在讲的事：让一台 compute 主机在队列还塞着的时候死掉。

**你会练到：** 把一次控制面故障和一次租户故障分开；把 day-2 的健康问题按两半来问 —— *租户的 VM 在
不在，以及控制面本身在不在？* —— 并且认出第一种变成第二种的那一刻。

## 这个 lab 为什么是纯本地的

[弧的第三步](../README.md)在 DevStack 上停掉 `n-api`，在 `openstack server list` 报错的同时 ping 一个
floating IP，你应该去做那件事 —— API 在你手下失败而实例还在应答，是一个终端里的一整课。但 DevStack
是一个节点上的一个服务，而这个发现讲的是整个控制面是一条通向*什么*的路径。这里，五个服务是一个布尔
值字典，三台 compute 主机带九台实例，一次 API 调用是一条穿过每个服务的路径，一次 ping 是一条不穿过
任何服务的路径。不用 DevStack、不用凭据、不用 `pip install`。Python 标准库，CI 跑得动它。

## 跑它

```bash
python3 platforms/openstack/labs/the-cloud-is-down-the-vms-are-up/control_plane_drill.py
```

退出码 `0` 表示关于这条教训的每一条断言都成立。

## 你会看到什么

1. **一朵健康的云。** `server list` 返回三台主机上的九台实例；九次 ping 都应答；健康检查是绿的。

2. **RabbitMQ 塞满了。** `server list` 失败，报 *rabbitmq is down*。九次 ping 仍然应答。**云挂了，
   VM 还活着** —— 队列在 API 的路径上，不在任何别人的路径上。

3. **一个问题，两半。** 租户的面板是绿的：他们的实例在应答。一个同时问控制面在不在的健康检查是红
   的。前者是从租户那一侧搭出来的监控在整场事故里报的结果，而那正是它不能作为监控的原因。

4. **有人需要的第一次变更。** 队列还塞着，`compute2` 死了。三台实例停止应答。`server evacuate`
   失败；租户自己的 `server reboot` 也失败。**什么都变不了** —— 而每一次变更都是一次 API 调用。这
   就是控制面故障变成租户故障的那一刻。

5. **队列排空了。** 一条 `server evacuate` 把三台实例挪走；九台应答；健康检查是绿的。修复从来都是
   一次控制面的修复。

6. **带进来的直觉。** 从托管云带来的：*API 挂了* 就是 *云挂了*：九台实例挂了。现实：零台挂了，而
   每一次 API 调用都失败。两个方向都错 —— 什么都没挂，也什么都修不了。

## 验证（别光信这个脚本说的）

```bash
python3 control_plane_drill.py --break-it control-plane-is-data-plane  # exit 1
python3 control_plane_drill.py --break-it green-is-healthy             # exit 1
```

`control-plane-is-data-plane` 让实例和 API 一起死 —— 托管云的直觉，当作模型来跑 —— 八条断言倒下，
从说 VM 还活着的那一条开始。`green-is-healthy` 让租户的面板成为健康问题的全部，恰好两条倒下：控制面
挂着而检查变绿的那一条，以及说监控必须两半都问的那一条。

然后在这个目录里自己卡住另一个服务：

```bash
python3 -c '
from control_plane_drill import Cloud, ControlPlaneDown
c = Cloud(); c.services["keystone"] = False
try: c.server_list()
except ControlPlaneDown as e: print("API:", e)
print("instances answering:", sum(c.ping(n) for n in c.instances), "of 9")
'
```

每个服务给出的形状都一样 —— API 整个失败，实例毫无察觉 —— 因为控制面是一条路径，数据面是另一条。

## 重点

- **控制面故障不是租户故障。** 在跑的实例不会为了继续跑去问 API。那是这场事故能熬过去的原因，也是
  它对一个只问租户的监控隐形的原因。
- **把健康问题两半都问。** *租户的 VM 在* 和 *控制面在* 是两个事实，配两个不同的传呼机。运维篇把它们
  写成一个要点里的两个分句；这个 drill 是第二个分句在那里的原因。
- **故障在第一次变更时变成租户的。** 一次疏散、一次重启、一次扩容、一个自动扩缩器的自愈 —— 每一个
  都是 API 调用，而队列卡住期间死掉的一台 compute 主机，就是三台停到队列排空为止的实例。
- **修控制面；工作负载从来不是问题。** 重启 compute、重刷主机、重建实例是直觉给的药方，而它们也全
  都是 API 调用。

## 拆除

无。这个 drill 把一切放在内存里，什么都不写。
