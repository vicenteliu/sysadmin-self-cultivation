# Ansible 线 — 修复的另一半

> [脚本](../)负责*发现*问题（只读，随处安全运行）。这些 Ansible role 负责*修复*
> ——幂等、声明式、一套控制面。二者闭环：`baseline-check` 报告、`baseline_hardening`
> 修复；`patch-report` 清点、`patch` 应用；`user-lifecycle` 规划、`user_lifecycle` 收敛。

## Role

| Role | 修什么 | 配对脚本 |
| --- | --- | --- |
| [`baseline_hardening`](roles/baseline_hardening/) | SSH 姿态、umask、sysctl、持久化 journald（逐项开关）| [`baseline-check`](../../baseline-check/) |
| [`patch`](roles/patch/) | 应用待更新（apt/dnf）+ reboot 编排 | [`patch-report`](../../patch-report/) |
| [`user_lifecycle`](roles/user_lifecycle/) | 声明式用户：present / disabled（锁定，默认不删）| [`user-lifecycle`](../../user-lifecycle/) |

## 约定（工具箱章程六条，应用到 Ansible）

1. **幂等。** 第二次运行报 `changed=0`。验证过，不是假设。
2. **默认安全。** 全部支持 `--check`（dry-run）。真正危险的开关（防火墙启用、
   自动重启、删用户）默认**关闭**，并在各 role README 里点明。
3. **诚实边界。** 每个 role 的 README 带 `Tested on:` 一行。容器 lab 验证不等于生产加固，直说。
4. **朴素依赖。** 面向完整 `ansible` 包（自带 `ansible.posix`），不只是 `ansible-core`。不引额外 Galaxy role。
5. **可读变量。** 每个行为都是 `defaults/` 里有文档的变量——tasks 里不藏东西。
6. **安静收敛，响亮失败。** 标准 Ansible 报告；handler 只重载真正改动的东西。

## 运行

```bash
# 先 check 模式——看会改什么，不碰任何东西
ansible-playbook -i inventory.ini playbooks/harden.yml --check --diff

# 然后真跑
ansible-playbook -i inventory.ini playbooks/harden.yml
ansible-playbook -i inventory.ini playbooks/patch.yml
ansible-playbook -i inventory.ini playbooks/users.yml
```

对控制节点自身做本地冒烟测试：

```bash
ansible-playbook -i 'localhost,' -c local playbooks/harden.yml --check --diff
```

inventory 形状见 [`inventory.example.ini`](../../../../toolbox/ansible/inventory.example.ini)。

## 这不是什么

不是完整的 CIS 修复，不是加固基础镜像或你现有配置管理的替代品。一组聚焦、诚实、
闭环的集合——如果某个 role 没在真实环境收敛过，它的 README 会告诉你它*在哪里*收敛过。
