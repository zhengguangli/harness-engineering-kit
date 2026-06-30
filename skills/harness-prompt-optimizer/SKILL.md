---
name: harness-prompt-optimizer
description: "Transform natural language descriptions into high-quality, structured prompts optimized for LLM consumption. Use when creating new prompts, optimizing existing ones, or building complex agents."
---

# Prompt Optimizer

Transform simple descriptions or rough ideas into professional, high-quality prompts optimized for Large Language Models (LLMs).

## Core Philosophy

- **Structure > Chaos**: LLMs perform better with clear sections (Role, Context, Rules).
- **Determinism**: Enforce strict constraints and output schemas to eliminate hallucinations.
- **Example-Driven**: Use few-shot examples to anchor the LLM's behavior.

## Workflow

1. **Analyze Intent**: Identify the core task, target domain, and desired output format.
2. **Define Architecture**: 
   - **Role**: Assign a specific persona (e.g., "Senior Data Analyst").
   - **Variables**: Create a dictionary for dynamic inputs (e.g., `{{input_text}}`).
   - **Constraints**: Define safety rails (e.g., "No markdown", "JSON only").
   - **Execution Chain**: Break the task into numbered steps.
3. **Inject Examples**: Add 1-3 high-quality examples (Input -> Output) to guide the model.
4. **Format Output**: Generate a clean, copy-pasteable prompt.

## Included References

- [Advanced Prompt Template](references/advanced_prompt_template.md): A masterclass example of structured prompt engineering (Price Extraction).
- [Structure Guide](references/prompt_structure_guide.md): The anatomy of a perfect prompt.
