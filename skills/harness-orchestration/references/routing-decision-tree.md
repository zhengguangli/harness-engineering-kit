# Routing Decision Tree（路由决策树参考）

本文件是 `harness-orchestration` 技能的可独立加载参考——将 SKILL.md 中的决策树和交接点提取为 agent 可按需查阅的结构化知识。工作流的详细步骤在 SKILL.md 中,这里只保留 SKILL.md 放不下的扩展内容。

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
    └── 最后在目标项目的架构文档领域表和质量评分表中各加一行（由 `bootstrap` 生成的骨架结构承接）
```

## 交接点表

以下产出物在 skill 之间有明确的"上游产出 → 下游消费"关系:

| 上游 skill | 产出物 | 下游消费者 |
|---|---|---|
| `project-intake` | 结构化项目卡片 | `bootstrap`(用卡片信息生成骨架) |
| `exec-plans` | exec-plan 文件 | `verification-loop`(按计划步骤执行并回写进度) |
| `architecture-boundaries` | lint 规则 / 结构化测试 | `verification-loop`(作为自检项)、`commit-gate`(作为门禁检查) |
| `observability-and-browser` | 截图/录屏/指标查询结果 | `verification-loop`(作为修复依据)、`commit-gate`(作为完成证据) |
| `golden-principles` | 修复队列(偏离模式列表) | `verification-loop`(逐项修复) |
| `repo-map` | AGENTS.md + 文档校验报告 | `bootstrap`(确认骨架完整性)、`authoring`(确认新 skill 已登记) |

## 常见省略

这 12 个 skill 是按需使用的,不是每次都要全走一遍:

- 小项目不需要 `architecture-boundaries`(没有多层架构要守)。
- 纯文档改动不需要 `verification-loop` 和 `observability-and-browser`。
- 已有完善 harness 结构的项目不需要重新走 Workflow 1。
- `authoring` 只在扩展 harness 体系本身时使用,日常开发不需要。

---
最后更新: 2026-06-29
