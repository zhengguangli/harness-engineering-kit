# Context Budget Management Guide

## Core Principle

Context windows are scarce resources. Every design decision should answer one question: **What is the impact of this content on the context budget?**

## Three-Layer Loading Mechanism

### Layer 1: Metadata (Always Resident)

**Budget**: ~100 words (name + description + when_to_use)

**Design Points**:
- name: Short and clear for easy retrieval (≤ 5 words)
- description: What it does + When to use (≥ 20 characters)
- when_to_use: Explicit/implicit trigger conditions + non-trigger conditions

**Example Comparison**:

```yaml
# ❌ Bad: vague, indistinguishable
description: Helps with code-related tasks

# ✅ Good: specific, distinguishable
description: Guides how to write new skills or subagents for the harness system — following progressive disclosure and context budget principles. Used for "how to write a good SKILL.md", "add new capabilities to harness" scenarios.
```

**Common Mistakes**:
- ❌ description too short (< 20 characters) — trigger conditions unclear
- ❌ description too long (> 200 words) — wastes resident context
- ❌ when_to_use missing — trigger and non-trigger boundaries are blurry

### Layer 2: SKILL.md Body (Loaded on Trigger)

**Budget**: ≤ 500 lines

**Design Points**:
- Core principles ≤ 5 (one sentence each)
- Execution flow steps ≤ 7
- Hard constraints ≤ 5
- Best practices per category ≤ 5

**Suggested Section Structure**:

| Section | Suggested Lines | Content |
|---|---|---|
| Core Principles | 10-20 lines | 3-5 core beliefs |
| When to Use | 10-20 lines | Trigger conditions (explicit/implicit/non-trigger) |
| Methodology | 50-150 lines | Core process and decision framework |
| Operation Steps | 30-80 lines | Concrete execution steps |
| Hard Constraints | 10-20 lines | Inviolable rules |
| Edge Cases | 20-40 lines | Skill-specific edge cases |
| Best Practices | 30-60 lines | Categorized best practices |
| Common Pitfalls | 10-20 lines | Typical mistakes |
| Agent Prompt | 50-150 lines | Agent system prompt |

**Blow-up Detection Signals**:
- A single section exceeds 100 lines → consider splitting into references/
- Total lines approach 450 → plan ahead for splitting
- "See details in..." appears without a corresponding file → need to create a references file

### Layer 3: Bound Resources (Loaded on Demand)

**Budget**: Unlimited (but each file should stay within reasonable bounds)

**File Organization Principles**:

```
references/
├── quick-reference.md      # Quick reference table (< 100 lines)
├── deep-dive-*.md          # Deep dive guides (each < 200 lines)
├── templates/              # Template files
├── examples/               # Example files
└── scripts/                # Executable scripts
```

**Loading Guide Style**:

```markdown
## In-Depth Reference
- Quick design pattern lookup → `references/quick-reference.md`
- Deep dive into a pattern → `references/deep-dive-{pattern-name}.md`
- Ready-to-copy templates → `references/templates/`
```

**Principle**: The body text should say "under what circumstances to read which reference file", not "detailed content follows below".

## Budget Monitoring Methods

### Line Count Check

```bash
# Check body line count of SKILL.md (excluding frontmatter)
total_lines=$(wc -l < SKILL.md)
frontmatter_end=$(awk '/^---$/{count++; if(count==2) print NR}' SKILL.md)
body_lines=$((total_lines - frontmatter_end - 1))
echo "Body lines: $body_lines"
if [ $body_lines -gt 450 ]; then
    echo "⚠️  Warning: Body approaching 500 line limit"
fi
```

### Content Density Check

| Metric | Pass Standard | Over-limit Action |
|---|---|---|
| Core principle count | ≤ 5 | Merge or move to references/ |
| Execution flow steps | ≤ 7 | Split into sub-processes |
| Hard constraints count | ≤ 5 | Merge or move to references/ |
| Lines per section | ≤ 100 | Split into references/ |
| Example count | ≤ 5 | Keep the 3 most typical |

## Split Strategy

### When to Split

- Body approaching 450 lines
- A single section exceeds 100 lines
- "See details in..." appears without a corresponding file
- Same information appears in multiple places (high maintenance cost)

### How to Split

**Method 1: Split by Topic**
```
Original SKILL.md (500 lines)
├── SKILL.md (trimmed to 300 lines)
├── references/pattern-a.md (100 lines)
├── references/pattern-b.md (100 lines)
└── references/examples.md (80 lines)
```

**Method 2: Split by Depth**
```
Original SKILL.md (500 lines)
├── SKILL.md (trimmed to 200 lines, only core process)
├── references/quick-reference.md (100 lines, quick lookup)
└── references/deep-dive.md (200 lines, in-depth guide)
```

**Method 3: Split by Role**
```
Original SKILL.md (500 lines)
├── SKILL.md (methodology section)
├── references/agent-guide.md (agent execution section)
└── references/templates.md (template section)
```

### Post-Split Reference Convention

```markdown
## Write loading guide in body text
- Design pattern details → `references/skill-design-patterns.md`
- Context management details → `references/context-budget-management-guide.md`
- Cross-platform sync details → `references/cross-platform-sync-guide.md`

## Reference in Agent Prompt
Use the `skills` field to preload related skills instead of duplicating content in the system prompt.
```

## Common Budget Problems and Solutions

| Problem | Cause | Solution |
|---|---|---|
| Body exceeds 500 lines | Everything crammed into the body | Split into references/ |
| Resident content too large | description written too long | Trim to core information |
| Missing loading guide | Split without adding references | Add "under what circumstances to read which file" |
| Information duplication | Same content appears in both body and references | Body only has summary, details go in references/ |
| Inaccurate triggering | Vague description | Specify trigger scenarios |

## Budget Optimization Checklist

When creating/modifying a skill, check each item:

- [ ] Is description ≤ 200 words?
- [ ] Does description include both "what it does" and "when to use"?
- [ ] Is the body ≤ 500 lines?
- [ ] Is each section ≤ 100 lines?
- [ ] Are core principles ≤ 5?
- [ ] Are execution flow steps ≤ 7?
- [ ] Are hard constraints ≤ 5?
- [ ] Is there a references/ subdirectory for on-demand loading?
- [ ] Does the body say "under what circumstances to read which reference file"?
- [ ] Is information duplication between body and references avoided?
