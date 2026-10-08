# 质量测量计划（Quality Measurement Program）

## Goal

把 harness-engineering-kit 的质量评估从**主观加权打分**迁移到**可复现测量**。

第 1-33 轮使用的 8 维度加权评分（`Σ 维度分 × 权重`）不满足基本测量属性：无外部基准（效度）、
单一评估者兼作者（信度）、13 个 skill 密集分布在 9.42-9.50（无区分度）、第 28 轮内容零变化
而平均分从 9.51 变 9.48（不可复现）。本计划用可机械复现的指标替代它，并保留人工判断的位置
但不给它虚假的精度。

## Scope / Non-goals

**In scope**
- 触发判别力测量（ranking accuracy / 混淆对 / 分差 / 置信区间）
- 规格可执行性审计（输出规格、任务集覆盖）
- 契约一致性棘轮（`when_to_use` ↔ `SKILL_KW` ↔ `REQUIRES`）
- 任务集与验收标准（供后续结果实验使用）

**Non-goals**
- 产出单一"质量总分"——加权主观判断不是测量
- 代理人工判断型的维度评分（clarity / UX / executability）

## Steps

### 已完成（2026-09-23 ~ 2026-09-24）

| # | 步骤 | 产物 | 状态 |
|---|---|---|---|
| 1 | TD-001 依赖机械强制 | `depends_on` 契约 + `validate_skill_dependencies.py` + 18 用例 | ✅ |
| 2 | 消除检查脚本三重重复 | `scripts/lib/harness_check.py` 唯一实现，1512→564 行 | ✅ |
| 3 | 修复 CI 假绿（退出码） | `sys.exit(checker.exit_code())` | ✅ |
| 4 | 补 3 个零覆盖校验脚本的测试 | `tests/scripts/`，23 用例 | ✅ |
| 5 | 测试接入 CI 第五阶段 | `run-all.py --run-type tests` | ✅ |
| 6 | 触发判别力测量工具 | `scripts/evaluate_trigger_discrimination.py` | ✅ |
| 7 | 用例扩充 51→138 + 门控/测量分离 | `cases.json` + `cases.diagnostic.json` | ✅ |
| 8 | 契约去歧义（3 类问题分类处理） | arch/golden/repo-map 的 `when_to_use` | ✅ |
| 9 | 契约漂移棘轮 | `TriggerContractConsistencyTests` | ✅ |
| 10 | 任务集 + 55 条验收标准 | `tests/tasks/tasks.json` | ✅ |
| 11 | 输出规格 + 任务覆盖审计 | `audit_output_specs.py` / `audit_task_coverage.py` | ✅ |
| 12 | REQUIRES 漂移棘轮 | `TaskCoverageMappingTests` | ✅ |
| 13 | 匹配机制对比（含留出集） | `compare_matchers.py` / `compare_matchers_holdout.py` | ✅ |

### 待办

| # | 步骤 | 阻塞原因 | 处理条件 |
|---|---|---|---|
| A | 扩标注到 ~150 正样本 | 需人工判断"哪些 skill 不该被选中" | 有人能标注歧义用例的完整应选/不应选集合 |
| B | 混合匹配器（语义排序 + 独立拒识信号） | 架构变更，非调参 | A 完成，或确认接受 68% 正准确率 |
| C | Tier-3 结果有效性 A/B 实验 | 需真实 agent 执行环境 | 有人拿 `tests/tasks/tasks.json` 分别带/不带 skill 跑一遍并回填结果 |
| D | 8 个 A 级 skill 的 A+ 人工重评 | 需 `harness-skill-quality-assessor` 人工打分 | 明确不机械指标替代 |

## Decision Log

| Date | Decision | Rationale | Rejected Alternatives |
|---|---|---|---|
| 2026-09-23 | 停用主观加权总分，改用机械检查点审计 | 加权主观判断不满足效度/信度/区分度/可复现；继续产出 9.xx 会误导决策 | 继续跑第 34 轮主观评估并只修 content |
| 2026-09-23 | 引入 `depends_on` frontmatter 而非改写 Related Skills 标注 | Related Skills 的 Upstream/Downstream 有两种相反语义，无法无歧义机械解析 | 规范化 Related Skills 为 input/output/routes-to/see-also 四标签（仍需人工判定每条） |
| 2026-09-24 | 门控集与测量集分离 | 测量集若设为门禁会迫使对着测量集调关键词，即过拟合 | 全部并入 cases.json（导致 17 FAIL，CI 恒红） |
| 2026-09-24 | 保留短语支持虽使指标下降 | "lint 规则"被空格拆成 "lint"+"规则"，碎片单独命中是白拿分；语义正确优先于数字 | 回退以保住了 78.6% 的表面数字 |
| 2026-09-24 | 不做混合匹配器 | 属架构变更，需先有足够标注数据才能验证 | 直接上语义匹配（无留出集验证等于盲改） |
| 2026-09-24 | 删掉 audit_task_coverage 的模糊回退 | 50% 词重叠回退放过了 "a quantum checksum of the diff must be computed before commit" | 提高重叠阈值到 70%（仍是同一类错误） |

## Acceptance Criteria

- [x] `python3 scripts/run-all.py` 七阶段全绿
- [x] 触发判别力有可复现数字 + 置信区间（当前 76.8%，CI [70.1%, 85.2%]）
- [x] 契约三份表示（`when_to_use`/`SKILL_KW`/`REQUIRES`）均有漂移棘轮
- [x] 任务集 + 55 条验收标准存在且全部有 SKILL.md 依据
- [x] 审计工具的敏感性经注入假数据验证（3/3 抓获）
- [ ] Tier-3 结果有效性有实测数字
- [ ] A+ 判定由人工完成并记录评估者与日期

## Risks / Known Unknowns

| 风险 | 说明 |
|---|---|
| 标注循环性 | 测量集标签来自各 skill 自己的 `when_to_use`，所以衡量的是"词表与契约的一致性"，不是"边界划分是否正确" |
| 样本量 | 138 用例的 CI 宽 13.8%；±5% 需 ~151 正样本 |
| 23 个用例标为 ambiguous | skill 边界本身模糊，与匹配器无关。这是比匹配器更根本的问题 |
| 三份表示的维护成本 | 每加一层抽象就多一份需同步的表示；已有棘轮管住，但未消除成本 |

## Change History

- 2026-09-24: 计划创建。步骤 1-13 完成，A-D 待办。
