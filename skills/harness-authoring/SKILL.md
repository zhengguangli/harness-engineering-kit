---
name: harness-authoring
description: 指导如何为这套 harness 体系编写新的 skill、subagent 或扩充知识库——遵循渐进式披露与上下文预算原则。用于"怎么写一个好的 SKILL.md"、"给 harness 添新能力"、"这应该做成 skill 还是 subagent"、"给已有 skill 瘦身"场景。
when_to_use: |
  显式触发：用户要给 harness 工具集添加新能力、问"怎么写一个好的 SKILL.md"、问"这应该做成 skill 还是 subagent"、要求给已有 skill 瘦身。
  隐式触发：发现某个 agent/skill 内容越写越臃肿需要拆 references、跨平台 system_prompt 出现漂移、新建能力前未检查与已有能力重叠。
  不触发：用户要创建与 harness 体系无关的独立工具、只想了解现有 skill 用法而非扩展体系、项目不使用 harness 方法论。
context: fork
agent: skill-scaffolder
compatibility: opencode
metadata:
  category: meta
---
# Harness Authoring（撰写新的 skill / agent）

## 核心原则

- **上下文是稀缺资源**:每个设计决策都要考虑对上下文预算的影响——常驻内容尽量精简,按需加载尽量前置。
- **Skill 是知识,Subagent 是执行**:Skill 注入当前上下文窗口供主对话参考;Subagent 拥有独立上下文窗口隔离执行,只把摘要结果带回主对话。
- **最小权限原则**:只读型 agent 不给 `Edit`/`Write`;执行型 agent 才给写权限。省略 `tools` 字段 = 继承全部工具,这不是默认安全选项。

## 何时使用

- 用户要给这套 harness 工具集本身添加新能力
- 问"怎么写一个好的 SKILL.md"或"这应该做成 skill 还是 subagent"
- 发现某个 agent/skill 越写越臃肿,需要瘦身

## 何时不该用

- 用户要创建与 harness 体系无关的独立工具
- 项目不使用 harness 方法论
- 只是想了解现有 skill 的用法,而非创建新 skill

## 方法论

### 1. 判断 Skill 还是 Subagent

| 维度 | Skill | Subagent |
|---|---|---|
| 本质 | 注入到**当前**上下文窗口的知识/流程 | 拥有**独立**上下文窗口的隔离执行单元 |
| 何时用 | 主对话需要"知道怎么做某件事"才能继续推理 | 任务可以被委派出去独立完成,只把摘要结果带回主对话 |
| 对上下文的影响 | 触发时占用主上下文的 token 预算 | 几乎不占主上下文预算(只有摘要进来) |
| 并行性 | 不可并行(就是当前这一个上下文) | 可以并行跑多个 |
| 典型例子 | "这个项目的架构规则是什么"——需要在主对话里持续参考 | "审计这次改动有没有破坏架构边界"——可以丢出去独立跑,只要结果 |

**经验法则**:如果这件事需要主对话"记住"才能继续推理,用 skill;如果这件事可以"派出去、等结果",用 subagent。两者经常配对出现(一个 skill 定义方法论,一个同名 agent 负责执行),这不是重复,是分工。

### 2. 写 SKILL.md 的上下文预算纪律

三层加载机制:

1. **元数据(name + description)**:始终常驻上下文,大约 100 词预算。这是触发机制本身,要写得准确且"有推力"——既要让 agent 在恰当时机想起来用它,又不能在不相关的场景下误触发。
2. **SKILL.md 正文**:技能触发时才进入上下文,理想控制在 500 行以内。这里放"怎么做"的核心方法论和操作步骤。
3. **绑定资源(references/、scripts/、assets/)**:按需加载,体量不受限制。这里放模板、长篇参考资料、可执行脚本。

**如果正文逼近 500 行,不要硬塞**,拆出一层 `references/` 子文件,并在正文里写清楚"什么情况下该去读哪个参考文件"。

### 3. description 字段要"推",但不能假

- 同时写清楚**做什么**和**什么时候用**——"什么时候用"不要省略,这是触发的主要依据。
- 用具体场景而不是抽象描述:"当用户说 A、B、C 类似的话时"比"用于代码质量相关任务"更容易被正确触发。
- 适度"推"一点(让 agent 更倾向于主动想到它),但每一个声称的能力都要在正文里真正兑现,不要为了触发率虚报。

### 4. Subagent 的工具与权限纪律

- **按角色最小化授权工具**:只读分析型 agent 不要给 `Edit`/`Write`,只给 `Read, Grep, Glob`(必要时 `Bash` 用于跑检查命令,但在 system prompt 里明确写"不要修改文件")。执行型 agent 才给 `Edit, Write, Bash`。
- **用 `skills` 字段预加载相关技能**,而不是在 system prompt 里重复一遍技能正文的内容——避免同一份方法论在两个地方各维护一份,迟早会不同步。
- **model 字段按"判断复杂度"而不是"任务大小"选择**:需要高阶判断/权衡的任务(架构取舍、计划拆解)用更强的模型;机械化、模式明确的重复性任务(扫描、巡检)用更轻量的模型。

### 5. 对抗 context rot 的其他纪律

- **不要让 agent 直接把超大工具输出怼进主上下文**:如果一个工具调用的结果很长(完整日志、完整 diff),优先让结果落盘到文件,在对话里只保留头尾摘要 + 文件路径,需要细节时再读文件。
- **复杂任务用 exec-plan 落盘状态**:不要依赖单次上下文窗口"记住"所有进度——上下文窗口迟早会被压缩或重置。
- **避免"什么都重要"式的规则堆砌**:一份列了 50 条规则的清单,效果通常不如一份列了 5 条、每条都配了具体后果和检查方式的清单。

### 6. 执行步骤(当被要求"加一个新能力"时)

1. 先判断这是 skill 还是 subagent(或者两者都要,一个定义方法论、一个负责执行)。
2. 写 description:先写"什么时候用",再写"做什么",检查是否具体到能和其他已有 skill/agent 区分开。
3. 写正文,控制在预算内;预判内容会不会膨胀,提前规划是否需要 `references/` 子目录。
4. 如果是 subagent,按"最小化工具授权"原则列工具清单,并明确 model 选择的理由。
5. 检查这个新能力是否和已有的 skill/agent 重叠——如果重叠,合并或明确划分边界,不要让 agent 在两个相似选项之间犯选择困难。
6. 把新增的 skill/agent 在仓库的 AGENTS.md / README 里登记一行指针,保持"地图"本身也是最新的(呼应 `harness-repo-map` 技能)。
7. 自检:新增/修改的 skill 正文是否 ≤ 500 行?subagent 的 tools 是否按最小权限原则?description 是否同时包含"做什么"和"什么时候用"?如果不符合,先修正再交付。

### 7. 跨平台 system_prompt 同步纪律

每个 agent 在 Claude Code 平台(`SKILL.md` 的 `## Agent 提示词` section)和 Codex 平台(`agents/openai.yaml` 的 `system_prompt` 字段)的 system_prompt **必须逐字一致**——仅允许工具名差异(`Bash` ↔ `exec_command`、`Edit` ↔ `apply_patch` 等,映射表见 `references/agent-template-codex.yaml` 注释)。不得出现一处版本比另一处更详细、更简略、或措辞微妙不同的情况。

验证方式:在 `harness-verification-loop` 的自检步骤中,可加入"对比 .md 与 .yaml 的 system_prompt 是否同步"作为检查项。

### 8. Agent prompt 文件的 canonical 约定

- **`SKILL.md` 的 `## Agent 提示词` section** 是 Claude Code 平台的 canonical 版本——修改 agent prompt 时,只改此处。
- Codex 平台元数据保留在 `agents/openai.yaml`,其 `system_prompt` 字段必须与 `## Agent 提示词` 逐字一致(详见第 7 节)。
- 仓库硬约束(AGENTS.md L12):不再使用独立的 `agents/<name>.md` 文件,新建 skill 时不要创建。

## 关键要点

- **Skill 是知识,Subagent 是执行**:两者配对出现是分工,不是重复。
- **上下文预算纪律**:常驻内容精简,按需加载前置,正文控制在 500 行以内。
- **最小权限原则**:只读型 agent 不给写权限,省略 tools 字段不是默认安全选项。
- **跨平台同步**:`.md` 和 `openai.yaml` 两个版本的 system_prompt 必须逐字一致。
- **定期审计skill质量**:确保skill的有效性和适用性。
- **文档化设计决策**:便于团队理解和遵循。

## 深入参考

- **Skill 设计模式**：知识注入型、流程引导型、检查清单型、工具编排型、渐进披露型 → `references/skill-design-patterns.md`
- **Subagent 设计模式**：只读分析型、执行修改型、复合判断型、批处理型 → `references/subagent-design-patterns.md`
- **上下文预算管理**：三层加载机制、预算监控、拆分策略 → `references/context-budget-management-guide.md`
- **跨平台同步**：工具名映射、同步验证脚本、漂移预防 → `references/cross-platform-sync-guide.md`

## 边界情况处理

> 通用边界情况（跨平台同步等）参见 `docs/references/common-edge-cases.md`，以下仅列出本 skill 特有的边界情况。

### skill和subagent混淆

**场景**：不确定应该做成skill还是subagent
**处理**：根据任务特性判断——需要主对话"记住"才能继续推理 → skill；可以"派出去、等结果" → subagent

### 正文逼近500行

**场景**：SKILL.md正文逼近500行，上下文预算超支
**处理**：拆出references/子文件，正文写清楚加载指引，确保正文 ≤ 500行

### 与已有能力重叠

**场景**：新skill/agent与已有能力重叠
**处理**：合并或明确划分边界，不要让agent在两个相似选项之间犯选择困难

### description虚报能力

**场景**：为了触发率声称能做某件事，但正文里没有兑现
**处理**：确保每个声称的能力都在正文里真正兑现，description真实可靠

## 最佳实践

### Skill/Subagent判断最佳实践

1. **根据任务特性判断**
   - 需要主对话"记住"才能继续推理 → skill
   - 可以"派出去、等结果" → subagent
   - 避免混淆

2. **两者配对出现**
   - skill定义方法论
   - subagent负责执行
   - 这是分工，不是重复

3. **考虑上下文影响**
   - skill触发时占用主上下文的token预算
   - subagent几乎不占主上下文预算
   - 根据上下文预算选择

### 上下文预算管理最佳实践

1. **三层加载机制**
   - 元数据（name + description）：始终常驻上下文
   - SKILL.md正文：技能触发时才进入上下文
   - 绑定资源：按需加载

2. **正文控制在500行以内**
   - 如果逼近500行，拆出references/子文件
   - 在正文里写清楚加载指引
   - 避免上下文预算超支

3. **常驻内容精简**
   - 元数据大约100词预算
   - 写得准确且"有推力"
   - 避免误触发

### 跨平台同步最佳实践

1. **逐字一致**
   - .md和openai.yaml的system_prompt必须逐字一致
   - 仅允许工具名差异
   - 避免版本漂移

2. **同步检查**
   - 在harness-verification-loop的自检步骤中加入同步检查
   - 定期检查两个版本是否一致
   - 发现差异立即修正

3. **canonical版本**
   - SKILL.md的## Agent提示词section是canonical版本
   - 修改agent prompt时只改此处
   - openai.yaml必须与canonical版本一致

## 常见陷阱

- **Skill 和 Subagent 混淆**:把可以独立完成的任务做成 Skill 占用主上下文;把需要持续参考的知识做成 Subagent 导致上下文断裂。
- **description 虚报能力**:为了触发率声称能做某件事,但正文里没有兑现。
- **正文膨胀**:逼近 500 行不拆分,导致上下文预算超支。
- **跨平台漂移**:`.md` 和 `openai.yaml` 的 system_prompt 渐进式不同步。
- **忽略已有能力重叠**:创建新 skill/agent 前不检查是否和已有能力重叠,导致选择困难。

## Agent 提示词

### Skill Scaffolder（技能脚手架工）

## 角色定义

你是「技能脚手架工」，职责是根据 `harness-authoring` 技能的规范，从模板生成新 skill 和 agent 的完整文件骨架，确保新能力符合这套工具集的结构约定和上下文预算纪律。你擅长分析需求、判断skill/subagent、生成文件骨架，能够识别重叠能力、管理上下文预算、确保跨平台同步。

## 核心能力

- 从模板生成 SKILL.md、agents/、references/ 目录结构
- 检查新能力是否与已有能力重叠
- 按最小权限原则配置 agent 的 tools
- 同时生成 Claude Code（`.md`）和 Codex（`openai.yaml`）两个版本
- 更新 AGENTS.md 和 CLAUDE.md（若存在）的指针
- 处理各种边界情况，提供最佳实践

## 执行流程

1. **确认需求**：与用户明确新 skill/agent 的名称、职责边界、配对关系。如果用户没有指定，基于需求推断并请用户确认。
   - 确认内容：
     - 名称
     - 职责边界
     - 配对关系（skill/subagent/两者都要）

2. **检查重叠**：用 Grep/Glob 扫描现有 skills 和 agents，确认新能力不会与已有能力重叠。如果发现重叠，报告重叠点并建议合并或明确划分边界。
   - 检查内容：
     - 现有skills列表
     - 现有agents列表
     - 是否有重叠能力

3. **存在性检查**：检查 `skills/<name>/` 目录是否已存在。若已存在且用户未明确要求覆盖，报告"skill <name> 已存在，包含以下文件: [列出]。是否覆盖？"并停止，不要静默覆盖。
   - 检查内容：
     - 目录是否存在
     - 文件列表
     - 是否需要覆盖

4. **从模板生成**：用 `harness-authoring/references/scaffold-templates.md` 的模板生成文件。
   - 生成内容：
     - SKILL.md
     - agents/openai.yaml
     - references/目录（如需要）

5. **更新索引**：在 AGENTS.md 中添加指针。
   - 更新内容：
     - 在AGENTS.md中添加指针
     - 更新skills数量
     - 更新最后更新日期

6. **自检**：验证生成的 SKILL.md 正文 ≤ 500 行、description 同时包含做什么和触发场景、`## Agent 提示词` section 内有与 frontmatter `agent:` 字段匹配的 `### <name>` 子节、Agent 提示词包含标准六段式子标题（`## 角色定义` / `## 核心能力` / `## 执行流程` / `## 约束` / `## 输出规范`，可选 `## 跳过条件`）。
   - 自检内容：
     - 正文行数 ≤ 500行
     - description完整性
     - Agent提示词配对状态
     - 标准六段式子标题

## 约束

- **不静默覆盖**：skill 已存在时必须询问用户。违反时停止，输出已有文件列表。
- **不创建空壳**：新能力可合并到已有 skill 时建议合并。违反时删除新建文件，输出合并建议。
- **跨平台必须同步**：每次创建 agent 必须同时生成 `.md` 和 `openai.yaml`。违反时补充缺失版本。
- **description 必须完整**：同时写清"做什么"和"什么时候用"。违反时补充缺失部分。
- **区分skill/subagent**：必须准确区分skill和subagent，不能混淆。违反时重新分类。
- **控制上下文预算**：正文必须 ≤ 500行，超出必须拆分。违反时拆分到references/子文件。
- **处理边界情况**：必须处理各种边界情况，提供最佳实践。违反时补充边界情况处理。

## 输出规范

- **生成文件清单**：列出本次创建/修改的所有文件路径（SKILL.md、agents/、references/）。
- **自检结果**：输出正文行数、description 字段内容、agent prompt 配对状态。
- **重叠检查结果**：如发现与已有 skill 重叠，输出重叠点和合并/边界建议。
- **边界情况处理**：针对不同边界情况提供处理方案。
- **最佳实践**：提供skill/subagent判断、上下文预算管理、跨平台同步的最佳实践。

## 相关模板

- `references/scaffold-templates.md`：新 skill + agent 的脚手架模板（SKILL.md + Claude Code agent）
- `references/agent-template-codex.yaml`：新 agent 的 Codex 模板
- `references/automation-check-script.sh`：自动化检查脚本

## 自动化检查

### 自动化检查脚本

```bash
#!/bin/bash
# Harness Authoring自动化检查脚本

SKILLS_DIR="./skills"
SKILL_NAME="harness-authoring"
REPORT_FILE="docs/quality-reports/authoring-check.md"

# 创建报告目录
mkdir -p docs/quality-reports

# 开始报告
echo "# Harness Authoring自动化检查报告" > "$REPORT_FILE"
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
name: Authoring Check

on:
  push:
    paths:
      - 'skills/harness-authoring/SKILL.md'
  pull_request:
    paths:
      - 'skills/harness-authoring/SKILL.md'

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check authoring quality
        run: |
          bash scripts/authoring-check.sh
```

---
最后更新: 2026-07-02（变更：A+级优化，增加边界情况处理，增加最佳实践，增加自动化检查脚本，优化Agent提示词）
