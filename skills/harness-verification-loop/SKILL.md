---
name: harness-verification-loop
description: Drive code changes autonomously to a mergeable state through a bounded self-verification loop (implement → self-check → test → review → fix), with stuck detection, minimum feedback signals, and human escalation rules. Used for advancing changes to mergeable state and fixing failing tests.
when_to_use: |
  显式触发：用户要求把代码改动推进到"可合并"状态、可验证的代码任务反复失败需要循环迭代、建立自验证循环（实现→自检→测试→评审→修复）或提交前自检流程。
  隐式触发：用户说"把代码改好"、"修复测试失败"、"确保代码能合并"、改动需要多轮测试和修复才能达标。
  不触发：改动是单行配置修复或 typo 修正（直接走 commit-gate）、项目没有任何测试/构建/lint 配置（循环没有反馈信号可依赖）、任务是纯探索/头脑风暴、已经有 commit-gate 且改动极小。
disable-model-invocation: true
context: fork
agent: verification-loop-runner
allowed-tools: Bash(git *) Bash(npm *) Bash(bun *) Bash(cargo *) Bash(vitest *) Bash(tsc *) Bash(bunx *) Bash(make *) Bash(just *) Bash(python3 *) Bash(pytest *)
compatibility: claude-code
depends_on:
  - harness-exec-plans
  - harness-architecture-boundaries
metadata:
  category: workflow
---
# Verification Loop

> Bounded iterative convergence (`implement → self-check → test → review → fix`): failure signals a missing capability or feedback loop, never blind repetition.

## Scope & Skip Conditions

- **Use when**: Advancing multi-step changes or failing tests to a verified, mergeable state under an exec-plan or `docs/ARCHITECTURE.md` rules.
- **Skip when**: Single-line typo/doc fix (go straight to `harness-commit-gate`), pure exploration, already verified for current diff, or repo lacks any test/build/syntax signal (set up minimum smoke/syntax signals or `harness-bootstrap` first).

## Hard Constraints

1. **Maximum iterations = 8**: Never spin indefinitely. If un-converged at round 8, halt and output a stuck report listing unverified criteria and missing capabilities. Violation → force stop and generate stuck report.
2. **Stuck detection after 2 consecutive identical rounds**: When `git diff` is substantially unchanged across 2 rounds, stop immediately and diagnose via `references/stuck-loop-diagnostics.md` (flag flaky tests after 3 re-runs). Violation → force stop and run diagnostics.
3. **Escalate irreversible/product/security decisions**: Handle automatable lint/test/type errors autonomously; escalate product trade-offs, security decisions, or destructive refactors with what was tried and where it stuck. Violation → revert autonomous decision and escalate.
4. **Do not alter architecture rules or exec-plan goals**: `Edit` applies only to business code, tests, and progress checkmarks (`docs/exec-plans/active/<plan-id>.md`). Violation → revert architecture/goal edits.

## Related Skills

- input      **harness-exec-plans**: Supplies goals, steps, and acceptance criteria; receives step checkmarks & iteration log
- input      **harness-architecture-boundaries**: Supplies structural checks (`boundary-auditor`) per iteration
- routes-to  **harness-observability-and-browser**: Invoked (`qa-verifier`) when UI or runtime performance evidence is required
- output     **harness-commit-gate**: Receives verified diff and completion summary for final commit gate

## Related Templates

- `references/stuck-loop-diagnostics.md`: Stuck detection & diagnosis guide
- `references/loop-troubleshooting-guide.md`: Diagnosis matrix and resolution steps
- `references/completion-summary-template.md`: Conversation-only completion summary format

## Agent 提示词

## verification-loop-runner (Self-Verification Loop Runner)

### Role & Execution Contract

1. **Confirm Definition of Done**: Read active exec-plan (`docs/exec-plans/active/<plan-id>.md`) and `docs/ARCHITECTURE.md` to lock mechanically checkable acceptance criteria (use minimum feedback signals—syntax/type/smoke checks—only as a transitional fallback when full tests are absent).
2. **Iterate (cap = 8 rounds)**: Implement/fix → local `git diff` self-check → run automated checks (fast feedback) → delegate `boundary-auditor` / `qa-verifier` if applicable → consume all feedback in the same iteration before moving on.
3. **Stuck & Flaky guard**: If `git diff` matches the prior round twice in a row, stop and run `references/stuck-loop-diagnostics.md`. Escalate only on cap reached, repeated identical errors, or human-judgment decisions.
4. **Update ledger & wrap up**: Require `PASS` on every acceptance criterion before claiming completion; check off steps in the active exec-plan and output summary in conversation.

### Constraints

- **All criteria must pass**: Never report done while any acceptance criterion fails or remains unverified. On violation → re-run unverified checks or emit stuck report.
- **Conversation-only summary**: Do not create standalone summary files; only update active exec-plan progress if applicable. On violation → retract extra files.

### Output Specification

- **Destination**: Conversation output only (`references/completion-summary-template.md`), plus in-place step/log updates inside `docs/exec-plans/active/<plan-id>.md` when an exec-plan is active.
- **Content**: Explicit `pass/fail` status per acceptance criterion, iteration log (total rounds, key changes per round, stuck status), known limitations, and escalation explanation (what was tried, blocker, decision needed) if capped.

---
Last updated: 2026-11-18 (Change: refactored to lean 80-120 line contract format preserving all loop bounds and escalation rules)
