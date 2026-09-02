---
kind: lab
axis: platforms
themes: [virtualization]
platforms: [vsphere]
marker: "🔨"
derived: true
mirrors: platforms/vsphere/labs/n-plus-one-decays/README.md
summary: "一个集群在建成那天是按对的尺寸建的；然后它一次开一台 VM 地长大，而 admission control 是唯一会注意到 N+1 不再成立的东西。六台主机、五百台 VM，以及那句就是保证本身的拒绝。"
---
# Lab —— N+1 是一个会衰减的数字

> 🌐 **语言：** [English（默认）](../../../../../../platforms/vsphere/labs/n-plus-one-decays/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/vsphere/labs/n-plus-one-decays/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

> **输入：** 无 · **输出：** 四种集群状态下，哪些 VM 重启、哪些停在那里 · **风险：** 无 ——
> 不用 vCenter、不用 ESXi、不用凭据 · **root：** 不需要

**目标：** 把[架构篇](../../architecture.md)的那道算术往时间前方推。六台主机而不是四台，是什么
让一台主机死掉时五百台 VM 还能在 78% 上全部跑着 —— *而 admission control 是让它成为一个保证、而不
是一个指望的东西。* 那篇在集群建成那天说了这句话。这个 drill 是那之后的一年：集群长大了，那个保证
拒绝了一次开机，有人把它关了，而下一次主机故障，就是当初买 N+1 要防的那场事故。

**你会练到：** 把一次拒绝读成保证在做它的工作、按 N+1 而不是按空闲内存去衡量增长、在用到它的那个
事件*之前*就设好 restart priority，以及把一台主机死掉之后的换机等待期当成它本来就是的那个暴露窗口。

## 这个 lab 为什么是纯本地的

[弧的第三步](../README.md)硬关一台嵌套主机、看着 HA 把一台 VM 重启起来，你应该去做那件事 ——
`VMHost` 那一列在你眼皮底下变化，就是握在手里的故障域。但底下的那条教训是一年增长之上的容量算术，
而一个嵌套实验室不会给你看一年。主机是带容量的字典；VM 每台四 GB、带一个 restart priority；HA 是
一个循环，把死掉主机上的 VM 放到负载最轻的幸存者上，直到没有地方为止。不用 vCenter、不用凭据、不用
`pip install`。Python 标准库，CI 跑得动它。

## 跑它

```bash
python3 platforms/vsphere/labs/n-plus-one-decays/n_plus_one_drill.py
```

退出码 `0` 表示关于这条教训的每一条断言都成立。

## 你会看到什么

1. **建成那天尺寸是对的。** 六台 512 GB 的主机；admission control 留下一台主机的量；五百台 VM 开
   机，用掉集群的 65%。

2. **一台主机死了，而那就是 HA 在工作。** 它上面的 83 台 VM 在幸存者上重启，幸存者现在以 **78%**
   跑着一切 —— 架构篇里那个数字，是算出来的而不是引用来的。

3. **集群长大了，而那个保证拒绝了你。** 又要了一百五十台 VM；140 台开起来了，第 141 台被拒绝，正好
   停在 2560 GB 可用里的 2560 GB。那次拒绝就是 N+1 在说不。

4. **那个标准的点击。** admission control 关掉，150 台全开，集群显示六台主机的 85%，还有大把空闲
   内存。主机再死一次：98 台 VM 重启，**10 台没有地方可去。** 纸面上的 HA，就是跑到没地方的 HA。

5. **谁停在那里，要么是一个决定，要么是一个意外。** 设了 restart priority，留下的十台就是有人排在
   最低的那十台。不设的话，同样的十台是 `vm-440 … vm-494` —— 生产 VM，由 HA 碰巧到达它们的顺序选中。

6. **N+1 是一次故障。** 在 admission control 的上限上，第一台主机的损失被吸收了。在第一台换回来之
   前的第二次损失，让 **128 台 VM 停机**，保证还开着。换机等待期就是暴露窗口，这也是运维篇把死掉的
   那台主机叫作事故的原因。

## 验证（别光信这个脚本说的）

```bash
python3 n_plus_one_drill.py --break-it admission-off        # exit 1
python3 n_plus_one_drill.py --break-it ha-ignores-capacity  # exit 1
```

`admission-off` 让集群按那次点击的假设去跑 —— 拒绝是个麻烦，内存是空着的 —— 两条断言倒下：增长
不再被拒绝，而那篇的集群不再守它自己的承诺。`ha-ignores-capacity` 让 HA 按人们听到 *HA* 这个词的
方式去跑 —— 全都会回来 —— 八条倒下，因为一次从不检查余量的重启，会把 VM 重启到已经满了的主机上，
而那不是重启。

然后在这个目录里自己驱动模型：

```bash
python3 -c '
from n_plus_one_drill import Cluster, fill
c = Cluster(6); print(fill(c, 700, "vm"), "of 700 accepted; refused from", c.refused[0])
'
```

把文件里的 `HOSTS` 改成七再跑：拒绝点正好移动一台主机的 VM 数量，那就是买第七台主机买到的全部。

## 重点

- **拒绝就是保证。** 一次被 admission control 拒绝的开机，是 N+1 在告诉你集群已经到了它被建成的
  那个尺寸。关掉它不会增加容量；它拿走的是唯一知道这件事的东西。
- **空闲内存不是余量。** 六台主机的 85% 是五台的 102%，而要紧的那一天你手里只有五台。
- **restart priority 是在安静的日子里设的。** 事件之后再说哪些 VM 要紧已经晚了；HA 已经按它碰巧到达
  的顺序决定了。
- **N+1 是一次故障，换机等待期是那个窗口。** [运维篇](../../operations.md)把 HA 事件叫作 HA 在工作、
  把死掉的主机叫作事故；这个 drill 是那句话背后的算术：保证花掉之后，下一次损失就是一场事故，直到
  货架送来一台主机。

## 拆除

无。这个 drill 把一切放在内存里，什么都不写。
