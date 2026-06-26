---
name: harness-architecture-boundaries
description: 为由 agent 大量生成代码的仓库设计并机械化强制分层架构与依赖方向规则——通过自定义 linter 和结构化测试约束 agent,而不是依赖人工 code review 去"靠感觉"挡住架构腐化。当用户要为项目建立"严格边界、局部自由"的分层架构、代码已出现架构腐化或循环依赖或层间越界、需要设计自定义 lint 规则或定义跨层依赖方向时使用。
---

# Architecture Boundaries(架构边界)

## 核心原则:约束不变量,不要管实现细节

人来写代码的世界里,架构腐化是缓慢的、可以靠 code review 慢慢挡。Agent 高吞吐量生成代码的世界里,**任何没有被机械强制的约束,都会在很短时间内被违反**——不是因为 agent "学坏了",而是因为它会忠实地复制仓库里已经存在的模式,包括坏模式。

所以这里的方法论是:**在边界上下狠功夫,在边界内充分放权**。

- **要严格约束**:模块/领域之间的依赖方向、数据进入系统边界时的形态、跨层调用路径。
- **不要约束**:某个具体函数怎么写、用什么库实现细节、变量命名是否符合人类审美。

这类似于管理一个大型平台工程组织:中心化地守住边界、正确性、可复现性;边界内部,允许团队(或 agent)用自己的方式实现。agent 写出来的代码不一定符合人类的风格偏好,只要它正确、可维护、对下一轮 agent 可读,就达标。

## 何时使用

- 用户要为项目建立"严格边界、局部自由"的分层架构。
- 代码已出现架构腐化、循环依赖或层间越界。
- 需要设计自定义 lint 规则或定义跨层依赖方向。

## 推导项目自有的分层模型

不要直接照搬下面的示例。流程是:

1. 列出项目里的主要领域/模块。
2. 对每个领域,识别数据流向:从最底层的类型定义到最上层的用户界面。
3. 确定"哪些层可以互相依赖、哪些必须单向"。
4. 识别横切关注点(鉴权、日志、配置等),确定它们的合法入口。
5. 把上述结果编码为依赖方向规则。

## 一个典型的分层模型

以下是一个可参考的通用分层(不是必须照搬,但展示了"固定的依赖方向 + 单一的横切入口"这个模式):

```
每个业务领域内部,代码只能"向前"依赖,方向固定:

    Types → Config → Repo → Service → Runtime → UI

横切关注点(鉴权、连接器、遥测、特性开关)不允许散落进任意层,
必须通过一个显式的 Providers 接口进入:

    Providers → Service → Runtime → UI

不属于上面任何一层的工具函数放在 Utils,
Utils 只能被 Providers 使用,不能反向依赖业务领域内部。
```

关键不是这个具体的六层模型,而是这个模式:**固定方向 + 有限的合法边数 + 横切关注点收口到单一入口**。把它套用到你项目的实际领域划分上。

## "Parse, don't validate" 作为数据边界规则

要求:**任何外部数据进入系统边界时,必须被解析成强类型,而不是被校验后当作弱类型继续传递**。不规定具体用什么库实现(项目可以自由选择 schema 验证库),只规定这个不变量本身要被机械检查到——比如 lint 规则禁止在边界层直接使用未经解析的 `any`/`dict`/动态字典访问。

## 怎么把规则变成机械约束

1. **把检查交给 `boundary-auditor` agent 内联执行,而不是只写文档**。文档里的规则会被遗忘,agent 用 Grep/Bash 等工具直接检查依赖方向是否违规,不需要项目预先配置独立的 lint 工具链——agent 本身就能执行这些检查。如果项目已有现成的检查工具(ESLint、dependency-cruiser、import-linter 等),`boundary-auditor` 也会优先利用它们。检查模式模板见本技能 `references/check-pattern-template.md`。
- `references/boundary-auditor-prompt.md`: boundary-auditor agent 系统提示词
2. **写结构化测试(可选)**,在测试层面断言"领域 A 的模块不会出现在领域 B 的依赖图里",而不只是功能测试。这需要项目自行编写,不属于 agent 自动生成的范畴。
3. **把修复指令写进报错信息本身**。无论是由 agent 内联检查还是由外部工具检查,报错不要只说"违反规则 X",要写成"检测到 `service/foo.ts` 直接 import 了 `runtime/bar.ts` 的内部模块,违反 Service→Runtime 单向依赖规则;请改为通过 `service/foo.ts` 暴露的公共接口访问,或将共享逻辑下沉到 Types/Config 层"。这样发现问题的 agent 能直接照着修,不需要人介入解释。
4. **区分"必须挡住"和"建议但不强制"**。把真正的不变量交给 `boundary-auditor` 阻塞检查;把风格偏好做成 `harness-golden-principles` 技能里讲的"周期性清扫",不要混进阻塞合并的硬规则里,否则会拖慢吞吐量又不增加安全边际。

## 操作步骤

1. 和用户一起明确:这个仓库/领域的依赖方向应该是什么?横切关注点的合法入口是什么?
2. 把这些规则写进 `ARCHITECTURE.md`(模板见本技能 `references/architecture-template.md`)作为人类/agent 可读的地图。
3. 让 `boundary-auditor` agent 对照 `ARCHITECTURE.md` 中的规则执行检查(内联或利用项目已有的检查命令),确保每条规则都被机械验证,而不只是写在文档里。
4. 给每条检查发现配上"如何修复"的具体指令文本,让接手修复的 agent 能直接照着改。
5. 让 `boundary-auditor` 的检查成为 `harness-verification-loop` 自验证循环里的一步(每次改动后委派审计),而不是事后人工 review 才发现。
6. 定期(配合 `boundary-auditor` agent)审计:是否出现了新的、还没被规则覆盖的越界模式?如果有,补充新规则,而不是靠记忆/感觉去挡。

## 配合的 agent

- `boundary-auditor` agent:只读地运行这些 lint/结构化测试,产出带文件行号和修复建议的报告,不直接改代码。

## 相关模板

- `references/architecture-template.md`: ARCHITECTURE.md 架构文档模板
- `references/check-pattern-template.md`: 架构检查模式模板(boundary-auditor 参考)
- `references/boundary-auditor-prompt.md`: boundary-auditor agent 系统提示词

---
最后更新: 2026-06-26
