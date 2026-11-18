# Skill Authoring & Contract Guide（内部维护参考）

本文件沉淀原 `harness-authoring` 与 `harness-skill-quality-assessor` 的内部维护契约，供修改或新增 `skills/harness-*/` 时参考。自 2026-11-18 起，这两项不再作为对外分发的 skill，规范由 `scripts/run-all.py` 与各 skill 的 `automated_check_script.py` 机械强制。

## 1. 精简契约结构（目标 80–120 行，硬上限 150 行）

强模型已内化通用编码与分步教学，保留在 `SKILL.md` 的仅限**硬约束、跳过边界、输出契约与模板指针**。所有 `SKILL.md` 遵循以下 6 节规范顺序：

1. `## Scope & Skip Conditions`（Use when / Skip when）
2. `## Hard Constraints`（编号列表，每条须写明 Violation 后果）
3. `## Related Skills`（须使用 `input` / `output` / `routes-to` / `see-also` 四标签）
4. `## Related Templates`（指向 `references/` 下的模板或跨 skill 引用）
5. `## Agent 提示词`（含 `## <agent-slug> (<Role>)` 及 3 个子节：`### Role & Execution Contract`、`### Constraints`、`### Output Specification`）
6. 文末 `Last updated: YYYY-MM-DD (...)`

## 2. Frontmatter 硬契约

- 必填：`name`、`description`（≥20 字符）、`when_to_use`（含 `显式触发：` / `隐式触发：` / `不触发：`）、`context: fork`、`agent`、`compatibility`、`depends_on`（无数据依赖写 `[]`）、`allowed-tools`、`metadata.category`。
- 禁止废弃字段 `version` 与旧章节 `## 触发信号`。
- `allowed-tools` 遵循最小权限，且必须覆盖执行流中实际引用的所有命令/工具。

## 3. 新增或修改 Skill 同步清单

1. `docs/ARCHITECTURE.md` — 更新分层图与 `Last updated`。
2. `scripts/validate_skill_dependencies.py` — 登记 `LAYERS` 或 `META_LAYER`。
3. `scripts/run_trigger_regression.py` & `tests/triggers/cases.json` — 更新 `SKILL_KW` 并新增用例（保持 `TriggerContractConsistencyTests` 0 漂移）。
4. `tests/tasks/tasks.json` & `scripts/audit_task_coverage.py` — 补充代表性任务与 `REQUIRES` 映射。
5. 提交前运行 `python3 scripts/run-all.py` 与各 skill `automated_check_script.py` 全绿。

---
Last updated: 2026-11-18 (Change: distilled from retired harness-authoring and harness-skill-quality-assessor skills into internal maintainer reference)
