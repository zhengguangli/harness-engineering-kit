---
name: harness-repo-map
description: 把仓库知识管理从巨型 AGENTS.md 重构为「地图 + 结构化 docs/」的渐进式披露模式。当项目需要从零搭建 AGENTS.md/docs 结构、现有 AGENTS.md 膨胀需要瘦身下沉到 docs/、需要审计文档是否过期/断链或与代码行为脱节、需要为渐进式披露设计目录层级、或抱怨 agent 缺乏项目背景时使用。
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

## 何时使用

- 项目还没有 AGENTS.md / docs 结构,需要从零搭建。
- 现有 AGENTS.md 已经膨胀到几百行,需要"瘦身为地图"并把内容下沉到 `docs/`。
- 需要审计文档是否过期、是否有断链、是否和真实代码行为脱节。
- 需要为"渐进式披露"设计目录层级(让 agent 从小入口开始,被教会去哪里找更多)。

## 目标目录骨架

参考本技能 `references/` 子目录里的各模板文件。典型结构:

```
AGENTS.md                  # 100 行左右的地图,只放"现在该看哪"
docs/
├── ARCHITECTURE.md        # 顶层架构地图:领域划分、分层规则
├── QUALITY_SCORE.md       # 按领域/分层的质量评分
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

写 AGENTS.md 的 4 条核心规则(长度、内容范围、变化频率、可验证性),详见 `references/agents-md-writing-rules.md`。

## 机械化校验,不要指望人工维护

仅靠人工记得更新文档是不会长期生效的。以下检查由 `doc-gardener` agent 在其固定工作流中内联执行,不需要额外生成独立脚本或 CI 配置文件:

- **断链检测**:扫描 `docs/` 内部的相互引用,确保指向的文件/锚点还存在。
- **新鲜度检测**:给关键文档加上"最后校验日期"或"对应代码版本"的元数据,超期未校验则标记为过期。
- **覆盖率检测**:对照代码里的领域/包列表,检查 `ARCHITECTURE.md` / `QUALITY_SCORE.md` 是否每个领域都有条目,新增领域没有文档时报告缺口。
- **结构检测**:检查 `docs/` 目录是否符合约定的骨架(比如新计划是否真的落在 `exec-plans/active/`)。

把这些检查的失败信息写成对 agent 友好的修复说明(参考 `harness-architecture-boundaries` 技能里"把修复指令写进报错信息"的做法),这样发现问题的 agent 能直接照着错误信息修。

## 初始化步骤(首次为项目搭建 docs/ 骨架时)

1. 创建当前平台的入口文件(参考 `references/agents-md-map-template.md`)。只创建自己平台的,不要替另一个平台创建。
2. 在 `docs/` 下创建 `ARCHITECTURE.md`（参考 `references/architecture-template.md`）和 `QUALITY_SCORE.md`（参考 `references/quality-score-template.md`）。这两个文件属于 `docs/`，不要放在根目录。
3. 按需创建以下空目录(如不存在):`docs/design-docs/`、`docs/exec-plans/active/`、`docs/exec-plans/completed/`、`docs/generated/`、`docs/product-specs/`、`docs/references/`。
4. 从 `references/` 子目录的模板创建对应索引文件:`docs/design-docs/index.md`、`docs/design-docs/core-beliefs.md`、`docs/product-specs/index.md`、`docs/exec-plans/tech-debt-tracker.md`。
5. 按项目实际情况填充模板里的占位符(领域名、代码路径、日期等)。
6. 文档校验由 `doc-gardener` agent 在其固定工作流中内联执行(断链检测、新鲜度检测、覆盖率检测、结构检测),不需要额外生成独立脚本。
7. 在入口文件顶部写明:"这个文件是地图,不是百科全书;深入信息请看 docs/"。

## 操作步骤(当你被要求"搭建/重构知识库"时)

1. 先盘点现状:现有 AGENTS.md/README 有多长?是地图还是百科全书?`docs/` 是否存在、是否有结构?
2. 设计/裁剪目录骨架(参考上面的模板),只创建项目真正需要的子目录。
3. 把百科全书式 AGENTS.md 里的内容,按主题拆分搬运到对应 `docs/*.md`,AGENTS.md 改写成指针表。
4. 给每个被搬运的文档补上一句"这是关于什么的、什么时候该看它"。
5. 如果项目还没有校验脚本,按初始化步骤第 6 步补上。
6. 在入口文件顶部写明:"这个文件是地图,不是百科全书;深入信息请看 docs/"。

## 配合的 agent

- `doc-gardener` agent:周期性地或在合并后扫描 `docs/` 是否和代码行为脱节,生成小颗粒度的修复建议或直接打开修复型 PR。日常维护用这个,不要等人工每周一次大扫除。

## 相关模板

- `references/agents-md-map-template.md`: AGENTS.md 地图模板
- `references/design-docs-index-template.md`: 设计文档索引模板
- `references/core-beliefs-template.md`: 核心信念模板
- `references/product-specs-index-template.md`: 产品规格索引模板
- `references/architecture-template.md`: ARCHITECTURE.md 架构文档模板
- `references/quality-score-template.md`: QUALITY_SCORE.md 质量评分模板
- `references/doc-gardener-prompt.md`: doc-gardener agent 系统提示词

---
最后更新: 2026-06-29
