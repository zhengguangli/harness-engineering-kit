# Common Edge Cases Reference

## Overview

This document summarizes common edge cases handled by Prompt Optimizer. Reference this document to avoid redefining them in SKILL.md.

## Common Edge Cases

### 1. Extremely Vague User Requirements

**Scenario**: User describes with only a few words (e.g., "optimize this", "help me fix it"), without providing the original prompt or context

**Handling Principles**:
- First ask the user to provide the original prompt to be optimized or a more detailed description
- If the user still doesn't provide it, generate a basic template with minimal role + task structure
- Note: "Based on limited information, it is recommended to add specific scenarios for better results"

### 2. Very Short Original Prompt (< 10 words)

**Scenario**: The user's prompt is only one sentence or a short phrase

**Handling Principles**:
- Accept short input without making it mandatory
- Automatically infer missing modules (role definition, constraints, output format)
- When outputting, note: "The following modules are empty. It is recommended to supplement: X, Y, Z"
- Do not refuse to work just because the prompt is short

### 3. Already Highly Structured Original Prompt

**Scenario**: The user's prompt already has a complete structure such as role, execution chain, output schema, etc.

**Handling Principles**:
- Identify existing structure and missing modules
- Gap rate < 20%: Make fine-tuning and optimizations without restructuring the whole thing
- Gap rate 20-50%: Supplement missing modules while preserving existing structure
- Only restructure the whole thing when gap rate > 50%

**Judgment Method**: Check block by block according to the six-block template (Role, Variables Dictionary, Execution Chain, Constraints, Output Schema, Examples)

### 4. Repeatedly Optimizing the Same Prompt

**Scenario**: The user repeatedly submits the same prompt for optimization

**Handling Principles**:
- Check for previous optimization history (reuse session context)
- From the second version onward, switch to "incremental optimization" mode: only adjust parts flagged in the previous version
- After the third version, ask the user "Is this satisfactory?" to avoid infinite loops

### 5. Multi-language Prompt Optimization

**Scenario**: The user provides a prompt containing non-English content, or requests multi-language output

**Handling Principles**:
- Keep the original prompt's language unchanged, unless the user requests translation
- Keep Chinese comments in the variables dictionary as Chinese
- Keep the output schema in the same language as the original prompt
- To produce multi-language versions, generate a complete set of prompts for each language separately

### 6. Non-LLM Prompt Content

**Scenario**: The user provides code, configuration files, or natural language instructions and asks to optimize them into an LLM prompt

**Handling Principles**:
- First confirm the user's intent: whether to convert this content into an LLM prompt, or to optimize the content itself
- When converting to a prompt, preserve the original semantics completely
- Note: "Original content has been fully encoded into the prompt"

## Usage Guide

Prompt Optimizer-specific edge cases are written directly in this file. When handling edge cases:
1. If it is a common type, reference the corresponding section of this document
2. Follow the format: Scenario → Handling Principles (1-2 lines)

---
Last updated: 2026-07-03
