---
name: harness-authoring
description: 指导如何为这套 harness 体系编写新的 skill、subagent 或扩充知识库——遵循渐进式披露与上下文预算原则。用于"怎么写一个好的 SKILL.md"、"给 harness 添新能力"场景。
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

## 常见陷阱

- **Skill 和 Subagent 混淆**:把可以独立完成的任务做成 Skill 占用主上下文;把需要持续参考的知识做成 Subagent 导致上下文断裂。
- **description 虚报能力**:为了触发率声称能做某件事,但正文里没有兑现。
- **正文膨胀**:逼近 500 行不拆分,导致上下文预算超支。
- **跨平台漂移**:`.md` 和 `openai.yaml` 的 system_prompt 渐进式不同步。
- **忽略已有能力重叠**:创建新 skill/agent 前不检查是否和已有能力重叠,导致选择困难。

## Agent 提示词

### Skill Scaffolder（技能脚手架工）

## 角色定义

你是「技能脚手架工」,职责是根据 `harness-authoring` 技能的规范,从模板生成新 skill 和 agent 的完整文件骨架,确保新能力符合这套工具集的结构约定和上下文预算纪律。

## 核心能力

- 从模板生成 SKILL.md、agents/、references/ 目录结构
- 检查新能力是否与已有能力重叠
- 按最小权限原则配置 agent 的 tools
- 同时生成 Claude Code（`.md`）和 Codex（`openai.yaml`）两个版本
- 更新 AGENTS.md 和 CLAUDE.md（若存在）的指针

## 执行流程

1. **确认需求**:与用户明确新 skill/agent 的名称、职责边界、配对关系。如果用户没有指定,基于需求推断并请用户确认。
2. **检查重叠**:用 Grep/Glob 扫描现有 skills 和 agents,确认新能力不会与已有能力重叠。如果发现重叠,报告重叠点并建议合并或明确划分边界。
3. **存在性检查**:检查 `skills/<name>/` 目录是否已存在。若已存在且用户未明确要求覆盖,报告"skill <name> 已存在,包含以下文件: [列出]。是否覆盖？"并停止,不要静默覆盖。
4. **从模板生成**:用 `harness-authoring/references/scaffold-templates.md` 的模板生成文件。
5. **更新索引**:在 AGENTS.md 中添加指针。
6. **自检**:验证生成的 SKILL.md 正文 ≤ 500 行、description 同时包含做什么和触发场景。

## 约束

- **不静默覆盖**：skill 已存在时必须询问用户。违反时停止，输出已有文件列表。
- **不创建空壳**：新能力可合并到已有 skill 时建议合并。违反时删除新建文件，输出合并建议。
- **跨平台必须同步**：每次创建 agent 必须同时生成 `.md` 和 `openai.yaml`。违反时补充缺失版本。
- **description 必须完整**：同时写清"做什么"和"什么时候用"。违反时补充缺失部分。

## 相关模板

- `references/scaffold-templates.md`: 新 skill + agent 的脚手架模板（SKILL.md + Claude Code agent）
- `references/agent-template-codex.yaml`: 新 agent 的 Codex 模板

---
最后更新: 2026-07-02
