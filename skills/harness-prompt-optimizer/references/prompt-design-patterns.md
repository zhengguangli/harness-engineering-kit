# Prompt Design Patterns Reference

## Pattern Overview

| Pattern | Applicable Scenarios | Complexity |
|---|---|---|
| Role-Anchor | Tasks requiring a specific professional perspective | Low |
| Execution-Chain-Driven | Multi-step workflow tasks | Medium |
| Constraint-First | High-risk / High-precision tasks | Medium |
| Example-Driven | Output-format-sensitive tasks | Medium |
| Hybrid | Complex comprehensive tasks | High |

## Pattern 1: Role-Anchor

Anchor the LLM's behavior boundaries through precise role definition.

**Applicable Scenarios**: Code review, technical writing, professional consulting

**Structure**:
```markdown
# Role
You are a [specific role] with [X] years of experience in [domain].
Your specialties are [skill 1], [skill 2], [skill 3].

# Background
[Task background and context]

# Rules
1. [Rule 1]
2. [Rule 2]

# Output
[Output format requirements]
```

**Design Points**:
- Role definition should be specific enough to be distinguishable (not "helpful assistant")
- Include domain of expertise and years of experience to increase anchoring effect
- Specialty list ≤ 5 items, focus on core capabilities

**Example Comparison**:
```markdown
# ❌ Bad: Too generic
You are a helpful assistant.

# ✅ Good: Specific and distinguishable
You are a senior TypeScript engineer with 8 years of experience in distributed systems.
Your specialties include: performance optimization, error handling patterns, and API design.
You prioritize type safety and always consider edge cases.
```

## Pattern 2: Execution-Chain-Driven

Use numbered steps to force the LLM to execute in a specific order.

**Applicable Scenarios**: Data processing, analysis workflows, multi-step decisions

**Structure**:
```markdown
# Execution Chain
1. [Step 1]: [Specific operation] → Output: [Intermediate result]
2. [Step 2]: Based on [Intermediate result], perform [Operation] → Output: [Intermediate result]
3. [Step 3]: Verify if [Intermediate result] meets [Condition]
4. [Step 4]: If met, perform [Operation]; if not, perform [Fallback operation]
```

**Design Points**:
- Each step has clear input and output
- Step count ≤ 7 (split if exceeded)
- Include judgment and branching logic
- Each step's output is the next step's input

**Anti-Patterns**:
- ❌ Vague step descriptions — "Analyze data" is less effective than "Count occurrences per category"
- ❌ Missing termination conditions — every path must have a clear endpoint
- ❌ No data flow between steps — previous step's output not used by the next step

## Pattern 3: Constraint-First

Eliminate the LLM's hallucination space through strict constraints.

**Applicable Scenarios**: Financial calculations, medical advice, legal documents, safety-related

**Structure**:
```markdown
# Constraints
- [Constraint 1]: [Rule]. Violation: [Handling method]
- [Constraint 2]: [Rule]. Violation: [Handling method]
- [Constraint 3]: [Rule]. Violation: [Handling method]

# Safety Rules
- Never [high-risk operation]
- If uncertain, [safe degradation behavior]
```

**Design Points**:
- Each constraint includes "what to do when violated"
- Constraint count ≤ 8 (LLM violates more with too many constraints)
- Safety rules listed separately, highest priority
- Include degradation behavior for "when uncertain"

**Example**:
```markdown
# Constraints
- Only use provided data, do not fabricate numbers. Violation: Output "Insufficient data, unable to calculate"
- All calculation results rounded to 2 decimal places. Violation: Recalculate and correct
- Do not give medical advice, only provide information reference. Violation: Remove advice content, note "For reference only"

# Safety Rules
- Never fabricate drug dosages or treatment plans
- If uncertain, output "Please consult a professional doctor"
```

## Pattern 4: Example-Driven

Use few-shot examples to anchor the LLM's output format and behavior.

**Applicable Scenarios**: Format conversion, content generation, classification tasks

**Structure**:
```markdown
# Examples

## Example 1: Standard Case
Input: [Input 1]
Output: [Output 1]

## Example 2: Edge Case
Input: [Input 2]
Output: [Output 2]

## Example 3: Error Case
Input: [Input 3]
Output: [Output 3]
```

**Design Points**:
- At least 3 examples: standard + edge case + error case
- Examples and rules must not conflict (when conflicting, LLM follows examples)
- Examples should cover the most important 80% of scenarios
- Each example includes complete input → output

**Anti-Patterns**:
- ❌ Only happy path — LLM behavior becomes unpredictable at boundary conditions
- ❌ Examples and rules conflict — LLM typically follows examples over rules
- ❌ Too many examples — 3-5 is optimal; too many dilute the impact of key examples

## Pattern 5: Hybrid

Combine multiple patterns for complex tasks.

**Structure**:
```markdown
# Role
[Role definition]

# Background
[Context]

# Variables Dictionary
[Variable declarations]

# Execution Chain
[Execution steps]

# Constraints
[Constraint rules]

# Output Schema
[Output format]

# Examples
[Examples]
```

**This is the six-block template** — when the task is complex enough to require multiple patterns, use the full six-block structure.

## Pattern Selection Decision Tree

```
Does the task require a specific professional perspective?
├── Yes → Role-Anchor
└── No → Is the task a multi-step process?
    ├── Yes → Execution-Chain-Driven
    └── No → Does the task have high risk/precision requirements?
        ├── Yes → Constraint-First
        └── No → Is the task output-format-sensitive?
            ├── Yes → Example-Driven
            └── No → Task is simple, no complete pattern needed
```

## Pattern Combination Guide

| Combination | Applicable Scenarios | Example |
|---|---|---|
| Role-Anchor + Constraint-First | Professional domain, high-risk tasks | Medical consultation, legal review |
| Execution-Chain + Example-Driven | Multi-step process + format sensitive | Data processing pipeline |
| Role-Anchor + Execution-Chain | Professional domain, multi-step tasks | Code review process |
| Constraint-First + Example-Driven | High-precision format tasks | Financial report generation |

## Common Design Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Role definition too generic | LLM behavior has no anchor | Specify role and expertise |
| Too many constraints | LLM violates more | Select ≤ 8 key constraints |
| Only happy path examples | Unpredictable behavior at boundaries | Add edge case and error case |
| Examples and rules conflict | LLM follows examples over rules | Fix conflicts, maintain consistency |
| Execution chain too many steps | LLM loses context | Keep ≤ 7 steps |
| Missing violation consequences | Constraints are ineffective | Add "what to do when violated" per constraint |
