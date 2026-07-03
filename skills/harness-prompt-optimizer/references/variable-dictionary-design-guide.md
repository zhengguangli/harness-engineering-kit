# Variable Dictionary Design Guide

## What is a Variable Dictionary

A Variable Dictionary is a declaration of dynamic inputs within a prompt — it tells the LLM "these values will be injected at runtime, you don't need to assume them yourself."

## Why You Need a Variable Dictionary

| Without Variable Dictionary | With Variable Dictionary |
|---|---|
| LLM makes assumptions about the scenario | LLM knows the input source |
| Hard-coded example values | Dynamically injected actual values |
| Unstable output format | Output corresponds to input |
| Hard to reuse | Same prompt applicable to different inputs |

## Variable Dictionary Structure

```markdown
# Variables Dictionary

| Variable | Type | Required | Description | Example Value |
|---|---|---|---|---|
| user_input | string | Yes | User's original input | "Help me optimize this code" |
| target_language | string | No | Target output language | "zh" / "en" |
| max_length | number | No | Maximum output length | 500 |
| context | object | No | Additional context information | {"project": "my-app"} |
```

## Design Principles

### Principle 1: Explicitly Declare All Dynamic Inputs

```markdown
# ❌ Bad: Undeclared variables
Please analyze the issues in this code.

# ✅ Good: Explicit declaration
# Variables Dictionary
| Variable | Type | Required | Description |
|---|---|---|---|
| code_snippet | string | Yes | Code snippet to analyze |
| language | string | Yes | Programming language (e.g., "typescript") |
| focus | string | No | Focus area ("performance" / "readability" / "security") |

Please analyze the issues in the following code:
```{{language}}
{{code_snippet}}
```
Focus area: {{focus}}
```

### Principle 2: Semantic Variable Names

```markdown
# ❌ Bad: Meaningless variable names
| Variable | Description |
|---|---|
| x | Input |
| y | Output |

# ✅ Good: Self-explanatory variable names
| Variable | Description |
|---|---|
| raw_user_message | User's original message |
| parsed_intent | Parsed user intent |
| response_format | Response format requirements |
```

### Principle 3: Provide Default Values or Mark as Optional

```markdown
# Variables Dictionary
| Variable | Type | Required | Default | Description |
|---|---|---|---|---|
| language | string | No | "en" | Output language |
| verbose | boolean | No | false | Whether to output detailed explanation |
| max_retries | number | No | 3 | Maximum retry count |
```

### Principle 4: Variable Reference Methods in the Prompt

```markdown
# Method 1: Mustache Template (Recommended)
Please answer the following question in {{language}}:
{{question}}

# Method 2: Placeholder
Please answer the following question in [LANGUAGE]:
[QUESTION]

# Method 3: Natural Language Reference
Please answer the question in the language specified by the language variable.
```

## Variable Type Design

### Basic Types

| Type | Description | Example |
|---|---|---|
| string | Text | "hello" |
| number | Numeric | 42 |
| boolean | Boolean | true / false |
| enum | Enumeration | "en" / "zh" |

### Composite Types

| Type | Description | Example |
|---|---|---|
| object | Object | {"key": "value"} |
| array | Array | ["item1", "item2"] |
| union | Union type | string \| number |

### Type Constraints

```markdown
# Variables Dictionary
| Variable | Type | Constraint | Description |
|---|---|---|---|
| temperature | number | 0.0 - 2.0 | Generation temperature |
| top_p | number | 0.0 - 1.0 | Nucleus sampling parameter |
| max_tokens | number | ≥ 1 | Maximum generation tokens |
| language | enum | "en" \| "zh" \| "ja" | Output language |
```

## Coordination with Execution Chain

The Variable Dictionary provides input for the Execution Chain:

```markdown
# Variables Dictionary
| Variable | Type | Required | Description |
|---|---|---|---|
| raw_data | string | Yes | Raw data (JSON format) |
| target_metric | string | Yes | Target metric name |
| threshold | number | Yes | Threshold value |

# Execution Chain
1. Parse {{raw_data}} into structured data
2. Extract the value of {{target_metric}}
3. Compare the value with {{threshold}}
4. Output comparison result and suggestion
```

## Coordination with Output Schema

Variables from the Variable Dictionary may appear in the output:

```markdown
# Variables Dictionary
| Variable | Type | Required | Description |
|---|---|---|---|
| analysis_target | string | Yes | Analysis target |
| report_format | enum | Yes | Report format ("brief" / "detailed") |

# Output Schema
{
  "target": "{{analysis_target}}",  // Variable reference
  "format": "{{report_format}}",    // Variable reference
  "findings": [...],
  "recommendations": [...]
}
```

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Undeclared variables | LLM assumes values on its own | Explicitly declare all dynamic inputs |
| Non-semantic variable names | Difficult to maintain | Use descriptive variable names |
| Missing type constraints | LLM output format unstable | Add types and constraints |
| Too many variables | High maintenance cost | Trim to essential variables |
| Missing default values | Must provide all variables every time | Provide defaults for optional variables |
| Variables and example values don't match | LLM confused | Keep variable declarations and examples consistent |
