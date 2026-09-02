---
kind: guided-run
axis: platforms
themes: [cloud]
platforms: [openstack]
marker: "🧭"
derived: true
mirrors: platforms/openstack/labs/README.md
summary: "对着 DevStack 做的三次 guided run —— 一台 VM 里的单节点一体化 OpenStack，是不需要数据中心就能认识这个平台那套管路的诚实方式。"
---
# OpenStack —— Guided run

> 🌐 **语言：** [English（默认）](../../../../../platforms/openstack/labs/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/openstack/labs/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

对着 **DevStack** 做的三次 guided run —— 一台 VM 里的单节点一体化 OpenStack，是不需要数据中心
就能认识这个平台那套管路的诚实方式。

**这些是 [guided run](../../../CONTEXT.md)，不是 lab。** 每一次都需要一个真实环境，所以这里没有
任何东西能断言你做过它，而 CI 也跑不了它。那就是全部的区分，而且它不是降级 —— 一次 guided run
够得到真实的延迟、真实的报错和真实的账单，而那是没有模型做得到的。

> **地面规则：** 把 **DevStack** 跑在一台用完即弃的 VM 里（它不是给生产用的，而且能干净地重新
> stack）。先 `source` 你的凭据文件（`source openrc admin admin`）。做完就把资源删掉。

## 为什么是命令行

OpenStack 有 Horizon（一个网页面板）—— 而运维者住在 **`openstack` CLI** 里，因为它**更快**、
**更精确**、**可复现**（同样的命令跨每一个部署都成立）、**可评审**，而且就是 Heat/Terraform 驱动
的那片界面。Horizon 是用来看的；那个统一的 `openstack` 客户端是用来运维的。一个二进制，每一个服务。

## 那条三节 guided run 弧

### Run 01 —— 身份 + 盘点（Keystone，那道正门）

一切都通过 **Keystone** 认证；从命令行盘点一个 project：

```bash
source openrc admin admin                            # 把凭据加载进环境变量
openstack token issue                                # 确认认证是通的

# 创建一个 project（租户）和一个受限用户
openstack project create lab
openstack user create --project lab --password-prompt labuser
openstack role add --project lab --user labuser member

# 盘点 —— 每一个服务上都是同一个 'list' 动词
openstack server list --all-projects -c Name -c Status -c Networks
openstack network list -c Name -c Subnets
openstack volume list -c Name -c Status -c Size
```

**验证：** 换成 `labuser`（一个受限的非 admin 身份）重新 source，然后看着 `--all-projects` 不再起作用
—— Keystone 的范围限定被变得可见了。

### Run 02 —— 网络 + 实例（跑在 KVM 上的 Nova，以及 Neutron）

一个租户网络、一台通往外部网络的路由器，和一个实例 —— 也就是你可能已经懂的 KVM，被裹在那个云控制
平面里：

```bash
# 一个租户网络 + 子网，以及一台通往 provider network 的路由器
openstack network create lab-net
openstack subnet create --network lab-net --subnet-range 10.0.1.0/24 lab-subnet
openstack router create lab-router
openstack router set --external-gateway public lab-router
openstack router add subnet lab-router lab-subnet

# 一个放行 SSH 的 security group，然后用一个 flavor 拉起一个实例
openstack security group rule create --proto tcp --dst-port 22 default
openstack server create --flavor m1.small --image ubuntu-22.04 \
  --network lab-net --security-group default --key-name mykey lab-vm

# 一个够到它的 floating IP
openstack floating ip create public
openstack server add floating ip lab-vm <FLOATING_IP>
```

**验证：** `openstack server show lab-vm -c status -c addresses` 显示 ACTIVE 并带着那个
floating IP；你 SSH 得进去。**拆除：** 删掉那台 server、那个 floating IP、那些路由器接口、
那个子网、那个网络。

### Run 03 —— 控制平面故障演练（真正的那个教训）

那个"云是你造的"所独有的教训 —— API 可以死掉，而你的 VM 继续跑
（[`the-stack/01`](../../../the-stack/01-physical.md)）：

```bash
# 注意：你的实例是 ACTIVE 而且够得到的
openstack server list

# 现在把控制平面「弄卡住」—— 停掉一个核心服务（在 DevStack 上是一个 systemd unit）
sudo systemctl stop devstack@n-api            # Nova API 挂掉

# 现在 API 失败了……
openstack server list                          # ERROR —— 控制平面挂了

# ……但那个在跑的实例毫发无损 —— ping 它、SSH 它：还在。
ping <FLOATING_IP>                             # 照样应答

# 恢复：
sudo systemctl start devstack@n-api
openstack server list                          # 又能用了
```

**验证：** 那台在跑的 VM 毫发无损地熬过了那次 API 故障 —— 控制平面即产品的那个现实，你在这里是
*感觉*到的，不是读到的。**拆除：** 重新 stack，或者把这些 lab 资源删掉。

## 弧之外 —— 一个纯本地的演练

上面那条三节弧需要一台 VM 里的 DevStack。还有一个 lab **什么都不需要** —— 一个纯本地、只用标准库、
能自我验证的演练，接着那篇[运维篇](../operations.md)：

### `the-cloud-is-down-the-vms-are-up/` —— 卡住的控制面 ✅ 已建（纯本地）

把上面的第三步做成模型：一条塞满的队列让每一次 API 调用停掉，而九台实例照样应答；只看租户的面板一直
是绿的；卡住期间死掉的一台 compute 主机在队列排空之前无法疏散 —— 控制面故障变成租户故障的那一刻。见
**[`the-cloud-is-down-the-vms-are-up/`](the-cloud-is-down-the-vms-are-up/)**。

```bash
python3 the-cloud-is-down-the-vms-are-up/control_plane_drill.py   # exit 0 = 那些教训成立；在 CI 里跑
```

---

一句诚实的说明：OpenStack 是一条 🧭 ramp —— DevStack 让它成为一条跑得起来的 ramp，而 lab 03 正是
把"控制平面现在归你了"那个警告从理论变成肌肉记忆的那块拼图。
