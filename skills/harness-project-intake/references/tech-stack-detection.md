<!-- Tech stack detection by language — used by project-analyzer agent -->
<!-- Extract framework, runtime, deployment target and other information from configuration files -->

## Detection Dimensions

Tech stack information is extracted across the following dimensions:

| Dimension | Data Source | Extraction Method |
|---|---|---|
| Language | Package manifest + file extensions | Pattern matching |
| Version | Package manifest + CLI commands | Regex extraction |
| Framework | Dependencies list | Keyword matching |
| Runtime | Configuration files + engines field | Regex extraction |
| Package Manager | Lock file | File existence |
| Deployment Target | Configuration files + CI config | Keyword matching |

## Framework Detection Rules

### Node.js / TypeScript Frameworks

| Framework | Detection Keyword | Source File |
|---|---|---|
| Next.js | `"next"` | `package.json` dependencies |
| Nuxt | `"nuxt"` | `package.json` dependencies |
| React | `"react"` | `package.json` dependencies |
| Vue | `"vue"` | `package.json` dependencies |
| Angular | `"@angular/core"` | `package.json` dependencies |
| Express | `"express"` | `package.json` dependencies |
| Fastify | `"fastify"` | `package.json` dependencies |
| NestJS | `"@nestjs/core"` | `package.json` dependencies |
| Hono | `"hono"` | `package.json` dependencies |
| Astro | `"astro"` | `package.json` dependencies |
| Remix | `"@remix-run/react"` | `package.json` dependencies |
| SvelteKit | `"@sveltejs/kit"` | `package.json` dependencies |

### Python Frameworks

| Framework | Detection Keyword | Source File |
|---|---|---|
| Django | `django` | `pyproject.toml` / `requirements.txt` |
| FastAPI | `fastapi` | `pyproject.toml` / `requirements.txt` |
| Flask | `flask` | `pyproject.toml` / `requirements.txt` |
| SQLAlchemy | `sqlalchemy` | `pyproject.toml` / `requirements.txt` |
| Celery | `celery` | `pyproject.toml` / `requirements.txt` |
| Tornado | `tornado` | `pyproject.toml` / `requirements.txt` |
| Starlette | `starlette` | `pyproject.toml` / `requirements.txt` |

### Go Frameworks

| Framework | Detection Keyword | Source File |
|---|---|---|
| Gin | `github.com/gin-gonic/gin` | `go.mod` |
| Echo | `github.com/labstack/echo` | `go.mod` |
| Fiber | `github.com/gofiber/fiber` | `go.mod` |
| Chi | `github.com/go-chi/chi` | `go.mod` |
| gRPC | `google.golang.org/grpc` | `go.mod` |
| GORM | `gorm.io/gorm` | `go.mod` |
| Ent | `entgo.io/ent` | `go.mod` |

### Rust Frameworks

| Framework | Detection Keyword | Source File |
|---|---|---|
| Actix | `actix-web` | `Cargo.toml` |
| Axum | `axum` | `Cargo.toml` |
| Tokio | `tokio` | `Cargo.toml` |
| Rocket | `rocket` | `Cargo.toml` |
| Warp | `warp` | `Cargo.toml` |
| Serde | `serde` | `Cargo.toml` |
| Clap | `clap` | `Cargo.toml` |

### Java Frameworks

| Framework | Detection Keyword | Source File |
|---|---|---|
| Spring Boot | `org.springframework.boot` | `pom.xml` / `build.gradle` |
| Quarkus | `io.quarkus` | `pom.xml` / `build.gradle` |
| Micronaut | `io.micronaut` | `pom.xml` / `build.gradle` |
| MyBatis | `org.mybatis` | `pom.xml` / `build.gradle` |
| Hibernate | `org.hibernate` | `pom.xml` / `build.gradle` |

### PHP Frameworks

| Framework | Detection Keyword | Source File |
|---|---|---|
| Laravel | `laravel/framework` | `composer.json` |
| Symfony | `symfony/framework-bundle` | `composer.json` |
| Slim | `slim/slim` | `composer.json` |
| Lumen | `laravel/lumen` | `composer.json` |

### Ruby Frameworks

| Framework | Detection Keyword | Source File |
|---|---|---|
| Rails | `rails` | `Gemfile` |
| Sinatra | `sinatra` | `Gemfile` |
| Hanami | `hanami` | `Gemfile` |

## Runtime Detection

| Runtime | Detection Method | Description |
|---|---|---|
| Node.js | `engines.node` in `package.json` | Server-side / full-stack |
| Bun | `engines.bun` in `package.json` or `bun.lockb` exists | Alternative runtime |
| Deno | `deno.json` exists | Alternative runtime |
| Browser | `browserslist` in `package.json` | Frontend |
| Python | `requires-python` in `pyproject.toml` | Server-side |
| JVM | `java.version` in `pom.xml` | Java/Kotlin |
| Go runtime | `go` directive in `go.mod` | Compiled |
| Rust native | `edition` in `Cargo.toml` | Compiled |

## Deployment Target Detection

| Deployment Target | Detection Keyword | Source File |
|---|---|---|
| Docker | `Dockerfile` / `docker-compose.yml` exists | Root directory |
| Vercel | `vercel.json` or `next.config.js` | Root directory |
| Netlify | `netlify.toml` | Root directory |
| Cloudflare Workers | `wrangler.toml` | Root directory |
| AWS Lambda | `serverless.yml` / `sam` configuration | Root directory |
| Kubernetes | `k8s/` / `kubernetes/` directory or Helm chart | Root directory |
| Fly.io | `fly.toml` | Root directory |
| Railway | `railway.toml` | Root directory |
| Render | `render.yaml` | Root directory |
| Heroku | `Procfile` | Root directory |
| GitHub Pages | `pages` keyword in `.github/workflows/` | CI configuration |
| Static | `static/` / `build/` output | Build configuration |

## CI/CD Detection

| CI/CD | Detection Keyword | Source File |
|---|---|---|
| GitHub Actions | `.github/workflows/` directory | Root directory |
| GitLab CI | `.gitlab-ci.yml` | Root directory |
| CircleCI | `.circleci/config.yml` | Root directory |
| Travis CI | `.travis.yml` | Root directory |
| Jenkins | `Jenkinsfile` | Root directory |
| Azure Pipelines | `azure-pipelines.yml` | Root directory |

## Database Detection

| Database | Detection Keyword | Source File |
|---|---|---|
| PostgreSQL | `postgresql` / `postgres` | Configuration files / docker-compose |
| MySQL | `mysql` | Configuration files / docker-compose |
| SQLite | `sqlite` / `.db` file | Configuration files |
| MongoDB | `mongodb` / `mongo` | Configuration files / docker-compose |
| Redis | `redis` | Configuration files / docker-compose |
| Elasticsearch | `elasticsearch` | Configuration files / docker-compose |

## Output Format

Tech stack information is output to the project card in the following format:

```markdown
### Tech Stack

| Dimension | Value |
|---|---|
| Language | TypeScript 5.3 |
| Framework | Next.js 14 (React 18) |
| Runtime | Node.js 20 |
| Package Manager | pnpm |
| Deployment Target | Vercel |
| Database | PostgreSQL 16 |
| CI/CD | GitHub Actions |
```
