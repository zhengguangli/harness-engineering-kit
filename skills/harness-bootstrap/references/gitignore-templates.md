<!-- .gitignore templates by tech stack — used by harness-bootstrapper agent -->
<!-- Select the corresponding template based on the project's tech stack and merge into .gitignore -->

## Common Rules (Required for All Projects)

```gitignore
# Auto-generated files (do not modify manually)
docs/generated/

# Editors and IDEs
.idea/
.vscode/
*.swp
*.swo
*~

# Operating system
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
# Binary files
*.exe
*.exe~
*.dll
*.so
*.dylib

# Test artifacts
*.test
*.out
*.prof

# Go workspace
go.work
go.work.sum

# Dependency directory
vendor/

# IDEs
.idea/
.vscode/

# Environment variables
.env
.env.*
!.env.example
```

## Rust

```gitignore
/target/
**/*.rs.bk
Cargo.lock

# IDEs
.idea/
.vscode/
*.swp

# Environment variables
.env
.env.*
!.env.example

# Test coverage report
tarpaulin-report.html
```

## Java / Kotlin

```gitignore
# Build artifacts
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

# IDEs
.idea/
*.iml
*.ipr
*.iws
.vscode/
.settings/
.classpath
.project
out/

# Environment variables
.env
.env.*
!.env.example

# Logs
*.log
```

## PHP

```gitignore
/vendor/
/composer.lock
.env
.env.*
!.env.example

# Framework-specific
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

# Dependency directory
node_modules/

# Environment variables
.env
.env.*
!.env.example

# IDEs
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

## Multi-stack Project

```gitignore
# Additional ignores for multi-stack projects
# Uncomment corresponding sections based on actual stacks used

# # Node.js
# node_modules/
# dist/

# # Python
# __pycache__/
# .venv/

# # Go
# vendor/
```

## Usage Guide

1. **Start with common rules**: All projects must include the Common Rules section
2. **Append by tech stack**: Add corresponding rules based on the project's actual tech stack
3. **Don't copy everything**: Only enable the sections actually used by the project
4. **docs/ must NOT be ignored**: `docs/` is the source knowledge directory and must never be completely ignored — only ignore `docs/generated/`
5. **Environment variable files**: `.env` files must be ignored, but keep `.env.example` templates
