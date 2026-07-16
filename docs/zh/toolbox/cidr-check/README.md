# cidr-check

> **输入：** CIDR 网段（参数或 `--file plan.txt`）· **输出：** stdout 上重叠报告 ·
> **风险：** 只读，不碰任何东西 · **root：** 不需要

在 CIDR 重叠变成对等连接冲突、VPN 路由意外、或无法合并的多云网络之前先发现它。
把规划里的每个子网都喂给它；它报告每一对重叠，并标出完全包含关系。IPv4 和 IPv6
都支持；比较只在同一地址族内进行。

从 multi-cloud lab 生长而来：经典翻车是两个团队（或两朵云）各自独立挑了
`10.0.0.0/16`。

## 用法

```bash
./cidr-check.py 10.0.0.0/16 10.0.1.0/24 192.168.0.0/24
./cidr-check.py --file plan.txt      # 行格式：CIDR [label] · 支持 # 注释
```

```
OVERLAP: 10.0.0.0/16 (aws-prod) <-> 10.0.1.0/24 (gcp-dev) — first contains second
1 overlap(s) across 3 ranges
```

## 退出码

| 码 | 含义 |
| --- | --- |
| 0 | 无重叠 |
| 1 | 发现重叠 |
| 2 | 用法错误或无法解析的 CIDR |

## 验证环境

仅 Python 3.9+ 标准库。已验证：macOS 26（Python 3.14）、Ubuntu 24.04 容器
（Python 3.12）。lab 验证过，非生产级加固。
