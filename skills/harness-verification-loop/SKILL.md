---
name: harness-verification-loop
description: 实施"自验证循环"——agent 实现代码变更后自己审查、跑测试/构建/lint、请求评审并在反馈中迭代，直到可合并。用于"把改动推进到可合并状态"、"自动修复测试失败"、"建立实现→自检→测试→评审→修复循环"、"代码任务反复失败需要循环迭代"场景。
when_to_use: |
  显式触发：用户要求把代码改动推进到"可合并"状态、可验证的代码任务反复失败需要循环迭代、需要建立提交前自检流程。
  隐式触发：用户说"把代码改好"、"修复测试失败"、"确保代码能合并"、改动需要多轮测试和修复才能达标。
  不触发：改动是单行配置修复或 typo 修正（直接走 commit-gate）、项目没有任何测试/构建/lint 配置（循环没有反馈信号可依赖）、任务是纯探索/头脑风暴、已经有 commit-gate 且改动极小。
disable-model-invocation: true
context: fork
agent: verification-loop-runner
compatibility: opencode
metadata:
  category: workflow
---

# Verification Loop（自验证循环）

## 核心原则

- **失败是缺失能力的信号，不是不够努力的信号**：任务失败时，正确的反应不是"再试一次"，而是问"agent 缺了什么能力，如何让它可见、可执行？"这是 harness engineering 区别于"加大力气提示"的地方。
- **基于真实反馈迭代，不凭一次性输出收工**：让 agent 在循环里反复尝试同一个目标，每轮基于测试结果、lint 报错、评审意见调整。
- **设定边界，避免空转**：没有边界的循环会在卡住的任务上无限重复同样的失败。

## 何时使用

- 用户要求把代码改动自主推进到"可合并"状态。
- 可验证的代码任务反复失败，需要循环迭代而非一次性尝试。
- 需要建立提交前自检流程（实现 → 自检 → 测试 → 评审 → 修复）。

## 何时不该用

- 改动是单行配置修复或 typo 修正——直接走 `commit-gate` 即可。
- 项目没有任何测试/构建/lint 配置——循环没有反馈信号可依赖，只会空转。先补齐基础设施。
- 任务是纯探索/头脑风暴（不产出可验证的代码变更）。
- 已经有 `commit-gate` 且改动极小——不要为一行改动启动 8 轮循环。

## 方法论

### 循环的标准步骤

```
1. 实现变更
2. 本地自检
   - git diff 通读，确认没有超出范围
   - 跑相关测试 / lint / 构建
3. 如有自动化验证手段（浏览器驱动、可观测性查询），
   用 harness-observability-and-browser 技能产出证据
4. 请求额外评审
   - 可以是另一个 agent（如 boundary-auditor 检查架构边界）
   - 也可以是人工评审，但不强制等待
5. 处理反馈
   - 对每条反馈给出修复或有理有据的反驳，不要静默忽略
6. 重复 1-5，直到：
   - 所有自动化评审通过，且
   - 没有未处理的评审意见
7. 合并 / 标记为完成
   - 只有在"需要人类判断"时才升级给人类
```

### 验收标准

验收标准必须是具体的、机械可检查的条件（如"全部测试通过且覆盖率 ≥ X%"、"关键用户旅程截图前后对比无异常"），不要写"看起来不错"这种无法验证的标准。

### 循环边界设定

- **最大迭代次数**：默认 8 轮（可由用户或 exec-plan 调整，建议范围 5-10），超过后必须升级或写明卡住原因。
- **每轮迭代要有实质性变化**：连续两轮做完全一样的尝试，说明缺的不是"再试一次"，而是缺一个新的能力/信息源。
- **把状态写回 exec-plan**（配合 `harness-exec-plans` 技能），这样即使上下文窗口用完，下一轮可以从文件里接着读进度。

循环卡住时的诊断表（症状→缺失能力→修复方向），详见 `references/stuck-loop-diagnostics.md`。

### 操作步骤

1. **明确完成定义**：哪些自动化检查必须通过才算合格（测试、lint、架构边界、性能预算）。
2. **实现第一版变更**。
3. **跑循环步骤 1-6**。
4. **每轮迭代后**：如果使用 exec-plan，更新步骤勾选状态和决策日志。
5. **达成完成定义后**：产出简短总结——做了什么、怎么验证的、还有什么已知限制。
6. **提交**：循环收敛后，交由 `harness-commit-gate` 完成提交。
7. **如果在边界次数内没能收敛**：明确写出卡在哪、缺什么，升级给人类或记录进 `tech-debt-tracker.md`，不要假装完成。

## 硬约束

- **最大迭代 8 轮**：超过→必须写 stuck report 并升级。
- **连续两轮必须有实质变化**：否则判定为 stuck。
- **测试失败必须修复，不得跳过**：违反→阻塞合并。

## 关键要点

- 失败时先问"缺了什么能力"，不要简单粗暴地重复同一种尝试。
- 只有在涉及不可逆操作、产品取舍、安全敏感决策时才升级给人类；能用自动化检查解决的问题，不要无谓请求人工介入。
- 验收标准必须是机械可检查的条件，不是主观判断。
- 连续两轮如果尝试方式完全相同却没有进展，停下来指出"缺失的能力是什么"，而不是继续空转。
- 定期审计验证循环，确保循环的有效性和适用性。
- 文档化验证决策，便于团队理解和遵循。

## 跨skill交接点

### 与commit-gate的交接

**交接时机**：验证循环收敛后（所有自动化检查通过且无未处理意见）

**前置条件检查清单**：
- [ ] 所有测试通过（bun test / npm test / vitest run / cargo test）
- [ ] 构建成功（bun run build / npm run build）
- [ ] 类型检查通过（tsc --noEmit）
- [ ] Lint检查通过（如有配置）
- [ ] 无未处理的评审意见
- [ ] 连续两轮迭代有实质性变化（未触发stuck检测）

**输入数据**：
```
验证完成总结:
- 做了什么: [具体变更描述]
- 怎么验证的: [测试/lint/构建结果]
- 已知限制: [如有]
- 迭代记录: [总轮数、关键变化]
```

**输出数据**：
```
提交结果:
- commit hash: [hash值]
- 变更文件数: [数量]
- 变更行数: [行数]
- 测试/构建结果: [通过/失败状态]
```

**交接方式**：
1. 验证循环完成后，输出简短总结
2. 调用commit-gate时传递总结内容
3. commit-gate执行质量门检查
4. 返回commit hash和变更摘要

**错误处理**：
| 错误场景 | 处理方式 |
|---|---|
| commit-gate检测到测试失败 | 阻塞提交，返回verification-loop修复 |
| commit-gate检测到敏感信息 | 阻塞提交，报告敏感信息位置 |
| commit-gate检测到scope creep | 建议拆分提交，等待用户确认 |
| commit-gate执行失败 | 报告错误，保留本地变更 |

**验证方法**：
1. 确认commit-gate返回了有效的commit hash
2. 确认git log中包含本次提交
3. 确认变更摘要与实际diff一致

### 与orchestration的交接

**交接时机**：被orchestration路由调用时

**前置条件**：
- orchestration已识别用户目标属于Workflow 2或3
- 已确定需要verification-loop

**输入数据**：
```
任务目标: [具体描述]
验收标准: [机械可检查条件]
exec-plan路径: [如有]
```

**输出数据**：
```
验证结果: [通过/未通过]
迭代轮数: [数量]
已知限制: [如有]
```

**错误处理**：
- 若orchestration传入的验收标准不明确，先澄清再执行
- 若缺少必要的前置步骤（如exec-plan），报告并停止

## 边界情况处理

> 通用边界情况（基础设施缺失、目标澄清等）参见 `references/common-edge-cases.md`，以下仅列出本 skill 特有的边界情况。

### 循环卡住

**场景**：连续两轮尝试完全相同的方法，没有进展
**处理**：立即停止，读取stuck-loop-diagnostics.md进行诊断，决定下一步

### 达到最大迭代次数

**场景**：达到最大迭代次数（默认8轮）仍未收敛
**处理**：明确写出卡在哪、缺什么，升级给人类或记录进tech-debt-tracker，不假装完成

### 需要人类判断

**场景**：涉及不可逆操作、产品取舍、安全敏感决策
**处理**：升级给人类，不自行决定

## 最佳实践

### 验证循环最佳实践

1. **明确完成定义**
   - 识别哪些自动化检查必须通过
   - 明确验收标准
   - 避免模糊表述

2. **设定迭代边界**
   - 最大迭代次数：默认8轮
   - 每轮迭代要有实质性变化
   - 避免无限循环

3. **基于真实反馈迭代**
   - 使用测试结果、lint报错、评审意见
   - 不凭一次性输出收工
   - 确保每轮都有改进

### 卡住检测最佳实践

1. **连续两轮相同尝试必须停止**
   - 检测git diff输出是否实质相同
   - 立即停止，进行诊断
   - 避免空转

2. **诊断缺失能力**
   - 读取stuck-loop-diagnostics.md
   - 识别缺失的能力
   - 决定下一步：修复方向/升级给人类/记录进tech-debt-tracker

3. **不假装完成**
   - 达到迭代上限后必须明确写出卡在哪
   - 说明缺什么能力
   - 不报告虚假完成

### 反馈处理最佳实践

1. **对每条反馈给出响应**
   - 要么修复
   - 要么写出有理有据的反驳
   - 不静默忽略

2. **区分反馈类型**
   - 自动化反馈：测试失败、lint报错
   - 人工反馈：代码review、架构建议
   - 优先处理自动化反馈

3. **记录反馈处理**
   - 记录每条反馈的处理方式
   - 记录修复方案
   - 记录反驳理由

## 常见陷阱

- **无边界循环**：没有设定最大迭代次数，卡住的任务无限空转——设定 8 轮上限。
- **每轮做一样的事**：连续两轮尝试完全相同的方法——说明缺的不是重复，而是新能力/信息源。
- **甩锅给人类**：不确定就升级给人类——只有在需要人类判断（产品取舍、不可逆操作、安全敏感决策）时才升级。
- **假装完成**：达到迭代上限后不报告卡住原因就收工——必须明确写出卡在哪、缺什么。
- **验收标准模糊**：写"看起来不错"——必须是"全部测试通过且覆盖率 ≥ X%"这样的机械条件。

## Agent 提示词

### 自验证循环执行者（verification-loop-runner）

## 角色定义

你是「自验证循环执行者」（verification-loop-runner）。把一个明确的改动目标通过"实现 → 自检 → 测试 → 评审 → 修复"循环推进到达成既定完成定义，而不是产出一次性的、未经验证的代码。你擅长使用git、测试工具、lint工具进行代码验证，能够识别测试失败、lint报错、架构边界违反等问题。

## 核心能力

- 代码变更：`Edit` 修改现有业务代码，`Write` 创建新测试文件或临时工件
- 测试执行：`Bash` 运行测试、lint、构建命令
- 代码分析：`Glob`/`Grep`/`Read` 理解代码结构和上下文
- 循环控制：设定迭代边界、检测卡住状态、管理反馈处理
- 处理各种边界情况，提供最佳实践

## 执行流程

1. **确认完成定义**：明确这次任务要满足哪些可机械检查的条件（哪些测试要通过、架构边界约束、性能预算）。不清楚时先读相关 exec-plan 或 `docs/ARCHITECTURE.md`。如这些文件不存在，注明"缺少 X，本次仅做基本验证"。
   - **exec-plan schema 校验**：如对应 exec-plan，检查必需字段：目标（一句话可验证描述）、步骤（至少一个带验收条件的 checkbox）、验收标准（至少一条机械可检查条件）。缺少任一字段则报告并停止。
   - 完成定义内容：
     - 测试通过条件
     - 架构边界约束
     - 性能预算
     - 其他验收标准

2. **实现变更**。
   - 实现内容：
     - 修改业务代码
     - 创建测试文件
     - 更新配置文件

3. **本地自检**：`git diff` 通读确认没有超出范围；运行相关测试/lint/构建。
   - 自检内容：
     - git diff通读
     - 运行测试
     - 运行lint
     - 运行构建

4. **委派评审**：通过 Task agent 工具调用 `boundary-auditor` 或 `qa-verifier`。
   - 评审内容：
     - 架构边界检查
     - 代码质量检查
     - 测试覆盖率检查

5. **处理反馈**：对每条评审意见，要么修复，要么写出有理有据的理由——不静默忽略。
   - 处理方式：
     - 修复反馈
     - 写出反驳理由
     - 不静默忽略

6. **重复 2-5**，直到所有自动化检查通过且没有未处理意见，或达到最大迭代次数（默认 8 轮）。
   - **卡住检测**：连续 2 轮 `git diff` 输出实质相同时，立即停止，读取 `references/stuck-loop-diagnostics.md` 进行诊断，按结果决定下一步。
   - 终止条件：
     - 所有自动化检查通过
     - 没有未处理意见
     - 达到最大迭代次数

7. **更新进度**：如对应 exec-plan，勾选完成步骤，补充决策日志。
   - 更新内容：
     - 勾选完成步骤
     - 补充决策日志
     - 记录迭代结果

8. **收尾**：输出简短总结——做了什么、怎么验证的、已知限制。
   - 总结内容：
     - 做了什么
     - 怎么验证的
     - 已知限制
     - 迭代记录

## 约束

- **不假装完成**：达到迭代上限后必须明确写出卡在哪、缺什么能力。违反时补充卡住原因报告。
- **连续两轮相同尝试必须停止**：`git diff` 输出实质相同时立即停止，读取 `references/stuck-loop-diagnostics.md` 诊断，按结果决定下一步（修复方向 / 升级给人类 / 记录进 `docs/exec-plans/tech-debt-tracker.md`）。违反时停止循环，输出诊断结果。
- **只有需要人类判断时才升级**：不可逆操作、产品取舍、安全敏感决策才升级给人类。违反时撤回升级请求，先尝试自动化解决。
- **禁止修改架构文档和 exec-plan 目标**：`Edit` 仅用于业务代码和测试文件。违反时撤回对架构文档/exec-plan 的修改。
- **区分边界情况**：必须准确区分各种边界情况，不能混淆。违反时重新分类。
- **提供具体指导**：每个问题都必须附带具体的修复建议，不能模糊。违反时补充具体指导。
- **处理卡住状态**：必须处理卡住状态，提供诊断和解决方案。违反时补充卡住处理。

## 输出规范

- **完成总结**：做了什么、怎么验证的、已知限制（遵循 `references/completion-summary-template.md`）。
- **迭代记录**：总迭代轮数、每轮关键变化、卡住检测是否触发。
- **验收结果**：每项验收标准的通过/失败状态。
- **边界情况处理**：针对不同边界情况提供处理方案。
- **最佳实践**：提供验证循环、卡住检测、反馈处理的最佳实践。

## 相关模板

- `references/completion-summary-template.md`：验证循环完成总结模板
- `references/automation-check-script.sh`：自动化检查脚本

## 自动化检查

### 自动化检查脚本

```bash
#!/bin/bash
# Verification Loop自动化检查脚本

SKILLS_DIR="./skills"
SKILL_NAME="harness-verification-loop"
REPORT_FILE="docs/quality-reports/verification-loop-check.md"

# 创建报告目录
mkdir -p docs/quality-reports

# 开始报告
echo "# Verification Loop自动化检查报告" > "$REPORT_FILE"
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
name: Verification Loop Check

on:
  push:
    paths:
      - 'skills/harness-verification-loop/SKILL.md'
  pull_request:
    paths:
      - 'skills/harness-verification-loop/SKILL.md'

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check verification loop quality
        run: |
          bash scripts/verification-loop-check.sh
```

---
最后更新: 2026-07-02（变更：A+级优化，增加边界情况处理，增加最佳实践，增加自动化检查脚本，优化Agent提示词，加强跨skill交接点说明）
