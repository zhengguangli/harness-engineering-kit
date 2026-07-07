# Skills A+ 突破计划

**目标**: 将 9 个 A 级 skill 推向 A+（9.50+），平均分从 9.48 提升至 9.55+
**创建日期**: 2026-07-07
**前置条件**: 全量验证通过（PASS=48, frontmatter 100%）

## 现状诊断

| 指标 | 当前值 | 目标值 | 差距 |
|------|--------|--------|------|
| 平均分 | 9.48 | 9.55+ | +0.07 |
| A+ 数量 | 4/13 | 9/13 | +5 |
| Agent 提示词质量均分 | 9.39 | 9.50+ | +0.11 |
| 最低分 skill | orchestration (9.42) | 9.50+ | +0.08 |

### 核心瓶颈

**Agent 提示词质量** 是 A→A+ 跃迁的最大障碍：
- A+ 参考 skill (prompt-optimizer) Agent Prompt 评分 9.65
- 9 个 A 级 skill 平均 Agent Prompt 9.39，差距 -0.26
- 仅靠 Example/Key Point/Best Practices 增量修补无法突破——需要 Agent Prompt 子节的结构性重构

### 各 skill 突破难度排序

| Skill | 当前分 | 距 A+ | 难度 | 突破策略 |
|-------|--------|-------|------|----------|
| commit-gate | 9.49 | -0.01 | ★☆☆ | Agent Prompt +1 Capability 即可 |
| repo-map | 9.48 | -0.02 | ★☆☆ | Agent Prompt Execution Flow 细化 |
| bootstrap | 9.47 | -0.03 | ★★☆ | Agent Prompt Constraints 扩展 |
| golden-principles | 9.46 | -0.04 | ★★☆ | Agent Prompt +自动化检查 |
| project-intake | 9.46 | -0.04 | ★★☆ | Agent Prompt Core Capabilities 细化 |
| verification-loop | 9.45 | -0.05 | ★★☆ | Agent Prompt Execution Flow 增强 |
| exec-plans | 9.44 | -0.06 | ★★★ | Agent Prompt 重构 + Output Spec |
| authoring | 9.42 | -0.08 | ★★★ | Agent Prompt 重构 + Design Principles |
| orchestration | 9.42 | -0.08 | ★★★ | Agent Prompt Constraints 重构 |

## 执行计划

### Phase 1: 速赢（预计 +0.03~0.05）

**目标**: commit-gate 突破 A+，验证策略有效性

| 步骤 | Skill | 动作 | 预期增幅 |
|------|-------|------|----------|
| 1.1 | commit-gate | Agent Prompt 增加 "push decision" 显式 Capability；Execution Flow 第 8 步细化 push 条件判断逻辑 | +0.02~0.03 |
| 1.2 | commit-gate | 评估是否达 A+，若未达则补充 Constraints（pre-existing failure 判定规则） | +0.01 |
| 1.3 | — | 运行 harness-skill-quality-assessor 确认 commit-gate 突破 | — |

**验证标准**: commit-gate 评分 ≥ 9.50

### Phase 2: Agent Prompt 结构性重构（预计 +0.05~0.08）

**目标**: 3 个中等难度 skill 突破 A+，建立可复制的 Agent Prompt 增强模式

| 步骤 | Skill | 动作 | 预期增幅 |
|------|-------|------|----------|
| 2.1 | repo-map | Agent Prompt Execution Flow 增加 "severity rating" 步骤；Core Capabilities 增加 "migration planning" 细化 | +0.03 |
| 2.2 | bootstrap | Agent Prompt Constraints 增加 "post-init checklist verification" 规则；Skip Conditions 细化 | +0.03 |
| 2.3 | golden-principles | Agent Prompt Core Capabilities 增加 "cross-file pattern drift detection"；自动化检查 3→5 | +0.03 |
| 2.4 | — | 批量验证 3 个 skill 评分 | — |

**关键模式**（从 A+ skill 提炼）:
1. Agent Prompt 每个子节必须有 **具体、可执行的规则**，不能只是描述性文字
2. Constraints 必须包含 **violation 行为**（"On violation, ..."）
3. Execution Flow 必须有 **明确的判断节点和分支**
4. Core Capabilities 必须是 **原子能力**，不能是笼统描述
5. Skip Conditions 必须覆盖 **所有不触发场景**，不能有遗漏

### Phase 3: 深度重构（预计 +0.05~0.10）

**目标**: 3 个高难度 skill 突破 A+

| 步骤 | Skill | 动作 | 预期增幅 |
|------|-------|------|----------|
| 3.1 | verification-loop | Agent Prompt Execution Flow 增加 "iteration convergence" 判断逻辑；Constraints 增加 flaky test 处理规则 | +0.04 |
| 3.2 | project-intake | Agent Prompt Core Capabilities 增加 "Monorepo multi-card generation"；Execution Flow 增加 "lockfile-only fallback" | +0.03 |
| 3.3 | exec-plans | Agent Prompt 重构：Execution Flow 增加 "plan overrun recovery"；Output Specification 增加 handoff artifact 模板 | +0.04 |
| 3.4 | — | 批量验证 | — |

### Phase 4: 最难突破（预计 +0.05~0.08）

**目标**: authoring + orchestration 突破 A+

| 步骤 | Skill | 动作 | 预期增幅 |
|------|-------|------|----------|
| 4.1 | authoring | Agent Prompt 增加 "Agent Prompt First" 设计原则；Constraints 增加 "permission escalation prevention" | +0.04 |
| 4.2 | orchestration | Agent Prompt Constraints 重构（7→9 条，增加 recovery 指引）；UX 维度继续优化（当前 9.15 最低） | +0.05 |
| 4.3 | — | 全量验证 + 最终评估 | — |

## 风险与回退

| 风险 | 影响 | 缓解 |
|------|------|------|
| Agent Prompt 过度膨胀 | 超出 context budget | 每个 skill Agent Prompt 控制在 60-80 行 |
| 评分标准漂移 | 增量修补无法突破 | 每轮用 harness-skill-quality-assessor 交叉验证 |
| 改动引入回归 | 触发回归测试失败 | 每步改动后运行 `python3 scripts/run-all.py` |

## 成功标准

- [ ] commit-gate 评分 ≥ 9.50（A+）
- [ ] 平均分 ≥ 9.55
- [ ] A+ 数量 ≥ 9/13
- [ ] 全量验证通过（PASS=48）
- [ ] 无 CRITICAL/HIGH/MEDIUM 级别问题

## 时间估算

| Phase | 预计耗时 | 累计 |
|-------|----------|------|
| Phase 1 速赢 | 30 分钟 | 30 分钟 |
| Phase 2 结构性重构 | 1 小时 | 1.5 小时 |
| Phase 3 深度重构 | 1.5 小时 | 3 小时 |
| Phase 4 最难突破 | 1 小时 | 4 小时 |

---
最后更新: 2026-07-07
