# Shell→Python 脚本迁移决策记录

## 背景

2026-07-06，将项目全部 .sh 脚本迁移到 Python 3，以支持跨平台（macOS/Linux/Windows via WSL）。

**迁移范围**：5 个主脚本（`scripts/`）+ 13 个 skills references 脚本（`skills/*/references/`）

## 关键决策

### 1. 语言选择：Python 3
- 已有间接依赖（部分脚本已调用 `python3`）
- 跨平台成熟，macOS/Linux/Windows 都预装
- 不需引入 `package.json` 等新依赖

### 2. 共享库 vs 自包含
- **主脚本**（`scripts/`）：共享 `scripts/lib/harness_check.py`
- **references 脚本**（`skills/*/references/`）：2026-09-24 去重重构后同样 import `scripts/lib/harness_check.py`（12/13；`harness-skill-quality-assessor` 因评分逻辑特有，保持自包含）

### 3. 共享库的部署代价与优雅降级（2026-10-08 修订）
- Skills 独立部署到 `~/.claude/skills/<name>/` 时，拷贝范围只有 `skills/<name>/`
- 2026-09-24 去重时接受该代价：13 份约 110 行的重复样板（1512 行，两两相似度 0.66-0.92）
  已实际发生漂移（编号列表化后多个副本静默少报 Hard Constraints 计数），
  去重收益（1512→564 行，-63%）大于独立部署时可运行性的损失
- 2026-10-08 补上降级路径：import 前先判断 `../../../scripts` 目录是否存在——
  存在则正常 import（库文件损坏时 ImportError 照常失败，**不产生 false-green CI**）；
  不存在（独立部署形态）则打印 `[SKIP]` 说明原因并 exit 0，不再以 traceback 崩溃
- 判定用"目录存在性"而非裸 `try/except ImportError`：后者会把仓库内真实的库损坏
  也吞成 exit 0，重现 CHANGELOG 记载过的 false-green CI 问题
- 回归覆盖：`tests/scripts/test_validation_scripts.py` 的
  `SkillAutomatedCheckScriptTests`（仓库内实跑 / 独立部署跳过 / 库损坏必失败）

### 4. 文件名命名
- 沿用 Python 惯例: kebab-case（`.sh`）→ snake_case（`.py`）
- `automated-check-script.sh` → `automated_check_script.py`
- `validate-skill-triggers.sh` → `validate_skill_triggers.py`

### 5. 重复样板不抽象的立场（2026-09-24 已修订）
原文立场：参考脚本的首要读者是人（学习参考），self-contained 的可读性优于 DRY。
该立场已被推翻——重复副本实际发生了静默漂移（见 §3）。现行立场：共享库
`scripts/lib/harness_check.py` 是唯一规范实现，skill 脚本只保留特有检查；
可读性通过库内文档字符串和每个脚本顶部的用法示例保证。

## 文件清单

| 原文件 | 新文件 | 说明 |
|---|---|---|
| `scripts/lib/` (新建) | `scripts/lib/__init__.py` + `harness_check.py` | 共享库，仅供主脚本 |
| `scripts/validate-skill-triggers.sh` | `scripts/validate_skill_triggers.py` | frontmatter 校验 |
| `scripts/run-trigger-regression.sh` | `scripts/run_trigger_regression.py` | 回归测试（用例数动态读出） |
| `scripts/validate-agent-prompt-sync.sh` | `scripts/validate_agent_prompt_sync.py` | Agent 提示词存在性 |
| （无对应 .sh） | `scripts/lib/harness_check.py` | 共享检查库（2026-09-24 起由主脚本与 12/13 skill 脚本共同 import；此前记录的 `skill_automated_check.py` / `skill_automation_check.py` 从未存在） |
| 13× `references/automated-check-script.sh` | 13× `references/automated_check_script.py` | 12 个 import 共享库 + 特有检查（独立部署时 `[SKIP]` 降级）；assessor 自包含 |

---

最后更新: 2026-10-08（变更：修正 §2/§3/§5 与 2026-09-24 去重重构的矛盾——references 脚本现已共享 `lib/harness_check.py`；§3 补充 2026-10-08 的 `[SKIP]` 优雅降级路径及其防 false-green 设计；删除文件清单中两个从未存在的脚本名）
