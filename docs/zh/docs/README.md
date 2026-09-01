---
kind: index
axis: meta
themes: []
platforms: []
derived: true
mirrors: docs/README.md
summary: "本项目的默认语言是英文；正本文档住在仓库根目录，以及 platforms/、cross-cutting/ 和 ai-workflow/ 下面。"
---
# docs/ —— 文档与翻译

> 🌐 **语言：** [English（默认）](../../README.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`docs/README.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

本项目的**默认语言是英文**；正本文档住在仓库根目录，以及 `platforms/`、
`cross-cutting/` 和 `ai-workflow/` 下面。

它同时持有这个仓库自己的元数据：[决策记录](../../adr/)、
[开放问题](../../questions.md) —— 有人问过这个仓库、而它还答不上的问题，包括那些被刻意划在
范围之外的、以及为什么 —— 还有**检索索引** —— [`index.json`](../../index.json)，由
[`build-index.py`](../../build-index.py) 从每个文件的 front-matter 生成，好让一个 agent 不用
遍历仓库就能搜索它。这个索引是生成的，绝不手改：改文件，然后跑脚本。`--check` 在它过期时
以非零码退出。

同一条"生成而非手改"的契约，覆盖 [`site/`](../site/README.md) 那个浏览器读取的两个文件
—— 它的标题映射和它的**搜索语料** —— 以及从四个门面图源派生出来的十二个产物。每个 builder
都接受 `--check`。

这个目录持有**翻译**（多语言支持）。每种语言得到一个子目录，随着翻译被贡献进来而镜像英文
的目录树。

```
docs/
└── zh/                 # 中文
    └── README.md       # 翻译过的总览；更多文档会陆续加入
```

**翻译可能滞后于英文源。** 两者不一致时，以英文根目录文档为准。要贡献一份翻译，把英文文件
的路径镜像到语言目录下（例如 `platforms/aws/README.md` → `docs/zh/platforms/aws/README.md`）。
