# vm-migration-assess

> **输入：** 一份 [`vsphere-inventory`](../vsphere-inventory/) JSON 文档
> （`--in 文件` 或 stdin）· **输出：** 每 VM 一个裁决的报告（或 `--json`）·
> **风险：** 只读——纯评估，两边环境都不碰 · **root：** 不需要

回答每一场 VMware→Proxmox 对话的第一个问题：**这些 VM 里哪些真能搬，每台会
在哪里跟你较劲？** 喂进清单 JSON，每台 VM 得到一个裁决——`EASY` / `MODERATE` /
`HARD`——以及裁决背后的具体发现，所以输出读起来是工作清单，不是打分游戏。

## 规则表

| 严重度 | 发现 | 为什么要紧 |
| --- | --- | --- |
| **hard** | RDM（裸设备映射）磁盘 | Proxmox 没有直接对应物——这块存储要重新设计 |
| **hard** | EOL Windows guest（XP/2003/2000/NT）| 没有 virtio 驱动；只能走 legacy 设备的权宜方案 |
| moderate | 有快照 | 快照链不转换——导出前先合并 |
| moderate | 现代 Windows guest | cutover 前/时必须装 virtio 驱动 |
| minor | Linux 上非 virtio 网卡 | 型号会换成 virtio；驱动本来就在内核里 |
| minor | EFI 固件 | 以 OVMF 重建 VM，核对 Secure Boot 预期 |
| minor | 磁盘总量 > 2 TiB | 规划传输窗口 |
| minor | 虚拟硬件老于 vmx-10 | 核实古董 guest 的各种假设 |
| info | 开着机 | 排停机窗口，或规划一次重同步 cutover |
| info | thick 置备磁盘 | 导出时按全尺寸走 |

裁决 = 最重的发现（info/minor → EASY）。规则就是一个读得懂的函数——你的
机群需要什么就往里加。

## 用法

```bash
./vm-migration-assess.py --in inventory.json          # 人读的报告
../vsphere-inventory/vsphere-inventory.py … | ./vm-migration-assess.py   # 管道
./vm-migration-assess.py --in inventory.json --json   # 机器可读
```

## 退出码

| 码 | 含义 |
| --- | --- |
| 0 | 已评估；没有 HARD 的 VM |
| 1 | 已评估；至少一台 HARD（人和流水线都在这上面分支）|
| 2 | 输入不是可读的清单文档 |

## 验证环境

macOS 26（Python 3.14）与 Ubuntu 24.04 容器（Python 3.12）：对 vcsim 的实链
（带快照的 VM 正确判 MODERATE）+ 一份把每条规则都打中的手工 fixture
（RDM→HARD、XP→HARD、Windows 2022 + EFI + 3 TiB + 快照→MODERATE、干净
Linux→EASY 零发现）。规则的*权重*是判断不是测量——lab 验证，且刻意保守。
