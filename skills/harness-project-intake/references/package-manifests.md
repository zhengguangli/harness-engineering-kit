<!-- 各语言包管理文件识别 — 由 project-analyzer agent 使用 -->
<!-- 根据文件存在性快速识别项目语言和包管理器 -->

## 识别优先级

按以下顺序检查，首次命中即确定主语言：

| 优先级 | 文件 | 语言/生态 | 包管理器 | 版本提取方式 |
|---|---|---|---|---|
| 1 | `package.json` | Node.js / TypeScript | npm / yarn / pnpm / bun | `node -v` 或 `engines.node` |
| 2 | `Cargo.toml` | Rust | cargo | `rustc --version` 或 `rust-version` |
| 3 | `go.mod` | Go | go modules | `go.mod` 中 `go` 指令 |
| 4 | `pyproject.toml` | Python | pip / poetry / uv / pdm | `python --version` 或 `requires-python` |
| 5 | `pom.xml` | Java | Maven | `<java.version>` 或 `<maven.compiler.source>` |
| 6 | `build.gradle` / `build.gradle.kts` | Java / Kotlin | Gradle | `sourceCompatibility` |
| 7 | `Gemfile` | Ruby | Bundler | `.ruby-version` 或 `ruby` 指令 |
| 8 | `composer.json` | PHP | Composer | `require.php` 版本约束 |
| 9 | `mix.exs` | Elixir | hex | `elixir` 版本约束 |
| 10 | `pubspec.yaml` | Dart / Flutter | pub | `environment.sdk` |
| 11 | `Package.swift` | Swift | Swift Package Manager | `swift-tools-version` |
| 12 | `*.csproj` / `*.sln` | C# / .NET | NuGet | `<TargetFramework>` |
| 13 | `stack.yaml` | Haskell | stack | `resolver` |

## 各语言详细提取规则

### Node.js / TypeScript

```bash
# 检查文件
ls package.json yarn.lock pnpm-lock.yaml bun.lockb 2>/dev/null

# 提取包管理器
if [ -f "pnpm-lock.yaml" ]; then echo "pnpm";
elif [ -f "yarn.lock" ]; then echo "yarn";
elif [ -f "bun.lockb" ]; then echo "bun";
else echo "npm"; fi

# 提取框架（从 package.json dependencies）
# Next.js: next
# React: react
# Vue: vue
# Nuxt: nuxt
# Express: express
# Fastify: fastify
# NestJS: @nestjs/core

# 提取运行时
# 浏览器: "browserslist"
# Node.js: "engines.node"
# Bun: "engines.bun"
# Deno: "deno.json"
```

### Python

```bash
# 检查文件
ls pyproject.toml setup.py setup.cfg requirements*.txt Pipfile poetry.lock 2>/dev/null

# 提取包管理器
if [ -f "poetry.lock" ]; then echo "poetry";
elif [ -f "uv.lock" ]; then echo "uv";
elif [ -f "Pipfile.lock" ]; then echo "pipenv";
elif [ -f "pdm.lock" ]; then echo "pdm";
else echo "pip"; fi

# 提取框架（从 pyproject.toml dependencies）
# Django: django
# FastAPI: fastapi
# Flask: flask
# SQLAlchemy: sqlalchemy
# Celery: celery
```

### Go

```bash
# 检查文件
ls go.mod go.sum 2>/dev/null

# 提取版本（从 go.mod 第一行）
head -1 go.mod  # module go 1.21

# 提取框架（从 go.mod require）
# Gin: github.com/gin-gonic/gin
# Echo: github.com/labstack/echo
# Fiber: github.com/gofiber/fiber
# gRPC: google.golang.org/grpc
```

### Rust

```bash
# 检查文件
ls Cargo.toml Cargo.lock 2>/dev/null

# 提取版本
grep '^edition' Cargo.toml  # edition = "2021"
grep '^rust-version' Cargo.toml  # rust-version = "1.70"

# 提取框架（从 Cargo.toml dependencies）
# Actix: actix-web
# Axum: axum
# Tokio: tokio
# Serde: serde
# Clap: clap
```

### Java / Kotlin

```bash
# 检查文件
ls pom.xml build.gradle build.gradle.kts 2>/dev/null

# Maven 项目
grep '<java.version>' pom.xml
grep '<spring-boot.version>' pom.xml

# Gradle 项目
grep 'sourceCompatibility' build.gradle
grep 'jvmTarget' build.gradle.kts

# 提取框架
# Spring Boot: org.springframework.boot
# Quarkus: io.quarkus
# Micronaut: io.micronaut
```

### PHP

```bash
# 检查文件
ls composer.json composer.lock 2>/dev/null

# 提取版本
cat composer.json | jq '.require.php'

# 提取框架（从 composer.json require）
# Laravel: laravel/framework
# Symfony: symfony/framework-bundle
# Slim: slim/slim
```

### Ruby

```bash
# 检查文件
ls Gemfile Gemfile.lock .ruby-version 2>/dev/null

# 提取版本
cat .ruby-version

# 提取框架（从 Gemfile）
# Rails: gem 'rails'
# Sinatra: gem 'sinatra'
```

### Dart / Flutter

```bash
# 检查文件
ls pubspec.yaml pubspec.lock 2>/dev/null

# 提取版本
grep 'sdk:' pubspec.yaml

# 提取框架
# Flutter: flutter
# Dart server: dart
```

### Swift

```bash
# 检查文件
ls Package.swift 2>/dev/null

# 提取版本
head -1 Package.swift  # swift-tools-version: 5.9
```

## 多语言项目处理

```bash
# 检查根目录和子目录
find . -maxdepth 2 -name "package.json" -o -name "go.mod" -o -name "Cargo.toml" -o -name "pyproject.toml" -o -name "pom.xml" -o -name "composer.json" -o -name "Gemfile" 2>/dev/null

# 识别 monorepo
# Node.js: packages/ 或 apps/ 目录 + package.json workspaces
# Go: 多个 go.mod 或 workspace 模式
# Java: 多模块 Maven/Gradle
```

## Fallback 规则

当所有已知包管理文件都不存在时：

```bash
# 按文件后缀推断
ls *.py 2>/dev/null && echo "Python"
ls *.go 2>/dev/null && echo "Go"
ls *.rs 2>/dev/null && echo "Rust"
ls *.java 2>/dev/null && echo "Java"
ls *.php 2>/dev/null && echo "PHP"
ls *.rb 2>/dev/null && echo "Ruby"
ls *.ts *.js 2>/dev/null && echo "Node.js"

# 在卡片中标注：推断（无包管理文件）
```
