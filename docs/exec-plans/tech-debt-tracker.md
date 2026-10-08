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
| TD-006 | 触发词判别力上限：diagnostic 集正样本 ranking accuracy 76.8%（Wilson 95% CI [68.2%, 83.6%]）；TF-IDF 留出集 97.0% vs 子串 68.2%（McNemar p<0.001）但正负样本分数区间重叠、无阈值能同时兼顾，故门禁仍用子串匹配 | 2026-10-08 | **开放（接受为设计限制）** | 出现可同时满足正负样本分离的匹配机制时再评估（如语义 embedding 匹配）；在那之前禁止为凑 diagnostic 通过率调 `SKILL_KW` 关键词——diagnostic 集是测量集不是门禁，调关键词即过拟合。结论依据：`scripts/compare_matchers_holdout.py`、`scripts/evaluate_trigger_discrimination.py` |
| TD-007 | harness-bootstrap 只给目标项目生成 CLAUDE.md，未跟进本仓库自身的 AGENTS.md 多平台入口整合 | 2026-10-08 | **开放（产品决策）** | 确定 kit 官方多平台入口策略后处理；需同步 bootstrap SKILL.md、模板、product-specs 与 task-bootstrap-01 用例 |

---
最后更新: 2026-10-08（变更：新增 TD-006——触发判别力限制登记为开放项，附处理条件与反过拟合约束；新增 TD-007——bootstrap 目标项目入口多平台化；TD-001~005 维持已完成）

## TD-007 详细清单

**是什么**：`harness-bootstrap` 目前只给目标项目生成 `CLAUDE.md` 作为入口。本仓库自身入口已于
2026-10-08 整合为 `AGENTS.md`（跨工具约定），但 kit 的**产品行为**未同步——多平台用户的目标项目
仍只会得到 Claude 专用入口。

**为什么不现在处理**：这是产品行为变更，影响所有 bootstrap 产出物的结构，需要产品决策（只生成
AGENTS.md？两者都生成？按检测到的 agent 平台分支？），不属于文档修正范畴。

**什么条件下应该处理**：确定 kit 的官方多平台入口策略后。处理时需同步更新 `harness-bootstrap`
的 SKILL.md 方法论、`references/claude-md-template.md`（及可能的 agents-md 模板）、
`docs/product-specs/index.md` 的规格行，以及回归用例中 task-bootstrap-01 的 expected_artifacts。

## TD-003 详细清单

已全部完成（Round 2，`skills-optimization-2026-07-02-round2.md`）。
