# site —— 文档浏览器

> **输入：** 仓库里已有的 Markdown · **输出：** 一个可浏览、可搜索的视图，位于
> `http://127.0.0.1:8000` · **风险：** 只读，只绑定 localhost，且只能访问
> [`docs/index.json`](../../index.json) 已登记的文件 · **root：** 不需要

> 🌐 **语言：** [English（默认）](../../../site/README.md) · 中文

二十万词已经超过了"翻目录"能应付的规模。这是同一批材料，外加导航、全文搜索、语言
切换和图形渲染——**仅此而已**。它显示的每一个字都是 GitHub 同样会渲染的文件；它是一个
**视图**，绝不是事实首次出现的地方（见
[ADR-0005](../docs/adr/0005-the-site-is-a-view-not-a-seventh-axis.md)）。

## 跑起来

两种方式，同一份文件，同一套 URL 契约。

```bash
python3 site/serve.py                              # http://127.0.0.1:8000
python3 site/serve.py --port 9000                  # 8000 被占用时

docker compose -f site/docker-compose.yml up       # http://127.0.0.1:8099
```

**两条路都不需要安装任何东西。** 直启只用 Python 标准库；`marked` 和 `mermaid` 已经
提交在 `site/vendor/` 下，所以它在离线、飞机上、隔离网环境里都能用。这就是仓库里为什么
躺着一个 2.5 MB 的 bundle——理由以及它击败的四个备选方案记在
[ADR-0006](../docs/adr/0006-the-viewer-vendors-its-dependencies.md)。

要把整套东西交给一个没有 clone 的人，烤一个自包含镜像：

```bash
python3 docs/build-index.py && python3 site/build-corpus.py   # 冻结当前内容
docker build -f site/Dockerfile -t sysadmin-docs .            # 构建上下文是仓库根
docker run --rm -p 8099:8080 sysadmin-docs
```

## 它能做什么

| | |
| --- | --- |
| **搜索** | 对每一篇文档做全文搜索，中英文都行。`/` 聚焦搜索框。 |
| **分面** | 侧栏可按 axis、platform、theme、kind 重新分组——用的就是 retrieval index 所依据的那份 front-matter。 |
| **语言** | 🌐 把文档换成它的中文镜像，界面文案跟着一起换。没有镜像的文档会**明说**，而不是静默回落到英文。 |
| **主题** | 跟随系统设置，切换按钮可覆盖。mermaid 会重新渲染，门面图会换成对应的明暗版本；**但楼面只有一套色板**，因为像素画不能靠机械反色得到可信的另一套（[ADR-0013](../docs/adr/0013-godot-is-a-design-tool-and-the-floor-keeps-one-palette.md)）。 |
| **路线** | `build-out/` 的十六步做成一条线性轨道——刻意不做成 axis 卡片。 |
| **楼面** | 一份[走读](../walkthrough/README.md)稿会在可交互的二维办公室上播放：拖动平移、滚轮缩放，或选 **楼面 / 房间 / 机柜** 让镜头对准一个有名字的对象。点一件东西，就能看它为什么在那里。它只渲染 Markdown 已经陈述的数字，自己不计算（[ADR-0011](../docs/adr/0011-the-floor-renders-the-reference-office-and-may-not-compute-it.md)）。 |

### 试一次楼面

```bash
python3 site/serve.py
# 打开 http://127.0.0.1:8000/#/walkthrough/01-the-network.zh.md
```

三个档位按钮不只是放大倍数：

- **楼面**框住整间办公室。
- **房间**框住你正在看的房间。如果先点一台无线接入点，它会框住放着那台设备的房间；当前没有房间时，默认打开大会议室。
- **机柜**框住 IDF，所以近景看到的是从接入端口到上联的路径，不是放大六倍的办公家具。

选择档位或上班日会进入自由浏览。此后调整窗口大小，镜头会重新框住刚才的选择。按 **上一拍**、**下一拍** 或 **播放**，镜头就交还给走读，由当前那一拍重新选档位和对象。

## 哪些文件是生成的

生成物都由源文件派生并提交。每个 builder 都有检查模式；输出落后时以非零码退出，
所以「过期」是被**发现**的，不是被撞见的。

```bash
python3 docs/build-index.py --check     # docs/index.json  ← 每个文件的 front-matter
python3 site/build-corpus.py --check    # titles.json + corpus.json ← 正文
python3 site/build-diagrams.py --check  # 21 个图形产物 ← 7 个 HTML 源，
                                        # 以及色板表 ← style profile
python3 tools/floor/build-tiles.py --check   # 楼面精灵图 ← tiles.tiles
python3 tools/floor/prove-topology.py --check  # plate 仍然可通行吗？
python3 walkthrough/guard-walkthrough.py     # 拍 ↔ plate ↔ 来源，以及发布冻结
```

图形检查比"是否过期"多管一件事。`diagram-design` 从 `~/.diagram-design/profiles/` 解析
style profile，而 clone 并不携带那个目录，所以皮肤本身作为
`assets/diagrams/sysadmin-brass.profile.md` 提交在这里。在一台从没在本仓库出过图的机器上：

```bash
python3 site/build-diagrams.py --install-profile
```

`corpus.json` 是**搜索语料（search corpus）**——1.2 MB 全文，只在有人真正搜索时才拉取。
它**不是** index：[`CONTENTS.md`](../CONTENTS.md) 是给人看的目录，目录下的
`README.md` 是那个文件夹的索引，`docs/index.json` 是 retrieval index。见
[`CONTEXT.md`](../CONTEXT.md)。

## URL 契约

```
/                             浏览器本体
/doc/<仓库相对路径>.md         一篇文档
/doc/docs/index.json          导航所依据的 retrieval index
```

`serve.py` 用一份**白名单**来执行这个契约，白名单直接从 retrieval index 读取：index 里
没有的路径一律 404，因此即使仓库根就在上一级目录，`.git/`、`.serena/` 以及树里所有非
Markdown 文件都不可达。`nginx.conf` 用文件扩展名加拒绝 dotfile 的方式实现同一套契约——
更松一些，因为 nginx 在请求时没有 index 可查——但仍然足以拒绝所有要紧的东西。一个自带
安全基线加固的仓库，不该同时自带一个把自己的 `.git` 挂到 localhost 上的浏览器。

这个契约是**被断言的，不只是被描述的**：

```bash
python3 site/serve-smoke.py     # 七个请求：三个必须答，四个必须拒
```

它不绑任何端口。handler 本质上是一个从字节到字节的函数，所以请求从一个提供
`makefile()` 和 `sendall()` 的缓冲区进去，再从另一个出来——走的正是 socket 会走到的那套
路由、白名单和错误路径。这样它就能在不允许监听的地方跑：受限的 CI runner、沙箱、
没有 loopback 的容器。

## 目录结构

```
site/
├── serve.py            直启路径——标准库、白名单、只绑 localhost
├── serve-smoke.py      断言上面那份 URL 契约——且不绑端口
├── build-corpus.py     titles.json + corpus.json
├── build-diagrams.py   从每个浅色源派生深色 HTML 和两份 SVG
├── index.html  style.css  strings.json
├── js/                 router · nav · search · render · i18n（原生 ES module）
├── assets/diagrams/    7 个手写门面图源 + 21 个派生文件
├── js/floor.js         走读的可交互二维办公室——Canvas2D，无框架
├── assets/floor/       tiles.png + tiles.json，生成物——见 tools/floor/
├── vendor/             marked + mermaid，刻意提交进仓库
├── nginx.conf  docker-compose.yml  Dockerfile
└── titles.json  corpus.json        生成物——不要手改
```

## 往里加东西

加新文档不需要动这里：写好带 front-matter 的 Markdown，跑那两个 builder，刷新即可。
加新图归 [`diagram-module`](../../../.claude/skills/diagram-module/SKILL.md) 管。这个
浏览器唯一持有的部署知识是 [`js/render.js`](../../../site/js/render.js) 顶部的 GitHub
URL，只用于白名单不提供的文件。

**它不是一台服务器。** 它绑定 `127.0.0.1`，没有任何认证，把它暴露到网络上不是被支持的
用法。要发布的话，把静态文件推上去就行——这个浏览器就是纯 HTML/CSS/JS，任何静态托管
都能直接跑，不用改一行。
