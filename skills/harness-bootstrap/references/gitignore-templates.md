<!-- 各技术栈 .gitignore 模板 — 由 harness-bootstrapper agent 使用 -->
<!-- 根据项目技术栈选用对应的模板，合并到 .gitignore 中 -->

## 通用规则（所有项目必须包含）

```gitignore
# 自动生成的文件（不要手改）
docs/generated/

# 编辑器和 IDE
.idea/
.vscode/
*.swp
*.swo
*~

# 操作系统
.DS_Store
Thumbs.db
```

## Node.js / TypeScript

```gitignore
node_modules/
dist/
build/
.env
.env.*
!.env.example
*.tsbuildinfo
.turbo/
next-env.d.ts
.vercel/
```

## Python

```gitignore
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
*.egg
dist/
build/
.eggs/
*.whl
.pytest_cache/
.mypy_cache/
.ruff_cache/
.tox/
.nox/
.venv/
venv/
env/
.env
.env.*
!.env.example
htmlcov/
.coverage
.coverage.*
coverage.xml
*.cover
*.log
.ipynb_checkpoints/
```

## Go

```gitignore
# 二进制文件
*.exe
*.exe~
*.dll
*.so
*.dylib

# 测试产物
*.test
*.out
*.prof

# Go workspace
go.work
go.work.sum

# 依赖目录
vendor/

# IDE
.idea/
.vscode/

# 环境变量
.env
.env.*
!.env.example
```

## Rust

```gitignore
/target/
**/*.rs.bk
Cargo.lock

# IDE
.idea/
.vscode/
*.swp

# 环境变量
.env
.env.*
!.env.example

# 测
tarpaulin-report.html
```

## Java / Kotlin

```gitignore
# 编译产物
*.class
*.jar
*.war
*.ear

# Gradle
.gradle/
build/
!gradle/wrapper/gradle-wrapper.jar

# Maven
target/
!**/src/main/**/target/
!**/src/test/**/target/

# IDE
.idea/
*.iml
*.ipr
*.iws
.vscode/
.settings/
.classpath
.project
out/

# 环境变量
.env
.env.*
!.env.example

# 日志
*.log
```

## PHP

```gitignore
/vendor/
/composer.lock
.env
.env.*
!.env.example

# 框架特定
/storage/*.key
/public/hot
/public/storage
/public/build
/public/mix-manifest.json
/bootstrap/cache/

# Laravel
storage/debugbar/
storage/framework/cache/
storage/framework/sessions/
storage/framework/views/
storage/logs/

# Symfony
/var/
public/bundles/
```

## Ruby

```gitignore
*.gem
*.rbc
/.config
/coverage/
/InstalledFiles
/pkg/
/spec/reports/
/spec/examples.txt
/test/tmp/
/test/version_tmp/
/tmp/

# Bundler
/.bundle/
/vendor/bundle
/lib/bundle/

# 依赖目录
node_modules/

# 环境变量
.env
.env.*
!.env.example

# IDE
.idea/
.vscode/
*.swp
```

## C# / .NET

```gitignore
bin/
obj/
.vs/
*.user
*.suo
*.userosscache
*.sln.docstates
packages/
*.nupkg
project.lock.json
project.fragment.lock.json
artifacts/

# Rider
.idea/
*.sln.iml
```

## Dart / Flutter

```gitignore
.dart_tool/
.flutter-plugins
.flutter-plugins-dependencies
.packages
pubspec.lock
build/
.dart_tool/
.idea/
*.iml
pubspec.lock
*.log
```

## Elixir

```gitignore
_build/
deps/
*.ez
.elixir_ls/
```

## Multi-stack 项目

```gitignore
# 多技术栈项目额外忽略
# 根据实际启用的栈取消对应注释

# # Node.js
# node_modules/
# dist/

# # Python
# __pycache__/
# .venv/

# # Go
# vendor/
```

## 使用说明

1. **先用通用规则**：所有项目必须包含通用规则部分
2. **按技术栈追加**：根据项目实际使用的技术栈追加对应规则
3. **不要照搬全部**：只启用项目实际使用的部分
4. **docs/ 不能忽略**：`docs/` 是源知识目录，绝对不能整体忽略，只忽略 `docs/generated/`
5. **环境变量文件**：`.env` 文件必须忽略，但保留 `.env.example` 模板
