# role: user_lifecycle

声明式用户：定义期望状态，role 收敛到它。[`user-lifecycle`](../../../../../toolbox/user-lifecycle/)
脚本的 Ansible 对应物，同样的法则——**停用 ≠ 删除**。

## `users` 变量

一个列表；每项：

```yaml
users:
  - name: alice
    state: present            # 省略时的默认
    groups: [sudo, docker]
    ssh_key: "ssh-ed25519 AAAA… alice@laptop"
  - name: carol
    state: present
  - name: bob
    state: disabled           # 锁定 + 过期，不删除
  - name: dave
    state: absent             # 显式删除（见安全）
```

| `state` | 效果 |
| --- | --- |
| `present`（默认）| 账户存在、在 `groups` 里、部署 `ssh_key`、未锁定 |
| `disabled` | 锁定 + 过期——不可用，但 home 和审计线索保留 |
| `absent` | 账户**删除**（home 保留，除非 `user_remove_home: true`）|

| 变量 | 默认 | 说明 |
| --- | --- | --- |
| `users` | `[]` | 上面的期望状态列表 |
| `user_remove_home` | `false` | `absent` 时同时删 home 目录 |

## 安全

- **`disabled` 是离职者的默认**，不是 `absent`——你几乎从不想在第一天就删掉
  离职者的文件、打断审计线索。
- `absent` 会删除；逐用户 opt-in，删 home 是第二道 opt-in。
- 跑 `--check --diff` 预览收敛。

## 用法

```bash
ansible-playbook -i inventory.ini ../playbooks/users.yml --check --diff
ansible-playbook -i inventory.ini ../playbooks/users.yml
```

把 `users` 列表放在 inventory/group_vars 里，让它在 Git 里可审阅——
joiner/mover/leaver 变成一个 pull request。

## 验证环境

Ubuntu 24.04 容器：`present`（带 groups + SSH key）、**幂等重跑 `changed=0`**、
`disabled`（锁定 + 过期）全部端到端验证。`absent` 路径用 module 的 `state: absent`
（容器运行里未演练——删除是逐用户 opt-in）。用 `ansible.posix.authorized_key`
（随 `ansible` 包）。lab 验证过，非生产级加固。
