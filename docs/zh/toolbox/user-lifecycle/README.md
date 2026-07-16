# user-lifecycle

> **输入：** 一个 `username,action[,groups]` 的 CSV · **输出：** 计划（dry-run）或
> 逐用户结果（`--apply`）· **风险：** **默认 dry-run**——仅 `--apply` 才改动状态 ·
> **root：** `--apply` 时必需

大规模的 joiner/mover/leaver 是一个 CSV，不是五十行手敲的 `useradd`。本工具从一个
文件批量执行用户创建和停用——真实基础设施 JD 里最密集的技能集群，可复现地完成。

两个值得知道的安全选择：

- **默认 dry-run。** 不加 `--apply` 时只打印将要做什么、不碰任何东西。你总能先看到计划。
- **停用 ≠ 删除。** 离职者被**锁定、过期、踢下线**，绝不 `userdel`——他们的文件和你的
  审计线索必须留存。删除是另一个需要慎重的决定。新建账户**锁定且无密码**；用 SSH key
  或带外 `passwd` 重置发给本人（命令行里不放任何密钥）。

## CSV 格式

```
# username,action,groups
alice,create,sudo|docker
carol,create
bob,disable
```

`#` 注释和空行忽略；`groups` 可选、仅 create 用。

## 用法

```bash
./user-lifecycle.sh users.csv              # dry-run——打印计划
sudo ./user-lifecycle.sh users.csv --apply # 执行
```

## 退出码

| 码 | 含义 |
| --- | --- |
| 0 | 成功（已规划，或已应用且无失败）|
| 1 | 一个或多个动作失败 |
| 2 | 用法错误、CSV 有误、或 `--apply` 未用 root |

## 验证环境

Ubuntu 24.04 容器（dry-run 及 root 下 `--apply`：带/不带组的创建、幂等重跑、停用、
用户不存在等情形）。lab 验证过，非生产级加固。
