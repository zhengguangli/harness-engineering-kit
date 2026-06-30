# 架构检查模式(Check Pattern Template)

定义 `boundary-auditor` agent 如何内联检查每一条 `ARCHITECTURE.md` 中记录的架构规则。每条规则对应一个检查模式——描述"查什么、怎么查、违规长什么样"。

> 这不是可执行脚本,而是给 agent 参考的检查方法论——agent 用 `Grep`/`Bash`/`list_dir` 等工具组合内联执行这些检查。
>
> 语言可移植性提示：下面示例中的 import 检索模式以 TypeScript 为主。在不同语言栈中请使用对应语法（如 Python: `import ... from ...` / `import module`；Go: `"import"`；Java: `import ...;`；Rust: `use ...`）。

## 检查模式结构

每条规则的检查模式包含以下字段:

```
## 规则: <规则名称>

- **约束描述**: <一句话说清楚这条规则限制什么>
- **检查方式**: <agent 用什么工具组合来查,例如:Grep 搜索 import 语句、Glob 枚举文件>
- **违规特征**: <什么搜索命中/文件存在/结构缺失算违规>
- **修复方向**: <发现违规后,最小修复路径是什么>
```

## 示例 1:分层依赖方向检查

```
## 规则: Service 层不能直接 import Runtime 内部模块

- **约束描述**: Service 层的代码只能向前依赖 Types/Config/Repo 层,不能反向 import Runtime 层的内部模块。
- **检查方式**:
  1. 用 Glob 枚举 `src/**/service/` 下的所有源文件。
  2. 对每个文件,用 Grep 搜索 `import.*runtime` 和 `from.*runtime` 等模式。
  3. 排除合法的公共接口引用(如果 Runtime 层有明确的公共 API 文件,检查是否只 import 了公共入口)。
- **违规特征**: `src/<domain>/service/foo.ts` 中存在 `import { Bar } from '../../runtime/bar'`——指向 Runtime 内部模块的直接引用。
- **修复方向**: 改为通过 Runtime 层暴露的公共接口访问,或将共享逻辑下沉到 Types/Config 层。
```

## 示例 2:数据边界检查

```
## 规则: 外部数据进入系统边界时必须被解析为强类型

- **约束描述**: 所有跨边界的外部数据(API 响应、用户输入)必须在边界处被解析(parse),不允许校验(validate)后继续传递弱类型。
- **检查方式**:
  1. 用 Glob 枚举边界层文件(如 `src/<domain>/api/`、`src/<domain>/routes/`)。
  2. 对每个文件,用 Grep 搜索 `any` 类型标注、`as` 类型断言、直接访问 `response.data` 等模式。
  3. 检查是否存在"校验了字段存在就继续往下传原始对象"的模式(如 `if (data.field) { return data; }`)。
- **违规特征**: 边界层函数返回类型含 `any` 或 `unknown`;边界层直接传递未经解析的原始响应对象。
- **修复方向**: 在边界处使用类型守卫或 schema 解析库,将外部数据解析为明确类型后再向下传递。
```

## 示例 3:横切关注点入口检查

```
## 规则: 横切关注点(鉴权/日志/配置)必须通过 Providers 单入口进入各层

- **约束描述**: 鉴权、连接器、遥测、特性开关等横切关注点不能散落在任意业务层中,必须通过显式的 Providers 接口进入。
- **检查方式**:
  1. 用 Glob 枚举所有非 Providers 层的源文件。
  2. 用 Grep 搜索横切关注点的 import 语句(如 `import.*auth`、`import.*logger`、`import.*config`)。
  3. 排除合法的 Providers 层自身引用和工具函数引用。
- **违规特征**: `src/<domain>/service/foo.ts` 中直接 `import { auth } from '@/infra/auth'`——绕过了 Providers 入口。
- **修复方向**: 改为通过 Providers 注入,或确认该依赖确实不属于横切关注点后更新规则。
```

## 新增检查模式的流程

1. 从 ARCHITECTURE.md 中取出一条规则。
2. 按上面的模板结构定义检查模式——关键是把"怎么查"拆成 agent 可执行的 Grep/Glob/Bash 操作步骤。
3. 如果检查需要项目特定的上下文(如具体层名、目录路径),在检查模式中明确标注为占位符,由 agent 在审计时从 ARCHITECTURE.md 读取实际值。
4. 把修复方向写具体——不是"请遵守规则",而是"将 X 改为 Y,或移动到 Z 位置"。
