---
kind: lab
axis: cross-cutting
themes: [containers]
platforms: []
derived: true
mirrors: cross-cutting/labs/k8s-reconcile-loop/README.md
summary: "Terraform 状态那一课的运行时双胞胎：你不是在管理进程，你是在声明期望态，而一个 controller 会永远地把实际态驱向期望态。删掉一个 pod，它会回来。"
---
# Lab —— pod 是牛，而一个 controller 会永远地调和

> 🌐 **语言：** [English（默认）](../../../../../cross-cutting/labs/k8s-reconcile-loop/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`cross-cutting/labs/k8s-reconcile-loop/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

**目标：** 感觉到那件**一个 Linux/systemd/Docker 系统管理员在 Kubernetes 上会搞错**的事 ——
你不是在管理进程，你是在声明期望态，而一个 **controller** 跑着一个调和循环，持续地把
*实际态 → 期望态*驱过去。它是 [Terraform 状态那一课](../../terraform-support.md)的运行时双胞胎：
声明式配置 + 一个会收敛的引擎 —— 一个在发放的时刻，一个在运行时*永远*进行着。

```
desired    the Deployment spec: replicas + pod template (you write this)
actual     the set of Pods that exist right now
reconcile  the controller closes the gap, every tick, forever
```

它演练什么 —— 从那一个模型里掉出来的六条教训：
1. **删掉一个 Pod → 它会回来。** 那个 controller 会把它重建出来（自愈）；你没法"就把这个 pod 删
   了" —— 去改那个期望态。
2. **手动修一个 Pod → 那个修复会消失。** `kubectl exec` 进去给一个在跑的 pod 打补丁，下一次调和就
   会按那个模板把它换掉。是牛，不是宠物 —— *去改那份 spec。*
3. **调整期望值 → 数目会收敛**（3 → 5 → 2）。你编辑的是那份 spec，不是那些 pod。
4. **坏镜像 → CrashLoopBackOff。** 那个 controller 会不停地重启一个崩溃的 pod，但重启一份坏的
   spec 会永远循环下去 —— *去改那个模板*，别重启。
5. **改那个模板 → 滚动替换。** 改掉那个期望的镜像，那个 controller 就把每一个 pod 都滚一遍；
   你改 spec，controller 来滚。
6. **readiness 失败 → 从 endpoints 里被摘掉。** 一个 Running 但没 Ready 的 pod 会被从那个 Service
   的 endpoints 里移除 —— *"服务挂了但 pod 还在 Running"* = 去查 endpoints。

## 为什么在本地

不用集群、不用 `kubectl`、不用云。这个演练是一份大约 200 行的 Deployment controller 调和循环模型
—— 期望副本数 + 模板、那些重建/伸缩/滚动的决策，以及那道 readiness→endpoints 的闸门 —— 好让你检视
的是那份*逻辑*，不是满屏的 YAML。它在任何跑得了 Python 的地方都跑得起来，在 CI 里也是。

## 跑

```bash
python3 reconcile_drill.py
```

## 你会看到什么

六个被叙述出来的步骤，每一个都带一个 `OK`/`XX`：一个被删掉的 pod 被重建出来；一次手动修复在替换时
消失；伸缩时那个数目收敛；一个坏掉的镜像在 CrashLoopBackOff 里循环（然后靠改模板、而不是靠重启修
好）；一次模板变更把每一个 pod 都滚了一遍；以及一个没 Ready 的 pod 被从 Service endpoints 里摘掉。
最后给出一个 PASS 判定，`exit 0`。

## 验证（要紧的那部分）

exit `0` = 每一条教训都成立；它兼作一个 CI 检查。现在**故意把这个模型弄坏** —— 有两条彼此独立的
破坏路径：

```bash
python3 reconcile_drill.py --sabotage no-reconcile        # controller 停止调和 -> 被删掉的 pod 就死了 -> 步骤 1 失败，exit 1
python3 reconcile_drill.py --sabotage ready-ignores-probe # endpoints 无视 readiness -> 一个坏掉的 pod 照样收流量 -> 步骤 6 失败，exit 1
```

如果那个 controller 睡着了 pod 还能自愈，那这个调和循环本来就什么都没做；如果一个没 Ready 的 pod
还在收流量，那这道 readiness 闸门本来就不承重。这些失败，正是这个模型确实要紧的证据。

## 重点

有两条系统管理员反射在这里同时被纠正。第一，**"进程是那个单位，而我在管它"** —— 在 Kubernetes 里
*Deployment/spec* 才是那个单位，而 pod 是一次性的；删掉或者编辑一个 pod 是徒劳的，因为一个
controller 会把它调和回来。第二，**"SSH 进去修一下"** —— 一个在运行中的 pod 内部做的修复，会在那个
pod 被替换时一起死掉。那门纪律是：声明期望态、改那份 *spec* 而不是那个 pod，而当"服务挂了"的时候，
去查 **endpoints**（readiness → selector）。pod 是牛。完整的工单目录见
[Kubernetes support 笔记](../../kubernetes-support.md)，对象模型见
[`kubernetes.md`](../../kubernetes.md)。

## 拆除

没有 —— 它就是一个自包含的脚本。把这个目录删掉就行。
