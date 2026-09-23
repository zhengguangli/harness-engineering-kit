# Core Beliefs

Defines the agent-first operating principles of the harness-engineering-kit. These are judgments that have been repeatedly confirmed and are worth long-term preservation, not temporary preferences.

## Beliefs

1. **"看不见就不存在"**: Any knowledge that exists only in chat history or verbal consensus is effectively nonexistent for an agent. New architectural consensus and product decisions must be recorded in the corresponding `docs/` files to be considered "effective."

2. **"约束不变量，不管实现细节"**: Architectural boundaries must be mechanically enforced, but the specific implementation details within those boundaries are free. A skill's frontmatter format is a contract; the methodology writing within can be flexible.

3. **"计划是工件，不是草稿"**: Plans for complex tasks must be persisted, versioned, and readable by subsequent agents in relay. An exec-plan is not a scratch note — it is the baton passed across context windows.

4. **When failing, first ask "缺了什么能力"**: Do not default to "try again" as the fix. The core of the Ralph Wiggum Loop: failure → identify missing capability → add skill/tool → retry.

5. **"熵增需要持续清扫，不要攒成大扫除"**: Technical debt is a high-interest loan; small, continuous repayments are more economical than batch cleanups. The periodic scanning of golden-principles exists precisely for this purpose.

6. **"渐进式披露，不要一次性灌入"**: An agent's context budget is a scarce resource. CLAUDE.md is the map — it holds only pointers; `docs/` holds the details. Skills use `when_to_use` to control loading timing.

7. **"跨平台兼容是设计约束，不是事后补丁"**: SKILL.md frontmatter is designed so that each platform reads only the fields it recognizes and ignores unknown fields. When adding a new field, the behavioral differences across three platforms must be considered.

8. **"并行度服从边际收益,不要为'全自动'堆数量"**: Running multiple subagents in parallel incurs triple overhead: coordination, context pollution, and cost. 3-4 is the sweet spot (task scale is manageable, output is aggregatable, timeout risk is low); unless there are clearly independent modules (e.g., reviewing each of 12 SKILL.md files once), 1-2 serial with occasional small-scale parallelism is more stable. subagent count > number of work units = waste.

9. **"已完成任务的详细清单应压缩为摘要"**: After an exec-plan is archived, the detailed step-by-step list (especially with line numbers) quickly goes stale as code changes. Retain a three-paragraph summary of "what was accomplished + key decisions + verification results" and delete the line-by-line details. The same applies to tech-debt-tracker — processed items should be compressed into a one-line completion record, not preserved as a 20-row stale table.

10. **"Agent 提示词结构一致性需要机械强制"**: Across skills, agent prompts can suffer from structural issues such as heading-level drift (h2/h3/h4 mixed), missing output specifications, and duplicate prohibition rules. Define a standard six-section format (Role Definition / Core Capabilities / Execution Flow / Constraints / Output Specification / Skip Conditions), mechanically verified by doc-gardener's "pairing completeness" check.

## 工作方式提示

- 复杂、可能跨多次会话的任务，先用 `harness-exec-plans` 技能落一份 exec-plan，不要直接动手。
- 改动完成后，跑自验证循环（`harness-verification-loop`）而不是一次性提交了事。
- 提交前跑 `make triggers-all` 确保 frontmatter 校验、关键词一致性、回归测试全部通过。
- 不确定某条规则是否仍然有效？去对应的 docs 文件查"最后校验日期"，过期的规则应该被标记而不是被信任。
- 要给这套体系添加新能力，参考 `harness-authoring` skill。
- **推送代码后**，主动询问用户是否同步技能包到 `~/.claude/skills`，获得允许后执行：

  ```bash
  rsync -av skills/ ~/.claude/skills/
  ```

---
最后更新: 2026-09-23（复核：内容未变更，仅刷新新鲜度戳）
