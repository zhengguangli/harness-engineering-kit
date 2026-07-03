# 领域特定设计模式（Domain-Specific Patterns）

不同领域的 prompt 设计有不同的侧重点。本文件提供常见领域的设计模式参考。

---

## 代码类（Code Review, Code Generation, Debugging）

**侧重点**：Constraints > Execution Chain > Examples

**设计要点**：
- **Constraints 必须严格**：代码类任务需要精确定义什么是"问题"，避免 LLM "为了找问题而找问题"
- **Severity Anchoring**：明确定义 CRITICAL / HIGH / MEDIUM / LOW 的含义
- **Actionable Fixes**：每个发现必须包含具体的修复建议
- **Line References**：要求输出包含文件名和行号

**必备约束**：
- `No Speculation`: Only flag issues you can point to with specific line references
- `Severity Anchoring`: CRITICAL = data loss/security breach, HIGH = runtime errors, MEDIUM = tech debt, LOW = style
- `Actionable Fixes`: Every finding must include a concrete fix suggestion

**示例结构**：
```
Role: Senior [Language] Engineer with [X] years of experience in [domain]
Execution Chain:
1. Parse & Understand intent
2. Check correctness (logic errors, edge cases)
3. Check security (injection, secrets, SSRF)
4. Check maintainability (naming, complexity)
5. Format findings
Constraints: No Speculation, Severity Anchoring, Actionable Fixes
Examples: Standard review, Clean code (no issues found), Critical security issue
```

---

## 文案类（Copywriting, Marketing, Content）

**侧重点**：Examples > Execution Chain > Constraints

**设计要点**：
- **Examples 比规则更重要**：文案类任务 LLM 更依赖示例来理解风格
- **Platform Calibration**：不同平台（Instagram, TikTok, Email, Landing Page）的文案结构完全不同
- **Tone Override**：提供可选的语气覆盖参数
- **Ban List**：给 LLM 一个具体的排除列表（如"不要用企业黑话"）比"写得自然"更有执行力

**必备约束**：
- `No Corporate Speak`: Ban specific words/phrases (leverage, synergy, empower, etc.)
- `Show Don't Tell`: Prefer concrete specifics over vague superlatives
- `Respect Platform Limits`: Hard stop on character limits

**示例结构**：
```
Role: Creative Copywriter specializing in [industry] targeting [demographic]
Execution Chain:
1. Understand product → extract core benefit (≤8 words)
2. Platform calibration → adjust format per platform
3. Write 3 variants (benefit-led, pain-point-led, social-proof-led)
4. Self-rate each variant (hook strength, clarity, platform fit)
Constraints: No Corporate Speak, Show Don't Tell, Respect Platform Limits
Examples: Instagram post, Email subject line, Landing page headline
```

---

## 分析类（Data Analysis, Research, Report Generation）

**侧重点**：Execution Chain > Constraints > Output Schema

**设计要点**：
- **Execution Chain 必须清晰**：分析类任务需要明确的步骤顺序
- **Data Anchoring**：要求 LLM 只基于提供的数据，不编造
- **Confidence Levels**：输出应包含置信度或不确定性声明
- **Structured Output**：分析结果通常需要结构化输出（JSON/表格）

**必备约束**：
- `Data Anchoring`: Only analyze provided data. Do not use external knowledge
- `Confidence Declaration`: State confidence level for each conclusion (HIGH/MEDIUM/LOW)
- `Source Citation`: Every claim must reference specific data points

**示例结构**：
```
Role: Senior Data Analyst specializing in [domain]
Execution Chain:
1. Understand the data structure and variables
2. Identify key patterns and anomalies
3. Calculate relevant metrics
4. Draw conclusions with confidence levels
Constraints: Data Anchoring, Confidence Declaration, Source Citation
Examples: Standard analysis, Missing data handling, Ambiguous data interpretation
```

---

## 客服类（Customer Service, Support, Chatbot）

**侧重点**：Constraints > Examples > Output Schema

**设计要点**：
- **Empathy Constraints**：要求 LLM 先承认用户感受再给解决方案
- **Escalation Triggers**：明确定义何时转人工（法律威胁、情绪激动、复杂问题）
- **Policy Anchoring**：严格按政策回答，不承诺无法兑现的内容
- **Response Tone**：定义语气（友好但专业、同理心但不卑微）

**必备约束**：
- `Empathy First`: Acknowledge customer frustration before delivering bad news
- `Policy Anchoring`: Never promise refunds/benefits that violate policy
- `Escalation Trigger`: If customer mentions "lawyer" or "sue", immediately offer human agent
- `No Speculation`: Do not invent reasons for denial

**示例结构**：
```
Role: Customer Service Specialist for [company/industry]
Execution Chain:
1. Identify intent (refund, status check, policy question)
2. Validate eligibility (check order info, policy)
3. Apply policy (eligible → process, not eligible → explain + alternatives)
4. Respond with empathy
Constraints: Empathy First, Policy Anchoring, Escalation Trigger
Examples: Eligible refund, Ineligible refund, Fraudulent claim, Angry customer
```

---

## 翻译类（Translation, Localization）

**侧重点**：Constraints > Examples > Variables Dictionary

**设计要点**：
- **Style Preservation**：要求保留原文风格（正式/非正式、技术/通俗）
- **Cultural Adaptation**：不仅是语言翻译，还要文化适配
- **Terminology Consistency**：专业术语必须一致
- **Format Preservation**：保留原文格式（Markdown、HTML、代码块）

**必备约束**：
- `Style Preservation`: Maintain the original tone and formality level
- `Cultural Adaptation`: Adapt idioms and cultural references for target audience
- `Terminology Consistency`: Use consistent translations for technical terms
- `Format Preservation`: Keep original formatting (Markdown, HTML, code blocks)

**示例结构**：
```
Role: Professional Translator specializing in [domain] (e.g., legal, medical, technical)
Variables:
- `{{source_text}}`: Text to translate (String, Required)
- `{{source_language}}`: Source language (String, Required)
- `{{target_language}}`: Target language (String, Required)
- `{{style_guide}}`: Terminology preferences (String, Optional)
Execution Chain:
1. Identify domain and terminology
2. Translate preserving style and format
3. Adapt cultural references
4. Verify terminology consistency
Constraints: Style Preservation, Cultural Adaptation, Terminology Consistency
Examples: Technical document, Marketing copy, Legal text
```

---

## 教育类（Tutoring, Explanation, Teaching）

**侧重点**：Execution Chain > Examples > Constraints

**设计要点**：
- **Scaffolding**：从简单到复杂逐步讲解
- **Check Understanding**：要求 LLM 检查用户是否理解
- **Multiple Explanations**：同一概念用不同方式解释
- **Practice Problems**：提供练习题巩固理解

**必备约束**：
- `Check Understanding`: After each concept, ask "Does this make sense?" or provide a quick quiz
- `Multiple Angles`: Explain each concept at least 2 different ways
- `No Jargon Without Definition`: Define technical terms before using them

**示例结构**：
```
Role: [Subject] Tutor with [X] years of teaching experience
Execution Chain:
1. Assess current understanding level
2. Break concept into smaller parts
3. Explain each part with analogies and examples
4. Check understanding with questions
5. Provide practice problems
Constraints: Check Understanding, Multiple Angles, No Jargon Without Definition
Examples: Beginner explanation, Advanced explanation, Misconception correction
```

---

## 快速选择指南

| 你的任务类型 | 侧重点 | 关键设计元素 |
|---|---|---|
| 代码审查/生成 | Constraints | Severity Anchoring, Actionable Fixes, Line References |
| 文案撰写 | Examples | Platform Calibration, Ban List, Multiple Variants |
| 数据分析 | Execution Chain | Data Anchoring, Confidence Levels, Source Citation |
| 客服对话 | Constraints | Empathy First, Policy Anchoring, Escalation Triggers |
| 翻译 | Constraints | Style Preservation, Cultural Adaptation, Terminology |
| 教育/讲解 | Execution Chain | Scaffolding, Check Understanding, Multiple Angles |

---
最后更新: 2026-07-02
