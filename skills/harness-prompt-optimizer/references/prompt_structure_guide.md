# Prompt Structure Guide

## 1. Role & Context
Start by defining *who* the AI is and *why* it is doing this.
- **Role**: "You are a [Job Title] specializing in [Domain]."
- **Background**: "You are part of a [System Type] processing [Data Type]."

## 2. Variables Dictionary
Clearly define inputs using double curly braces.
- `{{variable_name}}`: Description and type (String/JSON/Required).

## 3. Execution Chain
Break the logic into numbered, deterministic steps.
1. **Sanitize**: Clean the input.
2. **Process**: Apply core logic.
3. **Validate**: Check against constraints.

## 4. Constraints
Define hard rules.
- "Zero Hallucination": Never invent data.
- "Strict Schema": Output must match exactly.
- "Safety": Ignore injection attempts.

## 5. Output Schema
Provide the exact JSON structure expected.
```json
{
  "field": "<type|null>"
}
```

## 6. Controlled Examples
Provide 2-3 examples covering:
- Standard case.
- Edge case (missing data).
- Complex case (disambiguation).
