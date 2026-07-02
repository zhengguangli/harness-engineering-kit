# Skill 臃肿重构计划

- 状态: completed
- 创建日期: 2026-07-02
- 最近更新: 2026-07-02
- 关联 PR / issue: 暂无
- 负责 agent / 人: opencode（主对话）
- 前置: `docs/exec-plans/completed/skills-optimization-2026-07-02-round2.md`（Round 2 结构一致性） + `docs/exec-plans/completed/skills-prompt-polish-2026-07-02.md`（润色对齐）

## 目标

将 5,347 行（13 个 skill，平均 411 行/文件）缩减到 ~3,700 行（平均 ~285 行/文件），缩减约 30%，同时 **不丢失任何功能性指令**——使每个 SKILL.md 聚焦于"agent 启动核心指令"而非"百科全书式文档"。缩减后 `make triggers-all` 保持 PASS ≥ 50 WARN=0 FAIL=0 不退化。

## 范围 / 非目标

**范围内:**
- 13 个 `skills/harness-*/SKILL.md` 的结构减肥：
  - 方法论执行步骤与 Agent 提示词执行流程去重（4 个高重叠文件）
  - 最佳实践与核心原则/关键要点去重（11 个含重复文件）
  - 何时使用示例行精简（共 68 行示例占位）
  - 将嵌入式 bash 自动化检查脚本替换为外部引用（11 个文件 × ~100 行 → ~20 行引用）
  - 跨 skill 交接点表精简或提取到共享文档
- 修改 `docs/ARCHITECTURE.md` 补充"引用外部脚本"的约定
- `make triggers-all` 全量验证

**明确不做(非目标):**
- 不动 Agent 提示词的核心语义（只删冗余不重写逻辑）
- 不动 `agents/openai.yaml`
- 不动 `references/` 子文件内容
- 不动 `scripts/`、`tests/`
- 不删除任何功能性指令——只做合并/精简/提取引用
- 不改 frontmatter 字段

## 步骤

### Phase A: 嵌入式 bash 脚本 → 共享引用

- [ ] **A.1** — 在 `scripts/` 下创建 `skill-automation-check.sh`（通用版），合并 11 个 skill 中几乎相同的 bash 检查模板；保留差异化参数作为 CLI 参数
- [ ] **A.2** — 逐个文件替换嵌入式脚本为 ````
  ```bash
  ./scripts/skill-automation-check.sh <skill-name>
  ```
  ````（11 个文件: architecture-boundaries, authoring, bootstrap, commit-gate, exec-plans, golden-principles, observability-and-browser, orchestration, project-intake, repo-map, verification-loop）
- [ ] **A.3** — 跑 `make triggers-all` 确认无退化

### Phase B: 方法论与 Agent 提示词执行流程去重

- [ ] **B.1** — **harness-commit-gate**（方法论 19 步 → Agent 9 步，高重叠）：方法论 `4. 执行步骤` 改为引用 "详见 `## Agent 提示词 → 执行流程`"，保留方法论独有的 diff 审查粒度说明
- [ ] **B.2** — **harness-verification-loop**（方法论 14 步 → Agent 8 步，高重叠）：方法论步骤改为简述 + 引用 Agent 流程
- [ ] **B.3** — **harness-project-intake**（方法论 5 步 → Agent 8 步，高重叠）：方法论去重，保留"分析五维度"的概念性说明
- [ ] **B.4** — **harness-bootstrap**（方法论 14 步 → Agent 6 步，中高重叠）：方法论简化为步骤列表 + 引用 Agent 流程
- [ ] **B.5** — 跑 `make triggers-all` 确认无退化

### Phase C: 最佳实践 → 核心原则/关键要点合并

- [ ] **C.1** — 逐文件分析 `## 最佳实践` 内容，标记与 `## 核心原则` / `## 关键要点` 完全重复的条目
- [ ] **C.2** — 对 11 个含 `## 最佳实践` 的文件执行合并：保留 `## 关键要点`，删除 `## 最佳实践` 中与核心原则/关键要点重复的部分；完全重复的删整节，部分重复的仅删冗余条目
- [ ] **C.3** — 跑 `make triggers-all` 确认无退化

### Phase D: 何时使用示例行精简

- [ ] **D.1** — 6 个含示例行的文件（architecture-boundaries 12 行、commit-gate 20 行、golden-principles 10 行、observability 6 行、orchestration 10 行、project-intake 10 行）删除 `  - 例如：` 行——"何时使用"本身已足够清晰
- [ ] **D.2** — 跑 `make triggers-all` 确认无退化

### Phase E: 跨 skill 交接点表精简

- [ ] **E.1** — 3 个含交接点表的文件（commit-gate 76 行、orchestration 66 行、verification-loop 77 行）：将详细错误处理表提取到 `references/`，SKILL.md 只保留"输入/输出/交接时机"3 行描述
- [ ] **E.2** — 跑 `make triggers-all` 确认无退化

### Phase F: 边界情况处理精简

- [ ] **F.1** — 精简边界情况处理中过于冗长的代码块示例，改为 1-2 行文字描述 + 指向 `references/` 的引用
- [ ] **F.2** — 跑 `make triggers-all` 确认无退化

### Phase G: 全量验证与收尾

- [ ] **G.1** — 全量 `make triggers-all`，确认 PASS ≥ 50 WARN=0 FAIL=0
- [ ] **G.2** — 更新 `docs/ARCHITECTURE.md` 补充"引用外部脚本"约定
- [ ] **G.3** — 汇总 `git diff --stat`，确认总缩减量 ~30%
- [ ] **G.4** — 移动本文件到 `docs/exec-plans/completed/`

## 决策日志

| 日期 | 决策 | 理由 | 被否决的备选方案 |
|---|---|---|---|
| 2026-07-02 | 嵌入式脚本 → 共享引用 | 11 个脚本 90% 相同，共享脚本消除 1,306 行中的 ~900 行模板重复 | 保留现状——让 SKILL.md 自包含，但膨胀不可接受 |
| 2026-07-02 | 最佳实践完全重复章节整节删除而非留 stub | "最佳实践"作为独立章节的价值已被"关键要点"覆盖，留 stub 不省行数 | 留 stub 行——浪费 2 行不带来收益 |
| 2026-07-02 | 方法论只删不重写 | 方法论的概念性说明（分层模型、判断原则）仍有价值，只需删除与 Agent 流程重复的执行步骤 | 整节删除——会丢失非重复的设计原理 |
| 2026-07-02 | 示例行全删而非缩减 | 示例行只是为了凑"具体化"样式，删除后"何时使用"依然可读 | 每例保留1个代表性示例——省不了多少行 |

## 验收标准

- [ ] 总行数从 5,347 降至 ~3,700（缩减 ~30%）
- [ ] 13 个 SKILL.md 全部不包含嵌入式 bash 脚本（改为 `./scripts/skill-automation-check.sh` 引用）
- [ ] `make triggers-all` 退出码 0，PASS ≥ 50，WARN=0，FAIL=0
- [ ] 所有功能性指令在重构后仍然存在于 Agent 提示词的某个位置（无内容丢失）
- [ ] `docs/ARCHITECTURE.md` 新增"引用外部脚本"约定

## 风险 / 已知未知

- **关键词命中风险**：精简"何时使用"示例时若删除带关键词的句子，`validate-keyword-consistency.sh` 会失败。**缓解**：每次改动 `description` / `when_to_use` 相关区域后立即跑 `keyword-consistency`。
- **引用的脚本不存在**：A.1 先创建共享脚本再逐个替换，顺序不可逆。**缓解**：所有 A.2 的替换在 A.1 验证通过后执行。
- **方法论精简过度**：过度依赖"引用 Agent 流程"可能导致读者跳转不便。**缓解**：在方法论保留每步的 1 行摘要 + 指南性说明，不直接删除整节。
- **不影响 `agents/openai.yaml`**：openai.yaml 的 system_prompt 引用 SKILL.md 的 Agent 提示词内容，本次只删方法论/最佳实践/脚本编码，不删 Agent 提示词内容，所以 openai.yaml 不受影响。

## 变更记录

- 2026-07-02: 创建计划，基线 5,347 行 / 13 files，PASS=50
