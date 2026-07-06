<!-- Language package manifest identification — used by project-analyzer agent -->
<!-- Quickly identify project language and package manager based on file existence -->

## Identification Priority

Check in the following order, first match determines the primary language:

| Priority | File | Language/Ecosystem | Package Manager | Version Extraction Method |
|---|---|---|---|---|
| 1 | `package.json` | Node.js / TypeScript | npm / yarn / pnpm / bun | `node -v` or `engines.node` |
| 2 | `Cargo.toml` | Rust | cargo | `rustc --version` or `rust-version` |
| 3 | `go.mod` | Go | go modules | `go` directive in `go.mod` |
| 4 | `pyproject.toml` | Python | pip / poetry / uv / pdm | `python --version` or `requires-python` |
| 5 | `pom.xml` | Java | Maven | `<java.version>` or `<maven.compiler.source>` |
| 6 | `build.gradle` / `build.gradle.kts` | Java / Kotlin | Gradle | `sourceCompatibility` |
| 7 | `Gemfile` | Ruby | Bundler | `.ruby-version` or `ruby` directive |
| 8 | `composer.json` | PHP | Composer | `require.php` version constraint |
| 9 | `mix.exs` | Elixir | hex | `elixir` version constraint |
| 10 | `pubspec.yaml` | Dart / Flutter | pub | `environment.sdk` |
| 11 | `Package.swift` | Swift | Swift Package Manager | `swift-tools-version` |
| 12 | `*.csproj` / `*.sln` | C# / .NET | NuGet | `<TargetFramework>` |
| 13 | `stack.yaml` | Haskell | stack | `resolver` |

## Language-Specific Extraction Rules

### Node.js / TypeScript

```bash
# Check files
ls package.json yarn.lock pnpm-lock.yaml bun.lockb 2>/dev/null

# Extract package manager
if [ -f "pnpm-lock.yaml" ]; then echo "pnpm";
elif [ -f "yarn.lock" ]; then echo "yarn";
elif [ -f "bun.lockb" ]; then echo "bun";
else echo "npm"; fi

# Extract framework (from package.json dependencies)
# Next.js: next
# React: react
# Vue: vue
# Nuxt: nuxt
# Express: express
# Fastify: fastify
# NestJS: @nestjs/core

# Extract runtime
# Browser: "browserslist"
# Node.js: "engines.node"
# Bun: "engines.bun"
# Deno: "deno.json"
```

### Python

```bash
# Check files
ls pyproject.toml setup.py setup.cfg requirements*.txt Pipfile poetry.lock 2>/dev/null

# Extract package manager
if [ -f "poetry.lock" ]; then echo "poetry";
elif [ -f "uv.lock" ]; then echo "uv";
elif [ -f "Pipfile.lock" ]; then echo "pipenv";
elif [ -f "pdm.lock" ]; then echo "pdm";
else echo "pip"; fi

# Extract framework (from pyproject.toml dependencies)
# Django: django
# FastAPI: fastapi
# Flask: flask
# SQLAlchemy: sqlalchemy
# Celery: celery
```

### Go

```bash
# Check files
ls go.mod go.sum 2>/dev/null

# Extract version (from go.mod first line)
head -1 go.mod  # module go 1.21

# Extract framework (from go.mod require)
# Gin: github.com/gin-gonic/gin
# Echo: github.com/labstack/echo
# Fiber: github.com/gofiber/fiber
# gRPC: google.golang.org/grpc
```

### Rust

```bash
# Check files
ls Cargo.toml Cargo.lock 2>/dev/null

# Extract version
grep '^edition' Cargo.toml  # edition = "2021"
grep '^rust-version' Cargo.toml  # rust-version = "1.70"

# Extract framework (from Cargo.toml dependencies)
# Actix: actix-web
# Axum: axum
# Tokio: tokio
# Serde: serde
# Clap: clap
```

### Java / Kotlin

```bash
# Check files
ls pom.xml build.gradle build.gradle.kts 2>/dev/null

# Maven project
grep '<java.version>' pom.xml
grep '<spring-boot.version>' pom.xml

# Gradle project
grep 'sourceCompatibility' build.gradle
grep 'jvmTarget' build.gradle.kts

# Extract framework
# Spring Boot: org.springframework.boot
# Quarkus: io.quarkus
# Micronaut: io.micronaut
```

### PHP

```bash
# Check files
ls composer.json composer.lock 2>/dev/null

# Extract version
cat composer.json | jq '.require.php'

# Extract framework (from composer.json require)
# Laravel: laravel/framework
# Symfony: symfony/framework-bundle
# Slim: slim/slim
```

### Ruby

```bash
# Check files
ls Gemfile Gemfile.lock .ruby-version 2>/dev/null

# Extract version
cat .ruby-version

# Extract framework (from Gemfile)
# Rails: gem 'rails'
# Sinatra: gem 'sinatra'
```

### Dart / Flutter

```bash
# Check files
ls pubspec.yaml pubspec.lock 2>/dev/null

# Extract version
grep 'sdk:' pubspec.yaml

# Extract framework
# Flutter: flutter
# Dart server: dart
```

### Swift

```bash
# Check files
ls Package.swift 2>/dev/null

# Extract version
head -1 Package.swift  # swift-tools-version: 5.9
```

## Multi-Language Project Handling

```bash
# Check root and subdirectories
find . -maxdepth 2 -name "package.json" -o -name "go.mod" -o -name "Cargo.toml" -o -name "pyproject.toml" -o -name "pom.xml" -o -name "composer.json" -o -name "Gemfile" 2>/dev/null

# Identify monorepo
# Node.js: packages/ or apps/ directory + package.json workspaces
# Go: multiple go.mod or workspace mode
# Java: multi-module Maven/Gradle
```

## Fallback Rules

When no known package management files exist:

```bash
# Infer from file extensions
ls *.py 2>/dev/null && echo "Python"
ls *.go 2>/dev/null && echo "Go"
ls *.rs 2>/dev/null && echo "Rust"
ls *.java 2>/dev/null && echo "Java"
ls *.php 2>/dev/null && echo "PHP"
ls *.rb 2>/dev/null && echo "Ruby"
ls *.ts *.js 2>/dev/null && echo "Node.js"

# Note in card: Inferred (no package manifest files)
```
