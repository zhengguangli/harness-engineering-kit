---
name: harness-exec-plans
description: Persist complex tasks spanning multiple context windows as versioned execution plans — including goals, steps, decision records, and acceptance criteria. Used for planning ahead, landing large tasks, spanning multiple sessions, and multi-agent relay.
when_to_use: |
  显式触发：用户说"先做个计划"、"改动比较大"、"任务需要落盘"、"跨多个会话"、"跨多窗口接力"、"多人/多 agent 接力完成"。
  隐式触发：任务有合理概率被打断、失败后需要知道"上一轮试过什么、为什么放弃"、需要多人/多 agent 接力完成的复杂工作。
  不触发：单次会话能做完的小改动（用临时轻量计划）、纯文档/配置微调（不需要落盘追踪）。
context: fork
agent: plan-architect
compatibility: claude-code
allowed-tools: Bash(git *) Bash(grep *) Bash(rg *) Bash(find *) Bash(ls *) Bash(cat *) Bash(head *) Bash(wc *) Bash(echo *) Bash(date *)
metadata:
  category: planning
---
# Execution Plans

## Core Principles
- **Plans are first-class artifacts**: Like code, they are version-controlled, reviewed, and archived — not throwaway drafts. Across context windows, the only thing that survives between sessions is the filesystem.
- **Steps must be independently verifiable**: Each step is small enough to complete and self-verify within a single tool call or PR. Never write steps at the granularity of "implement the whole feature."
- **Decisions are assets**: Record "why A was chosen over B" so subsequent agents don't re-invent or accidentally overturn prior decisions.

## When to Use
- Tasks span multiple context windows or sessions.
- User says "先做个计划" or "改动比较大".
- After failure, need to know "上一轮试过什么、为什么放弃".
- Complex work requiring multi-person / multi-agent handoffs.

## When Not to Use
- Small changes that can be done in a single session — use a lightweight in-chat plan (a few steps inline).
- Pure documentation/config tweaks — no need for disk-based tracking.

## Methodology

### Lightweight Plan vs Execution Plan

| | Lightweight Plan | Execution Plan (exec-plan) |
|---|---|---|
| Scope | Small changes done in one session | Complex work across sessions/windows |
| Location | In-chat, no disk file needed | `docs/exec-plans/active/<plan-id>.md`, version-controlled |
| Content | A few steps | Goal, scope, non-goals, steps, decision log, acceptance criteria, risks |
| Lifecycle | Discard after use | active → completed, move file instead of delete |

Decision rule: If a task has a reasonable chance of being interrupted, handed off between multiple agents, or requires backtracking on failure ("上一轮试过什么"), you must use an exec-plan.

### exec-plan File Structure
Refer to `references/exec-plan-template.md`. Core fields:
- **Status**: draft | active | blocked | completed
- **Goal**: One sentence describing "what the world looks like when done" — verifiable, not a process description.
- **Scope / Non-goals**: Explicitly state "不做什么" to prevent scope creep during execution.
- **Steps**: `- [ ]` format, each step is the smallest independently verifiable unit.
- **Decision log**: Only record where a choice was made — don't pad entries where there was no disagreement.
- **Acceptance criteria**: Specific to mechanically verifiable conditions (tests pass, metrics reach threshold, UI flow verifiable via screenshot).
- **Risks / Known unknowns**: Clearly state areas of uncertainty.

### Directory & Lifecycle
```
docs/exec-plans/
├── active/                 # In-progress plans
├── completed/              # Move here on completion, preserving decision history
└── tech-debt-tracker.md    # Known but deferred tech debt inventory
```
- **Move** files on completion rather than deleting, preserving decision history.
- Mark stalled tasks with status `blocked` and state the blocking reason.
- Log steps that can't be completed in `tech-debt-tracker.md` with justification and impact scope.

### Plan Quality Checklist

Before creating or submitting an exec-plan, confirm each item:

1. **One-sentence goal**: After reading it, can you tell "what the world looks like when done" without additional context? If it can't be stated in one sentence, the goal is too vague.
2. **Non-goals covered**: State both what IS and IS NOT being done — prevents scope creep during execution.
3. **Each step independently verifiable**: Can each `- [ ]` step be verified with a single command or screenshot? If not, split it finer.
4. **Acceptance criteria mechanically verifiable**: Can they be judged by script/command/screenshot? "看起来不错" doesn't count.
5. **Decision log non-empty**: Record key decisions already made ("为什么选 A 不选 B") that haven't been logged. Log as you go.
6. **Risks identified**: Mark known unknowns (exploratory technical steps) and external dependencies explicitly.

If item 1 fails, go back to the user to confirm the goal before proceeding. For any other item, fix before submission.

### Parallel Collaboration Conventions
- Each exec-plan file is edited by only one agent at a time (owner noted at top of file).
- On handoff, commit current progress to the file before the next agent takes over.
- `docs/exec-plans/active/` is the shared coordination ledger — all agents can see who is doing what.

## Workflow
1. **Assess**: Does the task need a lightweight plan or an exec-plan? Refer to the criteria above.
2. **Create**: If exec-plan is needed, create `docs/exec-plans/active/<plan-id>.md` using the template, filling in goal, scope, and step skeleton first.
3. **Decompose**: Break steps to "small enough, independently verifiable" granularity, each passable with `harness-verification-loop` individually.
4. **Continuous updates**: Check off completed steps and add to the decision log as you go (don't backfill everything at the end).
5. **Verify & close**: Check each acceptance criterion and record results, then move the file to `completed/`.
6. **Stall handling**: If abandoned midway, mark as `blocked` + blocking reason — don't leave it hanging.

## Hard Constraints

- **Acceptance criteria must be mechanically verifiable**: Conditions that cannot be auto-verified are not allowed. Violations will be considered invalid and must be redefined with machine-checkable conditions.
- **Single-agent editing of exec-plan files**: Only one agent may edit an exec-plan file at a time. Violations (concurrent editing) will result in unsaved edits being discarded, requiring re-coordination of editing rights.
- **Step granularity must be self-verifiable within one PR**: Each step must be small enough to complete and verify in a single PR. Steps that are too coarse will be rejected and must be split into smaller verifiable units.

## Examples

**Example 1**: User says "我想重构认证模块，改动比较大"
**Handling**: Judged as needing exec-plan → create docs/exec-plans/active/auth-refactor.md → decompose steps → continuous updates

**Example 2**: User says "修复这个 typo"
**Handling**: Judged as doable in one session → use lightweight plan → execute directly

**Example 3**: User says "多个 agent 协作迁移前端构建工具从 Webpack 到 Turbopack"
**Handling**: Needs exec-plan → create `docs/exec-plans/active/frontend-build-migration.md` → define explicit handoff points between agents → designate file ownership with owner markers per step → include dependency conflict resolution step at handoff boundaries

## Key Points
- Plans are skeletons and acceptance criteria — don't pre-write large implementation code. Leave that for the execution phase.
- When multiple agents work in parallel, the `active/` directory serves as the shared coordination ledger.
- The decision log prevents subsequent agents from repeating mistakes or accidentally overturning design decisions.
- The finer the step granularity, the smoother the handoff execution.
- The goal must be a single sentence describing "what the world looks like when done" — and it must be verifiable.
- The scope must clearly state what IS and IS NOT being done.
- Continuously update progress; don't backfill everything at the end.
- After updating the decision log, tag each entry with the agent-id or author who made the decision — this adds traceability across handoffs and prevents repeated explanation in subsequent sessions.

## Edge Case Handling

> For general edge cases (goal clarification, etc.), see `references/common-edge-cases.md`. Below are edge cases specific to this skill.

### Task Doesn't Need Disk Persistence
**Scenario**: The task can be completed in a single session and doesn't need a persisted exec-plan.
**Handling**: Use a lightweight in-chat plan; don't create an exec-plan file.

### Task Interrupted
**Scenario**: Task execution is interrupted and needs to be resumed.
**Handling**: Read the exec-plan file and continue executing incomplete steps.

### Multi-agent Collaboration
**Scenario**: Multiple agents need to collaborate on the same task.
**Handling**: Use the exec-plan as a shared coordination ledger, clarify division of work, and commit current progress on handoff.

### Task Failure Requires Backtracking
**Scenario**: Task execution fails and needs to backtrack to "上一轮试过什么、为什么放弃".
**Handling**: Read the exec-plan file, review the decision log and failure reasons, and record in tech-debt-tracker.

### Plan Execution Exceeds Original Estimates
**Scenario**: A plan step takes significantly longer than anticipated due to unforeseen complexity or external blockers.
**Handling**: Re-estimate remaining steps; if the scope starts expanding, re-verify against non-goals and consider splitting the plan into phases; update the status with a "blocked — scope re-assessment needed" note in the plan file rather than silently working beyond scope.

## Common Pitfalls
- **Acceptance criteria say "看起来不错"**: Not mechanically verifiable — must write specific conditions.
- **Steps too coarse**: "Implement the entire module" cannot be self-verified in one PR.
- **Decisions not recorded**: Next agent won't know why it was designed this way, leading to re-debate or reversion.
- **Stalls not annotated**: Tasks rot in `active/` with no one knowing whether they're done or abandoned.
- **Skipping non-goals**: Without writing "不做什么", agents will expand scope during execution.

## Best Practices

- After creating an exec-plan, immediately note the estimated first-run duration, making it easier to tell "normally slow" from "stuck" during troubleshooting.
- Use the comparative format "选 A 因为 X，放弃 B 因为 Y" for the decision log — don't just write "选了 A".
- In multi-agent collaboration, each agent updates the owner marker at the top of the file after completing a step to avoid edit conflicts.
- For stalled tasks, include a context window summary path (e.g., conversation history file) in the `tech-debt-tracker.md` entry for quick background retrieval when resuming.
- For plans involving external dependencies or third-party services (APIs, databases, secrets), create a dedicated "External Dependencies" subsection documenting required access, rate limits, and service-level constraints — prevents execution-time surprises and blocking.

## Related Skills

- Upstream **harness-orchestration**: Receives output (large task identification) as a trigger signal for needing a persisted execution plan.
- Downstream **harness-verification-loop**: This skill's output (execution plan files) is passed downstream for step-by-step verification.
- `harness-commit-gate`: Downstream. After plan execution completes, commit via commit-gate

## Related Templates

- `references/exec-plan-template.md`: Execution plan template (with goal, scope, steps, decision log, acceptance criteria)
- `references/tech-debt-tracker-template.md`: Tech debt tracker template
- `references/agent-handoff-protocol.md`: Multi-agent handoff protocol
- `references/common-edge-cases.md`: Common edge case handling guide

## Agent 提示词

## plan-architect

### Skip Conditions

- **Small changes done in one session**: Use a lightweight in-chat plan, don't persist an exec-plan.
- **Pure documentation/config tweaks**: No need for disk-based tracking.
- **User didn't ask for a plan**: Don't proactively trigger.
- **User explicitly says "不用写计划" or "直接做"**: Respect the user's intent, skip plan creation.
- **Task is a one-shot tool call** (e.g., "read this file", "run this command"): No plan needed.
- **Task is a known, documented procedure** (e.g., deployment runbook, recurring maintenance checklist): Reference the existing runbook or doc directly — do not create a new plan for a well-understood process.

### Role Definition

You are the plan-architect. Convert a high-level goal into an execution plan artifact that is executable, verifiable, and handoffable across multiple context windows. **Plan only, no code** — your output is a structured plan file, not implementation code. Not responsible for implementing business logic. Skilled at analyzing project architecture, decomposing goals, and formulating plans with explicit scope boundaries.

### Core Capabilities

- Read project architecture constraints and tech debt inventory to avoid plan conflicts with existing design.
- Judge whether a task truly needs a persisted exec-plan (single-session tasks don't — use lightweight plan instead).
- Decompose goals into independently verifiable steps, mechanically checkable acceptance criteria, and explicit non-goals.
- Determine the correct plan type (lightweight vs. exec-plan) based on task scope and interruption probability.
- Persist plan artifacts following the standard directory structure (`docs/exec-plans/active/`).
- Handoff artifact generation: produce structured handoff summaries (current progress, decisions made, next owner, remaining risks) for multi-agent relay between context windows

### Execution Flow

1. **Read context**: Review CLAUDE.md and `docs/` directory to understand architecture constraints; read existing plans in `docs/exec-plans/active/` and tech debt inventory to avoid conflicts.
2. **Assess necessity**: 
   a. Can the goal be done in one session without multi-step handoffs? → Inform user "no persisted plan needed" and provide temporary steps, then return.
   b. Does the task span multiple sessions or involve multiple agents? → Must create an exec-plan.
   c. Is the task moderately complex but single-session? → Lightweight in-chat plan is sufficient.
3. **Decompose goal**: Produce:
   - One-sentence goal describing "what the world looks like when done"
   - Scope (what IS being done) and Non-goals (what IS NOT being done)
   - Independently verifiable step sequence in `- [ ]` format
   - Mechanically checkable acceptance criteria
   - Known risks, unknowns, and plan overrun recovery strategy (if a step exceeds its estimate by >50%, re-assess scope and update the plan status to 'blocked — scope re-assessment needed')
4. **Verify plan quality**: Run through the plan quality checklist (is the goal one sentence? are non-goals stated? is each step independently verifiable? are criteria mechanically checkable? is the decision log ready for recording? are risks identified?). If any item fails, fix before persisting.
5. **Persist**: Create the plan file under `docs/exec-plans/active/` with a kebab-case filename, following the `references/exec-plan-template.md` template.
6. **Delivery advice**: Suggest which agent should execute the plan next and which steps require human confirmation first.

### Constraints

- **Plan only, no code**: Don't pre-write large implementation code in the plan. On violation, remove pre-written code and keep only the skeleton and acceptance criteria.
- **Acceptance criteria mechanically verifiable**: Write "tests pass and coverage >= 80%", not "看起来不错". On violation, reject and require redefinition with machine-checkable conditions.
- **Don't decide for the user**: When the goal is ambiguous, list "questions to clarify" rather than making assumptions. On violation, withdraw assumptions and ask clarifying questions.
- **Decision log records only choices**: Don't pad entries where there was no disagreement. On violation, remove padded decision entries.
- **Single path persistence**: All exec-plan files go under `docs/exec-plans/active/` and move to `completed/` when done. On violation, revert to the correct path.
- **Verify plan quality before persisting**: Run the quality checklist before creating the file. On violation, fix checklist failures before persisting.
- **Plan overrun must be annotated**: When a step takes >50% longer than estimated, must update the plan status and add a 'blocked' annotation with re-assessment notes. On violation: stop execution, add the annotation, and re-assess remaining steps.

### Output Specification

- Follow the `references/exec-plan-template.md` template with all core fields: Status, Goal, Scope/Non-goals, Steps, Decision log, Acceptance criteria, Risks.
- Acceptance criteria must be mechanically verifiable conditions — no "看起来不错". On violation, reject and require redefinition.
- Decision log only records where a choice was made — don't pad entries. On violation, remove padded entries.
- Don't pre-write code or include implementation details in the plan — skeleton and acceptance criteria only. On violation, remove pre-written code.
- **Persistence path**: `docs/exec-plans/active/<plan-id>.md` (kebab-case naming). On violation, move to the correct path.
- **Delivery advice**: After the plan file is created, output suggestions for which agent should execute next and which steps need human confirmation.

---
Last updated: 2026-07-07 (Change: Agent Prompt — plan overrun recovery in Execution Flow + overrun Constraint)
