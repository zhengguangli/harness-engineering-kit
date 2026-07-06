# CI Integration Guide

## Purpose

Integrate commit-gate check logic into the project's CI pipeline, running quality gates automatically on GitHub Actions / GitLab CI and similar platforms.

## Division of Labor with Local Commit Gate

| Check Level | Local (commit-gate) | CI (After Push) |
|---------|------------------|-------------|
| Diff review (debug code / sensitive info) | ✅ Required | ✅ Re-check |
| Test execution | ✅ Required | ✅ Full suite |
| Type check | ✅ Required | ✅ Required |
| Lint | ✅ Recommended | ✅ Required |
| Build | ✅ Required | ✅ Required |
| Architecture boundary check | ❌ Not this skill's responsibility | ❌ Handled by boundary-auditor |
| Integration tests | ❌ Not this skill's responsibility | ✅ Full integration |

## GitHub Actions Example

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

      # Step 1: Sensitive information scan
      - name: Secret scan
        run: |
          ! grep -rE '(API_KEY|PASSWORD|SECRET|TOKEN|PRIVATE_KEY)' --include='*.{ts,js,py,go,rs}' . \
            | grep -v 'node_modules' | grep -v '.env.example'

      # Step 2: Tests
      - name: Tests
        run: npm test

      # Step 3: Type check
      - name: Type check
        run: npx tsc --noEmit

      # Step 4: Lint
      - name: Lint
        run: npm run lint

      # Step 5: Build
      - name: Build
        run: npm run build
```

## Toolchain Configuration Guide

### Node.js/TypeScript
```
npm test        # Tests
npx tsc --noEmit  # Type check
npm run lint    # Lint
npm run build   # Build
```

### Rust
```
cargo test      # Tests
cargo check     # Type/borrow check
cargo fmt --check  # Format check
cargo build     # Build
```

### Go
```
go test ./...       # Tests
go vet ./...        # Static analysis
golangci-lint run   # Lint
go build            # Build
```

### Python
```
pytest              # Tests
mypy .              # Type check
ruff check .        # Lint
```
