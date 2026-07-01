---
name: harness-architecture-boundaries
description: 为 agent 大量生成代码的仓库设计分层架构与依赖方向规则——通过自定义 linter 和结构化测试机械化强制约束。当用户要建立分层架构、出现循环依赖或层间越界、需要设计自定义 lint 规则时使用。
version: 0.1.0
---
# Architecture Boundaries（架构边界）

## 触发信号

### 显式触发（explicit）
- `harness-architecture-boundaries`
- `architecture boundaries`
- `architecture-boundaries`

### 语义意图（intent）
- 用户要建立分层架构与依赖方向规则
- 出现循环依赖、层间越界或架构腐化
- 需要自定义 lint 规则或结构化架构测试
- 想让架构约束被机械强制而非仅靠 review

### 证据触发（artifacts）
- `docs/ARCHITECTURE.md`
- `boundary-auditor`
- `lint`
- `import` / `dependency`
- `test`

### 避免触发（avoid_when）
- 纯风格偏好（交给 `harness-golden-principles`）
- 项目规模极小、无明显分层需求

## 核心原则

- **边界内放权,边界上狠功夫**:在模块间依赖方向、数据边界形态、跨层调用路径上严格约束;在具体实现细节上充分放权。
- **机械强制优于人工审查**:Agent 高吞吐量生成代码的世界里,任何没有被机械强制的约束都会在短时间内被违反——不是因为 agent "学坏了",而是因为它会忠实复制仓库里已存在的坏模式。
- **固定方向 + 有限合法边 + 横切入口收口**:这是分层架构的核心模式——固定依赖方向、限制合法的依赖边数、横切关注点通过单一入口进入。

## 何时使用

- 用户要为项目建立"严格边界、局部自由"的分层架构
- 代码已出现架构腐化、循环依赖或层间越界
- 需要设计自定义 lint 规则或定义跨层依赖方向

## 何时不该用

- 纯风格偏好类问题（交给 `harness-golden-principles`）
- 项目规模极小、模块间无明显分层需求
- 用户明确表示不需要架构约束

## 方法论

### 1. 推导项目自有的分层模型

不要照搬示例。流程:

1. 列出项目里的主要领域/模块
2. 对每个领域,识别数据流向:从最底层的类型定义到最上层的用户界面
3. 确定"哪些层可以互相依赖、哪些必须单向"
4. 识别横切关注点(鉴权、日志、配置等),确定它们的合法入口
5. 把上述结果编码为依赖方向规则

### 2. 典型分层模型参考

```
每个业务领域内部,代码只能"向前"依赖,方向固定:

    Types → Config → Repo → Service → Runtime → UI

横切关注点(鉴权、连接器、遥测、特性开关)不允许散落进任意层,
必须通过一个显式的 Providers 接口进入:

    Providers → Service → Runtime → UI

不属于上面任何一层的工具函数放在 Utils,
Utils 只能被 Providers 使用,不能反向依赖业务领域内部。
```

关键不是这个具体的六层模型,而是模式:**固定方向 + 有限的合法边数 + 横切关注点收口到单一入口**。

### 3. "Parse, don't validate" 作为数据边界规则

要求:**任何外部数据进入系统边界时,必须被解析成强类型,而不是被校验后当作弱类型继续传递**。不规定具体用什么库实现,只规定这个不变量要被机械检查——比如 lint 规则禁止在边界层直接使用未经解析的 `any`/`dict`/动态字典访问。

### 4. 执行步骤

1. 和用户一起明确:这个仓库/领域的依赖方向应该是什么?横切关注点的合法入口是什么?
2. 把规则写进 `docs/ARCHITECTURE.md`（模板见 `references/architecture-template.md`）
3. 把检查交给 `boundary-auditor` agent 内联执行——agent 用 Grep/Bash 等工具直接检查依赖方向是否违规,不需要项目预先配置独立的 lint 工具链
4. 给每条检查发现配上"如何修复"的具体指令文本
5. 区分"必须挡住"和"建议但不强制":真正的不变量交给 `boundary-auditor` 阻塞检查;风格偏好交给 `harness-golden-principles` 周期性清扫
6. 让 `boundary-auditor` 的检查成为 `harness-verification-loop` 自验证循环里的一步
7. 定期审计:是否出现了新的越界模式?补充新规则

## 关键要点

- **约束不变量,不管实现细节**:要严格约束模块间依赖方向和数据边界形态;不要约束具体函数写法、库选择、变量命名。
- **报错要有修复指引**:违反规则的报错不要只说"违反规则 X",要写成具体的修复指引。
- **区分数不变量和风格偏好**:真正的不变量阻塞检查;风格偏好周期性清扫。

## 常见陷阱

- **照搬分层模型**:不同项目的领域划分和依赖方向应该不同,不要盲目套用六层模型。
- **只检查不给修复建议**:报错没有修复指引会导致 agent 或人类无从下手。
- **忽略横切关注点收口**:鉴权、日志、配置散落进任意层会导致修改困难。
- **把风格偏好当不变量**:过度约束会降低 agent 效率,应该区分"必须挡住"和"建议但不强制"。

## 配合的 agent

- `boundary-auditor` agent:只读地运行 lint/结构化测试,产出带文件行号和修复建议的报告,不直接改代码。

## 相关模板

- `references/architecture-template.md`: ARCHITECTURE.md 架构文档模板
- `references/check-pattern-template.md`: 架构检查模式模板（boundary-auditor 参考）
- `agents/boundary-auditor.md`: boundary-auditor agent 系统提示词（canonical 版本）

---
最后更新: 2026-06-30
