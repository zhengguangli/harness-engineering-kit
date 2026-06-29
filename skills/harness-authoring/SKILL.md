---
name: harness-authoring
description: 指导如何为这套 harness 体系编写新的 skill、subagent 或扩充知识库,遵循渐进式披露与上下文预算原则对抗 context rot。当用户要给 harness 工具集添加新能力、问"怎么写一个好的 SKILL.md"或"这应该做成 skill 还是 subagent"、或发现某个 agent/skill 越写越臃肿需要瘦身时使用。
---

# Harness Authoring(撰写新的 skill / agent)

## 核心原则

这是一个元技能——不直接服务于某个具体任务,而是指导如何**给这套 harness 体系本身添加新的能力**,同时不破坏它原本要解决的问题(上下文是稀缺资源)。

## 何时使用

- 用户要给这套 harness 工具集本身添加新能力。
- 问"怎么写一个好的 SKILL.md"或"这应该做成 skill 还是 subagent"。
- 发现某个 agent/skill 越写越臃肿,需要瘦身。

## 先想清楚:这应该是一个 skill,还是一个 subagent?

| | Skill | Subagent |
|---|---|---|
| 本质 | 注入到**当前**上下文窗口的知识/流程 | 拥有**独立**上下文窗口的隔离执行单元 |
| 何时用 | 主对话需要"知道怎么做某件事"才能继续往下走 | 任务可以被委派出去独立完成,只把摘要结果带回主对话 |
| 对上下文的影响 | 触发时占用主上下文的 token 预算 | 几乎不占主上下文预算(只有摘要进来) |
| 并行性 | 不可并行(就是当前这一个上下文) | 可以并行跑多个 |
| 典型例子 | "这个项目的架构规则是什么"——需要在主对话里持续参考 | "审计这次改动有没有破坏架构边界"——可以丢出去独立跑,只要结果 |

经验法则:**如果这件事需要主对话"记住"才能继续推理,用 skill;如果这件事可以"派出去、等结果",用 subagent**。这套工具集里两者经常配对出现(一个 skill 定义方法论,一个同名思路的 agent 负责真正执行),这不是重复,是分工。

## 写 SKILL.md 时的上下文预算纪律

三层加载机制,决定了哪部分内容该放在哪:

1. **元数据(name + description)**:始终常驻上下文,大约 100 词的预算。这是触发机制本身,要写得准确且"有推力"——既要让 Claude 在恰当时机想起来用它,又不能在不相关的场景下误触发。
2. **SKILL.md 正文**:技能触发时才进入上下文,理想控制在 500 行以内。这里放"怎么做"的核心方法论和操作步骤。
3. **绑定资源(references/、scripts/、assets/)**:按需加载,体量不受限制。这里放模板、长篇参考资料、可执行脚本——脚本甚至可以执行而完全不进入上下文。

如果正文逼近 500 行,**不要硬塞**,拆出一层 `references/` 子文件,并在正文里写清楚"什么情况下该去读哪个参考文件"。

## description 字段要"推",但不能假

- 同时写清楚**做什么**和**什么时候用**——"什么时候用"不要省略,这是触发的主要依据。
- 用具体场景而不是抽象描述:"当用户说 A、B、C 类似的话时"比"用于代码质量相关任务"更容易被正确触发。
- 适度"推"一点(让 Claude 更倾向于主动想到它),但每一个声称的能力都要在正文里真正兑现,不要为了触发率虚报。

## 写 subagent 时的工具与权限纪律

- **按角色最小化授权工具**。只读分析型 agent(比如审计、巡检)不要给 `Edit`/`Write`,只给 `Read, Grep, Glob`(必要时 `Bash` 用于跑检查命令,但在 system prompt 里明确写"不要修改文件")。执行型 agent 才给 `Edit, Write, Bash`。
- **省略 `tools` 字段 = 继承全部工具**,这不是默认安全选项,只有真的需要全部权限时才这样做。
- **用 `skills` 字段预加载相关技能**,而不是在 system prompt 里重复一遍技能正文的内容——避免同一份方法论在两个地方各维护一份,迟早会不同步。
- **model 字段按"判断复杂度"而不是"任务大小"选择**:需要高阶判断/权衡的任务(架构取舍、计划拆解)用更强的模型;机械化、模式明确的重复性任务(扫描、巡检)用更轻量的模型,降低成本同时不损失质量。

## 对抗 context rot 的其他纪律

- **不要让 agent 直接把超大工具输出怼进主上下文**。如果一个工具调用的结果很长(完整日志、完整 diff),优先让结果落盘到文件,在对话里只保留头尾摘要 + 文件路径,需要细节时再读文件。
- **复杂任务用 exec-plan 落盘状态**(见 `harness-exec-plans`),不要依赖单次上下文窗口"记住"所有进度——上下文窗口迟早会被压缩或重置。
- **避免"什么都重要"式的规则堆砌**。一份列了 50 条规则的清单,效果通常不如一份列了 5 条、每条都配了具体后果和检查方式的清单。

## 操作步骤(当被要求"加一个新能力"时)

1. 先判断这是 skill 还是 subagent(或者两者都要,一个定义方法论、一个负责执行)。
2. 写 description:先写"什么时候用",再写"做什么",检查是否具体到能和其他已有 skill/agent 区分开。
3. 写正文,控制在预算内;预判内容会不会膨胀,提前规划是否需要 `references/` 子目录。
4. 如果是 subagent,按"最小化工具授权"原则列工具清单,并明确 model 选择的理由。
5. 检查这个新能力是否和已有的 skill/agent 重叠——如果重叠,合并或明确划分边界,不要让 Claude 在两个相似选项之间犯选择困难。
6. 把新增的 skill/agent 在仓库的 AGENTS.md / README 里登记一行指针,保持"地图"本身也是最新的(呼应 `harness-repo-map` 技能)。
7. 自检:新增/修改的 skill 正文是否 ≤ 500 行?subagent 的 tools 是否按最小权限原则?description 是否同时包含"做什么"和"什么时候用"?如果不符合,先修正再交付。

## 跨平台注意事项

这套 harness 体系同时服务于 Claude Code 和 Codex 两个平台。每个 agent 必须有两个版本的定义文件:

- **Claude Code**: `agents/<agent-name>.md` — YAML frontmatter + 系统提示词正文
- **Codex**: `agents/openai.yaml` — metadata + tools + system_prompt

两个版本必须**功能对等**:相同的系统提示词、等价的工具权限、相同的 skill 绑定。区别仅在于工具名和模型名的平台映射。

| Claude Code | Codex | 说明 |
|---|---|---|
| `Bash` | `exec_command` | 运行 shell 命令 |
| `Edit` | `apply_patch` | 修改已有文件 |
| `Write` | `apply_patch` | 创建新文件 |
| `Read` | `read_file` | 读取文件内容 |
| `Glob` | `list_dir` | 列出目录/文件 |
| `Grep` | `grep` | 搜索文本 |
| `sonnet` | `gpt-5.4` | 日常任务模型 |
| `opus` | `gpt-5.5` | 高阶判断模型 |

创建新 agent 时,使用 `agent-template.md` 生成 Claude Code 版本,使用 `agent-template-codex.yaml` 生成 Codex 版本。

## 配合的 agent

- `skill-scaffolder` agent:从模板生成新 skill/agent 的完整文件骨架,确保符合 harness-authoring 规范。只负责脚手架搭建,不负责内容填充。

## 相关模板

- `references/skill-template.md`: 新 skill 的 SKILL.md 模板
- `references/agent-template.md`: 新 agent 的 Claude Code 模板
- `references/agent-template-codex.yaml`: 新 agent 的 Codex 模板
- `references/skill-scaffolder-prompt.md`: skill-scaffolder agent 系统提示词

---
最后更新: 2026-06-29
