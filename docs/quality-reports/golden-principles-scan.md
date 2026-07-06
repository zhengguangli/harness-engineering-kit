# 黄金原则扫描报告 2026-07-02

检查时间: 2026-07-02
扫描范围: `/Users/lizhengguang/Documents/Github/harness-engineering-kit`
扫描方式: 多维度自动化扫描

---

## 总体评分

| 维度 | 状态 | 说明 |
|---|---|---|
| CLAUDE.md 健康度 | 🟢 PASS | 39 行，地图声明完整 |
| docs/ 元数据完整性 | 🟢 PASS | 28/28 有 `最后更新:` |
| docs/ 断链 | 🟢 PASS | 0 断链 |
| 死链到 agents/<name>.md | 🟢 PASS | skills/ 中 0 处，仅历史计划中有预期引用 |
| SKILL.md frontmatter | 🟢 PASS | 13/13 通过全部字段检查 |
| 6 段式 Agent Prompt | 🟡 PARTIAL | 4/13 完整，9/13 缺 `## 跳过条件` |
| SKILL.md 行数 | 🟡 2/13 ≥ 500 | architecture-boundaries (520)、commit-gate (519) |
| openai.yaml 同步 | ✅ RESOLVED | 2026-07-03 已全部删除，Codex/OpenCode 平台不再支持 |
| openai.yaml 教过时规则 | ✅ RESOLVED | 2026-07-03 已全部删除 |
| `.bak` 文件 | 🟢 CLEAN | 已清理 2 个残留 |

---

## 详细发现

### 发现 1: harness-authoring/openai.yaml 教过时规则（CRITICAL）

**位置**: `skills/harness-authoring/agents/openai.yaml:31,57`
**问题**: 仍然指导生成 `agents/<agent-name>.md`，称其为"Claude Code: `agents/<agent-name>.md` — YAML frontmatter + 系统提示词正文"
**实际**: 自 `consolidate-agents-into-skills.md` 之后，Claude Code 的 agent 提示词已内联到 `SKILL.md` 的 `## Agent 提示词` section
**影响**: 新建 skill 时会按过时模板生成，产生死文件
**修复**: 将 openai.yaml 中的引用改为 `SKILL.md` 的 `## Agent 提示词` section

---

### 发现 2: openai.yaml 全量不同步（KNOWN TD-002，仍严重）

**范围**: 13/13 技能
**表现**: `system_prompt` 字段内容与 `SKILL.md` 中 `## Agent 提示词` 内容不一致
**原因**: 历次优化（润色、heading 层级统一、内容重构）更新了 SKILL.md 但未同步到 openai.yaml
**建议**: 建立同步验证脚本，将 TD-002 提升为 P0 优先处理

---

### 发现 3: `## 跳过条件` 缺失（MEDIUM）

**Core-belief #10 要求**：
- 标准六段式：角色定义 / 核心能力 / 执行流程 / 约束 / 输出规范 / 跳过条件

**现状**：
| 完整（4/13） | 缺少 `跳过条件`（9/13） |
|---|---|
| commit-gate, observability-and-browser, orchestration, prompt-optimizer | architecture-boundaries, authoring, bootstrap, exec-plans, golden-principles, project-intake, repo-map, skill-quality-assessor, verification-loop |

**影响**: agent 不清楚何时应该跳过该技能，可能在不适合的场景误触发

---

### 发现 4: 2 个 SKILL.md 超过 500 行（MEDIUM）

| 文件 | 行数 | 超过阈值 |
|---|---|---|
| `skills/harness-architecture-boundaries/SKILL.md` | 520 | +20 |
| `skills/harness-commit-gate/SKILL.md` | 519 | +19 |

**建议**: 将 `references/` 模板内容从 SKILL.md 正文中拆出。architecture-boundaries 包含完整分层模型示例，可以拆到 `references/`；commit-gate 的详细检查策略表可以拆出。

---

### 发现 5: 文档超长（LOW）

| 文件 | 行数 | 备注 |
|---|---|---|
| `skills/harness-skill-quality-assessor/references/skill-evaluation-process.md` | 598 | 评估流程参考文件 |
| `skills/harness-skill-quality-assessor/references/evaluation-examples.md` | 516 | 评估示例 |

**建议**: `docs/skill-evaluation-process.md` 已删除， canonical 位置在 `skills/harness-skill-quality-assessor/references/skill-evaluation-process.md`。

---

### 发现 6: Agent Prompt 内部结构不统一（LOW）

Core-belief #10 定义六段式，但实际 agent prompt 主要使用两种结构：
- **编号式**: `### 1. xxx` / `### 2. xxx`（多数技能）
- **主题式**: `### Topic Name` 直接命名（部分技能）

这两种结构都是合理的，但 core-belief #10 的文字描述与实际情况存在差距。应更新 core-belief #10 以反映实际使用的结构模式，或统一所有 prompt。

---

## 建议立项的黄金原则

基于扫描发现，建议建立以下 4 条可机械检查的黄金原则：

### GP-001: `最后更新:` 全覆盖

**规则**: 所有 `docs/` 下的 `.md` 文件末尾必须包含 `最后更新: YYYY-MM-DD` 行。
**检查方式**: `for f in docs/**/*.md; do grep -q "最后更新:" "$f" || echo "MISSING: $f"; done` — `**` 递归通配需要 `shopt -s globstar`（Bash 4+）
**修复行为**: 追加到文件末尾
**当前状态**: 🟢 28/28 已覆盖

### GP-002: 无 agents/<name>.md 引用

**规则**: `skills/` 下的文件不允许引用 `agents/<name>.md`（历史 exec-plan 引用例外）。
**检查方式**: `rg "agents/[a-z-]*\.md" skills/`
**修复行为**: 删除或改为指向 `SKILL.md` 的 `## Agent 提示词`
**当前状态**: 🟢 0 违规

### GP-003: SKILL.md 行数 ≤ 500

**规则**: 每个 SKILL.md 不超过 500 行（core-belief #6：渐进式披露）。
**检查方式**: `wc -l < SKILL.md`
**修复行为**: 将模板/示例拆分到 `references/`
**当前状态**: 🟡 2/13 违规

### GP-004: 六段式 Agent Prompt 覆盖率

**规则**: Agent prompt 应包含 core-belief #10 定义的全部 6 个标准段。
**检查方式**: `grep "^## <sect>"` 对 6 个段逐项检查
**修复行为**: 补齐缺失段
**当前状态**: 🟡 4/13 完整

---

## 建议的清扫节奏

| 原则 | 检查频率 | 修复颗粒度 | 自动修复 |
|---|---|---|---|
| GP-001: 最后更新 | 每周 | 单行追加 | ✅ 可自动 |
| GP-002: 死链引用 | 每周 | 删除/替换 | ✅ 可自动 |
| GP-003: 行数限制 | 每月 | references/ 拆分 | ⚠️ 需人工 |
| GP-004: 六段式 | 每月 | 逐段补齐 | ❌ 需设计 |

建议将 GP-001 和 GP-002 作为 CI 的 pre-merge 检查项，GP-003/GP-004 作为月度质量扫描任务。

---

## 已执行修复

- [x] 12 个文件追加 `最后更新: 2026-07-02`（doc-gardener 审计项）
- [x] 1 个文件追加 `最后更新: 2026-07-01`（`skills-optimization-2026-07-01.md`，新发现）
- [x] 清理 `.claude/*.bak` 残留文件（2 个）

最后更新: 2026-07-02
