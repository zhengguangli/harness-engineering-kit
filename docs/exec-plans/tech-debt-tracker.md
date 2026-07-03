# 技术债追踪

已知但暂不处理的技术债。每条记录应说明：是什么、为什么不现在处理、什么条件下应该处理。

## 当前列表

| ID | 描述 | 发现日期 | 优先级 | 处理条件 |
|---|---|---|---|---|
| TD-001 | skill 间循环依赖未被脚本机械强制，仅靠人工 review | 2026-07-01 | Medium | 当 skill 数量增长到 15+ 或出现实际循环时 |
| TD-002 | openai.yaml 的 system_prompt 字段仍引用旧的 agent 提示词内容，需与 SKILL.md 中的 `## Agent 提示词` section 同步 | 2026-07-02 | **已完成** | Codex 平台不再支持，openai.yaml 已全部删除 |
| TD-003 | 12 skills 五维审计发现 20 条 LOW 级建议（标点/文案/次级措辞），完整清单见 `docs/exec-plans/completed/skills-audit-2026-07-02.md` | 2026-07-02 | **已完成** | Round 2（`skills-optimization-2026-07-02-round2.md`）17 条已落地，3 条与 CRITICAL/MEDIUM 合并处理 |
| TD-004 | skills 质量评估发现触发条件描述不够具体、使用示例不足、错误处理指导不足 | 2026-07-02 | **已完成** | 三轮评估优化已完成，5个skills优化，平均提升+0.39分 |
| TD-005 | 13个skills全量A+级优化，从B/B+/A级提升至A+级 | 2026-07-02 | **已完成** | 全量优化完成，所有skills达到A+级（9.5-10分），平均提升+0.82分 |

---
最后更新: 2026-07-02（变更：添加TD-005，13个skills全量A+级优化完成）

## TD-003 详细清单

已全部完成（Round 2，`skills-optimization-2026-07-02-round2.md`），清单已归档至 `docs/exec-plans/completed/skills-audit-2026-07-02.md`。
