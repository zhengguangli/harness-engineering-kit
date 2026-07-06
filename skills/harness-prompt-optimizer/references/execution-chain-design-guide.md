# Execution Chain Design Guide

## What is an Execution Chain

An Execution Chain is a numbered list of task execution steps within a prompt — it forces the LLM to follow a specific order rather than deciding the flow on its own.

## Why You Need an Execution Chain

| Without Execution Chain | With Execution Chain |
|---|---|
| LLM decides the execution order | Enforces step-by-step execution |
| Skips steps or processes out of order | Steps have data flow |
| Unpredictable output | Reproducible output |
| Hard to debug | Each step can be independently verified |

## Design Principles

### Principle 1: Steps ≤ 7

The LLM's context window is limited; too many steps will cause it to lose context from earlier steps.

```markdown
# ❌ Bad: Too many steps
1. Step 1
2. Step 2
3. Step 3
...
10. Step 10

# ✅ Good: Concise steps
1. Step 1
2. Step 2
3. Step 3
4. Step 4
```

**If steps exceed 7**:
- Merge related steps
- Split into sub-prompts
- Use conditional branching to reduce linear steps

### Principle 2: Each Step Has Clear Input and Output

```markdown
# ❌ Bad: No data flow
1. Analyze data
2. Generate report
3. Check quality

# ✅ Good: Has data flow
1. Parse input data → Output: structured data object
2. Calculate metrics across dimensions of structured data → Output: metrics summary
3. Generate report based on metrics summary → Output: report text
4. Check report text against specifications → Output: check result
```

### Principle 3: Steps Must Be Executable

```markdown
# ❌ Bad: Vague
1. Consider various scenarios
2. Make the best decision
3. Ensure quality

# ✅ Good: Specific
1. List all possible classifications (max 5)
2. Count occurrences for each classification
3. Sort by occurrence count in descending order
4. Select the top 3 classifications as key findings
```

### Principle 4: Include Decisions and Branching

```markdown
1. Check if input data format is JSON
   - Yes → proceed to step 2
   - No → output error message, terminate flow
2. Parse JSON data
3. Verify required fields exist
   - Yes → proceed to step 4
   - No → output missing fields list, terminate flow
4. Perform data analysis
```

## Execution Chain Templates

### Linear Flow

```markdown
# Execution Chain
1. [Input Processing]: Receive {{input}}, validate format → Output: validated_input
2. [Core Processing]: Analyze validated_input → Output: analysis_result
3. [Output Generation]: Generate output based on analysis_result → Output: final_output
4. [Verification]: Check final_output against specifications → Output: verification result
```

### Conditional Branching Flow

```markdown
# Execution Chain
1. Determine task type: {{task_type}}
   - "analysis" → proceed to step 2
   - "generation" → proceed to step 4
   - "review" → proceed to step 6

2. [Analysis Flow]: Perform data analysis → Output: analysis_result
3. Generate report based on analysis_result → Output: report, terminate

4. [Generation Flow]: Generate content based on {{requirements}} → Output: draft
5. Review draft quality → Output: final content, terminate

6. [Review Flow]: Check {{target}} against specifications → Output: review report, terminate
```

### Loop Flow

```markdown
# Execution Chain
1. Generate initial solution → Output: current_solution
2. Evaluate quality of current_solution → Output: evaluation_result
3. Determine if evaluation_result meets the standard
   - Yes → output current_solution, terminate
   - No → proceed to step 4
4. Optimize current_solution based on evaluation_result → Output: new_solution
5. Assign new_solution to current_solution → Return to step 2

# Constraint: Maximum 3 iterations. If still not meeting standard, output the best current solution
```

## Step Granularity Control

| Granularity | Applicable Scenarios | Example |
|---|---|---|
| Coarse | Simple tasks | "1. Analyze 2. Generate 3. Check" |
| Medium | Moderate complexity | "1. Parse 2. Count 3. Compare 4. Output" |
| Fine | Complex tasks | One step per sub-operation |

**Selection Principle**: Each step should be a complete, independently verifiable operation. If a step needs to be further broken down to be understood, the granularity is too coarse.

## Coordination with Variables Dictionary

Referencing variables from the Variables Dictionary in the Execution Chain:

```markdown
# Variables Dictionary
| Variable | Type | Required | Description |
|---|---|---|---|
| input_data | string | Yes | Input data |
| output_format | enum | Yes | Output format |

# Execution Chain
1. Parse {{input_data}} → Output: parsed_data
2. Analyze parsed_data → Output: analysis
3. Format analysis according to {{output_format}} → Output: final result
```

## Coordination with Constraints

Every step in the Execution Chain is subject to Constraints:

```markdown
# Execution Chain
1. Parse input data → Output: parsed_data
2. Analyze parsed_data → Output: analysis

# Constraints
- In step 1: Only parse provided data, do not fabricate fields
- In step 2: Only use fields present in parsed_data for analysis
- In step 2: If data is insufficient, output "Insufficient data, unable to analyze" rather than guessing
```

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Too many steps (> 7) | LLM loses context | Merge or split |
| Vague steps | LLM interprets on its own | Make each step concrete |
| No data flow | Disconnected steps | Clarify input/output relationships |
| No decision branching | Same route for all cases | Add conditional checks |
| Missing termination conditions | Infinite loop | Every path has an endpoint |
| Steps not executable | LLM skips them | Ensure each step is independently executable |

---
Last updated: 2026-07-03
