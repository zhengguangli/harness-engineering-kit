# R1 逻辑分区重构实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将测量/实验资产物理下沉到 `scripts/diagnostics/`、README 维护者内容归位到 `docs/references/`，并在 AGENTS.md/ARCHITECTURE.md 中建立「产品区 vs 工程区」分区叙事与门禁面定义。

**Architecture:** 纯目录/文档重构，无行为变更。门禁脚本、`run-all.py`、CI、`skills/` 全部不动；唯一功能变化是 3 个诊断脚本的仓库根定位从 `os.getcwd()` 改为 `__file__` 上溯。

**Tech Stack:** Python 3 标准库、git mv、Markdown。

**Spec:** `docs/superpowers/specs/2026-11-02-refactor-layout-design.md`

## Global Constraints

- 全程不触碰 `skills/` 下任何文件（对外契约区）
- 不移动 `docs/QUALITY_SCORE.md`（spec 非目标：4 个 skill 将其作为消费者项目的规定路径引用）
- 不修改 `scripts/run-all.py`、`scripts/lib/`、`scripts/validate_*`、`scripts/audit_*`、`.github/`、`.gitignore`、`tests/scripts/`、`tests/dependencies/`、`tests/tasks/`、`tests/triggers/cases.json`
- 每任务结束跑 `python3 scripts/run-all.py` 六阶段全绿
- 移动一律 `git mv` 保留历史；提交信息用 Conventional Commits、英文、subject ≤72 字符
- 文档正文中文；改动 ARCHITECTURE.md 时刷新其文末 Last updated 戳

## Review Focus

1. 从非仓库根 cwd 运行 `scripts/diagnostics/evaluate_trigger_discrimination.py` → 正常输出评估结果（ pinning Task 1 Step 5 的 /tmp 试跑）
2. `cases.diagnostic.json` 移动后无消费者引用旧路径 → 门禁不读它，但任何残留引用都是过期文档（pinning Task 4 Step 1 的 grep）
3. README 删除章节后无其他文件指向旧锚点/旧描述（pinning Task 2 Step 4 的引用 grep + product-specs 同步）
4. AGENTS.md 目录树注释与移动后的物理布局逐行一致（pinning Task 3 Step 3 的核对）
5. 分区叙事中「门禁面」定义与实际 `run-all.py` 调用集一致（六脚本 + test_*.py + cases.json）（pinning Task 4 Step 1 的门禁面核对）

---

### Task 1: 诊断区下沉到 scripts/diagnostics/

**Files:**
- Move: `scripts/compare_matchers.py` → `scripts/diagnostics/compare_matchers.py`
- Move: `scripts/compare_matchers_holdout.py` → `scripts/diagnostics/compare_matchers_holdout.py`
- Move: `scripts/evaluate_trigger_discrimination.py` → `scripts/diagnostics/evaluate_trigger_discrimination.py`
- Move: `tests/triggers/cases.diagnostic.json` → `scripts/diagnostics/cases.diagnostic.json`
- Modify: 上述 3 个 .py 的 ROOT 定位与 cases 路径
- Modify: `docs/exec-plans/tech-debt-tracker.md`（TD-006 行）、`docs/exec-plans/active/quality-measurement-program.md`（第 6/7/13 行）

**Interfaces:**
- Consumes: 无（第一个任务）
- Produces: `scripts/diagnostics/` 目录布局；3 个脚本可在任意 cwd 运行；后续任务的文档引用目标路径

- [ ] **Step 1: 创建目录并 git mv 四个文件**

```bash
mkdir -p scripts/diagnostics
git mv scripts/compare_matchers.py scripts/diagnostics/compare_matchers.py
git mv scripts/compare_matchers_holdout.py scripts/diagnostics/compare_matchers_holdout.py
git mv scripts/evaluate_trigger_discrimination.py scripts/diagnostics/evaluate_trigger_discrimination.py
git mv tests/triggers/cases.diagnostic.json scripts/diagnostics/cases.diagnostic.json
```

- [ ] **Step 2: 修复 3 个脚本的 ROOT 定位**

在每个脚本的 `ROOT = os.getcwd()`（compare_matchers.py:32、evaluate_trigger_discrimination.py:28、compare_matchers_holdout.py:43）处，改为：

```python
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

（`scripts/diagnostics/x.py` → 仓库根三级上溯。）同步修正各脚本内 `sys.path.insert(0, os.path.join(ROOT, "scripts"))` 之后的用法不变；`evaluate_trigger_discrimination.py` 的 `CASES_FILE`/`DIAG_FILE` 指向 `tests/triggers/cases.json` 与 `scripts/diagnostics/cases.diagnostic.json`；`compare_matchers_holdout.py` 的 `gate=`/`diag=` open 调用改为基于 `ROOT` 的绝对路径。

- [ ] **Step 3: 更新两份 exec-plan 文档的路径引用**

- `docs/exec-plans/tech-debt-tracker.md` TD-006 行：`scripts/compare_matchers_holdout.py`、`scripts/evaluate_trigger_discrimination.py` → `scripts/diagnostics/` 前缀
- `docs/exec-plans/active/quality-measurement-program.md` 第 6/7/13 行的三处脚本路径加 `diagnostics/` 前缀；第 7 行 `cases.diagnostic.json` 改为 `scripts/diagnostics/cases.diagnostic.json`

- [ ] **Step 4: 验证门禁不受影响**

Run: `python3 scripts/run-all.py`
Expected: 六阶段全绿（`✅ 全量验证通过`）

- [ ] **Step 5: 验证 cwd 解耦**

Run: `cd /tmp && python3 <repo>/scripts/diagnostics/evaluate_trigger_discrimination.py | head -5`
Expected: 正常输出「触发判别力评估」报告头，无 FileNotFoundError

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "refactor(scripts): move diagnostic tools into scripts/diagnostics/"
```

---

### Task 2: 维护者文档归位（README 瘦身）

**Files:**
- Create: `docs/references/validation-checks.md`
- Create: `docs/references/regression-case-guide.md`
- Modify: `README.md`（删除 195–285 行维护者区块，加指路行）
- Modify: `docs/product-specs/index.md:7`

**Interfaces:**
- Consumes: 无代码接口；Task 1 完成即可（本任务不依赖 diagnostics 路径）
- Produces: `docs/references/` 维护者参考区三文件格局；README 产品面

- [ ] **Step 1: 抽取 validation-checks.md**

将 README 中从 `## Skill Frontmatter QA（frontmatter 质量校验）` 起、到 `### 依赖方向与循环依赖校验` 小节结束（不含其后的 `## 回归用例维护规范（Case Guide）`）的整块（约 195–253 行），原样移入 `docs/references/validation-checks.md`，文件头加一行 H1：`# Validation Checks（维护者参考）`。

- [ ] **Step 2: 抽取 regression-case-guide.md**

将 README 中 `## 回归用例维护规范（Case Guide）` 起、到 `## 推荐的接入顺序` 之前（约 255–285 行）的整块，原样移入 `docs/references/regression-case-guide.md`，文件头加 H1：`# 回归用例维护规范（Case Guide）`。

- [ ] **Step 3: README 原位替换为指路行**

在两处删除位置各留一行（紧随 `## Skill Frontmatter QA` 原位置）：

```markdown
## 维护者参考

校验工具用法、依赖校验说明与回归用例维护规范见 [`docs/references/`](docs/references/)（`validation-checks.md`、`regression-case-guide.md`、`ci-pipeline.md`）。
```

确认 README 剩余部分无断链、无遗留锚点引用。

- [ ] **Step 4: 同步引用方**

- `docs/product-specs/index.md:7` README 行的描述列：删去「回归用例维护规范」（移至 `docs/references/regression-case-guide.md`），保留「安装方式、触发速查表」
- Run: `grep -rn "回归用例维护规范\|Frontmatter QA" --include="*.md" . | grep -v docs/references | grep -v docs/superpowers`
  Expected: 仅剩 AGENTS.md 文档图一行（Task 3 处理）与 exec-plans 历史记录中的合法提及

- [ ] **Step 5: 验证**

Run: `python3 scripts/run-all.py`
Expected: 六阶段全绿

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "docs(readme): move maintainer sections to docs/references/"
```

---

### Task 3: 分区叙事（AGENTS.md / ARCHITECTURE.md / CHANGELOG.md）

**Files:**
- Modify: `AGENTS.md`（§1 目录树注释、§4 测量集描述、Documentation Map 第 86 行）
- Modify: `docs/ARCHITECTURE.md`（Domain Division 表、Supporting Infrastructure、Last updated）
- Modify: `CHANGELOG.md`（§8 格式追加）

**Interfaces:**
- Consumes: Task 1 的最终路径（`scripts/diagnostics/`）、Task 2 的新文档（`docs/references/*.md`）
- Produces: 分区叙事与门禁面定义（终态文档事实）
- 注记：spec A 节「引用同步」中列出的 AGENTS.md §1/§4 更新归并到本任务执行，Task 1 不触碰 AGENTS.md，避免双重编辑

- [ ] **Step 1: 重写 AGENTS.md §1 目录树注释**

在现有目录树注释基础上：标注 `skills/` 为产品区（对外契约，`SKILL.md` 在 skill 根，布局受 `run-all.py --sync` / nacos-cli skill-sync 部署链路约束，不可动）；`scripts/ tests/ docs/ .github/` 为工程区。更新路径行：`scripts/diagnostics/  # 测量/实验工具（compare_matchers*、evaluate_trigger_discrimination、cases.diagnostic.json），非门禁`；`tests/triggers/` 行删去 cases.diagnostic.json 提及。

- [ ] **Step 2: 更新 AGENTS.md §4 与 Documentation Map**

- §4：`cases.diagnostic.json`（87 例）描述改为「位于 `scripts/diagnostics/`，契约派生测量集」；`scripts/evaluate_trigger_discrimination.py`、`scripts/compare_matchers*.py` 路径加 `diagnostics/` 前缀
- Documentation Map（第 86 行附近）：拆两行——「安装方式、触发速查表 | `README.md`」；「校验工具、回归用例维护规范、CI 说明 | `docs/references/`」；并新增一行指向本次 spec/plan（「R1 目录重构设计与计划 | `docs/superpowers/`」可选）

- [ ] **Step 3: 更新 ARCHITECTURE.md**

- Domain Division 表加行：`| diagnostics | 触发匹配测量/实验工具（非门禁） | scripts/diagnostics/ |`
- Supporting Infrastructure Dependency Direction 小节末尾补一句门禁面定义：「门禁面 = `scripts/*.py`（顶层，含 `lib/`）+ `tests/**/test_*.py` + `tests/triggers/cases.json`；`scripts/diagnostics/` 不属于门禁（TD-006）」
- 文末 Last updated 戳刷新为 2026-11-02，注明本次变更

- [ ] **Step 4: 追加 CHANGELOG.md**

按 §8 格式追加：`### [2026-11-02] 目录契约：诊断区建立与维护者文档归位`，含 Context & Trade-offs（R1 逻辑分区 vs R2 物理工程区；QUALITY_SCORE.md 因 skill 契约保持原位）与 Impact Radius（门禁行为零变化；消费方命令 `python3 scripts/run-all.py` 不变；诊断脚本路径变化）。

- [ ] **Step 5: 验证**

Run: `python3 scripts/run-all.py`
Expected: 六阶段全绿

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "docs(agents): document product/engineering zones and gate surface"
```

---

### Task 4: 终态审计

**Files:**
- 只读核对，无文件变更（发现问题回到对应任务修复）

**Interfaces:**
- Consumes: Task 1–3 的全部产出
- Produces: 重构完成证据

- [ ] **Step 1: 旧路径零残留 grep**

Run:
```bash
grep -rn "scripts/compare_matchers\|scripts/evaluate_trigger_discrimination\|tests/triggers/cases.diagnostic" --include="*.md" --include="*.py" --include="*.json" . | grep -v ".git/" | grep -v "scripts/diagnostics/"
```
Expected: 无输出（`scripts/diagnostics/` 内部自述与 superpowers spec/plan 中的历史描述除外——允许其存在，但 AGENTS.md、ARCHITECTURE.md、exec-plans 不得残留旧路径）

- [ ] **Step 2: 门禁面核对**

Run: `git show --stat HEAD~3..HEAD` 并逐行核对 AGENTS.md 目录树与物理布局（`ls scripts scripts/diagnostics tests/triggers docs/references`）
Expected: 目录树注释与实际文件一一对应；`run-all.py` 六阶段调用集与「门禁面」定义一致

- [ ] **Step 3: 全量验证终跑**

Run: `python3 scripts/run-all.py && git status --short`
Expected: `✅ 全量验证通过` 且工作区干净（无未提交变更、无意外未跟踪文件）
