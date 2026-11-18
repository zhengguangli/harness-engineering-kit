# Changelog

本文件只记录**架构级变更**：新的契约/不变量、CI 行为变更、验证方法论变更、
核心依赖变更。逐 commit 的流水账看 `git log`。

格式遵循 `AGENTS.md` 的 Change Log 节：Context & Trade-offs / Impact Radius。

---

## [2026-11-18] 套件减法（13→9）与 SKILL.md 精简契约化重构

- **Context & Trade-offs**: 基于 5/13 代表性任务 Tier-3 A/B 隔离实测（`quality-measurement-program.md`），强模型对“10 章节 + 6 子节教程八股”边际收益低甚至产生负向干扰（`task-assessor-01` 对照组查出 7 处真实缺陷而挂载 skill 组只查出 4 处），真正拉开差距的是**硬约束、跳过边界、持久化外部状态、机械验收标准与运行时传感器**。因此执行减法与契约瘦身：剥离内部维护与非工程主线 skill，并将保留的 `SKILL.md` 从 205–349 行压缩至 80–120 行精简契约格式，消除主文档与 `## Agent 提示词` 间的双份重复。
- **Impact Radius**:
  - **Skill 减法（13→9）**：
    - `harness-project-intake` 并入 `harness-bootstrap`（保留 `references/project-card-template.md` 与 `Not found` 防编造硬约束，删去冗余文档）
    - `harness-authoring` 与 `harness-skill-quality-assessor` 退出对外 `skills/`，核心规范沉淀至 `docs/references/skill-authoring-guide.md` 与 `scripts/lib/harness_check.py`
    - `harness-prompt-optimizer` 剥离出代码工程套件
  - **精简契约标准与机械检查**：
    - 全部 9 个 `SKILL.md` 重构为 6 节精简契约（`Scope & Skip Conditions` / `Hard Constraints` / `Related Skills` / `Related Templates` / `Agent 提示词` 3 子节），行数从 205–349 行压至 **67–75 行**（≤ 120 行目标）
    - `scripts/lib/harness_check.py` 与 9 个 `automated_check_script.py` 切换至新契约并引入 150/180 行预算门禁
    - 修复实测暴露的 `harness-commit-gate` 缺陷：`allowed-tools` 补全 `Read`/`Grep`/`Glob`/`ls`/`pytest`/`go` 等，修正 `diff-review-checklist.md` 中危险的 `git reset HEAD~` 为 `git reset HEAD`
  - **依赖图、回归门禁与文档**：
    - `scripts/validate_skill_dependencies.py`、`docs/ARCHITECTURE.md` 收敛为 5 层 DAG（L0 `bootstrap` → L4 `commit-gate` + Meta `orchestration`）
    - `scripts/run_trigger_regression.py`、`tests/triggers/cases.json`（42 例）、`tests/tasks/tasks.json`（10 任务 / 43 验收标准）、`scripts/audit_output_specs.py`、`scripts/audit_task_coverage.py`、`README.md`、`AGENTS.md`、`docs/product-specs/index.md`、`docs/QUALITY_SCORE.md` 同步更新

## [2026-11-18] TD-007 落地、触发契约棘轮归零与 CI skill 级门禁阻断化

- **Context & Trade-offs**:
  1. **目标项目入口统一为 `AGENTS.md`（TD-007）**：本仓库入口已于 2026-10-08 整合为 `AGENTS.md`，但产品产出仍停留在 `CLAUDE.md`。为保持跨平台一致，将 `harness-bootstrap` 与 `harness-repo-map` 的目标项目入口统一改为 `AGENTS.md`（重命名 3 个模板为 `agents-md-*.md`），并同步相关 skill 说明、产品规格与验收/回归用例；`README.md` 摘要 OpenAI 原文结论处保留原文语境，产品行为描述切换为 `AGENTS.md`。
  2. **触发契约漂移棘轮归零**：`TriggerContractConsistencyTests` 原基线容忍 19 个孤儿关键词与 13 条未覆盖显式触发短语（包括 `harness-repo-map` 中与 `不触发` 冲突的 `从零搭建`）。在不针对 `cases.diagnostic.json` 调参（遵守 TD-006）的前提下，对齐各 `SKILL.md` 的 `when_to_use` 与 `SKILL_KW` 并清零基线（0 / 0）。
  3. **CI 行为变更**：`.github/workflows/skill-triggers.yml` 中 13 个 `automated_check_script.py` 此前仅打 `::warning::` 而不失败。现改为任一失败即 `exit 1` 阻断 CI，与 `run-all.py` 一同构成硬门禁。
- **Impact Radius**:
  - `skills/harness-bootstrap/`、`skills/harness-repo-map/` 及其他引用目标入口的 `SKILL.md` / `references/` — 目标入口切换为 `AGENTS.md`；模板重命名为 `agents-md-template.md`、`agents-md-examples.md`、`agents-md-map-template.md`
  - `scripts/run_trigger_regression.py`、`tests/triggers/cases.json`、`tests/tasks/tasks.json` — `CLAUDE.md` 用例迁移至 `AGENTS.md`，`SKILL_KW` 与 `when_to_use` 双向对齐
  - `tests/scripts/test_validation_scripts.py` — `BASELINE_ORPHAN_KEYWORDS`（19→0）与 `BASELINE_UNCOVERED_PHRASES`（13→0）归零，`_uncovered_phrases` 过滤句末中文句号
  - `.github/workflows/skill-triggers.yml`、`docs/references/ci-pipeline.md` — skill 级 `automated_check_script.py` 升级为阻断门禁
  - `scripts/validate_skill_triggers.py` — 恢复对废弃 `version` frontmatter 字段的拒绝校验
  - `docs/exec-plans/tech-debt-tracker.md`、`docs/product-specs/index.md`、`docs/design-docs/core-beliefs.md`、`AGENTS.md`、`README.md` — 同步 TD-007 关闭状态与入口约定

## [2026-11-02] 目录契约：诊断区建立与维护者文档归位

- **Context & Trade-offs**: 「门控/测量分离」在 quality-measurement-program 中早已逻辑完成，
  但物理布局未跟上：`scripts/` 顶层混放 6 个门禁脚本与 3 个测量实验脚本，`tests/triggers/`
  混放门禁用例与测量集；README 混排产品文档与维护者文档。选择 R1 逻辑分区（物理小动）而非
  R2 物理工程区（顶层 `eng/` 重组）——后者需改动仓库根定位硬编码（`harness_check.py`、
  `run-all.py` 二级 dirname 上溯、tests 的 sys.path hack）、CI 命令与全部文档，收益仅是视觉分区。
  `docs/QUALITY_SCORE.md` 保持原位：harness-repo-map 等 4 个 skill 将其作为消费者项目的
  规定路径引用，移动会侵入对外契约区。`cases.diagnostic.json` 跟随唯一消费者移入
  `scripts/diagnostics/`；3 个诊断脚本的仓库根定位从 `os.getcwd()` 改为 `__file__` 上溯，
  可在任意 cwd 运行。
- **Impact Radius**:
  - `scripts/diagnostics/` — 新建：`compare_matchers*.py`、`evaluate_trigger_discrimination.py`、
    `cases.diagnostic.json`（自 `scripts/` 与 `tests/triggers/` 移入，git mv 保历史）
  - `docs/references/` — 新增 `validation-checks.md`、`regression-case-guide.md`
    （README 维护者区块移入，README 19223→15663 字节，原位留指路行）
  - `AGENTS.md` / `docs/ARCHITECTURE.md` — 建立「产品区 `skills/` vs 工程区」分区叙事；
    写明门禁面定义 = `scripts/*.py`（顶层，含 `lib/`）+ `tests/**/test_*.py` + `tests/triggers/cases.json`
  - 门禁行为零变化：`run-all.py`、CI workflow、`skills/` 全部未动；消费方命令
    `python3 scripts/run-all.py` 不变；仅诊断脚本调用路径增加 `scripts/diagnostics/` 前缀

## [2026-10-08] 入口文件整合：CLAUDE.md 合并至 AGENTS.md

- **Context & Trade-offs**: `c45b933`（2026-09）曾以"清理非 Claude Code 文件"为由把 AGENTS.md 合并进
  CLAUDE.md，其隐含前提是"本 kit 只服务 Claude Code"。该前提已不成立——维护者的实际工作流是
  Codex（读 AGENTS.md），且 kit 自身的 core-beliefs #7 要求"跨平台兼容是设计约束"。AGENTS.md 是
  跨工具的标准入口约定，故本次反向整合：删除 CLAUDE.md，其独有内容（导航表、frontmatter 硬约束、
  Skill Invocation、测试细则、开发工作流）全部并入 AGENTS.md。代价：Claude Code 会话不再自动加载
  入口地图（内容零丢失，需时直读 AGENTS.md）；收益：消除双入口重叠（`run-all.py` 命令曾在两文件
  各存一份，是本会话修复的多起文档漂移的共同根因），CHANGELOG 对格式的引用同步改为不依赖章节号。
  目标项目由 harness-bootstrap 生成 CLAUDE.md 的行为不变——那是 kit 的产物，不是 kit 的入口。
- **Impact Radius**:
  - `CLAUDE.md` — 删除（git rm）
  - `AGENTS.md` — 吸收其全部独有内容，由 6 节扩为 8 节（新增 Documentation Map、Development Workflow）
  - `CHANGELOG.md` — 格式引用由 "AGENTS.md §6" 改为 "AGENTS.md 的 Change Log 节"（解耦章节号）
  - `docs/design-docs/core-beliefs.md` — 信念 6 补充入口区分；`docs/design-docs/index.md` — 校验日期刷新
  - 无脚本/测试依赖 CLAUDE.md（已全量 grep 核实：tests/tasks/tasks.json 等处的 CLAUDE.md 均指目标项目产物）

## [2026-09-24] depends_on 契约与依赖机械强制

- **Context & Trade-offs**: TD-001（skill 间循环依赖仅靠人工 review）在 13 个 skill 的规模下已不可靠。
  在"新增 frontmatter 字段"与"改写 Related Skills 标注体系"之间选择了前者——后者需要把 13 个
  SKILL.md 的相关章节全部重写，且 `Upstream`/`Downstream` 在现有内容里有两种相反语义
  （"我消费它的产出" vs "它调用我"），无法无歧义地机械解析。代价是每个 SKILL.md 多一个字段。
- **Impact Radius**:
  - 全部 13 个 `skills/*/SKILL.md` — 新增 `depends_on` frontmatter（14 条依赖边，零循环，全部向下）
  - `scripts/validate_skill_dependencies.py` — 新增，5 类校验：环检测 / 向下流动 / Meta 层隔离 /
    引用有效性 / 跨 skill `../harness-*/references/*` 路径存在性
  - `scripts/run-all.py` — 新增第四阶段 `deps`，CI 自动继承（**deps 失败即阻断 PR**）
  - `tests/dependencies/test_dependency_validation.py` — 新增，18 个标准库 unittest 用例
  - `docs/ARCHITECTURE.md` — 新增 "Declaring a dependency" 契约说明

## [2026-09-24] 质量评估方法论由主观加权分改为机械检查点审计

- **Context & Trade-offs**: 第 1-33 轮的 9.xx 分依赖评估者对 clarity / executability / UX 等维度的
  主观判断，且 13 个 skill 已密集分布在 9.42-9.50——分差落入评估噪声，继续加权打分只会产生分数通胀。
  改为对 rubric 中可客观判定的检查点做全量机械审计。代价是失去单一可比较的总分。
- **Impact Radius**:
  - `docs/QUALITY_SCORE.md`、`docs/quality-reports/skills-quality-assessment.md` — 记录第 34 次审计
  - 第 33 次的 5 A+ / 8 A、平均 9.46 保留为**最后一次主观评估结果**，未被覆盖
  - 若需新的 A+ 判定，必须由 `harness-skill-quality-assessor` 按 rubric 人工执行

## [2026-09-24] SKILL.md 规范章节顺序确立

- **Context & Trade-offs**: 13 个 skill 的章节顺序分裂为多个变体（5 个把 `Related Skills` 放在
  `Best Practices` 之前，8 个放在之后；3 个把 `Key Points` 放在 `Examples` 之前）。
  顺序取全库**众数位置**而非个人偏好，使其可被无争议地收敛。8 个 skill 被重排，
  安全性校验：标题集合与总行数均未变化。
- **Impact Radius**:
  - `docs/ARCHITECTURE.md` — 新增 "Canonical section order" 章节，列出 13 个章节的规定顺序
  - 8 个 `skills/*/SKILL.md` — 章节重排（内容零变更）
  - `harness-orchestration` 的 `Routing Recommendation` 移至 `Methodology` 之后

## [2026-09-24] CI 分支门禁规则修正

- **Context & Trade-offs**: 原规则要求 `head_ref == "developer"`，但仓库在 `aee5cec` 已把该分支
  改名为 `develop`，导致**所有** PR 都被阻断，且错误信息指向一个不存在的分支名，极难排查。
  改为集合匹配 `develop|main|release/*`，符合 gitflow。
- **Impact Radius**:
  - `.github/workflows/skill-triggers.yml` — job 改名 `enforce-developer-flow` → `enforce-branch-flow`，
    规则由全等比较改为集合匹配（**行为变更**）
  - `.github/pull_request_template.md` — 修正分支名，并将死命令 `make triggers-all`
    （Makefile 不存在）替换为 `python3 scripts/run-all.py`

## [2026-09-24] 质量报告纳入版本控制

- **Context & Trade-offs**: `.gitignore` 忽略 `docs/quality-reports/*.md`，但
  `skills-quality-assessment.md` 实际被 git 跟踪——同一目录两种状态，导致新的质量报告**无法提交**。
  删除该忽略规则。副作用：此前被忽略的 `harness-commit-gate-check.md`（2026-07-06 一次性输出，
  无任何引用）变为可提交，已删除。
- **Impact Radius**:
  - `.gitignore` — 删除质量报告忽略规则
  - `docs/quality-reports/harness-commit-gate-check.md` — 删除

---

## [2026-09-24] 校验脚本去重与 CI 门禁修复

- **Context & Trade-offs**: 13 个 skill 级检查脚本各自复制约 110 行相同样板（1512 行，两两相似度
  0.66-0.92），`scripts/lib/harness_check.py` 存有第三份功能相同但无人 import 的副本，而
  `QUALITY_SCORE.md` 两轮评估详细描述的 `scripts/skill_automated_check.py` 共享脚本从未存在。
  同时 12 个脚本打印 `[FAIL]` 却永远 exit 0，使 CI 的 `fail_count` 永不递增、summary 恒显
  "13/13 passed"。选择"保留并启用 `lib/harness_check.py` 为唯一实现"而非新建模块——它已存在且
  功能等价，代价是需要把它的 API 对齐 in-skill 版（`read_file` 返回 str 而非 list）。
- **Impact Radius**:
  - `scripts/lib/harness_check.py` — 重写为唯一规范实现（249 行）
  - `skills/*/references/automated_check_script.py` — 12 个瘦身为 1512→564 行（-63%），
    JSON 输出经逐字节比对验证等价；新增 `sys.exit(checker.exit_code())`
  - `scripts/run-all.py` — 新增第五阶段 `tests`（**测试失败即阻断**）；回归用例数改为动态读取
  - `scripts/run_trigger_regression.py` — 全量去重 `SKILL_KW`（重复 token 会虚增匹配数，
    曾把 `ambiguous-03` 的判定从 WARN 误导为 PASS）；assessor 关键词补充空格容忍变体
  - `tests/scripts/test_validation_scripts.py` — 新增 18 个用例，覆盖此前零测试的 3 个校验脚本
  - `tests/triggers/cases.json` — 48→51，补上 assessor 的触发盲区
  - `skills/harness-skill-quality-assessor/references/automated_check_script.py` —
    `bidirectional-refs` 检查替换为 `depends-on-consistency`（前者要求双向引用，与分层架构冲突）
  - 12 个此前未在 `SKILL.md` 登记的 `references/` 文件已全部登记

---

## [2026-09-24] 质量测量体系建立（PR #16 / #17 合并）

- **Context & Trade-offs**: 第 1-33 轮的 8 维度加权评分不满足基本测量属性——无外部基准、
  单一评估者兼作者、13 个 skill 密集分布在 9.42-9.50（极差 0.08 低于评估噪声）、
  第 28 轮内容零变化而平均分从 9.51 变 9.48。选择"停用加权总分、改用可复现测量"而非
  "再跑一轮主观评估并只修 content"——后者会继续产出误导决策的假精度数字。
- **Impact Radius**:
  - `scripts/evaluate_trigger_discrimination.py` — 新增。产出准确率/混淆对/分差/Wilson 置信区间，
    **刻意不产出综合分**
  - `scripts/audit_output_specs.py`、`scripts/audit_task_coverage.py` — 新增，接入 CI 第七阶段
  - `scripts/compare_matchers.py`、`compare_matchers_holdout.py` — 新增，匹配机制对比实验
  - `tests/triggers/cases.json` + `cases.diagnostic.json` — 门控集与测量集分离（51 + 87）
  - `tests/tasks/tasks.json` — 13 任务 / 55 条机械可验证验收标准
  - `tests/scripts/` — 23 个用例，覆盖此前零测试的 3 个校验脚本
  - `scripts/run-all.py` — 三阶段 → 七阶段
  - `docs/exec-plans/active/quality-measurement-program.md` — 新增，记录 13 项已完成 + 4 项待办
  - `docs/exec-plans/tech-debt-tracker.md` — 新增 TD-006~TD-010

> **2026-11-02 勘误**：本节中 `scripts/evaluate_trigger_discrimination.py`、
> `scripts/compare_matchers*.py` 已于 2026-11-02 移至 `scripts/diagnostics/`，
> `cases.diagnostic.json` 同批移至该目录；此处保留原文作为历史记录。

### 关键实测结果

| 指标 | 值 |
|---|---|
| 门控集（51）正样本准确率 | 89.1% |
| 测量集（87）正样本准确率 | 68.2% |
| 合计（138） | 76.8%，95% CI [70.1%, 85.2%] |
| TF-IDF 留出集（阈值仅在 gate 上选） | 97.0%，McNemar p < 0.001 vs 子串 |

**门控集虚高 21 个百分点**——它只装了匹配器已能处理的用例，与本次修的退出码 bug 属同一失败形态。

---

最后更新: 2026-09-24
