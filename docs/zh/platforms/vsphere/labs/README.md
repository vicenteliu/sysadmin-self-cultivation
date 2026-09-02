---
kind: guided-run
axis: platforms
themes: [virtualization]
platforms: [vsphere]
marker: "🔨"
derived: true
mirrors: platforms/vsphere/labs/README.md
summary: "对着一个 lab vCenter（或者嵌套 ESXi）做的三次 guided run —— 在这个平台上，那句诚实的说明是它们已经跑过了，在生产里，跑了很多年。"
---
# vSphere —— Guided run

> 🌐 **语言：** [English（默认）](../../../../../platforms/vsphere/labs/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/vsphere/labs/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

对着一个 lab vCenter（或者嵌套 ESXi）做的三次 guided run。读 vMotion 和做 vMotion 是两项不同的
技能 —— 而在这个平台上，那句诚实的说明是：这些*已经跑过了*，在生产里，跑了很多年。

**这些是 [guided run](../../../CONTEXT.md)，不是 lab。** 每一次都需要一个真实环境，所以这里没有
任何东西能断言你做过它，而 CI 也跑不了它。那就是全部的区分，而且它不是降级 —— 一次 guided run
够得到真实的延迟、真实的报错和真实的账单，而那是没有模型做得到的。

> **地面规则：** 用一个 **lab/嵌套集群**，在破坏性步骤之前先打快照，做完把那些 VM 清理掉。
> 绝不要在生产主机上做测试。

## 为什么是命令行

vSphere 有一个很棒的 GUI —— 而老手们仍然用 **PowerCLI**（或者 `govc`）做自动化，因为命令行
**更快**（不用在 200 台 VM 上一路点过去）、**更精确**、**可复现**（每个维护窗口跑同一个脚本）、
**可评审**。GUI 是给一次性的事和看的；PowerCLI 是用来运维一片机队的。这就是那个差别最明显的平台：
没有人会把一次滚动的主机升级点两遍。

## 那条三节 guided run 弧

### Run 01 —— 连接 + 盘点（那一招"把所有东西列出来"）

连上 vCenter，从 **PowerCLI** 盘点这片估算面 —— 在一个真实集群上，你绝不会靠点鼠标去做的那一招：

```powershell
Connect-VIServer -Server vcenter.lab.local -User administrator@vsphere.local

# 每一台 VM、它的主机、电源状态和资源用量 —— 一行搞定
Get-VM | Select Name, PowerState, NumCpu, MemoryGB, VMHost | Sort-Object VMHost | Format-Table

# 每一台主机，以及它的集群/连接状态
Get-VMHost | Select Name, ConnectionState, @{N='Cluster';E={$_.Parent}}, Version | Format-Table

# datastore + 剩余空间（一个满掉的 datastore 是一次大面积故障 —— 盯住这个）
Get-Datastore | Select Name, @{N='FreeGB';E={[math]::Round($_.FreeSpaceGB)}}, @{N='CapGB';E={[math]::Round($_.CapacityGB)}} | Format-Table
```

**验证：** 那些数目和 vCenter 的清册视图对得上 —— 而且你是用一条命令拿到的，不是三个标签页。

### Run 02 —— 从一个模板发放一台 VM

带着一份 customization spec 从一个黄金模板克隆 —— 也就是 vSphere 上的那条镜像流水线
（[`the-stack/03`](../../../the-stack/03-compute-and-images.md)）：

```powershell
# 从一个模板把一台 VM 克隆到选定的主机 + datastore 上
New-VM -Name lab-vm01 -Template "ubuntu-2204-template" `
  -VMHost (Get-VMHost esxi01.lab.local) -Datastore (Get-Datastore vsanDatastore) `
  -OSCustomizationSpec "linux-dhcp"

Start-VM -VM lab-vm01

# 确认放置位置 + tools 状态
Get-VM lab-vm01 | Select Name, VMHost, PowerState, @{N='Tools';E={$_.ExtensionData.Guest.ToolsStatus}}
```

**验证：** 那台 VM 在你点名的那台主机上启动，并带着定制好的身份 —— 是牛，不是一只手工搭起来的
宠物。**拆除：** `Stop-VM lab-vm01 -Confirm:$false; Remove-VM lab-vm01 -DeletePermanently -Confirm:$false`。

### Run 03 —— 看着 HA 重启一台 VM（故障域，变得摸得着）

[`the-stack/01`](../../../the-stack/01-physical.md) 那一课故障域，落在它来自的那个平台上 ——
再加上每次升级都会用到的那次维护模式疏散：

```powershell
# 把一台主机置入维护模式 —— DRS/vMotion 会零停机地把它上面的 VM 疏散走
Set-VMHost -VMHost esxi02.lab.local -State Maintenance -Evacuate

# ……确认那些 VM 已经从它上面挪走了
Get-VMHost esxi02.lab.local | Get-VM      # 应该是空的

# 把它拉回来
Set-VMHost -VMHost esxi02.lab.local -State Connected

# （HA 演练，lab 里是安全的）硬断一台主机的电，看着 HA 在别处重启它上面的 VM：
#   在一个嵌套 lab 里，把一个 ESXi 节点断电，然后跑：
Get-VM lab-vm01 | Select Name, PowerState, VMHost   # HA 重启它时 VMHost 会变
```

**验证：** 维护模式下那些 VM 零停机地疏散走了；在一次模拟的主机故障里，HA 把它们在一台活着的主机
上重启了 —— 那个故障域，握在你自己手里。

## 弧之外 —— 一个纯本地的演练

上面那条三节弧需要一个 lab vCenter。还有一个 lab **什么都不需要** —— 一个纯本地、只用标准库、能自我
验证的演练，接着那篇[运维篇](../operations.md)：

### `n-plus-one-decays/` —— N+1 是一个会衰减的数字 ✅ 已建（纯本地）

把架构篇的六主机集群往时间前方推，证明 admission control 的拒绝*就是*保证：增长正好在 N+1 不再成立
的那一点被拒绝，把它关掉的那次点击让下一次主机损失留下十台 VM 停机，而换机窗口内的第二次损失即使
保证还开着也是一场事故。见 **[`n-plus-one-decays/`](n-plus-one-decays/)**。

```bash
python3 n-plus-one-decays/n_plus_one_drill.py   # exit 0 = 那些教训成立；在 CI 里跑
```

---

一句诚实的说明：这是那个 🔨 平台 —— 这些 lab 是那份生产工作被写下来，不是一条 ramp。GUI 对命令行
那个论点在这里落得最重：在机队规模上，你*只*通过 PowerCLI 运维。
