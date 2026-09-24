# 技术债追踪

已知但暂不处理的技术债。每条记录应说明：是什么、为什么不现在处理、什么条件下应该处理。

## 当前列表

| ID | 描述 | 发现日期 | 优先级 | 处理条件 |
|---|---|---|---|---|
| TD-001 | skill 间循环依赖未被脚本机械强制，仅靠人工 review | 2026-07-01 | **已完成** | 2026-09-23 关闭：新增 `depends_on` frontmatter 契约 + `scripts/validate_skill_dependencies.py` （环检测 / 向下流动 / Meta 隔离 / 引用有效性 / 跨 skill 路径存在性），接入 `run-all.py` 第四阶段，配 18 个回归用例。详见 `docs/ARCHITECTURE.md` 的 Declaring a dependency 小节。 |
| TD-002 | openai.yaml 的 system_prompt 字段仍引用旧的 agent 提示词内容，需与 SKILL.md 中的 `## Agent 提示词` section 同步 | 2026-07-02 | **已完成** | Codex 平台不再支持，openai.yaml 已全部删除 |
| TD-003 | 12 skills 五维审计发现 20 条 LOW 级建议（标点/文案/次级措辞），完整清单见本文的详细清单章节 | 2026-07-02 | **已完成** | Round 2（`skills-optimization-2026-07-02-round2.md`）17 条已落地，3 条与 CRITICAL/MEDIUM 合并处理 |
| TD-004 | skills 质量评估发现触发条件描述不够具体、使用示例不足、错误处理指导不足 | 2026-07-02 | **已完成** | 三轮评估优化已完成，5个skills优化，平均提升+0.39分 |
| TD-005 | 13个skills全量A+级优化，从B/B+/A级提升至A+级 | 2026-07-02 | **已完成** | 全量优化完成，所有skills达到A+级（9.5-10分），平均提升+0.82分 |

---
最后更新: 2026-09-23（变更：TD-001 已关闭，全部技术债处理完毕）

## TD-003 详细清单

已全部完成（Round 2，`skills-optimization-2026-07-02-round2.md`）。
