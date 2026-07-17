# role: baseline_hardening

修复 [`baseline-check`](../../../../../toolbox/baseline-check/) 审计的项——SSH 姿态、
默认 umask、sysctl 基线、持久化 journald。每项都是开关；任何可能把你锁在外面的项默认**关闭**。

## 变量（见 [`defaults/main.yml`](../../../../../toolbox/ansible/roles/baseline_hardening/defaults/main.yml)）

| 变量 | 默认 | 说明 |
| --- | --- | --- |
| `harden_ssh` | `true` | 管理 sshd 姿态 |
| `harden_ssh_permit_root` | `prohibit-password` | `no` 或 `prohibit-password` |
| `harden_ssh_password_auth` | `false` | **⚠️ 只在 key 认证已可用时设** — `false` 写入 `PasswordAuthentication no` |
| `harden_umask` | `true` / `027` | `/etc/login.defs` 默认 umask |
| `harden_sysctl` | `true` | 写 `/etc/sysctl.d/99-baseline-hardening.conf` |
| `harden_journald_persistent` | `true` | 建 `/var/log/journal`（下次 journald 重启/reboot 生效——role 不会 bounce journald 打断日志）|
| `harden_firewall` | **`false`** | ufw 启用——默认关；开启时先放行 OpenSSH |

每处 SSH 改动在写入前用 `sshd -t` 校验，坏配置绝不会重载。

## 安全

- **先跑 `--check --diff`。** 每个 task 支持 check 模式。
- `PasswordAuthentication no` 会把没有可用 SSH key 的人锁在外面——所以它默认*保留密码认证*直到你显式开启。
- 防火墙启用是 opt-in，切默认策略为 deny 前先放行 OpenSSH。

## 用法

```bash
ansible-playbook -i inventory.ini ../playbooks/harden.yml --check --diff
ansible-playbook -i inventory.ini ../playbooks/harden.yml
```

## 验证环境

Ubuntu 24.04 容器：配置写入正确（`PermitRootLogin prohibit-password`、
`PasswordAuthentication no`、sysctl drop-in），**幂等重跑 `changed=0`、`failed=0`**，
`--check` 模式干净。每处 SSH 编辑在排队 reload 前用 `sshd -t` 校验。

`reload sshd` handler 发起服务 reload，需要运行中的 init 系统——在真实 systemd 主机
上执行，但无法在裸容器里跑（Ansible-in-container 的常见限制），所以 reload 本身在真实
机器上验证，不在上面的容器运行里。防火墙 opt-in 路径用 `community.general.ufw`（随
`ansible` 包）。lab 验证过，非生产级加固。
