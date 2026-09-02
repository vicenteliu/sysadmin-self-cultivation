---
kind: lab
axis: the-stack
themes: []
platforms: [aws]
derived: true
mirrors: the-stack/labs/README.md
summary: "分层系列的可跑证据。每一章的「Lab」一节是一份规格；这个目录就是那些规格变成你真的跑得起来、验得了的代码的地方。"
---
# The Stack —— Lab

> 🌐 **语言：** [English（默认）](../../../../the-stack/labs/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`the-stack/labs/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

分层系列的可跑证据。每一章的"Lab"一节是一份规格；这个目录就是那些规格变成你真的跑得起来、验得了
的代码的地方。

> **设计偏好：** 只要概念允许，这些 lab 优先做成**纯本地、零成本、零凭据**的练习 —— 这样谁都跑得
> 起来，CI 也跑得起来。凡是一个 lab 真的需要一朵云或者一个 hypervisor，它会说出来，而且保持可拆
> （那些放在平台目录里的 lab，比如
> [`platforms/aws/labs/`](../../platforms/aws/labs/)，遵循沙箱账号 + 硬性预算告警那套地面规则）。

## 已建成

| Lab | 章节 | 它证明什么 | 需要什么 |
| --- | --- | --- | --- |
| [`01-failure-domains/`](01-failure-domains/) | [01 物理](../01-physical.md) | 同处一地的副本共享同一个命运；跨故障域的反亲和，才是"高可用"的意思 | 只要 Python 3.8+ |
| [`04-backup-not-snapshot/`](04-backup-not-snapshot/) | [04 存储](../04-storage.md) | 复制会忠实地把破坏也复制过去；只有一份独立的备份才救得了你，而且以它的 RPO 为限 | 只要 Python 3.8+ |

The Stack 之外也有可跑的 lab，一样是纯本地的精神：
[`foundations/labs/idempotence-drill/`](../../foundations/labs/idempotence-drill/)
（脆弱的脚本对上 `set -euo pipefail` 安全的脚本，bash）、
[`cross-cutting/labs/ci-cd-pipeline/`](../../cross-cutting/labs/ci-cd-pipeline/)（一条真实的
GitHub Actions 流水线 + 一个带测试的应用）、
[`cross-cutting/labs/m365-conditional-access-lockout/`](../../cross-cutting/labs/m365-conditional-access-lockout/)
（一条把管理员自己锁在外面的 Conditional Access 策略 —— 那个租户级的爆炸半径，被感觉到）、
[`platforms/aws/labs/iam-deny-by-default/`](../../platforms/aws/labs/iam-deny-by-default/)
（AWS IAM 策略求值 —— 默认拒绝，以及为什么 `Allow *` 不是那个解法）、
[`platforms/gcp/labs/gke-iam-vs-rbac/`](../../platforms/gcp/labs/gke-iam-vs-rbac/)
（GKE 的两个鉴权平面 —— 为什么会"我是 Owner，可 kubectl 说 Forbidden"）、
[`platforms/azure/labs/global-admin-is-not-owner/`](../../platforms/azure/labs/global-admin-is-not-owner/)
（Azure 的两个身份平面 —— 为什么一个 Global Admin 不是一个 Owner）、
[`platforms/oci/labs/a-compartment-is-not-an-account/`](../../platforms/oci/labs/a-compartment-is-not-an-account/)
（OCI 的动词层级 + compartment 范围 —— 为什么 `NotAuthorizedOrNotFound` 是一个 404，以及一个
compartment 不是一个账号）、
[`cross-cutting/labs/terraform-state-and-drift/`](../../cross-cutting/labs/terraform-state-and-drift/)
（Terraform 那个 配置/状态/现实 三角 —— 为什么一次手改会被改回去、一个不可变属性会逼出一次销毁，
而 `count` 会翻搅、`for_each` 却保持稳定）、
[`cross-cutting/labs/k8s-reconcile-loop/`](../../cross-cutting/labs/k8s-reconcile-loop/)
（Kubernetes 那个调和循环 —— 为什么一个被删掉的 pod 会回来、一次 exec 修复会消失，而一个
Running 但没 Ready 的 pod 会被从 Service endpoints 里摘掉）、
[`cross-cutting/labs/multi-cloud-cidr-overlap/`](../../cross-cutting/labs/multi-cloud-cidr-overlap/)
（多云网络 —— 为什么重叠的 CIDR 没法互联，以及跨云并不存在一个中央路由器）。

## 已规划（规格住在各章里）

| Lab | 章节 | 草图 |
| --- | --- | --- |
| `02-network-debug-ladder/` | [02 网络](../02-network.md) | 同一套三层网络建两遍（Terraform，在两朵云上）；用四种方式把它弄坏，再用那架调试阶梯修好 |
| `03-one-image-two-clouds/` | [03 计算](../03-compute-and-images.md) | Packer 黄金镜像 + cloud-init，投到 KVM 和一朵云上；把那个镜像破坏掉，再从串口控制台恢复 |
| `06-see-the-request/` | [06 可观测性](../06-observability.md) | Prometheus + Grafana + 一条 OTel trace；定义一个 SLO，然后故意把错误预算烧光 |
| `07-break-the-default/` | [07 安全](../07-security.md) | 把一个 bucket 配错成公开的，用一次姿态扫描抓住它，然后用 policy-as-code 让这件事变得不可能 |

lab 会随着各章稳定下来而增加。纯本地的那些先来 —— 证据应该便宜到容易复现。
