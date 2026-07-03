# Skill & Agent Scaffold Templates

This document merges the SKILL.md template for new skills and the Claude Code template for new agents — they are always used together.

---

## SKILL.md Template

```
---
name: <skill-name>
description: <what it does in one sentence>.<when to use, 2-3 trigger phrases, do not expand with detailed scenarios>.
---

# <Skill Name>

## Core Principles

<A one-sentence summary of the core problem this skill solves, and the most important counter-intuitive conclusion or design decision.>

## When to Use

- <Trigger scenario 1: specific enough to distinguish from other skills>
- <Trigger scenario 2>
- <Trigger scenario 3>

## Methodology

<Core knowledge content of the skill. If there are multiple sub-topics, organize with ### sub-headings:>

### <Sub-topic 1>

<Content>

### <Sub-topic 2>

<Content>

## Initialization Steps (when setting up for a project for the first time)

1. <Step>
2. <Step>

## Operation Steps (when you are asked to execute this skill)

1. <Step>
2. <Step>
3. <Step>

## Paired Agents

- `<agent-name>`: <agent's responsibility, one sentence>

## Related Templates

- `references/<template>.md`: <purpose>

---
Budget reminder:
- description should be ~100 words (resident context); detailed trigger scenarios go in the `## When to Use` section.
- Body text should be ~500 lines max; content beyond that goes into `references/` subdirectory.
- description should clearly state both "what it does" and "when to use" (phrase level, no expansion).
```

---

## Agent .md Template (Claude Code)

```
<!-- Place this file in skills/<paired-skill>/agents/<agent-name>.md -->

---
name: <agent-name>
description: <what it does>.<when to use, specific scenarios>.
type: <read-only | executor>
tools: Bash, Glob, Grep, Read
model: sonnet
skills: <related skill names>
---

You are "<Role Name>". Your sole responsibility is <one-sentence responsibility description>.

## Tool Risk Statement

<Explain the usage boundaries and prohibited operations for each tool in tools. Read-only agents emphasize "no write operations"; executor agents limit the scope of Edit/Write.>

## Workflow

1. Step 1
2. Step 2
3. Step 3

## Principles

- Principle 1
- Principle 2
- Principle 3

## Paired Skills

- `<skill-name>`: <skill's purpose>
```
