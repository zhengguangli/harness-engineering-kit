# Workflow 执行示例

## Workflow 1: Greenfield 初始化示例

**场景**：新创建的 Node.js/React 前端项目，需要初始化 harness 结构

```
用户说："帮我初始化这个项目的 harness"

1. project-intake → 分析 package.json → 识别 React+TypeScript+Vite
2. bootstrap → 生成 AGENTS.md（路由表） + docs/（ARCHITECTURE.md、QUALITY_SCORE.md）
3. repo-map → 校验：AGENTS.md ≤ 100 行？链接有效？
4. architecture-boundaries → 定义 3 层模型：Types → Components → Pages
   golden-principles → 注册 ESLint 规则和代码风格规范
```

**裁剪判断**：项目规模为"小型"，跳过 exec-plans/completed 目录，仅保留 active/。

---

## Workflow 2: 日常功能开发示例

**场景**：已有 harness 的项目需要添加"用户登录"功能

```
用户说："实现用户登录功能，后端 API + 前端页面"

1. exec-plans → 创建 auth-implementation.md
   - 目标：用户能用邮箱密码登录
   - 步骤：[POST /api/auth/login] [登录表单组件] [错误处理]
2. 实现 → agent 编写 API 路由 + React 组件
3. verification-loop → 实现→自检→测试→修复 循环
4. commit-gate → diff 审查 → 测试 → commit message 格式化
```

---

## Workflow 3: 代码质量修复示例

**场景**：现有代码出现大量 `any` 类型滥用

```
用户说："代码中太多 any 类型了，清理一下"

1. golden-principles → 注册"禁止使用 any"原则 → 扫描所有 .ts 文件
2. architecture-boundaries（可选）→ 若 any 出现在数据边界，补充 Parse 规则
3. verification-loop → 逐文件修复 → 类型检查通过
4. commit-gate → 原子提交
```

---

## Workflow 4: 扩展 harness 体系示例

**场景**：团队决定添加一个新的数据库迁移 skill

```
用户说："我想添加一个数据库迁移管理的 skill"

1. authoring → 新建 skills/harness-db-migration/
   - 判断：做 skill（方法论需要主对话参考）
   - description：写清"什么时候用"+"做什么"
   - 模板：按 scaffold-templates.md 生成
2. bootstrap（可选）→ 如涉及新的 docs/ 结构
3. repo-map → AGENTS.md 新增路由条目
```

---

## Workflow 5: Prompt 优化示例

**场景**：某个 skill 的 Agent 提示词效果不佳

```
用户说："优化一下 verification-loop 的 Agent 提示词"

1. prompt-optimizer → 读取 verification-loop SKILL.md
   - 分析现有提示词 → 五维评估（角色清晰度、执行链完整性等）
   - 重构 → 六区块模板重组
   - 输出 → 优化后的 ## Agent 提示词 section
```

---

## 跨流组合示例

**场景**：新项目需要初始化 harness，且已有的代码风格需要清理

```
用户说："新项目，先初始化 harness，再把现有代码风格统一一下"

跨流：Workflow 1 + Workflow 3

执行顺序：
1. project-intake（分析现有代码）
2. bootstrap（初始化骨架）
3. repo-map（校验）
4. golden-principles（注册风格规则 + 扫描）
5. commit-gate（提交）
```
