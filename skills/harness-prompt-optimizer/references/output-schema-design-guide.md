# Output Schema 设计指南

## 什么是 Output Schema

Output Schema 是对 LLM 输出格式的结构化定义——确保输出可被下游消费者（人或程序）解析和使用。

## 为什么需要 Output Schema

| 没有 Output Schema | 有 Output Schema |
|---|---|
| 输出格式不稳定 | 输出格式一致 |
| 下游需要二次解析 | 直接可用 |
| 无法自动化处理 | 可程序化消费 |
| 难以验证正确性 | 可自动校验 |

## Schema 设计原则

### 原则一：完整覆盖

Schema 必须覆盖所有可能的输出字段——包括成功和失败情况。

```markdown
# ❌ 差：只覆盖成功情况
{
  "result": "success",
  "data": {...}
}

# ✅ 好：覆盖所有情况
{
  "status": "success" | "error" | "partial",
  "data": {...},           // 成功时
  "error": {...},          // 失败时
  "warnings": [...]        // 部分成功时
}
```

### 原则二：类型明确

每个字段必须有明确的类型约束。

```markdown
# ❌ 差：类型模糊
{
  "score": "分数",
  "tags": "标签列表"
}

# ✅ 好：类型明确
{
  "score": "number (0-100)",
  "tags": "string[] (最多 5 个元素)",
  "created_at": "string (ISO 8601 格式)"
}
```

### 原则三：可选字段标注

明确哪些字段是必填，哪些是可选。

```markdown
{
  "required_field": "string",           // 必填
  "optional_field": "string | null",    // 可选
  "conditionally_required": "string"    // 条件必填
}
```

### 原则四：嵌套结构扁平化

尽量减少嵌套层级——层级越深，LLM 输出越容易出错。

```markdown
# ❌ 差：嵌套太深
{
  "analysis": {
    "metrics": {
      "performance": {
        "p99": 800,
        "p95": 600
      }
    }
  }
}

# ✅ 好：适当扁平化
{
  "p99_latency": 800,
  "p95_latency": 600,
  "performance_score": 85
}
```

## Schema 模板

### 基础模板

```markdown
# Output Schema
```json
{
  "status": "success | error | partial",
  "summary": "string (一句话总结)",
  "details": {
    "field1": "type (说明)",
    "field2": "type (说明)"
  },
  "evidence": [
    {
      "type": "screenshot | log | metric",
      "description": "string",
      "value": "string"
    }
  ],
  "recommendations": ["string"]
}
```
```

### 分析任务模板

```markdown
# Output Schema
```json
{
  "status": "success | error",
  "target": "string (分析目标)",
  "findings": [
    {
      "category": "string (发现分类)",
      "severity": "critical | warning | info",
      "description": "string (具体描述)",
      "evidence": "string (证据位置/内容)",
      "recommendation": "string (修复建议)"
    }
  ],
  "metrics": {
    "metric_name": "number (指标值)"
  },
  "summary": "string (总结)"
}
```
```

### 验证任务模板

```markdown
# Output Schema
```json
{
  "verification_result": "pass | fail | partial",
  "checks": [
    {
      "name": "string (检查项名称)",
      "result": "pass | fail | skip",
      "expected": "string (预期值)",
      "actual": "string (实测值)",
      "evidence": "string (证据)"
    }
  ],
  "capability_gaps": [
    {
      "gap": "string (缺口描述)",
      "impact": "string (影响)",
      "suggestion": "string (修复建议)"
    }
  ],
  "conclusion": "string (结论)"
}
```
```

## 字段类型设计

### 基础类型

| 类型 | 说明 | 示例 |
|---|---|---|
| string | 文本 | "hello" |
| number | 数字 | 42 |
| boolean | 布尔 | true |
| null | 空值 | null |

### 复合类型

| 类型 | 说明 | 示例 |
|---|---|---|
| string[] | 字符串数组 | ["a", "b"] |
| object | 嵌套对象 | {"key": "value"} |
| union | 联合类型 | "a" \| "b" \| "c" |

### 约束类型

| 约束 | 说明 | 示例 |
|---|---|---|
| 枚举 | 固定值列表 | "success" \| "error" |
| 范围 | 数值范围 | "number (0-100)" |
| 长度 | 字符串/数组长度 | "string (≤ 200 字符)" |
| 格式 | 特定格式 | "string (ISO 8601)" |

## 与 Execution Chain 的配合

Output Schema 定义最终输出，Execution Chain 定义如何到达：

```markdown
# Execution Chain
1. 解析输入 → 输出：parsed_data
2. 分析 parsed_data → 输出：analysis_result
3. 格式化 analysis_result 为 Output Schema 格式 → 输出：最终结果

# Output Schema
{
  "status": "success | error",
  "analysis": "string",
  "findings": [...],
  "evidence": [...]
}
```

## 与 Examples 的配合

Examples 展示 Output Schema 的实际使用：

```markdown
# Output Schema
{
  "status": "success | error",
  "score": "number (0-100)",
  "feedback": "string"
}

# Example
Input: "这段代码有性能问题"
Output:
{
  "status": "success",
  "score": 75,
  "feedback": "代码整体质量良好，但存在 2 个性能瓶颈：1) 循环内重复计算 2) 缺少缓存机制"
}
```

## 校验规则

### 自动校验

```markdown
# 校验清单
- [ ] 所有必填字段存在
- [ ] 字段类型正确
- [ ] 枚举值在允许范围内
- [ ] 数值在指定范围内
- [ ] 字符串长度在限制内
- [ ] 数组长度在限制内
- [ ] 嵌套结构完整
```

### 手动校验

```markdown
# 人工审查清单
- [ ] 输出内容与输入相关
- [ ] 发现有证据支撑
- [ ] 建议可执行
- [ ] 语言自然流畅
- [ ] 无矛盾信息
```

## 常见错误

| 错误 | 后果 | 修正 |
|---|---|---|
| 只覆盖成功情况 | 错误时输出不可解析 | 添加 error 状态 |
| 类型定义模糊 | LLM 输出类型不一致 | 明确类型约束 |
| 嵌套太深 | LLM 输出容易出错 | 扁平化结构 |
| 缺少必填标注 | 输出缺少关键字段 | 标注必填字段 |
| Schema 太复杂 | LLM 难以遵循 | 精简字段数量 |
| 与 Examples 不一致 | LLM 输出偏向 Examples | 保持 Schema 和 Examples 一致 |
