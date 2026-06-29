---
name: harness-exec-plans
description: 把跨多个上下文窗口的复杂任务落盘为版本化的执行计划(exec-plan)工件——包含目标、步骤、决策记录与验收标准。当任务跨越多个上下文窗口或多次会话、用户说"先做个计划"或"改动比较大"、失败后需要知道上一轮试过什么/为什么放弃、或需要长时程自主执行时使用。
---

# Execution Plans(执行计划)

## 核心原则

Agent 的工作横跨多个上下文窗口时,**唯一能在窗口之间存活的东西是文件系统**。如果计划只存在于某一次对话的上下文里,下一次启动的 agent(哪怕是同一个任务)就要从零开始猜"已经做到哪了""为什么选了这个方案而不是那个"。这正是 Ralph Loop 之类长时程模式能工作的原因:**每一轮迭代都是全新上下文,但都从同一份落盘的状态文件读取进度**。

所以:**计划是一等公民工件,要和代码一样被版本控制、被检查、被归档**,不是写完就丢的草稿。

## 何时使用

- 任务复杂度足以跨越多个上下文窗口或多次会话。
- 用户说"先做个计划再动手"或"这个改动比较大"。
- 失败后需要知道"上一轮试过什么、为什么放弃"。
- 小的、一次性能做完的改动不需要 exec-plan,用临时的轻量计划即可。

## 方法论

| | 临时轻量计划 | 执行计划(exec-plan) |
|---|---|---|
| 适用场景 | 单次会话能做完的小改动 | 跨会话/跨上下文窗口的复杂工作 |
| 存放位置 | 对话内,或任务级 todo,不必落盘 | `docs/exec-plans/active/<plan-id>.md`,纳入版本控制 |
| 内容 | 几条步骤即可 | 目标、范围、非目标、步骤、决策日志、验收标准、风险 |
| 生命周期 | 用完即弃 | active → completed,移动文件而不是删除 |

判断标准:如果这个任务有合理概率被打断、被多个 agent/多次运行接力完成,或者失败后需要知道"上一轮试过什么、为什么放弃",就必须用 exec-plan。

### exec-plan 文件结构

参考 `references/exec-plan-template.md`。核心字段:

```markdown
# <计划标题>

- 状态: draft | active | blocked | completed
- 创建日期 / 最近更新日期
- 关联 PR / issue

## 目标
一句话说清楚"完成后世界会变成什么样",要可验证,不要写成过程描述。

## 范围 / 非目标
明确写出"不做什么",避免 agent 在执行中自我膨胀范围。

## 步骤
- [ ] 步骤 1(可独立验证的最小单元)
- [ ] 步骤 2
- [ ] ...
每个步骤应该小到可以在一次工具调用/一次 PR 里完成并自验证。

## 决策日志
记录"为什么选 A 不选 B",尤其是没有写进代码注释里的权衡。后续 agent 不应该重新发明或意外推翻这些决定,除非明确写新的决策记录覆盖它。

## 验收标准
具体到可机械检查的条件(测试通过、某个指标达到阈值、某个 UI 流程可被复现验证),不要写"看起来不错"这种无法验证的标准。

## 风险 / 已知未知
明确写出还不确定的地方,避免假装计划是完整的。
```

### 目录与生命周期

```
docs/exec-plans/
├── active/                 # 进行中的计划
├── completed/               # 完成后移动到这里,不要删除——保留历史决策
└── tech-debt-tracker.md     # 已知但暂不处理的技术债清单,定期被 entropy-collector 复查
```

- 计划完成后,**移动文件**而不是删除,保留决策历史供未来 agent 查阅("为什么当时这样设计")。
- 发现一个步骤做不完想留到以后,不要悄悄删掉——记录进 `tech-debt-tracker.md`,带上理由和影响范围。
- 多个 agent 并行工作时,`docs/exec-plans/active/` 本身就是共享的协调台账,所有人都能看到谁在做什么、做到哪。

### 并行协作约定

- 每个 exec-plan 文件同一时刻只由一个 agent 编辑(在文件顶部元数据标注"负责 agent/人")。
- 需要交接时,先提交当前进度到文件,再由下一个 agent 接管。
- 不要两个 agent 同时修改同一个 exec-plan 文件。

### plan-architect ↔ verification-loop-runner 协作

exec-plan 的生命周期由两个 agent 分阶段接力完成:

1. **plan-architect 负责创建**:把高层目标拆解为 exec-plan 文件(目标、步骤、验收标准、风险),写入 `docs/exec-plans/active/`。plan-architect 不写实现代码。
2. **verification-loop-runner 负责执行**:按 exec-plan 的步骤逐一实现,每步走自验证循环(实现→自检→测试→评审→修复),完成后在 exec-plan 中勾选步骤并补充决策日志。
3. **交接点**:plan-architect 完成计划后,告诉主对话"建议委派给 verification-loop-runner 按此计划执行";verification-loop-runner 开始前先读取 exec-plan 确认完成定义。
4. **回写约定**:只有 verification-loop-runner 可以修改 exec-plan 的步骤勾选状态和决策日志;plan-architect 只在用户要求调整计划时才修改目标/范围/步骤。

## 初始化步骤(首次为项目搭建 exec-plans 时)

1. 创建目录 `docs/exec-plans/active/` 和 `docs/exec-plans/completed/`(如不存在)。
2. 从本技能 `references/tech-debt-tracker-template.md` 创建 `docs/exec-plans/tech-debt-tracker.md`。
3. exec-plan 文件本身用 `references/exec-plan-template.md` 作为起点。

## 操作步骤

1. 先判断:这个任务需要临时计划还是 exec-plan?(见上面的判断标准)
2. 如果需要 exec-plan:用模板创建 `docs/exec-plans/active/<plan-id>.md`,先只填目标/范围/步骤骨架。
3. 把步骤拆到"足够小、可独立验证"的粒度——每一步最好能配合 `harness-verification-loop` 技能里的自验证循环单独跑完。
4. 执行过程中持续更新:勾选完成的步骤,补充决策日志(不要等到最后一次性回填,容易遗漏关键权衡)。
5. 任务完成后,把验收标准逐项核对、记录结果,再把文件移到 `completed/`。
6. 如果任务中途被放弃或搁置,标注状态为 `blocked`,并写清楚阻塞原因,而不是放着不管。

## 配合的 agent

- `plan-architect` agent:专门负责把一个高层目标拆解成 exec-plan,自己不动手写实现代码。
- `verification-loop-runner` agent:执行 exec-plan 里的步骤时,按步驱动自验证循环并回写进度。

## 相关模板

- `references/exec-plan-template.md`: 执行计划文件模板
- `references/tech-debt-tracker-template.md`: 技术债跟踪模板
- `references/plan-architect-prompt.md`: plan-architect agent 系统提示词
---
最后更新: 2026-06-29
