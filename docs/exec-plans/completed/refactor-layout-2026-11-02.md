# R1 逻辑分区重构（已完成归档）

- **Status**: completed（2026-11-02，commit `6d3037a`..`0020936`）
- **Spec**: `docs/superpowers/specs/2026-11-02-refactor-layout-design.md`
- **Last updated**: 2026-11-18（归档压缩：按 `core-beliefs.md` #9 保留完成摘要、关键决策与验证结果）

## Accomplished

1. **诊断区下沉至 `scripts/diagnostics/`**：使用 `git mv` 将 `compare_matchers.py`、`compare_matchers_holdout.py`、`evaluate_trigger_discrimination.py` 与 `cases.diagnostic.json` 移入 `scripts/diagnostics/`，并将 3 个脚本的仓库根定位从 `os.getcwd()` 改为 `__file__` 三级上溯。
2. **维护者文档归位至 `docs/references/`**：将 README 中的校验工具与回归用例维护指南拆出至 `docs/references/validation-checks.md` 和 `docs/references/regression-case-guide.md`，README 保留产品面并留一行指路。
3. **建立「产品区 vs 工程区」分区叙事与门禁面定义**：更新 `AGENTS.md`、`docs/ARCHITECTURE.md`、`docs/product-specs/index.md`、`docs/exec-plans/tech-debt-tracker.md`、`docs/exec-plans/active/quality-measurement-program.md` 与 `CHANGELOG.md`。

## Key Decisions

- 选择 R1 逻辑分区（`scripts/diagnostics/`）而非 R2 顶层 `eng/` 重组，避免改动 `skills/` 对外契约、CI 命令与仓库根定位逻辑。
- `docs/QUALITY_SCORE.md` 保持原位，避免破坏 4 个 skill 中引用该路径作为目标项目约定位置的契约。
- 明确门禁面 = `scripts/*.py`（顶层，含 `lib/`）+ `tests/**/test_*.py` + `tests/triggers/cases.json`；`scripts/diagnostics/` 不参与门禁（TD-006）。

## Verification

- `python3 scripts/run-all.py` 六阶段全绿，门禁行为零变更。
- `scripts/diagnostics/evaluate_trigger_discrimination.py` 与 `compare_matchers*.py` 可在任意工作目录运行。
