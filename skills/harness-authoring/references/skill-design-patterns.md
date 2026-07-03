# Skill Design Patterns Reference

## Design Pattern Overview

| Pattern | Use Case | Complexity |
|---|---|---|
| Knowledge Injection | Main conversation needs ongoing reference to domain knowledge | Low |
| Process Guidance | Complex multi-step tasks need structured workflow | Medium |
| Checklist | Verification/audit scenarios requiring item-by-item checks | Low |
| Tool Orchestration | Needs to coordinate multiple tools/sub-agents | High |
| Progressive Disclosure | Large amount of information needs layered loading | High |

## Pattern 1: Knowledge Injection

The simplest skill form — injects domain knowledge into the current context for the main conversation to reference.

**Structure Template**:

```yaml
---
name: domain-knowledge
description: Provides domain knowledge reference for XXX scenarios.
context: fork
compatibility: claude-code
---
# Domain Knowledge

## Core Concepts
- Concept A: Definition and boundaries
- Concept B: Definition and boundaries

## Decision Rules
- When encountering X, choose Y
- When encountering Z, choose W

## Common Misconceptions
- Misconception 1: ... (correct approach: ...)
- Misconception 2: ... (correct approach: ...)
```

**Design Points**:
- Body text within 200 lines (this type of skill is typically compact)
- Core concepts ≤ 10; beyond that, split into references/
- Decision rules use the "When... choose..." format to eliminate ambiguity

**Anti-patterns**:
- ❌ Stuffing an entire textbook into a skill — should split into references/ for on-demand loading
- ❌ Vague concept definitions — "X is a good practice" is worse than "X refers to: 1/2/3"

## Pattern 2: Process Guidance

Defines the execution flow for complex multi-step tasks, with the main conversation progressing step by step.

**Structure Template**:

```yaml
---
name: workflow-guide
description: Guides the execution of XXX workflow — from A to B to C.
context: fork
compatibility: claude-code
---
# Workflow Guide

## Core Principles
- Principle 1: ...
- Principle 2: ...

## Execution Flow

### Phase 1: Preparation
1. Step 1 (check X)
2. Step 2 (prepare Y)

### Phase 2: Execution
3. Step 3 (execute A)
4. Step 4 (verify B)

### Phase 3: Wrap-up
5. Step 5 (record C)

## Edge Cases
- Case 1 → Handling approach
- Case 2 → Handling approach
```

**Design Points**:
- Phase count ≤ 5, steps per phase ≤ 5
- Each step must be actionable (not "consider X" but "check if X exists")
- Edge cases use "case → handling" mapping, no long paragraphs

**Anti-patterns**:
- ❌ Vague step descriptions — "make preparations" is worse than "confirm the following 3 items are ready: ..."
- ❌ Missing termination conditions — each Phase should have clear "completion criteria"

## Pattern 3: Checklist

Item-by-item verification structure for audit/validation scenarios.

**Structure Template**:

```yaml
---
name: quality-checklist
description: Checks whether XXX meets quality standards.
context: fork
compatibility: claude-code
---
# Quality Checklist

## Check Items

### Mandatory Items (all must pass to qualify)
- [ ] Check item 1: Standard description + judgment method
- [ ] Check item 2: Standard description + judgment method

### Recommended Items (suggested to pass)
- [ ] Check item 3: Standard description + judgment method

## Judgment Rules
- All mandatory items pass → ✅ Qualified
- Any mandatory item fails → ❌ Unqualified; list failed items
- Recommended item fails → ⚠️ Warning, not blocking

## Output Format
| Check Item | Result | Evidence |
|---|---|---|
| Check item 1 | ✅/❌ | Specific evidence |
```

**Design Points**:
- Mandatory items ≤ 10; group if exceeded
- Each item must have a clear judgment method (not "looks right")
- Fixed output format for automated parsing

## Pattern 4: Tool Orchestration

Coordinates multiple tools or sub-agents to complete complex tasks.

**Structure Template**:

```yaml
---
name: tool-orchestrator
description: Orchestrates XXX toolchain to complete YYY tasks.
context: fork
compatibility: claude-code
---
# Tool Orchestrator

## Tool Inventory
| Tool | Purpose | Permission |
|---|---|---|
| tool1 | Purpose 1 | read |
| tool2 | Purpose 2 | read, write |

## Orchestration Flow
1. Call tool1 (input: A, output: B)
2. Route based on B
3. Route 1 → call tool2
4. Route 2 → call tool3

## Error Handling
- tool1 fails → retry once, terminate if still failing
- tool2 times out → switch to fallback tool
```

**Design Points**:
- Tool inventory includes permission declarations (aligns with least-privilege principle)
- Orchestration flow described with data flow (input → processing → output)
- Each tool call must have an error handling path

## Pattern 5: Progressive Disclosure

Large knowledge systems organized in layers.

**Structure Template**:

```yaml
---
name: progressive-knowledge
description: XXX domain knowledge — dive deeper on demand.
context: fork
compatibility: claude-code
---
# Progressive Knowledge

## Core Concepts (Always Loaded)
- Concept 1: One-sentence definition
- Concept 2: One-sentence definition

## In-Depth Guides (Loaded on Demand)
- Detailed content → Reference `references/deep-dive-1.md`
- Detailed content → Reference `references/deep-dive-2.md`

## Quick Reference (High-Frequency Lookup)
| Scenario | Approach |
|---|---|
| Scenario A | Approach 1 |
| Scenario B | Approach 2 |
```

**Design Points**:
- Core concepts ≤ 5 (the part always loaded)
- In-depth guides use file references; body only says "under what circumstances to read which file"
- Quick reference table covers the 80% most frequent scenarios

## Pattern Selection Decision Tree

```
Need to inject knowledge into the main conversation?
├── Small knowledge volume (< 200 lines) → Knowledge Injection
├── Large knowledge volume → Progressive Disclosure
└── Need execution flow?
    ├── Linear flow → Process Guidance
    ├── Needs routing decisions → Tool Orchestration
    └── Needs item-by-item verification → Checklist
```

## Hybrid Patterns

In practice, patterns are often combined:

| Hybrid Approach | Example |
|---|---|
| Knowledge Injection + Checklist | Domain knowledge + quality inspection standards |
| Process Guidance + Tool Orchestration | Tool calls embedded in multi-step workflow |
| Progressive Disclosure + Process Guidance | Core flow + on-demand in-depth reference materials |

**Hybrid Principle**: Use one pattern as the primary, others as supplementary. Do not use more than 3 patterns in a single skill, otherwise the structure becomes chaotic.
