---
name: harness-bootstrap
description: 为任意项目快速初始化 harness 结构——生成 AGENTS.md 地图、docs/ 骨架与 .gitignore 规则。用于"init harness"、"为这个项目初始化 harness"、"Build a harness for this project"、"设计一套 harness 规范"场景。
when_to_use: |
  显式触发：用户说"init harness"、"Build a harness for this project"、"为这个项目初始化 harness"、"设计一套 harness 规范"。
  隐式触发：用户进入一个新项目希望用 harness 方法论管理 agent 协作、项目还没有 AGENTS.md/docs 结构、用户问"怎么开始用这套 harness"。
  不触发：项目已有完整的 harness 结构且用户未要求重新初始化、用户只想了解 harness 方法论而非实际初始化、项目规模极小不需要结构化知识管理、只需要重构 AGENTS.md/docs 结构而非全面初始化（用 harness-repo-map）。
disable-model-invocation: true
context: fork
agent: harness-bootstrapper
compatibility: opencode
metadata:
  category: workflow
---
# Harness Bootstrap（项目 Harness 初始化）

## 核心原则

- **最小可用知识骨架**:根据项目实际情况生成最小可用骨架——宁可少而准,不要多而空。
- **地图不是百科全书**:AGENTS.md 只包含路由表,不要把所有信息塞进来。
- **尊重现有内容**:先读取再决定覆盖还是增量更新,永远不要盲目覆盖。

## 何时使用

- 用户说"init harness"、"Build a harness for this project"
- 用户说"为这个项目初始化 harness"、"设计一套 harness 规范"
- 用户进入一个新项目,希望用 harness 方法论管理 agent 协作

## 何时不该用

- 项目已有完整的 harness 结构且用户未要求重新初始化
- 用户只想了解 harness 方法论,而非实际初始化
- 项目规模极小,不需要结构化知识管理
- 只需要重构 AGENTS.md/docs 结构而非全面初始化——用 `harness-repo-map`

## 方法论

### 1. 初始化的三层结构

1. **地图层（AGENTS.md）**:项目的"入口地图",告诉 agent 遇到问题去哪里找答案。
2. **知识层（docs/）**:结构化的项目知识——架构、设计决策、质量评分。
3. **约束层（.gitignore + CI）**:防止 agent 生成的噪音进入版本控制。

### 2. AGENTS.md 的设计原则

- **简短**:只包含"去哪里找答案"的路由表,不要把所有信息塞进来。
- **指向性**:每个条目指向一个具体的 `docs/` 文件或 `skills/` 目录。
- **硬约束极少数**:只有违反即阻塞合并的规则才放在这里。
- **工作方式提示**:告诉 agent 项目的编码风格、验证流程、提交规范。

### 3. docs/ 目录的最小可用集

| 文件 | 内容 | 是否必须 |
|---|---|---|
| `docs/ARCHITECTURE.md` | 项目架构、领域划分、依赖方向 | 是 |
| `docs/QUALITY_SCORE.md` | 各模块质量评分（可初始为空骨架） | 是 |
| `docs/design-docs/index.md` | 设计决策索引 | 推荐 |
| `docs/exec-plans/active/` | 当前执行计划目录 | 推荐 |
| `docs/exec-plans/completed/` | 已完成执行计划目录 | 推荐 |

### 4. .gitignore 规则

确保 `docs/generated/`、编辑器文件（`.idea/`、`.vscode/`、`*.swp`）、OS 文件（`.DS_Store`、`Thumbs.db`）被忽略。`docs/` 本身不能整体忽略。

### 5. 执行步骤

1. **项目探查**:执行 `harness-project-intake` 分析流程,了解技术栈、结构、现有文档。
2. **确认范围**:与用户确认需要初始化的组件（AGENTS.md / docs/ / .gitignore）。
3. **生成 AGENTS.md**:生成地图式 AGENTS.md（一句话描述 + 硬约束 + 路由表 + 工作方式提示）。
4. **生成 docs/ 骨架**:创建最小可用 docs/ 目录,每个文件只写骨架和"最后更新"日期。
5. **更新 .gitignore**:检查并补充缺失规则。
6. **自检**:验证文件存在、格式正确、docs/ 底部有日期,输出创建/修改清单。

## 关键要点

- **宁可少而准**:不确定是否需要时先不创建,在 AGENTS.md 路由表留占位条目。
- **尊重现有内容**:已有 AGENTS.md 或 docs/ 时先读取,再决定覆盖或增量更新。
- **AGENTS.md 是地图**:只放路由表和硬约束,不把所有知识塞进去。
- **每个 docs/ 文件底部必须有"最后更新"日期**:这是 harness 体系的硬约束。
- **AGENTS.md 硬约束精简**:只有违反即阻塞合并的规则才放在 AGENTS.md。
- **docs/ 最小可用集**:只创建必要骨架（ARCHITECTURE.md、QUALITY_SCORE.md、design-docs/index.md、exec-plans/）。
- **AGENTS.md 指向性明确**:每个条目指向具体 docs/ 文件,确保链接有效。
- **docs/ 可扩展性**:允许未来按需添加新文件,保持结构清晰。

## 边界情况处理

> 通用边界情况（项目规模极小、遗留项目改造、多团队协作等）参见 `references/common-edge-cases.md`，以下仅列出本 skill 特有的边界情况。

### 项目已有部分harness结构

**场景**：项目已有AGENTS.md或docs/目录，但不完整
**处理**：先读取现有内容，再决定是覆盖还是增量更新，输出修改清单供用户确认

### 项目技术栈复杂

**场景**：项目使用多种技术栈，需要特殊处理
**处理**：为每种技术栈提供定制化配置（.gitignore规则、docs/结构）

## 常见陷阱

- **过度初始化**:生成大量空壳文件,导致后续维护负担增加。
- **盲目覆盖**:不检查现有内容就覆盖 AGENTS.md 或 docs/,丢失有价值的信息。
- **忽略 .gitignore**:不更新 .gitignore 导致 agent 生成的噪音进入版本控制。
- **AGENTS.md 膨胀**:把所有知识塞进 AGENTS.md,导致文件过大、难以维护。
- **docs/ 文件缺少日期**:没有"最后更新"日期会导致无法判断信息是否过时。

## 相关 skill

- `harness-project-intake`:初始化前先分析项目（步骤 1 依赖）
- `harness-repo-map`:初始化后维护 AGENTS.md 和 docs/ 的健康状态

## 相关模板

- `references/agents-md-template.md`: AGENTS.md 生成模板
- `references/agents-md-examples.md`: 各技术栈 AGENTS.md 示例（Node.js/Python/Go/Rust/Java）
- `references/docs-skeleton-template.md`: docs/ 目录骨架模板
- `references/docs-skeleton-by-stack.md`: 各技术栈 docs/ 骨架补充模板
- `references/gitignore-templates.md`: 各技术栈 .gitignore 模板（Node.js/Python/Go/Rust/Java/PHP/Ruby/C#/Dart/Elixir）
- `references/init-workflows.md`: 各技术栈初始化流程与额外步骤
- `references/automation-check-script.sh`: 自动化检查脚本

## 最佳实践

- 宁可少而准：不确定是否需要时先不创建，在 AGENTS.md 路由表留占位条目。
- 尊重现有内容：项目已有 AGENTS.md 或 docs/ 时先读取再决定覆盖或增量更新。
- AGENTS.md 是地图：只放路由表和硬约束，不把项目所有知识塞进去。
- 每个 docs/ 文件底部必须有"最后更新"日期。

## Agent 提示词

### 角色定义

你是「Harness 初始化工匠」，职责是根据项目实际情况，生成最小可用的 harness 知识骨架——让 agent 在这个项目里有地图可循。

### 核心能力

- 用只读工具了解项目结构、技术栈、现有文档
- 生成地图式 AGENTS.md
- 创建 docs/ 目录结构和骨架文件
- 更新 .gitignore 规则
- 处理各种边界情况，提供最佳实践

### 执行流程

1. **项目探查**：用只读工具了解项目结构、技术栈、现有文档。已有 AGENTS.md 或 docs/ 时先读取，避免覆盖。
2. **与用户确认**：已有部分 harness 结构时，列出已有内容并询问是否覆盖或增量更新。
3. **生成 AGENTS.md**：按 `references/agents-md-template.md` 模板生成，参考 `references/agents-md-examples.md` 中对应技术栈示例，内容基于项目实际填充。
4. **生成 docs/ 骨架**：创建 ARCHITECTURE.md、QUALITY_SCORE.md、design-docs/index.md、exec-plans/active/、exec-plans/completed/。每个文件只写骨架，底部标注日期。
5. **更新 .gitignore**：参考 `references/gitignore-templates.md`，追加缺失规则。
6. **自检**：验证 AGENTS.md 存在且含路由表、docs/ 文件存在且有日期、.gitignore 包含关键规则，列出文件清单。

### 约束

- **Write 仅用于创建新文件**：禁止修改现有业务代码、测试文件、配置文件。
- **区分项目规模**：小项目简化初始化。
- **提供具体指导**：每个步骤必须可执行，不能模糊。
- **处理边界情况**：必须处理各种边界情况，提供最佳实践。

### 输出规范

- **格式**：Markdown 文件
- **内容**：AGENTS.md（路由表 + 硬约束 + 工作方式提示）；docs/ 骨架文件（最小内容 + "最后更新"日期）
- **修改清单**：列出所有创建/修改的文件清单

---
最后更新: 2026-07-02（变更：A+级优化，增加边界情况处理，增加最佳实践，增加自动化检查脚本，优化Agent提示词）
