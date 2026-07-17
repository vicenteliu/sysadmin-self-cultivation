# pve-inventory

> **输入：** 在 PVE 节点上无需输入（现场跑只读 `pvesh get`）；或 `--from 目录`
> 读捕获的输出 · **输出：** 一份 JSON 清单文档（stdout 或 `--out`），schema 与
> [`vsphere-inventory`](../vsphere-inventory/) 相同 · **风险：** 只读——只有
> `pvesh get`，从不写集群 · **root：** 现场模式在 `pvesh` 所在处运行（PVE 节点 shell）

VMware→Proxmox 迁移的目的端：把 Proxmox VE 集群清点成与 `vsphere-inventory`
**完全相同的 JSON schema**，迁移前后逐字段对照——VM 对 VM、磁盘对磁盘、
网卡对网卡。

每台 VM 采集：电源状态、vCPU/内存、guest OS 类型、固件（SeaBIOS/OVMF →
`bios`/`efi`）、机器类型、磁盘（容量、qcow2/raw/直通）、网卡（型号、bridge、
MAC）、快照数（`current` 标记不计）。另有节点、存储、以及 VM 配置引用到的 bridge。

## 用法

```bash
# 在 PVE 节点上
./pve-inventory.py --out pve.json

# 在任何地方，用捕获的输出——在节点上这样捕获：
#   pvesh get /cluster/resources --output-format json > resources.json
#   pvesh get /version --output-format json > version.json
#   pvesh get /nodes/<node>/qemu/<vmid>/config   --output-format json > config-<vmid>.json
#   pvesh get /nodes/<node>/qemu/<vmid>/snapshot --output-format json > snapshot-<vmid>.json
./pve-inventory.py --from ./captured/
```

[`fixtures/`](../../../../toolbox/pve-inventory/fixtures/) 是一份完整的示例捕获
（一个 PVE 8 节点 + 一台 Linux VM + 一台 OVMF Windows 11 VM）——它记录了文件
的准确形状，也给你一次干跑：`./pve-inventory.py --from fixtures`。

## 退出码

| 码 | 含义 |
| --- | --- |
| 0 | 清单已写出 |
| 1 | `pvesh` 缺失/失败（现场模式），或捕获目录不完整 |
| 2 | 用法错误 |

## 验证环境

解析器与 schema 在 macOS 26（Python 3.14）和 Ubuntu 24.04 容器（Python 3.12）
上对捆绑的 PVE-8 形状 fixtures（`--from`）验证过，含 cdrom/EFI 盘/TPM 状态的
排除与 `current` 快照处理。**在真实 PVE 节点上的现场运行仍是操作者的下一步**——
fixtures 按文档化的 `pvesh` 输出形状构造，但这一行只会在工具真跑过实机之后
更新。诚实 scope：家庭 lab 级 Proxmox，不是机群生产经验。
