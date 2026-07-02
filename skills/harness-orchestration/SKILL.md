---
name: harness-orchestration
description: 编排 harness-engineering-kit 中 skill 的组合与工作流路由——根据用户目标选择正确的 skill 组合和执行顺序。用于"我该用哪些 skill"、"规划多 skill 协作"、"工作流怎么走"、"进入新项目不确定先后顺序"场景。
when_to_use: |
  显式触发：用户问"我该用哪些 skill"、"怎么组合这些 skill"、"工作流怎么走"、"进入新项目不确定先后顺序"。
  隐式触发：用户面对多个 skill 不知如何组合、复杂任务需要规划多 skill 协作流程、用户进入新项目后第一次对话。
  不触发：用户明确知道要用哪个 skill（直接使用，不需要路由）、任务简单只涉及单个 skill、用户在问具体 skill 的用法而非组合。
context: fork
agent: orchestrator
compatibility: opencode
metadata:
  category: routing
---
# 技能编排与工作流路由（Orchestration）

## 核心原则
- **组合比单点更重要**：选择正确的 skill 组合和执行顺序，比掌握单个 skill 更关键。
- **按需使用，不全量启动**：12 个 skill 是按需使用的工具箱，不是每次都要全走一遍。
- **编排是路由知识**：主对话持续记住的决策逻辑，不是"委派出去等结果"的执行任务。
## 何时使用
- 用户问"我该用哪些 skill"或"怎么开始用这套 harness"
  - 例如：用户刚接触这套体系，不知道从哪个skill开始
  - 例如：用户问"我想提高代码质量，该用哪些skill"
- 用户问"怎么组合这些 skill"或"工作流怎么走"
  - 例如：用户想同时进行代码质量检查和性能验证
  - 例如：用户问"如何同时使用verification-loop和observability-and-browser"
- 面对多个 skill 不知如何组合
  - 例如：用户有多个skills可选，但不确定哪个组合最合适
  - 例如：用户想同时解决代码风格和架构边界问题
- 进入新项目，不确定先做什么后做什么
  - 例如：用户刚加入一个新项目，不知道如何开始使用harness体系
  - 例如：用户问"在这个项目中，我应该先做什么"
- 复杂任务需要规划多 skill 协作流程
  - 例如：用户要同时进行功能开发、质量检查和性能验证
  - 例如：用户要规划一个包含多个skills的完整开发流程
## 何时不该用
- 用户明确知道要用哪个 skill——直接使用，不需要路由。
- 任务简单，只涉及单个 skill——不需要编排开销。
## 五条标准工作流

### Workflow 1: Greenfield 初始化
1. Step 1: 执行 `project-intake`，产出结构化项目卡片
2. Step 2: 执行 `bootstrap`，生成 AGENTS.md + docs/ 骨架
3. Step 3: 执行 `repo-map`，校验文档结构完整性
4. Step 4: 执行 `architecture-boundaries` + `golden-principles`（小项目可跳过 `architecture-boundaries`）

**适用场景**：
- 新项目首次使用harness体系
- 项目还没有AGENTS.md和docs/结构
- 用户问"如何开始使用这套harness"

### Workflow 2: 日常功能开发
1. Step 1: （可选）执行 `exec-plans`，落盘执行计划
2. Step 2: 实现功能代码
3. Step 3: 执行 `verification-loop`，自验证循环
4. Step 4: 执行 `commit-gate`，提交前质量检查
- 简单改动可跳过 Step 1 和 Step 3

**适用场景**：
- 开发新功能或修复bug
- 需要确保代码质量
- 需要提交代码前进行质量检查

### Workflow 3: 代码质量修复
1. Step 1: 执行 `golden-principles`，扫描品味漂移
2. Step 2: （可选）执行 `architecture-boundaries`，处理结构性问题
3. Step 3: 执行 `verification-loop`，自验证循环
4. Step 4: 执行 `commit-gate`，提交前质量检查
- 纯品味漂移可跳过 Step 2

**适用场景**：
- 代码风格不统一
- 存在重复或不一致的实现模式
- 需要清理AI生成的代码

### Workflow 4: 扩展 harness 体系
1. Step 1: 执行 `authoring`，编写新 skill/agent
2. Step 2: （可选）执行 `bootstrap`，初始化新结构
3. Step 3: 执行 `repo-map`，校验文档结构完整性

**适用场景**：
- 需要添加新的skill或agent
- 需要扩展harness体系的功能
- 用户问"如何给这套体系添加新能力"

### Workflow 5: 优化 prompt 质量
1. Step 1: 执行 `prompt-optimizer`（独立使用，无需其他 skill 配合）

**适用场景**：
- 需要优化提示词质量
- 需要创建结构化的prompt
- 用户问"如何让AI更好地完成任务"

三层路由判断和详细交接点表见 `references/routing-decision-tree.md`。
## 方法论
### 常见省略场景
- 小项目不需要 `architecture-boundaries`（无多层架构要守）。
- 纯文档改动不需要 `verification-loop` 和 `observability-and-browser`。
- 已有完善 harness 结构的项目不重走 Workflow 1。
- `authoring` 只在扩展 harness 体系时使用。
- `prompt-optimizer` 只在需要优化提示词时使用。
## 硬约束
- **Workflow 1 不得跳过 `project-intake`**：违反则 `bootstrap` 生成的骨架可能与项目实际不符，导致后续返工。
- **不得对已明确 skill 的用户强制编排**：用户明确说"用 X skill"时直接执行，违反则浪费上下文窗口，降低效率。

## 关键要点
- 先判断用户目标属于哪条工作流，再决定 skill 组合。
- 目标跨多个工作流时，说明组合方式和交接点。
- 目标有歧义时先澄清再路由，不猜测。
- 简单任务跳过重量级 skill，避免过度工程。
- 定期审计工作流，确保流程的有效性和适用性。
- 文档化工作流决策，便于团队理解和遵循。

## 跨skill交接点

### 交接点总览

| 上游skill | 产出物 | 下游consumer | 交接方式 |
|---|---|---|---|
| `project-intake` | 结构化项目卡片 | `bootstrap` | 卡片信息直接传入 |
| `exec-plans` | exec-plan文件 | `verification-loop` | 文件路径传递 |
| `verification-loop` | 验证通过信号 | `commit-gate` | 完成总结传递 |
| `golden-principles` | 修复队列 | `verification-loop` | 逐项修复清单 |
| `architecture-boundaries` | lint规则 | `verification-loop`/`commit-gate` | 作为自检项 |

### Workflow 2 交接点详解（日常功能开发）

```
exec-plans → verification-loop → commit-gate
```

**交接点1: exec-plans → verification-loop**
- **前置条件**：exec-plan已创建，包含至少一个带验收条件的步骤
- **输入**：exec-plan文件路径
- **输出**：每轮迭代后的步骤勾选状态和决策日志
- **验证方法**：检查exec-plan文件中是否有已完成步骤的勾选标记
- **错误处理**：若exec-plan不存在或格式错误，报告并停止

**交接点2: verification-loop → commit-gate**
- **前置条件**：所有自动化检查通过，无未处理评审意见
- **输入**：验证完成总结（做了什么、怎么验证的、已知限制）
- **输出**：commit hash和变更摘要
- **验证方法**：确认commit-gate执行了git commit并返回hash
- **错误处理**：若验证未完成（有失败测试/lint），阻塞提交

### Workflow 3 交接点详解（代码质量修复）

```
golden-principles → verification-loop → commit-gate
```

**交接点1: golden-principles → verification-loop**
- **前置条件**：golden-principles已扫描完成，产出修复队列
- **输入**：修复队列（偏离模式列表）
- **输出**：逐项修复后的代码状态
- **验证方法**：检查修复队列中的每项是否已被处理
- **错误处理**：若修复队列为空，跳过verification-loop直接进入commit-gate

**交接点2: verification-loop → commit-gate**
- **前置条件**：所有修复项已完成，测试通过
- **输入**：修复完成总结
- **输出**：commit hash
- **验证方法**：确认所有修复项已体现在git diff中
- **错误处理**：若修复引入新问题，返回verification-loop继续迭代

### 跨工作流组合

**场景**：用户目标涉及多个工作流（如初始化+日常开发）

**组合方式**：
1. 先完成Workflow 1（初始化）
2. 确认初始化产出物完整（AGENTS.md + docs/骨架）
3. 再进入Workflow 2（日常开发）

**交接点验证**：
- 检查AGENTS.md是否存在且包含正确的skill地图
- 检查docs/目录结构是否完整
- 确认architecture-boundaries和golden-principles已配置（如需要）

## 边界情况处理

> 通用边界情况（目标澄清、项目规模极小、遗留项目改造、多团队协作等）参见 `references/common-edge-cases.md`，以下仅列出本 skill 特有的边界情况。

### 跨多个工作流

**场景**：用户目标涉及多个工作流
**处理**：识别跨工作流任务，说明组合方式和交接点

## 最佳实践

### 工作流选择最佳实践

1. **根据用户目标选择工作流**
   - 分析用户需求，确定属于哪条工作流
   - 避免全量启动所有skills
   - 确保工作流与用户目标匹配

2. **识别跨工作流任务**
   - 分析用户目标是否涉及多个工作流
   - 说明组合方式和交接点
   - 确保工作流之间的衔接顺畅

3. **简化简单任务**
   - 简单任务直接使用单个skill
   - 避免过度工程
   - 提高效率

### 工作流执行最佳实践

1. **遵循工作流顺序**
   - 严格按照工作流步骤执行
   - 确保前置步骤完成后再进行后续步骤
   - 避免跳过前置步骤

2. **控制工作流规模**
   - 根据项目规模调整工作流
   - 小项目简化工作流
   - 大项目完整执行工作流

3. **记录工作流决策**
   - 记录工作流选择的原因
   - 记录工作流执行的过程
   - 记录工作流执行的结果

### 团队协作最佳实践

1. **建立统一标准**
   - 建立统一的工作流规范
   - 确保团队成员理解并遵循
   - 定期审计标准执行情况

2. **提供工具支持**
   - 提供工作流执行工具
   - 集成到CI/CD流程
   - 提供IDE插件支持

3. **持续改进**
   - 定期审计工作流有效性
   - 根据团队反馈调整工作流
   - 持续优化工作流效率
## 常见陷阱
- **全量启动**：每次把 12 个 skill 全走一遍，浪费时间和上下文。
  - 解决方案：根据用户目标选择合适的工作流，只使用必要的skills
- **跳过前置步骤**：不走 `project-intake` 就开始 `bootstrap`，骨架可能和项目实际不符。
  - 解决方案：严格遵循工作流顺序，确保前置步骤完成后再进行后续步骤
- **混淆品味与结构**：用 `golden-principles` 处理结构性问题，或用 `architecture-boundaries` 处理品味偏好。
  - 解决方案：明确区分品味偏好和结构性约束，选择正确的skill处理
- **过度路由**：用户明确知道要什么 skill 时，不需要绕一圈编排。
  - 解决方案：当用户明确指定skill时，直接使用，不需要编排
- **忽略简单任务**：对简单任务使用复杂的编排流程。
  - 解决方案：简单任务直接使用单个skill，不需要编排开销
- **不澄清就路由**：目标有歧义时直接猜测用户意图。
  - 解决方案：目标有歧义时先澄清再路由，不猜测
## Agent 提示词

### 技能编排顾问（Orchestrator）

## 角色定义

只读路由顾问，根据用户目标推荐正确的 skill 组合和执行顺序，由主对话按建议调用对应 skill。你擅长分析用户需求，识别工作流，提供最佳的skill组合建议。

## 跳过条件

- **用户明确知道要用哪个 skill**：直接使用，不需要路由。
- **任务简单，只涉及单个 skill**：不需要编排开销。
- **用户在问具体 skill 的用法而非组合**：直接回答用法问题。

## 核心能力

- 判断用户目标属于哪条标准工作流（初始化/日常开发/质量修复/扩展 harness/prompt 优化）。
- 识别跨工作流任务，说明组合方式和交接点。
- 根据任务规模判断哪些 skill 可以省略。
- 处理各种边界情况，提供最佳实践。

## 执行流程

1. **理解目标**：判断用户意图——初始化、日常开发、质量修复、扩展 harness 还是 prompt 优化。
   - 分析内容：
     - 用户描述的需求
     - 项目的当前状态
     - 用户的技术背景

2. **匹配工作流**：参考 SKILL.md 中的五条标准工作流和决策树，选择匹配的工作流。
   - 匹配方法：
     - 分析用户目标，确定属于哪条工作流
     - 检查是否涉及多个工作流
     - 确定工作流的执行顺序

3. **输出建议**：推荐 skill 组合和执行顺序。
   - 建议内容：
     - 推荐的skill列表
     - 执行顺序
     - 省略建议
     - 交接点说明

4. **跨流组合**：如目标跨多个工作流，说明组合方式和交接点。
   - 组合内容：
     - 工作流组合方式
     - 交接点的前置条件
     - 交接点的产出物

## 约束

- **只读不执行**：不替用户调用任何 skill，只输出路由建议。违反时撤回执行，以建议形式输出。
- **先澄清再路由**：目标有歧义时先提问，不猜测。违反时补充澄清问题。
- **简单任务不绕路**：明确知道用哪个 skill 时直接建议，不需要绕一圈编排。违反时简化建议。
- **守住前置依赖**：跨工作流组合时按交接点表确认上游已落盘；尤其 Workflow 1 必须先经 `project-intake` 再 `bootstrap`，否则骨架与项目实际不符。违反时补充缺失的前置步骤。
- **区分工作流类型**：必须准确区分初始化、日常开发、质量修复、扩展 harness、prompt 优化等类型，不能混淆。违反时重新分类。
- **提供具体建议**：每个建议都必须具体、可执行，不能模糊。违反时补充具体建议。
- **处理边界情况**：必须处理各种边界情况，提供最佳实践。违反时补充边界情况处理。

## 输出规范

- **推荐 skill 列表**：按执行顺序排列，包含 skill 名称和简要职责说明。
- **工作流编号**：明确属于哪条标准工作流（1-5），或标注"跨流组合"。
- **省略建议**：标注哪些步骤可跳过及理由。
- **交接点说明**：跨工作流时，说明每个交接点的前置条件和产出物。
- **边界情况处理**：针对不同边界情况提供处理方案。
- **最佳实践**：提供工作流执行的最佳实践。

## 相关模板

- `references/routing-decision-tree.md`：路由决策树与标准工作流
- `references/automation-check-script.sh`：自动化检查脚本

## 自动化检查

### 自动化检查脚本

```bash
#!/bin/bash
# 技能编排自动化检查脚本

SKILLS_DIR="./skills"
SKILL_NAME="harness-orchestration"
REPORT_FILE="docs/quality-reports/orchestration-check.md"

# 创建报告目录
mkdir -p docs/quality-reports

# 开始报告
echo "# 技能编排自动化检查报告" > "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "检查时间: $(date)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

SKILL_FILE="$SKILLS_DIR/$SKILL_NAME/SKILL.md"

if [ -f "$SKILL_FILE" ]; then
    echo "## 检查结果" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    
    # 检查frontmatter
    echo "### Frontmatter检查" >> "$REPORT_FILE"
    if grep -q "^name:" "$SKILL_FILE"; then
        echo "- [x] name 字段存在" >> "$REPORT_FILE"
    else
        echo "- [ ] name 字段缺失" >> "$REPORT_FILE"
    fi
    
    if grep -q "^description:" "$SKILL_FILE"; then
        echo "- [x] description 字段存在" >> "$REPORT_FILE"
    else
        echo "- [ ] description 字段缺失" >> "$REPORT_FILE"
    fi
    
    # 检查标准章节
    echo "### 章节结构检查" >> "$REPORT_FILE"
    if grep -q "^## 核心原则" "$SKILL_FILE"; then
        echo "- [x] 核心原则章节存在" >> "$REPORT_FILE"
    else
        echo "- [ ] 核心原则章节缺失" >> "$REPORT_FILE"
    fi
    
    if grep -q "^## 何时使用" "$SKILL_FILE"; then
        echo "- [x] 何时使用章节存在" >> "$REPORT_FILE"
    else
        echo "- [ ] 何时使用章节缺失" >> "$REPORT_FILE"
    fi
    
    if grep -q "^## 方法论" "$SKILL_FILE"; then
        echo "- [x] 方法论章节存在" >> "$REPORT_FILE"
    else
        echo "- [ ] 方法论章节缺失" >> "$REPORT_FILE"
    fi
    
    # 检查示例数量
    example_count=$(grep -c "^### 示例\|^#### 示例\|^## 示例" "$SKILL_FILE" || echo "0")
    echo "### 示例统计" >> "$REPORT_FILE"
    echo "- 示例数量: $example_count" >> "$REPORT_FILE"
    
    # 检查错误处理指导
    if grep -q "错误处理\|故障排除\|常见问题" "$SKILL_FILE"; then
        echo "- [x] 包含错误处理指导" >> "$REPORT_FILE"
    else
        echo "- [ ] 缺少错误处理指导" >> "$REPORT_FILE"
    fi
    
    # 检查边界情况处理
    if grep -q "边界情况" "$SKILL_FILE"; then
        echo "- [x] 包含边界情况处理" >> "$REPORT_FILE"
    else
        echo "- [ ] 缺少边界情况处理" >> "$REPORT_FILE"
    fi
    
    # 检查最佳实践
    if grep -q "最佳实践" "$SKILL_FILE"; then
        echo "- [x] 包含最佳实践" >> "$REPORT_FILE"
    else
        echo "- [ ] 缺少最佳实践" >> "$REPORT_FILE"
    fi
    
    echo "" >> "$REPORT_FILE"
    echo "## 检查完成" >> "$REPORT_FILE"
else
    echo "## 错误" >> "$REPORT_FILE"
    echo "SKILL.md 文件不存在" >> "$REPORT_FILE"
fi

echo "自动化检查完成，报告已保存到 $REPORT_FILE"
```

### CI/CD集成

```yaml
name: Orchestration Check

on:
  push:
    paths:
      - 'skills/harness-orchestration/SKILL.md'
  pull_request:
    paths:
      - 'skills/harness-orchestration/SKILL.md'

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check orchestration quality
        run: |
          bash scripts/orchestration-check.sh
```

---
最后更新: 2026-07-02（变更：A+级优化，增加边界情况处理，增加最佳实践，增加自动化检查脚本，优化Agent提示词，加强跨skill交接点说明）
