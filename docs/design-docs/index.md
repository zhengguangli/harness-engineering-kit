# 设计文档索引

记录每篇设计文档的位置、当前校验状态和最近校验日期。

| 文档 | 主题 | 校验状态 | 最近校验日期 |
|---|---|---|---|
| `core-beliefs.md` | agent-first 的核心运作信念 | ✅ 已校验 | 2026-09-24 |
| `agent-prompt-inline-migration.md` | Agent 提示词内联迁移模式 | ✅ 已校验 | 2026-09-24 |
| `bash-to-python-migration.md` | Bash 到 Python 3 跨平台迁移设计 | ✅ 已校验 | 2026-09-24 |

校验状态说明:
- ✅ 已校验: 最近确认过和代码现状一致
- ⚠️ 待校验: 超过 30 天未确认，可能已过期
- ❌ 已知过期: 确认和代码现状不一致，等待修复

---
最后更新: 2026-09-24（变更：三篇设计文档已实际复核并与代码现状核对——core-beliefs 的 7 条信念仍成立；agent-prompt-inline-migration 的 agents/ 目录确已消除（悬空引用已修）；bash-to-python-migration 确认无 .sh 残留。校验日期如实更新）
