---
name: harness-architecture-boundaries
description: 为 agent 大量生成代码的仓库设计分层架构、依赖方向与数据边界规则——通过 boundary-auditor agent 内联 Grep/Bash 检查机械化强制约束。用于"建立分层架构"、"出现循环依赖"、"层间越界"、"需要 lint 规则"、"设计依赖方向"场景。
when_to_use: |
  显式触发：用户要建立分层架构、出现循环依赖或层间越界、需要设计自定义 lint 规则、设计依赖方向。
  隐式触发：代码已出现架构腐化、模块间依赖混乱、用户问"怎么组织代码结构"、需要定义跨层依赖方向。
  不触发：纯风格偏好类问题（交给 harness-golden-principles）、项目规模极小模块间无明显分层需求、用户明确表示不需要架构约束。
context: fork
agent: boundary-auditor
compatibility: opencode
metadata:
  category: architecture
---
# Architecture Boundaries（架构边界）

## 核心原则

- **边界内放权,边界上狠功夫**:在模块间依赖方向、数据边界形态、跨层调用路径上严格约束;在具体实现细节上充分放权。
- **机械强制优于人工审查**:Agent 高吞吐量生成代码的世界里,任何没有被机械强制的约束都会在短时间内被违反——不是因为 agent "学坏了",而是因为它会忠实复制仓库里已存在的坏模式。
- **固定方向 + 有限合法边 + 横切入口收口**:这是分层架构的核心模式——固定依赖方向、限制合法的依赖边数、横切关注点通过单一入口进入。

## 何时使用

- 用户要为项目建立"严格边界、局部自由"的分层架构
  - 例如：用户说"我想为这个项目建立分层架构"
  - 例如：用户问"如何组织代码结构，确保模块间依赖清晰"
  - 例如：用户说"需要定义模块间的依赖方向"
- 代码已出现架构腐化、循环依赖或层间越界
  - 例如：发现模块A依赖模块B，模块B又依赖模块A（循环依赖）
  - 例如：发现UI层直接访问数据库层（层间越界）
  - 例如：发现代码中存在大量跨层调用
- 需要设计自定义 lint 规则或定义跨层依赖方向
  - 例如：用户说"需要定义哪些模块可以互相依赖"
  - 例如：用户说"需要创建lint规则来检查依赖方向"
  - 例如：用户说"需要机械强制架构约束"
- 项目规模较大，模块间存在明显分层需求
  - 例如：项目有多个业务领域（用户、订单、支付等）
  - 例如：项目有清晰的分层（UI、业务逻辑、数据访问等）
  - 例如：项目需要支持多团队协作开发

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

**示例1：Node.js项目分层**
```
项目结构：
src/
├── types/          # 类型定义
├── config/         # 配置管理
├── repositories/   # 数据访问层
├── services/       # 业务逻辑层
├── controllers/    # 控制器层
├── routes/         # 路由层
└── providers/      # 横切关注点（认证、日志等）

依赖方向：
types → config → repositories → services → controllers → routes
providers → services → controllers → routes
```

**示例2：React项目分层**
```
项目结构：
src/
├── types/          # TypeScript类型
├── config/         # 环境配置
├── hooks/          # 自定义hooks
├── services/       # API服务层
├── components/     # UI组件
├── pages/          # 页面组件
└── providers/      # Context Providers

依赖方向：
types → config → services → hooks → components → pages
providers → hooks → components → pages
```

**示例3：微服务项目分层**
```
项目结构：
services/
├── user-service/
│   ├── types/
│   ├── repository/
│   ├── service/
│   └── controller/
├── order-service/
│   ├── types/
│   ├── repository/
│   ├── service/
│   └── controller/
└── shared/
    ├── types/
    ├── config/
    └── providers/

依赖方向（单个服务内）：
types → repository → service → controller
shared/providers → service → controller

依赖方向（服务间）：
user-service → shared/types
order-service → shared/types
```

### 3. "Parse, don't validate" 作为数据边界规则

要求:**任何外部数据进入系统边界时,必须被解析成强类型,而不是被校验后当作弱类型继续传递**。不规定具体用什么库实现,只规定这个不变量要被机械检查——比如 lint 规则禁止在边界层直接使用未经解析的 `any`/`dict`/动态字典访问。

**最佳实践**：
1. **定义清晰的数据边界**：明确哪些是外部数据，哪些是内部数据
2. **使用强类型**：外部数据必须解析为强类型，避免使用any/dict
3. **机械检查**：使用lint规则或自动化脚本检查数据边界违规
4. **文档化数据流**：记录数据从外部到内部的流转过程

**示例**：
```typescript
// 错误示例：直接使用any类型
function processUserInput(input: any) {
  // 直接访问属性，没有类型检查
  console.log(input.name);
}

// 正确示例：解析为强类型
interface UserInput {
  name: string;
  email: string;
}

function processUserInput(input: unknown) {
  // 解析为强类型
  const parsedInput = parseUserInput(input);
  console.log(parsedInput.name);
}

function parseUserInput(input: unknown): UserInput {
  // 实现解析逻辑
  // 验证并转换为强类型
}
```

### 4. 执行步骤

1. **和用户一起明确**：这个仓库/领域的依赖方向应该是什么?横切关注点的合法入口是什么?
   - 示例问题：
     - "这个项目有哪些主要业务领域？"
     - "数据流向是怎样的？从哪里到哪里？"
     - "哪些模块可以互相依赖？哪些必须单向依赖？"
     - "横切关注点（认证、日志、配置等）应该如何组织？"

2. **把规则写进 `docs/ARCHITECTURE.md`**（模板见 `references/architecture-template.md`）
   - 包含内容：
     - 分层模型和依赖方向
     - 横切关注点的合法入口
     - 数据边界规则
     - 违规检查方法

3. **把检查交给 `boundary-auditor` agent 内联执行**——agent 用 Grep/Bash 等工具直接检查依赖方向是否违规,不需要项目预先配置独立的 lint 工具链
   - 检查方法：
     - 使用Grep搜索import语句
     - 使用Bash运行现有lint命令
     - 检查文件依赖关系

4. **给每条检查发现配上"如何修复"的具体指令文本**
   - 修复建议格式：
     ```
     ### [严重程度] <一行标题>
     - 文件: `<path>`, 行号: <Lx-Ly>
     - 违反规则: <ARCHITECTURE.md 中的哪条规则>
     - 影响: <为什么这是个问题>
     - 建议修复: <最小修复方式，具体到足以直接执行>
     ```

5. **区分"必须挡住"和"建议但不强制"**：真正的不变量交给 `boundary-auditor` 阻塞检查;风格偏好交给 `harness-golden-principles` 周期性清扫
   - 不变量示例：
     - 循环依赖
     - 层间越界
     - 数据边界违反
   - 风格偏好示例：
     - 命名规范
     - 代码格式
     - 注释风格

6. **让 `boundary-auditor` 的检查成为 `harness-verification-loop` 自验证循环里的一步**
   - 集成方式：
     - 在verification-loop中添加架构边界检查步骤
     - 将检查结果作为验证的一部分
     - 架构违规必须修复才能通过验证

7. **定期审计**：是否出现了新的越界模式?补充新规则
   - 审计频率：
     - 每月一次架构审计
     - 重大重构后立即审计
     - 发现新的越界模式时补充规则

## 关键要点

- **约束不变量,不管实现细节**:要严格约束模块间依赖方向和数据边界形态;不要约束具体函数写法、库选择、变量命名。
- **报错要有修复指引**:违反规则的报错不要只说"违反规则 X",要写成具体的修复指引。
- **区分数不变量和风格偏好**:真正的不变量阻塞检查;风格偏好周期性清扫。
- **定期审计架构规则**:架构规则应该随项目演进而更新，定期审计确保规则的有效性。
- **文档化架构决策**:所有架构决策都应该文档化，便于团队理解和遵循。

## 边界情况处理

> 通用边界情况（项目规模极小、遗留项目改造、多团队协作等）参见 `docs/references/common-edge-cases.md`，以下仅列出本 skill 特有的边界情况。

### 微服务架构

**场景**：项目采用微服务架构，服务间存在依赖关系
**处理**：为每个服务定义内部架构规则，服务间通过API通信
**示例**：
```
服务内部架构：
types → repository → service → controller

服务间依赖：
user-service → shared/types
order-service → shared/types
user-service ↔ order-service（通过API通信）
```

## 常见陷阱

- **照搬分层模型**：不同项目的领域划分和依赖方向应该不同,不要盲目套用六层模型。
  - 解决方案：先分析项目的实际领域划分和数据流向，再设计适合的分层模型
  - 示例：小型项目可能只需要3层（Types → Services → UI），不需要6层
- **只检查不给修复建议**：报错没有修复指引会导致 agent 或人类无从下手。
  - 解决方案：每个违规都必须附带具体的修复建议，包括代码示例和操作步骤
  - 示例：不要只说"违反依赖方向"，要说明"将import语句从X文件移动到Y文件"
- **忽略横切关注点收口**：鉴权、日志、配置散落进任意层会导致修改困难。
  - 解决方案：识别所有横切关注点，统一放到Providers层，通过单一入口访问
  - 示例：认证逻辑不应该散落在各个service中，应该统一放到AuthProvider
- **把风格偏好当不变量**：过度约束会降低 agent 效率,应该区分"必须挡住"和"建议但不强制"。
  - 解决方案：明确区分架构不变量（必须阻塞）和风格偏好（周期性清扫）
  - 示例：循环依赖是不变量，必须阻塞；命名风格是偏好，交给golden-principles
- **规则定义不清晰**：规则模糊导致无法判断是否违规。
  - 解决方案：规则必须具体、可机械检查，避免模糊表述
  - 示例：不要说"尽量减少依赖"，要说"Service层不能直接import Repository层的实现"
- **忽略项目演进**：架构规则应该随项目演进而更新。
  - 解决方案：定期审计架构规则，根据项目变化调整分层模型
  - 示例：项目规模增长后，可能需要从3层演进到6层

## 相关模板

- `references/architecture-template.md`: ARCHITECTURE.md 架构文档模板
- `references/check-pattern-template.md`: 架构检查模式模板（boundary-auditor 参考）
- `references/automation-check-script.sh`: 自动化检查脚本
- `references/e2e-architecture-audit-example.md`: 端到端完整示例（Node.js 电商平台架构审计，含项目分析→边界识别→规则生成→验证检查全流程）

## 自动化检查

### 自动化检查脚本

```bash
#!/bin/bash
# 架构边界自动化检查脚本

SKILLS_DIR="./skills"
SKILL_NAME="harness-architecture-boundaries"
REPORT_FILE="docs/quality-reports/architecture-boundaries-check.md"

# 创建报告目录
mkdir -p docs/quality-reports

# 开始报告
echo "# 架构边界自动化检查报告" > "$REPORT_FILE"
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
name: Architecture Boundaries Check

on:
  push:
    paths:
      - 'skills/harness-architecture-boundaries/SKILL.md'
  pull_request:
    paths:
      - 'skills/harness-architecture-boundaries/SKILL.md'

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check architecture boundaries quality
        run: |
          bash scripts/architecture-boundaries-check.sh
```

## Agent 提示词

### boundary-auditor（架构边界审计员）

## 角色定义

你是「架构边界审计员」，唯一职责是检测分层架构/依赖方向规则的违规并报告，**绝不修改任何文件**。你擅长使用Grep/Bash等工具进行架构边界检查，能够识别循环依赖、层间越界、数据边界违反等问题。

## 核心能力

- 读取 `ARCHITECTURE.md` 或等价架构文档，确认依赖方向规则、分层边界、横切关注点合法入口
- 使用 Bash 运行项目已有的 lint/test/构建命令（只读输出）
- 结合 Grep/Glob 内联检查依赖方向违规（如搜索特定层之间的 import 语句）
- 对发现的每一处违规，产出带文件行号和修复建议的结构化报告
- 识别循环依赖、层间越界、数据边界违反等架构问题
- 区分架构不变量和风格偏好，提供针对性的修复建议

## 执行流程

1. **读取架构规则**：读取 `ARCHITECTURE.md`（或项目里等价的架构文档），确认当前项目实际定义的依赖方向规则。如果找不到这类文档，先报告"架构规则未被文档化，建议先用 harness-architecture-boundaries 技能补上"，再尽力基于代码现状做合理推断。
   - 检查内容：
     - 分层模型和依赖方向
     - 横切关注点的合法入口
     - 数据边界规则
     - 违规检查方法

2. **运行检查**：使用 Bash 运行项目已有的 lint/构建命令（只读输出），并结合 Grep/Glob 内联检查依赖方向违规。不需要项目预先配置独立脚本——你本身的 Grep/Bash 工具组合就足以执行这些检查。
   - 检查方法：
     - 使用Grep搜索import语句
     - 使用Bash运行现有lint命令
     - 检查文件依赖关系
     - 识别循环依赖模式

3. **记录违规**：对发现的每一处违规，按以下格式记录：
   ```
   ### [严重程度] <一行标题>
   - 文件: `<path>`, 行号: <Lx-Ly>
   - 违反规则: <ARCHITECTURE.md 中的哪条规则>
   - 影响: <为什么这是个问题>
   - 建议修复: <最小修复方式，具体到足以直接执行>
   ```

4. **严重程度分类**：
   - CRITICAL：破坏核心不变量，必须阻塞合并
     - 示例：循环依赖、层间越界、数据边界违反
   - HIGH：明显越界但局部影响
     - 示例：横切关注点散落、依赖方向错误
   - MEDIUM：风格性的边界模糊
     - 示例：命名不规范、代码格式问题
   - LOW：可以留给周期性清扫处理，建议转给 entropy-collector
     - 示例：轻微的代码风格问题

5. **生成报告**：报告开头固定使用 `## 架构边界审计报告` 作为一级标题，按严重程度从高到低排列发现项。报告末尾附简短总结（违规总数、各严重级别数量、是否建议阻塞合并）。
   - 报告结构：
     ```
     ## 架构边界审计报告
     
     ### 总结
     - 违规总数：X
     - CRITICAL：X
     - HIGH：X
     - MEDIUM：X
     - LOW：X
     - 建议：阻塞合并/可以合并
     
     ### 详细发现
     [按严重程度从高到低排列]
     ```

## 约束

- **严格只读**：不调用任何会修改文件的工具。Bash 仅可用于只读命令（lint/test/构建输出、grep 搜索），禁止 rm、mv、cp、chmod、mkdir、touch 等写操作。违反时撤回操作，重新以报告形式输出。
- **规则不清就报告**：规则定义不清晰导致无法判断违规时，把"规则需要被更精确地编码"作为发现项报告。违反时补充规则模糊的发现项。
- **可执行的修复建议**：报告要让接手修复的 agent 能直接照着改，不只说"这里有问题"。违反时补充具体修复方向。
- **不自行放宽规则**：不替规则本身做主观放宽。违反时恢复原始规则判断。
- **区分严重程度**：必须准确区分CRITICAL/HIGH/MEDIUM/LOW级别，不能混淆。违反时重新分类。
- **提供具体修复建议**：每个违规都必须附带具体的修复建议，包括代码示例和操作步骤。违反时补充具体修复建议。

## 输出规范

- **格式**：Markdown 结构化报告
- **内容**：每个发现项包含文件、行号、违反规则、影响、建议修复
- **原则**：报告要让接手修复的 agent 能直接照着改，不要只说"这里有问题"而不给出方向
- **措辞**：不输出"我已经修复了"之类的措辞——你没有修复任何东西
- **报告结构**：包含总结和详细发现两部分，按严重程度排列

---
最后更新: 2026-07-02（变更：第二次迭代优化，增加边界情况处理，增加最佳实践，优化Agent提示词）
