---
name: harness-commit-gate
description: 提交代码前自动执行质量检查——diff 审查、测试/构建/lint 验证、commit message 格式化,通过才允许 commit。当用户说"提交代码"、"commit"、"git commit"、"代码提交"、"修复，提交代码"时使用。
version: 0.1.0
---
# Commit Gate（提交质量门）

## 触发信号

### 显式触发（explicit）
- `harness-commit-gate`
- `提交代码`
- `commit`
- `git commit`

### 语义意图（intent）
- 提交代码并执行质量门
- 先修问题再提交（修复，提交代码）
- 格式化 commit message 并本地提交
- 用户要求 agent 处理 commit 流程

### 证据触发（artifacts）
- `git status`
- `git diff --staged`
- `git add`
- `git commit`
- `test`
- `build`
- `lint`

### 避免触发（avoid_when）
- 已在 `verification-loop` 完成完整自检且已放行，不再重复门检
- 工作区无可提交变更（无 staged 文件）
- 任务是纯探索/分析，不产出可提交代码

## 核心原则

- **提交是"验证通过"的信号**:每次提交前都应经过一个轻量的质量门:检查改了什么、跑相关测试、格式化 commit message。通过才放行,不通过就修到通过。
- **检查优先于提交**:宁可多花 30 秒跑测试,也不要提交一个破坏构建的 commit。
- **Commit Message 是给未来看的**:写清楚"做了什么"和"为什么",不要写"fix bug"或"update"这种无信息量的 message。

## 何时使用

- 用户说"提交代码"、"代码提交"、"commit"
- 用户说"git commit"并期望 agent 自动处理
- 用户说"修复，提交代码"（先修再提交的组合指令）
- 代码变更完成后,需要进入提交流程

## 何时不该用

- 已经在 `verification-loop` 中完成了完整的"实现→自检→测试→评审→修复"循环且所有检查通过——gate 的检查已被循环覆盖,不要重复跑
- 工作区没有任何可提交的变更(无 staged 文件)——没有东西需要门检
- 任务是纯调研/分析,不产出代码变更——不需要提交质量门

## 方法论

### 1. 质量门的三道检查

1. **Diff 审查**:`git diff --staged` 通读变更,检查:
   - 是否有调试代码残留（console.log、print、TODO hack）
   - 是否有超出本次任务范围的变更（scope creep）
   - 是否有敏感信息泄露（API key、密码、token）
2. **自动化验证**:根据项目配置运行:
   - 测试: `bun test` / `npm test` / `vitest run` / `cargo test`
   - 构建: `bun run build` / `npm run build`
   - 类型检查: `tsc --noEmit` / `bunx tsc --noEmit`
   - Lint: 如有配置
3. **Commit Message 格式化**:按项目约定生成 message:
   - 如果项目有 conventional commits 习惯,遵循 `type(scope): description`
   - 否则用简洁的祈使句描述变更内容

### 2. 检查策略:按项目实际配置

不要硬编码所有检查命令。在运行前先探测项目使用什么工具:

1. 检查 `package.json` scripts → 找 test / build / lint 命令
2. 检查 `Makefile` / `Justfile` → 找对应 target
3. 检查 `Cargo.toml` → 用 `cargo test` / `cargo check`
4. 如果什么都没找到,只做 diff 审查 + commit

### 3. 何时跳过自动验证

- 项目没有任何测试或构建配置 → 只做 diff 审查
- 用户明确说"不要跑测试" → 跳过自动化验证
- 变更只涉及文档（.md 文件） → 只做 diff 审查 + commit

### 4. 执行步骤

1. **检查工作区状态**:`git status` 确认有哪些变更。
2. **Stage 变更**:如果用户没有手动 stage,`git add` 相关文件。
3. **Diff 审查**:`git diff --staged` 检查变更内容,如有问题先报告再决定是否继续。
4. **自动化验证**:探测项目工具链并运行测试/构建/lint。记录结果。
5. **生成 commit message**:基于变更内容和项目约定生成 message。
6. **执行 commit**:`git commit -m "<message>"`。
7. **确认结果**:输出 commit hash 和变更摘要。
8. **处理推送**:默认不推送。如果用户说"提交并推送",额外执行 `git push`;如果用户说"不推送"或"本次不推送",明确确认。用户未提及推送时,仅完成本地 commit。

## 关键要点

- **按项目实际配置检查**:不要硬编码所有检查命令,先探测项目使用什么工具。
- **不要静默跳过**:如果测试失败或构建失败,明确报告,不要假装通过。
- **Commit Message 规范**:使用英文、祈使语气、≤72 字符、不含无信息量词汇。
- **单个提交保持原子性**:一个提交只做一件事,便于 review 和 revert。

## 常见陷阱

- **硬编码检查命令**:不同项目使用不同的工具链,不要假设所有项目都用 npm。
- **静默跳过失败**:测试失败时假装通过,导致破坏构建的代码进入版本历史。
- **Commit Message 质量差**:写"fix bug"、"update"、"changes"这种无信息量的 message。
- **忽略 scope creep**:diff 审查时没有检查是否有超出本次任务范围的变更。
- **忘记检查敏感信息**:没有扫描 API key、密码、token 等敏感信息泄露。

## 配合的 agent

- `commit-gate-runner` agent:执行型 agent,负责跑质量门和提交。
- `verification-loop-runner` agent:如果质量门失败,可以联动 `harness-verification-loop` 进入修复循环。

## 相关模板

- `references/commit-message-guide.md`: Commit Message 格式指南

---
最后更新: 2026-06-30
