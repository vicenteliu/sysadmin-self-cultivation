---
kind: guided-run
axis: platforms
themes: [virtualization]
platforms: [self-host]
marker: "🔨"
derived: true
mirrors: platforms/self-host/labs/README.md
summary: "在一台开了嵌套虚拟化的笔记本上做的三次 guided run —— 那些云需要一个账号，而这个平台需要的是那台笔记本；不需要数据中心就能练裸金属纪律的诚实方式。"
---
# 自托管 / 裸金属 —— Guided run

> 🌐 **语言：** [English（默认）](../../../../../platforms/self-host/labs/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/self-host/labs/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

在一台开了嵌套虚拟化的笔记本上做的三次 guided run。那些云需要一个账号，而这个平台需要的是
那台笔记本 —— 不需要数据中心就能练裸金属纪律的诚实方式。

**这些是 [guided run](../../../CONTEXT.md)，不是 lab。** 每一次都需要一个真实环境，所以这里没有
任何东西能断言你做过它，而 CI 也跑不了它。那就是全部的区分，而且它不是降级 —— 一次 guided run
够得到真实的延迟、真实的报错和真实的账单，而那是没有模型做得到的。

> **地面规则：** 把这些跑在一台**用完即弃的 VM / 嵌套 hypervisor** 里（Proxmox、libvirt/KVM，
> 或者 Workstation/Fusion）。这里没有一样需要真实硬件 —— 重点是那条*流水线和那些反射*，而它们在
> 任何规模上都一模一样。

## 为什么是命令行

自托管是这样一个平台：它大部分东西*根本没有* GUI —— 而命令行那些优点在这里最锋利。`virsh`、
`ipmitool`、`ansible` 和纯 shell **更快**（对一台无头机器，你连一个控制台都够不到）、**更精确**、
**可复现**（那条流水线在第 1 台和第 10000 台机器上跑得一模一样）、**可评审**。更要紧的是：裸金属
**没有撤销** —— 一条你读得了、能纳入版本管理、能评审的命令，是唯一安全地碰它的方式
（[`foundations/`](../../../foundations/)）。

## 那条三节 guided run 弧

### Run 01 —— 盘点那片机队（从代码，不是从一张表格）

在你自己拥有的硬件上做那一招"把所有东西列出来" —— 用 Ansible 对着一份清册做临时操作，再加上经
IPMI 的带外可达：

```bash
# 跨机队采集清册 fact —— 一条命令，每一台主机
ansible all -i inventory.ini -m setup -a 'filter=ansible_hostname,ansible_distribution,ansible_memtotal_mb'

# 快速扫一遍健康度：uptime + 剩余磁盘 + 负载，全都要
ansible all -i inventory.ini -a 'df -h / '
ansible all -i inventory.ini -a 'uptime'

# 经 BMC 够到一台「没有操作系统」的机器 —— 云上那个「串口控制台」不过是把它租给你
ipmitool -I lanplus -H 10.0.0.50 -U admin -P "$BMC_PW" chassis power status
ipmitool -I lanplus -H 10.0.0.50 -U admin -P "$BMC_PW" sdr type temperature   # 传感器
```

**验证：** 你在没有手动登录任何一台机器的情况下盘点了整片机队，并且经 IPMI 够到了一台已经断电的
机器 —— 带外管理，跑起来了。

### Run 02 —— 不用手地发放一个节点（那条流水线）

自托管那项标志性技能：不用手地把一台空白机器网络启动成一台能干活的机器
（[`the-stack/03`](../../../the-stack/03-compute-and-images.md)）。在一个嵌套 lab 里，
`virt-install` 替代 PXE + 镜像 + cloud-init：

```bash
# 造一份 cloud-init seed（流水线在首次启动时注入的那份个性化）
cat > user-data <<'EOF'
#cloud-config
hostname: lab-node01
users: [{name: ops, sudo: 'ALL=(ALL) NOPASSWD:ALL', ssh_authorized_keys: [ssh-ed25519 AAAA...]}]
package_update: true
packages: [qemu-guest-agent]
EOF
cloud-localds seed.img user-data                 # 把它打包成一块 seed 盘

# 从一个云镜像 + 那份 seed 做「等价于 PXE 的」不用手安装
virt-install --name lab-node01 --memory 2048 --vcpus 2 \
  --disk /var/lib/libvirt/images/lab-node01.qcow2,size=10 \
  --disk seed.img,device=cdrom \
  --import --os-variant ubuntu22.04 --noautoconsole

virsh list --all                                 # 这个节点起来了，而你没在任何控制台上敲过字
```

**验证：** 那个节点启动起来就已经个性化好了（主机名、用户、软件包）—— 没有点过任何安装器。重跑一遍
来证明它是**可复现且幂等**的。

### Run 03 —— 故障域 + RAID 那句真话（那些演练）

这个仓库里最有质感的两课，落在它们来自的那个平台上：

```bash
# 故障域：定义两个「机柜」（主机组），把一个 2 副本的服务铺在它们之上，
# 然后干掉一个「机柜」，看什么活下来（用嵌套 VM 替代那些主机）：
virsh destroy rack-a-node1     # 模拟一次机柜/主机故障（硬断电）
# ……rack-b 上那个副本继续服务。那就是一个故障域，握在你自己手里。

# RAID 不是备份：建一个软 RAID1，然后证明它熬得过一次「硬盘死亡」，
# 但熬不过一次「逻辑删除」：
mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/vdb /dev/vdc
mkfs.ext4 /dev/md0 && mount /dev/md0 /mnt && echo "data" > /mnt/canary
mdadm /dev/md0 --fail /dev/vdb --remove /dev/vdb   # 干掉一块盘 —— 数据「活着」（这是 RAID 的活）
cat /mnt/canary                                    # 还在
rm /mnt/canary                                     # 一次逻辑删除 —— RAID 把它「复制」没了
# 那只金丝雀在两块盘上都「没了」。RAID ≠ 备份 —— 得从那份独立副本里恢复。
```

**验证：** 那个服务熬过了一次"机柜"丢失；那个 RAID 阵列熬过了一次硬盘死亡，却没熬过一次 `rm` ——
恰好就是 [`the-stack/04`](../../../the-stack/04-storage.md) 划出的那个区别，在你手里被感觉到。把它
和那个可跑的[备份演练](../../../the-stack/labs/04-backup-not-snapshot/)配着做。

---

一句诚实的说明：这是那个 🔨 平台 —— 最深的那条根。这些 lab 就是那份机队工作被写下来，而且它们是这
个仓库里最容易复现的，因为它们除了一台笔记本什么都不需要。
