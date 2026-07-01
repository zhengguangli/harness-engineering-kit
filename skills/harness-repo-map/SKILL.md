---
name: harness-repo-map
description: 把仓库知识管理从巨型 AGENTS.md 重构为「地图 + 结构化 docs/」的渐进式披露模式。当项目需要从零搭建 AGENTS.md/docs 结构、现有 AGENTS.md 膨胀需要瘦身下沉到 docs/、需要审计文档是否过期/断链或与代码行为脱节、需要为渐进式披露设计目录层级、或抱怨 agent 缺乏项目背景时使用。
version: 0.1.0
---

# Repo Knowledge Map（仓库知识地图）

## 触发信号

### 显式触发（explicit）
- `harness-repo-map`
- `repo-map`
- `AGENTS.md`
- `docs/`

### 语义意图（intent）
- 从零搭建 AGENTS.md / docs 结构
- AGENTS.md 膨胀需瘦身并下沉到 docs/
- 审计文档过期、断链或与代码脱节
- 为渐进式披露设计目录层级

### 证据触发（artifacts）
- `AGENTS.md`
- `docs/`
- `references`
- `generated/`
- `links`

### 避免触发（avoid_when）
- 单文件脚本项目不需要结构化文档体系
- 只更新某一个具体文档，不是重构知识体系

## 核心原则

- **AGENTS.md 是地图，不是百科全书**：巨型 AGENTS.md 是反模式——它挤占上下文配额、无法被机械化校验、瞬间腐烂。正确做法是把 AGENTS.md 当目录（table of contents），指向 `docs/` 里的真相来源。
- **知识必须可机械化发现和校验**：Google Docs、Slack 讨论、人脑里的"团队共识"如果没有写进仓库，就和从未发生过一样。文档要以 agent 能机械化发现、机械化校验的方式存在。
- **渐进式披露**：agent 从小入口开始，被教会去哪里找更多。不要一次性把所有信息塞进一个文件。

## 何时使用

- 项目还没有 AGENTS.md / docs 结构，需要从零搭建。
- 现有 AGENTS.md 已膨胀到几百行，需要"瘦身为地图"并把内容下沉到 `docs/`。
- 需要审计文档是否过期、有断链、或与真实代码行为脱节。
- 需要为渐进式披露设计目录层级。
- 用户抱怨 agent 缺乏项目背景。

## 何时不该用

- 项目很小（单文件脚本），不需要结构化文档。
- 用户只需要更新某个具体文档，而不是重构整个知识体系。

## 方法论

### 目标目录骨架

```
AGENTS.md                  # 100 行左右的地图，只放"现在该看哪"
docs/
├── ARCHITECTURE.md        # 顶层架构地图：领域划分、分层规则
├── QUALITY_SCORE.md       # 按领域/分层的质量评分
├── design-docs/
│   ├── index.md           # 设计文档索引 + 校验状态
│   └── core-beliefs.md    # agent-first 的核心运作信念
├── exec-plans/
│   ├── active/            # 进行中的执行计划
│   ├── completed/         # 已完成计划的归档
│   └── tech-debt-tracker.md
├── generated/             # 由工具自动生成的文档（不要手改）
├── product-specs/
│   └── index.md
└── references/            # 第三方库/工具的精简参考
```

不是每个项目都需要全部子目录——按需裁剪。但目录本身要记录在 AGENTS.md 里，让 agent 第一次进入仓库就知道"信息分布在哪几类文件里"。

写 AGENTS.md 的 4 条核心规则（长度、内容范围、变化频率、可验证性），详见 `references/agents-md-map-template.md` 的附录 B。

### 初始化步骤（首次为项目搭建 docs/ 骨架）

1. 创建入口文件（参考 `references/agents-md-map-template.md`），只创建自己平台的。
2. 在 `docs/` 下创建 `ARCHITECTURE.md`（参考 `references/architecture-template.md`）和 `QUALITY_SCORE.md`（参考 `references/quality-score-template.md`）。这两个文件属于 `docs/`，不要放在根目录。
3. 按需创建空目录：`docs/design-docs/`、`docs/exec-plans/active/`、`docs/exec-plans/completed/`、`docs/generated/`、`docs/product-specs/`、`docs/references/`。
4. 从 `references/` 子目录的模板创建对应索引文件：`docs/design-docs/index.md`、`docs/design-docs/core-beliefs.md`、`docs/product-specs/index.md`、`docs/exec-plans/tech-debt-tracker.md`。
5. 按项目实际情况填充模板里的占位符（领域名、代码路径、日期等）。
6. 文档校验由 `doc-gardener` agent 在其工作流中内联执行，不需要额外生成独立脚本。
7. 在入口文件顶部写明："这个文件是地图，不是百科全书；深入信息请看 docs/"。

### 操作步骤（搭建/重构知识库）

1. **盘点现状**：现有 AGENTS.md/README 有多长？是地图还是百科全书？`docs/` 是否存在、是否有结构？
2. **设计目录骨架**：参考上面的模板，只创建项目真正需要的子目录。
3. **拆分搬运**：把百科全书式 AGENTS.md 里的内容按主题拆分到 `docs/*.md`，AGENTS.md 改写成指针表。
4. **补元信息**：给每个被搬运的文档补上"这是关于什么的、什么时候该看它"。
5. **设置校验**：按初始化步骤第 6 步，由 `doc-gardener` agent 负责校验。
6. **写明地图声明**：在入口文件顶部写明"这个文件是地图，不是百科全书；深入信息请看 docs/"。

### 机械化校验（doc-gardener agent 内联执行）

仅靠人工记得更新文档不会长期生效。以下检查由 `doc-gardener` agent 在其工作流中内联执行：

- **断链检测**：扫描 `docs/` 内部的相互引用，确保指向的文件/锚点还存在。
- **新鲜度检测**：给关键文档加上"最后校验日期"或"对应代码版本"元数据，超期未校验则标记为过期。
- **覆盖率检测**：对照代码里的领域/包列表，检查 `ARCHITECTURE.md` / `QUALITY_SCORE.md` 是否每个领域都有条目。
- **结构检测**：检查 `docs/` 目录是否符合约定骨架（如新计划是否落在 `exec-plans/active/`）。

失败信息写成对 agent 友好的修复说明（参考 `harness-architecture-boundaries` 技能里"把修复指令写进报错信息"的做法），让发现问题的 agent 能直接照着修。

## 关键要点

- AGENTS.md 超过 100 行就该瘦身，把内容下沉到 `docs/`。
- 目录骨架不需要一步到位，按需裁剪，但要记录在 AGENTS.md 里。
- 误导性内容（说了和现实不符）比缺失内容更危险，优先修复。
- 过时的执行记录（如已完成 exec-plan）本身有历史价值，不要删除——真正该清理的是"仍标着 active 却已不准确"的内容。

## 常见陷阱

- **百科全书式 AGENTS.md**：把所有规则塞进一个文件，agent 无法有效导航，上下文被挤占。
- **只建不维护**：创建了 docs/ 结构但没有校验机制，文档很快腐烂。
- **删除历史记录**：把过时的 exec-plan 决策记录删除——过时的执行记录仍有历史价值。
- **跨平台重复**：同时为 Codex 和 OpenAI agents 创建重复的入口文件，只需创建自己平台的。

## 相关模板

- `references/agents-md-map-template.md`: AGENTS.md 地图模板（含核心信念和写作规则附录）
- `references/docs-index-templates.md`: 设计文档索引 + 产品规格索引模板
- `references/architecture-template.md`: 基于 `harness-architecture-boundaries` 的本地适配副本
- `references/quality-score-template.md`: 基于 `harness-golden-principles` 的本地适配副本
- `agents/doc-gardener.md`: doc-gardener agent 系统提示词（canonical 版本）
