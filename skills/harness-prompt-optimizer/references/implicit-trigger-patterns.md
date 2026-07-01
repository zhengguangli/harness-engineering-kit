# 隐式触发模式（Implicit Trigger Patterns）

`harness-prompt-optimizer` 在用户没有明确点名时如何主动识别适合 prompt 优化的场景。本文件作为 SKILL.md frontmatter `when_to_use` 的详细参考——判断不确定时读取本文件。

## 显式触发关键词

用户直接表达意图的句式：

- "帮我写一个 prompt / system prompt / 提示词"
- "优化 / 改进 / 完善这个 prompt"
- "这个 prompt 效果不好 / 不准确 / 不稳定"
- "我需要一个 system prompt 给 XXX"
- "write me a prompt for XXX"
- "optimize / improve / refine this prompt"
- "this prompt doesn't work well"

## 隐式触发场景

以下情况用户没有说"prompt"，但本质上需要 prompt 优化：

### 场景 1：描述复杂需求但无结构

用户描述了需要 AI 反复执行的任务，但没有结构化：

- "我希望 AI 能帮我 review 代码，找出 bug 和不好的写法"
- "我想让 AI 从网页里提取商品价格"
- "帮我写个让 AI 写营销文案的东西"
- "I want an agent that can analyze financial reports"

→ 建议："这个需求适合转化为结构化 prompt，需要我帮你优化吗？"

### 场景 2：贴了一段 prompt 但没说意图

用户贴了一段文本，看起来像 prompt/指令：

- 贴了一段包含 "You are..."、"你的任务是..." 的文本
- 贴了一段编号步骤的指令
- 贴了一段包含约束/规则的文本

→ 询问："这段 prompt 是否需要优化？我可以帮你改进结构和约束。"

### 场景 3：agent 行为不符合预期

用户在调试 agent 或 AI 行为：

- "这个 agent 行为不对 / 输出格式不稳定"
- "AI 总是 hallucinate / 编造信息"
- "AI 不按我说的做"
- "the agent keeps ignoring my instructions"
- "output format is inconsistent"

→ 评估是否 prompt 缺少约束或示例，建议优化。

### 场景 4：在构建 agent/自动化流程

用户在搭建需要 system prompt 的系统：

- "我在做一个 code review bot"
- "我在搭建一个数据提取 pipeline"
- "I'm building an agent that does XXX"
- "需要一个 system prompt 给我的 chatbot"

→ 主动提供 prompt 优化能力。

### 场景 5：用户说"优化这个 XXX"但 XXX 不是 prompt

用户用了"优化"但对象不是 prompt（见 SKILL.md 判断表格）：

- "优化这个**指令**" → 可能是 prompt
- "优化这个**规范**" → 可能是 prompt
- "优化这个**函数**" → 不是 prompt
- "优化这个**文档**" → 不是 prompt

→ 不确定时询问确认。

## 关键词组合触发

当用户消息包含**动作词 + 对象词**组合时，优先考虑 prompt 优化场景：

| 动作词 | 对象词 |
|---|---|
| 优化、改进、完善、增强、提升、看看、分析、诊断、写、设计 | prompt、提示词、system prompt、指令、建议、规范、规则、指南、模板 |
| optimize, improve, refine, enhance, write, design, review | prompt, system prompt, instruction, guideline, template |

组合示例：
- "帮我看看这个**指令**" → 询问是否优化 prompt
- "优化这个**建议**" → 询问是否优化 prompt
- "设计一套**规则**给 AI 用" → 建议转化为结构化 prompt
- "review this **instruction**" → 询问是否优化 prompt

## 判断流程

```
用户消息
  ├─ 包含显式触发关键词？ → 直接进入优化流程
  ├─ 包含隐式触发场景？ → 询问确认后进入
  ├─ 包含动作词+对象词组合？ → 询问确认后进入
  └─ 都不匹配 → 不触发
```

## 使用方式

当主对话的判断不确定时，读取本文件作为辅助参考。

## 维护

本文件随 SKILL.md frontmatter `when_to_use` 同步更新。如果发现新的隐式触发模式，先加在这里，再在 `when_to_use` 补充一句指针。
