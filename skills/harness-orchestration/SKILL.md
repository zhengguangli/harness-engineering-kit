---
name: harness-orchestration
description: 编排 harness-engineering-kit 中 skill 的组合与工作流路由——根据用户目标选择正确的 skill 组合和执行顺序。
version: 0.1.0
---
# 技能编排与工作流路由（Orchestration）
## 触发信号

### 显式触发（explicit）
- `harness-orchestration`
- `编排`
- `路由`
- `我该用哪些 skill`

### 语义意图（intent）
- 不知道该用哪些 skill
- 需要规划多 skill 协作顺序
- 进入新项目不确定先做什么
- 目标跨多个工作流，需要组合与交接设计

### 证据触发（artifacts）
- `routing-decision-tree.md`
- `workflow`
- `skill`
- `bootstrap`
- `verification-loop`

### 避免触发（avoid_when）
- 用户已明确指定 skill
- 任务只涉及单个 skill

## 核心原则
- **组合比单点更重要**：选择正确的 skill 组合和执行顺序，比掌握单个 skill 更关键。单个 skill 方法论再好，用错时机或跳过前置步骤效果大打折扣。
- **按需使用，不全量启动**：12 个 skill 是按需使用的工具箱，不是每次都要全走一遍。
- **编排是路由知识**：主对话持续记住的决策逻辑，不是"委派出去等结果"的执行任务。
## 前置步骤（建议）

- 先扫描当前环境实际可用的 `skills/` 列表，再做路由；不要假设仓库固定拥有全部 12 个 skill。

## 何时使用
- 用户问"我该用哪些 skill"或"怎么开始用这套 harness"。
- 面对多个 skill 不知如何组合。
- 进入新项目，不确定先做什么后做什么。
- 复杂任务需要规划多 skill 协作流程。
## 何时不该用
- 用户明确知道要用哪个 skill——直接使用，不需要路由。
- 任务简单，只涉及单个 skill——不需要编排开销。
## 四条标准工作流

| # | 场景 | 流程 | 可省略条件 |
|---|---|---|---|
| 1 | Greenfield 初始化 | `project-intake` → `bootstrap` → `repo-map` → `architecture-boundaries` + `golden-principles` | 小项目可跳过 `architecture-boundaries` |
| 2 | 日常功能开发 | `exec-plans`(可选) → 实现 → `verification-loop` → `commit-gate` | 简单改动可跳过 `exec-plans` 和 `verification-loop` |
| 3 | 代码质量修复 | `golden-principles` → `architecture-boundaries`(可选) → `verification-loop` → `commit-gate` | 纯品味漂移可跳过 `architecture-boundaries` |
| 4 | 扩展 harness 体系 | `authoring` → `bootstrap`(可选) → `repo-map` | — |
| 5 | 优化 prompt 质量 | `prompt-optimizer`（独立使用） | — |

详细步骤和决策树见 `references/routing-decision-tree.md`。
## 方法论
### 交接点（上游产出 → 下游消费）

| 上游 skill | 产出物 | 下游消费者 |
|---|---|---|
| `project-intake` | 结构化项目卡片 | `bootstrap` |
| `exec-plans` | exec-plan 文件 | `verification-loop` |
| `architecture-boundaries` | lint 规则/结构化测试 | `verification-loop`、`commit-gate` |
| `observability-and-browser` | 截图/指标查询结果 | `verification-loop`、`commit-gate` |
| `golden-principles` | 修复队列 | `verification-loop` |
| `repo-map` | AGENTS.md + docs/ 校验报告 | `bootstrap`、`authoring` |
| `prompt-optimizer` | 结构化 prompt | `authoring`、其他需要高质量 prompt 的 skill |

### 常见省略场景
- 小项目不需要 `architecture-boundaries`（无多层架构要守）。
- 纯文档改动不需要 `verification-loop` 和 `observability-and-browser`。
- 已有完善 harness 结构的项目不重走 Workflow 1。
- `authoring` 只在扩展 harness 体系时使用。
- `prompt-optimizer` 只在需要优化提示词时使用。
## 关键要点
- 先判断用户目标属于哪条工作流，再决定 skill 组合。
- 目标跨多个工作流时，说明组合方式和交接点。
- 目标有歧义时先澄清再路由，不猜测。
- 简单任务跳过重量级 skill，避免过度工程。
## 常见陷阱
- **全量启动**：每次把 12 个 skill 全走一遍，浪费时间和上下文。
- **跳过前置步骤**：不走 `project-intake` 就开始 `bootstrap`，骨架可能和项目实际不符。
- **混淆品味与结构**：用 `golden-principles` 处理结构性问题，或用 `architecture-boundaries` 处理品味偏好。
- **过度路由**：用户明确知道要什么 skill 时，不需要绕一圈编排。
## 配合的 agent
- `orchestrator`：只读路由顾问，为主对话推荐 skill 组合和执行顺序。编排逻辑也可由主对话直接执行。
## 相关模板
- `references/routing-decision-tree.md`：路由决策树与标准工作流
---
最后更新: 2026-06-30
