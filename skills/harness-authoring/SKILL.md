---
name: harness-authoring
description: 指导如何为这套 harness 体系编写新的 skill、subagent 或扩充知识库——遵循渐进式披露与上下文预算原则。用于"怎么写一个好的 SKILL.md"、"给 harness 添新能力"、"这应该做成 skill 还是 subagent"、"给已有 skill 瘦身"场景。
when_to_use: |
  显式触发：用户要给 harness 工具集添加新能力、问"怎么写一个好的 SKILL.md"、问"这应该做成 skill 还是 subagent"、要求给已有 skill 瘦身。
  隐式触发：发现某个 agent/skill 内容越写越臃肿需要拆 references、新建能力前未检查与已有能力重叠。
  不触发：用户要创建与 harness 体系无关的独立工具、只想了解现有 skill 用法而非扩展体系、项目不使用 harness 方法论。
context: fork
agent: skill-scaffolder
compatibility: claude-code
allowed-tools: Bash(git *) Bash(grep *) Bash(rg *) Bash(find *) Bash(ls *) Bash(cat *) Bash(head *) Bash(wc *) Bash(echo *) Bash(date *)
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

**经验法则**:如果这件事需要主对话"记住"才能继续推理,用 skill;如果这件事可以"派出去、等结果",用 subagent。两者经常配对出现(一个 skill 定义方法论,一个同名 agent 负责执行),这不是重复,是分工。

### 2. 写 SKILL.md 的上下文预算纪律

三层加载机制:

1. **元数据(name + description)**:始终常驻上下文,约 100 词预算。要写得准确且"有推力"——让 agent 在恰当时机想起用它,又不能误触发。
2. **SKILL.md 正文**:技能触发时才进入上下文,控制在 500 行以内。
3. **绑定资源(references/、scripts/、assets/)**:按需加载,体量不受限制。

正文逼近 500 行就拆 `references/` 子文件,正文写清加载指引。

### 3. description 字段要"推",但不能假

- 同时写清楚**做什么**和**什么时候用**——"什么时候用"是触发主要依据。
- 用具体场景而不是抽象描述:"当用户说 A、B、C"比"用于代码质量相关任务"更容易被正确触发。
- 每一个声称的能力都要在正文里真正兑现,不为触发率虚报。

### 4. Subagent 的工具与权限纪律

- 只读型 agent 不给 `Edit`/`Write`,执行型 agent 才给。
- 用 `skills` 字段预加载相关技能,不在 system prompt 里重复技能正文——避免两处各维护一份迟早不同步。
- `model` 字段按"判断复杂度"选:高阶判断用强模型,机械化重复用轻量模型。

### 5. 对抗 context rot 的纪律

- 大工具输出落盘到文件,对话里只保留头尾摘要 + 文件路径。
- 复杂任务用 exec-plan 落盘状态,不依赖单次上下文窗口记进度。
- 5 条配具体后果的规则,优于 50 条规则堆砌。

### 6. 新增能力的执行步骤

1. 判断 skill 还是 subagent。
2. 写 description:先写"什么时候用",再写"做什么",确保能和已有能力区分。
3. 写正文,控制预算;预判膨胀,提前规划 `references/`。
4. subagent 按最小化工具授权列工具清单,说明 model 选择理由。
5. 检查与已有能力重叠——重叠则合并或划分边界。
6. 在 AGENTS.md/README 里登记新指针。
7. 自检:正文 ≤ 500 行?tools 最小权限?description 完整?

### 7. Agent 提示词 canonical 版本约定

- `SKILL.md` 的 `## Agent 提示词` 是 canonical 版本——改 prompt 只改此处。
- 不再使用独立的 `agents/<name>.md` 文件。

## 硬约束

1. **正文不得超过 500 行**：SKILL.md 正文（含 Agent 提示词）超过 500 行时必须拆分到 references/ 子文件。违反则打回要求拆分。
2. **description 必须同时写清"做什么"和"什么时候用"**：只写其一视为不完整。违反则补充缺失部分。
3. **新增 skill 前必须检查与已有能力重叠**：用 Grep/Glob 扫描现有 skills/，发现重叠时必须报告并建议合并或划分边界。违反则先完成重叠检查再继续。
4. **最小权限配置 agent tools**：只读型 agent 不给 Edit/Write，省略 tools 字段等于继承全部工具（非默认安全选项）。违反则重新按最小权限授权。

## 示例

**示例 1**：用户说"这应该做成 skill 还是 subagent"
**判断**：需要主对话持续参考的知识 → skill；可独立执行只返回结果 → subagent

**示例 2**：新 skill 与已有 harness-commit-gate 重叠
**处理**：合并或明确划分边界，不在两个相似选项间犯选择困难

## 关键要点

- **Skill 是知识,Subagent 是执行**:两者配对出现是分工,不是重复。
- **上下文预算纪律**:常驻内容精简,按需加载前置,正文 ≤ 500 行。
- **最小权限原则**:只读型 agent 不给写权限,省略 tools 不是默认安全选项。
- **三层加载机制**:元数据常驻→正文触发时载入→绑定资源按需加载。
- **description 必须真实**:每个声称的能力都要在正文里兑现。
- **避免能力重叠**:新增前检查已有能力,重叠则合并或划分边界。
- **canonical 版本**:`## Agent 提示词` 是唯一修改入口。

## 深入参考

- **Skill/Subagent 设计模式**：→ `references/skill-design-patterns.md`、`references/subagent-design-patterns.md`
- **上下文预算管理**：→ `references/context-budget-management-guide.md`

## 边界情况处理

> 通用边界情况参见 `references/common-edge-cases.md`，以下仅列出本 skill 特有的边界情况。

### skill和subagent混淆

**场景**：不确定应该做成skill还是subagent
**处理**：需要主对话"记住"才能继续推理 → skill；可以"派出去、等结果" → subagent

### 正文逼近500行

**场景**：SKILL.md正文逼近500行
**处理**：拆出references/子文件，正文写清楚加载指引

### 与已有能力重叠

**场景**：新skill/agent与已有能力重叠
**处理**：合并或明确划分边界，不让agent在相似选项间选择困难

### description虚报能力

**场景**：为触发率声称能力但正文未兑现
**处理**：每个声称能力都在正文里真正兑现

## 常见陷阱

- **Skill 和 Subagent 混淆**:把可以独立完成的任务做成 Skill 占用主上下文;把需要持续参考的知识做成 Subagent 导致上下文断裂。
- **description 虚报能力**:为了触发率声称能做某件事,但正文里没有兑现。
- **正文膨胀**:逼近 500 行不拆分,导致上下文预算超支。
- **忽略已有能力重叠**:创建新 skill/agent 前不检查是否和已有能力重叠,导致选择困难。

## 最佳实践

- 技能名称用 kebab-case，与目录名一致，便于 scripts 自动化遍历和引用。
- references/ 子文件的加载指引排在正文末尾、Agent 提示词之前，保证 agent 触发后先读到加载指引再读取执行流程。
- 新 skill 的 Agent 提示词先写跳过条件——如果跳过条件写清楚了，后面正文写错也不会导致误触发。
- 检查重叠时除了文件名扫描，再用 grep 搜索 `description` 字段中的动词短语，发现同义词组合即标记为潜在重叠。

## Agent 提示词

## Skill Scaffolder（技能脚手架工）

### 跳过条件

- **用户要创建与 harness 体系无关的独立工具**：不触发 skill-scaffolder。
- **用户只想了解现有 skill 用法而非扩展体系**：不触发，直接回答用法问题。
- **项目不使用 harness 方法论**：不触发。

### 角色定义

你是「技能脚手架工」，职责是根据 `harness-authoring` 技能的规范，从模板生成新 skill 和 agent 的完整文件骨架，确保新能力符合这套工具集的结构约定和上下文预算纪律。

### 核心能力

- 从模板生成 SKILL.md、references/ 目录结构
- 检查新能力是否与已有能力重叠
- 按最小权限原则配置 agent 的 tools
- 更新 AGENTS.md 指针

### 执行流程

1. **确认需求**：与用户明确新 skill/agent 的名称、职责边界、配对关系。未指定则推断并请确认。
2. **检查重叠**：用 Grep/Glob 扫描现有 skills/agents，发现重叠则报告并建议合并或划分边界。
3. **存在性检查**：`skills/<name>/` 已存在时询问用户是否覆盖，不静默覆盖。
4. **从模板生成**：用 `references/scaffold-templates.md` 生成 SKILL.md、references/。
5. **更新索引**：在 AGENTS.md 中添加指针。
6. **自检**：正文 ≤ 500 行、description 完整、Agent 提示词与 frontmatter agent 字段匹配、包含标准六段式子标题。

### 约束

- **不静默覆盖**：skill 已存在时必须询问用户。违反时要求用户先确认再继续。
- **不创建空壳**：可合并到已有 skill 时建议合并。违反时停止创建并给出合并建议。
- **description 必须完整**：同时写清"做什么"和"什么时候用"。违反时补充缺失部分。
- **控制上下文预算**：正文 ≤ 500 行，超出拆分到 references/ 子文件。违反时重新分配内容结构。
- **Agent 提示词 canonical 维护**：`## Agent 提示词` 是唯一修改入口。发现 `agents/<name>.md` 中有不同版本时，合并到 SKILL.md 后删除独立文件。违反时先合并再删除冗余版本。

### 输出规范

- **生成文件清单**：列出本次创建/修改的所有文件路径。
- **自检结果**：正文行数、description 内容、agent prompt 配对状态。
- **重叠检查结果**：发现重叠时输出合并/边界建议。

## 相关 Skill

- 上游 **harness-orchestration**: 接收产出物（编排决策）作为何时创建新 skill 的触发信号
- 下游 **所有其他 skill**: 本 skill 产出（新 skill 模板和规范）传递给下游作为搭建骨架

## 相关模板

- `references/scaffold-templates.md`：新 skill + agent 的脚手架模板

---
最后更新: 2026-07-03（变更：S1 关键要点/最佳实践去重）
