# 变量字典设计指南

## 什么是变量字典

变量字典是 prompt 中对动态输入的声明——告诉 LLM "这些值会在运行时注入，你不需要自己假设"。

## 为什么需要变量字典

| 没有变量字典 | 有变量字典 |
|---|---|
| LLM 自行假设场景 | LLM 知道输入来源 |
| 硬编码示例值 | 动态注入实际值 |
| 输出格式不稳定 | 输出与输入对应 |
| 难以复用 | 同一 prompt 适用于不同输入 |

## 变量字典结构

```markdown
# Variables Dictionary

| 变量名 | 类型 | 必填 | 说明 | 示例值 |
|---|---|---|---|---|
| user_input | string | 是 | 用户的原始输入 | "帮我优化这段代码" |
| target_language | string | 否 | 目标输出语言 | "zh" / "en" |
| max_length | number | 否 | 输出最大长度 | 500 |
| context | object | 否 | 额外上下文信息 | {"project": "my-app"} |
```

## 设计原则

### 原则一：显式声明所有动态输入

```markdown
# ❌ 差：未声明变量
请分析这段代码的问题。

# ✅ 好：显式声明
# Variables Dictionary
| 变量名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code_snippet | string | 是 | 需要分析的代码片段 |
| language | string | 是 | 代码语言（如 "typescript"） |
| focus | string | 否 | 关注点（"performance" / "readability" / "security"） |

请分析以下代码的问题：
\`\`\`{{language}}
{{code_snippet}}
\`\`\`
关注点：{{focus}}
```

### 原则二：变量名语义化

```markdown
# ❌ 差：变量名无意义
| 变量名 | 说明 |
|---|---|
| x | 输入 |
| y | 输出 |

# ✅ 好：变量名自解释
| 变量名 | 说明 |
|---|---|
| raw_user_message | 用户的原始消息 |
| parsed_intent | 解析后的用户意图 |
| response_format | 响应格式要求 |
```

### 原则三：提供默认值或标注可选

```markdown
# Variables Dictionary
| 变量名 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| language | string | 否 | "zh" | 输出语言 |
| verbose | boolean | 否 | false | 是否输出详细解释 |
| max_retries | number | 否 | 3 | 最大重试次数 |
```

### 原则四：变量在 prompt 中的引用方式

```markdown
# 方式一：Mustache 模板（推荐）
请用 {{language}} 语言回答以下问题：
{{question}}

# 方式二：占位符
请用 [LANGUAGE] 语言回答以下问题：
[QUESTION]

# 方式三：自然语言引用
请用用户指定的语言（由 language 变量提供）回答问题。
```

## 变量类型设计

### 基础类型

| 类型 | 说明 | 示例 |
|---|---|---|
| string | 文本 | "hello" |
| number | 数字 | 42 |
| boolean | 布尔 | true / false |
| enum | 枚举 | "zh" / "en" |

### 复合类型

| 类型 | 说明 | 示例 |
|---|---|---|
| object | 对象 | {"key": "value"} |
| array | 数组 | ["item1", "item2"] |
| union | 联合类型 | string \| number |

### 类型约束

```markdown
# Variables Dictionary
| 变量名 | 类型 | 约束 | 说明 |
|---|---|---|---|
| temperature | number | 0.0 - 2.0 | 生成温度 |
| top_p | number | 0.0 - 1.0 | 核采样参数 |
| max_tokens | number | ≥ 1 | 最大生成 token 数 |
| language | enum | "zh" \| "en" \| "ja" | 输出语言 |
```

## 与 Execution Chain 的配合

变量字典为 Execution Chain 提供输入：

```markdown
# Variables Dictionary
| 变量名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| raw_data | string | 是 | 原始数据（JSON 格式） |
| target_metric | string | 是 | 目标指标名称 |
| threshold | number | 是 | 阈值 |

# Execution Chain
1. 解析 {{raw_data}} 为结构化数据
2. 提取 {{target_metric}} 的值
3. 比较该值与 {{threshold}}
4. 输出比较结果和建议
```

## 与 Output Schema 的配合

变量字典中的变量可能出现在输出中：

```markdown
# Variables Dictionary
| 变量名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| analysis_target | string | 是 | 分析目标 |
| report_format | enum | 是 | 报告格式（"brief" / "detailed"） |

# Output Schema
{
  "target": "{{analysis_target}}",  // 引用变量
  "format": "{{report_format}}",    // 引用变量
  "findings": [...],
  "recommendations": [...]
}
```

## 常见错误

| 错误 | 后果 | 修正 |
|---|---|---|
| 未声明变量 | LLM 自行假设值 | 显式声明所有动态输入 |
| 变量名不语义化 | 维护困难 | 使用描述性变量名 |
| 缺少类型约束 | LLM 输出格式不稳定 | 添加类型和约束 |
| 变量太多 | 维护成本高 | 精简到必要的变量 |
| 缺少默认值 | 每次都要提供所有变量 | 为可选变量提供默认值 |
| 变量和示例值不匹配 | LLM 混淆 | 保持变量声明和示例一致 |
