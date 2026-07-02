# 12 Skills 全量审计（基于 6 区块 Audit Prompt）

- 状态: completed
- 创建日期: 2026-07-02
- 最近更新: 2026-07-02
- 关联 PR / issue: 暂无
- 负责 agent / 人: opencode（主对话） + 用户 review

## 执行摘要

- **多 subagent 并行执行**：12 个 general subagent 并发跑 12 个 skill 的五维评估
- **总建议 49 条**：CRITICAL 4 / HIGH 4 / MEDIUM 21 / LOW 20
- **实际落地 26 条**（4 CRITICAL + 3 HIGH + 19 MEDIUM），20 条 LOW 记入 tech-debt-tracker.md
- **3 个 commit 全部 PASS=30 不退化**：c744c42 / 9904ed9 / f4fcc79
- **关键发现**：`completed/skills-prompt-polish-2026-07-02.md` Phase A 声称清理 3 处死链，实际漏 3 处（plan-architect/qa-verifier/entropy-collector）；元技能 `harness-authoring` 教与硬约束相反的规则

## 目标

用上一轮 `harness-prompt-optimizer` 输出的 6 区块 audit prompt 全量审计 harness-engineering-kit 仓库的 12 个 SKILL.md，产出按"严重程度 → skill → 维度"三段排序的建议清单（含具体文件:行号、当前文本、目标文本、改后效果、effort）。用户在主对话 review 清单后决定采纳哪些条目，被采纳条目由 commit-gate 流程实施。

完成后:12 个 skill 的 frontmatter / 正文 / agent prompt 三段在五维（description_clarity / trigger_precision / frontmatter_consistency / agent_prompt_quality / internal_consistency）下都有明确的"现状/差距/建议修复"三段式记录，且触发回归 30/30 PASS 不退化。

## 范围 / 非目标

**范围内:**
- 12 个 `skills/harness-*/SKILL.md` 的 frontmatter、正文、`## Agent 提示词` section
- `make triggers-all` 校验链基线快照与回归对比
- 用户 review 后采纳的建议条目
- 实施采纳条目后的 commit（按 commit-gate 流程）

**明确不做(非目标):**
- 不动 `agents/openai.yaml`（TD-002 已知）
- 不动 `references/*.md` 子文件
- 不动 `scripts/`、`tests/`、`docs/`
- 不动 `agents/openai.yaml` 与 SKILL.md agent prompt 的内容同步
- 不新增 / 删除 SKILL.md 章节
- 不拆 `references/` 子文件

## 步骤

- [x] 1 — **基线快照**：跑 `make triggers-all 2>&1 | tee /tmp/baseline-2026-07-02.log`，记录 PASS/WARN/FAIL 数字；记录 12 个 SKILL.md 当前行数与 frontmatter 字段。**完成判据**：日志文件存在且三套校验退出码均为 0。
- [x] 2 — **跑 audit prompt**：把 6 区块 prompt 作为 system prompt 喂给新对话窗口（或本对话继续），跑 Step 1-3（建基线 + 五维评估 + 聚合建议）。**完成判据**：产出符合 Output Schema 的 JSON 报告，`recommendations` 数组对 12 个 skill 全部覆盖。
- [x] 3 — **人类 review**：在主对话把 JSON 报告渲染为人类可读清单，用户标注采纳/拒绝/延后。被延后条目记录进 `docs/exec-plans/tech-debt-tracker.md`。**完成判据**：所有 recommendations 条目有 [采纳/拒绝/延后] 标记。
- [x] 4 — **实施被采纳条目**：按采纳条目逐个 Edit，逐文件跑 `make triggers-all` 子目标验证（triggers-check / keyword-consistency / triggers-regression / prompts-sync-check 单独跑）。**完成判据**：所有采纳条目已落盘且未触发任何校验失败。
- [x] 5 — **全量验证**：跑 `make triggers-all` 全量，确认 PASS=30 不退化。**完成判据**：Summary 行显示 PASS=30 WARN=0 FAIL=0。
- [x] 6 — **commit 与归档**：按 commit-gate 流程逐个或批量 commit（commit message 用 `chore(skills): ...` 句式）；移动本文件到 `docs/exec-plans/completed/`，补充变更记录。**完成判据**：`git log --oneline` 出现对应 commit + 本文件路径在 `completed/` 下。

## 决策日志

| 日期 | 决策 | 理由 | 被否决的备选方案 |
|---|---|---|---|
| 2026-07-02 | 用 audit prompt 而不是手工逐文件审查 | 保证五维评估口径一致、节省时间、符合 prompt-optimizer 自身方法论 | 手工逐文件审视——12 个 skill × 5 维 = 60 次主观判断，口径容易漂移 |
| 2026-07-02 | 落盘 exec-plan 而非临时轻量计划 | 跨多次决策点（审计 → review → 实施 → 验证 → 归档），可能被中断，需可回溯"上一轮 review 到哪了" | 临时对话内计划——一旦对话窗口切换或压缩，进度丢失 |
| 2026-07-02 | 不动 openai.yaml | 已知 TD-002，本次范围聚焦 SKILL.md 三段 | 同步 openai.yaml——超出范围，且需要升级 `validate-agent-prompt-sync.sh` 才能机械校验 |
| 2026-07-02 | 单文件建议数 ≤ 8 条 | 与 prompt 自约束一致，避免信息过载 | 不设上限——LLM 在冗长清单下容易违反"不制造噪音"原则 |

## 验收标准

- [ ] 12 个 skill 全部出现在审计报告中（`recommendations` 或 `skipped_dimensions` 至少一处）
- [ ] 触发回归 PASS 数量不下降（基线 PASS=30，验收时 ≥ 30）
- [ ] 每条采纳建议含：文件:行号、当前文本、目标文本、effort 标签
- [ ] 单文件 suggestions 数 ≤ 8 条（违反则合并）
- [ ] 全部采纳条目已 commit 且 commit message 符合 `chore(skills):` 风格、≤ 72 字符
- [ ] 延后条目已写入 `tech-debt-tracker.md`
- [ ] `make triggers-all` 退出码 0

## 风险 / 已知未知

- **LLM 五维评估漂移风险**：5 维评分是 LLM 主观判断，可能漏判或重复建议。**缓解**：跑完后人工抽查 3 个 skill 的评估结果，若发现系统性问题（连续 3 个 skill 同一维度漏判）则调整 audit prompt 的 tie-breaker 规则。
- **采纳冲突风险**：多条建议可能影响同一段文本（如 description 删词 vs description 改句式），逐条应用时可能产生冲突 diff。**缓解**：同一文件的多条采纳在一次 commit 中完成，避免中间状态污染 `make triggers-all`。
- **触发关键词命中风险**：description 改词时若无意删除 `SKILL_KW[]` 数组中的关键词，`validate-keyword-consistency.sh` 会失败。**缓解**：实施每条建议前对照 `scripts/run-trigger-regression.sh` 第 20-32 行的关键词表。
- **跨会话接力状态丢失风险**：本计划可能跨多次会话。**缓解**：每完成一步立即勾选步骤状态，每轮会话开头从 active 目录读本文件恢复进度。

## 变更记录

- 2026-07-02: 创建计划，状态 active
- 2026-07-02: 12 subagent 并行完成五维审计，49 条建议
- 2026-07-02: 26 条落地（4 CRITICAL + 3 HIGH + 19 MEDIUM），3 个 commit 全部 PASS=30
- 2026-07-02: 20 条 LOW 记入 tech-debt-tracker.md (TD-003)
- 2026-07-02: 移动到 completed/
