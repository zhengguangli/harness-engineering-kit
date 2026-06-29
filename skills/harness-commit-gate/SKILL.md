---
name: harness-commit-gate
description: 提交代码前自动执行质量检查——diff 审查、测试/构建/lint 验证、commit message 格式化,通过才允许 commit。当用户说"提交代码"、"commit"、"git commit"、"代码提交"、"修复，提交代码"时使用。
---

# Commit Gate（提交质量门）

## 核心原则

提交不是"写完代码"的信号,而是**"验证通过"的信号**。每次提交前都应经过一个轻量的质量门:检查改了什么、跑相关测试、格式化 commit message。通过才放行,不通过就修到通过。

## 何时使用

- 用户说"提交代码"、"代码提交"、"commit"。
- 用户说"git commit"并期望 agent 自动处理。
- 用户说"修复，提交代码"（先修再提交的组合指令）。
- 代码变更完成后,需要进入提交流程。

## 何时不该用

- 已经在 `verification-loop` 中完成了完整的"实现→自检→测试→评审→修复"循环且所有检查通过——gate 的检查已被循环覆盖,不要重复跑。
- 工作区没有任何可提交的变更(无 staged 文件)——没有东西需要门检。
- 任务是纯调研/分析,不产出代码变更——不需要提交质量门。

## 方法论

### 质量门的三道检查

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

### 检查策略:按项目实际配置

不要硬编码所有检查命令。在运行前先探测项目使用什么工具:

1. 检查 `package.json` scripts → 找 test / build / lint 命令
2. 检查 `Makefile` / `Justfile` → 找对应 target
3. 检查 `Cargo.toml` → 用 `cargo test` / `cargo check`
4. 如果什么都没找到,只做 diff 审查 + commit

### 何时跳过自动验证

- 项目没有任何测试或构建配置 → 只做 diff 审查
- 用户明确说"不要跑测试" → 跳过自动化验证
- 变更只涉及文档（.md 文件） → 只做 diff 审查 + commit

## 操作步骤

1. **检查工作区状态**:`git status` 确认有哪些变更。
2. **Stage 变更**:如果用户没有手动 stage,`git add` 相关文件。
3. **Diff 审查**:`git diff --staged` 检查变更内容,如有问题先报告再决定是否继续。
4. **自动化验证**:探测项目工具链并运行测试/构建/lint。记录结果。
5. **生成 commit message**:基于变更内容和项目约定生成 message。
6. **执行 commit**:`git commit -m "<message>"`。
7. **确认结果**:输出 commit hash 和变更摘要。
8. **处理推送**:如果用户说"提交并推送",额外执行 `git push`;如果用户说"不推送"或"本次不推送",明确确认。

## 配合的 agent

- `commit-gate-runner` agent:执行型 agent,负责跑质量门和提交。
- `verification-loop-runner` agent:如果质量门失败,可以联动 `harness-verification-loop` 进入修复循环。

## 相关模板

- `references/commit-message-guide.md`: Commit Message 格式指南

---
最后更新: 2026-06-29
