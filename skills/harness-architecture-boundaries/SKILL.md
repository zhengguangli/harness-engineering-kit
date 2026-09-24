---
name: harness-architecture-boundaries
description: Design layered architecture, dependency direction, and data boundary rules for repos where agents generate large amounts of code — mechanically enforced via Grep/Bash checks in a boundary-auditor agent. Used for establishing layered architecture, circular dependency issues, cross-layer violations, lint rules, and dependency direction design.
when_to_use: |
  显式触发：用户要建立分层架构、出现循环依赖或层间越界、需要设计自定义 lint 规则、设计依赖方向。
  隐式触发：代码已出现架构腐化、模块间依赖混乱、用户问"怎么组织代码结构"、需要定义跨层依赖方向。
  不触发：纯风格偏好类问题（交给 harness-golden-principles）、项目规模极小模块间无明显分层需求、用户明确表示不需要架构约束。
context: fork
agent: boundary-auditor
compatibility: claude-code
depends_on:
  - harness-project-intake
  - harness-bootstrap
allowed-tools: Bash(git *) Bash(grep *) Bash(rg *) Bash(find *) Bash(ls *) Bash(cat *) Bash(head *) Bash(wc *) Bash(echo *) Bash(date *)
metadata:
  category: architecture
---
# Architecture Boundaries

## Core Principles

- **Freedom within boundaries, rigor at the edges**: Strictly enforce module dependency direction, data boundary forms, and cross-layer call paths; fully delegate implementation details.
- **Mechanical enforcement over manual review**: In a world where Agents generate code at high throughput, any constraint not mechanically enforced will be violated in short order — not because the agent "went bad," but because it faithfully replicates bad patterns already present in the repository.
- **Fixed direction + limited legal edges + cross-cutting chokepoint**: This is the core pattern of layered architecture — fix dependency direction, limit the number of legal dependency edges, and have cross-cutting concerns enter through a single chokepoint.

## When to Use

- 用户要为项目建立"严格边界、局部自由"的分层架构
- 代码已出现架构腐化、循环依赖或层间越界
- 需要设计自定义 lint 规则或定义跨层依赖方向
- 项目规模较大，模块间存在明显分层需求

## When Not to Use

- 纯风格偏好类问题（交给 `harness-golden-principles`）
- 项目规模极小、模块间无明显分层需求
- 用户明确表示不需要架构约束

## Methodology

### 1. Derive the Project's Own Layering Model

Don't copy reference models. Process:

1. List the project's main domains/modules
2. For each domain, identify the data flow: from the lowest-level type definitions to the top-level user interface
3. Determine "which layers can depend on each other, and which must be unidirectional"
4. Identify cross-cutting concerns (auth, logging, configuration, etc.) and define their legitimate entry points
5. Encode the above into dependency direction rules

### 2. Reference Layering Model

```
Within each business domain, code may only depend "forward" with a fixed direction:

    Types → Config → Repo → Service → Runtime → UI

Cross-cutting concerns (auth, connectors, telemetry, feature flags) must not be scattered across arbitrary layers —
they must enter through an explicit Providers interface:

    Providers → Service → Runtime → UI

Utility functions that don't belong to any of the above layers go in Utils.
Utils may only be used by Providers and must not have reverse dependencies into business domains.
```

The key is not this specific 6-layer model, but the pattern: **fixed direction + limited legal edges + cross-cutting concerns funneled through a single chokepoint**.

**Implementation variations across projects**: Node.js projects use `types/config/repositories/services/controllers`; React projects use `types/config/hooks/services/components/pages`; microservices reuse the same layering pattern within each service, sharing only type definitions across services.

### 3. "Parse, Don't Validate" as the Data Boundary Rule

Requirement: **Any external data entering the system boundary must be parsed into a strong type, rather than validated and then passed around as a weak type**. The specific library is not prescribed — only the invariant must be mechanically checked, e.g., a lint rule that prohibits using unparsed `any`/`dict`/dynamic dictionary access at boundary layers.

**Best Practices**:
1. **Define clear data boundaries**: Distinguish external data from internal data
2. **Use strong types**: External data must be parsed into strong types; avoid using any/dict
3. **Mechanical checks**: Use lint rules or automated scripts to check for data boundary violations
4. **Document data flow**: Record the data transformation process from external to internal

**Examples**:
```typescript
// Incorrect: using any type directly
function processUserInput(input: any) {
  // Accessing properties directly without type checking
  console.log(input.name);
}

// Correct: parse into a strong type
interface UserInput {
  name: string;
  email: string;
}

function processUserInput(input: unknown) {
  // Parse into a strong type
  const parsedInput = parseUserInput(input);
  console.log(parsedInput.name);
}

function parseUserInput(input: unknown): UserInput {
  // Implement parsing logic
  // Validate and convert to strong type
}
```

### 4. Execution Steps

1. **Clarify with the user** the dependency direction and legitimate entry points for cross-cutting concerns
2. **Write the rules into `docs/ARCHITECTURE.md`** (template at `references/architecture-template.md`)
3. **Delegate inspection to the `boundary-auditor` agent for inline execution** — use Grep/Bash to directly check dependency direction violations, no pre-configured lint toolchain needed in the project
4. **Attach concrete "how to fix" instructions to each finding** — format: `### [Severity] <Title>` + file + line number + violated rule + impact + suggested fix
5. **Distinguish "must block" from "suggested but not enforced"** — invariants (circular dependencies, cross-layer boundary violations, data boundary violations) are blocking checks for boundary-auditor; style preferences are periodic cleanup for harness-golden-principles
6. **Integrate into `harness-verification-loop`** — architectural violations must be fixed to pass the self-verification loop

**Severity Classification Reference**:

| Level | Applicable Violations | Action |
|-------|----------------------|--------|
| CRITICAL | Circular dependencies, cross-layer boundary violations | Blocks merge, must fix |
| HIGH | Scattered cross-cutting concerns, data boundary violations | Blocks merge, requires redesign |
| MEDIUM | Ambiguous style, rules needing refinement | Record as architecture debt, process next cycle |
| LOW | Minor inconsistencies, optimizable dependencies | Leave for golden-principles periodic cleanup |

## Hard Constraints

1. **Dependency direction must be unidirectional**: Layer N modules may only depend on Layer < N modules, never the reverse. Violations are marked CRITICAL in the report and block merge.
2. **Cross-cutting concerns must be funneled through a single chokepoint**: Auth, logging, configuration, etc. must not be scattered across layers — they must enter through a unified Providers interface. Violations are marked HIGH in the report and require redesign.
3. **External data must be parsed into strong types**: Any external data entering the system boundary must be parsed into a strong type; passing as any/dict is prohibited. Violations are marked HIGH and include a suggested fix.
4. **Every violation must include an actionable fix suggestion**: Each finding in the report must contain a specific fix direction (code example + steps), not just "there's a problem here." Violations are rejected and regenerated.
5. **Severity must be accurately classified**: CRITICAL (circular dependency/boundary violation, blocks merge) / HIGH (scattered cross-cutting concerns) / MEDIUM (ambiguous style) / LOW (leave for periodic cleanup). Violations are reclassified before output.

## Examples

**Example 1**: User says "这个项目的 Service 层不应该直接 import Repository 层实现"
**Handling**: Read `ARCHITECTURE.md` to confirm dependency direction rules → Use Grep to search for cross-layer imports → Find violations → Produce a report with file line numbers and fix suggestions

**Example 2**: User says "检查是否有循环依赖"
**Handling**: Read architecture rules → Search for inter-module import statements → Generate a dependency graph → Mark circular dependency paths → Produce fix suggestions (redesign interfaces or split modules)

**Example 3**: User says "帮我设计分层架构"
**Handling**: Analyze project domain divisions and data flow → Confirm dependency direction and cross-cutting concern entry points with the user → Write to `ARCHITECTURE.md` → Hand off to boundary-auditor for verification

**Example 4**: User says "这个项目的文件命名和 import 顺序太乱了，能不能定个规矩"
**Handling**: This is the boundary case with `harness-golden-principles`. Test each complaint against one question — *does violating it break a structural invariant?* Naming style and import ordering do not: they are taste, they degrade gracefully, and no module boundary is violated by ignoring them. So classify as style preference and hand off to golden-principles, which encodes taste as periodically-swept rules. Only route back here if a complaint turns out to mask a real boundary problem (e.g., "import order" is actually "service layer importing repository implementations").

## Key Points

- **Constrain invariants, not implementation details**: Strictly enforce module dependency direction and data boundary forms; do not constrain specific function writing style, library choices, or variable naming.
- **Errors must include fix guidance**: Violation reports should not just say "Rule X violated" — they must be written as concrete fix instructions.
- **Distinguish invariants from style preferences**: True invariants are blocking checks; style preferences are periodic cleanup.
- **Regularly audit architecture rules**: Architecture rules should evolve with the project; conduct periodic audits to ensure rule effectiveness.
- **Document architecture decisions**: All architecture decisions should be documented for team understanding and compliance.

## Edge Case Handling

> For general edge cases (very small projects, legacy project migration, multi-team collaboration, etc.) see `references/common-edge-cases.md`. Only skill-specific edge cases are listed below.

### Microservices Architecture

**Scenario**: The project uses a microservices architecture with dependencies between services
**Handling**: Define internal architecture rules for each service; services communicate via API

### Ambiguous Rule Definition

**Scenario**: An architecture rule is worded vaguely (e.g., "minimize dependencies") and the boundary-auditor cannot determine whether a specific import violates it
**Handling**: Report the ambiguity as a finding with severity MEDIUM. Rewrite the rule to be mechanically checkable (e.g., "Service layer must not import Repository layer implementations directly — must go through interfaces"). Do not attempt to enforce vague rules — precision over coverage.

### Multi-Team Codebase with Conflicting Conventions

**Scenario**: Different teams in the same repo follow different dependency patterns (Team A uses direct imports, Team B uses dependency injection)
**Handling**: Identify the conflict during the audit, report both patterns as findings, and recommend the team converge on one pattern. Do not unilaterally pick a winner — present both options with trade-offs and let the team decide. Record the decision in `docs/design-docs/`.

### Gradual Migration from Monolith to Layered Architecture

**Scenario**: The project is migrating from a monolith to a layered architecture, and not all modules have been migrated yet
**Handling**: Scope the audit to migrated modules only. Mark unmigrated modules as "out of scope" in the report with a note that they will be audited after migration. Do not flag violations in unmigrated code — that produces noise, not signal.


## Common Pitfalls

- **Copying layering models blindly**: Different projects have different domain divisions and dependency directions — don't mechanically apply the 6-layer model.
  - Solution: First analyze the project's actual domain divisions and data flow, then design a suitable layering model
  - Example: A small project may only need 3 layers (Types → Services → UI), not 6
- **Reporting violations without fix suggestions**: Errors without fix guidance leave agents or humans with no starting point.
  - Solution: Every violation must include a concrete fix suggestion, with code examples and actionable steps
  - Example: Don't just say "dependency direction violated" — say "move the import statement from file X to file Y"
- **Neglecting cross-cutting concern chokepoints**: Auth, logging, and configuration scattered across layers make modification difficult.
  - Solution: Identify all cross-cutting concerns, centralize them in the Providers layer, and access them through a single chokepoint
  - Example: Authentication logic should not be spread across various services — centralize it in AuthProvider
- **Treating style preferences as invariants**: Over-constraining reduces agent efficiency — distinguish "must block" from "suggested but not enforced."
  - Solution: Clearly distinguish architecture invariants (must block) from style preferences (periodic cleanup)
  - Example: Circular dependency is an invariant and must block; naming style is a preference and goes to golden-principles
- **Unclear rule definitions**: Vague rules make it impossible to determine whether something violates them.
  - Solution: Rules must be specific, mechanically checkable, and avoid vague wording
  - Example: Don't say "minimize dependencies" — say "Service layer must not directly import Repository layer implementations"
- **Ignoring project evolution**: Architecture rules should evolve as the project grows.
  - Solution: Periodically audit architecture rules and adjust the layering model as the project changes
  - Example: After significant project growth, you may need to evolve from 3 layers to 6 layers

## Best Practices

- Start with 3 layers (Types → Services → UI) when first defining a layered architecture, and expand gradually as the project grows — don't begin with a 6-layer model.
- Review dependency direction every time a new module is added — the new module's responsibilities should naturally belong to a specific layer, not be forced into an existing one.
- Group audit reports by severity, with each CRITICAL/HIGH finding including a "Before/After" code comparison to lower the fix barrier.
- Export cross-cutting concern Providers entry points through a unified `providers/index.ts` file; prohibit direct sub-module references from arbitrary layers.

## Related Skills
- input      **harness-project-intake**: Consumes its output (project information analysis) as input for architecture boundary analysis
- input      **harness-bootstrap**: Consumes its output (initialization skeleton) as input for architecture boundary setup
- see-also   **harness-golden-principles**: Style preference classification criteria feed periodic cleanup; the two skills run in parallel, neither consumes the other's output
- output     **harness-verification-loop**: Architecture rule documentation is consumed as self-check items by the verification loop


## Related Templates

- `references/architecture-template.md`: ARCHITECTURE.md architecture document template
- `references/check-pattern-template.md`: Architecture check pattern template (reference for boundary-auditor)
- `references/e2e-architecture-audit-example.md`: End-to-end full example (Node.js e-commerce platform architecture audit, including project analysis → boundary identification → rule generation → verification — the complete workflow)

## Agent 提示词

## boundary-auditor (Architecture Boundary Auditor)

### Skip Conditions

- 纯风格偏好类问题：交给 harness-golden-principles，不触发架构边界检查。
- 项目无多层架构或用户明确不需要架构约束：不触发。

### Role Definition

You are the "Architecture Boundary Auditor." Your sole responsibility is to detect violations of layered architecture / dependency direction rules and report them — **you never modify any file**. You are skilled at using Grep/Bash and similar tools to perform architecture boundary inspections, identifying issues such as circular dependencies, cross-layer boundary violations, and data boundary violations.

### Core Capabilities

- Read `ARCHITECTURE.md` or equivalent architecture documentation to confirm dependency direction rules, layer boundaries, and legitimate cross-cutting concern entry points
- Use Bash to run the project's existing lint/build/test commands (read-only output)
- Combine Grep/Glob for inline inspection of dependency direction violations (e.g., searching for import statements between specific layers)
- For each violation found, produce a structured report with file line numbers and fix suggestions
- Identify circular dependencies, cross-layer boundary violations, data boundary violations, and similar architecture issues
- Distinguish architecture invariants from style preferences, providing targeted fix suggestions

### Execution Flow

1. **Read architecture rules**: Read `ARCHITECTURE.md` to confirm dependency direction, cross-cutting concern entry points, and data boundary rules. If not found, first report "rules are not documented," then infer from the code.
2. **Run inspections**: Use Bash to run lint/build commands (read-only), use Grep/Glob to search for cross-layer imports, and check for circular dependencies.
3. **Record violations**: Format: `### [Severity] <Title>` + file + line number + violated rule + impact + suggested fix.
4. **Classify severity**: CRITICAL (circular dependency/boundary violation, blocks merge), HIGH (scattered cross-cutting concerns), MEDIUM (ambiguous style), LOW (leave for periodic cleanup). When uncertain, mark with the lower severity (lean conservative).
5. **Generate report**: Output to `docs/quality-reports/architecture-boundaries-audit.md`, title `## Architecture Boundary Audit Report`, ordered by severity, with a summary at the end (total count, count by level, whether it blocks). Overwrite on each run; history is trackable via git.

**Finding organization specification**: CRITICAL and HIGH findings are displayed first in the report, each with a "benefit of fixing" note (e.g., "fixing this eliminates coupling risk from N modules") to help the executor prioritize.

### Constraints

- **Strictly read-only**: Do not invoke any tool that modifies files. Bash may only be used for read-only commands (lint/test/build output, grep searches). Prohibit rm, mv, cp, chmod, mkdir, touch, and similar write operations. If violated, revert the operation and re-output as a report.
- **Report when rules are unclear**: When rule definitions are ambiguous and violations cannot be determined, report "the rule needs to be more precisely encoded" as a finding. If violated, supplement with a finding about the ambiguity.
- **Actionable fix suggestions**: The report must allow the agent who picks up the fix to work from it directly — not just "there's a problem here." If violated, supplement with specific fix directions.
- **Do not relax rules on your own**: Do not subjectively relax the rules themselves. If violated, revert to the original rule judgment.
- **Distinguish severity**: Must accurately distinguish CRITICAL/HIGH/MEDIUM/LOW levels — do not confuse them. If violated, reclassify.
- **Provide specific fix suggestions**: Every violation must include a concrete fix suggestion with code examples and actionable steps. If violated, supplement with specific fix suggestions.

### Output Specification

- **Format**: Markdown structured report
- **Output path**: `docs/quality-reports/architecture-boundaries-audit.md` (overwritten each run; history in git)
- **Content**: Each finding includes file, line number, violated rule, impact, and suggested fix
- **Principle**: The report must allow the agent who picks up the fix to work from it directly — don't just say "there's a problem here" without direction
- **Finding grouping**: First group by severity, then alphabetically by file path within each group
- **Wording**: Do not output phrases like "I have fixed this" — you have not fixed anything
- **Report structure**: Includes both a summary (total + severity distribution + whether it blocks) and detailed findings, ordered by severity

---
Last updated: 2026-09-24 (Change: added Example 4 drawing the architecture-boundaries vs golden-principles responsibility boundary; round-33 LOW #6)
