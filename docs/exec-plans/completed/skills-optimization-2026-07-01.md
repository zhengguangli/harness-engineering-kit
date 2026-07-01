# Skills 技能包批量优化

- 状态: completed
- 创建日期: 2026-07-01
- 最近更新: 2026-07-01
- 关联 PR / issue: 暂无
- 负责 agent / 人: opencode

## 目标

12 个 harness skills 全部通过质量评估（overall score ≥ 4），且触发精度（trigger_precision）≥ 4，确保 agent 能可靠识别何时使用哪个 skill。

## 范围 / 非目标

**范围内:**
- 评估全部 12 个 skills 的质量
- 优化 description / when_to_use 的触发精度
- 拆分超 500 行的 body 到 references/
- 补齐缺失的"最后更新"日期
- 优化约束的可执行性（添加违反后果）

**明确不做(非目标):**
- 不重写 skills 的核心方法论
- 不创建新的 skills
- 不修改 agent 的工具权限（除非发现明显违反最小权限原则）

## 步骤

- [x] 步骤 1 — 并行评估全部 12 个 skills，产出基线分数
- [x] 步骤 2 — 根据评估结果，按优先级分组（P0: score ≤ 2, P1: score = 3, P2: score ≥ 4 无需优化）
- [x] 步骤 3 — 并行执行 P0 组优化（预计 3-4 个 agent）
- [x] 步骤 4 — 并行执行 P1 组优化（预计 4-5 个 agent）
- [x] 步骤 5 — 验证优化结果：重新评估，确认全部 score ≥ 4
- [ ] 步骤 6 — 移动文件到 completed/

## 决策日志

| 日期 | 决策 | 理由 | 被否决的备选方案 |
|---|---|---|---|
| 2026-07-01 | 使用多 agent 并行执行 | 12 个 skills 串行优化耗时过长 | 逐个串行优化 |

## 验收标准

- [x] 全部 12 个 skills 的 overall score ≥ 4
- [x] 全部 12 个 skills 的 trigger_precision ≥ 4
- [x] 无 skill body 超过 500 行
- [x] 全部 skills 底部有"最后更新"日期

## 风险 / 已知未知

- 部分 skills 可能没有对应的 agent prompt，跨平台同步检查会跳过
- 优化可能影响 skills 之间的依赖关系，需要验证无循环依赖

## 优化结果

| Skill | 优化前 | 优化后 | 主要改进 |
|---|---|---|---|
| harness-golden-principles | 3 | 5 | +触发精度(口语化短语) +硬约束(5条) |
| harness-commit-gate | 4 | 5 | +硬约束(3条) |
| harness-exec-plans | 4 | 5 | +硬约束(3条) |
| harness-observability-and-browser | 4 | 5 | +执行清晰度(决策分支) +硬约束(2条) |
| harness-orchestration | 4 | 5 | +执行清晰度(编号步骤) +硬约束(2条) |
| harness-project-intake | 4 | 5 | +硬约束(3条) +fallback说明 |
| harness-prompt-optimizer | 4 | 5 | +硬约束(3条) |
| harness-repo-map | 4 | 4 | +硬约束(3条) |
| harness-verification-loop | 4 | 5 | +硬约束(3条) |
| harness-architecture-boundaries | 5 | 5 | 无需优化 |
| harness-authoring | 5 | 5 | 无需优化 |
| harness-bootstrap | 5 | 5 | 无需优化 |

## 变更记录

- 2026-07-01: 创建计划
- 2026-07-01: 完成全部优化，11个skills达到5分，1个达到4分
