# R1 逻辑分区：诊断区下沉 + 维护者文档归位 + 分区叙事

- 日期：2026-11-02
- 状态：已获口头批准，待用户审阅书面 spec
- 路径：`docs/superpowers/specs/2026-11-02-refactor-layout-design.md`

## 背景与动机

仓库顶层结构（`skills/ scripts/ tests/ docs/ .github/`）本身合理，但存在三处"逻辑已分离、物理未跟上"的错位：

1. **门禁与实验混放**：`scripts/` 顶层 6 个门禁脚本与 3 个测量/实验脚本（`compare_matchers*.py`、`evaluate_trigger_discrimination.py`）平级；`tests/triggers/` 中门禁 `cases.json` 与测量集 `cases.diagnostic.json` 平级。`docs/exec-plans/active/quality-measurement-program.md` 已将「门控/测量分离」标记完成，但布局未跟随。
2. **README 混排**：README（19K）中约 90 行维护者内容（frontmatter 校验、agent prompt 校验、依赖校验、回归用例维护规范）与产品文档（介绍/使用/安装/接入顺序）混在一处。
3. **分区叙事缺失**：AGENTS.md 的目录注释未区分「产品区（对外契约）」与「工程区（内部基建）」，门禁面没有书面定义。

动机是质量提升，无紧急痛点；约束是**不触碰 `skills/` 内容**（对外契约区：skill 平台要求 `SKILL.md` 在 skill 根，`run-all.py --sync` 与 nacos-cli skill-sync 部署链路依赖 `skills/` 布局）。

## 目标

- 门禁面物理可辨：看目录即可知道哪些脚本/用例是 CI 门禁
- README 只保留产品面；维护者文档集中在 `docs/references/`
- AGENTS.md / ARCHITECTURE.md 写明「产品区 vs 工程区」边界与门禁面定义
- 全程 `python3 scripts/run-all.py` 六阶段保持绿色，CI 行为零变化

## 非目标（明确不做）

- **不移动 `docs/QUALITY_SCORE.md`**：harness-repo-map 的 SKILL.md 指导消费者项目创建 `docs/QUALITY_SCORE.md`，4 个 skill 共 6 处引用它是规定路径；移动会级联刷新 skill 内容与 Last updated 戳，侵入对外契约区
- 不移动/重命名顶层目录（不做 `eng/` 物理工程区）
- 不改动 `skills/` 下任何文件
- 不改动 `run-all.py` 阶段逻辑与 `.github/workflows/`
- 不改 `tests/tasks/tasks.json` 位置（验收数据，审计脚本按现有路径消费）

## 变更设计

### A. 诊断区下沉 —— `scripts/diagnostics/`

**移动（全部 `git mv` 保留历史）：**

| 原路径 | 新路径 |
|---|---|
| `scripts/compare_matchers.py` | `scripts/diagnostics/compare_matchers.py` |
| `scripts/compare_matchers_holdout.py` | `scripts/diagnostics/compare_matchers_holdout.py` |
| `scripts/evaluate_trigger_discrimination.py` | `scripts/diagnostics/evaluate_trigger_discrimination.py` |
| `tests/triggers/cases.diagnostic.json` | `scripts/diagnostics/cases.diagnostic.json` |

`cases.diagnostic.json` 只被上述 3 个实验脚本消费（已全仓 grep 确认），数据跟随工具。

**顺手修复**：3 个脚本把 `ROOT = os.getcwd()` 改为 `__file__` 三级上溯定位（`scripts/diagnostics/x.py` → 仓库根），`sys.path.insert` 与 cases 路径基于新 ROOT。此后可在任意 cwd 运行。

**门禁面定义（写入 AGENTS.md 与 ARCHITECTURE.md）**：

> 门禁面 = `scripts/*.py`（顶层，含 `lib/`）+ `tests/**/test_*.py` + `tests/triggers/cases.json`。`scripts/diagnostics/` 是测量/实验区，不属于门禁；禁止为凑 diagnostic 通过率修改门禁关键词（TD-006）。

**引用同步**：
- `AGENTS.md` §1 目录树注释、§4 测量集描述
- `docs/exec-plans/tech-debt-tracker.md` TD-006 行的脚本路径
- `docs/exec-plans/active/quality-measurement-program.md` 第 6/7/13 行的路径列

### B. 维护者文档归位 —— README 瘦身

README 第 195–286 行的维护者内容移出，README 保留产品面并在原位置留一行指路（「维护者参考见 `docs/references/`」）：

| 新文件 | 接收内容（README 原章节） |
|---|---|
| `docs/references/validation-checks.md` | 「Skill Frontmatter QA」「Agent Prompt 存在性校验」「依赖方向与循环依赖校验」 |
| `docs/references/regression-case-guide.md` | 「回归用例维护规范（Case Guide）」整块（判定规则/关键词一致性/报告与产物） |

`docs/references/` 定位明确为维护者参考区（`ci-pipeline.md` + 新增 2 个）。AGENTS.md Documentation Map 增加对应行。README 中所有指向被移动章节的内部锚点改为指向新文件。

### C. 分区叙事 —— AGENTS.md / ARCHITECTURE.md / CHANGELOG.md

- **AGENTS.md §1**：目录树注释重写为两区表述——产品区 `skills/`（对外契约：`SKILL.md` 在 skill 根，布局受部署链路约束，不可动）与工程区 `scripts/ tests/ docs/ .github/`；附 A 节的门禁面定义
- **ARCHITECTURE.md**：Domain Division 表增加 `scripts/diagnostics/` 行（测量实验，非门禁）；Supporting Infrastructure 部分补门禁面边界说明；刷新文末 Last updated 戳
- **CHANGELOG.md**：按 §8 格式追加架构级变更记录（目录契约：诊断区建立、README 维护者内容迁移）

## 波及面清单

移动/新建：
- 移：3 个 py + 1 个 json（A 节）
- 新建：`docs/references/validation-checks.md`、`docs/references/regression-case-guide.md`
- 改写：README（删除 90 行 + 加指路）、AGENTS.md、ARCHITECTURE.md、tech-debt-tracker.md、quality-measurement-program.md、CHANGELOG.md

不触碰：`skills/`（全部 13 个 skill）、`scripts/run-all.py`、`scripts/lib/`、`scripts/validate_*` 与 `audit_*`、`tests/scripts/`、`tests/dependencies/`、`tests/tasks/`、`tests/triggers/cases.json`、`.github/`、`.gitignore`。

## 验证方式

1. 每完成一节即跑 `python3 scripts/run-all.py`，六阶段全绿
2. A 节完成后从非仓库根目录试跑 `python3 scripts/diagnostics/evaluate_trigger_discrimination.py` 验证 cwd 解耦
3. 终态：`python3 scripts/run-all.py` 全绿 + `git status` 确认纯移动/改写无意外文件
4. 全仓 grep 旧路径（`scripts/compare_matchers`、`tests/triggers/cases.diagnostic.json` 等）确认零残留

## 风险与回退

| 风险 | 评估 | 缓解 |
|---|---|---|
| 引用残留导致文档过期 | 低 | 第 4 项 grep 验证 |
| 诊断脚本路径修复引入新 bug | 低 | 仅 3 个非门禁脚本，试跑验证 |
| 门禁行为变化 | 无 | `run-all.py`/`tests/` 不改 |
| 回退 | — | 全部 `git mv` 单次 revert 即可；无数据/格式变更 |

## 决策记录

- **R1 vs R2（物理工程区）**：R2 需改动仓库根定位硬编码（`harness_check.py`、`run-all.py` 的 `dirname` 二级上溯、tests 的 `sys.path.insert("../../../scripts")`）、CI 命令与全部文档，收益仅是视觉分区；R1 以最小物理变动达成逻辑分区
- **QUALITY_SCORE.md 原位**：skill 契约优先于本仓库文档整洁
- **cases.diagnostic.json 移入 scripts/diagnostics/**：测量数据跟随唯一消费者（实验脚本），tests/triggers/ 下只留门禁用例
