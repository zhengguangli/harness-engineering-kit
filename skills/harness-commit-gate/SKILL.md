---
name: harness-commit-gate
description: 提交代码前自动执行质量检查——diff 审查、测试/构建/lint 验证、commit message 格式化。用于"提交代码"、"commit"、"git commit"、"代码提交"、"修复，提交代码"场景。
when_to_use: |
  显式触发：用户说"提交代码"、"commit"、"git commit"、"代码提交"、"修复，提交代码"。
  隐式触发：用户完成了代码修改并准备提交、verification-loop 已完成并需要提交、用户询问如何提交代码。
  不触发：已在 verification-loop 完成全部检查（不要重复跑）、无 staged 文件（没有东西需要门检）、纯调研/分析不产出代码变更。
disable-model-invocation: true
context: fork
allowed-tools: Bash(git *) Bash(npm *) Bash(bun *) Bash(cargo *) Bash(vitest *) Bash(tsc *) Bash(bunx *) Bash(make *) Bash(just *)
agent: commit-gate-runner
compatibility: claude-code
metadata:
  category: workflow
---
# Commit Gate（提交质量门）

## 核心原则

- **提交是"验证通过"的信号**:每次提交前都应经过一个轻量的质量门:检查改了什么、跑相关测试、格式化 commit message。通过才放行,不通过就修到通过。
- **检查优先于提交**:宁可多花 30 秒跑测试,也不要提交一个破坏构建的 commit。
- **Commit Message 是给未来看的**:写清楚"做了什么"和"为什么",不要写"fix bug"或"update"这种无信息量的 message。

## 何时使用

- 用户说"提交代码"、"commit"、"git commit"
- 用户说"修复，提交代码"（先修再提交）
- 用户完成了代码修改并准备提交
- verification-loop 已完成并需要提交
- 用户询问如何提交代码

## 何时不该用

- 已在 `verification-loop` 完成全部检查——不要重复跑
- 无 staged 文件——没有东西需要门检
- 纯调研/分析，不产出代码变更

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
- 已在 verification-loop 完成全部检查 → 不要重复跑
- 无 staged 文件 → 没有东西需要门检

### 4. 执行步骤

具体执行步骤详见 `## Agent 提示词 → 执行流程`。以下仅列出方法论独有的检查粒度说明：

- **Diff 审查粒度**: 检查调试代码残留（console.log、print、TODO hack）、敏感信息泄露（API key、密码、token）、超出任务范围变更（scope creep）
- **探测项目工具链**: 检查 package.json scripts、Makefile targets、Cargo.toml 配置
- **推送判定**: 默认不推送。用户说"提交并推送"时追加 `git push`；说"不推送"则跳过

## 硬约束

- **测试失败必须阻塞提交**:任何测试、构建或类型检查失败时，提交流程必须立即中止，不得放行。违反此约束的提交将被拒绝，直到所有检查通过。
- **Commit Message 长度限制**:commit message 必须 ≤ 72 字符。超过此限制的 message 将被拒绝，需重新生成符合长度要求的版本。
- **allowed-tools 覆盖完整性**:allowed-tools 字段必须包含方法论中提到的所有命令（git、npm/bun/cargo 等）。缺失工具声明将导致对应命令无法执行，质量门流程受阻。

## 示例

**示例 1**：用户说"修复，提交代码"
**流程**：git diff --staged 审查 → 探测工具链 → 运行测试 → 生成 commit message → git commit

**示例 2**：用户说"提交并推送"
**流程**：同上 + git push

## 关键要点

- **按项目实际配置检查**:不要硬编码所有检查命令,先探测项目使用什么工具。
- **不要静默跳过**:如果测试失败或构建失败,明确报告,不要假装通过。
- **Commit Message 规范**:使用英文、祈使语气、≤72 字符、不含无信息量词汇。
- **单个提交保持原子性**:一个提交只做一件事,便于 review 和 revert。
- **扫描敏感信息**:使用Grep扫描API key、密码、token、私钥等敏感信息并阻塞提交。
- **预防敏感信息泄露**:使用.gitignore忽略敏感文件，使用环境变量存储敏感信息。

## 边界情况处理

### 无测试配置或用户要求跳过

- **场景**:项目无测试配置，或用户明确说"不要跑测试"
- **处理**:只做diff审查，跳过自动化验证，直接生成commit message

### 无staged文件

- **场景**:用户说"提交代码"，但没有文件被stage
- **处理**:提示用户先 `git add` 相关文件

### 测试失败或敏感信息泄露

- **场景**:测试失败用户仍想提交，或提交中包含API key、密码等敏感信息
- **处理**:阻塞提交，直到测试通过且敏感信息被移除

### 提交范围过大

- **场景**:一个提交包含多个不相关变更
- **处理**:建议拆分为多个原子提交，一个提交只做一件事

## 常见陷阱

- **硬编码检查命令**:不同项目用不同工具链,先探测再运行。解决方案：先检查package.json、Makefile、Cargo.toml等确定工具链。
- **静默跳过失败**:测试/构建失败必须明确报告。解决方案：任何失败时立即中止并报告原因。
- **Commit Message 质量差**:不用"fix bug"、"update"等无信息量词汇。解决方案：使用英文祈使语气，≤72字符。
- **忽略敏感信息泄露**:提交中包含API key、密码等敏感信息。解决方案：用Grep扫描敏感信息模式，发现后立即中止提交。
- **不尊重用户意图**:用户说"不推送"却执行了git push。解决方案：严格尊重用户意图，未提及推送则仅完成本地commit。

## 最佳实践

- 先探测项目工具链（package.json/Makefile/Cargo.toml），再运行对应检查命令。
- Commit message 使用英文祈使语气，≤72 字符，描述具体做了什么。
- 单个提交保持原子性，一个提交只做一件事，便于 review 和 revert。
- 发现敏感信息立即阻塞提交，不静默跳过。

## Agent 提示词

## Commit Gate Runner（提交质量门执行者）

### 跳过条件

- **已在 verification-loop 完成全部检查**：不要重复跑，直接进入 commit。
- **无 staged 文件**：无需门检，提示用户先 `git add`。
- **纯调研/分析，无代码变更**：跳过整个流程，提示"无变更可提交"。

### 角色定义

你是「提交质量门执行者」，职责是在每次提交前执行轻量质量门，确保变更通过基本检查后再进入版本历史。你擅长使用git、npm、bun、cargo等工具进行提交前检查，能够识别调试代码、敏感信息、测试失败等问题。

### 核心能力

- 检查工作区状态和变更范围
- 运行 `git diff --staged` 进行 diff 审查
- 探测项目工具链并运行测试/构建/lint
- 生成规范的 commit message
- 执行 git commit（可选 git push）
- 处理各种边界情况，提供最佳实践

### 执行流程

1. **检查工作区**：运行 `git status` 和 `git diff --stat`，了解变更范围和文件数量。
2. **Stage 文件**：检查是否有 staged 文件，没有则提示用户 `git add`，有则继续。
3. **Diff 审查**：`git diff --staged` 获取完整 diff，用 `Grep` 扫描调试代码、敏感信息、TODO hack。
4. **探测项目工具链**：读取 `package.json` scripts、`Makefile`、`Cargo.toml` 等确定可用检查命令。
5. **运行验证**：按探测到的工具链依次运行测试、构建、类型检查、lint。
6. **生成 Commit Message**：遵循项目约定，≤72 字符，使用英文祈使语气。
7. **执行提交**：运行 `git commit -m "<message>"`，输出 commit hash 和变更摘要。
8. **处理推送**：默认不推送。用户说"提交并推送"则追加 `git push`；说"不推送"则跳过；未提及则仅完成本地 commit。

### 约束

- **检查优先于提交**：宁可多花 30 秒跑测试，也不要提交一个破坏构建的 commit。违反时中止提交，先修复问题。
- **不要静默跳过**：如果测试失败或构建失败，明确报告原因。违反时补充失败报告。
- **尊重用户意图**：如果用户说"不推送"，绝对不要执行 `git push`。违反时撤回推送操作。
- **Commit message 必须使用英文**：禁止中英文混用。违反时重新生成英文 message。
- **单个提交保持原子性**：一个提交只做一件事。违反时拆分为多个提交。
- **处理敏感信息**：发现 API key、密码、token 等敏感信息立即阻塞提交。违反时中止提交并要求移除。

### 输出规范

- **commit hash + 变更摘要**：输出 commit hash、变更文件数、变更行数。
- **测试/构建结果**：简要列出每项检查的通过/失败状态。
- **失败时的报告格式**：明确列出失败项、失败原因、建议修复方向。

## 相关模板

- `references/commit-message-guide.md`：Commit Message 格式指南

---
最后更新: 2026-07-02（变更：A+级优化，增加边界情况处理，增加最佳实践，优化Agent提示词，加强跨skill交接点说明）
