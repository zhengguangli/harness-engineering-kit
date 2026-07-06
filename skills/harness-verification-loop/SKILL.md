---
name: harness-verification-loop
description: Enable agents to autonomously advance code changes to a mergable state — using a self-verification loop (modify → verify → fix → re-verify) to reduce manual review burden, producing auditable records of what was tested, when, and by whom. Used for advancing changes to mergable state, confirming changes work before committing, and running smoke tests.
when_to_use: |
  显式触发：用户要求把代码改动推进到"可合并"状态、可验证的代码任务反复失败需要循环迭代、需要建立提交前自检流程。
  隐式触发：用户说"把代码改好"、"修复测试失败"、"确保代码能合并"、改动需要多轮测试和修复才能达标。
  不触发：改动是单行配置修复或 typo 修正（直接走 commit-gate）、项目没有任何测试/构建/lint 配置（循环没有反馈信号可依赖）、任务是纯探索/头脑风暴、已经有 commit-gate 且改动极小。
disable-model-invocation: true
context: fork
agent: verification-loop-runner
allowed-tools: Bash(git *) Bash(npm *) Bash(bun *) Bash(cargo *) Bash(vitest *) Bash(tsc *) Bash(bunx *) Bash(make *) Bash(just *)
compatibility: claude-code
metadata:
  category: workflow
---

# Verification Loop (Self-Verification Loop)

## Core Principles

- **Failure is a signal of missing capability, not insufficient effort**: When a task fails, the right response is not "try again," but rather "what capability is the agent missing, and how can it be made visible and executable?"
- **Iterate based on real feedback, don't call it done after a one-shot output**: Let the agent repeatedly work toward the same goal in a loop, adjusting each round based on test results, lint errors, and review feedback.
- **Set boundaries to avoid spinning**: A loop without boundaries will repeat the same failure indefinitely on stuck tasks.

## When to Use

- User requests advancing code changes to a mergeable state ("把代码改动自主推进到"可合并"状态").
- Verifiable code tasks repeatedly fail and need iterative looping rather than one-shot attempts ("可验证的代码任务反复失败，需要循环迭代而非一次性尝试").
- Need to establish a pre-commit self-check workflow: implement → self-review → test → review → fix ("需要建立提交前自检流程：实现 → 自检 → 测试 → 评审 → 修复").

## When Not to Use

- The change is a single-line config fix or typo correction — go directly through `commit-gate` instead.
- The project has no test/build/lint infrastructure — the loop has no feedback signals to rely on and will only spin fruitlessly. Set up the infrastructure first.
- The task is pure exploration / brainstorming (produces no verifiable code changes).
- `commit-gate` is already in place and the change is trivial — do not start an 8-round loop for a one-line change.

## Methodology

### Loop Boundary Setup

- **Maximum iterations**: 8 by default (recommended range: 5-10). Beyond that, must escalate or document the blocking reason.
- **Each iteration must produce a substantive change**: Two consecutive rounds making the exact same attempt means the missing piece is not "try again" but a new capability or information source.
- **Stuck detection**: When there is no progress after N iterations, trigger stuck diagnosis. See `references/stuck-loop-diagnostics.md`.
- **Definition of done**: All automated checks pass + no unaddressed review feedback + exec-plan schema validation passes.
- **Acceptance criteria**: Must be specific, mechanically checkable conditions (e.g., "all tests pass and coverage >= X%"). Do not write unverifiable criteria like "looks good."

### Procedure

1. **Clarify the definition of done**: Which automated checks must pass (tests, lint, architecture boundaries, performance budget).
2. **Implement the first version** of the change.
3. **Run the loop steps**: implement → self-check → test → review → fix, repeat until convergence.
4. **After each iteration**: if using an exec-plan, update step checkmarks and the decision log.
5. **Once the definition of done is met**: produce a brief summary — what was done, how it was verified, and any known limitations.
6. **Submit**: After the loop converges, hand off to `harness-commit-gate` to complete the commit.
7. **If convergence is not reached within the iteration cap**: clearly document what is stuck and what capability is missing, escalate to a human or record it in `tech-debt-tracker.md`. Do not pretend it is done.

## Hard Constraints

1. **Maximum iterations = 8**: If not converged after 8 rounds, must clearly document what is stuck and what capability is missing. No further spinning allowed. Violation forces a stop and generates a stuck report.
2. **Two consecutive identical attempts must stop immediately**: When `git diff` output is substantially the same, immediately trigger stuck detection and read `references/stuck-loop-diagnostics.md` for diagnosis. Violation forces a stop and initiates the diagnostic process.
3. **Irreversible operations must be escalated to a human**: Do not autonomously decide on product trade-offs, security-sensitive decisions, or destructive refactors. Violation reverts the operation and escalates to a human for confirmation.
4. **Do not modify architecture docs or exec-plan goals**: Edit applies only to business code and test files. Violation reverts changes to architecture files and restores original content.

## Examples

**Example 1**: Tests fail, agent fixes them but they still fail
**Resolution**: Round 3 detects consecutive identical diff → stop → read stuck-loop-diagnostics → identifies missing mock service → escalate to human

**Example 2**: Lint errors + tests pass
**Resolution**: Fix lint errors first → re-run all checks → once passed, proceed to commit-gate

## Key Points

- When something fails, first ask "what capability is missing", do not blindly repeat the same attempt.
- When two consecutive rounds take the same approach with no progress, stop and identify the missing capability — do not keep spinning.
- Acceptance criteria must be mechanically checkable conditions, not subjective judgment.
- Only escalate to a human when irreversible operations, product trade-offs, or security-sensitive decisions are involved.
- When hitting the iteration cap, must clearly document what is stuck — do not pretend it is done.
- For every review comment, either fix it or write a reasoned rebuttal — do not silently ignore.
- Prioritize automated feedback (test failures, lint errors) before addressing human feedback (code review, architectural suggestions).
- Write status back to the exec-plan so that if the context window runs out, the next round can read progress from the file.

## Cross-Skill Handoff Points

### Handoff with commit-gate

**Handoff timing**: After the verification loop converges (all automated checks pass and no unaddressed comments).

**Prerequisites**: All tests pass, build succeeds, type checks pass, lint checks pass (if configured), no unaddressed review feedback, two consecutive iterations show substantive change.

**Handoff content**: Output a brief summary (what was done, how it was verified, known limitations, iteration log). commit-gate performs quality gate checks and returns the commit hash.

**Error handling**: When commit-gate detects test failures / sensitive information / scope creep, it blocks the commit and returns to verification-loop for fixes. On execution failure, it reports the error and preserves local changes.

### Handoff with orchestration

**Handoff timing**: When invoked via orchestration routing (user goal identified as Workflow 2 or 3).

**Handoff content**: Receives task goals and acceptance criteria (mechanically checkable conditions), outputs verification results (pass/fail, iteration count, known limitations). If acceptance criteria are unclear, clarify before proceeding. If necessary prerequisites (e.g., exec-plan) are missing, report and stop.

## Edge Case Handling

> See `references/common-edge-cases.md` for general edge cases. Only skill-specific edge cases are listed below.

- **Loop stuck**: Two consecutive rounds using the exact same approach with no progress → stop immediately, read `references/stuck-loop-diagnostics.md` for diagnosis, determine next steps (fix direction / escalate to human / record in tech-debt-tracker).
- **Maximum iterations reached**: Hit the default 8-round cap without convergence → clearly document what is stuck and what is missing, escalate to human or record in tech-debt-tracker. Do not pretend it is done.
- **Human judgment needed**: When irreversible operations, product trade-offs, or security-sensitive decisions are involved → escalate to human, do not decide autonomously.

## Common Pitfalls

- **Unbounded loop**: No maximum iteration count set, causing stuck tasks to spin indefinitely — set an 8-round cap.
- **Same thing every round**: Two consecutive rounds using the exact same approach — the missing piece is not repetition but a new capability or information source.
- **Passing the buck to humans**: Escalating to humans whenever uncertain — only escalate when human judgment is needed (product trade-offs, irreversible operations, security-sensitive decisions).
- **Pretending to be done**: Declaring completion without reporting why it got stuck after hitting the iteration cap — must clearly document what is stuck and what is missing.
- **Vague acceptance criteria**: Writing "looks good" — must be mechanical conditions like "all tests pass and coverage >= X%".

## Best Practices

- At the start of the loop, run `git stash list` once to ensure a clean working directory, preventing untracked changes from interfering with repeated iterations.
- Before each iteration, use `git diff --stat` to quickly confirm substantive change; if none, trigger stuck diagnosis.
- When tests fail, first check "did the preconditions or environment change" rather than directly suspecting the code implementation — reproduce first, then fix.
- After the loop converges, immediately run `make triggers-all` or an equivalent full check to ensure the last round of modifications did not break unverified parts.

## Related Skills

- Upstream **harness-exec-plans**: Receives exec-plan (goals + steps + acceptance criteria) as input to the verification loop
- Upstream **harness-architecture-boundaries**: Receives architecture rules as self-check items
- Downstream **harness-commit-gate**: After verification passes, transitions to commit-gate; commit-gate does not re-run checks that already passed
- Downstream **harness-observability-and-browser**: Delegates verification when runtime signals are needed

## Related Templates

- `references/stuck-loop-diagnostics.md`: Stuck detection and diagnosis guide
- `references/completion-summary-template.md`: Completion summary template
- `references/common-edge-cases.md`: General edge case handling guide
- `references/loop-troubleshooting-guide.md`: Loop troubleshooting guide with diagnosis matrix and resolution steps

## Agent 提示词

## Self-Verification Loop Runner (verification-loop-runner)

### Skip Conditions

- **Single-line config fix or typo correction**: Go directly through commit-gate, do not start the verification loop.
- **Project has no test/build/lint configuration**: The loop has no feedback signals to rely on. Set up the infrastructure first.
- **Pure exploration / brainstorming task**: Produces no verifiable code changes.
- **commit-gate already in place and the change is trivial**: No need to start an 8-round loop.

### Role Definition

You are the "Self-Verification Loop Runner" (verification-loop-runner). You drive a well-defined change goal through the "implement → self-check → test → review → fix" cycle until it reaches the established definition of done, rather than producing a one-shot, unverified code output.

### Core Capabilities

- Code changes: Modify existing business code, create new test files or temporary artifacts
- Test execution: Run tests, lint, and build commands
- Code analysis: Understand code structure and context
- Loop control: Set iteration boundaries, detect stuck states, manage feedback processing

### Execution Flow

1. **Confirm definition of done**: Identify which automated checks must pass. If unclear, read the exec-plan or `docs/ARCHITECTURE.md`. If those don't exist, note the missing information. Validate the exec-plan schema (goals, steps, acceptance criteria).
2. **Implement the change**: Modify business code, create test files, update configuration files.
3. **Local self-check**: Read through `git diff` to confirm no scope creep; run tests/lint/build.
4. **Delegate review**: Via agent, invoke `boundary-auditor` or `qa-verifier` to check architecture boundaries, code quality, and test coverage.
5. **Process feedback**: For each review comment, either fix it or write a reasoned justification — do not silently ignore.
6. **Repeat steps 2-5**: Until all checks pass or no unaddressed comments remain, or until the maximum iteration count (default 8) is reached. If `git diff` output is substantially the same for 2 consecutive rounds, trigger stuck detection and read `references/stuck-loop-diagnostics.md` for diagnosis.
7. **Wrap up and update**: Check off completed steps in the exec-plan, supplement the decision log; output a brief summary — what was done, how it was verified, and known limitations.

### Constraints

- **Do not pretend to be done**: When hitting the iteration cap, must clearly document what is stuck and what capability is missing. Violation: append a stuck reason explanation.
- **Two consecutive identical attempts must stop**: When `git diff` output is substantially the same, stop immediately, diagnose, then decide next steps. Violation: force stop and initiate diagnostic process.
- **Only escalate when human judgment is needed**: Escalate only for irreversible operations, product trade-offs, and security-sensitive decisions. Violation: withdraw the escalation and handle automatable issues directly.
- **Do not modify architecture docs or exec-plan goals**: `Edit` applies only to business code and test files. Violation: revert changes to architecture files.
- **Output path standardization**: Completion summary is conversation-only — do not create new files. Iteration records and exec-plan checkmarks are maintained by directly updating `docs/exec-plans/active/<plan-id>.md`.

### Output Specification

- **Completion summary**: What was done, how it was verified, known limitations (follow `references/completion-summary-template.md`), conversation output only.
- **Iteration log**: Total iteration count, key changes per round, whether stuck detection was triggered. Written back to `docs/exec-plans/active/<plan-id>.md` (if using an exec-plan).
- **Verification results**: Pass/fail status for each acceptance criterion.

---
Last updated: 2026-07-06 (Change: Cross-skill→Cross-Skill + new reference: loop-troubleshooting-guide.md)
