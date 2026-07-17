# role: patch

在 apt 或 dnf 系统上应用待更新，然后报告——或者按你要求，处理需要的重启。
[`patch-report`](../../../../../toolbox/patch-report/) 的执行侧。

## 变量（见 [`defaults/main.yml`](../../../../../toolbox/ansible/roles/patch/defaults/main.yml)）

| 变量 | 默认 | 说明 |
| --- | --- | --- |
| `patch_upgrade_type` | `safe` | `safe` = 普通升级；`full` = Debian 上 `dist-upgrade` |
| `patch_autoremove` | `true` | 清理不再需要的包 |
| `patch_update_cache` | `true` | 先刷 apt cache |
| `patch_reboot_if_required` | **`false`** | 仅检测+报告；`true` = 升级需要时重启 |
| `patch_reboot_timeout` | `600` | 等主机回来的秒数 |

## 安全

- **重启默认关闭。** 默认下 role 告诉你需要重启然后停下——你决定何时。
  设 `patch_reboot_if_required: true`（如维护窗口的 play）让它重启。
- 全机群 play 前先对一台 canary 跑；playbook 里 `serial:` 分批推。

## 用法

```bash
ansible-playbook -i inventory.ini ../playbooks/patch.yml            # 打补丁，报告重启
ansible-playbook -i inventory.ini ../playbooks/patch.yml \
    -e patch_reboot_if_required=true                                # 打补丁 + 重启
```

## 验证环境

Ubuntu 24.04 容器（apt 升级带待更新；reboot-required 检测与报告；幂等重跑
`changed=0`）。dnf task 路径结构上镜像；重启检测用 `needs-restarting -r`。
lab 验证过，非生产级加固。
