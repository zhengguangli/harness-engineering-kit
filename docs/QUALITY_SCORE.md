# QUALITY_SCORE.md

<!-- Canonical owner: harness-golden-principles -->

按领域追踪 harness-engineering-kit 的质量与一致性评分。

## 评分维度

- **frontmatter 合规**: 每个 SKILL.md 是否满足必填字段要求
- **触发回归通过率**: `tests/triggers/cases.json` 中 PASS 的比例
- **关键词一致性**: `scripts/validate-keyword-consistency.sh` 的通过情况
- **文档新鲜度**: docs/ 中关键文档是否在 30 天内被校验过

## 当前评分

| 领域 | frontmatter 合规 | 触发回归 | 关键词一致性 | 文档新鲜度 | 最近评估日期 |
|---|---|---|---|---|---|
| skills (12个) | 待评估 | 待评估 | 待评估 | 待评估 | — |
| scripts | — | — | — | 待评估 | — |
| tests | — | — | — | 待评估 | — |

## 趋势备注

（首次创建，尚无历史数据。运行 `make triggers-all` 后可填充初始评分。）

---
最后更新: 2026-07-01
