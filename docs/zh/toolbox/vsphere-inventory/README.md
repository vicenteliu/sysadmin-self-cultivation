# vsphere-inventory

> **输入：** `--server 主机[:端口]`、`--user`、密码走 `VSPHERE_PASSWORD` 环境变量 ·
> **输出：** 一份 JSON 清单文档（stdout 或 `--out`），可选每 VM 一行的 CSV ·
> **风险：** 只读——登录、读属性、登出，什么都不改 · **root：** 不需要
> （一个只读 vSphere 角色就够）

用**纯 Python 标准库**清点一个 vSphere 环境——不装 pyvmomi、不装 SDK、不装
govc。工具直接说 vim25 SOAP 协议（`urllib` 发 XML over HTTPS）：既是迁移评估的
真实输入，也是一个演示——"vCenter API" 不过是你读得懂的 XML。

每台 VM 采集：电源状态、vCPU/内存、guest OS、固件（BIOS/EFI）、虚拟硬件版本、
每块磁盘（容量、thin/thick、VMDK 还是 **RDM**）、每块网卡（型号、网络、MAC）、
**快照数**——正是 [`vm-migration-assess`](../vm-migration-assess/) 要打分的那些
事实。另有 host、datastore、网络。JSON schema 与 [`pve-inventory`](../pve-inventory/)
共用，迁移的源端和目的端可以逐字段对照。

## 用法

```bash
export VSPHERE_PASSWORD='…'                     # 密钥不上命令行
./vsphere-inventory.py --server vcenter.lab --user readonly@vsphere.local \
    --out inventory.json --csv vms.csv
./vsphere-inventory.py --server 127.0.0.1:8989 --user user --insecure   # lab/vcsim
```

`--insecure` 跳过 TLS 校验（自签证书的 lab vCenter）。合适的凭据是一个专用
只读 vSphere 角色——工具从头到尾只读。

日常交互操作想要顺手的 CLI？`govc` 这些都能干且更多。这个工具的位置是：
需要零依赖、可审计、单文件采集器的场合（跳板机、agent、教学）。

## 退出码

| 码 | 含义 |
| --- | --- |
| 0 | 清单已写出 |
| 1 | 连不上端点，或 vCenter 返回 fault（凭据错误等）|
| 2 | 用法：没有提供密码 |

## 验证环境

macOS 26（Python 3.14）与 Ubuntu 24.04 容器（Python 3.12），对 **vcsim**
（govmomi 官方 vCenter 模拟器，4 VM/4 host）验证：完整文档、快照计数（含链式
快照）、磁盘/网卡设备解析；连接拒绝与缺密码路径都演练过。vSphere ✋ 深度是真的
（VCP 级、多年生产）；但**对真实 vCenter 的运行还没做过**——生产版本 vCenter 的
输出细节按 lab 验证对待，不按生产验证对待。
