---
kind: lab
axis: cross-cutting
themes: [ci-cd]
platforms: []
derived: true
mirrors: cross-cutting/labs/ci-cd-pipeline/README.md
summary: "那个 workflow 刻意住在 .github-workflows-example/ 下面 —— GitHub 只跑 .github/workflows/ 里的 workflow，所以它不会对着这个教学仓库执行。"
---
# Lab —— 一条真实的 CI/CD 流水线（测试 → 只构建一次 → 带闸门的部署）

> 🌐 **语言：** [English（默认）](../../../../../cross-cutting/labs/ci-cd-pipeline/README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`cross-cutting/labs/ci-cd-pipeline/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

**目标：** 用一个小应用上的**一条真实、有效的流水线**，把 [CI/CD 那一章](../../ci-cd.md)变具体 ——
演示那些要紧的规则：每次 push 都跑 CI（快速反馈）、**只构建一次产物然后把它晋级**、上生产之前有一道
**人工闸门**，以及**用 OIDC 而不是一把长寿命密钥**。

**你会练到：** 把一条流水线读成*一套带闸门和日志的自动化*、那条"只构建一次然后晋级"的规则，
以及那个部署 job 为什么不持有任何静态密钥。

## 这里有什么

```
ci-cd-pipeline/
├── app/
│   ├── hostcheck.py          # a tiny, testable unit (hostname validate/normalize)
│   └── test_hostcheck.py     # the tests CI runs on every push (pure stdlib)
└── .github-workflows-example/
    └── ci.yml                # the pipeline — copy to .github/workflows/ to run it
```

那个 workflow **刻意**住在 `.github-workflows-example/` 下面 —— GitHub 只跑
`.github/workflows/` 里的 workflow，所以它*不会*对着这个教学仓库执行。要真的跑它，把 `ci.yml`
拷进一个含有那个 `app/` 目录的仓库的 `.github/workflows/` 里。

## 在本地跑那些测试（也就是 CI 跑的东西，减去 GitHub）

这个应用是纯 Python 标准库的，所以那个测试 job 不需要 `pip install`：

```bash
cd app
python3 -m unittest -v          # 8 个测试，exit 0 = 绿
python3 hostcheck.py "  Web01.PROD  " "bad_host!"   # 看它做归一化 + 拒绝
```

那条 `python3 -m unittest` 恰好就是这条流水线的 **test** job 所跑的命令 ——
也就是"每一次提交都被自动构建和测试"的本地版本。

## 验证（别光信这个脚本说的）

一套绿的测试在你看见它变红之前什么都证明不了。打开 `app/hostcheck.py`，让 `is_valid()` 第一行就
`return True`，再跑一遍：

```bash
cd app
python3 -m unittest            # 那几条拒绝的测试失败 —— exit 1
git checkout hostcheck.py      # 改回去
```

那次红的运行就是流水线的 `test` job 会在 pull request 上显示的东西，也是 `build` 带着
`needs: test` 的全部理由。`check.py` 在这个仓库每次 push 时也跑这套测试，所以守着这个 lab 的测试
就是这个 lab 讲的那些测试。

## 那条流水线，以及它编码进去的那些规则

三个 job，每一个演示一条章节规则：

- **`test`** —— 每次 push 和 PR 都跑 lint（`py_compile`）+ `unittest`。反馈在几分钟内到，而不是
  等到发布。这里一个红掉的测试会把下游的一切拦住。
- **`build`** —— `needs: test`，所以只有在测试是绿的时候才跑，而且它把这个应用**只打包一次**成
  一个产物。下一个 job 晋级的是*同一个产物* —— 绝不是逐阶段各构建一次（正是那条杀掉"在 staging
  能用、到生产就坏"这个 bug 的规则）。
- **`deploy`** —— `needs: build`，跑在一个 `production` **environment** 里（一个受保护的
  environment = 那道**人工审批闸门**），并且申请 `id-token: write`，好让它能签出一个**短寿命的
  OIDC token** —— **仓库里没有任何长寿命的云密钥**。那段被注释掉的
  `configure-aws-credentials` 步骤展示了一次真实的 role-assume 该放在哪儿。

## 重点

- **这条流水线是通往生产的唯一路径** —— 一次绕过它的变更，就是部署层上的漂移。
- **只构建一次，晋级同一个产物** —— `build` 产出它，`deploy` 消费的是一模一样的那一个。
- **OIDC 优于静态密钥** —— 那个部署 job 没有任何密钥可以泄露；它签出一个短寿命 token。CI 系统能
  部署任何东西，这让它们成为高价值目标 —— 所以它们不持有任何常驻凭据。
- **闸门与日志** —— 那个 `production` environment 是那道人工闸门；那次 Actions 运行就是那份审计
  日志（"谁在什么时候部署了什么" = 运行历史）。

## 拆除

本地没有要拆的。如果你把 `ci.yml` 拷进了一个真实仓库的 `.github/workflows/`，就在那边把它删掉，
好让这条流水线停止运行。
