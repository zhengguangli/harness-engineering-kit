# QUALITY_SCORE.md

<!-- Canonical owner: harness-golden-principles -->

按领域追踪 harness-engineering-kit 的质量与一致性评分。

## 评分维度

- **frontmatter 合规**: 每个 SKILL.md 是否满足必填字段要求
- **触发回归通过率**: `tests/triggers/cases.json` 中 PASS 的比例
- **关键词一致性**: `scripts/run-trigger-regression.sh` 中关键词覆盖情况
- **文档新鲜度**: docs/ 中关键文档是否在 30 天内被校验过

## 当前评分

| 领域 | frontmatter 合规 | 触发回归 | 关键词一致性 | 文档新鲜度 | 最近评估日期 |
|---|---|---|---|---|---|
| skills (13个) | 13/13 (100%) ✅ | 48/48 (100%) ✅ | 13/13 (100%) ✅ | ✅ 7日内更新 | 2026-07-03 |
| scripts | — | — | — | ✅ 7日内更新 | 2026-07-03 |
| tests | — | — | — | ✅ 7日内更新 | 2026-07-03 |

## 趋势备注

2026-07-03: 初始评分填充。全部 13 个 skill 完成 A+ 级优化（平均分 9.57），`make triggers-all` 全绿通过（PASS=48 WARN=0 FAIL=0）。详见 `AGENTS.md` 和 `docs/quality-reports/skills-quality-improvement-2026-07-02.md`。

---
最后更新: 2026-07-03
