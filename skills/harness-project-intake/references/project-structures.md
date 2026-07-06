<!-- Project structure analysis by language — used by project-analyzer agent -->
<!-- Identify project type and architecture pattern based on directory layout -->

## Common Directory Patterns

| Directory/File | Meaning | Languages |
|---|---|---|
| `src/` | Source code directory | General |
| `lib/` | Library code directory | General |
| `test/` / `tests/` / `__tests__/` | Test directory | General |
| `docs/` | Documentation directory | General |
| `scripts/` | Scripts directory | General |
| `.github/` | GitHub Actions CI | General |
| `Dockerfile` / `docker-compose.yml` | Containerization | General |
| `Makefile` / `justfile` | Build scripts | General |
| `README.md` | Project description | General |

## Node.js / TypeScript

```
node-project/
├── src/                    # Source code
│   ├── index.ts            # Entry file
│   ├── routes/             # API routes (Express/Fastify)
│   ├── controllers/        # Controllers (NestJS)
│   ├── components/         # React components
│   ├── pages/              # Next.js pages
│   └── utils/              # Utility functions
├── public/                 # Static assets
├── prisma/                 # Prisma schema
├── migrations/             # Database migrations
├── package.json            # Package management
├── tsconfig.json           # TypeScript configuration
├── next.config.js          # Next.js configuration
├── vite.config.ts          # Vite configuration
├── .eslintrc.js            # ESLint configuration
└── jest.config.js          # Jest configuration
```

**Entry File Identification**:
- `src/index.ts` — General entry
- `src/main.ts` — NestJS entry
- `src/app.ts` — Express/Fastify entry
- `pages/_app.tsx` — Next.js App
- `app/layout.tsx` — Next.js App Router

## Python

```
python-project/
├── src/                    # Source code (or project-name/)
│   ├── __init__.py
│   ├── main.py             # Entry file
│   ├── models/             # Data models
│   ├── routes/             # API routes
│   ├── services/           # Business logic
│   ├── schemas/            # Pydantic schemas
│   └── utils/              # Utility functions
├── tests/                  # Tests
├── alembic/                # Database migrations (SQLAlchemy)
├── migrations/             # Database migrations (Django)
├── manage.py               # Django management script
├── pyproject.toml          # Project configuration
├── setup.py                # Traditional configuration
├── requirements.txt        # Dependencies list
├── Makefile                # Build scripts
└── Dockerfile              # Container configuration
```

**Entry File Identification**:
- `src/main.py` — FastAPI/Flask general entry
- `manage.py` — Django management script
- `app/main.py` — FastAPI common layout
- `wsgi.py` — WSGI entry (Django/Flask)
- `asgi.py` — ASGI entry (FastAPI)

## Go

```
go-project/
├── cmd/                    # Command entry
│   └── server/
│       └── main.go         # Main entry
├── internal/               # Private packages
│   ├── handler/            # HTTP handlers
│   ├── service/            # Business logic
│   ├── repository/         # Data access
│   ├── model/              # Data models
│   └── config/             # Configuration
├── pkg/                    # Public packages
├── api/                    # API definitions (proto/OpenAPI)
├── proto/                  # gRPC proto files
├── migrations/             # Database migrations
├── go.mod                  # Module definition
├── go.sum                  # Dependency checksums
├── Makefile                # Build scripts
├── Dockerfile              # Container configuration
└── .golangci.yml           # Lint configuration
```

**Entry File Identification**:
- `cmd/server/main.go` — Standard Go project entry
- `main.go` — Simple project entry
- `internal/handler/*.go` — HTTP handlers
- `internal/service/*.go` — Business logic

## Rust

```
rust-project/
├── src/
│   ├── main.rs             # Entry file (binary)
│   ├── lib.rs              # Library entry
│   ├── cli.rs              # CLI argument definitions
│   ├── models/             # Data models
│   ├── handlers/           # Request handlers
│   ├── services/           # Business logic
│   ├── errors.rs           # Error definitions
│   └── config.rs           # Configuration
├── tests/                  # Integration tests
├── benches/                # Performance benchmarks
├── examples/               # Example code
├── Cargo.toml              # Package management
├── Cargo.lock              # Dependency lock
├── clippy.toml             # Clippy configuration
├── rustfmt.toml            # Formatting configuration
└── Makefile                # Build scripts
```

**Entry File Identification**:
- `src/main.rs` — Binary entry
- `src/lib.rs` — Library entry
- `src/cli.rs` — CLI definition (clap)
- `src/handlers/*.rs` — HTTP handlers

## Java / Kotlin

```
java-project/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/
│   │   │       ├── Application.java    # Main entry
│   │   │       ├── controller/         # Controllers
│   │   │       ├── service/            # Business logic
│   │   │       ├── repository/         # Data access
│   │   │       ├── model/              # Data models
│   │   │       └── config/             # Configuration
│   │   └── resources/
│   │       ├── application.yml         # Configuration file
│   │       ├── db/migration/           # Database migrations
│   │       └── static/                 # Static resources
│   └── test/
│       └── java/
├── pom.xml                  # Maven configuration
├── build.gradle             # Gradle configuration
└── gradle/                  # Gradle wrapper
```

**Entry File Identification**:
- `Application.java` — Spring Boot main class
- `*Controller.java` — REST controllers
- `*Service.java` — Business logic
- `*Repository.java` — Data access

## PHP

```
php-project/
├── app/                    # Laravel application code
│   ├── Http/
│   │   └── Controllers/    # Controllers
│   ├── Models/             # Data models
│   └── Services/           # Business logic
├── routes/                 # Route definitions
├── database/
│   ├── migrations/         # Database migrations
│   └── seeders/            # Database seeders
├── public/                 # Public entry
│   └── index.php           # Entry file
├── config/                 # Configuration files
├── storage/                # Storage directory
├── tests/                  # Tests
├── composer.json           # Package management
├── artisan                 # Laravel CLI
├── .env.example            # Environment variable template
└── phpunit.xml             # Test configuration
```

**Entry File Identification**:
- `public/index.php` — Web entry
- `artisan` — CLI entry
- `routes/api.php` — API routes
- `app/Http/Controllers/*.php` — Controllers

## Ruby

```
ruby-project/
├── app/                    # Rails application code
│   ├── controllers/        # Controllers
│   ├── models/             # Data models
│   ├── views/              # Views
│   ├── services/           # Business logic
│   └── jobs/               # Background jobs
├── config/                 # Configuration files
├── db/
│   ├── migrate/            # Database migrations
│   └── seeds.rb            # Database seeders
├── lib/                    # Library code
├── spec/                   # RSpec tests
├── test/                   # Minitest tests
├── Gemfile                 # Dependencies
├── Rakefile                # Rake tasks
├── bin/rails               # Rails entry
└── config.ru               # Rack configuration
```

**Entry File Identification**:
- `bin/rails` — Rails CLI entry
- `config/routes.rb` — Route definitions
- `app/controllers/*.rb` — Controllers

## Dart / Flutter

```
dart-project/
├── lib/                    # Source code
│   ├── main.dart           # Entry file
│   ├── models/             # Data models
│   ├── screens/            # Screens
│   ├── widgets/            # Widgets
│   └── services/           # Business logic
├── test/                   # Tests
├── web/                    # Web platform
├── android/                # Android platform
├── ios/                    # iOS platform
├── pubspec.yaml            # Dependencies
└── analysis_options.yaml   # Lint configuration
```

## Project Type Identification

| Type | Characteristics | Common Tech Stacks |
|---|---|---|
| Web API | routes/ or controllers/ directory | Express, FastAPI, Gin, Spring |
| Full-Stack Web | pages/ or views/ + frontend framework | Next.js, Nuxt, Rails, Laravel |
| CLI Tool | cli.rs or argparse or cobra | Rust clap, Python click, Go cobra |
| Library | lib/ directory as main, no main entry | Various language library projects |
| Microservice | Independent deployment config + API definitions | gRPC, REST, message queue |
| Monorepo | Multiple package/module directories | Turborepo, Nx, Go workspace |
