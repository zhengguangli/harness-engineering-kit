# Workflow Summary Cheatsheet

> Quick reference table for the five standard workflows. Use when routing a user's goal to determine the right workflow, skill combination, and possible omissions.

## Five Workflows at a Glance

| Workflow | Purpose | Required Skills | Can Omit | When to Use |
|----------|---------|----------------|----------|-------------|
| **1. Greenfield** | Initialize new project harness | `project-intake` → `bootstrap` → `repo-map` → (`architecture-boundaries` + `golden-principles`) | `architecture-boundaries` (small projects) | New project, no existing harness |
| **2. Daily Dev** | Feature implementation | (`exec-plans`?) → implementation → `verification-loop` → `commit-gate` | `exec-plans` (single-session tasks) | New features, bug fixes, enhancements |
| **3. Quality Fix** | Code quality/style cleanup | `golden-principles` → (`architecture-boundaries`?) → `verification-loop` → `commit-gate` | `architecture-boundaries` (no structural issues) | Code style drift, taste inconsistencies |
| **4. Harness Extend** | Add new skill/agent | `authoring` → (`bootstrap`?) → `repo-map` | `bootstrap` (if structure exists) | Extending the harness system |
| **5. Prompt Optimize** | Improve prompt quality | `prompt-optimizer` (standalone) | All others | Prompt optimization only |

## Common Routing Decisions

| User says... | Default workflow | Clarifying question needed? |
|-------------|-----------------|----------------------------|
| "初始化" / "新建项目" | W1 | No |
| "实现" / "添加" / "开发" | W2 | "是功能开发还是修复问题？" |
| "修复" | W2 or W3 | "功能缺陷还是代码质量？" |
| "清理" / "重构" / "质量" | W3 | No |
| "新建 skill" / "新 agent" | W4 | No |
| "优化 prompt" | W5 | No |

## Workflow Ordering Rules

1. **Workflow 1 must start with `project-intake`** — the bootstrap skeleton depends on the intake card's output. Skipping this step may produce a mismatched skeleton.
2. **Workflow 3 → `architecture-boundaries` is optional** — only include when the user reports structural issues (circular dependencies, layer violations). Pure style problems don't need it.
3. **Cross-workflow combination** — when a goal spans multiple workflows, complete each workflow in order and use the handoff table to confirm upstream deliverables before proceeding.
4. **Small project trimming** — single-file changes in Workflow 2 can skip `exec-plans` and `verification-loop` (use `commit-gate` directly with diff review + quick checks).

## Decision Key

| Abbreviation | Meaning |
|-------------|---------|
| `W1`–`W5` | Workflow 1 through Workflow 5 |
| `→` | Sequential dependency (output → next input) |
| `?` | Optional step — omit based on project scale |
| `()` | Group — execute together, order within group flexible |
