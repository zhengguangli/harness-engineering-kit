# Agent 提示词内联迁移模式

- 创建日期: 2026-07-02
- 关联 exec-plan: `docs/exec-plans/completed/consolidate-agents-into-skills.md`

## 背景

原架构中每个 skill 的 agent 提示词维护在独立的 `agents/<name>.md` 文件中，与 `openai.yaml`（Codex 元数据）并存。这种模式存在以下问题：

1. **维护成本高**：修改 agent 提示词需同步 `.md` 和 `openai.yaml` 两个文件
2. **不符合官方规范**：Claude Code 官方文档展示的 skill 模式是单文件指令（SKILL.md 包含完整指令）
3. **结构冗余**：agent 提示词与 skill 方法论高度耦合，拆分为独立文件增加导航成本

## 决策

将 agent 提示词内联到 SKILL.md 的 `## Agent 提示词` section，消除独立的 `agents/<name>.md` 文件。

### 新的 Skill 目录结构

```
skills/<name>/
├── SKILL.md          # 方法论正文 + agent 提示词
├── agents/
│   └── openai.yaml   # Codex UI 元数据（保留）
└── references/       # 模板文件
```

### SKILL.md 内部结构

```yaml
---
name: <skill-name>
description: <做什么 + 什么时候用>
when_to_use: <触发场景>
context: fork          # 新增：指定在子 agent 中运行
agent: <agent-name>    # 新增：指定使用的 agent 类型
compatibility: opencode
---
# <Skill 标题>

## 核心原则
...

## 何时使用
...

## 方法论
...

## 相关模板
...

## Agent 提示词              # 新增 section

### <Agent 名称>

#### 角色定义
...

#### 核心能力
...

#### 执行流程
...

#### 约束
...

---
最后更新: <日期>
```

## 理由

1. **官方文档支持**：Claude Code skills 支持 `context: fork` + `agent` 字段，可在 SKILL.md 中指定子 agent 类型
2. **减少文件数**：消除 12 个 `agents/*.md` 文件，简化目录结构
3. **维护更简单**：agent 提示词与 skill 方法论在同一文件中，修改时无需跨文件同步
4. **渐进式披露**：SKILL.md 加载时自动包含 agent 提示词，无需额外文件读取

## 被否决的备选方案

| 方案 | 做法 | 否决理由 |
|---|---|---|
| 迁移到 `.claude/agents/` | 移动到项目级 agent 目录 | 改动面过大，12 个 agent 全部迁移 |
| 保持现状 | 维持 `skills/*/agents/` 结构 | 不符合官方推荐布局 |
| 合并进 frontmatter | 将 agent 提示词放入 YAML frontmatter | 会破坏 Codex 解析 |

## 跨平台同步注意事项

- `openai.yaml` 的 `system_prompt` 字段仍引用旧的 agent 提示词内容
- 后续 PR 需同步更新 `openai.yaml` 与 SKILL.md 中的 agent 提示词
- 校验脚本 `validate-agent-prompt-sync.sh` 已改为检查 section 存在性

## 相关文件

- `docs/exec-plans/completed/consolidate-agents-into-skills.md`：完整执行计划
- `docs/ARCHITECTURE.md`：目录结构说明
- `AGENTS.md`：硬约束描述

---
最后更新: 2026-07-02
