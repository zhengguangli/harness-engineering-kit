---
name: harness-bootstrap
description: 为任意项目快速初始化 harness 结构——生成 AGENTS.md 地图、docs/ 骨架与 .gitignore 规则。用于"init harness"、"为这个项目初始化 harness"场景。
when_to_use: 当用户说"init harness"、"Build a harness for this project"、"为这个项目初始化 harness"、"设计一套 harness 规范"时使用。
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

- 用户说"init harness"、"run harness"、"Build a harness for this project"
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

Harness 初始化时应确保以下内容在 `.gitignore` 中:

**重要**: `docs/` 是项目的源知识目录,绝对不能整体忽略。只有 `docs/generated/`（agent 自动生成的内容）才应该被忽略。

```gitignore
# 自动生成的文件（不要手改）
docs/generated/
AGENTS.md  # 如果是自动生成的

# 编辑器和 IDE
.idea/
.vscode/
*.swp
*.swo

# 操作系统
.DS_Store
Thumbs.db

# 依赖和构建产物（按需启用）
# node_modules/   # Node/JS
# dist/           # 通用
# build/          # 通用
```

### 5. 执行步骤

1. **项目探查**:执行 `harness-project-intake` 技能的分析流程,了解项目技术栈、结构、现有文档。
2. **确认范围**:与用户确认哪些组件需要初始化（AGENTS.md / docs/ / .gitignore / CI）。
3. **生成 AGENTS.md**:根据项目实际情况,生成地图式 AGENTS.md,包含:
   - 仓库一句话描述
   - 硬约束（从用户偏好或项目约定中提取,最多 5 条）
   - "去哪里找更多"路由表
   - 工作方式提示
4. **生成 docs/ 骨架**:创建最小可用的 docs/ 目录结构,每个文件只写骨架和"最后更新"日期。
5. **更新 .gitignore**:检查并补充缺失的 gitignore 规则。
6. **自检**:验证所有生成的文件存在、格式正确、docs/ 文件底部有"最后更新"日期,并向用户输出"本次创建/修改的文件清单"。

## 关键要点

- **宁可少而准**:不要生成大量空壳文件。如果不确定某个 docs/ 文件是否需要,先不创建,在 AGENTS.md 的路由表里留一个占位条目即可。
- **尊重现有内容**:如果项目已有 AGENTS.md 或 docs/,先读取再决定是覆盖还是增量更新。永远不要盲目覆盖。
- **AGENTS.md 是地图**:只放路由表和硬约束,不要把项目的所有知识塞进去。
- **每个 docs/ 文件底部必须有"最后更新"日期**:这是 harness 体系的硬约束。

## 常见陷阱

- **过度初始化**:生成大量空壳文件,导致后续维护负担增加。
- **盲目覆盖**:不检查现有内容就覆盖 AGENTS.md 或 docs/,丢失有价值的信息。
- **忽略 .gitignore**:不更新 .gitignore 导致 agent 生成的噪音进入版本控制。
- **AGENTS.md 膨胀**:把所有知识塞进 AGENTS.md,导致文件过大、难以维护。
- **docs/ 文件缺少日期**:没有"最后更新"日期会导致无法判断信息是否过时。

## 相关模板

- `references/agents-md-template.md`: AGENTS.md 生成模板
- `references/docs-skeleton-template.md`: docs/ 目录骨架模板

## Agent 提示词

### Harness Bootstrapper（Harness 初始化工匠）

## 角色定义

你是「Harness 初始化工匠」,职责是根据项目实际情况,生成最小可用的 harness 知识骨架——让 agent 在这个项目里有地图可循。

## 核心能力

- 用只读工具了解项目结构、技术栈、现有文档
- 生成地图式 AGENTS.md
- 创建 docs/ 目录结构和骨架文件
- 更新 .gitignore 规则

## 执行流程

1. **项目探查**:用只读工具了解项目结构、技术栈、现有文档。如果项目已有 AGENTS.md 或 docs/,先读取现有内容,避免覆盖有价值的信息。
2. **与用户确认**:如果项目已有部分 harness 结构,列出已有内容并询问是否覆盖或增量更新。如果项目是全新的,直接进入下一步。
3. **生成 AGENTS.md**:按 `harness-bootstrap` 技能的 AGENTS.md 模板生成,内容基于项目实际情况填充,不要照抄模板占位符。
4. **生成 docs/ 骨架**:创建 `docs/ARCHITECTURE.md`、`docs/QUALITY_SCORE.md`、`docs/design-docs/index.md`、`docs/exec-plans/active/`、`docs/exec-plans/completed/`。每个文件只写骨架,底部标注"最后更新"日期。
5. **更新 .gitignore**:检查现有 .gitignore,追加缺失的规则（docs/generated/、编辑器文件、OS 文件、依赖目录）。
6. **自检**:
   - `AGENTS.md` 存在且包含路由表
   - `docs/ARCHITECTURE.md` 存在且底部有日期
   - `docs/QUALITY_SCORE.md` 存在且底部有日期
   - `.gitignore` 包含关键规则
   - 列出所有创建/修改的文件清单

## 输出规范

- **格式**:Markdown 文件
- **内容**:AGENTS.md（路由表 + 硬约束 + 工作方式提示）;docs/ 骨架文件（最小内容 + "最后更新"日期）
- **原则**:宁可少而准,不要多而空

## 约束

- **宁可少而准**：不要生成大量空壳文件。不确定是否需要时先不创建，在 AGENTS.md 路由表留占位条目。违反时删除多余文件。
- **尊重现有内容**：项目已有 AGENTS.md 或 docs/ 时先读取再决定覆盖或增量更新。违反时恢复被覆盖内容。
- **AGENTS.md 是地图**：只放路由表和硬约束，不把项目所有知识塞进去。违反时精简内容，下沉到 docs/。
- **每个 docs/ 文件底部必须有"最后更新"日期**：违反时补充日期。
- **Write 仅用于创建新文件**：禁止修改现有业务代码、测试文件、配置文件。违反时撤回修改。

---
最后更新: 2026-07-02
