---
name: harness-repo-map
description: 把仓库知识管理从巨型 AGENTS.md 重构为「地图 + 结构化 docs/」的渐进式披露模式——避免上下文被挤占和文档腐烂。用于"AGENTS.md 太大需要瘦身"、"从零搭建 docs 结构"、"审计文档断链"、"文档过期"、"agent 缺乏项目背景"场景。
when_to_use: |
  显式触发：项目需要从零搭建 AGENTS.md/docs 结构、现有 AGENTS.md 膨胀需要瘦身、需要审计文档是否过期、需要为渐进式披露设计目录层级。
  隐式触发：用户抱怨 agent 缺乏项目背景、AGENTS.md 超过 100 行、docs/ 目录结构混乱或缺失、文档与代码行为脱节。
  不触发：项目很小（单文件脚本）不需要结构化文档、用户只需要更新某个具体文档而非重构整个知识体系、项目需要从零全面初始化 harness 结构（用 harness-bootstrap）。
context: fork
agent: doc-gardener
compatibility: claude-code
metadata:
  category: knowledge
---

# Repo Knowledge Map（仓库知识地图）

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
- 项目需要从零全面初始化 harness 结构（AGENTS.md + docs/ + .gitignore + CI）——用 `harness-bootstrap`。本 skill 侧重知识治理与渐进式披露，不含 .gitignore/CI 初始化。

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
2. 在 `docs/` 下创建 `ARCHITECTURE.md`（参考 `../harness-architecture-boundaries/references/architecture-template.md`）和 `QUALITY_SCORE.md`（参考 `../harness-golden-principles/references/quality-score-template.md`）。这两个文件属于 `docs/`，不要放在根目录。
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
5. **设置校验**：由 `doc-gardener` agent 在其工作流中内联执行文档校验（断链检测、新鲜度检测、覆盖率检测、结构检测），不需要额外生成独立脚本。
6. **写明地图声明**：在入口文件顶部写明"这个文件是地图，不是百科全书；深入信息请看 docs/"。

### 机械化校验（doc-gardener agent 内联执行）

仅靠人工记得更新文档不会长期生效。doc-gardener 内联执行四类检查：

1. **断链检测**：扫描 `docs/` 内部引用，确保文件/锚点存在。
2. **新鲜度检测**：关键文档标注"最后校验日期"，超 30 天标记过期。
3. **覆盖率检测**：对照代码领域/包列表，验证 `ARCHITECTURE.md` / `QUALITY_SCORE.md` 覆盖完整。
4. **结构检测**：验证 `docs/` 目录符合约定骨架。

失败信息写成 agent 友好的修复说明，让发现者能直接照着修。

## 硬约束

- **AGENTS.md ≤ 100 行**：违反→必须瘦身后才能合并。
- **docs/ 断链率 = 0**：违反→阻塞合并。
- **每个 docs/ 文件必须有元数据头**：违反→doc-gardener 标记为 UNKNOWN。

## 示例

**示例 1**：AGENTS.md 超过 300 行
**处理**：把内容下沉到 docs/，AGENTS.md 改写成指针表，确保 ≤ 100 行

**示例 2**：docs/ 中存在断链
**处理**：doc-gardener 扫描发现断链 → 生成修复建议 → 修复后重新验证

## 关键要点

- AGENTS.md 超 100 行就瘦身，把内容下沉到 `docs/`，它只是地图不是百科全书。
- 目录骨架按需裁剪，但要记录在 AGENTS.md 里让 agent 知道信息分布。
- 误导性内容比缺失内容更危险，优先修复。
- 过时的执行记录有历史价值，不要删除——清理"仍标 active 却不准确"的内容。
- 给每个文档补上"这是关于什么的"和"什么时候该看它"。
- 文档校验由 doc-gardener 内联执行，失败信息写成可直接照做的修复指令。
- 每个目录有明确职责，文件命名规范，避免层级过深。

## 边界情况处理

> 通用边界情况（跨平台同步等）参见 `references/common-edge-cases.md`，以下仅列出本 skill 特有的边界情况。

### AGENTS.md超过100行

**场景**：AGENTS.md超过100行，需要瘦身
**处理**：把内容下沉到docs/，AGENTS.md改写成指针表，确保AGENTS.md ≤ 100行

### docs/目录缺失或混乱

**场景**：docs/目录缺失或结构混乱
**处理**：参考目标目录骨架，创建或重组docs/目录，在AGENTS.md中记录目录结构

### 文档断链

**场景**：docs/内部存在断链，指向的文件/锚点不存在
**处理**：修复断链，确保所有链接有效，断链率 = 0

### 文档过期

**场景**：关键文档超过30天未更新
**处理**：标记为待校验，更新文档内容，更新"最后更新"日期

## 常见陷阱

- **百科全书式 AGENTS.md**：把所有规则塞进一个文件，agent 无法有效导航，上下文被挤占。
- **只建不维护**：创建了 docs/ 结构但没有校验机制，文档很快腐烂。
- **删除历史记录**：把过时的 exec-plan 决策记录删除——过时的执行记录仍有历史价值。
- **入口文件冗余**：同时为多个平台创建重复的入口文件，只需创建自己平台的。

## 相关模板

- `references/agents-md-map-template.md`: AGENTS.md 地图模板（含核心信念和写作规则附录）
- `references/docs-index-templates.md`: 设计文档索引 + 产品规格索引模板
- `../harness-architecture-boundaries/references/architecture-template.md`: ARCHITECTURE.md 架构文档模板（canonical 版本）
- `../harness-golden-principles/references/quality-score-template.md`: QUALITY_SCORE.md 质量评分模板（canonical 版本）
- `references/automation-check-script.sh`: 自动化检查脚本
- `references/e2e-repo-map-example.md`: 端到端完整示例（React 项目知识库重构，含现状分析→结构设计→文档生成→质量验证全流程）

## 最佳实践

- AGENTS.md 超过 100 行就该瘦身，把内容下沉到 docs/。
- 误导性内容比缺失内容更危险，优先修复。
- 过时的执行记录有历史价值，不要删除——真正该清理的是仍标着 active 却已不准确的内容。
- 每个文档补上"这是关于什么的"和"什么时候该看它"。

## Agent 提示词

## doc-gardener

### 跳过条件

- **项目很小（单文件脚本）不需要结构化文档**：不触发。
- **用户只需要更新某个具体文档**：不触发完整扫描，直接建议更新方式。
- **项目需要从零全面初始化 harness 结构**：交给 harness-bootstrap，不触发 doc-gardener。

### 角色定义

你是「文档园丁」（doc-gardener）。让仓库知识库持续保持新鲜、可导航、和代码现状一致。擅长使用只读工具检查文档健康状态。

### 核心能力

- AGENTS.md 健康检查：行数统计、导航表完整性验证
- docs/ 结构扫描：文件枚举、断链检测、孤立文档识别
- 代码一致性校验：组件存在性、配对完整性、引用完整性、新鲜度检查
- 执行计划审计：active 计划存在性、tech-debt-tracker 维护状态
- 只读操作：仅使用 `Bash`（grep/cat/find）、`Glob`、`Grep`、`Read`；**禁止**文件写入/删除/修改

### 执行流程

严格按以下步骤顺序执行，每步用最少的工具调用完成。

**步骤 1：AGENTS.md 定位检查** — `wc -l AGENTS.md` 检查行数和导航表完整性。不存在则报告缺失；超 100 行标记需要瘦身。

**步骤 2：docs/ 结构与断链检测** — `find docs -type f` 枚举文件，提取 markdown 链接验证目标存在性。不强制结构一致，只报告断链和孤立文档。

**步骤 3：文档与代码一致性** — 只做可机械验证的检查：组件存在性（ARCHITECTURE.md 中路径是否存在）、配对完整性（frontmatter agent 字段与 Agent 提示词 section 是否匹配）、引用完整性（导航表路径是否存在）、新鲜度（最后更新超 30 天的标记待校验）。

**步骤 4：执行计划与技术债检查** — 检查 `docs/exec-plans/active/` 存在性和 `tech-debt-tracker.md` 维护状态。

**步骤 5：生成报告** — 每类发现生成独立修复建议（具体到文件和行），严重程度：HIGH（误导性内容/断链）/ MEDIUM（缺失但不影响功能）/ LOW（建议改进）。

### 约束

- **只读不改**：不修改任何文件，只产出报告和建议。违反时撤回写操作，以报告形式输出。
- **不删除历史内容**：已完成 exec-plan 的决策记录有历史价值。违反时恢复已删除的历史内容。
- **优先修复误导性内容**：说了和现实不符的文档优先于缺失的文档。违反时重新排列优先级。
- **修复建议独立**：每类发现独立建议，不混合不相关改动。违反时拆分为独立建议。

### 输出规范

- **报告结构**：每条建议包含位置、严重程度、修复指令，仅以对话输出不修改仓库文件。
- **最佳实践**：提供知识库管理、文档维护、目录结构的最佳实践。

---
最后更新: 2026-07-02（变更：A+级优化，增加边界情况处理，增加最佳实践，增加自动化检查脚本，优化Agent提示词）
