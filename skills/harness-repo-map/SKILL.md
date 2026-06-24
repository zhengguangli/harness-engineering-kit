---
name: harness-repo-map
description: 把仓库知识管理从"一个巨大的 AGENTS.md / README"重构为"地图 + 结构化 docs/ 系统记录"的渐进式披露模式。每当用户要新建或重构 AGENTS.md、CLAUDE.md、项目说明文档,或者抱怨"agent 不了解项目背景""文档又和代码脱节了""AGENTS.md 越写越长但 agent 还是不知道该看哪"时,主动使用此技能。也适用于审计现有文档库的过期程度、设计 docs/ 目录骨架、或建立文档新鲜度的机械化校验。
---

# Repo Knowledge Map(仓库知识地图)

## 核心原则

对 agent 来说,**它在上下文里看不到的东西,就是不存在的**。Google Docs、Slack 讨论、人脑里的"团队共识",如果没有被写进仓库,就和从未发生过一样。所以这个技能要解决的不是"写不写文档",而是"知识要以 agent 能机械化发现、机械化校验的方式存在于仓库里"。

由此推出最重要的反直觉结论:**一个巨大的 AGENTS.md 是反模式**。常见失败模式:

- **上下文是稀缺资源**:一个巨型说明文件会挤占任务本身、代码、相关文档的上下文配额,agent 不得不在"记住所有规则"和"专注当前任务"之间二选一。
- **过度强调等于没有强调**:当文件里每一条都被标为"重要",agent 就只能局部模式匹配,而不是有意识地导航。
- **它会瞬间腐烂**:单体说明书没人愿意持续维护,很快变成一堆"曾经为真"的规则坟场。
- **它无法被校验**:一大段自然语言文本没法做覆盖率检查、新鲜度检查、归属检查、交叉引用检查,腐化是必然的。

正确模式:**把 AGENTS.md 当目录(table of contents),不要当百科全书。** 仓库里的结构化 `docs/` 目录才是知识的系统记录(system of record),AGENTS.md 只是一张地图,指向更深的真相来源。

## 何时使用这个技能

- 项目还没有 AGENTS.md / docs 结构,需要从零搭建。
- 现有 AGENTS.md 已经膨胀到几百行,需要"瘦身为地图"并把内容下沉到 `docs/`。
- 需要审计文档是否过期、是否有断链、是否和真实代码行为脱节。
- 需要为"渐进式披露"设计目录层级(让 agent 从小入口开始,被教会去哪里找更多)。

## 目标目录骨架

参考本技能 `references/` 子目录里的各模板文件。典型结构:

```
AGENTS.md                  # 100 行左右的地图,只放"现在该看哪"
ARCHITECTURE.md            # 顶层架构地图:领域划分、分层规则
QUALITY_SCORE.md           # ← 仓库根目录,不在 docs/ 内;按领域/分层打分
docs/
├── design-docs/
│   ├── index.md           # 设计文档索引 + 校验状态
│   └── core-beliefs.md    # agent-first 的核心运作信念
├── exec-plans/
│   ├── active/            # 进行中的执行计划(见 harness-exec-plans 技能)
│   ├── completed/         # 已完成计划的归档
│   └── tech-debt-tracker.md
├── generated/             # 由工具自动生成的文档(如 db-schema.md),不要手改
├── product-specs/
│   └── index.md
└── references/            # 第三方库/工具的 llms.txt 之类的精简参考
```

不是每个项目都需要全部子目录——按需裁剪,但**目录本身要被记录在 AGENTS.md 里**,这样 agent 第一次进入仓库就知道"信息分布在哪几类文件里",而不需要每次都重新探索。

## 写 AGENTS.md(地图)的规则

1. **目标长度 ~100 行**。如果写到 200 行还没收尾,说明你在写百科全书而不是地图,把内容下沉到 `docs/` 对应文件,AGENTS.md 里只留一行指针。
2. **只放三类内容**:(a) 仓库结构总览和"先看这里"的指针,(b) 极少数全局硬约束(例如"禁止手写代码""所有数据边界必须 parse 不要 validate"),(c) 指向 `docs/` 各子目录的导航表。
3. **不要写会频繁变化的细节**(具体 API 签名、当前进度、某个 bug 的状态)——这些放进 `docs/generated/`、`exec-plans/`,由工具或 agent 任务保持新鲜。
4. **每条规则都要可执行或可验证**。如果一条规则没法被 lint/测试机械检查,要么把它变成可检查的形式,要么承认它只是建议而不是约束,不要混在一起。

## 机械化校验,不要指望人工维护

仅靠人工记得更新文档是不会长期生效的。以下检查由 `doc-gardener` agent 在其固定工作流中内联执行,不需要额外生成独立脚本或 CI 配置文件:

- **断链检测**:扫描 `docs/` 内部的相互引用,确保指向的文件/锚点还存在。
- **新鲜度检测**:给关键文档加上"最后校验日期"或"对应代码版本"的元数据,超期未校验则标记为过期。
- **覆盖率检测**:对照代码里的领域/包列表,检查 `ARCHITECTURE.md` / `QUALITY_SCORE.md` 是否每个领域都有条目,新增领域没有文档时报告缺口。
- **结构检测**:检查 `docs/` 目录是否符合约定的骨架(比如新计划是否真的落在 `exec-plans/active/`)。

把这些检查的失败信息写成对 agent 友好的修复说明(参考 `harness-architecture-boundaries` 技能里"把修复指令写进报错信息"的做法),这样发现问题的 agent 能直接照着错误信息修。

## 初始化步骤(首次为项目搭建 docs/ 骨架时)

1. 在仓库根目录创建 `AGENTS.md`(参考本技能 `references/agents-md-template.md`)、`ARCHITECTURE.md`(参考 `harness-architecture-boundaries` 技能里的 `references/architecture-template.md`)、`QUALITY_SCORE.md`(参考 `harness-golden-principles` 技能里的 `references/quality-score-template.md`)。
2. 按需创建以下空目录(如不存在):`docs/design-docs/`、`docs/exec-plans/active/`、`docs/exec-plans/completed/`、`docs/generated/`、`docs/product-specs/`、`docs/references/`。
3. 从 `references/` 子目录的模板创建对应索引文件:`docs/design-docs/index.md`、`docs/design-docs/core-beliefs.md`、`docs/product-specs/index.md`、`docs/exec-plans/tech-debt-tracker.md`。
4. 按项目实际情况填充模板里的占位符(领域名、代码路径、日期等)。
5. 文档校验由 `doc-gardener` agent 在其固定工作流中内联执行(断链检测、新鲜度检测、覆盖率检测、结构检测),不需要额外生成独立脚本。
6. 在 AGENTS.md 顶部写明:"这个文件是地图,不是百科全书;深入信息请看 docs/"。

## 操作步骤(当你被要求"搭建/重构知识库"时)

1. 先盘点现状:现有 AGENTS.md/README 有多长?是地图还是百科全书?`docs/` 是否存在、是否有结构?
2. 设计/裁剪目录骨架(参考上面的模板),只创建项目真正需要的子目录。
3. 把百科全书式 AGENTS.md 里的内容,按主题拆分搬运到对应 `docs/*.md`,AGENTS.md 改写成指针表。
4. 给每个被搬运的文档补上一句"这是关于什么的、什么时候该看它"。
5. 如果项目还没有校验脚本,按初始化步骤第 5 步补上。
6. 在 AGENTS.md 顶部写明:"这个文件是地图,不是百科全书;深入信息请看 docs/"。

## 配合的 agent

- `doc-gardener` agent:周期性地或在合并后扫描 `docs/` 是否和代码行为脱节,生成小颗粒度的修复建议或直接打开修复型 PR。日常维护用这个,不要等人工每周一次大扫除。
