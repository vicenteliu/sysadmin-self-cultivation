# patch-report

> **输入：** 无（`--quiet` 只出计数）· **输出：** stdout 上待更新报告 ·
> **风险：** 只读——从不安装、从不刷新元数据 · **root：** 出报告不需要

有哪些补丁在等着装、这台机器需不需要重启？一条命令回答两者，两大包管理家族都支持：
apt（Debian/Ubuntu——`/var/run/reboot-required` 及导致它的软件包）或 dnf/yum
（RHEL 系——`check-update`、安全公告计数、`needs-restarting -r`）。

刻意的范围裁剪：本工具只报告机器**已有**的元数据——它绝不自己跑
`apt update`/`dnf makecache`，因为一个只读报告不该成为打你镜像源的那个动作。
按你自己的计划去刷新。

## 用法

```bash
./patch-report.sh            # 完整列表
./patch-report.sh --quiet    # 只出计数 + 结论——适合 cron/agent
```

## 退出码

| 码 | 含义 |
| --- | --- |
| 0 | 完全打好补丁，无待重启 |
| 1 | 有待更新和/或需重启 |
| 2 | 无受支持的包管理器 / 查询失败 |

## 验证环境

Ubuntu 24.04 容器（有待更新、干净、需重启等情形）。dnf 路径在 Rocky Linux 9 容器
验证。lab 验证过，非生产级加固。
