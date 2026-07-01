---
name: harness-prompt-optimizer
description: 将自然语言描述转化为高质量、结构化的 LLM prompt——包含角色定义、变量字典、执行链、约束、输出 schema 和 few-shot 示例。用于"帮我写/优化一个 prompt"、"这个 prompt 效果不好"场景。
when_to_use: 当用户说"帮我写/优化一个 prompt"、"这个 prompt 效果不好"、"我需要一个 system prompt"时使用。
compatibility: opencode
metadata:
  category: prompt-engineering
---

# Prompt Optimizer（提示词优化）

## 核心原则

LLM 的输出质量上限由 prompt 的结构质量决定。一份好的 prompt 不是"把需求写长一点"，而是用工程化方式消除歧义、约束行为空间、锚定输出格式：

- **结构 > 自由文本**：Role / Context / Rules / Examples 的分区结构让 LLM 行为更一致。
- **确定性 > 灵活性**：用严格约束和输出 schema 消除幻觉空间，宁可让 LLM 说"无法确定"也不要让它编造。
- **示例 > 描述**：1-3 个高质量 few-shot 示例比 10 段规则描述更能锚定行为。

## 何时使用

- 用户说"帮我写一个 prompt"、"优化这个 prompt"、"这个 prompt 效果不好"
- 用户在构建 agent 或自动化流程，需要高质量的 system prompt
- 用户给出粗糙需求描述，希望转化为可直接使用的结构化 prompt

## 何时不该用

- 用户要的是代码实现，不是 prompt 工程（编程任务交给 `harness-verification-loop` 或 `harness-bootstrap`）。
- 任务可由单次 API 调用或工具使用完成，不需要结构化 prompt。
- 用户在闲聊或做头脑风暴，无结构化输出需求。
- 任务一句话就能说清，硬塞六区块反而过度工程化。

## 方法论

### 步骤 0：触发模式判断

- **主动模式**：用户明确要求优化 → 直接进入步骤 1
- **被动模式**：用户描述需求或贴 prompt → 先询问是否需要优化，确认后进入步骤 1
- **句式触发**：用户说"优化/改进/看看这个 XXX" → 按判断规则确认后进入步骤 1
- **关键词触发**：用户消息包含动作词 + 对象词组合 → 询问确认后进入步骤 1

### 步骤 1：分析意图与评估现有 prompt

理解用户的核心任务、目标领域、期望输出格式。如果需求模糊，先用自己的话复述确认。如果用户提供了现有 prompt，从五维评估框架诊断质量问题：

| 维度 | 检查点 | 常见问题 |
|---|---|---|
| 角色定义 | 有明确 persona 和专业领域？ | "你是一个 AI 助手"——太泛，无锚定效果 |
| 上下文 | 提供了任务背景和约束环境？ | 缺少上下文导致 LLM 自行假设场景 |
| 执行链 | 任务拆分为编号步骤？ | 一段需求描述，LLM 自行决定执行顺序 |
| 约束 | 有安全栏和格式约束？ | 缺少约束导致输出格式不稳定 |
| 示例 | 有 few-shot 示例锚定行为？ | 纯规则描述，LLM 理解规则的方式各异 |

### 步骤 2：设计架构与填充内容

按六区块模板（`references/prompt-architecture-template.md`）设计 prompt 结构。先写 Role 和 Constraints（对行为影响最大），再写 Execution Chain，最后写 Examples。每个区块的填写要点、好/坏例子、tie-breaker 规则、必备约束类型见 `references/six-block-design-notes.md`。

六区块顺序：Role → Background & Context → Variables Dictionary → Execution Chain → Constraints → Output Schema + Examples。

### 步骤 3：自检

| 检查项 | 合格标准 |
|---|---|
| Role | 具体到可区分（不是 "helpful assistant"） |
| Variables Dictionary | 所有动态输入已声明 |
| Execution Chain | 步骤数 ≤ 7 |
| Constraints | 每条包含"违反时怎么办" |
| Output Schema | 完整覆盖所有输出字段 |
| Examples | 至少覆盖 standard + edge case |
| 一致性 | 规则和示例不矛盾 |

### 步骤 4：输出

生成完整的、可直接复制使用的 prompt。不包裹在 markdown 代码块里（除非用户要求），直接输出 prompt 本身。如果用户要求对比，附上优化前后的差异说明。

## 关键要点

- Role 和 Constraints 对行为影响最大，优先写这两块。
- 如果用户的任务很简单，不需要硬塞六个区块——评估后给出适当复杂度的 prompt。
- 如果发现用户的需求不需要 prompt 优化而是需要工具调用，坦率告知。

## 常见陷阱

- **只放 happy path 示例**：LLM 遇到边界情况时行为不可预测，务必覆盖 edge case。
- **示例和规则矛盾**：LLM 通常跟随示例而非规则，矛盾时行为会偏向示例。
- **约束过多**：超过 8 条约束 LLM 反而违反得更多，精选关键约束。
- **过度工程化**：简单任务不需要完整六区块，为形式完整而增加无用内容只会浪费 token。

## 配合的 agent

- `prompt-optimizer` agent：执行型 agent，负责分析需求并生成结构化 prompt。

## 相关模板

- `references/prompt-architecture-template.md`: Prompt 六区块架构模板（可直接复制填充）
- `references/optimization-examples.md`: 多领域 prompt 优化前后对比示例集
- `references/six-block-design-notes.md`: 六区块填写要点（好/坏例子、tie-breaker 规则、必备约束类型）
- `references/implicit-trigger-patterns.md`: 隐式触发模式（句式识别 / 关键词触发）详细参考

---
最后更新: 2026-07-01
