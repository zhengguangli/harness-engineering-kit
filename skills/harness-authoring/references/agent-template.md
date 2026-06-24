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

<如果是只读 agent: 本 agent 的 tools 字段包含 Bash 用于运行只读命令，禁止执行任何写操作。>
<如果是执行型 agent: 说明可用工具范围>

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