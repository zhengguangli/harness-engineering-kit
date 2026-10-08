# AGENTS.md

> 本文件是 harness-engineering-kit 的**唯一入口**（2026-10-08 由 `CLAUDE.md` 合并而来，沿革见 `CHANGELOG.md`）。它是地图，不是百科全书：这里没答案时去下文对应的 `docs/` 文件找，不要假设这个文件之外的信息不存在。
>
> 本仓库是 Harness Engineering Kit **自身**，不是被初始化的目标项目。目标项目在执行 `harness-bootstrap` 后各自生成自己的 `CLAUDE.md`——kit 给消费者的产物与 kit 自身入口是两回事，互不影响。

## 1. Project Structure & Module Organization

harness-engineering-kit 是与具体项目无关的 skills + agents 套件（13 个 skill），无编译步骤，全部为纯文本 + Python 3 标准库脚本。

```
skills/harness-*/    # 每个 skill：SKILL.md（方法论 + frontmatter + `## Agent 提示词`）+ references/ 模板
scripts/             # Python 校验脚本（snake_case，仅标准库，只读 skills/ 不修改）
tests/triggers/      # 触发词回归用例 cases.json（门禁）与 cases.diagnostic.json（测量集）
tests/dependencies/  # 依赖校验回归（unittest）
tests/scripts/       # 校验脚本自身行为回归
tests/tasks/         # 13 个代表性任务 + 55 条机械可验证验收标准
docs/                # 设计文档、执行计划、质量报告；docs/generated/ 自动生成，勿手改
.github/             # CI workflow 与 PR 模板
```

## 2. Build, Test, and Development Commands

无 build/install 步骤，核心入口是全量验证流水线（与 CI 同款，六阶段）：

```bash
python3 scripts/run-all.py                        # 全量：frontmatter → 触发回归 → Agent Prompt → 依赖校验 → 单元测试 → 审计
python3 scripts/run-all.py --run-type check       # 仅 frontmatter 字段校验
python3 scripts/run-all.py --run-type regression  # 触发词回归（加 --json 输出报告到 tests/triggers/report.json）
python3 scripts/run-all.py --run-type prompt      # 仅 agent prompt 存在性检查
python3 scripts/run-all.py --run-type deps        # 依赖方向 / 循环依赖校验
python3 scripts/run-all.py --run-type tests       # 仅单元测试（tests/ 下全部）
python3 scripts/run-all.py --sync                 # 全量验证 + 部署 skills 到 ~/.agents/skills/（维护 ~/.claude/skills 软链接）
```

提交前必须全绿；失败即阻断合并。各 skill 的 `references/automated_check_script.py` 仅在仓库布局内可运行；独立部署的 skill 副本会输出 `[SKIP]` 并退出——这是设计行为，不是故障。

## 3. Coding Style & Naming Conventions

- Python：仅标准库，snake_case 文件名与函数名，`python3` 直接运行，无第三方依赖。
- Skill 目录：`harness-` 前缀 + kebab-case。
- `SKILL.md` 章节顺序固定（见 `docs/ARCHITECTURE.md` 的 Canonical section order），不可随意重排。
- agent 提示词标题须以 `agent:` frontmatter 的 slug 开头（如 `## entropy-collector (Entropy Sweeper)`），由 assessor 检查脚本机械强制；agent 子节与主文档对应章节共存是规范设计（agent 提示词须自包含），只有逐行重复才算冗余。
- 改动 `SKILL.md` 后必须同步刷新其 `Last updated` 日期戳：assessor 检查脚本对全部 13 个 skill 强制 90 天新鲜度阈值（76-90 天预警），过期即记 FAIL。
- 文档正文可中文；代码注释、提交信息必须英文。

### Frontmatter 契约（违反即阻塞合并）

- 必填 `description`（≥20 字符）、`when_to_use`、`compatibility`、`depends_on`（无依赖写 `[]`）；禁止废弃的 `version` 字段。
- `depends_on` 只表达真实数据依赖（"我消费它的产出"）；路由/参见/模板出处指针放 `## Related Skills`，用 `input`/`output`/`routes-to`/`see-also` 四标签标注。
- `compatibility` 和 `metadata`（含 `category`）为 harness 自定义扩展字段，非 Claude Code 标准字段，会被静默忽略——跨平台兼容是设计约束。
- agent 提示词的 canonical 版本在 `SKILL.md` 的 `## Agent 提示词` section，不存在独立的 `agents/<name>.md` 文件。

### Skill Invocation

所有 skill 均使用 `context: fork`，通过 subagent 独立执行。3 个 `disable-model-invocation: true`（`harness-bootstrap`、`harness-commit-gate`、`harness-verification-loop`）不能直接用 Skill tool 调用，必须通过 `Agent` tool 或 Workflow 使用。13/13 个 skill 均显式声明 `allowed-tools`（最小权限）：commit-gate 与 verification-loop 为构建工具子集，其余为只读巡检子集。

## 4. Testing Guidelines

- 框架：标准库 `unittest`（无 pytest）。
- `tests/triggers/cases.json`（51 例）是回归门禁，必须全绿；新增 skill 必须同步更新 `scripts/run_trigger_regression.py` 的 `SKILL_KW` 关键词映射并新增 case（id 格式 `skill-topic-NN`）。
- `cases.diagnostic.json`（87 例）是契约派生测量集，**不是门禁**，禁止为凑通过率调关键词。判别力测量用 `scripts/evaluate_trigger_discrimination.py`；匹配机制对比实验见 `scripts/compare_matchers*.py`（结论：TF-IDF 更优但无阈值能兼顾正负样本，故门禁保留子串匹配，见 TD-006）。
- `tests/dependencies/test_dependency_validation.py`（18 例）：新增 skill 必须在 `scripts/validate_skill_dependencies.py` 的 `LAYERS` / `META_LAYER` 登记层级，否则 CI 失败（有意设计）。
- `tests/scripts/test_validation_scripts.py`：校验脚本自身的行为回归（含关键词重复检测、每 skill 至少一条回归用例、共享库降级行为等不变量）。
- `tests/tasks/tasks.json`：13 个代表性任务 + 55 条机械可验证验收标准；`scripts/audit_output_specs.py` 与 `scripts/audit_task_coverage.py` 审计其可执行性与覆盖。
- 以上测试由 `run-all.py` 第五阶段自动执行，CI 继承——**测试失败即阻断合并**。

**质量门现状**：最后一次主观加权评分为第 33 次（2026-07-10，平均 9.46，5 A+ / 8 A）；第 34 次（2026-09-23）起改为机械检查点审计，13/13 全绿。详见 `docs/QUALITY_SCORE.md`。

## 5. Documentation Map

| 我想知道… | 去看这里 |
|---|---|
| 13 个 skill 的分层架构与依赖方向 | `docs/ARCHITECTURE.md` |
| agent-first 的核心运作信念 | `docs/design-docs/core-beliefs.md` |
| 设计决策索引 | `docs/design-docs/index.md` |
| Agent Prompt 内联迁移设计 | `docs/design-docs/agent-prompt-inline-migration.md` |
| 设计决策详情 | `docs/design-docs/` |
| 当前执行计划 | `docs/exec-plans/active/` |
| 已知但暂不处理的技术债 | `docs/exec-plans/tech-debt-tracker.md` |
| 产品功能规格 | `docs/product-specs/index.md` |
| 各 skill 质量评分与趋势追踪 | `docs/QUALITY_SCORE.md` |
| 架构级变更记录（契约/CI/方法论变更） | `CHANGELOG.md` |
| Skills 质量评估报告 | `docs/quality-reports/skills-quality-assessment.md` |
| 13 个 skill 的方法论正文 + agent 提示词 + 模板 | `skills/` |
| 详细的安装方式、触发速查表、回归用例维护规范 | `README.md` |

## 6. Development Workflow

修改 skill 后按此顺序操作：

1. 修改 `skills/<name>/SKILL.md`
2. 运行全量验证脚本（`python3 scripts/run-all.py`）确保无断裂
3. 用 `harness-skill-quality-assessor` 评估修改质量
4. 提交前再跑一次全量验证——**这是硬约束，提交前必须通过**
5. 推送到 `develop` 分支（本仓库 PR 合并到 `main`）

**架构级变更必须同步更新 `CHANGELOG.md`**（新增/变更契约或不变式、CI 行为变更、验证方法论变更、核心依赖变更）；逐 commit 的流水账不进 CHANGELOG，看 `git log`。

## 7. Commit & Pull Request Guidelines

- Conventional Commits：`type(scope): imperative summary`，subject ≤72 字符、英文、原子提交；type ∈ `feat|fix|refactor|docs|chore|test|style|perf`。
- Gitflow：`feature/*` → `develop` → `main`；PR 只能从 `develop` / `main` / `release/*` 合入 `main`（CI 机械强制）。
- PR 描述使用 `.github/pull_request_template.md`，须勾选“本地已通过 `python3 scripts/run-all.py`”。

## 8. Change Log

架构级变更（新契约/不变量、CI 行为变更、验证方法论变更、核心依赖变更）必须更新 `CHANGELOG.md`。历史记录中发现过期命令/数字时，追加带日期的勘误注记（`> **YYYY-MM-DD 勘误**`），不改写原文。逐 commit 流水账不进：

```
### [YYYY-MM-DD] 变更标题
- Context & Trade-offs: ...
- Impact Radius: ...
```
