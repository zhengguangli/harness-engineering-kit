# Subagent Design Patterns Reference

## Subagent and Skill Pairing Relationship

Subagents do not exist independently — they are typically paired with a skill of the same name:
- **Skill**: Defines methodology (main conversation reference)
- **Subagent**: Executes specific operations (independent context window)

```
User request → Main conversation loads skill → Decides execution needed → Delegates to subagent → Returns summary
```

## Design Pattern Overview

| Pattern | Use Case | Tool Permissions | Typical Model |
|---|---|---|---|
| Read-Only Analysis | Audit, inspection, scanning | Read, Grep, Glob | Lightweight |
| Execution-Only | Code modification, file generation | Read, Write, Edit, Bash | Medium |
| Composite Judgment | Needs judgment + execution mix | On-demand combination | Stronger |
| Batch Processing | Repeated operations on multiple files/projects | Read, Write, Bash | Lightweight |

## Pattern 1: Read-Only Analysis

**Use Case**: Code audit, quality check, architecture boundary check, scan reports

**Tool Configuration**:
```yaml
tools:
  - Read
  - Grep
  - Glob
  - Bash  # For read-only commands only (e.g., git log, find)
```

**System Prompt Structure**:
```markdown
## Role Definition
You are [role name], responsible for [read-only analysis responsibility]. You do not modify code, only produce analysis reports.

## Core Capabilities
- Capability 1 (read-only operation)
- Capability 2 (read-only operation)

## Execution Flow
1. Collect information (Read/Grep/Glob)
2. Analyze information
3. Produce report

## Constraints
- Read-only, no modifications: Do not use Edit/Write to modify any files
- No conclusions without evidence: Each conclusion accompanied by code location
```

**Design Points**:
- Clearly state "do not modify code" in the role definition
- First constraint is "read-only, no modifications"
- Execution flow only includes collect → analyze → produce; no modification steps

**Anti-patterns**:
- ❌ Giving a read-only agent Edit/Write — the least-privilege principle requires not giving them
- ❌ Saying "try not to modify" in constraints — should be "never modify"

## Pattern 2: Execution-Only

**Use Case**: Code refactoring, file generation, batch modification

**Tool Configuration**:
```yaml
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
```

**System Prompt Structure**:
```markdown
## Role Definition
You are [role name], responsible for [execution responsibility]. You modify code/files according to clear instructions.

## Core Capabilities
- Capability 1 (read + write operations)
- Capability 2 (read + write operations)

## Execution Flow
1. Understand requirements
2. Read existing code
3. Modify code
4. Verify modifications

## Constraints
- Minimal modification: Only change necessary parts, no unrelated refactoring
- Maintain style: Follow the project's existing code style
- Verify results: Must verify after modification (lint/test)
```

**Design Points**:
- Constraints emphasize "minimal modification" and "maintain style"
- Execution flow includes a verification step
- Still needs least privilege — don't give tools that aren't needed

## Pattern 3: Composite Judgment

**Use Case**: Complex tasks that require analysis before execution (e.g., "inspect and fix")

**Tool Configuration**:
```yaml
tools:
  - Read
  - Grep
  - Glob
  - Edit
  - Write
  - Bash
```

**System Prompt Structure**:
```markdown
## Role Definition
You are [role name], responsible for [composite responsibility]. You first analyze problems, then decide whether/how to modify.

## Core Capabilities
- Analysis capability (read-only)
- Modification capability (read + write)
- Judgment capability (whether modification is needed)

## Execution Flow
1. Analyze current state (Read/Grep/Glob)
2. Judge problem (based on rules)
3. Decide action: fix / report / skip
4. If fixing needed: minimal modification + verification
5. Produce report

## Constraints
- Analyze before modify: do not skip the analysis step
- Don't modify unless necessary: only modify when clearly needed
- Verify after modification: must verify every modification
```

**Design Points**:
- Execution flow clearly states "analyze before modify" order
- Constraints emphasize "don't modify unless necessary"
- Output includes analysis report + modification record

## Pattern 4: Batch Processing

**Use Case**: Repeated operations on multiple files/projects

**Tool Configuration**:
```yaml
tools:
  - Read
  - Write
  - Bash
  - Glob
```

**System Prompt Structure**:
```markdown
## Role Definition
You are [role name], responsible for batch executing [operation] on multiple targets.

## Core Capabilities
- Batch scan targets
- Execute standardized operations on each target
- Aggregate results

## Execution Flow
1. Scan all targets (Glob)
2. Execute operation on each target
3. Record result for each target
4. Aggregate report

## Constraints
- Standardization: Execute the same operation on each target; do not change logic per target
- Fault tolerance: Failure on a single target does not interrupt the entire batch
- Aggregation: Must produce an aggregate report
```

**Design Points**:
- Emphasize standardization and fault tolerance
- Single failure does not interrupt the batch
- Must have an aggregate report

## Model Selection Guide

| Task Characteristics | Recommended Model | Rationale |
|---|---|---|
| Mechanical scanning, pattern matching | Lightweight model | Task is clear, no high-level judgment needed |
| Code audit, architecture assessment | Stronger model | Needs context understanding and trade-offs |
| Batch modification, template-based generation | Lightweight model | Task is repetitive, clear pattern |
| Complex refactoring, multi-file coordination | Stronger model | Needs understanding of global dependencies |
| Documentation generation, format conversion | Lightweight model | Task is mechanical, clear rules |

**Selection Principle**: Choose by "judgment complexity" rather than "task size". Large but mechanical tasks use lightweight models; small but judgment-intensive tasks use stronger models.

## Subagent Error Handling

### Fault Tolerance Strategy

| Error Type | Handling Method |
|---|---|
| File does not exist | Record and skip; continue processing other targets |
| Insufficient permissions | Record and skip; report capability gaps |
| Tool call failure | Retry once; if still failing, record and skip |
| Output format anomaly | Attempt to fix format; if unfixable, record raw output |

### Timeout Handling

- Set reasonable timeout (based on task size)
- On timeout, produce partial results + timeout explanation
- No silent failures — must have a clear timeout report

## Subagent Output Specification

### Summary Format

```markdown
## Execution Summary
- Objective: [Task objective]
- Result: Success / Partial Success / Failure
- Duration: [Time]

## Detailed Results
- [Result 1]
- [Result 2]

## Issues Record
- [Issue 1]: [Handling method]
- [Issue 2]: [Handling method]
```

### Evidence Format

```markdown
## Evidence
| File/Location | Operation | Result |
|---|---|---|
| path/to/file.ts:42 | Modified | ✅ Success |
| path/to/other.ts:18 | Skipped | ⚠️ Does not exist |
```

## Sync Discipline with Skills

1. **Skill defines methodology, Subagent executes**: Do not duplicate Skill methodology content in Subagent's system prompt
2. **Use skills field for preloading**: Reference the paired skill via the `skills` field in Subagent configuration, rather than copying content
3. **Maintain consistency**: When a Skill is updated, the Subagent's execution flow should be updated in sync (but not copy-pasted)
