---
name: harness-orchestration
description: 编排 harness-engineering-kit 中 12 个 skill 的组合与工作流路由——根据用户目标选择正确的 skill 组合和执行顺序,而不是让 agent 在相似技能之间犯选择困难。当用户问"我该用哪些 skill"、"怎么开始用这套 harness"、面对多个 skill 不知如何组合、或进入新项目不知道先做什么后做什么时使用。
version: 0.1.0
---


# Orchestration（技能编排与工作流路由）

## 核心原则

这 12 个 skill 不是孤立的工具箱,而是一条有标准顺序的工作流。**选择正确的 skill 组合比掌握单个 skill 更重要**——单个 skill 内部的方法论再好,如果用错了时机或跳过了前置步骤,效果会大打折扣。

这个 skill 不是一个"可委派出去等结果"的执行任务,而是主对话需要持续记住的路由知识——它帮助 agent 在恰当的时机调用恰当的技能。

## 何时使用

- 用户问"我该用哪些 skill"或"怎么开始用这套 harness"。
- 面对多个 skill 不知如何组合,需要路由决策。
- 进入新项目,不确定先做什么后做什么。
- 复杂任务需要规划多 skill 的协作流程。

## 四条标准工作流

| # | 场景 | 流程 | 何时可省略 |
|---|---|---|---|
| 1 | Greenfield 初始化 | `project-intake` → `bootstrap` → `repo-map` → `architecture-boundaries` + `golden-principles` | 小项目可跳过 `architecture-boundaries` |
| 2 | 日常功能开发 | `exec-plans`(可选) → 实现 → `verification-loop` → `commit-gate` | 简单改动可跳过 `exec-plans` 和 `verification-loop` |
| 3 | 代码质量修复 | `golden-principles` → `architecture-boundaries`(可选) → `verification-loop` → `commit-gate` | 纯品味漂移可跳过 `architecture-boundaries` |
| 4 | 扩展 harness 体系 | `authoring` → `bootstrap`(可选) → `repo-map` | — |
| 5 | 优化 prompt 质量 | `prompt-optimizer`（独立使用，输入用户粗糙描述，输出结构化 prompt） | — |

各工作流的详细步骤、交接点和常见省略场景,见 `references/routing-decision-tree.md`。

## 决策树

详见 `references/routing-decision-tree.md` 中的三层路由判断和完整决策树图。

## 交接点

以下产出物在 skill 之间有明确的"上游产出 → 下游消费"关系:

| 上游 skill | 产出物 | 下游消费者 |
|---|---|---|
| `project-intake` | 结构化项目卡片 | `bootstrap`(用卡片信息生成骨架) |
| `exec-plans` | exec-plan 文件(`docs/exec-plans/active/*.md`) | `verification-loop`(按计划步骤执行并回写进度) |
| `architecture-boundaries` | lint 规则 / 结构化测试 | `verification-loop`(作为自检项)、`commit-gate`(作为门禁检查) |
| `observability-and-browser` | 截图/录屏/指标查询结果 | `verification-loop`(作为修复依据)、`commit-gate`(作为完成证据) |
| `golden-principles` | 修复队列(偏离模式列表) | `verification-loop`(逐项修复) |
| `repo-map` | AGENTS.md + docs/ 校验报告 | `bootstrap`(确认骨架完整性)、`authoring`(确认新 skill 已登记) |
| `prompt-optimizer` | 优化后的结构化 prompt | `authoring`（作为新 skill 的 system prompt 输入）、任何需要高质量 prompt 的 skill/agent |

## 不需要全部启动

这 12 个 skill 是按需使用的,不是每次都要全走一遍。常见省略:

- 小项目不需要 `architecture-boundaries`(没有多层架构要守)。
- 纯文档改动不需要 `verification-loop` 和 `observability-and-browser`。
- 已有完善 harness 结构的项目不需要重新走 Workflow 1。
- `authoring` 只在扩展 harness 体系本身时使用,日常开发不需要。
- `prompt-optimizer` 只在需要优化提示词时使用，日常开发不需要。

## 配合的 agent

- `orchestrator` agent:只读的路由顾问,为主对话推荐 skill 组合和执行顺序,不独立执行任务。编排逻辑也可由主对话根据本文件的路由知识直接执行。

## 相关模板

- `references/routing-decision-tree.md`: 路由决策树与四条标准工作流（可独立加载的参考文件）

---
最后更新: 2026-06-30
