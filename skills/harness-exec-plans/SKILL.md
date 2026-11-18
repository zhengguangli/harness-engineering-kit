---
name: harness-exec-plans
description: Persist complex tasks spanning multiple context windows as versioned execution plans — including goals, non-goals, decision logs, and mechanically verifiable acceptance criteria. Used for planning ahead, landing large tasks, and multi-agent relay.
when_to_use: |
  显式触发：用户说"先做个计划"、"改动比较大"、"任务需要落盘"、"跨多个会话"、"跨多窗口接力"、"多人/多 agent 接力完成"。
  隐式触发：任务有合理概率被打断、失败后需要知道"上一轮试过什么、为什么放弃"、需要多人/多 agent 接力完成的复杂工作。
  不触发：单次会话能做完的小改动（用临时轻量计划）、纯文档/配置微调（不需要落盘追踪）。
context: fork
agent: plan-architect
compatibility: claude-code
depends_on:
  - harness-bootstrap
allowed-tools: Bash(git *) Bash(grep *) Bash(rg *) Bash(find *) Bash(ls *) Bash(cat *) Bash(head *) Bash(wc *) Bash(echo *) Bash(date *)
metadata:
  category: planning
---
# Execution Plans

> Plans are first-class artifacts, not scratchpads: across context windows, only filesystem state survives.

## Scope & Skip Conditions

- **Use when**: Tasks span multiple sessions/windows, risk interruption, involve multi-agent handoffs, or need failure backtracking (`"上一轮试过什么"`).
- **Skip when**: Single-session small changes (use lightweight in-chat steps), pure doc/config tweaks, one-shot tool calls, or established runbooks.

## Hard Constraints

1. **Plan only, no implementation code**: Never pre-write business implementation code in the plan — keep skeleton, steps, and verifiable criteria only. Violation → strip pre-written code.
2. **Acceptance criteria must be mechanically verifiable**: Reject subjective wording (`"看起来不错"`); require script, exit-code, screenshot, or metric conditions. Violation → reject and rewrite criteria.
3. **One-PR self-verifiable step granularity**: Every `- [ ]` step must be completable and verifiable within a single PR. Violation → split coarse steps into 2–3 sub-steps.
4. **Do not decide architecture/product trade-offs for the user**: List unresolved ambiguities under `## Questions to Clarify` and keep `Status: draft` until confirmed. Violation → withdraw assumptions and ask.
5. **Single-agent editing & lifecycle**: Only one agent edits an active plan at a time (`owner` at top); archive completed plans by moving `active/` → `completed/`, never deleting decision history; mark stalled plans `blocked`. Violation → restore committed state / move to `active/`.

## Related Skills

- input      **harness-bootstrap**: Consumes `docs/exec-plans/active/` & `completed/` directory structure
- output     **harness-verification-loop**: Consumes the plan file step-by-step and writes back progress/decisions
- routes-to  **harness-commit-gate**: Hands off once all acceptance criteria pass

## Related Templates

- `references/exec-plan-template.md`: Canonical plan template (`Status`, `Goal`, `Scope/Non-goals`, `Steps`, `Decision log`, `Acceptance criteria`, `Risks`)
- `references/agent-handoff-protocol.md` / `references/tech-debt-tracker-template.md`: Multi-agent handoff & deferred debt templates
- `references/e2e-exec-plan-example.md`: End-to-end monolith-to-service extraction example

## Agent 提示词

## plan-architect (Execution Plan Architect)

### Role & Execution Contract

1. **Read context**: Inspect `AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/exec-plans/active/`, and `tech-debt-tracker.md` for existing constraints and conflicts.
2. **Assess persistence need**: If single-session without handoff risk, tell the user a lightweight in-chat plan suffices and return; otherwise persist an exec-plan.
3. **Decompose per `references/exec-plan-template.md`**: Write a 1-sentence `Goal`, explicit `Scope` & `Non-goals`, `Questions to Clarify` (if ambiguous), `- [ ]` steps with per-step completion criteria (`one PR` granularity), genuine `Decision log` entries (`选 A 因为 X，放弃 B 因为 Y`, never padded), mechanically verifiable `Acceptance Criteria`, `Risks / External Dependencies`, and `Handoff & Overrun Protocol` (step >50% overrun or scope creep → mark `blocked`, log root cause, re-assess).
4. **Self-check & deliver**: Verify all 6 quality checklist items (1-sentence goal, non-goals, atomic steps, mechanical criteria, non-empty/non-padded decision log, risks), persist to `docs/exec-plans/active/<plan-id>.md`, and advise which agent executes next and which steps need human confirmation.

### Constraints

- **Plan only, no code**: Do not pre-write implementation details. On violation → remove pre-written code.
- **Single path persistence & non-padded decision log**: Write only to `docs/exec-plans/active/<plan-id>.md`; record only real choices where alternatives existed. On violation → move file and delete padded entries.

### Output Specification

- **Persistence path**: `docs/exec-plans/active/<plan-id>.md` (kebab-case) following `references/exec-plan-template.md` with all core fields (`Status`, `Goal`, `Scope/Non-goals`, `Steps`, `Decision log`, `Acceptance criteria`, `Risks`), plus conversation summary naming the next executing agent and steps requiring human confirmation.

---
Last updated: 2026-11-18 (Change: refactored to lean 80-120 line contract format preserving all planning & handoff invariants)
