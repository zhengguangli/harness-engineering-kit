---
name: harness-bootstrap
description: 为任意项目一键初始化 harness 结构——生成 AGENTS.md 地图、docs/ 骨架、.gitignore 规则、CI 模板。当用户说"init harness"、"Build a harness for this project"、"为这个项目初始化 harness"、"设计一套 harness 规范"时使用。
---

# Harness Bootstrap（项目 Harness 初始化）

## 核心原则

Harness 的核心价值是**让 agent 在项目里有地图可循**。初始化不是"复制一堆模板文件",而是根据项目的实际情况生成**最小可用的知识骨架**——宁可少而准,不要多而空。

## 何时使用

- 用户说"init harness"、"run harness"、"Build a harness for this project"。
- 用户说"为这个项目初始化 harness"、"设计一套 harness 规范"。
- 用户进入一个新项目,希望用 harness 方法论管理 agent 协作。

## 方法论

### 初始化的三层结构

1. **地图层（AGENTS.md）**:项目的"入口地图",告诉 agent 遇到问题去哪里找答案。
2. **知识层（docs/）**:结构化的项目知识——架构、设计决策、质量评分。
3. **约束层（.gitignore + CI）**:防止 agent 生成的噪音进入版本控制。

### AGENTS.md 的设计原则

AGENTS.md 是地图,不是百科全书:

- **简短**:只包含"去哪里找答案"的路由表,不要把所有信息塞进来。
- **指向性**:每个条目指向一个具体的 `docs/` 文件或 `skills/` 目录。
- **硬约束极少数**:只有违反即阻塞合并的规则才放在这里。
- **工作方式提示**:告诉 agent 项目的编码风格、验证流程、提交规范。

### docs/ 目录的最小可用集

| 文件 | 内容 | 是否必须 |
|---|---|---|
| `docs/ARCHITECTURE.md` | 项目架构、领域划分、依赖方向 | 是 |
| `docs/QUALITY_SCORE.md` | 各模块质量评分（可初始为空骨架） | 是 |
| `docs/design-docs/index.md` | 设计决策索引 | 推荐 |
| `docs/exec-plans/active/` | 当前执行计划目录 | 推荐 |
| `docs/exec-plans/completed/` | 已完成执行计划目录 | 推荐 |

### .gitignore 规则

Harness 初始化时应确保以下内容在 `.gitignore` 中:

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

# 依赖和构建产物
node_modules/
dist/
build/
```

## 初始化步骤

1. **项目探查**:执行 `harness-project-intake` 技能的分析流程,了解项目技术栈、结构、现有文档。
2. **确认范围**:与用户确认哪些组件需要初始化（AGENTS.md / docs/ / .gitignore / CI）。
3. **生成 AGENTS.md**:根据项目实际情况,生成地图式 AGENTS.md,包含:
   - 仓库一句话描述
   - 硬约束（从用户偏好或项目约定中提取,最多 5 条）
   - "去哪里找更多"路由表
   - 工作方式提示
4. **生成 docs/ 骨架**:创建最小可用的 docs/ 目录结构,每个文件只写骨架和"最后更新"日期。
5. **更新 .gitignore**:检查并补充缺失的 gitignore 规则。
6. **自检**:验证所有生成的文件存在、格式正确、docs/ 文件底部有"最后更新"日期。

## 配合的 agent

- `project-analyzer` agent:在初始化前先执行项目分析,获取技术栈和结构信息。
- `harness-bootstrapper` agent:执行型 agent,负责生成所有初始化文件。

## 相关模板

- `references/agents-md-template.md`: AGENTS.md 生成模板
- `references/docs-skeleton-template.md`: docs/ 目录骨架模板

---
最后更新: 2026-06-29
