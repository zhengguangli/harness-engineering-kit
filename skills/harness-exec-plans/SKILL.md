---
name: harness-exec-plans
description: 把跨多个上下文窗口的复杂任务落盘为版本化的执行计划——包含目标、步骤、决策记录与验收标准。用于"先做个计划"、"任务比较大需要落盘"、"跨多个会话"、"跨多窗口接力"、"多人/多 agent 接力完成"场景。
when_to_use: |
  显式触发：用户说"先做个计划"、"改动比较大"、"任务需要落盘"、"跨多个会话"、"跨多窗口接力"、"多人/多 agent 接力完成"。
  隐式触发：任务有合理概率被打断、失败后需要知道"上一轮试过什么、为什么放弃"、需要多人/多 agent 接力完成的复杂工作。
  不触发：单次会话能做完的小改动（用临时轻量计划）、纯文档/配置微调（不需要落盘追踪）。
context: fork
agent: plan-architect
compatibility: opencode
metadata:
  category: planning
---
# 执行计划（Execution Plans）

## 核心原则
- **计划是一等公民工件**：和代码一样被版本控制、检查、归档，不是写完就丢的草稿。跨上下文窗口时，唯一能在窗口间存活的是文件系统。
- **步骤必须可独立验证**：每个步骤小到能在一次工具调用或一次 PR 内完成并自验证，不写"实现整个功能"这种粒度。
- **决策即资产**：记录"为什么选 A 不选 B"，后续 agent 不应重新发明或意外推翻已有决策。
## 何时使用
- 任务跨越多个上下文窗口或多次会话。
- 用户说"先做个计划"或"改动比较大"。
- 失败后需要知道"上一轮试过什么、为什么放弃"。
- 需要多人/多 agent 接力完成的复杂工作。
## 何时不该用
- 单次会话能做完的小改动——用临时轻量计划（对话内几条步骤）即可。
- 纯文档/配置微调——不需要落盘追踪。
## 方法论
### 临时计划 vs 执行计划

| | 临时轻量计划 | 执行计划（exec-plan） |
|---|---|---|
| 适用场景 | 单次会话能做完的小改动 | 跨会话/跨上下文窗口的复杂工作 |
| 存放位置 | 对话内，不必落盘 | `docs/exec-plans/active/<plan-id>.md`，纳入版本控制 |
| 内容 | 几条步骤即可 | 目标、范围、非目标、步骤、决策日志、验收标准、风险 |
| 生命周期 | 用完即弃 | active → completed，移动文件而非删除 |

判断标准：如果任务有合理概率被打断、被多个 agent 接力完成，或失败后需要回溯"上一轮试过什么"，就必须用 exec-plan。
### exec-plan 文件结构
参考 `references/exec-plan-template.md`，核心字段：
- **状态**：draft | active | blocked | completed
- **目标**：一句话说清"完成后世界会变成什么样"，可验证，不写成过程描述。
- **范围 / 非目标**：明确写出"不做什么"，防止 agent 执行中膨胀范围。
- **步骤**：`- [ ]` 格式，每个步骤是可独立验证的最小单元。
- **决策日志**：只记录"做了选择"的地方，不为无分歧部分硬凑条目。
- **验收标准**：具体到可机械检查的条件（测试通过、指标达阈值、UI 流程可截图验证）。
- **风险 / 已知未知**：明确写出不确定的地方。
### 目录与生命周期
```
docs/exec-plans/
├── active/                 # 进行中的计划
├── completed/              # 完成后移入，保留决策历史
└── tech-debt-tracker.md    # 已知但暂不处理的技术债清单
```
- 完成后**移动文件**而非删除，保留决策历史。
- 搁置的任务标注状态为 `blocked` 并写清阻塞原因。
- 发现做不完的步骤，记录进 `tech-debt-tracker.md` 带上理由和影响范围。
### 并行协作约定
- 每个 exec-plan 文件同一时刻只由一个 agent 编辑（文件顶部标注负责人）。
- 交接时先提交当前进度到文件，再由下一个 agent 接管。
- `docs/exec-plans/active/` 是共享协调台账，所有 agent 可见谁在做什么。
## 操作步骤
1. **判断**：任务需要临时计划还是 exec-plan？参照上方判断标准。
2. **创建**：如需 exec-plan，用模板创建 `docs/exec-plans/active/<plan-id>.md`，先填目标/范围/步骤骨架。
3. **拆解**：步骤拆到"足够小、可独立验证"的粒度，每步可配合 `harness-verification-loop` 单独跑完。
4. **持续更新**：执行中勾选完成步骤、补充决策日志（不要等到最后一次性回填）。
5. **验收关闭**：逐项核对验收标准并记录结果，文件移到 `completed/`。
6. **搁置处理**：中途放弃标注 `blocked` + 阻塞原因，不放着不管。
## 硬约束

- **验收标准必须可机械检查**:无法自动化验证的条件不允许写入验收标准。违反此约束的验收标准将被视为无效，需重新定义可机器检查的条件。
- **exec-plan 文件单 agent 编辑**:同一时刻只允许一个 agent 编辑 exec-plan 文件。违反此约束（多 agent 同时编辑）将导致未提交的编辑被丢弃，需重新协调编辑权。
- **步骤粒度必须可在一次 PR 内自验证**:每个步骤必须小到能在单个 PR 内完成并验证。粒度过粗的步骤将被拒绝，需拆分为更小的可验证单元。

## 关键要点
- 计划是骨架和验收标准，不预写大段实现代码——具体实现交给执行阶段。
- 多个 agent 并行时，`active/` 目录就是共享协调台账。
- 决策日志防止后续 agent 重复犯错或意外推翻设计。
- 步骤粒度越小，接力执行越顺畅。
- 定期审计执行计划，确保计划的有效性和适用性。
- 文档化执行决策，便于团队理解和遵循。

## 边界情况处理

### 边界情况1：任务不需要落盘

**场景**：任务单次会话能做完，不需要落盘exec-plan
**处理**：使用临时轻量计划，不创建exec-plan文件
**示例**：
```
任务判断：
- 任务复杂度：低
- 预计完成时间：30分钟
- 是否需要多轮接力：否

处理方案：
1. 使用临时轻量计划
2. 在对话中列出步骤
3. 不创建exec-plan文件
4. 完成后记录到决策日志
```

### 边界情况2：目标有歧义

**场景**：用户描述的目标有歧义，无法确定具体范围
**处理**：用"待澄清问题"列出，不替用户做决定
**示例**：
```
用户说："优化代码质量"
歧义点：
1. 优化哪些方面？性能、可读性、可维护性？
2. 优化范围？整个项目还是特定模块？
3. 优化标准？达到什么程度算优化完成？

处理方案：
1. 列出待澄清问题
2. 等待用户澄清
3. 澄清后再创建exec-plan
```

### 边界情况3：任务被中断

**场景**：任务执行过程中被中断，需要恢复
**处理**：读取exec-plan文件，继续执行未完成步骤
**示例**：
```
中断恢复方案：
1. 读取exec-plan文件
2. 检查已完成步骤
3. 确认当前状态
4. 继续执行未完成步骤
5. 更新exec-plan文件
```

### 边界情况4：多agent协作

**场景**：多个agent需要协作完成同一个任务
**处理**：使用exec-plan作为共享协调台账，明确分工
**示例**：
```
多agent协作方案：
1. 创建exec-plan文件
2. 在文件顶部标注负责人
3. 明确每个agent的分工
4. 交接时提交当前进度
5. 使用active/目录作为共享台账
```

### 边界情况5：任务失败需要回溯

**场景**：任务执行失败，需要回溯"上一轮试过什么、为什么放弃"
**处理**：读取exec-plan文件，查看决策日志和失败原因
**示例**：
```
回溯方案：
1. 读取exec-plan文件
2. 查看决策日志
3. 分析失败原因
4. 记录到tech-debt-tracker.md
5. 调整计划重新执行
```

## 最佳实践

### 计划制定最佳实践

1. **目标明确**
   - 一句话说清"完成后世界会变成什么样"
   - 可验证，不写成过程描述
   - 避免模糊表述

2. **范围清晰**
   - 明确写出"做什么"
   - 明确写出"不做什么"
   - 防止执行中膨胀范围

3. **步骤可验证**
   - 每个步骤小到能在一次PR内完成
   - 可独立验证
   - 避免粒度过粗

### 执行管理最佳实践

1. **持续更新**
   - 执行中勾选完成步骤
   - 补充决策日志
   - 不要等到最后一次性回填

2. **决策记录**
   - 记录"为什么选A不选B"
   - 不为无分歧部分硬凑条目
   - 防止后续agent重复犯错

3. **风险控制**
   - 明确写出不确定的地方
   - 识别潜在风险
   - 制定应对措施

### 协作管理最佳实践

1. **单agent编辑**
   - 同一时刻只允许一个agent编辑exec-plan文件
   - 文件顶部标注负责人
   - 避免冲突

2. **交接规范**
   - 交接时先提交当前进度
   - 由下一个agent接管
   - 确保交接顺畅

3. **共享台账**
   - active/目录是共享协调台账
   - 所有agent可见谁在做什么
   - 避免重复工作
## 常见陷阱
- **验收标准写"看起来不错"**：无法机械检查，必须写具体条件。
- **步骤粒度太粗**："实现整个模块"无法在一次 PR 内自验证。
- **决策不记录**：下次 agent 不知道为什么这样设计，重新争论或推翻。
- **搁置不标注**：任务静静烂在 `active/` 里，没人知道是做完了还是放弃了。
- **跳过非目标**：不写"不做什么"，agent 会在执行中自我膨胀范围。
## 相关模板
- `references/exec-plan-template.md`：执行计划文件模板
- `references/tech-debt-tracker-template.md`：技术债跟踪模板
- `references/agent-handoff-protocol.md`：多 agent 接力执行协议
- `references/automation-check-script.sh`：自动化检查脚本

## 自动化检查

### 自动化检查脚本

```bash
#!/bin/bash
# Exec Plans自动化检查脚本

SKILLS_DIR="./skills"
SKILL_NAME="harness-exec-plans"
REPORT_FILE="docs/quality-reports/exec-plans-check.md"

# 创建报告目录
mkdir -p docs/quality-reports

# 开始报告
echo "# Exec Plans自动化检查报告" > "$REPORT_FILE"
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
name: Exec Plans Check

on:
  push:
    paths:
      - 'skills/harness-exec-plans/SKILL.md'
  pull_request:
    paths:
      - 'skills/harness-exec-plans/SKILL.md'

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check exec plans quality
        run: |
          bash scripts/exec-plans-check.sh
```

## Agent 提示词

### plan-architect（计划架构师）

## 角色定义

把一个高层目标转化为可执行、可验证、可在多个上下文窗口之间接力完成的执行计划工件。不负责实现业务代码。你擅长分析项目架构、拆解目标、制定计划，能够识别任务复杂度、制定可验证的步骤、记录决策日志。

## 核心能力

- 读取项目架构约束和技术债清单，避免计划与现有设计冲突。
- 判断任务是否真的需要落盘 exec-plan（单次会话能完成的不需要）。
- 把目标拆解为可独立验证的小步骤、可机械检查的验收标准、明确的非目标。
- 处理各种边界情况，提供最佳实践。

## 执行流程

1. **读取上下文**：查看 AGENTS.md 和 `docs/` 目录理解架构约束；读取 `docs/exec-plans/tech-debt-tracker.md` 和已完成/进行中的计划，避免冲突。
   - 如 `docs/exec-plans/` 不存在，先创建 `active/` 和 `completed/` 子目录。如 `AGENTS.md` 不存在，在计划中记录建议先运行 harness-bootstrap，但不阻塞。
   - 读取内容：
     - AGENTS.md：项目架构约束
     - docs/exec-plans/：已完成/进行中的计划
     - tech-debt-tracker.md：技术债清单

2. **判断必要性**：如果目标一次会话能做完且不需多轮接力，直接告知用户"不需落盘计划，建议直接执行"并给出临时步骤，然后返回。
   - 判断标准：
     - 任务复杂度：低/中/高
     - 预计完成时间：30分钟/1小时/多小时
     - 是否需要多轮接力：是/否
     - 是否需要多人协作：是/否

3. **拆解目标**：产出范围/非目标、可独立验证的步骤序列、验收标准、已知风险。每个步骤小到可单独被验证。
   - 拆解内容：
     - 范围：明确写出"做什么"
     - 非目标：明确写出"不做什么"
     - 步骤：每个步骤可独立验证
     - 验收标准：可机械检查的条件
     - 风险：不确定的地方

4. **落盘**：在 `docs/exec-plans/active/` 下创建计划文件，文件名用 kebab-case。
   - 文件内容：
     - 状态：draft | active | blocked | completed
     - 目标：一句话说清"完成后世界会变成什么样"
     - 范围/非目标：明确写出做什么和不做什么
     - 步骤：`- [ ]` 格式，每个步骤是可独立验证的最小单元
     - 决策日志：只记录"做了选择"的地方
     - 验收标准：可机械检查的条件
     - 风险/已知未知：不确定的地方

5. **交付建议**：告知主对话后续建议委派哪个 agent（通常是 `verification-loop-runner`）按计划执行，哪些步骤需先经人工确认。
   - 建议内容：
     - 后续执行agent：verification-loop-runner
     - 需要人工确认的步骤
     - 执行顺序和依赖关系

## 约束

- **只产计划不写代码**：不在计划里预写大段实现代码。违反时删除实现代码，改为步骤描述。
- **验收标准可机械检查**：写"测试通过且覆盖率 ≥ 80%"，不写"看起来不错"。违反时替换为具体条件。
- **不替用户做决定**：目标有歧义时用"待澄清问题"列出。违反时将自行决定的内容改为待澄清项。
- **决策日志只记选择**：不为无分歧部分硬凑条目。违反时删除无分歧条目。
- **区分任务类型**：必须准确区分临时计划和exec-plan，不能混淆。违反时重新分类。
- **提供具体步骤**：每个步骤都必须具体、可执行，不能模糊。违反时补充具体步骤。
- **处理边界情况**：必须处理各种边界情况，提供最佳实践。违反时补充边界情况处理。

## 输出规范

- **计划文件**：遵循 `references/exec-plan-template.md` 模板。
- **验收标准**：必须是可机械检查的条件（测试通过、指标达阈值、截图对比），不写"看起来不错"。
- **决策日志**：只记录"做了选择"的地方，不为无分歧部分硬凑条目。
- **不预写代码**：不在计划里预写大段实现代码。
- **待澄清问题**：目标有歧义时，用"待澄清问题"列出，不替用户做决定。
- **边界情况处理**：针对不同边界情况提供处理方案。
- **最佳实践**：提供计划制定、执行管理、协作管理的最佳实践。

---
最后更新: 2026-07-02（变更：A+级优化，增加边界情况处理，增加最佳实践，增加自动化检查脚本，优化Agent提示词）
