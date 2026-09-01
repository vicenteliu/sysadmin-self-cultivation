---
kind: glossary
axis: start-here
themes: []
platforms: []
derived: true
mirrors: CONTEXT.md
summary: "这个仓库的词表 —— 在这里有特定含义的词，以及它们容易被混淆成的那些词。"
---
# 系统管理员的自我修养 —— 词表

> 🌐 **语言：** [English（默认）](../../CONTEXT.md) · **中文**
>
> ⚠️ 本项目**默认语言为英文**，`CONTEXT.md` 是"事实来源"。本页中文是多语言支持的一部分，可能略滞后于英文版；两者不一致时以英文为准。

---

这个仓库的词表 —— 在这里有特定含义的词，以及它们容易被混淆成的那些词。别的东西不属于
这个文件：状态在 [`ROADMAP.md`](ROADMAP.md)，结构在 [`CONTENTS.md`](CONTENTS.md)，
决策在 [`docs/adr/`](../adr/)。

## 语言

### 三个都叫"skill"的东西

这个词在这里被三重重载，而混用它们已经害我们返工过一轮。它们互不相干。

**Skill map（技能图）**：
一份可勾选的能力清单 —— `- [ ]` 格子，按 **Core / Working / Depth** 分层，勾上一格
意味着你**做得到**这件事并且**讲得清它的故障模式**。存在两种取向：
[`platforms/*/skills-map.md`](../../platforms/aws/skills-map.md)（一个平台横跨所有主题）
与 [`cross-cutting/skills-maps/*.md`](../../cross-cutting/skills-maps/README.md)
（一个主题横跨所有平台）。
_避免_：skill list、能力矩阵、checklist

**Agent Skill**：
[`.claude/skills/`](../../.claude/skills/) 下的一份 `SKILL.md` 工作流，由 AI agent 调用
来**施行**这个仓库的方法。共十个。它是一个自动化单元，绝不是一个知识单元。
_避免_：skill（不加限定）、tool、command

**Demand cluster（需求集群）**：
[`ROADMAP.md`](ROADMAP.md) 里那张就业市场频率表的一行 —— 一组技术在真实岗位描述里出现
得有多频繁。它只决定构建顺序，别的什么都不决定。
_避免_：技能领域、话题、类别

### 诚实标记

**🔨（亲手做过的深度）**：
一个断言：作者真的在生产环境里运维过这件事，带着后果。它经得起一次深挖的追问。
_避免_：专家、精通、扎实、✋ 和 ⚒️（两个都已退役 —— 见
[ADR-0003](../adr/0003-the-honesty-markers-are-a-hammer-and-a-compass.md)，包括第二个
为什么只活了一天）

**🧭（经过验证的 ramp）**：
一个断言：这份材料被测绘过、对着文档核过、常常还在 lab 里验证过，但没有在生产里跑过。
它对这个落差是诚实的，而不是把它藏起来。
_避免_：熟悉、接触过、了解、🧗（已退役 —— 见 ADR-0003）

**Overclaim（过度声称，❌）**：
任何把 🔨 的动词按在 🧭 的经历上。这正是这些标记存在要防的那个故障模式；
[`honesty-audit`](../../.claude/skills/honesty-audit/SKILL.md) 就是用来检出它的。

### 面试材料

**Interview question（面试问题）**：
一个面试官真的会问的问题，配上**它在探什么** —— 被测的是判断力，不是被回忆的事实。
住在 [`cross-cutting/interview/`](../../cross-cutting/interview/README.md)，按与对应
[技能图](../../cross-cutting/skills-maps/README.md)相同的小节分组。技能图的一格说
*你能做什么*；一个面试问题说*他们怎么查*。
_避免_：测验题、闪卡、备考题

**Answer（答案）**：
跟在问题后面的东西，而**它的形状由该小节的 marker 决定** —— 🔨 的小节用一个
[work example](#) 来答，🧭 的小节用诚实 ramp 的说法来答。它是 marker 的证据，绝不是
一段用来背诵的稿子。注意这里有个反转：
[ADR-0002](../adr/0002-the-reference-office-is-parameters-not-a-bill-of-materials.md)
用*成品答案*指"不该写的那个东西"；
[ADR-0004](../adr/0004-interview-answers-are-evidence-for-a-marker.md) 把它反了过来。
_避免_：范文答案、样板答案、稿子、罐头回答

**Work example（工作实例）**：
真的在工作里发生过的事，匿名地讲 —— 规模和形状，绝不涉及地点或当事方，也不留可还原的
时间线。它挂在一个 🔨 小节上，是让那个 marker 变得可核而不只是被断言的东西。**不是 lab**
（那是合成的、可跑的 —— 见下），也**不是参考办公室**（那是这个仓库用来推理的一个虚构）。
_避免_：战斗故事、轶事、案例研究、经历

### 检索

**Retrieval index（检索索引）**：
生成的 `docs/index.json` —— 每个文件一条机器可读记录，由 `docs/build-index.py` 从
front-matter 构建，供 agent 不打开任何文件就能搜索。**"index" 在这里是三样东西，而只有
这一个是检索索引：**[`CONTENTS.md`](CONTENTS.md) 是给人看的目录，某个目录下的
`README.md` 是那个文件夹的本地索引，而这个两者都不是。
_避免_：catalog（那是 `toolbox/generate/catalog.json`，手工维护，与此无关）、manifest、
搜索索引（那是下面的**搜索语料**）

**Search corpus（搜索语料）**：
生成的 `site/corpus.json` —— 每篇文档的全文，摊平供站点搜索框使用，只在有人搜索时才被
取回。由 `site/build-corpus.py` 构建，它同时产出 `site/titles.json`，因为检索索引记录
summary 却从不记录标题。**刻意不叫 index**：那个词已经被占用了三次，而这是第四样东西
—— 是散文本身，不是关于它的记录。
_避免_：搜索索引、全文索引、catalog

**Hero diagram（门面图）**：
`site/assets/diagrams/` 下四张开启一条轴的品牌图之一 —— 轴图、the stack、ramp、路线。
以浅色 HTML 文件手写一次；深色 HTML 和两份 SVG 由 `site/build-diagrams.py`**派生**，
绝不手改。区别于文档内的 **mermaid** 图，后者才是默认：
[ADR-0007](../adr/0007-a-figures-medium-is-decided-by-what-renders-it.md) 决定一张图属于
哪种媒介，而两者都受它们之上那条规则约束 —— 一张图必须承载散文没有承载的东西。
_避免_：插图、图形、品牌图、figure（那指这两种中的任一种）

### 参考办公室

**The reference office（参考办公室）**：
一个虚构的**专名**：写在 [`the-reference-office.md`](../../the-reference-office.md) 里的
那间一百人、单层、混合办公的办公室，它的 scenario choice 是设定的，其余一切都从一条写明
的规则推导而来。当 [`build-out/`](../../build-out/) 的某一步说*一百个人*时，指的就是它；
而它是**参数，绝不是采购清单**
（[ADR-0002](../adr/0002-the-reference-office-is-parameters-not-a-bill-of-materials.md)）。
它**只消费服务、不运营服务** —— 没有产品、没有客户流量、没有它要负责的公开端点
（[ADR-0015](../adr/0015-the-reference-office-consumes-services-and-operates-none.md)）。

**"一间百人办公室"不是这个术语。** 那是个通用说法，好几个 lab 用它指自己的场景、带自己
的数字 —— 97 台设备、七类工单、两套文档 estate —— 没有一个引用这个文件。这是允许的；不
允许的是让两者模糊，因为一个有两间无名百人办公室的仓库，没法告诉你某个数字来自哪一间。
**专名是背后有文件的那一个。** 当某个 lab 的数字和这个文件的推导同时成立时，推导赢，
lab 被修正 —— 因为一个经得起规则的数字是参数，一个经不起的是巧合。

区别于**plate**（它被画成的那副拓扑）和**楼面**（那幅画），两者见下。
_避免_：the office（不加限定、而实指 plate 时）、场景、示例办公室、我们的办公室

### 走读

**Walkthrough（走读）**：
一次穿过 [`the-reference-office.md`](../../the-reference-office.md) 的叙述，写来
**被 TTS 引擎念出口、被听见** —— 绝不是读的。每篇走读一个文件，住在
[`walkthrough/`](../../walkthrough/)，两种语言并排。它是一条**路线**，不是一条轴：它不
教任何这个仓库尚未持有的页面，只决定**顺序和语域**
（[ADR-0009](../adr/0009-the-walkthrough-ships-its-script-not-its-audio.md)）。它的次序
是它自己的 —— 它不是 `build-out/` 的十六步配个声音，编号也不对应。
_避免_：episode（那指下面说的已发布音频）、script、旁白、tour、播客。在这个术语存在之前
有四处用 *walkthrough* 指一段引导式 lab 序列，术语确立后都改了措辞；**这个词被保留了**
—— 一步一步做的那种叫 *guided run*，而 **lab** 是自验证的那种。

**Beat（拍）**：
走读的构成单位：**一段话、一次 TTS 调用、一个音频片段、一个楼面状态。** 由一条带**稳定
id** 的 HTML 注释界定 —— `<!-- beat: coverage-not-capacity -->` —— GitHub、viewer 和语音
引擎都会忽略它，所以可见的文件里只剩会被念出口的那些字。id 绝不是序数，因为插入一段话不
可以悄无声息地把它之后每一个场景提示都挪一位。对齐按拍，绝不按时间戳
（[ADR-0012](../adr/0012-alignment-is-by-beat-not-by-timestamp.md)）。
_避免_：段落、segment、cue、章节、时间戳

**Episode（集）**：
**一份已发布的音频录音**，放在播客平台上，在这个仓库之外。走读是材料；episode 是渠道。
这两个词被分开，是因为
[ADR-0002](../adr/0002-the-reference-office-is-parameters-not-a-bill-of-materials.md)
已经就这个耦合做过裁决 —— *为服务某份录音而存在的内容，应该跟那份录音待在一起* ——
所以那个目录是按路线命名的，不是按 feed。
_避免_：用 "episode" 指那个 Markdown 文件（那是一篇 walkthrough）

_勘误_：有七条决策记录早于这个词条，用 *episode* 指文件 ——
[0002](../adr/0002-the-reference-office-is-parameters-not-a-bill-of-materials.md) 和
[0009](../adr/0009-the-walkthrough-ships-its-script-not-its-audio.md) 到
[0014](../adr/0014-the-plate-stops-at-topology.md)，出现在 `<episode>.floor.json`、
*the first episode*、*two scripts per episode* 和 *what an episode owns* 里。当那几条
记录说 *the published episode* 时，那个词就是这里定义的意思。
**记录不被编辑。** 这是 [ADR-0008](../adr/0008-a-count-is-not-a-bound.md) 立下的先例
—— 它让 ADR-0007 的句子原样留着，把更正写在旁边 —— 也是一篇冻结的走读遵循的同一条规矩：
错误变成勘误，因为静默的修正会让记录对自己说过的话撒谎。

**The plate**：
这层楼**是什么** —— 有哪些空间、每个是什么、挨着谁，以及你怎么从其中任一处走到另一处。
它住在 [`walkthrough/reference-office.plate.json`](../../walkthrough/README.md)，被每一篇
走读共享，而且它**止步于拓扑**：没有走廊宽度、没有疏散距离、没有卫生洁具数量、不声称这
张图能通过任何审查
（[ADR-0014](../adr/0014-the-plate-stops-at-topology.md)）。它的动线是写下来的，而不是从
"家具没占的地方"推断出来的，并且一个 headless Godot 工程证明了它整个都能从电梯厅走到，
且不穿过任何一张桌子。刻意不叫 *the plan* —— 那是**地址规划**，下一条 —— 也不叫
*the office*，那是[参考办公室](../../the-reference-office.md)，是它被建出来所依据的参数。
_避免_：the plan、the office、地图、布局、蓝图

**The floor（楼面）**：
plate **被画出来时的样子** —— viewer 里那个走读在其上播放的可交互二维场景，带平移、
缩放、可点物体和一群人。**plate 是楼面的主语；楼面是 plate 的渲染**，所以挪一堵墙是改
plate，而给它换个颜色不是。它是一个**视图**：它渲染 Markdown 里已经存在的事实，自己不
计算
（[ADR-0011](../adr/0011-the-floor-renders-the-reference-office-and-may-not-compute-it.md)）。
区别于**门面图**，后者是静态的、从一份 HTML 源派生的。刻意叫 *floor* 而不叫 *site*：那
个词已经同时指 [`site/`](site/README.md) 那个 viewer 和
[`site-network-design.md`](../../cross-cutting/site-network-design.md) 里的一个物理场地，
再来第三个意思就多了一个。
_避免_：地图、场景、模拟、site、the office（那是参考办公室）、plate（那是它画的东西）

**Prop（物体）**：
楼面上一个可点击的对象 —— 一个接入点、一台交换机、一个房间、一个 IDF、一个网段。它的 id
和它到 Markdown 锚点的绑定住在该走读的 `*.floor.json` 里，挨着稿子而不是放在 `site/` 下，
因为只有 viewer 持有的事实，会在 viewer 被删掉的那一刻一起消失。一个 prop 的面板显示
**判断与判据**，绝不显示配置：这个仓库不持有任何设备配置，也不会为了填满一个面板而去长
出一份来。
_避免_：object、实体、hotspot、marker

**Cast（人群）**：
楼面上那些人形，他们**就是无线负载，不是装饰** —— 参考办公室的出勤曲线被可视化出来，
按驱动接入点推导的那个设备数。cast 可以从仓库已陈述的数字被**渲染**出来，绝不可以被用来
**计算**仓库没有陈述的数字。
_避免_：角色、精灵图、agent、头像、NPC

### 技能图里的分层

**Core / Working / Depth**：
分层，而**锚点随图的取向而不同**。在一张平台图里，它们锚在平台**内部**（"Core：不会这个
就没法管 AWS"）。在一张主题图里，它们锚在**这项技能能走多远** —— Core 在全部七个平台上
都成立，Working 在多数平台上成立，Depth 是各平台真正分歧的地方。
_避免_：初级/中级/高级、junior/senior

### 在别处会撞车的词

**IdP**：
**Identity Provider（身份提供方）** —— Entra ID、Okta、Keycloak、ADFS。永远是这个意思，
绝不是 Internal Developer Platform；那个概念在这个仓库里不出现。
_避免_：IDP（大写 D）、身份平台

**Anchor（锚定）**：
一个**转轨**的动词，不是深度断言：把一个陌生平台拴到你已经会的东西上。是
[`ai-workflow/`](../../ai-workflow/how-i-use-ai-to-learn-and-operate.md) 编号规则里的
第 2 条。它属于 🧭，这也是 ⚓ 被否决为深度标记的原因。
_避免_：用 "anchor" 表示已确立的专长

**Vendor name（厂商名）**：
文中点名的一个产品或制造商，而**它在做两件事中的哪一件，决定了它该不该在这儿**。作为
**signature（签名）**它是允许的、而且已经在用 —— 说出你在某个环境里**会看见**什么
（`the-stack/02` 的 *LB signature* 那一行列了 HAProxy / keepalived / F5，好让读者认出一
套自建 estate），或者引述市场（`ROADMAP.md` 引了*"firewalls (Palo Alto/Fortinet)"*，因为
岗位描述就是那么写的）。作为**推荐**，在一份注明日期的 `Reference build` 之外是被禁止的，
依据
[ADR-0002](../adr/0002-the-reference-office-is-parameters-not-a-bill-of-materials.md)。
判据：*说出这个名字是在帮人认出自己身在何处，还是在告诉他该买什么？* 前者可迁移，后者会
过期。
_避免_：型号名（那更窄 —— ADR-0002 专门禁止它出现在 Selection rules 里）、品牌、产品

**Protocol name（协议名）**：
和上面**厂商名**同样的两件事，同样的判据。作为 **signature** 是允许的 —— 说出读者
**会看见**并且必须认出的东西：端口上的 802.1X 和 RADIUS、交换机上的 LLDP、路径里的 DHCP
relay。作为**机制**，它在这个仓库里处处都是出海拔的：握手怎么完成、一个帧怎么找到交换机
端口、一次租约怎么续。判据：*说出它的名字是在告诉人他身在何处，还是解释它在告诉人线上正
在发生什么？* 前者是 signature；后者是另一种能力，而这里只有前者。
_避免_：protocol（不加限定、而实指机制时）、标准、RFC

**Fleet（机队）**：
在这个仓库里有歧义，因此**绝不单独承重**。它已经出现在两个意思里：*配置管理之下的服务器
或 VM*（[`iac-and-config.md`](../../cross-cutting/iac-and-config.md)、
[`ci-cd.md`](../../cross-cutting/ci-cd.md)、
[`web-and-tls.md`](../../cross-cutting/web-and-tls.md)、
[`kubernetes.md`](../../cross-cutting/kubernetes.md)）以及*受管的终端人口*
（[`ROADMAP.md`](ROADMAP.md) 里的 "macOS/Windows fleet"、
[`platforms/self-host/`](../../platforms/self-host/) 里的 "PXE and image pipelines at
fleet scale"）。两者都已确立，也都不会被改名。**要么加限定，要么用更具体的词** ——
*endpoints*、*the estate*、*hosts under Ansible* —— 特别地，参考办公室的终端参数标题是
*Endpoints and spares*，不是 *the fleet*，好让第三个意思永远不被造出来。
_避免_：在读者分不清笔记本还是服务器的地方不加限定地用 fleet

**Deployment（部署）**：
**在这个仓库里是两件不相干的活，而且哪一件都不配拿这个光秃秃的词。** 在
[`ci-cd.md`](../../cross-cutting/ci-cd.md) 及其下游，deploy 指**把代码送到某个环境**。
在 [`endpoint/`](../../endpoint/README.md) 和
[`build-out/04`](../../build-out/04-devices-and-images.md) 里，同一个英文词指**把一台机器
交到一个人手上**。两种用法都已确立，也都不会被改名，所以设备那一侧说 **provisioning**
—— 或者专指构建那半时说 **imaging** —— 而代码那一侧保留 *deployment*。一个需要用光秃秃
那个词的句子，是一个出现在错误章节里的句子。
_避免_：用 deployment 指设备；两边都别用 rollout，因为它藏起了指的是哪一个

**File server / suite storage（文件服务器 / 套件存储）**：
对*文件住在哪*的两个答案，而
[`build-out/07`](../../build-out/07-files-and-collaboration.md) 已经把两者之间的迁移叫作
SaaS 化。**file server** 是这间办公室自己运行的存储：一台机器、一个文件系统、目录上的
权限，以及一份现在归你负责的备份。**suite storage** 是生产力租户里的那个云盘，决定谁能读
什么的是分享模型而不是文件系统 —— 这也是为什么
[`permission-sprawl`](../../cross-cutting/labs/permission-sprawl/) 是一个关于链接而不是
关于 ACL 的 lab。这个区分是承重的，因为两者的失败方式不同：文件服务器丢数据，套件存储
丢的是"谁能看见"这件事的账。
_避免_：网络驱动器、共享盘、云盘、网盘 —— 每一个都只命名了两者之一，却听起来像同时命名了
两者

**Inventory / asset register（盘点 / 资产登记册）**：
**inventory 是你发现到的东西。asset register 是你写下来的东西。** 前者来自某个会去看的
东西 —— 一次扫描、一个 agent、一个管理控制台。后者是一条带主人、成本中心和生命周期状态
的记录。它们从来不相等，而**两者之间的差额不是一个要被消灭的错误**：它是这套估算面的实际
状况，而测量它就是
[`asset-reconciliation`](../../cross-cutting/labs/asset-reconciliation/) 的全部内容 ——
那里两个系统都报九十七台设备，而仍有三条记录是错的。一个把差额对平到零的工具，是把发现
藏起来了，不是把它修好了。
_避免_：CMDB（那是登记册的一种实现）、资产清单、实指登记册时说 inventory system

**Altitude（海拔）**：
一件工作坐在机制之上多高的位置。两种用法，相关但不同。
**工具海拔** —— 你从哪一层去驱动一个 API（CLI、SDK、IaC），而伸手去够错的那一层，正是
`automation.md` 系列 companion 反复点名的那个错误。**内容海拔** —— 一份文档刻意在哪里
停住，这是一条编辑规则而不是一句描述：[`the-stack/02`](../../the-stack/02-network.md) 停
在"某个人必须做出并且负责的决策"，刻意排除协议机制，因为*会运维一个网络和会说出线上正在
发生什么，是两种不同的能力。* 一个漂到自己声明的海拔以下的小节是一个缺陷，哪怕它里面每
一句话都是真的。
_避免_：level、depth（那是 🔨 的断言）、layer（那是 `the-stack/`）

**Gap（缺口）**：
[`build-out/GAPS.md`](../../build-out/GAPS.md) 记录的东西：百人办公室场景里的某一步，
**本应**指向一个可跑 lab 或一个 [`toolbox/`](toolbox/) 工具却指不出来。**只从那个场景
派生。** 仓库里别处缺的材料不是 gap，也不进那个文件。
_避免_：todo、backlog 条目、缺的那块

**Lab**：
一个纯本地、零依赖、自验证的 drill，退出码 `0` 意味着教训成立。多数带一个 `--break-it`
开关，把**标准做法**换进去，然后展示它失败。**机械判据是 CI 跑不跑得动它**，这也是为什么
[`check.py`](../../check.py) 靠 `*_drill.py` 发现 lab，并在每次 push 时把它们全跑一遍。
_避免_：教程、exercise、demo

**Guided run（引导式实操）**：
另外那一种，而它需要一个自己的词，因为这个仓库两种都有。一次**对着真实环境的一步一步的
练习** —— 一个云沙箱、一个本地集群、一个开发者租户 —— 学习发生在做的过程里，而**没有任何
东西能断言你做过**。这个词是在上面 Walkthrough 那一条里为了空出 *walkthrough* 才造的；
在这里定义，是因为有十一个这样的东西正挂在树上、标着*planned lab*，而那承诺了一个永远不
会到来的产物。

**guided run 不是次一等的 lab。** 它够得到模型够不到的东西：真实的延迟、真实的报错、真实
的账单，以及一个控制台的肌肉记忆。它做不到的是在 CI 里失败，而这就是全部的区分。当一份
spec 要求一个沙箱账号、一个 `kind` 集群或者一次 `pip install` 时，它描述的就是这个。
_避免_：lab（那是自验证的那种）、教程、workshop

**Axis（轴）**：
这个仓库覆盖同一批材料的六个面之一 —— 按平台、按层、按主题，等等。一样不教任何新页面的
东西**不是**一条轴，无论它多有用
（[ADR-0001](../adr/0001-the-build-out-is-a-route-not-a-seventh-axis.md)）。
`build-out/` 是一条横穿这些轴的路线；`cross-cutting/skills-maps/` 是它们的一个转置视图；
[`site/`](site/README.md) 是一个**视图** —— 它渲染材料而不添加任何材料，这是同一条判据被
第二次施行
（[ADR-0005](../adr/0005-the-site-is-a-view-not-a-seventh-axis.md)）。
_避免_：section、类别、track
