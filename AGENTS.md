# AGENTS.md

> 本仓库贡献指南。项目事实与命令以本文件和 `CLAUDE.md` 为准；架构与分层规则详见 `docs/ARCHITECTURE.md`。

## 1. Project Structure & Module Organization

harness-engineering-kit 是与具体项目无关的 Claude Code skills 套件（13 个 skill），无编译步骤，全部为纯文本 + Python 3 标准库脚本。

```
skills/harness-*/    # 每个 skill：SKILL.md（方法论 + frontmatter + `## Agent 提示词`）+ references/ 模板
scripts/             # Python 校验脚本（snake_case，仅标准库，只读 skills/ 不修改）
tests/triggers/      # 触发词回归用例 cases.json（门禁）与 cases.diagnostic.json（测量集）
tests/dependencies/  # 依赖校验回归（unittest）
tests/scripts/       # 校验脚本自身行为回归
docs/                # 设计文档、执行计划、质量报告；docs/generated/ 自动生成，勿手改
.github/             # CI workflow 与 PR 模板
```

## 2. Build, Test, and Development Commands

无 build/install 步骤，核心入口是全量验证流水线（与 CI 同款）：

```bash
python3 scripts/run-all.py                        # 全量：frontmatter → 触发回归 → Agent Prompt → 依赖校验 → 单元测试 → 审计
python3 scripts/run-all.py --run-type check       # 仅 frontmatter 字段校验
python3 scripts/run-all.py --run-type regression  # 触发词回归（加 --json 输出报告）
python3 scripts/run-all.py --run-type deps        # 依赖方向 / 循环依赖校验
python3 tests/dependencies/test_dependency_validation.py  # 运行单个 unittest 文件
python3 scripts/run-all.py --sync                 # 验证通过后部署 skills 到 ~/.agents/skills/
```

提交前必须全绿；失败即阻断合并。

## 3. Coding Style & Naming Conventions

- Python：仅标准库，snake_case 文件名与函数名，`python3` 直接运行，无第三方依赖。
- Skill 目录：`harness-` 前缀 + kebab-case。frontmatter 必填 `description`（≥20 字符）、`when_to_use`、`compatibility`、`depends_on`（无依赖写 `[]`），禁止废弃的 `version` 字段。
- `SKILL.md` 章节顺序固定（见 `docs/ARCHITECTURE.md` 的 Canonical section order），不可随意重排。
- 文档正文可中文；代码注释、提交信息必须英文。

## 4. Testing Guidelines

- 框架：标准库 `unittest`（无 pytest）。
- `tests/triggers/cases.json` 是回归门禁，必须全绿；新增 skill 必须同步更新 `scripts/run_trigger_regression.py` 的 `SKILL_KW` 关键词映射并新增 case（id 格式 `skill-topic-NN`）。
- `cases.diagnostic.json` 是契约派生测量集，不是门禁，禁止为凑通过率调关键词。
- 新增 skill 必须在 `scripts/validate_skill_dependencies.py` 的 `LAYERS` / `META_LAYER` 登记层级，否则 CI 失败（有意设计）。

## 5. Commit & Pull Request Guidelines

- Conventional Commits：`type(scope): imperative summary`，subject ≤72 字符、英文、原子提交；type ∈ `feat|fix|refactor|docs|chore|test|style|perf`。
- Gitflow：`feature/*` → `develop` → `main`；PR 只能从 `develop` / `main` / `release/*` 合入 `main`（CI 机械强制）。
- PR 描述使用 `.github/pull_request_template.md`，须勾选"本地已通过 `python3 scripts/run-all.py`"。

## 6. Change Log

架构级变更（新契约/不变量、CI 行为变更、验证方法论变更、核心依赖变更）必须更新 `CHANGELOG.md`，逐 commit 流水账不进：

```
### [YYYY-MM-DD] 变更标题
- Context & Trade-offs: ...
- Impact Radius: ...
```
