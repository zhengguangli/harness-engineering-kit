# Commit Message 指南

## 格式选择

先检查项目的 git log 风格:

```bash
git log --oneline -10
```

如果项目使用 Conventional Commits:

```
type(scope): 用祈使句描述变更

可选的详细说明（为什么做这个变更）

可选的 BREAKING CHANGE 或 issue 引用
```

type 类型:
- `feat`: 新功能
- `fix`: 修复 bug
- `refactor`: 重构（不改变外部行为）
- `docs`: 仅文档变更
- `chore`: 构建/工具/依赖变更
- `test`: 添加或修改测试
- `style`: 代码格式调整（不影响逻辑）
- `perf`: 性能优化

如果项目不使用 Conventional Commits,用简洁的祈使句:

```
用一句话描述变更的核心内容
```

## 好的 Commit Message 示例

- `feat(auth): add API key validation with minimum length check`
- `fix(stream): handle empty delta in SSE translation`
- `refactor: split monolithic logger into modular structure`
- `docs: update README with new endpoint documentation`

## 差的 Commit Message 示例

- `fix bug` （修了什么 bug？）
- `update` （更新了什么？）
- `changes` （什么 changes？）
- `WIP` （不要提交 WIP 到主分支）

## 原则

- 说"做了什么",不要列文件名
- 用祈使语气（"add" 不是 "added"）
- 第一行不超过 72 个字符
- 如果需要更多上下文,在空行后写详细说明
