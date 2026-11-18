# Workflow Summary Cheatsheet

> Quick reference table for the three core engineering workflows across the 9 harness skills.

## Three Workflows at a Glance

| Workflow | Purpose | Required Skills | Can Omit | When to Use |
|---|---|---|---|---|
| **1. Greenfield** | Analyze & initialize harness | `bootstrap` → `repo-map` → (`architecture-boundaries` + `golden-principles`) | `architecture-boundaries` (small projects) | New project, no existing harness |
| **2. Daily Dev** | Feature implementation | (`exec-plans`?) → implementation → `verification-loop` → `commit-gate` | `exec-plans` (single-session tasks) | New features, bug fixes, enhancements |
| **3. Quality Fix** | Code quality/style cleanup | `golden-principles` → (`architecture-boundaries`?) → `verification-loop` → `commit-gate` | `architecture-boundaries` (no structural issues) | Code style drift, boundary violations |

## Common Routing Decisions

| User says... | Default workflow | Clarifying question needed? |
|---|---|---|
| "初始化" / "新建项目" / "分析项目" | W1 | No |
| "实现" / "添加" / "开发" | W2 | "是功能开发还是修复问题？" |
| "修复" | W2 or W3 | "功能缺陷还是代码质量？" |
| "清理" / "重构" / "质量" | W3 | No |

## Decision Key

- `W1`–`W3`: Workflow 1 through Workflow 3
- `→`: Sequential dependency (`output → next input`)
- `?`: Optional step — omit based on project scale
