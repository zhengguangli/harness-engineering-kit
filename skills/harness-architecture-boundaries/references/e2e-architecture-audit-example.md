# 端到端示例：Node.js 电商平台架构边界审计

## 场景背景

一个中型 Node.js 电商平台，代码量约 5 万行，团队 8 人。近期出现以下问题：
- `OrderService` 直接 `require` 了 `UserRepository`（层间越界）
- 认证逻辑散落在 3 个不同的 Service 里（横切关注点未收口）
- 一个循环依赖导致启动时偶发 crash

目标：建立分层架构规则，通过机械化检查防止问题复发。

---

## 步骤 1：分析项目现状

**输入**：项目代码目录

**操作**：

```bash
# 列出顶层目录结构
ls src/

# 识别主要模块
find src -maxdepth 2 -type d | head -30
```

**输出**：
```
src/
├── types/          # TypeScript 类型定义
├── config/         # 配置管理
├── repositories/   # 数据访问层
├── services/       # 业务逻辑层
├── controllers/    # 控制器层
├── routes/         # 路由层
├── middleware/     # 中间件（认证、日志等）
└── utils/          # 工具函数
```

**发现**：
- 项目有清晰的 6 层结构
- `middleware/` 目录存在但未被统一引用
- `utils/` 里混入了业务逻辑

---

## 步骤 2：识别依赖方向

**输入**：项目目录结构

**操作**：

```bash
# 检查当前依赖方向（搜索 import/require 语句）
rg "require\(|from ['\"]" src/ --no-filename | sort | uniq -c | sort -rn | head -20

# 检查跨层依赖
rg "require.*repositories" src/services/  # Service 是否直接引用 Repository
rg "require.*services" src/routes/        # Route 是否直接引用 Service
```

**输出**：
```
# 发现违规：
src/services/OrderService.ts:1  const userRepo = require('../repositories/UserRepository')
src/services/PaymentService.ts:1  const { verifyToken } = require('../middleware/auth')
src/controllers/UserController.ts:1  const { db } = require('../repositories')
```

**识别的依赖方向**：
```
types → config → repositories → services → controllers → routes
```

**横切关注点**：`middleware/`（认证、日志、错误处理）

---

## 步骤 3：定义架构规则

**输入**：步骤 1-2 的分析结果

**操作**：与用户确认以下规则

```markdown
## 依赖方向规则

### 正向依赖（必须单向）
types → config → repositories → services → controllers → routes

### 横切关注点入口
middleware/ 只能被 routes/ 引用，不能被 services/ 或 controllers/ 直接引用。

### 禁止的依赖
- services/ 不能直接 import repositories/ 的实现（必须通过接口）
- controllers/ 不能直接 import repositories/（必须经过 services/）
- 任何层不能反向依赖上层
```

**输出**：写入 `docs/ARCHITECTURE.md`

---

## 步骤 4：生成检查规则

**输入**：步骤 3 的架构规则

**操作**：boundary-auditor agent 内联执行检查

```bash
# 检查 1：Service 层直接引用 Repository
rg "require.*repositories|from.*repositories" src/services/

# 检查 2：Controller 层直接引用 Repository
rg "require.*repositories|from.*repositories" src/controllers/

# 检查 3：横切关注点散落
rg "require.*middleware|from.*middleware" src/services/ src/controllers/

# 检查 4：循环依赖检测
# 使用 madge 或手动检查 import 链
npx madge --circular src/
```

---

## 步骤 5：执行审计并生成报告

**输入**：步骤 4 的检查结果

**输出**：

```markdown
## 架构边界审计报告

### 总结
- 违规总数：5
- CRITICAL：1
- HIGH：3
- MEDIUM：1
- LOW：0
- 建议：阻塞合并（存在 CRITICAL 级别循环依赖）

### 详细发现

### [CRITICAL] 循环依赖导致启动 crash
- 文件: `src/services/OrderService.ts`, 行号: L1-L5
- 违反规则: 依赖方向必须单向，不能存在循环
- 影响: 导致模块加载顺序不确定，偶发启动 crash
- 建议修复:
  1. 将 `OrderService` 对 `UserService` 的依赖提取为接口
  2. 使用依赖注入替代直接 require
  ```typescript
  // Before
  const UserService = require('./UserService');

  // After
  interface UserServiceInterface {
    getUser(id: string): User;
  }
  constructor(private userService: UserServiceInterface) {}
  ```

### [HIGH] Service 层直接引用 Repository 实现
- 文件: `src/services/OrderService.ts`, 行号: L1
- 违反规则: services/ 不能直接 import repositories/ 的实现
- 影响: 违反分层架构，Service 与数据访问层耦合
- 建议修复:
  1. 在 `src/types/` 中定义 `UserRepositoryInterface`
  2. 通过依赖注入传入 Repository 实例
  ```typescript
  // Before
  const userRepo = require('../repositories/UserRepository');

  // After (在构造函数中注入)
  constructor(private userRepo: UserRepositoryInterface) {}
  ```

### [HIGH] 横切关注点散落进 Service 层
- 文件: `src/services/PaymentService.ts`, 行号: L1
- 违反规则: middleware/ 只能被 routes/ 引用
- 影响: 认证逻辑与业务逻辑耦合，无法统一管理
- 建议修复:
  1. 移除 `PaymentService` 中的 `verifyToken` 调用
  2. 将认证检查移到 `routes/payment.ts` 的中间件链中
  ```typescript
  // routes/payment.ts
  router.post('/pay', authMiddleware, PaymentController.pay);
  ```

### [HIGH] Controller 层直接引用 Repository
- 文件: `src/controllers/UserController.ts`, 行号: L1
- 违反规则: controllers/ 不能直接 import repositories/
- 影响: 跳过业务逻辑层，直接操作数据
- 建议修复:
  1. 将数据操作逻辑移入 `UserService`
  2. Controller 只调用 Service 方法
  ```typescript
  // Before
  const { db } = require('../repositories');

  // After
  const user = await this.userService.getUser(id);
  ```

### [MEDIUM] utils/ 混入业务逻辑
- 文件: `src/utils/validation.ts`, 行号: L10-L25
- 违反规则: utils/ 只能包含通用工具函数
- 影响: 工具函数与业务耦合，难以复用
- 建议修复:
  1. 将 `validateOrder` 移入 `src/services/OrderService`
  2. utils/ 只保留纯工具函数（如日期格式化、字符串处理）
```

---

## 步骤 6：集成到验证循环

**输入**：步骤 5 的审计报告

**操作**：将检查集成到 `harness-verification-loop`

```yaml
# 在 verification-loop 配置中添加
verification_steps:
  - name: architecture-boundaries-check
    command: |
      # 由 boundary-auditor agent 内联执行
      # 检查依赖方向、循环依赖、横切关注点
    blocking: true  # CRITICAL/HIGH 违规阻塞合并
```

---

## 步骤 7：定期审计

**频率**：每月一次 / 重大重构后

**操作**：
```bash
# 运行边界检查
# boundary-auditor agent 执行步骤 4 的检查
# 对比上次审计结果，识别新增违规
```

---

## 错误处理

### 场景 1：ARCHITECTURE.md 不存在
**处理**：boundary-auditor 报告"架构规则未被文档化"，建议先用 `harness-architecture-boundaries` 技能补上，再基于代码现状做合理推断。

### 场景 2：规则定义模糊导致无法判断
**处理**：boundary-auditor 将"规则需要被更精确地编码"作为发现项报告，不自行放宽规则。

### 场景 3：修复建议不可执行
**处理**：boundary-auditor 补充具体修复方向，包括代码示例和操作步骤。

---

## 验收标准

- [ ] `docs/ARCHITECTURE.md` 包含完整的分层模型和依赖方向规则
- [ ] boundary-auditor 能识别所有 CRITICAL/HIGH 违规
- [ ] 每个违规都附带可执行的修复建议
- [ ] 循环依赖被消除（`npx madge --circular src/` 无输出）
- [ ] 横切关注点统一通过 middleware/ 入口
