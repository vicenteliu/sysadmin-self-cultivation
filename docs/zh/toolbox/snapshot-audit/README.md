# snapshot-audit

> **输入：** 一份或多份清单 JSON（[`vsphere-inventory`](../vsphere-inventory/)
> 和/或 [`pve-inventory`](../pve-inventory/)；不给参数则读 stdin）· **输出：**
> 被标记 VM 的卫生报告（或 `--json`）· **风险：** 只读——只标记；删除或合并
> 始终是人的决定 · **root：** 不需要

被遗忘的快照是定时炸弹：它一直长到撑爆 datastore，拖累 I/O，而深链正是迁移
栽跟头的地方。这个工具读清单文档——**两个 hypervisor，一次审计**（因为
`vsphere-inventory` 和 `pve-inventory` 共用 schema）——把违反三条阈值的快照
全部标出：

| 阈值 | 默认 | 为什么 |
| --- | --- | --- |
| `--max-age-days` | 3 | VMware 自己的指引：快照别留过 ~72 小时 |
| `--max-depth` | 2 | 深链伤 I/O，迁移时也不转换 |
| `--max-count` | 3 | 一台 VM 挂一堆快照，通常说明没人负责清理 |

没有创建时间的快照报 `INFO`（年龄无法判断）；在快照明细存在之前生成的旧清单
会得到一条 `INFO` 提示重新采集——审计从不靠猜。

## 用法

```bash
./snapshot-audit.py inventory.json                      # 单侧
./snapshot-audit.py vsphere.json pve.json               # 两侧，一次审计
./snapshot-audit.py --max-age-days 7 --json inv.json    # 你的策略，机器可读
../vsphere-inventory/vsphere-inventory.py … | ./snapshot-audit.py    # 管道
```

## 退出码

| 码 | 含义 |
| --- | --- |
| 0 | 已审计；没有卫生警告（允许有 INFO 行）|
| 1 | 至少一条警告——有东西要清理了 |
| 2 | 输入不是可读的清单文档 |

## 验证环境

macOS 26（Python 3.14）与 Ubuntu 24.04 容器（Python 3.12）：vcsim 上现造的
3 层深快照链（深度警告）+ 捆绑的 PVE fixtures（约 12 天前的快照 → 年龄警告）
在同一次运行中审计；放宽阈值后干净通过；无明细的旧文档与不可读输入分别走
INFO / exit-2 路径。阈值编码的是公开指引与判断，不是测量——按你的机群调。
