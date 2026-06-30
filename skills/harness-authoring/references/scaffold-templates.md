# Skill & Agent 脚手架模板

本文件合并了新 skill 的 SKILL.md 模板和新 agent 的 Claude Code 模板——两者总是一起使用。

---

## SKILL.md 模板

```
---
name: <skill-name>
description: <做什么,一句话>。<什么时候用,2-3 个触发短语,不要展开详细场景>。
---

# <Skill 名称>(<中文名>)

## 核心原则

<一句话概括这个 skill 要解决的核心问题,以及最重要的反直觉结论或设计决策。>

## 何时使用

- <触发场景 1: 具体到能和其他 skill 区分开>
- <触发场景 2>
- <触发场景 3>

## 方法论

<skill 的核心知识内容。如果有多个子主题,用 ### 子标题组织:>

### <子主题 1>

<内容>

### <子主题 2>

<内容>

## 初始化步骤(首次为项目搭建时)

1. <步骤>
2. <步骤>

## 操作步骤(当你被要求执行此技能时)

1. <步骤>
2. <步骤>
3. <步骤>

## 配合的 agent

- `<agent-name>`: <agent 的职责,一句话>

## 相关模板

- `references/<template>.md`: <用途>

---
预算提醒:
- description 控制在 ~100 词以内(常驻上下文);详细触发场景放到 `## 何时使用` 段。
- 正文控制在 ~500 行以内;超出部分放入 `references/` 子目录。
- description 同时写清"做什么"和"什么时候用"(短语级,不要展开)。
```

---

## Agent .md 模板 (Claude Code)

```
<!-- 将此文件放置在 skills/<paired-skill>/agents/<agent-name>.md -->

---
name: <agent-name>
description: <做什么>。<什么时候用，具体场景>。
type: <read-only | executor>
tools: Bash, Glob, Grep, Read
model: sonnet
skills: <相关 skill 名称>
---

你是「<角色名>」。你的唯一职责是 <一句话职责描述>。

## 工具风险声明

<说明 tools 中每个工具的使用边界和禁止操作。只读 agent 强调"禁止任何写操作";执行型 agent 限定 Edit/Write 的作用范围。>

## 工作流程

1. 步骤一
2. 步骤二
3. 步骤三

## 原则

- 原则一
- 原则二
- 原则三

## 配合的 skill

- `<skill-name>`: <skill 的用途>
```
