# Execution Chain 设计指南

## 什么是 Execution Chain

Execution Chain 是 prompt 中对任务执行步骤的编号列表——强制 LLM 按特定顺序执行，而不是自行决定流程。

## 为什么需要 Execution Chain

| 没有 Execution Chain | 有 Execution Chain |
|---|---|
| LLM 自行决定执行顺序 | 强制按步骤执行 |
| 跳步或乱序 | 步骤间有数据流 |
| 输出不可预测 | 输出可复现 |
| 难以调试 | 每步可独立验证 |

## 设计原则

### 原则一：步骤数 ≤ 7

LLM 的上下文窗口有限，步骤太多会丢失前序步骤的上下文。

```markdown
# ❌ 差：步骤太多
1. 步骤1
2. 步骤2
3. 步骤3
...
10. 步骤10

# ✅ 好：精简步骤
1. 步骤1
2. 步骤2
3. 步骤3
4. 步骤4
```

**如果步骤超过 7 步**：
- 合并相关步骤
- 拆分为子 prompt
- 使用条件分支减少线性步骤

### 原则二：每步有明确的输入和输出

```markdown
# ❌ 差：无数据流
1. 分析数据
2. 生成报告
3. 检查质量

# ✅ 好：有数据流
1. 解析输入数据 → 输出：结构化数据对象
2. 统计结构化数据的各维度指标 → 输出：指标摘要
3. 基于指标摘要生成报告 → 输出：报告文本
4. 检查报告文本是否符合规范 → 输出：检查结果
```

### 原则三：步骤是可执行的

```markdown
# ❌ 差：模糊
1. 考虑各种情况
2. 做出最佳决策
3. 确保质量

# ✅ 好：具体
1. 列出所有可能的分类（最多 5 个）
2. 对每个分类统计出现次数
3. 按出现次数降序排列
4. 选择前 3 个分类作为主要发现
```

### 原则四：包含判断和分支

```markdown
1. 检查输入数据格式是否为 JSON
   - 是 → 进入步骤 2
   - 否 → 输出错误信息，终止流程
2. 解析 JSON 数据
3. 验证必要字段是否存在
   - 是 → 进入步骤 4
   - 否 → 输出缺失字段列表，终止流程
4. 执行数据分析
```

## Execution Chain 模板

### 线性流程

```markdown
# Execution Chain
1. [输入处理]：接收 {{input}}，验证格式 → 输出：validated_input
2. [核心处理]：分析 validated_input → 输出：analysis_result
3. [输出生成]：基于 analysis_result 生成输出 → 输出：final_output
4. [验证]：检查 final_output 是否符合规范 → 输出：验证结果
```

### 条件分支流程

```markdown
# Execution Chain
1. 判断任务类型：{{task_type}}
   - "analysis" → 进入步骤 2
   - "generation" → 进入步骤 4
   - "review" → 进入步骤 6

2. [分析流程]：执行数据分析 → 输出：analysis_result
3. 基于 analysis_result 生成报告 → 输出：报告，终止

4. [生成流程]：基于 {{requirements}} 生成内容 → 输出：draft
5. 审查 draft 质量 → 输出：最终内容，终止

6. [审查流程]：检查 {{target}} 是否符合规范 → 输出：审查报告，终止
```

### 循环流程

```markdown
# Execution Chain
1. 生成初始方案 → 输出：current_solution
2. 评估 current_solution 的质量 → 输出：evaluation_result
3. 判断 evaluation_result 是否达标
   - 是 → 输出 current_solution，终止
   - 否 → 进入步骤 4
4. 基于 evaluation_result 优化 current_solution → 输出：new_solution
5. 将 new_solution 赋值给 current_solution → 回到步骤 2

# 约束：最多循环 3 次，仍未达标则输出当前最佳方案
```

## 步骤粒度控制

| 粒度 | 适用场景 | 示例 |
|---|---|---|
| 粗粒度 | 简单任务 | "1. 分析 2. 生成 3. 检查" |
| 中粒度 | 中等复杂度 | "1. 解析 2. 统计 3. 比较 4. 输出" |
| 细粒度 | 复杂任务 | 每个子操作一个步骤 |

**选择原则**：每个步骤应该是一个完整的、可独立验证的操作。如果一个步骤需要进一步拆解才能理解，说明粒度太粗。

## 与变量字典的配合

Execution Chain 中引用变量字典的变量：

```markdown
# Variables Dictionary
| 变量名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input_data | string | 是 | 输入数据 |
| output_format | enum | 是 | 输出格式 |

# Execution Chain
1. 解析 {{input_data}} → 输出：parsed_data
2. 分析 parsed_data → 输出：analysis
3. 按 {{output_format}} 格式化 analysis → 输出：最终结果
```

## 与 Constraints 的配合

Execution Chain 的每一步都受 Constraints 约束：

```markdown
# Execution Chain
1. 解析输入数据 → 输出：parsed_data
2. 分析 parsed_data → 输出：analysis

# Constraints
- 步骤1中：只解析提供的数据，不编造字段
- 步骤2中：只使用 parsed_data 中存在的字段进行分析
- 步骤2中：如数据不足，输出"数据不足，无法分析"而非猜测
```

## 常见错误

| 错误 | 后果 | 修正 |
|---|---|---|
| 步骤太多（> 7） | LLM 丢失上下文 | 合并或拆分 |
| 步骤模糊 | LLM 自行解释 | 具体化每个步骤 |
| 无数据流 | 步骤间断裂 | 明确输入输出关系 |
| 无判断分支 | 所有情况走同一路由 | 添加条件判断 |
| 缺少终止条件 | 无限循环 | 每条路径有终点 |
| 步骤不可执行 | LLM 跳过 | 确保每步可独立执行 |
