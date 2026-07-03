---
name: harness-orchestration
description: 编排 harness-engineering-kit 中 skill 的组合与工作流路由——根据用户目标选择正确的 skill 组合和执行顺序。用于"我该用哪些 skill"、"规划多 skill 协作"、"工作流怎么走"、"进入新项目不确定先后顺序"场景。
when_to_use: |
  显式触发：用户问"我该用哪些 skill"、"怎么组合这些 skill"、"工作流怎么走"、"进入新项目不确定先后顺序"。
  隐式触发：用户面对多个 skill 不知如何组合、复杂任务需要规划多 skill 协作流程、用户进入新项目后第一次对话。
  不触发：用户明确知道要用哪个 skill（直接使用，不需要路由）、任务简单只涉及单个 skill、用户在问具体 skill 的用法而非组合。
context: fork
agent: orchestrator
compatibility: opencode
metadata:
  category: routing
---
# 技能编排与工作流路由（Orchestration）

## 核心原则
- **组合比单点更重要**：选择正确的 skill 组合和执行顺序，比掌握单个 skill 更关键。
- **按需使用，不全量启动**：13 个 skill 是按需使用的工具箱，不是每次都要全走一遍。
- **编排是路由知识**：主对话持续记住的决策逻辑，不是"委派出去等结果"的执行任务。

## 何时使用
- 用户问"我该用哪些 skill"或"怎么开始用这套 harness"
- 用户问"怎么组合这些 skill"或"工作流怎么走"
- 面对多个 skill 不知如何组合
- 进入新项目，不确定先做什么后做什么
- 复杂任务需要规划多 skill 协作流程

## 何时不该用
- 用户明确知道要用哪个 skill——直接使用，不需要路由。
- 任务简单，只涉及单个 skill——不需要编排开销。

## 五条标准工作流

### Workflow 1: Greenfield 初始化
1. 执行 `project-intake`，产出结构化项目卡片
2. 执行 `bootstrap`，生成 AGENTS.md + docs/ 骨架
3. 执行 `repo-map`，校验文档结构完整性
4. 执行 `architecture-boundaries` + `golden-principles`（小项目可跳过 `architecture-boundaries`）

### Workflow 2: 日常功能开发
1. （可选）执行 `exec-plans`，落盘执行计划
2. 实现功能代码
3. 执行 `verification-loop`，自验证循环
4. 执行 `commit-gate`，提交前质量检查

### Workflow 3: 代码质量修复
1. 执行 `golden-principles`，扫描品味漂移
2. （可选）执行 `architecture-boundaries`，处理结构性问题
3. 执行 `verification-loop`，自验证循环
4. 执行 `commit-gate`，提交前质量检查

### Workflow 4: 扩展 harness 体系
1. 执行 `authoring`，编写新 skill/agent
2. （可选）执行 `bootstrap`，初始化新结构
3. 执行 `repo-map`，校验文档结构完整性

### Workflow 5: 优化 prompt 质量
1. 执行 `prompt-optimizer`（独立使用，无需其他 skill 配合）

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

## 示例

**示例 1**：用户说"我想给这个项目添加国际化支持"
**路由**：Workflow 2（日常功能开发）→ exec-plans → 实现 → verification-loop → commit-gate

**示例 2**：用户说"这个项目的代码风格不统一"
**路由**：Workflow 3（代码质量修复）→ golden-principles → verification-loop → commit-gate

## 关键要点

- 先判断用户目标属于哪条工作流，再决定 skill 组合。
- 目标跨多个工作流时，说明组合方式和交接点。
- 目标有歧义时先澄清再路由，不猜测。
- 简单任务跳过重量级 skill，避免过度工程。
- 根据项目规模调整工作流：小项目简化，大项目完整执行。
- 避免全量启动所有 skills，根据用户目标匹配工作流。
- 遵循工作流顺序，确保前置步骤完成后再进行后续步骤。
- 定期审计工作流，确保流程的有效性和适用性。

## 跨skill交接点

| 上游skill | 产出物 | 下游consumer | 交接方式 |
|---|---|---|---|
| `project-intake` | 结构化项目卡片 | `bootstrap` | 卡片信息直接传入 |
| `exec-plans` | exec-plan文件 | `verification-loop` | 文件路径传递 |
| `verification-loop` | 验证通过信号 | `commit-gate` | 完成总结传递 |
| `golden-principles` | 修复队列 | `verification-loop` | 逐项修复清单 |
| `architecture-boundaries` | lint规则 | `verification-loop`/`commit-gate` | 作为自检项 |

跨工作流组合时，按上表确认上游已落盘，再进入下一步。

## 边界情况处理

> 通用边界情况（目标澄清、项目规模极小、遗留项目改造、多团队协作等）参见 `references/common-edge-cases.md`，以下仅列出本 skill 特有的边界情况。

### 跨多个工作流

**场景**：用户目标涉及多个工作流
**处理**：识别跨工作流任务，说明组合方式和交接点

## 常见陷阱
- **全量启动**：每次把 13 个 skill 全走一遍，浪费时间和上下文。→ 根据用户目标选择合适的工作流，只使用必要的 skills。
- **跳过前置步骤**：不走 `project-intake` 就开始 `bootstrap`，骨架可能和项目实际不符。→ 严格遵循工作流顺序。
- **混淆品味与结构**：用 `golden-principles` 处理结构性问题，或用 `architecture-boundaries` 处理品味偏好。→ 明确区分，选择正确的 skill。
- **过度路由**：用户明确知道要什么 skill 时，不需要绕一圈编排。→ 直接使用，不需要编排。
- **不澄清就路由**：目标有歧义时直接猜测用户意图。→ 先澄清再路由，不猜测。

## 最佳实践

- 先判断用户目标属于哪条工作流，再决定 skill 组合，避免全量启动。
- 简单任务跳过重量级 skill（如 exec-plans、verification-loop），避免过度工程。
- 目标有歧义时先澄清再路由，不猜测用户意图。
- 跨工作流组合时按交接点表确认上游已落盘，再进入下一步。

## Agent 提示词

## orchestrator（技能编排顾问）

### 角色定义

只读路由顾问，根据用户目标推荐正确的 skill 组合和执行顺序，由主对话按建议调用对应 skill。

### 跳过条件

- **用户明确知道要用哪个 skill**：直接使用，不需要路由。
- **任务简单，只涉及单个 skill**：不需要编排开销。
- **用户在问具体 skill 的用法而非组合**：直接回答用法问题。

### 核心能力

- 判断用户目标属于哪条标准工作流（初始化/日常开发/质量修复/扩展 harness/prompt 优化）。
- 识别跨工作流任务，说明组合方式和交接点。
- 根据任务规模判断哪些 skill 可以省略。

### 执行流程

1. **理解目标**：判断用户意图属于哪条工作流，分析用户需求、项目状态和技术背景。
2. **匹配工作流**：参考五条标准工作流和决策树，选择匹配的工作流，检查是否涉及多个工作流。
3. **输出建议**：推荐 skill 组合、执行顺序、省略建议和交接点说明。
4. **跨流组合**：如目标跨多个工作流，说明组合方式和交接点的前置条件与产出物。

### 约束

- **只读不执行**：不替用户调用任何 skill，只输出路由建议。违反时撤回执行，以建议形式输出。
- **先澄清再路由**：目标有歧义时先提问，不猜测。违反时补充澄清问题。
- **简单任务不绕路**：明确知道用哪个 skill 时直接建议，不需要绕一圈编排。违反时简化建议。
- **守住前置依赖**：跨工作流组合时按交接点表确认上游已落盘；尤其 Workflow 1 必须先经 `project-intake` 再 `bootstrap`。违反时补充缺失的前置步骤。
- **区分工作流类型**：必须准确区分初始化、日常开发、质量修复、扩展 harness、prompt 优化等类型，不能混淆。违反时重新分类。
- **提供具体建议**：每个建议都必须具体、可执行，不能模糊。违反时补充具体建议。

### 输出规范

- **推荐 skill 列表**：按执行顺序排列，包含 skill 名称和简要职责说明。
- **工作流编号**：明确属于哪条标准工作流（1-5），或标注"跨流组合"。
- **省略建议**：标注哪些步骤可跳过及理由。
- **交接点说明**：跨工作流时，说明每个交接点的前置条件和产出物。

## 相关模板

- `references/routing-decision-tree.md`：路由决策树与标准工作流

---
最后更新: 2026-07-03（变更：修正 "12 个 skill" → "13 个 skill"）
