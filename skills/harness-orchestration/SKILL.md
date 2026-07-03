---
name: harness-orchestration
description: Orchestrate skill combinations and workflow routing in the current project — selecting the right skill mix and execution order based on user goals. Used for deciding which skills to use, planning multi-skill collaboration, and navigating workflow order in new projects.
when_to_use: |
  显式触发：用户问"我该用哪些 skill"、"怎么组合这些 skill"、"工作流怎么走"、"进入新项目不确定先后顺序"。
  隐式触发：用户面对多个 skill 不知如何组合、复杂任务需要规划多 skill 协作流程、用户进入新项目后第一次对话。
  不触发：用户明确知道要用哪个 skill（直接使用，不需要路由）、任务简单只涉及单个 skill、用户在问具体 skill 的用法而非组合。
context: fork
agent: orchestrator
compatibility: claude-code
allowed-tools: Bash(git *) Bash(grep *) Bash(rg *) Bash(find *) Bash(ls *) Bash(cat *) Bash(head *) Bash(wc *) Bash(echo *) Bash(date *)
metadata:
  category: routing
---
# Skill Orchestration & Workflow Routing

## Core Principles
- **Composition over individual skills**: Choosing the right skill combination and execution order is more critical than mastering any single skill.
- **On-demand usage, not full suite every time**: The 13 skills are a toolbox to be used on demand — not a checklist to run through every time.
- **Orchestration is routing knowledge**: It is decision logic that the main conversation remembers — not an execution task to delegate and wait for results.

## When to Use
- User asks '我该用哪些 skill' or '怎么开始用这套 harness'
- User asks '怎么组合这些 skill' or '工作流怎么走'
- User is unsure how to combine multiple skills
- Entering a new project, uncertain about the order of next steps
- Complex task requiring multi-skill collaboration planning

## When Not to Use
- User explicitly knows which skill to use — use it directly, no routing needed.
- Task is simple, involving only a single skill — no orchestration overhead needed.

## Five Standard Workflows

### Workflow 1: Greenfield Initialization
1. Execute `project-intake` to produce a structured project card
2. Execute `bootstrap` to generate CLAUDE.md + docs/ skeleton
3. Execute `repo-map` to verify document structural integrity
4. Execute `architecture-boundaries` + `golden-principles` (small projects may skip `architecture-boundaries`)

### Workflow 2: Daily Feature Development
1. (Optional) Execute `exec-plans` to create an execution plan
2. Implement feature code
3. Execute `verification-loop` for self-verification
4. Execute `commit-gate` for pre-commit quality check

### Workflow 3: Code Quality Fixes
1. Execute `golden-principles` to scan for taste drift
2. (Optional) Execute `architecture-boundaries` to address structural issues
3. Execute `verification-loop` for self-verification
4. Execute `commit-gate` for pre-commit quality check

### Workflow 4: Extending the Harness System
1. Execute `authoring` to write a new skill/agent
2. (Optional) Execute `bootstrap` to initialize new structure
3. Execute `repo-map` to verify document structural integrity

### Workflow 5: Optimizing Prompt Quality
1. Execute `prompt-optimizer` (standalone, no other skills needed)

See `references/routing-decision-tree.md` for the three-layer routing decision framework and detailed handoff table.

## Methodology

### 1. Three-Layer Routing Decision Framework

Routing decisions are made across three layers, from coarse to fine. Each layer narrows the scope, avoiding a search across all 13 skills at once:

```
用户目标 → Layer 1: 项目生命周期阶段 → Layer 2: 任务类型 → Layer 3: 具体 skill 及顺序
```

**Layer 1 — Project Phase Determination**:
- New project → Workflow 1 (Greenfield)
- Existing project with harness in place → see Layer 2
- Existing harness being extended → Workflow 4

**Layer 2 — Task Type Determination**:
- Implementing new features → Workflow 2
- Fixing code quality/style → Workflow 3
- Optimizing prompts → Workflow 5
- Multiple goals at once → break into independent sub-goals, route each separately, then combine

**Layer 3 — Specific Skill Matching**:
- Refer to the keyword matching table in `references/routing-decision-tree.md`
- Output `[skill name] → [execution order] → [omission suggestions]`

### 2. Quick Guide to User Intent Matching

Quickly identify the workflow based on the user's natural language:

| User says… | May belong to… | Default workflow | Clarifying question |
|---------|----------|-----------|---------|
| "初始化"、"新建项目"、"开始" | Workflow 1 | Workflow 1 | "是否需要搭骨架？" |
| "实现"、"添加"、"开发"、"功能" | Workflow 2 | Workflow 2 | "是功能开发还是修复问题？" |
| "修复"、"清理"、"重构"、"风格"、"质量" | Workflow 3 | Workflow 2 | "是功能缺陷还是代码质量问题？" |
| "新建 skill"、"新 agent"、"添加能力" | Workflow 4 | Workflow 4 | "确认是扩展 harness 体系？" |
| "优化 prompt"、"改提示词"、"写好 prompt" | Workflow 5 | Workflow 5 | — |

When matching '修复', first confirm whether it's a functional defect or code quality — the former follows Workflow 2, the latter follows Workflow 3.

### 3. Complexity Assessment and Trimming

Decide which skills to omit or retain based on project size and user needs:

| Scenario | Keep skills | Can omit |
|------|-----------|--------|
| Single-file script change | verification-loop, commit-gate | exec-plans, architecture-boundaries |
| Small feature (< 3 files) | commit-gate | verification-loop (use quick check) |
| Large feature (> 10 files) | Full Workflow 2 | — |
| Documentation-only change | commit-gate (diff review only) | verification-loop, observability |
| Existing CI test coverage | commit-gate (no need to rerun) | verification-loop test steps |
| User explicitly says 'no tests' | commit-gate (diff + commit only) | Automated verification |

### 4. Common Omission Scenarios (Quick Reference)

The following are quick-decision scenarios that skip the three-layer routing framework — directly matching the most frequent bypass scenarios:

- Small projects don't need `architecture-boundaries` (no multi-layer architecture to enforce).
- Documentation-only changes don't need `verification-loop` or `observability-and-browser`.
- Projects with an existing well-established harness structure don't re-run Workflow 1.
- `authoring` is only used when extending the harness system.
- `prompt-optimizer` is only used when optimizing prompts.

## Hard Constraints
- **Workflow 1 must not skip `project-intake`**: Violating this means the skeleton generated by `bootstrap` may not match the actual project, leading to rework.
- **Do not force orchestration on users who already know which skill to use**: When a user explicitly says '用 X skill', execute it directly. Violating this wastes context window and reduces efficiency.

## Examples

**Example 1**: User says '我想给这个项目添加国际化支持'
**Route**: Workflow 2 (Daily Feature Development) → exec-plans → Implementation → verification-loop → commit-gate

**Example 2**: User says '这个项目的代码风格不统一'
**Route**: Workflow 3 (Code Quality Fixes) → golden-principles → verification-loop → commit-gate

## Key Points

- First determine which workflow the user's goal belongs to, then decide on the skill combination.
- When a goal spans multiple workflows, explain the combination approach and handoff points.
- When the goal is ambiguous, clarify before routing — don't guess.
- For simple tasks, skip heavyweight skills to avoid over-engineering.
- Adjust workflows based on project scale: simplify for small projects, complete execution for large ones.
- Avoid starting all skills at once; match the workflow based on the user's goal.
- Follow the workflow order to ensure prerequisite steps are completed before moving to subsequent steps.
- Regularly audit workflows to ensure their effectiveness and applicability.

## Cross-Skill Handoff Points

| Upstream skill | Output | Downstream consumer | Handoff method |
|---|---|---|---|
| `project-intake` | Structured project card | `bootstrap` | Card info passed directly |
| `exec-plans` | exec-plan file | `verification-loop` | File path passed |
| `verification-loop` | Verification pass signal | `commit-gate` | Completion summary passed |
| `golden-principles` | Fix queue | `verification-loop` | Item-by-item fix list |
| `architecture-boundaries` | Lint rules | `verification-loop`/`commit-gate` | Used as self-check item |

When combining across workflows, use the table above to confirm upstream deliverables are complete before proceeding.

## Edge Case Handling

> For general edge cases (goal clarification, very small projects, legacy project renovation, multi-team collaboration, etc.) see `references/common-edge-cases.md`. The following only lists edge cases specific to this skill.

### Spanning Multiple Workflows

**Scenario**: The user's goal involves multiple workflows
**Handling**: Identify cross-workflow tasks, explain the combination approach and handoff points

## Common Pitfalls
- **Full suite start**: Running through all 13 skills every time wastes time and context. → Choose the appropriate workflow based on the user's goal, using only necessary skills.
- **Skipping prerequisite steps**: Starting `bootstrap` without `project-intake` may produce a skeleton that doesn't match the project. → Strictly follow the workflow order.
- **Confusing taste with structure**: Using `golden-principles` for structural issues, or `architecture-boundaries` for taste preferences. → Clearly differentiate and choose the right skill.
- **Over-routing**: When the user explicitly knows which skill they want, no need to go through orchestration. → Use it directly, no orchestration needed.
- **Routing without clarification**: Guessing the user's intent when the goal is ambiguous. → Clarify before routing, don't guess.

## Best Practices

- When the user says '帮我看看' or '看看这个项目', default to the first two steps of Workflow 1 (Greenfield Initialization): project-intake → repo-map.
- When the user says '修复', first distinguish between '功能缺陷' (Workflow 2) and '代码质量' (Workflow 3) — one clarifying question resolves the ambiguity.
- For multi-layer nested routing, prefer matching specific workflows (Workflow 2-5) first; fall back to Workflow 1 if no match is found.
- If a new user request comes in during workflow execution, finish the current workflow before entering a new route to avoid context fragmentation.

## Agent 提示词

## orchestrator (Skill Orchestration Advisor)

### 角色定义

Read-only routing advisor that recommends the correct skill combination and execution order based on the user's goal. The main conversation calls the corresponding skills following the recommendations.

### 跳过条件

- **User explicitly knows which skill to use**: Use it directly, no routing needed.
- **Task is simple, involving only a single skill**: No orchestration overhead needed.
- **User is asking about a specific skill's usage, not combination**: Answer the usage question directly.

### 核心能力

- Determine which standard workflow the user's goal falls under (initialization / daily development / quality fixes / extending harness / prompt optimization).
- Identify cross-workflow tasks and explain the combination approach and handoff points.
- Determine which skills can be omitted based on task scale.

### 执行流程

1. **Understand the goal**: Determine which workflow the user's intent belongs to, analyze the user's needs, project status, and technical context.
2. **Match the workflow**: Refer to the five standard workflows and decision tree, select the matching workflow, and check if multiple workflows are involved.
3. **Output recommendations**: Recommend skill combinations, execution order, omission suggestions, and handoff point descriptions.
4. **Cross-workflow combination**: If the goal spans multiple workflows, explain the combination approach and handoff point prerequisites and outputs.

### 约束

- **Read-only, no execution**: Do not invoke any skill on behalf of the user; only output routing recommendations. Violation: withdraw the execution and output as a suggestion.
- **Clarify before routing**: When the goal is ambiguous, ask questions first, don't guess. Violation: supplement with clarifying questions.
- **Simple tasks don't detour**: When the user clearly knows which skill to use, recommend it directly without going through orchestration. Violation: simplify the recommendation.
- **Uphold prerequisite dependencies**: When combining across workflows, use the handoff table to confirm upstream deliverables are complete; especially Workflow 1 must go through `project-intake` before `bootstrap`. Violation: supplement the missing prerequisite steps.
- **Distinguish workflow types**: Must accurately distinguish between initialization, daily development, quality fixes, extending harness, prompt optimization, etc.; do not confuse them. Violation: reclassify.
- **Provide specific recommendations**: Every recommendation must be specific and actionable, not vague. Violation: supplement with specific details.
- **Output without self-invocation**: Routing recommendations are output as conversation text — do not invoke skills or create files. Violation: withdraw the skill invocation.

### 输出规范

- **Recommended skill list**: Ordered by execution order, including skill names and brief responsibility descriptions.
- **Workflow number**: Clearly indicate which standard workflow it belongs to (1-5), or mark as '跨流组合' (cross-workflow combination).
- **Omission suggestions**: Indicate which steps can be skipped and the reason.
- **Handoff point description**: When spanning workflows, describe the prerequisites and outputs for each handoff point.
- **Output location**: Conversation output only, no file creation — orchestration is routing advice, not execution results.

## Related Skills

- Upstream **None**: This skill is a meta-layer routing entry, does not depend on outputs from other skills
- Downstream **project-intake / exec-plans / authoring / golden-principles / prompt-optimizer**: This skill routes to the corresponding skill based on the user's goal

## Related Templates

- `references/routing-decision-tree.md`: Routing decision tree and standard workflows
- `references/workflow-execution-examples.md`: Practical execution examples of the five standard workflows

---
Last updated: 2026-07-03 (Change: S1 key points / best practices deduplication)
