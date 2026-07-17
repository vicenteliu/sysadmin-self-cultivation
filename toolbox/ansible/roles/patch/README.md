# role: patch

Applies pending updates on apt or dnf systems, then reports — or, if you ask —
acts on a required reboot. The execution half of
[`patch-report`](../../patch-report/).

## Variables (see [`defaults/main.yml`](defaults/main.yml))

| Variable | Default | Notes |
| --- | --- | --- |
| `patch_upgrade_type` | `safe` | `safe` = normal upgrade; `full` = `dist-upgrade` on Debian |
| `patch_autoremove` | `true` | drop packages no longer needed |
| `patch_update_cache` | `true` | refresh apt cache first |
| `patch_reboot_if_required` | **`false`** | detect + report only; `true` = reboot when the upgrade needs it |
| `patch_reboot_timeout` | `600` | seconds to wait for the host to come back |

## Safety

- **Reboot defaults to off.** By default the role tells you a reboot is required
  and stops — you decide when. Set `patch_reboot_if_required: true` (e.g. for a
  maintenance-window play) to let it reboot.
- Run against a canary/one host before a fleet-wide play; `serial:` in the
  playbook to roll it out in batches.

## Usage

```bash
ansible-playbook -i inventory.ini ../playbooks/patch.yml            # patch, report reboot
ansible-playbook -i inventory.ini ../playbooks/patch.yml \
    -e patch_reboot_if_required=true                                # patch + reboot
```

## Tested on

Ubuntu 24.04 container (apt upgrade with pending updates; reboot-required
detection and reporting). dnf task path is structurally mirrored; the reboot
detection uses `needs-restarting -r`. Lab-verified, not production-hardened.
