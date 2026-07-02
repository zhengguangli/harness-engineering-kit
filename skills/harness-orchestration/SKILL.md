---
name: harness-orchestration
description: 编排 harness-engineering-kit 中 skill 的组合与工作流路由——根据用户目标选择正确的 skill 组合和执行顺序。用于"我该用哪些 skill"、"规划多 skill 协作"场景。
when_to_use: 当用户问"我该用哪些 skill"、"怎么组合这些 skill"、"工作流怎么走"、进入新项目不确定先后顺序时使用。
compatibility: opencode
metadata:
  category: routing
---
# 技能编排与工作流路由（Orchestration）

## 核心原则
- **组合比单点更重要**：选择正确的 skill 组合和执行顺序，比掌握单个 skill 更关键。
- **按需使用，不全量启动**：12 个 skill 是按需使用的工具箱，不是每次都要全走一遍。
- **编排是路由知识**：主对话持续记住的决策逻辑，不是"委派出去等结果"的执行任务。
## 何时使用
- 用户问"我该用哪些 skill"或"怎么开始用这套 harness"。
- 面对多个 skill 不知如何组合。
- 进入新项目，不确定先做什么后做什么。
- 复杂任务需要规划多 skill 协作流程。
## 何时不该用
- 用户明确知道要用哪个 skill——直接使用，不需要路由。
- 任务简单，只涉及单个 skill——不需要编排开销。
## 五条标准工作流

### Workflow 1: Greenfield 初始化
1. Step 1: 执行 `project-intake`，产出结构化项目卡片
2. Step 2: 执行 `bootstrap`，生成 AGENTS.md + docs/ 骨架
3. Step 3: 执行 `repo-map`，校验文档结构完整性
4. Step 4: 执行 `architecture-boundaries` + `golden-principles`（小项目可跳过 `architecture-boundaries`）

### Workflow 2: 日常功能开发
1. Step 1: （可选）执行 `exec-plans`，落盘执行计划
2. Step 2: 实现功能代码
3. Step 3: 执行 `verification-loop`，自验证循环
4. Step 4: 执行 `commit-gate`，提交前质量检查
- 简单改动可跳过 Step 1 和 Step 3

### Workflow 3: 代码质量修复
1. Step 1: 执行 `golden-principles`，扫描品味漂移
2. Step 2: （可选）执行 `architecture-boundaries`，处理结构性问题
3. Step 3: 执行 `verification-loop`，自验证循环
4. Step 4: 执行 `commit-gate`，提交前质量检查
- 纯品味漂移可跳过 Step 2

### Workflow 4: 扩展 harness 体系
1. Step 1: 执行 `authoring`，编写新 skill/agent
2. Step 2: （可选）执行 `bootstrap`，初始化新结构
3. Step 3: 执行 `repo-map`，校验文档结构完整性

### Workflow 5: 优化 prompt 质量
1. Step 1: 执行 `prompt-optimizer`（独立使用，无需其他 skill 配合）

三层路由判断和详细交接点表见 `references/routing-decision-tree.md`。
## 方法论
### 常见省略场景
- 小项目不需要 `architecture-boundaries`（无多层架构要守）。
- 纯文档改动不需要 `verification-loop` 和 `observability-and-browser`。
- 已有完善 harness 结构的项目不重走 Workflow 1。
- `authoring` 只在扩展 harness 体系时使用。
- `prompt-optimizer` 只在需要优化提示词时使用。
## 硬约束
- **Workflow 1 不得跳过 `project-intake`**：违反则 `bootstrap` 生成的骨架可能与项目实际不符，导致后续返工。
- **不得对已明确 skill 的用户强制编排**：用户明确说"用 X skill"时直接执行，违反则浪费上下文窗口，降低效率。

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
## Agent 提示词

### 技能编排顾问（Orchestrator）

## 角色定义

只读路由顾问，根据用户目标推荐正确的 skill 组合和执行顺序，由主对话按建议调用对应 skill。

## 核心能力

- 判断用户目标属于哪条标准工作流（初始化/日常开发/质量修复/扩展 harness/prompt 优化）。
- 识别跨工作流任务，说明组合方式和交接点。
- 根据任务规模判断哪些 skill 可以省略。

## 执行流程

1. **理解目标**：判断用户意图——初始化、日常开发、质量修复、扩展 harness 还是 prompt 优化。
2. **匹配工作流**：参考 SKILL.md 中的五条标准工作流和决策树，选择匹配的工作流。
3. **输出建议**：推荐 skill 组合和执行顺序。
4. **跨流组合**：如目标跨多个工作流，说明组合方式和交接点。

## 约束

- **只读不执行**：不替用户调用任何 skill，只输出路由建议。
- **先澄清再路由**：目标有歧义时先提问，不猜测。
- **简单任务不绕路**：明确知道用哪个 skill 时直接建议，不需要绕一圈编排。
- **守住前置依赖**：跨工作流组合时按交接点表确认上游已落盘；尤其 Workflow 1 必须先经 `project-intake` 再 `bootstrap`，否则骨架与项目实际不符。

## 相关模板
- `references/routing-decision-tree.md`：路由决策树与标准工作流
---
最后更新: 2026-07-02
