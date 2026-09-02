---
kind: lab
axis: platforms
themes: [identity, cloud, containers]
platforms: [gcp]
derived: true
mirrors: platforms/gcp/labs/gke-iam-vs-rbac/README.md
summary: "不用集群、不用凭据、不花钱、不装外部包 —— 只要 Python 3.8+。"
---
# Lab —— GKE 有两个鉴权平面（亲手把它证明出来）

> 🌐 **语言：** [English（默认）](../../../../../../platforms/gcp/labs/gke-iam-vs-rbac/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`platforms/gcp/labs/gke-iam-vs-rbac/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

**目标：** 把 [GCP support 笔记](../../support.md)里那条头号 GKE 教训变得摸得着 ——
**GKE 用 Cloud IAM 给你「认证」，用 Kubernetes RBAC 给你「授权」；它们是两个独立的平面，所以
`Unauthorized`（认证）和 `Forbidden`（授权）是两种不同的失败，解法也不同 —— 而且身为 IAM 的
"Cluster Admin" 并「不会」让 `kubectl get secrets` 跑得通。** 你会跑一个忠实的 GKE 授权流水线模型，
看着请求因为多数 GKE 访问工单背后的那些确切原因而失败。

**你会练到：** 把一次 GKE 访问失败读成*"是哪个平面说了不？"* —— 没有 `container.clusters.get`
（连认证都过不去）对上 已认证但没有 RBAC（Forbidden）—— 以及那篇笔记坚持的那个反射：
**用一次 RBAC 绑定去修集群内的访问，而不是去抬高 IAM。**

## 这个 lab 为什么是纯本地的

不用集群、不用凭据、不花钱、不装外部包 —— 只要 Python 3.8+。IAM 角色和 RBAC 角色是几个小字典；
那个求值器是 GKE 真实顺序的一份忠实实现：

1. **认证（Cloud IAM）：** 调用者需要 `container.clusters.get` 才能够得到那个 API server。
   没有 IAM 的集群角色 → **`Unauthorized`**。
2. **授权（先 RBAC，后回落到 IAM）：** GKE 先查有没有一条 RBAC 绑定；如果没有，它回落到调用者在
   集群内的 IAM 权限。两个都没授予这个动词 → **`Forbidden`**。

（那些权限字符串是示意性的；那个*行为* —— 认证与授权分离、先 RBAC 后回落 IAM、`clusterAdmin` ≠
集群内 —— 是真实的。）

## 跑它

```bash
python3 gke_authz_drill.py
```

就这样 —— 不用装任何东西。exit code `0` 表示每一条断言都成立，所以它兼作一个 CI 检查。

## 你会看到什么

七个被叙述出来的步骤，每一个都以一条被检查过的教训收尾：

```
=== 2. Authenticated ≠ authorized: reaching the cluster grants nothing inside ===
  kubectl get pods  as viewer (clusterViewer, no RBAC) → Forbidden
  ✓ viewer authenticates but is Forbidden — the two planes are separate (LESSON 2)
=== 3. The trap: IAM 'Cluster Admin' is NOT the RBAC cluster-admin ===
  kubectl get secrets  as infra-admin (clusterAdmin IAM) → Forbidden
  ✓ container.clusterAdmin changes cluster INFRA but grants nothing inside (LESSON 3)
=== 4. The fix is an RBAC binding — not escalating IAM ===
  support-eng (clusterViewer + RBAC 'view'):  get pods → OK,  delete pods → Forbidden
```

## 验证（别光信这个脚本说的）

在一个 Python shell 里自己去驱动这个模型：

```python
from gke_authz_drill import Principal, kubectl
infra = Principal("infra-admin", ["roles/container.clusterAdmin"])
print(kubectl(infra, "get", "secrets"))   # ('Forbidden', ...) —— IAM admin ≠ 集群内
infra.rbac_roles = ["view"]                # 加一条 RBAC 绑定
print(kubectl(infra, "get", "pods"))       # ('OK', 'authorized via RBAC')
```

然后刻意把它弄坏 —— 让 `authorize()` 跳过那条"先 RBAC"的规则 —— 再跑一次：这个演练必须**非零**
退出。一个不会失败的自我验证器毫无价值。

## 重点

- **两个平面，两个问题。** *你够得到这个集群吗？*（Cloud IAM 认证）和*你能在它里面做这个动作吗？*
  （Kubernetes RBAC 授权）是分开的。同一个 Google 身份可以过掉一个、却挂在另一个上。
- **`Unauthorized` ≠ `Forbidden`。** Unauthorized 是一个认证问题（凭据错了/过期了、缺
  `gke-gcloud-auth-plugin`、没有 `container.clusters.get`）；Forbidden 是一个授权问题（没有 RBAC
  绑定）。把其中一个当成另一个来修，是那个经典的时间黑洞。
- **IAM 的 "Cluster Admin" 不是 RBAC 的 `cluster-admin`。** 那个 IAM 角色改的是集群*基础设施*；
  它在*里面*什么都不授予。"我是 Owner，kubectl 怎么 Forbidden？"说的就是这个，一字不差。
- **用 RBAC 去修集群内的访问，而且要带范围。** 一条 `view` 绑定授予 `get pods` 而*不*授予
  `delete pods` —— 这就是 RBAC 胜过一个宽泛 IAM 角色的意义。你刚刚看着那个带范围的解法生效，
  也看着那条过宽的 IAM 路径"能用但过度授权"。

## 拆除

没有创建任何持久化的东西 —— 这个演练不写任何文件。没有要清理的。
