# Routing Decision Tree（路由决策树参考）

本文件是 `harness-orchestration` 技能的可独立加载参考——将 SKILL.md 中的决策树和标准工作流提取为 agent 可按需查阅的结构化知识。orchestrator agent 在需要精确路由判断时加载此文件,不必将全部 SKILL.md 内容注入上下文。

## 三层路由判断

面对一个任务时,用以下 3 层判断快速路由:

```
用户要什么?
├── 初始化/新项目 → Workflow 1
├── 写代码/改代码 → Workflow 2
│   ├── 任务复杂度?
│   │   ├── 简单(单次可完成) → 跳过 exec-plans,直接 verification-loop + commit-gate
│   │   └── 复杂(跨会话) → exec-plans → verification-loop → commit-gate
│   └── 涉及 UI/性能?
│       └── 是 → verification-loop 内触发 observability-and-browser
├── 修质量/清扫 → Workflow 3
│   ├── 纯品味漂移 → golden-principles → verification-loop → commit-gate
│   └── 结构性违规 → golden-principles + architecture-boundaries → verification-loop → commit-gate
└── 给 harness 加能力 → Workflow 4
```

## 四条标准工作流

### Workflow 1: Greenfield 初始化

适用场景:新项目首次接入 harness 体系。

```
project-intake  →  bootstrap  →  repo-map  →  architecture-boundaries + golden-principles
(分析项目)       (生成骨架)    (建立地图)    (确立规则)
```

- `project-intake` 产出结构化项目卡片,`bootstrap` 依赖这些信息生成 AGENTS.md 和 docs/ 骨架。
- `repo-map` 在骨架生成后校验地图是否完整、指针是否准确。
- `architecture-boundaries` 和 `golden-principles` 可以并行:前者确立结构性红线,后者编码品味规则。
- 如果项目规模很小(单文件脚本、简单工具),可以跳过 `architecture-boundaries`,只用 `golden-principles` 即可。

### Workflow 2: 日常功能开发

适用场景:在已有 harness 结构的项目里写代码、改代码。

```
exec-plans(可选)  →  实现  →  verification-loop  →  commit-gate
(计划)             (写代码)   (自验证循环)           (提交质量门)
```

- `exec-plans` 按复杂度决定是否使用:单次会话能做完的小改动用临时轻量计划,跨会话/跨窗口的复杂工作必须用 exec-plan。
- `verification-loop` 是核心循环:实现→自检→测试→评审→修复,直到收敛。
- `observability-and-browser` 作为 `verification-loop` 的传感器被调用——需要 UI 验证或性能确认时,它产出证据,不需要单独触发。
- `commit-gate` 是最终关口:diff 审查 + 自动化验证 + commit message 格式化。
- 如果任务很简单(改一行配置、修个 typo),可以跳过 `exec-plans` 和 `verification-loop`,直接走 `commit-gate`。

### Workflow 3: 代码质量修复

适用场景:发现代码漂移、重复模式、架构违规,需要系统性修复。

```
golden-principles(发现漂移)  →  architecture-boundaries(确认边界)  →  verification-loop(修复循环)  →  commit-gate
```

- `golden-principles` 的 `entropy-collector` agent 扫描出偏离的模式,生成修复队列。
- `architecture-boundaries` 的 `boundary-auditor` agent 确认是否存在结构性违规(依赖方向、层间越界)。
- 两者结果合并后进入 `verification-loop` 逐项修复。
- `commit-gate` 确保修复本身没有引入新问题。
- 如果漂移是纯品味层面的(命名不一致、复用不足),可以只走 `golden-principles` → `verification-loop` → `commit-gate`,跳过 `architecture-boundaries`。

### Workflow 4: 扩展 harness 体系

适用场景:给 harness 工具集本身添加新能力。

```
authoring(设计新 skill)  →  bootstrap(如涉及新项目结构)  →  repo-map(更新地图)
```

- `authoring` 指导如何写 SKILL.md、选择 skill vs subagent、控制上下文预算。
- 如果新 skill 需要改变目标项目的 docs/ 结构,用 `bootstrap` 的模板补全。
- 最后用 `repo-map` 更新 AGENTS.md 导航表,确保地图反映最新状态。
- 新增的 skill 要在 `docs/ARCHITECTURE.md` 领域表和 `docs/QUALITY_SCORE.md` 评分表中各加一行。

## 交接点表

以下产出物在 skill 之间有明确的"上游产出 → 下游消费"关系:

| 上游 skill | 产出物 | 下游消费者 |
|---|---|---|
| `project-intake` | 结构化项目卡片 | `bootstrap`(用卡片信息生成骨架) |
| `exec-plans` | exec-plan 文件(`docs/exec-plans/active/*.md`) | `verification-loop`(按计划步骤执行并回写进度) |
| `architecture-boundaries` | lint 规则 / 结构化测试 | `verification-loop`(作为自检项)、`commit-gate`(作为门禁检查) |
| `observability-and-browser` | 截图/录屏/指标查询结果 | `verification-loop`(作为修复依据)、`commit-gate`(作为完成证据) |
| `golden-principles` | 修复队列(偏离模式列表) | `verification-loop`(逐项修复) |
| `repo-map` | AGENTS.md + docs/ 校验报告 | `bootstrap`(确认骨架完整性)、`authoring`(确认新 skill 已登记) |

## 常见省略

这 11 个 skill 是按需使用的,不是每次都要全走一遍:

- 小项目不需要 `architecture-boundaries`(没有多层架构要守)。
- 纯文档改动不需要 `verification-loop` 和 `observability-and-browser`。
- 已有完善 harness 结构的项目不需要重新走 Workflow 1。
- `authoring` 只在扩展 harness 体系本身时使用,日常开发不需要。

---
最后更新: 2026-06-29
