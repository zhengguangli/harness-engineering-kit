<!-- 各技术栈初始化流程 — 由 harness-bootstrapper agent 使用 -->
<!-- 根据项目技术栈选用对应的初始化流程 -->

## 通用流程（所有项目适用）

1. 执行 `harness-project-intake` 分析项目
2. 与用户确认初始化范围
3. 生成 AGENTS.md（参考 `references/agents-md-examples.md`）
4. 生成 docs/ 骨架（参考 `references/docs-skeleton-template.md`）
5. 更新 .gitignore（参考 `references/gitignore-templates.md`）
6. 自检并输出修改清单

## Node.js / TypeScript 项目

### 额外初始化步骤

1. **检查 `package.json` scripts**：提取 `dev`、`test`、`build`、`lint` 命令填入 AGENTS.md
2. **检查 `tsconfig.json`**：了解 TypeScript 配置（strict 模式、路径别名）
3. **检查 `.eslintrc` / `prettier`**：了解代码风格配置
4. **检查 `next.config.js` / `vite.config.ts`**：了解构建框架配置

### .gitignore 补充

```gitignore
node_modules/
dist/
build/
.env
.env.local
.next/
.turbo/
```

### AGENTS.md 工作方式提示模板

```markdown
- 用 TypeScript strict 模式
- 提交前跑 `npm run lint && npm run typecheck`
- 组件用函数式写法
- 数据库变更走 ORM migration
```

## Python 项目

### 额外初始化步骤

1. **检查 `pyproject.toml`**：了解项目配置（Python 版本、依赖组）
2. **检查 `setup.py` / `setup.cfg`**：传统 Python 项目配置
3. **检查 `requirements*.txt`**：依赖列表
4. **检查 `Makefile` / `justfile`**：常用命令
5. **检查 `.flake8` / `ruff.toml`**：代码风格配置

### .gitignore 补充

```gitignore
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
.venv/
.env
*.egg-info/
htmlcov/
.coverage
```

### AGENTS.md 工作方式提示模板

```markdown
- Python >=3.11，使用 type hints
- 提交前跑 `ruff check . && mypy .`
- 测试用 pytest
- 虚拟环境用 venv 或 uv
```

## Go 项目

### 额外初始化步骤

1. **检查 `go.mod`**：了解 Go 版本和依赖
2. **检查 `Makefile`**：Go 项目常用 Make 管理构建
3. **检查 `.golangci.yml`**：lint 配置
4. **检查 `proto/` 目录**：如有 gRPC，了解 proto 文件结构

### .gitignore 补充

```gitignore
*.exe
*.dll
*.so
*.dylib
*.test
*.out
vendor/
.env
```

### AGENTS.md 工作方式提示模板

```markdown
- Go >=1.21，遵循 go fmt + go vet
- 提交前跑 `golangci-lint run`
- 错误处理用 errors.Is/As
- 命名遵循 Go conventions
```

## Rust 项目

### 额外初始化步骤

1. **检查 `Cargo.toml`**：了解 Rust 版本、依赖、features
2. **检查 `clippy.toml`**：clippy 配置
3. **检查 `rustfmt.toml`**：格式化配置
4. **检查 `src/` 结构**：了解模块划分

### .gitignore 补充

```gitignore
/target/
**/*.rs.bk
tarpaulin-report.html
```

### AGENTS.md 工作方式提示模板

```markdown
- Rust edition 2021
- 提交前跑 `cargo clippy -- -D warnings && cargo fmt --check`
- unsafe 必须有 SAFETY 注释
- 错误处理用 anyhow 或 thiserror
```

## Java / Kotlin 项目

### 额外初始化步骤

1. **检查 `pom.xml` / `build.gradle.kts`**：了解构建配置
2. **检查 Java 版本**：`java.version` 或 `sourceCompatibility`
3. **检查 Spring 配置**：`application.yml` / `application.properties`
4. **检查数据库迁移**：`Flyway` / `Liquibase` 配置

### .gitignore 补充

```gitignore
*.class
*.jar
.gradle/
target/
build/
.idea/
*.iml
.env
```

### AGENTS.md 工作方式提示模板

```markdown
- Java 17+，Spring Boot 3.x
- 提交前跑 `./mvnw verify` 或 `./gradlew check`
- 分层约束：Controller → Service → Repository
- 代码风格用 Google Java Format
```

## PHP 项目

### 额外初始化步骤

1. **检查 `composer.json`**：了解依赖和脚本
2. **检查框架**：Laravel / Symfony / Slim
3. **检查 `.env.example`**：环境变量模板
4. **检查 Artisan 命令**：如有 Laravel

### .gitignore 补充

```gitignore
/vendor/
composer.lock
.env
storage/*.key
/public/build
```

### AGENTS.md 工作方式提示模板

```markdown
- PHP >=8.1，使用 strict types
- 提交前跑 `composer cs && composer test`
- 数据库迁移用 Artisan migration
- 依赖管理用 Composer
```

## 选择指南

1. **先执行通用流程**：所有项目的通用步骤必须完成
2. **按技术栈追加**：根据项目实际使用的技术栈追加对应步骤
3. **不确定就跳过**：如果某个步骤不确定是否适用，先跳过
4. **输出修改清单**：初始化完成后列出所有创建/修改的文件
