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
- **references 脚本**（`skills/*/references/`）：完全自包含，不依赖外部模块

### 3. 自包含原因
- Skills 独立部署到 `~/.claude/skills/<name>/`，拷贝范围只有 `skills/<name>/`
- 项目根 `scripts/` 不在部署范围内
- 内联 80 行样板代码的代价远低于维护 base.py 同步机制的复杂度

### 4. 文件名命名
- 沿用 Python 惯例: kebab-case（`.sh`）→ snake_case（`.py`）
- `automated-check-script.sh` → `automated_check_script.py`
- `validate-skill-triggers.sh` → `validate_skill_triggers.py`

### 5. 重复样板不抽象的立场
参考脚本的首要读者是人（学习参考），不是解释器。self-contained 的可读性优于 DRY。且基础设施层改动频率 ≈ 0。

## 文件清单

| 原文件 | 新文件 | 说明 |
|---|---|---|
| `scripts/lib/` (新建) | `scripts/lib/__init__.py` + `harness_check.py` | 共享库，仅供主脚本 |
| `scripts/validate-skill-triggers.sh` | `scripts/validate_skill_triggers.py` | frontmatter 校验 |
| `scripts/run-trigger-regression.sh` | `scripts/run_trigger_regression.py` | 48 case 回归测试 |
| `scripts/validate-agent-prompt-sync.sh` | `scripts/validate_agent_prompt_sync.py` | Agent 提示词存在性 |
| `scripts/skill-automated-check.sh` | `scripts/skill_automated_check.py` | 共享检查器（JSON） |
| `scripts/skill-automation-check.sh` | `scripts/skill_automation_check.py` | 中文检查器（Markdown） |
| 13× `references/automated-check-script.sh` | 13× `references/automated_check_script.py` | 自包含 |

---

最后更新: 2026-07-06
