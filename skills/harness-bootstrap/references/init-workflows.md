<!-- Initialization workflows by tech stack — used by harness-bootstrapper agent -->
<!-- Select the corresponding initialization workflow based on the project's tech stack -->

## Common Workflow (Applies to All Projects)

1. Run `harness-project-intake` to analyze the project
2. Confirm the initialization scope with the user
3. Generate CLAUDE.md (see `references/claude-md-examples.md`)
4. Generate docs/ skeleton (see `references/docs-skeleton-template.md`)
5. Update .gitignore (see `references/gitignore-templates.md`)
6. Self-check and output the change list

## Node.js / TypeScript Project

### Additional Initialization Steps

1. **Check `package.json` scripts**: Extract `dev`, `test`, `build`, `lint` commands for CLAUDE.md
2. **Check `tsconfig.json`**: Understand TypeScript configuration (strict mode, path aliases)
3. **Check `.eslintrc` / `prettier`**: Understand code style configuration
4. **Check `next.config.js` / `vite.config.ts`**: Understand build framework configuration

### .gitignore Supplement

```gitignore
node_modules/
dist/
build/
.env
.env.local
.next/
.turbo/
```

### CLAUDE.md Workflow Tips Template

```markdown
- Use TypeScript strict mode
- Run `npm run lint && npm run typecheck` before committing
- Use functional components
- Database changes go through ORM migration
```

## Python Project

### Additional Initialization Steps

1. **Check `pyproject.toml`**: Understand project configuration (Python version, dependency groups)
2. **Check `setup.py` / `setup.cfg`**: Traditional Python project configuration
3. **Check `requirements*.txt`**: Dependency list
4. **Check `Makefile` / `justfile`**: Common commands
5. **Check `.flake8` / `ruff.toml`**: Code style configuration

### .gitignore Supplement

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

### CLAUDE.md Workflow Tips Template

```markdown
- Python >=3.11, use type hints
- Run `ruff check . && mypy .` before committing
- Tests with pytest
- Virtual environment with venv or uv
```

## Go Project

### Additional Initialization Steps

1. **Check `go.mod`**: Understand Go version and dependencies
2. **Check `Makefile`**: Go projects commonly use Make for build management
3. **Check `.golangci.yml`**: Lint configuration
4. **Check `proto/` directory**: If using gRPC, understand proto file structure

### .gitignore Supplement

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

### CLAUDE.md Workflow Tips Template

```markdown
- Go >=1.21, follow go fmt + go vet
- Run `golangci-lint run` before committing
- Error handling with errors.Is/As
- Naming follows Go conventions
```

## Rust Project

### Additional Initialization Steps

1. **Check `Cargo.toml`**: Understand Rust version, dependencies, features
2. **Check `clippy.toml`**: Clippy configuration
3. **Check `rustfmt.toml`**: Formatting configuration
4. **Check `src/` structure**: Understand module layout

### .gitignore Supplement

```gitignore
/target/
**/*.rs.bk
tarpaulin-report.html
```

### CLAUDE.md Workflow Tips Template

```markdown
- Rust edition 2021
- Run `cargo clippy -- -D warnings && cargo fmt --check` before committing
- unsafe must have SAFETY comments
- Error handling with anyhow or thiserror
```

## Java / Kotlin Project

### Additional Initialization Steps

1. **Check `pom.xml` / `build.gradle.kts`**: Understand build configuration
2. **Check Java version**: `java.version` or `sourceCompatibility`
3. **Check Spring configuration**: `application.yml` / `application.properties`
4. **Check database migration**: `Flyway` / `Liquibase` configuration

### .gitignore Supplement

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

### CLAUDE.md Workflow Tips Template

```markdown
- Java 17+, Spring Boot 3.x
- Run `./mvnw verify` or `./gradlew check` before committing
- Layered constraints: Controller → Service → Repository
- Code style with Google Java Format
```

## PHP Project

### Additional Initialization Steps

1. **Check `composer.json`**: Understand dependencies and scripts
2. **Check framework**: Laravel / Symfony / Slim
3. **Check `.env.example`**: Environment variable template
4. **Check Artisan commands**: If using Laravel

### .gitignore Supplement

```gitignore
/vendor/
composer.lock
.env
storage/*.key
/public/build
```

### CLAUDE.md Workflow Tips Template

```markdown
- PHP >=8.1, use strict types
- Run `composer cs && composer test` before committing
- Database migrations with Artisan migration
- Dependency management with Composer
```

## Selection Guide

1. **Start with the common workflow**: The common steps apply to all projects and must be completed
2. **Append by tech stack**: Add corresponding steps based on the project's actual tech stack
3. **Skip if unsure**: If unsure whether a step applies, skip it
4. **Output the change list**: After initialization, list all created/modified files
