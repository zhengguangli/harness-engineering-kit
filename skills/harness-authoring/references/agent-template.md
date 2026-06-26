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