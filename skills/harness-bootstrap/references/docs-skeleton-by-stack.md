<!-- Docs/ skeleton templates by tech stack — used by harness-bootstrapper agent -->
<!-- Select the corresponding docs/ addition files based on the project's tech stack -->

## Common Skeleton (Required for All Projects)

See `references/docs-skeleton-template.md`.

The following are **additional recommended** docs/ files per tech stack.

## Node.js / TypeScript Project

```
docs/
├── ARCHITECTURE.md          # Project architecture
├── QUALITY_SCORE.md         # Quality score
├── API_REFERENCE.md         # API documentation (if the project exposes external APIs)
├── DEPLOYMENT.md            # Deployment guide
├── MIGRATION_GUIDE.md       # Database migration guide (if using ORM)
├── design-docs/
│   └── index.md             # Design decision index
└── exec-plans/
    ├── active/
    └── completed/
```

**ARCHITECTURE.md Skeleton Example**:

```markdown
# Architecture

## Overview

Project built on [Express/Fastify/NestJS], [one sentence describing the overall architecture].

## Domain Breakdown

| Domain | Responsibility | Entry File |
|---|---|---|
| <domain1> | <responsibility> | `<path>` |
| <domain2> | <responsibility> | `<path>` |

## Dependency Direction

[Describe module dependency relationships and constraints]

## Data Flow

[Describe request processing flow]

---
Last updated: <YYYY-MM-DD>
```

## Python Project

```
docs/
├── ARCHITECTURE.md
├── QUALITY_SCORE.md
├── API_REFERENCE.md         # FastAPI/Flask API documentation
├── DEPLOYMENT.md
├── ENVIRONMENT_SETUP.md     # Python environment setup guide
├── design-docs/
│   └── index.md
└── exec-plans/
    ├── active/
    └── completed/
```

**ARCHITECTURE.md Skeleton Example**:

```markdown
# Architecture

## Overview

Project built on [Django/FastAPI/Flask], [one sentence description].

## Domain Breakdown

| Domain | Responsibility | Package/Module |
|---|---|---|
| <domain1> | <responsibility> | `<package_path>` |
| <domain2> | <responsibility> | `<package_path>` |

## Dependency Direction

[Describe package dependency relationships]

## Database Design

[Describe ORM model relationships, if any]

---
Last updated: <YYYY-MM-DD>
```

## Go Project

```
docs/
├── ARCHITECTURE.md
├── QUALITY_SCORE.md
├── API_REFERENCE.md         # HTTP/gRPC interface documentation
├── DEPLOYMENT.md
├── PROTOBUF_GUIDE.md        # Proto file management (if using gRPC)
├── design-docs/
│   └── index.md
└── exec-plans/
    ├── active/
    └── completed/
```

**ARCHITECTURE.md Skeleton Example**:

```markdown
# Architecture

## Overview

Project built on [Gin/Echo/Standard library], [one sentence description].

## Package Structure

| Package | Responsibility | Dependencies |
|---|---|---|
| `cmd/` | Entry point | Internal packages |
| `internal/` | Business logic | `pkg/` |
| `pkg/` | Shared utilities | No external dependencies |

## Dependency Direction

`cmd/` → `internal/` → `pkg/`

## Concurrency Model

[Describe goroutine/channel usage patterns]

---
Last updated: <YYYY-MM-DD>
```

## Rust Project

```
docs/
├── ARCHITECTURE.md
├── QUALITY_SCORE.md
├── API_REFERENCE.md
├── DEPLOYMENT.md
├── SAFETY_NOTES.md          # unsafe usage records
├── design-docs/
│   └── index.md
└── exec-plans/
    ├── active/
    └── completed/
```

**ARCHITECTURE.md Skeleton Example**:

```markdown
# Architecture

## Overview

Project built on [Actix/Axum/Tokio], [one sentence description].

## Crate Structure

| Crate | Responsibility | Visibility |
|---|---|---|
| `src/main.rs` | Entry point | binary |
| `src/lib.rs` | Core library | public |
| `src/models/` | Data models | pub(crate) |

## Dependency Direction

[Describe crate dependencies]

## Memory Safety

[Describe unsafe code usage constraints]

---
Last updated: <YYYY-MM-DD>
```

## Java / Kotlin Project

```
docs/
├── ARCHITECTURE.md
├── QUALITY_SCORE.md
├── API_REFERENCE.md
├── DEPLOYMENT.md
├── DATABASE_MIGRATION.md     # Flyway/Liquibase migration guide
├── design-docs/
│   └── index.md
└── exec-plans/
    ├── active/
    └── completed/
```

**ARCHITECTURE.md Skeleton Example**:

```markdown
# Architecture

## Overview

Project built on [Spring Boot/Quarkus/Ktor], [one sentence description].

## Module Breakdown

| Module | Responsibility | Technology |
|---|---|---|
| `api/` | Interface layer | REST/gRPC |
| `service/` | Business layer | Spring Service |
| `repository/` | Data layer | JPA/MyBatis |

## Dependency Direction

`api/` → `service/` → `repository/`

## Layering Constraints

[Describe inter-layer communication rules]

---
Last updated: <YYYY-MM-DD>
```

## PHP Project

```
docs/
├── ARCHITECTURE.md
├── QUALITY_SCORE.md
├── API_REFERENCE.md
├── DEPLOYMENT.md
├── ARTISAN_COMMANDS.md       # Artisan command reference (Laravel)
├── design-docs/
│   └── index.md
└── exec-plans/
    ├── active/
    └── completed/
```

## Ruby Project

```
docs/
├── ARCHITECTURE.md
├── QUALITY_SCORE.md
├── API_REFERENCE.md
├── DEPLOYMENT.md
├── RAKE_TASKS.md             # Rake task reference
├── design-docs/
│   └── index.md
└── exec-plans/
    ├── active/
    └── completed/
```

## Selection Guide

1. **Start with the common skeleton**: All projects must include ARCHITECTURE.md and QUALITY_SCORE.md
2. **Append by tech stack**: Add corresponding files based on the project's actual tech stack
3. **Skip if unsure**: If unsure whether a file is needed, don't create it yet, leave a placeholder entry in the CLAUDE.md routing table
4. **Keep skeletons lean**: Write only the skeleton and "Last updated" date per file, don't fill in large amounts of empty content
