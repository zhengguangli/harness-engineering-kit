# Implicit Trigger Patterns

How `harness-prompt-optimizer` proactively identifies scenarios suitable for prompt optimization even when the user doesn't explicitly name it. This file serves as a detailed reference for the SKILL.md frontmatter `when_to_use` field — read this file when uncertain about a decision.

## Explicit Trigger Keywords

Sentences where the user directly expresses intent:

- "帮我写一个 prompt / system prompt / 提示词"
- "优化 / 改进 / 完善这个 prompt"
- "这个 prompt 效果不好 / 不准确 / 不稳定"
- "我需要一个 system prompt 给 XXX"
- "write me a prompt for XXX"
- "optimize / improve / refine this prompt"
- "this prompt doesn't work well"

## Implicit Trigger Scenarios

The following cases do not mention "prompt" explicitly, but fundamentally require prompt optimization:

### Scenario 1: Describing Complex Requirements Without Structure

The user describes a task that requires the AI to execute repeatedly, but without structure:

- "我希望 AI 能帮我 review 代码，找出 bug 和不好的写法"
- "我想让 AI 从网页里提取商品价格"
- "帮我写个让 AI 写营销文案的东西"
- "I want an agent that can analyze financial reports"

→ Suggestion: "This requirement is well-suited to be converted into a structured prompt. Would you like me to help optimize it?"

### Scenario 2: Pasting a Prompt Without Stating Intent

The user pastes text that looks like a prompt/instruction:

- Pastes text containing "You are...", "你的任务是..."
- Pastes a numbered list of instructions
- Pastes text containing constraints/rules

→ Ask: "Does this prompt need optimization? I can help improve its structure and constraints."

### Scenario 3: Agent Behavior Not Meeting Expectations

The user is debugging agent or AI behavior:

- "这个 agent 行为不对 / 输出格式不稳定"
- "AI 总是 hallucinate / 编造信息"
- "AI 不按我说的做"
- "the agent keeps ignoring my instructions"
- "output format is inconsistent"

→ Evaluate whether the prompt is missing constraints or examples, suggest optimization.

### Scenario 4: Building an Agent/Automation Pipeline

The user is building a system that requires a system prompt:

- "我在做一个 code review bot"
- "我在搭建一个数据提取 pipeline"
- "I'm building an agent that does XXX"
- "需要一个 system prompt 给我的 chatbot"

→ Proactively offer prompt optimization capabilities.

### Scenario 5: User Says "optimize this XXX" But XXX Is Not a Prompt

The user uses "optimize" but the target is not a prompt (see SKILL.md judgment table):

- "优化这个**指令**" → could be a prompt
- "优化这个**规范**" → could be a prompt
- "优化这个**函数**" → not a prompt
- "优化这个**文档**" → not a prompt

→ Ask for clarification when uncertain.

## Keyword Combination Triggers

When the user's message contains a combination of **action word + object word**, prioritize prompt optimization scenarios:

| Action Words | Object Words |
|---|---|
| 优化、改进、完善、增强、提升、看看、分析、诊断、写、设计 | prompt、提示词、system prompt、指令、建议、规范、规则、指南、模板 |
| optimize, improve, refine, enhance, write, design, review | prompt, system prompt, instruction, guideline, template |

Combination examples:
- "帮我看看这个**指令**" → Ask if prompt optimization is needed
- "优化这个**建议**" → Ask if prompt optimization is needed
- "设计一套**规则**给 AI 用" → Suggest converting to a structured prompt
- "review this **instruction**" → Ask if prompt optimization is needed

## Decision Flow

```
User message
  ├─ Contains explicit trigger keywords? → Enter optimization flow directly
  ├─ Matches implicit trigger scenario? → Ask for confirmation, then enter
  ├─ Contains action word + object word combination? → Ask for confirmation, then enter
  └─ No match → Do not trigger
```

## Usage

Read this file as supplementary reference when the main conversation's decision is uncertain.

## Maintenance

This file is kept in sync with the SKILL.md frontmatter `when_to_use`. If new implicit trigger patterns are discovered, add them here first, then add a pointer in `when_to_use`.
