<!-- CLAUDE.md examples by tech stack — used by harness-bootstrapper agent -->
<!-- Pick the closest example based on the actual project as a starting point -->

## Example 1: Node.js Full-Stack Project

```markdown
# CLAUDE.md

> This file is a map, not an encyclopedia. If you don't find the answer here, look for it in the corresponding `docs/` files below.

## What This Repository Is

A SaaS admin dashboard based on Next.js + Prisma, providing user management, data dashboards, and API gateway functionality.

## Hard Constraints (few, violations block merge)

- `prisma/schema.prisma` is the source of truth for the database schema, do not manually modify SQL
- API routes must be validated through Zod schemas, do not trust req.body directly
- `docs/` is the source knowledge directory, `.gitignore` must NOT ignore the entire `docs/`

## Where to Find More

| I want to know… | Go here |
|---|---|
| Overall architecture & API design | `docs/ARCHITECTURE.md` |
| Prisma schema & data model | `prisma/schema.prisma` |
| Environment variable configuration | `.env.example` |
| Component library & style conventions | `src/components/` |
| Quality score per module | `docs/QUALITY_SCORE.md` |

## Workflow Tips

- Use TypeScript strict mode, no `any`
- Run `npm run lint && npm run typecheck` before committing
- Use functional components, no class components
- Database changes must go through Prisma migrate

---
Last updated: <YYYY-MM-DD>
```

## Example 2: Python FastAPI Project

```markdown
# CLAUDE.md

> This file is a map, not an encyclopedia. If you don't find the answer here, look for it in the corresponding `docs/` files below.

## What This Repository Is

A FastAPI-based microservice handling order and payment flows, using PostgreSQL + Redis.

## Hard Constraints (few, violations block merge)

- All API endpoints must have Pydantic response models
- Database operations must go through SQLAlchemy sessions, no raw SQL
- Environment variables managed via pydantic-settings, no hardcoding

## Where to Find More

| I want to know… | Go here |
|---|---|
| Overall architecture & data flow | `docs/ARCHITECTURE.md` |
| API interface documentation | `docs/API_REFERENCE.md` |
| Database models | `app/models/` |
| Environment variable reference | `.env.example` |
| Quality score per module | `docs/QUALITY_SCORE.md` |

## Workflow Tips

- Python >=3.11, use type hints
- Tests with pytest, coverage >80%
- Run `ruff check . && mypy .` before committing
- Use `async def` consistently for async functions

---
Last updated: <YYYY-MM-DD>
```

## Example 3: Go Microservice

```markdown
# CLAUDE.md

> This file is a map, not an encyclopedia. If you don't find the answer here, look for it in the corresponding `docs/` files below.

## What This Repository Is

Go microservice providing dual gRPC + HTTP protocol access, handling user authentication and permission management.

## Hard Constraints (few, violations block merge)

- gRPC proto files are the source of truth for interface definitions; interface changes must start with proto changes
- All errors must be wrapped with `fmt.Errorf`, no bare returns
- `internal/` packages are not visible externally, `pkg/` is the public API

## Where to Find More

| I want to know… | Go here |
|---|---|
| Package structure & dependency direction | `docs/ARCHITECTURE.md` |
| Proto interface definitions | `proto/` |
| Configuration & environment variables | `config/` |
| Quality score per module | `docs/QUALITY_SCORE.md` |

## Workflow Tips

- Go >=1.21, follow `go fmt` + `go vet`
- Tests with `go test -race ./...`
- Run `golangci-lint run` before committing
- Error handling with `errors.Is/As`

---
Last updated: <YYYY-MM-DD>
```

## Example 4: Rust CLI Tool

```markdown
# CLAUDE.md

> This file is a map, not an encyclopedia. If you don't find the answer here, look for it in the corresponding `docs/` files below.

## What This Repository Is

Rust CLI tool for local configuration management and deployment automation.

## Hard Constraints (few, violations block merge)

- `unsafe` code must have `// SAFETY:` comments explaining the safety justification
- All public APIs must have doc comments `///`
- Dependency versions locked in `Cargo.lock`, no `cargo update` in CI

## Where to Find More

| I want to know… | Go here |
|---|---|
| Module structure & dependencies | `docs/ARCHITECTURE.md` |
| CLI argument definitions | `src/cli.rs` |
| Configuration file format | `docs/CONFIG_FORMAT.md` |
| Quality score per module | `docs/QUALITY_SCORE.md` |

## Workflow Tips

- Rust edition 2021, use clippy lint
- Tests with `cargo test`, cover critical paths
- Run `cargo clippy -- -D warnings && cargo fmt --check` before committing
- Error handling with `anyhow` or custom error types

---
Last updated: <YYYY-MM-DD>
```

## Example 5: Java Spring Boot Project

```markdown
# CLAUDE.md

> This file is a map, not an encyclopedia. If you don't find the answer here, look for it in the corresponding `docs/` files below.

## What This Repository Is

Spring Boot microservice providing REST APIs, integrating RabbitMQ message queue and Elasticsearch search.

## Hard Constraints (few, violations block merge)

- Controller layer must not directly access Repository, must go through Service
- All entities must use JPA annotations, no raw JDBC
- Configuration managed via `application.yml`, sensitive info through Vault

## Where to Find More

| I want to know… | Go here |
|---|---|
| Layered architecture & module division | `docs/ARCHITECTURE.md` |
| API interface documentation | Swagger UI `/swagger-ui.html` |
| Database migrations | `src/main/resources/db/migration/` |
| Quality score per module | `docs/QUALITY_SCORE.md` |

## Workflow Tips

- Java 17+, Spring Boot 3.x
- Tests with JUnit 5 + Mockito
- Run `./mvnw verify` before committing
- Code style with Google Java Format

---
Last updated: <YYYY-MM-DD>
```

## Selection Guide

1. **Find the closest example**: Choose the example that best matches your project's tech stack
2. **Adjust based on actual situation**: Modify the one-sentence description, hard constraints, and routing table
3. **Don't copy verbatim**: Examples are a starting point, not the final answer
4. **Keep it concise**: CLAUDE.md should only contain the routing table and hard constraints, don't let it bloat
