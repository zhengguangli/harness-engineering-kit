---
name: harness-authoring
description: Guide on how to write new skills, subagents, or expand the knowledge base for this harness system — following progressive disclosure and context budget principles. Used for writing good SKILL.md files, adding new capabilities, deciding skill vs subagent, and sliming existing skills.
when_to_use: |
  显式触发：用户要给 harness 工具集添加新能力、问"怎么写一个好的 SKILL.md"、问"这应该做成 skill 还是 subagent"、要求给已有 skill 瘦身。
  隐式触发：发现某个 agent/skill 内容越写越臃肿需要拆 references、新建能力前未检查与已有能力重叠。
  不触发：用户要创建与 harness 体系无关的独立工具、只想了解现有 skill 用法而非扩展体系、项目不使用 harness 方法论。
context: fork
agent: skill-scaffolder
compatibility: claude-code
allowed-tools: Bash(git *) Bash(grep *) Bash(rg *) Bash(find *) Bash(ls *) Bash(cat *) Bash(head *) Bash(wc *) Bash(echo *) Bash(date *)
metadata:
  category: meta
---
# Harness Authoring (Authoring New Skills / Agents)

## Core Principles

- **Context is a scarce resource**: Every design decision must consider its impact on the context budget — keep resident content as lean as possible, and prioritize on-demand loading.
- **Skill is knowledge, Subagent is execution**: Skills inject into the current context window for the main conversation to reference; Subagents have their own isolated context window for execution and only bring summary results back to the main conversation.
- **Principle of least privilege**: Read-only agents do not get `Edit`/`Write`; only execution agents get write access. Omitting the `tools` field means inheriting all tools, which is not the default safe option.

## When to Use

- The user wants to add a new capability to the harness toolset itself.
- The user asks "how to write a good SKILL.md" or "should this be a skill or subagent."
- An existing agent/skill is becoming bloated and needs trimming.

## When Not to Use

- The user wants to create an independent tool unrelated to the harness system.
- The project does not use the harness methodology.
- The user only wants to understand existing skill usage, not create a new skill.

## Methodology

### 1. Skill vs. Subagent Decision

| Dimension | Skill | Subagent |
|---|---|---|
| Nature | Knowledge/workflow injected into the **current** context window | An isolated execution unit with its **own** context window |
| When to use | The main conversation needs to "know how to do something" to continue reasoning | The task can be delegated to complete independently, only bringing summary results back to the main conversation |
| Context impact | Consumes the main context window's token budget when triggered | Barely consumes the main context budget (only the summary enters) |
| Parallelism | Not parallelizable (there's only one current context) | Can run multiple instances in parallel |

**Rule of thumb**: If the main conversation needs to "remember" something to continue reasoning, use a skill; if something can be "delegated out and wait for results", use a subagent. The two often appear paired (a skill defines the methodology, an agent with the same name handles execution) — this is not duplication, it is division of labor.

### 2. Context Budget Discipline for SKILL.md

Three-tier loading mechanism:

1. **Metadata (name + description)**: Always resident in context, roughly 100-word budget. Write it accurately and with "push" — help the agent remember to use it at the right time without false triggering.
2. **SKILL.md body**: Enters context only when the skill is triggered, keep it within 500 lines.
3. **Bound resources (references/, scripts/, assets/)**: Loaded on demand, no size limit.

When the body approaches 500 lines, split content into `references/` sub-files, and write clear loading instructions in the body.

### 3. The description Field Must "Push" But Not Exaggerate

- Clearly state both **what it does** and **when to use it** — "when to use it" is the primary trigger basis.
- Use concrete scenarios rather than abstract descriptions: "当用户说 A、B、C" triggers more reliably than "用于代码质量相关任务".
- Every claimed capability must be substantiated in the body — don't inflate for trigger rate.

### 4. Subagent Tool and Permission Discipline

- Read-only agents do not get `Edit`/`Write`; only execution agents do.
- Use the `skills` field to preload relevant skills, don't duplicate skill content in the system prompt — avoid maintaining two copies that will eventually drift out of sync.
- Choose the `model` field based on "judgment complexity": high-level reasoning uses a strong model, mechanical repetition uses a lightweight model.

### 5. Combating Context Rot

- Dump large tool outputs to files, keep only the head/tail summary plus file path in the conversation.
- Use exec-plans to persist state for complex tasks instead of relying on a single context window to track progress.
- 5 rules with concrete consequences are better than 50 rules piled together.

### 6. Steps to Add a New Capability

1. Decide whether it is a skill or a subagent.
2. Write the description: write "when to use it" first, then "what it does", ensuring it can be distinguished from existing capabilities.
3. Write the body, control the budget; anticipate bloat and plan `references/` in advance.
4. For subagents, list tools following minimal tool authorization, and explain the model selection rationale.
5. Check for overlap with existing capabilities — merge or define boundaries if overlap is found.
6. Register new pointers in CLAUDE.md/README.
7. Self-check: Body ≤ 500 lines? Tools with least privilege? description complete?

### 7. Agent Prompt Canonical Version Convention

- The `## Agent 提示词` section in `SKILL.md` is the canonical version — only edit prompts here.
- Do not use standalone `agents/<name>.md` files anymore.

## Hard Constraints

1. **Body must not exceed 500 lines**: When the SKILL.md body (including the Agent prompt) exceeds 500 lines, it must be split into references/ sub-files. Violation → rejected and required to split.
2. **description must clearly state both "what it does" and "when to use it"**: Stating only one is considered incomplete. Violation → supplement the missing part.
3. **Must check for overlap with existing capabilities before adding a new skill**: Use Grep/Glob to scan existing skills/. If overlap is found, it must be reported and a merge or boundary definition suggested. Violation → complete the overlap check first before proceeding.
4. **Configure agent tools with least privilege**: Read-only agents do not get Edit/Write; omitting the tools field inherits all tools (not the default safe option). Violation → re-authorize with minimal permissions.

## Examples

**Example 1**: User says "这应该做成 skill 还是 subagent"
**Judgment**: Knowledge the main conversation needs to reference continuously → skill; something that can execute independently and only return results → subagent

**Example 2**: New skill overlaps with existing harness-commit-gate
**Action**: Merge or clearly define boundaries, don't create choice paralysis between two similar options

**Example 3**: User says "这个 skill 超过 500 行了，帮我瘦身"
**Action**: Check current line count, identify content that can be extracted as complete topic blocks into `references/` sub-files, update `SKILL.md` body with loading instructions, and update navigation pointers in CLAUDE.md

**Example 4**: User says "我要加一个新 subagent 专门跑自动化测试"
**Action**: Determine it's a subagent (can execute independently), configure `allowed-tools` with test runner tools only (no `Write`/`Edit`), choose a lightweight model for test execution, and skip creating a full skill

## Key Points

- **Skill is knowledge, Subagent is execution**: The two appearing paired is division of labor, not duplication.
- **Context budget discipline**: Keep resident content lean, load on demand upfront, body ≤ 500 lines.
- **Principle of least privilege**: Read-only agents do not get write access; omitting tools is not the default safe option.
- **Three-tier loading mechanism**: Metadata resident → body loads on trigger → bound resources load on demand.
- **description must be truthful**: Every claimed capability must be substantiated in the body.
- **Avoid capability overlap**: Check existing capabilities before adding new ones; merge or define boundaries if overlap exists.
- **Canonical version**: `## Agent 提示词` is the single entry point for modifications.
- **Agent prompt and skill body are co-located**: Maintaining both in a single `SKILL.md` avoids the drift problem of separate agent prompt files — edit once, synchronize automatically.

## Related Templates

- `references/scaffold-templates.md`: Scaffolding templates for new skills and agents
- `references/skill-design-patterns.md`: Skill design patterns reference
- `references/subagent-design-patterns.md`: Subagent design patterns reference
- `references/context-budget-management-guide.md`: Context budget management guidelines
- `references/common-edge-cases.md`: General edge case handling guide

## Edge Case Handling

> For general edge cases, see `references/common-edge-cases.md`. The following list only covers edge cases specific to this skill.

### Skill vs. Subagent Confusion

**Scenario**: Unsure whether to make something a skill or a subagent
**Action**: If the main conversation needs to "remember" it to continue reasoning → skill; if it can be "delegated out and wait for results" → subagent

### Body Approaching 500 Lines

**Scenario**: The SKILL.md body is approaching 500 lines
**Action**: Split into references/ sub-files, write clear loading instructions in the body

### Overlap with Existing Capabilities

**Scenario**: A new skill/agent overlaps with existing capabilities
**Action**: Merge or clearly define boundaries, don't let the agent struggle between similar options

### description Exaggerating Capabilities

**Scenario**: Claims capabilities for trigger rate but the body does not deliver
**Action**: Every claimed capability must be genuinely substantiated in the body

### Subagent Tool Permission Escalation

**Scenario**: A subagent initially configured as read-only later needs write capability for a new task
**Action**: Explicitly update `allowed-tools` in the frontmatter — do not write silent exceptions in the agent prompt body, as this creates a gap between declared permissions and actual behavior

## Common Pitfalls

- **Skill and Subagent confusion**: Making a task that could be completed independently into a Skill, consuming the main context; or making knowledge that needs continuous reference into a Subagent, causing context discontinuity.
- **description exaggerating capabilities**: Claiming to do something for trigger rate without delivering it in the body.
- **Body bloat**: Not splitting when approaching 500 lines, causing context budget overruns.
- **Ignoring existing capability overlap**: Creating a new skill/agent without checking for overlap with existing capabilities, causing choice paralysis.

## Best Practices

- Use kebab-case for skill names, consistent with the directory name, for easy automated traversal and reference by scripts.
- Place loading instructions for references/ sub-files at the end of the body, before the Agent prompt, so the agent reads the loading guide first, then the execution flow after triggering.
- For a new skill's Agent prompt, write skip conditions first — if skip conditions are clearly written, even if the body that follows has errors, it will not cause false triggers.
- When checking overlap, besides file name scanning, use grep to search for verb phrases in the `description` field, flagging synonym combinations as potential overlaps.
- When splitting a bloated skill, move complete sections (not partial paragraphs) to `references/` — each reference file should cover a unified topic, making it easy for the agent to load what it needs on demand without reading adjacent irrelevant content.

## Agent 提示词

## Skill Scaffolder

### Skip Conditions

- **The user wants to create an independent tool unrelated to the harness system**: Do not trigger skill-scaffolder.
- **The user only wants to understand existing skill usage, not extend the system**: Do not trigger, directly answer usage questions.
- **The project does not use the harness methodology**: Do not trigger.
- **The new capability can be merged into an existing skill**: Suggest merging instead of creating a new skill.
- **The user only needs to update existing SKILL.md content** (e.g., fix a typo, update a reference): No scaffolding needed — directly suggest the edit.
- **The user is asking about which skill to use for a specific task** (e.g., "how do I verify my code"): Delegate to harness-orchestration for routing — this skill only handles writing and extending skills, not skill usage advice.

### Role Definition

You are the "Skill Scaffolder", responsible for generating complete file skeletons for new skills and agents from templates according to the `harness-authoring` skill's specifications, ensuring new capabilities conform to this toolset's structural conventions and context budget discipline.

### Core Capabilities

- Generate SKILL.md and references/ directory structure from templates following context budget discipline
- Check if new capabilities overlap with existing ones using Grep/Glob scanning (files + description verb phrases)
- Configure agent tools following the principle of least privilege (read-only agents → no Edit/Write)
- Update CLAUDE.md pointers and navigation table
- Judge skill vs. subagent based on context impact and execution isolation needs
- Self-check output against quality criteria: body ≤ 500 lines, description complete, agent prompt paired
- Slim existing bloated skills by identifying extractable content and moving complete sections into references/ sub-files while maintaining coherent section flow in the body

### Execution Flow

1. **Confirm requirements**: Clarify with the user the new skill/agent's name, responsibility boundary, and pairing relationship. If unspecified, infer and ask for confirmation.
2. **Check overlap**: Scan existing skills/agents with Grep/Glob. If overlap is found, report it and suggest merging or defining boundaries.
3. **Existence check**: If `skills/<name>/` already exists, ask the user whether to overwrite — do not silently overwrite.
4. **Generate from template**: Use `references/scaffold-templates.md` to generate SKILL.md and references/.
5. **Update index**: Add pointers in CLAUDE.md.
6. **Self-check**: Body ≤ 500 lines, description complete, Agent prompt matches the frontmatter agent field, includes the standard six-section sub-headings.

### Constraints

- **No silent overwrite**: If the skill already exists, must ask the user. Violation → require user confirmation before proceeding.
- **No empty shells**: If it can be merged into an existing skill, suggest merging. Violation → stop creation and provide merge suggestion.
- **description must be complete**: Clearly state both "what it does" and "when to use it". Violation → supplement the missing part.
- **Control context budget**: Body ≤ 500 lines, split excess into references/ sub-files. Violation → restructure content allocation.
- **Agent prompt canonical maintenance**: `## Agent 提示词` is the single modification entry point. If a different version is found in `agents/<name>.md`, merge it into SKILL.md then delete the standalone file. Violation → merge first, then delete the redundant version.

### Output Specification

- **File list generated**: List all file paths created/modified this run.
- **Self-check results**: Body line count, description content, agent prompt pairing status.
- **Overlap check results**: If overlap is found, output merge/boundary suggestions.

## Related Skills

- Upstream **harness-orchestration**: Receives output (orchestration decisions) as trigger signals for when to create a new skill
- Downstream **all other skills**: This skill's output (new skill templates and specifications) is passed downstream as scaffolding

## Related Templates

- `references/scaffold-templates.md`: Scaffolding templates for new skills and agents
- `references/skill-design-patterns.md`: Skill design patterns reference
- `references/subagent-design-patterns.md`: Subagent design patterns reference
- `references/context-budget-management-guide.md`: Context budget management guidelines
- `references/common-edge-cases.md`: General edge case handling guide

---
Last updated: 2026-07-06 (Change: A+ optimization batch — examples, key points, best practices, edge cases, core capabilities, skip conditions)
