# baseline-check

> **输入：** 无 · **输出：** 每项 PASS/FAIL/INFO/SKIP + 汇总 · **风险：** 只读，
> 不改任何东西 · **root：** 可选——shadow 和 sshd 生效值检查需要它

一组刻意精简、高信号的加固审计——审查者会最先看的十项：SSH root 登录与密码认证
姿态、防火墙是否启用、UID-0 唯一性、空密码字段、`/etc` 下的全局可写文件、默认
umask、IP 转发、持久化 journald、以及是否存在任何自动打补丁机制。

诚实边界：这是一个**带 CIS 味道的样本，不是 CIS 扫描器**——它告诉你基础项是否守住，
不判断你是否合规。而且它只**审计**：修复属于配置管理（工具箱的 Ansible 波次），
不属于一个做一次性改动的脚本。

## 用法

```bash
./baseline-check.sh          # 非特权：部分项 SKIP 或改读配置文件
sudo ./baseline-check.sh     # 完整：sshd -T 生效值 + shadow 检查
```

## 退出码

| 码 | 含义 |
| --- | --- |
| 0 | 无 FAIL（INFO/SKIP 仍值得一读）|
| 1 | 一个或多个 FAIL |
| 2 | 非 Linux |

## 验证环境

Ubuntu 24.04 容器（非特权 + root；通过与故意破坏的配置）。lab 验证过，非生产级加固。
