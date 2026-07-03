# 上下文预算管理指南

## 核心理念

上下文窗口是稀缺资源。每个设计决策都要回答一个问题：**这个内容对上下文预算的影响是什么？**

## 三层加载机制详解

### 第一层：元数据（始终常驻）

**预算**：~100 词（name + description + when_to_use）

**设计要点**：
- name：简短明确，便于检索（≤ 5 词）
- description：做什么 + 什么时候用（≥ 20 字符）
- when_to_use：显式/隐式触发条件 + 不触发条件

**示例对比**：

```yaml
# ❌ 差：模糊，无法区分
description: 帮助处理代码相关任务

# ✅ 好：具体，能区分
description: 指导如何为 harness 体系编写新的 skill 或 subagent——遵循渐进式披露与上下文预算原则。用于"怎么写一个好的 SKILL.md"、"给 harness 添新能力"场景。
```

**常见错误**：
- ❌ description 太短（< 20 字符）——触发条件不明确
- ❌ description 太长（> 200 词）——常驻上下文浪费
- ❌ when_to_use 缺失——触发和不触发边界模糊

### 第二层：SKILL.md 正文（触发时加载）

**预算**：≤ 500 行

**设计要点**：
- 核心原则 ≤ 5 条（每条一句话）
- 执行流程步骤 ≤ 7 步
- 硬约束 ≤ 5 条
- 最佳实践每类 ≤ 5 条

**章节结构建议**：

| 章节 | 建议行数 | 内容 |
|---|---|---|
| 核心原则 | 10-20 行 | 3-5 条核心信念 |
| 何时使用 | 10-20 行 | 触发条件（显式/隐式/不触发） |
| 方法论 | 50-150 行 | 核心流程和决策框架 |
| 操作步骤 | 30-80 行 | 具体执行步骤 |
| 硬约束 | 10-20 行 | 不可违反的规则 |
| 边界情况 | 20-40 行 | 特有边界情况 |
| 最佳实践 | 30-60 行 | 分类的最佳实践 |
| 常见陷阱 | 10-20 行 | 典型错误 |
| Agent 提示词 | 50-150 行 | agent 的 system prompt |

**膨胀检测信号**：
- 单个章节超过 100 行 → 考虑拆分到 references/
- 总行数接近 450 行 → 提前规划拆分
- 出现"详细内容见..."但没有对应文件 → 需要创建 references 文件

### 第三层：绑定资源（按需加载）

**预算**：无限制（但每个文件应控制在合理范围）

**文件组织原则**：

```
references/
├── quick-reference.md      # 快速查阅表（< 100行）
├── deep-dive-*.md          # 深入指南（各 < 200行）
├── templates/              # 模板文件
├── examples/               # 示例文件
└── scripts/                # 可执行脚本
```

**加载指引写法**：

```markdown
## 深入参考
- 快速查阅设计模式 → `references/quick-reference.md`
- 深入了解某个模式 → `references/deep-dive-{模式名}.md`
- 获取可复制模板 → `references/templates/`
```

**原则**：正文里写"什么情况下该去读哪个参考文件"，不写"详细内容如下"。

## 预算监控方法

### 行数检查

```bash
# 检查 SKILL.md 正文行数（不含 frontmatter）
total_lines=$(wc -l < SKILL.md)
frontmatter_end=$(awk '/^---$/{count++; if(count==2) print NR}' SKILL.md)
body_lines=$((total_lines - frontmatter_end - 1))
echo "正文行数: $body_lines"
if [ $body_lines -gt 450 ]; then
    echo "⚠️ 警告：正文接近 500 行上限"
fi
```

### 内容密度检查

| 指标 | 合格标准 | 超标处理 |
|---|---|---|
| 核心原则数量 | ≤ 5 条 | 合并或移至 references/ |
| 执行流程步骤数 | ≤ 7 步 | 拆分为子流程 |
| 硬约束数量 | ≤ 5 条 | 合并或移至 references/ |
| 单章节行数 | ≤ 100 行 | 拆分到 references/ |
| 示例数量 | ≤ 5 个 | 保留最典型的 3 个 |

## 拆分策略

### 何时拆分

- 正文逼近 450 行
- 单个章节超过 100 行
- 出现"详细内容见..."但没有对应文件
- 同一信息在多处出现（维护成本高）

### 拆分方式

**方式一：按主题拆分**
```
原 SKILL.md（500行）
├── SKILL.md（精简到 300行）
├── references/pattern-a.md（100行）
├── references/pattern-b.md（100行）
└── references/examples.md（80行）
```

**方式二：按深度拆分**
```
原 SKILL.md（500行）
├── SKILL.md（精简到 200行，只保留核心流程）
├── references/quick-reference.md（100行，快速查阅）
└── references/deep-dive.md（200行，深入指南）
```

**方式三：按角色拆分**
```
原 SKILL.md（500行）
├── SKILL.md（方法论部分）
├── references/agent-guide.md（agent 执行部分）
└── references/templates.md（模板部分）
```

### 拆分后的引用规范

```markdown
## 在正文中写加载指引
- 设计模式详情 → `references/skill-design-patterns.md`
- 上下文管理细节 → `references/context-budget-management-guide.md`
- 跨平台同步细节 → `references/cross-platform-sync-guide.md`

## 在 Agent 提示词中引用
使用 `skills` 字段预加载相关技能，而不是在 system prompt 里重复内容。
```

## 常见预算问题与解决

| 问题 | 原因 | 解决 |
|---|---|---|
| 正文超 500 行 | 所有内容都塞在正文里 | 拆分到 references/ |
| 常驻内容过多 | description 写太长 | 精简到核心信息 |
| 加载指引缺失 | 拆分后忘记写引用 | 补充"什么情况下读哪个文件" |
| 信息重复 | 同一内容在正文和 references 都出现 | 正文只写摘要，details 放 references/ |
| 触发不准确 | description 模糊 | 具体化触发场景 |

## 预算优化清单

创建/修改 skill 时，逐项检查：

- [ ] description 是否 ≤ 200 词？
- [ ] description 是否同时包含"做什么"和"什么时候用"？
- [ ] 正文是否 ≤ 500 行？
- [ ] 单个章节是否 ≤ 100 行？
- [ ] 核心原则是否 ≤ 5 条？
- [ ] 执行流程步骤是否 ≤ 7 步？
- [ ] 硬约束是否 ≤ 5 条？
- [ ] 是否有 references/ 子目录按需加载详细内容？
- [ ] 正文是否写了"什么情况下读哪个参考文件"？
- [ ] 是否避免了信息在正文和 references 中重复？
