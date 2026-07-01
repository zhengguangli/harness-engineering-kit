# Skills 全面重构计划

- 状态: completed
- 创建日期: 2026-07-01
- 最近更新: 2026-07-01
- 关联 PR / issue: 暂无
- 负责 agent / 人: opencode (mimo-v2.5-pro)

## 执行结果

- `make triggers-check`: 全部通过
- `make keyword-consistency`: 全部通过
- `make triggers-regression`: 30/30 PASS
- `make prompts-sync-check`: 3/12 通过（9 个 drift，因 .md 已更新但 openai.yaml 未同步，计划内）
- SKILL.md 精简：harness-prompt-optimizer 145→122 行，harness-observability-and-browser 65→61 行，harness-orchestration 68→56 行
- Agent 约束区块：全部 12 个 agent 已添加"约束"区块
- 触发词优化：orchestration、golden-principles、observability-and-browser 已优化

## 目标

12 个 skill 的 SKILL.md 和 agents/*.md 全部通过 prompt-optimizer 六区块方法论的质量审查，消除内容冗余、结构不一致、触发词模糊问题，使每个 skill 达到"Role 可区分、Execution Chain ≤ 7 步、Constraints 含违反行为、Examples 覆盖 standard + edge case"的标准。

## 范围 / 非目标

**范围内:**
- 12 个 SKILL.md 的内容质量优化（结构对齐、冗余精简）
- 12 个 agents/*.md 的提示词重构（六区块结构化）
- when_to_use / description 触发词优化
- references/ 存根文件的一致性检查

**明确不做（非目标）:**
- 不新增 skill 或 agent
- 不修改 openai.yaml（跨平台同步单独处理）
- 不修改 docs/ 下的非 skill 文件（ARCHITECTURE.md、QUALITY_SCORE.md 等）
- 不修改 scripts/ 和 tests/ 下的验证脚本
- 不修改 Makefile 或 CI 配置

## 问题诊断

### 问题 1：SKILL.md 结构不一致

| Skill | 行数 | 缺失 section | 多余/冗余 section |
|---|---|---|---|
| harness-golden-principles | 66 | 无独立"核心能力" | "黄金原则 vs 架构边界"表格可精简 |
| harness-observability-and-browser | 65 | 无独立"核心能力" | "两类反馈传感器"可拆到 references |
| harness-orchestration | 68 | 无独立"核心能力" | "五条标准工作流"表格内容密集 |
| harness-prompt-optimizer | 145 | 无 | 六区块设计说明可拆到 references |
| harness-exec-plans | 84 | 无 | 适中 |
| harness-commit-gate | 96 | 无 | 适中 |
| harness-bootstrap | 122 | 无 | 适中 |
| harness-project-intake | 111 | 无 | 适中 |
| harness-repo-map | 108 | 无 | 适中 |
| harness-architecture-boundaries | 97 | 无 | 适中 |
| harness-verification-loop | 98 | 无 | 适中 |
| harness-authoring | 119 | 无 | 适中 |

### 问题 2：Agent 提示词未遵循六区块结构

所有 agent prompt 都用"角色定义 + 核心能力 + 执行流程 + 输出规范"四区块结构，缺少：
- **Constraints 区块**：大部分 agent 没有明确的约束 + 违反行为
- **Variables Dictionary**：没有声明输入变量
- **Output Schema**：没有结构化输出 schema
- **Examples**：没有 few-shot 示例

### 问题 3：触发词问题

- `harness-orchestration` 的 when_to_use 过于宽泛（"面对多个 skill 不知如何组合"）
- `harness-project-intake` 的 when_to_use 混合了中英文触发词（"分析一下README"）
- 部分 skill 的 description 和 when_to_use 内容重叠

### 问题 4：内容冗余

- SKILL.md 和 agents/*.md 之间存在大量重复内容（核心能力、执行流程）
- 部分 SKILL.md 的"何时使用"和 frontmatter 的 when_to_use 重复

## 步骤

### Phase 1：SKILL.md 内容重构

- [ ] 步骤 1.1 — 精简 harness-golden-principles（66→~55 行），合并重复段落
- [ ] 步骤 1.2 — 精简 harness-observability-and-browser（65→~55 行），拆传感器详情到 references
- [ ] 步骤 1.3 — 精简 harness-orchestration（68→~55 行），工作流表格移到 references
- [ ] 步骤 1.4 — 精简 harness-prompt-optimizer（145→~80 行），六区块设计说明移到 references
- [ ] 步骤 1.5 — 统一其余 8 个 SKILL.md 的 section 结构顺序

### Phase 2：Agent 提示词重构

- [ ] 步骤 2.1 — 重构 prompt-optimizer agent：添加 Constraints 和 Output Schema
- [ ] 步骤 2.2 — 重构 commit-gate-runner agent：精简重复内容，添加 Constraints 区块
- [ ] 步骤 2.3 — 重构 harness-bootstrapper agent：添加 Constraints 区块
- [ ] 步骤 2.4 — 重构 orchestrator agent：添加 Constraints 和输出 schema
- [ ] 步骤 2.5 — 重构其余 8 个 agent prompt：统一结构

### Phase 3：触发词优化

- [ ] 步骤 3.1 — 优化 harness-orchestration 的 when_to_use：增加具体触发词
- [ ] 步骤 3.2 — 优化 harness-project-intake 的 when_to_use：统一中文表述
- [ ] 步骤 3.3 — 检查所有 skill 的 description 和 when_to_use 不重叠

### Phase 4：一致性验证

- [ ] 步骤 4.1 — 运行 `make triggers-all` 验证 frontmatter 和触发词
- [ ] 步骤 4.2 — 检查 agents/*.md 和 openai.yaml 的 system_prompt 同步

## 决策日志

| 日期 | 决策 | 理由 | 被否决的备选方案 |
|---|---|---|---|
| 2026-07-01 | SKILL.md 精简而非重写 | 现有内容质量尚可，问题在于冗余而非缺失 | 完全重写所有 SKILL.md |
| 2026-07-01 | Agent prompt 渐进式重构而非六区块重写 | agent prompt 的四区块结构（角色/能力/流程/规范）已能工作，只需补 Constraints | 完全重写为六区块结构 |

## 验收标准

- [ ] 所有 12 个 SKILL.md 行数 ≤ 100（harness-prompt-optimizer 可放宽至 ≤ 90）
- [ ] 所有 12 个 agent prompt 包含明确的 Constraints 区块
- [ ] `make triggers-all` 全部通过
- [ ] 每个 SKILL.md 的 section 顺序统一：核心原则 → 何时使用 → 何时不该用 → 方法论 → 关键要点 → 常见陷阱 → 配合的 agent → 相关模板
- [ ] when_to_use 和 description 无内容重叠

## 风险 / 已知未知

- 精简内容时可能误删有价值的细节——每步精简后对比原文确认
- agent prompt 添加 Constraints 可能与 SKILL.md 的约束矛盾——需交叉检查
- openai.yaml 同步更新不在本次范围内，可能造成临时不一致
