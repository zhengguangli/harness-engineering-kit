---
name: harness-golden-principles
description: Encode human expertise as mechanized Golden Principles, establish periodic codebase scanning, continuously detect pattern drift, and generate small-grained fix PRs. Used for scanning code smells, cleaning AI-generated code, establishing lint rules, unifying code style, and encoding review feedback as rules.
when_to_use: |
  显式触发：用户想把人类品味编码为机械化规则、治理 AI 生成代码的重复/不一致模式、建立周期性代码扫描机制、扫描代码异味、清理 AI 代码风格不统一、给代码库建立自动化 lint 规则。
  隐式触发：review 里反复出现同类反馈、代码质量参差不齐出现重复模式、团队靠人工定期"打扫 AI 写的代码"、用户问"怎么让代码风格统一"。
  不触发：需要结构性架构约束（用 harness-architecture-boundaries）、项目规模极小没有重复模式、用户只想了解现有规则而非建立新规则。
context: fork
agent: entropy-collector
compatibility: claude-code
allowed-tools: Bash(git *) Bash(grep *) Bash(rg *) Bash(find *) Bash(ls *) Bash(cat *) Bash(head *) Bash(wc *) Bash(echo *) Bash(date *)
metadata:
  category: quality
---
# Golden Principles & Garbage Collection

## Core Principles
- **Deviation lifetime approaches zero**: Inconsistent patterns are detected and fixed within days of the next scan, rather than accumulating for months.
- **Small continuous repayments**: Technical debt interest is high — making continuous small repayments is far more economical than waiting until it becomes unbearable and tackling it all at once.
- **Code once, enforce forever**: Human judgment only needs to be given once; thereafter, every line of code is checked against this rule without having to repeat the same feedback in every review.

## When to Use
- Agent 生成的代码质量参差不齐，出现重复或不一致的实现模式。
- 团队还在靠人工定期"打扫 AI 写的代码"。
- 想把人类品味编码为机械化规则持续生效。
- 扫描代码异味、清理AI代码风格不统一。
- 给代码库建立自动化lint规则。

## When Not to Use
- 需要的是结构性架构约束（依赖方向、数据边界）——用 `harness-architecture-boundaries`。
- 项目规模极小、没有重复模式——不需要周期性扫描。

## Golden Principles vs Architecture Boundaries

| | `architecture-boundaries` | `golden-principles` |
|---|---|---|
| Nature | Structural invariants | Habit/taste consistency |
| Enforcement timing | Pre-merge blocking (CI red line) | Post-merge periodic sweep |
| Violation consequence | Must fix before merge | Enters sweep queue, can auto-merge fix |
| Example | "Service layer must not import Runtime internal modules" | "Prefer shared utility packages over handwritten helpers" |

Don't confuse them: taste preferences should not be CI hard blocks (they slow throughput), and structural constraints should not be treated as "suggestions" (that's equivalent to having no constraints).

## Methodology
### Distilling Golden Principles
1. **Capture from real signals**: Repeated similar feedback in reviews, recurring user bugs, similar issues repeatedly fixed in refactoring PRs.
2. **From specific to general**: Distill "how to fix this time" into a general statement of "how it should always be done."
3. **Encode as mechanical rules**: If it can be written as a lint rule, write a lint rule; otherwise, document it as a reference for periodic scanning.

### Designing Sweep Rhythm
- **Project initialization phase**: Daily scans for the first week to clean up accumulated deviations.
- **Steady state**: One scan per week (Monday morning), with each fix PR limited to 3-5 deviation types.
- **After emergency fixes**: Immediately run an additional scan on related principles to prevent similar patterns from spreading.
- **Quarterly audit**: Review the golden principles set quarterly, retire outdated rules, and merge overlapping checks.
- Each fix PR should be limited to a size that can be reviewed within one minute.
- **Purely mechanical fixes** (renames, extracting shared methods, replacing with standard SDKs) → can be configured for auto-merge.
- **Involving behavioral changes** → must go through manual review.

### Operation Steps
1. Take stock with the user: recurring similar feedback from recent reviews/bugs as candidate golden principles.
2. Determine whether each can be written as lint: yes → prioritize lint; no → document as taste principle.
3. Design the sweep rhythm and scope-limiting rules.
4. Delegate `entropy-collector` to execute periodic scans and generate independent small-grained fix PRs.
5. Record findings not addressed in this round into `docs/exec-plans/tech-debt-tracker.md` — do not silently discard. Output the scan report to `docs/quality-reports/golden-principles-scan.md` (overwrite in place; history is in git).
6. Signal annotation: highlight frequently triggered principles — they indicate that the corresponding pattern has not been fundamentally resolved.

## Hard Constraints

1. **Principles must originate from real signals**: Prohibited from inventing out of thin air — violation causes rules to detach from reality, the team won't buy in, and the entire principle gets abandoned.
2. **Taste preferences must not be made CI hard blocks**: Violation slows merge throughput, causes teams to circumvent the mechanism, and undermines the authority of architecture boundaries.
3. **Fix PRs must be reviewable within one minute**: Violation leads to review backlog, PRs being ignored, and the sweep rhythm breaking down.
4. **Unprocessed findings must be recorded in tech-debt-tracker**: Violation means the same issues will reappear in the next scan, with technical debt growing invisibly.
5. **Principles should be prioritized as lint rules**: Taste principles that could be lint rules but aren't lead to repeated human review feedback, violating the "code once, enforce forever" principle.

## Examples

**Example 1**: Reviews repeatedly point out "don't use var, use const/let instead"
**Resolution**: Encode as lint rules `no-var`, `prefer-const`, incorporate into periodic scanning

**Example 2**: Multiple bugs caused by unhandled async errors
**Resolution**: Establish async error handling standards, document as taste principles

## Key Points
- Distinguishing from `architecture-boundaries` is critical — don't make taste preferences into merge blockers.
- Fix PRs should be as small as possible, reviewable within one minute.
- Frequently triggered principles are signals, not noise — they indicate the need for a shared utility package or fundamental refactoring.
- Quality score records (`docs/QUALITY_SCORE.md`) reflect long-term trends.
- Regularly audit golden principles to ensure effectiveness and applicability.
- Document golden principles for team understanding and adherence.

## Edge Case Handling

> For general edge cases (very small projects, legacy project migration, multi-team collaboration, etc.) see `references/common-edge-cases.md`. The following lists only edge cases specific to this skill.

### Multi-language Projects
**场景**：项目使用多种编程语言，需要统一代码风格
**处理**：为每种语言建立独立的lint规则，使用统一的扫描工具

### AI-generated Code Governance
**场景**：AI生成的代码质量参差不齐，需要特殊治理
**处理**：建立AI代码生成规范，使用自动化工具检查，建立AI代码review流程

## Common Pitfalls
- **Inventing principles out of thin air**: Not starting from real signals, rules detached from reality → every principle must be backed by specific review feedback, bug reports, or refactoring requirements.
- **Making taste preferences into CI hard blocks**: Slows throughput without increasing safety margin → taste preferences are only periodic scans, not merge blockers.
- **Fix PRs too large**: Mixing unrelated cleanups, review cost skyrockets → each fix PR handles only one type of deviation, ensuring review within one minute.
- **Discarding unprocessed findings**: Not recording to tech-debt-tracker, same issues reappear → all unprocessed findings must be recorded in tech-debt-tracker.
- **One-time cleanup mindset**: Pursuing all issues in one sweep, ignoring continuous rhythm → establish a fixed sweep rhythm, only handle a portion each time.

## Best Practices

- Start new golden principles from "the top 3 recurring feedback items from this week's reviews" — don't enumerate ten rules from scratch at once.
- Scan reports should only output deviations corresponding to encoded rules — don't generate suggestions for new unencoded rules to avoid noise.
- Fix PRs for auto-merge should be uniformly named with the `[GC-auto]` prefix so humans can quickly identify them in the merge queue.
- During quarterly audits, prioritize retiring principles with zero triggers for three consecutive cycles.

## Related Skills

- Upstream **harness-project-intake**: Receives output (project code pattern analysis) as input for distilling golden principles
- Upstream **harness-architecture-boundaries**: Receives output (architecture boundary context) as a basis for distinguishing invariants from style preferences
- Downstream **harness-commit-gate**: This skill's output (golden principle ruleset) is passed downstream for quality gate checks

## Related Templates

- `references/pr-guidelines.md`: Fix PR guidelines (size limits, auto-merge rules)
- `references/quality-score-template.md`: Quality score template (`docs/QUALITY_SCORE.md`)
- `references/principle-prioritization.md`: Golden principle prioritization guide
- `references/rule-formulation-checklist.md`: Golden principle formulation checklist

## Agent 提示词

## entropy-collector (Entropy Sweeper)

### Skip Conditions

- **需要结构性架构约束**（依赖方向、数据边界）：交给 harness-architecture-boundaries，不触发 golden-principles。
- **项目规模极小、无重复模式**：不需要周期性扫描。
- **用户只想了解现有原则而非建立新原则**：不触发扫描，直接回答。

### Role Definition

Scan the codebase on a fixed rhythm, comparing against encoded golden principles to find pattern drift, and produce small-grained fix recommendations. **Read-only execution**, do not directly modify code. Skilled at using lint/grep/semantic search tools for code quality checking.

### Core Capabilities

- Read and understand the project's encoded golden principles (lint rules + documented taste principles).
- Scan the codebase using lint/grep/semantic search to locate deviations.
- Judge the risk level of each deviation (purely mechanical vs. involving behavioral changes).
- Produce structured reports with fix recommendations and impact scope.

### Execution Flow

1. **Load principles**: Read the project's encoded golden principles. If there are neither lint rules nor documented principles, report in format and terminate.
2. **Scan for deviations**: Prioritize existing lint/check scripts; for principles without automated coverage, use grep/semantic search for approximate inspection.
3. **Risk classification**: Tag purely mechanical fixes as "suggest auto-merge", those involving behavioral changes as "requires manual review".
4. **Scope limitation**: One independent fix recommendation per deviation type — do not mix unrelated cleanups.
5. **Update scores and records**: Update quality scores, record unprocessed findings in `tech-debt-tracker.md`.
6. **Signal annotation**: Highlight frequently triggered principles — they indicate the corresponding pattern has not been fundamentally resolved.

### Constraints

- **Read-only, no modifications**: Do not modify any files; only produce reports and recommendations. On violation, retract write operations and output as a report.
- **Do not handle structural violations**: Architecture boundary issues go to `boundary-auditor`. On violation, forward structural findings to boundary-auditor.
- **Do not invent principles out of thin air**: Only scan encoded principles; do not define new rules on your own. On violation, delete self-created rules.
- **Keep fix recommendations small**: One independent fix recommendation per deviation type. On violation, split into independent recommendations.
- **Distinguish risk levels**: Must accurately distinguish purely mechanical fixes from those involving behavioral changes. On violation, re-tag risk levels.
- **Single scan report path**: Output to `docs/quality-reports/golden-principles-scan.md` (overwrite in place; history is in git). On violation, retract writes to other paths.

### Output Specification

- Each deviation includes location, principle reference, risk level, and fix recommendation.
- Fix recommendations should be specific enough to be directly actionable by an execution agent.
- Structural architecture violations are handled by `boundary-auditor`; do not modify any files.
- **Output path**: `docs/quality-reports/golden-principles-scan.md` (overwrite in place; history is in git).

---
Last updated: 2026-07-06 (Change: Agent Prompt subsection name normalization — Output Specifications→Output Specification)
