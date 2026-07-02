# 技术债追踪

已知但暂不处理的技术债。每条记录应说明：是什么、为什么不现在处理、什么条件下应该处理。

## 当前列表

| ID | 描述 | 发现日期 | 优先级 | 处理条件 |
|---|---|---|---|---|
| TD-001 | skill 间循环依赖未被脚本机械强制，仅靠人工 review | 2026-07-01 | Medium | 当 skill 数量增长到 15+ 或出现实际循环时 |
| TD-002 | openai.yaml 的 system_prompt 字段仍引用旧的 agent 提示词内容，需与 SKILL.md 中的 `## Agent 提示词` section 同步 | 2026-07-02 | Low | 当 Codex 平台需要使用 agent 提示词时 |
| TD-003 | 12 skills 五维审计发现 20 条 LOW 级建议（标点/文案/次级措辞），完整清单见 `docs/exec-plans/completed/skills-audit-2026-07-02.md` | 2026-07-02 | **已完成** | Round 2（`skills-optimization-2026-07-02-round2.md`）17 条已落地，3 条与 CRITICAL/MEDIUM 合并处理 |

---
最后更新: 2026-07-02

## TD-003 详细清单

已全部完成（Round 2，`skills-optimization-2026-07-02-round2.md`），清单已归档至 `docs/exec-plans/completed/skills-audit-2026-07-02.md`。
