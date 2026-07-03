# CI 集成指南

## 目的

将 commit-gate 的检查逻辑集成到项目的 CI 管道中，在 GitHub Actions / GitLab CI 等平台上自动运行质量门。

## 与本地 commit-gate 的分工

| 检查层次 | 本地 (commit-gate) | CI (推送后) |
|---------|------------------|-------------|
| diff 审查（调试代码/敏感信息） | ✅ 必须 | ✅ 复检 |
| 测试运行 | ✅ 必须 | ✅ 完整套件 |
| 类型检查 | ✅ 必须 | ✅ 必须 |
| Lint | ✅ 推荐 | ✅ 必须 |
| 构建 | ✅ 必须 | ✅ 必须 |
| 架构边界检查 | ❌ 非本 skill 职责 | ❌ 由 boundary-auditor 处理 |
| 集成测试 | ❌ 非本 skill 职责 | ✅ 完整集成 |

## GitHub Actions 示例

```yaml
# .github/workflows/commit-gate.yml
name: Commit Gate
on: [push, pull_request]

jobs:
  quality-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - run: npm ci

      # 步骤 1: 敏感信息扫描
      - name: Secret scan
        run: |
          ! grep -rE '(API_KEY|PASSWORD|SECRET|TOKEN|PRIVATE_KEY)' --include='*.{ts,js,py,go,rs}' . \
            | grep -v 'node_modules' | grep -v '.env.example'

      # 步骤 2: 测试
      - name: Tests
        run: npm test

      # 步骤 3: 类型检查
      - name: Type check
        run: npx tsc --noEmit

      # 步骤 4: Lint
      - name: Lint
        run: npm run lint

      # 步骤 5: 构建
      - name: Build
        run: npm run build
```

## 工具链配置指引

### Node.js/TypeScript
```
npm test        # 测试
npx tsc --noEmit  # 类型检查
npm run lint    # Lint
npm run build   # 构建
```

### Rust
```
cargo test      # 测试
cargo check     # 类型/借用检查
cargo fmt --check  # 格式检查
cargo build     # 构建
```

### Go
```
go test ./...       # 测试
go vet ./...        # 静态分析
golangci-lint run   # Lint
go build            # 构建
```

### Python
```
pytest              # 测试
mypy .              # 类型检查
ruff check .        # Lint
```
