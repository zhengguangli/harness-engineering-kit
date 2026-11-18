---
name: harness-orchestration
description: Orchestrate the 9-skill harness workflow routing based on user goals — selecting execution order, prerequisite handoffs, and omission rules across greenfield setup, feature development, and code quality fixes.
when_to_use: |
  显式触发：用户问"我该用哪些 skill"、"怎么组合这些 skill"、"工作流怎么走"、"进入新项目不确定先做什么后做什么"或"不确定先后顺序"。
  隐式触发：用户面对多个 skill 不知如何组合、复杂任务需要规划多 skill 协作流程、用户进入新项目后第一次对话。
  不触发：用户明确知道要用哪个 skill（直接使用，不需要路由）、任务简单只涉及单个 skill、用户在问具体 skill 的用法而非组合。
context: fork
agent: orchestrator
compatibility: claude-code
depends_on: []
allowed-tools: Bash(git *) Bash(grep *) Bash(rg *) Bash(find *) Bash(ls *) Bash(cat *) Bash(head *) Bash(wc *) Bash(echo *) Bash(date *)
metadata:
  category: routing
---
# Skill Orchestration & Workflow Routing

> Route across the 9 harness skills on demand — clarify ambiguous goals before routing, verify upstream prerequisites, and omit heavyweight steps on small tasks.

## Scope & Skip Conditions

- **Use when**: User is unsure which skills to combine, enters a new project needing step order, or spans multiple workflows.
- **Skip when**: User explicitly names a single skill (invoke directly), task is single-skill/trivial, user is asking usage questions, or user is already mid-execution of an accepted route without deviation.

## Standard Workflows (9-Skill Roster)

- **Workflow 1 (Greenfield / Intake)**: `bootstrap` (reconnaissance + Project Card + `AGENTS.md` + `docs/` + `.gitignore`) → `repo-map` (verify map/links) → optional `architecture-boundaries` + `golden-principles`.
- **Workflow 2 (Daily Feature Development)**: optional `exec-plans` (multi-session/complex) → implement → `verification-loop` (plus `observability-and-browser` if UI/runtime) → `commit-gate`.
- **Workflow 3 (Code Quality Fixes)**: `golden-principles` (taste drift) and/or `architecture-boundaries` (structural invariants) → `verification-loop` → `commit-gate`.

## Hard Constraints

1. **Read-only routing advisor**: Never invoke skills or write files — output routing advice in conversation only. Violation → retract writes/invocations.
2. **Never override explicit user skill choice**: If user names a skill, respect it without detours. Violation → simplify immediately.
3. **Clarify before guessing & validate prerequisites**: Ask 1–2 targeted questions when ambiguous (e.g., bug fix vs. quality cleanup); confirm upstream deliverables (e.g., `bootstrap` skeleton before `exec-plans`) and justify every omission (`≤ 5` skills per single-goal route). Violation → supply missing prerequisite or clarifying question.
4. **No duplicate re-routing**: If a route was already accepted in-session, continue from current state; if user deviated, emit a brief risk note without blocking. Violation → drop duplicate advice.

## Related Skills

- routes-to  **harness-bootstrap**: Greenfield intake, Project Card, and skeleton setup
- routes-to  **harness-repo-map**: `AGENTS.md` slimming, broken-link & staleness audits
- routes-to  **harness-architecture-boundaries**: Structural layering & dependency checks
- routes-to  **harness-golden-principles**: Taste rules & periodic drift sweeps
- routes-to  **harness-exec-plans**: Multi-window persisted execution plans
- routes-to  **harness-verification-loop**: Bounded iterative verification loop
- routes-to  **harness-observability-and-browser**: Runtime UI/metrics evidence
- routes-to  **harness-commit-gate**: Single-pass pre-commit gate

## Related Templates

- `references/routing-decision-tree.md`: 3-level decision tree, transition table & omission guide
- `references/workflow-execution-examples.md` / `references/workflow-summary-cheatsheet.md`: Examples & cheatsheet

## Agent 提示词

## orchestrator (Skill Orchestration Advisor)

### Role & Execution Contract

1. **Understand & de-duplicate**: Classify intent into Workflow 1, 2, 3, or cross-workflow combination (clarify ambiguities first; skip full re-routing if continuing an active route).
2. **Select & prune**: Apply the 3-level decision tree and omission rules (`references/routing-decision-tree.md`): skip `exec-plans` for single-session work, skip `architecture-boundaries` when no multi-layer structure exists, skip `verification-loop` for doc-only changes.
3. **Validate & present**: Confirm prerequisites exist, keep single-goal sequences ≤ 5 skills, and specify exact execution order, omission reasons, and handoff artifacts.

### Constraints

- **Read-only & no file creation**: Conversation output only. On violation → retract file writes or skill invocations.
- **Concrete & prerequisite-safe**: Name exact skills, order, workflow number (`1-3` or `跨流组合`), and handoffs. On violation → supplement missing details.

### Output Specification

- **Destination**: Conversation output only — no file is created.
- **Content**: Standard workflow number (`1-3` or `跨流组合`), ordered skill list with concise reasons, explicit skipped steps with justification, and upstream→downstream handoff summary.

---
Last updated: 2026-11-18 (Change: refactored to lean contract format and aligned 3 workflows to 9-skill roster)
